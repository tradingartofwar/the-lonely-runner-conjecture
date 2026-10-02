# Identical complete duration data, different local existence

September 27, 2026. Continuation of the [physical duration-collision investigation](RESIDUE_COLLISIONS_2026_09_27.md). Baseline: `8a4b1415aff92a53473237183b18076cdc2d8537`. Material AI involvement: derivation, exact computation, counterchecks, and writing.

**Result:** two actual common-start eight-runner configurations have identical **every-order joint blocking durations** on the same window, and identical pair gcds among all seven nonzero relative speeds, yet one has a lonely instant in that window and the other has none.

Keep `{0,1,3,4,5,10,28}` fixed and compare the eighth speeds **1680 and 3360**. For reference 0, threshold `1/8`, core `{1,4,5}`, and `J=[9/32,3/8]`:

| Eighth speed | Complete allowed set in J | Clear duration |
| --- | --- | ---: |
| 1680 | `{9/32}` | 0 |
| 3360 | Empty | 0 |

This establishes physical information loss about **local existence**, beyond the earlier 45/90 loss about positive duration. Both configurations have a strict lonely witness outside J at `t=11/64`, with minimum distance `9/64>1/8`. The example does not defeat Lonely Runner; it defeats a proposed sufficient local summary.

**Status:** the concrete examples, complete moment matches, and finite classification below are **OBSERVED**, independently counterchecked. The assertion that complete local joint duration moments, even with these pair gcds, always determine local nonemptiness for common-start integer configurations is **DISPROVEN**. The written unbounded family and arithmetic arguments are **HYPOTHESIS/proof candidates** pending independent review. No novelty claim is made.

## 1. What exactly agrees

Label the four extra blockers `(3,10,28,y)`, with `B_v={t in J: ||vt||<1/8}`. Equality at the threshold is safe. For every subset A of these four labels, record the duration of their simultaneous blocking, including the empty-subset duration `|J|`.

All 16 moments agree for y=1680 and y=3360. Consequently all 16 exact-state durations also agree: the amount of time during which precisely any chosen subset blocks is the same. The core is safe everywhere in J, so every blocking moment involving a core runner is zero. Thus the match extends to **all 128 subset moments of the seven nonreference runners**.

The following fixed-region lengths determine the entire common moment vector:

| Subset of fixed blockers | Its intersection duration |
| --- | ---: |
| Empty subset, meaning J | 3/32 |
| {3} | 1/12 |
| {10} | 1/40 |
| {3,10} | 1/48 |
| {28} | 3/112 |
| {3,28} | 1/56 |
| {10,28} | 3/1120 |
| {3,10,28} | 0 |

Adding y to any row multiplies its duration by exactly **1/4**, for both configurations. This supplies the other eight moments. The archive also contains every exact-state mass, not merely a digest of equality.

Every fixed nonzero speed in `{1,3,4,5,10,28}` divides 1680. Therefore its gcd with either variable speed is that fixed speed itself; all fixed-fixed gcds are unchanged. This preserves all 21 pair gcds among the seven nonzero relative speeds. It does not preserve raw speeds, reduced ratios, full temporal order, or statistics for other reference runners. Including the stationary reference in a gcd would directly reveal y through `gcd(0,y)=y`; that is not the pair-repetition summary being tested.

## 2. A complete constructive explanation

The fixed blocking sets in J are

`B3=(7/24,3/8)`,

`B10=(23/80,5/16)`,

`B28=(9/32,65/224) union (71/224,73/224) union (79/224,81/224)`.

The first B28 interval overlaps B10, and B10 overlaps B3. Together they cover the whole open interval `(9/32,3/8)`. Both endpoints are safe for all fixed runners. Thus before adding y, the complete allowed set is exactly

`{9/32,3/8}`.

Now let **y=1680h**, for any positive integer h. At the two candidates,

`y(3/8)=630h`,

`y(9/32)=945h/2`.

The right endpoint is always strictly blocked. At the left endpoint, odd h gives phase 1/2 and even h gives phase 0. Hence

`F_J(1680h)={9/32}` for odd h, and `F_J(1680h)=empty` for even h.

To show that all joint durations remain unchanged, use the same exact primitive as the preceding investigation:

`C(z)=floor(z+1/8)/4+min(frac(z+1/8),1/4)`,

`psi(z)=C(z)-z/4`.

The function psi is 1-periodic and satisfies **psi(0)=psi(1/2)=1/8**. Every endpoint of every fixed blocking region lies on the grid with denominator

`lcm(32,24,80,224)=3360`.

Multiplying any such endpoint by 1680h gives an integer or half-integer. Therefore, for every interval [a,b] whose endpoints come from this grid,

