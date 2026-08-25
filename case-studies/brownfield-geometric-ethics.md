# Brownfield conversion — the Geometric Ethics corpus

**Subject:** *Geometric Ethics* (book v1.24, ~35k lines) + six foundation papers
+ the ErisML keystone paper.
**Converted:** 2026-08-25, per [PE-BRW-1.0](../spec/PE-BRW-1.0.md).
**Result:** **234 claim objects** · debt ratio **0.962** · L3 with 5 findings ·
**6 registrable predictions identified**.

*Converted in two phases: Appendix F's tagged registry (141 rows), then the
untagged domain chapters 20–28 and the foundation papers (93 rows).*

This is the discipline's first brownfield conversion, and the corpus was chosen
because it is the hard case: a large, expansive, philosophically ambitious body
of work written before the ledger method existed, by an author who has since
adopted it elsewhere. The question was whether conversion could be done without
either laundering the work or destroying it.

---

## 1. The corpus already had a ledger

The single most important finding. The book carries **Appendix F: "Mathematical
Ledger — Status of Formal Claims"**, a table with columns
`Ref | Name | Status | Dependencies | §`, using five epistemic statuses whose
definitions are quoted in the appendix header:

> *Conditional Theorem: a result that is mathematically proved given stated
> assumptions (listed in the Dependencies column); **the theorem is as strong as
> its premises**.*

138 rows extracted mechanically. **The DAG spine already existed** — the author
had done the inventory step (PE-BRW §5.1) years before the specification asked
for it. Conversion was therefore extraction, not authorship, which is the best
possible case and worth stating plainly: *a corpus that tags its own claims is
most of the way to a ledger.*

The same is true of the epistemic culture. The book's §17.0.2 states the norms
this specification enforces — "epistemic status tags … are load-bearing
epistemic infrastructure", "retractions are a feature, not an embarrassment",
"every revision has provenance." PE-CLS-1.0 adds enforcement, not ethics.

## 2. What conversion found

### 2.1 The corrections were recorded but never propagated

