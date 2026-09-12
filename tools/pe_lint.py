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
    # s4.4: a stipulation asserts nothing about the world, so it can never cap
    # a claim that uses it. Ranked above everything for the support-cap check.
    "definition":    {"support": 99, "priority": 99},
    "refuted":       {"support": -1, "priority": -1},
    "withdrawn":     {"support": -1, "priority": -1},
    "suspended":     {"support": -1, "priority": -1},
    "void":          {"support": -1, "priority": -1},
    # PE-DSC-1.0 s5.2-5.3: two RECORD classes. They carry no evidence grade of
    # their own, so they rank with exploratory on both axes and can never lift
    # a claim that cites them. They are not terminal: a witness row records
    # what broke a claim, it does not retract the claim.
    "witness":       {"support": 0, "priority": 0},
    "revised":       {"support": 0, "priority": 0},
}
TERMINAL = {"refuted", "withdrawn", "suspended", "void"}
RECORD_CLASSES = {"witness", "revised"}


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
    result_commit: str | None = None
    seal_commit: str | None = None
    source: str = ""
    # s6.4: per-edge provenance, keyed (kind, target) -> {declared, entered,
    # declared_in}. Absent key means the edge was declared as a bare id and the
    # ledger does not know when it was declared.
    edge_prov: dict = field(default_factory=dict)


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
            prov: dict = {}

            def _edges(kind):
                # s6.4: an entry is a bare id, or an object carrying provenance.
                out = []
                for e in (dep.get(kind, []) or []):
                    if isinstance(e, dict):
                        tid = e.get("id")
                        if not tid:
                            continue
                        out.append(tid)
                        prov[(kind, tid)] = {
                            "declared": e.get("declared"),
                            "entered": e.get("entered"),
                            "declared_in": e.get("declared_in"),
                        }
                    else:
                        out.append(e)
                return out

            claims[obj["id"]] = Claim(
                id=obj["id"], statement=obj.get("statement", ""),
                cls=obj.get("class", "exploratory"), scope=obj.get("scope", ""),
                status=obj.get("status", "classified"),
                retrospective=bool(obj.get("retrospective", False)),
                uses=_edges("uses"),
                corroborates=_edges("corroborates"),
                cites=_edges("cites"),
                result_commit=obj.get("result_commit"),
                source=os.path.relpath(p, root),
                edge_prov=prov,
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



def classify_edge(meta: dict | None) -> str:
    """s6.4: prospective | backfilled | retrospective | unrecorded."""
    if not meta:
        return "unrecorded"
    declared = str(meta.get("declared") or "").strip()
    entered = str(meta.get("entered") or "").strip()
    di = meta.get("declared_in") or {}
    if not entered:
        return "prospective" if declared else "unrecorded"
    # entered => the row was written later than the declaration it reports
    named = all(str(di.get(k) or "").strip() for k in ("path", "hash", "commit"))
    return "backfilled" if named else "retrospective"


def check_p4(claims: dict[str, Claim], edges_expressible: bool = True,
             min_coverage: float | None = None) -> tuple[list[Finding], dict]:
    """Coherence: dependencies resolve, acyclic, support-cap holds, and the
    graph is non-vacuous (s9.1).

    The non-vacuity clause exists because every other check here passes
    perfectly on a ledger with no edges at all: nothing fails to resolve,
    nothing cycles, and no claim outranks a support it does not have. That is
    the same shape of defect the judgment arm rules out by pairing invariance
    with non-degeneracy, and it went unnoticed here until the checker was run
    against a deployment whose format cannot store edges.
    """
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
            elif c.cls == "definition" and d.cls != "definition":
                # s4.4(2): a stipulation cannot be weakened, but one that RESTS
                # on a substantive claim is a modeling axiom in disguise.
                out.append(Finding("P4", "WARN", c.id,
                                   f"definition depends on '{dep}' ({d.cls}), "
                                   f"a substantive claim -- may be a modeling "
                                   f"axiom in disguise (s4.4(2))"))
            elif not dominates(d.cls, c.cls):
                capped += 1
                out.append(Finding("P4", "ERROR", c.id,
                                   f"class '{c.cls}' exceeds weakest "
                                   f"load-bearing dependency '{dep}' "
                                   f"({d.cls}) -- support-cap violation"))

    # s6.4 edge provenance. Accounted over resolvable `uses` edges: those are
    # the edges blast radius traverses and the only ones an appraisal claim
    # rests on.
    kinds = {"prospective": 0, "backfilled": 0, "retrospective": 0,
             "unrecorded": 0}
    for c in claims.values():
        for dep in c.uses:
            if dep not in claims:
                continue
            meta = c.edge_prov.get(("uses", dep))
            kinds[classify_edge(meta)] += 1
            if not meta:
                continue
            declared = str(meta.get("declared") or "").strip()
            entered = str(meta.get("entered") or "").strip()
            di = meta.get("declared_in") or {}
            if entered and not all(str(di.get(k) or "").strip()
                                   for k in ("path", "hash", "commit")):
                out.append(Finding("P4", "ERROR", c.id,
                    f"edge -> '{dep}' is a backfill (entered {entered}) with no "
                    f"declared_in naming path, hash and commit -- an edge "
                    f"recorded after the fact must say where its declaration "
                    f"is, or it is a dependency written knowing the result "
                    f"(s6.4)"))
            elif entered and declared and declared > entered:
                out.append(Finding("P4", "ERROR", c.id,
                    f"edge -> '{dep}' declared {declared} but entered "
                    f"{entered} -- an edge cannot be entered before it was "
                    f"declared (s6.4)"))
            elif entered and not c.result_commit:
                out.append(Finding("P4", "INFO", c.id,
                    f"edge -> '{dep}' backfilled from {di.get('path')}; "
                    f"declaration asserted, ancestry not verified (no "
                    f"result_commit on this claim) (s6.4)"))

    # s9.1 non-vacuity. Counted over resolvable `uses` edges only: a
    # `corroborates` edge is support, not load, and carries nothing for blast
    # radius to traverse.
    edges = sum(1 for c in claims.values()
                for dep in c.uses if dep in claims)
    with_deps = sum(1 for c in claims.values()
                    if any(dep in claims for dep in c.uses))
    coverage = (with_deps / len(claims)) if claims else 0.0

    if not edges_expressible:
        out.append(Finding("P4", "ERROR", "(ledger)",
                           "this ledger's format has no field for dependency "
                           "edges, so P4 would be decided over an empty graph "
                           "and blast radius would be zero for every claim. "
                           "L3 and above require a format that can express "
                           "them (s9.1). Re-run at --level L2, or migrate to "
                           "native claim objects."))
    elif claims and edges == 0:
        out.append(Finding("P4", "ERROR", "(ledger)",
                           "dependency graph is empty: no claim declares a "
                           "load-bearing dependency on another. Every P4 check "
                           "passes vacuously and blast radius is zero "
                           "everywhere, so L3 certifies nothing (s9.1)."))
    elif min_coverage is not None and coverage < min_coverage:
        out.append(Finding("P4", "ERROR", "(ledger)",
                           f"edge coverage {coverage:.3f} is below the "
                           f"declared minimum {min_coverage:.3f} -- "
                           f"{with_deps} of {len(claims)} claims declare a "
                           f"dependency (s9.1)."))

    fixed = kinds["prospective"] + kinds["backfilled"]
    return out, {"claims": len(claims), "cap_violations": capped,
                 "uses_edges": edges, "claims_with_deps": with_deps,
                 "edge_coverage": round(coverage, 3),
                 "edge_provenance": kinds,
                 "prospective_fraction": round(fixed / edges, 3) if edges else 0.0}


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
    # s6.4: the same graph restricted to edges whose declaration is known to
    # predate the result. Only this subgraph supports a statement about what the
    # record fixed in advance; the full graph says what the programme believes
    # today.
    fixed_in: dict[str, list[str]] = {c: [] for c in claims}
    for c in claims.values():
        for d in c.uses:
            if d in uses_in:
                uses_in[d].append(c.id)
                if classify_edge(c.edge_prov.get(("uses", d))) in (
                        "prospective", "backfilled"):
                    fixed_in[d].append(c.id)
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

    pro, pseen = [], {target}
    pstack = [target]
    while pstack:
        node = pstack.pop()
        for parent in fixed_in.get(node, []):
            if parent not in pseen:
                pseen.add(parent)
                pro.append(parent)
                pstack.append(parent)

    return {"target": target,
            "suspended": sorted(suspended),
            "prospective_suspended": sorted(pro),
            "recompute_support": recompute,
            "untouched_count": len(untouched),
            "untouched": untouched}


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

LEVEL_PROPS = {"L1": ["P2"], "L2": ["P2", "P1"],
               "L3": ["P2", "P1", "P4", "P3"], "L4": ["P2", "P1", "P4", "P3"]}

# --------------------------------------------------------------------------
# discovery arm: transformation registries (PE-DSC-1.0)
# --------------------------------------------------------------------------

DSC_LEVEL_PROPS = {"D-L1": ["D1", "D4"],
                   "D-L2": ["D1", "D4", "D2"],
                   "D-L3": ["D1", "D4", "D2", "D3"]}

# PE-DSC-1.0 s3.4. Closed on purpose: a failure that absorbs into nothing on
# this list has been described rather than reduced.
ABSORBERS = {"representation", "metric", "constraint", "budget", "dynamics",
             "equivalence", "declaration", "measurement"}
OUTCOMES = {"survived", "failed", "boundary", "predicted", "proved"}
NEEDS_WITNESS = {"failed", "boundary"}
HEADER_FIELDS = ("x", "y", "equivalence", "complexity_ordering")


def parse_registries(root: str) -> tuple[dict[str, dict], list[str]]:
    """Parse every claims/transformations/*.toml under root."""
    import tomllib

    regs: dict[str, dict] = {}
    notes: list[str] = []
    tdir = os.path.join(root, "claims", "transformations")
    if not os.path.isdir(tdir):
        return regs, [f"no claims/transformations/ under {root}"]
    for name in sorted(os.listdir(tdir)):
        if not name.endswith(".toml"):
            continue
        path = os.path.join(tdir, name)
        try:
            with open(path, "rb") as fh:
                regs[name] = tomllib.load(fh)
        except Exception as exc:                       # malformed TOML is a finding,
            notes.append(f"{name}: unparsable ({exc})")  # not a crash
    return regs, notes


def check_d1(regs: dict[str, dict]) -> tuple[list[Finding], dict]:
    """D1 Declaration: every test names a family declared in the same registry,
    and every backfilled row says where its declaration actually is."""
    findings, tested, undeclared, backfilled = [], 0, 0, 0
    for name, reg in regs.items():
        declared = {t.get("id") for t in reg.get("transformation", [])}
        for fam in reg.get("transformation", []):
            entered = str(fam.get("entered") or "").strip()
            if not entered:
                continue
            # s3.2: a row written later than its declaration is a backfill. It
            # is admissible only if it names the sealed declaration it mirrors.
            backfilled += 1
            fid = fam.get("id", "(no id)")
            if not str(fam.get("declared_in") or "").strip():
                findings.append(Finding("D1", "ERROR", name,
                    f"'{fid}' is a backfill (entered {entered}) with no "
                    f"declared_in -- name the sealed registration that declared "
                    f"it, or the row is a family chosen to fit a result"))
            declared_on = str(fam.get("declared") or "").strip()
            if declared_on and declared_on > entered:
                findings.append(Finding("D1", "ERROR", name,
                    f"'{fid}' declared {declared_on} but entered {entered} -- "
                    f"a row cannot be entered before it was declared"))
            elif declared_on:
                findings.append(Finding("D1", "INFO", name,
                    f"'{fid}' backfilled: declared {declared_on}, "
                    f"entered {entered}"))
        for test in reg.get("test", []):
            tested += 1
            tid = test.get("transformation")
            if not tid:
                undeclared += 1
                findings.append(Finding("D1", "ERROR", name,
                    f"test '{_snip(test.get('claim'))}' names no transformation"))
            elif tid not in declared:
                undeclared += 1
                findings.append(Finding("D1", "ERROR", name,
                    f"test cites undeclared transformation '{tid}' -- a family "
                    f"entered after the result is a family chosen to fit it"))
    return findings, {"tests": tested, "undeclared": undeclared,
                      "backfilled": backfilled}


def check_d2(regs: dict[str, dict]) -> tuple[list[Finding], dict]:
    """D2 Reduction: failed and boundary tests carry a witness and an absorber."""
    findings, need, reduced = [], 0, 0
    for name, reg in regs.items():
        for test in reg.get("test", []):
            outcome = (test.get("outcome") or "").strip()
            if outcome and outcome not in OUTCOMES:
                findings.append(Finding("D2", "ERROR", name,
                    f"outcome '{outcome}' is not one of {sorted(OUTCOMES)}"))
            if outcome not in NEEDS_WITNESS:
                continue
            need += 1
            claim = _snip(test.get("claim"))
            if not (test.get("witness") or "").strip():
                findings.append(Finding("D2", "ERROR", name,
                    f"{outcome} test '{claim}' carries no witness -- record the "
                    f"reduction, or what stopped it"))
                continue
            absorber = (test.get("absorbed_by") or "").strip()
            if absorber not in ABSORBERS:
                findings.append(Finding("D2", "ERROR", name,
                    f"{outcome} test '{claim}' absorbed_by '{absorber}' is not "
                    f"in the closed list of s3.4"))
                continue
            reduced += 1
    return findings, {"failed_or_boundary": need, "reduced": reduced}


def check_d3(regs: dict[str, dict]) -> tuple[list[Finding], dict]:
    """D3 Revision: failed and boundary tests say what was revised, or that
    nothing was and why. Silence is the failure mode this catches."""
    findings, need, stated = [], 0, 0
    for name, reg in regs.items():
        for test in reg.get("test", []):
            if (test.get("outcome") or "").strip() not in NEEDS_WITNESS:
                continue
            need += 1
            rev = (test.get("revision") or "").strip()
            if not rev:
                findings.append(Finding("D3", "ERROR", name,
                    f"{_snip(test.get('claim'))}: no revision field -- cite the "
                    f"revised commitment, or state that none is registered and why"))
            elif rev.lower() in {"none", "n/a", "-"}:
                # A bare "none" satisfies nothing. s5.3 wants the reason.
                findings.append(Finding("D3", "WARN", name,
                    f"{_snip(test.get('claim'))}: revision is a bare '{rev}' "
                    f"with no reason given"))
                stated += 1
            else:
                stated += 1
    return findings, {"failed_or_boundary": need, "stated": stated}


def check_d4(regs: dict[str, dict]) -> tuple[list[Finding], dict]:
    """D4 Envelope: the header tuple is fixed, ranks exist, ids are unique."""
    findings, seen, nfam = [], {}, 0
    for name, reg in regs.items():
        header = reg.get("registry", {})
        for field_name in HEADER_FIELDS:
            if not (header.get(field_name) or "").strip():
                findings.append(Finding("D4", "ERROR", name,
                    f"registry header has no '{field_name}'" +
                    (" -- no minimality claim is possible without it"
                     if field_name == "complexity_ordering" else "")))
        for fam in reg.get("transformation", []):
            nfam += 1
            fid = fam.get("id")
            if not fid:
                findings.append(Finding("D4", "ERROR", name,
                                        "transformation has no id"))
                continue
            if fid in seen:
                findings.append(Finding("D4", "ERROR", name,
                    f"id '{fid}' already declared in {seen[fid]}"))
            seen[fid] = name
            if not isinstance(fam.get("rank"), int):
                findings.append(Finding("D4", "ERROR", name,
                    f"'{fid}' has no integer rank -- a witness cannot be "
                    f"minimal under an ordering the registry does not give"))
        ranks = [f.get("rank") for f in reg.get("transformation", [])]
        if ranks and all(r == 1 for r in ranks) and len(ranks) > 2:
            findings.append(Finding("D4", "WARN", name,
                f"all {len(ranks)} families are rank 1 -- s8, a registry whose "
                f"families are all simplest has declared no ordering"))
    return findings, {"registries": len(regs), "transformations": nfam,
                      "unique_ids": len(seen)}


def _snip(text: str | None, n: int = 52) -> str:
    text = " ".join((text or "(no claim)").split())
    return text if len(text) <= n else text[:n - 1] + "…"


def report_registries(root: str, level: str, as_json: bool) -> int:
    """The --registry front end. Mirrors the ledger report."""
    regs, notes = parse_registries(root)
    findings: list[Finding] = []
    stats: dict[str, dict] = {}
    props = DSC_LEVEL_PROPS[level]

    if not regs:
        findings.append(Finding(
            "D0", "ERROR", "(registry)",
            f"no transformation registries found under {root} -- refusing to "
            f"report conformance for an empty registry set."))
    runner = {"D1": check_d1, "D2": check_d2, "D3": check_d3, "D4": check_d4}
    for prop in props:
        f, s = runner[prop](regs)
        findings += f
        stats[prop] = s

    # predicted rows that never became anything else (s4)
    npred = sum(1 for r in regs.values() for t in r.get("test", [])
                if (t.get("outcome") or "").strip() == "predicted")
    if npred:
        notes.append(f"{npred} test(s) still 'predicted' (sealed and unrun)")

    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]

    if as_json:
        print(json.dumps({
            "root": root, "level": level, "stats": stats, "notes": notes,
            "findings": [f.__dict__ for f in findings],
            "conforming": not errors,
        }, indent=2))
        return 0 if not errors else 1

    print("=" * 74)
    print(f"PE-DSC-1.0 conformance report -- level {level}")
    print(f"registries: {root}")
    print("=" * 74)
    for n in notes:
        print(f"  note: {n}")
    print(f"  registries parsed: {len(regs)}   "
          f"tests: {sum(len(r.get('test', [])) for r in regs.values())}")
    print()
    labels = {"D1": "Declaration", "D2": "Reduction",
              "D3": "Revision", "D4": "Envelope"}
    for prop in props:
        pf = [f for f in findings if f.prop == prop]
        errs = sum(1 for f in pf if f.severity == "ERROR")
        verdict = f"FAIL ({errs})" if errs else "PASS"
        print(f"  {prop} {labels[prop]:13s} {verdict:12s} {stats.get(prop, {})}")
        for f in pf[:12]:
            print(f)
        if len(pf) > 12:
            print(f"         ... and {len(pf) - 12} more")
    for f in (f for f in findings if f.prop == "D0"):
        print(f)
    print()
    print("=" * 74)
    if errors:
        print(f"NON-CONFORMING at {level}: {len(errors)} error(s), "
              f"{len(warns)} warning(s)")
    else:
        print(f"CONFORMING at {level}"
              + (f" ({len(warns)} warning(s))" if warns else ""))
    print("=" * 74)
    return 0 if not errors else 1


