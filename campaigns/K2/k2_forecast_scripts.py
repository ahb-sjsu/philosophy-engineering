"""Download the four R scripts from OSF tcfb9/scripts (code only) and show every line naming a forecast file or a team."""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.osf.io/v2"
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)


def get(url):
    time.sleep(0.3)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/vnd.api+json"}), timeout=60) as r:
        return json.load(r)


prov = get(f"{API}/nodes/tcfb9/files/")["data"][0]
top = get(prov["relationships"]["files"]["links"]["related"]["href"])["data"]
sdir = next(i for i in top if i["attributes"]["kind"] == "folder" and i["attributes"]["name"] == "scripts")
pat = re.compile(r"KeyW|anon_p1|singletrace|pooledMarkets|market|repliCATS|RM\b|cs_m\d+|method", re.I)
for f in get(sdir["relationships"]["files"]["links"]["related"]["href"])["data"]:
    dest = out / f["attributes"]["name"]
    if not dest.exists():
        urllib.request.urlretrieve(f["links"]["download"], dest)
    print("==", dest.name)
    for i, line in enumerate(dest.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if pat.search(line):
            print(f"{i:5}: {line.strip()[:200]}")