`|B_y intersect [a,b]|=(b-a)/4+(psi(yb)-psi(ya))/y=(b-a)/4`.

Every fixed intersection and every fixed exact-state region is a finite union of such intervals. Thus adding y blocks exactly one quarter of each region in duration, for **every h**. All joint moments and all exact-state durations are constant throughout the infinite class `{1680,3360,5040,6720,...}`, while local existence alternates.

The underlying distinction is precise: the periodic primitive has the same value at phase 0 and phase 1/2, while the blocking indicator has different values there. Equal accumulated duration does not force equal instantaneous safety. The physical speed constraint does not remove that ambiguity in this family.

## 3. The closed geometric certificate

For y=1680 and witness `t=9/32`, order the nonzero speeds as

`(1,3,4,5,10,28,1680)`.

Their safe-lap labels are

`(0,0,1,1,2,7,472)`.

Intersecting the closed intervals `(k+1/8)/v <= t <= (k+7/8)/v` gives exactly `{9/32}`. Speed **4** sets the lower bound and speed **28** sets the upper bound. The cell has zero width but is feasible. Speed 1680 lies at phase 1/2 there and preserves it. Speed 3360 is at phase 0 and removes it.

The same construction works for every odd h, with variable lap `(945h-1)/2`. No assignment can survive at either endpoint for even h, and the fixed runners already block the entire interior.

This identifies a sufficient repair for this family: retain the closed feasibility of the two fixed candidate contacts, or just the left-endpoint safety bit once the right endpoint is excluded. Adding further duration moments cannot repair the loss because every such moment already agrees. Computing a useful small candidate-contact set for general configurations remains a separate problem.

## 4. Why the original fixed-speed-3 test gave a negative result

The requested starting family was `{0,1,4,5,6,7,3,y}` on the same J. Its fixed blockers leave only `{3/8}`. Adding y removes this point exactly when 8 divides y.

That family has more identifiability than expected: write the **individual** blocked duration on J as a reduced fraction `D_y=p/q`, taking q=1 if D_y=0. Then

**`8 divides y` if and only if `64 divides q`.**

So D_y alone determines whether the sole candidate survives. No exact match of complete moments can have different local existence in this family.

Here is a short all-speed argument. Every clipped blocking-interval endpoint has denominator dividing `lcm(8y,32)`. If 8 does not divide y, that denominator contains at most five factors of 2; so the reduced denominator of D_y cannot be divisible by 64. Conversely:

| Speed class | Exact duration consequence | Power of 2 in reduced denominator |
| --- | --- | --- |
| 16 divides y | D_y=3/128 | Exactly 7 |
| y=8h with h odd | D_y=(an odd integer)/(64h) | Exactly 6 |
| 8 does not divide y | Denominator divides lcm(8y,32) | At most 5 |

For the first row, the scaled window endpoints have integer or half-integer phases, with equal psi corrections. For the second, the right endpoint is an integer phase and the left is a quarter or three-quarter phase; the scaled blocked length is an odd multiple of 1/8. These observations give the stated exact denominator powers. A separate 32-residue congruence certificate in the verifier checks the same all-speed argument using `D_y=(3y+c_r)/(128y)` for `r=y mod 32`.

This denominator fact concerns **any positive integer speed on this particular J**, not only the fixed-speed-3 family. Consequently matching labelled single durations preserves safety at 3/8 across arbitrary common-start positive integer configurations at threshold 1/8. The unsuccessful endpoint cannot be made ambiguous merely by changing the other fixed runners.

However, this does not reconstruct every endpoint. In the original family, y=336 and y=672 match all joint duration moments, but at the left endpoint 9/32 they have phases 1/2 and 0. Fixed runner 7 already blocks that endpoint, so the lost distinction does not change the allowed set. This exact control suggested changing the fixed runners to `(3,10,28)`: it makes the hidden left-endpoint distinction consequential while maintaining the same core, window, threshold, runner count, and common start. The second construction is an evidence-driven change of fixed triple, not a counterexample within the first triple.

## 5. Complete classification of the original family

This calculation is preserved even though the shorter denominator proof already excludes the desired match there.

For the original labels `(6,7,3,y)`, all joint moments follow from

`M(y)=(D_y,O6,y,O7,y,O3,y)`.

Indeed B6 is contained in B3, B6 and B7 are disjoint, and B7 union B3 covers J except for its right endpoint. Therefore

`T6,3,y=O6,y`,

`T7,3,y=O7,y+O3,y-D_y`,

and the other triples and quadruple have zero duration. These are measure identities; the endpoint exception is retained separately.

The rational endpoints have period `P=lcm(32,48,56,24)=672`. As in the previous note,

