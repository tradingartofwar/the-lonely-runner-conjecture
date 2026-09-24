# Four fast runners sharing an integer clock

For a self-contained statement and proposed proof of the affine-family extension, start with [the review note](REVIEW_AFFINE_FAMILY.md). The development history and broader diagnostics remain below.

**Date:** September 24, 2026. **Status:** HYPOTHESIS/proof candidate for the general argument; OBSERVED for the exact diagnostics; DISPROVEN for the specific necessity claim tested below. AI materially generated the argument and implementation. Independent mathematical review remains outstanding. No novelty claim.

Vance approved continuing the pair-selection question: what arithmetic structure forces enough useful overlap? Sections 1–6 check a tempting local pattern and develop a fixed-offset argument. Sections 7–11 extend it to different integer winding rates, including speed differences that grow with the common parameter. Neither continuation expands a speed-set search or optimizes another cutoff.

## 1. A particular sum relation is not necessary

The six positive-duration components that defeated every single-pair certificate came in three reflection pairs. Their extra speeds included either 6+7=13 or 3+5=8. That suggested checking whether those particular sums explained the successful trees.

Nine prescribed decompositions compare:

- Cores {1,4,8} and {2,3,5}, each with extras {6,7,11,x}, for x=12,13,14.
- Core {1,2,4}, with extras {3,5,6,x}, for x=7,8,9.

Three are the previous cases; six are nearby replacements. We retain every core component and every equality point.

For core {1,4,8}, J=[9/64,7/32], changing 13 to 12 leaves precisely the same valid interval [17/88,7/32], of duration 9/352. Every single-pair bound is still negative, while the tree bound equals the clear duration. Thus the particular relation 6+7=13 is **not necessary** for this opening or its tree certificate. This does not rule out other useful arithmetic relations: 12, for example, is twice 6.

The more general question is how collective overlap can be forced without naming a particular successful pair.

## 2. Separate common rotation from internal spacing

Keep eight common-start runners and selected reference 0. Fix:

- Three distinct positive integer core speeds C={c1,c2,c3}.
- Four distinct fixed nonnegative integer offsets 0=a0<a1<a2<a3.

The four other speeds are

$$q+a_0,\ q+a_1,\ q+a_2,\ q+a_3.$$

Their positions can be written

$$(q+a_i)t=qt+a_i t.$$

The common term qt rotates the group. The offsets a_i t control its internal spacing. Increasing q changes the first rate while leaving the speed differences fixed. Close speeds do not mean close positions at every time.

For the moment, write x for a possible common rotation and consider

$$\|c_jt\|>1/8,\qquad \|x+a_i t\|>1/8. \tag{1}$$

These two coordinates are an auxiliary way to find a safe region. In the actual common-start system, x is constrained by x={qt}. It is not an independently selectable starting phase. Section 4 explicitly realizes a suitable rotation at a nearby actual time.

## 3. Why the auxiliary phase must have a gap

Each core runner blocks exactly 1/4 of a unit time period. Their union therefore blocks at most 3/4. The core leaves a set of measure at least 1/4. Removing the finitely many equality boundaries does not change its measure, so there is a nonempty interval on which all three core inequalities are strict.

At a fixed time t in such an interval, each extra runner forbids an arc of common rotations x of length 1/4, centered at -a_i t. The four arc lengths sum to exactly 1.

Consequently, if the arcs overlap in positive length, their union has length less than 1 and an open safe phase gap remains. Complete coverage in measure requires the four arcs to tile the circle exactly, with centers spaced by 1/4.

This can be seen directly by sorting the four offset positions {a_i t}. Let their four cyclic gaps, counting zero gaps for coincident positions, be g1,...,g4. Their sum is 1. The total strictly safe phase length is

$$G(t)=\sum_{\ell=1}^4\max(g_\ell-1/4,0). \tag{2}$$

Thus G(t)=0 if and only if every gap is exactly 1/4. If the gaps are unequal, at least one exceeds 1/4.

Perfect quarter-spacing implies, in particular,

$$4a_1t\in\mathbb Z. \tag{3}$$

Because a1 is a fixed positive integer, these exceptional candidate times form a finite set in [0,1]. A positive-length core opening cannot consist only of them. Choose a rational t0 strictly inside a core opening and outside this grid. Then choose rational x0 strictly inside one of its safe phase gaps. This yields positive margins

$$\mu_C=\min_{c\in C}\|ct_0\|-1/8>0,$$

$$\mu_A=\min_i\|x_0+a_i t_0\|-1/8>0. \tag{4}$$

