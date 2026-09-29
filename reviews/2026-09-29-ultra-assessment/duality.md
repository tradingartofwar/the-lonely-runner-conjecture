# Ultra assessment: relations, dual certificates, and the equality boundary

September 29, 2026. Pinned repository head: `7b0101376e00dbb71537d3a62e39ec75cee113cc`. Assigned review: alternative representations with a mathematical payoff. Material AI involvement: this report's derivations, criticism, and literature comparison. No executable mathematical calculation was run. Static repository reading and primary-source retrieval only.

**Status:** the elementary deductions below are **HYPOTHESIS / proof candidates**, not independently certified results. Existing exact records retain **OBSERVED** status. No novelty claim is made.

**Correction added during team review:** the proposed P2 strict-existence target in Section 4 is already implied by established lower-runner results. A rational vertex of the relaxed speed subspace merges several speeds, giving a lower-runner witness in the relaxed torus; the argument is recorded in Section 7 below and in `arithmetic.md`, Section 6. The literature reviewer also located the conditional conclusion in Allikvere v2, Lemma 3.3, attributed there to Giri–Kravitz. That source was located by the other reviewer, not independently inspected in this report. P2's original proposal is preserved as development history, not as a remaining open problem. The current recommendation is an actual-orbit-preserving additive-core lift, or a quantitatively useful transfer estimate beyond existing bounds; bare relaxed-torus feasibility is not a new research milestone.

## Assessment

The strongest retained mechanism in this direction is the critical-duty averaging argument: an exactly normalized positive kernel, plus strict-overlap topology, rules out a sufficiently long blocking chain. It supplies a finite local selection bound. The exact missing implication remains that the physical configuration must supply a suitable core window, compatible collection of windows, or equality witness on its actual orbit. Improving a local representation does not supply that implication by itself.

A useful alternative representation is the **whole integer relation module**, not the existence of one short relation. Fourier averaging makes this distinction exact. A supplied safe core gives a positive baseline; destroying it forces a short relation involving additional coordinates. A second deduction below shows that **one independent relation added to the core `{1,4,5}` cannot itself destroy strict safe mass in the relaxed phase space**. Subsequent team review supplied the stronger correction: every proper relation relaxation here has strict safe points by known lower-runner results. The value would therefore lie in useful quantitative mass or transfer bounds, not another relaxed existence theorem. Nothing here currently gives a smaller remaining parameter box or a new existence conclusion.

There are two firm warnings. First, a short-relation theorem applied directly to this family is vacuous: `1+4-5=0` already supplies the relevant short odd relation. Second, an integral that only lower-bounds safe duration cannot certify the tight control's isolated points. Threshold continuation repairs the second representational loss, but without a new inequality it is equivalent to the original existence problem.

## 1. What the current duals see and miss

The short-kernel note proves its candidate by averaging `M-1`, where `M` counts four quarter-duty blockers. The full kernel has zero signed excess at every translate. If a strict chain covers its entire support, an overlap has positive kernel mass, giving a contradiction. This uses **placement, positivity, and strict endpoints together**; it is stronger than knowing only total duration.

The same note's Section 5 provides an unusually useful failure certificate. For residuals `{6,7,11,16}` on `J=[9/32,3/8]`, every translate of the stated wide-box mixture with positive mass on `J` has positive truncated signed excess, although `[17/56,39/128]` survives. Hence another translation search within this class cannot help. Localizing the kernel more finely changes the certificate class and its proof obligations.

The all-order event LP has a separate limitation. Even if every atom mass is retained, measure-zero safe points disappear. The joint-triple note correctly records that every duration LP for tight13 has optimum zero while `t=3/8` remains safe. This is not evidence that a different moment inequality should recover positive duration.

Two precise no-go statements are worth retaining:

