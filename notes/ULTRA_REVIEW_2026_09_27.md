# Ultra review — what the distinctions now tell us

September 27, 2026. Reviewed baseline: `e94a87f650264826569cae63412c43a5175f5ae4`, on `research/near-doubling-overlap-2026-09-24`, draft PR #3. Six fresh-context GPT-6 Astra reviewers used Ultra reasoning, divided among arithmetic, geometry, optimization, rigor, literature, and strategy. The coordinator integrated the results and supplied the threshold-profile argument below. Material AI involvement includes all these activities and the verification code.

**Assessment:** the central distinction-audit calculations survived separately structured reconstruction. The review found useful stronger statements, several limits on what they imply, and a better-defined next question: **how do we select one place where a witness can be certified?** We have not proved Lonely Runner or established novelty. Bounded calculations are OBSERVED / REPRODUCED in their specified scopes. Internally derived unbounded statements below remain HYPOTHESIS / proof candidates under [CLAIM_STATUS.md](../CLAIM_STATUS.md).

This review builds on the [September 25 Ultra review](ULTRA_REVIEW_2026_09_25.md); it does not repeat every earlier proof review. No reviewer individually audited the entire repository. Separate AI assignments and exact arithmetic do not constitute outside referee acceptance.

## 1. The main correction in perspective

The strongest recent example is

\[
v_h=(1,3,4,5,10,28,1680h),\qquad h\ge1,
\]

with reference 0, eight total common-start runners, threshold \(\delta=1/8\), core \(1,4,5\), and \(J=[9/32,3/8]\). Let \(F_J\) be the closed allowed set and \(U_J\) its duration. All subset blocking durations on J agree for every h, but

\[
F_J(v_h)=\begin{cases}\{9/32\},&h\text{ odd},\\\varnothing,&h\text{ even}.\end{cases}
\]

The review strengthens the matching: **all 128 joint blocking durations on the full period [0,1] also agree**, including the core constraints. The reason is the common fixed-event grid of denominator 3360. Every variable runner spends exactly one quarter of each fixed-state region blocking. The six fixed runners leave total duration \(15/112\), so every h has full-period allowed duration

\[
U_{[0,1]}(v_h)=\frac34\frac{15}{112}=\frac{45}{448}>0.
\]

The fixed duration was computed by two independently implemented exact partitions/intersections. The all-h factorization has the elementary argument in the arithmetic report. This is a failure to recover **local existence and topology** from these summaries. It is not a full-period empty-versus-nonempty example, and does not show that a proof of global existence must recover all local detail.

There is also a direct global selector. At \(t_0=11/64\), every fixed runner is at least \(9/64\) away. Choose m nearest to \(yt_0-1/2\) and set \(t_y=(m+1/2)/y\). Then

\[
|t_y-t_0|\le\frac1{2y},\qquad
\min_v\|vt_y\|\ge\min\left(\frac12,\frac9{64}-\frac{14}{y}\right).
\]

Every \(y>896\) therefore has a strict witness. For \(y=1680h\), the bound is at least \(127/960=1/8+7/960\). This is the existing slow/fast perturbation mechanism applied explicitly, not a new general principle. It gives a demanding control for any proposed selection rule: the troublesome J is unnecessary for these configurations.

## 2. What our summaries provably omit

| Retained information | Exact control | Omitted information / conclusion |
| --- | --- | --- |
| Labelled single and pair durations | Fixed extras 6,7,11; y=45 versus 90 | U differs: 1/210 versus 31/5040. Quantitative triple mass supplies the difference. |
| Those durations, blocker-pair gcds, and the entire positive Boolean support | Same fixed extras; y=266 versus 532 | U differs: 13/2128 versus 1/152. Knowing which states are possible still does not determine how long they occur. |
| Every subset duration on J and [0,1], and all pair gcds of moving constraints | v1 versus v2 above | Local nonemptiness differs, although global duration is the same positive 45/448. |
| Every opposing threshold-contact time and its equality-controller labels/directions | Same 1680/3360 pair | The contact at 9/32 is strictly safe for the fast runner in one case and strictly blocked in the other. Candidate geometry is not full feasibility. |
| Orbit-closure dimension | Rational speeds (1,2+1/N), odd N, versus (1,2) | All closures are one-dimensional; global optima are 1/2 versus 1/3. Winding and observation horizon matter. |

