#!/usr/bin/env python
"""K2 rubric v2 coding unit: the pages where SCORE located the claim; nothing else.

Owner, 2026-10-21: "cut the unit by SCORE's claim location". The 4.1 unit
(Method and Results, k2_sections) finds nothing in economics and politics
papers, which seldom have Method headings. repliCATS phase one (d9x6s) quotes,
for each claim, the passages its coders used: the hypothesis (claim3a), the
test specification (claim3b), the inferential test (claim4), and the sample
size, effect size and p-value, each with the page of SCORE's own PDF.

Our copy may be paginated differently (an accepted manuscript has its own
pages), so passages are found by their text, not by SCORE's page number:
each quoted part (parts are separated by " | ") is normalised to lower-case
letters and digits, cut into 60-character probes every 30 characters, and
placed on the page of our text where most probes occur. A part too short to
probe (under 15 characters, such as "Table 1" or "2.768"), or one found
nowhere, is placed on SCORE's page shifted by the median offset between
SCORE's pages and ours over the parts that were found; with no part found the
offset is not guessed and the part is dropped.

The unit is the located pages, in page order, with:
  - page 1 dropped always (title block, cover page, first-page footers); the
    abstract (claim2) is not used to locate pages for the same reason
  - on a page holding the reference heading, the text from the heading on
    dropped; later pages are kept only if a passage was placed on them (a
    table page after the references in an accepted manuscript)
  - each page's running page number dropped (owner, 2026-10-25: it places the
    article in its journal issue): the bare line equal to the page's own
    printed number, from the offset between PDF page and printed number that
    the whole article agrees on (k2_blinding.running_page_offset)
An article with no hypothesis, test or result passage (claim3a, claim3b,
claim4) placed off page 1 returns found=False and goes to a person; nothing
is guessed.

    from k2_claimunit import cut
    unit, info = cut(raw_text, claim_rows)
"""
from __future__ import annotations

import re
import statistics

from k2_blinding import drop_running_number, running_page_offset

TEXT_COLS = {"claim3a": "claim3a_concretehyp", "claim3b": "claim3b_testspec",
             "claim4": "claim4_inftest", "sample_size": "sample_size",
             "effect_size": "effect_size", "p_value": "p_value"}
CORE = ("claim3a", "claim3b", "claim4")
PROBE, STEP, MIN_PART = 60, 30, 15

REF_HEAD = re.compile(r"^\s*(references|reference list|literature cited|"
                      r"bibliography|works cited|notes and references)\s*:?\s*$",
                      re.I | re.M)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def _place(part: str, pages: list[str]) -> int | None:
    """0-based page with the most probe hits, or None."""
    n = _norm(part)
    if len(n) < MIN_PART:
        return None
    probes = [n[i:i + PROBE] for i in range(0, max(1, len(n) - PROBE + 1), STEP)]
    hits = [sum(p in pg for p in probes) for pg in pages]
    best = max(hits)
    return hits.index(best) if best else None


def _score_pages(pg: str) -> list[int | None]:
    out = []
    for x in pg.split("|"):
        x = x.strip()
        out.append(int(x) if x.isdigit() else None)
    return out


def cut(text: str, rows: list[dict]) -> tuple[str, dict]:
    raw_pages = text.split("\f")
    pages = [_norm(p) for p in raw_pages]
    placed: list[tuple[str, int | None, int | None]] = []  # (field, our page, SCORE page)
    for r in rows:
        for field, col in TEXT_COLS.items():
            t = (r.get(col) or "").strip()
            if not t or t.lower() == "na":
                continue
            parts = [p.strip() for p in t.split(" | ")]
            spg = _score_pages(r.get(field + "_pg", "") or "")
            for k, part in enumerate(parts):
                s = spg[k] if len(spg) == len(parts) else (spg[0] if len(spg) == 1 else None)
                placed.append((field, _place(part, pages), s))
    offs = [p + 1 - s for _, p, s in placed if p is not None and s is not None]
    off = int(statistics.median(offs)) if offs else None
    final: list[tuple[str, int]] = []
    for field, p, s in placed:
        if p is None and s is not None and off is not None:
            p = s - 1 + off
        if p is not None and 0 <= p < len(raw_pages):
            final.append((field, p))
    keep = sorted({p for _, p in final if p > 0})
    heads = [m for m in REF_HEAD.finditer(text) if m.start() > 0.6 * len(text)]
    ref_page = text[:heads[-1].start()].count("\f") if heads else None
    offset = running_page_offset(raw_pages)
    out, dropped = [], 0
    for p in keep:
        page, n = drop_running_number(raw_pages[p], p, offset)
        dropped += n
        if ref_page is not None and p == ref_page:
            m = list(REF_HEAD.finditer(page))
            page = page[:m[-1].start()] if m else page
        out.append(page.strip())
    # pages stay form-feed separated: redaction finds running page numbers by
    # their place at a page's top or bottom
    unit = "\f".join(out).strip()
    core_off_p1 = sum(f in CORE and p > 0 for f, p in final)
    info = {"found": core_off_p1 > 0,
            "parts": len(placed),
            "parts_by_text": sum(p is not None for _, p, _ in placed),
            "parts_by_offset": len(final) - sum(p is not None for _, p, _ in placed),
            "parts_dropped": len(placed) - len(final),
            "parts_on_page1": sum(p == 0 for _, p in final),
            "page_offset": off,
            "pages_kept": " ".join(str(p + 1) for p in keep),
            "pages_total": len(raw_pages),
            "references_cut": ref_page is not None,
            "running_offset": offset, "page_numbers_dropped": dropped,
            "kept_share": round(len(unit) / max(1, len(text)), 4)}
    return unit, info