1. If a certificate is `integral F(t) dt > 0`, with `F <= 1_safe` almost everywhere, it cannot certify a zero-duration safe set. The obstruction persists with any absolutely continuous weight.
2. A trigonometric polynomial `P>=0` that is required to vanish at every unsafe time is identically zero for every nontrivial common-start runner configuration: an open interval around the common start is unsafe, and a trigonometric polynomial vanishing on an interval vanishes identically. A nonnegative finite polynomial cannot be an exact supported safe-window function.

These do **not** rule out sign-changing trigonometric minorants, spectral bounds on the maximum separation, atomic endpoint certificates, threshold limits, or a zero-integral argument supplemented by strict-cover topology. In particular, the kernel's own equality-sensitive contradiction is not refuted by the first statement.

## 2. An explicit relative short-relation deduction

Let `v=(c_1,...,c_s,u_1,...,u_r)` be distinct positive integers, with `k=s+r`, and choose a threshold `0<delta<1/2`. Set `h=1/2-delta`.

Use the cosine-autocorrelation window from Beck–Everett, Section 2:

`W_h(x)=sum_j (-1)^j a_j exp(2 pi i j x)`,

where `a_j>=0`, `sum a_j=1`, `sum j^2 a_j=1/(4h^2)`, and `a_0=8h/pi^2`. The window is positive exactly for `||x||>delta`. Its Fourier series is absolutely convergent. Define

`A=integral_0^1 product_{i=1}^s W_h(c_i t) dt`.

Assume **A>0**, which is equivalent to a strictly safe time for the supplied core. Let

`L(v)={m in Z^k : m dot v=0}`,

`L_C={m in L(v) : m_{s+1}=...=m_k=0}`.

**Relative extraction candidate.** If `v` has no strictly delta-safe time, there exists `m in L(v)\L_C` with odd coordinate sum and

`||m||_2 <= sqrt(k)/(2h sqrt(A a_0^r))`,

`||m||_1 <= k/(2h sqrt(A a_0^r))`.                         (R)

Here “outside the core” means at least one residual coefficient is nonzero. It does not mean independent of every relation the project has already retained.

**Derivation.** Write `w(m)=product_i a_{m_i}`. Absolute convergence gives

`integral product_i W_h(v_i t) dt = sum_{m in L(v)} (-1)^{sum m_i} w(m)`.

The contribution of `L_C` is exactly `A a_0^r`. With no strict safe time the left side is zero, so the total weight of odd-sum relations in `L(v)\L_C` is at least `A a_0^r`; even-sum additional relations only increase the cancellation required. Also

`sum_{m in Z^k} ||m||_2^2 w(m)=k/(4h^2)`.

Weighted averaging therefore supplies one such odd relation with squared norm at most `k/(4h^2 A a_0^r)`. Cauchy–Schwarz gives the stated 1-norm bound. This proof uses a second moment rather than an unproved tail truncation. It handles the real upper bound directly; a larger rounded integer cutoff is optional.

### Explicit specialization to the live core

For `c=(1,4,5)`, `delta=1/8`, and `h=3/8`, take

`I=[21/64,27/80]`, with `|I|=3/320`.

Each of `t,4t,5t` modulo one lies in `[5/16,11/16]` on `I`. The autocorrelation formula, with `z=||x-1/2||/h`, is

`W_h(x)=(1-z)cos(pi z)+sin(pi z)/pi` for `0<=z<=1`.

It decreases on this interval; for `z<=1/2`, it is at least `1/pi`. Thus

`A >= 3/(320 pi^3)`,

`A a_0^4 >= 243/(320 pi^11)`.

Any seven-speed instance in the family with no strictly safe time consequently has an odd relation involving at least one of `a,b,c,d`, with

`||m||_1 <= (28/3) sqrt(320 pi^11/243)`.                  (R145)

The expression is deliberately left exact. This is a loose explicit specialization of established inverse-Fourier reasoning, not a claimed improvement on the literature's general bounds.

### Why this does not shrink today's remainder

The headline Beck–Everett condition already holds through `(1,1,-1,0,0,0,0)`, of norm 3 and odd coordinate sum. Even the relative bound (R145) is automatically met after the existing `a<=34` reduction:

