# An adaptive pair covers every phase in the variable-speed family

September 28, 2026 UTC. Baseline `3ffb0c7b5edb75a81e60de0ceed58f5a40edae7b`.

**Outcome:** the existing speed-dependent time, together with its reflection, supplies a lonely instant for every admissible integer V and every starting phase of runner 11 in the family below. When 8 divides V, a directed endpoint argument also supplies a positive interval of length at least `1/(56V)` for every such phase. The two prescribed instants themselves always have minimum distance exactly 1/8 at their best.

**Status:** HYPOTHESIS / proof candidates. Exact finite calculations are separately reconstructed; the unbounded conclusions rest on the arguments below. AI supplied the derivation, implementation, and internal reviews. Independent human review and originality assessment remain outstanding. This is a restricted-family, selected-reference result, not a proof of the general Lonely Runner Conjecture.

The [old variable-speed argument](VARIABLE_SPEED_FAMILY.md) already covered every V at common start. The change here is the quantifier over runner 11's starting phase. The [fixed-template study](TIME_TEMPLATE_CLASSIFICATION_2026_09_27.md) covered 117 of 120 residue classes with four fixed times; the adaptive pair covers all three classes missed by that fixed menu. No new speed search is needed.

## Precise statement

Take eight velocities

\[
\{0,1,4,5,6,7,11,V\},\qquad
V\in\mathbb Z_{>0}\setminus\{1,4,5,6,7,11\}.
\]

Select reference 0 and threshold \(\delta=1/8\). All initial phases are zero except runner 11, whose phase is \(\theta\in\mathbb R/\mathbb Z\). Only \(\theta=0\) is the original common-start input. Put

\[
F_{V,\theta}(u)=\min\bigl(\|u\|,\|4u\|,\|5u\|,
\|6u\|,\|7u\|,\|Vu\|,\|11u+\theta\|\bigr).
\]

Freeze the old rule, without changing it after the test:

\[
t(V)=\begin{cases}
1/8,&8\nmid V,\\
17/56,&8\mid V,\ 56\nmid V,\\
17/56+1/(8V),&56\mid V.
\end{cases}
\]

The proposed conclusions are

\[
\max\{F_{V,\theta}(t(V)),F_{V,\theta}(1-t(V))\}=1/8
\quad\text{for every admissible }V\text{ and every }\theta,
\]

and, writing \(D_V(\theta)\) for the total allowed duration in one period,

\[
8\mid V\quad\Longrightarrow\quad D_V(\theta)\ge\frac1{56V}>0
\quad\text{for every }\theta.
\]

The first formula describes performance of this pair, not the maximum over all times. The second is a sufficient lower bound, not exact duration or an optimized bound.

## Why a reflected pair works

For every unchanged integer speed w, \(\|w(1-t)\|=\|wt\|\). Let c be the minimum unchanged distance at either time. Runner 11's unshifted phases have circular separation

\[
d=\|11t-11(1-t)\|=\|22t\|.
\]

For every \(\theta\), the circle triangle inequality gives

\[
\|11t+\theta\|+\|11(1-t)+\theta\|\ge d.
\]

At least one selected-runner distance is at least d/2. At that time the full minimum is at least \(\min(c,d/2)\). If the unchanged minimum is exactly c at both times, neither full minimum can exceed c. Thus c=1/8 and d≥1/4 suffice for the claimed constant pair performance. This is the previously supplied [two-time lemma](TWO_TIME_CERTIFICATES_2026_09_27.md), reproduced here to make the argument self-contained.

## The three arithmetic branches

Let \(a=17/56\), \(b=5/16\). The phases of the unchanged fixed core on \([a,b]\) are:

| Speed | Phase at a | Phase at b |
| ---: | --- | --- |
| 1 | 17/56 | 5/16 |
| 4 | 3/14 | 1/4 |
| 5 | 29/56 | 9/16 |
| 6 | 23/28 | 7/8 |
| 7 | 1/8 | 3/16 |

