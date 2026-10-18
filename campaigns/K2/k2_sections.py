#!/usr/bin/env python
"""K2 coding unit: the Method and Results sections of an article, and the
stretch before each Method heading; nothing else.

Registration 4.1 (adopted by the owner 2026-10-18). A person's read of six
texts that passed the leak check found identifying residue in all six, nearly
all of it in the front matter (cover pages, title block, first-page header and
footer). So the front matter is dropped, not redacted: coders see only the
text under Method and Results headings, for every study in the article, and
the redaction rules (k2_blinding) run on that text as a second line.

The text from pdftotext is split at heading lines. A KEEP heading (Method,
Results, Participants, ...) opens a kept stretch; a STOP heading (Introduction,
Discussion, Experiment 2, References, ...) closes it. Subheadings inside a
Method section (Design, Procedure, Measures) change nothing. An article with
no Method-type or no Results-type heading is returned with found=False and
goes to a person (k2_intake quarantines it); nothing is guessed.

The unit also keeps the LEAD before each Method heading: up to LEAD characters
of whole lines, where a study's predictions are usually stated (owner,
2026-10-18; on the 23 development articles the Method+Results unit alone kept
a quarter of the A1 Nonvacuity evidence, k2_unit_coverage). A lead never
reaches back past a heading, into a kept stretch or onto page 1, so it does
not run into the front matter or a previous study's discussion; an
"Experiment 2" heading that bounds it is kept, so coders see which study the
lead belongs to.

    from k2_sections import extract
    kept, info = extract(text)
"""
from __future__ import annotations

import re

# a heading line: optional numbering ("2.", "2.1", "II."), the heading words,
# optional colon; short enough not to be a sentence
_NUM = r"(?:(?:\d+(?:\.\d+)*|[IVX]+)\.?\s+)?"
METHOD = (r"methods?|materials?\s+and\s+methods?|methods?\s+and\s+materials?|"
          r"methodology|general\s+methods?|participants(?:\s+and\s+design)?|"
          r"subjects|design\s+and\s+participants")
RESULTS = (r"results|results\s+and\s+discussion|results\s*&\s*discussion|"
           r"general\s+results")
STOP = (r"introduction|overview|discussion|general\s+discussion|conclusions?|"
        r"concluding\s+remarks|summary|limitations|implications|references|"
        r"reference\s+list|bibliography|acknowledge?ments?|author\s+notes?|"
        r"notes|footnotes|appendix(?:\s+[a-z])?|appendices|supplementa\w+(?:\s+\w+)?|"
        r"abstract|keywords")
HEADING = re.compile(rf"^\s*{_NUM}(?P<h>{METHOD}|{RESULTS}|{STOP})\s*:?\s*$", re.I)
# "Experiment 2", "Study 1b: Replication with adults" open a new study; its
# own introduction is not kept, so the line closes a kept stretch
STUDY = re.compile(r"^\s*(?:experiment|study)\s+\d+[a-z]?\b[^.]{0,80}$", re.I)
_KEEP = re.compile(rf"^(?:{METHOD}|{RESULTS})$", re.I)
_IS_METHOD = re.compile(rf"^(?:{METHOD})$", re.I)
_IS_RESULTS = re.compile(rf"^(?:{RESULTS})$", re.I)


def _kind(line: str) -> str | None:
    m = HEADING.match(line)
    if m:
        h = re.sub(r"\s+", " ", m.group("h")).strip()
        if _IS_METHOD.match(h):
            return "method"
        if _IS_RESULTS.match(h):
            return "results"
        return "stop"
    if STUDY.match(line) and len(line.strip()) <= 90:
        return "stop"
    return None


LEAD = 2000


def extract(text: str) -> tuple[str, dict]:
    """Return (kept text, info). info: found (bool), method/results heading
    counts, lead_chars, kept_share (characters kept / characters in)."""
    lines = text.replace("\f", "\n").splitlines()
    kinds = [_kind(line) for line in lines]
    keep = [False] * len(lines)
    on = False
    for i, k in enumerate(kinds):
        if k:
            on = k in ("method", "results")
        keep[i] = on
    n = {k: kinds.count(k) for k in ("method", "results", "stop")}
    # page 1 is front matter (title block, first-page footers with addresses
    # and ISSN lines), so no lead reaches into it
    page1 = len(text.split("\f")[0].splitlines()) if "\f" in text else 0
    lead = [False] * len(lines)
    for i, k in enumerate(kinds):
        if k != "method" or (i and keep[i - 1]):
            continue
        j, size = i - 1, 0
        while j >= page1 and not keep[j] and kinds[j] is None and size < LEAD:
            lead[j], size = True, size + len(lines[j]) + 1
            j -= 1
        if j >= page1 and not keep[j] and kinds[j] == "stop" and STUDY.match(lines[j]):
            lead[j] = True
    kept: list[str] = []
    for i, line in enumerate(lines):
        if not (keep[i] or lead[i]):
            continue
        if kinds[i] or (i and not (keep[i - 1] or lead[i - 1])):
            kept.append("")  # a blank line before each heading and each stretch
        kept.append(line.strip() if kinds[i] else line)
    out = "\n".join(kept).strip()
    info = {"found": n["method"] > 0 and n["results"] > 0,
            "method_headings": n["method"], "results_headings": n["results"],
            "stop_headings": n["stop"],
            "lead_chars": sum(len(lines[i]) + 1 for i in range(len(lines)) if lead[i]),
            "kept_share": round(len(out) / max(1, len(text)), 4)}
    return out, info
