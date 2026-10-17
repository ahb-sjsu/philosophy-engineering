#!/usr/bin/env python
"""Self-test for pe_lint's P6 Integrity (PE-CLS-1.0 s7.6).

Builds fixtures in a temporary directory: one claim per path through
check_p6, plus reference p-values for the statistics I3 recomputes.

    python tools/test_pe_lint_p6.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pe_lint  # noqa: E402

# (test, stat, df, df2, tail) -> reference p (standard tables)
REFERENCE_P = [
    (("t", 2.0, 10, None, "two"), 0.07339),
    (("t", 2.228, 10, None, "two"), 0.0500),
    (("t", 1.812, 10, None, "one"), 0.0500),
    (("z", 1.96, None, None, "two"), 0.04999),
    (("f", 3.49, 2, 20, "two"), 0.0502),
    (("chi2", 3.841, 1, None, "two"), 0.0500),
    (("chi2", 18.307, 10, None, "two"), 0.0500),
]

GOOD_CSV = "id,gene,score\n1,SEPT2,0.5\n2,MARCH1,1.25\n3,TP53,2\n"
SCHEMA = {"key": "id", "columns": {"id": "int", "gene": "id", "score": "float"}}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    bad = []
    for args, want in REFERENCE_P:
        got = pe_lint.p_value(*args)
        if abs(got - want) > 5e-4:
            bad.append(f"p_value{args} = {got:.5f}, reference {want}")

    good_t = {"test": "t", "value": "2.23", "df": 10, "p": ".05", "n": 11}
    cases = {
        "I-OK": ({"inputs": [{"path": "data/good.csv", "sha256": sha(GOOD_CSV),
                              "schema": SCHEMA}],
                  "reported": [good_t, {"test": "grim", "mean": "3.45",
                                        "n": 20}]}, None),
        "I-NOINPUTS": ({"inputs": []}, "no inputs listed"),
        "I-ABSENT": ({"inputs": [{"path": "data/gone.csv", "sha256": "0"}]},
                     "is not in the repository"),
        "I-HASH": ({"inputs": [{"path": "data/good.csv", "sha256": sha("x"),
                                "schema": SCHEMA}]}, "does not match"),
        "I-RESTRICTED-BARE": ({"inputs": [{"restricted": True,
                                           "sha256": "ab"}]},
                              "restricted input missing"),
        "I-RESTRICTED-OK": ({"inputs": [{"restricted": True, "sha256": "ab",
                                         "custodian": "registry X",
                                         "access": "data-use agreement"}]},
                            None),
        "I-EXCEL": ({"inputs": [{"path": "data/excel.csv",
                                 "sha256": sha("id,gene,score\n1,2-Sep,0.5\n"),
                                 "schema": SCHEMA}]},
                    "shape of a spreadsheet coercion"),
        "I-DUPKEY": ({"inputs": [{"path": "data/dup.csv",
                                  "sha256": sha("id,gene,score\n1,A,1\n1,B,2\n"),
                                  "schema": SCHEMA}]}, "not unique"),
        "I-NOSCHEMA": ({"inputs": [{"path": "data/good.csv",
                                    "sha256": sha(GOOD_CSV)}]}, "no schema"),
        "I-DF": ({"inputs": [{"restricted": True, "sha256": "ab",
                              "custodian": "c", "access": "a"}],
                  "reported": [{"test": "t", "value": "2.50", "df": 150,
                                "p": ".014", "n": 95}]}, "is impossible"),
        "I-P": ({"inputs": [{"restricted": True, "sha256": "ab",
                             "custodian": "c", "access": "a"}],
                 "reported": [{"test": "t", "value": "1.20", "df": 30,
                               "p": ".02"}]}, "gives p in"),
        "I-GRIM": ({"inputs": [{"restricted": True, "sha256": "ab",
                                "custodian": "c", "access": "a"}],
                    "reported": [{"test": "grim", "mean": "3.47", "n": 10}]},
                   "GRIM"),
        "I-UNASSESSED": ("unassessed", None),
        "I-EXEMPT": ({"exempt": "theorem verified numerically; no data file"},
                     None),
        "I-MISSING": ("<omit>", "no integrity block"),
    }
    files = {"data/good.csv": GOOD_CSV,
             "data/excel.csv": "id,gene,score\n1,2-Sep,0.5\n",
             "data/dup.csv": "id,gene,score\n1,A,1\n1,B,2\n"}
    with tempfile.TemporaryDirectory() as root:
        os.makedirs(os.path.join(root, "claims"))
        os.makedirs(os.path.join(root, "data"))
        for rel, text in files.items():
            with open(os.path.join(root, rel), "w", newline="") as fh:
                fh.write(text)
        for cid, (blk, _) in cases.items():
            obj = {"spec": "PE-CLS-1.0", "id": cid, "class": "demonstrated",
                   "statement": cid, "evidence": [], "status": "classified",
                   "depends": {"uses": [], "corroborates": [], "cites": []}}
            if blk != "<omit>":
                obj["integrity"] = blk
            with open(os.path.join(root, "claims", cid + ".json"), "w") as fh:
                json.dump(obj, fh)
        claims = pe_lint.parse_native_ledger(root)
        findings, stats = pe_lint.check_p6(root, claims)

    errs: dict[str, list[str]] = {}
    for f in findings:
        if f.severity == "ERROR":
            errs.setdefault(f.claim, []).append(f.message)
    for cid, (_, frag) in cases.items():
        got = errs.get(cid, [])
        if frag is None and got:
            bad.append(f"{cid}: expected clean, got {got}")
        if frag is not None and not any(frag in m for m in got):
            bad.append(f"{cid}: expected '{frag}', got {got}")
    if "P6" not in pe_lint.LEVEL_PROPS["L4"] or "P6" in pe_lint.LEVEL_PROPS["L3"]:
        bad.append("P6 must be required at L4 and not at L3 (s9)")

    for b in bad:
        print("FAIL", b)
    n_ref = len(REFERENCE_P)
    print(f"{'FAIL' if bad else 'PASS'}: {n_ref} reference p-values, "
          f"{len(cases)} integrity paths, stats {stats}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
