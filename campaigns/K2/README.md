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
| [`k2_placebo_witness.py`](k2_placebo_witness.py), `k2_placebo_witness_result.json`, `k2_placebo_witness_run1.json` | placebo-gate witness (prereg 4.3 item 2): run 1 FAILED on its own design (leak too weak to credit), run 2 PASSED (quiet on signal and adjusted strata, fires on an unadjusted leak) |
| [`k2_reliability_witness.py`](k2_reliability_witness.py), `k2_reliability_witness_result.json` | how coder error (per-check flips) attenuates the physics test, one coder vs the two-coder mean; places the I1 single-coder ICC bar (prereg 7.2) |
| [`k2_blinding.py`](k2_blinding.py), [`k2_blinding_test.py`](k2_blinding_test.py), `k2_blinding_test_result.json` | redaction and gate I3 leak check (prereg 4.1), version 2: version 1 passed its synthetic test and missed eleven leak kinds on real articles; v2 test PASSES on all 132 records |
| [`k2_fulltext_fetch.py`](k2_fulltext_fetch.py), [`k2_intake.py`](k2_intake.py), `devset/crossref_meta.json`, `devset/fetch_log.csv`, `devset/fetch_log_manual.csv`, `devset/intake_manifest.csv` | open-access fetch (7 of 30 'open' articles by script; 17 more on 2026-10-18 by script from Atlas and through the owner's browser, 6 unobtainable) and intake: PDF text, references cut, redaction, I3, scan quarantine, over-redaction share; PDFs and texts stay on Atlas (copyright), only metadata and hashes here |
| [`k2_devset_access.py`](k2_devset_access.py), `devset/access.csv` | open-access status of the 132 dev-set DOIs (OpenAlex): 30 open, 102 closed |
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
5a. 2026-10-17 later: Inbar 2016 READ (the coded feature's association vanished with subdiscipline as a covariate, OR 0.85, P 0.51): B3 is a covariate in the primary M0, never an interaction test; Van Bavel's coding design read (reliability was of a 3-rater mean on 25 of 100). Van Bavel's reply to Inbar read in full later the same day (quotes checked against the PMC page in the owner's browser): with subdiscipline and the coded feature in one model neither is significant (P = 0.453, P = 0.132), so the RP:P could not separate them; B3 coding source now fixed in prereg 5. Placebo gate and U-sensitivity analyses implemented and witnessed. Dev-set open access 23%: full-text access is the binding owner decision.
6. Rubric: v0 drafted 2026-10-17 ([`RUBRIC-v0.md`](RUBRIC-v0.md), 17 items over A1-A4 (A4.5 multiplicity added after the K-1 held-out test), evidence rule, U rule). Development set = RP:P + Many Labs originals (owner, 2026-10-17); both leave the test pool. Next: DOI-match the assembled list against SCORE (after Oct 19), seeded draw of ~40 claims, code, revise, freeze as `RUBRIC.md`, hash. Plus a ~30-claim non-psychology supplement from SCORE's journals/years, not replicated (owner, 2026-10-17; registration 7.1.1); test results also by discipline.
7. Reliability, contamination (now needs the recall-free text model, 4.2), and power probes; pilot. Reliability bar placed 2026-10-17 by simulation (prereg 7.2): coder noise turns true effects into graded fails, so I1 = single-coder ICC(2,1) >= 0.80 on the run's own double codes (draft); Van Bavel's coders (~0.67 single-coder, derived) would miss it. Blinding check (I3) implemented and witnessed 2026-10-17 (prereg 4.1). Contamination reference (4.2): recall-free rule written; competence limit recorded, a self-contrast gate recommended (owner/seal decision). Intake run on the 7 downloadable open articles: 6 released, 1 scan quarantined, redaction 0.6-2.1% of words.
8. Cold reread in a fresh session; then seal.

Human coders, an ethics determination if one is needed, and any compute
submission are owner decisions and have not been started.
