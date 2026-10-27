# K2 rubric v2: plan (DRAFT, 2026-10-21)

**Decided (owner, 2026-10-21): D1 (b), D2 n = 60 (go at ICC ≥ 0.73), D4 (b).**
D3 and D5 are open.

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

### D1 Articles to measure v2 on: DECIDED (b), owner 2026-10-21 (registration 7.1.1)

A fresh held-out set is needed; the question is where it comes from.

| Option | Pool | Cost and risk |
|---|---|---|
| (a) Closed-access development articles | 102 RP:P / Many Labs originals, through the SJSU library | Needs the owner's reading of the SJSU license for text-mining and model input; psychology only; the most famous replications, so recognition risk is highest |
| (b) Non-psychology supplement (7.1.1) | Draw from the 2,861 forecast-but-unreplicated SCORE phase-1 papers (claims in OSF d9x6s, not yet opened) | Fresh by construction and never replicated, so no outcome can leak; also fills the discipline gap 7.1 consequence 3 left open; open-access rate unmeasured; claim statements come in SCORE's own format |
| (c) Both | (b) as the held-out set, (a) or the spent 22 as revise material | Most work |

The drafting session recommended (b), or (c) if the license allows; (b) is the only pool
where the held-out articles cannot have a known replication outcome, and the
supplement is already registered as development data.

### D2 How large the held-out set must be (computed 2026-10-21; Owner picks n)

`k2_d2_sizing.py`, run on NRP (`k2_d2_nrp.py`: a timing Job, then one run Job,
exempt class), 4,000 draws per cell, seed 20261021, result
`k2_d2_sizing_result.json`. Model (an assumption, registration 7.2's): true
gate = Binomial(4, p) with p varying by article as in the k2_witness world;
each of two coders misreads each check independently with probability e,
calibrated so the population ICC(2,1) hits each target; a second set of cells
adds a bias (coder 2 turns a passed check into a failure 5% of the time),
which changed nothing that matters below.

**Spread of the estimate** (no bias; 95% of estimates fall in the range):

| Articles | true 0.60 | true 0.80 | true 0.85 |
|---:|---|---|---|
| 10 | 0.00 to 0.89 | 0.37 to 0.97 | 0.46 to 1.00 |
| 20 | 0.22 to 0.83 | 0.54 to 0.94 | 0.62 to 0.96 |
| 40 | 0.36 to 0.77 | 0.63 to 0.90 | 0.71 to 0.93 |
| 60 | 0.41 to 0.75 | 0.67 to 0.89 | 0.74 to 0.92 |
| 100 | 0.45 to 0.72 | 0.71 to 0.87 | 0.77 to 0.91 |

**A go rule.** Proceed with v2 if the held-out estimate reaches t_n, set so
that a rubric whose true ICC is 0.60 goes ahead only 5% of the time:

| Articles | t_n | go if true 0.70 | go if true 0.80 | go if true 0.85 | go if true 0.90 |
|---:|---:|---:|---:|---:|---:|
| 10 | 0.86 | 0.15 | 0.34 | 0.51 | 0.71 |
| 20 | 0.81 | 0.17 | 0.49 | 0.71 | 0.90 |
| 30 | 0.77 | 0.22 | 0.65 | 0.86 | 0.98 |
| 40 | 0.75 | 0.28 | 0.77 | 0.93 | 0.99 |
| 60 | 0.73 | 0.35 | 0.88 | 0.99 | 1.00 |
| 80 | 0.71 | 0.44 | 0.95 | 1.00 | 1.00 |

**What it shows.**

1. **v1's held-out half was too small to pass anything,** as feared: at 10
   articles even a rubric at true 0.85 clears the 5%-error bar half the time.
   It was not too small to fail, though: under this model, an estimate of
   −0.31 on 9 articles lies below the 2.5th percentile even at a true 0.60
   (0.00), so v1's result points to true agreement well under 0.60, not to
   bad luck. That sharpens 7.4.1 item 1, under this model's assumptions.
2. **Using 0.80 itself as the go bar is a coin flip** at a true 0.80 (51 to
   53% at every n), so the go rule needs a margin set from n, as above.
3. **About 40 held-out articles** (t = 0.75) go ahead 93% of the time at a true
   0.85 and 77% at 0.80, and 5% at 0.60. **About 60** (t = 0.73) raise those to
   99% and 88%. Telling 0.70 from 0.80 needs far more: at 80 articles a true
   0.70 still goes ahead 44% of the time. The held-out measurement can screen
   out a rubric that fails badly, not certify I1, which stays on the full run's
   double codes (7.2).
4. **Cost.** Each held-out article is coded four times (two families, two
   codings): 160 codings at 40, 240 at 60, at 30 to 50 s each through the
   gateway at 2 calls at a time. The draw has to be larger than n by the
   share of articles whose full text cannot be obtained, which is unmeasured
   for the supplement.

**DECIDED (owner, 2026-10-21): n = 60 held-out articles, go threshold
t = 0.73** (between-family gate ICC(2,1) on the held-out set; under the model,
go 5% of the time at a true 0.60, 88% at 0.80, 99% at 0.85). The seed is
committed with the draw frame (strata and the d9x6s source), before the draw.

### D3 Coders (Owner)

| Option | What it changes | Limit |
|---|---|---|
| (a) Same two families (gpt-oss, minimax-m2) | Nothing; comparable with v0 and v1 | Both are hosted aliases that cannot be pinned (4.3 rule 5) |
| (b) Several codings per family, averaged | Raises within-family reliability | Does not raise agreement between families (7.4.1), which is what I1 measures |
| (c) Add or swap a family | A third reading of the rubric | glm-5 and deepseek-v4-flash reasoned to the limit without answering; qwen3 took 5 to 20 min per answer |
| (d) Human coders | The design the registration was written for | None available (owner, 2026-10-19) |

Model calls go through the NRP ELLM gateway at no more than 2 at a time.

### D4 What to do with A1: DECIDED (b), owner 2026-10-21 (registration 4 and 12)

| Option | Effect on the registration |
|---|---|
| (a) Rewrite A1.2 to A1.4 again | Keeps the gate 0 to 4; v1 already made A1.2 harder, not easier |
| (b) Keep A1.1 only in the gate (prediction stated before Results: closest to a locatable fact); A1.2 to A1.4 become reported secondary items | The gate still has four checks; A1 is narrower than PE-CLS §7.5 A1, which Section 12 must say |
| (c) Drop A1 from the gate (gate 0 to 3), report it separately | Changes the claim in Section 1: K2 then tests A2 to A4, not P5 as a whole |

Chosen: (b). The gate's A1 is A1.1 only; A1.2 to A1.4 are scored and
reported as secondary items. The narrowing is stated in registration Sections
4 and 12.

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

## 5. Extraction design (2026-10-26)

Owner, 2026-10-26: "Research v2, and proceed with a new design more likely to
make actual progress." This section is that design. It answers D5 (extraction
before judgment) by making it the whole instrument, and it leaves D3 open with
a recommendation.

