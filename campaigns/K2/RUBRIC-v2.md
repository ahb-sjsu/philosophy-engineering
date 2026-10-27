# K2 coding rubric, v2: facts extracted, checks computed (DRAFT, NOT FROZEN)

Operationalizes PE-CLS-1.0 §7.5 checks A1 to A4 for a **published empirical
claim**. Governs [`PREREG-K2-DRAFT.md`](PREREG-K2-DRAFT.md) Section 4. The
design and the evidence for it are in [`RUBRIC-v2-PLAN.md`](RUBRIC-v2-PLAN.md)
Section 5.

**What changed from v1.** Coders no longer score checks. They answer factual
questions about the article, each answer tied to a verbatim quote or recorded
as not stated, and the check scores are computed from the answers by the rules
in [`k2_v2_rules.py`](k2_v2_rules.py), which are frozen with this file. Every
judgment item of v1 (A1.2 to A1.4, A2.3, A2.4, A3.3, A3.4, A4.4) is out of the
gate (v1 pilot: no coder pair read them alike; 7.4.1).

**Status.** Written from the v0 and v1 pilots and the literature in the plan,
before any v2 coding. Revised only on development articles (the spent 22 units,
the v2 development papers, and further undrawn papers from the eligible frame),
never on the held-out 18, whose texts nobody drafting v2 reads.

## 0. Unit, inputs, and rules for every question

**Unit.** One claim: the finding the replication project targeted, as it stated
it, and the test it named. Answer about the study and the test that support
that claim, not the whole article.

**Inputs.** The blinded coding unit and the claim statement. Not the replication
report, any forecast, or a web search.

**Answer only what the text states.** Every answer other than "not stated"
carries a quote copied exactly from the text (no paraphrase, no ellipsis inside
it). A quote that cannot be found in the text voids its answer:
the rules then treat the question as unanswerable (U). "Not stated" needs no
quote; it means you searched the text and the article does not say.

**Recognition first.** Record whether you recognize the study and whether you
know if it was replicated, before answering. A coder who knows the outcome does
not code that claim.

## 1. The questions

Each question has a fixed set of answers. Choose one. For the yes/no questions
(Q2.2, Q3.2, Q4.3, Q5.4, Q6.1, Q6.2), "no" includes "the article does not say".
Questions are answered in the order given; Q2.3 is asked with Q2.

### Q1 Design (decides which checks apply)

- **Q1.1 How were the conditions or groups compared in the claim's test
  formed?** `researcher_assigned` (the researchers manipulated the variable or
  assigned units to conditions, at random or not: an experiment) ·
  `natural_or_policy_variation` (a policy, event, cutoff or rule outside the
  researchers' control) · `observed_variation` (the compared values were
  measured, not assigned) · `not_stated`
- **Q1.2 Where do the data for the claim's test come from?**
  `collected_for_this_study` · `existing_dataset` (survey waves, administrative
  or archival records, a database, data from earlier work) · `not_stated`

### Q2 Prediction stated in advance (A1, gated item A1.1)

- **Q2.1 Quote the first sentence in the text that states what the authors
  predicted, hypothesized or expected for the claim (its direction, or that no
  effect was expected), worded as a prediction.** A sentence that reports what
  was found is a finding, not a prediction, even when it says "as expected" or
  "as predicted". `quoted` (give the quote) · `none` (no such sentence in the
  text)
- **Q2.3 Quote the first sentence in the text that reports a result of the
  claim's test (a statistic, or a statement of what was found).** `quoted` ·
  `none`. The rules compare where the two quotes sit in the text; you do not
  judge which comes first.
- **Q2.2 Does the article cite a preregistration or pre-analysis plan for this
  study?** `yes` (quote the registration statement) · `no`

### Q3 The claim's outcome measure (A2)

- **Q3.1 What kind of measure is the outcome of the claim's test?**
  `multi_item_scale` (answers to several questions or rating items by the
  participants, combined into one score, whatever the article calls it: scale,
  index, composite, average of items) ·
  `single_item_report` (one question answered by participants or respondents) ·
  `human_coded_or_rated` (people other than the participants coded or rated
  responses or materials) ·
  `constructed_index` (the authors combined several variables that are not
  questionnaire items, such as records or counts, into one) ·
  `behavior_or_performance` (what the participants did in the study, and any
  score computed from it: choices, amounts, times, accuracy, errors, rates,
  proportions or means of their responses) ·
  `record_or_physical` (data not produced by participants in the study:
  administrative or archival values, prices, money, votes, counts from
  records, and rates or ratios computed from them; physical or physiological
  quantities) · `not_stated` (the text does not say what the outcome is
  measured with)
