#!/usr/bin/env python3
"""Submit the option (b) power simulation (k2_power_b.py) to NRP, one Job per scenario, and collect the results.

Runs ON ATLAS (it needs the NATS hub and kubectl), with /home/claude/env/bin/python (nats-py + nats_bursting).
Moved off Atlas on 2026-10-20 because the thermal guardian had pinned the 16-worker run to one core during gaming.

PREFLIGHT, scored against reference_nrp_job_policies line by line:
  * CPU-only (gpu = 0): numpy logistic fits and bootstraps; no GPU rule can apply.
  * Exempt class: cpu = 1, memory = 1Gi, ephemeral-storage 1Gi, requests == limits (the renderer sets them equal).
    OMP/OPENBLAS/MKL threads = 1.
  * Sized by a MEASUREMENT (2026-10-20, Atlas, one core, scenario b5_w0.5_1.0 at 20 reps x 500 boot):
    wall 7.2 s, peak RSS 61 MB. 400 reps -> ~145 s; the bound TIMEOUT is ~12x that. MEASURED below is checked.
  * Self-terminating: `timeout` bounds the run; no sleep in any Job; backoff_limit = 0.
  * Self-contained: no PVC, no ConfigMap. Code rides in gzip + base64 with sha256 asserted; numpy pinned to the
    version on Atlas (2.5.4). The result comes back in the Job log between markers.
  * Submitted via nats-bursting; names checked absent before submit, creationTimestamp checked fresh after;
    submissions spaced 20 s apart. Logs read only from Jobs that succeeded. --cleanup deletes finished Jobs only.

  /home/claude/env/bin/python k2_power_b_nrp.py --dry-run
  /home/claude/env/bin/python k2_power_b_nrp.py --i-have-checked-nrp-policy
  /home/claude/env/bin/python k2_power_b_nrp.py --collect     # parts/<scenario>.json, then k2_power_b_result.json
  /home/claude/env/bin/python k2_power_b_nrp.py --cleanup     # finished Jobs only
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import datetime as dt
import gzip
import hashlib
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

from nats_bursting.descriptor import JobDescriptor, Resources

NS = "ssu-atlas-ai"
HERE = Path(__file__).resolve().parent
IMAGE = "python:3.12-slim"
PINS = "numpy==2.5.4"
FILES = ("k2_analysis.py", "k2_witness.py", "k2_power_b.py")
ARGS = "--reps 400 --boot 500 --seed 20261020"
CPU, MEM, EPH = "1", "1Gi", "1Gi"
MEASURED = {"reps": 20, "wall_s": 7.2, "peak_rss_mb": 61}
TIMEOUT_S = 1800
BATCH = "k2-power-b"
BEGIN, END = "----BEGIN k2 result gz-b64----", "----END k2 result----"
ARG_LIMIT = 120_000


def kubectl(*args):
    return subprocess.run(["kubectl", "-n", NS, *args], capture_output=True, text=True)


def scenarios():
    out = subprocess.run([sys.executable, str(HERE / "k2_power_b.py"), "--seed", "20261020", "--list"],
                         capture_output=True, text=True, check=True, cwd=HERE).stdout.split()
    return out


def job_name(s):
    return "k2-powb-" + s.replace("_", "-").replace(".", "p").lower()


def command(s, blobs):
    lines = ["set -euo pipefail",
             "export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PIP_ROOT_USER_ACTION=ignore",
             "mkdir -p /work && cd /work"]
    for f, (b64, sha) in blobs.items():
        lines += [f"echo '{b64}' | base64 -d | gunzip > {f}", f"echo '{sha}  {f}' | sha256sum -c - || exit 3"]
    lines += [f"pip install -q --no-cache-dir {PINS} 2>&1 | tail -1 || true",
              "python -c \"import numpy, sys; print('numpy', numpy.__version__, 'python', sys.version.split()[0])\"",
              f"timeout {TIMEOUT_S} python -u k2_power_b.py {ARGS} --only {s} --out part.json",
              f"echo '{BEGIN}'", "gzip -c part.json | base64 -w0", "echo", f"echo '{END}'"]
    return "\n".join(lines) + "\n"


def descriptor(s, blobs, head):
    return JobDescriptor(name=job_name(s), image=IMAGE, command=["/bin/bash", "-c", command(s, blobs)],
                         env={"K2_SCENARIO": s, "K2_HEAD": head},
                         resources=Resources(cpu=CPU, memory=MEM, gpu=0, ephemeral_storage=EPH),
                         labels={"atlas.io/batch": BATCH, "app": "pe-k2"}, backoff_limit=0)


def preflight(d):
    r, problems = d.resources, []
    if r.gpu != 0: problems.append("GPU requested for a CPU workload")
    if float(r.cpu) > 1: problems.append(f"cpu {r.cpu} outside the exempt class")
    if not r.memory.endswith("Gi") or float(r.memory[:-2]) > 2: problems.append(f"memory {r.memory} outside the exempt class")
    if not r.ephemeral_storage: problems.append("ephemeral-storage not declared")
    body = " ".join(d.command)
    if "sleep" in body: problems.append("command contains sleep")
    if f"timeout {TIMEOUT_S} python" not in body: problems.append("run not bounded by timeout")
    if d.backoff_limit != 0: problems.append("backoff_limit must be 0")
    if len(d.name) > 63: problems.append("name longer than 63 characters")
    if max(len(a.encode()) for a in d.command) > ARG_LIMIT: problems.append("command argument too long")
    full_s = MEASURED["wall_s"] * 400 / MEASURED["reps"]
    if full_s * 1.25 > TIMEOUT_S: problems.append(f"measured {full_s:.0f} s x 1.25 exceeds the bound {TIMEOUT_S} s")
    if MEASURED["peak_rss_mb"] * 1.25 > 1024: problems.append("measured RSS x 1.25 exceeds 1Gi")
    got = kubectl("get", "job", d.name, "-o", "name")
    if got.returncode == 0 and got.stdout.strip(): problems.append(f"Job {d.name} already exists")
    if problems:
        raise SystemExit(f"PREFLIGHT VETO {d.name}: " + "; ".join(problems))


async def publish(d, listen_s=15.0):
    import nats
    nc = await nats.connect("nats://localhost:4222"); seen = []; jid = f"{d.name}-{uuid.uuid4().hex[:8]}"

    async def on_msg(msg):
        try:
            ev = json.loads(msg.data.decode())
        except Exception:
            ev = {"raw": msg.data.decode(errors="replace")}
        if msg.subject.endswith(jid): seen.append(ev)

    await nc.subscribe("burst.status.>", cb=on_msg); await nc.flush()
    await nc.publish("burst.submit", json.dumps({"job_id": jid, "descriptor": d.to_dict()}).encode()); await nc.flush()
    t0 = time.time()
    while time.time() - t0 < listen_s and not any(e.get("state") in ("submitted", "error") for e in seen):
        await asyncio.sleep(0.5)  # local wait on Atlas for the controller's status reply, not in any Job
    await nc.close()
    return seen


def created(name):
    got = kubectl("get", "job", name, "-o", "jsonpath={.metadata.creationTimestamp}")
    if got.returncode != 0 or not got.stdout.strip(): return None
    return dt.datetime.fromisoformat(got.stdout.strip().replace("Z", "+00:00"))


def submit(dry):
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip() or "untracked"
    blobs = {}
    for f in FILES:
        raw = (HERE / f).read_bytes()
        blobs[f] = (base64.b64encode(gzip.compress(raw, mtime=0)).decode(), hashlib.sha256(raw).hexdigest())
    descs = [descriptor(s, blobs, head) for s in scenarios()]
    for d in descs: preflight(d)
    print(json.dumps({"head": head, "n_jobs": len(descs), "jobs": [d.name for d in descs],
                      "sha256": {k: v[1] for k, v in blobs.items()}, "resources": [CPU, MEM, EPH],
                      "timeout_s": TIMEOUT_S, "measured": MEASURED}, indent=1))
    if dry:
        print(command(scenarios()[0], {k: ("<b64>", s) for k, (_, s) in blobs.items()})); return 0
    for i, d in enumerate(descs):
        if i: time.sleep(20)  # space submissions apart (submitter on Atlas, not a Job)
        t_sub = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=5)
        ev = asyncio.run(publish(d)); c = None
        for _ in range(12):
            c = created(d.name)
            if c: break
            time.sleep(5)
        fresh = c is not None and c >= t_sub
        print(json.dumps({"job": d.name, "events": ev, "created": c.isoformat() if c else None, "fresh": fresh}), flush=True)
        if not fresh:
            raise SystemExit(f"{d.name}: no fresh Job after submit; read the status events above")
    return 0


def collect():
    parts = HERE / "parts"; parts.mkdir(exist_ok=True); missing = []
    for s in scenarios():
        p = parts / f"{s}.json"
        if p.exists(): continue
        name = job_name(s)
        st = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
        if not st.startswith("1/"):
            missing.append(f"{name}:{st or 'absent'}"); continue
        log = kubectl("logs", f"job/{name}").stdout
        if BEGIN not in log:
            missing.append(f"{name}:no-block"); continue
        p.write_bytes(gzip.decompress(base64.b64decode(log.split(BEGIN, 1)[1].split(END, 1)[0].strip())))
        print("wrote", p.name)
    if missing:
        print("NOT YET:", " ".join(missing)); return 2
    return subprocess.run([sys.executable, str(HERE / "k2_power_b.py"), "--seed", "20261020", "--merge",
                           *[str(parts / f"{s}.json") for s in scenarios()],
                           "--out", str(HERE / "k2_power_b_result.json")], cwd=HERE).returncode


def cleanup():
    for s in scenarios():
        name = job_name(s)
        got = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}/{.status.active}")
        if got.returncode != 0: print(f"{name}: absent"); continue
        su, fa, ac = (got.stdout.strip().split("/") + ["", "", ""])[:3]
        if ac not in ("", "0") or (su in ("", "0") and fa in ("", "0")):
            print(f"{name}: NOT finished; refusing to delete"); continue
        print(name, kubectl("delete", "job", name).stdout.strip())
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args()
    if a.collect: return collect()
    if a.cleanup: return cleanup()
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    return submit(a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
