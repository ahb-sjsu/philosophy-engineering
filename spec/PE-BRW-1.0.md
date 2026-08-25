# PE-BRW-1.0 — Brownfield Conversion

**Philosophy Engineering · Inquiry arm, brownfield mode · Draft, version 1.0**
Companion practice specification to [PE-CLS-1.0](PE-CLS-1.0.md) · 2026-08-25

> *Legacy code is simply code without tests.* — Michael Feathers
>
> **A legacy claim is simply a claim without a registration.**

Normative sections use RFC 2119 keywords and extend PE-CLS-1.0 §4.3, which
remains the authority on retrospective classification. This document is the
practice guide: how to convert an existing corpus without either laundering it
or destroying it.

---

## 1. Why this document exists

PE-CLS-1.0 describes a ledger as though a programme starts with one. Almost none
do. The realistic case is a corpus of papers, chapters, and results built over
years under ordinary scholarly norms, whose author now wants it governed. That
is **brownfield**, and it is the discipline's main entrance rather than a special
case.

It is also where the specification is most likely to be abused, and the abuse is
tempting rather than cynical: a claim that has been argued for, illustrated,
cited, and believed for three years *feels* established, and there is no moment
at which entering it as `demonstrated` feels like fraud. **The conversion is the
single highest-risk operation in the discipline**, because it is the one place
where a class can be assigned by confidence rather than by history.

## 2. Definitions *(normative)*

**Legacy claim.** A claim whose supporting evidence was available before the
claim was fixed in a form that could have failed. Equivalently: a claim with no
registration preceding its evidence. The definition is *historical*, not
qualitative — a legacy claim may be true, important, well-argued, and
well-evidenced.

**Epistemic debt.** The obligation a legacy claim carries: the risk it never
took. Debt is not error. A corpus with high debt is not wrong; it is
*unfalsified*, which is a different and recoverable condition.

**Debt ratio.** The fraction of a ledger's claims that are `retrospective`. A
conforming brownfield conversion MUST report it (PE-CLS-1.0 §4.3), and
`pe_lint` computes it as `retro_fraction`.

**Characterization classification.** Assigning a class that captures *what
support a claim actually has*, not what its author believes about it — the
analogue of Feathers' characterization test, which pins current behavior rather
than intended behavior.

## 3. The conversion is not a re-derivation *(normative)*

The instinct on adopting a rigorous method is to re-derive everything under it.
Resist this. It is the big-bang rewrite, and it fails for the same reasons:

- it is unbounded, so it never finishes;
- it destroys working results while in flight;
- it produces no falsifiable output until it is complete, so it cannot be
  checked;
- and it *cannot succeed anyway*, because re-deriving a claim does not give it
  the priority it lacked. **You cannot rewrite your way to a registration.**

A conforming conversion is therefore **descriptive first and reformative
second**: classify what exists honestly, then grow risk-bearing claims alongside
it.

## 4. The strangler-fig pattern for claims *(normative)*

Fowler's strangler fig grows a new system around an old one, migrating
capability incrementally until the old one can be removed. The claim analogue:

1. The legacy claim is entered **as it stands**, `retrospective: true`, classed
   by characterization (§2). It is not edited, weakened, or deleted.
2. A **prospective successor** is registered: a claim that puts some part of the
   legacy claim at risk on data it has not seen.
3. When the successor resolves, it carries the strong class. The legacy claim
   remains at `exploratory` with a `corroborates` edge to the successor —
   supported, but never itself promoted.
4. Over time the load-bearing weight shifts to the registered claims. The legacy
   rows stay as history, which is where they belong.

**The seam.** In legacy code a *seam* is a place where behavior can be changed
without editing in place. Here the `corroborates` edge is the seam: it attaches
new evidence to an old claim without rewriting the claim, so the historical
record and the current support are separately visible. A conversion that edits
legacy statements to match new evidence has destroyed exactly the information
the ledger exists to keep.

## 5. Procedure *(normative)*

Extends PE-CLS-1.0 §4.3's five steps with brownfield specifics.

**5.1 Inventory before classifying.** Enumerate substantive claims first. If the
corpus already carries epistemic markings, those markings are data and MUST be
carried over rather than re-derived — an author's own tag of *speculation* is
the most reliable signal in the corpus, because nobody over-tags their work as
weak.

**5.2 Classify by history.** For each claim ask only two questions: *what kind
of support exists?* and *did the claim precede its evidence?* Do not ask whether
it is true. Truth is what the subsequent registrations are for.

**5.3 Declare the dependency graph.** The step that pays for the exercise. A
legacy corpus carries dependencies in prose, so no refutation in its history has
ever had its blast radius computed. Expect this step to surface corrections that
were applied locally — in the section where they were discovered — and never
propagated. That is the normal condition of a careful corpus, not a mark against
it.

**5.4 Propagate the corpus's own corrections.** A programme honest enough to
record its own falsifications has already done the hard part. Run §6.3
propagation on each recorded refutation and publish the blast radius. **A
correction that has been recorded but not propagated is the highest-value defect
a conversion can find**, because it is invisible to readers of both the original
claim and the correction.

