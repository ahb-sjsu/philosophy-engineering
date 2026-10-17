# PREREG K2: design-admissibility failures predict replication failure beyond the known predictors

**Status: DRAFT, NOT SEALED.** Sealing is the rename to `PREREG-K2.md`, the
commit of that rename, and the recording of its blob hash in `README.md`, in that
order, and only after Section 7 is filled from a rubric self-test, a
reliability probe, a contamination probe and a pilot that have actually run.
Before sealing, a session other than the drafting one rereads this file cold, and
the reread is recorded in Section 10 rather than applied silently.

This registration is itself subject to PE-CLS-1.0 §7.5 (P5). Its admissibility
block is Section 9. A design that cannot pass the property it tests is not
registered.

## 1. Claim under test

`PE-K2-1`, stage K-2 of [`docs/kuhnian-path.md`](../../docs/kuhnian-path.md).
Among published studies later subjected to a large-scale replication attempt,
studies whose **original** design fails one or more of the admissibility checks
A1 to A4 (PE-CLS-1.0 §7.5), as scored by auditors blind to the replication
outcome, replicate less often, and the gate score carries predictive information
about replication **beyond** the predictors already established in the
replication literature.

Why this claim and not another. The Kuhn paper (`papers/kuhn`) scored
Philosophy Engineering as failing Kuhn's crisis criterion, because the anomaly it
addresses does not register as failure on the reigning instruments. Replication
is a reigning instrument, and current practice already scores replication
failure as its own failure. If the gates explain part of that failure that
current practice cannot explain, the anomaly is visible on the predecessor's own
instrument. If they do not, the crisis cell stays failed, with a measurement
behind it.

## 2. Why incremental validity is the whole design

Replication failure is already predictable from cheap features: the original
effect size, its p-value, the sample size, and, where they exist, prediction
markets and surveys of researchers. A gate score could correlate with
replication simply by proxying those. A small-N study tends to fail A4 (unstable
denominators) and also tends not to replicate, and a gate that only rediscovers
small N has added nothing.

The gate is therefore **the increment**: out-of-sample discrimination of a model
with the baseline predictors plus the gate score, against the same model without
the gate score, on the same studies. The gate score's marginal correlation with
replication is reported and is not the gate.

## 3. World

**Candidate datasets (survey of 2026-10-17; items marked † are from memory, not
yet verified, and MUST be verified before sealing).**

| Role | Dataset | Size | Baselines on the same studies |
|---|---|---|---|
| Primary | **SCORE** replication set: Tyner et al., *Nature* 652:143–150 (2026), doi:10.1038/s41586-025-10078-y. Data: living repository doi:10.17605/OSF.IO/G5SNY; **archived as-published version doi:10.17605/OSF.IO/BZFGY** (the version this registration will name) | 274 claims of positive results from 164 papers (2009–2018, 54 journals). Replicated: 151/274 claims (55.1%), 80.8/164 papers weighted (49.3%), significance-in-original-pattern criterion | Human forecasts (repliCATS, Replication Markets) and machine scores are reported in separate SCORE preprints, not in the Nature paper; per-claim coverage **not confirmed** |
| Secondary | Pooled markets: Gordon et al., *PLOS ONE* (2021), doi:10.1371/journal.pone.0248780, R package `pooledmaRket` (RP:P, EE-RP, ML2, SSRP), **restricted to EE-RP and SSRP**: RP:P and Many Labs are the rubric development set (7.1, owner decision 2026-10-17) and MUST NOT be test data | ~39 findings (EE-RP 18, SSRP 21†); too few to grade alone, reported as secondary | Market prices and surveys (73% correct; r = 0.581 for prices); Altmejd et al. 2019 ML scores on an overlapping set† |
| Not primary | RP:CB (Errington et al., *eLife* 2021) | 50 experiments from 23 papers | Few; too few papers to cluster |
| Not primary | Brazilian Reproducibility Initiative (*eLife* 2026, reviewed preprint) | 45 experiments, 3 methods | DOI, license, original identification not confirmed |

Deduplicate SCORE against RP:P before pooling. Realistic total: about 250
original papers. **Power by simulation (Section 7.5):** at SCORE's shape (~274
claims, 164 papers, baseline AUC ~0.75) the design has 80% power only for a true
out-of-sample ΔAUC of about 0.055, and 31% at about 0.026. A real but small
increment is likely to be graded `fail` at a smallest effect of interest of
0.05; that is the bar doing its job, and the owner should set it knowing this.

