# Threshold-touching cases: 4, 8, and 12 runners

**Date:** September 19, 2026. **Question from Vance:** record cases that only touch the threshold, double and triple the runner count, and compare what the tight cases share.

## Result and meaning of "touch"

We extended the four-runner example to eight and twelve runners. We found four tight cases in this specified comparison: the three consecutive-speed examples and one known nonconsecutive eight-runner example. Their selected runner's **global maximum** distance from its nearest neighbor is exactly `1/n`. Merely crossing or touching the threshold at some time would not establish tightness.

Every runner starts at the same point. Speeds below are laps per time unit; the selected runner has speed **1**. Calculations cover the complete relative-motion period `[0,1]`, not a sampled time window. Other reference runners are a separate question.

| Total runners | Actual speeds | Exact maximum for speed-1 runner | All attaining times in one period |
| --- | --- | --- | --- |
| 4 | 1,2,3,4 | 1/4 | 1/4, 3/4 |
| 8 | 1,2,3,4,5,6,7,8 | 1/8 | 1/8, 3/8, 5/8, 7/8 |
| 12 | 1,2,3,4,5,6,7,8,9,10,11,12 | 1/12 | 1/12, 5/12, 7/12, 11/12 |
| 8, uneven speeds | 1,2,3,4,5,6,8,13 | 1/8 | 1/8, 3/8, 5/8, 7/8 |

Subtracting the reference speed gives relative speeds `1,...,n-1` in the first three rows. The last row has relative speeds `{1,2,3,4,5,7,12}`. That is a previously known tight example, reproduced here, not a new discovery [S1, Section 4](SOURCES.md).

## What they share, and what they do not

1. **Only isolated successful moments.** All four selected runners reach their threshold at finitely many points per cycle; there is no positive-width interval at or above it. Equality counts.
2. **Opposing distance slopes at each peak.** Exactly two runners determine each listed peak: one distance is increasing, the other decreasing. Their curves meet at the threshold. The closer runner changes identity there, capping the minimum distance. This is a local explanation; the complete-period computation supplies the global maximum. Such handoffs also occur at non-tight peaks, so a handoff alone does not characterize tightness.
3. **Matching arithmetic in these examples.** Each peak time is `q/n` with `gcd(q,n)=1`. The two limiting positive relative speeds sum to `n`. At the first peak they are `1` and `n-1`. At the additional peaks for eight runners they are `3,5`; for twelve they are `5,7`. The uneven eight-runner case has the same peak times and limiting pairs as the consecutive one. These observations are not asserted for every tight configuration.
4. **Even speed spacing is not necessary.** The uneven example has the same threshold, peak times, and limiting pairs despite different speeds. At time `1/8`, its relative positions are `0,1/8,1/4,3/8,1/2,5/8,7/8,1/2`: two other runners coincide halfway around the track. Even position spacing of everyone is not necessary either.

We also checked all reference runners in these four configurations. In each consecutive case, only the slowest and fastest are tight; the interior runners attain more than `1/n`. In the uneven eight-runner case, only the speed-1 runner is tight. This study does not require every runner to be lonely simultaneously.

## Why the consecutive family works for every runner count

This is a standard known family [S1, Section 4](SOURCES.md), not an extrapolation from three computations.

For relative speeds `1,...,n-1`, time `1/n` places the selected runner and the others at equally spaced points, so the nearest distance is `1/n`.

For any time `t`, put the `n` points `0,t,2t,...,(n-1)t` on the circle. Some consecutive circular gap is at most `1/n`. The difference between the indices of its endpoints has magnitude between 1 and `n-1`, so one of the available relative speeds gives distance at most `1/n` from the origin. Thus the selected runner can never exceed `1/n`.

Moreover, if its minimum reaches `1/n`, all pairwise distances among these points are at least `1/n`, because every index difference is an available relative speed. The points must be equally spaced. Hence all successful times in `[0,1]` are exactly `q/n` with `gcd(q,n)=1`. This explains why twelve runners have four such times, not six or twelve.

The general conjecture still asks for arbitrary distinct speeds. Proving this particular family for all `n` does not prove that broader statement.

## Bounded comparison with nearby speed choices

