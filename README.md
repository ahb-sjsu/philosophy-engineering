# Philosophy Engineering

**The systematic discipline of translating philosophical commitments — epistemic
norms, ethical principles, logical consistency requirements — into
computationally enforceable constraints.**

Philosophy Engineering (PE) proceeds by declaring a domain-specific equivalence
relation over representations ("same case"), declaring invariances ("what must
not matter"), implementing a canonicalization or quotient that enforces them,
and packaging evidence into machine-checkable audit artifacts. This reframes
broad philosophical desiderata — objectivity, rationality, consistency,
non-arbitrariness — into contracts that are **falsifiable** (invariance claims
are testable, not aspirational), **localizable** (a failure produces a minimal
witness transformation), and **non-trivial** (passing by collapsing to a
constant output is detected and rejected).

The discipline has three arms. They are the same idea applied at three levels.

| Arm | Governs | Core artifact | Status |
|---|---|---|---|
| **[Judgment](spec/)** — the original programme | what an autonomous system asserts | the per-judgment **audit artifact** | [Foundation v1.0](foundation/) (March 2026) — EIP, BIP, 16 knowledge areas |
| **[Inquiry](spec/PE-CLS-1.0.md)** — what a programme may claim | what a *research programme* asserts | the per-claim **ledger row** | **PE-CLS-1.0** (this repo) |
| **[Discovery](spec/PE-DSC-1.0.md)** — what a programme may claim *survives* | which transformations a claim was tested against, and what broke it | the per-entry **invariance envelope** | **PE-DSC-1.0** (this repo) |

The second arm is the reflexive move. Philosophy Engineering says: take an
epistemic norm and make it mechanically checkable. Apply that to science's own
epistemic norms — priority of registration, absence of a file drawer, not
asserting beyond your evidence — and you get a **claim ledger**: a repository in
which each claim is an individually versioned, independently classified,
dependency-tracked object, and in which the norms are enforced by a linter
rather than by trust.

### The two arms were already the same rule

This is not a new idea grafted onto the discipline; it is a convergence that had
already happened in the corpus and was noticed once, in passing, in a draft
paper:

> *"This is same rule as philosophy engineering: **book may not assert what
> ledger cannot show**."*
> — `geometric-observation/paper/flip_paper_revtex.tex`

The Geometric Ethics book states the ledger's epistemic culture as a
*professional norm* three years before this specification made it checkable
(Part V Prelude, §17.0.2):

> *"Epistemic status tags as a discipline standard. Every claim in this book
> carries one of four tags … The tags are not decorative. They are load-bearing
> epistemic infrastructure."*
>
> *"Retractions are a feature, not an embarrassment. … A discipline that cannot
> be falsified cannot learn. Philosophy Engineering embeds 'predict, test,
> revise' as a professional norm: every model version is archived, every
> falsification is documented, and every revision has provenance."*

PE-CLS-1.0 changes exactly one thing about those sentences: it makes them
**enforceable**. A norm that says every revision *should* have provenance is a
culture; a checker that refuses a claim whose provenance does not resolve is an
engineering discipline. That step — from stated norm to mechanical refusal — is
the same step the judgment arm took when it turned "differences that do not
matter should not make a difference" into a witness-producing invariance test.

The two vocabularies were disjoint in wording and identical in structure. The
specification unifies them:

| Judgment arm (Foundation v1.0, Geometric Ethics §17.0) | Inquiry arm (PE-CLS-1.0) |
|---|---|
| Epistemic status tags — *definition / theorem (conditional) / empirical / speculation* | Claim classes — *proved / demonstrated / replicated / predicted / exploratory* |
| **Witness** — minimal counterexample to an invariance claim | **`refuted` row** + verification incident |
| Predict → test → revise, as professional norm | seal → govern → verdict → sealed revision act, as checked lifecycle |
| **Philosophy Engineering Dossier (PED)** — the versioned bundle that is the unit of work | **ledger row** — registration + instrument + result + verification + class |
| "Retractions are a feature" | `withdrawn`/`refuted` classes with defined propagation (§4.2, §6.3) |
| Equivalence registry Γ, versioned | gap-free identifier registry with dispositions (**P2**) |

The claim ledger is, in the existing vocabulary, **a PED for a research programme
rather than for a deployed system** — and the four properties of §7 are what a
PED's audit-artifact schema becomes when its subject is a theory.

---

## The problem the ledger arm solves

Standard practice publishes **monolithic PDFs** in which claims, proofs,
evidence, and citations are bundled into one indivisible artifact with a single
version and a single verdict. Four consequences follow, and all four are
structural rather than cultural:

1. **Granularity mismatch.** The unit of publication (the paper) is not the unit
   of truth (the claim). A paper containing nine sound results and one bad lemma
   has no way to express that state.
2. **All-or-nothing retraction.** Because the artifact is indivisible, correcting
   one lemma means retracting everything bundled with it — so the incentive is to
   correct nothing. Retraction burns the tree to prune a branch.
3. **Uncomputable blast radius.** Nothing records which results *depend* on the
   bad lemma. After a refutation, the question "what else falls?" is answered by
   memory and reading, not by traversal.
4. **The file drawer is unobservable.** Absence of a result is invisible by
   construction; "we report everything" is an unfalsifiable claim about an
   unobservable set.

A claim ledger addresses each one by treating scientific epistemology the way
software engineering treats a codebase: stable identifiers, explicit
dependencies, versioned status, deprecation semantics, and continuous
integration. **If a lemma is disproven, its row is deprecated and the blast
radius is computed — the tree is pruned, not burned.**

## What is actually new here

The components are not new and the specification says so at length
([PRIOR-ART.md](PRIOR-ART.md)). Preregistration, nanopublications,
micropublications, Manubot, research objects, and machine-checked libraries each
solve part of this. What PE-CLS-1.0 contributes is (a) the **conjunction**,
operated as a live programme, and (b) four **checkable properties** that convert
norms usually asserted on trust into predicates a machine can refuse:

| Property | The norm | The predicate |
|---|---|---|
| **P1 Priority** | "we registered before we measured" | the seal commit is a **git ancestor** of the first commit adding the result |
| **P2 Completeness** | "no file drawer" | the identifier sequence is **gap-free** and every ID resolves to a disposition |
| **P3 Authority** | "we don't assert beyond our evidence" | no document cites a claim **above its class** |
| **P4 Coherence** | "we know what depends on what" | every declared dependency **resolves**, and no claim outranks its weakest load-bearing support |

P2 is the sharpest of the four. "No file drawer" is normally unfalsifiable. Make
identifier assignment contiguous and require every identifier — including the
abandoned, the void, and the never-run — to carry a disposition, and the claim
becomes a property of a finite list that anyone can check in seconds.

### The discovery arm adds four more

PE-CLS-1.0 governs what a programme may claim. It says nothing about the step
where a claimed invariance **fails**, and that step is where a discovery
programme learns most. PE-DSC-1.0 adds four properties over a **transformation
registry**, the versioned declaration of the transformations a claim was tested
against:

| Property | The norm | The predicate |
|---|---|---|
| **D1 Declaration** | "we did not pick the class after seeing the result" | every test's family is **declared in the registry**, dated before the seal |
| **D2 Reduction** | "we reduced the failure" | every `failed` or `boundary` test carries a **witness** and an absorbing component from a closed list |
| **D3 Revision** | "we recorded what we changed our minds about" | every such test **cites the revised commitment**, or states that none is registered and why |
| **D4 Envelope** | "the invariance claim cites a record, not a sentence" | the registry fixes its tuple and ranks its families, so each entry's **envelope is generated** rather than written |

D3 is the one with no analogue in the other two arms. Without it a programme can
revise a commitment in response to evidence and leave no trace that it did, which
in the accounting is indistinguishable from never having been wrong.

The methodology these records serve is stated in *Discovery Philosophy
Engineering* (Bond, draft September 2026), whose Definitions 1 to 4 correspond
to the registry test, the envelope, comparative fundamentality, and the witness
respectively. That manuscript is not yet public and this specification does not
depend on it.

## Repository layout

### Greenfield and brownfield

Almost nobody adopting this starts from zero. The realistic case is a corpus
built over years under ordinary scholarly norms, whose author now wants it
governed — **brownfield**, and it is the discipline's main entrance rather than
a special case. [PE-BRW-1.0](spec/PE-BRW-1.0.md) specifies the conversion:
characterization classification, the strangler-fig pattern for claims, the
`corroborates` edge as the seam, and the debt ratio as the metric that matters.

Its governing definition, after Feathers: **a legacy claim is simply a claim
without a registration.** Not wrong, not weak — *unfalsified*, which is a
different and recoverable condition. Conversion is descriptive first and
reformative second, because **you cannot rewrite your way to a registration**:
priority is the one property no amount of later rigor reconstructs.

Brownfield is a *mode* of the inquiry arm, not a third arm. Judgment vs inquiry
is about the subject governed; greenfield vs brownfield is about the state of
that subject when the discipline arrives. Both axes apply to both arms.

| Path | Contents |
|---|---|
| [`spec/PE-CLS-1.0.md`](spec/PE-CLS-1.0.md) | **The Claim Ledger Specification** — normative. Objects, classes, lifecycle, dependency semantics, the four properties, conformance levels |
| [`spec/PE-BRW-1.0.md`](spec/PE-BRW-1.0.md) | **Brownfield Conversion** — bringing an existing corpus into a ledger without laundering it |
| [`spec/schema/`](spec/schema/) | JSON Schemas for the claim, registration, and verification objects |
| [`tools/pe_lint.py`](tools/pe_lint.py) | Reference validator. Checks P1–P4 against a real ledger; computes blast radius |
| [`docs/for-philosophers.md`](docs/for-philosophers.md) | **Start here if you came from philosophy.** The discipline without the code: what it takes from Popper, Lakatos, Merton and Hohfeld, where it is weakest, and five ways in |
| [`PRIOR-ART.md`](PRIOR-ART.md) | Honest positioning: what exists, what is borrowed, what is added |
| [`case-studies/`](case-studies/) | Worked retractions and promotions from live programmes |
| [`foundation/`](foundation/) | The judgment arm: Philosophy Engineering Foundation v1.0 (EIP, BIP, knowledge areas) |

## Reference deployment

The specification is descriptive of a programme that already runs it: the
Observation Theory ledger ([geometric-observation](https://github.com/ahb-sjsu/geometric-observation)),
91 sealed registrations with gap-free accounting, claim classes, adversarial
fresh-context verification, CI-rerun harnesses, and machine-checked cores in Lean
4. `tools/pe_lint.py` is developed against that ledger and its conformance report
is committed in [`case-studies/`](case-studies/).

The discovery arm is descriptive of the same programme's transformation
registries, which are not yet public. Checking a registry set:

```
tools/pe_lint.py --registry path/to/programme --level D-L3
```

Run against that programme the checks are **not** currently clean, and the
first finding is the one D1 exists for. Ten tests in one registry cite three
transformation families the registry never declares. The families were declared
in those gates' own sealed registrations and were not mirrored into the
registry, which is exactly the bookkeeping slip a mechanical check catches and a
reading does not. The specification had no way to record an honest repair: it
admitted a conforming row or a missing one, so the late registry and the fitted
one looked alike. [PE-DSC-1.0 §3.2.1](spec/PE-DSC-1.0.md) now separates them. A
backfill must carry the date it was written, name the sealed artifact that holds
the real declaration, and show that the declaration precedes the result;
otherwise it is a family chosen to fit a result and MUST NOT be entered. Deleting
the offending tests is not a repair either, because removing a test that ran is
the file drawer P2 exists to prevent.

## Status

PE-CLS-1.0 and PE-DSC-1.0 are **draft specifications**. They describe practice
that exists and formalize it; they are not proposals for practice nobody has
tried. Sections
marked *normative* carry MUST/SHOULD in the RFC 2119 sense; sections marked
*informative* do not. Breaking changes will increment the major version.

*The discipline's house rule, inherited from the judgment arm and applied to
itself: **a programme may not assert what its ledger cannot show.***
