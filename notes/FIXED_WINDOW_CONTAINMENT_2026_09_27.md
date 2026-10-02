# Which speeds preserve the fixed-window containment?

September 27, 2026. Baseline `9831bbee22c0e226911eac99e65a0c9624bef963`. This completes the replacement-speed classification proposed in [CORE_EXCHANGE_NEIGHBORS_2026_09_27.md](CORE_EXCHANGE_NEIGHBORS_2026_09_27.md). Material AI involvement includes the derivation, implementations, calculations, and writing.

**Result:** there are exactly 30 admissible replacements for speed 11 under the stated containment condition. The largest is 73. Five meet the safety threshold at an endpoint and must be retained. The same core, window, and tree then give an exact duration for every admissible y and a positive bound for every integer y>=29. A small integer-lattice certificate explains the finite reduction.

The finite calculations are OBSERVED / independently REPRODUCED in the stated scope. Completeness over all positive integers and the all-y consequences are supplied arguments, retained as HYPOTHESIS / proof candidates under [CLAIM_STATUS.md](../CLAIM_STATUS.md), pending further independent review. No novelty, newly covered Lonely Runner family, or full-conjecture result is claimed.

## The precise question

Keep eight common-start runners

\[
\{0,1,4,5,6,7,x,y\},
\]

with reference 0, threshold 1/8, positive integer x,y, and all eight original speeds distinct. In particular, x,y are not in `{1,4,5,6,7}` and x is not y. We do not change the runner count when a condition is redundant on a window.

Write `B_v={t: ||vt||<1/8}`. The fixed core `{1,4,6}` has the complete safe component

\[
J=[9/32,5/16].
\]

On J, speed 5 never blocks and speed 7 leaves exactly

\[
S=[17/56,5/16],\qquad |S|=1/112.
\]

Thus the precise condition being classified is

\[
B_x\cap J\subseteq B_7\cap J
\quad\Longleftrightarrow\quad B_x\cap S=\varnothing.
\]

This is containment of the strict blocking sets, including correct behavior at their endpoints. It is not a classification of all configurations with lonely time, all successful cores, or all successful trees.

## A complete finite reduction and a lattice certificate

The map t -> xt sends the connected interval S to a connected real interval. The safe lifted phase set consists of separated closed intervals `[m+1/8,m+7/8]`, for integer m. Therefore all of S is safe for x exactly when **one common lap m** satisfies

\[
m+1/8\le17x/56,\qquad5x/16\le m+7/8.
\]

Checking the two circular endpoint distances alone would lose the common-lap condition. For example, x=85 is safe at both endpoints, but t=26/85 lies strictly inside S and gives an exact collision. This is a failure of that weaker endpoint test, not of Lonely Runner.

The common-lap criterion is equivalent to

\[
\left\lceil5x/16-7/8\right\rceil
\le\left\lfloor17x/56-1/8\right\rfloor.
\]

The lifted interval has width x/112, while a safe lap has width 3/4. Hence x<=84 is necessary, so checking x=1,...,84 exhausts the positive integer possibilities once this reduction is accepted.

There is also a two-dimensional integer-lattice formulation:

\[
17x-56m\ge7,\qquad5x-16m\le14.
\]

For a feasible integer point define nonnegative integer slacks

\[
p=17x-56m-7,\qquad q=16m+14-5x.
\]

They obey

\[
\boxed{2p+7q=84-x},\qquad
m=\frac{203-5p-17q}{8}.
\]

The first identity supplies the same upper bound directly; the second retains the integer compatibility that an interval-width bound discards. The phase margins at the left and right endpoints are respectively p/56 and q/16. At x=84, the first identity forces p=q=0, but the resulting m=203/8 is not an integer. Thus even equality in the width bound is insufficient.

Equivalently, for each lap m,

\[
\frac{56m+7}{17}\le x\le\frac{16m+14}{5}.
\]

Feasibility requires `0<=m<=25`, because `8m<=203`. The independent verifier enumerates the integer points using these two inequalities, separately from the floor/ceiling classification. There are 35 points. At m=22, only x=73 occurs; the last three lap intervals contain no integers:

