# Conformance report — Observation Theory ledger

**Ledger:** `geometric-observation` (the Observation Theory evidence ledger)
**Checked:** 2026-08-25 · `tools/pe_lint.py` at L3 · raw output:
[`conformance-geometric-observation.txt`](conformance-geometric-observation.txt)

> **Status: REMEDIATED, same day.** The P1 failure described below was fixed by
> re-anchoring, not by editing this report. Final verdict:
> **CONFORMING at L3** — P1 32/32, P2 91 rows gap-free, P3, P4 clean. The
> failure analysis is retained in full because it is the report's most useful
> content and because deleting it would violate the specification it tests.

| Property | Verdict (as found) | Verdict (after remediation) | Detail |
|---|---|---|---|
| **P2 Completeness** | **PASS** | **PASS** | 91 registry rows, range 001–091, **0 gaps**, 4 void-with-reason |
| **P1 Priority** | **FAIL (1 error, 11 warnings)** | **PASS (32/32)** | 32 seals checkable; 20 verified initially, 12 recovered by re-anchor |
| **P4 Coherence** | **PASS** | **PASS** | 78 claims, 0 support-cap violations, no dependency cycles |
| **P3 Authority** | **PASS (2 warnings)** | **PASS (2 warnings)** | 3 narrative documents scanned |

## What passed, and why it matters

**P2 is the headline.** The ledger's "no file drawer" claim is not a promise
here; it is a checkable property of a finite list, and it checks. Every
identifier from 001 to 091 resolves to a disposition, including the four that
carry no result: two never assigned (proven absent from the full history), one
void reservation abandoned pre-seal, and one identifier burned by a design
failure its own pilot caught. **A programme that hides a failed run under this
regime must either leave a visible hole or write a false disposition.** That is
the strongest form the guarantee can take, and the reference deployment holds it.

**P4 passed with zero support-cap violations** — no claim in the ledger holds a
class stronger than its weakest load-bearing dependency. Given that the ledger
was built before this specification existed, that is evidence the underlying
discipline was already sound rather than evidence that the checker is lenient.

## What failed — and the specification change it forced

**P1 failed, and the failure is instructive because the written record is
honest.** Three groups:

1. **20 seals verify.** `git merge-base --is-ancestor <seal> <result>` returns
   true. Priority proved mechanically.
2. **One seal resolves but fails ancestry** (row 068, seal `50a1ffe`). The
   registry row *itself* says `sealed 50a1ffe→rebased 078687e`. Checking the
   rebased hash: ancestry holds. So the priority was real, the author recorded
   the rebase, and only the machine check failed — on a stale identifier.
3. **Eleven seals do not resolve at all** (rows 076–086). The commits named no
   longer exist in the repository. These are the GO-14 block, sealed during a
   period when the author was pushing from multiple machines with
   rebase-on-pull.

The cause in cases 2 and 3 is the same and it is not dishonesty: **rebasing
rewrites commit hashes, and a recorded seal hash is a reference to an object that
rebasing destroys.** The priority was genuine in every case; the *evidence for it*
was collateral damage from ordinary version-control hygiene.

This produced a normative addition to the specification, **§7.1.1**:

- a conforming ledger MUST NOT rewrite history containing seal commits;
- registrations MUST carry a content hash independent of commit identity, so a
  rewritten ledger can be re-anchored;
- a rewritten seal MUST record the old→new mapping in its row;
- a non-resolving seal without such a mapping is a **failure**, not a warning —
  a claim whose priority cannot be checked is a claim whose priority is unproven.

**This is the report's most useful outcome.** A checker that only confirmed what
the author already believed would have taught nothing. This one found a defect
that prose had absorbed silently — the registry's own "→rebased" note shows the
author noticed the event but not that it had broken the proof — and the fix is a
protected branch plus a content hash, not a change to any scientific claim.

## Remediation — done, and what it found

The fix was to stop failing, not to soften the report.

1. **Re-anchored 12 rows** (`scripts/reanchor_seals.py`). For each orphaned
   seal the script recovers the current commit identity from the prereg file
   and refuses to write unless three things hold: the content hash still
   matches under the repository's *own* sealing scheme, the commit is the first
   that added the prereg, and it is a git ancestor of the result commit. All
   twelve verified on ancestry. Rows now read
   ``sealed <old> (rebased; current commit `<new>`)`` — the historical hash is
   never deleted.
2. **A third finding fell out of it.** Two rows (079, 081) failed the
   content-hash check. Investigation showed both carry **dated, disclosed,
   post-seal amendments** appended to the prereg body — permitted by the
   protocol and honestly recorded. Appending them changed the body, so the
   seal hash stopped verifying. That is a specification gap, not misconduct:
   PE-CLS-1.0 required amendments to be dated and reasoned but said nothing
   about what they do to the content commitment. Those rows are re-anchored
   with an explicit `content hash superseded by disclosed post-seal
   amendments` note, and the correct general design — sealed body immutable,
   amendments appended as separately hashed records — is now stated.
3. **Made the failure unrepeatable.** `.githooks/pre-rebase` refuses any rebase
   over a range touching `prereg/`, naming the reason and the recovery path;
   `core.hooksPath` is set.
4. **Closed the deeper gap.** `scripts/anchor_seal.py` anchors a seal's
   *content hash* to a third party (RFC 3161, or OpenTimestamps for an
   authority-free proof). Ancestry proves order; an anchor proves wall-clock
   time to a stranger. See §7.1.2.

**Result: CONFORMING at L3** (P1 32/32, P2 gap-free, P3, P4 clean).

L4 additionally requires fresh-context verification records and machine-checked
cores as first-class ledger objects. Both exist in this deployment (R-IND-5
passes; Lean developments with zero `sorry`) but are recorded in prose rather
than as linked objects, so L4 is not claimed.

## What the exercise demonstrates

The report's value was never the passing rows. A checker that only confirms
what its author already believes teaches nothing. This one found three real
defects — destroyed seal identities, an unhandled interaction between
amendments and content hashes, and an unclosed gap between ordering and
timestamping — in a programme whose written record was accurate throughout.
Every one was invisible to a careful human reader and obvious to a linter.

## Warnings worth reading, not fixing blindly

Two P3 warnings flag narrative documents citing registrations whose class sits
outside the declared umbrella policy (`proved`/`replicated`/`predicted`):
`ch11` citing a `demonstrated` row, and `OBSERVATION.md` citing an `exploratory`
one. Both may be legitimate — the citation may be contextual rather than
load-bearing, which is exactly the `uses`/`cites` distinction of §6.1 that the
markdown front end cannot see. **They are warnings precisely because the checker
cannot tell**, and resolving them requires either a human reading or migration to
native claim objects that declare the edge type.

That limitation is itself informative: it is the concrete cost of running the
specification against a ledger that predates it.
