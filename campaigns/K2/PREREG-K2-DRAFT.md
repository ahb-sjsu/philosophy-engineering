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
| Primary | **SCORE** replication set: Tyner et al., *Nature* 652:143–150 (2026), doi:10.1038/s41586-025-10078-y. Data: living repository doi:10.17605/OSF.IO/G5SNY; **archived as-published version doi:10.17605/OSF.IO/BZFGY** (the version this registration will name) | 274 claims of positive results from 164 papers (2009–2018, 54 journals). Replicated: 151/274 claims (55.1%), 80.8/164 papers weighted (49.3%), significance-in-original-pattern criterion | Human forecasts (repliCATS, Replication Markets) and machine scores are reported in separate SCORE preprints, not in the Nature paper. **Coverage confirmed 2026-10-19 (7.0):** the forecasts are per paper, on the phase-1 claim. 249 of the 274 claims are on forecasted papers, but only the 134 phase-1 claims are the claim that was forecast |
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
| A1 Nonvacuity | No outcome reported or reportable would have been taken against the hypothesis: flexible or unstated primary outcome, a hypothesis stated only post hoc, components fit after the data that can absorb any result. **As gated (owner decision 2026-10-21, `RUBRIC-v2-PLAN.md` D4(b)): only a prediction stated after the results (rubric A1.1).** The other A1 items are scored and reported as secondary items, not counted in the gate, because no coder pair has read them alike (7.4.1) |
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

**Coding unit (adopted by the owner 2026-10-18): the Method and Results
sections of every study in the article, and the lead before each Method
heading; nothing else.** The lead is up to 2,000 characters of whole lines
before a Method heading, where a study's predictions are usually stated (added
by the owner the same day, for A1; below). It stops at any heading, at a kept
stretch and at the end of page 1, so it does not run into the front matter or
a previous study's discussion; an "Experiment N" heading that bounds it is
kept. Front matter, abstract, the rest of the introductions, discussions and
reference lists are dropped, not redacted (`k2_sections.py`); title, authors,
journal, year and DOI are then redacted from what remains. An article without a Method-type and a
Results-type heading goes to a person. Blinding is imperfect for famous
studies, and the contamination probe below measures how imperfect.

**Implemented 2026-10-17: `k2_blinding.py`** (stdlib only), with intake
`k2_intake.py` (PDF text by poppler's pdftotext, reference list cut at the
last references heading, redaction, check). `redact()` removes the fields;
`leaks()` is gate I3 and runs on the text each auditor will see, not trusting
the redaction. An article with any residual leak, no references heading, or
letter-spaced scanned type is quarantined for a person and never released.
The rule list and its stated limits are in the module's docstring.

**Version 1 passed its own test and failed on real articles.** Its witness
used the 132 development-set articles' real metadata with a synthetic
paragraph and passed. Then the open-access copies were fetched
(`k2_fulltext_fetch.py`: of the 30 that OpenAlex lists as open, a script
could download **7** as PDFs; 15 links were web pages and 8 failed), run
through intake, and the blinded text read. Version 1 had missed: a journal
name stored with an HTML entity ("Memory &amp; Cognition"), surnames in
capitals and all given names, affiliations, volume and page ranges,
repository cover pages carrying a full citation, running heads with and
without a label, a cover-page title differing by one word and a typo, a
working-paper year one off the issue year, citations without a comma
("Bless 1990"), letter-spaced scanned type, and a stylized header with broken
spacing ("PS YC HOLOGICA L SC IENCE"). Version 2 adds a rule for each, and a
planted case for each in `k2_blinding_test.py`, which passes on all 132
records (`k2_blinding_test_result.json`). In-text citations with years count
as leaks because the newest cited year bounds the publication year.

**Over-redaction is a cost to coders and is measured.** The first version 2
run applied partial and fuzzy title matching to the whole text and blanked
one article's construct about 46 times, because its title names the
construct a coder must see to score the manipulation-check item. Partial and
fuzzy title matching now applies only to the first 4,000 characters; the
full title is removed anywhere. The share of words redacted is in the intake
manifest (`devset/intake_manifest.csv`, hashes and counts only): 0.6% to 2.1%
on the six released articles. The year rule removes any number within two
years of publication, by design.

**Result on the 7 real articles:** 6 released with no residual leak; 1 (a
scanned 1990 working paper, single-letter share 0.11 against 0.05 to 0.074 for
the born-digital six) quarantined. **Not caught, stated limits:** place names
("Princeton, New Jersey"), institutes named only by acronym or city, grant
numbers, and what the study itself makes recognizable. A person reads every
article of the pilot (7.4) for misses before release, and each miss becomes a
rule and a planted case before sealing. Seven articles are too few to bound
the miss rate.

**Versions matter as well as access.** Of the 30 open copies, 24 are listed as
the submitted manuscript, not the published article. A manuscript can differ
from what reviewers and readers saw (added analyses, a changed manipulation
check), so the version coded is recorded per article and the published
version is preferred where one is available.

**Second intake (2026-10-18): passing the check is not being blind.** The
other 23 open copies were fetched with the owner's permission: 3 by script
from Atlas (eScholarship, Geneva) and 14 through the owner's browser (PubMed
Central, Erasmus, Indiana, Amsterdam, Plymouth, Cambridge, SSRN); sources,
sizes and hashes are in `devset/fetch_log_manual.csv`. Six could not be had:
four sites answer with a bot check that is not bypassed (Durham, PhilPapers,
Wiley, VU Amsterdam), one server did not respond (UNC Greensboro), and one
figshare record has no file. Of the 24 PDFs now held, the leak check released
23 and quarantined the 1990 scan, after one rule fix: a running head longer
than 8 words ("D.M. Name et al. / Journal ... 45 (2009) ...") counts as
repeated only once its fields are redacted, and its initials were left
behind; repeated lines are now removed again after redaction (planted case
added; the test fails on the old code with 77 residuals and passes on the new).
Then a person read the opening of 6 released texts, and **all 6 still
identified the article or narrowed it sharply**: author initials and surname
particles ("R. [REDACTED]", "Van [REDACTED]"); institution names before a
redacted "University" ("Indiana [REDACTED], South Bend"), addresses, phone
numbers, postcodes and building names; volume and issue numbers ("34(1)");
APA's ISSN-and-year line ("0278-7393/08/$12.00", which names the journal and
year); report-series and repository labels and numbers ("ERIM Report Series",
"PEARL", "Archive ouverte UNIGE", "ScienceDirect"); a manuscript whose title
differs from the published one, so no title rule fires; and a title with a
curly apostrophe. Almost all of it sits in the front matter (cover page,
title block, first-page header and footer). So redacting a whole PDF is the
wrong unit, and the owner adopted Method and Results as the unit (above).

