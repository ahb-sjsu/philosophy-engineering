# -*- coding: utf-8 -*-
"""Brownfield conversion of the observation ledger to native claim objects.

PE-BRW-1.0: descriptive first. No statement is edited, no claim re-derived,
nothing deleted. The markdown ledger stays where it is and remains the source.

Dependency edges are DECLARED RETROSPECTIVELY and every object says so. The
edges below were generated mechanically as candidates (mentions of one claim id
inside another claim's row) and then adjudicated one at a time against the
sentence that produced them; the sentence is recorded on each edge as evidence.
Type adjudication is not automated, because s6.1 is explicit that a checker
cannot tell a load-bearing edge from a contextual one.
"""
import io, json, os, re, sys

SRC = r"C:\source\geometric-observation"
OUT = os.path.join(SRC, "ledger", "claims")
TODAY = "2026-09-12"

# --- id normalisation: the markdown id cell carries prose ------------------
RENAME = {
    "GO-2 (neg. half: **not** reconstruction)": "GO-2-NEG",
    "GO-2 (pos. half: consumer-projected covariance *controls*)": "GO-2-POS",
    "GO-2/GO-12/GO-13 operational (KV serving, 077)": "GO-OP-077",
    "NEG-16** (KV serving, end-task)": "NEG-16",
    "NEG-15** (Bell boundary)": "NEG-15",
    "NEG-13 \u2192 **resolved": "NEG-13",
}
DROP = {"Incident"}          # a table header, not a claim

def norm(cid):
    if cid in RENAME:
        return RENAME[cid]
    return re.sub(r"\s*\(.*$", "", cid).strip().rstrip("*").strip()

# --- class tokens the markdown uses that the spec does not -----------------
CLASS_FIXUP = {"refuted-as-sealed": "refuted"}

CLASSES = ("proved replicated predicted demonstrated exploratory definition "
           "refuted withdrawn suspended void witness revised").split()
CLASS_RE = re.compile(r"`?\[((?:refuted-as-sealed)|" + "|".join(CLASSES) + r")\]`?")

# --- adjudicated edges: (source, target, type, the sentence that shows it) --
EDGES = [
 ("OT-10","OT-3","uses","the cliff whose location OT-10 claims never moves is OT-3's object; the sub-bar contradicts OT-3's committed affinities"),
 ("OT-9","OT-2","uses","'Forward transfer of readings across measures via the OT-2 law'"),
 ("GO-2-POS","NEG-10","cites","'Regime bound = NEG-10 (needs recon-matched arms)'"),
 ("GO-2-POS","NEG-5","cites","'Priors: NEG-5...10'"),
 ("GO-5","NEG-11","cites","'Per sealed prereg, a miss -> refuted -> NEG-11' (its own refutation record)"),
 ("GO-7","VI-8","cites","'R-IND-5 pass = VI-8' (independent verification incident)"),
 ("GO-9","GO-8","cites","'Same caveat as GO-8 -- 054's verdict rests on the same post-hoc control-statistic bug fix'"),
 ("GO-10","VI-10","cites","'incl. the VI-10 obtuse regression' (verification incident)"),
 ("GO-10","GO-9","corroborates","'the strong side matches GO-9's 0.56x'"),
 ("GO-11","GO-10","corroborates","'a nine-parameter matrix program from which the GO-10 tax-gap formula is derived'"),
 ("GO-12","GO-11","uses","'with time-local slice access the tax is GO-11's static quadratic with the substitution set by the encoder's access'"),
 ("GO-12","GO-8","corroborates","\"GO-8's age-dependence is the slice regime's operational face\""),
 ("GO-OP-077","GO-2-POS","uses","the row is the operational measurement of GO-2/GO-12/GO-13"),
 ("GO-OP-077","GO-12","uses","the row is the operational measurement of GO-2/GO-12/GO-13"),
 ("GO-OP-077","GO-13","uses","the row is the operational measurement of GO-2/GO-12/GO-13"),
 ("NEG-16","GO-2-POS","cites","'Honest Negatives . operational GO-2'"),
 ("NEG-5","GO-2-POS","cites","'refutes the *test*, not GO-2' -- the row disclaims the dependency explicitly"),
 ("NEG-7","GO-1","cites","'a direct GO-1 instance'"),
 ("NEG-7","GO-2-POS","cites","\"the sharpest form of GO-2's negative half\""),
 ("NEG-11","GO-5","cites","'(GO-5, prospective x4)' -- the refutation record of GO-5"),
 ("NEG-12","NEG-10","cites","'Precondition (as in NEG-10)'"),
 ("GO-B-Llama","NEG-12","cites","'Bounds the theory to synthetic consumers on this evidence -> NEG-12'"),
 ("GO-B-Llama-rematch","NEG-12","cites","'Fixes the NEG-12 flaw: the two key-error arms are recon-matched by construction'"),
 ("GO-B-legal","GO-1","uses","'replace the estimated read op with the GO-1 blind-probe margin-sensitivity'"),
 ("GO-B-whale","GO-1","uses","'GO-1 blind margin read op (top-r=4)'"),
 ("VI-14","VI-15","cites","'sealing-commit timeline verified by the DR-3 pass (VI-15), not this one'"),
 ("GO-EC-7","VI-13","cites","'The v3 analytic instrument is independently verified -- VI-13 above'"),
]

