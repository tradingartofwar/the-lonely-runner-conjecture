# Across domains: invariants, phases, and dimensions

**Date:** September 20, 2026. **Scope:** A first sourced map and three exact illustrations, not a literature census or a proposed proof of the general conjecture.

Vance asked to explore algebra, geometry, number theory, physics, quantum theory, and then extra dimensions, looking for concepts our present representation may hide. We call the method **structural translation**: keep the same question, identify what a change of representation preserves, and test whether the new language supplies an additional argument.

## What the earlier multiplicative work supplies

The earlier Class C document's Section 8 explicitly labels its broad hyperuniformity, spectral, heavy-tail, sensitivity, and universality statements as conjectures. They are research leads with assumptions, not established laws for all multiplicative systems. Prior confident wording does not upgrade their evidence status. The document was consulted for this limited comparison; its contents are not imported into this repository.

The usable methodological idea is to compare phase relationships, transformations, and event definitions across domains. A log coordinate can expose multiplication as addition. That identity alone supplies neither the Lonely Runner bound nor the statistical signatures proposed for Class C.

## One object, several languages

Choose a reference runner among `n` total runners. Its `k=n-1` nonzero relative speeds are `u_j`. Every runner starts at the same position. Set

$$\theta_j(t)=u_jt\pmod 1,\qquad f(t)=\min_j\|u_jt\|,\qquad \delta=1/n.$$

| Domain | Representation | Useful question or limit |
| --- | --- | --- |
| Algebra | Transformations of the speeds and integer relations between them | Which changes preserve the complete distance function? |
| Number theory | Fractional parts, divisibility, residues, rational approximation | Which arithmetic relations constrain simultaneous separation? |
| Geometry | The vector of phases moves through a box whose opposite faces are identified | Does this path meet the closed target box? |
| Classical dynamics | Uniform motion of uncoupled phase variables | Does the orbit repeat, or explore a larger set over time? |
| Harmonic analysis | Periodic window functions and their products | Which frequency combinations survive time averaging? |
| Quantum mathematics | Rotating complex phases under a diagonal Hamiltonian | What is shared by the phase equations, and what would require a different observable? |
| Log coordinates | Reparameterize time by `x=exp(t)` | Which conclusions survive a coordinate change, and which depend on its measure? |

These are established areas around the problem; the exact comparisons below are our exposition. For prior geometric formulations see Beck–Hoşten–Schymura, *Lonely Runner Polyhedra*, Section 2 and Proposition 1 ([S10](SOURCES.md)). For connections and irrational-speed reduction see the survey ([S1](SOURCES.md)); for interval coverage see Tao ([S4](SOURCES.md)).

## Exact invariants we can derive directly

1. **Common change of speed:** replacing every original speed `v_i` by `v_i+c` leaves all relative speeds and all pairwise distances unchanged.
2. **Common scale:** replacing every speed by `a v_i`, with `a>0`, gives the old motion at time `a t`. Achievable gaps are unchanged; clock times change.
3. **Selected-reference sign symmetry:** `||-u t||=||u t||`. Independently reversing relative speeds preserves the chosen runner's distance function. Other runners' pairwise distances may change. Retain the original runner count if constraints coincide.
4. **Integer phase relations:** if integers `m_j` satisfy `sum(m_j u_j)=0`, then `sum(m_j theta_j(t))=0 mod 1` at every time.

The fourth item is the bridge between domains. Writing `z_j(t)=exp(2 pi i u_j t)` gives

$$\prod_j z_j(t)^{m_j}=1.$$

The same constraint is an integer relation in number theory, a restriction on the orbit in geometry, and a constant product of phases in wave notation. It follows immediately by adding exponents; this is not a newly discovered invariant.

Merely having a relation is insufficient: the vectors `(1,2)` and `(1,3)` both have one, but their maximum gaps are `1/3` and `1/2`. Likewise, the tight eight-runner vector `(1,2,3,4,5,7,12)` and the non-tight control `(1,2,3,4,5,7,11)` share `2u_1-u_2=0`. Their previously checked maxima are `1/8` and `1/6`. A proposed signature must distinguish these controls.

