"""Forecast coverage of SCORE's replicated claims.

Uses from repli_outcomes only identifier/design columns; from the forecast files only
paper_id, method, and whether the score is present. No outcome and no forecast value is printed.
"""
import json
import sys
from collections import Counter

import pandas as pd
import rdata

rda, fdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
rep = rdata.read_rda(rda)["repli_outcomes"][["paper_id", "claim_id", "repli_version_of_record", "repli_type", "is_manylabs"]].copy()
rep["paper_id"] = rep["paper_id"].astype(str).str.strip()
rep["single_trace"] = rep["claim_id"].astype(str).str.contains("single-trace")

keyw = pd.read_csv(f"{fdir}/KeyW_CS_2020-10-19.csv", dtype={"paper_id": str})
keyw["paper_id"] = keyw["paper_id"].str.strip()
cs_cols = [c for c in keyw.columns if c.startswith("cs_m")]
anon = pd.read_csv(f"{fdir}/anon_p1_singletrace_confidence_scores.csv", dtype={"paper_id": str})
anon["paper_id"] = anon["paper_id"].str.strip()

keyw_any = set(keyw.loc[keyw[cs_cols].notna().any(axis=1), "paper_id"])
keyw_by = {c: set(keyw.loc[keyw[c].notna(), "paper_id"]) for c in cs_cols}
anon_any = set(anon.loc[anon["cs"].notna(), "paper_id"])
anon_by = {m: set(g.loc[g["cs"].notna(), "paper_id"]) for m, g in anon.groupby("method")}


def cover(df, papers):
    return {"claims": int(df["claim_id"].nunique()),
            "claims_with_forecast": int(df.loc[df["paper_id"].isin(papers), "claim_id"].nunique())}


claims = rep.drop_duplicates("claim_id")
vor = rep[rep["repli_version_of_record"].astype(str) == "True"].drop_duplicates("claim_id")
res = {
    "forecast_files": {"KeyW_CS_2020-10-19.csv": {"papers": int(keyw["paper_id"].nunique()), "papers_with_any_cs": len(keyw_any),
                                                  "cs_columns": len(cs_cols)},
                       "anon_p1_singletrace_confidence_scores.csv": {"papers": int(anon["paper_id"].nunique()),
                                                                     "methods": int(anon["method"].nunique()),
                                                                     "papers_with_any_cs": len(anon_any)}},
    "score_claims": int(claims["claim_id"].nunique()),
    "score_papers": int(claims["paper_id"].nunique()),
    "claims_by_trace": dict(Counter(claims["single_trace"].map({True: "single-trace", False: "bushel"}))),
    "keyw_any": cover(claims, keyw_any),
    "anon_any": cover(claims, anon_any),
    "either": cover(claims, keyw_any | anon_any),
    "both": cover(claims, keyw_any & anon_any),
    "keyw_any_single_trace": cover(claims[claims["single_trace"]], keyw_any),
    "keyw_any_bushel": cover(claims[~claims["single_trace"]], keyw_any),
    "keyw_any_version_of_record": cover(vor, keyw_any),
    "keyw_any_by_repli_type": {t: cover(g, keyw_any) for t, g in claims.groupby(claims["repli_type"].astype(str))},
    "keyw_any_by_manylabs": {t: cover(g, keyw_any) for t, g in claims.groupby(claims["is_manylabs"].astype(str))},
    "keyw_per_column": {c: cover(claims, s)["claims_with_forecast"] for c, s in keyw_by.items()},
    "anon_per_method_min_max": [min(cover(claims, s)["claims_with_forecast"] for s in anon_by.values()),
                                max(cover(claims, s)["claims_with_forecast"] for s in anon_by.values())],
    "score_papers_not_in_phase1_forecasts": int((~claims["paper_id"].isin(set(keyw["paper_id"]) | set(anon["paper_id"]))).sum()),
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
