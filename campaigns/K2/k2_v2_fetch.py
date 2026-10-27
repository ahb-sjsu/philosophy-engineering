#!/usr/bin/env python
"""K2 rubric v2: fetch the 90 drawn papers' open full texts and Crossref metadata (registration 7.1.1).

For each paper in devset/v2_draw.csv, OpenAlex is asked for every open location of the DOI. Only locations whose
version is the published or the accepted version are tried (owner rule, 2026-10-21), published first, PDF links
before landing pages; a file is kept only if it is a PDF. Nothing is read or printed from any article: the log
records the outcome, the version and host used, the hash and the size. Crossref metadata (surnames, title,
journal and short names, year) is fetched for every paper, as k2_intake's blinding needs it.

Held-out texts are handled by script only until v2 is committed (7.1.1). Files are written OUTSIDE the
repository (articles are copyrighted); the log goes in the repository.

    python k2_v2_fetch.py devset/v2_draw.csv /archive/experiments/k2/raw/v2 devset/v2_fetch_log.csv
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
import urllib.parse
from pathlib import Path

from k2_fulltext_fetch import crossref, get

KEEP = ("publishedVersion", "acceptedVersion")
UA_HEAD = {"User-Agent": "pe-k2-devset/0.1 (philosophy-engineering)"}


def is_ssrn(loc: dict) -> bool:
    """SSRN copies are excluded (owner, 2026-10-24); added before the development fetch of 2026-10-27."""
    urls = " ".join(str(loc.get(k) or "") for k in ("pdf_url", "landing_page_url"))
    return "ssrn" in urls.lower() or "ssrn" in str((loc.get("source") or {}).get("display_name", "")).lower()


def locations(doi: str) -> list[dict]:
    url = ("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)
           + "?select=open_access,best_oa_location,locations")
    for attempt in range(4):
        try:
            body, _ = get(url)
            w = json.loads(body)
            locs = [l for l in (w.get("locations") or []) if l.get("is_oa") and l.get("version") in KEEP
                    and not is_ssrn(l)]
            locs.sort(key=lambda l: (KEEP.index(l["version"]), not l.get("pdf_url")))
            return locs
        except Exception:  # noqa: BLE001 - retried, then recorded as no locations
            time.sleep(5 * (attempt + 1))
    return []


def main() -> int:
    draw, out, log_path = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
    (out / "pdf").mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(draw, encoding="utf-8")))
    meta, log = {}, []
    for r in rows:
        pid = r["paper_id"]
        meta[pid] = crossref(r["doi"])
        time.sleep(0.2)
        entry = {"order": r["order"], "paper_id": pid, "doi": r["doi"], "stratum": r["stratum"],
                 "result": "no published or accepted open location", "version": "", "host": "",
                 "tries": 0, "sha256": "", "bytes": ""}
        dest = out / "pdf" / f"{pid}.pdf"
        if dest.exists():
            body = dest.read_bytes()
            entry.update(result="pdf (kept from an earlier run)", sha256=hashlib.sha256(body).hexdigest(), bytes=len(body))
            log.append(entry)
            continue
        for loc in locations(r["doi"]):
            for url in (loc.get("pdf_url"), loc.get("landing_page_url")):
                if not url:
                    continue
                entry["tries"] += 1
                try:
                    body, ctype = get(url)
                except Exception as exc:  # noqa: BLE001 - recorded per paper
                    entry["result"] = f"download failed ({type(exc).__name__})"
                    time.sleep(1)
                    continue
                time.sleep(1)
                if body[:5] == b"%PDF-":
                    dest.write_bytes(body)
                    entry.update(result="pdf", version=loc["version"], host=urllib.parse.urlparse(url).netloc,
                                 sha256=hashlib.sha256(body).hexdigest(), bytes=len(body))
                    break
                entry["result"] = f"not a pdf ({ctype.split(';')[0] or 'unknown'})"
            if entry["result"] == "pdf":
                break
        log.append(entry)
    (out / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    with open(log_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, list(log[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(log)
    tally: dict[str, int] = {}
    for e in log:
        k = e["result"].split(" (")[0]
        tally[k] = tally.get(k, 0) + 1
    print(json.dumps({"papers": len(log), "results": tally,
                      "pdf_by_version": {v: sum(e["version"] == v for e in log) for v in KEEP},
                      "crossref_errors": sum("error" in m for m in meta.values())}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
