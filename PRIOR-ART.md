# Prior art and positioning

*Companion to PE-CLS-1.0. Informative.*

A specification that does not say what already exists is not a specification, it
is an advertisement. Almost every component of PE-CLS-1.0 has been proposed
before, several of them decades ago and better funded. This document names them,
says what is borrowed, and states precisely what is left over.

---

## 1. The philosophical ancestors

**Popper (1934/1959), *The Logic of Scientific Discovery.*** Falsifiability as
the demarcation criterion. §3.1's requirement that a `statement` be falsifiable
*as written* is Popper applied at the level of the record rather than the theory.

**Lakatos (1970), "Falsification and the Methodology of Scientific Research
Programmes."** The direct ancestor of this specification's central promise.
Lakatos distinguishes a programme's **hard core** from its **protective belt** of
auxiliary hypotheses, and observes that a refutation ordinarily strikes the belt,
not the core — so a programme survives by modifying auxiliaries rather than
collapsing. PE-CLS-1.0's blast radius (§8) is Lakatos made computable: the
`uses` graph *is* the distinction between core and belt, and traversal replaces
the historian's judgment about which is which. What the specification adds is
that the distinction must be declared **in advance**, not reconstructed after the
refutation by an author with an interest in the answer.

**Duhem–Quine.** No hypothesis is tested in isolation; a failed prediction
indicts a conjunction. This is exactly why undeclared dependencies (§10.3) are
the method's blind spot: the specification can only localize a refutation to the
extent that the conjunction was written down beforehand.

**Merton (1942), the norms of science** — communalism, universalism,
disinterestedness, organized skepticism. §7's four properties are an attempt to
make two of these (communalism, organized skepticism) mechanically checkable
rather than professionally exhorted.

**Ioannidis (2005), "Why Most Published Research Findings Are False."** The
quantitative case that the file drawer and analytic flexibility dominate the
literature's error rate. P2 targets the first; §3.2's bar-and-power requirement
targets the second.

## 2. Registration and priority

