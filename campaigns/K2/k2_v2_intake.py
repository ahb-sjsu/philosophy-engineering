#!/usr/bin/env python
"""K2 rubric v2 intake: PDF -> text -> claim-location unit -> redaction -> leak check.

As k2_intake.py, with the coding unit cut by SCORE's claim location
(k2_claimunit) in place of Method and Results (owner, 2026-10-21). For each
<id>.pdf under <root>/pdf with claim rows in the repliCATS phase-one claims
file (d9x6s):

    1. hash the PDF and extract text with poppler's pdftotext
    2. k2_claimunit.cut: the pages holding SCORE's quoted hypothesis, test and
       result passages, page 1 and reference lists dropped
    3. k2_blinding.redact with the paper's Crossref metadata (<root>/meta.json)
    4. k2_blinding.leaks on the result; a paper with any residual leak, no
       located passage off page 1, or letter-spaced scanned type is
       quarantined for a person, never released to coders

Texts are written under <root>, outside the repository; only the manifest
(hashes, counts, flags) is committed. Prints counts only, never text.

    python k2_v2_intake.py <root> <claims.csv> <manifest.csv>
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from k2_blinding import leaks, redact
from k2_claimunit import cut
from k2_intake import SINGLE_LETTER_MAX


def main() -> int:
    root, claims, manifest = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    csv.field_size_limit(10**8)
    ids = {p.stem for p in (root / "pdf").glob("*.pdf")}
    rows_by: dict[str, list[dict]] = {}
    with open(claims, encoding="utf-8", errors="replace", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["paper_id"] in ids:
                rows_by.setdefault(r["paper_id"], []).append(r)
    for d in ("blinded", "quarantine"):
        (root / d).mkdir(exist_ok=True)
        for old in (root / d).glob("*.txt"):  # a rerun replaces the earlier unit
            old.unlink()
    out = []
    for pdf in sorted((root / "pdf").glob("*.pdf")):
        pid = pdf.stem
        m = meta[pid]
        raw = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        unit, info = cut(raw, rows_by.get(pid, []))
        blind = redact(unit, m)
        residual = leaks(blind, m)
        pre = leaks(unit, m)
        toks = re.findall(r"[A-Za-z]+", raw)
        single = sum(len(t) == 1 for t in toks) / max(1, len(toks))
        scan = single > SINGLE_LETTER_MAX
        status = "quarantine" if residual or scan or not info["found"] else "blinded"
        (root / status / f"{pid}.txt").write_text(blind, encoding="utf-8")
        kinds: dict[str, int] = {}
        for k, _ in pre:
            kinds[k] = kinds.get(k, 0) + 1
        out.append({"paper_id": pid, "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                    "claim_rows": len(rows_by.get(pid, [])), **info,
                    "chars_raw": len(raw), "chars_blinded": len(blind),
                    "leaks_before": len(pre), "leak_kinds_before": json.dumps(kinds, sort_keys=True),
                    "residual_leaks": len(residual),
                    "residual_kinds": json.dumps(sorted({k for k, _ in residual})),
                    "single_letter_share": round(single, 4), "scan_flag": scan,
                    "redacted_share": round(blind.count("[REDACTED]") / max(1, len(blind.split())), 4),
                    "status": status})
    with open(manifest, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(json.dumps({"papers": len(out),
                      "blinded": sum(r["status"] == "blinded" for r in out),
                      "quarantined": sum(r["status"] == "quarantine" for r in out),
                      "not_located": sum(not r["found"] for r in out),
                      "residual_leaks": sum(r["residual_leaks"] > 0 for r in out)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
