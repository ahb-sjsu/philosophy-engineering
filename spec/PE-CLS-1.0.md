# PE-CLS-1.0 — The Claim Ledger Specification

**Philosophy Engineering · Inquiry arm · Draft specification, version 1.0**
Andrew H. Bond · 2026-08-25

> **House rule.** A programme may not assert what its ledger cannot show.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in *normative*
sections are to be interpreted as in RFC 2119. Sections marked *informative*
carry no conformance weight.

---

## 1. Scope

This specification defines a **claim ledger**: a version-controlled repository in
which the atomic unit is not the paper but the **claim**, and in which four
epistemic norms — priority of registration, completeness of the record, fidelity
of assertion to evidence, and integrity of dependencies — are enforced by
mechanical check rather than by trust.

It specifies the objects a conforming ledger contains (§3), the evidence classes
a claim may carry (§4), the lifecycle transitions a claim may undergo (§5), the
dependency edges between claims and their propagation semantics (§6), the four
checkable properties (§7), the blast-radius computation that makes localized
retraction possible (§8), and four conformance levels (§9). §10 records the
failure modes of the method itself.

This specification does **not** prescribe what a programme should study, which
claims are worth making, or what counts as an adequate experiment in any
particular field. It prescribes only the form in which claims and their support
are recorded, and the checks that form makes possible.

## 2. Motivation *(informative)*

A monolithic publication bundles claim, argument, evidence, and citation into one
indivisible artifact carrying one version and receiving one verdict. Four
structural consequences follow.

**Granularity mismatch.** The unit of publication is not the unit of truth. A
paper with nine sound results and one bad lemma has no representation for that
state; the literature must treat it as wholly standing or wholly withdrawn.

**All-or-nothing retraction.** Because the artifact is indivisible, correcting a
component requires retracting the whole. The incentive is therefore to correct
nothing, and the observed retraction rate reflects that incentive rather than the
underlying error rate.

**Uncomputable blast radius.** Dependencies between results are carried in prose
if at all. After a refutation the question *what else falls?* is answered by
recollection. Nobody can enumerate the affected set, so nobody does.

**Unobservable file drawer.** The absence of a result is invisible. "We report
all outcomes" is a claim about an unobservable set and is therefore
unfalsifiable — the one assertion in a paper that no reader can check.

The remedy this specification pursues is not cultural exhortation but a change of
representation: make the claim the addressable unit, declare the edges, and
define the checks. Software engineering solved the structurally identical problem
for code with stable identifiers, explicit dependency declaration, semantic
versioning, deprecation policy, and continuous integration. None of that
machinery is novel. Applying it to the epistemology rather than to the artifacts
is the move this specification makes.

## 3. Objects *(normative)*

A conforming ledger contains five object types. Each MUST have a stable
identifier that is never reused, and MUST be stored in a version-control system
whose commit graph is preserved (§7.1 depends on ancestry).

### 3.1 Claim

The atomic unit of assertion.

| Field | Req. | Meaning |
|---|---|---|
| `id` | MUST | Stable, unique, never reused |
| `statement` | MUST | One sentence, falsifiable as written |
| `class` | MUST | One of §4 |
| `scope` | MUST | The conditions under which the statement is asserted; a claim asserted outside its scope is a different claim |
| `evidence` | MUST | Edges to registrations, results, or machine-checked proofs |
| `depends` | MUST | Edges to other claims (§6), possibly empty — but the field MUST be present, so that "nothing" is asserted rather than omitted |
| `status` | MUST | §5 lifecycle state |
| `history` | MUST | Append-only record of class and status changes with reasons |
| `supersedes` | MAY | The claim this one replaces |

A claim's `statement` MUST be falsifiable *as written*. "Method X is effective"
is not a claim; "Method X exceeds baseline B by ≥ δ on metric M under scope S"
is.

### 3.2 Registration (seal)

A prediction recorded **before** the measurement that tests it.

