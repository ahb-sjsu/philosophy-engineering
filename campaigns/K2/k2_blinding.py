#!/usr/bin/env python
"""K2 blinding (registration 4.1) and its automated check, gate I3.

    redact(text, meta) -> text with the identifying fields removed
    leaks(text, meta)  -> list of (kind, matched text); empty means I3 passes

`meta` is the article's Crossref record as k2_fulltext_fetch.py stores it:
title, authors (surnames), given (given names), journal, journal_short,
year, volume, page, doi. HTML entities in it are decoded ("&amp;" -> "&").
The check runs on whatever text an auditor will see and does not trust the
redaction.

What counts as a leak:

    doi          any DOI-shaped string, not only the article's own
    url, email   any URL or e-mail address
    title        the full title anywhere; in the front matter (first FRONT
                 characters) also any run of TITLE_RUN consecutive title
                 words, or a window holding at least TITLE_FUZZ of the
                 title's content words (a cover page that drops or adds a
                 word, or misspells one, still names the article). Partial
                 matches are not applied to the body because a title often
                 names the construct coders must see (a first intake blanked
                 an article's construct about 46 times); cost: a body
                 sentence that restates most of the title is left in
    author       a surname or given name (3+ letters) as a whole word, as
                 written or in capitals ("SHAFIR")
    journal      the full name and each Crossref short name; names of two or
                 more words case-insensitively, a one-word name ("Cognition")
                 case-sensitively, so the ordinary word survives
    year         a year within YEAR_WINDOW of publication (a working paper or
                 online-first year differs from the issue year); cost: such
                 numbers are redacted from the body too
    citation     a capitalized word followed by a year ("Smith, 2005",
                 "Bless 1990", "et al. (2005)", "August 2009"), with the
                 author list before it ("Hoang and Rothaermel (2005)",
                 "Rabe, Lee, and Taylor 2010"); the newest cited year bounds
                 the publication year
    name_residue on redacted text, a particle, initials or a co-author ("Hoang
                 and [REDACTED]") still beside a redaction mark
    biblio       the article's page range, "pp." with its first page, and
                 "Vol." / "Volume" with a number
    institution  "University of X", "X University", "Institute", "College"
                 and their German and French forms: affiliations narrow the
                 authors
    cover        any line naming a running head, a suggested citation, a
                 repository or publisher stamp ("Research Portal", "First
                 publ. in", "Published online by", "version of record",
                 "Downloaded from", "©"); the whole line is removed. Also a
                 short line repeated on 3+ lines (a running head without a
                 label) and a whole page carrying 2+ repository cover markers
                 ("General rights", "Take down", "Nutzungsbedingungen", ...),
                 and a correspondence footnote ("Address correspondence to",
                 "Corresponding author", ...) to its paragraph's end, at most
                 6 lines

Every rule also runs on a copy with letter-spaced runs joined ("N o r b e r
t" -> "Norbert", scanned type), and the title and journal (two or more
words, 12+ letters) are also matched on letters and digits only
(title_or_journal), so broken spacing ("PS YC HOLOGICA L SC IENCE") cannot
hide them.

Not checked, stated limits: place names ("Princeton, New Jersey"),
institutes named without University/College/Institute (a research centre's
acronym), abbreviations Crossref does not list, grant
numbers, acknowledgments that name people without a year, and the content
of the study itself (a famous paradigm can identify a famous study).

Stdlib only, like k2_analysis: the registered check must not change with a
library upgrade between seal and run.
"""
from __future__ import annotations

import html
import re
import unicodedata

TITLE_RUN = 6
TITLE_FUZZ = 0.75
FRONT = 4000  # characters treated as front matter for partial title matches
YEAR_WINDOW = 2
STOP = set("a an and the of in on for to with from by at as or is are be its "
           "their this that than into over under during".split())