Each phase increases linearly without wrapping. All five are strictly safe in the interior; at a only speed 7 is at threshold. This interval has length 1/112.

| Condition | Unchanged minimum c | Unchanged equality controllers at either candidate | Selected phase separation d |
| --- | --- | --- | --- |
| 8 does not divide V | 1/8 | 1 and 7; also V if V≡1 or7 modulo8 | 1/4 |
| 8 divides V but 56 does not | 1/8 | 7 | 9/28 |
| 56 divides V | 1/8 | V | 9/28−11/(4V)≥61/224>1/4 |

**First branch.** At t=1/8 the five core distances are \((1/8,1/2,3/8,1/4,1/8)\). A nonzero eighth residue gives \(\|V/8\|\ge1/8\). The selected phases are 3/8 and 5/8, separated by 1/4.

**Second branch.** Write V=8m, with 7 not dividing m. At a, \(Va=17m/7\), a nonzero seventh residue. Its distance is at least 1/7>1/8. Runner 11's phases are 19/56 and 37/56, separated by 9/28.

**Third branch.** Write V=56m, m≥1. Then \(Vt=17m+1/8\), while

\[
0<t-a=\frac1{8V}\le\frac1{448}<b-a.
\]

The five core runners are strictly safe and V is at equality. Runner 11's phase at t is \(x=19/56+11/(8V)\). It lies between 19/56 and 163/448, hence in (1/4,1/2). Its reflected phase is 1−x, so

\[
d=1-2x=\frac9{28}-\frac{11}{4V}
\ge\frac9{28}-\frac{11}{224}=\frac{61}{224}>\frac14.
\]

The three cases exhaust the domain and prove the claimed pair formula within this supplied argument. The unbounded step is the residue classification and these inequalities, not extrapolation from diagnostic examples.

## Equality can be the beginning of an interval

For 8 dividing V, select the candidate whose **runner 11 distance is larger**, breaking a tie arbitrarily. Its selected-runner distance is at least d/2>1/8. Do not instead choose an arbitrary candidate with full minimum 1/8: those full minima can tie even when the selected-runner margins differ.

An exact countercheck makes this distinction necessary. In the second branch, set θ=15/28. At t=a, runner 11's phase is 7/8 while speed 7's phase is 1/8: their permitted directions oppose, isolating this candidate. At 1−a, runner 11's phase is 11/56, strictly safe. Both full minima are 1/8, but only choosing the larger runner-11 margin supports the directed interval argument below. This is an algebraic boundary check, not an extra phase grid.

At t, the unchanged runners admit movement to the right; at 1−t they admit movement to the left. Set \(R=1/(56V)\). We check all inward displacements \(0<h<R\).

In the second branch, V≥8. The core remains in (a,b) because R<1/112. Write the phase of V at a as j/7, with 1≤j≤6. Its increase across R is VR=1/56, so

\[
\frac18<\frac j7+Vh<\frac j7+\frac1{56}\le\frac78.
\]

Thus V is strictly safe throughout the open interval. Runner 11 starts with distance at least 9/56, and distance is 11-Lipschitz in time. Its distance excess throughout the closed displacement range is bounded below by

\[
\frac1{28}-11R=\frac{2V-11}{56V}>0.
\]

In the third branch, V≥56. The core stays inside (a,b), since

\[
b-t-R=\frac1{112}-\frac1{7V}>0.
\]

Runner V moves from phase 1/8 to 1/7 across R and is strictly safe for h>0. Runner 11's distance excess remains at least

\[
\frac d2-\frac18-11R
=\frac1{28}-\frac{11}{8V}-\frac{11}{56V}
=\frac{V-44}{28V}>0.
\]

Reflection gives the same unchanged distances for the leftward interval at 1−t. The Lipschitz estimate applies in either time direction, with the same actual phase θ. Hence the selected side is an allowed interval of length R, with all distances strictly greater than 1/8 in its open interior. This supplies \(D_V(\theta)\ge R\).

