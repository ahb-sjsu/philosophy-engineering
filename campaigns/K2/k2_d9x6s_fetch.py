"""Download the repliCATS phase-one claims file from OSF d9x6s (registration 7.1.1); print its shape and columns only.

Only phase_one_singletrace_claims_anonymised.csv is fetched. No cell value is printed: per column, the count of
non-empty cells, of distinct values and the longest value's length, so the columns can be read before any content.
"""
import csv
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.osf.io/v2"
WANT = "phase_one_singletrace_claims_anonymised.csv"
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
csv.field_size_limit(10**8)


def get(url):
    time.sleep(0.3)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/vnd.api+json"}), timeout=60) as r:
        return json.load(r)


prov = get(f"{API}/nodes/d9x6s/files/")["data"][0]
url = prov["relationships"]["files"]["links"]["related"]["href"]
f = None
while url and f is None:
    page = get(url)
    f = next((i for i in page["data"] if i["attributes"]["name"] == WANT), None)
    url = page["links"].get("next")
if f is None:
    sys.exit(f"{WANT} not found at the top of d9x6s")
dest = out / WANT
if not dest.exists():
    urllib.request.urlretrieve(f["links"]["download"], dest)
sha = hashlib.sha256(dest.read_bytes()).hexdigest()
osf = f["attributes"].get("extra", {}).get("hashes", {}).get("sha256")
with open(dest, encoding="utf-8", errors="replace", newline="") as fh:
    rd = csv.reader(fh)
    header = next(rd)
    stats = [{"nonempty": 0, "distinct": set(), "maxlen": 0} for _ in header]
    n = 0
    for row in rd:
        n += 1
        for s, v in zip(stats, row):
            if v.strip():
                s["nonempty"] += 1
            s["distinct"].add(v)
            s["maxlen"] = max(s["maxlen"], len(v))
cols = [{"column": c, "nonempty": s["nonempty"], "distinct": len(s["distinct"]), "max_len": s["maxlen"]} for c, s in zip(header, stats)]
log = {"file": WANT, "bytes": dest.stat().st_size, "sha256": sha, "osf_sha256_match": osf == sha,
       "license_node": "d9x6s", "rows": n, "columns": cols}
json.dump(log, open(out / "fetch_log.json", "w"), indent=1)
print(f"{WANT}: {dest.stat().st_size} B, {n} rows, sha256 match {osf == sha}")
for c in cols:
    print(f"  {c['column']:40} nonempty {c['nonempty']:6}  distinct {c['distinct']:6}  max_len {c['max_len']}")
