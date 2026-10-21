# K2 rubric v2: plan (DRAFT, 2026-10-21; nothing here is adopted)

What it would take to get a rubric that passes I1 (single-coder gate
ICC(2,1) ≥ 0.80 between independent coders, registration 7.2) without
measuring it on articles that shaped it. Every choice marked **Owner** is
open. Where this plan recommends one option, the recommendation is the
drafting session's, not a decision.

## 1. Where v1 left things

- **v1 failed on its held-out half** (registration 7.4.1): between-family gate
  ICC −0.31 (9 articles), gpt-oss against itself 0.22, minimax-m2 against
  itself −0.52. The revise half reached 0.61. Either v1 was fitted to the
  articles it was written from, or 9 to 11 articles are too few to tell; the
  pilot cannot separate the two.
- **A1 is the obstacle.** Held-out check agreement between families: A1 44%,
  A2 89%, A3 83%, A4 78%. gpt-oss agrees with itself on held-out A1 only 36%.
- **The 22 coded units are spent** as a test of any later version. They remain
  usable as material to revise from.
- **Defects to fix whatever is chosen:** a claim text named the replication
  project (DEV-ML-001, "Many Labs 1"), and gpt-oss then claimed to know the
  outcome; gpt-oss's quotes trace to the text in 203 of 238 cases even
  allowing for layout, after "quote exactly" (v1); minimax-m2 ran to its
  8,000-token limit on 37 of 82 tries (v0) and lost both codings of two units (v1).
- **Not yet run:** the planted-defect calibration (4.3 rule 1), the only check
  on whether agreeing coders are right, and the contamination probe (7.3).

## 2. The decisions

### D1 Articles to measure v2 on (Owner)

A fresh held-out set is needed; the question is where it comes from.

| Option | Pool | Cost and risk |
|---|---|---|
| (a) Closed-access development articles | 102 RP:P / Many Labs originals, through the SJSU library | Needs the owner's reading of the SJSU license for text-mining and model input; psychology only; the most famous replications, so recognition risk is highest |
| (b) Non-psychology supplement (7.1.1) | Draw from the 2,861 forecast-but-unreplicated SCORE phase-1 papers (claims in OSF d9x6s, not yet opened) | Fresh by construction and never replicated, so no outcome can leak; also fills the discipline gap 7.1 consequence 3 left open; open-access rate unmeasured; claim statements come in SCORE's own format |
| (c) Both | (b) as the held-out set, (a) or the spent 22 as revise material | Most work |

**Recommendation: (b), or (c) if the license allows.** (b) is the only pool
where the held-out articles cannot have a known replication outcome, and the
supplement is already registered as development data.

### D2 How large the held-out set must be (computed, then Owner)

9 to 11 articles could not distinguish a fitted rubric from chance. Before any
draw, a simulation (Atlas, not CPU 0, or NRP) should give, for a true
between-family ICC of 0.80 to 0.90, the number of double-coded articles at
which the 95% interval on the estimate is narrow enough to tell 0.80 from
0.60. The held-out size is then fixed from that number and committed before
the draw. No figure is given here because none has been computed.

### D3 Coders (Owner)

| Option | What it changes | Limit |
|---|---|---|
| (a) Same two families (gpt-oss, minimax-m2) | Nothing; comparable with v0 and v1 | Both are hosted aliases that cannot be pinned (4.3 rule 5) |
| (b) Several codings per family, averaged | Raises within-family reliability | Does not raise agreement between families (7.4.1), which is what I1 measures |
| (c) Add or swap a family | A third reading of the rubric | glm-5 and deepseek-v4-flash reasoned to the limit without answering; qwen3 took 5 to 20 min per answer |
| (d) Human coders | The design the registration was written for | None available (owner, 2026-10-19) |

Model calls go through the NRP ELLM gateway at no more than 2 at a time.

### D4 What to do with A1 (Owner)

| Option | Effect on the registration |
|---|---|
| (a) Rewrite A1.2 to A1.4 again | Keeps the gate 0 to 4; v1 already made A1.2 harder, not easier |
| (b) Keep A1.1 only in the gate (prediction stated before Results: closest to a locatable fact); A1.2 to A1.4 become reported secondary items | The gate still has four checks; A1 is narrower than PE-CLS §7.5 A1, which Section 12 must say |
| (c) Drop A1 from the gate (gate 0 to 3), report it separately | Changes the claim in Section 1: K2 then tests A2 to A4, not P5 as a whole |

**Recommendation: (b) for this round, with the narrowing stated in Section 12.**
It keeps the claim's shape and removes the items no coder pair has read the
same way.

### D5 Extraction before judgment (drafting change; Owner may veto)

Most A2 to A4 splits in v0 were about what an item covers, not about the text.
v2 could ask coders first for facts that can be checked against the article
(N recruited and analyzed per condition, exclusions and their reasons, the
focal outcome and its type, whether a manipulation check is reported and its
result, how many tests of the claim are reported), each with a quote, and then
derive the A2.1, A2.2, A3.1, A3.2, A4.1 to A4.3 and A4.5 scores from those facts
by rule in code. The judgment items (A2.3, A2.4, A3.3, A3.4, A4.4, and A1) stay
coder-scored. This is a change to the instrument, so it is piloted like any
other, and the derivation rules are frozen with the rubric.

## 3. Procedure, once D1 to D5 are settled

1. **Fix the known defects** (Section 1): target texts name no replication
   project; a recognition claim excludes the coding before scoring;
   minimax-m2's token limit raised or the family replaced (D3).
2. **Size the held-out set** (D2) and commit the size and the seed.
3. **Draw and split before reading anything.** The fresh pool is drawn by
   seed; the held-out articles are set aside unopened by anyone drafting.
   The spent 22 units, and any fresh revise articles, are the revise material.
4. **Write v2 from the revise material only**, each change tied to a dated
   finding as in v1's change table. No replication outcome is read
   (7.1 consequence 5); the supplement has none.
5. **Commit and hash v2 before the held-out coding starts**, and check the
   commit time against the first coding's time (the v1 commit missed by 12 s).
6. **Code the held-out set once.** Two families, two codings each, same
   settings as recorded in the commit.
7. **Read the result against the bar fixed in advance.** If the between-family
   gate ICC on the held-out set reaches the D2 criterion, run the
   planted-defect calibration (4.3 rule 1) before calling v2 ready to freeze.
   If it does not, v2 fails, the held-out set is spent like the last one, and
   the next step is an owner decision; no v3 is measured on the same articles.
8. **Record** in registration 7.4.2, with the result file committed and raw
   responses kept on Atlas.

## 4. What this plan does not settle

- Whether model coders can carry K2 at all. If v2 also fails on a properly
  sized held-out set, that is evidence they cannot on this rubric, and the
  remaining routes are human coders or a narrower claim.
- The contamination probe (7.3) and the I1 bar itself (0.80, from 7.2), which
  this plan takes as given.
- Ethics and compute sizing, which stay owner decisions.