The corpus documents three genuine falsifications, all reported prominently
rather than buried — the SU(2) gauge group (CHSH tests, N=600, all |S| ≤ 2), the
obligation-hysteresis prediction (double-blind, N=630, not confirmed and
reversed), and the ERT sacred-axis schism prediction ("zero confirmations and
falsified on the best-powered instrument available"). Each was applied **in the
section where it was discovered**.

None had its blast radius computed, because the dependency column never recorded
which claims rested on the falsified ones. This is PE-BRW §5.4's *orphan
correction* anti-pattern, and it is the normal condition of a careful corpus:
prose can hold a correction, but only a graph can propagate it.

Wiring the five rows that are *about* the gauge group and recomputing:

```
blast radius of the D4-as-measured claim
  suspended (5): Thm 12.2 (Discrete Symmetry = D4) · Thm 12.3 (Gauge Group
                 Uniqueness) · Prop A.2 (Discrete Conservation from D4) ·
                 Prop 8.3 (D4 Structure of Hohfeldian Transitions) ·
                 Lemma 9.1 (D4 Constraint on Metric Components)
  untouched (135): everything else, named explicitly
```

Five claims, not the book. That is the difference between pruning and burning.

### 2.2 The corpus tells the D₄ story two ways

The sharpest live inconsistency, and it is genuinely subtle because **the
correction is right and nearly complete**. The foundation papers now state it
carefully:

> *"The measured deontic symmetry group is the Klein four-group V₄ … The
> dihedral group D₄ is posited as an ambient group, licensed only if quarter-turn
> operations are independently demonstrated as normative operations."*

The book's own registry agrees, grading D₄ a **Conditional Theorem from Axioms
A1–A5**, and its skeptic's appendix states the empirical test **has not been
run**. But the methodology chapter says the opposite in the same volume:

> *"The D₄ symmetry was **found by testing** every transformation against
> thousands of moral scenarios"* … *"These structural constraints … are empirical
> findings about moral reasoning. They are **discovered, not chosen**."*

The measured 82–87% correlative symmetry supports the two commuting involutions
— the V₄ core. The quarter-turn generator that promotes V₄ to D₄ is nowhere
measured. Entered as `GE-D4-MEASURED`, **suspended**, with both resolutions
named: withdraw the discovered-in-data wording, or register the quarter-turn
measurement prospectively.

Propagation is complete in `erisml-lib` (36 of 36 mentions correct) and
**incomplete in `erisml-compiler`**, where two sentences still assert a
"D₄-structured Hohfeld module" — one of which survives untouched in the revised
draft that retracts it 93 lines later.

### 2.3 The self-refuting negative control

The keystone paper's `body.tex` states a falsification condition — *exhibit a
genuine moral consideration independent of all nine dimensions and the basis
must be extended* — and then, 112 lines later, calls Purity/sanctity "the quiet
negative control" **because it has no cell in the basis**. The revised draft
catches this itself, and the correction is worth quoting because it is the
discipline working:

> *"Treating Purity's absence as a convenient negative control would have been
> **using the basis's incompleteness as evidence for the basis**; we do the
> opposite and take the branch the data selected."*

A ledger would have caught it mechanically: the falsification condition and the
negative-control claim are the same row, asserted in opposite directions.

### 2.4 The DAG's roots are outside the corpus

Every load-bearing theorem in the foundational paper is discharged by a *proof
sketch* deferring to an uncirculated monograph — six distinct deferrals
(Theorems 9.2, 11.1, 11.3, 14.1, 17.1, 17.2). The abstract says "We prove"; the
body says "see [companion]". The only self-contained proofs in the corpus are
short EIP/BIP algebra results, none of which is a claim about morality.

In ledger terms these are `uses` edges pointing outside the ledger. The
converter logged 29 such rows. **A dependency you cannot resolve is not a
dependency you can rely on**, and P4 makes that visible where a citation does
not.

### 2.5 Phase 2: the dark matter, and a registry that contradicts itself

Chapters 20–28 contain **81 numbered theorems, propositions, corollaries and
lemmas that carry no epistemic tag and appear in no registry** — roughly a third
of the corpus's formal content, invisible to its own accounting. Domain claims
about economics, clinical ethics, law, finance, theology, environment, AI,
bioethics and military ethics, several of them strong (*"QALY discrimination
against the elderly and disabled is not an implementation failure. It is
mathematical"*).

All 81 are entered `exploratory`/`retrospective` by characterization, and 49
were wired to the three roots the inventory identified — the nine-dimensional
basis, BIP, and Scalar Irrecoverability — which the domain chapters invoke
constantly and cite almost never. **Thm 15.1 (Scalar Irrecoverability) is itself
absent from Appendix F**, despite four domain theorems being explicit
instantiations of it; it had to be added as a root.

Phase 2 also exposed an internal contradiction in the source registry. Three
rows are graded **`Proved`** — which Appendix F defines as *"a result that
follows from standard mathematics alone, **without ethical modeling
assumptions**"* — while their own Dependencies column lists modeling
constructs:

| Row | Name | Declared dependency |
|---|---|---|
| Prop 11.3 | Satisfaction as Directional Derivative | Def 6.1, Prop 11.1 |
| Prop 11.4 | A* Optimality on Stratified Spaces | Def 11.2 |
| Prop 6.2 | Decomposition of Disagreement | Def 6.4 |

A row cannot be both "no ethical modeling assumptions" and dependent on ethical
modeling constructs. Either the status or the dependency list is wrong, and only
the author can say which. **These are the ledger's four surviving P4 errors, and
they should stay red until resolved** — that is what a conformance failure is
for.

They also forced a specification change. §3 forbids the converter from
resolving them, but a gate that fails permanently gates nothing — the next real
regression would land in a report that was already red. **PE-BRW-1.0 §5.6 (the
ratchet)** resolves the tension: the four are *acknowledged*, each naming its
owner and what would settle it, and the gate now blocks anything *new*. The
mechanism is built to be unusable as a laundering channel — entries match on the
exact finding text, so a promoted claim stops matching; a stale entry fails the
run; a missing `owner` fails the run; and no run with a non-empty baseline may
report unconditional conformance. **A baseline may only shrink.**

The baseline is a second debt metric, and it means something different from the
debt ratio: the ratio measures how much of a corpus was written before its
evidence, the baseline measures **how much of a corpus contradicts itself in
ways only its author can settle**. The first shrinks by doing new work; the
second shrinks by making decisions.

## 3. Classification, and one specification change

Mapping the book's five statuses required a distinction the specification did
not have.

A **Conditional Theorem** is *two claims*: the implication (proved) and the
consequent (only as strong as its premises). Classing them `proved` produced 49
support-cap violations — correctly, since their premises are Modeling Axioms.
The fix is to class by the **consequent**, which is what the row asserts about
moral reasoning, and record the mathematical status in the evidence. The book
says this itself: *"the theorem is as strong as its premises."*

A residue of 9 violations then exposed a genuine gap in **PE-CLS-1.0**: a
*Formal Definition* ("Topological Manifold") is a stipulation, not a falsifiable
claim, and cannot weaken a theorem that uses it. The specification had no object
for that. **§4.4 (`definition` class) was added**, with the guard that a
definition resting on a substantive claim is a modeling axiom in disguise — which
now fires as a warning on 4 rows.

Final state: 23 `definition`, 105 `exploratory`, 11 `proved`, 2 `refuted`.

## 4. The debt ratio, and what it means

**0.986** — 139 of 141 rows retrospective. The corpus states the reason itself:

> *"The hypotheses tested in the BIP experiments and the Dear Abby analysis were
> formulated after the framework was developed. The experiments are therefore
> **confirmatory-by-design**."*

This is not a criticism; it is a measurement, and one the corpus had already
made in prose. What the number adds is that it is now *reportable* — and that
its trajectory is the metric that matters.

Two observations sharpen it. First, the summary tables mark five results
"Confirmed" with **no test statistic, effect size, CI, or null model** anywhere;
the only significance figures in the foundational paper (28.7%, 6.3σ) appear
solely in a supplementary-materials list and are never analyzed in the body.
Second, and decisively: **the one prospective, double-blind study in the corpus
is the one that falsified a prediction.** That is what prospective design does,
and it is the strongest argument available for minting more exposure.

## 5. What conversion did *not* do

Per PE-BRW §3, no claim was re-derived, no statement was edited, and nothing was
deleted. The moral-manifold apparatus is intact. Chapters 20–28 (~100 domain
theorems with predictions and explicit "falsified if" clauses) are untagged and
unregistered in the source, and remain outside this ledger — the largest
remaining conversion work, and the place where the corpus's own prediction lists
make prospective registration cheapest.

## 6. Next step: mint the exposure

A conversion that stops here has *described* the corpus, not reformed it
(PE-BRW §6, "the tidy ledger"). The corpus supplies its own candidates, already
written as falsifiable predictions with thresholds:

- **The quarter-turn measurement.** Resolves `GE-D4-MEASURED` and unsuspends
  five theorems. The corpus states the test: demonstrate quarter-turn operations
  as normative operations, or withdraw D₄ to V₄ everywhere.
- **Prediction 20.6** (economics): *factor analysis of economic behavioral data
  recovers ≈9 dimensions; falsified if fewer than 7 or more than 11.* A
  registrable prediction with a pre-stated interval, on public data.
- **Prediction 22.x** (law): the same shape for ~8 legal dimensions.

Each is a `corroborates` edge waiting to be attached to a high-load
`exploratory` row — the strangler fig, applied where the corpus is already
load-bearing.

### 6.1 One is now sealed — and the reread is the point

`GE-P-2026-006` (Prediction 20.6) was drafted, **reread cold in a later
session**, and **rewritten rather than sealed**. The programme's rate-limit rule
— seal only after a reread in a session other than the drafting one — caught a
defect that would otherwise have been permanent:

> The draft named the **Moral Machine aggregated AMCE matrix** as one of three
> corpora. That dataset carries **nine attribute dimensions by design**, so no
> factor solution on it can exceed k = 9 — and the published clause's *"more than
> eleven"* branch was **unreachable by construction.** Half the falsification
> condition could not fire.

Two related defects followed from the same blind spot: an instrument gate of 20
items, *below the 33 needed to identify 11 factors*, and an unnamed third corpus
inside a document whose entire purpose is eliminating unnamed choices. All three
were fixed before sealing, and the reread is recorded **inside the sealed
document** rather than quietly corrected.

This is the strongest single argument in the case study for the rate-limit rule,
and it is worth stating in its general form: **a one-directional test reported as
a two-directional one is not a weak result, it is a wrong one** — and it is
invisible in prose, because the prose said "three public corpora," which sounds
like more rigour rather than less.

Sealed `sha256:11c168e5…`, with the pre-rebase hook installed *before* the seal
so the priority evidence cannot be lost the way the sibling programme lost
eleven anchors (PE-CLS-1.0 §7.1.1).

**Phase 2 found these already written.** Six chapter predictions carry
pre-written falsification clauses and have never been tested; they are entered
with status **`registrable`** and are the only non-retrospective rows in the
ledger besides the refutations. Examples, verbatim from the source:

> *Prediction 6 (Manifold Dimensionality): Factor analysis of economic
> behavioral data should recover approximately nine dimensions. **Falsified if**
> fewer than seven or more than eleven.*

> *Prediction 5 (Heuristic Admissibility): moral heuristics should satisfy
> h(n) ≤ h\*(n).*

A pre-stated interval, on public data, written by the author years ago and never
run. **The corpus's route out of 0.962 debt is not new theory — it is executing
predictions it already published.** That is the most encouraging thing this
conversion found.

---

*Ledger: `geometric-ethics/ledger/claims/` (141 objects).
Verify: `python tools/pe_lint.py --ledger geometric-ethics/ledger --level L3`.*