DEFAULT_BASELINE = "CONFORMANCE-BASELINE.json"


def load_baseline(root: str, explicit: str | None) -> tuple[list[dict], str | None]:
    """Load acknowledged findings (PE-BRW-1.0 s5.6, the ratchet).

    A baseline records conformance failures that are REAL, KNOWN, and blocked on
    a decision only a named person can make. It never hides them: acknowledged
    findings are printed in full on every run and counted separately. It exists
    so that a brownfield ledger with inherited contradictions can still gate
    against NEW failures -- which is the whole value of a gate.
    """
    path = explicit or os.path.join(root, DEFAULT_BASELINE)
    if not os.path.isfile(path):
        if explicit:
            # A baseline named on the command line and silently ignored would
            # report a filtered verdict from an unfiltered run -- the exact
            # failure mode this tool exists to prevent.
            raise SystemExit(f"--baseline: no such file: {path}")
        return [], None
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("acknowledged", []), path


def apply_baseline(findings: list[Finding],
                   acked: list[dict]) -> tuple[list[Finding], list[Finding], list[Finding]]:
    """Split findings into (unacked, acknowledged, ratchet-violations).

    Matching is on the exact (prop, claim, message) triple. If a claim's class
    changes, its message changes and the entry STOPS matching -- so a baseline
    cannot silently cover a claim that has been promoted. That is the ratchet.
    """
    violations: list[Finding] = []
    index: dict[tuple[str, str, str], dict] = {}
    for e in acked:
        missing = [k for k in ("prop", "claim", "message", "owner",
                               "resolution_required") if not e.get(k)]
        if missing:
            violations.append(Finding(
                "BASE", "ERROR", e.get("claim", "?"),
                f"baseline entry missing required field(s) {missing} -- an "
                f"acknowledged failure must name who owes the decision and what "
                f"would resolve it, or it is laundering, not accounting"))
            continue
        index[(e["prop"], e["claim"], e["message"])] = e

    unacked, matched = [], set()
    for f in findings:
        key = (f.prop, f.claim, f.message)
        if f.severity == "ERROR" and key in index:
            matched.add(key)
        else:
            unacked.append(f)

    ack_findings = [
        Finding(k[0], "ACKED", k[1], index[k]["message"]) for k in sorted(matched)
    ]
    for key, e in index.items():
        if key not in matched:
            violations.append(Finding(
                "BASE", "ERROR", e["claim"],
                f"STALE baseline entry: this finding no longer fires. Either it "
                f"was resolved (remove the entry) or the claim changed shape "
                f"(re-examine it). A baseline may only shrink."))
    return unacked, ack_findings, violations