A registration MUST carry: the prediction; the bar (the numeric threshold that
constitutes success); how the bar was sized (power analysis, pilot value with
margin, or an explicit declaration that neither was done); the design (n,
stopping rule, clustering unit); the falsification condition; and a content hash.

A registration MUST distinguish **physics gates** (a miss refutes the claim) from
**instrument gates** (a miss voids the run). Conflating them permits a failed
experiment to be re-described as a broken instrument after the fact, which
defeats the purpose of registering.

Amendments MUST be dated, MUST state their reason, and MUST precede unblinding.

### 3.3 Instrument

The code that produces evidence. MUST be content-hashed, and the hash MUST be
recorded in the registration that governs it. A ledger SHOULD re-execute
instruments in continuous integration and compare against committed results.

### 3.4 Result

A measurement artifact. MUST be committed to the repository (not merely
described), MUST record the seed and configuration that produced it, and SHOULD
be machine-readable. A result whose instrument cannot be re-run MUST be marked as
such.

### 3.5 Verification

An independent check of a claim's derivation or evidence. A verification record
MUST state: what was checked, by whom or what, whether the verifier had access to
the author's reasoning (**fresh-context** verification is verification by an
agent that did not participate in producing the claim), and the findings —
including findings that were *not* errors.

A verification that finds nothing is evidence only if the search was real and
visible. A ledger SHOULD record the verification's scope so that a null finding
is interpretable.

## 4. Evidence classes *(normative)*

A claim's class states **what kind of support it has**, not how strongly its
author believes it.

| Class | Support | Priority | Minimum evidence |
|---|---|---|---|
| `proved` | deductive | n/a | Complete written proof **and** at least one independent line-by-line verification; machine-checked where feasible; known gaps named |
| `replicated` | multiple independent settings | registered | ≥2 independent settings (models, datasets, source families) each meeting its own registered bar |
| `demonstrated` | one setting | registered | Registration predating the run; committed result; instrument re-runnable |
| `predicted` | out-of-sample | registered in advance | Registered before the data existed or before unblinding; blinded where feasible |
| `exploratory` | suggestive | none | Labeled as such in every context; MUST NOT support a claim of any higher class |
| `refuted` | evidence against | — | The registered prediction failed against **valid** evidence |
| `withdrawn` | evidence invalid | — | The supporting evidence is defective; the claim reverts to unknown (§4.2) |

### 4.1 The class order is partial, not total

Classes vary along two independent axes: **support** (how much evidence) and
**priority** (whether the claim was at risk before measurement). `demonstrated`
carries more support than `predicted` but less priority. Neither dominates.

A conforming ledger MUST therefore express its citation policy as an explicit
predicate over classes, not as a numeric rank. Example, from the reference
deployment: *an umbrella principle may cite only `proved`, `replicated`, and
`predicted` rows* — which admits `predicted` while excluding the
better-supported `demonstrated`, because the umbrella's warrant is risk borne,
not evidence accumulated.

### 4.2 `withdrawn` is not `refuted`

This distinction is normative and load-bearing.

- A claim is **`refuted`** when a valid measurement contradicted its registered
  prediction. The world answered, and the answer was no. This is *information*:
  the negation is now supported.
- A claim is **`withdrawn`** when its supporting evidence is discovered to be
  invalid — instrument defect, provenance failure, arm contamination,
  irreproducible aggregation. The world did not answer. The claim returns to
  **unknown**, and its negation gains nothing.

Conflating the two corrupts the record in both directions: it manufactures
negative results from broken instruments, and it permits genuine refutations to
be laundered as instrument failures. The propagation rules of §6.3 differ between
the two cases, so the distinction is not merely descriptive.

*Worked instance:* [`case-studies/kv-longgen-withdrawal.md`](../case-studies/kv-longgen-withdrawal.md) —
a claim that a quantizer degraded under long generation, withdrawn after
re-validation attributed the effect to arm-label contamination, where the
*opposite* claim (the effect belongs to a different codebook) proved true.