- **Q3.2 Does the article cite an earlier source for this measure, or a
  validation of it?** `yes` (quote the citation) · `no`
- **Q3.3 Is a reliability coefficient for the outcome reported (alpha, omega,
  split-half, test-retest, ICC, kappa, or percent agreement of coders)?** give
  the value as a number between 0 and 1 (the lowest one if several), or
  `not_reported`

### Q4 Manipulation check (A3; asked only when Q1.1 is `researcher_assigned`)

- **Q4.1 Is a check reported that the manipulation changed what it was meant to
  change (a manipulation check)?** `reported` · `not_reported`
- **Q4.2 If reported, what did it show?** `succeeded` · `failed_or_mixed` ·
  `result_not_given` · `na` (no check reported)
- **Q4.3 Does the article cite an earlier study that validated this same
  manipulation?** `yes` · `no`

### Q5 Sample flow (A4)

Units are participants, respondents or the dataset's rows (firms, regions).
Dropping trials, responses or observations within a unit by a stated rule
(response-time cutoffs, error trials, practice trials) is not an exclusion.

- **Q5.1 How many units entered the study or dataset for the claim's test
  (recruited, sampled, randomized)?** a whole number as the text states it, or
  `not_stated`
- **Q5.2 How many units are in the claim's test?** a whole number only where
  the text states it as a count (N =, n =, "112 participants"); do not compute
  it from degrees of freedom. Otherwise `not_stated`.
- **Q5.3 Does the text say that units were excluded, removed or dropped from
  the claim's test, and how?** `none_excluded` (it says none were, or it
  mentions no exclusion) · `counted_with_reasons` (each exclusion's reason is
  given, and the number excluded, or the numbers before and after, are given) ·
  `excluded_without_count` (it says units were excluded, but not how many, or
  not why). Answer from what the text says about exclusions only; the rules
  compare Q5.1 and Q5.2 themselves.
- **Q5.4 Were any units excluded because of their values on the claim's outcome
  (as outliers on the outcome) without a rule stated before the exclusion?**
  `yes` · `no`

### Q6 Tests of the claim (A4)

- **Q6.1 Besides the claim's test, does the article report another test of the
  same claim that did not support it (in its stated direction, at the
  significance level the article uses): another subgroup, time point, sample,
  specification or model version of the same outcome?** Tests of other
  hypotheses do not count. `yes` (quote the unsupportive result) · `no`
- **Q6.2 Is a correction for multiple tests applied to the tests of the claim,
  or a family of tests named?** `yes` · `no`

## 2. Checks, computed (`k2_v2_rules.py`)

Each check is 1 (fails), 0 (passes), na (does not apply) or U (an answer it
needs is void or not stated where the rule cannot proceed). Gate score = number
of checks scored 1, 0 to 4, as in registration Section 4.

| Check | 1 (fails) when | na when |
|---|---|---|
| A1 (A1.1) | Q2.2 is `no`, and Q2.1 is `none`, or Q2.1's quote sits after Q2.3's in the text. A Q2.1 quote holding a test statistic is a finding and is voided | never |
| A2 | Q3.1 is `multi_item_scale`, `human_coded_or_rated` or `constructed_index` and Q3.2 is `no`; or Q3.1 is `multi_item_scale` or `human_coded_or_rated` and Q3.3 is `not_reported` or below 0.70 | Q3.1 is `single_item_report`, `behavior_or_performance` or `record_or_physical` (only the validity half can fail, and these carry none here) |
| A3 | Q4.1 is `not_reported` and Q4.3 is `no`; or Q4.2 is `failed_or_mixed` | Q1.1 is `natural_or_policy_variation` or `observed_variation` |
| A4 | Q5.3 is `excluded_without_count`; or Q5.4 is `yes`; or Q6.1 is `yes` and Q6.2 is `no` | never |

The rules fix the remaining cases (which answers give 0 and which give U); the
code is the definition and is tested case by case
([`k2_v2_rules_test.py`](k2_v2_rules_test.py)).

## 3. What v2 does not cover, stated

- **The judgment items** of v1 are not measured. A2's construct link, A3's
  demand paths, A1's absorbing components and A4's alternative analyses are
  part of PE-CLS §7.5 and are not part of this gate. A pass or fail of K2 with
  v2 is about the factual core of A1 to A4 (registration Section 12).
