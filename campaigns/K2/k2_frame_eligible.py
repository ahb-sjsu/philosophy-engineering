#!/usr/bin/env python
"""K2 v2 draw frame, eligible papers (owner rules 2026-10-21, registration 7.1.1).

From the 2,852-paper frame (devset/frame_access.csv):
  1. A paper with no Web of Science category ("NA") takes its journal's category: the most common category among
     the categorized frame papers of the same journal (publication_standard). A journal with none stays NA and the
     paper is excluded and counted.
  2. Any category that names Psychology, alone or mixed, is excluded.
  3. Only papers whose best open copy on record is the published or the accepted version are eligible.

Reads only paper_id, publication_standard and category from the claims file. Writes the eligible list and counts.

    python k2_frame_eligible.py <claims.csv> <frame_access.csv> <eligible.csv> <summary.json>
"""
from __future__ import annotations

import collections
import csv
import json
import sys

claims_csv, access_csv, out_csv, out_json = sys.argv[1:5]
csv.field_size_limit(10**8)
journal = {}
with open(claims_csv, encoding="utf-8", errors="replace", newline="") as fh:
    for r in csv.DictReader(fh):
        journal[r["paper_id"].strip()] = r["publication_standard"].strip()
frame = list(csv.DictReader(open(access_csv, encoding="utf-8")))
for f in frame:
    f["journal"] = journal[f["paper_id"]]

by_journal = collections.defaultdict(collections.Counter)
for f in frame:
    if f["category"] != "NA":
        by_journal[f["journal"]][f["category"]] += 1
classed, unclassed, ties = 0, 0, []
for f in frame:
    f["category_source"] = "wos"
    if f["category"] == "NA":
        c = by_journal.get(f["journal"])
        if c:
            top = c.most_common()
            if len(top) > 1 and top[0][1] == top[1][1]:
                ties.append(f["journal"])
            f["category"], f["category_source"] = top[0][0], "journal"
            classed += 1
        else:
            f["category_source"] = "none"
            unclassed += 1

no_psych = [f for f in frame if f["category_source"] != "none" and "psychology" not in f["category"].lower()]
eligible = [f for f in no_psych if f["is_oa"] == "True" and f["best_oa_version"] in ("publishedVersion", "acceptedVersion")]
cols = ["paper_id", "doi", "journal", "category", "category_source", "oa_status", "best_oa_version", "best_has_pdf"]
with open(out_csv, "w", newline="", encoding="utf-8") as fh:
    wr = csv.DictWriter(fh, cols, extrasaction="ignore")
    wr.writeheader()
    wr.writerows(sorted(eligible, key=lambda f: f["paper_id"]))
summary = {
    "frame": len(frame),
    "na_classed_by_journal": classed, "na_journal_uncategorized": unclassed,
    "na_journals_with_tied_categories": sorted(set(ties)),
    "after_psychology_excluded": len(no_psych),
    "eligible_published_or_accepted": len(eligible),
    "eligible_by_version": dict(collections.Counter(f["best_oa_version"] for f in eligible)),
    "eligible_with_pdf_link": sum(f["best_has_pdf"] == "True" for f in eligible),
    "eligible_by_category": dict(collections.Counter(f["category"] for f in eligible).most_common()),
    "eligible_classed_from_na": sum(f["category_source"] == "journal" for f in eligible),
    "eligible_journals": len({f["journal"] for f in eligible}),
    "non_psych_by_category": dict(collections.Counter(f["category"] for f in no_psych).most_common()),
}
json.dump(summary, open(out_json, "w"), indent=1)
print(json.dumps(summary, indent=1))
