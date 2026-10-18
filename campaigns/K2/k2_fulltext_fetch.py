#!/usr/bin/env python
"""K2: fetch the open-access full texts of the development set, and every
article's Crossref metadata (the blinding check's input).

Registration 7.1, Access. OpenAlex lists 30 of 132 development-set articles as
open (devset/access.csv); that is a database record. This tries the listed
location and keeps a file only if it is a PDF, so the result is the number of
open texts coders can actually get. Closed articles are not attempted.

Metadata comes from Crossref for every DOI, open or not: all author surnames,
title, journal name AND its short (abbreviated) name, and year, which the
k2_blinding check needs. The OpenAlex "version" is carried: a green copy is
often the submitted manuscript, which can differ from the published article
a reviewer saw.

Files are written OUTSIDE the repository (articles are copyrighted):

    python k2_fulltext_fetch.py devset/access.csv /archive/experiments/k2/raw/fulltext devset/crossref_meta.json
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "pe-k2-devset/0.1 (philosophy-engineering)"}


def get(url: str, timeout: int = 60) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return fh.read(), fh.headers.get("Content-Type", "")


def crossref(doi: str) -> dict:
    for attempt in range(4):
        try:
            body, _ = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
            m = json.loads(body)["message"]
            parts = (m.get("published") or m.get("issued") or {}).get("date-parts", [[None]])
            return {"doi": doi,
                    "title": " ".join(m.get("title") or []),
                    "authors": [a["family"] for a in m.get("author", []) if a.get("family")],
                    "given": [a["given"] for a in m.get("author", []) if a.get("given")],
                    "volume": m.get("volume", ""), "page": m.get("page", ""),
                    "journal": " ".join(m.get("container-title") or []),
                    "journal_short": m.get("short-container-title") or [],
                    "publisher": m.get("publisher", ""),
                    "year": str(parts[0][0] or "")}
        except Exception as exc:  # noqa: BLE001 - retried, then recorded
            err = repr(exc)
            time.sleep(5 * (attempt + 1))
    return {"doi": doi, "error": err}


def main() -> int:
    access, out = sys.argv[1], Path(sys.argv[2])
    (out / "pdf").mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(access, encoding="utf-8")))
    meta, log = {}, []
    for r in rows:
        meta[r["dev_id"]] = crossref(r["doi"])
        time.sleep(0.2)
        entry = {"dev_id": r["dev_id"], "doi": r["doi"], "oa_status": r["oa_status"],
                 "version": r["best_oa_version"], "result": "closed, not attempted"}
        if r["is_oa"] == "True" and r["best_oa_url"]:
            try:
                body, ctype = get(r["best_oa_url"])
                if body[:5] == b"%PDF-":
                    (out / "pdf" / f"{r['dev_id']}.pdf").write_bytes(body)
                    entry.update(result="pdf", sha256=hashlib.sha256(body).hexdigest(),
                                 bytes=len(body))
                else:
                    entry["result"] = f"not a pdf ({ctype.split(';')[0] or 'unknown'})"
            except Exception as exc:  # noqa: BLE001 - recorded per article
                entry["result"] = f"download failed ({type(exc).__name__})"
            time.sleep(1)
        log.append(entry)
    (out / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    if len(sys.argv) > 3:  # bibliographic metadata only, safe to commit
        Path(sys.argv[3]).write_text(json.dumps(meta, indent=1), encoding="utf-8")
    with open(out / "fetch_log.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, ["dev_id", "doi", "oa_status", "version", "result",
                                "sha256", "bytes"])
        w.writeheader()
        w.writerows(log)
    tally: dict[str, int] = {}
    for e in log:
        k = e["result"].split(" (")[0]
        tally[k] = tally.get(k, 0) + 1
    print(json.dumps({"articles": len(log), "results": tally,
                      "crossref_errors": sum("error" in m for m in meta.values())}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
