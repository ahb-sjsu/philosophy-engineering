#!/usr/bin/env python
"""K2 coding unit: the Method and Results sections of an article, nothing else.

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


def extract(text: str) -> tuple[str, dict]:
    """Return (kept text, info). info: found (bool), method/results heading
    counts, kept_share (characters kept / characters in)."""
    kept: list[str] = []
    on = False
    n = {"method": 0, "results": 0, "stop": 0}
    for line in text.replace("\f", "\n").splitlines():
        k = _kind(line)
        if k:
            n[k] += 1
            on = k in ("method", "results")
            if on:  # the heading is kept, so coders see where each stretch starts
                kept += ["", line.strip()]
            continue
        if on:
            kept.append(line)
    out = "\n".join(kept).strip()
    info = {"found": n["method"] > 0 and n["results"] > 0,
            "method_headings": n["method"], "results_headings": n["results"],
            "stop_headings": n["stop"],
            "kept_share": round(len(out) / max(1, len(text)), 4)}
    return out, info
