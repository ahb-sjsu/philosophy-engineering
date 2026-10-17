#!/usr/bin/env python
"""Score a K-1 held-out record: author key vs reader answers.

    python benchmark/defects/score_heldout.py benchmark/defects/heldout-2026-10-17.json

Reports agreement on expressible-or-not, on the primary gate (exact, and
counting a match on either side's secondary), and on checkability, plus the
direction of every expressibility disagreement: an author who over-credits
the specification is the failure this test exists to catch.
"""
from __future__ import annotations

import json
import sys


def expressible(g) -> bool:
    return g is not None and str(g).lower() != "none"


def main() -> int:
    rec = json.load(open(sys.argv[1], encoding="utf-8"))
    key, sec = rec["author_key"], rec.get("author_secondary", {})
    chk, ans = rec["author_checkable"], rec["reader_answers"]
    ids = sorted(key)
    n = len(ids)
    exp_agree = gate_exact = gate_loose = chk_agree = 0
    over, under = [], []
    for i in ids:
        a, r = key[i], ans[i]
        ea, er = expressible(a), expressible(r["primary"])
        exp_agree += ea == er
        if ea and not er:
            over.append(i)
        if er and not ea:
            under.append(i)
        gate_exact += a == r["primary"]
        a_set = {a, sec.get(i)} - {None}
        r_set = {r["primary"], r.get("secondary")} - {None}
        gate_loose += bool(a_set & r_set) or (not ea and not er)
        chk_agree += chk[i] == r["checkable"]
    out = {
        "n": n,
        "expressible_agreement": f"{exp_agree}/{n} ({exp_agree / n:.0%})",
        "primary_gate_exact": f"{gate_exact}/{n} ({gate_exact / n:.0%})",
        "gate_match_incl_secondary": f"{gate_loose}/{n} ({gate_loose / n:.0%})",
        "checkable_agreement": f"{chk_agree}/{n} ({chk_agree / n:.0%})",
        "author_expressible": sum(expressible(key[i]) for i in ids),
        "reader_expressible": sum(expressible(ans[i]["primary"]) for i in ids),
        "author_over_credited_spec": over,
        "author_under_credited_spec": under,
    }
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