**The unit, measured on the same 24 PDFs.** `k2_sections.extract` found
Method and Results headings in 23; the 24th (a 1993 article with no such
headings) goes to a person, as does the 1990 scan, so 22 pass intake. The
unit keeps 16% to 64% of each body. *Residue:* `k2_unit_residue.py` counts
the kinds the person's read found. Redacting the whole body leaves residue
in 19 of 23 articles; redacting the unit, in 2, and both are false alarms
(a redacted citation after a test's and a book's name). Building the unit
exposed three more misses, now fixed with planted cases: PubMed Central
footers on every page ("J Pers Soc Psychol. Author manuscript; available in
PMC ..." names the journal and year), surname particles and initials beside a
redacted name ("Van [REDACTED]", "W. [REDACTED]", mostly self-citations), and
curly apostrophes, which hid "Thaler’s (1985)" from the citation rule and a
title from the title rule. The leak check shares redaction's normalization,
so a blind spot in one is a blind spot in both; the curly-quote case is
therefore checked by name in the test, and the committed code before this
fix fails it on all 132 records. *Not caught, stated limit:* where the
sample was drawn ("students at [REDACTED] Rotterdam, the Netherlands"), which
Method sections report by convention and which narrows the authors'
institution. A person still reads every pilot text.

**What the unit costs the rubric (measured, a proxy).** `k2_unit_coverage.py`
counts sentences carrying each check's evidence words (hypothesis and
prediction for A1; reliability and validity for A2; manipulation check and
demand for A3; exclusion and attrition for A4) and the share inside the unit,
over 23 articles: A1 25% (71 of 290; in 10 of 23 articles none of them),
A2 44% (4 of 14 lose all), A3 76% (none loses all), A4 66% (1 of 20 loses
all). `k2_unit_where.py` places A1's lost sentences: 72 in the 2,000
characters before a Method heading (where a study's predictions are usually
stated), 69 elsewhere in introductions, 77 in discussions. A3 and A4 are
scoreable from the unit. **A1 is not, as written**: "a hypothesis stated only
post hoc" needs where the hypothesis was first stated, and that is mostly
outside the unit. A2 is weakened. Word counts say where evidence words sit,
not what a coder would score; the pilot (7.4) codes a subset both from the
unit and from the full text to measure the difference. Offered keeping the
unit (A1 scored U more often) or adding the stretch before each Method
heading, the owner chose the second (2026-10-18).

