# Brownfield conversion — the Geometric Ethics corpus

**Subject:** *Geometric Ethics* (book v1.24, ~35k lines) + six foundation papers
+ the ErisML keystone paper.
**Converted:** 2026-08-25, per [PE-BRW-1.0](../spec/PE-BRW-1.0.md).
**Result:** 141 claim objects · **debt ratio 0.986** · L3 with 4 findings.

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

---

*Ledger: `geometric-ethics/ledger/claims/` (141 objects).
Verify: `python tools/pe_lint.py --ledger geometric-ethics/ledger --level L3`.*
