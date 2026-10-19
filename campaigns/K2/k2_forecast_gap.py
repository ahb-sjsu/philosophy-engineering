"""Which SCORE phase the forecast-less replicated claims come from (identifier and tracking flags only)."""
import sys
from collections import Counter

import pandas as pd
import rdata

d = rdata.read_rda(sys.argv[1])
rep = d["repli_outcomes"][["paper_id", "claim_id", "is_covid", "type_internal"]].drop_duplicates("claim_id").copy()
rep["paper_id"] = rep["paper_id"].astype(str).str.strip()
fc = set(pd.read_csv(f"{sys.argv[2]}/KeyW_CS_2020-10-19.csv", dtype={"paper_id": str})["paper_id"].str.strip())
st = d["paper_status_tracking"].copy()
st["paper_id"] = st["paper_id"].astype(str).str.strip()
st = st.drop_duplicates("paper_id").set_index("paper_id")
rep["forecast"] = rep["paper_id"].isin(fc)
for col in ("is_covid", "type_internal"):
    print(col, dict(Counter(zip(rep["forecast"], rep[col].astype(str)))))
for flag in ("p1_delivery", "p2_delivery", "bushel"):
    v = rep["paper_id"].map(st[flag].astype(str)) if flag in st else None
    print(flag, dict(Counter(zip(rep["forecast"], v.fillna("not tracked")))))
