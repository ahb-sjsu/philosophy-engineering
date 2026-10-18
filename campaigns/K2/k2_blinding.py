#!/usr/bin/env python
"""K2 blinding (registration 4.1) and its automated check, gate I3.

    redact(text, meta) -> text with the identifying fields removed
    leaks(text, meta)  -> list of (kind, matched text); empty means I3 passes

`meta` holds the article's own title, author surnames, journal, year and DOI.
The check is deliberately stricter than the redaction it audits, and it does
not trust the redaction: it is run on whatever text an auditor will see.

What counts as a leak:

    doi        any DOI-shaped string, not only the article's own
    title      the full title, or any run of TITLE_RUN consecutive title words
    author     an author surname as a whole word (case-sensitive)
    journal    the journal's full name (case-insensitive); abbreviations are
               NOT checked, a stated limit
    year       the publication year as a whole token
    citation   an in-text citation with a year ("Smith, 2005", "et al. (2005)");
               the newest cited year bounds the publication year, so citations
               date the paper even with the reference list removed
    url, email any URL or e-mail address (lab pages, OSF links, contact lines)

Stdlib only, like k2_analysis: the registered check must not change with a
library upgrade between seal and run.
"""
from __future__ import annotations

import re
import unicodedata

TITLE_RUN = 6

DOI = re.compile(r"\b10\.\d{4,9}/\S+", re.I)
URL = re.compile(r"\b(?:https?://|www\.)\S+|\b\S+\.(?:org|com|edu|io)/\S*", re.I)
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
YEAR = r"(?:1[89]|20)\d\d[a-z]?"
CITATION = re.compile(
    r"\b[A-Z][\w'\-]+(?:\s+et\s+al\.?|\s+(?:and|&)\s+[A-Z][\w'\-]+)?"
    r"(?:,\s*|\s+\(\s*)" + YEAR + r"\b"
    r"|\(\s*[A-Z][^()]{0,80}?,\s*" + YEAR + r"\s*[;)]")


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def _words(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", _norm(s).lower())


def _title_runs(title: str) -> list[list[str]]:
    w = _words(title)
    if len(w) <= TITLE_RUN:
        return [w] if w else []
    return [w[i:i + TITLE_RUN] for i in range(len(w) - TITLE_RUN + 1)]


def _word_span_pattern(words: list[str]) -> re.Pattern:
    # words separated by any non-alphanumeric run, so punctuation, line breaks
    # and hyphenation do not hide a title
    return re.compile(r"\b" + r"[^a-z0-9]+".join(map(re.escape, words)) + r"\b")


def _dehyphenate(s: str) -> str:
    # "Tra-" at a line end then "cing" is "Tracing" in a PDF text layer
    return re.sub(r"(\w)-[ \t]*\n\s*(\w)", r"\1\2", s)


def leaks(text: str, meta: dict) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    # checked on the text and on a de-hyphenated copy; a hit in either counts
    plain = _norm(text) + "\n" + _dehyphenate(_norm(text))
    low = plain.lower()
    for kind, rx in (("doi", DOI), ("url", URL), ("email", EMAIL),
                     ("citation", CITATION)):
        found += [(kind, m.group(0)) for m in rx.finditer(plain)]
    for run in _title_runs(meta.get("title", "")):
        m = _word_span_pattern(run).search(low)
        if m:
            found.append(("title", m.group(0)))
    for name in meta.get("authors", []):
        name = _norm(name).strip()
        if name:
            found += [("author", m.group(0)) for m in
                      re.finditer(r"\b" + re.escape(name) + r"\b", plain)]
    journal = _words(meta.get("journal", ""))
    if journal:
        m = _word_span_pattern(journal).search(low)
        if m:
            found.append(("journal", m.group(0)))
    year = str(meta.get("year", "")).strip()
    if year:
        found += [("year", m.group(0)) for m in
                  re.finditer(r"(?<!\d)" + re.escape(year) + r"(?!\d)", plain)]
    return found


def redact(text: str, meta: dict, mark: str = "[REDACTED]") -> str:
    """Remove what leaks() looks for. Citations go first, so an author's
    surname inside a citation does not leave a dangling year behind."""
    out = _dehyphenate(_norm(text))
    for rx in (CITATION, DOI, URL, EMAIL):
        out = rx.sub(mark, out)
    title = _words(meta.get("title", ""))
    for run in ([title] if title else []) + _title_runs(meta.get("title", "")):
        out = re.sub(_word_span_pattern(run).pattern, mark, out, flags=re.I)
    journal = _words(meta.get("journal", ""))
    if journal:
        out = re.sub(_word_span_pattern(journal).pattern, mark, out, flags=re.I)
    for name in meta.get("authors", []):
        name = _norm(name).strip()
        if name:
            out = re.sub(r"\b" + re.escape(name) + r"\b", mark, out)
    year = str(meta.get("year", "")).strip()
    if year:
        out = re.sub(r"(?<!\d)" + re.escape(year) + r"(?!\d)", mark, out)
    return out
