#!/usr/bin/env python
"""K2 intake: PDF -> text -> reference list cut -> redaction -> gate I3.

Registration 4.1. For each <dev_id>.pdf in the input directory:

    1. hash the PDF (sha256) and extract text with poppler's pdftotext
    2. drop each page's running page number (k2_blinding.running_page_offset,
       added 2026-10-25), then cut the reference list at the LAST line that is only a references
       heading in the back 40% of the text; if none is found the article is
       flagged, not guessed at
    3. k2_sections.extract: keep only Method and Results sections (the coding
       unit, adopted 2026-10-18); front matter, introductions and discussions
       are dropped
    4. k2_blinding.redact with the article's Crossref metadata (meta.json from
       k2_fulltext_fetch.py: all surnames, title, journal and its short names,
       year)
    5. k2_blinding.leaks on the result; an article with any residual leak, no
       reference heading, no Method or no Results heading, or letter-spaced
       scanned type (SINGLE_LETTER_MAX) is quarantined for a person, never
       released to coders

Blinded texts are written next to the PDFs, outside the repository (articles
are copyrighted). Only the manifest (hashes, counts, flags) is committed.

    python k2_intake.py /archive/experiments/k2/raw/fulltext manifest.csv
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from k2_blinding import drop_running_number, leaks, redact, running_page_offset
from k2_sections import extract

# share of one-letter words above which the text is treated as a letter-spaced
# scan. Chosen before any value was seen; on the 7 open articles the six
# born-digital PDFs measured 0.05 to 0.074 and the one scan 0.11, so it
# separates them with a thin margin. Recheck on the pilot.
SINGLE_LETTER_MAX = 0.10

REF_HEAD = re.compile(r"^\s*(references|reference list|literature cited|"
                      r"bibliography|works cited|notes and references)\s*:?\s*$",
                      re.I | re.M)


def cut_references(text: str) -> tuple[str, bool]:
    heads = [m for m in REF_HEAD.finditer(text) if m.start() > 0.6 * len(text)]
    if not heads:
        return text, False
    return text[:heads[-1].start()], True


def main() -> int:
    root, manifest = Path(sys.argv[1]), sys.argv[2]
    meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    (root / "blinded").mkdir(exist_ok=True)
    (root / "quarantine").mkdir(exist_ok=True)
    rows = []
    for pdf in sorted((root / "pdf").glob("*.pdf")):
        dev = pdf.stem
        m = meta[dev]
        raw = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        # running page numbers place the article in its journal issue (owner,
        # 2026-10-25); dropped page by page before the pages are joined
        pages = raw.split("\f")
        offset = running_page_offset(pages)
        pages, dropped = zip(*(drop_running_number(p, k, offset) for k, p in enumerate(pages)))
        body, cut = cut_references("\f".join(pages))
        # the coding unit is Method and Results only (4.1, adopted
        # 2026-10-18); front matter is dropped, then the rest is redacted
        unit, sec = extract(body)
        blind = redact(unit, m)
        residual = leaks(blind, m)
        pre = leaks(unit, m)
        # scanned, letter-spaced type ("N o r b e r t") defeats the word rules
        # and garbles the text for coders; such articles go to a person
        toks = re.findall(r"[A-Za-z]+", raw)
        single = sum(len(t) == 1 for t in toks) / max(1, len(toks))
        ocr_flag = single > SINGLE_LETTER_MAX
        dest = root / ("quarantine" if residual or not cut or ocr_flag
                       or not sec["found"] else "blinded") / f"{dev}.txt"
        dest.write_text(blind, encoding="utf-8")
        kinds: dict[str, int] = {}
        for k, _ in pre:
            kinds[k] = kinds.get(k, 0) + 1
        rows.append({
            "dev_id": dev, "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "chars_raw": len(raw), "chars_blinded": len(blind),
            "references_cut": cut,
            "sections_found": sec["found"], "method_headings": sec["method_headings"],
            "results_headings": sec["results_headings"], "lead_chars": sec["lead_chars"],
            "kept_share": sec["kept_share"],
            "running_offset": offset, "page_numbers_dropped": sum(dropped),
            "leaks_before": len(pre), "leak_kinds_before": json.dumps(kinds, sort_keys=True),
            "residual_leaks": len(residual),
            "residual_kinds": json.dumps(sorted({k for k, _ in residual})),
            "single_letter_share": round(single, 4), "scan_flag": ocr_flag,
            # over-redaction: marks per word of the blinded text
            "redacted_share": round(blind.count("[REDACTED]")
                                    / max(1, len(blind.split())), 4),
            "status": dest.parent.name})
    with open(manifest, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(json.dumps({"articles": len(rows),
                      "blinded": sum(r["status"] == "blinded" for r in rows),
                      "quarantined": sum(r["status"] == "quarantine" for r in rows),
                      "no_reference_heading": sum(not r["references_cut"] for r in rows)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