DOI = re.compile(r"\b10\.\d{4,9}/\S+", re.I)
URL = re.compile(r"\b(?:https?://|www\.)\S+|\b\S+\.(?:org|com|edu|io|de|nl|uk)/\S*", re.I)
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
YEAR = r"(?:1[89]|20)\d\d[a-z]?"
# a cited author list: "Hoang and Rothaermel (2005)", "Rabe, Lee, and Taylor
# 2010", "Anand & Khanna 2000". Without it only the name before the year went
# and the first authors stayed ("Hoang and [REDACTED]", v2 development papers,
# 2026-10-25). Cost: a capitalized word before "and" goes with the list
# ("However, Smith and Lee (2005)" loses "However")
_CNAME = r"[A-Z][\w'\-]+"
_CLIST = rf"(?:{_CNAME},\s+){{0,5}}{_CNAME},?\s+(?:and|&)\s+"
CITATION = re.compile(
    rf"\b(?:{_CLIST})?{_CNAME}(?:\s+et\s+al\.?)?,?\s+\(?\s*" + YEAR + r"\b"
    r"|\(\s*[A-Z][^()]{0,80}?,\s*" + YEAR + r"\s*[;)]")
INSTITUTION = re.compile(
    r"(?:\b[A-Z][\w.&'\-]*\s+){0,4}"
    r"(?:University|College|Institute|Universit[äa]t|Universit[ée]|Hochschule|"
    r"Department|Dept\.|School|Laboratory|Center|Centre)"
    r"(?:\s+(?:of|for|at|de|du|zu)(?:\s+(?:and\s+|&\s+)?[A-Z][\w.'\-]*){1,5})?")
VOLUME = re.compile(r"\b(?:Vol\.|Volume)\s*\d+", re.I)
COVER = re.compile(
    r"^.*(?:running\s+head|suggested\s+citation|empfohlene\s+zitierung|"
    r"research\s+portal|first\s+publ|published\s+online\s+by|version\s+of\s+record|"
    r"downloaded\s+from|citation\s+for\s+published\s+version|©|\(c\)\s*\d{4}|"
    # PubMed Central page stamps: "J Pers Soc Psychol. Author manuscript;
    # available in PMC 2010 ..." names the journal (NLM abbreviation) and year
    r"author\s+manuscript|available\s+in\s+pmc|nih-pa|hhs\s+public\s+access|"
    r"europe\s+pmc\s+funders).*$",
    re.I | re.M)
# a correspondence footnote, to the paragraph's end (at most 6 lines): its
# street address and city outlive the name rules (DEV-RPP-070, whose page-2
# footnote reached the coding unit through the Method lead, 2026-10-18)
CORRESPONDENCE = re.compile(
    r"^.*(?:address\s+correspondence|correspondence\s+(?:concerning|should|to|"
    r"regarding|may)|corresponding\s+author|reprint\s+requests|requests\s+for\s+reprints)"
    r".*(?:\n(?!\s*\n).*){0,5}",
    re.I | re.M)
# what redaction leaves around a removed name: a surname particle ("Van
# [REDACTED]", "van der [REDACTED]") or initials ("A. B. [REDACTED]",
# "[REDACTED], A. B."); built per mark in _name_residue
PARTICLES = r"(?:(?:[Vv]an|[Vv]on|[Dd]e|[Dd]er|[Dd]en|[Dd]i|[Dd]u|[Ll]a|[Ll]e|[Tt]er|[Tt]en)\s+)+"
INITIALS = r"(?:[A-Z]\.\s?){1,3}"


def _name_residue(mark: str) -> re.Pattern:
    m = re.escape(mark)
    # a capitalized part hyphen-joined to a mark is the rest of a hyphenated
    # name too short for the name rules ("Chen-Bo" -> "[REDACTED]-BO")
    # a capitalized word joined to a mark by "and" / "&" is a co-author the
    # citation rule missed ("Portegijs and [REDACTED]")
    return re.compile(rf"\b{PARTICLES}{m}|\b{INITIALS}\s?{m}|{m},?\s{INITIALS}(?=[,;&)]|\s|$)"
                      rf"|{m}-[A-Z][\w']*|\b[A-Z][\w']*-{m}"
                      rf"|\b{_CNAME},?\s+(?:and|&)\s+{m}")