- If `a` is even, `a e_1-e_a` is an odd-sum cross relation of norm `a+1<=35`.
- If `a` is odd, `4e_a-a e_4` is an odd-sum cross relation of norm `a+4<=38`.

Both are far below (R145). Collecting one additional relation would therefore be activity without a new restriction. The relation's **independence from the full retained module**, and the geometry after imposing it, are the relevant next quantities.

## 3. The full-module version and one actual rank-growth payoff

Let `Lambda` be a saturated subgroup of `L(v)` and let

`H_Lambda={x in T^k : m dot x=0 mod1 for all m in Lambda}`.

This is a connected subtorus containing the actual orbit. Put

`A_Lambda=integral_{H_Lambda} product_i W_h(x_i) dHaar(x)`.

If `A_Lambda>0` but the actual orbit has no strict safe time, the same argument gives an odd relation **outside Lambda** with

`||m||_1 <= k/(2h sqrt(A_Lambda))`.                      (RM)

The Fourier contribution of `Lambda` is now exactly `A_Lambda`. Saturating `Lambda+Z m` increases its rank, because a saturated subgroup already contains every integer vector in its real span. The initial assessment treated positivity of the next Haar mean as the missing induction step. Section 7 corrects that: known lower-runner results already give positivity for every proper relaxation here. What remains missing is a useful quantitative estimate and a transfer to the actual one-dimensional orbit, where strict positivity can fail legitimately.

There is, however, a simple first step specific to the live core.

**One-cross-relation lemma candidate.** Start with the exact core relation module for `{1,4,5}` and add one independent relation, then saturate. If the resulting module is contained in the relation module of an admissible integer tuple `{1,4,5,a,b,c,d}`, its subtorus contains a point with all seven coordinates strictly between `1/8` and `7/8`. In particular, its Haar safe mean is positive.

**Proof.** After imposing the core relations, phase coordinates have the form

`(t,4t,5t,y_a,y_b,y_c,y_d)` modulo one.

The saturated additional equation is

`q t+r_a y_a+r_b y_b+r_c y_c+r_d y_d=0 mod1`,

where `(q,r)` is primitive, `r!=0`, and `q+r dot(a,b,c,d)=0`.

If `||r||_1>=2`, allowing every residual coordinate to range through `(1/8,7/8)` makes `r dot y` range over an open interval of length `(3/4)||r||_1>1`. For every strictly core-safe `t`, this interval contains a value congruent to `-qt` modulo one. Hence a strictly safe point exists.

If `||r||_1=1`, one residual coordinate is fixed as the phase of a single admissible integer speed `|q|`; the remaining three are free. The existing core bound `Q(|q|)<=1/6` leaves at least `3/8-1/6=5/24` safe measure for this four-constraint core. Removing its finitely many threshold points preserves positive measure, so a strict point again exists. This invokes the repository's core-measure proof candidate, rather than claiming a new four-constraint existence theorem.

A strict point has a relatively open neighborhood in the subtorus, of positive Haar measure. This completes the argument.

Thus an absence of strict loneliness forces a **second independent cross relation**, with its coefficient bound supplied by (RM) applied after the first. A finite first-relation bound gives only finitely many first modules; their positive means have a positive minimum. This is a qualitative finite second bound, not an evaluated or useful numerical one. The current small `a,b` region already contains obvious independent relations, so rank growth alone still supplies no claimed pruning.

## 4. Development proposal: two added relations — superseded by Section 7

The next useful claim to attack is:

> **P2 (originally proposed OPEN; now resolved conditionally by known lower-runner results).** For every saturated rank-two subgroup `Gamma` of `Z^5` that annihilates some `(1,a,b,c,d)` with distinct positive admissible speeds, the subtorus obtained by imposing `Gamma` on `(t,y_a,y_b,y_c,y_d)`, together with the core phases `(t,4t,5t)`, contains a strictly `1/8`-safe point.

