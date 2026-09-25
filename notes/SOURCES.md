# Research sources and frontier check

**Initial check:** September 20, 2026. **Latest targeted update:** September 25, 2026.

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

### September 25 update: version 2 reports fifteen total runners

Jaan Allikvere, *Fourteen and fifteen lonely runners*, arXiv:2609.02604v2, revised September 24, 2026, 11:58:42 UTC.

[Versioned abstract and history](https://arxiv.org/abs/2609.02604v2)

During the Ultra review, a separate reviewer and the root reviewer each opened the versioned primary record. The revised abstract reports proofs for fourteen and fifteen total runners; the comments identify the fifteen-runner addition and public code/certificate archives. We inspected the abstract, comments, and version history only. We did not audit the revised proof, download or rerun its computation, establish peer-review status, or claim independent reproduction. The v1 entry above remains the record of the earlier reading. This updates project orientation and does not certify or invalidate our structured-family arguments.

## S8 — Single-speed modifications and uncovered intervals

Yuhan Zhang, *Single-speed modifications of the tight Lonely Runner instance: an effective bound and the complete classification for r = 2*, arXiv:2608.13599v1. The inspected HTML is dated August 1, 2026.

[Versioned HTML](https://arxiv.org/html/2608.13599v1)

Inspected the abstract, Section 1.1 (restating Goddyn–Wong's acceleration criterion), the divisibility observation, and the interval setup. The preprint reports classifications and exact censuses beyond our study; these have not been independently audited. Its use of uncovered intervals is directly relevant to our speed-6 deletion. We derived and checked that fixed eight-runner calculation ourselves. The paper uses `n` total runners, matching our convention.

The original Goddyn–Wong article is *Tight Instances of the Lonely Runner*, Integers 6 (2006), A38, DOI 10.5281/zenodo.8275490. The journal's [volume index](https://math.colgate.edu/~integers/vol6.html) was inspected, but direct PDF retrieval failed. The acceleration criterion was read in S8 and cross-checked against S1, not independently rederived in its generality. No source is being used to support a novelty claim.

## S9 — Short relations, Fourier analysis, and geometry

Matthias Beck and Samuel Everett, *Lonely Runner Relations*, arXiv:2609.06259v1, submitted September 5, 2026 (manuscript dated September 4).

[Versioned HTML](https://arxiv.org/html/2609.06259v1)

Read Theorems 1–2, the Fourier proof, Proposition 4, and open questions. Relevant necessary condition recorded in [the domain map](DOMAIN_CONNECTIONS.md). The paper uses `k` moving speeds, so our total is `n=k+1`. No independent proof audit.

## S10 — Original polyhedral formulation

Matthias Beck, Serkan Hoşten, and Matthias Schymura, *Lonely Runner Polyhedra*, Integers 19 (2019), A29, published June 3, 2019.

[Journal PDF](https://math.colgate.edu/~integers/t29/t29.pdf)

Read the abstract, introduction, Section 2, and Proposition 1. They connect a line meeting translated closed cubes with integer points in a polyhedron and with projected zonotopes. These provide established precedents for our phase-space explanation; the formulation is not our discovery. Its `k` equals our `n-1`.

September 20 additions also consulted S1 on connections and rational independence, and S4 on interval coverage. The Class C document was read solely to check the scope of Vance's prior hypothesis; it supplies no proof of a Lonely Runner claim.

The initial September 20 Fibonacci follow-up re-opened S1 Section 7.3 on lacunary sequences and its displayed successive-doubling theorem. Fibonacci speeds fit the broader lacunary definition but not that doubling hypothesis. Its unsuccessful targeted searches were superseded by the recurrence continuation: S11–S12 directly address the pattern. See [the original bounded check](FIBONACCI_CHECK.md) and [the continuation](FIBONACCI_RECURRENCE.md).

## S11 — Exact Fibonacci-prefix maxima

Victoria Zhuravleva, *Diophantine approximations with Fibonacci numbers*, arXiv:1112.6142v1, December 28, 2011.

[Versioned paper](https://arxiv.org/abs/1112.6142v1) · [HTML](https://arxiv.org/html/1112.6142v1)

Inspected Theorems 1–2, Corollary 1, Table 1, and the proof structure; no complete independent audit. Her largest index `N` equals our total runner count `n`: removing duplicate `F_1=F_2` leaves `N-1` moving speeds. Her stage index is our `m-1`. The exact plateau formula and limiting optimum match our reconstruction. This resolves the earlier source gap; these results are not ours.

## S12 — A modular Fibonacci witness

Ram Krishna Pandey, *On Some Magnified Fibonacci Numbers Modulo a Lucas Number*, Journal of Integer Sequences 16 (2013), Article 13.1.7, published January 26, 2013.

[Journal page](https://cs.uwaterloo.ca/journals/JIS/VOL16/Pandey/pandey7.html) · [PDF](https://cs.uwaterloo.ca/journals/JIS/VOL16/Pandey/pandey7.pdf)

Inspected the introduction, congruence lemmas, and Theorem 5; no complete independent audit. His index `t` is our total `n`; his stage `n` is our `m-1`. The theorem supplies the witness lower bound, not alone the global maximum. Its listed endpoint order appears reversed; our note gives the exact `mod 11` check. The bound itself matches the calculations.

## S13 — Exact pairwise blocking correlations

Guillem Perarnau and Oriol Serra, *Correlation Among Runners and Some Results on the Lonely Runner Conjecture*, Electronic Journal of Combinatorics 23(1) (2016), P1.50, published March 18, 2016. Preprint arXiv:1407.3381v3, September 12, 2015.

[Journal page](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v23i1p50) · [Journal PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v23i1p50/pdf/) · [Versioned preprint](https://arxiv.org/abs/1407.3381v3)

Inspected the pair-intersection derivation, Propositions 7–8, and Corollary 9 on September 24, 2026. Their n counts moving speeds, so our total is n+1 in their notation; the pair formula uses an independently chosen threshold delta. Proposition 8 matches our ratio calculation at delta=1/8. The journal's stated threshold range includes this value. No audit of the paper's other theorems. See [SPEED_RATIOS.md](SPEED_RATIOS.md) for our reconstruction and local application.

Additional bounded reading on September 24: Lemma 13, equation (12), and the following maximum-tree selection sentence. The authors attribute the tree inequality to Hunter. It bounds the probability of avoiding all events using individual event probabilities and the pair intersections on any spanning tree. Restricting time to a positive-length core opening gives the local tree certificate in CORE_TRANSFER.md Sections 6–8. The tree idea and maximizing its pair weight are established in this source; no novelty is claimed. This reading is not an audit of Lemma 14 or the paper's resulting general bounds.

## S14 — Bernoulli-polynomial form and unequal thresholds

Alathea Jensen, *Mixed thresholds in the Lonely Runner Conjecture*, arXiv:2605.27941v1, May 27, 2026.

[Versioned preprint](https://arxiv.org/abs/2605.27941v1) · [HTML](https://arxiv.org/html/2605.27941v1)

Inspected the introduction, Lemma 4.1, its Fourier derivation, and the following unsafe-set remark on September 24, 2026. Specializing both thresholds to 1/8 gives our fractional-part formula exactly, since B2(x)=1/6-x(1-x). Jensen identifies S13 as the equal-threshold predecessor. Her k is our n-1. This source led us to S13; no claim to have audited the full mixed-threshold theory or its frontier statements.

## S15 — One very fast runner and time perturbation

Noah Kravitz, *Barely lonely runners and very lonely runners: a refined approach to the Lonely Runner Problem*, Combinatorial Theory 1 (2021), paper 17, published December 15, 2021. DOI 10.5070/C61055383.

[Journal record](https://escholarship.org/uc/item/3wx931fh) · [Published PDF](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf)

Inspected Proposition 6.1 and its proof on printed pages 12–13 on September 24, 2026. It preserves a safe interval for slower runners while one sufficiently fast runner moves through it. This is an established precedent for the time-perturbation argument in FAST_CLUSTER.md. The four-runner common-rotation construction is not claimed to be this proposition verbatim or to be new. The paper's n counts moving speeds in its technical formulation, so our total is n+1. No audit of the wider spectrum results.

September 24 scaled-perturbation follow-up: inspected Section 2, printed page 5, on pre-jumps, and the common-factor opening of Theorem 5.2's proof on printed page 10. Time increments j/q fix the q-divisible runners and adjust the others. SCALED_PERTURBATION.md applies this known mechanism to a six-runner core and a coprime exceptional speed; no novelty claim or full-paper audit.

September 24 four-perturbation follow-up: revisited the Section 2 pre-jump paragraph. FOUR_PERTURBATIONS.md keeps the core phase fixed and explicitly rounds an auxiliary opening onto actual times. Its fifth-grid argument and finite remainder are our unreviewed specialization; this source is methodological precedent, not a novelty certificate.

September 25 unequal-offset follow-up: revisited the same Section 2 pre-jump paragraph. UNEQUAL_PERTURBATIONS.md uses exact phase intervals and midpoint rounding for one doubled offset. Its tiling divisibility lemma and 44-case finite remainder are our unreviewed synthesis; no novelty or wider literature-audit claim.

September 25 two-doubled-offset follow-up: revisited Section 2, printed page 5, on core-preserving pre-jumps. TWO_DOUBLED_OFFSETS.md combines this known time-grid method with our proposed tiling criterion and parity obstruction. The changed-coefficient control preserves the limits of the specialization. No broader literature or novelty audit.

September 25 local-tiling follow-up: read Section 2, Proposition 2.1 and the adjacent discussion on printed pages 4–5, and revisited the pre-jump paragraph on page 5. These supply established context for opposing threshold contacts and core-preserving time increments. LOCAL_TILING_RULE.md derives a conditional local escape rule and uniform q>=8 construction for a positive-coefficient tiling class. Its cyclic boundary-velocity identity, denominator bounds, and exact examples are our unreviewed synthesis, not claims attributed to this source. No wider literature or novelty audit.

## S16 — Relative spectra and two-dimensional subtori

Vanshika Jain and Noah Kravitz, *Relative Lonely Runner spectra*, Combinatorial Theory 6(1) (2026), paper 1, published April 20, 2026. Inspected preprint: arXiv:2411.12684v2, December 9, 2024.

[Journal record](https://escholarship.org/uc/item/3mx8w3js) · [Versioned HTML](https://arxiv.org/html/2411.12684v2) · [Published PDF](https://escholarship.org/content/qt3mx8w3js/qt3mx8w3js_noSplash_9e8150c4b1543e5d1d9da402dec3a64a.pdf)

September 24 follow-up: read definitions, Theorem 1.1, Section 1.4, and the Section 2.1 proof outline. Their n counts our n-1 moving coordinates. This upgrades the earlier search-excerpt lead; the full proof remains unaudited. FAST_CLUSTER.md Section 7 gives the comparison and our own mapping. We do not attribute our Fourier argument, threshold guarantee, or novelty to this source.

## S17 — Two exceptional runners under a pre-jump

Ho Tin Fan and Alec Sun, *Amending the Lonely Runner Spectrum Conjecture*, Electronic Journal of Combinatorics 33(1) (2026), P1.38, published February 27, 2026.

[Published PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i1p38/pdf/)

Inspected Lemma 23 and its proof (printed pages 12–13), and the Section 5.3 case split, September 24, 2026. Related modular method; its 1/4-target lemma excludes equal/opposite residues. Our ±1 family has that excluded relation. See TWO_PERTURBATIONS.md for the distinct counting argument. No full-paper audit or novelty conclusion.

## Source discipline

Record exactly what was read, what a paper claims, and what we independently checked. Prior assistant recommendations are motivation, not sources. Finding a preprint is not validating its proof; reproducing a toy case is not reproducing its full computation. Cite original results when developing an argument, and check corrections or newer versions before relying on a research frontier.
