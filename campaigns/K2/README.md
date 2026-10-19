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
| [`k2_sections.py`](k2_sections.py), [`k2_unit_coverage.py`](k2_unit_coverage.py), [`k2_unit_where.py`](k2_unit_where.py), [`k2_unit_residue.py`](k2_unit_residue.py) and their `_result.json` | coding unit = Method + Results sections plus the lead before each Method heading (up to 2,000 characters, not reaching past a heading or onto page 1; adopted 2026-10-18); what the unit keeps of each rubric check's evidence (A1 40%, A2 47%, A3 76%, A4 66%; 25/44/76/66 without the lead), where A1's lost evidence sat before the lead was added (`k2_unit_where`), and residue left after redaction (whole body 17 of 23 articles, unit 2, both false alarms); counts only, no article text |
| [`k2_pilot_code.py`](k2_pilot_code.py), [`k2_pilot_summary.py`](k2_pilot_summary.py), `k2_pilot_summary_result.json` | model-coder pilot (prereg 7.4, 2026-10-19): gpt-oss and minimax-m2 each coded the 22 blinded units twice plus 6 whole bodies; gate agreement between the two families ICC 0.11 (within each 0.66 and 0.63) against the 0.80 bar, so RUBRIC-v0 needs revision before sealing; scores only, raw responses stay on Atlas |
| [`RUBRIC-v1.md`](RUBRIC-v1.md), [`k2_rubric_split.py`](k2_rubric_split.py), `k2_rubric_split.json`, [`k2_dev_claims.py`](k2_dev_claims.py), `devset/claims_dev.csv` | rubric v1 (prereg 7.4.1): written from the v0 disagreements on a revise half of the 22 units, split and committed before any reasoning was read; scores the claim's focal test; coders now get the claim (RP:P original-side description and test, never a replication column); v1 pilot measured on the held-out half (`k2_pilot_v1_summary_result.json`): **v1 fails**, between-family gate ICC −0.31 on 9 held-out articles (0.61 on the revise half), A1 the main obstacle |
| [`k2_quote_check.py`](k2_quote_check.py), `k2_quote_check_v0_result.json`, `k2_quote_check_v1_result.json` | traces each quoted evidence string to the text the coder saw: v0 gpt-oss 170 of 191 found allowing for layout, v1 203 of 238; counts only |
| [`k2_score_doi_match.py`](k2_score_doi_match.py), `k2_score_doi_match_result.json` | SCORE archive (OSF BZFGY, CC0; data package `analysis data and code package 15 Dec 2025 1708.zip`, sha256 `80a221f0…7af2`, matches OSF; `analyst data.RData` sha256 `5e2ac8e7…6b`) read on Atlas with `rdata` 1.1.0: dataset shapes and column names, and the development set matched to SCORE by DOI. 1 of 132 matches (DEV-ML-013, SCORE paper 88xa, 1 new-data replication report; its outcome NOT opened). SCORE's papers are from 2009–2018 plus 100 from 2020, and RP:P's originals are from 2008. Only identifier and design columns of `repli_outcomes` are touched; no outcome value is read or stored |
| [`k2_devset_access.py`](k2_devset_access.py), `devset/access.csv` | open-access status of the 132 dev-set DOIs (OpenAlex): 30 open, 102 closed |
| [`k2_devset_rpp.py`](k2_devset_rpp.py), [`k2_devset_ml.py`](k2_devset_ml.py), [`devset/`](devset/) | development set, assembled from the projects' GitHub mirrors with Crossref-verified DOIs; no outcomes in the files (prereg 7.1) |

## Accounting

| | Count |
|---|---|
| Registrations drafted | 1 |
| Sealed | 0 |
| Run | 0 |

## Next, in order

1. After OSF's migration window closes (2026-10-19 09:00 EDT): list the archived SCORE repository (doi:10.17605/OSF.IO/BZFGY), confirm the per-claim outcome table, its license, the restricted fraction, and forecast coverage. **Partly done 2026-10-19:**
   - The license is CC0, and the code is MIT.
   - A per-claim outcome table exists: `repli_outcomes`, 427 replication reports keyed by `claim_id`. `orig_outcomes` has 825 claims, and `paper_metadata` has 4,000 papers.
   - The development-set overlap is 1 article (`k2_score_doi_match_result.json`).
   - The public package has 427 replication reports on 331 distinct claims; 309 reports are marked version of record.
   - **G5SNY (living repository, CC0), checked 2026-10-19.** It has no forecasts. It holds the same data package (same file name and size, 3,460,701 bytes), a figures zip, and one component, uqegb "Effect size conversions" (269 per-attempt folders of conversion scripts and some raw data). Nothing marks withheld records.
   - **Forecasts are elsewhere.** Mody et al. (osf.io/vgyed) is a preprint, version 2 of 2026-10-15, with a CC0 license. Its data links are tcfb9 ("Supplementary material for the SCORE paper", CC BY 4.0: Replication Markets and repliCATS forecast files, a pooled-markets table, a replication-outcomes CSV, scripts), d9x6s (repliCATS phase-one single-trace data, CC BY 4.0), and w4xsk (401: not public). Its abstract reports the forecasts validated on **only n = 37** high-power replications: AUC 0.76 for both Replication Markets and repliCATS. Rajtmajer et al. (osf.io/bdmte, machine assessment) links only to the programme page dtzx4. File contents not opened, and the outcome CSV in tcfb9 is under the same rule as SCORE's.
   - **Restricted fraction: still unknown.** No public file counts withheld records. Comparing the paper's own count of replicated claims with the 331 public ones would give it. `rr_internal_tracking.results_available` is documented as no longer meaningful.
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
