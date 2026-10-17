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
| Entries | 29 (26 corpus, 3 seeded) |
| Caught | 22 |
| Broken | 0 |
| Gaps | 7 |
| External | **0 of 20** (the K-1 exit requires 20) |

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

## The K-1 falsifier

If entries from outside the author's corpus cannot be caught by any check
expressible in the specification, the method only sees its author's own kind of
error. The 20 external entries are the test of that, and none is in yet.
Sources and rules for entering them are in `entries.json` under `external`.
