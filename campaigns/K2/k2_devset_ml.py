#!/usr/bin/env python
"""K2 development set, part 2: the Many Labs originals, with DOIs.

PREREG-K2-DRAFT.md Section 7.1. Sources, all public mirrors of the projects'
own files (OSF was offline for migration when this was written):

    ML1  ManyLabsOpenScience/ManyLabs1, ML_Original_ES95CI.xls, "Reference"
         column (the caller passes its path; SHA-256 recorded)
    ML2  ManyLabsOpenScience/ManyLabs2, the per-effect folder names under
         OSFdata/ ("Framing (Tversky & Kahneman, 1981)"), read from the
         GitHub contents API
    ML4  one effect, named in the ML4 article's own title (mortality salience,
         Greenberg et al. 1994)
    ML3  NOT sourced here: no public file outside OSF lists its originals.
         Written as pending, never filled from memory.
    ML5  its originals are RP:P studies: reported as overlap with the RP:P
         list, never as new entries.

Each original (first author, year) is accepted only if the Many Labs article's
own Crossref reference list cites a work with that first author and year. Its
DOI is taken from that reference, or, if the reference has none, from a
Crossref search verified on first author and year. More than one citing match
is written as ambiguous. Outcomes are not read (Section 7.1 consequence 5).

    python k2_devset_ml.py ML1_Original_ES95CI.xls devset_rpp.csv devset_ml.csv
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

import xlrd

ML_DOI = {"ML1": "10.1027/1864-9335/a000178", "ML2": "10.1177/2515245918810225",
          "ML3": "10.1016/j.jesp.2015.10.012", "ML4": "10.1525/collabra.35271",
          "ML5": "10.1177/2515245920958687"}
ML2_TREE = ("https://api.github.com/repos/ManyLabsOpenScience/ManyLabs2/"
            "contents/OSFdata")
UA = {"User-Agent": "pe-k2-devset/0.1 (philosophy-engineering)"}
FIELDS = ["dev_id", "source", "effect", "first_author", "year", "citation",
          "doi", "doi_status", "cited_title"]


def get(url: str):
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as fh:
                return json.load(fh)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", s.lower())


def parse_ref(text: str) -> tuple[str, str]:
    """'Oppenheimer et al., 2009' / 'Carter et al., 2011; Study 2' -> (a, y)."""
    m = re.match(r"\s*([A-Za-z' -]+?)(?:,| et al| &| and).*?(\d{4})", text)
    return (m.group(1).strip(), m.group(2)) if m else ("", "")


def cited(refs: list, author: str, year: str) -> list:
    a = fold(author.split()[-1])
    out = []
    for r in refs:
        ra = fold(r.get("author", "")) or fold(r.get("unstructured", "")[:40])
        if a and a in ra and str(r.get("year", "")).startswith(year):
            out.append(r)
        elif a and r.get("unstructured") and \
                fold(r["unstructured"]).startswith(a) and year in r["unstructured"]:
            out.append(r)
    return out


def search_doi(ref: dict, author: str, year: str) -> tuple[str, str]:
    q = ref.get("article-title") or ref.get("unstructured") or ""
    if not q:
        return "", "cited; no DOI and no title in the reference"
    res = get("https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": f"{q} {author} {year}", "rows": "5"}))
    for it in res["message"]["items"]:
        fam = fold((it.get("author") or [{}])[0].get("family", ""))
        yr = str((it.get("issued", {}).get("date-parts") or [[None]])[0][0])
        if fam == fold(author.split()[-1]) and yr == year:
            return it["DOI"].lower(), "cited; DOI by Crossref search, verified on first author+year"
    return "", "cited; no DOI found (pre-DOI or book likely)"


# Originals missing from the Many Labs reference lists as DOIs. The title is
# supplied here by the script's author (a search key, not evidence); a DOI is
# accepted only if Crossref's record agrees on first author, year AND title.
TITLE_HINTS = {
    ("Caruso", "2012"): "Mere exposure to money increases endorsement of "
                        "free-market systems and social inequality",
    ("Critcher", "2008"): "Incidental environmental anchors",
}


def hinted(author: str, year: str) -> tuple[str, str, str]:
    hint = TITLE_HINTS.get((author, year))
    if not hint:
        return "", "unresolved: not found in the Many Labs article's reference list", ""
    res = get("https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": f"{hint} {author}", "rows": "5"}))
    for it in res["message"]["items"]:
        fam = fold((it.get("author") or [{}])[0].get("family", ""))
        yr = str((it.get("issued", {}).get("date-parts") or [[None]])[0][0])
        title = (it.get("title") or [""])[0]
        # +-1 year: an "in press" citation, or online vs print issue dates
        if fam == fold(author) and yr.isdigit() and abs(int(yr) - int(year)) <= 1                 and fold(title).startswith(fold(hint)[:30]):
            return it["DOI"].lower(), ("not a DOI in the Many Labs reference list; "
                                       "DOI by Crossref search on a title hint, "
                                       "verified on first author+title, year "
                                       f"within 1 (Crossref {yr})"), title
    return "", "unresolved: title hint found no agreeing Crossref record", ""


def pubmed_doi(pmid: str) -> tuple[str, str]:
    m = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
            f"db=pubmed&retmode=json&id={pmid}")["result"][pmid]
    doi = next((a["value"] for a in m.get("articleids", [])
                if a["idtype"] == "doi"), "")
    return doi.lower(), m.get("title", "")


def resolve(refs, author, year, coauthor="", taken=frozenset()):
    hits = cited(refs, author, year)
    if coauthor and len(hits) > 1:
        hits = [h for h in hits if fold(coauthor) in
                [fold(x) for x in h.get("authors", [])]] or hits
    how = ""
    if len(hits) > 1:
        rest = [h for h in hits if h.get("DOI", "").lower() not in taken]
        if len(rest) == 1:
            hits, how = rest, " (by elimination: the other candidate is assigned to another effect)"
    if not hits:
        return hinted(author, year)
    if len({(h.get("DOI") or h.get("unstructured", "")[:60]) for h in hits}) > 1:
        return "", "ambiguous: several cited works match first author+year: " + \
            "; ".join(h.get("DOI", "no-doi") for h in hits), ""
    h = hits[0]
    if h.get("DOI"):
        return h["DOI"].lower(), ("matched: cited by the Many Labs article "
                                  "(DOI in its reference)" + how), h.get("article-title", "")
    doi, status = search_doi(h, author, year)
    return doi, status, h.get("article-title", "")


EXPAND_FAILED = []


def expand(refs: list) -> list:
    """Crossref deposits many references as a bare DOI: fetch each cited
    work's first author, year and title so it can be matched."""
    out = []
    for r in refs:
        if r.get("DOI") and not r.get("authors"):
            try:
                try:
                    m = get("https://api.crossref.org/works/" +
                            urllib.parse.quote(r["DOI"]))["message"]
                except Exception:
                    time.sleep(30)
                    m = get("https://api.crossref.org/works/" +
                            urllib.parse.quote(r["DOI"]))["message"]
                r = {**r,
                     "author": (m.get("author") or [{}])[0].get("family", ""),
                     "authors": [a.get("family", "") for a in m.get("author") or []],
                     "year": str((m.get("issued", {}).get("date-parts")
                                  or [[""]])[0][0]),
                     "article-title": (m.get("title") or [""])[0]}
            except Exception:
                EXPAND_FAILED.append(r["DOI"])  # reported in the summary
            time.sleep(0.5)
        out.append(r)
    return out


