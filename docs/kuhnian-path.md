# From reform to paradigm: a synthesis and a path

*Working document, 2026-10-17. Not a paper; a plan. Inputs: the outside draft
"An Architecture for Continuous Auditable Science" (Draft 0.1, October 2026,
[`philosophy-engineering-and-epistemic-sciops.docx`](philosophy-engineering-and-epistemic-sciops.docx),
hereafter **the SciOps draft**), the three arm specifications, and
[`papers/kuhn`](../papers/kuhn/) (hereafter **the Kuhn paper**).*

**Attribution.** The SciOps draft is the owner's, written with ChatGPT (5.6) and
outside this corpus, so it did not know the specs existed. Ideas marked
**[SciOps]** come from it. Its AI-use acknowledgment should name the model.

---

## 1. The goal, stated so it can fail

The owner's goal is a Kuhnian change in the scientific method. The Kuhn paper
already ran Kuhn's criteria against Philosophy Engineering and returned:

| Criterion | Verdict (Kuhn paper, Sept 2026) |
|---|---|
| Symbolic generalizations | Partial |
| Exemplars | Partial: five or six, no training pipeline |
| Community | **Fail**: one author |
| Crisis in a predecessor | **Fail**: the anomaly does not register on the reigning instruments |
| Incommensurability | **Fail**: PE-BRW-1.0 is a working translation procedure |

A path to the goal is therefore a plan to change specific cells of that table by
evidence, with each change registered in advance and each one able to fail. The
Kuhn paper is the baseline record. Nothing in this plan revises its verdict by
argument; only the measurements in §4 may do that.

One point, stated once. Incommensurability is the cell least likely to move,
because PE is designed to translate the old record rather than replace it. The
plan below targets the other four and treats the fifth honestly in §5.

## 2. What the SciOps draft already shares with the corpus

These need no integration, only cross-reference. The draft reaches them
independently, which is weak external corroboration of the design.

| SciOps draft | Corpus |
|---|---|
| Minimum claim object (Table 2) | PE-CLS-1.0 §3.1 |
| Claim graph, typed edges (§3.4) | PE-CLS-1.0 §6.1 (`uses`/`corroborates`/`scopes`/`supersedes`/`refutes`/`cites`) |
| "Supported never represented as proved" | PE-CLS-1.0 §4 class order, P3 authority |
| Withdrawal without erasing history (§4.4) | PE-CLS-1.0 §5 (rows never deleted), §4.2 (`withdrawn` is not `refuted`) |
| Dependency-triggered rebuild (§4.2) | PE-CLS-1.0 §6.3 propagation, §8 blast radius |
| Nonvacuity gate (gate 3) | PE-CLS-1.0 §9.1 (for the ledger), §10.5 registration theater; Foundation v1.0 non-degeneracy |
| Maturity levels 1–4 | PE-CLS-1.0 §9 L1–L4 (different cut, same idea) |
| Kuhnian only "in a restricted and testable sense" (§1, §11) | The Kuhn paper's verdict |
| Risks §10 | PE-CLS-1.0 §10 failure modes |

**Conflict to resolve, not merge:** the draft treats *Definition* as a claim kind
with a warrant state `defined`. PE-CLS-1.0 §4.4 makes definitions stipulations
exempt from the support cap. Keep the spec's rule. The draft's three-axis split
(kind / warrant / lifecycle, Table 1) is still useful; see I-1.

## 3. What is new and worth integrating

Ranked by how much each moves a cell in §1's table.

### I-1. Experimental-admissibility gates [SciOps §4.3, gates 3–5, 7]

The corpus checks the **record**: was it registered first (P1), is anything
missing (P2), does the prose overstate it (P3), do the dependencies close (P4).
It does not check whether the **design could grade the claim at all**. The
draft's gates do:

- **Nonvacuity (of the design, not the ledger):** some possible record withholds
  the promotion; free components that absorb every outcome are named.
- **Identification:** what the test relies on is identified on evidence fit for
  its role; calibration/evaluation overlap declared; a claimed subspace has a
  measured gap.
- **Intervention:** the manipulation moved the named construct, did not destroy
  the instrument, and did not construct the predicted response.
- **Inference:** treatment-induced selection handled on the target population;
  fixed denominator.

This is the largest gap the draft exposes. It is also the one the corpus's own
history keeps hitting (the OLGC audit; the KV long-generation withdrawal in
`case-studies/kv-longgen-withdrawal.md`), so it is a codification of practice, not
an import.

