#!/usr/bin/env python
"""K2 reliability witness: where the I1 bar should sit (registration 6, 7.2).

A gate score read with coder error is a noisy measure of the true score, and
noise attenuates the increment toward zero without any warning (a low ΔAUC
from a bad instrument looks like a small effect). This script asks how much
coder error the design can carry before the physics test loses its power.

Data are the k2_witness signal scenario: the TRUE gate score (failed checks
out of 4) drives replication with log-odds slope g. Each of two coders reads
each of the 4 checks and records it wrongly with probability e, independently.
For each e the script reports

    icc_single    ICC(2,1) of one coder's score, estimated from the two coders
                  (k2_analysis.icc_single), the quantity gate I1 is stated on
    pass_true     pass rate with the true score (the k2_witness power)
    pass_one      pass rate with one coder's score
    pass_mean     pass rate with the mean of the two coders' scores, a
                  conservative stand-in for the registered reconciled
                  consensus (reconciliation by discussion should do no worse
                  than averaging, which is an assumption, not a result)

The world is k2_witness.WORLD; the error model (independent, symmetric,
per-check flips) is an assumption. Coders who share a misreading are not
modeled and would inflate icc_single without making the score more valid.

    python k2_reliability_witness.py --reps 200 --boot 300 --seed 20261020
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from multiprocessing import Pool

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np  # noqa: E402

from k2_analysis import analyze, icc_single  # noqa: E402
from k2_witness import WORLD, draw  # noqa: E402

N_CHECKS = 4


def coded(rng, gate, e):
    """Two coders' scores for a true failed-check count per claim."""
    n = len(gate)
    # which checks failed: exchangeable, so any gate-sized subset
    truth = (rng.random((n, N_CHECKS)).argsort(axis=1)
             < gate[:, None]).astype(int)
    out = []
    for _ in range(2):
        flip = rng.random((n, N_CHECKS)) < e
        out.append(np.where(flip, 1 - truth, truth).sum(axis=1).astype(float))
    return np.column_stack(out)


def one(job):
    g, e, seed, boot = job
    rng = np.random.default_rng(seed)
    y, base, gate, paper = draw(rng, f"signal_{g}", g)
    two = coded(rng, gate, e)
    s = int(rng.integers(2**31))
    v = {name: analyze(y, base, x, paper, n_boot=boot, seed=s)["verdict"]
         for name, x in (("true", gate), ("one", two[:, 0]),
                         ("mean", two.mean(axis=1)))}
    return g, e, icc_single(two), v


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--boot", type=int, default=300)
    ap.add_argument("--slopes", default="0.75,1.0")
    ap.add_argument("--errors", default="0,0.05,0.1,0.15,0.2,0.3")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", default="k2_reliability_witness_result.json")
    args = ap.parse_args()
    cells = [(float(g), float(e)) for g in args.slopes.split(",")
             for e in args.errors.split(",")]
    ss = np.random.SeedSequence(args.seed)
    seeds = [int(c.generate_state(1)[0]) for c in ss.spawn(len(cells) * args.reps)]
    jobs = [cells[i // args.reps] + (seeds[i], args.boot)
            for i in range(len(seeds))]
    with Pool(args.workers) as pool:
        res = pool.map(one, jobs)
    report = {"world": WORLD, "n_checks": N_CHECKS, "reps": args.reps,
              "boot": args.boot, "seed": args.seed, "cells": []}
    for g, e in cells:
        r = [x for x in res if x[0] == g and x[1] == e]
        row = {"gate_slope": g, "flip_prob": e,
               "icc_single": float(np.mean([x[2] for x in r])),
               "icc_single_sd": float(np.std([x[2] for x in r]))}
        for name in ("true", "one", "mean"):
            row[f"pass_{name}"] = float(np.mean([x[3][name] == "pass" for x in r]))
            row[f"fail_{name}"] = float(np.mean([x[3][name] == "fail" for x in r]))
        report["cells"].append(row)
        print(json.dumps(row), flush=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