The original proposal treated P2 as stronger than closed lonely-time existence for the relaxed torus and potentially false. Section 7 corrects that assessment: the available lower-runner theorem already guarantees a strict margin. The warning about the proposed proof method remains valid: the one-relation proof does not extend by replacing interval length with the area of an image, because area does not force the right lattice coset.

Here is an exact, endpoint-sensitive formulation. Write the two equations as

`q t+R y in Z^2`, with `R` a rank-two integer `2 by 4` matrix.

At a fixed strictly core-safe `t`, a closed residual solution exists precisely when some `b in Z^2` satisfies

`z=b-qt-(1/2)R 1 in R[-3/8,3/8]^4`.

Equivalently, for every `lambda in R^2`,

`lambda dot z <= (3/8)||R^T lambda||_1`.                (Z)

This is the support-function characterization of a zonotope, supplied here by taking the maximum of a linear functional over a cube. A strict solution is obtained by using the open cube. The compact closed version preserves equality contacts. An infeasible candidate `b` has a separating linear functional violating (Z); a successful candidate supplies actual phase coordinates. These are reviewable dual and primal objects, not a numerical optimizer's assertion.

**Original falsifier, now superseded:** an admissible rank-two module for which every relevant `b` violates (Z) for every strictly core-safe `t`, or has only boundary solutions. The lower-runner implication rules this out. The affine endpoint formulation still gives a way to verify constructive certificates or quantitative estimates; no counterexample search for P2 is recommended.

**Corrected success criterion:** obtain a useful explicit Haar-mass lower bound or a controlled certificate whose transfer to the actual orbit improves an existing bound. Proving P2 again or finding short vectors without such a consequence does not meet the criterion.

## 5. Threshold continuation recovers what duration erased

Let `f_v(t)=min_i ||v_i t||`, `V=max_i v_i`, and

`mu_v(delta)=measure{t in [0,1]: f_v(t)>=delta}`.

For integer speeds, `f_v` is continuous piecewise affine with finitely many pieces. Its superlevel measure is piecewise affine in the threshold. Suppose its maximum is `R=1/n<1/2`. The maximizing set is finite: no affine piece of the lower envelope has zero slope. At a maximum `t_j`, let `p_j` be the largest active positive slope and `q_j` the largest absolute active negative slope. For all sufficiently small positive `epsilon`,

`mu_v(R-epsilon)=epsilon sum_j (1/p_j+1/q_j)`.          (E)

Indeed, inactive constraints retain a positive margin near `t_j`; on the left the largest active ascending speed controls the minimum, and on the right the largest descending speed controls it. The two local lengths are `epsilon/p_j` and `epsilon/q_j`. Outside small neighborhoods of the finitely many maxima there is a fixed gap below `R`.

Reflection gives a distinct partner for every tight maximum: `t=0` cannot maximize at positive threshold, while at `t=1/2` each integer-speed distance is either 0 or 1/2, never `1/n`. Consequently a tight tuple satisfies

`lim_{epsilon down to 0} V mu_v(1/n-epsilon)/epsilon >=4`.

For a strictly lonely tuple the ratio tends to infinity. For a tuple whose maximum is less than `1/n`, it is eventually zero. Thus, for `n>=3`, the lower-limit inequality with right side 4 is **equivalent to existence**, not an advance toward it. It is a clean quantitative target for a new dual estimate and a useful way to retain the tight case. Its utility depends on deriving the bound without already knowing a safe point or reconstructing the full threshold profile.

Do not differentiate an unsmoothed Fourier series term by term without a convergence argument. The finite piecewise-affine proof above needs no such interchange.

## 6. Literature and reading limits

All sources below were retrieved September 29, 2026. Their runner-count conventions must be translated: this report uses `k=n-1` moving speeds.

