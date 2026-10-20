#!/usr/bin/env python
"""K2 power at the option (b) shape: the phase-1 subset with a forecast baseline.

PREREG-K2-DRAFT.md Section 5 leaves M0 open. Option (b) makes the primary test
the 134 phase-1 claims (133 papers: 132 with one claim, one with two) with the
forecast B5 in M0. This reruns the Section 7.5 simulation at that shape. The
world is k2_witness.WORLD (same assumptions, same registered analysis); what is
new is the shape and the forecast column, both ASSUMPTIONS:

    f = eta_base + w * gate_term + noise

eta_base is the replication log-odds without the gate's own signal; gate_term
is that signal. w is how much of the design signal the forecasters already see
(0: none, 1: all of it). The noise SD is calibrated once so that f alone has
AUC ~0.76 in the null world, the value the forecasts reached on their n = 37
validation (Section 7.0). Scenarios:

    nob5_g      option (b) shape, M0 = B1-B3 (sample size alone)
    b5_w{w}_g   option (b) shape, M0 = B1-B3 + B5, overlap w
    null, proxy option (b) shape with B5: must not pass (A1 at this shape)

    python k2_power_b.py --reps 400 --boot 500 --seed 20261020 --workers 16
"""
from __future__ import annotations

import argparse
import json
import sys
from multiprocessing import Pool

import numpy as np

from k2_analysis import analyze, auc
from k2_witness import WORLD

PAPERS = 133
CLAIMS_PER_PAPER = np.array([2] + [1] * 132)   # 134 claims
TARGET_F_AUC = 0.76


def draw(rng, scenario, g, w, noise_sd, with_b5):
    W = WORLD
    paper = np.repeat(np.arange(PAPERS), CLAIMS_PER_PAPER)
    n = len(paper)
    q = rng.normal(size=PAPERS)[paper]
    base = rng.normal(size=(n, 3))
    base[:, 0] += 0.5 * rng.normal(size=PAPERS)[paper]
    eta = W["intercept"] + base @ np.array(W["baseline_slopes"])
    eta += W["paper_sd"] * rng.normal(size=PAPERS)[paper]
    lp0 = np.log(W["gate_p_mean"] / (1 - W["gate_p_mean"]))
    if scenario == "null":
        logit_p = np.full(n, lp0)
    elif scenario == "proxy":
        logit_p = lp0 - 0.9 * base[:, 0]
    else:
        logit_p = lp0 - 0.9 * q
    gate = rng.binomial(4, 1 / (1 + np.exp(-logit_p))).astype(float)
    gate_term = -g * (gate - gate.mean())
    y = (rng.random(n) < 1 / (1 + np.exp(-(eta + gate_term)))).astype(float)
    if with_b5:
        f = eta + w * gate_term + noise_sd * rng.normal(size=n)
        base = np.column_stack([base, f])
    return y, base, gate, paper.astype(str)