Condition (3) is necessary for quarter-tiling, not sufficient. For offsets {0,1,2,3}, t=1/4 does tile: the only allowed phases are the four odd eighths, with no positive margin. At t=13/50, a positive phase gap reappears. For offsets {0,1,5,7}, t=1/4 lies on the candidate grid but two positions coincide; there is a positive phase gap instead of a tiling.

This supplies the forcing mechanism in the auxiliary model: the sum of blocking lengths is fixed, and the only way to avoid duplicate blocking is a rigid equal-spacing pattern that cannot persist throughout a core opening.

## 4. Realize the gap at an actual time

Let M=max(C), A=a3, and let eta be the distance from t0 to the nearer endpoint of its chosen core component. For a positive integer q, choose the nearest integer

$$m_q=\left\lfloor qt_0-x_0+\frac12\right\rfloor,$$

and put

$$t_q=\frac{m_q+x_0}{q}. \tag{5}$$

Then

$$|t_q-t_0|\leq\frac1{2q},\qquad qt_q=m_q+x_0.$$

The distance-to-integer function is 1-Lipschitz. For core speeds,

$$\|ct_q\|\geq\frac18+\mu_C-\frac{M}{2q}. \tag{6}$$

For extra speeds, the large common term becomes an exact integer plus x0:

$$\|(q+a_i)t_q\|=\|x_0+a_i t_q\|
\geq\frac18+\mu_A-\frac{A}{2q}. \tag{7}$$

The last error depends on the fixed offset A, not on q+A. That is the key benefit of separating common rotation from internal motion.

It follows that every integer q satisfying

$$q>\max\left(M,\frac{M}{2\mu_C},\frac{A}{2\mu_A},\frac1{2\eta}\right) \tag{8}$$

has a strict valid time t_q inside the chosen core opening. The first term makes the four large speeds disjoint from the core. The last keeps the rounded time inside the chosen component. All speeds are positive and distinct.

**Proof candidate:** for any fixed core triple C and fixed four distinct offsets as above, all sufficiently large integer q give positive clear duration for reference 0. The same construction works in any chosen positive-length core component, with a component-dependent bound.

This is a proposed infinite implication from the written argument, not an inference from finitely many passing computations. No averaging assumption, random phases, or equidistribution limit is needed. Strict separation at t_q gives an interval around it by continuity.

## 5. A complete explicit family and its countercheck

For core {1,4,5} and offsets {0,1,5,7}, choose

$$t_0=\frac{21}{64},\qquad x_0=\frac{23}{128}.$$

These choices give

$$\mu_C=\frac3{16},\qquad \mu_A=\frac7{128}.$$

The internal-drift requirement in (8) is q>64 and dominates the other terms. Hence the candidate argument covers **every integer q>=65** in

$$\{0,1,4,5,q,q+1,q+5,q+7\}.$$

A witness is given directly by (5). At q=65, the full speeds are {0,1,4,5,65,66,70,72}, and

$$t_{65}=\frac{2711}{8320},\qquad
\min_{v\ne0}\|v t_{65}\|=\frac{23}{128}>\frac18.$$

This is not a sharp cutoff. The same rounded construction also succeeds at q=64, outside the stated strict sufficient range.

The small q=6 member is the original tight set {0,1,4,5,6,7,11,13}. Its only valid times are the four odd eighths. Formula (5), applied outside its guarantee, gives t=93/256, where speed 11 is only 1/256 from the reference. A safe point in the auxiliary phase space is therefore not by itself a safe actual time; the drift condition is essential.

The same fixed rule for choosing t0 and x0 gives these additional bounded profiles:

| Core | Fixed offsets | Sufficient integer q from (8) |
| --- | --- | ---: |
| {1,4,5} | {0,1,5,7} | 65 |
| {1,4,8} | {0,1,5,7} | 74 |
| {2,3,5} | {0,1,5,7} | 32 |
| {1,2,4} | {0,2,3,5} | 13 |
| {1,3,5} | {0,1,2,3} | 15 |

These are certificates for particular choices, not optimized thresholds. Further cutoff polishing remains parked.

## 6. Evidence, literature, and limits

Run **python -m scripts.analyze_fast_cluster**. The [script](../scripts/analyze_fast_cluster.py) and [exact JSON](../experiments/fast_cluster.json) preserve:

- Five family profiles with exact core and phase margins.
- Twenty rounded-time checks: the integer just below each sufficient cutoff, the cutoff, the next integer, and twice the cutoff.
- Twenty affine certificates for positive-width intervals around those witnesses. All five below-cutoff checks happen to pass; none establishes a minimal cutoff.
- Nine nearby decompositions and all 54 core components, with 324 pair-duration crosschecks.
- Thirty complete allowed-set boundary reconstructions across the witness and nearby checks, including the tight small-q control.
- Eight frozen-phase reconstructions by both interval intersection and boundary-cell predicates, with the cyclic-gap formula checked separately.
- The explicit quarter-tiling, perturbed-tiling, and grid-but-not-tiling controls.

All checks pass. They verify the stated finite diagnostics, not independent mathematical review of the general argument.

The fast-motion/slow-motion idea has established precedent. S15, Noah Kravitz's *Barely lonely runners and very lonely runners* (2021), Proposition 6.1, preserves a safe interval for slower runners while a sufficiently fast additional runner moves through it. Our use of a common rotation for four runners is a scoped reconstruction prompted by the current examples. We do not claim that this family argument is new. S16, Jain–Kravitz's *Relative Lonely Runner spectra* (2026), is a relevant primary-source lead for the wider two-dimensional-subtorus setting; its theorems have not been audited here.

The present result keeps C and every a_i fixed while q grows. It does not apply uniformly when the core speeds or internal speed differences grow with q. It concerns one selected reference among eight total runners and does not certify all other references. It proves no general tree-selection rule, does not identify all tight cases, and does not settle arbitrary seven-speed inputs in this investigation.

**Question carried into the continuation below:** how much common rotation is enough relative to internal drift, and can the same separation of motions work for several groups or offsets that grow with q? Sections 7–11 record the subsequent source reading and extension. The S16 reading limit and fixed-offset scope above describe the first stage, rather than the completed continuation.


## 7. Allow different integer winding rates

**Continuation, September 24:** the fixed-offset restriction in Sections 2–6 can be relaxed. Keep a fixed core C of three distinct positive integers, but now take

$$v_i(q)=b_iq+a_i,\qquad i=1,2,3,4, \tag{9}$$

with fixed positive integers b_i, fixed integers a_i, and four distinct pairs (b_i,a_i). For sufficiently large positive integer q, all seven relative speeds are positive and distinct. The total runner count stays eight, the threshold stays 1/8, and reference 0 is selected.

The auxiliary positions become

$$c_jt,\qquad b_ix+a_it\pmod1. \tag{10}$$

Thus one common clock x can drive one, two, three, or more turns per cycle. The actual trajectory still has x={qt}; no starting phases have been changed.

This resolves a concrete failure of our old estimate. In the family q,2q+1,3q+5,4q+7, expressing everything as q plus an offset gives offsets 0,q+1,2q+5,3q+7. The old drift allowance A(q)/(2q) exceeds 3/2, whereas a strict safety margin can never exceed 3/8. That estimate cannot certify this family. It does not demonstrate actual blocking. Using fixed winding rates b=(1,2,3,4) removes the large part of the error exactly.

### Relation to the paper we located

S16, Jain–Kravitz, arXiv:2411.12684v2 (December 9, 2024), studies one-dimensional trajectories inside two-dimensional subtori. Its Theorem 1.1 describes their relative spectra, up to finitely many exceptions, by reciprocal arithmetic progressions above D(U). Sections 1.4 and 2.1 connect fast-runner limits with integer generators and phase grids. We inspected these statements and the proof outline, not the full proof. This establishes relevant precedent, not our threshold claim or novelty.

Our mapping into that framework is

$$U=\{(c_1t,c_2t,c_3t,b_1x+a_1t,\ldots,b_4x+a_4t)\pmod1\}.$$

The two integer generators are independent because the first three x-coefficients vanish and their t-coefficients do not. Every coordinate is nonconstant, so U is a proper two-dimensional subtorus in the paper's terminology. Its ambient dimension is seven: the paper counts moving coordinates, whereas our n=8 counts the reference as well. The actual trajectory T_q is the image of x=qt. In the source's distance convention, strict loneliness means D(T_q)<3/8.

A safe point in U is not automatically on T_q. The next two sections separately establish an auxiliary opening and a controlled actual time.

## 8. A Fourier component that complete blocking would have to cancel

At fixed t, let

$$B_i(t)=\{x\in\mathbb R/\mathbb Z:\|b_ix+a_it\|<1/8\},\qquad
M_t(x)=\sum_{i=1}^4{\bf1}_{B_i(t)}(x).$$

Each set consists of b_i small arcs and has total length 1/4. Hence

$$\int_0^1 M_t(x)\,dx=1. \tag{11}$$

