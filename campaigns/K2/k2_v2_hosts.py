"""Where the v2 fetch failed: for each drawn paper without a PDF, the hosts of its published/accepted open locations
(OpenAlex records only; nothing is downloaded), and the HTTP status a HEAD request to the first one returns.

    python k2_v2_hosts.py v2_fetch_log.csv hosts.json
"""
import collections
import csv
import json
import sys
import time
import urllib.parse
import urllib.request

from k2_v2_fetch import UA_HEAD, locations

log = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
hosts, codes, per = collections.Counter(), collections.Counter(), []
for r in log:
    if r["result"].startswith("pdf"):
        continue
    locs = locations(r["doi"])
    hs = [urllib.parse.urlparse(l.get("pdf_url") or l.get("landing_page_url") or "").netloc for l in locs]
    code = ""
    if locs:
        url = locs[0].get("pdf_url") or locs[0].get("landing_page_url")
        try:
            req = urllib.request.Request(url, headers=UA_HEAD, method="HEAD")
            with urllib.request.urlopen(req, timeout=30) as fh:
                code = str(fh.status)
        except urllib.error.HTTPError as exc:
            code = str(exc.code)
        except Exception as exc:  # noqa: BLE001
            code = type(exc).__name__
        time.sleep(1)
    hosts.update(set(hs))
    codes[code or "no location"] += 1
    per.append({"order": r["order"], "paper_id": r["paper_id"], "hosts": hs, "first_status": code})
json.dump({"by_host": dict(hosts.most_common()), "first_status": dict(codes.most_common()), "papers": per},
          open(sys.argv[2], "w"), indent=1)
print(json.dumps({"by_host": dict(hosts.most_common()), "first_status": dict(codes.most_common())}, indent=1))