**The lead, measured.** The unbounded 2,000-character window had suggested
about 50% for A1. Bounded as above, the unit keeps A1 40% (117 of 290;
articles with none of it, 3 of 23 instead of 10), A2 47% (3 of 14 lose all),
A3 76%, A4 66%, and 23% to 70% of each body. The bounds cost the difference:
an unbounded lead reached page 1 and brought in two leaks, an Elsevier
first-page ISSN line (it names the journal) and an author's correspondence
address. With page 1 excluded, the address still came in from DEV-RPP-070,
whose page 1 is a cover sheet: its correspondence footnote and author block
sit on page 2 ("77 Massachusetts Ave. ..., Cambridge, MA", "[REDACTED], San
Diego"). Two rules close that, each with a planted case (the committed code
fails the correspondence case on all 132 records; the author-block case was
not run against it separately): a correspondence footnote ("Address
correspondence to", "Corresponding author", ...) is removed to its
paragraph's end, at most 6 lines; and a line of redaction marks only is
dropped with up to two following lines that begin with a mark and go on in
capitalized words only (an author block's affiliation and city). A
capitalized part hyphen-joined to a mark ("[REDACTED]-BO", from "Chen-Bo") is
now part of it. On the 22 real units the author-block rule dropped only
mark-only lines and DEV-RPP-070's affiliation lines. Residue in the unit is
back to the same 2 false alarms; whole-body residue falls from 19 articles to
17. A1 remains the weakest check, so its U rate is reported per check
(Section 4). Until the pilot, intake status "blinded" means only "passed the
automated check", and nothing is released to a coder.

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
- **What "recall-free" requires of the reference (added 2026-10-17).** The
  reference is fit on development-set outcomes, so it must have no component
  that could carry those or SCORE's outcomes from elsewhere: no pretrained
  language model and no pretrained embedding whose training corpus is undated
  or postdates 2015 (the RP:P's publication). Features are learned from the
  development texts themselves, or come from a corpus with a stated date before
  that. Yang et al. 2020 used word2vec, and its corpus is not checked here.
- **Known limit of this reference: competence, not recall (added 2026-10-17).**
  A text model fit on the development set (132 articles) is a weak reader. A strong
  auditor stream can beat it by reading better, with no recall at all, and the
  probe as written would then void a clean stream. The direction is safe (it
  voids, it never admits a contaminated stream), and the cost is that the
  retrospective arm may grade nothing (Section 11). The comparison that
  separates recall from competence is the stream against **itself**: its
  no-rubric guess on claims whose outcomes it cannot have seen (made public
  after its training cutoff, or the prospective arm) against claims whose
  outcomes it could have. **Recommended, not adopted:** where at least one
  such set exists with enough claims, that self-contrast is the I2 gate and the
  text-model comparison is reported beside it; where none exists, the
  text-model comparison stands as written. Either way the margin is stated in
  standard errors of the AUC difference at the realized N (about 0.03 for one
  AUC near 0.7 on 270 claims), not as a bare number.
- **Recognition exclusion.** Articles an auditor reports recognizing are coded by
  a different auditor, or excluded, and the count is reported.
- **Prospective arm.** Studies whose replication outcomes are not yet public at
  the seal are audited, and their codes are committed and hashed, before the
  outcomes appear. This arm cannot be contaminated by recall. It is the stronger
  test and probably the smaller one. Its sampling frame is fixed in Section 3
  before sealing.

### 4.3 Auditors are instruments (draft 2026-10-17)

Adopted from the owner's book *All Tests Pass* (draft 0.3: ch. 10 "The
Evaluator Is an Instrument"; patterns V04 Independent Witness, V09 Placebo Run,
V10 Calibrated Judge, S05 Selection Is Fitting). Each is a requirement on this
design, not a citation:

1. **Planted-defect calibration (instrument gate, joins I1).** Before any test
   coding, every auditor stream codes development-set articles with known
   plants: a manipulation-check paragraph removed (A3), a primary outcome made
   post hoc (A1), a condition-dependent exclusion inserted (A4). Recall per
   check is measured, and a stream below a bar fixed from the pilot is not
   used. Plants never touch test articles.
2. **Placebo gate (secondary, must not pass).** Gate scores permuted within
   discipline × design-type strata (B2, B3), run through the registered
   analysis 400 times; its pass rate is reported beside the real result. A
   placebo that passes more than 5% means the strata leak. Implemented as
   `k2_analysis.placebo` (article-level permutation; CLI `--strata`).
   **Witness** (`k2_placebo_witness.py`, 60 synthetic datasets × 100 placebo
   permutations per scenario, on Atlas). Run 1 (seed 20261019) FAILED on its
   own design: its leak was too weak for the real analysis to credit (1.7%
   real passes), so there was nothing for the placebo to flag
   (`k2_placebo_witness_run1.json`, kept). Run 2 (seed 20261020, stronger
   leak, stated in the script beside run 1's values) PASSED: real signal,
   real 100% / placebo flags 0%; unadjusted stratum leak, real 98% / placebo
   flags 100%; same leak with the stratum in M0, real 0% / placebo 0%.
   **Limit:** the placebo sees only the strata it is given. With B2 and B3 in
   M0 additively, it guards against what the additive model misses (a stratum
   effect on the gate's slope, a stratum not coded), not against strata never
   named.
3. **U is not missing at random.** Badly reported articles are plausibly both
   high-U and less replicable. Registered sensitivity analyses: U scored as
   fail, U scored as pass, and the excluded fraction by outcome. Implemented
   in `k2_analysis.py` (output `u_sensitivity`; smoke-tested on Atlas).
4. **Two model families, each one opinion.** Model auditors come from at least
   two model families; agreement between two runs of one family counts once.
   Each stream is recorded as a description (family, revision, context, what
   it saw), not as "independent".
5. **Pinned revisions.** Every model auditor is named with an exact revision. A
   hosted model that can change or be withdrawn after the seal is recorded as
   such, and a withdrawn auditor voids its stream (I1), not the run.
6. **Prompts are selected on reliability only.** Model-auditor prompts are
   chosen on development-set agreement and plant recall, never on
   development-set replication outcomes (7.1 consequence 5 extended to
   prompts).
7. **Order and decoration.** Rubric items are presented in randomized order,
   and the sensitivity of scores to confident prose is measured on the pilot
   (persuasive writing may track the outcome).

## 5. Estimator

Primary: the difference in out-of-sample AUC (ΔAUC) between logistic models

- M0: replication outcome ~ baseline predictors
- M1: M0 + gate score

**Baseline set (draft 2026-10-17, owner to confirm; B5's availability on SCORE
claims confirmed 2026-10-19, see 7.0).** Each enters because prior work shows it
predicts replication, or because a gate could proxy it:

| | Baseline | Why |
|---|---|---|
| B1 | original effect size, p-value, N (log) | Altmejd et al. 2019; the statistical-inference rival (Branch 2019; Stanley et al. 2018) lives here |
| B2 | experimental or not; main effect or interaction | Youyou et al. 2023 (experiments replicate less) and Altmejd et al. 2019 (interactions); A3 applies only to experiments, so without B2 an A3 increment can be the design type |
| B3 | discipline, and subfield within psychology (covariates, never an interaction test in their place) | Inbar 2016: Van Bavel et al.'s coded feature lost its association once subdiscipline was a covariate (OR = 0.85, P = 0.51); in RP:P, cognitive studies replicated 53% and social-personality 28%. Van Bavel et al.'s reply: with both entered, neither is significant (P = 0.453 and 0.132), and the RP:P's own subdiscipline coding is unreported and binary. **Coding source:** the discipline and subfield fields SCORE releases, else the journal's subject category, fixed before sealing and never recoded after outcomes are seen |
| B4 | recall-free text score (the 4.2 reference model) | Yang et al. 2020: text alone predicts |
| B5 | forecasts (markets, surveys), where present on the same claims. On SCORE: the Replication Markets final market price (`cs_m1` of `KeyW_CS_2020-10-19.csv`, OSF tcfb9), with its survey (`cs_m11`) and the repliCATS aggregate (`ArMean` of `anon_p1_singletrace_confidence_scores.csv`) as secondaries. The column names are fixed from tcfb9's own analysis scripts. The other ten `cs_m*` columns are undocumented in what was read and are not used | strongest known human baseline |

The primary M0 is B1 to B3 (owner decision below). **B5 "where available" splits
the SCORE set (7.0):** B5 exists for at most 134 of the 274 claims, the phase-1
claims. The 115 bushel claims sit on forecasted papers, but their forecast was
made for a different claim, so using it would compare the gate against a forecast
of something else. The 25 phase-2 claims have none. A single M0 over all 274
cannot include B5. **Owner decision, 2026-10-21: option (a).** The primary test
runs on all 274 claims with M0 = B1 to B3, which keeps the power of Section 7.5
(simulated at 274 claims and 164 papers). **The B5 test is a registered
secondary test** on the 134 phase-1 claims, with M0 = B1 to B3 plus B5
(`cs_m1`), the same estimator and the same verdict rules; it is reported beside
the primary verdict and does not replace it. Its power is that of 7.5.1: 80% only
at a true ΔAUC near 0.09 to 0.10, and lower if the forecasters already see the
design signal the gates measure. The option not taken, (b), made the phase-1
subset with B5 the primary test. **M0+B4 is a registered
secondary test:** the gates beyond a text model is a stronger claim than the
gates beyond known features, and both are reported. Which of the two is primary
is an owner decision, recorded before sealing.

estimated by cross-validation, with folds blocked by original article, so that
no article contributes to both fit and evaluation (an article replicated in two
projects carries one `paper_id` after deduplication, so blocking by article also
keeps it on one side). *Corrected 2026-10-17:* the earlier text also blocked by
replication project, which `k2_analysis.py` never did, and which cannot be done
with one primary project; the code was right and the text was not. Per-project
results are a secondary report. The 95% interval is a cluster bootstrap over original articles.
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
| I1 Rubric reliability | Single-coder ICC(2,1) of the gate score, computed on the run's own double codes (every article is coded twice), at or above 0.80 (draft bar, set from the Section 7.2 witness, not from the probe it gates) |
| I2 Contamination | Section 4.2 probe within its bar for every auditor stream used in the primary analysis |
| I3 Blinding leak | `k2_blinding.leaks()` finds nothing in the text each auditor sees: title, author, journal, year, DOI, in-text citations with years, URLs, e-mail (4.1) |
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

**Done 2026-10-19, after the window.** Only file listings, column names,
identifiers and counts were read. No replication outcome and no forecast value
was opened. Scripts and results are in the campaign folder: `k2_score_doi_match`,
`k2_forecast_coverage`, `k2_forecast_coverage_274` and `k2_forecast_scripts`.

- **Layout and license.** BZFGY is CC0. Its data package (`analysis data and code
  package 15 Dec 2025 1708.zip`, sha256 matches OSF) holds the analysis code (MIT)
  and one R data file of 17 tables. G5SNY, also CC0, holds the same package, a
  figures archive, and a component of per-attempt effect-size conversions. It
  has no forecasts.
- **Outcome table.** `repli_outcomes` has 427 replication reports on 331 claims.
  `repli_binary` holds the success measures for exactly **274 reports, on 274
  claims from 164 papers**, which is the Nature paper's analysis set. Every one
  of its report identifiers is present in `repli_outcomes`.
- **Restricted fraction.** For the analysis set it is **zero at the record
  level**: all 274 analysed claims are in the public data. Whether every field
  of each record is present has not been checked. The availability statement's
  "shared without restriction" may refer to raw replication data, not these
  records.
- **Development-set overlap.** Of the 132 development-set articles, 1 is in
  SCORE, DEV-ML-013 (SCORE paper 88xa, one new-data replication). SCORE's papers
  are from 2009–2018 plus 100 COVID papers from 2020. It is already outside
  the test pool, and its SCORE outcome is never opened (7.1).
- **Forecasts.** Both pointers are preprints.
  - Mody et al. (vgyed, version 2, 2026-10-15) is the human forecasts. Its data
    links are tcfb9 (CC BY 4.0), d9x6s (repliCATS phase-one data, CC BY 4.0) and
    w4xsk (not public). tcfb9's analysis scripts name the files.
    `KeyW_CS_2020-10-19.csv` is Replication Markets (`cs_m1` market price,
    `cs_m11` survey), and `anon_p1_singletrace_confidence_scores.csv` is repliCATS
    (main aggregate `ArMean`, 38 methods). Both are keyed by **paper** and cover
    the same 3,000 phase-1 papers.
  - Rajtmajer et al. (bdmte) is the machine assessment. It links only to the
    programme page dtzx4, and no per-claim machine scores were found.
- **Coverage on the analysis set.**

  | | Claims | Of these, on a forecasted paper |
  |---|---|---|
  | Phase 1 | 134 | 134 (this claim is the one forecast) |
  | Bushel | 115 | 115 (a different claim was forecast) |
  | Phase 2 | 25 | 0 |
  | **Total** | **274** (164 papers) | **249** (139 papers) |

  The forecast files carry no claim identifier, so whether each phase-1 claim in
  `repli_outcomes` is exactly the claim forecast is inferred from the design
  (one claim per paper in phase 1), not checked row by row. The B5 consequence is
  in Section 5.
- **The baseline's own validation is small.** The Mody et al. abstract
  reports forecast accuracy validated against **n = 37** independent high-power
  replications: AUC 0.76 [0.72–0.82] for Replication Markets and 0.76
  [0.68–0.81] for repliCATS, with classification accuracy 73% and 68%. The 37
  are selected in tcfb9's scripts by `TA2_include_singletrace_*` flags in an
  outcomes file not opened here. A comparison against B5 on up to 134 claims
  would be about 3.6 times the size of the forecasts' own published validation.
- **Supplement source (7.1.1).** The forecasts cover 3,000 phase-1 papers, of
  which 139 are in the analysis set. That leaves 2,861 sampled, forecast and
  not replicated, the preferred supplement frame. Their claim statements are in
  d9x6s (`phase_one_singletrace_claims_anonymised.csv`, not opened). Restricting
  them to non-psychology disciplines and the SCORE journals is still to do.

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
  and replicability in psychology may be spurious" (**read in full 2026-10-17**,
  PMC5003252 fetched from Atlas, sha256 c64dd396…). The association (r = −0.23,
  P = 0.024) "is entirely the result of an omitted third variable", subdiscipline:
  cognitive studies replicated more (53% vs. 28%) and were rated less
  context-dependent (d = −1.85); within each subdiscipline r = −0.08 (P = 0.54)
  and r = −0.04 (P = 0.79); entered as a covariate in a logistic regression,
  "the previously significant effect of context dependence disappears, OR =
  0.85, Z = –0.66, P = 0.51". Van Bavel et al. had tested the interaction, which
  "asks 'does the effect differ by subdiscipline?' not 'is there an effect
  controlling for subdiscipline?'". Inbar also notes that the subdisciplines
  differ in "greater use of within-subject designs in cognitive psychology",
  so subdiscipline itself bundles design differences. A reply exists (Van Bavel
  et al. 2016, *PNAS*, doi:10.1073/pnas.1609700113, "Reply to Inbar:
  Contextual sensitivity helps explain the reproducibility gap between social
  and cognitive psychology"; PMC5003241, not open access). **The reply, read in
  full 2026-10-17** (first through a fetch tool's summary and quotes, then the
  PMC page itself in the owner's browser; every quote below checked against
  it). It reports a hierarchical regression (its Table 1, Step 2) with original
  effect size, original n, replication power, replication similarity, the two
  surprisingness ratings, subdiscipline and contextual sensitivity entered
  together; the subdiscipline coefficient falls from b = −1.45 (SE 0.72) in
  Step 1 to −0.66 (SE 0.88), Nagelkerke R² 0.60 to 0.62. In that
  model "subdiscipline no longer predicts reproducibility once context is added
  to the model (P = 0.453", and contextual sensitivity is not significant
  either (P = 0.132). Without context, subdiscipline "predicts reproducibility
  (P = 0.044) even after adjusting for methodological factors". The authors
  read this as "multicollinearity" that "makes it inappropriate to categorize
  one as a confound", and argue the causal order runs from subdiscipline
  through context ("Contextual sensitivity cannot cause a change in
  subdiscipline"). They also note that the RP:P did not report how it coded
  subdiscipline and that a binary social/cognitive split misfits fields such
  as social cognition. **What this adds for K-2:** with both variables in one
  model neither survives, so the RP:P data could not separate the coded
  feature from subfield in either direction. K-2's Section 6 rule is graded on
  the ΔAUC interval, so collinearity with B3 shows up as width: it can move a
  result from pass to `unresolved` but cannot produce a `fail`, which needs the
  upper end below the SESOI. The causal-order argument does not change the
  primary model, because K-2's claim is the predictive increment beyond the
  known predictors, not the causal effect of the gates. And B3 must be coded
  from a stated source with more than two levels where the data allow (Section
  5), not from an unreported binary split. **One further difference:** that
  model also conditions on properties of the replication (its power, P = 0.020
  in Step 2, and how surprising its result was), which are not known before
  replication. K-2's baselines are all properties of the original (B1 to B5),
  because the claim is prediction from the original article. A gate that
  tracks replication power (for example, small originals given larger
  replications) would be credited for it, so replication N or power, where
  SCORE releases it, enters a registered sensitivity analysis that grades
  nothing. **Van Bavel et al.'s coding design**, read in
  full (PMC4988618): three coders, ratings from the abstract (methods when no
  abstract, 5 of 100), raters "unaware of the results of replication attempts";
  25 studies coded by all three (reliability α = 0.86, ICC(2,3), the
  reliability of the three-rater **mean**), the other 75 coded by one coder each.
  **Consequences for this design:** (i) B3 enters M0 as a covariate; no
  interaction test substitutes for it; (ii) the reliability bar (I1) is stated
  for a **single** coder's score, and the primary score is the consensus of two
  coders on every article, never a single coder on most; (iii) because
  subdiscipline bundles design, an increment that vanishes with B3 in the model
  is still graded by Section 6 exactly as registered, and a `fail` stands: the
  claim is "beyond the known predictors", and subfield is one. What a fail
  would not show is that the gates are irrelevant to replication, only that
  this design cannot separate them from subfield, and the report says so in
  that sentence. The analysis without B3 is reported as a secondary and
  grades nothing.
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
  best-metric; the Mody et al. preprint, read 2026-10-19, gives AUC 0.76 for
  both teams on n = 37 replications, see 7.0). **The increment is measured against the strongest baseline
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
- **Found while assembling:** the GitHub copy of RP:P's data file (the OSF original not yet checked) stores four page ranges
  as spreadsheet dates (pages 1-15 as "15-jan"; pages 22-24, probably entered as RP:P's abbreviation "22-4",
  as "22-apr"; also "20-jan" and "18-sep"). This is PE-CLS-1.0 §7.6 I2's defect family in a central
  replication dataset. It does not touch outcomes; it is a reason the
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
their claim statements already exist in SCORE's own format (confirmed
2026-10-19: 2,861 such phase-1 papers, claims in OSF d9x6s; see 7.0). Otherwise, draw
articles from the journal list and pick the claim by SCORE's documented
claim-selection procedure, or failing documentation, the first finding stated
in the abstract with an inferential test.

*Size.* About 30 claims, with at least 8 each from economics and political
science and the rest spread across SCORE's other non-psychology disciplines,
in proportion to SCORE's own mix. Seeded draw; the seed is committed before the
draw. Two independent coders, as for the main development set.

*Also the v2 measurement pool (owner decision 2026-10-21, `RUBRIC-v2-PLAN.md`
D1(b)).* RUBRIC-v1's held-out half is spent (7.4.1), so v2 is measured on
supplement articles. The held-out part is drawn by seed, split off and set
aside unread before v2 is written. **Its size is 60 articles (owner,
2026-10-21, from the D2 sizing simulation), and v2 goes ahead only if the
between-family gate ICC(2,1) on them is at least 0.73.** The draw is larger
than 60 by the share whose full text cannot be obtained.

*Frame and access, measured 2026-10-21* (`k2_d9x6s_frame.py`,
`k2_frame_access.py`; OpenAlex records, not verified downloads). The d9x6s
claims file covers SCORE's 3,000 phase-one papers; removing the 148 SCORE
replicated and 1 development-set DOI leaves 2,852 papers in 62 journals,
2009 to 2018. Of these, 1,052 (37%) have an open copy on record, but the best
open copy is the published version for only 345 (12%); 569 are submitted
manuscripts and 124 accepted manuscripts. Without any psychology category,
and counting the 305 papers with no category, the frame is 1,924 papers, 713
(37%) open on record and 242 (13%) open as published. On the development set,
17 of 23 records marked open were obtained and 22 of 24 obtained texts passed
intake (4.1), small samples that make any oversampling factor a rough one.

*Eligibility (owner, 2026-10-21; `k2_frame_eligible.py`,
`devset/frame_eligible.csv`).* (1) Only papers whose best open copy on record
is the published or the accepted version, because SCORE's claim records locate
the claim in the published article and a submitted manuscript can differ in
what the rubric scores. (2) Any category naming psychology, alone or mixed, is
excluded. (3) A paper with no Web of Science category takes its journal's most
common category among the frame's categorized papers (187 classed, no ties).
Three journals have no categorized paper in the frame, so their 118 papers
stay unclassed and are excluded for now: *Computers & Education* (48 papers,
5 eligible on access), *Social Science & Medicine* (47, 4) and *Journal of
Experimental Political Science* (23, 1). **Result: 325 eligible papers in 34
journals** (228 published, 97 accepted versions): business and economics 192
(including the mixed economics categories), government, law, international
relations and public administration 67, demography 36, sociology 25,
criminology 4, education 1.

*Draw (owner, 2026-10-21; `k2_v2_draw.py`).* 90 papers, strata proportional to
the eligible pool (largest-remainder allocation), **seed 20261021**, frame
pinned by hash; the seed, rule and hash were committed before the draw was
run. The 90 are put in one seeded order, and the held-out set is the first 60
in that order whose text is obtained and passes intake; usable papers after
the 60th are revise material. Held-out texts are handled by script only until
v2 is committed. **Drawn 2026-10-21 22:24:36 UTC on Atlas** (`devset/v2_draw.csv`),
after the seed commit (535dd86, 22:23:48 UTC) and a correction of the frame
hash constant (d08e8f0, 22:24:23 UTC; the first run had stopped at the hash
check without drawing): economics 53, politics 19, demography 10, sociology 7,
criminology 1, education 0; 63 published and 27 accepted versions.

*Fetch and intake, run 2026-10-21 on Atlas* (`k2_v2_fetch.py`,
`k2_v2_fetch_meta.py`, `k2_intake.py`; logs in `devset/`). Only published or
accepted open locations were tried. **10 of 90 PDFs obtained** (8 published, 2
accepted; draw orders 18, 27, 29, 42, 44, 45, 51, 65, 82, 88). For 70 papers
the first open location answered a script with HTTP 403 (publisher bot
protection, not worked around); 11 answered with a web page, one of which led
to the PDF through its `citation_pdf_url` tag. **All 10 were quarantined at
intake: none has a Method-type heading**, so the 4.1 coding unit (Method and
Results, built on psychology articles) finds nothing to keep; one also has
residual leaks. The texts were handled by script only and were not read. Still development data: no
replication outcome exists for these claims.

*SSRN copies excluded (owner, 2026-10-24).* For 36 of the 80 papers still
missing, the only open location resolves to SSRN. OpenAlex labels these copies
published or accepted, but SSRN copies are usually working papers, so they do
not meet the published-or-accepted rule and are not fetched. The same rule
drops 3 of the 12 development papers (el4m, K8XW, A2lr). After the exclusion
at most 54 drawn papers can be obtained (the 10 in hand and 44 others), fewer
than the 60 the held-out set needs.

*Second fetch, through the owner's Chrome, 2026-10-24.* One request per host,
made from a script running in a publisher or repository page. The owner had
cleared the hosts' checks in their own tabs. Eight hosts were tried. Wiley
and Duke still showed the check. Wiley, Oxford and the Bristol and Manchester
repositories answered the scripted request with HTTP 403. Wiley, Cambridge and
the AEA sent the reader to the abstract page, which means the copy is not open
to this reader despite OpenAlex's open label. The Copenhagen repository links
only to a time-limited Oxford copy. MUSE, SAGE, ScienceDirect, INFORMS and the
Groningen repository were not tried. No PDF was obtained; nothing was worked
around.

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
**Measured 2026-10-17** (`k2_devset_access.py`, `devset/access.csv`): of the
132 development-set DOIs, OpenAlex records 30 (23%) as open access (27 green,
2 bronze, 1 gold) and 102 as closed. These are database records, not verified
downloads. Coding even the development set therefore needs a library route for
about three articles in four; the SCORE test set's rate is unmeasured until its
claim list is available.

### 7.2 Reliability probe

Probe on real coders: not run. **Where the bar sits (simulation, run
2026-10-17/18 on Atlas):** `k2_reliability_witness.py` takes the Section 7.5
signal world, has two coders read each of the 4 checks and record it wrongly
with probability e (independent, symmetric), and runs the registered analysis
on the true score, on one coder's score, and on the mean of both (a
conservative stand-in for the reconciled consensus). 200 datasets per cell,
300 bootstrap draws, seed 20261020; result in
`k2_reliability_witness_result.json`. The ICC check reproduces Shrout and
Fleiss's (1979) worked example (ICC(2,1) = 0.29).

At the design slope 0.75 (the true score passes 76 to 86% of the time across cells):

| Flip e | Single-coder ICC | pass, one coder | fail, one coder | pass, two-coder mean | fail, two-coder mean |
|---:|---:|---:|---:|---:|---:|
| 0 | 1.00 | 0.86 | 0.02 | 0.86 | 0.02 |
| 0.03 | 0.90 | 0.76 | 0.08 | 0.79 | 0.06 |
| 0.05 | 0.84 | 0.78 | 0.07 | 0.79 | 0.06 |
| 0.08 | 0.74 | 0.65 | 0.14 | 0.75 | 0.10 |
| 0.10 | 0.68 | 0.52 | 0.25 | 0.61 | 0.13 |
| 0.15 | 0.54 | 0.43 | 0.35 | 0.63 | 0.15 |
| 0.20 | 0.41 | 0.26 | 0.47 | 0.51 | 0.28 |
| 0.30 | 0.19 | 0.06 | 0.84 | 0.17 | 0.62 |

The true-score fail rate in the same cells is 0.02 to 0.06. Monte Carlo
standard error on each rate is about 0.03.

**What it shows.** Coder error does not only cost power. It turns a real
effect into a graded `fail`, because noise pulls ΔAUC toward zero and the
interval then lies below the SESOI: at single-coder ICC 0.54 one coder fails a
true effect 35% of the time, against 4% for the true score. That is the
failure Section 6 must not mistake for physics, so I1 is an instrument gate
(a miss voids the run) and its bar is set where the two-coder mean's fail rate
stays near the true score's: **0.80**, between the 0.74 cell (fail 0.10) and
the 0.84 cell (fail 0.06). At slope 1.0 the same bar holds pass at or above
0.95. Double coding every article is worth the cost: at ICC 0.54 the mean
cuts one coder's false-fail rate by more than half (0.15 against 0.35).

**Against the precedent.** Van Bavel et al.'s reported α = 0.86 is ICC(2,3),
the reliability of a three-coder mean. Inverting Spearman-Brown,
0.86 / (3 − 2 × 0.86) ≈ 0.67 for one coder (derived here, not reported by
them). Coders of that reliability would miss this I1 bar.

**Limits.** The error model is an assumption. Coders who share a misreading
(the same ambiguous rubric item read the same wrong way) raise the ICC without
making the score more valid, so a high I1 does not certify the score; the
planted-defect calibration of Section 4.3 is the check on validity. The bar is
on the point estimate from the full run's double codes (about 270 claims,
simulation SD of the estimate 0.02 to 0.06); the ~40-claim development probe
estimates it far less precisely and is used to decide whether to proceed, not
to pass I1.

### 7.3 Contamination probe

Not run. The pilot's recognition self-report (7.4) is not this probe.

### 7.4 Pilot

Purpose: realized N, U rate, recognition rate, and the variance needed to size
the I5 power bar and the physics bar.

**Model-coder pilot (run 2026-10-19 on Atlas, against the NRP ELLM gateway).**
`k2_pilot_code.py` gave RUBRIC-v0 sections 0 and A1 to A4 (check order shuffled
per call, 4.3 rule 7) and one blinded coding unit (4.1) to each model coder;
the 22 development-set units that passed intake were each coded twice per
model, and a seeded subset of 6 was coded once more from the redacted whole
body. Temperature 0.2, JSON output, "reason briefly" in the system prompt, up
to 4 tries per coding. Scores only in `k2_pilot_summary_result.json`
(`k2_pilot_summary.py`); raw responses hold article quotes and stay on Atlas.
No replication outcome was read (7.1 consequence 5).

Owner's decisions and deviations, recorded before any score was read:

- Coders: two model families, each coding every unit twice. glm-5 and then
  deepseek-v4-flash were dropped because they reasoned to the token limit
  without answering (deepseek's 2 failed codings remain in the record);
  qwen3 was smoke-tested and not used. The streams are gpt-oss (returned
  `openai/gpt-oss-120b`, limit 48,000 tokens, 02:26 to 03:08 UTC) and
  minimax-m2 (returned `MiniMaxAI/MiniMax-M2.7`, limit 8,000 tokens, 10:48 to
  12:10 UTC). Hosted aliases: neither revision can be pinned (4.3 rule 5).
- The target claim was given as the study only (RP:P study number, Many Labs
  effect name), not as claim wording: a deviation from RUBRIC-v0 section 0.
- Model coders saw the texts before the person's leak read (4.1); that read
  still precedes any human coder. No human coder has coded.

| | gpt-oss | minimax-m2 |
|---|---:|---:|
| Codings scored | 50 of 50 | 45 of 50 |
| Extra tries | 0 | 32 |
| Median seconds, median completion tokens (last try) | 51, 2,093 | 30, 2,377 |
| Unit codings fail A1 / A2 / A3 / A4 | 75 / 89 / 84 / 98% | 41 / 64 / 77 / 74% |
| Gate mean (0 to 4), variance | 3.46, 0.52 | 2.56, 1.78 |
| Gate distribution 0/1/2/3/4 | 0/1/3/15/25 | 4/6/5/12/12 |
| Says it recognizes the study / guess names the article | 3 / 1 of 50 | 0 / 0 of 45 |
| Says it knows the replication outcome | 0 | 0 |
| Quoted evidence found verbatim in the unit | 78 of 191 | 8 of 13 |

| Agreement on the gate | Articles | ICC(2,1) | Exact | Check agreement A1 / A2 / A3 / A4 |
|---|---:|---:|---:|---|
| gpt-oss, coding 1 vs 2 | 22 | 0.66 | 77% | 86 / 95 / 100 / 95% |
| minimax-m2, coding 1 vs 2 | 17 | 0.63 | 29% | 71 / 82 / 88 / 71% |
| **gpt-oss vs minimax-m2, coding 1** | 19 | **0.11** | 32% | 42 / 74 / 81 / 74% |
| Unit vs whole body, gpt-oss | 6 | 0.64 | 4 of 6 | 67 / 100 / 100 / 100% |
| Unit vs whole body, minimax-m2 | 6 | 0.59 | 2 of 6 | 67 / 83 / 67 / 67% |

**What it shows.**

1. **RUBRIC-v0 does not give one score across coders.** Two runs of one
   family count once (4.3 rule 4), so the agreement that bears on I1 is
   between families, and it is ICC 0.11 against the 0.80 bar (7.2). Each
   family also misses the bar against itself. The lowest cell of the 7.2
   simulation, single-coder ICC 0.19, fails a true effect 84% of the time
   with one coder and 62% with the two-coder mean; 0.11 is below that cell.
   The rubric must be revised and re-piloted before sealing; A1 (42%
   check agreement between families) and A4 disagree most.
2. **gpt-oss's ceiling is partly the coder.** gpt-oss put 25 of 44 unit
   codings at gate 4 (variance 0.52); minimax-m2 used the whole range
   (variance 1.78). Two coders cannot say which reading of the rubric is
   right; the planted-defect calibration (4.3 rule 1) is the check on that,
   and it has not run.
3. **U rate:** no coding of either stream had more than two U checks, and U
   appeared only on items A3.2 (gpt-oss 9%, minimax-m2 13% of codings) and
   A4.2 (5%, 18%). Neither model used U as a way out of a hard item.
4. **Recognition:** low on these units (1 correct identification in 95
   scored codings, none claiming an outcome). This is self-report, not the
   contamination probe (7.3), which has not run.
5. **Realized N:** 22 of the 132 development articles reached coding (intake,
   4.1); this pilot says nothing yet about N on the test set.
6. **Variance for the bars:** not usable yet. The two streams' gate
   variances differ more than threefold, so a power bar sized from either
   would describe the coder, not the articles.

**Limits.** minimax-m2's 5 failed codings each ran to the token limit on all
4 tries; its kept codings come only from tries that finished, which may favour
shorter reasoning. 37 of its 82 tries ran to the limit. gpt-oss's quoted
evidence is found verbatim only 41% of the time; 7.4.1 item 5 traces most of
the rest to layout (line breaks, page numbers, ellipses) and some to reworded
sentences inside quotation marks. Six whole-body codings are too few for
the unit-vs-body comparison to bound anything.

**Human coders (owner, 2026-10-19):** none are available at this time. The
coders are the two model families until that changes. The steps that need a
person stay open: the person's leak read (4.1), the third coder of the
Adjudication rule, and any human stream for I1.

#### 7.4.1 Rubric v1 and its pilot

The owner left the next step to the drafting session (2026-10-19), which took
it as follows, in this order.

1. **Split before reading reasons** (commit 3ae8320). The 22 units were split,
   seeded and stratified by source, into a revise half (11) and a held-out half
   (11), `k2_rubric_split.json`, before any item code or coder reasoning was
   read. Aggregate check and item rates over all 22 and per-article gate scores
   had been seen. On the v0 codings the between-family gate ICC is 0.41 on the
   revise half (8 articles with both rep-1 codings) and **−0.07 on the held-out
   half (11)**.
2. **Diagnosis on the revise half only.** Item scores and evidence of both
   families on the 11 revise units. Most cross-family splits were over what an
   item covers, not over what the text says: one family scored any test,
   outcome or measure anywhere in the article, the other scored the claim's own
   test. The table at the end of `RUBRIC-v1.md` lists each change and the
   finding it answers.
3. **RUBRIC-v1** ([`RUBRIC-v1.md`](RUBRIC-v1.md)), committed with this
   paragraph in 60e556b (15:08:16 UTC). That commit's message says it came
   before any v1 coding returned; it did not, by 12 seconds: the first coding
   (gpt-oss, DEV-ML-001 rep 1) was written at 15:08:04, unread. The file is
   unchanged since the run started (15:07:18), and every coding record carries
   its hash. Scores the focal test, needs a
   failure that can be pointed to, defines scope and a threshold where v0 had
   none (A2.1, A2.2, A2.3, A3.2, A3.3, A4.1 to A4.5), and leaves A1.1, A1.3,
   A1.4, A2.4, A3.1 and A3.4 as in v0. A3.1's treatment of directly perceived
   stimulus manipulations is a validity question left open there.
4. **Claims restored.** v1 coders get the claim as RUBRIC section 0 specifies,
   ending the v0 pilot's study-number deviation: for RP:P, the original-side
   `Description.of.effect.O` and `Test.statistic.O` (no `.R` column is read,
   7.1 consequence 5); for Many Labs, the effect label and, for Many Labs 1,
   the comparison as its codebook states it (`k2_dev_claims.py`,
   `devset/claims_dev.csv`).
5. **v1 pilot.** The same two coders and settings as v0 (gpt-oss at 48,000
   tokens, minimax-m2 at 8,000, temperature 0.2, same check orders), all 22
   units twice plus the 6 whole bodies, output `/archive/experiments/k2/pilot_v1`.
   The number that counts for v1 is the between-family gate ICC on the
   **held-out half**; the revise half is reported beside it and is expected to
   be higher.

**Result (run 2026-10-19, 15:07 to 17:04 UTC; gpt-oss done 15:31).** `k2_pilot_v1_summary_result.json`;
the v0 rows by half are in `k2_pilot_summary_result.json` (regenerated with the
split file; its other rows are unchanged). gpt-oss scored 50 of 50 codings;
minimax-m2 42 of 50 (42 extra tries; both codings of DEV-RPP-006 and of
DEV-RPP-035 failed).

| Gate agreement, ICC(2,1) (articles) | v0 revise | v0 held-out | v1 revise | **v1 held-out** |
|---|---:|---:|---:|---:|
| gpt-oss vs minimax-m2, coding 1 | 0.41 (8) | −0.07 (11) | 0.61 (10) | **−0.31 (9)** |
| gpt-oss, coding 1 vs 2 | 0.79 (11) | 0.50 (11) | 0.84 (11) | 0.22 (11) |
| minimax-m2, coding 1 vs 2 | 0.59 (7) | 0.68 (10) | 0.75 (9) | −0.52 (8) |

| Check agreement between families, held-out | A1 | A2 | A3 | A4 |
|---|---:|---:|---:|---:|
| v0 | 36% | 73% | 78% | 73% |
| v1 | 44% | 89% | 83% | 78% |

1. **v1 fails.** On the held-out half the two families do not agree on the
   gate (ICC −0.31 on 9 articles), and gpt-oss does not agree with itself
   (0.22). The gains on the revise half did not carry over, which is what a
   revision fitted to the articles it was written from would do; with 8 to 11
   articles per cell, chance is the other explanation, and these rows cannot
   separate the two. (Added 2026-10-21: the D2 sizing simulation in
   `RUBRIC-v2-PLAN.md` bears on the chance reading. Under the 7.2 coder model,
   an estimate of −0.31 on 9 articles is below the 2.5th percentile even at a
   true single-coder ICC of 0.60, so chance alone is an unlikely account of a
   rubric that good.) No reading of them reaches the 0.80 bar.
2. **What did change.** The ceiling is gone: gpt-oss's gate mean fell from
   3.46 to 1.84 and minimax-m2's from 2.56 to 1.62, and the families' failure
   rates moved closer on every check but A1 (gpt-oss / minimax-m2, v0 then
   v1: A1 75/41 then 39/16, A2 89/64 then 46/41, A3 84/77 then 71/81, A4
   98/74 then 30/24%). Check-level agreement between families rose on the
   held-out half for every check, and the gate ICC fell anyway; with 9
   articles this session cannot say why.
3. **A1 is the obstacle.** Held-out A1 agreement is 44% between families, and
   gpt-oss agrees with itself on held-out A1 only 36% of the time (91% in
   v0). Rewriting A1.2 as "outcomes that disagree" made it a harder judgment,
   not an easier one. This is the v0 rubric's own known gap (A1.3, A1.4 and
   now A1.2).
4. **The claim text leaked.** With claim wording, gpt-oss said it knew the
   replication outcome on 3 codings (none in v0): DEV-ML-001 rep 2, whose
   target text named "Many Labs 1" (written into `devset/claims_dev.csv` by
   this session, a defect: the target must not name the replication project),
   and both codings of DEV-RPP-093. By the Recognition rule those 3 codings
   should not count; all three units are in the revise half, so the held-out
   rows are unaffected, and the revise-half rows above include them.
5. **Quotes.** `k2_quote_check.py` traces each quoted evidence string to the
   text the coder saw. v0 gpt-oss: 170 of 191 found once ligatures, page-number
   lines, line-break hyphens and ellipses are allowed for, 5 partly, 16 not;
   the not-found ones compared by eye (DEV-ML-034, DEV-RPP-006) were reworded
   real sentences, not invented content, and the rest were not checked. v1
   gpt-oss, after "quote the text exactly": 203 of 238 found, 11 partly, 24
   not, so the rule did not help. minimax-m2 quoted in double quotes once in
   v1 (13 times in v0); its evidence is located absences and paraphrase.

**What this means for the design.** Model coders on this rubric do not reach
I1, before or after a revision, and the held-out half is now spent: any v2
measured on these 22 units would be measured on units that shaped it. A v2
needs fresh development articles (the 102 closed-access articles need the
license decision in 7.1), or a different coder arrangement (human coders, or
the mean of several codings per family, which raises within-family
reliability but not agreement between families). Decided by the owner, not
here.

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

### 7.5.1 Power at the option (b) shape (simulation, run 2026-10-20)

The owner chose option (a) on 2026-10-21 (Section 5), so this is the power of
the registered B5 secondary test, not of the primary. `k2_power_b.py` reruns the
7.5 world at the phase-1 shape: 134 claims on 133 papers (132 with one claim, one with two), 400 draws per
scenario, 500 bootstrap draws each, seed 20261020, SESOI 0.05, through the same
`k2_analysis.py`. It ran twice with identical per-scenario seeds, once on Atlas
and once as 22 NRP Jobs (`k2_power_b_nrp.py`); the two results agree exactly.
Result committed as `k2_power_b_result.json`.

The forecast column is an **assumption**, not evidence: f = (replication
log-odds without the gate's own signal) + w × (the gate's signal) + noise, with
the noise set so that f alone has AUC ~0.76 in the null world, the value the
forecasts reached on their n = 37 validation (7.0). w is how much of the design
signal the forecasters already see: 0 none, 1 all.

**A1 witness at this shape: PASS.** Null passes 0.003, proxy 0.005 (with B5 in M0).

Pass rate (mean ΔAUC in brackets) by gate slope:

| M0 | slope 0.5 | 0.75 | 1.0 | 1.25 | 1.5 |
|---|---:|---:|---:|---:|---:|
| B1–B3 (no forecast) | 0.11 (0.025) | 0.42 (0.056) | 0.77 (0.091) | 0.94 (0.130) | 1.00 (0.175) |
| B1–B3 + B5, w = 0 | 0.13 (0.025) | 0.43 (0.053) | 0.78 (0.090) | 0.95 (0.136) | 1.00 (0.173) |
| B1–B3 + B5, w = 0.5 | 0.07 (0.013) | 0.18 (0.029) | 0.27 (0.039) | 0.51 (0.054) | 0.54 (0.054) |
| B1–B3 + B5, w = 1 | 0.02 (0.005) | 0.04 (0.009) | 0.03 (0.011) | 0.06 (0.012) | 0.06 (0.011) |

**Reading.** (1) Halving the sample costs about half the sensitivity: at slope
0.75 (ΔAUC ~0.055) the pass rate falls from 0.84 at 274 claims (7.5) to 0.42 at
134; 80% power needs a true ΔAUC near 0.09 to 0.10. (2) If the forecasters
already see half of what the gates measure, the pass rate stays at or below 0.54
across the slopes run. If they see all of it, the gate cannot pass (≤ 0.06) and
the test usually returns `fail` (0.65 to 0.78), which is the correct verdict for
a gate that adds nothing beyond the forecast. (3) Which w holds on SCORE is not
known; the simulation shows how much option (b)'s result depends on it, not what
it is.

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
  carries the claim alone. The text-model reference makes this more likely than
  contamination alone would, because a stream can beat a weak reference by
  reading well (4.2, competence limit).
- **Domain.** The large replication projects are mostly social and behavioral
  science. A pass is scoped there.
- **A pass can credit a proxy.** If the baselines measure a cause of
  replication with low reliability and the gates track that cause, the
  increment is real and its attribution is wrong (7.5, noisy proxy: 22% pass at
  reliability 0.3). B4, B5 and the per-check pattern reduce this; nothing here
  removes it.
- **The development set is the most-studied set in the field.** Yang et al.
  trained on it, Van Bavel et al. recoded it, and its outcomes are famous. Its
  outcomes never choose, weight, or cut a rubric item (7.1, item 5), and that
  rule is what keeps its fame out of the gate score. They are used, by design,
  in two places that are not the rubric: to fit the recall-free reference text
  model (4.2, B4) and to calibrate the contamination probe (7.1, item 4).
  *Corrected 2026-10-17:* this bullet said "never for outcomes", which
  contradicted both.

## 12. What a pass would and would not mean

A pass would mean that design defects of the kind the gates name explain part
of a failure that current practice measures and does not explain: the shape a
Kuhnian crisis requires, on the predecessor's own instrument. It would not mean
that the gates improve research going forward (that is K-3's prospective
multi-team study), that Philosophy Engineering is a paradigm (community and
incommensurability are untouched), or that the result holds outside the domains
sampled. Nor would it cover PE-CLS-1.0 §7.5 A1 as a whole: the gate scores A1
only as a prediction stated before the results (Section 4, owner decision
2026-10-21), so outcome switching, absorbing components and unfalsifiable
framing are reported, not tested.
