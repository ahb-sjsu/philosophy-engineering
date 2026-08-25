# Case study — withdrawal, not refutation

**The episode that forced §4.2.** A claim was removed from a paper because its
evidence was invalid, not because the world contradicted it — and the distinction
turned out to matter in both directions.

---

## The claim

A KV-cache quantization study reported that its own method (asymmetric NF4)
degraded under long generation: LongBench `gov_report` ROUGE falling **13.7
points** at 512 generated tokens, with a monotone sweep across generation lengths
(gaps of 0.25 → 4.19 → 9.60 → 13.7 at 64/128/256/512 tokens) and a matching
12.1-point drop on a second model. The paper drew a general conclusion: *4-bit KV
quantization degrades under long autoregressive decoding, and the effect is
orthogonal to the codebook.*

The claim was load-bearing in a specific way worth noting: it was a limitation of
the authors' own method, reported against interest. That is normally a marker of
credibility, and it was one reason the result went unexamined for six weeks.

## The discovery

Re-validation using the same harness and the benchmark's own metrics ($n=40$ per
cell, both arms seeing identical documents) produced:

| cell | recorded gap | re-measured gap | verdict |
|---|---:|---:|---|
| gov_report, model A, 512 | 13.70 | **−0.31** | does not reproduce |
| gov_report, model A, 256 | 9.60 | **−0.05** | does not reproduce |
| multi_news, model A, 512 | 7.50 | **+0.51** | does not reproduce |
| gov_report, model B, 512 | 12.13 | **−0.83** | does not reproduce |
| multi_news, model B, 512 | 9.00 | **−0.35** | does not reproduce |
| gov_report, model A, 512, **symmetric** codebook | — | **+26.64** | reproduces |

Five of six cells vanish. The sixth — never part of the original claim — shows a
*larger* effect under a **different codebook**.

Root cause could not be pinned definitively (raw outputs from the original run
were never committed), but git history ruled out implementation drift, and the
recorded pattern is inconsistent with any single-codebook run of the committed
code. The most probable cause is **arm-label contamination** during off-repo
aggregation of two back-to-back sweeps whose tags differ by one character.

## Why this is `withdrawn` and not `refuted`

Under §4.2 the classes differ in what they assert about the world:

- **`refuted`** would mean: the method does *not* degrade under long generation,
  and we now have evidence for that negation.
- **`withdrawn`** means: we never had valid evidence either way. The claim
  returns to unknown.

The correct class is `withdrawn`. The re-validation used $n=40$ against the
original's $n=200$, on a subsample; it establishes that the recorded numbers do
not reproduce, not that the underlying effect is absent at every size. Recording
this as `refuted` would have manufactured a negative result out of a broken
instrument — an error in the opposite direction from the original, and equally
corrupting.

**The distinction had teeth.** The withdrawn claim's negation is not what the
data supports either. What the data supports is a *third* proposition: the long-generation
collapse is real but belongs to the **symmetric** codebook — which is the paper's
own headline finding, deepening under long decoding rather than a separate,
codebook-independent limitation. Had the row been marked `refuted`, that
proposition would have looked like a contradiction of the record instead of what
it is: the correct claim, recoverable only once the invalid one was cleared
rather than negated.

## Blast radius

The withdrawal's transitive closure over load-bearing edges:

| Claim | Edge to withdrawn row | Disposition |
|---|---|---|
| §5 "long-generation degradation is a general property of 4-bit KV quantization" | the claim itself | **withdrawn** |
| §5 "the effect is not GQA-specific" | `uses` | **suspended** — its entire support was the second model's row |
| §5 "mechanism is compounding error over decode steps" | `uses` | **suspended** — mechanism for a non-effect |
| §4 breadth aggregate (7-task average) | `uses` (two of seven cells) | **recomputed**: 37.3 → ~40.4 against fp16 ~41.2 |
| Limitations sentence citing §5 | `cites` | edited, not suspended |
| **§3 headline collapse result** | — | **untouched** |
| **§4 mechanism (representation × tolerance)** | — | **untouched** |
| **§5 RoPE-frequency structure of the offset** | — | **untouched** |
| **§6 machine-checked geometry** | — | **untouched** |

Four claims affected; four untouched and *named as untouched*. The paper lost a
section and kept its results.

## What the ledger method bought, concretely

1. **The error was findable.** The claim was a row with an instrument, a
   committed result file, and a re-runnable harness. Re-validation was a matter
   of executing the recorded configuration, not reconstructing an experiment from
   a methods paragraph.
2. **The correction was local.** Because the aggregate's dependency on the two
   bad cells was traceable, the fix was a recomputation, not a retraction of the
   paper.
3. **The correction improved the paper.** The withdrawn claim was a fabricated
   limitation of the authors' own method. Removing it left a *stronger* result:
   the method is near-lossless on all seven breadth tasks.
4. **The record survived the author.** The paper's source file, written a month
   before the re-validation, still contained the retracted section. What caught
   it was not memory but the ledger: the CHANGELOG erratum and the re-validation
   matrix were in the repository, and a review pass that read them found the
   inconsistency mechanically.

Point 4 is the argument for the whole method in one observation. **The author of
the paper and the author of the erratum were the same person, six weeks apart,
and the paper still shipped the retracted claim.** No amount of care substitutes
for a record that a checker can read.

## Specification consequences

This episode is the source of:

- **§4.2** (`withdrawn` ≠ `refuted`), including the requirement that a withdrawn
  claim's negation gain nothing;
- **§6.3**'s distinct propagation rules for the two cases — a claim depending on
  a *refuted* row must be re-derived or demoted; a claim depending on a
  *withdrawn* row is suspended and may be restored intact if the row is repaired;
- **§3.4**'s requirement that results be committed rather than described, since
  the un-committed raw outputs are exactly why root cause could not be pinned;
- **§8**'s requirement that a blast-radius report name the **untouched** claims
  explicitly, since that is the assurance a reader actually needs after a
  withdrawal.
