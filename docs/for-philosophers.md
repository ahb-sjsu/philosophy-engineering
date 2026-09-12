# Philosophy Engineering — an introduction for philosophers

*Informative. Written for readers who know the philosophy and not the code.*

Philosophy Engineering is the practice of taking a philosophical commitment and
building a machine that refuses to violate it.

The interesting part is not the machine. It is what happens to the commitment
when you try. A norm that survives ordinary philosophical scrutiny — stated
carefully, defended against objections, taught for decades — will usually not
survive the demand that it be *checkable*. Something in it turns out to be
underspecified in a way that matters, or to require a distinction nobody had
drawn, or to be satisfiable by a system that obviously does not satisfy it. That
residue is the discipline's real output, and it is philosophical work that cannot
be done from the armchair alone, because the armchair never forces the question.

So this is not a proposal to replace philosophy with computation, and it is not
an ethics-consulting arrangement in which philosophers supply values and
engineers supply implementations. It is a claim that **implementability is a
source of philosophical evidence** — that trying to make a norm mechanically
enforceable tells you things about the norm that you cannot learn any other way.

---

## 1. A distinction that turned out to be load-bearing

Start with a small case, because it shows the shape of the work better than any
manifesto.

A paper in our own programme reported that its method degraded under long
generation: a 13.7-point benchmark drop, monotone across four generation lengths,
replicated on a second model. It was reported *against interest* — a limitation
of the authors' own technique — which is normally a credibility marker, and is
one reason it went unexamined for six weeks.

Re-validation found that the effect in five of six cells did not reproduce at
all. The most probable cause was label contamination between two sweeps whose
tags differ by one character.

Now: what should the record say? The obvious answer is *refuted*. It is the wrong
answer. "Refuted" asserts something about the world — that the method does *not*
degrade, and that we have evidence for the negation. We have no such evidence.
The re-validation ran at n=40 against the original's n=200. What we have is a
broken instrument, and the correct verdict is **withdrawn**: we never had valid
evidence either way, and the claim returns to unknown.

Recording it as `refuted` would have manufactured a negative result out of a
broken instrument — an error in the opposite direction from the original, and
equally corrupting. And the distinction had teeth. The data actually supported a
*third* proposition, which became visible only once the bad claim was cleared
rather than negated.

That is a piece of ordinary conceptual analysis — the difference between *not-p
is supported* and *p is unsupported* — and it is now a normative clause in a
specification, with defined propagation behavior through a dependency graph
([PE-CLS-1.0 §4.2](../spec/PE-CLS-1.0.md)). It was forced by an engineering
situation that would not accept a vague answer. Philosophers make distinctions
like this professionally. Most of them never get to find out which ones were
load-bearing.

The full case is in [`case-studies/kv-longgen-withdrawal.md`](../case-studies/kv-longgen-withdrawal.md).

---

## 2. The core move: from norm to predicate

The discipline's central technique is monotonous and, once seen, hard to unsee:

1. Declare an equivalence relation over representations — what counts as **the
   same case**.
2. Declare the invariances — **what must not matter**.
3. Implement something that enforces them (canonicalization, a quotient, an
   equivariant architecture).
4. Package the evidence as a machine-checkable artifact.

Applied to judgment, this yields the **Epistemic Invariance Principle** (EIP): a
judgment procedure must give equivalent outputs for representations that are
equivalent under a declared transformation group.

The *norm* here is not new, and the framework does not pretend otherwise. It is
visible in the identity of indiscernibles read contrapositively (a procedure that
distinguishes indiscernibles is treating non-properties as properties); in the
verificationist claim that statements with identical verification conditions have
identical meaning; in the pragmatist maxim; and in universalizability, since a
procedure yielding contradictory verdicts under admissible redescriptions of one
situation cannot be consistently universalized. In philosophy of mind it has a
cleaner name: representation dependence is a **failure of intentionality**. The
system is responding to the representation rather than to what the representation
is about. Kahneman and Tversky's framing effects are empirical demonstrations
that human cognition violates EIP routinely.

Three things are added by making it a predicate rather than a principle:

- **Falsifiability.** "Judge the case, not the wording" is aspirational.
  *For all x and all admissible transformations τ, J(x) and J(τx) must be
  equivalent* is a claim a test suite can refute.
- **Localizability.** When it fails, you do not get "the model is biased." You get
  a **witness** — a minimal transformation that flips the verdict. A
  counterexample, produced automatically, with the property that removing any part
  of it makes the failure go away. This is the single most useful thing the
  formalism gives you, and it is what turns a complaint into a bug report.