Let G(t) be the measure of the clear phases, where M_t=0. Since M_t is integer-valued,

$$G(t)=\int_0^1(M_t(x)-1)_+\,dx,\qquad
\int_0^1|M_t(x)-1|\,dx=2G(t). \tag{12}$$

Clear space and duplicated blocking have exactly equal measure. In particular, no positive clear phase length would require M_t=1 almost everywhere. Equality points still count as valid and are not excluded by this statement.

To test that rigid requirement, set b_* = min_i b_i and use the Fourier convention

$$\widehat f(k)=\int_0^1f(x)e^{-2\pi ikx}\,dx.$$

An individual indicator has period 1/b_i. Splitting its integral into b_i translates shows that its coefficient at k vanishes unless b_i divides k. Therefore every runner with b_i>b_* contributes zero at frequency b_*.

For a runner with b_i=b_*, substitution over its b_i periods gives

$$\widehat{{\bf1}_{B_i(t)}}(b_*)
=e^{2\pi ia_it}\int_{-1/8}^{1/8}e^{-2\pi iy}\,dy
=\frac{\sqrt2}{2\pi}e^{2\pi ia_it}.$$

Consequently,

$$\widehat M_t(b_*)=\frac{\sqrt2}{2\pi}P(t),\qquad
P(t)=\sum_{i:b_i=b_*}e^{2\pi ia_it}. \tag{13}$$

If P(t) is nonzero, M_t cannot be the constant 1 almost everywhere, so there is positive clear phase length. More quantitatively, (12) gives

$$G(t)\geq\frac{\sqrt2}{4\pi}|P(t)|. \tag{14}$$

These are analytic identities and a proposed general argument; the script does not certify them by floating-point Fourier sampling.

There are two useful consequences:

- If exactly one runner has the smallest winding rate, |P(t)|=1 for every t. A positive phase opening exists at every slow time.
- If several share that rate, their contributions can cancel, but only at finitely many t modulo 1. Indeed, P(0)>0, and multiplying P(t) by a suitable exponential makes it a nonzero polynomial in z=e^{2πit}, because all a_i are integers. A nonzero polynomial has finitely many roots.

The three core runners leave strict safe intervals, as in Section 3. Any such interval contains a rational t0 outside the finite zero set of P. At that time, the finite collection of arc boundaries cannot exhaust a positive-length clear set. Choose rational x0 strictly inside a clear phase interval. Both core and fast-coordinate margins are positive.

This is the forcing mechanism in this family: complete blocking would have to cancel a lowest-frequency component that the faster winding rates do not possess. Tied lowest rates may cancel one another at particular phases, but they cannot do so throughout a core opening.

The equal-quarter-spacing criterion from Section 3 was specific to b_i=1. Different winding rates allow more complicated exact tilings. Vanishing of P is necessary for zero clear length, not sufficient.

## 9. Transfer the auxiliary opening to the actual trajectory

Write

$$\mu_C=\min_{c\in C}\|ct_0\|-1/8>0,\qquad
\mu_F=\min_i\|b_ix_0+a_it_0\|-1/8>0.$$

Let M=max(C), A=max_i|a_i|, and let eta be the distance from t0 to its chosen core-component boundary. Use the same rounding construction:

$$m_q=\lfloor qt_0-x_0+1/2\rfloor,\qquad
t_q=(m_q+x_0)/q,\qquad |t_q-t_0|\leq1/(2q).$$

Now

$$(b_iq+a_i)t_q=b_im_q+b_ix_0+a_it_q.$$

The term b_i*m_q is an integer. It disappears when measuring distance to an integer, leaving only the fixed-offset change a_i(t_q-t0). Therefore

$$\|ct_q\|\geq1/8+\mu_C-M/(2q),$$

$$\|(b_iq+a_i)t_q\|\geq1/8+\mu_F-A/(2q). \tag{15}$$

The sufficient condition is

$$q>\max\left(M+A,\;2A,\;\frac{M}{2\mu_C},\;
\frac{A}{2\mu_F},\;\frac1{2\eta}\right). \tag{16}$$

The first term places every extra speed above the core. The second makes extra speeds with different b_i distinct; equal b_i already have different a_i. The remaining terms guarantee strict safety and keep t_q inside the core opening. Fixed negative offsets are allowed by the absolute-value bound.

**HYPOTHESIS/proof candidate:** for any fixed core triple and fixed four pairs satisfying Section 7, every sufficiently large integer q has a positive-length lonely interval for reference 0. The construction works in each positive-length core component, with its own sufficient bound. This is an AI-generated proposed infinite implication, awaiting independent review.

