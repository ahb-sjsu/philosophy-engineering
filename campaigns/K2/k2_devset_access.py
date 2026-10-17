#!/usr/bin/env python
"""K2: how much of the development set can coders read without a library?

Registration 7.1, Access: coders need full texts, and the access route is an
owner decision. This looks up every development-set DOI in OpenAlex and records
its open-access status and best open location. It reads no article. OpenAlex's
status is a database record, not a check that the file opens; the result is a
planning number for the owner's decision, nothing more.

    python k2_devset_access.py devset/devset_rpp.csv devset/devset_ml.csv devset/access.csv
"""
from __future__ import annotations

import collections
import csv
import json
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "pe-k2-devset/0.1 (philosophy-engineering)"}


def lookup(doi: str) -> dict:
    url = "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                        timeout=60) as fh:
                return json.load(fh)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return {}
            time.sleep(5 * (attempt + 1))
        except Exception:
            time.sleep(5 * (attempt + 1))
    return {"error": "lookup failed"}


def main() -> int:
    *inputs, out = sys.argv[1:]
    dois = {}
    for p in inputs:
        for r in csv.DictReader(open(p, encoding="utf-8")):
            if r["doi"]:
                dois.setdefault(r["doi"], r["dev_id"])
    rows = []
    for doi, dev in sorted(dois.items(), key=lambda kv: kv[1]):
        w = lookup(doi)
        oa = w.get("open_access") or {}
        best = w.get("best_oa_location") or {}
        rows.append({"dev_id": dev, "doi": doi,
                     "found": bool(w) and "error" not in w,
                     "is_oa": oa.get("is_oa"), "oa_status": oa.get("oa_status"),
                     "best_oa_url": best.get("pdf_url") or best.get("landing_page_url") or "",
                     "best_oa_version": best.get("version") or ""})
        time.sleep(0.2)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    summary = {"distinct_dois": len(rows),
               "found_in_openalex": sum(r["found"] for r in rows),
               "is_oa": sum(bool(r["is_oa"]) for r in rows),
               "oa_status": dict(collections.Counter(str(r["oa_status"]) for r in rows)),
               "note": "OpenAlex records, not verified downloads"}
    print(json.dumps(summary, indent=1))
    with open(out.replace(".csv", "_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
