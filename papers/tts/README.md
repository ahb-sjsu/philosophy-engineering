# Checkable Properties for a Research Record

*A specification, a reference validator, and three defects it found that careful
reading did not.*

**Target:** IEEE Transactions on Technology and Society (quarterly, online-only,
rolling submission). Scope match: "the ethical, professional and social
responsibility in the practice of science, technology, engineering and
mathematics."
**Status:** draft, September 2026 · 7 pp IEEEtran two-column · 1 figure, 1 table
**Companion:** [`../kuhn/`](../kuhn/) — the theory half. See *The pair* below.

---

## The argument

Four assertions a research artifact normally makes on trust — we registered
before we measured, there is no file drawer, we do not assert beyond our
evidence, we know what depends on what — are restated as predicates over a
version-controlled record, decided by a 939-line checker, and run against two
live corpora that were not built for them.

**Three defects found, none visible to reading:**

1. **Twelve priority proofs destroyed by rebasing.** Commit hashes are the seal;
   rebase rewrites them. The written record stayed accurate throughout and the
   author had even noted the rebase, without noting that it had broken the proof.
   Forced a normative addition to the spec (§7.1.1). Remediation then found a
   *third* defect: disclosed post-seal amendments change the body and silently
   break the content hash.
2. **A correction with a blast radius of zero.** 87 occurrences rewritten, 2,126
   equations verified identical, and the published book now reads as though the
   stronger claim was never made. The zero *is* the finding. Argued in the paper
   as the most consequential result for research accountability, because no
   existing mechanism detects it — retraction notices cover withdrawn papers,
   version control records that text changed, and neither surfaces a thesis
   quietly weakened into invisibility.
3. **Results graded above their own declared dependencies.** Three claims graded
   as assumption-free while their dependency lists name modeling constructs.
   Acknowledged in the baseline with a named owner; the spec forbids the
   converter from deciding which half is wrong.

**And one defect in our own specification (§6), which is the paper's most serious
finding.** The validator certifies **L3** for Deployment A, but L3 exists for
dependency structure and that deployment's markdown format has no field for
dependency edges. Verified directly: 0 of 78 claims carry an edge, and
`parse_markdown_ledger` never assigns the field. So P4 passes over an empty
graph and blast radius is zero everywhere for a parsing reason. The sibling arm
of the same programme requires judgment procedures to prove non-degeneracy,
precisely because a constant function satisfies invariance vacuously. The record
spec imposes no such condition on itself.

**Fix implemented** (PE-CLS-1.0 §9.1, `check_p4` non-vacuity). L3+ now reports
edge coverage in every run, fails when no resolving `uses` edge exists, and caps
an edge-incapable storage format at L2. `--min-edge-coverage FRAC` enforces a
programme-declared floor; the spec sets no general value, because the defensible
one depends on how many claims are genuinely independent.

Verified outcomes after the change:

| ledger | before | after | edge coverage |
|---|---|---|---|
| geometric-observation (markdown) | CONFORMING L3 | **NON-CONFORMING L3 · CONFORMING L2** | 0.000 (0/78) |
| geometric-ethics (native) | CONFORMING L3 vs baseline | **unchanged** | 0.653 (154/236) |

Nothing about either programme changed. No scientific claim is affected. What
changed is that the report stops saying coherence was verified when what was
verified was an empty graph. `case-studies/conformance-geometric-observation.md`
supersedes its own L3 verdict in place rather than editing it, the way it already
kept its P1 failure analysis.

**Framing.** This is reported as a return, not a confession. A check that surfaces
something is a check working; a specification its own instrument could not catch
would be the worse object. The gap stood through a written conformance report and
a published case study because every reader checked whether P4 *passed* — whether
it had anything to pass *over* is a question a check answers in milliseconds and a
reading does not raise.

## §7: wiring a graph into Deployment A, and the bigger gap it found

The non-vacuity clause caps an edge-less format, so we gave Deployment A edges:
77 native claim objects, 27 declared edges (8 bearing weight, 3 corroborating,
16 contextual), edge coverage 0.078. Full write-up:
[`../../case-studies/wiring-the-observation-spine.md`](../../case-studies/wiring-the-observation-spine.md).

