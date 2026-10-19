# K2 coding rubric, v1 (DRAFT, NOT FROZEN)

Operationalizes PE-CLS-1.0 §7.5 checks A1 to A4 for a **published empirical
claim** whose article was not written with them in mind. Governs
[`PREREG-K2-DRAFT.md`](PREREG-K2-DRAFT.md) Section 4.

**Status.** v1 revises [`RUBRIC-v0.md`](RUBRIC-v0.md) after the v0 pilot
(registration 7.4), in which two model families agreed on the gate score at
ICC 0.11. It was written from the coders' item scores and evidence on the
revise half of the development units only (`k2_rubric_split.json`, committed
before any of that was read); the held-out half measures it. The changes are
listed at the end. It is revised only on the development set, which is
disjoint from every test-set article. The frozen version is renamed
`RUBRIC.md`, and its blob hash is recorded in the registration's Section 9
before any test-set coding starts. After the freeze, changes are dated
amendments that apply only to articles not yet coded.

## 0. Unit, inputs, and the rules that apply to every item

**Unit.** One *claim*: the specific finding the replication project targeted,
as that project stated it, and the original test it named where it named one
(the *focal test*). Code the study in the article that supports that claim,
not the whole article.

**Score the focal test, not the article.** Every item asks about the focal
test and the outcome, sample and analysis it uses. Other studies, other
hypotheses, manipulation checks, descriptive statistics and secondary measures
in the article count only where an item names them. A study that reports many
tests is not thereby failing any item.

**Inputs.** The blinded article (title, authors, journal, year, DOI, and
references removed), its supplement if the article points to one, and the
claim statement. **Not** the replication report, any forecast, or a web search.

**A failure is something you can point to.** Score 1 only for a defect the item
names that you can quote or locate. The absence of a reassurance (no demand
check, no validity citation, no statement that a rule was fixed in advance) is
a 1 only where an item says that absence is the failure.

