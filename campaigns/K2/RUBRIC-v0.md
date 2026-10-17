# K2 coding rubric, v0 (DRAFT, NOT FROZEN)

Operationalizes PE-CLS-1.0 §7.5 checks A1 to A4 for a **published empirical
claim** whose article was not written with them in mind. Governs
[`PREREG-K2-DRAFT.md`](PREREG-K2-DRAFT.md) Section 4.

**Status.** v0 is written from the specification and the prior art, before any
article has been coded. It is revised only on the development set (Section 7.1
of the registration), which is disjoint from every test-set article. The frozen
version is renamed `RUBRIC.md`, and its blob hash is recorded in the
registration's Section 9 before any test-set coding starts. After the freeze,
changes are dated amendments that apply only to articles not yet coded.

## 0. Unit, inputs, and the rules that apply to every item

**Unit.** One *claim*: the specific finding the replication project targeted,
as that project stated it (SCORE claims are stated per claim). Code the study
in the article that supports that claim, not the whole article.

**Inputs.** The blinded article (title, authors, journal, year, DOI, and
references removed), its supplement if the article points to one, and the
claim statement. **Not** the replication report, any forecast, or a web search.

**Evidence rule.** Every item scored 1 (a failure) MUST carry a verbatim quote
or a located absence ("Method, Participants: no exclusion criteria stated;
Results reports N = 112 of 130 recruited"). An item scored 1 without evidence is
recoded U by the adjudicator.

**Absence vs. silence.** The rubric scores what the article shows, which is what
a reviewer could see. A practice that was carried out and not reported scores
as not reported. This is the registration's scope, stated in its Section 11.

**U (cannot be assessed).** Use U only when the article lacks the information
needed to answer *and* the absence is not itself the failure the item names.
"No manipulation check reported" is a 1 on A3.1, not U. "The supplement holding
the measure is not provided" is U on A2.1.

**Check score.** A check is 1 if any of its items is 1. It is 0 if every item is
0 or not applicable. It is U if no item is 1 and at least one is U. Gate score =
number of checks scored 1 (0 to 4).

**Recognition.** Before coding, the coder records whether they recognize the
study, and if so whether they know its replication outcome (Section 4.2 of the
registration). A coder who knows the outcome does not code that claim.

## A1 Nonvacuity: could any reportable outcome have counted against the claim?

| Item | Score 1 when the article shows… | Score 0 when… |
|---|---|---|
| A1.1 Prediction stated in advance | The hypothesis tied to the claim appears only in Discussion, or is introduced after results are presented, with no registration cited | The direction (or a stated null) is given before Results, or a registration is cited |
| A1.2 Primary outcome fixed | Several outcomes or scorings are reported for the claim and none is designated primary, or the claim rests on whichever was significant | One outcome is designated, or the claim holds for all reported outcomes |
| A1.3 No absorbing component | A component fitted or chosen after the data can reconcile any result with the claim: an unconstrained moderator invoked post hoc, a "conditions under which" clause added after the data, a free model parameter that rescues the effect | No such component, or it was fixed in advance |
| A1.4 A disconfirming result is reportable | The article's own framing treats every outcome pattern as supporting (e.g. an effect and its reversal both read as confirming) | At least one pattern is named, or plainly implied, that would count against it |

## A2 Identification: are the objects the test relies on identified, on data fit for their role?

| Item | Score 1 when… | Score 0 when… |
|---|---|---|
| A2.1 Measure validity evidence | The outcome measure is ad hoc (created for the study, items not given) or modified with no validity evidence, and nothing beyond face validity is offered | A validated instrument is cited for this population and use, or validity evidence is reported |
| A2.2 Reliability reported | A multi-item or coded measure is used and no reliability (α, ω, ICC, κ) is reported, or reliability is reported below the field's convention without comment | Reliability is reported and adequate, or the measure is single-item and behavioral |
| A2.3 Calibration and evaluation separated | A cutoff, composite, weighting, or classification used in the test was derived on the same data it is evaluated on, without saying so | Derived on separate data, fixed in advance, or the overlap is declared and corrected for |
| A2.4 Construct-to-measure link | The claim names a construct the measure does not plausibly capture without an argument (e.g. "trust" measured by a single donation decision with no link given) | The link is argued or conventional |

Source for A2.1 to A2.2: Flake & Fried 2020; Hussey & Hughes 2020.

## A3 Intervention: did the manipulation move the named construct, leave the instrument measuring, and not build the response?

Not applicable to purely correlational claims. Record "na: no manipulation" and
skip the check.

| Item | Score 1 when… | Score 0 when… |
|---|---|---|
| A3.1 Manipulation check | No manipulation check is reported, and no prior validation of this manipulation is cited | A check is reported and succeeds, or a prior validation of the same manipulation is cited |
| A3.2 Check succeeds | A check is reported and fails, or succeeds only in a subgroup, and the claim is stated without qualification | The check succeeds in the sample the claim is about |
| A3.3 Instrument intact | The manipulation plausibly changes how participants respond to the measure itself rather than the construct (demand, an instruction that changes the response format, a condition that changes who completes the measure) and nothing addresses it | Not plausible, or addressed (blind measure, demand check, a design that rules it out) |
| A3.4 Response not built in | The manipulation's content overlaps the outcome measure so that the predicted response is partly entailed (the prime contains the outcome words, the "treatment" is a version of the dependent measure) | No such overlap |

Source for A3.1: Chester & Lasko 2021 (roughly one third of JPSP 2017
manipulations reported a check).

## A4 Inference: is the estimand the registered one, on the population the claim is about?

| Item | Score 1 when… | Score 0 when… |
|---|---|---|
| A4.1 Exclusions fixed and reported | Participants are excluded with no stated rule, by a rule stated only after the data, or the number excluded is not given | Rule stated in advance or justified independently of outcome, and counts given |
| A4.2 Exclusions not condition-dependent | Exclusion or attrition differs across conditions by more than a few points and is not analyzed | Similar across conditions, or analyzed (intent-to-treat, sensitivity analysis) |
| A4.3 Denominator fixed | The analyzed sample is conditioned on a post-treatment variable (completers, passers of a post-treatment attention check, those who "understood" the treatment) with no analysis of the full sample | The analyzed sample is defined pre-treatment, or the full-sample result is reported |
| A4.4 One analysis convention | The claim's test is chosen among alternatives visible in the article (covariates added only in some models, a transformation applied without reason, a one-tailed test not justified in advance) and the alternatives disagree or are not reported | One analysis, fixed or conventional, or the alternatives are reported and agree |

## Adjudication

Two coders per claim, independent. Disagreements on a check score go to a third
coder who sees both evidence records and neither coder's identity. The
reliability bar (registration I1) is computed on the two independent codings
before adjudication, at the check level and on the gate score.

## Known gaps in v0, to be settled on the development set

- A1.3 and A1.4 are the most judgment-heavy items, and the likeliest to fail I1.
  If they do, they are cut or rewritten before the freeze, and the registration
  says which.
- "A few points" in A4.2 needs a number. It is set on the development set from
  the distribution of attrition differences, not here.
- Field conventions for reliability (A2.2) differ across SCORE's disciplines.
  The development set must cover at least economics, psychology, and political
  science before the freeze.
- The model-auditor prompt is this rubric verbatim plus the evidence rule. It is
  frozen with the rubric and hashed with it.