**Registered Reports** (Chambers, *Cortex*, 2013–) and the preregistration
movement more broadly (Center for Open Science; AsPredicted; ClinicalTrials.gov,
mandatory since 2007). These establish the norm PE-CLS-1.0's P1 enforces, and
they do it at scale in real journals. Two differences: registries are *external
services* (the researcher trusts a third party's timestamp), and registration is
*per-study*, not per-claim with a dependency graph.

**What PE-CLS-1.0 changes.** Priority is proved by **repository ancestry** rather
than by a registry's timestamp — no third party, verifiable from any archived
copy, and checkable by anyone with the repository. §7.1.1 records the cost of
this choice: ancestry is fragile under history rewriting in a way a timestamp
service is not. Neither approach dominates; they compose.

## 3. Claim-level publication — the closest prior art

**Nanopublications** (Groth, Gibson, Velterop 2010; Mons et al.). The proposal
that the smallest publishable unit be a single assertion with its provenance,
identified by URI and machine-readable. This is the same granularity move as
PE-CLS-1.0 §3.1, made fifteen years earlier and with a proper RDF serialization.

**Micropublications** (Clark, Ciccarese, Goble, *J. Biomedical Semantics*, 2014).
Argumentation graphs for scientific claims: claims linked to evidence, methods,
and to each other by support and challenge edges, building on Toulmin's argument
model. This is the same dependency move as §6, again earlier, and with a
better-developed formal semantics for *support*.

**Research Objects** (Bechhofer, De Roure, Goble). Bundling data, methods, and
provenance as a citable unit.

**These three are the works PE-CLS-1.0 most resembles, and any presentation of
this specification that does not cite them is misrepresenting its novelty.**

**What is left over.** Nanopublications and micropublications solve *granularity*
and *linkage*. They do not address:

- **Completeness (P2).** Neither has a mechanism making the *absence* of a claim
  observable. A nanopublication registry is a set of things that were published;
  it is silent about what was not.
- **Priority (P1).** Provenance records *who asserted what*; it does not
  establish that a prediction preceded its test.
- **Authority (P3).** Neither constrains what a *narrative* document may assert
  relative to the claims it cites.
- **Class demotion and propagation (§6.3).** Micropublications have challenge
  edges; they do not define what a challenge *does* to the class of a dependent
  claim, nor distinguish refutation from withdrawal (§4.2).

## 4. Versioned and executable scholarship

**Manubot** (Himmelstein et al., *PLOS Comp. Bio.*, 2019) — manuscripts as
git repositories with continuous integration. The infrastructure model
PE-CLS-1.0 assumes. Manubot versions the *document*; this specification versions
the *claims inside it*.

**Executable papers**: Jupyter, Whole Tale, Code Ocean, ReproZip. These target
result reproducibility, which is §3.3–3.4's concern. L4 conformance essentially
requires an executable-paper substrate.

**Semantic versioning; dependency resolution (npm, Cargo, Maven); deprecation
policy; CI.** The engineering ancestors of §5, §6, and §9. The specification's
entire structural argument is that these solved, for code, the problem the
literature still has for claims. No originality is claimed for the machinery —
only for its target.

## 5. Machine-checked mathematics

**Lean 4 / Mathlib**, Coq, Isabelle; **Formal Abstracts** (Hales) — the project of
making theorem *statements* machine-readable and individually addressable;
**QED-style library curation**, where a library-wide refactor propagates through
a dependency graph and the build tells you exactly what broke.

Mathlib is the existing system closest to PE-CLS-1.0's ideal, and it is worth
being blunt about this: **a proof assistant's library already implements §6 and
§8 perfectly, for the fragment of claims that are formalizable.** Change a lemma,
and the compiler names every downstream consequence — blast radius, computed
exactly, for free. PE-CLS-1.0 is in large part an attempt to extend that
discipline to *empirical* claims, where no compiler exists and the dependency
edges must therefore be declared by hand and checked by convention. L4's
requirement to machine-check formalizable cores is the acknowledgment that where
a compiler *can* do this work, it should.

## 6. Adversarial and independent verification

**Red teams; adversarial collaboration** (Kahneman); **replication initiatives**
(Reproducibility Project: Psychology, 2015; Many Labs); **peer review** itself.
§3.5's fresh-context verification is a lightweight, in-programme version of
adversarial collaboration, with the specific requirement that the verifier not
share the author's working context.

**What is added:** verification is a *lifecycle stage with a recorded artifact*,
including null findings and the scope of the search, rather than an event that
either happens privately or produces an unpublished referee report.

## 7. Blockchains: run none, borrow one

Various proposals exist for putting scientific records on distributed ledgers.
The distinction PE-CLS-1.0 draws (§7.1.2) is between **operating a chain** and
**anchoring in one that already exists**, and it goes in opposite directions.

**Operating a chain: rejected.** A blockchain solves consensus among mutually
distrusting writers over shared state. A claim ledger has exactly one writer and
needs a timestamp. Running a chain would add key management, governance, and
availability obligations while providing nothing the alternatives below do not,
and describing a git-backed registry as a "cryptographic ledger" overstates what
it guarantees.

**Anchoring in one: endorsed, and it is the strongest option.**
[OpenTimestamps](https://opentimestamps.org) (Todd) aggregates a hash into a
Merkle tree and commits the root to Bitcoin — you run nothing, hold nothing, pay
nothing, and the resulting proof depends on *no authority at all*. That is a
better trust model than an RFC 3161 Time-Stamp Authority, which is in turn
better than an archival deposit, which is what most programmes have.

The honest framing is that these are **timestamping** technologies, and the
literature on them long predates blockchains: Haber & Stornetta's 1991 "How to
time-stamp a digital document" is the origin of both the Merkle-chain
construction and, by a well-known lineage, of Bitcoin's own design.
Certificate Transparency (Laurie et al., RFC 6962) and
[Sigstore/Rekor](https://www.sigstore.dev) are the modern software-supply-chain
descendants and are equally usable here.

So: the gap ancestry leaves open (§7.1.2 — order but not wall-clock time) is
real, and closing it is cheap. It just is not a job for a chain of one's own.

## 8. The residue

After the concessions above, what PE-CLS-1.0 contributes is:

1. **P2 as a checkable no-file-drawer proof.** Contiguous identifier assignment
   with mandatory disposition of every identifier, including the void and the
   never-run. This converts the one unfalsifiable sentence in a typical paper
   into a finite enumeration. I am not aware of prior art for this specific
   move, and it is the component I would defend first.
2. **P3, the assertion-authority separation.** Narrative documents hold no
   independent authority to assert; they are views over the ledger, and the
   citation policy is a predicate over classes, checkable by parsing.
3. **`withdrawn` ≠ `refuted` with distinct propagation** (§4.2, §6.3) — a
   distinction forced by a real episode, not by taxonomy for its own sake.
4. **The partial order over classes** (§4.1): evidence classes vary along
   *support* and *priority* independently, so citation policy cannot be a rank.
5. **The conjunction, operated at scale.** Each part exists; the assembly running
   as a live programme with 91 sealed registrations, machine-checked cores, and a
   published conformance report does not appear to.

And the honest counterweight, restated from §10.7: this document is itself an
unregistered claim about how inquiry should be governed. It carries no evidence
class. Programmes other than its author's have not tried it. Read it as
`exploratory` until they have.