def main() -> int:
    ap = argparse.ArgumentParser(
        description="PE-CLS-1.0 ledger and PE-DSC-1.0 registry validator")
    ap.add_argument("--ledger")
    ap.add_argument("--registry", metavar="ROOT",
                    help="check transformation registries (PE-DSC-1.0) under "
                         "ROOT/claims/transformations/ instead of a ledger")
    ap.add_argument("--level", default="L3",
                    choices=list(LEVEL_PROPS) + list(DSC_LEVEL_PROPS))
    ap.add_argument("--blast-radius", metavar="CLAIM_ID")
    ap.add_argument("--min-edge-coverage", type=float, default=None,
                    metavar="FRAC",
                    help="s9.1: fail P4 unless at least FRAC of claims declare "
                         "a load-bearing dependency. Off by default; the "
                         "empty-graph refusal always applies.")
    ap.add_argument("--policy", default="proved,replicated,predicted",
                    help="citation policy for P3")
    ap.add_argument("--baseline", metavar="FILE",
                    help=f"acknowledged-findings file (default: "
                         f"<ledger>/{DEFAULT_BASELINE} if present)")
    ap.add_argument("--no-baseline", action="store_true",
                    help="ignore any baseline; report true unfiltered state")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if bool(args.ledger) == bool(args.registry):
        print("give exactly one of --ledger or --registry", file=sys.stderr)
        return 2

    if args.registry:
        root = os.path.abspath(args.registry)
        if not os.path.isdir(root):
            print(f"not a directory: {root}", file=sys.stderr)
            return 2
        level = args.level if args.level in DSC_LEVEL_PROPS else "D-L3"
        return report_registries(root, level, args.json)

    if args.level not in LEVEL_PROPS:
        print(f"--level {args.level} is a discovery-arm level; it needs "
              f"--registry, not --ledger", file=sys.stderr)
        return 2

    root = os.path.abspath(args.ledger)
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    native = parse_native_ledger(root)
    if native:
        claims, registry, notes = native, {}, ["native ledger format"]
        edges_expressible = True
    else:
        claims, registry, notes = parse_markdown_ledger(root)
        # The markdown front end recovers ids, classes, statements and
        # registrations. It has no field for `uses`, so a dependency graph
        # cannot be read out of it (s9.1).
        edges_expressible = False
        notes.append("markdown front end: dependency edges are not "
                     "expressible in this format; P4 non-vacuity fails by "
                     "construction above L2 (s9.1)")

    if args.blast_radius:
        report = blast_radius(claims, args.blast_radius)
        print(json.dumps(report, indent=2))
        return 0 if "error" not in report else 1

    findings: list[Finding] = []
    stats: dict[str, dict] = {}
    props = LEVEL_PROPS[args.level]

    if not claims and not registry:
        # A ledger with nothing in it passes every check vacuously. Reporting
        # that as CONFORMING lets a mistyped path go green in CI, which is
        # indistinguishable from a healthy ledger in the exit code.
        findings.append(Finding(
            "P0", "ERROR", "(ledger)",
            f"no claims and no registry rows found under {root} -- refusing to "
            f"report conformance for an empty ledger. Check the --ledger path."))
    if "P2" in props:
        f, s = check_p2(registry); findings += f; stats["P2"] = s
    if "P1" in props:
        f, s = check_p1(root, registry); findings += f; stats["P1"] = s
        fr, sr = check_p1_retro(claims)
        findings += fr
        stats["P1"] = {**s, **sr}
    if "P4" in props:
        f, s = check_p4(claims, edges_expressible=edges_expressible,
                        min_coverage=args.min_edge_coverage)
        findings += f; stats["P4"] = s
    if "P3" in props:
        f, s = check_p3(root, claims, set(args.policy.split(","))); findings += f
        stats["P3"] = s

    acked_entries, baseline_path = ([], None) if args.no_baseline else \
        load_baseline(root, args.baseline)
    ack_findings: list[Finding] = []
    if acked_entries or baseline_path:
        findings, ack_findings, ratchet = apply_baseline(findings, acked_entries)
        findings += ratchet
        notes.append(f"baseline: {baseline_path} "
                     f"({len(ack_findings)} acknowledged, still open)")

    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]

    if args.json:
        print(json.dumps({
            "ledger": root, "level": args.level, "stats": stats,
            "notes": notes,
            "findings": [f.__dict__ for f in findings],
            "acknowledged": [f.__dict__ for f in ack_findings],
            "conforming": not errors,
            "conforming_unfiltered": not errors and not ack_findings,
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
        nack = sum(1 for f in ack_findings if f.prop == prop)
        if errs:
            verdict = f"FAIL ({errs})"
        elif nack:
            verdict = f"PASS/{nack} ACKED"
        else:
            verdict = "PASS"
        print(f"  {prop} {label:13s} {verdict:12s} {s}")
        for f in pf[:12]:
            print(f)
        if len(pf) > 12:
            print(f"         ... and {len(pf) - 12} more")
    for f in (f for f in findings if f.prop == "P0"):
        print(f)

    base = [f for f in findings if f.prop == "BASE"]
    if base:
        print()
        print(f"  BASELINE INTEGRITY ({len(base)}) -- the acknowledged-findings "
              f"file is itself invalid:")
        for f in base:
            print(f)

    if ack_findings:
        print()
        print(f"  ACKNOWLEDGED ({len(ack_findings)}) -- real, open, and blocked "
              f"on a named decision. Acknowledging is not resolving.")
        for f in ack_findings:
            print(f)

    print()
    print("=" * 74)
    if errors:
        print(f"NON-CONFORMING at {args.level}: {len(errors)} error(s), "
              f"{len(warns)} warning(s)")
    elif ack_findings:
        print(f"CONFORMING at {args.level} AGAINST BASELINE: "
              f"0 new error(s), {len(ack_findings)} acknowledged, "
              f"{len(warns)} warning(s)")
        print(f"  NOT unconditionally conforming. Run --no-baseline for the "
              f"unfiltered state.")
    else:
        print(f"CONFORMING at {args.level}"
              + (f" ({len(warns)} warning(s))" if warns else ""))
    print("=" * 74)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
