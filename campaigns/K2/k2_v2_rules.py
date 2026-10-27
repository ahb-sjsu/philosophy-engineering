#!/usr/bin/env python
"""K2 rubric v2: check scores computed from a coder's factual answers (RUBRIC-v2.md Section 2).

The coder answers the questions of RUBRIC-v2.md Section 1; this module is the definition of the checks.
Frozen with the rubric (its hash goes beside the rubric's).

    from k2_v2_rules import clean, checks
    answers, voided = clean(raw_answers, unit_text)   # quotes verified against the text the coder saw
    scores = checks(answers)                          # {"A1": "1", "A2": "na", ..., "gate": 1, "n_U": 0}

An answer is VOID when its value is not one the question allows, or when it needs a quote and the quote
is missing or cannot be found in the text (verbatim, or after the layout normalization of
k2_quote_check.letters: ligatures, line-break hyphens, page-number lines, punctuation). A VOID answer
the rule needs makes the check U; an answer that already fails the check is enough without the others.
"""
from __future__ import annotations

import re

from k2_quote_check import letters

VOID = "VOID"
NUMBER = "number"

# allowed answers; NUMBER takes a non-negative number (a whole number except Q3.3)
ALLOWED = {
    "Q1.1": {"researcher_assigned", "natural_or_policy_variation", "observed_variation", "not_stated"},
    "Q1.2": {"collected_for_this_study", "existing_dataset", "not_stated"},
    "Q2.1": {"quoted", "none"},
    "Q2.2": {"yes", "no"},
    "Q2.3": {"quoted", "none"},
    "Q3.1": {"multi_item_scale", "single_item_report", "human_coded_or_rated", "constructed_index",
             "behavior_or_performance", "record_or_physical", "not_stated"},
    "Q3.2": {"yes", "no"},
    "Q3.3": {NUMBER, "not_reported"},
    "Q4.1": {"reported", "not_reported"},
    "Q4.2": {"succeeded", "failed_or_mixed", "result_not_given", "na"},
    "Q4.3": {"yes", "no"},
    "Q5.1": {NUMBER, "not_stated"},
    "Q5.2": {NUMBER, "not_stated"},
    "Q5.3": {"none_excluded", "counted_with_reasons", "excluded_without_count"},
    "Q5.4": {"yes", "no"},
    "Q6.1": {"yes", "no"},
    "Q6.2": {"yes", "no"},
}
# answers that are statements about the text and so need a quote; absences ("not_stated", "no", "never") do not
NEEDS_QUOTE = {
    "Q1.1": {"researcher_assigned", "natural_or_policy_variation", "observed_variation"},
    "Q1.2": {"collected_for_this_study", "existing_dataset"},
    "Q2.1": {"quoted"},
    "Q2.2": {"yes"},
    "Q2.3": {"quoted"},
    "Q3.1": ALLOWED["Q3.1"] - {"not_stated"},
    "Q3.2": {"yes"},
    "Q3.3": {NUMBER},
    "Q4.1": {"reported"},
    "Q4.2": {"succeeded", "failed_or_mixed"},
    "Q4.3": {"yes"},
    "Q5.1": {NUMBER},
    "Q5.2": {NUMBER},
    "Q5.3": {"counted_with_reasons", "excluded_without_count"},
    "Q5.4": {"yes"},
    "Q6.1": {"yes"},
    "Q6.2": {"yes"},
}
QUESTIONS = list(ALLOWED)
# derived in clean() from the quotes' positions in the text, not answered by the coder (v2.3)
DERIVED = ["Q2.order"]
# a "prediction" holding a test statistic is a finding (v2.3: qwen3-small quoted "As expected, the condition
# effect was significant, F(2, 43) = 3.36" as a prediction stated before the results)
STATISTIC = re.compile(r"\b[tFrzZ]\s*\(\s*\d|\bp\s*[<>=≤≥⬍⫽]|χ|\bchi-?square|\b[Ftz]\s*=\s*-?\d|η2|\bβ\s*=|"
                       r"\bM\s*=\s*-?\d|\bSD\s*=")
# yes/no questions about something the article may not mention: "no" is the absence, so a coder's
# "not_stated" means "no" (RUBRIC-v2 Section 1; gpt-oss answered Q5.4 "not_stated", trial 2026-10-27)
ABSENCE_NO = {"Q2.2", "Q3.2", "Q4.3", "Q5.4", "Q6.1", "Q6.2"}
MANIPULATED = {"researcher_assigned"}
VALIDITY_TYPES = {"multi_item_scale", "human_coded_or_rated", "constructed_index"}
RELIABILITY_TYPES = {"multi_item_scale", "human_coded_or_rated"}
RELIABILITY_MIN = 0.70
MAX_QUOTE_WORDS = 120  # verifiable at any length; round 2 voided 15 exact quotes over 40 words
MIN_QUOTE_CHARS = 4


def _number(v, whole: bool):
    if isinstance(v, bool):
        return None
    if isinstance(v, str):
        v = v.strip().replace(",", "")
        if not re.fullmatch(r"\d+(\.\d+)?|\.\d+", v):
            return None
        v = float(v)
    if not isinstance(v, (int, float)) or v < 0:
        return None
    if whole:
        return int(v) if float(v).is_integer() else None
    return float(v)


