# Philosophy Engineering Is Not a Paradigm

*A test against Kuhn's criteria, and a present-tense answer to Feyerabend's
objection to Lakatos.*

**Status:** draft, September 2026 · 12 pp · ~5,350 words body
**Evidence class:** `exploratory` — see §10. No document in this corpus may cite
its thesis above that class (PE-CLS-1.0 P3).

---

## What the paper argues

The claim tested is the one the programme's author has made in conversation and
correspondence: that Philosophy Engineering is a new paradigm for science in
Kuhn's sense. The paper runs Kuhn's own criteria against the programme and
**rejects the claim**. Three findings:

1. **Community fails decisively.** Kuhn's unit of analysis is a community of
   practitioners. One author, a department, a few students and a chat server is a
   position, not a disciplinary matrix.
2. **The anomaly cannot generate a crisis.** Kuhn's crises require a paradigm to
   fail *by its own standards*. Representation dependence does not make a model
   fail its benchmark — accuracy is computed against one fixed encoding per case
   and never presents the alternative. The reigning instruments do not score the
   defect as a failure; they do not see it. That is the wrong shape for a
   Kuhnian crisis, and the point is derived from the *strongest* card in the case
   for.
3. **The translation procedure is counter-evidence.** PE-BRW-1.0 is a specified,
   executed algorithm for carrying a legacy corpus into the ledger with its
   standing intact. Kuhn says no such algorithm exists between paradigms. Either
   the corpus and the ledger are not separated by a revolution, or Kuhn is wrong
   about incommensurability. The first is far more likely. PE is a **conservative
   extension** of ordinary scholarship.

What survives is smaller and better supported: Lakatos's core/belt partition was
attacked by Feyerabend for yielding verdicts only in hindsight, and the objection
holds because ordinary records never fix the partition in advance. P1 (priority
by repository ancestry) and P4 (declared dependencies) make it a property of the
record, so **"what does this refutation strike?" acquires a present-tense
answer.** That is a contribution to the appraisal of research programmes, not a
revolution.

§8 states four falsifiers (P-I blast-radius shape, P-II negative-result rate,
P-III loss of discontinuity in revision, P-IV declared vs. retrospective
partition). P-IV is cheap and runnable on the existing corpus today.

## Why the thesis is not the one that was requested

A paper straightforwardly asserting "PE is a new paradigm" would violate the
programme's own house rule and would be dismissed by the audience it is meant to
reach. The steelman for the original claim is preserved in full as §4; §5 is what
happens when it is tested. Reverting to the affirmative thesis means keeping §4
and discarding §5–§6, which is a smaller edit than it looks.

## Prior art checked before any novelty claim was written

| Source | What it owns | Consequence for this paper |
|---|---|---|
| Vazire (2018), credibility revolution | Reform of evidentiary standards as a discipline-wide change; the literature's own verdict that it is **reform, not a Kuhnian paradigm shift** | §6's conclusion is *not original*. Credited, not claimed. |
| Feyerabend (1975); SEP *Lakatos* | The retrospectivity objection itself | §7's problem statement is borrowed. Only the mechanism answering it is claimed. |
| Horstmeyer (2023), *Lakat*, arXiv:2306.09298 | Lakatos-inspired CI publishing, p2p, Proof-of-Review consensus | Adjacent. Concerns publishing governance, not programme appraisal. Distinguished in §9. |
| Nanopublications; micropublications; Manubot | Claim-level granularity, argumentation graphs, versioned manuscripts | Already conceded in `PRIOR-ART.md`; restated in §9. |
| Bowker & Star (1999); Leonelli (2016); Hacking (1992); Galison (1997) | Infrastructure and styles as non-theory scientific change | The category §6 places the inquiry arm in. |

**Residue claimed:** declaring the dependency partition before the test, plus
priority by ancestry, converts core/belt from retrospective reconstruction into a
property of the record, answering one standing objection to Lakatos. No prior art
located for that specific move.

## Negatives disclosed in the paper

Per house rule 4, all of these are in §10 rather than a memory hole:

- n=1; the author is the subject; confirmation risk is severe and irreducible from inside.
- The discovery-arm checks **do not pass** (ten tests citing three undeclared families), left unrepaired because backfilling is what D1 forbids.
- P2 completeness is bounded by identifier assignment, and that boundary is set by the person the property constrains.
- Three recorded falsifications (SU(2)/CHSH N=600; obligation hysteresis N=630; ERT schism) had **no blast radius computed**, because the dependency records did not exist yet.
- The paper is itself unregistered, uninstrumented, and unverified in fresh context.

## Build

```bash
PDFLATEX="/c/Users/abptl/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe"
"$PDFLATEX" -interaction=nonstopmode kuhn_paradigm.tex   # twice, for refs
pandoc kuhn_paradigm.tex -o kuhn_paradigm.docx --resource-path=".;build"
```

Outputs: `kuhn_paradigm.pdf` (12 pp), `kuhn_paradigm.docx`.
`lmodern` is required — without it microtype's font expansion aborts the build.

## Finalization checklist

- [x] Abstract narrative, zero math (`awk '/begin{abstract}/,/end{abstract}/' | grep -c '\$'` → 0)
- [x] Banned-word grep clean (one hit, `genuinely`, removed)
- [x] No em-dashes in prose (`grep -- "---"` → empty)
- [x] No colored text (`grep -nE "textcolor|\\color\{|\\hl\b"` → empty)
- [x] No undefined citations or references in pass 2
- [x] Prior-art search run **before** the novelty claim in §9 was written
- [x] Negatives disclosed (§10)
- [x] AI-use disclosure included
- [x] Every corpus figure checked against the repository (234 claims, debt 0.962, N=600, N=630, ten tests / three families)
- [ ] **Verify on final:** Feyerabend chapter/pages for the rhetoric charge; Kuhn (1974) page range; SEP *Lakatos* authorship and edition year — all three carry `% verify` marks in the `.tex`, which must not be silently removed
- [ ] Venue not yet chosen. Candidates: *Synthese*, *Erkenntnis*, *Studies in History and Philosophy of Science*, *Philosophy of Science*
- [ ] Owner submits. Not submitted, posted, or emailed.
