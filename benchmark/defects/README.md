# The defect benchmark

Stage K-1 of [`docs/kuhnian-path.md`](../../docs/kuhnian-path.md). Kuhn's
paradigm in the narrow sense is the **exemplar**, the solved problem people
learn by doing. This is the exemplar library: defects this programme actually
committed, each with its source, how it was found, what refuses it, and the
minimal repair.

```
python benchmark/defects/run.py          # table
python benchmark/defects/run.py --json   # machine-readable
```

Run it on Atlas, not the laptop. It imports `tools/pe_lint.py` and needs `git`.

## How an entry is graded

Every entry records two things separately:

- **detected by**: what actually found the defect (a derivation, a cold reread,
  a placebo run, the linter, a reader).
- **enforced by**: the `pe_lint` property that refuses the *recorded* defect, or
  `none`.

For the design defects (DB-001 to DB-007), the audit detected the defect and
`pe_lint` only enforces that a recorded failure cannot stand under a promoted
claim. The benchmark does not pretend the linter found them.

An enforced entry carries a **defective** and a **repaired** fixture, built in a
temporary directory at run time. It is `CAUGHT` only if the expected finding
fires on the defective fixture *and* nothing fires on the repaired one. The
second condition is the benchmark's non-vacuity: a check that refused everything
would pass the first. An entry with no enforcing check is a `GAP`, a finding
about the specification, and stays in the benchmark.

## State, 2026-10-17

| | Count |
|---|---:|
| Entries | 53 (26 corpus, 3 seeded, 24 external) |
| Caught (fixtured entries) | 26 |
| Broken | 0 |
| Gaps (corpus) | 6 |
| External entered | **24** (target 20) |
| External the spec can express | **20 of 24** after P6 and the A1/A4 amendments (16 before; 14 by the held-out reader's reading of the pre-change spec) |
| Inexpressible | 4, all fabrication (LaCour, Hwang, Stapel, Shu et al.), disclaimed in s7.6.1 |

**Two gaps were closed the day the benchmark was built**, which is what it is
for:

- **DB-026** was *found* by the benchmark. A fixture written with the outcome
  `fail` (PE-DSC-1.0 §4 says `failed`) produced no finding, because D3 silently
  skipped any outcome outside its set. A misspelled failure needed no revision.
  `pe_lint` now refuses outcomes outside §4.
- **DB-015** (`[refuted-as-sealed]` read as a live class) is now refused on
  native objects: a class outside §4 is an error, never a default.

Neither change altered the verdict on any live corpus (geometric-observation,
geometric-ethics, the OD registries).

## Open gaps

| Entry | What is not checked | What would check it |
|---|---|---|
| DB-009 | A registration's content hash after a post-seal amendment | Hash the blob at the seal commit; amendments in a separate dated file |
| DB-010 | A claim's meaning changed with no version bump (the orphan correction) | Claim semantic versioning (kuhnian-path I-3) |
| DB-016 | A report's claim count against an independent count | Two counts per report, fail on disagreement |
| DB-023 | Withdrawn vs refuted | Nothing mechanical: a recorded human decision |
| DB-024 | A campaign summary against its registrations | Generated, never typed, accounting |
| DB-025 | Prose claiming a status change the ledger never made | P3 over all narrative files, claim-state phrases resolved to history |

## The K-1 falsifier, first reading (2026-10-17)

*Registered question:* can the specification express defects from outside the
author's corpus, or does it only see its author's own kind of error?

24 documented defects from neuroscience, machine learning, economics, physics,
cosmology, microbiology, genomics, psychology, toxicology and political science
were entered from primary sources (verified citations; partial verifications
are marked in the entry). External entries are **classified, not fixtured**:
each names the spec gate that could express it, or `none`.

**16 of 24 are expressible.** The falsifier is not triggered. Most land on A2
(selection and evaluation on the same data: Vul, Kriegeskorte, Kapoor &
Narayanan, BICEP2) and A4 (flexibility: Reinhart-Rogoff, power posing,
Simmons et al.). Eklund et al.'s cluster failure is A1's witness record exactly:
null data run through the grading pipeline.

**But 12 of the 16 are judgment, not computation.** The linter enforces a
recorded verdict; a coder has to reach it. That is what the K-2 rubric is for,
and it means the benchmark's strength here is the rubric's reliability, which
is not yet measured.

**8 of 24 are inexpressible, in two families:**

1. **Fabrication (5):** LaCour, Surgisphere, Hwang, Stapel, Shu et al. Every
   record property presumes the record is honest. Priority, completeness and
   admissibility of invented data all pass. This is a limit to state in every
   presentation of the method, not a gap to close with another check.
2. **Data integrity (3):** spreadsheet row offsets (Baggerly & Coombes), gene
   names converted to dates (Ziemann et al.), reported statistics that are
   impossible (van der Zee et al.). These *are* mechanically checkable (input
   manifests, type schemas on data files, consistency checks of reported test
   statistics against their degrees of freedom and N), and the specification
   has no property for them. Together with DB-022 (raw inputs never committed),
   they are the case for a sixth property. **Owner decision.**

**Follow-up the same day.** The data-integrity family became **P6 Integrity**
(PE-CLS-1.0 s7.6, required at L4): I1 hashed input manifests (with a rule for
restricted data), I2 typed and keyed data files with a spreadsheet-coercion
check, I3 recomputed p-values, possible degrees of freedom, and GRIM. DB-022,
DB-X14, DB-X18 and DB-X21 now carry fixtures and are CAUGHT; DB-X09 is
expressible only in part (I2 shows a key exists, not that the analysis joined by
it). Surgisphere moved from fabrication to provenance: P6 refuses data no
independent party can examine, which is not the same as showing data genuine.

## Held-out test, first run (2026-10-17)

Record: [`heldout-2026-10-17.json`](heldout-2026-10-17.json); score it with
`python benchmark/defects/score_heldout.py benchmark/defects/heldout-2026-10-17.json`.

A fresh-context agent (same model family as the author, so partial independence
only, s10.6) was given the two specifications as they stood at `ce252fa` and the
24 external entries with the author's classification removed, and nothing else.

| | Agreement |
|---|---:|
| Expressible or not | 22/24 (92%) |
| Primary gate, exact | 20/24 (83%) |
| Gate, counting secondaries | 22/24 (92%) |
| Mechanical / judgment / none | 17/24 (71%) |

The plan's K-1 exit asked for 80%; this clears it, with the caveat that the
reader was a model, not a person. **Both expressibility disagreements ran the
same way: the author over-credited the specification, and the reader was right.**

- **DB-X03** (dead salmon): A4 had no multiplicity rule. The author had credited
  it from the rubric, not the spec.
- **DB-X04** (cluster failure): A1 required one witness record, and a 70%
  false-positive rate is a property of a distribution.

Both were fixed in s7.5 the same day (A1 witness distribution, A4 multiplicity
rule, rubric item A4.5), and are reported here rather than absorbed. A human
reader remains the real test.
