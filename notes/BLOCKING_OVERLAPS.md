# When blocking windows overlap, touch, or leave a gap

**Date:** September 20, 2026. **Evidence:** elementary derivations and exact calculations on seven existing eight-runner configurations. No new speed-set search, novelty claim, or general proof of the conjecture.

This continues the [equal individual blocking fractions](TIGHT_CASES_4_8_12.md#further-patterns-equal-blocking-time-equivalent-references-and-peak-width). At the eight-runner threshold, each other runner is too close for exactly one quarter of a common integer-speed cycle. We now examine the placement of those periods.

Reproduce with `python -m scripts.analyze_blocking_overlaps`. The [script](../scripts/analyze_blocking_overlaps.py) writes [exact evidence](../experiments/blocking_overlaps.json). The seven configurations and their previously checked all-reference profiles remain in [cooperative_blocking.json](../experiments/cooperative_blocking.json).

## A rule written entirely in fractions and integers

Use positive integer absolute relative speeds, original total runner count `n`, and target `delta=1/n`. Speed `a` meets the selected runner at times `p/a`, for integer `p`. Around that meeting it is strictly too close during the open interval

$$B_{a,p}=\left(\frac{p-1/n}{a},\frac{p+1/n}{a}\right).$$

The meeting time is the center, and the half-width is `1/(na)`. Endpoints are permitted: equality counts.

Consider two meetings in order, `p/a < q/b`, and put

$$D=aq-bp>0.$$

Their centers are `D/(ab)` apart. The sum of their half-widths is `(a+b)/(nab)`. Thus the signed separation between the facing endpoints is

$$G=\frac{q-1/n}{b}-\frac{p+1/n}{a}
  =\frac{nD-(a+b)}{nab}.$$

| Integer comparison | Two blocking windows |
| --- | --- |
| `nD < a+b` | Overlap |
| `nD = a+b` | Just touch; their common endpoint belongs to neither open window |
| `nD > a+b` | Leave a positive gap of length `G` |

When one interval contains the other, `-G` is not their intersection length; the sign still correctly detects overlap. Our three examples below have no containment. This is a direct interval calculation, not a newly claimed theorem. It connects the scheduling question to the cross-products used when subtracting fractions.

## The same pair does all three

Keep the same tight eight-runner instance throughout: actual speeds `{1,2,5,6,7,8,12,14}`, selected speed 1, hence relative speeds `{1,4,5,6,7,11,13}`. Focus on relative speeds 11 and 13. Their sum is 24, so touching requires `D=3`.

| Meetings of 11 and 13 with the reference | `D = 11q-13p` | Result |
| --- | ---: | --- |
| `5/11`, `6/13` | 1 | Overlap by `2/143` cycle |
| `4/11`, `5/13` | 3 | Just touch at `3/8` cycle |
| `3/11`, `4/13` | 5 | Leave a gap of `2/143` cycle |

At the middle example, the two open windows are `(31/88,3/8)` and `(3/8,41/104)`. Every other runner is also at least `1/8` away at `3/8`, so that endpoint is a valid lonely time. Speed 5 also touches the threshold there, as recorded in the earlier three-way tie.

In the last example, the pair leaves the closed gap `[25/88,31/104]`. However, speed 7's blocking window `(15/56,17/56)`, centered at `2/7`, contains that entire gap, including its endpoints. A gap between this pair therefore supplies no lonely time. All of this occurs in a single fixed speed configuration.

The first example is the earlier cooperative overlap near `6/13`; the second and third comparisons now explain why this same pair behaves differently elsewhere. The differing integer cross-products, not a change of speed, determine the three outcomes.

## A stronger version of our speed-sum observation

Earlier we derived divisibility of a controlling speed sum by `n` under the extra assumption that the touch time is a reduced fraction `q/n`. That extra assumption is unnecessary.

For `n>=3`, suppose the selected runner's maximum is exactly `1/n`. At any maximizing time, at least one active distance curve must have positive slope and another negative slope. Indeed, the active curves are affine near that time because `0<1/n<1/2`. If all active slopes had the same sign, moving slightly in that direction would increase every active distance; the finitely many inactive distances have positive margins, so the minimum would also increase, contradicting maximality.

Call an increasing active speed `a` and a decreasing one `b`. The first is leaving its blocking interval and the second is entering its own. Their facing endpoints coincide. The integer comparison above then gives

$$a+b=n(aq-bp),\qquad\text{so } n\mid(a+b).$$

This applies to integer absolute relative speeds (and rational inputs after a common rescaling to integers), without assuming a particular denominator for the time. It does not assert `a+b=n`: the 11/13 handoff gives `24=3n`. For the consecutive middle peak, speeds 3 and 5 give `8=n`.

This is only a necessary condition for exact tightness. It neither proves the desired lower bound nor determines whether other times offer greater separation. Our non-tight controls retain threshold handoffs. The script verifies the integer identity for every opposite-boundary contact in all seven selected-reference schedules. This is a derivation and a bounded check, not an originality claim or an independently reviewed research result.

## A fixed overlap accounting identity

Let `M(t)` count other runners strictly closer than `1/n` at time `t`. Over a common cycle of integer speeds, individual blocking fractions give

$$\int_0^1 M(t)\,dt=\frac{2(n-1)}n.$$

Let `U` be the duration with `M=0`, and let `R` count blocking beyond the first blocker, integrated over time. If three runners block simultaneously, this latter count is two, not three pair overlaps. Pointwise,

$$M=\mathbf 1_{M>0}+(M-1)_+,$$

and therefore

$$R=\int_0^1(M-1)_+\,dt=\frac{n-2}{n}+U.$$

For eight runners, `R=3/4+U`. Every extra amount of completely clear time is accompanied by an equal increase in this measure of overlapping blocking elsewhere. The three tight schedules have `U=0` and `R=3/4`, despite different overlap arrangements.

This is an accounting identity, not a proof that a valid time exists. A duration of zero cannot distinguish isolated valid contacts from an empty feasible set. The exact closed feasible sets are retained separately throughout our calculations. For arbitrary real speeds there need not be a common cycle; no finite-cycle identity is asserted for them here.

## Countercheck: more total pair overlap does not order tightness

Sum, over all 21 pairs, the duration during which both members block. This counts three simultaneously blocking runners three times, unlike the `R` measure above.

| Relative-speed set, selected reference fixed | Summed pair overlap | Maximum separation | Completely clear duration |
| --- | ---: | ---: | ---: |
| `{1,4,5,6,7,11,13}` | `307691/240240` (about 1.281) | `1/8` | 0, with four isolated valid times |
| `{1,4,5,6,7,12,13}` | `2983/2184` (about 1.366) | `2/11` | `115/2184` (about 5.27%) |
| `{1,2,3,4,5,6,7}` | `157/105` (about 1.495) | `1/8` | 0, with four isolated valid times |

The non-tight example lies between two tight examples in this statistic. A single total of pair overlaps does not monotonically track the selected runner's best separation. This does not rule out methods retaining the full pair data or additional structure.

## What was checked, and what remains

The script partitions each cycle at every exact blocking-status boundary. A rational midpoint determines the status on each resulting open cell because no blocking predicate changes inside it. This is a complete finite partition, not sampled-time simulation. It records the histogram of the number of blockers, the full cell schedule, and opposite-boundary contacts.

All 147 pair-overlap durations are separately checked by direct intersection of individual intervals. Completely clear durations and full closed allowed sets agree with the existing interval checker and the earlier data, whose maxima and all-reference profiles were independently crosschecked. The three local interval examples are checked by exact rational endpoint calculations. No new configurations or all-reference claims were added.

The next useful question is narrower: can we trace a small set of blocking intervals that certifies coverage between successive valid touch times, while preserving the exceptional endpoints? Such a certificate may explain why a particular speed is necessary even when it never controls a peak. It would explain fixed configurations; turning it into a uniform argument for arbitrary speeds remains unresolved.

**September 23 continuation:** [Blocking chains beyond Fibonacci](BLOCKING_CHAINS.md) constructs minimum chains and independently crosschecks 46 graph components across eight specified inputs. It identifies a modular shortcut shared by the old examples, then tests a 13-to-8 replacement that destroys every old lonely time while creating other valid intervals. The general noncoverage question remains open.