For each `n=4,8,12`, start with relative speeds `1,...,n-1`. Replace exactly one speed `r` by an integer `b`, with `1<=r<=n-1` and `n<=b<=2(n-1)`. This is a deliberately specified perturbation family, not all speed sets below a bound.

| Total runners | Single-speed replacements checked | Still tight | Above threshold | Below threshold |
| --- | ---: | ---: | ---: | ---: |
| 4 | 9 | 0 | 9 | 0 |
| 8 | 49 | 1 | 48 | 0 |
| 12 | 121 | 0 | 121 | 0 |

Across 179 replacements, the sole tight one replaces relative speed `6` by `12` at `n=8`; in actual speeds, `7` becomes `13`. There are 182 selected-reference inputs including the three original consecutive cases. Absence of further tight examples in this domain is not evidence that no others exist outside it.

As explicit controls, increase only the fastest actual speed from `n` to `n+1`. The exact maximum becomes `1/3`, `1/7`, and `1/11` at `n=4,8,12`, respectively. These exceed the corresponding targets `1/4`, `1/8`, and `1/12`.

## Reproduction and evidence

```bash
python -m scripts.compare_tight_cases
```

- [Script](../scripts/compare_tight_cases.py) and [complete rational results](../experiments/tight_cases_4_8_12.json).
- Checker baseline: commit `2d97b34828c8ceadc81fe5c6ceb60439e554b4c1`; the output records the checker's SHA-256 hash.
- Method A intersects exact closed allowed-time intervals at `1/n` for all 182 selected-reference inputs. Only singleton intersections certify tightness. A positive-width intersection implies strictly greater separation somewhere: the finite lower envelope has nonzero slopes on its linear pieces and cannot remain constant on an interval.
- Method B independently enumerates all corners and affine crossings for each tight case and each explicit control. It agrees with Method A at the exact global maximum. All 32 reference runners across the four tight configurations were also checked using both methods.
- Peak identities, directions of distance change, positions, and exact polygon vertices are saved. The polygon uses the same piecewise-linear construction as Method B; it is display data, not a third independent proof method. Browser coordinates round these exact fractions for drawing only.
- `python -m unittest discover -s tests -q`: all 25 existing checker tests passed after this addition. These remain separate regression coverage. No paid compute, random sampling, large search, or external proof audit was used.

## Follow-up question selected

Why does accelerating relative speed `6` to `12` preserve every bottleneck in the eight-runner case, when the other 178 tested changes create room above the threshold? Compare its allowed-time intervals directly with the original speed-6 intervals, then relate that difference to the known acceleration criterion of Goddyn and Wong cited in S1. Do not infer that matching a few peak times is by itself sufficient to preserve the global maximum.

## Continuation: the two openings and the replacement that covers them

Vance asked to preserve the work, investigate that question, and watch for anomalies and patterns throughout the process. The following is an exact elementary explanation for this fixed case, consistent with known work. It is not a new general theorem or a proof of the full conjecture.

All speeds in this section are **relative to the chosen runner**. The actual chosen speed remains 1, so relative 6, 12, and 18 correspond to actual 7, 13, and 19. Temporarily omit the speed-6 constraint, leaving `C={1,2,3,4,5,7}`, but retain the original eight-runner threshold `1/8`.

The complete set of times when every constraint in C is at least `1/8` consists of the four isolated points `1/8,3/8,5/8,7/8`, plus two closed intervals:

```
J1 = [9/56, 7/40]
J2 = [33/40, 47/56] = 1 - J1.
```

The interior of each interval is strictly above the threshold. Thus these are the only places where the omitted runner needs to prevent an improvement. J1 contains `1/6`; J2 contains `5/6`. These are not intervals around `1/3`: the still-present speed 3 prevents separation there.

At `1/6`, all six remaining distances are at least `1/6`. Relative speeds 6 and 12 both meet the chosen runner at that instant. More importantly, they remain within `1/8` throughout the **entire** opening. On J1, speed 6 never exceeds distance `1/20`, and speed 12 never exceeds `1/10`; both are strictly less than `1/8`. The reflected statement holds on J2. Meanwhile, speed 12 is half a lap away at each of the four original touch times, so those times survive unchanged.

