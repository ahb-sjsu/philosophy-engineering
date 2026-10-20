"""Forecast coverage on the analysis set: the report_ids in repli_binary (only the key column is used).

Joins repli_binary.report_id to repli_outcomes identifiers (paper_id, claim_id, type_internal,
is_covid, is_manylabs), then to the per-paper forecast files. No outcome or forecast value is read out.
"""
import json
import sys
from collections import Counter

import pandas as pd
import rdata

rda, fdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
d = rdata.read_rda(rda)
keys = set(d["repli_binary"]["report_id"].astype(str).str.strip())
rep = d["repli_outcomes"][["report_id", "paper_id", "claim_id", "type_internal", "is_covid", "is_manylabs"]].copy()
for c in ("report_id", "paper_id"):
    rep[c] = rep[c].astype(str).str.strip()
a = rep[rep["report_id"].isin(keys)]
markets = set(pd.read_csv(f"{fdir}/KeyW_CS_2020-10-19.csv", dtype={"paper_id": str})["paper_id"].str.strip())
replicats = set(pd.read_csv(f"{fdir}/anon_p1_singletrace_confidence_scores.csv", dtype={"paper_id": str})["paper_id"].str.strip())
a = a.assign(forecast=a["paper_id"].isin(markets))
res = {
    "repli_binary_rows": len(d["repli_binary"]),
    "matched_reports": len(a),
    "unmatched_report_ids": len(keys - set(rep["report_id"])),
    "claims": int(a["claim_id"].nunique()),
    "papers": int(a["paper_id"].nunique()),
    "by_type_internal": {t: {"claims": int(g["claim_id"].nunique()), "on_forecast_paper": int(g.loc[g["forecast"], "claim_id"].nunique())}
                         for t, g in a.groupby(a["type_internal"].astype(str))},
    "claims_on_forecast_paper": int(a.loc[a["forecast"], "claim_id"].nunique()),
    "papers_with_forecast": int(a.loc[a["forecast"], "paper_id"].nunique()),
    "markets_equals_replicats_papers": markets == replicats,
    "is_manylabs": dict(Counter(a["is_manylabs"].astype(str))),
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
