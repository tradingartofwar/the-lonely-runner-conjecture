# Research sources and frontier check

**Checked:** September 19, 2026  
**Scope:** Targeted source check for project planning, not an exhaustive literature review or independent proof audit.

## S1 — Orientation and tight examples

Guillem Perarnau and Oriol Serra, *The Lonely Runner Conjecture turns 60*, arXiv:2409.20160v3, August 12, 2025.

[Versioned paper](https://arxiv.org/abs/2409.20160v3) · [HTML](https://arxiv.org/html/2409.20160v3)

Inspected the formulation/reduction, tight-instance discussion (Section 4), and open-problem collection (Section 11). Use it for definitions, known examples, and pointers to original proofs. Its frontier discussion predates later results. Its notation counts moving speeds, not our total runners; add one when translating. Tight-example classification supplies a candidate research direction, whose current status still needs a targeted update before a novelty claim.

## S2 — Accessible entry to computer-assisted methods

Matthieu Rosenfeld, *The lonely runner conjecture holds for eight runners*, arXiv:2509.14111v2, October 16, 2025.

[Versioned paper](https://arxiv.org/abs/2509.14111v2) · [HTML](https://arxiv.org/html/2509.14111v2)

Inspected the abstract and available method outline. This is an entry point to finite reductions and modular computation. Before reproduction, read the relevant proofs and implementation instructions in full, resolve the authors' code, pin a revision, and select a small test. No code from this paper was executed in project initialization.

## S3 — Reported finite-runner frontier

Touch Sungkawichai and Tanupat Trakulthongchai, *Eleven, twelve, and thirteen lonely runners*, arXiv:2604.23906v2, September 1, 2026.

[Versioned paper](https://arxiv.org/abs/2604.23906v2) · [HTML](https://arxiv.org/html/2604.23906v2) · [Author-linked code](https://github.com/vzsky/13-lonely-runners)

Theorem 1.3 states the result for `k<=12` moving speeds: 13 total runners in our notation. Inspected the theorem, implementation discussion, and proof conclusion. The paper describes modular sieving, symmetry reduction, and supporting computations.

Fourteen total runners is beyond this paper's theorem, but a later source check in the same conversation found S7 reporting that case. Do not call either result independently reproduced, peer-review status verified, or the next case tractable. The linked code and logs have not been audited here. Refresh the literature before choosing frontier work.

## S4 — A second account of the standard formulation

Terence Tao, *Some remarks on the lonely runner conjecture*, January 10, 2017.

[Author's exposition](https://terrytao.wordpress.com/2017/01/10/some-remarks-on-the-lonely-runner-conjecture/)

Explains the covering viewpoint, integer-speed reduction, and why finite reducibility alone need not make verification feasible. Its historical runner-count frontier is obsolete; do not reuse it as current status.

## S5 — Do not conflate the shifted variant

Mónica Blanco, Francisco Criado, and Francisco Santos, *Coloopless zonotopes and counterexamples to the Shifted Lonely Runner Conjecture*, arXiv:2603.24784v2, April 27, 2026.

[Versioned paper](https://arxiv.org/abs/2603.24784v2)

Abstract inspected. It reports counterexamples to the shifted variant and to a related auxiliary property. Those are not counterexamples to the common-start conjecture studied here. If we explore freely chosen starting phases, it must be labeled a different problem; inspect the full definitions before transferring any result.

## S6 — Fresh lead to resolve before spectrum claims

Francesco Cordella, *Odd denominators in the Lonely Runner spectrum for six speeds*, arXiv:2609.03444, September 3, 2026, appeared in search results during this check.

[Research lead](https://arxiv.org/abs/2609.03444)

Direct abstract and HTML retrieval failed in this session. Treat it as an unverified lead, not as a relied-upon theorem. Obtain and inspect the paper before making claims about unclassified near-tight values for six speeds. No findings or counts from its search snippet are adopted here.

## S7 — Later source check: reported fourteen-runner result

Jaan Allikvere, *Fourteen lonely runners*, arXiv:2609.02604v1, September 2, 2026.

[Versioned PDF](https://arxiv.org/pdf/2609.02604v1)

Inspected the abstract and introduction. The preprint reports a computer-assisted proof for 14 total runners, extending S3's finite-checking framework. Its code, certificates, proof, and review status have not been independently audited here. This corrects the earlier provisional frontier note; it has no role in certifying our 4/8/12 example calculations.

## Source discipline

Record exactly what was read, what a paper claims, and what we independently checked. Prior assistant recommendations are motivation, not sources. Finding a preprint is not validating its proof; reproducing a toy case is not reproducing its full computation. Cite original results when developing an argument, and check corrections or newer versions before relying on a research frontier.
