#!/usr/bin/env python
"""Self-test for pe_lint's P5 (PE-CLS-1.0 s7.5) against tools/fixtures/p5.

Each fixture claim exercises one path through check_p5. The test fails if a
claim that should be refused passes, or a claim that should pass is refused.
No test framework needed:

    python tools/test_pe_lint_p5.py
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pe_lint  # noqa: E402

FIXTURE = os.path.join(HERE, "fixtures", "p5")

# claim id -> substring every ERROR on it must contain (None = no ERROR allowed)
EXPECT_ERROR = {
    "P5-MISSING": "no admissibility block",
    "P5-UNASSESSED-LATE": "while admissibility is unassessed",
    "P5-ALLNA": "satisfied vacuously",
    "P5-YES": "is an assertion, not an artifact",
    "P5-FAIL": "inadmissible design grades nothing",
    "P5-NOSIZING": "threshold given with no sizing",
    "P5-NOREASON": "not applicable with no reason",
    "P5-DANGLING": "does not resolve",
    "P5-HUMAN-BARE": "human decision missing",
}
EXPECT_CLEAN = {"P5-OK", "P5-UNASSESSED", "P5-EXEMPT", "P5-HUMAN"}
OUT_OF_SCOPE = {"P5-PROVED", "P5-REFUTED"}


def main() -> int:
    claims = pe_lint.parse_native_ledger(FIXTURE)
    want = set(EXPECT_ERROR) | EXPECT_CLEAN | OUT_OF_SCOPE
    assert set(claims) == want, f"fixture drift: {sorted(set(claims) ^ want)}"

    findings, stats = pe_lint.check_p5(FIXTURE, claims)
    errs: dict[str, list[str]] = {}
    for f in findings:
        if f.severity == "ERROR":
            errs.setdefault(f.claim, []).append(f.message)

    bad = []
    for cid, frag in EXPECT_ERROR.items():
        msgs = errs.get(cid, [])
        if not any(frag in m for m in msgs):
            bad.append(f"{cid}: expected an ERROR containing '{frag}', got {msgs}")
    for cid in EXPECT_CLEAN | OUT_OF_SCOPE:
        if cid in errs:
            bad.append(f"{cid}: expected no ERROR, got {errs[cid]}")

    expected_stats = {"in_scope": 13, "unassessed": 2, "exempt": 1,
                      "missing": 1, "all_na": 1}
    for k, v in expected_stats.items():
        if stats[k] != v:
            bad.append(f"stats[{k}] = {stats[k]}, expected {v}")

    # s7.5.3 / s9.1(3) analogue: a format that cannot hold the block counts
    # its claims as unassessed and never passes them silently.
    f2, s2 = pe_lint.check_p5(FIXTURE, claims, block_expressible=False)
    if s2["unassessed"] != 13 or not any(f.severity == "WARN" for f in f2):
        bad.append(f"inexpressible format not counted as unassessed: {s2}")

    if "P5" not in pe_lint.LEVEL_PROPS["L3"]:
        bad.append("P5 missing from L3 (s9)")

    for b in bad:
        print("FAIL", b)
    print(f"{'FAIL' if bad else 'PASS'}: {len(EXPECT_ERROR)} refusal paths, "
          f"{len(EXPECT_CLEAN)} clean paths, stats {stats}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