# curly quotes as straight ones: "Thaler’s (1985)" must match the citation
# rule and "Objects’ Typical Location" the title (second intake, 2026-10-18)
_QUOTES = str.maketrans({"‘": "'", "’": "'", "‚": "'", "‛": "'",
                         "′": "'", "“": '"', "”": '"', "„": '"'})


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", html.unescape(s or "")).translate(_QUOTES)
    return "".join(c for c in s if not unicodedata.combining(c))


def _words(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", _norm(s).lower())


def _title_runs(title: str) -> list[list[str]]:
    w = _words(title)
    if len(w) <= TITLE_RUN:
        return [w] if w else []
    return [w] + [w[i:i + TITLE_RUN] for i in range(len(w) - TITLE_RUN + 1)]


def _word_span(words: list[str], flags: int = re.I) -> re.Pattern:
    # words separated by any non-alphanumeric run, so punctuation, line breaks
    # and hyphenation do not hide a title
    return re.compile(r"\b" + r"[^a-z0-9]+".join(map(re.escape, words)) + r"\b", flags)


def _dehyphenate(s: str) -> str:
    # "Tra-" at a line end then "cing" is "Tracing" in a PDF text layer
    return re.sub(r"(\w)-[ \t]*\n\s*(\w)", r"\1\2", s)


def _names(meta: dict) -> list[str]:
    out = []
    for n in list(meta.get("authors", [])) + list(meta.get("given", [])):
        for part in re.split(r"[\s\-]+", _norm(n)):
            part = part.strip(".")
            if len(part) >= 3:
                out.append(part)
    return sorted(set(out))


def _rules(meta: dict) -> list[tuple[str, re.Pattern]]:
    """Every regex rule, in the order redact() applies them."""
    # title and journal before citations: "Memory & Cognition 1993" must go
    # as a journal name, not leave "Memory &" behind a citation match
    rules: list[tuple[str, re.Pattern]] = [("cover", CORRESPONDENCE), ("cover", COVER)]
    # the full title anywhere; partial and fuzzy title matches only in the
    # front matter (_front_title_spans), because a title often names the
    # study's construct and the body must keep it for coders
    full = _words(meta.get("title", ""))
    if full:
        rules.append(("title", _word_span(full)))
    names = [meta.get("journal", "")] + list(meta.get("journal_short", []))
    for name in {_norm(n).strip() for n in names if n and n.strip()}:
        w = _words(name)
        if len(w) >= 2:
            rules.append(("journal", _word_span(w)))
        elif w:
            rules.append(("journal", re.compile(r"\b" + re.escape(name.strip(" .")) + r"\b")))
    rules += [("citation", CITATION), ("doi", DOI), ("url", URL), ("email", EMAIL)]
    for name in _names(meta):
        rules.append(("author", re.compile(r"\b(?:" + re.escape(name) + "|"
                                           + re.escape(name.upper()) + r")\b")))
    year = str(meta.get("year", "")).strip()
    if year.isdigit():
        y = int(year)
        alts = "|".join(str(v) for v in range(y - YEAR_WINDOW, y + YEAR_WINDOW + 1))
        rules.append(("year", re.compile(r"(?<!\d)(?:" + alts + r")(?!\d)")))
    page = _norm(str(meta.get("page", ""))).strip()
    first = re.match(r"\d+", page)
    if first:
        rules.append(("biblio", re.compile(r"\bpp?\.\s*" + first.group(0) + r"\b")))
        last = re.search(r"[-‐-―](\d+)\s*$", page)
        if last:
            rules.append(("biblio", re.compile(
                r"(?<!\d)" + first.group(0) + r"\s*[-‐-―]\s*" + last.group(1) + r"(?!\d)")))
    rules += [("biblio", VOLUME), ("institution", INSTITUTION)]
    return rules


SECTION_WORDS = set("method methods results discussion general participants procedure "
                    "design materials experiment experiments study studies overview "
                    "apparatus stimuli data analysis analyses and of introduction "
                    "conclusion conclusions table figure note notes".split())
COVER_PAGE = re.compile(
    r"general\s+rights|take\s+down|nutzungsbedingungen|terms\s+of\s+use|"
    r"provided\s+in\s+cooperation\s+with|this\s+version\s+is\s+available|"
    r"research\s+portal|deposit-lizenz|ssoar|repository|link\s+to\s+publication",
    re.I)


def _repeated_lines(text: str) -> set[str]:
    """Running heads and footers without a label: a short line that recurs on
    3 or more lines and is not a section heading or a bare number."""
    counts: dict[str, int] = {}
    for line in text.splitlines():
        key = re.sub(r"\s*\d+\s*", " ", line).strip()
        w = _words(key)
        # 2+ real words, so a repeated table header such as "M SD" is kept
        if (2 <= len(w) <= 8 and sum(len(x) >= 3 for x in w) >= 2
                and not set(w) <= SECTION_WORDS):
            counts[key] = counts.get(key, 0) + 1
    return {k for k, n in counts.items() if n >= 3}


def _cover_pages(text: str) -> list[int]:
    """Pages (form-feed separated) carrying 2+ repository cover markers."""
    return [i for i, page in enumerate(text.split("\f"))
            if len({m.group(0).lower() for m in COVER_PAGE.finditer(page)}) >= 2]


def _fuzzy_title_spans(text: str, title: str) -> list[tuple[int, int]]:
    content = [w for w in _words(title) if len(w) >= 4 and w not in STOP]
    need = set(content)
    if len(need) < 4:
        return []
    toks = [(m.group(0).lower(), m.start(), m.end())
            for m in re.finditer(r"[A-Za-z0-9]+", text)]
    width = len(_words(title)) + 3
    spans, i = [], 0
    while i < len(toks):
        win = toks[i:i + width]
        hit = [t for t in win if t[0] in need]
        if hit and hit[0] is toks[i] and len({t[0] for t in hit}) >= TITLE_FUZZ * len(need):
            spans.append((hit[0][1], hit[-1][2]))
            i += width
        else:
            i += 1
    return spans


def _unspace(s: str) -> str:
    """Letter-spaced type in scans ("N o r b e r t"): join runs of 3 or more
    single letters separated by single spaces."""
    return re.sub(r"\b[A-Za-z](?: [A-Za-z]){2,}\b",
                  lambda m: m.group(0).replace(" ", ""), s)


def _squashed_spans(text: str, meta: dict) -> list[tuple[int, int]]:
    """Title and journal (two or more words) matched on letters and digits
    only, so broken spacing ("PS YC HOLOGICA L SC IENCE") cannot hide them.
    Returns spans in `text`, merged and sorted."""
    keep = [(i, c.lower()) for i, c in enumerate(text) if c.isalnum()]
    flat = "".join(c for _, c in keep)
    targets = [meta.get("title", ""), meta.get("journal", "")]
    targets += list(meta.get("journal_short", []))
    spans = []
    for t in targets:
        if len(_words(t)) < 2:
            continue
        sq = "".join(_words(t))
        if len(sq) < 12:
            continue
        for m in re.finditer(re.escape(sq), flat):
            spans.append((keep[m.start()][0], keep[m.end() - 1][0] + 1))
    spans.sort()
    merged: list[tuple[int, int]] = []
    for a, b in spans:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


def _squashed_hits(text: str, meta: dict) -> list[tuple[str, str]]:
    return [("title_or_journal", text[a:b]) for a, b in _squashed_spans(text, meta)]


def _front_title_spans(text: str, meta: dict) -> list[tuple[int, int]]:
    """Partial (TITLE_RUN words) and fuzzy title matches in the first FRONT
    characters: the title block, a cover page, a first-page header."""
    front = text[:FRONT]
    spans = _fuzzy_title_spans(front, meta.get("title", ""))
    for run in _title_runs(meta.get("title", ""))[1:]:
        spans += [m.span() for m in _word_span(run).finditer(front)]
    spans.sort()
    merged: list[tuple[int, int]] = []
    for a, b in spans:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


def leaks(text: str, meta: dict) -> list[tuple[str, str]]:
    # checked on the text, a de-hyphenated copy and a letter-joined copy; a
    # hit in any counts
    variants = [_norm(text), _dehyphenate(_norm(text)), _unspace(_norm(text))]
    plain = "\n".join(variants)
    found = [(kind, "letters only: " + x) for kind, x in _squashed_hits(plain, meta)]
    found += [(kind, m.group(0).strip()) for kind, rx in _rules(meta)
              for m in rx.finditer(plain) if m.group(0).strip()]
    found += [("title", v[a:b]) for v in variants
              for a, b in _front_title_spans(v, meta)]
    found += [("cover", k) for k in _repeated_lines(_norm(text))]
    found += [("cover", f"repository cover page {i + 1}") for i in _cover_pages(_norm(text))]
    # on redacted text: a particle or initials still beside a redaction mark
    found += [("name_residue", m.group(0)) for m in _name_residue("[REDACTED]").finditer(text)]
    return found


def _drop_author_blocks(text: str, mark: str) -> str:
    """An author block after redaction: a line of marks only, and under it up
    to two affiliation lines that begin with a mark and go on in capitalized
    words only ("[REDACTED], San Diego"). The city outlives the institution
    rule (DEV-RPP-070, page 2, reached the unit through the Method lead)."""
    m = re.escape(mark)
    names = re.compile(rf"^[\s,&]*(?:(?:{m}|and)[\s,.&-]*)+$")
    affil = re.compile(rf"^\s*{m}(?:[\s,&]+(?:{m}|[A-Z][\w.'\-]*|of|at|and|de))*[\s,.]*$")
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        if names.match(lines[i]) and mark in lines[i]:
            i += 1
            for _ in range(2):
                if i < len(lines) and affil.match(lines[i]):
                    i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def redact(text: str, meta: dict, mark: str = "[REDACTED]") -> str:
    """Remove what leaks() looks for: repository cover pages and repeated
    running heads first, then cover lines, title and journal, then citations
    (so a surname inside a citation does not leave a dangling year), then the
    rest."""
    pages = _norm(text).split("\f")
    drop = set(_cover_pages(_norm(text)))
    out = "\f".join(p for i, p in enumerate(pages) if i not in drop)
    heads = _repeated_lines(out)
    out = "\n".join(line for line in out.splitlines()
                    if re.sub(r"\s*\d+\s*", " ", line).strip() not in heads)
    out = _unspace(_dehyphenate(out))
    for a, b in reversed(_squashed_spans(out, meta)):
        out = out[:a] + mark + out[b:]
    for a, b in reversed(_front_title_spans(out, meta)):
        out = out[:a] + mark + out[b:]
    for kind, rx in _rules(meta):
        out = rx.sub("" if kind == "cover" else mark, out)
    # particles and initials left beside a removed name join it (repeated,
    # since "A. van [REDACTED]" takes two passes)
    rx = _name_residue(mark)
    while rx.search(out):
        out = rx.sub(mark, out)
    out = _drop_author_blocks(out, mark)
    # a running head longer than 8 words ("D.M. Name et al. / Journal of ...
    # 45 (2009) 867-872") only becomes short enough to count as repeated once
    # its fields are redacted, and its initials stay behind; drop such lines
    while heads := _repeated_lines(out):
        out = "\n".join(line for line in out.splitlines()
                        if re.sub(r"\s*\d+\s*", " ", line).strip() not in heads)
    return out
