# Wiring the spine — the observation ledger's dependency graph

**Subject:** `geometric-observation` claims ledger (the Deployment A of the T-TS paper)
**Converted:** 2026-09-12, per [PE-BRW-1.0](../spec/PE-BRW-1.0.md) §5
**Occasion:** [PE-CLS-1.0 §9.1](../spec/PE-CLS-1.0.md) capped this ledger at L2,
because its markdown format has no field for a dependency edge and P4 was
therefore deciding an empty graph.
**Result:** **77 claim objects · 27 declared edges · edge coverage 0.078 ·
6 findings · and one gap in the specification that lands on the companion
paper's central claim.**

---

## 1. What was done

The markdown ledger stays where it is and remains the source. Nothing was
edited, no claim was re-derived, nothing was deleted. A native claim object was
written for each row into `ledger/claims/`, carrying the row's statement, its
class, its registration where the row names one, and its dependency edges.

Edges were generated as **candidates mechanically** — every mention of one
claim's identifier inside another claim's row, with 95 characters of context
either side — and then **adjudicated one at a time by reading the sentence that
produced them**. The sentence is stored on the object as `edge_provenance`. Type
adjudication was not automated, because §6.1 is explicit that a checker cannot
tell a load-bearing edge from a contextual one, and the whole value of the
exercise depends on not guessing.

52 raw candidates reduced to 25 after excluding self-matches inside a row's own
identifier cell. 27 edges were declared: **8 `uses`, 3 `corroborates`, 16
`cites`**. Script: [`../papers/tts/build/wire_spine.py`](../papers/tts/build/wire_spine.py).

## 2. Most of the first run was the converter's fault

Worth recording, because it is the normal shape of a conversion and a report
that omits it is not reproducible.

| run | errors | what they were |
|---|---:|---|
| first | 44 | 43 were mine |
| second | 12 | 6 were mine |
| third | **6** | the findings |

**Round 1 (43 spurious).** Every object was written `retrospective: true`,
reasoning that the edges were declared today. That is the wrong object: §4.3's
flag is about the *claim's* priority, not about when its edges were written, and
this ledger's claims are prospectively registered. Fixing the conflation removed
43 errors.

**Round 2 (6 spurious).** The registration detector matched `GO-P-2026-NNN` and
nothing else, so the entire OT crucible family — sealed before any test ran,
under `PREREG-OT*.md` — was reported as unregistered. **The ledger uses more
than one registration-naming scheme, and a reader keyed to one reports the other
as absent.** That is a defect in the reader, not the programme, and it is worth
stating because a conversion run by someone less familiar with the corpus would
have recorded six false accusations of missing priority.

The residue after both corrections is the finding set. A conversion that reports
its first run is reporting its author's unfamiliarity with the corpus.

## 3. The six findings

**3.1 Three claims assert priority without a registration.** `GO-EC-5`,
`GO-EC-6`, `GO-EC-7` are classed `predicted`. `predicted` asserts that the claim
was fixed before the test. Their rows name no registration under any of the
schemes in §2. Either a registration exists and the row does not cite it, or the
class is above what the record supports.

**3.2 Two verification incidents are classed as predictions.** `VI-10` and
`VI-13` are fresh-context verification records carrying class `predicted` with
no registration. The specification has `witness` and `revised` record classes for
exactly this kind of object, which carry no evidence grade of their own. This
looks like a class assignment that should be a record class.

**3.3 A support-cap violation that prose cannot show: `GO-12` over `GO-11`.**
This is the one worth the exercise.

```
[ERROR] P4 GO-12: class 'predicted' exceeds weakest load-bearing
        dependency 'GO-11' (replicated) -- support-cap violation
```

`GO-12` is `predicted`: registered in advance, so high on priority and moderate
on support. `GO-11` is `replicated`: high on support, lower on priority. Under
the §4.1 partial order neither dominates the other, and a claim may not outrank
what it rests on **on either axis**.

The content is not a bookkeeping quibble. `GO-12`'s row says the dynamic tax
"is GO-11's static quadratic with the substitution set by the encoder's access",
so `GO-12` rests on `GO-11` and inherits its standing. What the check says is
that **priority does not propagate upward through a dependency**: a claim
registered in advance, resting on a claim that was not, cannot carry its
registered status past the joint. That is a real and subtle property of the
evidence order, it is invisible in prose, and it is the kind of thing the ledger
exists to surface.

