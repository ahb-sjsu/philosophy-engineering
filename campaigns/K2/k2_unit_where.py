#!/usr/bin/env python
"""Where do the rubric markers the Method+Results unit drops sit? (4.1)

For each marker sentence outside the unit, classify its position: before the
first Method heading (front matter and introduction), in the LEAD (the last
LEAD characters before any Method heading, where a study's predictions are
usually stated), or after the unit (discussions). Counts only.

    python k2_unit_where.py /archive/experiments/k2/raw/fulltext result.json
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from k2_intake import cut_references
from k2_sections import _kind
from k2_unit_coverage import MARKERS

LEAD = 2000


def main() -> int:
    root, out = Path(sys.argv[1]), sys.argv[2]
    tally = {k: {"in_unit": 0, "lead": 0, "intro_other": 0, "discussion_or_other": 0}
             for k in MARKERS}
    for pdf in sorted((root / "pdf").glob("*.pdf")):
        raw = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        body, _ = cut_references(raw)
        # label every character: unit, lead (LEAD chars before a method
        # heading, outside the unit), pre (before the first method heading)
        lines, pos, labels = body.replace("\f", "\n").splitlines(), 0, []
        on, first_method, method_starts = False, None, []
        for line in lines:
            k = _kind(line)
            if k:
                on = k in ("method", "results")
                if k == "method":
                    method_starts.append(pos)
                    first_method = pos if first_method is None else first_method
            labels.append((pos, pos + len(line) + 1, on))
            pos += len(line) + 1
        if first_method is None:
            continue
        flat = "\n".join(lines)
        for m in re.finditer(r"[^.!?]*[.!?]", flat):
            s = m.group(0)
            for kname, rx in MARKERS.items():
                if not re.search(rx, s, re.I):
                    continue
                at = m.start() + len(s) // 2
                inside = any(a <= at < b and on for a, b, on in labels)
                if inside:
                    tally[kname]["in_unit"] += 1
                elif any(0 <= ms - at <= LEAD for ms in method_starts):
                    tally[kname]["lead"] += 1
                elif at < first_method:
                    tally[kname]["intro_other"] += 1
                else:
                    tally[kname]["discussion_or_other"] += 1
    Path(out).write_text(json.dumps({"lead_chars": LEAD, "by_check": tally}, indent=1),
                         encoding="utf-8")
    print(json.dumps(tally, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
