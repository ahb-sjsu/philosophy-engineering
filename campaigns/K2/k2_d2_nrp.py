#!/usr/bin/env python3
"""Submit the D2 sizing simulation (k2_d2_sizing.py) to NRP as one Job and collect its result.

Runs ON ATLAS (NATS hub and kubectl), with /home/claude/env/bin/python. Transport, preflight and log-block
return are k2_power_b_nrp.py's, imported. Two roles:
  timing  --reps 100: the measurement itself (exempt class, so its only risk is OOM, which its footprint shows)
  run     --reps 4000: vetoed unless timing.json carries a footprint whose wall time x 40 x 1.25 fits the bound
          and whose peak RSS x 1.25 fits the memory request.

PREFLIGHT (reference_nrp_job_policies): CPU-only, exempt class cpu 1 / memory 1Gi / ephemeral 1Gi, requests ==
limits, one thread; bounded by `timeout`, no sleep, backoff_limit 0; names checked absent before submit and
creationTimestamp fresh after; code shipped gzip+base64 with sha256 asserted; numpy pinned to Atlas's 2.5.4.

  /home/claude/env/bin/python k2_d2_nrp.py --role timing --dry-run
  /home/claude/env/bin/python k2_d2_nrp.py --role timing --i-have-checked-nrp-policy
  /home/claude/env/bin/python k2_d2_nrp.py --role timing --collect      # d2_timing.json (+ footprint)
  /home/claude/env/bin/python k2_d2_nrp.py --role run --i-have-checked-nrp-policy
  /home/claude/env/bin/python k2_d2_nrp.py --role run --collect         # k2_d2_sizing_result.json
  /home/claude/env/bin/python k2_d2_nrp.py --role run --cleanup         # finished Jobs only
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
from pathlib import Path

from nats_bursting.descriptor import JobDescriptor, Resources

from k2_power_b_nrp import ARG_LIMIT, BEGIN, END, IMAGE, PINS, created, kubectl, publish

HERE = Path(__file__).resolve().parent
FILES = ("k2_analysis.py", "k2_d2_sizing.py")
SEED = 20261021
ROLES = {"timing": {"reps": 100, "timeout_s": 3600}, "run": {"reps": 4000, "timeout_s": 4 * 3600}}
CPU, MEM, EPH, MEM_MB = "1", "1Gi", "1Gi", 1024
BATCH = "k2-d2-sizing"


def job_name(role):
    return f"k2-d2-sizing-{role}"


def out_path(role):
    return HERE / ("k2_d2_sizing_result.json" if role == "run" else "d2_timing.json")


def command(role, blobs):
    R = ROLES[role]
    lines = ["set -euo pipefail",
             "export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PIP_ROOT_USER_ACTION=ignore",
             "mkdir -p /work && cd /work"]
    for f, (b64, sha) in blobs.items():
        lines += [f"echo '{b64}' | base64 -d | gunzip > {f}", f"echo '{sha}  {f}' | sha256sum -c - || exit 3"]
    lines += [f"pip install -q --no-cache-dir {PINS} 2>&1 | tail -1 || true",
              "python -c \"import numpy, sys; print('numpy', numpy.__version__, 'python', sys.version.split()[0])\"",
              f"timeout {R['timeout_s']} python -u k2_d2_sizing.py --reps {R['reps']} --seed {SEED} --out part.json",
              f"echo '{BEGIN}'", "gzip -c part.json | base64 -w0", "echo", f"echo '{END}'"]
    return "\n".join(lines) + "\n"


def descriptor(role, blobs, head):
    return JobDescriptor(name=job_name(role), image=IMAGE, command=["/bin/bash", "-c", command(role, blobs)],
                         env={"K2_HEAD": head}, resources=Resources(cpu=CPU, memory=MEM, gpu=0, ephemeral_storage=EPH),
                         labels={"atlas.io/batch": BATCH, "atlas.io/role": role, "app": "pe-k2"}, backoff_limit=0)


def measured_ok():
    p = out_path("timing")
    if not p.exists(): return ["no timing measurement collected"]
    fp = json.loads(p.read_text(encoding="utf-8")).get("footprint") or {}
    if "wall_seconds" not in fp or "peak_rss_mib" not in fp: return ["timing.json has no footprint"]
    out, scale = [], ROLES["run"]["reps"] / ROLES["timing"]["reps"]
    if fp["wall_seconds"] * scale * 1.25 > ROLES["run"]["timeout_s"]:
        out.append(f"wall {fp['wall_seconds']:.0f} s x {scale:.0f} x 1.25 exceeds the bound {ROLES['run']['timeout_s']} s")
    if fp["peak_rss_mib"] * 1.25 > MEM_MB:
        out.append(f"peak {fp['peak_rss_mib']:.0f} MiB x 1.25 exceeds {MEM_MB} MiB")
    return out


def preflight(d, role):
    r, problems = d.resources, []
    if r.gpu != 0: problems.append("GPU requested for a CPU workload")
    if float(r.cpu) > 1: problems.append("cpu outside the exempt class")
    if not r.memory.endswith("Gi") or float(r.memory[:-2]) > 2: problems.append("memory outside the exempt class")
    if not r.ephemeral_storage: problems.append("ephemeral-storage not declared")
    body = " ".join(d.command)
    if "sleep" in body: problems.append("command contains sleep")
    if f"timeout {ROLES[role]['timeout_s']} python" not in body: problems.append("run not bounded by timeout")
    if d.backoff_limit != 0: problems.append("backoff_limit must be 0")
    if max(len(a.encode()) for a in d.command) > ARG_LIMIT: problems.append("command argument too long")
    if role == "run": problems += measured_ok()
    got = kubectl("get", "job", d.name, "-o", "name")
    if got.returncode == 0 and got.stdout.strip(): problems.append(f"Job {d.name} already exists")
    if problems:
        raise SystemExit(f"PREFLIGHT VETO {d.name}: " + "; ".join(problems))


def submit(role, dry):
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip() or "untracked"
    blobs = {}
    for f in FILES:
        raw = (HERE / f).read_bytes()
        blobs[f] = (base64.b64encode(gzip.compress(raw, mtime=0)).decode(), hashlib.sha256(raw).hexdigest())
    d = descriptor(role, blobs, head)
    preflight(d, role)
    print(json.dumps({"job": d.name, "role": role, "reps": ROLES[role]["reps"], "timeout_s": ROLES[role]["timeout_s"],
                      "resources": [CPU, MEM, EPH], "sha256": {k: v[1] for k, v in blobs.items()}}, indent=1))
    if dry:
        print(command(role, {k: ("<b64>", s) for k, (_, s) in blobs.items()})); return 0
    t_sub = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=5)
    ev = asyncio.run(publish(d)); c = None
    for _ in range(12):
        c = created(d.name)
        if c: break
        time.sleep(5)  # submitter on Atlas waiting for the Job object, not a Job
    fresh = c is not None and c >= t_sub
    print(json.dumps({"job": d.name, "events": ev, "created": c.isoformat() if c else None, "fresh": fresh}))
    return 0 if fresh else 1


def collect(role):
    name, p = job_name(role), out_path(role)
    if p.exists():
        print(f"{p.name} already collected"); return 0
    st = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
    if not st.startswith("1/"):
        print(f"{name}: status {st or 'absent'}"); return 2
    log = kubectl("logs", f"job/{name}").stdout
    if BEGIN not in log:
        print(f"{name}: no result block"); return 2
    p.write_bytes(gzip.decompress(base64.b64decode(log.split(BEGIN, 1)[1].split(END, 1)[0].strip())))
    print("wrote", p.name, json.dumps(json.loads(p.read_text(encoding="utf-8")).get("footprint")))
    return 0


def cleanup(role):
    name = job_name(role)
    got = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}/{.status.active}")
    if got.returncode != 0: print(f"{name}: absent"); return 0
    su, fa, ac = (got.stdout.strip().split("/") + ["", "", ""])[:3]
    if ac not in ("", "0") or (su in ("", "0") and fa in ("", "0")):
        print(f"{name}: NOT finished; refusing to delete"); return 1
    print(name, kubectl("delete", "job", name).stdout.strip()); return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", choices=list(ROLES), required=True)
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args()
    if a.collect: return collect(a.role)
    if a.cleanup: return cleanup(a.role)
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    return submit(a.role, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
