"""Draw frame for the v2 held-out set (registration 7.1.1): d9x6s phase-one papers minus every paper SCORE replicated.

Reads only identifier and classification columns of the d9x6s claims file (paper_id, DOI_CR, pub_year_CR,
publication_standard, category, WOS_category, version) and the identifier columns of SCORE's repli_outcomes
(paper_id). No claim text, author field or outcome is read. Prints counts only.

    python k2_d9x6s_frame.py <claims.csv> <analyst data.RData> <devset/access.csv> <out.json>
"""
import csv
import json
import sys
from collections import Counter

import rdata

claims_csv, rda, access_csv, out = sys.argv[1:5]
csv.field_size_limit(10**8)
KEEP = ("paper_id", "DOI_CR", "pub_year_CR", "publication_standard", "category", "WOS_category", "version")
with open(claims_csv, encoding="utf-8", errors="replace", newline="") as fh:
    rows = [{k: r[k].strip() for k in KEEP} for r in csv.DictReader(fh)]

d = rdata.read_rda(rda)
replicated = set(d["repli_outcomes"]["paper_id"].astype(str).str.strip())


def norm(doi):
    doi = doi.lower().strip()
    for p in ("https://doi.org/", "http://dx.doi.org/", "doi:"):
        if doi.startswith(p):
            doi = doi[len(p):]
    return doi


with open(access_csv, encoding="utf-8", newline="") as fh:
    dev = {norm(r.get("doi", "")) for r in csv.DictReader(fh)} - {""}

frame = [r for r in rows if r["paper_id"] not in replicated and norm(r["DOI_CR"]) not in dev]
res = {
    "rows": len(rows),
    "replicated_papers_in_file": sum(r["paper_id"] in replicated for r in rows),
    "dev_doi_matches": sum(norm(r["DOI_CR"]) in dev for r in rows),
    "frame": len(frame),
    "frame_by_category": dict(Counter(r["category"] for r in frame).most_common()),
    "frame_by_year": dict(sorted(Counter(r["pub_year_CR"] for r in frame).items())),
    "frame_journals": len({r["publication_standard"] for r in frame}),
    "version_values": dict(Counter(r["version"] for r in rows)),
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
