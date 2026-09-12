# PE-DSC-1.0 — The Transformation Registry Specification

**Philosophy Engineering · Discovery arm · Draft specification, version 1.0**
Andrew H. Bond · 2026-09-11

> **House rule.** A programme may not claim an invariance it did not declare a
> family for, and may not close a failure it did not reduce.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in *normative*
sections are to be interpreted as in RFC 2119. Sections marked *informative*
carry no conformance weight.

---

## 1. Scope

This specification defines a **transformation registry**: a versioned,
machine-readable declaration of the transformations under which a programme
claims its results survive, together with the tests it ran against them, the
reduced witness each failure produced, and the revision each witness forced.

It specifies the objects a conforming registry contains (§3), the outcomes a test
may carry (§4), the four checkable properties (§5), the protocol steps those
properties enforce (§6), and three conformance levels (§7). §8 records the
failure modes of the method itself.

This specification does **not** prescribe which transformations a programme
should declare admissible. That choice is the programme's, and making it
explicit, versioned, and contestable rather than objective is the entire point.
What is prescribed is that the choice be written down before the seal that tests
it, and that the record show what happened when it was tested.

## 2. Motivation *(informative)*

The judgment arm asks what an autonomous system may assert. The inquiry arm
(PE-CLS-1.0) asks what a research programme may assert. Both take an epistemic
norm and make it mechanically checkable. Neither covers the step in between,
which is what happens when a claimed invariance **fails**.

A programme that records only its verdicts records the least useful half of what
it learned. "The law did not transfer" names no cause and constrains no successor.
"The law's concentration term is a reciprocal, it diverges where the
tenth-neighbour concentration falls below 0.015, and removing the reciprocal
loses the real corpora the reciprocal is what fits" names a boundary of the
family's shape, and the next registration either carries a term that fixes it or
declares the scope. The second sentence is a **reduced witness**. It is the
object this specification exists to make mandatory.

Four objects of the discovery loop tend to live in prose, where the accounting
cannot see them.

1. The **transformation family** a claim was tested against. Without a record it
   is chosen after the result, and the objection that the theorist picked the
   class is unanswerable.
2. The **envelope** of what a claim survived, which is the comparative object.
   Two claims of comparable adequacy are ranked by their envelopes or not at all.
3. The **witness**, the reduced counterexample and the component that absorbs it.
   Without it a failure teaches nothing and the next attempt repeats it.
4. The **revised commitment**. Without a record of it, a programme can change
   what it believes in response to evidence and leave no trace that it did, which
   is indistinguishable in the record from never having been wrong.

This specification makes all four record types rather than prose.

## 3. Objects *(normative)*

A conforming programme MUST keep one registry per track or campaign, in a
version-controlled file under a declared path. The reference deployment uses
`claims/transformations/<TRACK>.toml`.

### 3.1 Registry header

Every registry MUST fix four things before any test is entered.

| Field | Meaning |
|---|---|
| `x` | the representation space the transformations act on |
| `y` | the output space, what a judgment or prediction returns |
| `equivalence` | the output equivalence and its tolerance, what "unchanged" means for `y` |
| `complexity_ordering` | the declared ordering over transformations a witness must be minimal under |

A registry without `complexity_ordering` cannot support a minimality claim, and
any witness it carries is a counterexample rather than a **boundary** witness.
The distinction is the whole content of Definition 4 of the discovery arm's
methodology paper.

### 3.2 Transformation

| Field | Meaning |
|---|---|
| `id` | `TRACK:slug`, unique across the programme |
| `family` | the transformations, in one sentence |
| `parameters` | the parameter set or ladder, or `none` |
| `closure` | what the family is closed under: composition, inversion, or `none` |
| `rank` | position in the complexity ordering, 1 the simplest |
| `declared` | the date the family was declared |
| `declared_in` | where the declaration is, when it is not this registry. Required on a backfill |
| `entered` | the date the row was written, when later than `declared`. Its presence marks a backfill |

`declared` MUST precede the seal of any registration that tests the family. This
is the discovery arm's analogue of PE-CLS-1.0 **P1**, and it is what the registry
buys. A family entered after a result is a family chosen to fit it.

### 3.2.1 Backfills

A registry can be late without its programme having been dishonest. The common
case is a family declared in a gate's own sealed registration and never mirrored
into the registry, so that tests cite a family the registry does not carry.

Such a row MAY be added afterwards, as a **backfill**, under three conditions,
all of which MUST hold and MUST be checkable by a third party.

1. The row carries `entered`, the date it was written, so that no reader mistakes
   it for a contemporaneous declaration.
2. The row carries `declared_in`, naming the sealed artifact that carries the
   real declaration, with enough identity to retrieve it: path, content hash, and
   the commit that sealed it.