In contrast, when 8 does not divide V, the selected times 1/8 and 7/8 are locally isolated by unchanged speeds 1 and 7: their equality constraints require opposite time directions. This is a statement about these two times. It does not say the entire configuration has only isolated solutions. The old V=13, θ=0 tight control really has zero duration; other phases of that same control have positive duration elsewhere.

The consequential distinction is therefore **which direction each active equality permits**. A scalar pair margin of 1/8 loses that information: it occurs both at isolated contacts and at endpoints that lead into strict openings.

## Exact checks and preserved controls

The frozen [protocol](../reviews/2026-09-28-adaptive-pair/protocol.json), SHA256 `55d73b9e425f4ad8fa74441029cb88569f2091fcb3bdf3494c4cca656d92f7f7`, selects exactly the eight already-used values V=13,16,32,56,88,112,120,56000000000000. The large value is handled by rational substitutions, without enumerating its laps. No time or phase grid, extra pair search, or full safe-set reconstruction is used.

The primary calculation records residues, unchanged distances, equality controllers, selected phase separation, and directed interval certificates. The separate verifier reconstructs the finite records and complete rational phase envelopes without reading or importing the primary implementation. Their exact counts, digests, dependency hashes, and review limits are in the [manifest](../reviews/2026-09-28-adaptive-pair/manifest.json).

Run from the repository root:

```bash
python -B reviews/2026-09-28-adaptive-pair/calculate.py --check
python -B reviews/2026-09-28-adaptive-pair/verify.py --check
```

Both read-only commands pass. The verifier matches every diagnostic field and canonical digest. Its 16 raw/full phase envelopes use 119 algebraic cells and 135 event-point evaluations. Seven directed certificates include 42 unchanged safe-lap checks and 98 selector-phase cells with 105 event-point evaluations; 166 displayed-formula substitutions also agree. These counts include repeated geometry across controls. The resulting archive SHA256 is `0a46e3baf91d8cc740e23d019f39803362b0f92a789fb3f8685c697f68658364` for the primary results and `e3bac53a4bb1f620f31a2577c2d13719d11379ef7802f8866115991d0e4c0b87` for the independent verification.

The [arithmetic](../reviews/2026-09-28-adaptive-pair/arithmetic.md), [endpoint](../reviews/2026-09-28-adaptive-pair/endpoints.md), [challenge](../reviews/2026-09-28-adaptive-pair/challenge.md), and [coverage](../reviews/2026-09-28-adaptive-pair/coverage.md) reports retain the independent internal perspectives. General statements remain proof candidates; successful exact finite checks are not a mechanical verification of the unbounded proof.

## What this adds, and the next useful question

The prior fixed menu missed V≡0,32,88 modulo120. All of these speeds are divisible by eight, so the directed argument now gives all-phase positive duration throughout all three classes. The old diagnostic projections certified only their selected representatives. The adaptive pair also gives threshold survival for every other admissible V, using a bounded number of rational operations; integer bit cost still grows with V.

This pair does not supersede the older fifteenth pair: that pair attains the larger distance 2/15 on its successful residue classes. Nor do we claim a positive-duration classification for all V not divisible by eight. The original common-start family was already covered, and this argument still relies on the special fixed core, integrality, one selected reference, and variation of only one starting phase.

The finite rational-menu obstruction remains intact. A sufficiently large integer multiple of every fixed denominator collides at all fixed candidate times. Here the candidate denominator moves with V in the third branch, escaping that obstruction; a small certificate need not occupy fixed positions.

**Next proposed:** return to the [small-gcd selection priority](SMALL_GCD_DISTINCTION_REVIEW_2026_09_27.md). Audit which inputs the existing local certificates require, and which can be selected from speed relations before reconstructing the full allowed set. Use the existing 56/113 case, its 112 contrast, the tight 6/7/11/13 case, and preserved summary-collision controls. Distinguish verifying a supplied certificate from selecting one and from proving some certificate must succeed. No broad speed search or further pair optimization is proposed; +7/+9 remains parked.