All examples retain the original runner count and threshold when constraints are selected or repeated. The 266/532 row does **not** retain gcds with every core speed; the gcd with 4 changes. None of these rows says the complete integer relation lattice or complete zonotope is the same.

The full joint-duration vector is the histogram of instantaneous blocking states. At a uniform random time it determines every statistic of that Boolean state, including its entropy. It loses temporal order, location, and isolated points. In the 1680h family the variable blocking bit is independent of the entire fixed Boolean state. This is observable independence under uniform time, not independent phase trajectories: all coordinates still share one clock.

That observation bounds an information-theory approach. Repackaging the same histogram cannot distinguish the contact. A useful new quantity must change the retained information: time conditioning, a phase/residue label, signed endpoint data, or a variable threshold. No partial-information decomposition or numerical synergy measure was performed.

## 3. Exact optimization separates qualitative from quantitative repairs

The optimization reviewer treated the 16 exact blocking-state durations as nonnegative variables. Fixing the single/pair moments gives a linear program for the smallest and largest possible uncovered duration. Floating-point optimization was used only to discover candidate bases. The archive contains **244 exact rational primal/dual certificates across ten prescribed controls**, replayed without an optimizer.

* **6,7,11,16:** pair information permits U=0. The single extra exclusion \(T_{6,11,16}=0\) raises the optimal lower bound to the actual \(1/896\). This isolates the useful geometrical fact from other exclusions that add nothing.
* **6,7,11,266/532:** both actual inputs have exactly the same 12 positive states; only states containing both 6 and 7 are absent. Those zeros are already forced by their zero pair overlap. Every true Boolean support restriction consequently adds no information to the pair relaxation. The mass \(H=T_{6,11,y}+T_{7,11,y}\), not merely its presence, recovers U. Requiring the remaining states to be strictly positive still gives no better infimum without quantitative lower bounds.
* **56,64,72,113:** the optimal pair-only bound is \(63239/3644928\), exceeding the best-tree bound \(58073/3644928\). One optimal inequality is

\[
U\ge |J|-\sum D_i+O_{56,64}+O_{56,72}+O_{64,113}+O_{72,113}-O_{56,113}.
\]

  It uses a four-cycle with a subtracted diagonal. Thus “best tree” is not synonymous with “best consequence of pair data.” Adding the known zero triple \(T_{56,64,113}=0\) improves the bound further, to \(72311/3644928\).
* **3,10,28,1680/3360:** pair data already force U=0 in both. Higher moment order cannot repair their differing local existence.

These are optimal inequalities for the specified abstract event-mass relaxations. Feasible LP mass tables are not automatically realizable by constant-speed runners. The physical examples and the abstract optimization claims remain distinct.

## 4. A contact selector, with an explicit completeness condition

For threshold \(1/n\), positive integer speeds u and v can hit opposite safe boundaries at the same time exactly when

\[
n\mid\frac{u+v}{\gcd(u,v)}.
\]

Write \(g=\gcd(u,v),a=u/g,b=v/g\). Under that condition \(a\) is invertible modulo n. The orientation where u hits \(1/n\) has progression

\[
t=\frac{nj+c}{ng},\qquad c\equiv a^{-1}\pmod n.
\]

Use the reversed orientation too. **If U_J=0 is already known**, these progressions, together with J's endpoints, are a complete candidate list: any surviving interior singleton must have both a lower and an upper safety controller. Every candidate must then pass every runner's inequality.

For the whole 1680h family the only qualifying fixed pairs are \(\{3,5\}\) and \(\{4,28\}\), and no fast-runner pair qualifies. Their candidates in J are exactly its two endpoints. This gives a family-wide two-candidate selector, followed by the modular test that keeps the left point precisely when h is odd.

Three limitations are material:

1. Opposing equality controllers alone do not certify a point; another runner may strictly block it. Replace the loose instruction “retain all active constraints” with **evaluate all constraints, retaining the active ones and every other runner's slack**.
2. A point isolated only by clipping to J may have a single controller. This is why the window endpoints must be checked separately.
3. Without U_J=0, opposing-boundary candidates can miss positive intervals. Even with zero duration, unrestricted candidate counts need not be small: at n=4, the pair q,3q produces 2q times in a full period. A symbolic progression still leaves modular feasibility to solve.

