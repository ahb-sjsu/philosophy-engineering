#!/usr/bin/env python
"""Split the 22 blinded development units into a revise half and a held-out half.

The v0 pilot (registration 7.4) found the two model families far apart. The
rubric is revised by reading why they disagree, and reading that on the same
units that then measure the revised rubric would overstate its agreement
(the reasons would be fitted to those articles). So the split is fixed here,
seeded and stratified by source (Many Labs, RP:P), and committed before any
item-level disagreement or coder reasoning is read. Only the revise half's
reasoning is read; the held-out half's v1 agreement is the reported number.

    python k2_rubric_split.py   # writes k2_rubric_split.json
"""
from __future__ import annotations

import csv
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 20261019


def main() -> int:
    man = list(csv.DictReader(open(HERE / "devset" / "intake_manifest.csv", encoding="utf-8")))
    devs = sorted(r["dev_id"] for r in man if r["status"] == "blinded")
    rng = random.Random(SEED)
    revise, held = [], []
    for src in ("DEV-ML-", "DEV-RPP-"):
        group = [d for d in devs if d.startswith(src)]
        rng.shuffle(group)
        k = len(group) // 2
        revise += group[:k]
        held += group[k:]
    out = {"seed": SEED, "units": len(devs), "revise": sorted(revise), "held_out": sorted(held)}
    (HERE / "k2_rubric_split.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
