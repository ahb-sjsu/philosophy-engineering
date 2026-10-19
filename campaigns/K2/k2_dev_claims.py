#!/usr/bin/env python
"""Claim statements for the blinded development units (RUBRIC-v1 section 0).

RP:P states each claim on the original side of its master data
(RPPdataConverted.csv): Description.of.effect.O and Test.statistic.O. Only
those two columns are read; no replication-side (.R) column is opened, so no
outcome enters (registration 7.1 consequence 5).

The Many Labs sources hold materials, not written claims. A Many Labs target
is its effect label, plus, for Many Labs 1, the comparison as the ML1 codebook
states its items (copied below from ML1_Codebook.xlsx, sheet Foglio1). No claim
sentence is written here that a source does not hold.

    python3 k2_dev_claims.py /archive/experiments/k2/raw/rpp/RPPdataConverted.csv
    # writes devset/claims_dev.csv
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ML1_COMPARISON = {
    "Sunk Costs": "Many Labs 1 compared participants told they had paid handsomely for "
                  "a game ticket with participants told it was free from a friend, on a "
                  "1 (stay at home) to 9 (go to game) choice for a freezing-cold game day.",
    "Retrospective gambler fallacy": "Many Labs 1 compared estimates of how many times a "
                  "man had rolled the dice before the participant walked by, after an "
                  "imagined roll of three 6s versus a roll of two 6s and a 3.",
}


def main() -> int:
    man = {r["dev_id"]: r for r in csv.DictReader(open(HERE / "devset" / "intake_manifest.csv", encoding="utf-8"))}
    blind = {d for d, r in man.items() if r["status"] == "blinded"}
    rpp = {r["dev_id"]: r for r in csv.DictReader(open(HERE / "devset" / "devset_rpp.csv", encoding="utf-8"))}
    ml: dict[str, list] = {}
    for r in csv.DictReader(open(HERE / "devset" / "devset_ml.csv", encoding="utf-8")):
        ml.setdefault(r["dev_id"], []).append(r)
    orig = {}
    with open(sys.argv[1], encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            orig[r["Local.ID"]] = (r["Description.of.effect.O"].replace("�", "'").strip(),
                                   r["Test.statistic.O"].strip())
    rows = []
    for d in sorted(blind):
        if d in rpp:
            desc, test = orig[rpp[d]["rpp_local_id"]]
            rows.append({"dev_id": d, "study": rpp[d]["study_number"], "claim": desc,
                         "focal_test": test, "source": "RP:P Description.of.effect.O, Test.statistic.O"})
        else:
            effs = sorted({r["effect"] for r in ml[d]})
            label = " / ".join(effs)
            comp = " ".join(ML1_COMPARISON[e] for e in effs if e in ML1_COMPARISON)
            rows.append({"dev_id": d, "study": "", "claim": f'The effect labelled "{label}". {comp}'.strip(),
                         "focal_test": "", "source": "Many Labs effect label" + (", ML1 codebook" if comp else "")})
    with open(HERE / "devset" / "claims_dev.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["dev_id", "study", "claim", "focal_test", "source"])
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "claims written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