**Integration:** a new property family in PE-CLS (proposed **P5 Admissibility**,
with sub-checks A1–A4 for the four gates), or a fourth spec. Recommend P5 inside
PE-CLS: an inadmissible run is a fact about a claim's evidence, and it already
has a lifecycle exit (`void`/`withdrawn`). Each sub-check must emit an artifact
(counterexample record, eigengap, manipulation-check statistic), never a
self-marked yes.

### I-2. Three outcomes, not two [SciOps §3.5]

Support, contradiction, **inability to grade**. A run whose preconditions fail is
*inadmissible for that claim*, not negative evidence. **Correction after reading
the spec closely:** PE-CLS §3.2 already has this, as the physics-gate /
instrument-gate split (an instrument-gate miss voids the run). What was missing
is that the instrument gates were optional and untyped. Integrated as part of P5
(§7.5): A2 to A4 are mandatory instrument gates, and a voided run records which
check failed. No new state was needed.

### I-3. Semantic versioning of claims [SciOps §4.4]

Major = meaning, scope, or dependency change; minor = evidence or tested domain;
patch = presentation. *"A semantic change never masquerades as a clerical
correction."* This is the missing rule behind the corpus's most consequential
finding: the tts paper's **correction with a blast radius of zero** (87
occurrences rewritten, the stronger claim gone without a trace) is exactly a
major change shipped as a patch. With versioned claims it becomes a detectable
violation: a scope narrowing in the text with no major bump on the row. Also
closes PE-CLS §10.4 scope drift, which the spec currently leaves to humans.

### I-4. The scientific release [SciOps §4.4]

An immutable, addressable snapshot of claims + contracts + gate results + a
narrative rendering, citable at the level actually used. The corpus has ledgers
and papers but no release object binding them. This is the artifact a journal
can be asked to accept (step K-3), and the object whose adoption would count as
a change in the unit of record (§5).

### I-5. Authority separation for agents [SciOps §5.3]

*"One adaptive process cannot control every path to its own success."* Four
roles (author, executor, auditor, release authority) logged per action; no single
model instance generates, selects evidence, grades, and releases. The corpus
discloses AI use but has no rule here, and PE-CLS §10.6 verifier capture names the
problem without a control. Integrate as an extension of P3 (authority) or as a
release-gate requirement.

### I-6. Fault-injection maturity assessment [SciOps §7]

Assess conformance by *operating* it: pick a released claim, inject a controlled
upstream change, check the system marks every affected claim. PE-CLS conformance
is currently assessed by static checks. This is how you get a falsifiable
conformance claim rather than a self-reported one, and it gives P4's
under-declaration problem (29 dangling deps in the converted corpus) a test.

### I-7. Failed cases as the curriculum [SciOps §8.3]

*"Training should use failed cases... each exemplar should publish its rejected
designs and the minimal condition that would admit a revision."* This is the
draft's most Kuhnian idea, though the draft does not say so. Kuhn's paradigm in
the narrow sense **is** the exemplar, the solved problem students learn by doing.
A **defect benchmark** of seeded and natural defects, each with its gate and its
repair, is an exemplar library with a training pipeline, which is exactly what
the Kuhn paper scored as missing.

### I-8. Independent prospective evaluation [SciOps §9]

H1–H5, a matched multi-team study, success criteria registered by an
**independent methods team**, tools frozen first. This directly answers the Kuhn
paper's two worst negatives: n = 1, and "no external party is entitled to
demand these accounts."

### Not integrated

- The DevOps correspondence table (§4.1): useful for teaching, already the
  spine of `PRIOR-ART.md` §4. Use in talks, not specs.
- The 0–36 month phase plan as written: its Phases 0–1 are largely done in this
  repo. Replaced by §4.
- The draft's redefinition of Philosophy Engineering: superseded by the
  three-arm definition in the README. The SciOps layer is the operational
  practice of the inquiry and discovery arms, not a new discipline.

## 4. The path

Four stages. Each names the Kuhn cell it targets, a registered exit test, and
the falsifier that ends or redirects it. Register each stage as a ledger row of
class `predicted` before starting it (eat the dog food: the plan is itself a
claim set).

### K-1. Exemplars (Partial → Pass). Months 0–4.

