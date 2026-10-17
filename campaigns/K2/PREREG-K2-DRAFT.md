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
| Secondary | Pooled markets: Gordon et al., *PLOS ONE* (2021), doi:10.1371/journal.pone.0248780, R package `pooledmaRket` (RP:P, EE-RP, ML2, SSRP), **restricted to EE-RP and SSRP**: RP:P and Many Labs are the rubric development set (7.1, owner decision 2026-10-17) and MUST NOT be test data | ~39 findings (EE-RP 18, Camerer et al. 2016, Science, doi:10.1126/science.aaf0918; SSRP 21, Camerer et al. 2018, Nat. Hum. Behav., doi:10.1038/s41562-018-0399-z; counts verified 2026-10-17); too few to grade alone, reported as secondary | Market prices and surveys (73% correct; r = 0.581 for prices); Altmejd et al. 2019 ML scores on an overlapping set† |
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
  guess is measured. **Reference (revised 2026-10-17):** the first draft
  compared that guess with the baseline predictors. That comparison cannot
  separate recall from reading, because blinded text predicts replication
  without any recall (Yang, Youyou & Uzzi 2020, 7.0.1: narrative-only accuracy
  0.68 out of sample). The reference is therefore a **recall-free text
  predictor**: a text model fit on the development set only (RP:P and Many
  Labs, 7.1), which cannot have seen SCORE outcomes. A stream whose no-rubric
  guess beats that reference, by a margin fixed from the probe, has its gate
  scores declared inadmissible for the retrospective arm. A second, independent
  signal is recorded and is not gated: the guess's discrimination on claims
  whose outcomes were public before the model's training cutoff, against those
  made public after it (SCORE, 2026-04-01).
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

**Baseline set (draft 2026-10-17, owner to confirm; availability on SCORE
claims unconfirmed until OSF returns).** Each enters because prior work shows it
predicts replication, or because a gate could proxy it:

| | Baseline | Why |
|---|---|---|
| B1 | original effect size, p-value, N (log) | Altmejd et al. 2019; the statistical-inference rival (Branch 2019; Stanley et al. 2018) lives here |
| B2 | experimental or not; main effect or interaction | Youyou et al. 2023 (experiments replicate less) and Altmejd et al. 2019 (interactions); A3 applies only to experiments, so without B2 an A3 increment can be the design type |
| B3 | discipline, and subfield within psychology | the risk named by Inbar 2016's title; RP:P's replication rate differed by subfield (cognitive and social) |
| B4 | recall-free text score (the 4.2 reference model) | Yang et al. 2020: text alone predicts |
| B5 | forecasts (markets, surveys), where present on the same claims | strongest known human baseline |

The primary M0 is B1 to B3 plus B5 where available. **M0+B4 is a registered
secondary test:** the gates beyond a text model is a stronger claim than the
gates beyond known features, and both are reported. Which of the two is primary
is an owner decision, recorded before sealing.

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
- **Van Bavel, Mende-Siedlecki, Brady et al. 2016**, *PNAS* 113:6454–6459,
  doi:10.1073/pnas.1521897113 (verified 2026-10-17, abstract read via Europe
  PMC): recoded the 100 RP:P originals for the contextual sensitivity of the
  research topic; it "was associated with replication success, even after
  statistically adjusting for several methodological characteristics (e.g.,
  statistical power, effect size)", and the association "did not differ across
  psychological subdisciplines". **This is K-2's design, on K-2's development
  set:** a coded property of the original, tested for an increment over the
  known predictors. Differences: one property rather than four checks; a
  topic-level judgement rather than a design defect with an evidence quote;
  in-sample regression rather than out-of-sample ΔAUC. **Inbar 2016**, *PNAS*
  113, doi:10.1073/pnas.1608676113, "Association between contextual dependence
  and replicability in psychology may be spurious" (verified as published; the
  text could not be read on 2026-10-17, PMC and PNAS both refused the fetch, and
  its argument is NOT summarized here from memory; read before sealing). The
  title alone states the risk this design must answer: a coded property that
  proxies something else. Consequence: baseline B3 below.
- **Chester & Lasko 2021**, *Perspect. Psychol. Sci.* 16(2):377–395: 348 JPSP
  manipulations coded; ~one third had a manipulation check. Not linked to
  replication. Base rate for A3.
- **Flake & Fried 2020** (AMPPS, doi:10.1177/2515245920952393) and **Hussey &
  Hughes 2020** (AMPPS 3(2):166–184): measurement practices. Source for A2's
  rubric.