## A directly relevant current lead

Beck and Everett's September 5, 2026 preprint *Lonely Runner Relations* ([S9](SOURCES.md)) reports that a tight integer instance, or a counterexample, must have a nonzero integer relation `m dot u=0` with `sum |m_j| <= 2k+3` and odd `sum m_j`. Its Fourier and geometric arguments connect short arithmetic relations to constrained separation. This is a necessary condition, not a characterization or a proof of LRC. We read the statement, the Fourier argument, the geometric reformulation, and the open questions; no independent proof audit is claimed.

## Extra dimensions already present in the question

For three total runners, write the two relative positions as one point `(theta_1,theta_2)` in a square. The acceptable region is `[1/3,2/3]^2`, including its boundary. Crossing an outer edge wraps the corresponding coordinate to the opposite edge: the state space is a two-dimensional torus.

For arbitrary `n`, the same construction is

$$\theta(t)\in\mathbb T^{n-1},\qquad B_n=[1/n,1-1/n]^{n-1}.$$

The conjecture asks whether every permitted orbit through the common starting point meets this closed box. These dimensions record existing runners; the conjecture has not been changed into motion on a physically higher-dimensional track.

Distinguish the **number of coordinates** from the **dimension of the orbit's closure**. Seven integer relative speeds give seven coordinates but a closed one-dimensional orbit. For rationally independent relative speeds, continuous-time Kronecker theory makes the orbit dense in the full torus, so it comes arbitrarily close to the half-lap point in every coordinate [S1]. Intermediate rational relations give intermediate orbit closures. Density concerns the closure over unbounded time, not the dimension of a finite path segment. Thus “more coordinates” alone cannot distinguish tight from non-tight integer examples.

## Three exact geometric comparisons

All rows have three total runners and reference speed zero. `t` uses the displayed speed units.

| Relative speeds | Required gap | Allowed times in one cycle | Geometric behavior |
| --- | --- | --- | --- |
| `(1,2)` | `1/3` | `1/3, 2/3` only | Touches two target corners; never enters the interior |
| `(1,3)` | `1/3` | `[4/9,5/9]` | Enters the interior; reaches the center at `t=1/2` |
| `(1,2)` | Artificial target `2/5` | None | Misses the smaller target box |

The last row is an intentionally stronger demand, **not a counterexample**: the conjecture's threshold remains `1/3`. It helps distinguish an incorrect target from a failed conjecture.

Reproduce with `python -m scripts.check_phase_space_examples`; exact outputs are in [phase_space_examples.json](../experiments/phase_space_examples.json). The maximum checker and interval method agree, and the script separately verifies the phase coordinates, target-box membership, and integer relations at witnesses. The conversation visualization uses complete straight segments split at wrap times, not sampled estimates of the allowed sets.

## What waves and quantum notation add—and what they do not

Loneliness is a conjunction: **every** distance must meet the threshold. A sum of waves can cancel while one runner remains too close. A sum's zero is therefore not automatically a loneliness certificate.

For integer `u`, let `g_delta(x)` be the periodic indicator of `[delta,1-delta]`. Then

$$P_\delta(t)=\prod_j g_\delta(u_jt)$$

is an exact indicator of a lonely time. Its integral over `[0,1]` measures total allowed duration. For finite Fourier approximations, integrating a product keeps exactly those frequency terms with `sum m_j u_j=0`; passing to a full series needs convergence care. This gives a reason to investigate the integer relations rather than treating all phases as independent.

**Boundary warning:** in the first geometric example the integral is zero, although two valid times exist. At the exact conjectured threshold, zero duration cannot distinguish boundary contact from complete avoidance. Positive duration proves feasibility; zero duration does not disprove it. The same issue applies to smooth windows designed to detect strict separation.

