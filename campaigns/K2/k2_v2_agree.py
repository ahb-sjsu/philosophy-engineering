#!/usr/bin/env python
"""Agreement of RUBRIC-v2 codings (k2_v2_extract.py): per question, per check, and on the gate score.

Scores and counts only; no quotes or article text are written. Codings whose coder says it knows the
replication outcome are dropped and counted (RUBRIC-v2 Section 0). Reported for every pair of streams
(between families, rep 1) and within each stream (rep 1 vs rep 2), overall and per unit set:

  questions   share of units where the two answers are equal (VOID counts as an answer), and Cohen's
              kappa for the categorical questions; numbers are equal only if identical
  checks      share equal (na kept: an na/0 split is a disagreement about applicability)
  gate        ICC(2,1) (k2_analysis.icc_single, the I1 statistic) and exact agreement

    python3 k2_v2_agree.py /archive/experiments/k2/v2dev_r1 out.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

from k2_analysis import icc_single
from k2_v2_rules import ALLOWED, MANIPULATED, NUMBER, QUESTIONS

CHECKS = ["A1", "A2", "A3", "A4"]


def kappa(pairs):
    if not pairs:
        return None
    po = sum(a == b for a, b in pairs) / len(pairs)
    ca, cb = Counter(str(a) for a, _ in pairs), Counter(str(b) for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / len(pairs) ** 2
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def compare(A: dict, B: dict, units: list) -> dict:
    both = [u for u in units if u in A and u in B]
    res = {"n": len(both), "questions": {}, "checks": {}}
    if not both:
        return res
    for q in QUESTIONS:
        # Q4 is asked only of manipulated designs: compared where both coders say there was one
        on = [u for u in both if not q.startswith("Q4.")
              or (A[u]["answers"]["Q1.1"] in MANIPULATED and B[u]["answers"]["Q1.1"] in MANIPULATED)]
        pairs = [(A[u]["answers"][q], B[u]["answers"][q]) for u in on]
        if not pairs:
            res["questions"][q] = {"n": 0}
            continue
        row = {"n": len(pairs), "agree": round(sum(a == b for a, b in pairs) / len(pairs), 3)}
        if NUMBER not in ALLOWED[q]:
            row["kappa"] = kappa(pairs)
        res["questions"][q] = row
    for c in CHECKS:
        pairs = [(A[u]["scored"][c], B[u]["scored"][c]) for u in both]
        res["checks"][c] = round(sum(a == b for a, b in pairs) / len(pairs), 3)
    x = np.array([[A[u]["scored"]["gate"], B[u]["scored"]["gate"]] for u in both], dtype=float)
    res["gate_icc21"] = round(icc_single(x), 3) if len(both) > 2 and x.std() > 0 else None
    res["gate_exact"] = round(float(np.mean(x[:, 0] == x[:, 1])), 3)
    return res


def main() -> int:
    run, out = Path(sys.argv[1]), sys.argv[2]
    S, dropped, failed, ops = {}, Counter(), Counter(), {}
    for p in sorted((run / "raw").glob("*/*.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        m = r["model_requested"]
        o = ops.setdefault(m, {"codings": 0, "scored": 0, "models_returned": set(), "finish": Counter(),
                               "seconds": [], "voided_answers": Counter()})
        o["codings"] += 1
        for a in r["attempts"]:
            o["models_returned"].add(str(a.get("model_returned")))
            o["finish"][str(a.get("finish_reason"))] += 1
        if "scored" not in r:
            failed[m] += 1
            continue
        o["scored"] += 1
        o["seconds"].append(r["attempts"][-1].get("seconds"))
        for q, why in (r.get("voided") or {}).items():
            o["voided_answers"][why] += 1
        if (r.get("recognition") or {}).get("knows_replication_outcome") is True:
            dropped[m] += 1
            continue
        S[(m, r["rep"], r["unit"])] = r | {"set_": r["set"]}
    models = sorted(ops)
    sets = {r["unit"]: r["set"] for r in S.values()}
    groups = {"all": sorted(sets)} | {s: sorted(u for u in sets if sets[u] == s) for s in sorted(set(sets.values()))}

    def stream(m, rep):
        return {u: r for (mm, rr, u), r in S.items() if mm == m and rr == rep}

    rel = {}
    for g, units in groups.items():
        for m1, m2 in combinations(models, 2):
            rel[f"between {m1} and {m2} (rep 1) [{g}]"] = compare(stream(m1, 1), stream(m2, 1), units)
        for m in models:
            rel[f"within {m} (rep 1 vs 2) [{g}]"] = compare(stream(m, 1), stream(m, 2), units)
    dist = {}
    for m in models:
        rows = list(stream(m, 1).values()) + list(stream(m, 2).values())
        dist[m] = {"gate": dict(Counter(r["scored"]["gate"] for r in rows)),
                   **{c: dict(Counter(r["scored"][c] for r in rows)) for c in CHECKS}}
    report = {"operations": {m: {**o, "models_returned": sorted(o["models_returned"]), "finish": dict(o["finish"]),
                                 "median_seconds": float(np.median([s for s in o["seconds"] if s])) if o["seconds"] else None,
                                 "voided_answers": dict(o["voided_answers"]), "seconds": None}
                             for m, o in ops.items()},
              "failed": dict(failed), "dropped_knows_outcome": dict(dropped),
              "distribution": dist, "reliability": rel}
    Path(out).write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1)[:6000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
