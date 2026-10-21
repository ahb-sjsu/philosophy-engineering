#!/usr/bin/env python
"""Chrome work lists for v2 (owner, 2026-10-21: open copies fetched through the owner's Chrome).

  dev:      a seeded sample of 12 eligible papers that were NOT drawn (unit development material, never held-out)
  heldout:  the drawn papers with no PDF yet, in draw order

For each paper, the published/accepted open locations from OpenAlex (published first, PDF links first). Nothing is
downloaded here.

    python k2_v2_urls.py devset/frame_eligible.csv devset/v2_draw.csv <pdf dir> devset/v2_chrome_worklist.json
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

from k2_v2_fetch import locations

DEV_SEED, DEV_N = 20261022, 12

elig = sorted(csv.DictReader(open(sys.argv[1], encoding="utf-8")), key=lambda r: r["paper_id"])
draw = list(csv.DictReader(open(sys.argv[2], encoding="utf-8")))
have = {p.stem for p in Path(sys.argv[3]).glob("*.pdf")}
drawn = {r["paper_id"] for r in draw}
undrawn = [r for r in elig if r["paper_id"] not in drawn]
dev = [undrawn[i] for i in np.random.default_rng(DEV_SEED).permutation(len(undrawn))[:DEV_N]]


def entry(r, role):
    locs = locations(r["doi"])
    return {"role": role, "order": r.get("order", ""), "paper_id": r["paper_id"], "doi": r["doi"],
            "urls": [{"version": l["version"], "pdf_url": l.get("pdf_url") or "",
                      "landing_page_url": l.get("landing_page_url") or ""} for l in locs]}


work = [entry(r, "dev") for r in dev] + [entry(r, "heldout") for r in draw if r["paper_id"] not in have]
json.dump({"dev_seed": DEV_SEED, "papers": work}, open(sys.argv[4], "w", encoding="utf-8"), indent=1)
print(json.dumps({"dev": DEV_N, "heldout_missing": sum(w["role"] == "heldout" for w in work),
                  "no_location": sum(not w["urls"] for w in work)}))