def quote_found(quote: str, text_letters: str) -> bool:
    """Found after layout normalization; at least MIN_QUOTE_CHARS letters or digits ("N = 213"). A quote with
    an ellipsis passes when every fragment of 12 or more characters is found (round 1: 36 such quotes)."""
    if not isinstance(quote, str) or len(quote.split()) > MAX_QUOTE_WORDS:
        return False
    if "..." in quote or "…" in quote:
        frags = [letters(f) for f in re.split(r"\.\.\.|…", quote)]
        frags = [f for f in frags if len(f) >= 12]
        return bool(frags) and all(f in text_letters for f in frags)
    q = letters(quote)
    return len(q) >= MIN_QUOTE_CHARS and q in text_letters


def _position(quote: str, text_letters: str) -> int:
    parts = re.split(r"\.\.\.|…", quote)
    frags = [letters(f) for f in parts if len(letters(f)) >= MIN_QUOTE_CHARS]
    return text_letters.find(frags[0]) if frags else -1


def clean(raw: dict, text: str) -> tuple[dict, dict]:
    """Coder answers -> {question: value or VOID}, and {question: why voided}."""
    tl = letters(text)
    out, why = {}, {}
    for q in QUESTIONS:
        item = raw.get(q) if isinstance(raw, dict) else None
        if not isinstance(item, dict) or "answer" not in item:
            out[q], why[q] = VOID, "missing"
            continue
        a = item["answer"]
        if NUMBER in ALLOWED[q] and not (isinstance(a, str) and a.strip() in ALLOWED[q]):
            n = _number(a, whole=(q != "Q3.3"))
            if n is None or (q == "Q3.3" and n > 1):
                out[q], why[q] = VOID, "not an allowed number"
                continue
            a, kind = n, NUMBER
        else:
            a = a.strip() if isinstance(a, str) else a
            if q in ABSENCE_NO and a == "not_stated":
                a = "no"
            if q == "Q5.3" and a == "not_stated":  # no exclusion mentioned (v2.2; scored the same in v2.1)
                a = "none_excluded"
            if a not in ALLOWED[q]:
                out[q], why[q] = VOID, "not an allowed answer"
                continue
            kind = a
        if kind in NEEDS_QUOTE.get(q, set()) and not quote_found(item.get("quote", ""), tl):
            out[q], why[q] = VOID, "quote not found in the text"
            continue
        out[q] = a
    # Q2.order (v2.3): where the first prediction sits against the first result, decided by position
    p, r = out["Q2.1"], out["Q2.3"]
    if p == "quoted" and STATISTIC.search(str(raw["Q2.1"].get("quote", ""))):
        out["Q2.1"] = p = VOID
        why["Q2.1"] = "a finding, not a prediction"
    if p == VOID:
        order = VOID
    elif p == "none":
        order = "no_prediction"
    elif r == "none":
        order = "prediction_no_result"
    elif r == VOID:
        order = VOID
    else:
        pp, rp = _position(raw["Q2.1"]["quote"], tl), _position(raw["Q2.3"]["quote"], tl)
        order = "prediction_first" if pp < rp else "result_first"
    out["Q2.order"] = order
    return out, why


def a1(x: dict) -> str:
    order = x["Q2.order"]
    if x["Q2.2"] == "yes" or order in ("prediction_first", "prediction_no_result"):
        return "0"
    if order in ("no_prediction", "result_first") and x["Q2.2"] == "no":
        return "1"
    return "U"


def a2(x: dict) -> str:
    kind = x["Q3.1"]
    if kind in (VOID, "not_stated"):
        return "U"
    if kind not in VALIDITY_TYPES:
        return "na"
    src, rel = x["Q3.2"], x["Q3.3"]
    if src == "no":
        return "1"
    if kind in RELIABILITY_TYPES and (rel == "not_reported" or (isinstance(rel, float) and rel < RELIABILITY_MIN)):
        return "1"
    if src == VOID or (kind in RELIABILITY_TYPES and rel == VOID):
        return "U"
    return "0"


def a3(x: dict) -> str:
    design = x["Q1.1"]
    if design in ("natural_or_policy_variation", "observed_variation"):
        return "na"
    if design not in MANIPULATED:
        return "U"
    chk, res, prior = x["Q4.1"], x["Q4.2"], x["Q4.3"]
    if res == "failed_or_mixed":
        return "1"
    if chk == "not_reported":
        return {"no": "1", "yes": "0"}.get(prior, "U")
    if chk == "reported" and res in ("succeeded", "result_not_given"):
        return "0"
    return "U"


def a4(x: dict) -> str:
    flow, outlier = x["Q5.3"], x["Q5.4"]
    n_in, n_test = x["Q5.1"], x["Q5.2"]
    other, corr = x["Q6.1"], x["Q6.2"]
    fails = flow == "excluded_without_count" or outlier == "yes"
    # numbers that show unexplained loss in data collected for the study (not a dataset's design restrictions)
    if (x["Q1.2"] == "collected_for_this_study" and isinstance(n_in, int) and isinstance(n_test, int)
            and n_test < n_in and flow == "none_excluded"):
        fails = True
    if other == "yes" and corr == "no":
        fails = True
    if fails:
        return "1"
    if VOID in (flow, outlier, other) or (other == "yes" and corr == VOID):
        return "U"
    return "0"


def checks(x: dict) -> dict:
    out = {"A1": a1(x), "A2": a2(x), "A3": a3(x), "A4": a4(x)}
    out["gate"] = sum(v == "1" for v in out.values())
    out["n_U"] = sum(v == "U" for k, v in out.items() if k.startswith("A"))
    return out
