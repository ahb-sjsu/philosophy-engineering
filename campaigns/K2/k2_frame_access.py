#!/usr/bin/env python
"""K2 v2 draw frame: how much of it can coders read without a library? (RUBRIC-v2-PLAN D2, registration 7.1.1)

Looks up every frame DOI (k2_d9x6s_frame.py's frame: d9x6s phase-one papers minus SCORE's replicated papers and
dev-set matches) in OpenAlex, 50 DOIs per request, and records open-access status, the best open location's
version (published, accepted or submitted manuscript) and whether it has a PDF link. It reads no article. Like
k2_devset_access.py, these are database records, not verified downloads: on the development set 17 of the 23
records marked open were obtained, and most open copies were submitted manuscripts (7.1, 4.1).

Reads only paper_id, DOI_CR and category from the claims file.

    python k2_frame_access.py <claims.csv> <analyst data.RData> <devset access.csv> <out.csv>
"""
from __future__ import annotations

import collections
import csv
import json
import sys
import time
import urllib.parse
import urllib.request

import rdata

UA = {"User-Agent": "pe-k2-frame/0.1 (philosophy-engineering)"}
BATCH = 50


def norm(doi):
    doi = doi.lower().strip()
    for p in ("https://doi.org/", "http://dx.doi.org/", "doi:"):
        if doi.startswith(p):
            doi = doi[len(p):]
    return doi


def fetch(dois):
    q = urllib.parse.quote("doi:" + "|".join(dois), safe=":|/")
    url = f"https://api.openalex.org/works?filter={q}&per-page={BATCH}&select=doi,open_access,best_oa_location"
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as fh:
                return json.load(fh)["results"]
        except Exception:
            time.sleep(5 * (attempt + 1))
    return None


def main() -> int:
    claims_csv, rda, access_csv, out = sys.argv[1:5]
    csv.field_size_limit(10**8)
    replicated = set(rdata.read_rda(rda)["repli_outcomes"]["paper_id"].astype(str).str.strip())
    dev = {norm(r["doi"]) for r in csv.DictReader(open(access_csv, encoding="utf-8"))} - {""}
    frame = []
    with open(claims_csv, encoding="utf-8", errors="replace", newline="") as fh:
        for r in csv.DictReader(fh):
            pid, doi = r["paper_id"].strip(), norm(r["DOI_CR"])
            if pid not in replicated and doi not in dev:
                frame.append({"paper_id": pid, "doi": doi, "category": r["category"].strip()})
    found, failed = {}, 0
    for i in range(0, len(frame), BATCH):
        res = fetch([f["doi"] for f in frame[i:i + BATCH]])
        if res is None:
            failed += 1
            continue
        for w in res:
            found[norm(w.get("doi") or "")] = w
        time.sleep(0.5)
    rows = []
    for f in frame:
        w = found.get(f["doi"])
        oa = (w or {}).get("open_access") or {}
        best = (w or {}).get("best_oa_location") or {}
        rows.append({**f, "found": w is not None, "is_oa": bool(oa.get("is_oa")), "oa_status": oa.get("oa_status") or "",
                     "best_oa_version": best.get("version") or "", "best_has_pdf": bool(best.get("pdf_url"))})
    with open(out, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)

    def share(rs):
        n = len(rs)
        oa = [r for r in rs if r["is_oa"]]
        pub = [r for r in oa if r["best_oa_version"] == "publishedVersion"]
        return {"papers": n, "is_oa": len(oa), "oa_share": round(len(oa) / n, 3) if n else None,
                "oa_published_version": len(pub), "published_share": round(len(pub) / n, 3) if n else None}

    by_cat = collections.defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)
    summary = {"frame": len(rows), "found_in_openalex": sum(r["found"] for r in rows), "failed_batches": failed,
               "all": share(rows),
               "oa_status": dict(collections.Counter(r["oa_status"] or "none" for r in rows).most_common()),
               "best_oa_version": dict(collections.Counter(r["best_oa_version"] or "none" for r in rows if r["is_oa"]).most_common()),
               "oa_with_pdf_link": sum(r["is_oa"] and r["best_has_pdf"] for r in rows),
               "by_category": {c: share(rs) for c, rs in sorted(by_cat.items(), key=lambda kv: -len(kv[1]))},
               "note": "OpenAlex records, not verified downloads"}
    with open(out.replace(".csv", "_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
