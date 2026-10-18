#!/usr/bin/env python
"""Witness for gate I3 (k2_blinding): run against the 132 development-set
articles' Crossref records (devset/crossref_meta.json: titles, all surnames
and given names, journal and short names, year, pages), with a synthetic body.

For each article these texts are checked:

    clean      a methods paragraph with no identifying field, but with numbers
               and capitalized words that a careless check would flag
                                            -> leaks() finds nothing, except
                                               the year trap below
    planted    the paragraph with every leak kind planted, the title split
               across a line break and hyphenated
                                            -> leaks() finds every kind
    fuzzy      the title alone with "the" inserted and one word misspelled,
               as on a repository cover page
                                            -> the fuzzy title rule fires
                                               (titles with 4+ content words)
    redacted   redact(planted)              -> leaks() finds nothing

Version 2 (2026-10-17) adds the kinds that the first real-article intake
(k2_intake.py on 7 open PDFs) showed the first version missed: given names,
capitalized surnames, institutions, volume and pages, cover and running-head
lines, near years, "Name YEAR" citations, entity-encoded journal names, and
fuzzy titles. A long running head with author initials (more than 8 words,
so repeated only after redaction) was added after the second intake
(2026-10-18, 24 articles), and a correspondence footnote with a street
address and an author block with a city after the Method lead was added to
the coding unit. The body is synthetic, so this shows each rule works on real
metadata; the real-article read is the check on what the rules miss.

    python k2_blinding_test.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from k2_blinding import STOP, YEAR_WINDOW, _fuzzy_title_spans, _norm, leaks, redact

HERE = Path(__file__).resolve().parent
KINDS = ["doi", "title", "author", "journal", "year", "citation", "url", "email",
         "biblio", "institution", "cover"]

BODY = ("Participants (N = 120; 64 women) were recruited in Study 2 and "
        "completed 1998 trials in a 2 x 2 design. Responses were scored by "
        "Condition, and Experiment 1 used the same Stroop procedure. The "
        "effect was F(1, 118) = 5.21, p = .024, d = 0.42.")


def planted(m):
    w = _norm(m["title"]).split()
    half = len(w) // 2
    title = " ".join(w[:half]) + "\n" + " ".join(w[half:])
    if len(w[half - 1]) > 4:  # hyphenate the word before the break as well
        title = title.replace(w[half - 1] + "\n", w[half - 1][:3] + "-\n" + w[half - 1][3:] + " ", 1)
    sur, given = m["authors"][0], (m.get("given") or ["Alex"])[0].split()[0]
    parts = [f"{title}.", BODY,
             f"As {sur} (2003) reported, see also Smith et al., 1999, and Bless 1990.",
             f"{given} {sur.upper()}",
             f"Published {int(m['year']) - 1}. doi:{m['doi']}.",
             "Materials: https://osf.io/abcde/ Contact: lab@univ.edu",
             "Department of Psychology, University of Waterloo",
             f"Running head: {w[0].upper()} EFFECTS",
             "Vol. 34"]
    if m.get("journal"):
        parts.append(f"Accepted by {_norm(m['journal'])}.")
    if re.match(r"\d+", str(m.get("page", ""))):
        parts.append(f"pp. {m['page']}")
    # an unlabelled running head on three pages, and a repository cover page
    parts += ["Selection Effects 12", BODY, "Selection Effects 13", BODY,
              "Selection Effects 14"]
    # a running head of more than 8 words, as Elsevier prints it: it counts as
    # repeated only after its fields are redacted (DEV-ML-001, 2026-10-18)
    head = (f"{given[0]}.Q. {sur} et al. / {_norm(m.get('journal') or 'Journal of Studies')}"
            f" 45 ({m['year']}) 101-112")
    parts += [head, BODY, head, BODY, head]
    # self-citations leave particles and initials beside the removed surname,
    # and PubMed Central stamps every page (second intake, 2026-10-18)
    parts += [f"see van der {sur} and Q. R. {sur}, also {sur}, Q. R., and others",
              "the task follows Thaler’s (1985) beer pricing study",
              "J Exp Psychol. Author manuscript; available in PMC 2010 May 1."]
    # a correspondence footnote over three lines: the street and city carry no
    # name, so only the footnote rule removes them (DEV-RPP-070, 2026-10-18)
    parts += [f"Address correspondence to {given} {sur}, Department",
              "of Brain Science, 77 Elm Street", "Springfield, MA 01101.", "",
              # an author block whose city survives the institution rule
              f"{given.upper()} {sur.upper()}", "University of Waterloo, Port Mesa", ""]
    return ("Repository copy\nGeneral rights: see the portal.\nTake down policy: "
            "contact us.\f" + "\n".join(parts))


def fuzzy(m):
    w = _norm(m["title"]).split()
    i = max(range(len(w)), key=lambda k: len(w[k]))  # misspell the longest word
    w[i] = w[i][:2] + w[i][2] + w[i][2:]
    w.insert(len(w) // 2, "the")
    return " ".join(w)


def main() -> int:
    meta = json.loads((HERE / "devset" / "crossref_meta.json").read_text(encoding="utf-8"))
    report = {"version": 2, "articles": len(meta), "clean_false_leaks": [],
              "planted_missed": [], "fuzzy_missed": [], "fuzzy_not_applicable": 0,
              "spaced_missed": [],
              "redacted_residual": [], "year_trap_fired": [], "metadata_errors": []}
    for dev, m in sorted(meta.items()):
        if "error" in m or not m.get("title") or not m.get("authors"):
            report["metadata_errors"].append(dev)
            continue
        # BODY's "1998 trials" is a deliberate trap: for an article published
        # within YEAR_WINDOW of 1998 the year rule must fire on it (the stated
        # cost of the rule); for every other article the clean body leaks nothing
        y = int(m["year"]) if str(m["year"]).isdigit() else 0
        expect = {"year"} if abs(y - 1998) <= YEAR_WINDOW else set()
        got_clean = {k for k, _ in leaks(BODY, m)}
        if got_clean != expect:
            report["clean_false_leaks"].append([dev, leaks(BODY, m)])
        elif expect:
            report["year_trap_fired"].append(dev)
        t = planted(m)
        found = leaks(t, m)
        got = {k for k, _ in found}
        want = set(KINDS) - ({"journal"} if not m.get("journal") else set())
        values = {v for _, v in found}
        for extra in ("Selection Effects", "repository cover page 1"):
            if extra not in values:
                got.discard("cover")
                want.add(f"cover: {extra}")
        # leaks() normalizes the way redact() does, so a shared blind spot
        # passes the residual check; the curly-quote citation is checked by name
        if not any(k == "citation" and "Thaler" in v for k, v in found):
            want.add("citation: curly apostrophe")
        if want - got:
            report["planted_missed"].append([dev, sorted(want - got)])
        f = fuzzy(m)
        if len({x for x in re.findall(r"[a-z0-9]+", _norm(m["title"]).lower())
                if len(x) >= 4 and x not in STOP}) < 4:
            report["fuzzy_not_applicable"] += 1
        elif not _fuzzy_title_spans(f, m["title"]):
            report["fuzzy_missed"].append([dev, f])
        # scanned type: a letter-spaced surname, and a journal name with
        # broken spacing (e.g. "PS YC HOLOGICA L SC IENCE")
        sur = _norm(m["authors"][0])
        if len(sur) >= 3 and "author" not in {k for k, _ in leaks(" ".join(sur), m)}:
            report["spaced_missed"].append([dev, " ".join(sur)])
        jw = re.sub(r"[^A-Za-z0-9]", "", _norm(m.get("journal", "")))
        broken = ""
        if len(_norm(m.get("journal", "")).split()) >= 2 and len(jw) >= 12:
            broken = " ".join(jw[i:i + 3].upper() for i in range(0, len(jw), 3))
            if "title_or_journal" not in {k for k, _ in leaks(broken, m)}:
                report["spaced_missed"].append([dev, broken])
        red = redact(t + "\n" + f + "\n" + " ".join(sur) + "\n" + broken, m)
        r = leaks(red, m)
        r += [("correspondence", x) for x in ("Elm Street", "Springfield", "Port Mesa")
              if x in red]
        if r:
            report["redacted_residual"].append([dev, r])
    ok = not any(report[k] for k in ("clean_false_leaks", "planted_missed",
                                     "fuzzy_missed", "spaced_missed",
                                     "redacted_residual",
                                     "metadata_errors"))
    report["verdict"] = "PASS" if ok else "FAIL"
    print(json.dumps(report, indent=1)[:5000])
    with open(HERE / "k2_blinding_test_result.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
