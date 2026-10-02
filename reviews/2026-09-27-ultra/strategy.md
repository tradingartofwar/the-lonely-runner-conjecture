# Strategy review: turn representation failures into a selection question

September 27, 2026. Baseline snapshot: `e94a87f650264826569cae63412c43a5175f5ae4`. Material AI involvement: this review, derivations, and exact controls. This is a strategic/adversarial review, not independent human certification or a novelty claim. Only this report and its two companion control files were written by this reviewer.

## Assessment

The fixed-core work has established useful, testable statements about what summaries retain. The recent physical collisions are stronger evidence than the earlier artificial occupancy distributions. They still attack **reconstructing a specified local answer**, not the statement **somewhere a valid time exists**. An adequate proof representation need not recover every local topology, every component, or every duration. It must retain enough information to force one witness, including equality when necessary.

There is a concrete reason to change emphasis now. The entire `1680h` family with alternating local existence admits the elementary strict global selector below. Thus it is an unusually good stress test for *avoiding an unhelpful window*, but it is poor evidence that the global problem intrinsically requires all its local detail. Complete duration data lose pointwise facts; this does not imply that an arbitrarily complicated pointwise record is necessary for global existence. The arithmetic review's full-period result is complementary: a positive full-period opening can survive the same local ambiguity.

The missing quantifier is not another overlap identity. Current statements have forms such as

`for this core/window/fixed coefficient tuple, every sufficiently large parameter has a certificate`.

A global route needs an implication of the form

`for every admissible configuration and selected reference, some controllably selected core/window/relation model has a valid witness certificate`.

“Some certificate can be checked cheaply” and “a useful certificate can be found without rebuilding every threshold event” are different claims. So are “all contacts in a window have been identified” and “at least one of those contacts survives.” The geometry review's small contact menu can solve the first local problem without implying the second global statement.

## Verified controls that change priorities

### 1. All local parity cases have a strict global witness

Let the slow relative speeds be `s=(1,3,4,5,10,28)` and `t0=11/64`. Direct evaluation gives

`min_s ||s t0|| = 9/64 = 1/8 + 1/64`.

For any positive real `y`, choose an integer `m` nearest `y*t0−1/2`, and set

`t_y=(m+1/2)/y`.

Then the new runner is exactly half a lap away, and `|t_y−t0|≤1/(2y)`. The slow distance functions are Lipschitz with constants at most 28, so

`min_{v in (s,y)} ||v t_y|| ≥ min(1/2, 9/64−14/y)`.

Consequently every `y>896` has a strict global witness. In particular, every `y=1680h`, `h≥1`, has separation at least `127/960 = 1/8+7/960`. The finite controls independently substitute eight values through `h=10^12`; the displayed inequality is the all-parameter argument, a proof candidate under repository policy. Nothing in it needs the local `J` parity or any overlap moment.

By contrast, a fixed finite rational time menu `T={a_j/b_j}` chosen before the added speed can never force success for all `y`: a positive `y` divisible by all `b_j` blocks every menu item. Even the menu `{9/32,3/8,11/64}` is killed by `y=6720`, while the adaptive half-lap selector still works. This is an exact obstruction to **guaranteed surviving fixed candidates**, not to listing all possible local contact candidates. It permits menus that depend on all the speeds and permits interval-based approximation arguments.

### 2. Rational perturbations change the global optimum without changing closure dimension

Use three total runners and relative speeds `(1, 2+1/N)` with odd positive integer `N`. At `t=N/2`, both phases equal `1/2`, so the global maximum is exactly `1/2`. The limiting speeds `(1,2)` instead have maximum `1/3`. All these rational configurations have one-dimensional periodic orbits. Thus dimension alone does not describe their target geometry or their return scale.

This is not a discontinuity of the motion on a fixed time window. Let `f_N(t)` be the minimum distance and `f_0(t)` the limiting minimum. On `[0,T]`,

`|f_N(t)−f_0(t)|≤T/N`.

Since `f_0(t)≤1/3`, achieving distance `2/5` requires `T≥N/15`. The first exact half-lap alignment is `t=N/2`: writing the first phase as `t=m+1/2` forces `2m+1=N mod 2N`. The changed global maximum uses a growing clock horizon, even though an earlier strict witness above `1/3` can have a shrinking margin. Five odd `N` values through 101 are checked with both existing exact checker methods.