- **Reported, not done.** The questions record what the article states. A check
  done and not reported scores as not reported (as in v1).
- **Directly perceived manipulations** (A3, v1 known gap) still fail A3 without
  a check; left open.
- **Condition-dependent exclusions** (v1 A4.2) need per-condition counts that
  articles of this period seldom give; not in the gate.

## 4. Changes from v2.0 (development round 1, 2026-10-27)

Read on the 25 development units coded by gpt-oss and qwen3-small (thinking
off), two codings each (`k2_v2_dev_r1_agree.json`): gate ICC between families
0.51 (24 units), within 0.67 and 0.89.

| Change | Round-1 finding |
|---|---|
| Q1.1 merges random and non-random assignment into `researcher_assigned` | A3 needs only whether the researchers assigned conditions; 10 of 24 cross-family pairs split on randomness or on "not stated" for the same experiment |
| Q3.2 asks only whether a source is cited | gpt-oss read "new or modified" into an uncited measure (12 of 24 pairs split, κ 0.15) |
| Q6 asks whether an unsupportive test of the claim is reported, not how many tests | counts differed in 9 of 24 pairs, and 1 was void |
| Quotes (`k2_v2_rules.quote_found`): 4 letters or digits suffice, and a quote with an ellipsis passes when every fragment of 12 or more characters is found | the 8-character minimum voided short quotes ("N = 213"): 40 voided quotes were found verbatim by `k2_quote_check`; 36 used an ellipsis whose fragments are all in the text |
| Not changed: Q2.1 | its splits are on the psychology units, which are cut to Method and Results and so often lack the introduction where a prediction is stated; the v2 unit keeps the hypothesis page. The psychology units are weak material for A1 |

## 5. Changes from v2.1 (development round 2, 2026-10-27)

Round 2 (`k2_v2_dev_r2_agree.json`): gate ICC between families 0.51 (23
units), exact gate agreement 65% (38% in round 1); Q3.2 κ 0.15 to 0.68; voided
gpt-oss answers 110 to 43.

| Change | Round-2 finding |
|---|---|
| Q5.3 drops `not_stated`; "no exclusion mentioned" is `none_excluded` | the rules already scored the two alike; 4 of 23 pairs split between them |
| Quote length limit raised from 40 to 120 words | 15 quotes found verbatim were voided for length alone |
| Units: 3 more development papers shaped like the held-out set (`v2dev2`: L9OZ, m8V1, qWvQ; seeded draw `k2_v2dev_draw.py`) | 20 of the 23 compared units are psychology units cut to Method and Results, unlike the held-out unit |

## 6. Changes from v2.2 (the disputed evidence, 2026-10-27)

Owner, 2026-10-27: "read the disputed evidence and write rules". The drafting
session read both families' answers and quotes on every development unit where
their majority answers (three codings each, round 3) differed, for Q2.1, Q3.1,
Q5.2 and Q5.3. The splits were systematic, and each rule below answers one.

| Change | What the disputed evidence showed |
|---|---|
| Q2.1 becomes two quotes (the first prediction, the first result); code compares their positions; a "prediction" quote holding a test statistic is voided | 8 units split. qwen3-small quoted findings ("We found that...", "As expected, the condition effect was significant, F(2, 43)...") as predictions stated before the results; gpt-oss read "as expected" in a result as the prediction first stated with it. Judging before/after was the coder's job and neither did it the same way |
| Q3.1: combined questionnaire items are `multi_item_scale` whatever the article calls them; `constructed_index` only for non-questionnaire variables; scores computed from what participants did are behavior; records are data participants did not produce; `not_stated` added | 11 units split: averaged items called a scale by one family and an index by the other (3 units); error rates, word percentages and report probabilities called behavior, index or record; a dependent variable named but not described |
| Q5: trial-level dropping is not an exclusion; Q5.3 is what the text says about exclusions only; "counted" means the number excluded or the numbers before and after | 6 units split: spoiled trials (about 20% of data) read as excluded participants; exclusions inferred from the recruited N |
| Q5.2: a number only where the text states the count; no conversion from degrees of freedom | 8 units split, several on converting degrees of freedom (t(62) to 64 or 63; F(1, 99) to 101 or 103) |
| Not changed: which study the claim names (DEV-ML-034: 228 recruited against 80 analyzed in another study) | a target problem, not a rubric one |

These rules were written from the development units they will be scored on
next, so the next round overstates agreement; the held-out 18 measure it.
