# Two variable runners can cooperate, but this family still has an opening

**September 24, 2026.** Vance approved moving from one variable runner to two. We retain five fixed relative speeds and ask whether the added pair can take turns blocking every opportunity.

**Outcome:** a written finite-reduction argument covers every admissible integer pair in this family. A local duration estimate handles all pairs with both speeds at least 34. Certificates for 28 possible smaller speeds leave eight pairs, each with a directly verified lonely time. Independent proof review remains outstanding; no novelty or general Lonely Runner theorem is claimed.

[Reproduction script](../scripts/analyze_two_variable_speeds.py) · [Exact certificates](../experiments/two_variable_speeds.json). Run `python -m scripts.analyze_two_variable_speeds`.

## Claim and conventions

The eight velocities are

$$\{0,1,4,5,6,7,x,y\},\qquad
0<x<y,\quad x,y\in\mathbb Z,\quad x,y\notin\{1,4,5,6,7\}.$$

All start together. Only the speed-zero reference is studied. Ordering x and y loses nothing because their labels are interchangeable. The goal is a time t for which all seven distances `||vt||` to the nearest integer are at least `delta=1/8`. The original total remains eight when we temporarily omit constraints. The argument does not handle arbitrary real x,y, certify other references, or determine every configuration's maximum.

## First, the previous argument really does break

Our earlier clear interval was

$$I=[17/56,5/16].$$

Choose the added speeds **16 and 23**. Speed 23 blocks the left side through its seventh meeting; speed 16 blocks the right side through its fifth meeting:

$$B_{23,7}=(55/184,57/184),\qquad
B_{16,5}=(39/128,41/128).$$

Their endpoints satisfy

$$55/184<17/56<39/128<57/184<5/16<41/128.$$

Thus their open windows cover the entire closed I, with an overlap of `15/2944`. Neither runner can do this alone: speed 16 is `1/7` away at I's left endpoint, while speed 23 is `3/16` away at its right endpoint. Speed 16 also blocks the old eighth times. This is genuine cooperative blocking, so reusing the single-runner argument unchanged would be wrong.

Nevertheless, another full interval remains clear for this pair, and at `t=5/11` the seven distances are

$$\frac1{11}(5,2,3,3,2,3,5),$$

in speed order `(1,4,5,6,7,16,23)`. The minimum is `2/11>1/8`. Closing one opening does not certify complete coverage.

## A new interval and an exact duration bound

The five fixed runners are clear throughout

$$J=[25/56,15/32],\qquad L=|J|=5/224.$$

The following affine phase certificate checks every time in J, not just a grid. Each integer part stays fixed, and each phase increases between the displayed values inside `[1/8,7/8]`.

| Speed | Integer part | Phase at left | Phase at right |
| --- | ---: | --- | --- |
| 1 | 0 | 25/56 | 15/32 |
| 4 | 1 | 11/14 | 7/8 |
| 5 | 2 | 13/56 | 11/32 |
| 6 | 2 | 19/28 | 13/16 |
| 7 | 3 | 1/8 | 9/32 |

For a runner of speed v, let `D_v(J)` be its total strictly-too-close duration inside J. Each full period `1/v` is blocked for exactly one-quarter of its duration. This does **not** mean that a short interval J is one-quarter blocked: a slow runner might cover all of J. We must account for partial periods.

Write `vL=q+r`, where q is a nonnegative integer and `0<=r<1`. Partition J into q full periods and one remainder. The full periods contribute `q/(4v)`; the remainder can contribute at most `min(r,1/4)/v`. Therefore

$$D_v(J)\le\frac{q/4+\min(r,1/4)}v
=\frac L4+\frac{\min(r,1/4)-r/4}v
\le\frac L4+\frac3{16v}.$$

For `r<=1/4`, the last numerator is `3r/4<=3/16`; for `r>=1/4`, it is `(1-r)/4<=3/16`. This proves the boundary allowance for every speed and starting phase of J. Open endpoints do not change duration, but they still count as allowed when selecting a witness.

