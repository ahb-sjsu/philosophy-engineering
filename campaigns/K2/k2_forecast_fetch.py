"""Download the forecast files from OSF tcfb9/data (never the replication-outcomes CSV); print headers and row counts only."""
import csv
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.osf.io/v2"
WANT = {"KeyW_CS_2020-10-19.csv", "anon_p1_singletrace_confidence_scores.csv", "pooledMarketstable.csv"}
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)


def get(url):
    time.sleep(0.3)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/vnd.api+json"}), timeout=60) as r:
        return json.load(r)


prov = get(f"{API}/nodes/tcfb9/files/")["data"][0]
top = get(prov["relationships"]["files"]["links"]["related"]["href"])["data"]
data_dir = next(i for i in top if i["attributes"]["kind"] == "folder" and i["attributes"]["name"] == "data")
log = []
for f in get(data_dir["relationships"]["files"]["links"]["related"]["href"])["data"]:
    name = f["attributes"]["name"]
    if name not in WANT:
        continue
    dest = out / name
    if not dest.exists():
        urllib.request.urlretrieve(f["links"]["download"], dest)
    sha = hashlib.sha256(dest.read_bytes()).hexdigest()
    osf = f["attributes"].get("extra", {}).get("hashes", {}).get("sha256")
    with open(dest, encoding="utf-8", errors="replace", newline="") as fh:
        rd = csv.reader(fh)
        header = next(rd)
        n = sum(1 for _ in rd)
    log.append({"file": name, "bytes": dest.stat().st_size, "sha256": sha, "osf_sha256_match": osf == sha, "rows": n, "columns": header})
    print(f"== {name}: {n} rows, sha256 match {osf == sha}\n   columns: {header}")
json.dump(log, open(out / "fetch_log.json", "w"), indent=1)