For an irrational perturbation `(1,2+epsilon)`, sampling at `t=m+1/2` makes the second phase an irrational rotation, so the supremum is `1/2`; simultaneous exact half-lap alignment is impossible. This distinguishes maximum from supremum. The irrational-density step uses the familiar rotation fact rather than a numerical experiment. No irrational case is represented by a floating-point speed in the verifier.

A related local control needs no density theorem: with slow `(1,3,4,5,10,28)` and `y=3360+epsilon`, `|epsilon|<1/3`, both fixed candidate endpoints of `J` remain strictly blocked by `y`; the fixed runners already block its interior. Thus `J` remains empty even for arbitrarily small irrational perturbations that release the fast phase in the long-time closure.

### 3. The fixed-coefficient quantifier cannot be dropped

At every integer `q≥8`, write the tight consecutive configuration as

`{0,1,2,3, q+(4−q), q+(5−q), q+(6−q), q+(7−q)}`.

It formally has the affine shape with arbitrarily large `q`, but its maximum stays exactly `1/8`. At `t=1/8` this value is attained. For the upper bound, among the eight points `0,t,...,7t` some circular gap is at most `1/8`; its endpoints differ by one of the seven allowed relative speeds.

Here the offsets vary with `q`, and `A=q−4`. The affine proof's required `q>2A` fails for every `q≥8`. Each *frozen* coefficient tuple can have a later valid cutoff; this diagonal sequence does not cross it. This is a direct counterexample to promoting “eventual for each fixed tuple” into “every sufficiently large arbitrary decomposition.” It is not a counterexample to the written affine proposition.

## Ranked investigations

### 1. Falsify a precise global certificate-selection rule

**Proposed question.** For eight total runners, when there is a strict lonely time for a selected reference, must some three-constraint core and one of its complete positive-length safe components have a positive best spanning-tree overlap bound on the remaining four constraints? Keep threshold `1/8`; do not reset it when choosing a core. Use the occurrence convention and bound formula already implemented. Restrict the first falsification domain to references with seven distinct absolute relative speeds; then handle duplicated constraints explicitly without changing `n`.

This is a sharply stated intermediate hypothesis, not an assertion that tree bounds suffice. It asks whether existing certificate *content* can succeed somewhere before spending effort on a fast selector. It is much stronger than checking one designated core and much weaker than full LRC. If it survives, selecting among the cores/components without enumerating their full event lists remains a separate task.

**Small useful experiment.** Check the existing named local failures, including `6/7/11/16`, `56/64/72/112`, `56/64/72/113`, the `1680/3360` contacts, and the already archived tight controls. For each eligible reference, exhaust the 35 cores and every full safe component, recording the best certificate and an exact global witness independently. Use tight inputs to audit a separate contact branch; never expect a positive duration certificate there. The no-core/all-core distinction matters more than another speed cutoff scan.

**Success criterion.** A bounded positive result must name the exact input/reference scope. Mathematical progress would be a structural lemma selecting a successful core/component for an infinite class where the choice was previously uncontrolled, with complexity measured separately. A proposed rule must work after reference changes and rescaling, or expressly declare its invariant scope.

**Failure criterion.** One exact strictly lonely vector/reference for which every admissible core/component has nonpositive tree bound disproves the hypothesis. Archive all cores, their best bound, and the independent strict witness. Such a result would justify richer certificate content; another failure in an already unsuitable chosen window would not. Any finite menu chosen before the added speed must also survive the common-denominator obstruction above or be rejected immediately.

**Priority consequence.** Do not repeat searches whose target is merely another moment collision. The representation-insufficiency question now has decisive physical controls. Make the next missing statement about *finding one useful place to certify*.

### 2. Use relation lattices to separate obstruction geometry from clock resolution

**Proposed LTCM.** Record `Lambda(u)={m in Z^k:m·u=0}` and the corresponding phase constraints `m·theta=0 mod 1`. For continuous time the speed equation is exactly zero; `m·u` merely being an integer is insufficient. Keeping a saturated sublattice of relations gives an auxiliary torus containing the actual orbit; arbitrary unsaturated equation lists can instead define a disconnected subgroup. Full relation data encode the speed direction rather than magically compressing it. A useful reduced model needs a theorem transferring its strict target margin to the actual trajectory.

The ambient coordinate count, the dimension of the orbit closure, the dimension of a feasible target intersection, and the scale of winding/return are four different quantities. An auxiliary point on the target boundary need not be visited by a dense orbit: `(1,alpha)` with irrational `alpha` never reaches `(1/2,1/2)`, though that point lies in its closure. That example uses the artificially stronger `1/2` target for three runners; it warns against a closure-to-attainment inference, not against LRC.