The union of two runners' blocked times has duration at most the sum of their individual durations, regardless of overlap. If `x,y>=34`, the duration they leave clear in J is consequently at least

$$L-\left(\frac L2+\frac3{16}\left(\frac1x+\frac1y\right)\right)
\ge\frac5{448}-\frac3{272}
=\frac1{7616}>0.$$

So both runners cannot be fast enough to fall in this range and still cover J. **Any hypothetical complete blocker has smaller speed x<34.** This handles an unbounded region of speed pairs with one inequality.

## The remaining infinite strips reduce to eight pairs

First use the old time `1/8`. Every fixed speed is clear there. If neither x nor y is divisible by 8, both added runners are clear too. A hypothetical complete blocker must therefore satisfy `8|x` or `8|y`.

For each remaining smaller speed `x<34`, select a positive-length closed interval `J_x` clear for the five fixed speeds and x. The larger speed y would have to cover this whole connected interval by its disjoint open blocking windows. Just as in the [single-variable argument](VARIABLE_SPEED_FAMILY.md), this requires

$$\frac1{4y}>|J_x|,\qquad y<\frac1{4|J_x|}.$$

The following table covers **every** admissible smaller integer x. All 28 intervals have direct affine phase certificates in the JSON, separately checked from the interval-intersection procedure that selected them. The argument only needs a certified interval of the stated width, not a claim that it is the longest possible one. The last column additionally imposes `y>x`, distinctness from the fixed speeds, and divisibility of at least one variable speed by 8.

| Smaller speed x | Certified interval J_x | Necessary y < | Remaining y |
| ---: | --- | ---: | --- |
| 2 | [17/48, 3/8] | 12 | 8 |
| 3 | [25/56, 15/32] | 56/5 | 8 |
| 8 | [25/56, 15/32] | 56/5 | 9, 10, 11 |
| 9 | [17/48, 3/8] | 12 | none |
| 10 | [25/56, 15/32] | 56/5 | none |
| 11 | [17/56, 5/16] | 28 | 16, 24 |
| 12 | [25/56, 15/32] | 56/5 | none |
| 13 | [17/48, 3/8] | 12 | none |
| 14 | [25/56, 15/32] | 56/5 | none |
| 15 | [17/48, 3/8] | 12 | none |
| 16 | [25/56, 15/32] | 56/5 | none |
| 17 | [25/56, 63/136] | 119/8 | none |
| 18 | [17/48, 3/8] | 12 | none |
| 19 | [25/56, 71/152] | 133/11 | none |
| 20 | [57/160, 3/8] | 40/3 | none |
| 21 | [25/56, 15/32] | 56/5 | none |
| 22 | [17/56, 5/16] | 28 | 24 |
| 23 | [25/56, 15/32] | 56/5 | none |
| 24 | [17/48, 71/192] | 16 | none |
| 25 | [25/56, 15/32] | 56/5 | none |
| 26 | [17/48, 3/8] | 12 | none |
| 27 | [97/216, 15/32] | 216/17 | none |
| 28 | [81/224, 3/8] | 56/3 | none |
| 29 | [17/48, 3/8] | 12 | none |
| 30 | [25/56, 37/80] | 140/9 | none |
| 31 | [89/248, 3/8] | 31/2 | none |
| 32 | [25/56, 119/256] | 448/33 | none |
| 33 | [11/24, 15/32] | 24 | none |

Exactly eight pairs remain. Each has a simple rational witness:

| Pair (x,y) | Valid time | Minimum distance to selected runner |
| --- | --- | --- |
| (2,8) | 4/13 | 2/13 |
| (3,8) | 5/11 | 2/11 |
| (8,9) | 6/13 | 2/13 |
| (8,10) | 5/11 | 2/11 |
| (8,11) | 4/13 | 2/13 |
| (11,16) | 7/15 | 2/15 |
| (11,24) | 4/13 | 2/13 |
| (22,24) | 4/13 | 2/13 |