The geometry report also constructs an endpoint-sensitive inclusion-exclusion channel: on a common event stratification, use “included vertices minus included open edges.” For a closed allowed set this is its number of components, including isolated points. Signed contributions for open blocking sets are essential. This is exact but, if the entire stratification is built, does not improve candidate selection or complexity.

## 5. A productive extra dimension: change the separation threshold

Define

\[
G_J(y)=\max_{t\in J}\min_{v\in(1,3,4,5,10,28,y)}\|vt\|,
\quad
W_y(\varepsilon)=\left|F_J(1/8-\varepsilon)\right|.
\]

Complete moments at one threshold do not determine this threshold-response function. The literature reviewer independently found the first four maxima; the coordinator derived the following all-h candidate and checked its exact component lists separately. The geometry reviewer checked the local inequalities.

For \(y=1680h\), put \(\varepsilon_c=3/[8(y+3)]\). Then

\[
G_J(y)=
\begin{cases}
1/8,&h\text{ odd},\\
y/[8(y+3)],&h\text{ even},
\end{cases}
\qquad
W_y(\varepsilon)=
\begin{cases}
\varepsilon/28,&h\text{ odd},\\
0,&h\text{ even},
\end{cases}
\quad(0\le\varepsilon<\varepsilon_c).
\]

Thus an isolated valid instant expands immediately when the threshold is lowered. An even-family near miss requires a positive relaxation first. The deficit tends to zero with y, so a fixed-resolution plot or a fixed positive list of relaxations cannot separate the entire family.

### Derivation and endpoint checks

Write \(a=9/32,b=3/8,\delta=1/8\). For \(0\le\varepsilon\le\varepsilon_c\), the six fixed constraints allow exactly

\[
[a,a+\varepsilon/28]\ \cup\ [b-\varepsilon/3,b].
\]

To see that nothing in the middle survives, use the blocking intervals of 28, 10, and 3 in that order. Their adjacent overlaps have lengths

\[
3/1120-\varepsilon(1/28+1/10),\qquad
1/48-\varepsilon(1/10+1/3).
\]

Both stay positive: their cutoffs are 3/152 and 5/104, far above \(\varepsilon_c\le3/(8\cdot1683)\). The first interval begins at \(a+\varepsilon/28\), the last ends at \(b-\varepsilon/3\). Direct linear phase substitution verifies all six fixed inequalities in the two remaining endpoint intervals.

At the left endpoint, y has phase 0 for even h and phase 1/2 for odd h. Throughout the left interval its phase displacement is at most \(y\varepsilon/28<3/224\). Consequently that whole interval is blocked for even h and safe for odd h. At the right endpoint y has phase zero for all h. On the right interval its distance is at most \(y\varepsilon/3\), which is less than \(\delta-\varepsilon\) precisely when \(\varepsilon<\varepsilon_c\).

At \(\varepsilon=\varepsilon_c\), the right interval first meets y's safe set at

\[
t_*=b-\frac1{8(y+3)},\qquad
\|3t_*\|=\|yt_*\|=\frac{y}{8(y+3)}.
\]

All other fixed constraints are safe there. This proves the even branch has no point above that level and attains the level. The odd branch attains \(\delta\) at a, and the fixed constraints already preclude a larger value on J. At zero relaxation, the two zero durations still correspond to different closed sets.

The root checker verifies h=1,2,3,4 at relaxations \(0,\varepsilon_c/2,\varepsilon_c,2\varepsilon_c\), including the singleton birth and complete clipped component lists, plus infeasibility just above the asserted even maximum. The finite checks support the written argument; they do not substitute for it. Values for even h=2,4 are \(140/1121\) and \(280/2241\).

More generally, continuity on a nondegenerate compact J gives

\[
F_J(\delta)\ne\varnothing
\quad\Longleftrightarrow\quad
|F_J(\delta-\varepsilon)|>0\text{ for every }0<\varepsilon<\delta.
\]

A point at level δ has a positive one-sided neighborhood at every smaller level. Conversely, an empty level-δ set has maximum strictly below δ. This repairs existence in principle by retaining threshold dependence. It supplies neither a finite uniform threshold menu nor a proof that the maximum reaches 1/n.

