#!/usr/bin/env python
"""Run the PE defect benchmark against the reference validator.

For every entry enforced by a pe_lint property, materialize its defective and
repaired fixtures in a temporary directory and require that

  * the defective fixture produces the expected finding (severity + fragment),
  * the repaired fixture produces neither that finding nor any ERROR from the
    same check.

The second half is the benchmark's own non-vacuity: a check that refuses
everything would pass the first half. Entries enforced by nothing are counted
and listed as gaps; they are findings about the specification, not failures
of this run.

    python benchmark/defects/run.py [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import pe_lint  # noqa: E402

PASS = {"status": "pass", "artifact": "results/artifact.json"}
CHECKS = ("A1", "A2", "A3", "A4")


def _admissibility(spec):
    if spec == "_pass":
        return {k: dict(PASS) for k in CHECKS}
    if spec == "_all_na":
        return {k: {"status": "na", "reason": "fixture"} for k in CHECKS}
    if isinstance(spec, dict) and "_fail" in spec:
        blk = {k: dict(PASS) for k in CHECKS}
        blk[spec["_fail"]]["status"] = "fail"
        return blk
    return spec


def _write_native(root: str, claims: list[dict]) -> None:
    os.makedirs(os.path.join(root, "claims"))
    os.makedirs(os.path.join(root, "results"))
    with open(os.path.join(root, "results", "artifact.json"), "w") as fh:
        fh.write("{}\n")
    for c in claims:
        meta = c.get("edge_meta", {})
        uses = [({"id": t, **meta[t]} if t in meta else t)
                for t in c.get("uses", [])]
        obj = {"spec": "PE-CLS-1.0", "id": c["id"], "class": c["class"],
               "statement": f"benchmark fixture {c['id']}", "scope": "fixture",
               "retrospective": c.get("retrospective", False),
               "evidence": [], "status": "classified",
               "depends": {"uses": uses, "corroborates": [], "cites": []},
               "history": [{"date": "2026-09-01", "event": "created"}]}
        if "admissibility" in c:
            obj["admissibility"] = _admissibility(c["admissibility"])
        with open(os.path.join(root, "claims", c["id"] + ".json"), "w",
                  encoding="utf-8") as fh:
            json.dump(obj, fh, indent=1)


def _git(root: str, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", root, "-c", "user.name=bench", "-c",
         "user.email=bench@example.invalid", "-c", "commit.gpgsign=false",
         *args], capture_output=True, text=True, check=True).stdout.strip()


def _write_git(root: str, fx: dict) -> None:
    os.makedirs(os.path.join(root, "claims"))
    _git(root, "init", "-q")
    hashes = {}
    files = {"seal": ("prereg/r1.md", "prediction: r1 exceeds the bar\n"),
             "result": ("results/r1.json", "{\"r1\": 1}\n")}
    for step in fx["steps"]:
        rel, text = files[step]
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        with open(os.path.join(root, rel), "w") as fh:
            fh.write(text)
        _git(root, "add", rel)
        _git(root, "commit", "-q", "-m", step)
        hashes[step] = _git(root, "rev-parse", "--short", "HEAD")
    row = fx["row"].replace("{seal}", hashes.get("seal", "0000000"))
    with open(os.path.join(root, "claims", "REGISTRY-ACCOUNTING.md"), "w") as fh:
        fh.write("| id | registration | disposition |\n|---|---|---|\n" + row + "\n")


def _write_registry(root: str, toml_text: str) -> None:
    d = os.path.join(root, "claims", "transformations")
    os.makedirs(d)
    with open(os.path.join(d, "FX.toml"), "w", encoding="utf-8") as fh:
        fh.write(toml_text)


def findings_for(entry: dict, which: str) -> list:
    fx = entry["fixture"]
    with tempfile.TemporaryDirectory() as root:
        if fx["kind"] == "native":
            _write_native(root, fx[which])
            claims = pe_lint.parse_native_ledger(root)
            chk = entry["check"]
            if chk == "p5":
                return pe_lint.check_p5(root, claims)[0]
            if chk == "p4":
                return pe_lint.check_p4(claims)[0]
            if chk == "p1_retro":
                return pe_lint.check_p1_retro(claims)[0]
        elif fx["kind"] == "git":
            _write_git(root, fx[which])
            _claims, registry, _notes = pe_lint.parse_markdown_ledger(root)
            if entry["check"] == "p1":
                return pe_lint.check_p1(root, registry)[0]
            if entry["check"] == "p2":
                return pe_lint.check_p2(registry)[0]
        elif fx["kind"] == "registry":
            _write_registry(root, fx[which])
            regs, _notes = pe_lint.parse_registries(root)
            fn = {"d1": pe_lint.check_d1, "d2": pe_lint.check_d2,
                  "d3": pe_lint.check_d3, "d4": pe_lint.check_d4}[entry["check"]]
            return fn(regs)[0]
    raise ValueError(f"{entry['id']}: unsupported fixture/check "
                     f"{fx['kind']}/{entry['check']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    with open(os.path.join(HERE, "entries.json"), encoding="utf-8") as fh:
        bench = json.load(fh)

    rows, bad = [], 0
    for e in bench["entries"]:
        if e["origin"] == "external" and not e.get("check"):
            # Classified, not fixtured: the question for an external defect is
            # whether the specification can express it at all (K-1 falsifier).
            inexp = str(e.get("spec_gate", "none")).lower().startswith("none")
            rows.append({"id": e["id"], "origin": "external",
                         "result": "EXT-NONE" if inexp else "EXT-EXPR",
                         "title": e["title"], "spec_gate": e.get("spec_gate"),
                         "checkable": e.get("checkable")})
            continue
        if not e.get("check"):
            rows.append({"id": e["id"], "result": "GAP", "origin": e["origin"],
                         "title": e["title"], "would_need": e.get("would_need")})
            continue
        exp = e["expect"]
        d = findings_for(e, "defective")
        hit = any(f.severity == exp["severity"] and exp["contains"] in f.message
                  for f in d)
        r = findings_for(e, "repaired")
        clean = not any(exp["contains"] in f.message or f.severity == "ERROR"
                        for f in r)
        ok = hit and clean
        bad += not ok
        rows.append({"id": e["id"], "origin": e["origin"], "title": e["title"],
                     "result": "CAUGHT" if ok else "BROKEN",
                     "defective_fires": hit, "repaired_clean": clean,
                     **({} if ok else {"defective": [str(f) for f in d],
                                       "repaired": [str(f) for f in r]})})

    caught = sum(r["result"] == "CAUGHT" for r in rows)
    gaps = [r for r in rows if r["result"] == "GAP"]
    # Counted, never typed (DB-024): the K-1 tally comes from the entries.
    ext = [e for e in bench["entries"] if e["origin"] == "external"]
    expressible = [e for e in ext
                   if not str(e.get("spec_gate", "none")).lower().startswith("none")]
    summary = {"entries": len(rows), "caught": caught, "broken": bad,
               "gaps": len(gaps),
               "external": f"{len(ext)}/{bench['external']['target']}",
               # The K-1 falsifier: of the defects from outside the corpus, how
               # many can the specification express at all?
               "external_expressible": f"{len(expressible)}/{len(ext)}"}
    if args.json:
        print(json.dumps({"summary": summary, "rows": rows}, indent=1))
    else:
        for r in rows:
            print(f"  {r['result']:7s} {r['id']:7s} {r['title']}")
            for k in ("defective", "repaired"):
                for line in r.get(k, []):
                    print(f"            {k}: {line}")
        print(summary)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