A formal quantum correspondence can be constructed without asserting a quantum solution: choose a diagonal matrix `H` with entries `2 pi hbar v_j`. The amplitudes `a_j(t)=a_j(0) exp(-2 pi i v_j t)` solve `i hbar a'(t)=H a(t)`. Their relative phase rotations have the runners' relative speeds, up to sign. Nonzero initial amplitudes with common phase reproduce the common-start phase setup. Actual quantum transition probabilities also depend on amplitudes and the measurement; phase separation from one component is not state orthogonality, entanglement, or measurement-induced isolation. No specifically quantum theorem or advantage has been transferred here.

For the logarithmic comparison, `t=log x` changes `f(t)` to `f(log x)` for `x>=1`. A period `T` becomes invariance under `x -> exp(T)x`. This is a valid coordinate translation. A uniform time measure becomes `dx/x`, so apparent spacing or spectra in ordinary `x` are not automatically preserved. Taking logarithms of the *speeds* is a different change and generally changes the problem.

## Next question, with a way to be wrong

For the known tight eight-runner cases and their non-tight controls, compare the short integer relations **together with the target faces touched and the blocking intervals between contacts**. Ask which combination explains boundary-only contact and which permits entry into the interior. A relation found in both a tight example and a non-tight control cannot by itself explain tightness. The existing `(1,2,3,4,5,7,12)` versus replacement `11` comparison is an immediate such control.

Then resume the parked double-replacement example `(1,4,5,6,7,11,13)`, asking how arithmetic relations and cooperative interval coverage fit together. This is a bounded next investigation, not a large scan.