**Most of the first run was our error, which the paper reports.** 44 errors → 43
were ours (marked every claim retrospective when it's the *edges* that are).
12 → 6 were ours (registration detector knew one of the ledger's naming schemes,
so the whole crucible family read as unregistered). Residue: **6 findings**,
including `GO-12` `predicted` resting on `GO-11` `replicated` — a support-cap
violation whose content is that **priority does not propagate upward through a
dependency**. Also: two claims tagged `[refuted-as-sealed]`, a token the spec
doesn't define, silently read as the *live* class `exploratory` where the
programme means terminal; and a table header that has been counted as a claim in
every previous report (true count 77, not 78).

**The finding that outranks those six.** We declared 27 edges into a corpus whose
results were all in, and the validator accepted every one. **PE-CLS-1.0 gives
claims a priority property and gives edges none** — nothing requires an edge to
predate the test it bears on, nothing records when it was declared, no check can
tell a graph wired in advance from one wired afterwards.

That lands on the companion paper's central claim. Its answer to Feyerabend needs
the edges to be prospective; a top-level-conforming ledger may be wired entirely
in hindsight, and this one now is. **Kuhn §7 has been corrected** to state the
claim as what a ledger makes possible rather than what any deployment shows, and
the abstract now reports against itself on that point.

**Fix implemented** — PE-CLS-1.0 §6.4. Edge entries carry
`declared`/`entered`/`declared_in`, classify as prospective / backfilled /
retrospective / unrecorded, and blast radius reports the **prospective subgraph**
beside the full one. Errors on a backfill naming no declaration, and on an edge
entered before it was declared. Unrecorded edges are reported, not failed —
otherwise every converted corpus goes non-conforming at a stroke.

Populated from the record, not by assertion: each of the 8 edges was audited by
asking whether the source claim's **sealed prereg already names the target**.
Two do — and one of them is `GO-12`→`GO-11`, the edge behind the support-cap
violation, so that finding is **not** an artifact of wiring the graph today. The
programme committed in advance to GO-12 resting on GO-11 and the class assignment
has disagreed with that commitment ever since.

| refuting | strikes today | strikes on what the record fixed in advance |
|---|---|---|
| `GO-11` | `GO-12`, `GO-OP-077` | **`GO-12`** |
| `GO-1` | `GO-B-legal`, `GO-B-whale` | **`GO-B-whale`** |

Prospective fraction: **Deployment A 0.25, Deployment B 0.00** (all 196 of B's
edges unrecorded). Both stay as conforming as they were. What changed is that a
programme can no longer quote the full blast radius while claiming the warrant of
the prospective one, because the report prints both.

## The pair

| | Theory (`../kuhn/`) | Practice (this) |
|---|---|---|
| Venue | *Synthese* / *SHPS* | IEEE T-TS |
| Claim | PE is not a Kuhnian paradigm; the ledger answers Feyerabend's retrospectivity objection to Lakatos | Four properties are checkable, a validator decides them, here is what it caught |
| Evidence | **none, and says so** | two corpora, one figure, computed |
| Reviewers need | Kuhn, Lakatos, Feyerabend, Hart | git, CI, research software |

**Why this is a pair and not salami-slicing.** Each is incomplete in a way the
other names. The theory paper states five predictions and admits it cannot test
them; the practice paper supplies the first measurement of P-I. The practice
paper asserts four properties and does not argue why *these four*; the theory
paper does. Both now carry an explicit **Companion Paper** section saying what
the other does and that they are separable. That disclosure is the defense
against a salami charge, and it happens to be true.

**Submission order matters.** Practice first or simultaneous. If the theory paper
lands first it cites a companion that does not exist yet.

**The pair already corrected itself once.** P-I predicted blast radii "small and
right-skewed" and offered a discriminator: large radii concentrated on few
high-in-degree claims would indicate under-declaration rather than a real core.
The measurement came back right-skewed (75% zero, 85% ≤2, max 112) with the tail
on definitional claims — and the discriminator **does not discriminate**, because
a genuine foundational core and pervasive under-declaration produce the same
signature. The theory paper's §8 now records this as a defect in the prediction
rather than in the result. That exchange is the pair doing its job.

## Numbers, and where they come from

Every quantity is emitted by `build/blast_distribution.py` reading the live
ledgers. **None is transcribed from the case studies**, which have drifted:

| | case study (Aug 2026) | live (Sep 2026, used in paper) |
|---|---|---|
| brownfield claims | 234 | **236** |
| debt ratio | 0.962 | **0.958** |

Live figures used: 236 claims · 196 edges · 154/236 with ≥1 edge · mean blast
radius 2.771 · median 0 · max 112 · 75.0% zero · 84.8% ≤2 · max in-degree 33 ·
4 acknowledged cap violations · 4 warnings. Greenfield: 78 claims · 91 registry
rows 001–091 · 0 gaps · 4 void · P1 32/32 · P4 0 violations · P3 3 docs, 2
warnings.

Historical figures cited *as* historical (from the conformance and conversion
reports): 20 seals verified on first run, 1 stale, 11 non-resolving, 2
content-hash failures; 87 occurrences and 2,126 equations in the invisible
retraction; 5 suspended / 135 untouched in the symmetry-group case; 81 untagged
results, 49 wired, 29 dangling.

## Build

```bash
python build/blast_distribution.py     # -> build/blast_distribution.json
python build/fig_blast.py              # -> build/fig_blast.{pdf,png}
PDFLATEX="/c/Users/abptl/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe"
"$PDFLATEX" -interaction=nonstopmode checkable_records.tex   # twice
pandoc checkable_records.tex -o checkable_records.docx --resource-path=".;build"
```

Regenerate the figure before any resubmission — the ledgers are live and the
numbers move.

## Finalization checklist

- [x] Abstract narrative, zero math
- [x] Banned-word grep clean (one hit, `load-bearing`, removed)
- [x] No em-dashes in prose; no colored text; no undefined refs
- [x] Every number from a script reading the live record, not from the case studies
- [x] Figure caption states the takeaway, both panels
- [x] Negatives disclosed (§8): two corpora one author, discovery-arm checks fail, P2 bounded by identifier-space origin, L4 not claimed, deployments not comparable
- [x] Prior art credited before novelty claimed (§9)
- [x] AI-use disclosure included
- [x] Companion sections added to **both** papers
- [ ] **Verify on final:** Merton reprint pagination (`% verify` mark in the `.tex`)
- [x] §6 fix implemented (spec §9.1 + `check_p4`); both ledgers re-run; case study superseded in place
- [ ] Owner submits. Not submitted, posted, or emailed.
