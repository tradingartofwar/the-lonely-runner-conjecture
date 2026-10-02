# Independent analytic audit of the core-window reduction

Date: 2026-09-29. Scope: the selected stationary reference in the common-start
integer-speed family with fixed moving core `{1,4,5}`, and residuals
`a<b<c<d`, positive and distinct and outside that core. Threshold: `1/8`,
with equality safe. Baseline pin supplied by the coordinator:
`db2867ed65c4df3668f5275878f21ba400faff2b`.

Status: HYPOTHESIS / proof candidates under internal AI mathematical review;
not external independent review, a novelty claim, or an all-reference theorem.
This report was written without reading the primary implementation or output.
The finite threshold-event verification is separately documented after the
coordinator freezes its scope.

## Positive safe measure after absorbing one residual

For any positive integer `a` outside `{1,4,5}`, let

`S_a = {t in [0,1] : ||v t|| >= 1/8 for v in {1,4,5,a}}`.

Let `M(t)` count the strictly blocking constraints (`||v t||<1/8`).
Each integer speed completes an integer number of periods over `[0,1]`, so
its blocking indicator has integral `1/4`; consequently `integral M = 1`.
With `m=max{5,a}`, all four constraints block on the two common-start
neighborhoods `[0,1/(8m))` and `(1-1/(8m),1]`, whose total measure is `1/(4m)`.
Since `M` is integer-valued,

`measure(S_a) = integral (M-1)_+ >= 3/(4m) > 0`.

The equality is the integral of `M-1`, with the region `M=0` separated from
`M>=1`. The lower bound uses only the excess multiplicity three in the two
common-start neighborhoods. Thus the critical total blocking duty of one
cannot tile the circle: the imposed common-start overlap forces positive
uncovered measure. No selection or scan of physical configurations is used.

The set `S_a` is a finite union of closed intervals, including possible
singletons, because its membership changes only at rational threshold events.
It therefore has at least one positive-length component. More quantitatively,
there are at most `a+10` positive components: every positive component begins
at a safe-entry threshold of at least one speed, and speed `v` has exactly
`v` such thresholds in `(0,1)`. Thus a widest component has width at least

`3 / (4 max{5,a} (a+10))`.

This rough bound is auxiliary; the prescribed finite verification computes
actual widest widths for the coordinator's 31 values of `a`.

## Three-residual span guarantee

Write residual periods as `P=1/b >= Q=1/c >= R=1/d`. A strictly advancing
projection starts at a time strictly inside one open blocking occurrence
and ends at its right endpoint. Its displacement is strictly below the
occurrence width, which is one quarter of that label's period. Consecutive
advances therefore form an actual strictly overlapping chain with increasing
right endpoints. This argument permits arbitrary phases for the three
remaining residuals.

In a two-label chain with periods `u>=v`, the `u` label cannot recur. Between
two successive `u` occurrences there could be at most one `v`, because
successive occurrences of one label cannot strictly overlap. A return would
advance by at least `u` between right endpoints but strictly less than
`(u+v)/4<=u/2`. Therefore a pair chain has at most three occurrences, with
at most one `u` and two `v`.

In a three-label chain, a return to `P` would have a `Q,R` piece between
successive `P` occurrences. The pair result bounds that piece by one `Q`
and two `R`. The return would advance by at least `P` but strictly less
than `(P+Q+2R)/4<=P`, a contradiction. Hence `P` occurs at most once.
The two `Q,R` pieces around it give at most two `Q` and four `R` occurrences.
These statements also cover chains omitting one or more labels.

Starting at the left endpoint `L` of a supplied closed core-safe interval
`W=[L,U]`, repeatedly project any blocking residual to its next safe time,
and stop when all three are safe. More than seven advancing moves would
contradict the occurrence bounds. If any advance occurs, the total waiting
time is strictly below

`T3 = P/4 + Q/2 + R = 1/(4b) + 1/(2c) + 1/d`.

Consequently `width(W)>=T3` guarantees a joint safe point inside `W`.
When `L` is already jointly safe it is the witness; otherwise the witness
is strictly before `L+T3`. Equality in the sufficient width condition is
therefore harmless. A safety check after the last allowed move is required;
advancing moves are not the same as raw scheduled projection calls.

## Scope and review limits

A finite list of `a` values plus finite lower cutoffs for `b` is not a finite
reduction in all residual coordinates. Below the cutoff, `c,d` remain
unbounded. The implication is a sufficient condition on the selected
reference, not a failure assertion when the condition is false. Positive
core-safe measure alone does not show that adding arbitrary three more
constraints preserves any point. These distinctions must survive summary.

## Analytic tail formula before finite evaluation

The inherited fixed-core window `J=[9/32,3/8]` has width `3/32`.
Every component of `S_a` lies within one closed safe lap of speed `a`,
so every component has width at most `3/(4a)`. The starts of those safe laps
form the arithmetic progression `(m+1/8)/a`, with spacing `1/a`.
A full lap lies inside `J` if its start belongs to
`[9/32,3/8-3/(4a)]`. This interval has length at least `1/a` whenever

`3/32 >= 7/(4a)`, equivalently `a>=56/3`.

Any closed interval of length at least `1/a` meets that start progression.
Hence, for every integer `a>=19`, a full safe lap of `a` lies in `J` and
is a complete component of the four-constraint safe set: the immediately
adjacent points outside that lap are blocked by `a`. Therefore the widest
component has exactly

