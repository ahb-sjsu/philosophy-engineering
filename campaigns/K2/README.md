# Campaign K2: do admissibility failures predict replication failure?

Stage K-2 of [`docs/kuhnian-path.md`](../../docs/kuhnian-path.md). It tests the
crisis criterion that [`papers/kuhn`](../../papers/kuhn/) scored as failed, using
replication outcomes, which the reigning practice already treats as its own
measure of failure.

| File | State |
|---|---|
| [`PREREG-K2-DRAFT.md`](PREREG-K2-DRAFT.md) | DRAFT, NOT SEALED (2026-10-17) |
| [`k2_analysis.py`](k2_analysis.py) | registered estimator (numpy only): blocked-CV ΔAUC, paper-cluster bootstrap, verdict |
| [`k2_witness.py`](k2_witness.py), `k2_witness_result.json` | A1 witness + power simulation, run on Atlas |

## Accounting

| | Count |
|---|---|
| Registrations drafted | 1 |
| Sealed | 0 |
| Run | 0 |

## Next, in order

1. After OSF's migration window closes (2026-10-19 09:00 EDT): list the archived SCORE repository (doi:10.17605/OSF.IO/BZFGY), confirm the per-claim outcome table, its license, the restricted fraction, and forecast coverage.
2. ~~META-REP check~~ done 2026-10-17: no results published (poster only); overlaps A2 and part of A4. Re-check at sealing.
3. ~~A1 witness~~ done 2026-10-17: `k2_witness.py` on `k2_analysis.py`, PASS (null 0/400, proxy 1/400). Power: 80% at true ΔAUC ~0.055.
4. Rubric: v0 drafted 2026-10-17 ([`RUBRIC-v0.md`](RUBRIC-v0.md), 16 items over A1-A4, evidence rule, U rule). Next: choose a development set disjoint from SCORE's test claims, code it, revise, freeze as `RUBRIC.md`, hash.
5. Reliability, contamination, and power probes; pilot.
6. Cold reread in a fresh session; then seal.

Human coders, an ethics determination if one is needed, and any compute
submission are owner decisions and have not been started.
