#!/usr/bin/env python
"""K2 registered analysis (PREREG-K2-DRAFT.md Section 5 and 6).

Input: a CSV with one row per replicated claim and columns

    claim_id, paper_id, project, replicated (0/1), gate_score (0-4),
    and the baseline predictor columns named with --baseline.

Estimand: out-of-sample AUC of M1 (baselines + gate_score) minus that of M0
(baselines), with cross-validation folds blocked by original paper so that no
paper contributes to both fit and evaluation. Interval: cluster bootstrap over
papers of the pooled out-of-sample predictions. Verdict per Section 6:

    pass        CI lower > 0 and gate coefficient < 0 (more failures, less
                replication)
    fail        CI upper < SESOI (the increment is shown small)
    unresolved  otherwise

Dependency-light on purpose (numpy only): the registered estimator must not
change with a library upgrade between seal and run.

    python k2_analysis.py data.csv --baseline log_n,abs_effect,p_value --sesoi 0.05
"""
from __future__ import annotations

import argparse
import csv
import json
import sys

import numpy as np


def fit_logistic(X: np.ndarray, y: np.ndarray, ridge: float = 1e-4,
                 iters: int = 50) -> np.ndarray:
    """Newton-IRLS with a tiny ridge (not on the intercept) for separability."""
    Xb = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(Xb.shape[1])
    R = ridge * np.eye(Xb.shape[1])
    R[0, 0] = 0.0
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-np.clip(Xb @ w, -30, 30)))
        g = Xb.T @ (y - p) - R @ w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + R
        step = np.linalg.solve(H, g)
        w += step
        if np.max(np.abs(step)) < 1e-9:
            break
    return w


def predict(w: np.ndarray, X: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(w[0] + X @ w[1:], -30, 30)))


def auc(y: np.ndarray, s: np.ndarray) -> float:
    """Mann-Whitney AUC with midranks for ties."""
    _, inv, counts = np.unique(s, return_inverse=True, return_counts=True)
    starts = np.concatenate([[0], np.cumsum(counts)[:-1]])
    ranks = (starts + (counts + 1) / 2.0)[inv]
    n1 = y.sum()
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def standardize(train: np.ndarray, test: np.ndarray):
    mu, sd = train.mean(0), train.std(0)
    sd[sd == 0] = 1.0
    return (train - mu) / sd, (test - mu) / sd


def oos_predictions(X0: np.ndarray, X1: np.ndarray, y: np.ndarray,
                    groups: np.ndarray, k: int, rng: np.random.Generator):
    """Out-of-sample predictions for M0 and M1, folds blocked by group."""
    ug = rng.permutation(np.unique(groups))
    fold_of = {g: i % k for i, g in enumerate(ug)}
    f = np.array([fold_of[g] for g in groups])
    p0, p1 = np.empty(len(y)), np.empty(len(y))
    for i in range(k):
        tr, te = f != i, f == i
        a, b = standardize(X0[tr], X0[te])
        p0[te] = predict(fit_logistic(a, y[tr]), b)
        a, b = standardize(X1[tr], X1[te])
        p1[te] = predict(fit_logistic(a, y[tr]), b)
    return p0, p1


def analyze(y, base, gate, groups, *, k=5, n_boot=2000, sesoi=0.05,
            seed=0) -> dict:
    rng = np.random.default_rng(seed)
    X0 = base
    X1 = np.column_stack([base, gate])
    p0, p1 = oos_predictions(X0, X1, y, groups, k, rng)
    d = auc(y, p1) - auc(y, p0)

    ug = np.unique(groups)
    idx = {g: np.flatnonzero(groups == g) for g in ug}
    boots = []
    for _ in range(n_boot):
        rows = np.concatenate([idx[g] for g in rng.choice(ug, len(ug))])
        yb = y[rows]
        if yb.min() == yb.max():
            continue
        boots.append(auc(yb, p1[rows]) - auc(yb, p0[rows]))
    lo, hi = np.percentile(boots, [2.5, 97.5])

    # Sign of the gate coefficient on the full data (standardized), the
    # second half of the pass condition.
    a, _ = standardize(X1, X1)
    coef = float(fit_logistic(a, y)[-1])

    if lo > 0 and coef < 0:
        verdict = "pass"
    elif hi < sesoi:
        verdict = "fail"
    else:
        verdict = "unresolved"
    return {"n_claims": int(len(y)), "n_papers": int(len(ug)),
            "auc_m0": auc(y, p0), "auc_m1": auc(y, p1), "delta_auc": d,
            "ci95": [float(lo), float(hi)], "gate_coef": coef,
            "sesoi": sesoi, "verdict": verdict}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv")
    ap.add_argument("--baseline", required=True,
                    help="comma-separated baseline predictor columns")
    ap.add_argument("--sesoi", type=float, required=True,
                    help="smallest effect of interest in AUC units; fixed "
                         "before sealing (Section 6), never after")
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()

    cols = args.baseline.split(",")
    with open(args.csv, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    y = np.array([int(r["replicated"]) for r in rows], dtype=float)
    base = np.array([[float(r[c]) for c in cols] for r in rows])
    gate = np.array([float(r["gate_score"]) for r in rows])
    groups = np.array([r["paper_id"] for r in rows])
    out = analyze(y, base, gate, groups, k=args.folds, n_boot=args.boot,
                  sesoi=args.sesoi, seed=args.seed)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