*Status 2026-10-17:* P5 in PE-CLS and `pe_lint` done. Defect benchmark v0.1 in
[`benchmark/defects/`](../benchmark/defects/): 53 entries, 26 caught, 0 broken,
6 gaps; **24 external, 20 expressible** after P6 Integrity (s7.6) and two
amendments to A1/A4. The falsifier below is not triggered; the 4 inexpressible
are fabrication, disclaimed in s7.6.1. **Held-out test (fresh agent, blinded):
92% agreement on expressibility, 83% on exact gate;** both disagreements were
the author over-crediting the spec, and both were fixed. A human reader is the
remaining K-1 item.

1. Write P5 Admissibility (I-1), the `ungradeable` state (I-2), claim semver
   (I-3), and the release object (I-4) into PE-CLS 1.1. Extend `pe_lint`.
2. Build the **defect benchmark** (I-7) from the corpus's own failures: the OLGC
   audit's four defects, the twelve rebase-destroyed priority proofs, the
   orphan correction, the results graded above their dependencies, the KV
   withdrawal, the D1 undeclared families. Each entry: defect, the gate that
   catches it, the minimal repair, a fixture `pe_lint` must fail on.
3. Seed it with defects from the outside literature (target ≥ 20 entries not
   from the author's corpus).

*Exit:* `pe_lint` catches every benchmark entry; a reader who did not build it
can classify ≥ 80% of held-out entries using only the benchmark (threshold to be
set in the registration, not here). *Falsifier:* the corpus-external entries
are not catchable by any gate expressible in the spec, i.e. the method only
sees the author's own kind of error.

### K-2. Crisis (Fail → Pass). Months 3–12. **The critical stage.**

The Kuhn paper's crisis verdict concerned the judgment-arm anomaly
(representation dependence in benchmarks), which the reigning instruments do
not score as failure. The inquiry arm has a different anomaly, and the reigning
instrument **does** score it: **replication failure.** Science already measures
its own failure here by its own standards; that is why the field calls itself
in crisis (the Kuhn paper notes the rhetoric; the replication record is the
measurement behind it). What the reforms have not done is explain the residue:
studies that were preregistered, reproducible, peer reviewed, and still did not
replicate. The SciOps draft's §1 names that residue exactly: *reproducibility
can faithfully reproduce a conceptual error.*

**The test:** independent auditors, blind to replication outcomes, score the
original protocols of a set of studies that have since been replicated, using
gates A1–A4 only. Registered prediction: gate failures predict replication
failure **beyond** the predictors already known in the replication literature
(effect size, p-value, sample size, prediction-market prices where they exist).

- If it holds, the anomaly becomes visible **on the reigning instrument**: the
  method explains a measured failure of current practice that current practice
  cannot explain. That is the shape the Kuhn paper said a crisis requires.
- If it fails, the gates catch things replication does not care about, the
  crisis lever is not there, and the honest outcome is "reform, not paradigm"
  with a measurement behind it rather than an argument.

*Campaign:* [`campaigns/K2/`](../campaigns/K2/), registration drafted
2026-10-17, not sealed. Primary data: SCORE (274 claims, 164 papers, Nature
2026). Baseline to beat: AUC about 0.73 to 0.77 (markets, Altmejd et al. 2019).
Closest prior art: META-REP (Jekel & Smela), which already codes validity
indicators of originals to predict replication; if it has published, K-2's
novelty narrows to A1 and A4.

The draft's H5 is the second crisis vector and can run in parallel at lower
cost: AI-generated papers (AI Scientist-style systems) scored by narrative
review vs. by the gates. If narrative review passes defects the gates catch,
the predecessor practice (peer review of prose) fails by its own standard on
the input it is about to be flooded with.

### K-3. Community and external enforcement (Fail → Partial). Months 6–24.

1. **Independent teams** run the frozen K-1 toolkit without the author (I-8,
   the draft's H1–H4). Success criteria written by a methods team the author
   does not control.
2. **One external enforcer.** A Registered Reports venue, workshop, or funder
   that accepts a release (I-4) alongside the Stage-1 manuscript as a pilot.
   This is the Kuhn paper's double-entry point: the method spreads when someone
   other than the constrained party can demand the accounts.
3. **A training pipeline.** The defect benchmark as course material. The owner
   teaches graduate methods-adjacent courses; whether and where to use it is the
   owner's call and is not assumed here.

*Exit:* ≥ 3 programmes not by the author conform at L3 with fault-injection
assessment (I-6), and at least one external body requires or accepts the
release. *Falsifier:* teams cannot use it without the author (the draft's §9.3),
or adopt it only as post-hoc compliance (registration theater at community
scale).

### K-4. Unit of record (the Kuhnian residue). Months 18+.

The observable sign the SciOps draft proposes (§11) and the one worth adopting:
releases, not papers, become the maintained record, and **a refused design
counts as a result** (credited, citable negative engineering, the draft's §8.4).
That last change alters the disciplinary matrix's *values*, what a competent
scientist is rewarded for, which is a Kuhnian component independent of
incommensurability.

## 5. Incommensurability, stated plainly

PE-BRW-1.0 translates old records into ledgers, so by the Kuhn paper's own
argument the change is a conservative extension. The plan does not try to hide
that. Two honest positions remain, and the owner should choose between them
after K-2, not now:

1. **The translation is one-way.** A paper converts into a ledger; a ledger
   does not convert back into a paper without losing blast radius, class
   propagation, and admissibility verdicts. Kuhn's own Newton/Einstein case had
   a formal limiting translation too, and he still argued the concepts had
   changed. This is the argument for keeping the word "Kuhnian," and it would
   need to be made in the Kuhn paper's §5, against its current text.
2. **Kuhnian in four of five criteria.** Claim the change in exemplars, crisis,
   community, and values, and concede incommensurability. This is the more
   defensible claim and the one the SciOps draft's §11 already makes.

## 6. Open items before any of this is written into specs or papers

- [x] Authorship: owner + ChatGPT 5.6. Byline correct; name the model in the .docx AI acknowledgment.
- [x] **P5 Admissibility written into PE-CLS (§7.5), 2026-10-17**, required at L3. `pe_lint` does not check it yet.
- [x] **OLGC case checked against `geometric-cognition` (HEAD fdf124b), 2026-10-17.**
  The four defects are all in the record (C1 projected stimulus: 4e59e85, 6404279;
  isotropic moment on [0,100]³, calibration directions 56° apart vs 60° random:
  PREREG-C1-DRAFT.md:478-490; position bias with deliberation off: 4e59e85;
  unparsed-as-disagreement and survivor conditioning: 2d7758c, e5a7bc3).
  Three statements need correcting before any use:
  1. *"Preregistered bars"*: the C1 registration was a draft and was **never
     sealed**; no confirmatory seed was drawn (PREREG-C1-DRAFT.md:3).
  2. *"Changed the programme's claim states from testable or demonstrated to
     open"*: **contradicted**. CAMPAIGN.md:362 says no ledger claim has been
     raised or lowered by a gate; GC-34 is still `predicted`; the "manipulable
     budget" row was *added* as open, not lowered.
  3. "One audit" was several cold rereads plus refusals of C2 (twice) and C3
     (three times); the readers were sessions run by the programme itself, so
     the independence the draft implies is not there.
  The draft also omits the random-plane placebo that reproduced the contrast
  (CAMPAIGN.md:298-306), which is the strongest single exemplar for gate A3, and
  the selected scoring convention (three conventions, three signs; e5a7bc3).
  Separately, CAMPAIGN.md:352-360 and LEDGER.md:136-138 are stale (they predate C2,
  C3, H1): an OLGC-side repair, and itself a defect-benchmark entry (a record that
  stops tracking its own campaign).
- [x] **References checked, 2026-10-17.** All 11 checked exist; none fabricated.
  Fix [24]: Nature **655(8122):487–496** (online 19 May 2026). [18] is v2 (2024; v1
  Dec 2023). [23]: write "Chris Lu, Cong Lu". [22] GSN has no DOI; standard
  citation only. No prior use of "Epistemic SciOps" found (not exhaustive). No
  prior work found combining a versioned claim graph with status-changing gates;
  closest: Kuhn et al. 2016 nanopublications (doi:10.7717/peerj-cs.78), ORKG
  (doi:10.1145/3360901.3364435), Octopus (abstract only,
  doi:10.1136/bmjebm-2019-ebmlive.56).
- [ ] Add SciOps (Johnson et al., arXiv:2401.00077), Nuyujukian (arXiv:2310.08247),
  ORKG and Octopus to `PRIOR-ART.md`.
- [x] Owner decision: P5 inside PE-CLS. K-2 is the next campaign.
