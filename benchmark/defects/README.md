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
| Corpus + seeded: caught | 22 |
| Corpus + seeded: broken | 0 |
| Corpus + seeded: gaps | 7 |
| External entered | **24** (target 20) |
| External the spec can express | **16 of 24** |
| ... of which mechanically checkable | 4 (multiplicity, null-data witness, priority, power) |

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
| DB-022 | Raw inputs behind an aggregate result | A result manifest of hashed, committed inputs |
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

**Not yet done:** the K-1 exit's held-out test, in which a reader who did not
build the benchmark classifies the external entries from the entries alone. The
`spec_gate` values above are the author's classification, which is exactly what
that test is meant to check.