**Consequence for the prospective arm.** SCORE's outcomes became public on
2026-04-01, so SCORE cannot be prospective. A partial substitute: model auditors
whose training cutoff predates 2026-04-01 cannot have learned SCORE outcomes from
the SCORE papers, though they may have seen preprints or forecasts. The
contamination probe measures the residue rather than assuming it is zero. A truly
prospective arm needs replications not yet reported at the seal (registered
replication reports in progress, or a new multi-site project); its frame is an
open item.

*Requirements on any dataset admitted:*

1. Per-study replication outcome under a definition the project fixed before its
   own results (not one this registration chooses after seeing them).
2. The original article identifiable per study, with full methods available to
   the auditors.
3. Baseline predictors available on the **same** studies: at minimum original
   effect size, p-value and N. Prediction-market or survey forecasts where they
   exist.
4. License permitting redistribution of derived codes, or else the codes are
   committed and the source is referenced.

The primary outcome definition is the one the replication project itself
registered. Where a project reports several, the registration names one here
before sealing and reports the others as secondary.

## 4. The audit instrument

**Rubric.** A coding rubric operationalizes A1 to A4 for published empirical
studies that were not designed with them in mind. Each check is scored 0 (passes),
1 (fails), or U (cannot be assessed from the article), with a required evidence
quote from the article for every 1. The rubric is frozen before any test-set
article is coded (Section 7.1).

| Check | Scored as a failure when the original article shows… |
|---|---|
| A1 Nonvacuity | No outcome reported or reportable would have been taken against the hypothesis: flexible or unstated primary outcome, a hypothesis stated only post hoc, components fit after the data that can absorb any result |
| A2 Identification | A key measure or construct used without validity or reliability evidence fit for its role, or calibrated on the same data it evaluates |
| A3 Intervention | No manipulation check, a manipulation check that fails or is not reported, or a manipulation that plausibly produces the measured response by construction (demand, stimulus identity with the outcome) |
| A4 Inference | Estimand, exclusions or denominator not fixed; exclusions that depend on condition; treatment-dependent attrition unaddressed; selected among analysis conventions |

**Gate score.** The count of checks scored 1, range 0 to 4. U is treated as
missing and its rate is reported per check. A study with more than two U is
excluded from the primary analysis and counted (A4 applied to this design).

**Auditors.** Two independent auditor streams per article:

- *Human:* at least two coders with methods training, blind to the replication
  outcome. Recruitment is the owner's decision and is not assumed here.
- *Model:* language-model auditors run with the frozen rubric, under the
  contamination control of Section 4.2. Their role is reliability and scale. The
  primary analysis uses the human consensus score unless Section 7 shows model
  and human scores interchangeable at the registered reliability bar.

### 4.1 Blinding

Articles are presented with title, authors, journal, year, and DOI removed, and
with reference lists removed. Blinding is imperfect for famous studies, and the
contamination probe below measures how imperfect.

### 4.2 Contamination

The replication outcomes of the large projects are widely known, and language
models have almost certainly seen them. A blind audit that recalls the outcome
measures memory, not design.

- **Contamination probe (instrument gate).** Each auditor, human and model, is
  asked separately, on the blinded article alone, whether it recognizes the
  study and whether it replicated. Out-of-sample discrimination of that direct
  guess is measured. If an auditor stream predicts replication from the blinded
  text **without the rubric** better than the baseline predictors do, by a
  margin to be fixed from the probe, that stream's gate scores are inadmissible
  for the retrospective arm.
- **Recognition exclusion.** Articles an auditor reports recognizing are coded by
  a different auditor, or excluded, and the count is reported.
- **Prospective arm.** Studies whose replication outcomes are not yet public at
  the seal are audited, and their codes are committed and hashed, before the
  outcomes appear. This arm cannot be contaminated by recall. It is the stronger
  test and probably the smaller one. Its sampling frame is fixed in Section 3
  before sealing.

## 5. Estimator

Primary: the difference in out-of-sample AUC (ΔAUC) between logistic models

- M0: replication outcome ~ baseline predictors
- M1: M0 + gate score

estimated by cross-validation, with folds blocked by replication project and,
within project, by original article, so that no article contributes to both fit
and evaluation. The 95% interval is a cluster bootstrap over original articles.
Clustering is by article because the gate score lives on the article
(several replicated effects can come from one paper).

Secondary: the M1 gate-score coefficient and its interval; per-check
contributions (A1 to A4 entered separately), reported and not gated; the
retrospective and prospective arms separately.