## 5. Lifecycle *(normative)*

```
    registered ──▶ measured ──▶ classified ──┬─▶ promoted   (class ↑, new evidence)
        │                           │        ├─▶ demoted    (class ↓, support lost)
        │                           │        ├─▶ superseded (replaced; row retained)
        │                           │        ├─▶ refuted    (terminal, informative)
        │                           │        └─▶ withdrawn  (→ unknown, repairable)
        │                           │
        └─▶ void (never run) ───────┘
```

Rows MUST NOT be deleted. A row that is superseded, refuted, withdrawn, or void
remains in the ledger with its history intact. **Deletion is the failure mode the
ledger exists to prevent**; deprecation is the supported operation.

A `void` identifier — assigned but never run — MUST carry the reason it was never
run. Identifiers burned by a design failure discovered before sealing are `void`,
not absent, and their disclosure is part of §7.2.

## 6. Dependency edges and propagation *(normative)*

### 6.1 Edge types

| Edge | Meaning | Load-bearing |
|---|---|---|
| `uses` | The claim's derivation or argument **requires** the target | **Yes** |
| `corroborates` | The target is one of several independent supports | Partially |
| `scopes` | The target narrows this claim's conditions | Yes (for scope) |
| `supersedes` | This claim replaces the target | n/a |
| `refutes` | This claim contradicts the target | n/a |
| `cites` | Contextual or motivational reference only | **No** |

The `uses`/`cites` distinction is the specification's most consequential
requirement. **A dependency that would change the claim's truth if removed MUST
be declared `uses`**, regardless of how the prose reads. Declaring a load-bearing
dependency as `cites` defeats §8 silently, which is the one failure this
specification cannot detect from the outside.

The `uses` and `corroborates` relations MUST form a directed acyclic graph. A
cycle indicates circular support and MUST be reported as a conformance failure.

### 6.2 The support-cap rule

A claim MUST NOT hold a class stronger than the weakest class among its
load-bearing (`uses`) dependencies, where "stronger" is evaluated in the partial
order of §4.1 along the relevant axis.

A `proved` claim whose derivation uses an `exploratory` claim is not proved. A
`replicated` claim resting on a single `demonstrated` result is not replicated.
This rule is checkable (§7.4) and is the most frequently violated in practice,
because prose permits an author to lean on a weak result without noticing.

### 6.3 Propagation on status change

When claim `c` transitions to `refuted` or `withdrawn`, for every claim `a` with
a path to `c`:

**If the path is `uses` (load-bearing):**
- `c` refuted → `a` MUST be re-derived without `c`, or demoted. `a`'s status
  becomes `suspended` until one of those occurs. `a` MUST NOT retain a class that
  depended on `c` being true.
- `c` withdrawn → `a`'s status becomes `suspended`. Because `c` reverted to
  unknown rather than false, `a` MAY be restored unchanged if `c` is repaired;
  the ledger MUST record that `a` is awaiting `c`'s repair rather than refuted.

**If the path is `corroborates` (redundant-capable):**
- `a`'s support set is recomputed without `c`. If the remaining support meets
  `a`'s class minimum (§4), `a` stands and the ledger MUST record the reduced
  support. Otherwise `a` is demoted to the class its remaining support sustains.

**If there is no path:** `a` is **untouched**, and §8 requires this to be
*reported*, not assumed.

The last clause is the point of the whole construction. A retraction under this
specification produces a named, finite, checkable set of affected claims and an
explicit statement that everything else stands. That is what it means to prune
rather than burn.

## 7. The four checkable properties *(normative)*

Each property converts a norm that is ordinarily asserted on trust into a
predicate over the repository. A conforming ledger MUST be able to demonstrate
each mechanically.

### 7.0 Provenance of the four properties *(informative)*

These are not new commitments. They are the discipline's existing four
commitments — stated for deployed systems in the keystone paper's §6 — made
checkable when the subject is a research programme rather than a judgment
engine:

