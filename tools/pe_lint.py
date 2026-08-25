#!/usr/bin/env python
"""pe_lint -- reference validator for PE-CLS-1.0 (the Claim Ledger Specification).

Checks the four properties a conforming claim ledger must demonstrate
mechanically, and computes blast radius for a retraction.

    P1  Priority     seal commit is a git ancestor of the result commit
    P2  Completeness identifier sequence gap-free, every ID dispositioned
    P3  Authority    no document cites a claim above its class
    P4  Coherence    dependencies resolve, graph acyclic, support-cap holds

Two front ends:

  * NATIVE ledgers -- directories of YAML/JSON claim objects per Appendix A.
  * MARKDOWN ledgers -- the reference deployment's format (a registry
    accounting table plus a claims table).  Parsed heuristically so the
    specification can be checked against a real programme that predates it.

Usage
-----
    pe_lint.py --ledger PATH [--level L1|L2|L3|L4] [--json]
    pe_lint.py --ledger PATH --blast-radius CLAIM_ID

Exit codes: 0 conforming at the requested level, 1 non-conforming, 2 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# claim classes (PE-CLS-1.0 section 4)
# --------------------------------------------------------------------------

CLASSES = {
    "proved":        {"support": 4, "priority": 3},
    "replicated":    {"support": 3, "priority": 2},
    "predicted":     {"support": 2, "priority": 3},
    "demonstrated":  {"support": 2, "priority": 2},
    "exploratory":   {"support": 0, "priority": 0},
    "refuted":       {"support": -1, "priority": -1},
    "withdrawn":     {"support": -1, "priority": -1},
    "suspended":     {"support": -1, "priority": -1},
    "void":          {"support": -1, "priority": -1},
}
TERMINAL = {"refuted", "withdrawn", "suspended", "void"}


def dominates(a: str, b: str) -> bool:
    """Partial order (section 4.1): a dominates b iff >= on BOTH axes."""
    if a not in CLASSES or b not in CLASSES:
        return False
    ca, cb = CLASSES[a], CLASSES[b]
    return ca["support"] >= cb["support"] and ca["priority"] >= cb["priority"]


@dataclass
class Claim:
    id: str
    statement: str = ""
    cls: str = "exploratory"
    scope: str = ""
    status: str = "classified"
    retrospective: bool = False
    uses: list[str] = field(default_factory=list)
    corroborates: list[str] = field(default_factory=list)
    cites: list[str] = field(default_factory=list)
    registration: str | None = None
    result: str | None = None
    seal_commit: str | None = None
    source: str = ""


@dataclass
class Finding:
    prop: str            # P1..P4
    severity: str        # ERROR | WARN | INFO
    claim: str
    message: str

    def __str__(self) -> str:
        return f"  [{self.severity:5s}] {self.prop} {self.claim}: {self.message}"


# --------------------------------------------------------------------------
# git helpers (P1)
# --------------------------------------------------------------------------

def _git(repo: str, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                             text=True, timeout=60)
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


def is_ancestor(repo: str, older: str, newer: str) -> bool | None:
    """True/False, or None if either commit is unknown to this repo."""
    for c in (older, newer):
        if _git(repo, "cat-file", "-e", f"{c}^{{commit}}") is None:
            return None
    try:
        r = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor",
                            older, newer], capture_output=True, timeout=60)
        return r.returncode == 0
    except Exception:
        return None


def first_commit_adding(repo: str, path: str) -> str | None:
    out = _git(repo, "log", "--diff-filter=A", "--format=%h", "--", path)
    return out.splitlines()[-1] if out else None


# --------------------------------------------------------------------------
# markdown front end (reference deployment)
# --------------------------------------------------------------------------

ID_IN_ROW = re.compile(r"^\|\s*\**\s*(\d{3})\s*\**\s*\|")
CLASS_TOKEN = re.compile(r"`\[(" + "|".join(CLASSES) + r")\]`|\[(" +
                         "|".join(CLASSES) + r")\]")
SEAL_HASH = re.compile(r"\b(?:sealed|seal)\s+`?([0-9a-f]{7,40})`?", re.I)
# A re-anchored row (PE-CLS-1.0 s7.1.1) records both the historical hash and
# the current commit identity. The current one is the checkable evidence.
CURRENT_HASH = re.compile(r"current commit\s+`?([0-9a-f]{7,40})`?", re.I)


def parse_markdown_ledger(root: str) -> tuple[dict[str, Claim], dict, list[str]]:
    """Parse a reference-deployment ledger. Returns (claims, registry, notes)."""
    notes: list[str] = []
    registry: dict[str, dict] = {}

    acct = os.path.join(root, "claims", "REGISTRY-ACCOUNTING.md")
    if os.path.isfile(acct):
        with open(acct, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = ID_IN_ROW.match(line)
                if not m:
                    continue
                rid = m.group(1)
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                disp = cells[2] if len(cells) > 2 else ""
                cur = CURRENT_HASH.search(line)
                seal = SEAL_HASH.search(line)
                registry[rid] = {
                    "disposition": disp,
                    "row": line.strip(),
                    "seal": (cur.group(1) if cur
                             else (seal.group(1) if seal else None)),
                    "reanchored": bool(cur),
                    "void": bool(re.search(r"never-run|void|reserved-unsealed",
                                           line, re.I)),
                }
    else:
        notes.append("no claims/REGISTRY-ACCOUNTING.md found -- P2 unavailable")

    claims: dict[str, Claim] = {}
    ledger = os.path.join(root, "claims", "LEDGER.md")
    if os.path.isfile(ledger):
        with open(ledger, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if not line.startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 3:
                    continue
                cid = cells[0].strip("* ")
                if not cid or cid.lower() in {"id", "---"} or set(cid) <= {"-"}:
                    continue
                blob = line
                cm = CLASS_TOKEN.search(blob)
                cls = (cm.group(1) or cm.group(2)) if cm else "exploratory"
                regs = re.findall(r"GO-P-2026-(\d{3})", blob)
                claims[cid] = Claim(
                    id=cid, cls=cls, statement=cells[1][:200],
                    registration=regs[0] if regs else None,
                    source="LEDGER.md",
                )
                if len(regs) > 1:
                    claims[cid].corroborates = [f"reg:{r}" for r in regs[1:]]
    else:
        notes.append("no claims/LEDGER.md found -- P3/P4 limited")

    return claims, registry, notes


# --------------------------------------------------------------------------
# native front end
# --------------------------------------------------------------------------

def parse_native_ledger(root: str) -> dict[str, Claim]:
    claims: dict[str, Claim] = {}
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            if not fn.endswith((".json", ".yaml", ".yml")):
                continue
            p = os.path.join(dirpath, fn)
            try:
                if fn.endswith(".json"):
                    with open(p, encoding="utf-8") as fh:
                        obj = json.load(fh)
                else:
                    try:
                        import yaml  # optional dependency
                    except ImportError:
                        continue
                    with open(p, encoding="utf-8") as fh:
                        obj = yaml.safe_load(fh)
            except Exception:
                continue
            # A native claim object must be unambiguous: either it carries the
            # spec marker, or it has the full required field set of section 3.1.
            if not isinstance(obj, dict):
                continue
            marked = str(obj.get("spec", "")).startswith("PE-CLS")
            complete = all(k in obj for k in
                           ("id", "class", "statement", "evidence", "depends"))
            if not (marked or complete):
                continue
            dep = obj.get("depends", {}) or {}
            claims[obj["id"]] = Claim(
                id=obj["id"], statement=obj.get("statement", ""),
                cls=obj.get("class", "exploratory"), scope=obj.get("scope", ""),
                status=obj.get("status", "classified"),
                retrospective=bool(obj.get("retrospective", False)),
                uses=list(dep.get("uses", []) or []),
                corroborates=list(dep.get("corroborates", []) or []),
                cites=list(dep.get("cites", []) or []),
                source=os.path.relpath(p, root),
            )
    return claims


# --------------------------------------------------------------------------
# the four properties
# --------------------------------------------------------------------------

def check_p2(registry: dict) -> tuple[list[Finding], dict]:
    """Completeness: contiguous IDs, every ID dispositioned."""
    out: list[Finding] = []
    if not registry:
        return out, {"checked": 0}
    ids = sorted(int(k) for k in registry)
    lo, hi = ids[0], ids[-1]
    present = set(ids)
    missing = [i for i in range(lo, hi + 1) if i not in present]
    for i in missing:
        out.append(Finding("P2", "ERROR", f"{i:03d}",
                           "identifier in range has NO disposition row "
                           "(file-drawer gap)"))
    undispositioned = [k for k, v in registry.items()
                       if not v["disposition"] or v["disposition"] in {"-", "—"}]
    for k in sorted(undispositioned):
        out.append(Finding("P2", "ERROR", k, "row present but disposition empty"))
    return out, {"checked": len(registry), "range": f"{lo:03d}-{hi:03d}",
                 "gaps": len(missing), "void": sum(1 for v in registry.values()
                                                   if v["void"])}


def check_p1(root: str, registry: dict) -> tuple[list[Finding], dict]:
    """Priority: seal commit is an ancestor of the result commit."""
    out: list[Finding] = []
    checked = ok = unknown = 0
    for rid in sorted(registry):
        entry = registry[rid]
        seal = entry.get("seal")
        if not seal or entry["void"]:
            continue
        m = re.search(r"([A-Za-z0-9_\-]+\.json)", entry["row"])
        if not m:
            continue
        result_rel = os.path.join("results", m.group(1))
        if not os.path.isfile(os.path.join(root, result_rel)):
            continue
        run = first_commit_adding(root, result_rel)
        if not run:
            continue
        checked += 1
        verdict = is_ancestor(root, seal, run)
        if verdict is None:
            unknown += 1
            out.append(Finding("P1", "WARN", rid,
                               f"seal {seal} or result commit unknown to repo"))
        elif verdict:
            ok += 1
        else:
            out.append(Finding("P1", "ERROR", rid,
                               f"seal {seal} is NOT an ancestor of result "
                               f"commit {run} -- priority unproven"))
    return out, {"checked": checked, "ancestor_ok": ok, "unknown": unknown}


def check_p4(claims: dict[str, Claim]) -> tuple[list[Finding], dict]:
    """Coherence: dependencies resolve, acyclic, support-cap holds."""
    out: list[Finding] = []
    for c in claims.values():
        for dep in c.uses + c.corroborates:
            if dep.startswith("reg:"):
                continue
            if dep not in claims:
                out.append(Finding("P4", "ERROR", c.id,
                                   f"dependency '{dep}' does not resolve"))
    # acyclicity over uses+corroborates
    colour: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> None:
        colour[node] = 1
        for nxt in claims[node].uses + claims[node].corroborates:
            if nxt.startswith("reg:") or nxt not in claims:
                continue
            if colour.get(nxt) == 1:
                cyc = " -> ".join(stack + [nxt])
                out.append(Finding("P4", "ERROR", node,
                                   f"dependency cycle: {cyc}"))
            elif colour.get(nxt, 0) == 0:
                visit(nxt, stack + [nxt])
        colour[node] = 2

    for cid in claims:
        if colour.get(cid, 0) == 0:
            visit(cid, [cid])
    # support cap
    capped = 0
    for c in claims.values():
        if c.cls in TERMINAL:
            continue
        for dep in c.uses:
            if dep not in claims:
                continue
            d = claims[dep]
            if d.cls in TERMINAL:
                out.append(Finding("P4", "ERROR", c.id,
                                   f"load-bearing dependency '{dep}' is "
                                   f"{d.cls}; claim must be suspended"))
            elif not dominates(d.cls, c.cls):
                capped += 1
                out.append(Finding("P4", "ERROR", c.id,
                                   f"class '{c.cls}' exceeds weakest "
                                   f"load-bearing dependency '{dep}' "
                                   f"({d.cls}) -- support-cap violation"))
    return out, {"claims": len(claims), "cap_violations": capped}


def check_p1_retro(claims: dict[str, Claim]) -> tuple[list[Finding], dict]:
    """Section 4.3: priority is not retroactively satisfiable.

    A retrospective claim (data seen before the claim was fixed) may never be
    `predicted`, and an empirical retrospective claim is capped at
    `exploratory` unless a separately-registered replication carries the
    stronger class.
    """
    out: list[Finding] = []
    retro = [c for c in claims.values() if c.retrospective]
    for c in retro:
        if c.cls == "predicted":
            out.append(Finding("P1", "ERROR", c.id,
                               "retrospective claim classed 'predicted' -- "
                               "priority cannot be reconstructed (s4.3)"))
        elif c.cls in {"demonstrated", "replicated"}:
            # legitimate only if a registered replication corroborates it
            backed = any(d in claims and not claims[d].retrospective
                         for d in c.corroborates)
            if not backed:
                out.append(Finding(
                    "P1", "ERROR", c.id,
                    f"retrospective empirical claim classed '{c.cls}' with no "
                    f"prospectively-registered corroboration -- cap is "
                    f"'exploratory' (s4.3)"))
    return out, {"retrospective": len(retro), "total": len(claims),
                 "retro_fraction": (round(len(retro) / len(claims), 3)
                                    if claims else 0.0)}


def check_p3(root: str, claims: dict[str, Claim],
             policy: set[str]) -> tuple[list[Finding], dict]:
    """Authority: prose must not cite a claim above the citing policy."""
    out: list[Finding] = []
    scanned = 0
    by_reg = {c.registration: c for c in claims.values() if c.registration}
    umbrella_files = []
    for cand in ("chapters/ch18_the_principle.md", "chapters/ch11_the_recognizer.md",
                 "OBSERVATION.md"):
        p = os.path.join(root, cand)
        if os.path.isfile(p):
            umbrella_files.append(p)
    for p in umbrella_files:
        scanned += 1
        with open(p, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for reg in re.findall(r"GO-P-2026-(\d{3})", text):
            c = by_reg.get(reg)
            if c and c.cls not in policy and c.cls not in TERMINAL:
                out.append(Finding(
                    "P3", "WARN", c.id,
                    f"{os.path.basename(p)} cites registration {reg} of class "
                    f"'{c.cls}', outside the declared citation policy "
                    f"{sorted(policy)}"))
    return out, {"documents_scanned": scanned}


def blast_radius(claims: dict[str, Claim], target: str) -> dict:
    """Transitive closure of load-bearing edges INTO target (section 8)."""
    uses_in: dict[str, list[str]] = {c: [] for c in claims}
    corr_in: dict[str, list[str]] = {c: [] for c in claims}
    for c in claims.values():
        for d in c.uses:
            if d in uses_in:
                uses_in[d].append(c.id)
        for d in c.corroborates:
            if d in corr_in:
                corr_in[d].append(c.id)
    if target not in claims:
        return {"error": f"claim '{target}' not in ledger"}
    suspended, seen = [], {target}
    stack = [target]
    while stack:
        node = stack.pop()
        for parent in uses_in.get(node, []):
            if parent not in seen:
                seen.add(parent)
                suspended.append(parent)
                stack.append(parent)
    recompute = sorted({p for n in seen for p in corr_in.get(n, [])
                        if p not in seen})
    untouched = sorted(set(claims) - seen - set(recompute))
    return {"target": target,
            "suspended": sorted(suspended),
            "recompute_support": recompute,
            "untouched_count": len(untouched),
            "untouched": untouched}


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

LEVEL_PROPS = {"L1": ["P2"], "L2": ["P2", "P1"],
               "L3": ["P2", "P1", "P4", "P3"], "L4": ["P2", "P1", "P4", "P3"]}


def main() -> int:
    ap = argparse.ArgumentParser(description="PE-CLS-1.0 ledger validator")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--level", default="L3", choices=list(LEVEL_PROPS))
    ap.add_argument("--blast-radius", metavar="CLAIM_ID")
    ap.add_argument("--policy", default="proved,replicated,predicted",
                    help="citation policy for P3")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.ledger)
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    native = parse_native_ledger(root)
    if native:
        claims, registry, notes = native, {}, ["native ledger format"]
    else:
        claims, registry, notes = parse_markdown_ledger(root)

    if args.blast_radius:
        report = blast_radius(claims, args.blast_radius)
        print(json.dumps(report, indent=2))
        return 0 if "error" not in report else 1

    findings: list[Finding] = []
    stats: dict[str, dict] = {}
    props = LEVEL_PROPS[args.level]
    if "P2" in props:
        f, s = check_p2(registry); findings += f; stats["P2"] = s
    if "P1" in props:
        f, s = check_p1(root, registry); findings += f; stats["P1"] = s
        fr, sr = check_p1_retro(claims)
        findings += fr
        stats["P1"] = {**s, **sr}
    if "P4" in props:
        f, s = check_p4(claims); findings += f; stats["P4"] = s
    if "P3" in props:
        f, s = check_p3(root, claims, set(args.policy.split(","))); findings += f
        stats["P3"] = s

    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]

    if args.json:
        print(json.dumps({
            "ledger": root, "level": args.level, "stats": stats,
            "notes": notes,
            "findings": [f.__dict__ for f in findings],
            "conforming": not errors,
        }, indent=2))
        return 0 if not errors else 1

    print("=" * 74)
    print(f"PE-CLS-1.0 conformance report -- level {args.level}")
    print(f"ledger: {root}")
    print("=" * 74)
    for n in notes:
        print(f"  note: {n}")
    print(f"  claims parsed: {len(claims)}   registry rows: {len(registry)}")
    print()
    for prop in props:
        s = stats.get(prop, {})
        pf = [f for f in findings if f.prop == prop]
        errs = sum(1 for f in pf if f.severity == "ERROR")
        label = {"P1": "Priority", "P2": "Completeness", "P3": "Authority",
                 "P4": "Coherence"}[prop]
        verdict = "PASS" if errs == 0 else f"FAIL ({errs})"
        print(f"  {prop} {label:13s} {verdict:12s} {s}")
        for f in pf[:12]:
            print(f)
        if len(pf) > 12:
            print(f"         ... and {len(pf) - 12} more")
    print()
    print("=" * 74)
    if errors:
        print(f"NON-CONFORMING at {args.level}: {len(errors)} error(s), "
              f"{len(warns)} warning(s)")
    else:
        print(f"CONFORMING at {args.level}"
              + (f" ({len(warns)} warning(s))" if warns else ""))
    print("=" * 74)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