Every displayed distance exceeds `1/8`. The script checks all seven distances directly and verifies membership in the independently calculated allowed intervals. These witness values are not claims of global maxima.

The argument is exhaustive for the stated integer family: the modular case, the fast case, the 28 smaller-speed intervals, and the eight residual witnesses cover every admissible pair. The computation is finite because of the reduction, not because an arbitrary search cutoff was chosen.

## Patterns, counterchecks, and the next conceptual limit

1. **Two runners can share an opening.** The `(16,23)` example covers the entire old interval through strict overlap, yet preserves the new J. The previous one-runner mechanism genuinely needed to be extended.
2. **Faster does not mean better at covering a fixed opening.** For the prescribed fast pair `(40,48)`, both runners destroy the old eighth times, but their exact clear duration within J is `73/6720`, above the universal fast-case guarantee `1/7616`. The boundary allowance is essential; a quarter-cycle fraction cannot simply be applied to an arbitrary short interval.
3. **The residual witnesses recur at familiar fractions.** Four use `4/13`, where speeds 6 and 7 balance; two use `5/11`, where speeds 4 and 7 balance. These are useful witnesses, not universal times: adding speed 13 or 11 respectively produces a collision there. No Fibonacci restriction is involved.
4. **Strict slack in the eight residual checks does not make the whole family non-tight.** The existing pair `(11,13)` belongs to this family and leaves only the four isolated odd-eighth times. The script rechecks this complete allowed set. The family therefore contains both positive-duration openings and exact touches.

For r variable runners at the unchanged eight-runner target, treat `7-r` competitors as fixed, keeping eight total runners including the reference. The same duration calculation gives

$$\left|J\setminus\bigcup_{i=1}^r B_{v_i}\right|
\ge \left(1-\frac r4\right)L-\frac3{16}\sum_{i=1}^r\frac1{v_i},$$

provided the fixed runners are clear on J. With one, two, or three added runners, sufficiently high speeds make this bound positive. With **four**, the leading term vanishes; even letting all speeds grow cannot make this particular lower bound positive. This is a limitation of the estimate, not a counterexample or a claim that four runners really cover the interval. Forced overlaps or further arithmetic restrictions would then need to supply information that the sum of durations discards.

That suggests a useful next conceptual question: **what forces enough overlap when the individual blocking durations could add up to complete coverage?** It is a proposed continuation, not a completed three- or four-variable result.

## Evidence and provenance

The computation records 28 closed-interval certificates, eight residual-pair witnesses, and three prescribed pair controls: cooperative `(16,23)`, fast `(40,48)`, and tight `(11,13)`. All use exact fractions. The unbounded steps are the written periodic-duration bound and connected-interval argument. No broad speed scan, all-reference computation, sampled-time certification, or new maximum classification was run.

[Tao's exposition, S4](https://terrytao.wordpress.com/2017/01/10/some-remarks-on-the-lonely-runner-conjecture/), re-opened September 24, supplies established context for Bohr-set coverage, the individual duration `2*delta`, and the union-bound obstruction. His n counts moving speeds, our n-1; his extremal-radius formulation uses closed sets, while strictly-too-close intervals at our fixed threshold are open. The local boundary estimate and fixed-family reduction are derived explicitly above. We do not use the source's historical frontier as current status or present this family as a new result. The argument has not received independent proof review.

Vance supplied the direction to investigate cooperation beyond the single-variable family; the AI supplied this reduction, certificates, and counterchecks. This account records the work and its limits, without treating the repository note as independent corroboration.

September 24 follow-up: [local overlap](LOCAL_OVERLAP.md) responds to Vance's suggestion that an omitted quantity might create room. With three fixed speeds and four other competitors, it tracks `clear duration = redundancy - excess local blocking`. A doubled pair q,2q has union fraction 3/8, allowing an independent positive-duration bound for the structured family `{0,1,4,5,q,2q,u,v}` when q>=53 and u,v>=q, with all speeds distinct. This overcomes the coarse four-individual-duration estimate for that family; it does not settle arbitrary four-speed inputs and still needs independent proof review.