### 5.1 What the evidence says

Collected 2026-10-26 by a literature search; sources opened and numbers read
from them, except where marked.

- **Holistic quality judgments are unreliable for humans too.** Cochrane RoB 2,
  4 experienced raters on 70 trials: overall Fleiss κ 0.16, domains 0.04 to
  0.45 (Minozzi et al. 2020, J Clin Epidemiol 126:37,
  doi:10.1016/j.jclinepi.2020.06.015). ROBINS-I: overall 0.06 (Minozzi et al.
  2019, doi:10.1016/j.jclinepi.2019.04.001). Newcastle-Ottawa: from 0.68 on a
  factual item (follow-up length) to −0.06 on judgment items, total score 0.29
  (Hartling et al. 2013, doi:10.1016/j.jclinepi.2013.03.003). RoB 1: "agreement
  was poorer for those items that required more judgment" (Hartling et al.
  2009, BMJ 339:b4012). K2's 0.80 bar on a holistic gate is above what expert
  humans reach with these tools.
- **Rules raise agreement.** RoB 2 with a written rule for every signalling
  question: overall κ from −0.15 to 0.42 (Minozzi et al. 2022,
  doi:10.1016/j.jclinepi.2021.09.021). LLM judges: replacing Likert scores with
  yes/no checklist items raised Krippendorff's α across 12 judges from 0.09 to
  0.48 and 0.06 to 0.45 on two benchmarks (CheckEval, Lee et al., EMNLP 2025,
  arXiv:2403.18771). Counter-evidence: older LLMs answering RoB 2's signalling
  questions and applying its algorithm did no better than direct prediction
  (Šuster et al. 2024, doi:10.1002/jrsm.1749); decomposition helps only when
  the sub-questions are themselves low-inference.
