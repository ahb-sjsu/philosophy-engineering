#!/usr/bin/env python
"""Does the Method+Results unit keep what the rubric needs? (Registration 4.1)

A proxy, not a coding study: for each rubric check, count sentences in the
article body (reference list cut) that carry that check's evidence markers,
and the share of them still present in the Method+Results unit. A check whose
markers mostly fall outside the unit cannot be scored reliably from it. The
proxy says where evidence words sit, not whether a coder would score the
same; the pilot (7.4) codes a subset both ways to measure that.

Outputs counts only (no article text).

    python k2_unit_coverage.py /archive/experiments/k2/raw/fulltext result.json
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from k2_intake import cut_references
from k2_sections import extract

MARKERS = {
    "A1 Nonvacuity": r"hypothes[ie]s|hypothesi[sz]ed|we predict|predicted that|"
                     r"prediction|we expected|expected that|preregist|pre-regist|"
                     r"primary (?:outcome|measure|dependent)",
    "A2 Identification": r"reliab|cronbach|internal consistency|test-retest|α =|"
                         r"alpha =|validat|intraclass|inter-rater|interrater",
    "A3 Intervention": r"manipulation check|check(?:ed)? (?:on )?the manipulation|"
                       r"manipulation (?:was|had been) (?:successful|effective)|"
                       r"demand characteristic|suspicion|funnel debrief",
    "A4 Inference": r"exclu|attrition|dropped out|drop-out|outlier|were removed|"
                    r"final sample|did not complete|failed to complete",
}


def sentences(t: str) -> list[str]:
    t = re.sub(r"\s+", " ", t)
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", t) if s]


def main() -> int:
    root, out = Path(sys.argv[1]), sys.argv[2]
    per, pooled = {}, {k: [0, 0] for k in MARKERS}
    for pdf in sorted((root / "pdf").glob("*.pdf")):
        raw = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        body, _ = cut_references(raw)
        unit, info = extract(body)
        full_s, unit_s = sentences(body), set(sentences(unit))
        row = {"sections_found": info["found"], "kept_share": info["kept_share"]}
        for k, rx in MARKERS.items():
            hits = [s for s in full_s if re.search(rx, s, re.I)]
            kept = sum(s in unit_s for s in hits)
            row[k] = [kept, len(hits)]
            if info["found"]:
                pooled[k][0] += kept
                pooled[k][1] += len(hits)
        per[pdf.stem] = row
    found = [d for d, r in per.items() if r["sections_found"]]
    summary = {}
    for k in MARKERS:
        lost_all = [d for d in found if per[d][k][1] > 0 and per[d][k][0] == 0]
        summary[k] = {"marker_sentences_kept": pooled[k][0],
                      "marker_sentences_total": pooled[k][1],
                      "share_kept": round(pooled[k][0] / max(1, pooled[k][1]), 3),
                      "articles_with_markers_all_outside_unit": len(lost_all),
                      "articles_with_markers": sum(per[d][k][1] > 0 for d in found)}
    res = {"articles": len(per), "sections_found": len(found),
           "not_found": sorted(set(per) - set(found)),
           "kept_share_range": [min(per[d]["kept_share"] for d in found),
                                max(per[d]["kept_share"] for d in found)] if found else None,
           "by_check": summary, "per_article": per}
    Path(out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "per_article"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