- **Beck–Everett, _Lonely Runner Relations_, arXiv:2609.06259v2, September 23, 2026.** Read Theorems 1.1 and 2.1, Lemma 2.2, and the Fourier proof through equation (2.12); also the geometric formulation in Proposition 3.1. The paper gives short odd-sum relations when strict loneliness fails. Its cosine-autocorrelation coefficients provide the analytic input to (R). The relative/module deductions above are specializations developed here, with no novelty claim. [Versioned HTML](https://arxiv.org/html/2609.06259v2).
- **Tao, _Some remarks on the lonely runner conjecture_, arXiv:1701.02048v4.** Read Section 2, Lemma 2.2 and its Fourier argument; Section 3, equation (3.12), Proposition 3.3 and its proof. These already extract arithmetic relations relative to previously selected speeds from enlarged intersection structure. This is clear prior art for the relative-inverse philosophy, though not a claim that its hypotheses coincide verbatim with (R). [Versioned HTML](https://arxiv.org/html/1701.02048v4).
- **Gonçalves–Ramos, _Bounds for the Lonely Runner Problem via Linear Programming_, arXiv:2010.02271.** Read the LP definition, Theorem 1 and its proof, and Section 3's denominator-conditioned lower bound. Their trigonometric-polynomial method bounds maximum separation, including equality, and is not the duration-only ansatz ruled out above. The stronger lower-bound route requires information about a maximizing denominator; importing an oracle denominator would hide the hard step. The PDF also reports degree/feasibility limitations of its basic lower-bound program. No numerical results were reproduced. [Primary PDF](https://arxiv.org/pdf/2010.02271).

These readings do not establish novelty of the one-cross-relation lemma or P2, and do not constitute a full audit of any paper.

## 7. Team correction: proper relaxed tori already have strict points

Let `Lambda` be a saturated relation module in `Z^k`, and let its rational real nullspace `K` have dimension `d>=2` and contain a strictly positive speed vector. Consider

`P={w in K : w_i>=1 for every i}`.

This polyhedron is nonempty after scaling the positive vector. Minimize `sum w_i`. An appropriate sublevel set is compact, so the minimizing face has a rational vertex. At least `d` coordinate inequalities have independent restrictions active there; otherwise a nonzero direction in `K` preserving all active equalities would give a small two-sided perturbation inside `P`, contradicting extremality. Thus at least `d` coordinates of the vertex equal 1.

After merging these duplicates and clearing denominators, there are at most `k-d+1` distinct positive moving speeds. Assuming the corresponding lower-runner Lonely Runner theorem, their orbit has a point with every coordinate distance at least

`1/(k-d+2) > 1/(k+1)`.

The vertex lies in `K`, so this point lies in the relaxed torus defined by `Lambda`. It need not lie on the original speed vector's orbit. This is exactly why relaxed existence does not finish the physical problem.

For P2, `k=7` and `d=3`, so established six-total-runner existence gives margin `1/6>1/8`. For any proper relation relaxation in the current seven-moving-speed problem, `d>=2`, and established seven-total-runner existence supplies at least `1/7>1/8`. Therefore every proper relaxation has positive strict Haar mass. The actual rank-six relation module leaves a one-dimensional torus, where this reduction no longer lowers the number of distinct constraints.

The arithmetic reviewer supplied this vertex derivation; the coordinator and audit reviewer checked it independently at the AI-review level. The literature reviewer located an established statement with this conditional conclusion in Allikvere v2, Lemma 3.3, credited there to Giri–Kravitz. See the integrated literature report for the exact source inspection. The original Section 4 proposal remains above to make the correction visible.

## Corrected recommendation

Retain the exact short-kernel and two-window mechanisms as local tools. Preserve isolated equality witnesses separately. Do not launch a generic polynomial search, another translated-kernel scan, or a census of short relations in the current speed box.

The original recommendation to attack P2's bare feasibility is withdrawn. In this direction, require a quantitatively useful mass bound and actual-orbit transfer beyond known finite-reduction bounds. For the integrated project, prioritize an actual-orbit-preserving additive-core lift: the certificate must constrain the real compatible phases or lap choices rather than certify only a larger relaxed torus. The remaining bridge concerns the original one-dimensional orbit, including its equality contacts. Neither the Fourier reformulation, the known relaxed-torus existence result, nor threshold continuation has supplied that bridge.