- **LLMs extract facts well and judge quality poorly.** Data extraction: 96.3%
  accuracy on 160 elements, about 96% on two reruns (Gartlehner et al. 2024,
  doi:10.1002/jrsm.1710). RoB 2 judgments by an LLM: overall κ 0.22 against
  Cochrane authors, identical across 3 runs for 68 of 100 trials (Eisele-Metzger
  et al. 2025, doi:10.1017/rsm.2025.12). Explicit variables 92 to 93%, derived
  categories 64 to 80% (Schroeder et al., arXiv:2501.11840, a pilot on 8
  sources).
- **Agreement between two model families marks the reliable fields.** Fields
  where two LLMs agreed (87% of fields) were 0.94 accurate; fields where they
  disagreed, 0.41 to 0.50 (Khan et al. 2025, JAMIA, doi:10.1093/jamia/ocae325).
- **The gates' variance in SCORE's period.** Preregistration in social-science
  articles of 2014 to 2017: 0 of 156 (Hardwicke et al. 2020,
  doi:10.1098/rsos.190806). Manipulation checks: 33% of 614 psychology
  articles, 15 to 63% by journal (Hauser et al. 2018,
  doi:10.3389/fpsyg.2018.00998). 106 of SCORE's 164 replicated papers are
  outside psychology (Abatayo et al., SCORE credibility preprint,
  osf.io/preprints/metaarxiv/7u58q_v1, Table 2). So A1 will vary little, and A3
  will be not applicable for most claims.
- **The baselines are weak on SCORE.** In the same preprint (Table 3), original
  p-value correlates with replication at r = −.11 [−.26, .04] and original
  effect size at .01 [−.19, .18]. Registration 7.5 simulated power with a
  baseline AUC near 0.75. If B1 is that weak on SCORE, the simulated world is
  wrong about M0, and the power statement (7.5, I5) has to be redone; this
  design does not settle it.

### 5.2 The design

1. **Coders extract facts; code applies the rules.** [`RUBRIC-v2.md`](RUBRIC-v2.md)
   asks 17 factual questions (design, where the prediction is stated,
   registration, the outcome's type and source and reliability, manipulation
   check, sample flow, tests of the claim), each with a fixed answer set.
   [`k2_v2_rules.py`](k2_v2_rules.py) computes A1 to A4 from the answers; it is
   frozen and hashed with the rubric and tested case by case against the
   rubric's table ([`k2_v2_rules_test.py`](k2_v2_rules_test.py): 35 rule cases
   and 13 quote cases, PASS on Atlas 2026-10-26).
2. **Every positive answer carries an exact quote, checked in code.** A quote not
   found in the text the coder saw (after layout normalization) voids its
   answer, and a check that needs a void answer is U. This replaces "the
   adjudicator recodes a 1 without evidence" with a test anyone can rerun.
3. **Applicability is a coded fact.** Q1.1 decides whether A3 applies; Q3.1
   decides whether A2 applies. An observational economics claim is na on A3 by
   rule, not by a coder's reading.
4. **Reliability is measured per question first, then on the gate.** Between
   families, rep 1 ([`k2_v2_agree.py`](k2_v2_agree.py)). A question that two
   families do not answer alike on development units is rewritten or dropped
   before the commit; the gate ICC on the held-out set stays the go criterion
   (D2, 7.1.1: ICC ≥ 0.81 on the 18).
5. **The judgment items leave the gate** and are reported as out of scope
   (RUBRIC-v2 Section 3; registration Section 12 must say so).
6. **Development material.** The spent 22 psychology units, the 3 v2
   development papers, and, if more are needed, papers from the 235 undrawn
   eligible papers (165 published versions, 70 accepted manuscripts, 135 with a
   PDF link). The undrawn papers were never replicated, so no outcome can leak
   from them; the 22 have outcomes, and nothing here reads them.

### 5.3 Coders (D3, Owner)

The hosted aliases moved under the pilots: `minimax-m2` served
`MiniMaxAI/MiniMax-M2.7` through 2026-10-19 and `MiniMaxAI/MiniMax-M3.1-Flash`
on 2026-10-26 (7.4.2). Registration 4.3 rule 5 needs pinned revisions, which a
hosted alias cannot give. Two ways:

