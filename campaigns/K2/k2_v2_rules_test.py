#!/usr/bin/env python
"""Case tests for k2_v2_rules (RUBRIC-v2.md Section 2). Each case is a set of answers and the scores the
rubric's table says they must give; a failing case means the code and the table disagree.

    python k2_v2_rules_test.py      # writes k2_v2_rules_test_result.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from k2_v2_rules import VOID, checks, clean

TEXT = """Participants were randomly assigned to the gain or the loss frame.
We predicted that the loss frame would increase risk taking (Hypothesis 1).
Trust was measured with a six-item scale we developed for this study (alpha = .62).
The manipulation check showed that participants in the loss frame felt the stakes were higher.
Of the 130 participants recruited, 112 were included in the analysis.
Two participants were removed as outliers on the risk measure.
The effect was significant for women but not for men.
The study was preregistered at AsPredicted (#1234)."""

BASE = {  # every check passes: an experiment with a validated, reliable scale and a clean sample
    "Q1.1": "researcher_assigned", "Q1.2": "collected_for_this_study",
    "Q2.1": "before_results", "Q2.2": "no",
    "Q3.1": "multi_item_scale", "Q3.2": "yes", "Q3.3": 0.85,
    "Q4.1": "reported", "Q4.2": "succeeded", "Q4.3": "no",
    "Q5.1": 120, "Q5.2": 120, "Q5.3": "none_excluded", "Q5.4": "no",
    "Q6.1": "no", "Q6.2": "no",
}

CASES = [  # (name, changes to BASE, expected {check: score})
    ("all pass", {}, {"A1": "0", "A2": "0", "A3": "0", "A4": "0"}),
    ("A1: prediction only with results, no registration", {"Q2.1": "with_or_after_results"}, {"A1": "1"}),
    ("A1: no prediction, no registration", {"Q2.1": "never"}, {"A1": "1"}),
    ("A1: no prediction but registered", {"Q2.1": "never", "Q2.2": "yes"}, {"A1": "0"}),
    ("A1: void timing, not registered", {"Q2.1": VOID}, {"A1": "U"}),
    ("A2: scale with no cited source", {"Q3.2": "no"}, {"A2": "1"}),
    ("A2: index with no cited source", {"Q3.1": "constructed_index", "Q3.2": "no"}, {"A2": "1"}),
    ("A2: cited index, no reliability needed", {"Q3.1": "constructed_index", "Q3.3": "not_reported"}, {"A2": "0"}),
    ("A2: scale without reliability", {"Q3.3": "not_reported"}, {"A2": "1"}),
    ("A2: scale below .70", {"Q3.3": 0.62}, {"A2": "1"}),
    ("A2: coded outcome at .70", {"Q3.1": "human_coded_or_rated", "Q3.3": 0.70}, {"A2": "0"}),
    ("A2: behavior is na", {"Q3.1": "behavior_or_performance", "Q3.2": "no",
                            "Q3.3": "not_reported"}, {"A2": "na"}),
    ("A2: records are na", {"Q3.1": "record_or_physical"}, {"A2": "na"}),
    ("A2: single item is na", {"Q3.1": "single_item_report"}, {"A2": "na"}),
    ("A2: source void", {"Q3.2": VOID}, {"A2": "U"}),
    ("A3: observational is na", {"Q1.1": "observed_variation", "Q4.1": "not_reported"}, {"A3": "na"}),
    ("A3: policy variation is na", {"Q1.1": "natural_or_policy_variation"}, {"A3": "na"}),
    ("A3: design not stated", {"Q1.1": "not_stated"}, {"A3": "U"}),
    ("A3: no check, no prior validation", {"Q4.1": "not_reported", "Q4.2": "na"}, {"A3": "1"}),
    ("A3: no check, prior validation", {"Q4.1": "not_reported", "Q4.2": "na", "Q4.3": "yes"}, {"A3": "0"}),
    ("A3: check failed", {"Q4.2": "failed_or_mixed"}, {"A3": "1"}),
    ("A3: check result not given", {"Q4.2": "result_not_given"}, {"A3": "0"}),
    ("A4: exclusions without count", {"Q5.3": "excluded_without_count"}, {"A4": "1"}),
    ("A4: outliers on outcome", {"Q5.4": "yes"}, {"A4": "1"}),
    ("A4: unexplained loss in collected data", {"Q5.1": 130, "Q5.2": 112}, {"A4": "1"}),
    ("A4: counted loss", {"Q5.1": 130, "Q5.2": 112, "Q5.3": "counted_with_reasons"}, {"A4": "0"}),
    ("A4: dataset restriction is not loss", {"Q1.2": "existing_dataset", "Q5.1": 5000, "Q5.2": 2100},
     {"A4": "0"}),
    ("A4: unsupportive test, no correction", {"Q6.1": "yes"}, {"A4": "1"}),
    ("A4: unsupportive test, corrected", {"Q6.1": "yes", "Q6.2": "yes"}, {"A4": "0"}),
    ("A4: unsupportive test, correction void", {"Q6.1": "yes", "Q6.2": VOID}, {"A4": "U"}),
    ("A4: other-test answer void", {"Q6.1": VOID}, {"A4": "U"}),
    ("A4: void but outlier fail", {"Q6.1": VOID, "Q5.4": "yes"}, {"A4": "1"}),
    ("gate counts failures", {"Q2.1": "never", "Q3.3": "not_reported", "Q5.4": "yes"},
     {"A1": "1", "A2": "1", "A3": "0", "A4": "1", "gate": 3}),
]


def quote_cases() -> list:
    """clean(): quotes must be in the text; absences need none; bad values and numbers are voided."""
    out = []

    def run(name, raw, q, want):
        got = clean(raw, TEXT)[0][q]
        if got != want:
            out.append([name, q, got, want])

    ok = "researcher_assigned"
    run("verbatim quote kept", {"Q1.1": {"answer": ok,
        "quote": "Participants were randomly assigned to the gain or the loss frame."}}, "Q1.1", ok)
    run("layout difference kept", {"Q1.1": {"answer": ok,
        "quote": "participants were randomly-assigned to the gain  or the loss frame"}}, "Q1.1", ok)
    run("paraphrase voided", {"Q1.1": {"answer": ok,
        "quote": "People were randomly allocated to one of two frames."}}, "Q1.1", VOID)
    run("ellipsis with found fragments kept", {"Q1.1": {"answer": ok,
        "quote": "Participants were randomly assigned ... or the loss frame."}}, "Q1.1", ok)
    run("ellipsis with an unfound fragment voided", {"Q1.1": {"answer": ok,
        "quote": "Participants were randomly assigned ... to a neutral control frame."}}, "Q1.1", VOID)
    run("ellipsis with only short fragments voided", {"Q1.1": {"answer": ok,
        "quote": "We predicted ... frame."}}, "Q1.1", VOID)
    run("short numeric quote kept", {"Q5.2": {"answer": 112, "quote": "112 were"}}, "Q5.2", 112)
    run("too-short quote voided", {"Q5.2": {"answer": 112, "quote": "112"}}, "Q5.2", VOID)
    run("missing quote voided", {"Q2.1": {"answer": "before_results"}}, "Q2.1", VOID)
    run("absence needs no quote", {"Q2.1": {"answer": "never"}}, "Q2.1", "never")
    run("bad value voided", {"Q2.2": {"answer": "maybe"}}, "Q2.2", VOID)
    run("not_stated on a yes/no absence question is no", {"Q5.4": {"answer": "not_stated"}}, "Q5.4", "no")
    run("not_stated where not allowed voided", {"Q3.1": {"answer": "not_stated"}}, "Q3.1", VOID)
    run("missing question voided", {}, "Q3.1", VOID)
    run("number with quote", {"Q5.1": {"answer": "130", "quote": "Of the 130 participants recruited"}}, "Q5.1", 130)
    run("non-whole count voided", {"Q5.1": {"answer": 130.5, "quote": "Of the 130 participants recruited"}},
        "Q5.1", VOID)
    run("reliability above 1 voided", {"Q3.3": {"answer": 62, "quote": "a six-item scale we developed for this study (alpha = .62)"}}, "Q3.3", VOID)
    run("reliability kept", {"Q3.3": {"answer": ".62", "quote": "a six-item scale we developed for this study (alpha = .62)"}}, "Q3.3", 0.62)
    run("unsupportive test needs its quote", {"Q6.1": {"answer": "yes"}}, "Q6.1", VOID)
    run("unsupportive test with quote", {"Q6.1": {"answer": "yes",
        "quote": "The effect was significant for women but not for men."}}, "Q6.1", "yes")
    run("not_stated source is no", {"Q3.2": {"answer": "not_stated"}}, "Q3.2", "no")
    run("exclusions not stated is none_excluded", {"Q5.3": {"answer": "not_stated"}}, "Q5.3", "none_excluded")
    return out


def main() -> int:
    report = {"cases": len(CASES), "wrong": [], "quote_cases_wrong": quote_cases()}
    for name, change, want in CASES:
        got = checks({**BASE, **change})
        bad = {k: (got[k], v) for k, v in want.items() if got[k] != v}
        if bad:
            report["wrong"].append([name, bad])
    report["verdict"] = "PASS" if not report["wrong"] and not report["quote_cases_wrong"] else "FAIL"
    print(json.dumps(report, indent=1))
    Path(__file__).with_name("k2_v2_rules_test_result.json").write_text(json.dumps(report, indent=1) + "\n",
                                                                         encoding="utf-8")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
