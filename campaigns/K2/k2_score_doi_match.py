"""Shape of the SCORE analyst data and a DOI match against the K2 development set.

Reads no replication outcome: from repli_outcomes it touches only identifier and
design columns (SAFE_REPLI). Prints shapes, column names, counts and dev_ids.
"""
import csv
import json
import re
import sys
from collections import Counter

import rdata

SAFE_REPLI = ["paper_id", "claim_id", "rr_id", "report_id", "repli_type", "is_manylabs",
              "manylabs_type", "repli_version_of_record", "type_internal", "is_covid"]

rda, access, out = sys.argv[1], sys.argv[2], sys.argv[3]
data = rdata.read_rda(rda)


def norm(d):
    d = str(d or "").strip().lower()
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", d)


shapes = {}
for name, obj in data.items():
    if hasattr(obj, "columns"):
        shapes[name] = {"rows": int(obj.shape[0]), "columns": [str(c) for c in obj.columns]}
    else:
        shapes[name] = {"type": type(obj).__name__}
for name, s in shapes.items():
    print(name, s.get("rows", s.get("type")), "rows" if "rows" in s else "")
    if "columns" in s:
        print("   ", ", ".join(s["columns"])[:600])

meta = data["paper_metadata"]
doi_col = next(c for c in meta.columns if c.strip().lower() == "doi")
pid_col = next(c for c in meta.columns if c.strip().lower() == "paper_id")
score_doi = {}
for pid, d in zip(meta[pid_col], meta[doi_col]):
    if norm(d):
        score_doi.setdefault(norm(d), set()).add(str(pid).strip())
print("paper_metadata:", len(meta), "rows,", len(score_doi), "distinct DOIs")

dev = list(csv.DictReader(open(access, encoding="utf-8")))
rep = data["repli_outcomes"][[c for c in SAFE_REPLI if c in data["repli_outcomes"].columns]]
orig = data["orig_outcomes"]
matches = []
for r in dev:
    pids = sorted(score_doi.get(norm(r["doi"]), []))
    if not pids:
        continue
    sub = rep[rep["paper_id"].astype(str).str.strip().isin(pids)]
    matches.append({
        "dev_id": r["dev_id"], "doi": norm(r["doi"]), "score_paper_ids": pids,
        "score_claims": int(orig["paper_id"].astype(str).str.strip().isin(pids).sum()),
        "score_replication_reports": int(len(sub)),
        "repli_type": dict(Counter(map(str, sub["repli_type"]))) if "repli_type" in sub else None,
        "is_manylabs": dict(Counter(map(str, sub["is_manylabs"]))) if "is_manylabs" in sub else None,
    })

ml = rep["is_manylabs"].astype(str) if "is_manylabs" in rep else None
summary = {
    "rda": rda, "shapes": shapes,
    "score_distinct_dois": len(score_doi),
    "dev_articles": len(dev), "dev_with_doi": sum(1 for r in dev if norm(r["doi"])),
    "matched": len(matches),
    "matched_with_replication_report": sum(1 for m in matches if m["score_replication_reports"]),
    "matches": matches,
    "score_manylabs_reports": dict(Counter(ml)) if ml is not None else None,
    "score_manylabs_types": dict(Counter(map(str, rep["manylabs_type"]))) if "manylabs_type" in rep else None,
}
json.dump(summary, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != "shapes"}, indent=1))