| Option | Pinned | Cost |
|---|---|---|
| Gateway families (gpt-oss plus one more), `model_returned` checked on every call and the run voided if it changes | No: recorded, not pinned | None; fast |
| Open-weight GGUF files on Atlas (Qwen3-32B Q5_K_M, gemma-4-31B Q5_K_M, Qwen2.5-72B Q5_K_M are on disk), run by llama.cpp with the file hash recorded | Yes, by sha256 | A GPU: GPU 1 had 24 of 32 GB in use on 2026-10-26, so a 32B model needs that load to move, or an NRP GPU Job |

Development rounds use the gateway (cheap, reversible). The held-out coding
should use the pinned option if it can be had; the owner decides.

### 5.4 Development rounds (2026-10-27)

Coders: gpt-oss (`openai/gpt-oss-120b`) and qwen3-small (`Qwen/Qwen3.8-27B-FP8`,
thinking off: 6 s a coding against 520 to 780 s with thinking, answers
otherwise alike). A trial on 2 units ruled out gemma (no answer on the
gateway, each try ended at 20 minutes), glm-5 (token limit), kimi (3 to 15
minutes a coding) and minimax-m2 (now MiniMax-M3.1-Flash, 1 to 4 minutes).
Every round: both families, two codings per unit, `k2_v2_agree.py`; codings
whose coder says it knows the replication outcome dropped (gpt-oss 4, qwen 1
in round 3, all psychology units).

| Between families, rep 1 | v2.0 (r1) | v2.1 (r2) | v2.2 (r3) |
|---|---:|---:|---:|
| Units | 24 | 23 | 25 |
| Gate ICC(2,1) | 0.51 | 0.51 | 0.43 |
| Exact gate agreement | 38% | 65% | 56% |
| Check agreement A1 / A2 / A3 / A4 | 63/50/38/63% | 78/65/48/65% | 76/76/72/68% |
| Within gpt-oss / within qwen3-small, gate ICC | 0.67 / 0.89 | 0.67 / 0.92 | 0.74 / 0.84 |

v0 and v1 on comparable units: 0.11 and −0.31 between families (7.4, 7.4.1).
In round 3 the factual questions agree at κ 0.66 to 0.84 (design 0.68, data
source 0.84, cited measure 0.66, manipulation check reported 0.67); the two
weak questions are Q2.1, where the prediction is first stated (κ 0.19; the
psychology units are cut to Method and Results, so the introduction is often
missing) and Q5.3, exclusions (κ 0.27).

**Reading.** Question-level agreement is now in the range the extraction
literature reports, and check-level agreement roughly doubled from v0, but the
gate ICC has not moved past about 0.5, against a go bar of 0.81 on the
held-out 18. Three things hold it down: residual splits on four checks compound
in the gate; most units score 0 or 1, and ICC is harsh when the true variance is
small; and gpt-oss is noisy against itself (0.67 to 0.74). These are 25
development units, most of them psychology units unlike the held-out set; only
6 are shaped like it (3 + 3 from the seeded draw of 60, of which 3 could be
fetched by script). The rounds were scored on the units they were revised on,
so they overstate what the held-out set would show.

**Options (owner).** (a) Keep revising Q2.1 and Q5.3 on development units. (b)
Each family codes three times and its answer per question is the majority,
which cuts gpt-oss's own noise; the between-family ICC is still what I1
measures. (c) Revisit the I1 bar: expert humans reach κ 0.16 overall on RoB 2
(5.1), and the 0.80 bar came from the 7.2 attenuation simulation, so an
alternative is to measure the instrument's reliability and correct the
estimate for it rather than gate on 0.80; a change to the registration's
design. (d) More held-out-shaped development units, which need the browser
fetch the owner found too laborious. The held-out 18 stay unread and uncoded.

**Option (b) tried (owner, 2026-10-27: "try (b), three codings per family").**
A third coding per family on round 3's 28 units, rubric and rules unchanged
(hashes checked against round 3's plan); each family's answer per question is
the value more than half its codings give, else void (`k2_v2_agree.majority`;
`k2_v2_dev_r3_maj_agree.json`). Gate ICC between families: single codings 0.43,
0.47, 0.39 (passes 1 to 3, 25 to 26 units); majority of 3: **0.34**. Exact gate
agreement 50 to 56% single, 42% majority. The majority does not help: the
families' disagreement is systematic (each reads some questions its own way,
consistently), not noise that voting cancels; questions with no majority turn
void and push checks to U. Q2.1 is the clearest case (κ 0.03 between the
majorities). (b) is not adopted. What would settle the systematic splits is
knowing which reading is right on each disputed question: a read of the
development units' evidence on the disputed answers, then a rule that says
which reading the rubric means.