3. That declaration demonstrably precedes the result. The seal commit is an
   ancestor of the commit that added the gate's result, and the sealed artifact
   still hashes to the recorded value.

If condition 3 cannot be shown, the row is not a backfill. It is a family chosen
to fit a result, and it MUST NOT be entered. Deleting the offending tests is also
not a repair, because removing the record of a test that ran is the file drawer
the inquiry arm's **P2** exists to prevent.

A conforming report MUST list backfilled rows rather than pass over them.
Backfilling is a repair of bookkeeping and never a repair of priority, and a
registry with many backfills is one whose programme is not writing declarations
down when it makes them.

### 3.3 Test

| Field | Meaning |
|---|---|
| `transformation` | the `id` tested |
| `claim` | the invariance claim in one sentence, the thing that survives or fails |
| `entries` | the entry identifiers the test bears on, possibly empty |
| `outcome` | one of the five in §4 |
| `record` | `repo/path:first-last` of the verdict, at the commit the registry names |
| `boundary` | for `boundary`: the parameter value at which the claim stops holding, and the tolerance |
| `witness` | for `failed` and `boundary`: the reduced counterexample |
| `absorbed_by` | for `failed` and `boundary`: which component absorbed the change |
| `revision` | the record of the revised commitment that followed, or an explicit `none` with its reason |

A test is entered when its verdict is committed, not when it is planned, except
for `predicted` (§4).

### 3.4 Absorbing component

`absorbed_by` MUST be exactly one of `representation`, `metric`, `constraint`,
`budget`, `dynamics`, `equivalence`, `declaration`, `measurement`.

The list is closed on purpose. A failure that absorbs into nothing on it has not
been reduced, it has been described. `measurement` and `declaration` are the two
that implicate the programme rather than the world, and a programme whose
witnesses never name either should be read with suspicion.

## 4. Outcomes *(normative)*

| Outcome | Meaning |
|---|---|
| `survived` | the claim held across the whole family within the equivalence tolerance |
| `failed` | it did not, with the witness saying where |
| `boundary` | the family has a parameter and the claim holds up to a measured value |
| `predicted` | the test is sealed and unrun |
| `proved` | the invariance is a theorem for the declared family, and the record is the proof |

`predicted` is the only outcome that MAY be entered before a run, and a registry
in which `predicted` rows never become anything else is a file drawer with extra
steps. A conforming programme SHOULD report the age of its oldest `predicted`
row.

`boundary` is not a weaker `survived`. A boundary row asserts two things, that
the claim holds inside the measured value and that it does not hold outside it,
and a programme that declares a scope MUST be able to show the second. The
reference deployment enforces this by requiring the out-of-scope error to exceed
the in-scope limit, failing the claim as stated otherwise. Without that second
clause a scope is a way of dropping the cases that fail.

## 5. The four checkable properties *(normative)*

### 5.1 D1 — Declaration

Every test's `transformation` MUST resolve to a transformation declared in the
same registry, and that transformation's `declared` date MUST precede the seal of
the registration the test records. A row bearing `entered` MUST satisfy §3.2.1,
and a conforming report MUST name it as a backfill.

*What it stops.* Naming the admissible class after seeing which transformations
the result survived.

*What it caught.* The reference programme's own OD registry declared four
families while its tests cited seven. Ten tests, entered over a single day of
gate records, named three families the registry had never carried. Every one of
the three was properly declared in its gate's sealed registration, before the
run, so nothing about the programme's priority was wrong. Only the registry was
late, and no amount of reading the registry had found that in two days. This is
the ordinary yield of the property. It catches bookkeeping, which is what
bookkeeping checks are for, and it distinguishes a late registry from a chosen
class, which is what §3.2.1 is for.

### 5.2 D2 — Reduction

Every test with outcome `failed` or `boundary` MUST carry a non-empty `witness`
and an `absorbed_by` from the closed list of §3.4. A programme that attempted
reduction and could not MUST say so in the `witness` field, and say what stopped
it. An empty witness on a failed test is a conformance error.

*What it stops.* Recording that something failed without recording what failed,
which is the ordinary way a programme learns nothing from its negatives.

### 5.3 D3 — Revision

Every test with outcome `failed` or `boundary` MUST carry a `revision` field.
It either cites the record of the revised commitment, which SHOULD be a `revised`
ledger row where the programme also runs an inquiry-arm ledger, or states
explicitly that no revision is registered and why.

Silence is the failure mode this property exists to catch. A programme that
revises a commitment in response to a witness and leaves no record has, in the
accounting, never been wrong.

*What it stops.* The last arrow of the loop going unrecorded.

### 5.4 D4 — Envelope

The registry header MUST fix all four fields of §3.1, every transformation MUST
carry a `rank`, and every `id` MUST be unique within the programme.