| m | Lower x | Upper x | Integer x |
| ---: | ---: | ---: | --- |
| 23 | 1295/17 | 382/5 | None |
| 24 | 1351/17 | 398/5 | None |
| 25 | 1407/17 | 414/5 | None |

These calculations give a concrete lattice certificate for this selected window. They do not construct a lattice representation that resolves arbitrary runner configurations.

## The classification

All five fixed moving speeds `{1,4,5,6,7}` occur among the 35 safe values. They are excluded as replacements because the original eight speeds must be distinct. The remaining 30 are:

```
 2,  8,  9, 11, 12, 14, 15, 17, 18, 21,
22, 24, 25, 27, 28, 31, 34, 37, 38, 40,
41, 44, 47, 50, 54, 57, 60, 63, 70, 73.
```

Twenty-five are strictly safe throughout the closed interval S. The other five are strictly safe in its interior and attain distance exactly 1/8 at one endpoint:

| x | Lap m | Endpoint at threshold | Left phase margin | Right phase margin |
| ---: | ---: | --- | ---: | ---: |
| 22 | 6 | 5/16 | 31/56 | 0 |
| 38 | 11 | 5/16 | 23/56 | 0 |
| 54 | 16 | 5/16 | 15/56 | 0 |
| 63 | 19 | 17/56 | 0 | 3/16 |
| 70 | 21 | 5/16 | 1/8 | 0 |

The endpoint cases satisfy the containment. Removing them would silently change the problem's non-strict safety condition. Endpoint contact here does not mean the whole configuration has only isolated lonely time: the y>=29 certificate below gives positive duration even for these five replacements.

The [exact archive](../reviews/2026-09-27-lr2/fixed_containment.json) records every x=1,...,84, an additional x=85 failure control, every feasible lap and margin, and a rational strict blocking witness for every rejected value. Values 74,...,84 all fail; 73 is the actual maximum, whereas 84 is the analytic search bound.

## What the same certificate now guarantees

Let `D_v=|B_v intersect J|` and `O_uv=|B_u intersect B_v intersect J|`. For any listed x, use the fixed tree on residual labels `{5,7,x,y}` with edges `(5,7),(7,x),(7,y)`. Since `D_5=O_5,7=0` and `O_7,x=D_x`,

\[
\begin{aligned}
T_J(x,y)
&=|J|-D_5-D_7-D_x-D_y+O_{5,7}+O_{7,x}+O_{7,y}\\
&=\frac1{112}-|B_y\cap S|\\
&=U_J(x,y).
\end{aligned}
\]

This identity holds for every admissible positive integer y, not just large y. Indeed the entire allowed set on J is `S minus B_y`, independent of which of the 30 listed x is used. This is a local conditional equivalence among these replacements, not equality of their full-period behavior or of all their overlap statistics.

The previous note's primitive argument gives

\[
U_J(x,y)\ge\frac3{448}-\frac3{16y}>0\quad(y>28).
\]

For completeness, a primitive of the 1/8 blocking indicator is

\[
A(z)=\lfloor z\rfloor/4+\min(\{z\},1/8)+\max(0,\{z\}-7/8).
\]

The periodic correction `A(z)-z/4` is affine between fractional parts `0,1/8,7/8,1`, with respective values `0,3/32,-3/32,0`. Its range has width 3/16. Thus `|B_y intersect S|=[A(5y/16)-A(17y/56)]/y <= |S|/4+3/(16y)`, proving the displayed sufficient bound.

Consequently the same certificate works for all 30 listed x and every integer y>=29 subject to distinctness. The labels x,y can be interchanged, although this classification assigns x the containment role. This certifies strict lonely time for reference 0; it does not silently assert a result for every reference.

As a finite check, all 30 configurations at y=29 have exactly the same allowed portion of J,

\[
[17/56,71/232],\qquad U_J=1/406,
\]

and the common strict witness `495/1624` passes all seven constraints. The earlier y=44,45,46 values at x=11 reproduce exactly. The y=28 control at x=11 has U=1/112, so 29 is a sufficient uniform cutoff, not a necessary threshold for success.

## A failed containment can still give a successful certificate