# --- read the markdown rows ------------------------------------------------
lines = io.open(os.path.join(SRC, "claims", "LEDGER.md"),
                encoding="utf-8").read().split("\n")
rows, fixups = {}, []
for line in lines:
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 3:
        continue
    raw = cells[0].strip("* ")
    if not raw or raw.lower() in {"id", "---"} or set(raw) <= {"-"} or raw in DROP:
        continue
    if not re.match(r"^(OT|GO|NEG|VI)\b", raw):
        continue
    cid = norm(raw)
    m = CLASS_RE.search(line)
    token = m.group(1) if m else None
    cls = CLASS_FIXUP.get(token, token) or "exploratory"
    if token in CLASS_FIXUP:
        fixups.append((cid, token, cls))
    # A claim is prospective iff its row names a sealed registration. The
    # `retrospective` flag is about the CLAIM's priority, not about when its
    # dependency edges were declared -- those are retrospective for every row
    # here and are marked as such in history and edge_provenance.
    # The ledger uses more than one registration-naming scheme. GO-P-2026-NNN
    # preregs, and the crucible's PREREG-OT*.md appendices. A detector keyed to
    # one scheme reports the other family as unregistered, which is a defect in
    # the reader and not in the programme.
    regs = re.findall(r"GO-P-2026-(\d{3})", line)
    if not regs:
        pre = re.findall(r"\]\((\.\./[^)]*[Pp][Rr][Ee][Rr][Ee][Gg][^)]*)\)", line)
        regs = [os.path.basename(pre[0]).replace(".md", "")] if pre else []
    rows[cid] = {"raw_id": raw, "statement": cells[1][:400], "class": cls,
                 "token": token, "registration": regs[0] if regs else None,
                 "retrospective": not regs}

# --- attach edges ----------------------------------------------------------
dep = {cid: {"uses": [], "corroborates": [], "cites": []} for cid in rows}
prov, unresolved = {}, []
for src, dst, kind, why in EDGES:
    if src not in rows or dst not in rows:
        unresolved.append((src, dst, kind))
        continue
    dep[src][kind].append(dst)
    prov.setdefault(src, []).append({"target": dst, "type": kind, "evidence": why})

os.makedirs(OUT, exist_ok=True)
for cid, r in rows.items():
    obj = {
        "spec": "PE-CLS-1.0",
        "id": cid,
        "statement": r["statement"],
        "class": r["class"],
        "scope": f"geometric-observation claims/LEDGER.md; ledger label: {r['raw_id']}",
        "retrospective": r["retrospective"],
        "evidence": [{"source": "claims/LEDGER.md", "ledger_class_token": r["token"],
                      "registration": (f"GO-P-2026-{r['registration']}"
                                       if r["registration"] else None),
                      "kind": "ledger row"}],
        "depends": dep[cid],
        "status": "classified",
        "history": [{"date": TODAY,
                     "event": "brownfield conversion of the markdown ledger to native "
                              "claim objects (PE-BRW-1.0 s5.1-5.2). Dependency edges "
                              "declared retrospectively; see edge_provenance."}],
    }
    if cid in prov:
        obj["edge_provenance"] = prov[cid]
    io.open(os.path.join(OUT, cid + ".json"), "w", encoding="utf-8").write(
        json.dumps(obj, indent=1, ensure_ascii=False))

n_retro = sum(1 for r in rows.values() if r["retrospective"])
print(f"wrote {len(rows)} claim objects to {OUT}")
print(f"prospective (row names a sealed registration): {len(rows)-n_retro}; "
      f"retrospective: {n_retro}")
print(f"edges declared: uses={sum(len(d['uses']) for d in dep.values())} "
      f"corroborates={sum(len(d['corroborates']) for d in dep.values())} "
      f"cites={sum(len(d['cites']) for d in dep.values())}")
if fixups:
    print("class tokens outside the specification, mapped:")
    for cid, tokn, cls in fixups:
        print(f"  {cid}: '[{tokn}]' -> {cls}")
if unresolved:
    print("edges whose endpoint did not resolve:", unresolved)