- **Non-triviality.** A constant function satisfies EIP perfectly and is useless.
  So compliance requires a paired **non-degeneracy** condition: the procedure must
  still distinguish genuinely different cases. Invariance without discrimination
  is not rigor; it is silence. Any formalized norm needs its own version of this
  check, and most proposals lack one.

That third bullet is where formalization usually earns its keep. The degenerate
satisfier is invisible in prose and unmissable in code.

---

## 3. What applied ethics gets: the accountability theorem

The second principle is the one I would most like philosophers working in applied
ethics to attack, because if it holds it changes how ethics review can be
conducted.

Separate two things that ordinary moral judgment fuses:

- **Bonds** — the objective relational structure of the case. Who stands in what
  relation to whom; what obligations, dependencies, powers, and vulnerabilities
  obtain. (The deontic vocabulary here is Hohfeld's: right/duty,
  liberty/no-right, power/liability, immunity/disability.)
- **Lens** — the evaluative framework. Value commitments, weightings, thresholds,
  lexical priorities, risk tolerances. Versioned. Hashed. Declared before use.

The **Bond Invariance Principle** requires that transformations preserving bond
structure must not change the verdict. From which the **Accountability Theorem**:

> If two judgments differ, the difference is attributable to exactly one of —
> the bonds differ, the lens differs, or both. There is no fourth option.
>
> **Corollary.** Any challenge to a judgment reduces to exactly two questions:
> *Is the bond extraction correct?* (factual) and *Is the lens appropriate?*
> (normative).

The corollary is the payload. Most disputes about an automated decision are
currently unstructured: the complainant cannot tell whether the system got the
facts wrong, applied the wrong values, or simply responded to the phrasing. The
third possibility contaminates the other two — it is why "the algorithm is
biased" arguments so often fail to converge. Eliminate representational artifacts
by construction, and every remaining disagreement is forced into one of two
buckets, one of which is squarely the philosopher's.

**Normative theories become lenses, not competitors.** A consequentialist lens
weights aggregate outcomes; a deontological lens installs hard constraints as
inviolable boundaries; a virtue lens weights agent dispositions; a care lens
weights relational dependency and vulnerability. The accountability guarantee
holds for *any* lens. Disagreement between them is legitimate normative
disagreement, now cleanly separated from representational noise.

This is a substantive metaethical position and you may well reject it. But notice
what it makes possible: a lens is a file. Here is a real one, abridged, from the
`erisml-lib` reference implementation:

```json
{
  "name": "Jain-1",
  "principlism":   { "beneficence": 0.32, "non_maleficence": 0.34,
                     "autonomy": 0.11, "justice": 0.23 },
  "risk_attitude": { "appetite": "risk_averse", "max_overall_risk": 0.2 },
  "override_mode": "rights_first",
  "lexical_layers": [
    { "name": "rights_and_duties",
      "principles": ["autonomy", "rights", "rule_following_legality"],
      "hard_stop": true }
  ]
}
```

That is principlism with the weights written down, a lexical priority made
explicit, and a version number. You can disagree with every figure in it — which
is the point. Currently, two clinicians who disagree about a case argue about the
case. With lenses, they can run the *same* case through *both* declared
frameworks and find the precise point of divergence, or discover that their
frameworks agree here and the disagreement was actually factual. Comparative
normative ethics becomes something you can run.

I am not claiming the numbers are right. I am claiming that a normative
commitment specific enough to be wrong is worth more than one general enough to
be unobjectionable.

---

## 4. The reflexive turn: governing a research programme

Here is the move that made this a question about paradigms rather than about
technique.

Philosophy Engineering says: take an epistemic norm and make it mechanically
checkable. Apply that to *science's own* epistemic norms — priority of
registration, absence of a file drawer, not asserting beyond your evidence — and
you get a **claim ledger**: a repository in which every claim is an individually
versioned, independently classified, dependency-tracked object, with the norms
enforced by a linter rather than by professional trust.

The diagnosis is that four familiar pathologies are *structural* rather than
cultural — consequences of publishing monolithic PDFs:

1. **Granularity mismatch.** The unit of publication (the paper) is not the unit
   of truth (the claim). A paper with nine sound results and one bad lemma has no
   way to express that state.
2. **All-or-nothing retraction.** Because the artifact is indivisible, correcting
   one lemma means retracting everything bundled with it — so the incentive is to
   correct nothing. *Retraction burns the tree to prune a branch.*
3. **Uncomputable blast radius.** Nothing records what *depends* on the bad lemma.
   "What else falls?" is answered by memory and rereading.