## 6. Bars and what falsifies

*Bars are fixed from the pilot before sealing (Section 7). The structure is
fixed now.*

**Instrument gates.** A miss voids the run and does not grade the claim.

| Gate | Passes when |
|---|---|
| I1 Rubric reliability | Inter-rater agreement on the gate score at or above a bar fixed from the reliability probe |
| I2 Contamination | Section 4.2 probe within its bar for every auditor stream used in the primary analysis |
| I3 Blinding leak | Redaction leaves none of title, author, journal, year or DOI, by automated check |
| I4 Coverage | Fewer than a fixed fraction of studies excluded for U or recognition |
| I5 Power | The minimum detectable ΔAUC at the realized N is stated and is below a value fixed before sealing; if it is not, the run is reported as underpowered and grades nothing |

**Physics gate.** A miss refutes the claim at this scope.

- **Pass:** the lower end of the 95% interval for ΔAUC exceeds 0 **and** the
  gate-score coefficient has the predicted sign (more failures, less
  replication).
- **Fail:** the upper end of the 95% interval for ΔAUC lies below the smallest
  effect of interest fixed before sealing, i.e. the increment is shown small. A result between the two is
  reported as unresolved, not as a pass.

**What a fail means.** The admissibility gates do not explain replication failure
beyond what is already known. The crisis cell of the Kuhn paper's table stays at
Fail, and the plan's §5 position 2 (reform, not paradigm) is the one supported.

## 7. Before sealing (all run, recorded here)

### 7.0 Dataset survey

Run 2026-10-17. The Nature paper's data and code availability statements were
read directly. They give the living repository (OSF G5SNY) and an archived,
as-published registration (OSF BZFGY) holding the data, code, and a
push-button package that regenerates every statistic. Only data that "can be
shared without restriction" are public, so some per-claim records may be
withheld. The survey's earlier pointer (osf.io/dtzx4) is the COS programme page,
not the paper's data. **OSF was down for a scheduled migration
(2026-10-16 09:00 to 2026-10-19 09:00 EDT, status.cos.io), so the file layout,
license, and the restricted fraction are still unconfirmed.** After the window:
list BZFGY's files, confirm a per-claim outcome table and its license, count the
restricted claims, and locate the forecast data (Mody et al., osf.io/vgyed;
Rajtmajer et al., osf.io/bdmte).

### 7.0.1 Prior art that this design must cite and distinguish