- **Baselines:** Altmejd et al. 2019, *PLOS ONE* 14(12):e0225826,
  doi:10.1371/journal.pone.0225826 (verified; four replication projects;
  cross-validated accuracy 70%, AUC 0.77; preregistered out-of-sample 71%, AUC
  0.73; "sample and effect sizes in original papers, and whether reported
  effects are single-variable main effects or two-variable interactions, are
  predictive"); Yang, Youyou & Uzzi 2020 (below); SCORE forecasters (76–78%
  best-metric). **The increment is measured against the strongest baseline
  available on the same claims, not the weakest.**
- **Yang, Youyou & Uzzi 2020**, *PNAS* 117(20):10762–10768,
  doi:10.1073/pnas.1909046117 (verified; full text read via PMC7245108): a
  text model (word2vec over the paper with "all nontext content (e.g.,
  authors, numbers, graphics, etc.)" stripped; bagged random forests and
  logistic) **trained on RP:P (n = 96 papers)**, tested on four out-of-sample
  sets (psychology n = 117, Psychfiledrawer 57, EE-RP 18, Economics
  Replication Wiki 122); accuracy 0.65 to 0.78 out of sample; narrative-only
  0.68 against reported-statistics-only 0.66 (P < 0.001); no AUC reported.
  Three consequences for this design, each applied below: (i) **text alone
  predicts replication without recall**, which breaks the contamination probe
  as first drafted (4.2, revised); (ii) a text score is a known predictor and
  belongs in a baseline (B4); (iii) its training set is this design's
  development set, and its EE-RP test set is in this design's secondary arm.
- **Youyou, Yang & Uzzi 2023**, *PNAS* 120(6):e2208863120,
  doi:10.1073/pnas.2208863120 (verified; abstract read): the 2020 model applied
  to 14,126 papers from six top psychology journals over 20 years;
  "replication rates are strongly correlated with research methods in all
  subfields. Experiments replicate at a significantly lower rate than do
  non-experimental studies." **A3 applies only to experiments,** so A3
  failures can track being an experiment. Consequence: baseline B2.
- **Rival explanations the baselines must carry.** Branch 2019, *Perspect.
  Behav. Sci.* 42(1):77–89, doi:10.1007/s40614-018-0158-5 (position paper, no
  data; owner-supplied 2026-10-17): significance testing and its use as a
  publication criterion as "the prime culprit". Stanley, Carter & Doucouliagos
  2018, *Psychol. Bull.* 144:1325–1346, doi:10.1037/bul0000169: mean power
  33.1–36.4% over 200 meta-analyses, median heterogeneity I² = 74%. Both live
  in the p, N and effect-size baselines; a pass means the gates add something
  beyond them, and says nothing against them.
- **Sources for rubric items (development, not baselines):** Nieuwenhuis,
  Forstmann & Wagenmakers 2011, *Nat. Neurosci.* 14:1105–1107,
  doi:10.1038/nn.2886 (78 of 157 papers tested a difference by contrasting
  significant with non-significant: an A4 candidate item); Begley & Ioannidis
  2015, *Circ. Res.* 116:116–126, doi:10.1161/circresaha.114.303819 (blinding,
  positive and negative controls, validated reagents: A3/A2 candidates);
  Loken & Gelman 2017, *Science* 355:584–585, doi:10.1126/science.aal3618
  (measurement error: A2); García-Berthou & Alcaraz 2004, *BMC Med. Res.
  Methodol.* 4:13, doi:10.1186/1471-2288-4-13 (11% of results incongruent
  between test statistic and p: PE-CLS P6 I3, recomputable, not coded).
  Candidate items enter the rubric only through the 7.1 procedure.
- Survey of the Wikipedia article "Replication crisis" (revision 1379868267,
  read 2026-10-17, owner-supplied): the article was read in full; its 255
  unique references were scanned by title only, and that scan found no further
  work coding design defects of originals against replication (a title scan
  can miss one).
  Makel, Plucker & Hegarty 2012 (doi:10.1177/1745691612460688; replication
  success 91.7% with author overlap against 64.6% without) names a
  replication-side covariate; Serra-Garcia & Gneezy 2021 (*Sci. Adv.*,
  doi:10.1126/sciadv.abd1705) finds that experts predict replicability.

### 7.1 Rubric development set

The rubric is developed on articles **disjoint** from the test set (not in any
replication project used for testing, or a held-out project). Its versions are
committed. The frozen version's hash goes in Section 9.

**Development set (owner decision, 2026-10-17): the originals of the
Reproducibility Project: Psychology (Open Science Collaboration 2015, 100
replications) and of the Many Labs projects (ML1 to ML5; all five article DOIs verified 2026-10-17, see the table below).** Consequences,
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

**Assembled 2026-10-17 (OSF offline; from the projects' public GitHub
mirrors, DOIs verified through Crossref; files in `devset/`).**