| Philosophy Engineering commitment (keystone §6) | Property here |
|---|---|
| **Declared modeling choices** — "every bridge from a moral claim to a computational object carries its epistemic status … so that what is proven is not confused with what is posited" | **P3 Authority** — every claim carries a class, and no document may cite above it |
| **Stated invariances** — "written down and tested, not assumed silently" | **§3.1 `scope`** — the conditions of assertion are a required field; a claim asserted outside its scope is a different claim |
| **Extracted predictions** — "a model earns its keep by entailing measurable claims" | **P1 Priority** — the prediction and its bar exist, in the repository, before the measurement |
| **Versioned revision** — "when a prediction fails the model is amended and the change recorded" | **P4 Coherence** + §6.3 propagation — the amendment's consequences are computed, not recalled |

**P2 Completeness has no counterpart in the judgment arm**, and this is
structural rather than an oversight. A deployed system's audit artifacts are
generated per judgment, so the set of judgments is observable by construction. A
research programme's set of *attempted* results is not observable at all unless
the programme makes it so. P2 is what the reflexive move adds: the requirement
that the enumeration exist.

### 7.1 P1 — Priority

*The norm:* the prediction was registered before the measurement that tested it.

*The predicate:* for every claim of class `demonstrated`, `replicated`, or
`predicted`, the commit introducing its registration MUST be an **ancestor in the
version-control graph** of the commit that first introduced its result.

```
git merge-base --is-ancestor <seal-commit> <first-commit-adding-result>
```

Ancestry, not timestamp. Timestamps are author-controlled and can be backdated;
ancestry is a property of the commit graph that is verifiable at any later
snapshot, including from an archived copy. This is a *tamper-evident* guarantee,
not a cryptographic proof of time — a ledger MAY strengthen it with an external
timestamp authority, and MUST NOT describe ancestry alone as proof of wall-clock
priority.

#### 7.1.1 History rewriting destroys P1 evidence *(normative)*

Commit hashes are not stable under history rewriting. A rebase, squash, filter,
or amend **re-parents the commit and changes its hash**, after which a recorded
seal hash either (a) resolves to a commit that is no longer an ancestor, or (b)
does not resolve at all. In both cases the priority evidence is destroyed even
though the underlying priority was real, and the ledger becomes unable to prove a
true claim.

This is not hypothetical. The reference deployment records 32 checkable seals; 20
verify, one resolves but fails ancestry because the sealing commit was rebased
(the row itself documents the rebase, so the *record* is honest and only the
*machine check* fails), and eleven name commits that no longer exist in the
repository at all. See
[`case-studies/conformance-geometric-observation.md`](../case-studies/conformance-geometric-observation.md).

Therefore:

- A conforming ledger **MUST NOT rewrite the history of any commit that seals a
  registration.** Rebasing the ledger branch is a conformance-destroying
  operation and SHOULD be prevented mechanically (protected branch, or a
  pre-rebase hook that refuses when the range contains a seal commit).
- A registration **MUST** additionally carry a **content hash** of its own text
  (independent of commit identity). Content hashes survive rewriting and let a
  rewritten ledger be re-anchored: the registration is still identifiable even
  when its commit is not.
- If history is rewritten despite the above, the ledger **MUST** record the
  mapping from the old commit identifier to the new one in the affected row.
  A row that names a non-resolving seal without such a mapping **MUST** be
  reported as a P1 failure, not a warning: a claim whose priority cannot be
  checked is, for conformance purposes, a claim whose priority is unproven.
- A ledger **SHOULD** anchor seals with an identifier that is stable by
  construction — a signed tag, a git note, or an external timestamp — so that P1
  survives operational accidents.

*Design note.* This is an instance of the specification's general posture: the
purpose of a mechanical check is to fail loudly on a defect that prose would
absorb silently. Here the defect is not dishonesty but ordinary version-control
hygiene, and the check found it in a programme whose written record was already
accurate.