**5.5 Mint the forward exposure.** Conversion ends by registering at least one
prospective claim. A corpus converted to all-`exploratory` with no new
registration has been *described*, not *reformed*, and a ledger whose debt ratio
is 1.0 forever is a filing system.

**5.6 Acknowledge what only the author can resolve — the ratchet.**
*(normative)*

A conversion will surface contradictions internal to the legacy corpus that
**§3 forbids the converter from resolving**: a row graded as needing no modeling
assumptions while its own dependency list names them, a status and a proof that
disagree. These are not conversion defects. They are findings, and the correct
disposition is neither to fix them (that is re-derivation) nor to leave the gate
permanently red (a gate that always fails gates nothing).

A converted ledger MAY therefore carry a **baseline** of acknowledged findings,
subject to all of the following. Each is a defence against the baseline becoming
the laundering channel this specification exists to close:

1. **Named ownership.** Every entry MUST record `owner` and
   `resolution_required` — who can settle it, and what settling it looks like.
   An entry missing either is invalid and fails the run. *You may not
   acknowledge a failure without saying whose decision it waits on.*
2. **Full visibility.** Acknowledged findings MUST be printed in full on every
   run, under a heading that says they remain open. They are never suppressed,
   only *separated*.
3. **No unconditional pass.** A run with a non-empty baseline MUST NOT report
   plain conformance. It reports *conformance against baseline*, and MUST offer
   an unfiltered mode that reports the true state.
4. **Exact matching.** An entry matches only the exact `(property, claim,
   message)` triple. If a claim is promoted, its finding text changes and the
   entry stops matching — **so a baseline can never cover a claim that has been
   strengthened since it was written.** This is the mechanism that makes the
   ratchet one-directional.
5. **Monotone decrease.** An entry matching no current finding is STALE and
   fails the run: it was either resolved (remove it) or the claim changed shape
   (re-examine it). **A baseline may only shrink.**
6. **Fail loudly on absence.** A baseline named but not found MUST abort, never
   be silently skipped — otherwise a filtered verdict gets reported from an
   unfiltered run, which is the precise failure this whole apparatus prevents.

The baseline count is a second debt metric alongside the debt ratio, and it
carries a different meaning: the debt ratio measures how much of a corpus was
written before its evidence, while **the baseline measures how much of a corpus
contradicts itself in ways only its author can settle.** The first shrinks by
doing new work. The second shrinks by making decisions.

## 6. Anti-patterns *(informative)*

1. **Retroactive laundering.** Entering legacy claims at `demonstrated` because
   they are well-supported. The check exists (`pe_lint` §4.3) precisely because
   this one is invisible from inside.
2. **Big-bang re-derivation.** §3.
3. **Debt denial.** Converting only the strong claims and omitting the
   speculative ones — which breaks P2 and converts a corpus into a highlight
   reel. **Every substantive claim goes in the ledger, including the ones you no
   longer believe.**
4. **Statement drift under conversion.** Silently tightening a claim's wording
   as you enter it, so the ledger records a defensible version of a claim the
   corpus never made. Enter the claim as stated; if it is too loose to be
   falsifiable, that fact is itself the finding.
5. **Orphan corrections.** Recording a refutation in the section where it was
   found and nowhere else. §5.4.
6. **The tidy ledger.** A conversion that produces a clean, conforming, entirely
   `exploratory` ledger and stops. Conformance is not the goal; exposure is.

## 7. Debt paydown *(informative)*

A brownfield conversion's success metric is not the debt ratio at conversion —
which is near 1.0 by construction — but its **trajectory**. Useful practice:

- Report the debt ratio in the ledger's accounting from day one.
- Rank legacy claims by *load* (in-degree in the `uses` graph). The most-depended-on
  legacy claims are where prospective registration buys the most, and a
  high-load claim at `exploratory` is the corpus's structural risk.
- Register successors against high-load claims first. This is the equivalent of
  putting characterization tests around the code everything else calls.
- Expect the ratio to fall slowly and never reach zero. History does not
  convert.

## 8. Relationship to the rest of the discipline *(informative)*

Brownfield conversion is a **mode of the inquiry arm**, not a third arm of
Philosophy Engineering. The judgment/inquiry distinction is about the *subject*
governed — a deployed system versus a research programme. Greenfield/brownfield
is about the *state of the subject when the discipline arrives*, which is an
independent axis. A judgment-arm deployment can equally be brownfield: an
existing model given an equivalence registry and a canonicalizer after the fact
faces the same temptation to certify invariances it has never actually been
tested against.

| | Greenfield | Brownfield |
|---|---|---|
| **Judgment arm** | declare Γ and κ, then build | wrap an existing system; characterize invariances before certifying them |
| **Inquiry arm** | seal, measure, classify | inventory, characterize, propagate, then mint exposure |

The unifying rule is the same in all four cells: **record what is actually
true of the artifact's history, and never let the record assert more than that
history supports.**
