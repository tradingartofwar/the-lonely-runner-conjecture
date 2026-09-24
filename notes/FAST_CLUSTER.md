# Four fast runners with fixed speed differences

**Date:** September 24, 2026. **Status:** HYPOTHESIS/proof candidate for the general argument; OBSERVED for the exact diagnostics; DISPROVEN for the specific necessity claim tested below. AI materially generated the argument and implementation. Independent mathematical review remains outstanding. No novelty claim.

Vance approved continuing the pair-selection question: what arithmetic structure forces enough useful overlap? This continuation checks a tempting local pattern and then develops a constructive family argument. It does not expand a speed-set search or optimize another cutoff.

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

**Next useful question:** how much common rotation is enough relative to internal drift, and can the same separation of motions work for several groups or offsets that grow with q? Before extending that claim, compare this construction with the two-dimensional-subtorus literature and identify a specific failure of the fixed-offset assumption. Preserve the distinction between a gap in auxiliary phase space and a time the actual trajectory reaches.

