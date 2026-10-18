#!/usr/bin/env python
"""Residue the leak check does not catch, whole article vs Method+Results (4.1).

Counts, per redacted text, the kinds a person's read found on 2026-10-18 in
texts that had passed k2_blinding.leaks: author initials next to a redaction,
surname particles, ISSN and APA price lines, repository and series labels,
phone numbers, postcodes and street addresses, institution stems before a
redacted word. A pattern count is not a read: it finds only these kinds, so a
person still reads the pilot texts. Counts only.

    python k2_unit_residue.py /archive/experiments/k2/raw/fulltext result.json
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from k2_blinding import redact
from k2_intake import cut_references
from k2_sections import extract

R = r"\[REDACTED\]"
RESIDUE = {
    "initials": rf"\b(?:[A-Z]\.\s?){{1,3}}\s?{R}|{R},?\s(?:[A-Z]\.\s?){{1,3}}(?=[,;&)]|\s|$)",
    "particle": rf"\b(?:[Vv]an|[Vv]on|[Dd]e|[Dd]er|[Dd]en|[Ll]a|[Dd]i|[Dd]u)\s{R}",
    # ISSN, or APA's "0278-7393/08/$12.00" line; a bare "$3.04" is a
    # participant payment or a price in the method, not a leak
    "issn_price": r"\b\d{4}-\d{3}[\dX]\b|/\d\d/\$\s?\d+\.\d\d\b",
    "repository_label": r"ScienceDirect|journal homepage|\bPEARL\b|\bERIM\b|Archive ouverte|"
                        r"eScholarship|PubMed Central|NIH Public Access|HHS Public Access|"
                        r"Author manuscript|Advance online publication|copy of record|"
                        r"Report Series|Working Paper",
    "phone_fax": r"(?:Tel|Phone|Fax|Telephone)\.?:?\s*\+?[\d()\s-]{7,}",
    "address": r"P\.?\s?O\.?\s?Box|\b\d{4,5}\s?[A-Z]{2}\b|\b[A-Z]{2}\s\d{5}\b|"
               r"\b(?:Hall|Building|Street|Avenue|Road)\b",
    "institution_stem": rf"\b[A-Z][a-z]+\s{R}(?=,|\s(?:and|of)\b)",
}


def count(t: str) -> dict[str, int]:
    return {k: len(re.findall(rx, t)) for k, rx in RESIDUE.items()}


def main() -> int:
    root, out = Path(sys.argv[1]), sys.argv[2]
    meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    per, tot = {}, {"whole": dict.fromkeys(RESIDUE, 0), "unit": dict.fromkeys(RESIDUE, 0)}
    for pdf in sorted((root / "pdf").glob("*.pdf")):
        d = pdf.stem
        raw = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        body, _ = cut_references(raw)
        unit, info = extract(body)
        if not info["found"]:
            continue
        w, u = count(redact(body, meta[d])), count(redact(unit, meta[d]))
        per[d] = {"whole": w, "unit": u}
        for k in RESIDUE:
            tot["whole"][k] += w[k]
            tot["unit"][k] += u[k]
    articles_any = {s: sum(any(v[s].values()) for v in per.values()) for s in ("whole", "unit")}
    res = {"articles": len(per), "totals": tot, "articles_with_any": articles_any,
           "per_article": per}
    Path(out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "per_article"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
