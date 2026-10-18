#!/usr/bin/env python
"""K2 registered analysis (PREREG-K2-DRAFT.md Section 5 and 6).

Input: a CSV with one row per replicated claim and columns

    claim_id, paper_id, project, replicated (0/1), gate_score (0-4),
    n_u (checks scored U; rows with n_u > 2 are excluded and listed),
    and the baseline predictor columns named with --baseline.
    `project` is carried for the per-project secondary report and is not
    used here.

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


def placebo(y, base, gate, groups, strata, *, reps=400, k=5, n_boot=500,
            sesoi=0.05, seed=0) -> dict:
    """Registration 4.3 item 2: permute article-level gate scores among
    articles of the same stratum and rerun the registered analysis. The
    permutation destroys any link between a gate score and its own article
    while keeping the gate's distribution within each stratum, so a placebo
    that passes more often than 5% means the increment rides on differences
    between strata that M0 does not absorb (the strata leak)."""
    rng = np.random.default_rng(seed)
    papers, first = np.unique(groups, return_index=True)
    p_gate = gate[first]
    p_stratum = strata[first]
    row_paper = np.searchsorted(papers, groups)
    passes = 0
    for _ in range(reps):
        g = p_gate.copy()
        for s in np.unique(p_stratum):
            idx = np.flatnonzero(p_stratum == s)
            g[idx] = p_gate[rng.permutation(idx)]
        out = analyze(y, base, g[row_paper], groups, k=k, n_boot=n_boot,
                      sesoi=sesoi, seed=int(rng.integers(2**31)))
        passes += out["verdict"] == "pass"
    rate = passes / reps
    return {"reps": reps, "pass_rate": rate, "bar": 0.05,
            "strata_leak": bool(rate > 0.05)}


def icc_single(scores: np.ndarray) -> float:
    """Gate I1: ICC(2,1), two-way random effects, absolute agreement, the
    reliability of ONE coder's score (Shrout and Fleiss 1979). `scores` is
    articles x coders. Van Bavel et al. 2016 reported ICC(2,3), the
    reliability of a three-coder mean, which is higher for the same coders;
    the registered bar is on this single-coder value."""
    x = np.asarray(scores, dtype=float)
    n, k = x.shape
    grand = x.mean()
    msr = k * ((x.mean(axis=1) - grand) ** 2).sum() / (n - 1)
    msc = n * ((x.mean(axis=0) - grand) ** 2).sum() / (k - 1)
    resid = x - x.mean(axis=1, keepdims=True) - x.mean(axis=0) + grand
    mse = (resid ** 2).sum() / ((n - 1) * (k - 1))
    return float((msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n))


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
    ap.add_argument("--strata", default="",
                    help="comma-separated stratum columns for the placebo "
                         "gate (registration 4.3 item 2: discipline, design)")
    ap.add_argument("--placebo-reps", type=int, default=400)
    args = ap.parse_args()

    cols = args.baseline.split(",")
    with open(args.csv, newline="", encoding="utf-8") as fh:
        every = list(csv.DictReader(fh))
    # Registration Section 4: a study with more than two checks scored U is
    # excluded from the primary analysis and counted. The CSV carries n_u.
    excluded = [r for r in every if int(r["n_u"]) > 2]
    rows = [r for r in every if int(r["n_u"]) <= 2]

    def arrays(rs, u_as=None):
        y = np.array([int(r["replicated"]) for r in rs], dtype=float)
        base = np.array([[float(r[c]) for c in cols] for r in rs])
        gate = np.array([float(r["gate_score"]) for r in rs])
        if u_as == "fail":
            gate = gate + np.array([float(r["n_u"]) for r in rs])
        return y, base, gate, np.array([r["paper_id"] for r in rs])

    y, base, gate, groups = arrays(rows)
    out = analyze(y, base, gate, groups, k=args.folds, n_boot=args.boot,
                  sesoi=args.sesoi, seed=args.seed)
    out["excluded_more_than_two_u"] = {"n": len(excluded),
                                       "claims": [r["claim_id"] for r in excluded]}

    # Registration 4.3 item 3: U is not missing at random. Reported, not
    # graded: gate_score counts checks scored 1, so U as pass is the score as
    # recorded and U as fail adds n_u; both runs keep every study.
    sens = {}
    for u_as in ("pass", "fail"):
        r = analyze(*arrays(every, u_as), k=args.folds, n_boot=args.boot,
                    sesoi=args.sesoi, seed=args.seed)
        sens[f"u_as_{u_as}"] = {k: r[k] for k in
                                ("n_claims", "delta_auc", "ci95", "verdict")}

    def rate(rs):
        return sum(int(r["replicated"]) for r in rs) / len(rs) if rs else None

    sens["replication_rate_included"] = rate(rows)
    sens["replication_rate_excluded"] = rate(excluded)
    out["u_sensitivity"] = sens

    if args.strata:
        scol = args.strata.split(",")
        strata = np.array(["|".join(r[c] for c in scol) for r in rows])
        out["placebo"] = placebo(y, base, gate, groups, strata,
                                 reps=args.placebo_reps, k=args.folds,
                                 n_boot=min(args.boot, 500), sesoi=args.sesoi,
                                 seed=args.seed + 1)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
