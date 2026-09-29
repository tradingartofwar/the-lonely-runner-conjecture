# Core scope: the fifth constraint still has an elementary positive window

September 29, 2026. Pinned research parent:
`db2867ed65c4df3668f5275878f21ba400faff2b`.

**Status: HYPOTHESIS / analytically derived proof candidates, pending independent
review.** No novelty claim and no new executable check or speed-tuple scan.
The twelve one-variable values below were derived by the displayed elementary
interval intersections. They should be independently reviewed before promotion.

Scope: positive distinct integer speeds at common start, selected reference 0,
threshold `1/8`, fixed core `1,4,5`, and ordered residuals `a<b<c<d` excluding
that core. This report does not invoke a Lonely Runner existence theorem.

## 1. The critical-duty overlap argument does absorb a

For four integer constraints, let M(t) count their open blocked sets on the
unit circle. Each has measure `1/4`, so `integral M=1`. If U is the common-safe
set, then

`measure(U) = integral_(M>=1) (M-1)`.

For speeds `{1,4,5,a}`, all four block the arc of radius `1/(8 max(5,a))`
around 0. This arc has length `1/(4 max(5,a))` and multiplicity four, giving

`measure(U) >= 3/(4 max(5,a)) > 0`.

This elementary argument proves a positive component exists; it is stronger
than merely establishing an equality witness. For five constraints, however,
the same identity is `measure(U)=integral_(M>=1)(M-1)-1/4`.
The common overlap does not by itself force the required excess above `1/4`.
Failure of that argument is not failure of positive core windows.

## 2. A fixed-core discrepancy calculation bypasses the apparent obstruction

The safe set S for `{1,4,5}` consists of three intervals and their reflections:

| Name | Interval in the first half-period | Width |
| --- | --- | --- |
| A | `[1/8,7/40]` | `1/20` |
| B | `[9/32,3/8]` | `3/32` |
| C | `[17/40,15/32]` | `7/160` |

Thus `measure(S)=3/8`. For an integer speed v, write

`Q(v)=measure(S intersect {t: ||vt||<1/8})`.

For the blocked train of speed v, a periodic primitive of its indicator minus
`1/4` has range `3/(16v)`: it rises at slope `3/4` across a blocked interval
of width `1/(4v)`, then falls at slope `-1/4` across the safe gap. Consequently
the blocked measure on any one interval I is at most

`width(I)/4 + 3/(16v)`.

Summing over the six fixed core intervals gives the unconditional bound

`Q(v) <= 3/32 + 9/(8v)`.

For `v>=16`, this is at most `21/128<1/6`. Only
`v in {2,3,6,7,8,9,10,11,12,13,14,15}` remains. The following table supplies
their exact hand calculations. Its middle columns are blocked lengths in the
scaled intervals vA, vB, vC, intersected with the intervals
`(j-1/8,j+1/8)` for integer j. Reflection and scaling give
`Q(v)=2*(q_A+q_B+q_C)/v`.

| v | q_A | q_B | q_C | Q(v) |
| ---: | ---: | ---: | ---: | ---: |
| 2 | `0` | `0` | `1/16` | `1/16` |
| 3 | `0` | `1/4` | `0` | `1/6` |
| 6 | `7/40` | `1/4` | `0` | `17/120` |
| 7 | `1/4` | `5/32` | `3/20` | `89/560` |
| 8 | `1/8` | `1/8` | `0` | `1/16` |
| 9 | `0` | `1/4` | `1/4` | `1/9` |
| 10 | `0` | `1/4` | `0` | `1/20` |
| 11 | `1/20` | `9/32` | `1/4` | `93/880` |
| 12 | `9/40` | `1/4` | `1/40` | `1/12` |
| 13 | `1/4` | `1/4` | `7/32` | `23/208` |
| 14 | `1/4` | `7/16` | `7/40` | `69/560` |
| 15 | `1/4` | `1/4` | `5/32` | `7/80` |

Every row is at most `1/6`. This proves the proposed uniform inequality

**`Q(v)<=1/6` for every positive integer v outside `{1,4,5}`.**

No asymptotic approximation or independence assumption appears here. The
periodic primitive controls all large integers; the table exhausts the
remaining one-parameter cases.

## 3. Uniform positive measure for the four- and five-constraint cores

Deleting one or two residual blocked sets from S and using the union bound
now gives

`measure(safe{1,4,5,a}) >= 3/8-1/6 = 5/24`,

**`measure(safe{1,4,5,a,b}) >= 3/8-2/6 = 1/24`.**

The second conclusion handles every admissible a,b, even though the five
constraints have total duty `5/4`. It uses arithmetic of the fixed core and
integrality of the added speeds, not just mean multiplicity. Positive overlaps
between the added blocked sets can only improve the bound.