4. **The file drawer is unobservable.** Absence of a result is invisible by
   construction.

Four properties convert norms usually asserted on trust into predicates:

| | The norm | The predicate |
|---|---|---|
| **P1 Priority** | "we registered before we measured" | the seal commit is a **git ancestor** of the first commit adding the result |
| **P2 Completeness** | "no file drawer" | the identifier sequence is **gap-free**, every ID resolving to a disposition |
| **P3 Authority** | "we don't assert beyond our evidence" | no document cites a claim **above its class** |
| **P4 Coherence** | "we know what depends on what" | every dependency resolves; no claim outranks its weakest support |

P2 is the one I would put in front of a philosopher of science first. "We report
everything" is the paradigm case of an unfalsifiable meta-claim: it quantifies
over an unobservable set. Make identifier assignment *contiguous*, and require
every identifier — including the abandoned, the void, and the never-run — to
carry a disposition, and the claim becomes a property of a finite list that
anyone can verify in seconds. An unfalsifiable norm becomes a finite check. That
transformation is the discipline in miniature.

The ancestry is explicit and, where borrowed, credited ([PRIOR-ART.md](../PRIOR-ART.md)):
Popper on falsifiability, applied at the level of the *record* rather than the
theory; Merton's norms, two of which P1–P4 attempt to mechanize; Ioannidis on the
file drawer's contribution to the literature's error rate. The closest ancestor
is Lakatos. His distinction between a programme's hard core and its protective
belt — and the observation that refutations usually strike the belt — is what
**blast radius** computes. The dependency graph *is* the core/belt distinction,
and graph traversal replaces the historian's retrospective judgment about which
was which. What the specification adds is the requirement that the distinction be
declared **in advance**, rather than reconstructed after the refutation by an
author with an interest in the answer.

Duhem–Quine sets the honest limit: the specification can localize a refutation
only to the extent that the conjunction was written down beforehand. Undeclared
dependencies remain the method's blind spot, and the spec says so.

A third arm, **discovery**, governs what a programme may claim *survives*: which
transformations a claim was actually tested against. Its fourth property has no
analogue elsewhere and is the one I find most uncomfortable — **D3 Revision**
requires that when a claimed invariance fails, the record cite the commitment you
revised in response, or state that none was registered and why. Without it, a
programme can change its mind under pressure of evidence and leave no trace that
it did, *which in the accounting is indistinguishable from never having been
wrong.*

---

## 5. What I am not claiming, and where you should push

The house rule is *a programme may not assert what its ledger cannot show*, so:

**The framework does not choose the invariances.** It provides the machinery for
declaring and enforcing a transformation group; it is silent on which
transformations *ought* to be declared irrelevant in a given domain. That is a
philosophical judgment, and it is listed as Known Limitation #1 in the Foundation
document. It is a gap in the theory, and it is precisely the kind of gap only
philosophical work closes.

**The meta-problem is unsolved.** Who decides which invariances to declare? This
is governance, not mathematics. The reference implementation is called a
*democratically governed* ethics module engine, and I think that word is
currently doing more work than it has earned. I would like a political
philosopher to tell me so in detail.

**Natural-language equivalence is not decidable.** Paraphrase equivalence is
approximated by a classifier. There is a theorem bounding the resulting
compliance error, but the bound is only as good as the classifier, and the whole
edifice rests on that joint.

**"Computational objectivity" is the most contestable thing in the corpus.** The
claim is that objectivity requires not a transcendent origin but *mathematical
inevitability under constraint* — as a droplet is spherical not by decree but
because the sphere minimizes surface energy. I find it compelling. I am also
aware that it is the sort of claim that looks strongest to the person who thought
of it, and that a metaethicist will spot the move it is making faster than I
will. It needs a competent adversary more than it needs another sympathetic
reader.

**The formalism reaches past its evidence in places, and the corpus says where.**
One example, because it is the honest kind: Hohfeld's four relations, together
with the correlative and negation operations, generate the Klein four-group V₄.
That much is demonstrated. The larger dihedral group D₄ is *posited* as an
ambient structure and would require quarter-turn operations to be independently
exhibited as genuine normative operations. They have not been. The gap is stated
in the document rather than papered over — and finding more gaps like it is
useful work.

**The programme has recorded its own falsifications.** An SU(2) gauge structure
was refuted by CHSH-style tests (N=600); a predicted obligation-hysteresis effect
was not confirmed and reversed under double-blind conditions (N=630); a predicted
schism effect had, in the corpus's own words, "zero confirmations and was
falsified on the best-powered instrument available." Each was reported in the
section where it was found. None had its blast radius computed, because the
dependency records did not exist yet — which is exactly the pathology the ledger
arm was built to fix, discovered in my own work.