This accounts for all times in the cycle: outside the two openings the common constraints already cap separation at `1/8`; inside them the replacement supplies the cap; at the four surviving points equality is attained.

### Why 12 is the only faster integer replacement for this deleted speed

This improves the earlier bounded observation for **the fixed eight-runner deletion of relative speed 6**. Let the inserted relative speed be an integer `w>7`.

1. At `t=1/6`, tightness requires `||w/6||<=1/8`. This distance is a multiple of `1/6`, so it must be zero: **6 divides w**.
2. A continuous interval on which this replacement stays within `1/8` of the origin must lie within a single neighborhood of one meeting time. Around `1/6`, that neighborhood has half-width `1/(8w)`.
3. The right side of J1 extends `7/40 - 1/6 = 1/120` past the meeting. Covering the entire opening therefore requires `1/(8w)>=1/120`, or **w<=15**.
4. The only multiple of 6 with `7<w<=15` is **12**, and the direct calculation above verifies that it works.

This is an argument over every eligible integer w, not an extrapolation from a finite list. It does not classify replacements of other deleted speeds, multiple simultaneous replacements, irrational inputs, or arbitrary tight configurations. Independent external review has not been performed; no originality claim is made.

### Controls that distinguish timing from coverage

| Inserted relative speed | Exact full-cycle maximum | Global peak times | Explanation |
| --- | --- | --- | --- |
| 6 (original) | 1/8 | 1/8,3/8,5/8,7/8 | Covers both openings |
| 11 | 1/6 | 1/6,5/6 | Misses the critical meetings |
| 12 | 1/8 | 1/8,3/8,5/8,7/8 | Same critical meetings; coverage still wide enough |
| 13 | 1/6 | 1/6,5/6 | Misses the critical meetings |
| 18 | 3/23 | 4/23,19/23 | Meets at the right instants, but passes too quickly to cover the whole opening |

All five cases still have distance exactly `1/8` at the four original touch times. In the non-tight cases, new, higher peaks appear elsewhere. Consequently, **preserving the visible touch schedule is insufficient to preserve tightness**. Even being a multiple of the removed speed is insufficient: 18 meets the chosen runner at `1/6` but its blocking neighborhood ends at `25/144`, before J1 ends at `7/40`.

## The spacing pattern Vance noticed

For the consecutive relative-speed family, the exact times are `q/n` with `1<=q<n` and `gcd(q,n)=1`, as derived above. That arithmetic restriction produces regular structure, but does not always produce equal gaps.

| Total runners | Cyclic gaps between successive global touch times, including the next cycle |
| --- | --- |
| 4 | 1/2, 1/2 |
| 8 | 1/4, 1/4, 1/4, 1/4 |
| 12 | 1/3, 1/6, 1/3, 1/6 |
| 16 (additional check) | Eight gaps, each 1/8 |

For powers of two, the allowable numerators are exactly the odd integers, so the gap is uniformly `2/n`. For twelve, numerators divisible by 2 or 3 are excluded, leaving `1,5,7,11`; the gaps therefore alternate. In this consecutive family, a candidate `q/n` excluded by a common divisor produces a collision with the reference: relative speed `n/gcd(q,n)` is present and has completed an integer number of laps.

There is also a broader reflection symmetry: for any integer relative speeds, `f(1-t)=f(t)`. It explains mirrored times, including J1/J2 and the non-tight peaks `4/23,19/23`. It is not special evidence of tightness. Nor should a repeating pattern among peak times be confused with a smaller period of the full distance curve.

## Pattern and exception record

| Observation or proposed explanation | Evidence and limit |
| --- | --- |
| All touch times are equally spaced | False in the twelve-runner example; arithmetic regularity survives |
| Consecutive tight times use coprime numerators | Derived for that entire family; do not silently generalize to every tight set |
| Reflection about half a cycle | Exact for integer speeds, tight or not |
| Preserving the old touch times preserves tightness | False for replacements 11, 13, and 18 |
| Matching meeting times is sufficient | False for 18; coverage width also matters |
| The successful doubling is tied to runner count | Known acceleration criterion gives `n=8,14,20,...` for this particular family; checked 4,8,12,14 below |