A safe set obtained by intersecting S with constraints a,b has at most
`K=a+b+6` positive-length components: S starts with six, and deleting the
blocked intervals of a speed v can increase that count by at most v. This is
a deliberately conservative bound. Endpoints and isolated safe points do
not affect the measure argument; a positive component's closure is safe.
Therefore some closed core-five window has width at least

`w_5 >= 1/[24(a+b+6)]`.

Likewise the four-constraint core has a window of width at least
`5/[24(a+6)]`. Exact one-parameter window selection can substantially improve
this generic width estimate.

## 4. Explicit remaining-speed guarantees

For the two remaining quarter-duty trains c<d, a strict increasing-endpoint
chain uses c at most once and d at most twice. Its total span is strictly below

`T_2=1/(4c)+1/(2d)`.

Hence every closed interval of width at least T_2 has a point safe for both.
Using the core-five window above, the sufficient condition is

`1/(4c)+1/(2d) <= 1/[24(a+b+6)]`.

In particular, **`c>=18(a+b+6)` suffices**, since d>c makes
`T_2<3/(4c)`. This is a parameter-dependent selected-reference guarantee.
If earlier arguments bound a and b in the unresolved cases, it gives a finite
bound on c in those remaining cases. It does not yet bound d.

A second useful conditional regime absorbs c before applying the one-train
window bound. Let `K=a+b+6`, and apply the periodic-primitive estimate to each
positive component of the core-five safe set. Its surviving measure after c
is at least

`(3/4)*(1/24)-3K/(16c) = (c-6K)/(32c)`.

Thus c>6K guarantees a positive core-six window, with width at least

`(c-6K)/[32c(K+c)]`.

An additional speed d cannot cover a closed interval whose width is at least
its blocked-interval width `1/(4d)`. Consequently

**`c>6K` and `d>=8c(K+c)/(c-6K)` suffice.**

The sharper version uses the actual core-five measure R and actual positive
component count k: c>k/(4R) gives core-six measure at least
`(3/4)R-3k/(16c)`, and the same one-train argument applies. The generic
constants above are convenient explicit guarantees, not claimed optimal.

## 5. The next genuine recursive obstruction and the joint arithmetic needed

The fifth constraint is therefore not the stopping point of the elementary
fixed-core argument. The unresolved next universal claim is:

> For every admissible distinct a,b,c, does `{1,4,5,a,b,c}` have a
> positive-measure safe set at threshold 1/8 by a direct argument in this
> framework?

This report does not settle that claim when c<=6(a+b+6). Bounds on a,b,c can
make its parameter set finite while d remains unbounded; finite parameter
count alone is not an exact verification or a proof of the claim. An imported
lower-runner existence theorem would have to be stated and credited, and would
not make that underlying existence conclusion new.

Here is an exact target for higher-order information. Define
`Q_ij=measure(S intersect B_i intersect B_j)` and
`Q_abc=measure(S intersect B_a intersect B_b intersect B_c)`.
Then the six-constraint core has measure exactly

`3/8-Q(a)-Q(b)-Q(c)+Q_ab+Q_ac+Q_bc-Q_abc`.

A positive lower bound on this expression gives a window after division by
the component bound `a+b+c+6`. Pair overlap lower bounds together with a
triple-overlap upper bound can therefore supply the missing measure guarantee.
For example, an arithmetic exclusion of one triple can be useful only after
the remaining signed terms are controlled. A tree correction also gives the
weaker sufficient bound

`3/8-Q(a)-Q(b)-Q(c)+max(Q_ab+Q_ac,Q_ab+Q_bc,Q_ac+Q_bc)`.

These are concrete certificates; there is no assertion that a favorable
certificate must always exist or can always be selected cheaply. They preserve
the repository's distinction between moments, actual overlap placement, and
universal window existence.

## 6. Scope relative to the archived adaptive pair

The September 28 adaptive reflected-pair note already covers every admissible
V in `{0,1,4,5,6,7,11,V}`, including every initial phase of runner 11. It gives
positive duration at least `1/(56V)` when 8 divides V, using directed endpoint
information. Its common-start family coverage was older still. Nothing here
is a new coverage claim for that family or a rediscovery offered as an extension.

The tight `{0,1,4,5,6,7,11,13}` example also warns against requiring positive
measure at the final seven-constraint stage: equality witnesses may be all
that remain. The positive-core/window method must retain the closed-endpoint
test when the last constraints are restored.

Independent review targets: the six core-three intervals; the primitive's
range `3/(16v)`; the twelve scaled-intersection rows; the component-count
argument; the strict chain versus closed-window endpoint implication; and the
distinction between a finite next-core parameter set and a completed reduction.