## 10. A concrete extension and its limits

For core {1,4,5} and pairs (1,0),(2,1),(3,5),(4,7), use

$$t_0=21/64,\quad x_0=875/1536,\quad
\mu_C=3/16,\quad\mu_F=115/512.$$

The largest term in (16) is 1792/115, so the construction covers every integer q>=16 in

$$\{0,1,4,5,q,2q+1,3q+5,4q+7\}.$$

At q=16 the actual speeds are {0,1,4,5,16,33,53,71}, and

$$t_{16}=8555/24576,\qquad
\min_{v\ne0}\|vt_{16}\|=6377/24576>1/8.$$

This is a strict witness, not a maximum claim or a sharp cutoff.

Three prescribed profiles give:

| Core | Four extra speeds | Chosen t0 | Sufficient integer q |
| --- | --- | --- | ---: |
| {1,4,5} | q,2q+1,3q+5,4q+7 | 21/64 | 16 |
| {1,4,5} | q,q+1,q+5,q+7 | 21/64 | 65 |
| {2,3,5} | q,q+4,2q+3,2q+5 | 13/100 | 667 |

The second reproduces our previous witness. The third deliberately chooses a time close to an exact tiling, giving a small fast margin 3/800 and a conservative cutoff. It is a sensitivity control, not a proposed optimal bound.

### Cancellation and exact tiling controls

Keep core {2,3,5}, which is strictly safe at t=1/8.

| Four auxiliary positions | Slow time | P(t) | Clear phase length |
| --- | --- | --- | ---: |
| x, x+4t, 2x+3t, 2x+5t | 1/8 | 0 | 0 |
| x, x+4t, 2x+3t, 2x+5t | 13/100 | nonzero | 1/40 |
| x, x+4t, 2x+3t, 2x+6t | 1/8 | 0 | 1/8 |

The first row tiles with two quarter-length arcs and four eighth-length arcs. It retains exactly six valid phases: 1/8,1/4,3/8,5/8,3/4,7/8. Those are isolated equality points in the auxiliary phase circle, not automatically six actual lonely times.

The second row perturbs the slow time, breaking the tiling. The third leaves the tested Fourier component canceled but has a positive gap: other components prevent complete coverage. Thus one vanished component is not a full characterization of tiling.

Two further controls mark the argument's scope:

- The original small-q member {0,1,4,5,6,7,11,13} still has only the four odd-eighth times. Its rounded auxiliary witness fails below the sufficient range, as recorded in Section 5.
- Scaling every speed together, {0,q,2q,...,7q}, leaves the reference exactly tight for every positive q: it merely rescales time. Exact checks at q=1,2,3 retain only isolated times. The all-q implication follows from the time change s=qt and the already recorded consecutive-speed case. Large speeds alone do not create strict room.

## 11. Reproduction and the remaining obstacle

Run **python -m scripts.analyze_affine_family**. The [script](../scripts/analyze_affine_family.py) and [data](../experiments/affine_family.json) record:

- Three prescribed profiles and twelve rounded-time checks, at one below, at, one above, and twice each sufficient cutoff.
- Twelve positive-width affine interval certificates; all three below-cutoff diagnostics also pass.
- Six auxiliary-phase reconstructions using both affine-strip intersection and independent boundary-cell predicates. Individual blocked lengths and the identity G=redundant blocking agree exactly.
- Sixteen complete actual allowed-set reconstructions, including the small-q failure and three common-scaling controls.
- The three explicit cancellation/tiling comparisons above.

All checks pass, as do the existing 25 checker tests. Complete positive-duration unions are compared in memory; the JSON preserves their hashes, component counts, durations, endpoint components, and explicit witness certificates. All zero-duration allowed sets are retained in full. No broad scan was run. These computations are exact finite diagnostics, not independent review of the general argument.

This extension permits internal speed differences proportional to q. It still requires a fixed core and fixed affine coefficients; it does not supply a uniform bound when those data vary. It addresses one selected runner among eight and neither proves arbitrary-speed coverage by our method nor characterizes all tight inputs. The two-coordinate representation adds an analytical degree of freedom, not a physical unknown variable or independently adjustable start.

**Next useful question:** can a comparable obstruction to complete blocking survive when the three core speeds also vary? First classify the equality obstruction in a small two-parameter model and retain common scaling as a mandatory tight control. If the limiting auxiliary system has only equality points, the strict-margin rounding argument stops; handling that case needs a different idea. Further cutoff polishing remains parked.