For the family replacing relative speed `n-2` by `2(n-2)`, the known Goddyn–Wong criterion, restated in [S8](SOURCES.md), requires that `n-2` share a factor with both 2 and 3. Thus, for `n>=4`, this family is tight exactly when `n` is 2 modulo 6. Our exact checks reproduce success at 8 and 14, and failure at 4 and 12, whose maxima are `2/7` and `2/23`, respectively. The family rule comes from the cited result; four checks alone would not prove it.

## Continuation evidence and next step

```bash
python -m scripts.analyze_eight_runner_replacement
```

[Script](../scripts/analyze_eight_runner_replacement.py) · [rational evidence](../experiments/eight_runner_replacement.json). The output records the source revision and checker hash, complete core intervals, strict-opening checks, blocking neighborhoods, five replacement cases, four spacing checks, four acceleration-family checks, and exact vertices for a zoomed plot. All 13 full-case checks use the independent maximum and interval methods. Plotting uses rounded display coordinates only. The earlier experiment and its 179 replacement results remain preserved unchanged.

A targeted literature check also found an August 2026 preprint devoted to single-speed modifications, including an uncovered-interval method [S8](SOURCES.md). Its broader claims and computational census have not been independently audited; our fixed-case explanation does not depend on those claims.

**Next useful question:** does the same interval-coverage explanation clarify the known two-speed eight-runner case `{1,4,5,6,7,11,13}`? It replaces relative speeds 2 and 3 by 11 and 13 together. Track whether two replacements close openings cooperatively even when a single change does not, and check whether the touch-time pattern survives. This is a proposed bounded next step, not a classification claim.

## Follow-up: must the special runner be the slowest?

Vance asked whether only the slowest runner is exactly tight in other examples, then suggested the particular runner might differ from the slowest and could be part of the puzzle. Exact all-reference checks support that distinction. The speed rank is not intrinsic to tightness.

The new [script](../scripts/compare_reference_runners.py) and [results](../experiments/reference_runner_roles.json) check all 96 reference runners in 13 explicit configurations. Each maximum is crosschecked with the interval method. This is a selected comparison, not a census or an estimate of prevalence.

| Actual speeds (all start together) | Exactly tight runners |
| --- | --- |
| 1,2,3,4,5,6,7,8 | Speeds 1 and 8; both have maximum 1/8 |
| 1,2,3,4,5,6,8,13 (original uneven case) | Only speed 1; maximum 1/8 |
| 1,2,3,4,8,9,11,16 | Only speed 4, fourth in speed order; maximum 1/8 |
| 1,6,8,9,10,11,12,13 | Only speed 13, the fastest; maximum 1/8 |
| 1,2,4,8,16,32,64,128 | None; even the smallest best gap is 32/127, greater than 1/8 |

Additional comparisons: actual speeds `{1,2,4,5,8}` have two tight runners, speeds 1 and 4, each at 1/5. The nonconsecutive six-runner, second eight-runner, and fourteen-runner examples in the data each have only their slowest runner tight. These examples show that neither uniqueness nor the slowest-speed position should be assumed.

### Why the identity can move

**Reverse the entire speed order.** Replace every actual speed v in the original eight-runner case by `14-v` and sort. Every pairwise relative speed changes sign, so every corresponding circular distance is unchanged at every time. The former slowest runner becomes the fastest while retaining exactly the same distance history. The checker verifies the corresponding maxima and times for all eight runners.

**Move the selected runner into the middle.** In the original example its positive relative speeds are `{1,2,3,4,5,7,12}`. Change the first three to `-1,-2,-3` and choose actual reference speed 4. This gives actual speeds `{1,2,3,4,8,9,11,16}`. Since `||-ut||=||ut||`, the speed-4 runner has the same seven distance curves as the old speed-1 runner. Its tight times remain `1/8,3/8,5/8,7/8`. Other runners' pairwise distances can change under independent sign changes, so their maxima were recomputed; all seven exceed 1/8.

More generally, independent relative sign choices can put a selected runner at any speed rank while preserving that runner's entire distance function. Add a sufficiently large common speed to keep every actual velocity positive. This observation does not by itself preserve the other runners' results or prove uniqueness; those require separate checks.

### A useful precise version of the proposed role

