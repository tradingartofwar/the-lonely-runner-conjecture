# Targeted literature and structural assessment — 2026-09-29

Pinned project head: `7b0101376e00dbb71537d3a62e39ec75cee113cc`.
Scope: fresh primary-source reading for the Ultra assessment, not an exhaustive literature review, novelty certification, or independent audit of the cited computational proofs. No mathematical executable, outside message, or new search experiment was run. Shell use was limited to reading project text; this report is the only file written by this reviewer.

## Assessment

The strongest retained contribution is an explicit mechanism: endpoint-sensitive, common-time placement certificates explain why specified blocking patterns cannot cover a supplied safe set. The two-window hull/gap criterion is a particularly compact example. The project has reached substantially better structural explanations and auditable certificates for a restricted family. It has not reached a new unresolved eight-runner existence case: the standard eight-runner theorem already covers every instance of the physical family.

The exact missing implication is **selection/completeness**. The current arguments certify a supplied useful core/window pair or a supplied affine contact model. They do not show that every arbitrary speed vector admits one of those certificates, nor that a failure of the current certificate must belong to a classified arithmetic exception. More fixed examples or another coordinate representation will not supply that implication by themselves.

The most useful fresh source correction is that Beck–Everett has a **September 23 v2**, whereas the project source note still pins v1. Its short odd-sum relation condition remains uninformative by itself on the fixed family: `(1,1,-1,0,0,0,0)` annihilates `(1,4,5,a,b,c,d)`, has odd coefficient sum and norm 3. Any useful inverse statement must extract a relation involving residual coordinates, beyond relations already forced by the selected core.

## Source checks and exact reading limits

### 1. Reported fifteen-runner frontier

