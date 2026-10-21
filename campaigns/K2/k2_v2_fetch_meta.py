"""Second pass for v2 papers whose open location returned a web page: follow the page's standard
<meta name="citation_pdf_url"> tag (Highwire/Google Scholar convention) and keep the file only if it is a PDF.
Only the meta tag is parsed; no article text is read. Appends outcomes to the fetch log's companion file.

    python k2_v2_fetch_meta.py v2_hosts.json v2_draw.csv /archive/experiments/k2/raw/v2 v2_fetch_meta_log.csv
"""
import csv
import hashlib
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

from k2_fulltext_fetch import get
from k2_v2_fetch import locations

META = re.compile(rb'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']', re.I)
META2 = re.compile(rb'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url["\']', re.I)

hosts = json.load(open(sys.argv[1], encoding="utf-8"))
doi = {r["paper_id"]: r["doi"] for r in csv.DictReader(open(sys.argv[2], encoding="utf-8"))}
out = Path(sys.argv[3]) / "pdf"
log = []
for p in hosts["papers"]:
    if p["first_status"] != "200":
        continue
    pid = p["paper_id"]
    entry = {"order": p["order"], "paper_id": pid, "result": "no citation_pdf_url", "version": "", "host": "", "sha256": "", "bytes": ""}
    for loc in locations(doi[pid]):
        page_url = loc.get("pdf_url") or loc.get("landing_page_url")
        try:
            page, _ = get(page_url)
        except Exception as exc:  # noqa: BLE001
            entry["result"] = f"page failed ({type(exc).__name__})"
            continue
        time.sleep(1)
        m = META.search(page) or META2.search(page)
        if not m:
            continue
        pdf_url = urllib.parse.urljoin(page_url, m.group(1).decode("utf-8", "replace"))
        try:
            body, _ = get(pdf_url)
        except Exception as exc:  # noqa: BLE001
            entry["result"] = f"pdf link failed ({type(exc).__name__})"
            time.sleep(1)
            continue
        time.sleep(1)
        if body[:5] == b"%PDF-":
            (out / f"{pid}.pdf").write_bytes(body)
            entry.update(result="pdf", version=loc["version"], host=urllib.parse.urlparse(pdf_url).netloc,
                         sha256=hashlib.sha256(body).hexdigest(), bytes=len(body))
            break
        entry["result"] = "pdf link is not a pdf"
    log.append(entry)
with open(sys.argv[4], "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, list(log[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(log)
print(json.dumps({"tried": len(log), "pdf": sum(e["result"] == "pdf" for e in log),
                  "results": {k: sum(e["result"] == k for e in log) for k in {e["result"] for e in log}}}, indent=1))