For our integer-speed experiments, first let every runner choose its own best moment:

```
L_i = max over t in [0,1] of min over j != i of ||(v_j-v_i)t||.
G(V) = min over runners i of L_i.
```

The runners attaining G have the smallest best achievable gap: they are the most constrained in this sense. At least one exists, and ties are possible. The conjecture in this setting asks for `G(V)>=1/n`. The order of operations matters: these best moments need not be simultaneous.

An **exactly tight** runner has `L_i=1/n`. A **most constrained** runner minimizes L_i, whether or not that minimum equals the threshold. For the powers-of-two eight-runner control, the speed-2 runner is the unique most constrained one, with `L_i=32/127`; all runners have extra room. No runner is exactly tight. Thus “every configuration has a most constrained runner” is automatic from a finite minimum; “every configuration has an exactly tight runner” is false.

For fixed velocities, this comparison is over complete cycles; it assigns a fixed set of minimizing runners. The identity of a nearest neighbor at a particular instant can still change repeatedly. These are separate roles.

The next interval-coverage comparison should retain the full per-runner profile rather than assuming that the initially selected slowest runner represents every runner. No novelty claim is made for these standard symmetries or the minimum-of-maxima formulation.

Reproduce this follow-up with `python -m scripts.compare_reference_runners`. The JSON records the checker hash, all maxima and attaining times, speed ranks, tight flags, most-constrained identities, and the symmetry checks. The previously saved experiments are unchanged.

## September 20: cooperative blocking and a changing tight runner

The next comparison is complete. [Script](../scripts/analyze_cooperative_blocking.py) and [exact data](../experiments/cooperative_blocking.json) examine seven specified eight-runner configurations, all 56 reference runners, and three constraint deletions at the fixed original target `1/8`. Each maximum is crosschecked by the interval method. This is a bounded comparison of known examples and controls, not a new classification.

### Six openings, with two runners sharing the coverage

Start with relative speeds `{1,2,3,4,5,6,7}`. Temporarily omit 2 and 3, retaining the original eight-runner target. The remaining constraints are `C={1,4,5,6,7}`. They permit strict extra room in six open intervals: the three below and their reflections under `t -> 1-t`. They also permit two isolated threshold times, `1/8` and `7/8`.

| First-half opening, with endpoints excluded | What inserted relative speeds 11 and 13 do |
| --- | --- |
| `(17/56,5/16)` | 13 blocks the whole opening |
| `(17/48,3/8)` | 11 blocks the whole opening |
| `(25/56,15/32)` | 11 blocks the earlier part; 13 blocks the later part; their coverage overlaps |

“Blocks” means the inserted runner is strictly closer than `1/8` to the reference. For the third opening, the relevant open blocking intervals are

```
11: (39/88,41/88), centered at 5/11
13: (47/104,49/104), centered at 6/13.
```

Their overlap has length `2/143`. Together they cover the entire third opening; neither does so alone. The script partitions all six openings at every blocking threshold endpoint and checks each resulting subinterval with constant blocking status and every internal boundary with exact fractions. Thus this conclusion covers the whole intervals, not a sampled set of times.

Three convenient witnesses inside the third opening make the cooperation visible:

| Time | Smallest gap from the five retained constraints | Distance of 11 | Distance of 13 |
| --- | --- | --- | --- |
| `9/20` | `3/20` | `1/20`: blocks | `3/20`: permits |
| `6/13` | `2/13` | `1/13`: blocks | `0`: blocks |
| `7/15` | `2/15` | `2/15`: permits | `1/15`: blocks |

The complete set `{1,4,5,6,7,11,13}` leaves exactly `1/8,3/8,5/8,7/8` as acceptable times. Some endpoints of the core openings are removed by the inserted constraints; all endpoints are included in the full closed-interval check. This explains the known double-replacement example through cooperation in coverage.

### An exception to the earlier limiting-pair pattern

At `t=3/8`, relative speeds 5, 11, and 13 all have distance `1/8`. Their local distance slopes are respectively `-5,+11,-13`. Just before the peak, 11 gives the smallest distance; just after it, 13 does. Speed 5 touches the threshold but does not control the nearest-distance envelope on either adjacent side.

