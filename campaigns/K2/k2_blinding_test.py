#!/usr/bin/env python
"""Witness for gate I3 (k2_blinding): run against the 132 development-set
articles' real titles, authors, journals and years, with a synthetic body.

For each article three texts are checked:

    clean      a methods paragraph with no identifying field, but with numbers
               and capitalized words that a careless check would flag
                                            -> leaks() must find nothing
    planted    the same paragraph with every leak kind planted, the title split
               across a line break and hyphenated
                                            -> leaks() must find every kind
    redacted   redact(planted)              -> leaks() must find nothing

The body is synthetic and the article texts are not used (most are closed
access, 7.1), so this shows the check works on real metadata, not that it
catches every leak a real article can carry.

    python k2_blinding_test.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from k2_blinding import leaks, redact

HERE = Path(__file__).resolve().parent
KINDS = ["doi", "title", "author", "journal", "year", "citation", "url", "email"]

BODY = ("Participants (N = 120; 64 women) were recruited in Study 2 and "
        "completed 1998 trials in a 2 x 2 design. Responses were scored by "
        "Condition, and Experiment 1 used the same Stroop procedure. The "
        "effect was F(1, 118) = 5.21, p = .024, d = 0.42.")


def articles():
    with open(HERE / "devset" / "devset_rpp.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["doi"]:
                yield {"id": r["dev_id"], "title": r["crossref_title"] or r["title"],
                       "authors": [a.strip().split()[-1] for a in r["authors"].split(",")
                                   if a.strip()],
                       "journal": r["journal"], "year": "2008",  # RP:P sampled 2008
                       "doi": r["doi"]}
    with open(HERE / "devset" / "devset_ml.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["doi"]:
                yield {"id": r["dev_id"], "title": r["cited_title"],
                       "authors": [r["first_author"]], "journal": "",
                       "year": r["year"], "doi": r["doi"]}


def planted(m):
    w = m["title"].split()
    half = len(w) // 2
    title = " ".join(w[:half]) + "\n" + " ".join(w[half:])
    if len(w[half - 1]) > 4:  # hyphenate the word before the break as well
        title = title.replace(w[half - 1] + "\n", w[half - 1][:3] + "-\n" + w[half - 1][3:] + " ", 1)
    parts = [f"{title}.", BODY,
             f"As {m['authors'][0]} (2003) reported, see also Smith et al., 1999.",
             f"Published {m['year']}. doi:{m['doi']}.",
             "Materials: https://osf.io/abcde/ Contact: lab@univ.edu"]
    if m["journal"]:
        parts.append(f"Accepted by {m['journal']}.")
    return "\n".join(parts)


def main() -> int:
    arts = list(articles())
    report = {"articles": len(arts), "clean_false_leaks": [], "planted_missed": [],
              "redacted_residual": [], "year_trap_fired": [],
              "distinct_dois": len({m["doi"].lower() for m in arts})}
    for m in arts:
        # BODY's "1998 trials" is a deliberate trap: for an article published
        # in 1998 the year rule must fire on it (the stated cost of the rule:
        # a number equal to the year is redacted); for every other article
        # the clean body must leak nothing
        expect = {"year"} if m["year"] == "1998" else set()
        got_clean = {k for k, _ in leaks(BODY, m)}
        if got_clean != expect:
            report["clean_false_leaks"].append([m["id"], leaks(BODY, m)])
        elif expect:
            report["year_trap_fired"].append(m["id"])
        t = planted(m)
        got = {k for k, _ in leaks(t, m)}
        want = set(KINDS) - ({"journal"} if not m["journal"] else set())
        if want - got:
            report["planted_missed"].append([m["id"], sorted(want - got)])
        r = leaks(redact(t, m), m)
        if r:
            report["redacted_residual"].append([m["id"], r])
    ok = not any(report[k] for k in ("clean_false_leaks", "planted_missed",
                                     "redacted_residual"))
    report["verdict"] = "PASS" if ok else "FAIL"
    print(json.dumps(report, indent=1)[:4000])
    with open(HERE / "k2_blinding_test_result.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