For arbitrary admissible x,y, the same star tree obeys the more informative identities

\[
T_J=|S|-|B_x\cap S|-|B_y\cap S|,
\]

\[
U_J-T_J=|B_x\cap B_y\cap S|.
\]

To check the second identity pointwise: where 7 blocks, the tree expression and uncovered indicator both vanish; where 7 is safe, their difference is the product of the two remaining blocking indicators. Speed 5 is always safe on J. Integration gives the formula with no endpoint-measure ambiguity. The separately reconstructed allowed sets still retain all equality points.

The list therefore describes a condition that makes this tree exact **uniformly in y**. For a fixed pair, exactness only requires zero simultaneous blocking by x and y inside S, and positivity may hold even with some simultaneous blocking.

The control x=19,y=45 demonstrates the latter distinction. Neither is in the containment list. Their strict blocking portions in S are `(47/152,5/16]` and `(37/120,5/16]`, respectively. The exact calculations give

\[
T_J=47/31920>0,\qquad U_J=1/210,\qquad U_J-T_J=1/304.
\]

Thus failure of containment is not failure of the tree and certainly not failure of lonely time.

There is also a converse to uniform exactness. If x fails containment, `B_x intersect interior(S)` contains a nonempty open interval. Choose a rational time r there and choose y to be a sufficiently large multiple of its denominator, avoiding the finitely many disallowed speeds. Then yr is an integer. Both x and y strictly block in a neighborhood of r, so `|B_x intersect B_y intersect S|>0`, and the tree is not exact for that y. This argument works with y>=29 as well. It establishes the precise uniform-exactness role of the containment list, without asserting that the resulting non-exact tree is nonpositive.

## Verification and claim limits

The primary program uses rational floor/ceiling arithmetic for the classification, an exact periodic primitive for blocked duration, threshold-event state masses for the tree moments, and closed safe-interval intersections for the allowed sets. The independent verifier imports no project code: it enumerates integer lattice points, tests strict containment at all event vertices and open cells, reconstructs allowed sets from threshold events, and calculates moments by intersecting blocking intervals.

Both implementations agree on 85 classifications, the 35 raw feasible values, all five admissible endpoint contacts, and 35 full local certificates: every listed x at y=29; x=11 at y=28,44,45,46; and the x=19,y=45 countercontrol. Every positive-duration case includes a strict rational witness checked against all seven moving speeds.

```bash
python -B reviews/2026-09-27-lr2/check_fixed_containment.py --check
python -B reviews/2026-09-27-lr2/crosscheck_fixed_containment.py --check
```

- [Primary calculation](../reviews/2026-09-27-lr2/check_fixed_containment.py)
- [Exact archive](../reviews/2026-09-27-lr2/fixed_containment.json)
- [Independent verifier](../reviews/2026-09-27-lr2/crosscheck_fixed_containment.py)
- [Independent comparison](../reviews/2026-09-27-lr2/fixed_containment_crosscheck.json)
- [Package manifest](../reviews/2026-09-27-lr2/fixed_containment_manifest.json)

No existing checker or earlier evidence archive changed. The broader regression suite and prior all-core enumeration were not rerun. These are new calculations about an existing family's certificate, not a novelty/literature assessment or outside proof review. The analytic finite reduction is stated explicitly; the finite replay alone does not certify unbounded claims.

## What this suggests next

The useful information here is a **conditional implication on a selected opening**: when 7 is safe, x is safe. The lattice inequalities certify that implication for this window. They retain lap alignment, which a width bound or separate circular endpoint tests discard. This is one precise version of the earlier intuition that useful information can belong to relationships among constraints.

The next high-value investigation is a small test of a selector driven by these implications. On the already studied named controls, construct directed edges `u -> v` when `B_u intersect J` is contained in `B_v intersect J`, mark blockers that vanish on J, and ask which successful or failed tree windows this structure predicts. Include the x=19,y=45 control so the proposed selector can fail honestly: absence of a containment does not exclude success. Compare implication structure with the exact simultaneous-blocking slack, before scanning a larger domain. That selector experiment has not been performed here. The +7/+9 extension remains parked.