| Source | Entries | DOI resolved | How verified |
|---|---:|---:|---|
| RP:P (CenterForOpenScience/rpp, `RPPdataConverted.csv`, sha256 e753eae6…) | 100 replications | 99 (97 distinct articles) | Crossref record agrees on ISSN, volume, first page and main title |
| ML1 (`ML_Original_ES95CI.xls`) | 12 originals | 11 | cited in the ML1 article's Crossref reference list, matched on first author and year (one by co-author, one by elimination) |
| ML2 (per-effect folder names) | 26 originals (28 effects) | 25 | as ML1, in the ML2 reference list |
| ML4 | 1 (Greenberg et al. 1994, study 1) | 1 | PubMed 7965609, the ID the ML4 repository README links |
| ML3 | 10 effects | **pending** | no public list outside OSF; not filled from memory |
| ML5 | (its 10 originals) | n/a | all 10 are already in the RP:P list (DOI match against ML5's reference list) |

- Without DOI: DEV-RPP-053 (RP:P's own row gives a *Psychological Science*
  title with a *JPSP* volume and page: Crossref's record at that volume and page
  is a different Rule & Ambady 2008 article; resolve from the OSF project page,
  never by choosing); DEV-ML-006 (Hyman & Sheatsley 1950) and DEV-ML-019
  (Tversky & Gati 1978), books or chapters without DOIs. Two ML1 citations
  (Caruso 2012, Critcher & Gilovich 2008) were absent from the reference list as
  DOIs; their DOIs came from a Crossref search on a title the script's author
  supplied, accepted only on agreement of first author, title and year within
  one (Crossref gives 2013 and 2007: in press, and online before print).
- Shared articles: Risen & Gilovich 2008 (RP:P and ML2); Tversky & Kahneman
  1981 (ML1 and ML2); two RP:P articles each contributed two replications.
  132 distinct articles with DOIs, before ML3. Rubric development codes the article.
- **Found while assembling:** RP:P's master data file stores four page ranges
  as spreadsheet dates ("1-15" as "15-Jan"; "22-4", RP:P's abbreviation of
  22-24, as "22-Apr"). This is PE-CLS-1.0 §7.6 I2's defect family in the most
  cited replication dataset. It does not touch outcomes; it is a reason the
  SCORE files get the same check (I2) when they arrive.
- The files carry no replication outcomes (consequence 5 above).

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

**Noisy-proxy scenario (run 2026-10-17, seed 20261018, 400 reps, 500 boot;
`k2_witness.py --noisy`, result `k2_witness_noisy_result.json`).** Replication
depends on the true value of baseline 1; M0 sees it with reliability r; the gate
tracks the true value and carries no design signal at all.

| Baseline reliability r | Mean ΔAUC | pass | fail | unresolved |
|---:|---:|---:|---:|---:|
| 0.9 | -0.002 | 0.000 | 0.998 | 0.003 |
| 0.7 | 0.002 | 0.010 | 0.970 | 0.020 |
| 0.5 | 0.010 | 0.073 | 0.793 | 0.135 |
| 0.3 | 0.024 | 0.223 | 0.448 | 0.330 |

**Reading.** At r ≥ 0.7 the analysis does not credit the proxy. At r = 0.5 it
passes 7% of the time and at r = 0.3, 22%. Such a pass is a real increment over
the baselines **as measured**, credited to the wrong construct. Reported N and
p are measured almost exactly, but as measures of a study's true power they may
be far less reliable than that, because published effect sizes are inflated
(7.0.1: Stanley et al. 2018). Consequences: (1) the claim is scoped to "beyond
the baselines as measured"; (2) B4 and B5 (Section 5) are the best available guard,
because a text model and forecasters can absorb what the noisy features miss;
(3) the per-check secondary results matter, because a proxy for power should
load on A4 and not on A1 or A3. Not a witness failure; a limit, stated before
the run.

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
- **A pass can credit a proxy.** If the baselines measure a cause of
  replication with low reliability and the gates track that cause, the
  increment is real and its attribution is wrong (7.5, noisy proxy: 22% pass at
  reliability 0.3). B4, B5 and the per-check pattern reduce this; nothing here
  removes it.
- **The development set is the most-studied set in the field.** Yang et al.
  trained on it, Van Bavel et al. recoded it, and its outcomes are famous. It is
  used for reliability and calibration only, never for outcomes, and that rule
  is what keeps its fame from mattering.

## 12. What a pass would and would not mean

A pass would mean that design defects of the kind the gates name explain part
of a failure that current practice measures and does not explain: the shape a
Kuhnian crisis requires, on the predecessor's own instrument. It would not mean
that the gates improve research going forward (that is K-3's prospective
multi-team study), that Philosophy Engineering is a paradigm (community and
incommensurability are untouched), or that the result holds outside the domains
sampled.
