#!/usr/bin/env python
"""Summarize the K2 pilot coding (k2_pilot_code.py) for the repository.

Scores and counts only: no evidence text, no identity guesses, no article
text. No replication outcome is read (7.1 consequence 5), so nothing here says
whether a gate score predicts anything; the pilot measures the instrument.

Reported:
  - calls, failures, parse retries, latency, tokens, model names returned
  - per check and stream: share scored 1, U, na; articles with more than two
    U checks (excluded from the primary analysis, Section 4)
  - gate score distribution and variance per stream
  - reliability: ICC(2,1) of the gate score and check-level percent agreement,
    within a stream (rep 1 vs rep 2, same model: one opinion, 4.3 rule 4) and
    between streams (the two model families, rep 1)
  - unit vs full text (4.1): agreement of the gate and checks on the subset
  - recognition: share recognizing the study, share whose guess names the
    first author's surname or most of the title, share claiming to know the
    replication outcome
  - evidence check: share of quoted evidence strings found verbatim in the
    text the model saw (whitespace-normalized)

    python3 k2_pilot_summary.py /archive/experiments/k2/pilot /archive/experiments/k2/raw/fulltext out.json
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

from k2_analysis import icc_single

CHECKS = ["A1", "A2", "A3", "A4"]


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", t.replace("’", "'").replace("“", '"').replace("”", '"')).strip().lower()


def quotes(ev: str) -> list[str]:
    return [a or b for a, b in re.findall(r"\"([^\"]{12,})\"|“([^”]{12,})”", ev or "")]


def recognized_right(guess: str | None, m: dict) -> bool:
    if not guess:
        return False
    g = norm(guess)
    if any(norm(a) in g for a in m.get("authors", [])[:1] if len(a) >= 3):
        return True
    w = [x for x in re.findall(r"[a-z]{5,}", norm(m.get("title", "")))]
    return bool(w) and sum(x in g for x in w) >= max(2, int(0.6 * len(w)))


def agree(pairs):
    """Percent agreement over pairs of check scores (na excluded)."""
    ok = [a == b for a, b in pairs if "na" not in (a, b)]
    return round(sum(ok) / len(ok), 3) if ok else None


def main() -> int:
    pilot, root, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    recs = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((pilot / "raw").glob("*/*.json"))]
    ok = [r for r in recs if "scored" in r]
    res: dict = {"calls": len(recs), "scored": len(ok),
                 "failed": sorted(f"{r['model_requested']}/{r['dev_id']}_{r['input']}_r{r['rep']}"
                                  for r in recs if "scored" not in r)}
    streams = sorted({r["model_requested"] for r in recs})
    S = {(r["model_requested"], r["dev_id"], r["input"], r["rep"]): r for r in ok}

    ops = {}
    for m in streams:
        rs = [r for r in recs if r["model_requested"] == m]
        last = [r["attempts"][-1] for r in rs if r["attempts"]]
        ops[m] = {"calls": len(rs), "scored": sum("scored" in r for r in rs),
                  "extra_attempts": sum(len(r["attempts"]) - 1 for r in rs),
                  "models_returned": sorted({str(a.get("model_returned")) for a in last}),
                  "finish_reasons": sorted({str(a.get("finish_reason")) for a in last}),
                  "median_seconds": statistics.median([a.get("seconds", 0) for a in last]) if last else None,
                  "median_prompt_tokens": statistics.median([(a.get("usage") or {}).get("prompt_tokens", 0) for a in last]) if last else None,
                  "median_completion_tokens": statistics.median([(a.get("usage") or {}).get("completion_tokens", 0) for a in last]) if last else None}
    res["operations"] = ops

    unit = [r for r in ok if r["input"] == "unit"]
    per = {}
    for m in streams:
        rs = [r for r in unit if r["model_requested"] == m]
        if not rs:
            continue
        d = {"codings": len(rs)}
        for c in CHECKS:
            v = [r["scored"]["checks"][c] for r in rs]
            d[c] = {k: round(v.count(k) / len(v), 3) for k in ("1", "0", "U", "na")}
        gates = [r["scored"]["gate"] for r in rs]
        d["gate_distribution"] = {str(g): gates.count(g) for g in range(5)}
        d["gate_mean"] = round(statistics.mean(gates), 3)
        d["gate_variance"] = round(statistics.pvariance(gates), 3)
        d["more_than_two_U"] = sum(r["scored"]["n_U"] > 2 for r in rs)
        items = sorted(rs[0]["scored"]["items"])
        d["item_U_share"] = {i: round(sum(r["scored"]["items"][i] == "U" for r in rs) / len(rs), 3) for i in items}
        per[m] = d
    res["by_stream"] = per

    devs = sorted({r["dev_id"] for r in unit})
    rel = {}

    def pair(a, b, label):
        both = [d for d in devs if a(d) and b(d)]
        if len(both) < 3:
            rel[label] = {"n": len(both)}
            return
        x = np.array([[a(d)["scored"]["gate"], b(d)["scored"]["gate"]] for d in both], float)
        icc = icc_single(x) if x.std() > 0 else None
        rel[label] = {"n": len(both), "gate_icc21": None if icc is None else round(icc, 3),
                      "gate_exact": round(float(np.mean(x[:, 0] == x[:, 1])), 3),
                      "checks": {c: agree([(a(d)["scored"]["checks"][c], b(d)["scored"]["checks"][c])
                                           for d in both]) for c in CHECKS}}

    for m in streams:
        pair(lambda d, m=m: S.get((m, d, "unit", 1)), lambda d, m=m: S.get((m, d, "unit", 2)),
             f"within {m} (rep1 vs rep2)")
    for m1, m2 in combinations(streams, 2):
        pair(lambda d: S.get((m1, d, "unit", 1)), lambda d: S.get((m2, d, "unit", 1)),
             f"between {m1} and {m2} (rep1)")
    for m in streams:
        pair(lambda d, m=m: S.get((m, d, "unit", 1)), lambda d, m=m: S.get((m, d, "fulltext", 1)),
             f"unit vs fulltext, {m}")
    res["reliability"] = rel

    rec = {}
    for m in streams:
        rs = [r for r in ok if r["model_requested"] == m]
        rg = [(r["parsed"].get("recognition") or {}) for r in rs]
        rec[m] = {"codings": len(rs),
                  "says_recognizes": sum(bool(g.get("recognizes_study")) for g in rg),
                  "guess_names_article": sum(recognized_right(g.get("identity_guess"), meta[r["dev_id"]])
                                             for g, r in zip(rg, rs)),
                  "says_knows_replication_outcome": sum(bool(g.get("knows_replication_outcome")) for g in rg)}
    res["recognition"] = rec

    ev = {}
    for m in streams:
        found = total = 0
        for r in (x for x in ok if x["model_requested"] == m):
            path = root / "blinded" / f"{r['dev_id']}.txt"
            if r["input"] != "unit" or not path.exists():
                continue
            text = norm(path.read_text(encoding="utf-8"))
            for it in (r["parsed"].get("items") or {}).values():
                for q in quotes((it or {}).get("evidence", "")):
                    total += 1
                    found += norm(q) in text
        ev[m] = {"quoted_strings": total, "found_verbatim": found,
                 "share": round(found / total, 3) if total else None}
    res["evidence_quotes_unit"] = ev

    Path(out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