`M(y)=M0+e(r)/(4Py)`, with `r=y mod P`.

The exhaustive coefficient table has 534 nonzero signed primitive-vector classes, containing 168 unordered pairs of residues that could be proportional. None of these primitive-vector classes mixes divisibility by 8. Enforcing the speed congruences gives 34 nonzero residue-pair collision families: **12 have empty J and 22 have `{3/8}` in both configurations**. A separate zero-vector class comprises all positive multiples of 336, all with empty J. The same primitive-vector and coprime-multiplier reduction as the preceding note proves completeness; all family parameterizations are archived.

Concrete controls include 48/144 with identical complete moments and empty J, 95/190 with identical complete moments and `{3/8}`, and 336/672 in the zero-vector class. Thus the exclusion is not simply injectivity of the summary.

Less informative overlaps can still match across opposite outcomes: speeds 2 and 8 have the same O6,y=O7,y=0; speeds 10 and 24 have the same O3,y=1/48. D_y separates both pairs. The choice of measured region matters as well as the order of the overlap.

## 6. Exact identification versus finite precision

Even the original family's one-statistic identification is not uniformly robust to absolute measurement error. Let `y=672m` and `z=672m+1`, with m>=1. The y configuration has empty J and the z configuration retains `{3/8}`.

Their moments not involving the variable runner agree. For every moment involving that runner,

`moment(z)=moment(y)*(1-1/z)`.

This follows from the periodic endpoint formula: residue 0 has zero correction, and residue 1 has correction equal to the negative leading term because a speed-1 runner never blocks on J. Consequently the largest difference across the entire 16-moment vector is exactly

`3/(128(672m+1))`,

which tends to zero. No fixed positive absolute error tolerance guarantees recovering the endpoint outcome throughout this unbounded family. Exact rational arithmetic still distinguishes it. This is a separate precision limitation from the second family's stronger **exact equality** of complete moment vectors across opposite outcomes.

## 7. What this changes in the distinction audit

The physical examples now separate three targets:

| Retained information | Demonstrated loss |
| --- | --- |
| Individual and pair durations | Positive lonely duration can change: 45/90 |
| Every joint duration moment | Component structure can change: earlier 2/25 versus 2/75 |
| Every joint duration moment, plus all nonzero pair gcds | Local nonemptiness can change: 1680/3360 with fixed 3/10/28 |

The decisive conflation here is **coverage almost everywhere versus coverage at every point**. Both new configurations have zero uncovered measure and the same complete occupancy distribution. Only one completely covers the chosen window.

There is also a useful counterweight: failure to assign mass to points does not automatically imply failure to infer point membership within every constrained physical family. The right-endpoint denominator criterion is an exact instance of indirect recovery. The relevant questions are which physical class is allowed, which statistic is retained exactly, which point is being tested, and which outcome actually depends on it.

A representation intended to settle the conjecture must preserve or separately certify equality contacts when its measure argument yields zero. Closed safe-lap cells already provide the exact benchmark. A candidate supplement is a small record of feasible contact times with all active constraints, rather than only pair crossing directions. The earlier third-controller counterexample remains a required stress test. Merely enumerating every threshold event would re-express the existing exact checker; a useful smaller selection rule remains open.

## 8. Reproduction and limits

```bash
python -B reviews/2026-09-27-lr2/check_contact_moments.py --check
python -B reviews/2026-09-27-lr2/crosscheck_contact_moments.py --check
```

The [standalone verifier](../reviews/2026-09-27-lr2/check_contact_moments.py) has no project imports. The [exact archive](../reviews/2026-09-27-lr2/contact_moments.json) pins its source hash and contains the 32-residue denominator certificate, the 672-row coefficient digest, all 34 original collision families, 11 original phase controls, exact closeness controls, all moments/states for h=1,2,3,4 in the constructive family, the fixed endpoint certificate, two closed safe cells, and the outside-J witnesses.

Periodic endpoint integration and independently structured phase-event partitions agree on all physical controls. The [separate comparison](../reviews/2026-09-27-lr2/crosscheck_contact_moments.py) uses the existing safe-interval intersection checker: all **15** complete local component lists agree, and every checked configuration also has solutions elsewhere in the full period. The [comparison archive](../reviews/2026-09-27-lr2/contact_checker_comparison.json) records dependencies by SHA-256. Large closeness parameters use the proven endpoint formula, not an attempted huge-speed event enumeration.

The first family is classified completely; the second is a constructive infinite equivalence class, not a complete collision classification or a minimal-speed search. Neither result selects a useful window for arbitrary inputs or settles all reference runners. Old scripts, outputs, and claims remain preserved. The draft research branch remains the review location; no outside publication, outreach, or novelty assertion is made.
