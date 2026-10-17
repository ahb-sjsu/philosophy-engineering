#!/usr/bin/env python
"""K2 A1 witness, construction check, and power simulation.

PREREG-K2-DRAFT.md Section 9 requires a witness record: data on which the
registered analysis (k2_analysis.analyze) must NOT return `pass`. This script
generates synthetic SCORE-shaped data under stated assumptions and runs the
registered analysis on many draws per scenario:

    null      gate score independent of everything        -> must not pass
    proxy     gate score tracks the baselines only (small  -> must not pass:
              studies fail more checks), no own signal        the increment
                                                              must not credit
                                                              proxying
    signal_g  gate score carries its own signal, log-odds  -> pass rate is
              slope g per failed check                        the power

Everything about the world is an ASSUMPTION, stated in WORLD below, chosen to
resemble SCORE's published shape (164 papers, ~274 claims, ~55% replicated,
baseline AUC near 0.75). It sizes the I5 power bar; it is not evidence about
the gates.

    python k2_witness.py --reps 400 --boot 500 --seed 20261017
"""
from __future__ import annotations

import argparse
import json
import sys

import numpy as np

from k2_analysis import analyze

WORLD = {
    "n_papers": 164,
    "extra_claims_poisson": 0.67,   # 1 + Poisson -> ~274 claims
    "intercept": 0.25,              # ~55% replicate
    "baseline_slopes": [0.9, 0.6, -0.5],   # log_n, abs_effect, p (z-scored)
    "paper_sd": 0.6,                # shared paper effect on replication
    "gate_p_mean": 0.3,             # mean per-check failure probability
}


def draw(rng, scenario: str, g: float = 0.0):
    W = WORLD
    per = 1 + rng.poisson(W["extra_claims_poisson"], W["n_papers"])
    paper = np.repeat(np.arange(W["n_papers"]), per)
    n = len(paper)
    # paper-level design quality: shared by a paper's claims
    q = rng.normal(size=W["n_papers"])[paper]
    base = rng.normal(size=(n, 3))
    base[:, 0] += 0.5 * rng.normal(size=W["n_papers"])[paper]  # N is per paper
    eta = W["intercept"] + base @ np.array(W["baseline_slopes"])
    eta += W["paper_sd"] * rng.normal(size=W["n_papers"])[paper]

    if scenario.startswith("noisy_proxy"):
        # Replication runs on the TRUE value of baseline 0 (say, the study's
        # real power); M0 sees it only with reliability `rel`, while the gate
        # tracks the true value. The gate then carries information the
        # baselines lack without measuring design at all (Section 7.5 limit).
        rel = g
        true0 = base[:, 0].copy()
        sd = true0.std()
        base[:, 0] = np.sqrt(rel) * true0 + np.sqrt(1 - rel) * sd * rng.normal(size=n)
        logit_p = np.log(W["gate_p_mean"] / (1 - W["gate_p_mean"])) - 0.9 * true0 / sd
        gate = rng.binomial(4, 1 / (1 + np.exp(-logit_p))).astype(float)
        y = (rng.random(n) < 1 / (1 + np.exp(-eta))).astype(float)
        return y, base, gate, paper.astype(str)
    if scenario == "null":
        logit_p = np.full(n, np.log(W["gate_p_mean"] / (1 - W["gate_p_mean"])))
    elif scenario == "proxy":
        # small-N studies fail more checks; the gate adds nothing of its own
        logit_p = np.log(W["gate_p_mean"] / (1 - W["gate_p_mean"])) - 0.9 * base[:, 0]
    else:
        # design quality q drives check failures AND replication
        logit_p = np.log(W["gate_p_mean"] / (1 - W["gate_p_mean"])) - 0.9 * q
    gate = rng.binomial(4, 1 / (1 + np.exp(-logit_p))).astype(float)
    if scenario.startswith("signal"):
        eta = eta - g * (gate - gate.mean())
    y = (rng.random(n) < 1 / (1 + np.exp(-eta))).astype(float)
    return y, base, gate, paper.astype(str)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=400)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--sesoi", type=float, default=0.05)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--slopes", default="0.25,0.5,0.75,1.0")
    ap.add_argument("--noisy", default="",
                    help="comma-separated baseline reliabilities for the "
                         "noisy-proxy scenarios; when given, only those run")
    ap.add_argument("--out", default="k2_witness_result.json")
    args = ap.parse_args()

    if args.noisy:
        scenarios = [(f"noisy_proxy_rel{r}", float(r))
                     for r in args.noisy.split(",")]
    else:
        scenarios = [("null", 0.0), ("proxy", 0.0)] + [
            (f"signal_{s}", float(s)) for s in args.slopes.split(",")]
    rng = np.random.default_rng(args.seed)
    report = {"world": WORLD, "reps": args.reps, "boot": args.boot,
              "sesoi": args.sesoi, "seed": args.seed, "scenarios": {}}
    for name, g in scenarios:
        tally = {"pass": 0, "fail": 0, "unresolved": 0}
        deltas, base_aucs, n_claims = [], [], []
        for _ in range(args.reps):
            y, base, gate, paper = draw(rng, name, g)
            r = analyze(y, base, gate, paper, n_boot=args.boot,
                        sesoi=args.sesoi, seed=int(rng.integers(2**31)))
            tally[r["verdict"]] += 1
            deltas.append(r["delta_auc"])
            base_aucs.append(r["auc_m0"])
            n_claims.append(r["n_claims"])
        report["scenarios"][name] = {
            "gate_slope": g,
            "rates": {k: v / args.reps for k, v in tally.items()},
            "mean_delta_auc": float(np.mean(deltas)),
            "mean_auc_m0": float(np.mean(base_aucs)),
            "mean_n_claims": float(np.mean(n_claims)),
        }
        print(name, json.dumps(report["scenarios"][name]), flush=True)

    if args.noisy:
        # Not an A1 verdict: a pass here is a real increment over the
        # baselines AS MEASURED, credited to the wrong construct. Reported,
        # for the registration to scope the claim by.
        report["construction"] = {
            s: v["rates"]["pass"] for s, v in report["scenarios"].items()}
        print(json.dumps({"noisy_proxy_pass_rates": report["construction"]}))
        witness_ok = True
    else:
        witness_ok = all(report["scenarios"][s]["rates"]["pass"] <= 0.05
                         for s in ("null", "proxy"))
        report["a1_witness"] = ("PASS: null and proxy pass at <= 5%" if witness_ok
                                else "FAIL: the analysis credits a gate score "
                                     "that carries no signal of its own")
        print(json.dumps({"a1_witness": report["a1_witness"]}))
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0 if witness_ok else 1


if __name__ == "__main__":
    sys.exit(main())
