#!/usr/bin/env python
"""K2 rubric v2, decision D2: how many held-out articles the v2 measurement needs.

RUBRIC-v2-PLAN.md D2. v1 was measured on 9 to 11 articles and the result could
not separate a fitted rubric from chance. This sizes the next held-out set
before any draw: for n double-coded articles, how precisely does the
between-coder gate ICC(2,1) (k2_analysis.icc_single, the I1 quantity) estimate
the population value?

World (ASSUMPTIONS, the registration 7.2 model): each article's TRUE gate score
is Binomial(4, p) with logit p = logit(0.3) - 0.9 q, q ~ N(0, 1) (the k2_witness
signal world's gate); which checks failed is exchangeable. Each of two coders
records each check wrongly with probability e, independently. Optional coder
BIAS b: coder 2 also turns a passed check into a failure with probability b
(one family reading the rubric more harshly), which ICC(2,1) with absolute
agreement penalizes. e is calibrated per b on 400,000 articles so that the
population ICC hits each target.

For each (b, target ICC, n): the estimate's mean, SD and 2.5/50/97.5
percentiles, and P(estimate >= 0.80). The sizing rule is then read off:
t_n = the 95th percentile of the estimate when the population ICC is 0.60, and
the power P(estimate >= t_n) at populations 0.80, 0.85 and 0.90.

    python k2_d2_sizing.py --reps 4000 --seed 20261021
"""
from __future__ import annotations

import argparse
import json
import resource
import sys
import time

import numpy as np

from k2_analysis import icc_single

N_CHECKS = 4
LP0 = np.log(0.3 / 0.7)
TARGETS = (0.60, 0.70, 0.80, 0.85, 0.90)
BIASES = (0.0, 0.05)
NS = (10, 15, 20, 30, 40, 60, 80, 100, 150, 200)


def scores(rng, n, e, b):
    q = rng.normal(size=n)
    gate = rng.binomial(N_CHECKS, 1 / (1 + np.exp(-(LP0 - 0.9 * q))))
    truth = (rng.random((n, N_CHECKS)).argsort(axis=1) < gate[:, None]).astype(int)
    out = []
    for c in range(2):
        x = np.where(rng.random((n, N_CHECKS)) < e, 1 - truth, truth)
        if c == 1 and b > 0:
            x = np.where((x == 0) & (rng.random((n, N_CHECKS)) < b), 1, x)
        out.append(x.sum(axis=1).astype(float))
    return np.column_stack(out)


def calibrate(target, b, seed, n=400_000):
    """Flip probability e giving population ICC `target` under bias b (bisection,
    common random numbers)."""
    lo, hi = 0.0, 0.5
    for _ in range(30):
        mid = (lo + hi) / 2
        icc = icc_single(scores(np.random.default_rng(seed), n, mid, b))
        if icc > target:
            lo = mid
        else:
            hi = mid
    e = (lo + hi) / 2
    return e, icc_single(scores(np.random.default_rng(seed + 1), n, e, b))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=4000)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", default="k2_d2_sizing_result.json")
    args = ap.parse_args()
    t0 = time.time()

    rng = np.random.default_rng(args.seed)
    report = {"reps": args.reps, "seed": args.seed, "n_checks": N_CHECKS,
              "gate_model": "Binomial(4, p), logit p = logit(0.3) - 0.9 q",
              "cells": [], "sizing": []}
    est = {}
    for b in BIASES:
        for t in TARGETS:
            e, pop = calibrate(t, b, args.seed + int(1000 * t) + int(100 * b))
            if b > 0 and e <= 1e-6:
                print(json.dumps({"bias": b, "target": t, "skipped": "bias alone is below target"}), flush=True)
                continue
            for n in NS:
                v = np.array([icc_single(scores(rng, n, e, b)) for _ in range(args.reps)])
                v = v[np.isfinite(v)]
                est[(b, t, n)] = v
                row = {"bias": b, "target_icc": t, "flip_prob": e, "population_icc": pop,
                       "n_articles": n, "mean": float(v.mean()), "sd": float(v.std()),
                       "p2_5": float(np.percentile(v, 2.5)), "p50": float(np.percentile(v, 50)),
                       "p97_5": float(np.percentile(v, 97.5)),
                       "p_ge_0_80": float((v >= 0.80).mean())}
                report["cells"].append(row)
                print(json.dumps(row), flush=True)
    for b in BIASES:
        for n in NS:
            if (b, 0.60, n) not in est:
                continue
            t_n = float(np.percentile(est[(b, 0.60, n)], 95))
            row = {"bias": b, "n_articles": n, "threshold_95pct_under_0_60": t_n}
            for t in (0.70, 0.80, 0.85, 0.90):
                if (b, t, n) in est:
                    row[f"power_at_{t:.2f}"] = float((est[(b, t, n)] >= t_n).mean())
            report["sizing"].append(row)
            print(json.dumps(row), flush=True)
    # footprint of this process, the measurement the NRP run is sized from
    report["footprint"] = {"wall_seconds": time.time() - t0,
                           "peak_rss_mib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