**3.4 Two claims carry a class the specification does not define.** `OT-9` and
`OT-10` are tagged `[refuted-as-sealed]` in the markdown. The token matches no
class in §4, so the markdown parser fell through to its default and read both as
**`exploratory`** — a live class — when the programme's own meaning is
**refuted**, which is terminal and suspends dependents. Nothing currently rests
on either claim, so no suspension was missed. The conversion maps both to
`refuted` and records the original token in `evidence.ledger_class_token`.

**3.5 The two front ends are exclusive, so nothing checks the whole ledger.**
`pe_lint` uses the native parser when it finds claim objects and the markdown
parser otherwise. This ledger now has native claims and a markdown registry
accounting table, and no single invocation reads both: run against
`ledger/`, P2 and P1 see zero registry rows; run against the repository root,
the 91-row accounting returns and the claim objects are ignored. Neither run
checks the ledger.

**3.6 A table header is a claim.** The markdown parser reads the `| Incident |
Verifier |` header of the verification table as a claim with id `Incident`.
It is one of the 78 claims every previous report of this ledger counted. The
conversion drops it; the true count is 77.

## 4. The graph

8 `uses` edges over 77 claims: **edge coverage 0.078**, six claims declaring a
dependency. Non-vacuous, so §9.1 is satisfied and P4 now decides something, but
low, and the reason is worth stating plainly: **the corpus's dependency
structure is mostly not written down anywhere.** Wiring from the ledger recovers
only the fraction that one row happens to mention in another row's prose. The
rest exists in the author's head and in the chapters, and recovering it is not a
conversion task.

Blast radius, computed rather than argued:

| claim | suspends | which |
|---|---:|---|
| `GO-1` | 2 | `GO-B-legal`, `GO-B-whale` — both instruments are GO-1's blind-probe read operator |
| `GO-11` | 2 | `GO-12`, and `GO-OP-077` transitively |
| `GO-12` | 1 | `GO-OP-077` |
| `GO-13` | 1 | `GO-OP-077` |
| `GO-2-POS` | 1 | `GO-OP-077` |
| `OT-2` | 1 | `OT-9` |
| `OT-3` | 1 | `OT-10` |

No claim in a terminal class has anything resting on it, so the ledger owes no
suspension it has not made. `GO-1` is the load-bearing root of the domain-transfer
bench, which matches what the corpus says about itself.

## 5. The finding that outranks the other six

**PE-CLS-1.0 gives claims a priority property and gives edges none.**

P1 requires a claim's registration to be a git ancestor of its result, and §4.3
caps a claim that cannot show it. There is no analogue for a dependency edge.
Nothing in the specification requires an edge to have been declared before the
test it bears on, nothing records when an edge was declared, and no check can
distinguish a graph wired in advance from a graph wired afterwards.

This conversion is the demonstration. **27 edges were declared today, into a
corpus whose results were all in, and the checker accepted every one without a
murmur.** The ledger moved from vacuous to non-vacuous and gained a real blast
radius, and none of that structure carries any evidence that it preceded the
results it organises.

That lands on the companion paper. [`../papers/kuhn/`](../papers/kuhn/) argues
that a claim ledger answers Feyerabend's objection to Lakatos — that
progressive-versus-degenerating is visible only in hindsight — because declaring
the dependency partition *before* the test makes the core/belt split a property
of the record rather than a reconstruction by someone with an interest in the
answer. The argument needs the edges to be prospective. **The specification
neither requires nor checks that**, so as written the answer to Feyerabend holds
for a discipline the specification does not yet describe. The paper's §7 now says
so.

**The fix, by analogy with a clause the discovery arm already has.**
[PE-DSC-1.0 §3.2.1](../spec/PE-DSC-1.0.md) faced the same problem for
transformation families and solved it: a late row is admissible as a backfill
when it carries the date it was written, names the sealed artifact holding the
real declaration, and shows that declaration preceding the result. Dependency
edges want the same treatment — `declared`, `entered`, `declared_in` — and blast
radius should then report the prospective subgraph separately, because that is
the only part of the graph Feyerabend's objection is answered by.

Not implemented here. It changes what every existing edge in both deployments
means, and after §9.1 that is a decision to make deliberately rather than in the
same sitting as the conversion that motivated it.

---

*Reproduce: `python papers/tts/build/wire_spine.py` then*
*`python tools/pe_lint.py --ledger C:\source\geometric-observation\ledger --level L3`.*
*The 77 objects are written into the `geometric-observation` working tree and are*
*uncommitted there; committing them is that repository's decision.*