These are the conditions under which an **invariance envelope** can be generated
rather than written. An envelope is, for one entry, the transformations its
claims survived, the boundaries measured, the transformations failed with their
witnesses and absorbing components, and the transformations only predicted. It
MUST be generated from the registries and MUST NOT be hand-maintained. An entry
no test names prints `none declared`, which is an honest reading and not an
omission.

*What it stops.* An invariance claim in a paper citing a sentence rather than a
record.

## 6. Protocol steps *(normative)*

The four properties are checks. These are the four points in a programme's
workflow at which they bind.

1. **No registration claiming an invariance is sealed** without the family it
   claims it for already entered in the registry. (D1)
2. **A verdict of failure or indeterminacy is not complete** until its witness is
   recorded, or the record says reduction was attempted and what stopped it. (D2)
3. **A registration that supersedes another because of a witness** records the
   revised commitment before it is sealed. (D3)
4. **An invariance claim in a paper cites the envelope**, not a sentence, and a
   registry test names the entries it bears on so that the envelope can be
   built. (D4)

## 7. Conformance levels *(normative)*

| Level | Name | Requires |
|---|---|---|
| **D-L1** | Declared | §3 objects; a registry per track; **D1** and **D4** |
| **D-L2** | Reduced | D-L1 + **D2** on every failed and boundary test |
| **D-L3** | Closed | D-L2 + **D3** + generated envelopes published with the entries |

D-L1 is a file and an afternoon, and it already answers the objection that the
theorist chose the class. D-L3 is what a programme running sealed gates against
its own theory should target.

## 8. Failure modes of the method *(informative)*

**The registry becomes a formality.** Families are declared so broadly that
every result is inside one. The guard is `rank` and `complexity_ordering`, which
force the programme to say which transformations are simpler than which, and a
registry whose families are all rank 1 has declared nothing.

**The witness becomes a restatement.** "The law failed on heavy tails" in the
`witness` field satisfies D2 mechanically and reduces nothing. No check can
catch this. The reference deployment's practice is that a witness names a
mechanism and a number, and a reader can tell the difference.

**Scope creep as scope.** A boundary declared after seeing which cases fail is
the file drawer wearing a specification. §4's second clause is the guard, and it
is the one clause of this document that a programme is most likely to want to
drop.

**Reduction is expensive.** Reducing a failure often costs more than the run that
produced it. A programme under deadline will record verdicts and skip witnesses,
and D2 is what makes that visible rather than invisible.

## 9. Relationship to the other two arms *(informative)*

| Judgment arm (Foundation v1.0) | Inquiry arm (PE-CLS-1.0) | Discovery arm (this document) |
|---|---|---|
| Equivalence registry Γ, versioned | gap-free identifier registry with dispositions (**P2**) | transformation registry with declaration dates (**D1**) |
| Witness — minimal counterexample to an invariance claim | `refuted` row + verification incident | `witness` field + `absorbed_by` (**D2**) |
| Predict → test → revise, as professional norm | seal → govern → verdict → sealed revision act | `revision` field, and the `revised` class it cites (**D3**) |
| The per-judgment audit artifact | the per-claim ledger row | the per-entry invariance envelope (**D4**) |

The three arms are one rule at three levels. The judgment arm governs what a
system asserts about a case, the inquiry arm what a programme asserts about a
claim, and the discovery arm what a programme asserts about the transformations
under which its claims survive. Each turns a norm that was a culture into a check
that refuses.

## Appendix A — Minimal conforming registry (informative)

```toml
[registry]
track = "XX"
title = "one line"
x = "the representation space"
y = "what the judgment returns"
equivalence = "agreement within 1e-12"
complexity_ordering = "changes of observer first, then changes of world, then of scale"

[[transformation]]
id = "XX:observer-family"
family = "change of observer within the declared family"
parameters = "spectral exponent on the ladder 0, 0.5, 1, 2"
closure = "composition"
rank = 1
declared = "2026-09-01"

[[test]]
transformation = "XX:observer-family"
claim = "the measured quantity is unchanged across the observer family"
entries = ["xx-entry"]
outcome = "boundary"
record = "repo/experiments/XX/grade.json:1-40"
boundary = "holds to exponent 1.0, tolerance 0.05"
witness = "at exponent 2 the reader sees one direction and the quantity is undefined rather than changed"
absorbed_by = "budget"
revision = "none registered; a family with the degenerate reader removed is a change of declaration, not of claim"
```

## Appendix B — Checking a registry (informative)

```
tools/pe_lint.py --registry path/to/repo --level D-L3
```

The reference validator parses every `claims/transformations/*.toml` under the
given root and reports D1 through D4 with per-property verdicts, in the same
form as the ledger checks.
