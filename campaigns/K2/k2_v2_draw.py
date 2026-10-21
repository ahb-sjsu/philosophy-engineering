#!/usr/bin/env python
"""K2 rubric v2: seeded draw of 90 papers from the eligible frame (owner, 2026-10-21; RUBRIC-v2-PLAN D2).

The seed, the frame file's hash and the allocation rule are committed in this file BEFORE the draw is run.

Frame: devset/frame_eligible.csv (325 papers, commit d404f68), checked by sha256 of its text with line endings
normalized to LF. Strata (proportional to the eligible pool, largest-remainder allocation of 90):

    economics      any category naming Business & Economics
    politics       Government & Law, International Relations or Public Administration
    demography     Demography
    sociology      Sociology or Family Studies
    criminology    Criminology & Penology
    education      Education & Educational Research

Within each stratum the paper_ids are sorted, permuted with the seeded generator, and the stratum's quota taken.
The 90 drawn papers are then put in one seeded order. Held-out rule: the held-out set is the first 60 papers in
that order whose text is obtained and passes intake (4.1); usable papers after the 60th are revise material.
Nobody drafting v2 reads a held-out text; intake is run by script.

    python k2_v2_draw.py devset/frame_eligible.csv devset/v2_draw.csv
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys

import numpy as np

SEED = 20261021
N_DRAW = 90
# Corrected in the commit after 535dd86, before any draw ran: 535dd86 held a7c50460..., the hash of the laptop copy
# with CRLF line endings, not of the LF-normalized text this script checks. Same frame (blob in d404f68).
FRAME_SHA256_LF = "b5bb1d61edc936833c4bd44383c67fcd913dbcbae77c1211bda310e6eb9c96ab"
STRATA = ("economics", "politics", "demography", "sociology", "criminology", "education")


def stratum(category: str) -> str:
    c = category.lower()
    if "business & economics" in c:
        return "economics"
    if "government & law" in c or "international relations" in c or "public administration" in c:
        return "politics"
    if "demography" in c:
        return "demography"
    if "sociology" in c or "family studies" in c:
        return "sociology"
    if "criminology" in c:
        return "criminology"
    if "education" in c:
        return "education"
    raise SystemExit(f"category with no stratum: {category}")


def allocate(sizes: dict, n: int) -> dict:
    total = sum(sizes.values())
    exact = {s: n * k / total for s, k in sizes.items()}
    out = {s: int(v) for s, v in exact.items()}
    for s in sorted(exact, key=lambda s: (-(exact[s] - out[s]), STRATA.index(s)))[: n - sum(out.values())]:
        out[s] += 1
    return out


def main() -> int:
    src, dst = sys.argv[1:3]
    raw = open(src, "rb").read().replace(b"\r\n", b"\n")
    sha = hashlib.sha256(raw).hexdigest()
    if sha != FRAME_SHA256_LF:
        raise SystemExit(f"frame hash {sha} is not the committed frame {FRAME_SHA256_LF}")
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    by = {s: sorted((r for r in rows if stratum(r["category"]) == s), key=lambda r: r["paper_id"]) for s in STRATA}
    quota = allocate({s: len(v) for s, v in by.items() if v}, N_DRAW)
    rng = np.random.default_rng(SEED)
    drawn = []
    for s in STRATA:
        if not quota.get(s):
            continue
        idx = rng.permutation(len(by[s]))[: quota[s]]
        drawn += [dict(by[s][i], stratum=s) for i in idx]
    order = rng.permutation(len(drawn))
    cols = ["order", "paper_id", "doi", "journal", "category", "stratum", "best_oa_version", "best_has_pdf"]
    with open(dst, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, cols, extrasaction="ignore", lineterminator="\n")
        wr.writeheader()
        for k, i in enumerate(order, 1):
            wr.writerow(dict(drawn[i], order=k))
    print(json.dumps({"seed": SEED, "frame_sha256_lf": sha, "frame": len(rows),
                      "pool": {s: len(v) for s, v in by.items()}, "quota": quota, "drawn": len(drawn)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