### 7.2 P2 — Completeness (no file drawer)

*The norm:* every result is reported, whatever its sign.

*The predicate:* identifiers MUST be assigned from a **contiguous sequence**, and
**every** identifier in the range MUST resolve to a disposition — reported,
superseded, void with reason, or never-assigned with proof of never-assignment
(e.g. absence from the full version-control history).

This is the specification's sharpest lever. "No file drawer" is otherwise an
unfalsifiable claim about an unobservable set. Contiguous assignment makes the
set *finite and enumerable*: a reader checks that the sequence has no unexplained
holes. A hidden failure now requires either a visible gap or a false disposition,
both of which are attackable.

A gap-free sequence does not prove that no work was hidden — an author could
maintain a second, unregistered sequence. It proves that hiding requires
affirmative falsification rather than mere silence, which is the achievable
guarantee.

### 7.3 P3 — Authority

*The norm:* no document asserts more than its evidence supports.

*The predicate:* every assertion in a programme's prose MUST resolve to a ledger
row, and the citing context's declared class policy (§4.1) MUST admit the cited
row's class. A synthesis that cites an `exploratory` row as though it were
`replicated` is a conformance failure detectable by parsing.

Corollary — the **assertion-authority separation**: narrative documents (papers,
books, talks) hold *no* independent authority to assert. They are views over the
ledger. This is what makes the ledger the unit of truth rather than a supplement
to the paper.

### 7.4 P4 — Coherence

*The norm:* the programme knows what depends on what.

*The predicate:* (a) every declared dependency resolves to an existing row; (b)
the `uses`/`corroborates` graph is acyclic; (c) the support-cap rule (§6.2) holds
for every claim; (d) no claim is `suspended` without a recorded reason naming the
dependency that suspended it.

## 8. Blast radius *(normative)*

**Definition.** For a claim `c` in ledger `L`, the **blast radius**
`BR(c)` is the transitive closure of load-bearing dependency edges into `c`:

> `BR(c) = {c} ∪ { a ∈ L : a ⟶uses* c }`

extended by the `corroborates` recomputation of §6.3.

**Proposition (containment).** If `L` satisfies P4 — every load-bearing
dependency is declared and the dependency graph is acyclic — then a status change
to `c` affects no claim outside `BR(c)`.

*Proof.* Immediate from the definition of the transitive closure: a claim with no
`uses` path to `c` has, by P4(a), no undeclared dependency on `c`, and its
support set is therefore unchanged by any status change to `c`. ∎

**Remark (where the work is).** The proposition is mathematically trivial and its
force lies entirely in its hypothesis. The theorem is not the contribution; the
discipline that makes its hypothesis *true* is. A ledger that permits
load-bearing dependencies to go undeclared satisfies the letter of §6.1 while
rendering §8 vacuous, and no external check can detect this. Declaration
integrity is the one property this specification must take on trust, and
programmes SHOULD therefore treat undeclared-dependency discovery as a
first-class defect — recorded, like any other error, in the row's history.

**Reporting.** On any transition to `refuted` or `withdrawn`, a conforming ledger
MUST publish the blast-radius report: the affected set, the disposition of each
member, and the explicit statement that claims outside the set are unaffected.

## 9. Conformance levels *(normative)*

A ledger MAY claim conformance at one of four levels. Each includes the previous.

| Level | Name | Requires |
|---|---|---|
| **L1** | Accounted | §3 objects; §4 classes on every claim; **P2** (gap-free, dispositioned) |
| **L2** | Prioritized | L1 + **P1** (ancestry-verified registration) + physics/instrument gate separation |
| **L3** | Coherent | L2 + §6 declared edges + **P4** + **P3** + blast-radius reporting |
| **L4** | Verified | L3 + fresh-context verification for load-bearing claims + machine-checked cores where the claim is formalizable + CI re-execution of instruments |