- **META-REP project (Jekel & Smela, DFG SPP 2317)**, "Replicating Failed
  Replications: A Validity-based Framework for Predicting Replication Success":
  codes validity indicators of original studies (construct validation of
  measures, attrition, design; Fabrigar's four validities) and adds them to
  Altmejd-style prediction. Ran Feb 2022 to Jan 2025 (Cologne project page).
  **Re-checked 2026-10-17: no paper, preprint, dataset, or predictive result
  found;** the one public output is a poster abstract, Smela (2024), "Predicting
  the Success of Replication Based on Validity Indicators", TeaP 2024
  Regensburg, coding attrition, sample differences, measure validation, and
  within/between design (abstract seen only via search summary). Overlap: A2
  (measure validation) and part of A4 (attrition). **Not covered there:** A1
  nonvacuity, A3 manipulation checks and construction, A4 treatment-dependent
  selection and selected scoring conventions. The registration MUST cite it and
  MUST re-check for publication at sealing. Framework source: **Fabrigar,
  Wegener & Petty 2020**, *Personality and Social Psychology Review*
  24(4):316–344, doi:10.1177/1088868320931366.
- **Boyce, Mathur & Frank 2023**, *R. Soc. Open Sci.* 10(11):231240,
  doi:10.1098/rsos.231240: 176 student replications; codes design features
  (within/between subjects, vignettes, trials, online switch) against
  replication; within-subjects OR 2.59, weakened once effect size and p are
  in. No manipulation checks coded, no AUC. Precedent for design features as
  predictors; its weak increment is a warning for this bar.
- **Van Bavel et al. 2016, PNAS**† coded RP:P originals for contextual
  sensitivity and related it to replication; Inbar 2016† disputed the increment.
  Direct precedent for coding originals beyond N and effect size.
- **Chester & Lasko 2021**, *Perspect. Psychol. Sci.* 16(2):377–395: 348 JPSP
  manipulations coded; ~one third had a manipulation check. Not linked to
  replication. Base rate for A3.
- **Flake & Fried 2020** (AMPPS, doi:10.1177/2515245920952393) and **Hussey &
  Hughes 2020** (AMPPS 3(2):166–184): measurement practices. Source for A2's
  rubric.
- **Baselines:** Altmejd et al. 2019, *PLOS ONE* 14(12):e0225826 (AUC 0.77 CV,
  0.73 preregistered out-of-sample); Yang, Youyou & Uzzi 2020, PNAS (0.65–0.78);
  SCORE forecasters (76–78% best-metric). **The increment is measured against
  the strongest baseline available on the same claims, not the weakest.**

### 7.1 Rubric development set

The rubric is developed on articles **disjoint** from the test set (not in any
replication project used for testing, or a held-out project). Its versions are
committed. The frozen version's hash goes in Section 9.

**Development set (owner decision, 2026-10-17): the originals of the
Reproducibility Project: Psychology (Open Science Collaboration 2015, 100
replications†) and of the Many Labs projects (ML1 to ML5†).** Consequences,
recorded now so none is discovered later:

1. **They leave the test pool permanently.** No RP:P or Many Labs claim is test
   data in any arm, including the secondary arm (Section 3).
2. **Disjointness from SCORE is checked, not assumed.** RP:P sampled 2008
   issues and SCORE's papers run 2009 to 2018, so they should not overlap; Many
   Labs effects span decades, and ML2 in particular includes post-2009
   originals. Before the freeze, every development-set original is matched by
   DOI against SCORE's claim list, and any match is removed from the
   development set, never from the test set. The match list is committed.
3. **Coverage gap.** Both projects are psychology. SCORE spans economics,
   political science, sociology, and others, and the rubric's items on
   reliability conventions (A2.2) and analysis choices (A4.4) differ by field.
   A psychology-only freeze would be a psychology-calibrated rubric applied
   to a multi-discipline test set. **Resolved (owner, 2026-10-17): a
   non-psychology supplement is added (7.1.1).** Test results are also
   reported by discipline, as a secondary analysis.
4. **The development set is the contamination probe's calibration set.** These
   are the most famous replications in the literature. Recall on them gives the
   ceiling of the contamination problem; the Section 4.2 probe's bar is set
   from how well each auditor stream guesses RP:P and Many Labs outcomes from
   blinded text, before it is applied to SCORE.
5. **Outcomes are visible to the developers.** Rubric development uses item
   reliability and evidence quality only. Development-set replication outcomes
   MUST NOT be used to choose, weight, or cut items: that would fit the rubric
   to the outcome it is meant to predict. Any item change is justified by
   reliability or by a coding ambiguity, in a dated note.

#### 7.1.1 Non-psychology supplement

*Purpose:* calibrate the rubric's field-dependent items on the disciplines
SCORE tests, so that the freeze is not psychology-only. *Used for:* inter-rater
reliability by discipline (I1), the field conventions A2.2 (reliability) and
A4.2 (the attrition-difference threshold) are set from, and evidence-rule
practice. *Not used for:* anything involving replication. These claims have no
replication outcome, so no item can be fitted to one.

*Frame.* Articles from the **same journals and years as SCORE** (2009 to 2018;
SCORE's journal list, taken from its data) in its non-psychology disciplines,
that were **not** among SCORE's replicated claims and were never replicated in
any project used here. Same journals and years means the supplement differs from
the test set only in not having been replicated, which is the property wanted.
Preferred source, to verify when OSF returns: if SCORE's data include claims
that were sampled and forecast but not replicated, draw from those, because
their claim statements already exist in SCORE's own format. Otherwise, draw
articles from the journal list and pick the claim by SCORE's documented
claim-selection procedure, or failing documentation, the first finding stated
in the abstract with an inferential test.

*Size.* About 30 claims, with at least 8 each from economics and political
science and the rest spread across SCORE's other non-psychology disciplines,
in proportion to SCORE's own mix. Seeded draw; the seed is committed before the
draw. Two independent coders, as for the main development set.

*Disjointness.* Every supplement article is matched by DOI against SCORE's
replicated claims and against the secondary arm (EE-RP, SSRP); any match is
redrawn. The supplement is development data permanently and never test data.

**Size and sampling (main development set).** About 40 claims, stratified
across RP:P's three journals and the Many Labs projects, drawn by seeded random sample from the
full list once it is assembled; the seed is committed before the draw. Two
coders code all 40 independently.

**Access.** Coders need full texts. Most originals are paywalled journal
articles; access route (institutional library) to be confirmed. Article PDFs
are not committed to this public repository; their DOIs and hashes are.

### 7.2 Reliability probe

Not run.

### 7.3 Contamination probe

Not run.

### 7.4 Pilot

Not run. Purpose: realized N, U rate, recognition rate, and the variance needed
to size the I5 power bar and the physics bar.

### 7.5 A1 witness, construction check, and power (simulation, run 2026-10-17)

`k2_witness.py` draws synthetic SCORE-shaped data (assumptions in its `WORLD`
block, not evidence about the gates) and runs the registered analysis
`k2_analysis.py` 400 times per scenario, 500 bootstrap draws each, seed
20261017, SESOI 0.05, on Atlas. Result committed as `k2_witness_result.json`.

| Scenario | Mean ΔAUC | pass | fail | unresolved |
|---|---:|---:|---:|---:|
| null (gate independent) | -0.003 | 0.000 | 1.000 | 0.000 |
| proxy (gate tracks N only) | -0.002 | 0.003 | 0.998 | 0.000 |
| signal, slope 0.25 | 0.005 | 0.028 | 0.923 | 0.050 |
| signal, slope 0.5 | 0.026 | 0.310 | 0.413 | 0.278 |
| signal, slope 0.75 | 0.057 | 0.843 | 0.030 | 0.128 |
| signal, slope 1.0 | 0.092 | 0.983 | 0.000 | 0.018 |

**A1 witness: PASS.** The analysis does not credit a gate score with no signal
(0/400) or one that only proxies a baseline (1/400). **Limits:** the proxy
scenario has the gate track a baseline M0 already contains. A gate that tracks a
quantity the baselines measure *with error* would earn a legitimate-looking
increment; that case is not simulated and belongs in the reread. The bootstrap
resamples pooled out-of-sample predictions and does not refit, so fold-to-fold
variance is not in the interval; the null's zero pass rate suggests this is not
inflating passes here, but it is a choice the reread should examine.

## 8. Compute

Model auditors run on NRP or Atlas, never on the laptop. NRP submissions follow
the PREFLIGHT checklist in the NRP policy memory and go through the existing
NATS burst path. No sizing is chosen in this draft.

## 9. Admissibility block (PE-CLS-1.0 §7.5, applied to this design)

| Check | Discharged by | Status |
|---|---|---|
| A1 Nonvacuity | **Witness record:** a synthetic dataset in which gate scores are independent of replication; the registered analysis code must score it as a miss. **Free components:** rubric wording (frozen on the development set before test coding); outcome definition (fixed by the replication projects); model auditor prompts (frozen with the rubric) | Witness built and run: PASS (7.5) |
| A2 Identification | The gate score is identified only if coders agree: I1. The rubric is fit on the development set only, disjoint from the test set (7.1) | Pending 7.1, 7.2 |
| A3 Intervention | Not applicable: observational, no manipulation. **Construction check still applies:** the gate score could encode the outcome through recall; I2 and the prospective arm are the construction checks | Pending 7.3 |
| A4 Inference | Estimand ΔAUC (Section 5), denominator all studies in the sampling frame, exclusions counted per reason (U, recognition), one outcome definition named before sealing | Partly fixed; outcome definition pending Section 3 |

## 10. Reread record

None yet.

## 11. Known weaknesses

- **The author designed the gates being tested.** The rubric operationalizes
  checks the author wrote. An independent methods team, as in plan stage K-3,
  would remove this; K-2 does not. The rubric's freeze on a disjoint development
  set and the cold reread are the mitigations, and they are partial.
- **Published articles under-report.** A missing manipulation check may be
  missing from the article and present in the study. The rubric scores what the
  article shows, which is what a reviewer sees, and the claim is scoped to that.
- **Retrospective contamination may be unremovable.** If I2 fails for every
  auditor stream, the retrospective arm grades nothing and the prospective arm
  carries the claim alone.
- **Domain.** The large replication projects are mostly social and behavioral
  science. A pass is scoped there.

## 12. What a pass would and would not mean

A pass would mean that design defects of the kind the gates name explain part
of a failure that current practice measures and does not explain: the shape a
Kuhnian crisis requires, on the predecessor's own instrument. It would not mean
that the gates improve research going forward (that is K-3's prospective
multi-team study), that Philosophy Engineering is a paradigm (community and
incommensurability are untouched), or that the result holds outside the domains
sampled.