Jaan Allikvere, *Fourteen and fifteen lonely runners*, [arXiv:2609.02604v2 HTML](https://arxiv.org/html/2609.02604v2), September 24, 2026.

Read the abstract, introduction and Theorem 1.1; Section 2's definitions and prime-divisibility argument; Sections 3.1–3.3 through the statement of Proposition 3.4; Sections 4.1–4.4's covering/lifting statements and proofs; and Sections 5–7. The theorem explicitly reports fourteen and fifteen **total** runners. The technical `k` counts moving speeds, so fifteen runners means `k=14`. The paper combines a lattice-basis flag bound with modular computations. Section 6 explicitly says the full computation has not been independently reimplemented or formally verified. I did not inspect all of Section 3, download certificates, or audit code. Versioned abstract and PDF retrieval initially failed; versioned HTML succeeded. A targeted search for sixteen-runner results found no usable primary result; this is not proof of absence. Use “reported fifteen-runner result,” not an independently certified frontier.

### 2. The standard eight-runner conclusion

Matthieu Rosenfeld, *The lonely runner conjecture holds for eight runners*, [arXiv:2509.14111v2 HTML](https://arxiv.org/html/2509.14111v2); [current record and history](https://arxiv.org/abs/2509.14111), October 16, 2025.

Read Theorem 1, Sections 2–4, and Section 6's implementation outline. Theorem 1 gives distance at least `1/8` for seven moving integer speeds. The proof combines a finite counterexample-product bound with computer-verified divisibility by specified primes. The current arXiv record still identifies v2. Equality is included. This is the standard common-start result applicable to the physical project family; the computation was not rerun or independently audited here. The printed computational description must not be copied into a reproduction without resolving its notation and checking the actual implementation.

### 3. Short relations: newer version and the core obstruction

Matthias Beck and Samuel Everett, *Lonely Runner Relations*, [arXiv:2609.06259v2](https://arxiv.org/html/2609.06259v2), September 23, 2026; manuscript dated September 22.

Read Theorem 1.1, Section 2 including Theorem 2.1 and the Fourier proof, Section 3 including Proposition 3.1 and Theorem 3.2, and Section 4. No strict lonely time implies an odd-sum integer relation of `L1` norm at most `2k+3`; the geometric bound uses flatness. These are necessary conditions, not classifications. The authors explicitly credit earlier Fourier, additive-relation, and lattice-width methods. Their open problems include behavior on a prescribed short-relation hyperplane. The inspected statements do not force a relation outside a preselected core's relation lattice. This is a source-reading observation, not a claim that such a result does not exist elsewhere.

### 4. Conditional inverse extraction already has a direct precedent

Terence Tao, *Some remarks on the lonely runner conjecture*, [arXiv:1701.02048v4](https://arxiv.org/html/1701.02048v4), November 2, 2017; [published paper, Contributions to Discrete Mathematics 13(2), 2018](https://cdm.ucalgary.ca/article/download/62728/46825).

Read the introduction's normalization, Section 2's generalized progressions and Lemma 2.2 with proof, and Section 3 equations (3.10)–(3.17), Proposition 3.3 with proof; only the statement of Proposition 3.4. Lemma 2.2 connects Bohr-intersection measure to bounded relation multiplicity. Proposition 3.3 extracts a relation involving an additional speed relative to two fixed speeds when triple-versus-pair multiplicities are sufficiently large. Thus conditional/relative inverse extraction is established methodology. An explicit safe-core localization with usable constants can be a specialization, but should not be presented as inventing that inverse principle. The full asymptotic proof was not audited.

### 5. Polyhedral compatibility is established mathematics

Matthias Beck, Serkan Hoşten, Matthias Schymura, *Lonely Runner Polyhedra*, Integers 19 (2019), A29, [published PDF](https://math.colgate.edu/~integers/t29/t29.pdf), published June 3, 2019.

Read the introduction, Section 2, equation (5), and Proposition 1; visually inspected printed page 4 because PDF extraction mangles mathematical signs. Integer-point feasibility of the lonely-runner polyhedron and the equivalent projected-zonotope formulation are established. Restricting its time fiber to a core window is a direct specialization. Constructing the same object in more dimensions is not itself a new proof method; the contribution would be a quantitative width, separation, or certificate-completeness statement particular to the retained arithmetic.

Romanos Diogenes Malikiosis, Francisco Santos, Matthias Schymura, *Linearly exponential checking is enough for the lonely runner conjecture and some of its variants*, [publisher article](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/linearly-exponential-checking-is-enough-for-the-lonely-runner-conjecture-and-some-of-its-variants/A51A991DE89B8C9C2E2FF13FBD4501DA), Forum of Mathematics, Sigma 13 (2025), e164, published October 1, 2025.

Fresh reading was limited to publication metadata, abstract, Theorem A and surrounding explanation. Theorem A is conditional on the lower-runner case and involves the sum of subset gcds for a primitive positive speed vector. It provides a finite reduction, not a claim that enumerating the resulting region is affordable. The original paper's shifted reduction has an additional Lonely Vector Problem dependency; do not silently transfer it to common-start or vice versa. DOI redirect failed; the publisher URL succeeded. No full finite-reduction proof was inspected in this pass.

### 6. Near-tight spectra: what the applicable theorem actually gives

Vanshika Jain and Noah Kravitz, *Relative Lonely Runner spectra*, [arXiv:2411.12684v2](https://arxiv.org/html/2411.12684v2), December 9, 2024.

Read definitions and Sections 1.1–1.4, especially Theorem 1.1 and Corollary 1.2. A fixed proper two-dimensional subtorus has an order-one spectrum differing finitely from a finite union of reciprocal arithmetic progressions translated by its distance `D(U)`. Maximum loneliness is `1/2-D`, so the direction of inequalities reverses when using the project's loneliness convention. This is directly relevant to one fixed affine pencil of speed vectors, not a uniform classification over all pencils or arbitrary speeds. Its introductory runner frontier is obsolete. The full proof and published-version comparison were not audited here.

Francesco Cordella, *Odd denominators in the Lonely Runner spectrum for six speeds*, [primary record](https://arxiv.org/abs/2609.03444), September 3, 2026.

The primary arXiv search abstract was retrieved. Direct abstract/HTML/PDF attempts failed in this pass, as in earlier project checks. Therefore this remains an important uninspected full-paper lead, not an input to a claimed classification. Its abstract discusses all-but-finitely-many six-speed spectrum behavior; a project statement that this area is wholly unclassified would be unsafe. No theorem number, proof, family formula, code, or exception set was verified.

### 7. Shifted counterexamples and overlap with our certificate language

Mónica Blanco, Francisco Criado, Francisco Santos, *Coloopless zonotopes and counterexamples to the Shifted Lonely Runner Conjecture*, [arXiv:2603.24784v2](https://arxiv.org/html/2603.24784v2), April 27, 2026.

Read definitions in Section 1, Proposition 1.7, Section 5.1's Lemma 5.1/proof and Definition 5.2, the interval-cover description in Section 5.2, and Proposition 5.10. The paper distinguishes central minimum (common start) from covering radius (arbitrary shifts). Proposition 5.10 reports shifted loneliness `15/94<1/6` for speeds `(1,2,3,4,5)`. Section 5.1 already uses lap-labelled inequalities and open/closed certificate polytropes, distinguishing strict, equality and failure cases. Our F/P/Z bookkeeping is a tailored containment taxonomy, not discovery of endpoint-sensitive polyhedral feasibility. The supplied last-runner auxiliary result changes only one phase, so it does not assert the false unrestricted shifted conjecture. No full algorithm/code audit was performed.

Daria Poliakova, *More (shifted) runners, less loneliness*, [arXiv:2609.23952v1 HTML](https://arxiv.org/html/2609.23952), September 20, 2026.

New lead absent from the inspected source list. Read the abstract, introduction, Section 1's definitions and Theorems 1–2. With `n` moving speeds and arbitrary shifts, the infimum is parameterized as `1/(n+1+E_n)`; the paper proves a positive linear lower bound for `E_n`. The construction/proof was not audited. This reinforces the need to preserve common-start compatibility in any scalable argument. Initial direct retrieval failed, but opening the primary search result succeeded.

## Duplication versus plausible specialization

| Project ingredient | Literature assessment | Remaining potentially useful specialization |
| --- | --- | --- |
| Common-time torus, lattice, cube, or polyhedron | Established formulation | A speed-uniform bound or a small complete certificate family |
| Lap labels and strict/closed inequalities | Established compatibility language | The exact two-window hull/gap obstruction and explicit endpoint records |
| Short relations from failure of separation | Established inverse mechanism | Relations involving residual speeds after fixed-core dependencies are removed, with useful constants |
| Pre-jumps and sufficiently fast added runner | Established mechanisms already credited in project sources | Sharper thresholds, explicit local geometry, and residue-sensitive entry times |
| Fixed affine pencils and rational asymptotics | Established relative-spectrum framework | An explicit global formula/certificate for a chosen pencil and a complete exceptional range |
| Existence for the present eight-runner family | Already covered by the standard theorem | Explanatory certificates that remain meaningful when the runner number varies |

The word “plausible” describes a research target. None of these rows certifies novelty.

## Two actionable leads

### A. A quantitative inverse statement relative to a safe core

**Proposed statement to derive, not an established project theorem:** Fix an integer core `C` and a threshold `0<delta<1/2` such that the strict core-safe set has positive measure. For each residual count `r`, produce explicit finite constants `Q(C,delta,r)` and `M(C,delta,r)` such that, for every positive integer residual tuple `(u_1,...,u_r)`, absence of a strict simultaneous safe time forces

`q + m_1 u_1 + ... + m_r u_r = 0`,

where `|q|<=Q`, `0<sum |m_j|<=M`. The nonzero residual vector is essential; a relation internal to `C` is not enough.

A direct route uses a nonnegative smooth function supported inside a strict core opening, a nonnegative periodic safe-arc bump for each residual coordinate, and explicit trigonometric approximations. If no bounded residual relation exists, only the positive constant term survives integration. This is a standard Fourier strategy, with Tao and Beck–Everett as methodological dependencies. The value to this project would be explicit constants and a rigorous residual condition.

**Quickest falsifier/usefulness check:** verify that the proposed finite-frequency relation cannot be discharged entirely inside the core. Next test the symbolic scale of its constants against the already available finite bounds. A theorem with enormous constants, or one repeatedly satisfied by a fixed small residual speed, will not advance the selection gap. Even a correct lemma needs an additional rank-growth/quotient argument before it can govern all residual coordinates. Do not claim that extracting one more relation completes a finite classification.

**Next action:** one written derivation and adversarial review, starting from an existing positive core opening; no enumeration is needed to decide whether the constants are competitive. Coordinate with the duality review, which is independently deriving this direction.

### B. Use one affine pencil to connect local contacts to a global spectrum

Fix integer vectors `A,B` and an admissible range of integer `q` for which `v(q)=qA+B` has positive distinct entries. Use one **already studied** tiling/affine family. Its orbit lies in the fixed subtorus generated by `A,B`; check properness and dimension before invoking relative-spectrum results.

**Precise next target:** give explicit `q0`, a modulus `M`, and finitely many rational functions, with an exact branch rule, computing `max_t min_i ||v_i(q)t||` for every admissible `q>=q0`, plus the finite exceptional `q` range. This asks whether the project's local contact construction actually controls the global optimum. Existing safe-time witnesses do not establish that upper bound.

**Quickest falsifier:** compare the proposed winning contact against the other inherited contact branches by exact symbolic inequalities, retaining ties and common-factor normalization. Any other branch with a larger attained minimum disproves the proposed global formula; a local first-entry calculation alone is insufficient.

**Dependencies and payoff:** Jain–Kravitz explains why a fixed two-dimensional setting is a sensible place to seek arithmetic structure. It does not establish this particular formula without calculation. The payoff is a stronger, sharply scoped theorem than another existence example. Its relation to known spectra must be checked before any novelty claim. This is secondary to A if the mission is a mechanism that can scale in runner count.

## Recommendation

### Addendum: targeted additive-triple contraction check

At the strategy review's request, searched both search engines for an all-runner-count theorem for speed sets containing `p,q,p+q`, including the phrases “additive triple”, “sum of two”, and “contraction”. Revisited the inspected Beck–Everett statements and read Sections 2, 3.4, and 7.1 of Perarnau–Serra's [survey v3](https://arxiv.org/html/2409.20160v3), August 12, 2025, for pointers. I did not locate a theorem supplying the proposed equality-preserving extension from the lower-runner case. This small negative search does not certify novelty or openness.

The deletion/contraction search hit concerned nowhere-zero flows and regular matroids, a related weaker problem. A new vector in a flow space need not be a common-time scalar multiple of the original velocity vector. Such a result cannot be treated as the requested runner lift without an additional orbit-preservation argument.

There is an immediate stress test for a naive deletion proof: an old witness can put `pt` and `qt` at opposite safe phases, making `(p+q)t` integral. Therefore the prospective gate must prove an appropriate **choice** of lower-case witness and a valid common-time lift, including threshold contacts. The mere fact that the three speeds obey a short relation establishes neither. Freeing the ratio `1:4:5` is a meaningful scope change, but remains a proposed proof problem.

### Late correction: relaxed-subspace existence is already supplied by lower cases

The arithmetic and root reviewers give a concise positive-cone argument. Let `K` be a rational subspace of `R^k`, of dimension `d>=2`, containing a vector with all coordinates positive. Minimize the sum of coordinates on `K intersect [1,infinity)^k` and choose a vertex of the minimizing face. At least `d` coordinate inequalities are active there, so at least `d` coordinates equal 1. A rational such vector has at most `k-d+1` distinct positive entries. Applying the lower-runner theorem to those distinct speeds yields a point of the relaxed torus with coordinate distances at least `1/(k-d+2)`. This is strictly above `1/(k+1)` when `d>=2`.

**Direct inspected precedent:** Allikvere v2, Section 3.2, **Lemma 3.3 and proof**, already states the corresponding rational-subspace conclusion and credits **Giri–Kravitz Lemma 3.3**. Its proof uses coordinate collisions and induction. This reviewer read those lines in the initial primary-source pass; Giri–Kravitz's original lemma was not independently opened in this pass. The positive-cube vertex argument is a short alternate derivation under positivity, not a new existence theorem. In the proposed `P2` case `k=7,d=3`, the relaxed separation bound is `1/6`, using the established six-total-runner result.

Consequently, mere existence of a strictly safe point in the `P2` relaxation is **not an open next target**. The bound finds a point along a selected rational direction inside `K`; it does not make the original physical velocity orbit visit that point. This actual-orbit versus relaxed-torus distinction is the remaining obligation. The affine-spectrum lead above asks for a global maximum on the actual specified orbit, so that stronger target survives this correction, but it is secondary to the orbit-preserving problem.

**Updated priority:** first formulate and attack the additive-core, orbit-preserving lift described in the addendum. Keep the relative inverse lemma as a supporting quantitative tool only if it supplies usable constants and a relation involving previously uncontrolled coordinates. Keep the two-window criterion as a clean structural lemma, without another broad success scan. A global affine-spectrum calculation remains an alternative bounded project with a clear upper-bound obligation. Retain a separate boundary/equality path throughout: strict positivity and measure estimates cannot detect every valid lonely moment.

Material AI involvement: this report was prepared by an AI reviewer through primary-source reading and hand reasoning. It provides orientation and criticism, not external mathematical certification.