def main() -> int:
    xls, rpp_csv, out = sys.argv[1:4]
    refs = {k: expand(get(f"https://api.crossref.org/works/{d}")["message"]
                      .get("reference", []))
            for k, d in ML_DOI.items() if k != "ML3"}
    rows, src = [], {}

    raw = open(xls, "rb").read()
    src["ML1_xls_sha256"] = hashlib.sha256(raw).hexdigest()
    sh = xlrd.open_workbook(file_contents=raw).sheet_by_index(0)
    seen = {}
    for i in range(1, sh.nrows):
        effect, ref = str(sh.cell_value(i, 1)), str(sh.cell_value(i, 2))
        if not ref.strip():
            continue
        seen.setdefault(ref.split(";")[0].strip(), []).append(effect)
    ml1 = []
    for ref, effects in seen.items():
        a, y = parse_ref(ref)
        m = re.search(r"(?:&| and) ([A-Z][A-Za-z]+)", ref)
        ml1.append([ref, effects, a, y, m.group(1) if m else ""])
    for second_pass in (False, True):
        taken = frozenset(r["doi"] for r in rows if r["doi"])
        for item in ml1:
            ref, effects, a, y, co = item[:5]
            if len(item) > 5 and item[5]["doi"]:
                continue
            doi, status, title = resolve(refs["ML1"], a, y, co,
                                         taken if second_pass else frozenset())
            row = {"source": "ML1", "effect": " | ".join(effects),
                   "first_author": a, "year": y, "citation": ref, "doi": doi,
                   "doi_status": status, "cited_title": title}
            if len(item) > 5:
                rows[rows.index(item[5])] = row
                item[5] = row
            else:
                rows.append(row)
                item.append(row)
            time.sleep(1)

    names = [e["name"] for e in get(ML2_TREE) if e["type"] == "dir"
             and not e["name"].startswith("!!")]
    src["ML2_folders"] = len(names)
    by = {}
    for n in names:
        m = re.match(r"(.+?) \((.+?), (\d{4})\)$", n)
        by.setdefault((m.group(2), m.group(3)), []).append(m.group(1))
    for (cit, y), effects in by.items():
        a = re.split(r" et al\.| & ", cit)[0].strip()
        doi, status, title = resolve(refs["ML2"], a, y)
        rows.append({"source": "ML2", "effect": " | ".join(effects),
                     "first_author": a, "year": y, "citation": f"{cit}, {y}",
                     "doi": doi, "doi_status": status, "cited_title": title})
        time.sleep(1)

    # The ML4 repository README (raklein/ml4) names the original as
    # Greenberg et al., 1994, study 1, linked to PubMed 7965609.
    doi, title = pubmed_doi("7965609")
    doi = doi.replace("//", "/")  # PubMed carries APA's legacy "10.1037//" form
    rows.append({"source": "ML4", "effect": "Mortality salience (worldview defense)",
                 "first_author": "Greenberg", "year": "1994",
                 "citation": "Greenberg et al., 1994, study 1",
                 "doi": doi, "cited_title": title,
                 "doi_status": ("from PubMed 7965609, the ID the ML4 repository "
                                "README links" if doi else
                                "unresolved: PubMed record has no DOI")})
    rows.append({"source": "ML3", "effect": "(10 effects)", "first_author": "",
                 "year": "", "citation": "", "doi": "",
                 "doi_status": "pending: ML3's original list is sourced from OSF only; "
                               "not filled from memory"})

    for i, r in enumerate(rows, 1):
        r["dev_id"] = f"DEV-ML-{i:03d}"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, FIELDS)
        w.writeheader()
        w.writerows(rows)

    rpp = {r["doi"] for r in csv.DictReader(open(rpp_csv, encoding="utf-8")) if r["doi"]}
    ml5 = {r["DOI"].lower() for r in refs["ML5"] if r.get("DOI")}
    ml_dois = [r["doi"] for r in rows if r["doi"]]
    summary = {**src,
               "entries": len(rows),
               "by_source": {s: sum(r["source"] == s for r in rows)
                             for s in ("ML1", "ML2", "ML3", "ML4")},
               "doi_resolved": len(ml_dois),
               "no_doi": [[r["dev_id"], r["citation"], r["doi_status"]]
                          for r in rows if not r["doi"]],
               "reference_lookups_failed": EXPAND_FAILED,
               "ml_rpp_overlap": sorted(set(ml_dois) & rpp),
               "ml_internal_duplicates": sorted(
                   {d for d in ml_dois if ml_dois.count(d) > 1}),
               "distinct_articles_rpp_plus_ml": len(set(ml_dois) | rpp),
               "ml5_refs_in_rpp_list": len(ml5 & rpp),
               "ml5_refs_with_doi": len(ml5)}
    print(json.dumps(summary, indent=1))
    with open(out.replace(".csv", "_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
