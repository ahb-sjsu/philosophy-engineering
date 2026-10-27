#!/usr/bin/env python
"""K2 rubric v2: seeded draw of 60 more DEVELOPMENT papers from the undrawn part of the eligible frame.

Owner, 2026-10-27: "Yes, a seeded 60". v2 needs development papers shaped like the held-out set (SCORE
non-psychology papers, claim-location unit); it had 3 (34Rd, 13Nv, BPXj). The pool is the eligible frame
(devset/frame_eligible.csv, the frame k2_v2_draw.py checks by hash) minus the 90 drawn papers
(devset/v2_draw.csv, every held-out paper among them) minus those 3. Strata and allocation as k2_v2_draw.py
(proportional, largest remainder). The seed is committed in this file before the draw is run.

These papers are revise material: anyone drafting v2 may read their codings. None was replicated by SCORE
(the frame is forecast-but-unreplicated papers), so no outcome can leak from them.

    python k2_v2dev_draw.py devset/frame_eligible.csv devset/v2_draw.csv devset/v2dev2_draw.csv
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys

import numpy as np

from k2_v2_draw import FRAME_SHA256_LF, STRATA, allocate, stratum

SEED = 20261027
N_DRAW = 60
EARLIER_DEV = {"34Rd", "13Nv", "BPXj"}


def main() -> int:
    src, drawn_csv, dst = sys.argv[1:4]
    raw = open(src, "rb").read().replace(b"\r\n", b"\n")
    sha = hashlib.sha256(raw).hexdigest()
    if sha != FRAME_SHA256_LF:
        raise SystemExit(f"frame hash {sha} is not the committed frame {FRAME_SHA256_LF}")
    drawn = {r["paper_id"] for r in csv.DictReader(open(drawn_csv, encoding="utf-8"))}
    assert len(drawn) == 90, len(drawn)
    rows = [r for r in csv.DictReader(raw.decode("utf-8").splitlines())
            if r["paper_id"] not in drawn and r["paper_id"] not in EARLIER_DEV]
    by = {s: sorted((r for r in rows if stratum(r["category"]) == s), key=lambda r: r["paper_id"]) for s in STRATA}
    quota = allocate({s: len(v) for s, v in by.items() if v}, N_DRAW)
    rng = np.random.default_rng(SEED)
    out = []
    for s in STRATA:
        if not quota.get(s):
            continue
        idx = rng.permutation(len(by[s]))[: quota[s]]
        out += [dict(by[s][i], stratum=s) for i in idx]
    order = rng.permutation(len(out))
    cols = ["order", "paper_id", "doi", "journal", "category", "stratum", "best_oa_version", "best_has_pdf"]
    with open(dst, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, cols, extrasaction="ignore", lineterminator="\n")
        wr.writeheader()
        for k, i in enumerate(order, 1):
            wr.writerow(dict(out[i], order=k))
    print(json.dumps({"seed": SEED, "frame_sha256_lf": sha, "pool": len(rows),
                      "pool_by_stratum": {s: len(v) for s, v in by.items()}, "quota": quota, "drawn": len(out)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
