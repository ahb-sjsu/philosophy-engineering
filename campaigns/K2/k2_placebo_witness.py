#!/usr/bin/env python
"""K2 witness for the placebo gate (registration 4.3 item 2).

The placebo permutes article-level gate scores within strata and must pass at
no more than 5%. This script shows the placebo can do its job in both
directions on synthetic SCORE-shaped data (k2_witness.draw):

    signal          the gate carries its own signal; a binary stratum S is
                    irrelevant          -> real analysis passes, placebo must not
    leak_unadjusted replication and gate failures both depend on S, the gate
                    has no signal of its own, M0 omits S
                                        -> real analysis credits S; the placebo
                                           must fire (that is the leak it exists
                                           to show)
    leak_adjusted   the same data with S in M0
                                        -> neither may pass

Assumptions about the world are in k2_witness.WORLD and STRATUM below; they are
not evidence about the gates.

    python k2_placebo_witness.py --datasets 60 --placebo-reps 100 --seed 20261019
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

from k2_analysis import analyze, placebo  # noqa: E402
from k2_witness import WORLD, draw  # noqa: E402

# Run 1 (seed 20261019) used replication_slope -1.0 and gate_logit_slope 1.2.
# Its leak_unadjusted real analysis passed only 1.7%, so the scenario made no
# leak for the placebo to find and the witness FAILED on its own design
# (k2_placebo_witness_run1.json). Run 2 strengthens the leak until the real
# analysis credits the stratum, which is the condition the placebo must flag.
STRATUM = {"p": 0.5, "replication_slope": -2.5, "gate_logit_slope": 3.0}


def make(rng, scenario):
    if scenario == "signal":
        y, base, gate, paper = draw(rng, "signal_1.0", 1.0)
        s_paper = rng.random(WORLD["n_papers"]) < STRATUM["p"]
        s = s_paper[paper.astype(int)].astype(float)
        return y, base, gate, paper, s
    # stratum leak: S per paper moves replication and gate failures together
    y, base, gate, paper = draw(rng, "null", 0.0)
    p_idx = paper.astype(int)
    s = (rng.random(WORLD["n_papers"]) < STRATUM["p"])[p_idx].astype(float)
    lp = np.log(WORLD["gate_p_mean"] / (1 - WORLD["gate_p_mean"]))
    gp = 1 / (1 + np.exp(-(lp + STRATUM["gate_logit_slope"] * (s - 0.5))))
    paper_gate = rng.binomial(4, gp[np.unique(p_idx, return_index=True)[1]])
    gate = paper_gate[p_idx].astype(float)  # the gate lives on the article
    eta = WORLD["intercept"] + base @ np.array(WORLD["baseline_slopes"]) \
        + STRATUM["replication_slope"] * (s - 0.5)
    y = (rng.random(len(y)) < 1 / (1 + np.exp(-eta))).astype(float)
    return y, base, gate, paper, s


def one(job):
    scenario, seed, reps, boot = job
    rng = np.random.default_rng(seed)
    y, base, gate, paper, s = make(rng, scenario)
    if scenario == "leak_adjusted":
        base = np.column_stack([base, s])
    real = analyze(y, base, gate, paper, n_boot=boot, seed=seed)
    plc = placebo(y, base, gate, paper, s.astype(int).astype(str), reps=reps,
                  n_boot=boot, seed=seed + 1)
    return scenario, real["verdict"] == "pass", plc["pass_rate"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", type=int, default=60)
    ap.add_argument("--placebo-reps", type=int, default=100)
    ap.add_argument("--boot", type=int, default=300)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()
    scen = ["signal", "leak_unadjusted", "leak_adjusted"]
    ss = np.random.SeedSequence(args.seed)
    seeds = [int(c.generate_state(1)[0]) for c in ss.spawn(len(scen) * args.datasets)]
    jobs = [(scen[i // args.datasets], seeds[i], args.placebo_reps, args.boot)
            for i in range(len(seeds))]
    with Pool(args.workers) as pool:
        res = pool.map(one, jobs)
    report = {"world": WORLD, "stratum": STRATUM, "datasets": args.datasets,
              "placebo_reps": args.placebo_reps, "boot": args.boot,
              "seed": args.seed, "scenarios": {}}
    for sc in scen:
        r = [x for x in res if x[0] == sc]
        rates = np.array([x[2] for x in r])
        report["scenarios"][sc] = {
            "real_pass_rate": float(np.mean([x[1] for x in r])),
            "placebo_mean_pass_rate": float(rates.mean()),
            "placebo_flags_leak": float(np.mean(rates > 0.05)),
        }
        print(sc, json.dumps(report["scenarios"][sc]), flush=True)
    S = report["scenarios"]
    # The leak scenario is informative only if the real analysis credits the
    # stratum; report that precondition with the verdict.
    report["leak_precondition_real_pass"] = S["leak_unadjusted"]["real_pass_rate"]
    ok = (S["signal"]["placebo_flags_leak"] <= 0.10
          and S["leak_unadjusted"]["placebo_flags_leak"] >= 0.80
          and S["leak_adjusted"]["placebo_flags_leak"] <= 0.10)
    report["verdict"] = ("PASS: the placebo is quiet on real signal and on an "
                         "adjusted stratum, and fires on an unadjusted one"
                         if ok else "FAIL: the placebo does not separate the "
                                    "scenarios at the stated rates")
    print(report["verdict"])
    with open("k2_placebo_witness_result.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