## 6. LTCMs worth using, and what they must carry

Vance's “Languages That Carry Models” is useful as a working label. The review favors representations with explicit retained information and falsification tests.

| LTCM | Concrete mathematical object | Useful information | Limit to preserve |
| --- | --- | --- | --- |
| Integer-lattice geometry | \(P_J=Jv-[\delta,1-\delta]^k\), with integer point m | Closed feasibility and the exact time fiber for that lap vector | Full integer-point enumeration can recreate the old checker. |
| Modular arithmetic | Opposing-contact progressions and all-runner residues | Equality, repetition, and the candidate's actual safety | A fixed list chosen before all speeds can be defeated. |
| Piecewise-linear geometry | Threshold maximum, contact locations, one-sided slopes | How isolated contact expands, and the size of a near miss | Exact profile complexity and tiny deficits still need control. |
| Convex optimization | Nonnegative state masses, moment constraints, rational duals | Best bound from declared data; value of each extra restriction | Abstract masses need not be physically realizable. |
| Dynamics / relation lattices | \(\Lambda(v)=\{m\in\mathbb Z^k:m\cdot v=0\}\), auxiliary torus, quantitative return | The shared clock and relations among phase coordinates | Dimension or orbit closure alone does not guarantee hitting a boundary target. |
| Topology / signed cell counting | Endpoint-sensitive Euler data | Components and isolated points erased by duration | Constructing all cells gives no automatic compression. |

The lattice formulation has a direct exact certificate. For integer m, its fiber is

\[
J\cap\left[\max_i\frac{m_i+\delta}{v_i},\ \min_i\frac{m_i+1-\delta}{v_i}\right].
\]

It retains a singleton when the endpoints meet. The usual global projection along v loses which window contained that fiber unless time is retained. [The literature report](../reviews/2026-09-27-ultra/literature.md) connects this to Beck–Hoşten–Schymura's closed-cube formulation. It also separates common-start central minimum from the stronger shifted covering-radius problem. These established translations are not claimed as our discoveries.

For the “perhaps the runners are not separate” intuition, the precise current model is the common-time orbit inside phase space. A candidate contact is an intersection of constraints; no one runner carries its feasibility. An auxiliary torus can have higher dimension than the actual orbit, but the actual orbit remains constrained by its arithmetic winding. This gives the proposed relationship-space idea a mathematical object and tests; it does not require a physical field, gravity, or relativistic dynamics. No benefit from importing those additional physical laws has been demonstrated here.

Two completed thought experiments make the distinction concrete:

* A finite rational time menu chosen from slow runners can always be blocked by an added speed divisible by every menu denominator. Adaptive half-phase rounding escapes this trap whenever a strict slow margin is available.
* For odd N, relative speeds \((1,2+1/N)\) attain separation 1/2 at \(t=N/2\), while their limit \((1,2)\) has maximum 1/3. On a fixed horizon \([0,T]\), the distance functions differ by at most T/N; reaching 2/5 requires \(T\ge N/15\). The dimension stays one. The clock scale changes. For irrational perturbations, distinguish a supremum from an attained maximum.

The arithmetic review supplies one further exact repair. On \(K=[9/32,9/32+1/6720]\), the variable block duration equals \(1/26880\) for every even h, and differs by \(1/(26880h)\) for every odd h, with sign determined modulo 4. Thus one well-chosen new window detects the lost parity exactly. Its separation tends to zero. **Exact identifiability and robust identification are different questions.** A general rational-grid aliasing lemma and finite residue criterion in that report explain both the collisions and when this sort of repair can work.

## 7. Three next investigations, in order

### A. Test whether our certificate can succeed somewhere

Move from a designated bad window to an explicit selection hypothesis: whenever an eight-runner reference has strict lonely time, does some three-constraint core and one of its complete safe components give a positive best-tree bound on the remaining four constraints? Preserve threshold 1/8. Start with the named controls already in the repository, exhaust the 35 cores where seven absolute relative speeds are distinct, and record every component's bound together with an independently verified global witness. Handle repeated absolute constraints and changed references explicitly.

One exact strictly lonely case with every candidate bound nonpositive disproves this precise hypothesis. If found, apply the optimal pair LP to the same failed components to distinguish an insufficient tree formula from insufficient pair information. If all named inputs pass, that is only bounded evidence; the next target is a structural selector for a stated infinite class. The fixed-core 16 example already passes in other windows, so repeating its one-window failure would teach nothing new.

