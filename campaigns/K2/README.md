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
| `k2_witness_noisy_result.json` | noisy-proxy scenario (`--noisy`): a gate tracking what the baselines measure with error passes 7% at reliability 0.5, 22% at 0.3 (prereg 7.5) |
| [`k2_devset_rpp.py`](k2_devset_rpp.py), [`k2_devset_ml.py`](k2_devset_ml.py), [`devset/`](devset/) | development set, assembled from the projects' GitHub mirrors with Crossref-verified DOIs; no outcomes in the files (prereg 7.1) |

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
4. ~~Development list~~ assembled 2026-10-17: RP:P 99/100 DOIs, ML1 11/12, ML2 25/26, ML4 1/1; 132 distinct articles. Open: ML3 (OSF only), DEV-RPP-053 (RP:P row contradicts itself), DOI-match against SCORE (after Oct 19).
5. Prior art read 2026-10-17 (owner-supplied: Branch 2019; the IPR piece on Uzzi's text models; the Wikipedia "Replication crisis" article): baselines B1-B5 drafted (prereg 5), contamination-probe reference changed to a recall-free text model (4.2), Van Bavel 2016 identified as the closest precedent. Read Inbar 2016's text before sealing (fetch refused).
6. Rubric: v0 drafted 2026-10-17 ([`RUBRIC-v0.md`](RUBRIC-v0.md), 17 items over A1-A4 (A4.5 multiplicity added after the K-1 held-out test), evidence rule, U rule). Development set = RP:P + Many Labs originals (owner, 2026-10-17); both leave the test pool. Next: DOI-match the assembled list against SCORE (after Oct 19), seeded draw of ~40 claims, code, revise, freeze as `RUBRIC.md`, hash. Plus a ~30-claim non-psychology supplement from SCORE's journals/years, not replicated (owner, 2026-10-17; registration 7.1.1); test results also by discipline.
7. Reliability, contamination (now needs the recall-free text model, 4.2), and power probes; pilot.
8. Cold reread in a fresh session; then seal.

Human coders, an ethics determination if one is needed, and any compute
submission are owner decisions and have not been started.