def calibrate(seed):
    """Noise SD giving f alone AUC ~TARGET_F_AUC in the null world (bisection,
    one large draw)."""
    rng = np.random.default_rng(seed)
    W = WORLD
    n = 200_000
    base = rng.normal(size=(n, 3))
    base[:, 0] += 0.5 * rng.normal(size=n)
    eta = W["intercept"] + base @ np.array(W["baseline_slopes"])
    eta += W["paper_sd"] * rng.normal(size=n)
    y = (rng.random(n) < 1 / (1 + np.exp(-eta))).astype(float)
    z = rng.normal(size=n)
    lo, hi = 0.0, 10.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if auc(y, eta + mid * z) > TARGET_F_AUC:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def run(job):
    name, scenario, g, w, with_b5, noise_sd, reps, boot, sesoi, seed = job
    rng = np.random.default_rng(seed)
    tally = {"pass": 0, "fail": 0, "unresolved": 0}
    deltas, m0, fa = [], [], []
    for _ in range(reps):
        y, base, gate, paper = draw(rng, scenario, g, w, noise_sd, with_b5)
        r = analyze(y, base, gate, paper, n_boot=boot, sesoi=sesoi,
                    seed=int(rng.integers(2**31)))
        tally[r["verdict"]] += 1
        deltas.append(r["delta_auc"])
        m0.append(r["auc_m0"])
        if with_b5:
            fa.append(auc(y, base[:, -1]))
    out = {"scenario": scenario, "gate_slope": g, "overlap_w": w,
           "b5_in_m0": with_b5,
           "rates": {k: v / reps for k, v in tally.items()},
           "mean_delta_auc": float(np.mean(deltas)),
           "mean_auc_m0": float(np.mean(m0))}
    if fa:
        out["mean_auc_forecast_alone"] = float(np.mean(fa))
    return name, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=400)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--sesoi", type=float, default=0.05)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--slopes", default="0.5,0.75,1.0,1.25,1.5")
    ap.add_argument("--overlaps", default="0,0.5,1")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--out", default="k2_power_b_result.json")
    ap.add_argument("--only", default="",
                    help="run this one scenario serially (one NRP Job each); "
                         "its seed is the same as in the pooled run")
    ap.add_argument("--list", action="store_true", help="print scenario names")
    ap.add_argument("--merge", nargs="+", default=[],
                    help="merge per-scenario JSON files into --out")
    args = ap.parse_args()
    if args.workers > 20:
        sys.exit("Atlas thermal cap: at most 20 workers")
    if args.merge:
        return merge(args.merge, args.out)

    noise_sd = calibrate(args.seed)
    slopes = [float(s) for s in args.slopes.split(",")]
    overlaps = [float(w) for w in args.overlaps.split(",")]
    specs = [("null", "null", 0.0, 0.0, True), ("proxy", "proxy", 0.0, 0.0, True)]
    specs += [(f"nob5_{g}", "signal", g, 0.0, False) for g in slopes]
    specs += [(f"b5_w{w}_{g}", "signal", g, w, True)
              for w in overlaps for g in slopes]
    ss = np.random.SeedSequence(args.seed).spawn(len(specs))
    jobs = [(n, s, g, w, b, noise_sd, args.reps, args.boot, args.sesoi,
             int(q.generate_state(1)[0])) for (n, s, g, w, b), q in zip(specs, ss)]
    if args.list:
        print("\n".join(j[0] for j in jobs))
        return 0
    if args.only:
        jobs = [j for j in jobs if j[0] == args.only]
        if not jobs:
            sys.exit(f"no scenario {args.only}")
        results = dict(map(run, jobs))
    else:
        with Pool(args.workers) as pool:
            results = dict(pool.map(run, jobs))
    for n in results:
        print(n, json.dumps(results[n]), flush=True)

    report = {"world": WORLD, "shape": {"papers": PAPERS, "claims": int(CLAIMS_PER_PAPER.sum())},
              "target_forecast_auc": TARGET_F_AUC, "forecast_noise_sd": noise_sd,
              "reps": args.reps, "boot": args.boot, "sesoi": args.sesoi,
              "seed": args.seed, "scenarios": results}
    if args.only:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=1)
        return 0
    return finish(report, args.out)


def finish(report, out):
    s = report["scenarios"]
    witness_ok = all(s[k]["rates"]["pass"] <= 0.05 for k in ("null", "proxy"))
    report["a1_witness_at_b_shape"] = "PASS" if witness_ok else "FAIL"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0 if witness_ok else 1


def merge(paths, out):
    """Per-scenario files from the NRP Jobs -> one report; every file must
    carry the same settings, and null and proxy must be present."""
    parts = [json.load(open(p, encoding="utf-8")) for p in paths]
    keys = ("world", "shape", "forecast_noise_sd", "reps", "boot", "sesoi", "seed")
    for p in parts[1:]:
        if any(p[k] != parts[0][k] for k in keys):
            sys.exit("per-scenario files disagree on settings")
    report = {k: parts[0][k] for k in keys + ("target_forecast_auc",)}
    report["scenarios"] = {}
    for p in parts:
        report["scenarios"].update(p["scenarios"])
    return finish(report, out)


if __name__ == "__main__":
    sys.exit(main())