This is the highest-value next global experiment. The point is to determine whether certificate **content** can succeed before investing in fast certificate **selection**. Tight equality-only configurations require a separate contact branch and cannot falsify a strict-duration hypothesis.

### B. Transfer the contact/threshold repair beyond its anchor

For the existing equality controls and matched-duration pairs, record each candidate's lap vector, opposing controllers, all-runner slacks, one-sided slopes, and threshold deficit. Compare the progression selector with the complete closed-interval benchmark. Count generated candidates and arithmetic bit sizes separately from checking cost.

Seek a finite residue-and-slope formula for one additional parameter family. Reject any proposed small record if two configurations match it but differ in its declared target. Reject a proposed uniformly short candidate list if growing-gcd controls make it grow. Jain–Kravitz's rational-grid piecewise-linear framework is relevant precedent; the local adaptation still requires its own proof.

### C. Join relation geometry to a quantitative clock bound

Try a transfer statement of the form “auxiliary strict margin η plus a stated arithmetic approximation bound produces an actual witness by time T.” Require it to recover the existing affine rounding estimate and the simple half-phase selector. Test it against the rational perturbation example and boundary targets not attained by a dense orbit.

Stress the coefficient quantifier. Writing the tight speeds 4,5,6,7 as \(q+(4-q),\ldots,q+(7-q)\) allows arbitrarily large q without creating strict loneliness. The offsets vary with q and the old sufficient inequality fails. A useful uniform statement must compare coefficient growth, approximation error, and shrinking margin explicitly. An eventual theorem for each fixed tuple is not an arbitrary-configuration theorem.

The +7/+9 offset extension remains parked. Further blind searches for another moment collision are lower priority: the specified insufficiency questions now have exact physical answers.

## 8. Review evidence, sources, and remaining limits

| Assignment | Report | Principal bounded verification |
| --- | --- | --- |
| Arithmetic | [arithmetic.md](../reviews/2026-09-27-ultra/arithmetic.md) | Two complete full-period state laws; 96 grid controls; exact parity-window and chronology controls |
| Geometry | [geometry.md](../reviews/2026-09-27-ultra/geometry.md) | 8,192 oriented pair identities; four duration/Euler tables; clipped and third-controller controls; direct large-h selectors |
| Optimization | [optimization.md](../reviews/2026-09-27-ultra/optimization.md) | 244 rational primal/dual certificates on ten prescribed physical controls |
| Rigor | [rigor.md](../reviews/2026-09-27-ultra/rigor.md) | 35 cases, 27 complete archive comparisons; original 2,775-input audit; both 118- and 34-family residue classifications |
| Literature | [literature.md](../reviews/2026-09-27-ultra/literature.md) | Seven primary-source records with reading limits; four independently calculated local maxima |
| Strategy | [strategy.md](../reviews/2026-09-27-ultra/strategy.md) | Adaptive witnesses, finite-menu obstruction, rational perturbations, reference and moving-coefficient controls |
| Coordinator | [root_check.py](../reviews/2026-09-27-ultra/root_check.py) | Four full-period controls and threshold component profiles, with independent global witness substitution |

Reproduce the six executable groups, without rewriting archives:

```bash
python -B reviews/2026-09-27-ultra/verify.py
```

The literature reading is documented, not automatically replayed. Counts overlap and are not counts of independent discoveries. No existing checker or research analysis implementation was changed; the broad regression suite was not repeated. The rigor archive's source hashes describe its pinned review inputs, including the pre-update handoff; they are not requirements that future governance files stay unchanged. The package manifest pins the new artifacts separately.

The dated source record is in [SOURCES.md](SOURCES.md) and the literature archive. The current Allikvere arXiv record was rechecked as v2, September 24, 2026, reporting fourteen and fifteen runners; its full proof and computational certificates were not audited. No exhaustive novelty search, human correctness certification, outside outreach, or main-branch merge occurred.

The remaining mathematical gap is explicit: local certificates and fixed-family transfer arguments do not yet give a sufficiently general rule selecting a surviving witness for an arbitrary configuration and every reference. The review improves the representation and the tests we can put that missing rule through.