For `|h|<=1/10000`, the exact local formula is

```
f(3/8+h) = 1/8 + 11h  for h <= 0,
f(3/8+h) = 1/8 - 13h  for h >= 0.
```

The script checks that each distance curve is affine throughout these neighborhoods, bounds it against the proposed envelope at the endpoints, and identifies an attaining curve. Thus the handoff assertion is more than a close-time sample.

The controlling relative speeds sum to `24=3*8`, **not 8**. The earlier sum-equals-runner-count observation does not generalize. A weaker conditional arithmetic statement follows: if a threshold contact occurs at `q/n` with `gcd(q,n)=1`, and active relative speeds `a,b` have phases `1/n` and `1-1/n`, then `a q=1 mod n` and `b q=-1 mod n`, hence `n` divides `a+b`. This condition concerns that specified contact time; it does not establish all peak times or global tightness.

Deleting speed 5 nevertheless raises the best gap to `1/5` at the original fixed target comparison. So a constraint can be non-controlling near one peak and still essential elsewhere. Deleting 11 or 13 raises the best gap to `2/11` or `2/13` respectively. Earlier speed 12 illustrated the other direction: a runner can be essential while never touching the final threshold at a peak.

### Identical touch snapshots can conceal extra room

Keep the five core relative speeds fixed, and vary the two other ones:

| Added relative speeds | Selected reference's maximum | Global peak times |
| --- | --- | --- |
| `11,13` | `1/8` | `1/8,3/8,5/8,7/8` |
| `19,13` | `4/25` | `9/25,16/25` |
| `11,21` | `2/13` | `4/13,9/13` |

Changing one speed by 8 preserves its phase at every `q/8`. Consequently these three configurations have **identical labeled phase vectors** at all four original touch times, not merely the same minimum distance. The latter two have larger gaps between those snapshots. Their all-reference checks show no exactly tight runner anywhere. Congruences at the contact times capture some structure; the intervening trajectory and coverage remain necessary.

### The tight role moves under a one-speed change

This is a separate control. Express all runners in actual, positive speeds:

| Actual speeds | Unique tight runner | Speed-1 runner's best gap | Speed-8 runner's best gap |
| --- | --- | --- | --- |
| `{1,2,5,6,7,8,12,14}` | Speed 1 | `1/8` | `1/5` |
| `{1,2,5,6,7,8,12,13}` | Speed 8 | `2/13` | `1/8` |

Slowing the fastest runner from 14 to 13 transfers the unique tight role to a runner whose own speed is unchanged. Relative to actual speed 8, the new signed differences are `{-7,-6,-3,-2,-1,4,5}`. Their magnitudes are exactly `{1,2,3,4,5,6,7}`. The selected distance function is therefore identical to the ordinary consecutive tight example, by sign symmetry. This gives an exact explanation of the role change; the other seven references were separately checked.

Accordingly, the relative set `{1,4,5,6,7,11,12}` is **non-tight for the initially selected reference**, while the full eight-runner configuration still has a tight runner. Do not label the whole configuration non-tight from one reference's result.

### Simple relationship counts also fail as an explanation

Count relations `a+b=c` with `a<=b`, allowing `a=b`, among positive relative speeds. The consecutive, single-replacement, and double-replacement tight cases have respectively 12, 9, and 6 such relations. Controls `{1,4,5,6,7,11,12}` and `{1,4,5,6,7,12,13}` have 8 and 7, yet their selected-reference maxima exceed `1/8`. Thus more of these short relations does not monotonically mean tighter separation. Every set also contains a shortest nonzero integer relation of coefficient absolute-sum 3; that minimum alone cannot distinguish them. This tests one simple statistic, not all ways to characterize the relation lattice.

**Pattern record:** same touch times is insufficient; even identical touch configurations are insufficient; a threshold tie is not always a controlling constraint; more short additive relations is not a tightness criterion; and a one-speed change can move the unique tight role to another runner. Each statement above has an explicit exact control.

**Next useful question:** group tight reference runners by their normalized absolute relative speeds before comparing configurations. Then ask whether any remaining differences in their full-cycle coverage require a new explanation, rather than counting disguised copies of an already-understood case as new patterns.