**Completed later September 20:** [the cooperative-blocking continuation](TIGHT_CASES_4_8_12.md#september-20-cooperative-blocking-and-a-changing-tight-runner) checks seven configurations and all 56 reference runners. It explains the shared coverage, corrects the earlier pair-sum pattern, and supplies equal-snapshot controls with different maxima. A one-speed change also transfers the unique tight role to another runner whose absolute relative speeds form the consecutive set. The next comparison should group such equivalent reference descriptions before treating them as different structures.

Vance's idea about distributed intelligence is retained as a methodological hypothesis: different people, tools, and disciplines may supply different useful representations. Success here would be an explicit translation that explains a previously unexplained observation or certifies a new case. The present mathematics neither establishes a universal intelligence law nor shows that a missing concept is the only obstacle to solving LRC.

## Models not yet used systematically: a prioritized follow-up

After the [Fibonacci check](FIBONACCI_CHECK.md), Vance asked which additional modeling languages could reveal structure. The distinction is between a field we have mentioned and a specific representation we have actually used to explain or certify something.

| Priority | Representation | Status and concrete question |
| --- | --- | --- |
| 1 | Discrete dynamics and recurrence matrices | Continuous-time phase motion was already examined. A recurrence advancing through Fibonacci **runner indices** has not been used to explain the maxima. Can its allowed trajectories explain the plateaus? |
| 2 | Continued fractions | Fractions and residues were used, but not the hierarchy of rational approximations to an irrational number. Why do the observed maximizing times occupy particular levels of this hierarchy? |
| 3 | Graphs of blocking intervals | Interval coverage was computed exactly; a graph-based certificate has not been constructed. Which intervals form a small covering chain, and which runners are essential away from peaks? |
| 4 | Integer-lattice geometry | Polyhedra and zonotopes were read about and mapped, but not constructed for our examples. Can an integer-point or width argument explain feasibility or boundary-only contact? |

Graph-coloring and lattice-geometric connections are established parts of the literature, as described in S1 Sections 3.3–3.5 and S10. Our proposed interval-overlap graph is a particular construction to investigate; it is not asserted to be identical to the survey's distance-graph coloring formulation. Any coverage graph must retain interval positions and open/closed endpoint information: overlap adjacency alone loses valid isolated contacts.

### A small exact preview of the first two models

For Fibonacci relative speeds at a **fixed physical time** t, two consecutive phases determine the next one:

$$T(x,y)=(y,x+y\pmod1),\qquad
A=\begin{pmatrix}0&1\\1&1\end{pmatrix}.$$

The distinct positive speed list begins 1,2, so the initial phase pair is `(t,2t mod 1)`. Iterating T advances through the speed list; it does **not** advance physical time. A prefix meets a target delta exactly when all its phase coordinates stay in the closed interval `[delta,1-delta]`. The initial pair is restricted to that one-parameter line; it is not an arbitrary point of the two-dimensional torus.

Direct integer multiplication gives

$$A^5=\begin{pmatrix}3&5\\5&8\end{pmatrix},\quad
A^7=\begin{pmatrix}8&13\\13&21\end{pmatrix},\quad
A^9=\begin{pmatrix}21&34\\34&55\end{pmatrix}.$$

Their diagonal sums are 11,29,76, the observed Lucas denominators, and their diagonal entries are the corresponding two observed peak-time numerators. This suggests examining how the recurrence and its admissible phase trajectories generate extremal times. The matrix identities alone do not show that these times are admissible or maximizing.

Separately, exact continued-fraction evaluation confirms that `3/11,8/29,21/76` are alternating convergents (indices 4,6,8, with the initial 0 indexed as 0) of

$$\alpha=[0;3,1,1,1,\ldots]
=\frac{1}{2+\varphi}=\frac{5-\sqrt5}{10},\qquad
\varphi=\frac{1+\sqrt5}{2}.$$

For example, `[0;3,1,1,1]=3/11`; adding two more trailing 1s gives 8/29, and two further 1s gives 21/76. These exact arithmetic identities re-express the observed finite Fibonacci/Lucas pattern. They are not independent evidence that the maximum formula continues, nor a proof that actual maximizing times converge to alpha. Those require controlling the full prefix constraints.

Recommended next investigation: combine the two-coordinate recurrence with the continued-fraction candidates, seeking an upper bound and a matching feasible witness. No new speed-set computation, graph construction, or lattice construction was performed for this shortlist. The only new checks here were the three matrix powers and three continued-fraction evaluations.

**Continuation completed:** [Explaining the Fibonacci plateaus](FIBONACCI_RECURRENCE.md) combines small-subset upper bounds with exact witnesses through 21 total runners. The subsequent source check identifies the general formula as an established result (S11), with a matching modular construction (S12). Our own interval reconstruction remains unreviewed. At the limiting time, advancing through Fibonacci runner indices approaches a four-phase cycle with a shrinking error; this supplies a concrete use of the recurrence model. Eight nearby speed controls distinguish the residue mechanism from mere proximity of speeds. Graph and lattice certificates remain unimplemented.

**September 23 update:** Vance explicitly asked that Fibonacci not constrain our direction. The detour is complete for present purposes. [Blocking chains beyond Fibonacci](BLOCKING_CHAINS.md) now implements the interval-graph model: vertices are blocking windows, directed edges preserve strict overlap and advance the covered endpoint, and shortest paths certify minimum chains. Forty-six components across eight fixed inputs agree with a separate greedy construction. Window counts alone do not distinguish tightness. The new 13-to-8 control also removes the common modulo-8 witness, linking the graph gaps to a broader arithmetic question about times whose small denominators are all blocked. Integer-lattice certificates remain unimplemented.

## September 25: LTCMs and runner thought experiments

**LTCM — Languages That Carry Models** is Vance's working term for structured ways to express objects, relationships, constraints, and predictions. It is a project term, not an assertion that mathematical disciplines are trained computational language models. A domain names a subject area; an LTCM identifies a representational language we can use within or across subjects. For each translation ask what it preserves, what it suppresses, and what additional inference it permits.

The proposed interpretation of "perhaps the runners are not actually separate" is to study one joint configuration with many phase coordinates. The runners remain dynamically noninteracting; their phases are constrained by one time parameter, the common start, and fixed speeds. For seven integer relative speeds the ambient torus has seven coordinates but the motion is a closed one-dimensional orbit. This reuses our existing geometry, not a newly added physical dimension.

The "sealed room" metaphor motivates looking for information inaccessible in a compressed representation. Here a concrete candidate is compatibility among individual and pairwise blocking events. The mathematical object is the joint configuration and its constraints; no new physical field, gravitational influence, quantum entanglement, or universal law of synergy is inferred.

| LTCM to pursue | Position before this continuation | Question it could answer |
| --- | --- | --- |
| Integer lattices and polyhedra | Established sources read (S10); not constructed for our principal examples | Which phase/lap combinations share a possible time? |
| Multivariate information theory | Not applied; S19 supplies an introductory source | Which information about a chosen target is available jointly rather than individually? |
| Higher-order intersection structures | Specific triple tests exist, but no systematic treatment | Which pairwise possibilities cannot coexist as a larger group? |
| Constraint satisfaction and optimization | Partial ingredients, no general selection procedure | What small extra condition rules out an artificial complete-cover arrangement? |

The following thought experiments separate exact translations from intentional changes of problem.

1. **Independent clocks, then one clock.** With reference 0 and moving speeds 1,2, separate times can put both movers at phase 1/2. A common time enforces `theta_2=2 theta_1 mod 1`, excluding that point. The actual target `[1/3,2/3]^2` remains attainable at the two previously certified corner contacts `t=1/3,2/3`. Independent clocks are a relaxation, not the original conjecture.
2. **Preserve summaries, change the joint arrangement.** Ultra's abstract distribution for extras 6,7,11,16 preserves every single/pair blocking duration in J=`[9/32,3/8]` but removes the actual `1/896` opening. It is an abstract event distribution, not a demonstrated common-start speed configuration. Test which additional compatibility information it violates.
3. **Change the observer.** Adding the same speed to every original runner preserves all relative distances. Changing the selected reference is a separate operation: selected-reference feasibility must still be checked for that runner. Classical reference frames provide useful invariant language.
4. **Release the common start.** Give the runners independent initial phases. This changes the allowed trajectories and the problem. Compare which phase identities gain nonzero constants; do not transfer a shifted-start conclusion back without an argument.

Spacetime can depict trajectories on a time-by-track cylinder. Relativistic or gravitational mechanisms have not been mapped to the prescribed constant-speed problem. The useful criterion for any analogy is an explicit preserved observable or a testable extra constraint.

Information-theoretic synergy requires selected random variables, a probability measure (for example uniform time on a specified window), a target, and a decomposition convention. No such numerical decomposition has been performed. Pair-marginal insufficiency alone does not establish a particular synergy value. Measures of duration also miss isolated valid times, so the equality route must survive any statistical translation.

**Continuation:** [Lap-labelled constraints](LAP_LABELLED_CONSTRAINTS.md) carries out experiment 2. The lost distinction is which occurrence of a runner's blocking interval participates in each pair overlap. Restoring that distinction excludes the artificial triple and gives exact forest certificates for the five existing local controls. This connects the earlier interval-chain LTCM with the overlap LTCM; it is not a new general existence theorem.

**Further continuation:** [The two-speed transfer](TWO_SPEED_SPARSE_TRANSFER.md) constructs an explicit local lattice model: two integer lap labels must lie in a rectangle and satisfy `|ym-xn|<(x+y)/8`. This tests common-time compatibility, rather than adding independent physical dimensions. A two-window rule bounds the smaller-speed lap list and selects a compact certificate for the already-studied two-variable family. The general Lonely Runner polyhedral/zonotope construction remains unimplemented. The same continuation identifies an infinite family with a genuinely empty first window, separating missing model information from an unsuitable window.

**Quantitative continuation:** [Four-blocker cycle corrections](FOUR_BLOCKER_CYCLE_CORRECTIONS.md) distinguishes whether a joint event is possible from how long it lasts. Graph cycle rank measures overcounting; disconnected active states explain the gap after that correction. In the 56/64/72/113 example, shared-clock phase bounds exclude a triple; replacing 113 by 112 makes all four blockers overlap, so a useful cyclic certificate must pay for that duration. These are exact relations within a mathematical representation, not a physical field or a measured information-theoretic synergy. The bounded comparison improves certificates for already-studied inputs and leaves speed-uniform computation and general selection open.