`w_a=3/(4a)`, and the coarse cutoff is `B_a=ceil(7a/3)`.

This tail formula was derived and communicated before the independent finite
evaluation and without reading primary outputs. It explains a full infinite
range analytically; only the 31 frozen inputs are evaluated computationally.
The earliest widest component may occur outside `J`, so the formula by itself
does not determine the protocol's earliest-component tie-break.

## Frozen exact verification and comparison

The coordinator approved `PRIMARY_PROTOCOL.md` with SHA-256
`d5ff2d4e06c1d8c7629c6c115fb9faa23a0a1510791cb9b983903277726e65d0`.
The independent code uses no project imports and never reads or imports the
primary source. Before reading primary output it constructed the exact set of
all threshold events `(8j+1)/(8v)` and `(8j+7)/(8v)`, checked every event with
the modular safety predicate, checked every intervening open cell at its
midpoint, and walked the alternating endpoint/cell topology to reconstruct
all maximal connected components. Endpoint predicates independently retain
isolated safe points. This is separate from the primary's successive
closed-lap-band intersection method.

The exact scope was only `a in {2,3,6,...,34}`: 31 four-speed cores,
1,814 endpoint checks, 1,783 open-cell checks, 348 positive components and
20 isolated points (368 components in all). No residual speed tuples,
phases, words, extra values of `a`, or other reference runners were evaluated.

Before primary-output access, the final independent artifacts were frozen as:

- `independent_core_windows.py` SHA-256
  `71c85ae66897aada6e094ae9c1df6b1b12b4fc80650b69931f8b4aec6c936d14`;
- `independent_core_windows.json` SHA-256
  `434fcbb15424c6c2d4387a1281eef2a808dcbd34a281ac73d85c7372c29a587e`.

The comparison then read primary JSON SHA-256
`4bbf907e6dc9b85d868a4d739e7f75a88969dead514ae2aca4a9879ca7fa997a`.
All 31 records agree across **1,932 numerical leaf fields**, counting speed
labels, endpoints, safe measures, component and tie counts, selected point
distances, widths and coarse cutoffs. Compound objects and their ordering
also agree. All positive components and isolated points are included.
Repeated endpoints and derived quantities are counted as fields, not as
independent observations. There were zero disagreements.

The coordinator additionally authorized comparison of the twelve hand
`Q(v)` totals in `scope.md`. Each uses an already-evaluated core row through
`Q(v)=3/8-measure(S_v)`. All twelve values agree:

| v | Verified Q(v) |
| ---: | ---: |
| 2 | 1/16 |
| 3 | 1/6 |
| 6 | 17/120 |
| 7 | 89/560 |
| 8 | 1/16 |
| 9 | 1/9 |
| 10 | 1/20 |
| 11 | 93/880 |
| 12 | 1/12 |
| 13 | 23/208 |
| 14 | 69/560 |
| 15 | 7/80 |

This compares the final `Q` totals, not the three hand `q_A,q_B,q_C` columns
separately. The comparison source and output are `compare_independent.py`
and `independent_comparison.json`. Reproduction from the repository root:

```bash
python reviews/2026-09-29-core-windows/independent_core_windows.py --protocol-hash d5ff2d4e06c1d8c7629c6c115fb9faa23a0a1510791cb9b983903277726e65d0
python reviews/2026-09-29-core-windows/compare_independent.py
```

## Review of the fixed-core measure extension

The six displayed components of the `{1,4,5}` safe set have total measure
`3/8`. A periodic primitive of the speed-v blocking indicator minus `1/4`
has exact range `3/(16v)`: the rise on the blocked part of one period is
`(3/4)*(1/(4v))`, equalling the fall on the remaining safe part. Therefore
on any closed interval the blocking measure is at most one quarter of its
length plus that range. Applying the bound to the six components gives

`Q(v)<=3/32+9/(8v)<=21/128<1/6` for `v>=16`.

Together with the twelve independently verified `Q` totals, this supports
`Q(v)<=1/6` for every positive integer `v` outside the fixed core. Thus the
safe measure after absorbing both `a,b` is at least `1/24`, without a scan
of their pairs. Deleting the blocked intervals of a speed v increases the
number of positive components by at most v; boundary-clipped intervals do
not increase this bound. Hence `K=a+b+6` is a conservative component bound.
The widest positive component has width at least `1/(24K)`.

The pair-chain displacement is strictly below
`1/(4c)+1/(2d) <= 3/(4c)`, so `c>=18K` indeed suffices. The extension that
also absorbs c gives surviving measure at least
`1/32-3K/(16c)=(c-6K)/(32c)`, and positive-component count at most `K+c`.
For `c>6K` its widest component is at least
`(c-6K)/(32c(K+c))`. Requiring this to be at least the last blocker's width
`1/(4d)` gives exactly `d>=8c(K+c)/(c-6K)`. These algebraic implications
are consistent. They do not establish a positive six-constraint core when
`c<=6K`, nor make the full unresolved d direction finite.

No fatal defect was identified in the reviewed arguments. The new mathematical
implications remain proof candidates under internal AI review. Exact finite
agreement is OBSERVED/reproduced arithmetic within its stated scope, and is
not an independent human proof certificate or a novelty audit.
