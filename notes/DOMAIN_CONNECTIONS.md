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