**A useful already-verified negative control.** In the `1680h` family, all integer relations with coefficient norm `sum|m_j|≤17` are the same, even though the local parity differs. Any relation involving the fast speed would need to cancel at least `y≥1680`, while the other coefficients contribute at most `28*16=448`. Hence its fast coefficient must vanish. This is an elementary norm bound; 17 is a chosen diagnostic budget, not a claimed universally sufficient cutoff. Again, losing this local distinction is harmless to the strict global selector above.

**Small useful experiment.** Compare the rational perturbation family, an irrational perturbation described symbolically, and the fixed-core contact family. Keep three outputs separate: exact short-relation sets, a rigorously certified auxiliary target margin, and the time/error bound needed to realize that margin. Test whether adding relation *length and near-relation error* predicts the long waiting scale that dimension misses. In `(1,2+1/N)`, the formerly exact relation `(2,−1)` has error `−1/N`; the genuine integer relation has coefficients `(2N+1,−N)`.

**Success criterion.** Produce a certified implication of the form `auxiliary margin eta + specified arithmetic approximation bound => actual witness by time T`, and recover both the affine `O(1/q)` transfer and the slow-fast selector as examples. New progress would cover coefficient or scale patterns that neither existing lemma controls.

**Failure criterion.** Two inputs with the proposed retained arithmetic data have incompatible certified time/margin requirements, or the proposed transfer uses an unattained boundary point. That rejects the reduced model or its quantitative claim. Mere local-topology mismatch does not reject a model whose declared target is global strict existence.

**Literature positioning.** Jain and Kravitz, *Relative Lonely Runner spectra*, arXiv:2411.12684v2 (December 9, 2024), Sections 1.1–1.2, explicitly formulate loneliness through distance of subtori to the half-lap point and discuss limits of one-dimensional subtori in larger subtori. This is an existing mathematical framework, not a new dimensional mechanism. This reviewer inspected those sections; not the paper's full proof. [Primary source](https://arxiv.org/html/2411.12684v2).

### 3. Stress the affine argument along moving-coefficient and changing-reference limits

**Proposed question.** Which quantitatively specified families can satisfy the affine transfer uniformly when coefficients also vary? Rewrite the operative condition as small ratios `M/(q*mu_C)` and `A/(q*mu_F)` plus the distinctness conditions. This exposes whether the auxiliary margin disappears at the same rate as the rounding error. Calling `q` large in isolation carries no information.

**Small useful experiment.** Start from the existing reviewed affine examples, vary one offset with `q`, and retain exact auxiliary margins and actual maxima at selected values. Include the tight diagonal above as a compulsory negative control. Change the selected reference and record the winding multiplicities rather than assuming the original slow/fast split survives. The previous Ultra review covers some reference classes; mixed multiplicities must not be silently imported into that result. Even `(0,1,2)` has maxima `(1/3,1/2,1/3)` across its three references, with the middle reference having duplicated absolute constraints but the same `1/3` conjecture threshold.

**Success criterion.** Prove one uniform transfer theorem with explicit allowed coefficient growth and a positive margin dominating its error, preferably for a presently uncontrolled reference/multiplicity pattern. State all quantifiers before computation. A route toward the global conjecture would additionally need a reduction placing every hypothetical obstruction into covered strata; that reduction is not supplied by an asymptotic example.

**Failure criterion.** A claimed uniform bound admits the tight diagonal, loses its margin as fast as its error, or chooses coefficients after seeing `q` without accounting for their growth. If every diagonal test merely changes the family-specific cutoff, stop describing it as progress toward arbitrary configuration selection.

## Reproduction and limits

Run `python -B reviews/2026-09-27-ultra/strategy_check.py --check`. The archive pins this script and `lonely_runner/checker.py`. It records eight direct adaptive witnesses, the finite rational menu obstruction, five rational-perturbation maxima crosschecked by the existing two methods, the three-reference control, and three diagonal decompositions. The maximum claims use small normalized cases; the huge `h` witness uses direct exact substitution, not large event enumeration. The all-parameter inequalities above require review beyond the finite checks.

The ranked experiments have **not** been run here. They are proposed falsifiable investigations. No broad search, outside outreach, repository publication, or shared-note edit was performed. The strategic recommendation is to keep the contact repair as a focused local task and devote the next substantial investigation to an explicit global selection/transfer statement.
