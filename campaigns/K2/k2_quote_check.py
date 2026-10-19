#!/usr/bin/env python
"""Why are model coders' quoted evidence strings not found verbatim? (registration 7.4)

The v0 pilot summary found only 78 of gpt-oss's 191 quoted strings verbatim in
the unit it was given (k2_pilot_summary.py normalizes whitespace and curly
quotes only). This classifies every quote, in order:

  verbatim      found after the summary's normalization
  formatting    found once ligatures are unfolded (NFKC), page-number lines and
                hyphenation at line breaks are dropped, and punctuation, dash
                and symbol variants are removed (letters and digits only)
  elided        the quote contains an ellipsis and every fragment of at least
                12 characters is found (formatting-normalized)
  redaction     the quote contains [REDACTED] and every fragment around it is found
  partial       at least half of the quote's 8-word windows are found
  not_found     none of the above: paraphrase inside quotation marks, or invented

Counts only; no quote text is written (the raw responses stay on Atlas).

    python3 k2_quote_check.py /archive/experiments/k2/pilot /archive/experiments/k2/raw/fulltext out.json
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from k2_pilot_summary import norm, quotes


def letters(t: str) -> str:
    t = unicodedata.normalize("NFKC", t)  # PDF ligatures: "ﬁt" -> "fit"
    t = re.sub(r"(?m)^\s*\d{1,4}\s*$", "", t)  # page numbers between two lines of a sentence
    t = re.sub(r"-\s*\n\s*", "", t)  # word broken at a line end
    return re.sub(r"[^a-z0-9]+", "", t.lower())


def classify(q: str, text_n: str, text_l: str) -> str:
    if norm(q) in text_n:
        return "verbatim"
    if letters(q) and letters(q) in text_l:
        return "formatting"
    for mark, kind in ((r"\.\.\.|…", "elided"), (r"\[REDACTED\]", "redaction")):
        if re.search(mark, q):
            parts = [letters(p) for p in re.split(mark, q)]
            parts = [p for p in parts if len(p) >= 12]
            if parts and all(p in text_l for p in parts):
                return kind
    words = re.findall(r"[A-Za-z0-9]+", q)
    wins = [letters(" ".join(words[i:i + 8])) for i in range(0, max(1, len(words) - 7))]
    if wins and sum(w in text_l for w in wins) >= len(wins) / 2:
        return "partial"
    return "not_found"


def main() -> int:
    pilot, root, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    res = {}
    for mdir in sorted((pilot / "raw").iterdir()):
        c = Counter()
        for p in sorted(mdir.glob("*_unit_r*.json")):
            r = json.loads(p.read_text(encoding="utf-8"))
            if "scored" not in r:
                continue
            raw = (root / "blinded" / f"{r['dev_id']}.txt").read_text(encoding="utf-8")
            tn, tl = norm(raw), letters(raw)
            for it in (r["parsed"].get("items") or {}).values():
                for q in quotes((it or {}).get("evidence", "")):
                    c[classify(q, tn, tl)] += 1
        if c:
            n = sum(c.values())
            res[mdir.name] = {"quoted_strings": n, **{k: c[k] for k in
                              ("verbatim", "formatting", "elided", "redaction", "partial", "not_found")}}
    Path(out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
