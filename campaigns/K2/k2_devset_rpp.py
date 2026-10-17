#!/usr/bin/env python
"""K2 development set, part 1: the RP:P originals, with DOIs.

PREREG-K2-DRAFT.md Section 7.1. Reads the Reproducibility Project: Psychology
master data file (CenterForOpenScience/rpp, data_allformats/
RPPdataConverted.csv; the caller passes its path and the script records its
SHA-256), keeps the 100 completed replications, and resolves each original
article's DOI through the Crossref REST API, filtered to the article's journal
ISSN and to 2008.

A DOI is accepted only when Crossref's record agrees with the RP:P row on
volume, first page AND main title. Anything else is written as unresolved,
never guessed.

The output carries bibliographic fields only. Replication outcomes are
deliberately left out: Section 7.1 consequence 5 forbids using development-set
outcomes to shape the rubric, and a file without them cannot be used that way.
The contamination probe (7.3) reads outcomes from the source file by hash.

    python k2_devset_rpp.py RPPdataConverted.csv devset_rpp.csv
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request

ISSN = {"PS": "0956-7976", "JPSP": "0022-3514", "JEPLMC": "0278-7393"}
JOURNAL = {"PS": "Psychological Science",
           "JPSP": "Journal of Personality and Social Psychology",
           "JEPLMC": "Journal of Experimental Psychology: Learning, Memory, and Cognition"}
FIELDS = ["dev_id", "source", "rpp_local_id", "journal", "volume", "issue",
          "pages", "study_number", "title", "authors", "doi", "doi_status",
          "crossref_title"]


MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
          "oct", "nov", "dec"]


def first_page_candidates(pages: str) -> tuple[list[str], bool]:
    """First-page candidates, undoing a spreadsheet date coercion.

    The RP:P master file stores some page ranges as dates ("1-15" became
    "15-jan"; "22-4", RP:P's abbreviation of 22-24, probably became "22-apr").
    PE-CLS-1.0 s7.6 I2's defect family. Which of month-day or day-month the
    spreadsheet used is not recoverable from the cell, so both readings are
    candidates and Crossref decides; the row is flagged either way.
    """
    m = re.fullmatch(r"\s*(\d{1,2})-([A-Za-z]{3})\s*", pages or "")
    if m and m.group(2).lower() in MONTHS:
        return [m.group(1), str(MONTHS.index(m.group(2).lower()) + 1)], True
    return [first_page(pages)], False


def same_title(rpp: str, cr: str) -> bool:
    """Crossref often drops the subtitle; compare main titles."""
    cr = re.sub(r"<[^>]+>", "", cr)  # Crossref titles can carry JATS markup
    a = re.sub(r"[^a-z0-9 ]", "", rpp.lower().split(":")[0])
    b = re.sub(r"[^a-z0-9 ]", "", cr.lower().split(":")[0])
    a, b = " ".join(a.split()), " ".join(b.split())
    return bool(b) and (a.startswith(b) or b.startswith(a))


def first_page(pages: str) -> str:
    m = re.match(r"\s*([A-Za-z]?\d+)", pages or "")
    return m.group(1) if m else ""


def crossref(row: dict) -> tuple[str, str, str]:
    q = urllib.parse.urlencode({
        "query.bibliographic": f"{row['Study.Title.O']} {row['Authors.O']}",
        "filter": f"issn:{ISSN[row['Journal.O']]},from-pub-date:2008-01-01,"
                  f"until-pub-date:2008-12-31",
        "rows": "5"})
    req = urllib.request.Request(
        "https://api.crossref.org/works?" + q,
        headers={"User-Agent": "pe-k2-devset/0.1 (philosophy-engineering)"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as fh:
                items = json.load(fh)["message"]["items"]
            break
        except Exception as exc:  # network: retry, then report, never guess
            if attempt == 3:
                return "", f"unresolved: {type(exc).__name__}", ""
            time.sleep(5 * (attempt + 1))
    vol = row["Volume.O"].strip()
    fps, _ = first_page_candidates(row["Pages.O"])
    near = ""
    for it in items:
        title = (it.get("title") or [""])[0]
        if it.get("volume", "").strip() == vol and \
                first_page(it.get("page", "")) in fps:
            if same_title(row["Study.Title.O"], title):
                return it["DOI"].lower(), \
                    "matched: issn+volume+first-page+title", title
            near = near or f"; volume+page agree but title differs ({it['DOI']})"
    return "", "unresolved: no Crossref record agrees on volume, first page " \
               "and title" + near, ""


def main() -> int:
    src, out = sys.argv[1], sys.argv[2]
    raw = open(src, "rb").read()
    rows = list(csv.DictReader(raw.decode("latin-1").splitlines()))
    done = [r for r in rows if r["Completion.R"] == "1"]
    assert len(done) == 100, len(done)
    res = []
    for i, r in enumerate(done, 1):
        _, coerced = first_page_candidates(r["Pages.O"])
        doi, status, ctitle = crossref(r)
        if coerced:
            status += "; pages field is a spreadsheet date in the source"
        res.append({"dev_id": f"DEV-RPP-{i:03d}", "source": "RP:P",
                    "rpp_local_id": r["Local.ID"],
                    "journal": JOURNAL[r["Journal.O"]],
                    "volume": r["Volume.O"], "issue": r["Issue.O"],
                    "pages": r["Pages.O"],
                    "study_number": r["Replicated.study.number.R"],
                    "title": r["Study.Title.O"].strip(),
                    "authors": r["Authors.O"].strip(), "doi": doi,
                    "doi_status": status, "crossref_title": ctitle})
        print(f"{i:3d} {status[:9]:9s} {doi}", flush=True)
        time.sleep(1.0)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, FIELDS)
        w.writeheader()
        w.writerows(res)
    summary = {"source_file": src,
               "source_sha256": hashlib.sha256(raw).hexdigest(),
               "rows_in_source": len(rows), "completed": len(done),
               "doi_matched": sum(bool(r["doi"]) for r in res),
               "distinct_dois": len({r["doi"] for r in res if r["doi"]}),
               "unresolved": [r["dev_id"] for r in res if not r["doi"]],
               "pages_coerced_in_source": [r["dev_id"] for r in res
                                           if "spreadsheet date" in r["doi_status"]],
               "shared_doi": sorted(
                   [r["dev_id"], r["doi"]] for r in res if r["doi"] and
                   sum(s["doi"] == r["doi"] for s in res) > 1)}
    print(json.dumps(summary, indent=1))
    with open(out.replace(".csv", "_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