**Evidence rule.** Every item scored 1 (a failure) MUST carry a verbatim quote
or a located absence ("Method, Participants: 130 recruited; Results: df imply
112 analyzed; no exclusions reported"). An item scored 1 without evidence is
recoded U by the adjudicator. Quote the text exactly; do not paraphrase inside
quotation marks.

**Absence vs. silence.** The rubric scores what the article shows, which is what
a reviewer could see. A practice that was carried out and not reported scores
as not reported. This is the registration's scope, stated in its Section 11.

**U (cannot be assessed).** Use U only when the article lacks the information
needed to answer *and* the absence is not itself the failure the item names.
"No manipulation check reported" is a 1 on A3.1, not U. "The supplement holding
the measure is not provided" is U on A2.1.

**na (not applicable).** Use na only where an item says so. A3 is na as a whole
for a claim with no manipulation.

**Check score.** A check is 1 if any of its items is 1. It is 0 if every item is
0 or na. It is U if no item is 1 and at least one is U. Gate score = number of
checks scored 1 (0 to 4).

**Recognition.** Before coding, the coder records whether they recognize the
study, and if so whether they know its replication outcome (Section 4.2 of the
registration). A coder who knows the outcome does not code that claim.

## A1 Nonvacuity: could any reportable outcome have counted against the claim?

| Item | Score 1 when the article shows… | Score 0 when… |
|---|---|---|
| A1.1 Prediction stated in advance | The hypothesis tied to the claim appears only in Discussion, or is introduced after results are presented, with no registration cited | The direction (or a stated null) is given before Results, or a registration is cited |
| A1.2 Outcome not chosen after the fact | Two or more outcome measures or scorings could each have tested the claim, they disagree (one supports it, another does not or is not reported in full), and the claim rests on the one that supports it | The claim names its outcome or uses one outcome; or every outcome that could test the claim supports it. A missing "primary" label is not by itself a failure |
| A1.3 No absorbing component | A component fitted or chosen after the data can reconcile any result with the claim: an unconstrained moderator invoked post hoc, a "conditions under which" clause added after the data, a free model parameter that rescues the effect | No such component, or it was fixed in advance |
| A1.4 A disconfirming result is reportable | The article's own framing treats every outcome pattern as supporting (e.g. an effect and its reversal both read as confirming) | At least one pattern is named, or plainly implied, that would count against it |

## A2 Identification: are the objects the test relies on identified, on data fit for their role?

| Item | Score 1 when… | Score 0 when… |
|---|---|---|
| A2.1 Measure validity evidence | The focal test's outcome is a self-report scale, a rating, a coded response or a constructed index that was created for the study (items not given) or modified, and no validity evidence or source is offered | A validated or previously used instrument is cited; or the outcome is a direct behavioral or performance measure (response time, accuracy, error rate, choice, amount given, count, physical quantity), which A2.4 covers instead |
| A2.2 Reliability reported | The focal outcome is a multi-item scale or composite, or is coded or rated by people, and no reliability (α, ω, split-half, ICC, κ) is reported, or it is below .70 without comment | Reliability is reported at .70 or above, or the outcome is a single item, or a direct behavioral or performance measure averaged over trials |
| A2.3 Calibration and evaluation separated | A cutoff, window, item selection, weighting or classification used in the focal test was chosen by looking at the same data's outcomes (stated, or evident from wording such as "we chose the window that captured…"), and no robustness to the choice is reported | The quantity is fixed by design or convention (condition labels, a simple mean or sum, a published formula, a conventional trimming rule), or derived on separate data, or the article reports that other reasonable choices give the same result. Fitting a model to estimate its parameters is not by itself a failure |
| A2.4 Construct-to-measure link | The claim names a construct the measure does not plausibly capture without an argument (e.g. "trust" measured by a single donation decision with no link given) | The link is argued or conventional |

Source for A2.1 to A2.2: Flake & Fried 2020; Hussey & Hughes 2020.

## A3 Intervention: did the manipulation move the named construct, leave the instrument measuring, and not build the response?

Not applicable to purely correlational claims. Record "na: no manipulation" and
skip the check.

| Item | Score 1 when… | Score 0 when… |
|---|---|---|
| A3.1 Manipulation check | No manipulation check is reported, and no prior validation of this manipulation is cited | A check is reported and succeeds, or a prior validation of the same manipulation is cited |
| A3.2 Check succeeds | A check is reported and fails, or succeeds only in a subgroup, and the claim is stated without qualification | The check succeeds in the sample the claim is about. **na when no check is reported** (A3.1 carries that) |
| A3.3 Instrument intact | You can name a specific path by which the manipulation changes how participants respond to the measure itself rather than the construct (an instruction that cues the expected answer, a condition that changes the response format or who completes the measure), and the design does not rule it out. Naming the path as a limitation does not rule it out | No such path can be named, or the design rules it out (blind measure, demand check, a control that shares the path). A missing demand check is not by itself a failure |
| A3.4 Response not built in | The manipulation's content overlaps the outcome measure so that the predicted response is partly entailed (the prime contains the outcome words, the "treatment" is a version of the dependent measure) | No such overlap |

Source for A3.1: Chester & Lasko 2021 (roughly one third of JPSP 2017
manipulations reported a check).

## A4 Inference: is the estimand the registered one, on the population the claim is about?

Participants are the unit in A4.1 to A4.3. Trial-level trimming by a stated
conventional rule (response-time cutoffs, error trials, practice trials) is not
an exclusion here.

| Item | Score 1 when… | Score 0 when… |
|---|---|---|
| A4.1 Exclusions reported and outcome-independent | Participants were excluded and the number is not given (including when the analyzed N or degrees of freedom imply fewer than were recruited), or participants were excluded on the focal outcome itself (e.g. as outliers on the dependent variable) with no fixed rule stated | No participant was excluded; or each exclusion is counted and its reason does not depend on the focal outcome (suspicion, equipment failure, missing demographics, non-compliance, a stated outlier rule) |
| A4.2 Exclusions not condition-dependent | Exclusions or attrition differ across conditions by 10 percentage points or more and by at least 3 participants, and this is not analyzed | The difference is smaller, or analyzed (intent-to-treat, sensitivity analysis), or the design is within-participants, or no participant was excluded. U if more than 5% of participants were excluded and the split by condition is not given |
| A4.3 Denominator fixed | At least 5% of randomized participants were excluded on a variable measured after or affected by the treatment (a post-manipulation attention check, suspicion probe, compliance with the treatment, completion), and the focal test is reported only on the remaining sample | The analyzed sample is defined before treatment, or fewer than 5% were excluded this way, or the full-sample result is also reported |
| A4.4 One analysis of the focal outcome | Two or more analyses of the same focal outcome for the same claim are visible that differ in specification (sample restriction, covariates, transformation, one- vs two-tailed, a different test), they disagree, and the claim rests on the one that supports it | One analysis of the focal outcome; or the alternatives agree; or a one-tailed test is justified by a direction stated before Results. Different tests of different outcomes or hypotheses are not alternatives |
| A4.5 Multiplicity | The claim is supported by a subset of several tests of it (subgroups, time points, pairwise comparisons among conditions), the others did not support it or are not reported, and no correction or family is stated. Several outcome measures are A1.2, not here | The claim rests on a single focal test; or every test of the claim supports it; or a correction is applied to a stated family. Tests of other hypotheses in the article do not count |

## Adjudication

Two coders per claim, independent. Disagreements on a check score go to a third
coder who sees both evidence records and neither coder's identity. The
reliability bar (registration I1) is computed on the two independent codings
before adjudication, at the check level and on the gate score.

## Changes from v0, and the v0 pilot finding each answers

Read on the 11 revise-half units: 36 cross-family pairs of codings per item.

| Change | v0 finding (revise half) |
|---|---|
| Section 0: score the focal test, not the article; a failure is something you can point to; quote exactly | gpt-oss scored A4.5, A4.4 and A1.2 as failures because the article contained several tests, outcomes or hypotheses at all |
| Unit names the focal test | The pilot gave only the study number (a deviation from v0), so coders could not tell which test was the claim's |
| A1.2 scores outcomes that disagree, not a missing "primary" label | 19 of 36 pairs split; studies of this era rarely label a primary outcome, and gpt-oss scored 73% failures on that alone |
| A2.1 limited to scales, ratings, coded responses and indices | 18 of 36 split, mostly on response times, error rates and offers, which one family called invalid for lacking a citation |
| A2.2 scope and a .70 threshold | gpt-oss's two codings of the same article split on 5 of 11, on whether response times need an α |
| A2.3 limited to choices made by looking at the outcome | 18 of 36 split; simple means, model fits and published formulas were called "calibrated on the same data" |
| A3.2 is na without a check | A3.2 split on 25 of 36: with no check reported, coders scored it 1, 0, U and na |
| A3.3 needs a named path | gpt-oss scored "no demand check reported" as a failure |
| A4 participant unit; trial trimming excluded | A4.1 and A4.3 split over response-time trims, practice trials and outlier rules |
| A4.1 drops "stated in advance" | Not observable in pre-registration articles; coders split on articles with no exclusions at all |
| A4.2 threshold: 10 points and 3 participants; U rule | v0's "a few points" had no number (a known v0 gap); one coder called 5 of 24 against 9 of 24 similar |
| A4.3 needs 5% excluded post-treatment | One non-complier in 44 was scored as a conditioned denominator |
| A4.4 alternatives are analyses of the same outcome | Separate tests of separate outcomes were scored as alternative conventions |
| A4.5 the claim must rest on a subset of its own tests | 16 of 36 split; any uncorrected test anywhere in the article was scored |

The two thresholds (A4.2, A4.3) and the .70 in A2.2 were set while writing this
version, from the convention they name, not by checking how they score the
held-out units.

## Known gaps in v1, to be settled on the development set

- A1.3 and A1.4 are the most judgment-heavy items, and the likeliest to fail I1.
  If they do, they are cut or rewritten before the freeze, and the registration
  says which.
- Field conventions for reliability (A2.2) differ across SCORE's disciplines.
  The development set is RP:P + Many Labs (psychology) plus a ~30-claim
  non-psychology supplement from SCORE's journals and years (registration
  7.1.1). The A2.2 threshold and the A4.2 and A4.3 thresholds are checked per
  discipline on it.
- A3.1 scores a missing manipulation check as a failure even where the
  manipulated variable is a stimulus property the participant perceives
  directly (timing, position, a word shown), for which a check is rarely
  meaningful. Both families agree on it (5 of 36 pairs split), so it is a
  validity question, not a reliability one, and v1 leaves it as in v0.
- Many Labs targets carry the effect label and, for Many Labs 1, the comparison
  from its codebook, not a written claim (the sources hold none).
- The model-auditor prompt is this rubric verbatim plus the evidence rule. It is
  frozen with the rubric and hashed with it.