**The checks are not currently clean.** Running the discovery-arm validator on
the reference programme fails: ten tests cite three transformation families the
registry never declares. The interesting part is what happened next. The
specification could not tell an honest late row from a dishonest one, so it now
says when a backfill is admissible — it must carry the date it was written, name
the sealed artifact holding the real declaration, and show that the declaration
preceded the result — and when it is instead a family chosen to fit a result,
which may not be entered at all. A conformance report that passes on its first
run is usually measuring the wrong thing.

---

## 6. How philosophers get involved

Five tracks, roughly by increasing commitment. Each produces something that is
simultaneously a philosophical result and a runnable artifact — which is the
point, and also, I think, the recruiting argument: this is a way to do
philosophical work that has a second life.

**(a) Declare a transformation group for a domain you know.**
Pick a domain — clinical consent, employment discrimination, research ethics
review. Answer, carefully: which redescriptions of a case *must not* change the
verdict, and which *must*? Passive voice? Party names? Order of disclosed facts?
Currency units? The boundary is not obvious, and the interesting cases are the
near-misses, where a redescription that looks purely formal turns out to carry
morally relevant information. Output: a declared group with a written defense,
plus an adversarial test suite. This is Known Limitation #1, and it is a paper.

**(b) Write a lens — then run it against a rival.**
Take a normative framework you know deeply and specify it precisely enough to be
versioned and executed: weights, lexical priorities, hard stops, thresholds. Then
run the same case set through yours and through an opposing lens, and find where
they actually diverge. My expectation — worth testing — is that rival theories
agree far more often than their literatures suggest, and that the genuine
divergences cluster somewhere unexpected. If that is right it is a finding about
normative ethics. If it is wrong, that is a finding too.

**(c) Be the adversary.**
The programme runs adversarial fresh-context verification: someone who has not
seen the reasoning tries to break the claim. Philosophers are professionally
trained at exactly this and are systematically underused for it. Find the
degenerate satisfier. Find the case where the equivalence relation is wrong. Find
where a specification's clause is satisfiable by something that obviously fails
its intent. Low commitment, immediate value, and every witness you produce goes
into the record with your name on it.

**(d) Audit the metaethics and the governance.**
Sections 3 and 5 above, taken seriously. Is the bond/lens separation coherent, or
does bond extraction smuggle in evaluation? (I think it partly does; I would like
to know how much.) Is "computational objectivity" a real position or a relabeled
constructivism? What makes a declared invariance *legitimate* — and by what
procedure, binding on whom? These are the hardest questions here and the ones I
am least equipped to settle alone.

**(e) Teach it.**
The lowest-friction and possibly highest-value option. A course unit in which
students take one principle — informed consent, the doctrine of double effect,
Rawlsian fair equality of opportunity — and try to make it checkable. They will
fail in instructive ways, and the failures are the curriculum: what they discover
is that the principle they could recite was not specified well enough to apply.
Students hit the underspecification in week two, which takes philosophers a
career of careful reading to notice and engineers no time at all to trip over.
The implementation repository has open student tasks and a community set up for
this already.

---

## 7. Where to start reading

Roughly forty minutes, in order:

1. This document, then the [repository README](../README.md) — the three arms and
   how they relate.
2. [`case-studies/kv-longgen-withdrawal.md`](../case-studies/kv-longgen-withdrawal.md)
   — five pages, and the fastest way to see the method do real work.
3. [Foundation v1.0](../foundation/), the sections on EIP and BIP — the formal
   core, with proofs. The Values-tier knowledge areas (metaethics, normative
   ethics, epistemology, philosophy of mind, political philosophy) are written for
   you, and are where the framework is thinnest.
4. [PE-CLS-1.0](../spec/PE-CLS-1.0.md) §7 — the four properties, if the
   philosophy-of-science arm is what interests you. Read
   [PRIOR-ART.md](../PRIOR-ART.md) first if you want to know what is borrowed
   before you learn what is claimed.
5. The implementation — [`erisml-lib`](https://github.com/ahb-sjsu/erisml-lib) —
   if you want to see a lens actually run.

---

*The discipline's house rule, applied to itself: **a programme may not assert what
its ledger cannot show.** If you find this document asserting something the
repository cannot show, that is a finding, and it is the kind I most want.*

— Andrew H. Bond · Department of Computer Engineering, San José State University
· andrew.bond@sjsu.edu