L1 is achievable by an individual researcher in an afternoon and already delivers
the file-drawer guarantee. L4 is what a programme making theoretical claims at
scale should target.

## 10. Failure modes of the method *(informative)*

A specification that cannot say how it fails is a marketing document.

1. **Bureaucratic capture.** The apparatus can become the output. A programme
   that produces registrations and conformance reports but no results has failed,
   and no conformance level detects this. The ledger's own value MUST be judged
   by the claims it carries, not by its tidiness.
2. **Granularity gaming.** Splitting a claim into many small rows inflates
   apparent output; merging many into one hides internal failure. The unit of
   claim is a judgment call the specification cannot make.
3. **Undeclared dependency.** §8's blind spot, above.
4. **Scope drift.** A claim's `scope` can be quietly widened in a later document
   while the row is cited unchanged. P3 checks the class, not the scope. Scope
   verification remains a human task.
5. **Registration theater.** A registration whose bars are set so loosely that no
   outcome could miss them is conforming and worthless. §3.2's power requirement
   mitigates but does not eliminate this.
6. **Verifier capture.** A fresh-context verifier that shares the author's
   assumptions, tools, or training will miss the same things the author missed.
   Independence is a matter of degree and SHOULD be characterized, not asserted.
7. **The reflexive problem.** This specification is itself an unregistered claim
   about how inquiry should be governed. It carries no evidence class. It should
   be read as `exploratory` until programmes other than its author's have tried
   it and reported what broke.

## 11. Relationship to the judgment arm *(informative)*

Philosophy Engineering's original programme (Foundation v1.0) governs what an
autonomous system asserts: declare an equivalence over representations, enforce
invariance, emit a per-judgment audit artifact. This specification governs what a
*research programme* asserts, and the structure is deliberately parallel:

| Judgment arm | Inquiry arm |
|---|---|
| Declared transformation group `T` | Declared claim scope |
| Invariance under `T` | Class stability under re-derivation |
| Canonicalization before judgment | Registration before measurement |
| Per-judgment audit artifact | Per-claim ledger row |
| Witness for an invariance failure | Blast-radius report for a retraction |
| Non-degeneracy (not constant) | Non-triviality (bars that could miss) |

Both arms make the same move: take a norm that is ordinarily enforced by
professional culture, and give it a representation in which violation is
mechanically detectable.

---

## Appendix A — Minimal conforming claim (informative)

```yaml
id: OT-GO-16-T1
statement: >
  Leakage to a rank-k-budgeted adversarial reader depends on the record policy
  only through the revelation operator K = F'N^-1 F, and the minimal value cost
  of achieving K is exactly tr(S(I-K)S').
class: predicted
scope: >
  LQG disclosure game; Gaussian source; m >= n with S full column rank;
  singular K by epsilon-limit. Not claimed for m < n.
evidence:
  - registration: GO-P-2026-090        # sealed 3a74638, governed seed 20260822
  - result: results/go16-partition-verify-governed.json   # ALL PASS 9/9
  - machine_checked: lean/AdversarialObserver.lean        # 6 lemmas, 0 sorry
depends:
  uses:
    - OT-GO-11-KYFAN      # Ky Fan maximum principle (imported, classical)
  corroborates:
    - OT-GO-16-TWIN       # discrete twin, GO-P-2026-091
  cites:
    - OT-GO-13-THM1       # motivational only; no derivation depends on it
status: classified
history:
  - 2026-08-21: created, class=exploratory
  - 2026-08-21: R-IND-5 fresh-context verification, 7 findings, all addressed
  - 2026-08-22: promoted to predicted on governed run 090
```

## Appendix B — Checking a ledger (informative)

The reference validator implements P1–P4 and the blast-radius computation:

```
python tools/pe_lint.py --ledger <path> --level L3
python tools/pe_lint.py --ledger <path> --blast-radius OT-GO-16-T1
```

Its conformance report against the reference deployment is committed in
`case-studies/`.
