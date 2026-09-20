# Checking the Fibonacci suggestion

**Date:** September 20, 2026. **Prompt:** Vance noticed that the controlling pair `3+5=8` is a Fibonacci step and asked us to check whether this is more than a coincidence.

**Conclusion:** the general speed-sum condition does not require Fibonacci numbers. Deliberately choosing a whole Fibonacci speed family does produce exact additive constraints and a striking finite pattern of maxima and peak times. Neither establishes a Fibonacci explanation of the general conjecture or of all tight cases.

Reproduce with `python -m scripts.check_fibonacci_patterns`. [Script](../scripts/check_fibonacci_patterns.py) · [Exact data](../experiments/fibonacci_patterns.json).

## Inputs and scope

The selected runner is stationary in its own reference frame. Give the other runners the first `k` distinct positive Fibonacci speeds:

`1,2,3,5,8,13,21,34,55,89,144,233,377`.

We omit the repeated initial 1 to keep all original speeds distinct. Total runners are `n=k+1`, and the target is `1/n`, not the reciprocal of the largest speed. Adding the same positive constant to all speeds makes everyone move without changing any distances.

The prescribed calculations are:

- Twelve prefixes, `n=3,...,14`. All references were checked for `n<=10`; only the selected stationary reference for `n=11,...,14`.
- Four nearby eight-runner controls, each with all eight references checked: replace 21 by 20 or 22, or replace 13 by 12 or 14, in the seven-speed prefix through 21.
- Seven consecutive-Fibonacci pair comparisons with the reference stationary, hence three total runners in each comparison.

The reproducible script makes 95 reference evaluations, including the repeated selected reference of `(0,1,2)` in the prefix and pair comparisons. Every maximum is found by the exact piecewise-linear method and crosschecked with the separately implemented closed-interval method. These are specified examples, not an exhaustive search. The extension from ten to fourteen total runners was a targeted check of the emerging plateau pattern, not a general fourteen-runner verification.

## The additive recurrence has a direct effect

Suppose two positive relative speeds `a,b` have phases `delta` and `1-delta` at the same time, with `0<delta<=1/2`. Their distances from the selected runner agree, on opposite sides of the track. Then

$$at=p+\delta,\qquad bt=q+1-\delta,$$

so

$$ (a+b)t=p+q+1\in\mathbb Z.$$

If a runner at relative speed `a+b` is present, it coincides with the selected runner at that time. Consequently, a pair whose sum is present cannot control a positive lonely peak through opposite phases. This elementary observation applies to any additive triple, not just Fibonacci numbers.

In particular, at the old eight-runner touch time `t=3/8`:

| Relative speed | Phase around the track | Shorter-arc distance |
| --- | ---: | ---: |
| 3 | `1/8` | `1/8` |
| 5 | `7/8` | `1/8` |
| 8 | 0 | 0 |

The original consecutive eight-runner relative speeds are `1,...,7`, so speed 8 is absent there. Including the Fibonacci triple `{3,5,8}` blocks that candidate moment. This does not say adding a runner preserves the original runner-count threshold; the collision blocks every positive target.

Every consecutive Fibonacci triple repeats the additive relation. At a positive lonely peak of a Fibonacci prefix, consecutive Fibonacci speeds whose successor is also present therefore cannot supply this opposite-phase controlling pair. In the eight-runner Fibonacci prefix the actual controllers at `3/11` are speeds 8 and 3, summing to 11, which is absent.

The script verifies all equal-distance opposite-phase candidates `t=j/(a+b)` for every consecutive triple through 377 and for the non-Fibonacci control `{4,7,11}`. The general statement follows from the algebra above; these finite checks are examples, not the proof of its unbounded scope.

## Exact prefix results

Here “best gap” means the selected stationary runner's maximum nearest-neighbor separation over a complete cycle.

| Total runners | Largest Fibonacci speed included | Best gap | All maximizing times in one cycle |
| --- | --- | --- | --- |
| 3 | 2 | `1/3` | `1/3, 2/3` |
| 4 | 3 | `1/4` | `1/4, 3/4` |
| 5 | 5 | `1/4` | `1/4, 3/4` |
| 6–9 | 8, 13, 21, 34 | `2/11` | `3/11, 8/11` |
| 10–13 | 55, 89, 144, 233 | `5/29` | `8/29, 21/29` |
| 14 only | 377 | `13/76` | `21/76, 55/76` |

The first two prefixes coincide with ordinary consecutive-speed cases and are tight. Every selected-reference maximum from `n=5` through `n=14` exceeds `1/n`. Among the fully checked prefixes `n=5,...,10`, no reference runner is tight; the stationary reference has the smallest best gap. No all-reference conclusion is asserted for `n=11,...,14`.

For eight runners, the selected best gap is `2/11`, about 0.1818 lap, compared with the target `1/8=0.125` lap. Thus the full Fibonacci configuration does not reproduce the tight eight-runner behavior that originally prompted the question.

## The pattern worth preserving: Fibonacci numerators, Lucas denominators

Define Fibonacci numbers by `F_0=0,F_1=1` and Lucas numbers by `L_0=2,L_1=1`, both with the rule that each term is the sum of the previous two. The relevant terms are

- Fibonacci: `2,5,13` for the gap numerators, and `3,8,21,55` for the time numerators.
- Lucas: `11,29,76` for the denominators.

The three observed stages match

$$\text{gap}=\frac{F_{2m-1}}{L_{2m+1}},\qquad
  \text{first peak time}=\frac{F_{2m}}{L_{2m+1}},\quad m=2,3,4.$$

The second time is the reflected time `1-t`. Within each of these two-step subsequences, successive terms obey `x_next=3*x_current-x_previous`: `13=3*5-2`, `21=3*8-3`, `76=3*29-11`.

**Evidence limit:** we verified two full four-configuration plateaus and the first case of a third. We have not proved that this formula continues, that each later plateau has length four, or what the infinite-prefix limit is. The eight-runner example alone would not establish any of this structure. No novelty claim is made; the literature check below was not exhaustive.

## Why a plateau ends, and nearby counterchecks

The first plateau cannot survive adding speed 55 at its old maxima:

$$55\cdot\frac{3}{11}=15,\qquad 55\cdot\frac{8}{11}=40.$$

Both old maximizing times become collisions. The earlier full maximum was attained only at those two times, so adding 55 must strictly lower that maximum; the checker finds `5/29`. Likewise, adding 377 destroys the next plateau's old maximizing times, since `377=13*29`, giving a collision at both `8/29` and `21/29`. The new maximum is `13/76`.

However, the first plateau is not exclusive to Fibonacci inputs:

| Change to eight-runner relative speeds `{1,2,3,5,8,13,21}` | Selected best gap | Peak times |
| --- | --- | --- |
| None | `2/11` | `3/11, 8/11` |
| `21 -> 20` | `2/11` | `3/11, 8/11` |
| `21 -> 22` | `1/6` | `1/6, 5/6` |
| `13 -> 12` | `2/11` | `3/11, 8/11` |
| `13 -> 14` | `2/11` | `3/11, 8/11` |

At `t=3/11`, speed 20 is `5/11` away, speed 21 is `3/11` away, and speed 22 is at distance zero. The subset `{1,2,3,5,8}` already supplies the upper bound `2/11`. A replacement that stays at least that far away at an old peak preserves the bound by a witness, even if it is not Fibonacci. Thus this local stability has a simple modular explanation.

## Pair-only comparison

With just the selected stationary runner and two consecutive Fibonacci speeds, the target is always `1/3`:

| Two moving speeds | Selected best gap |
| --- | ---: |
| `1,2` | `1/3` |
| `2,3` | `2/5` |
| `3,5` | `1/2` |
| `5,8` | `6/13` |
| `8,13` | `10/21` |
| `13,21` | `1/2` |
| `21,34` | `27/55` |

So the pair `3,5` does not force an eighth-lap bound by itself; it can be half a lap from the stationary runner. Both speeds are odd, making `t=1/2` a witness. The other five runners of the earlier eight-runner example mattered.

## Literature check and interpretation

Targeted web searches for Fibonacci and Lonely Runner connections did not locate a primary source establishing the specific prefix formula above. Several searches returned largely irrelevant results, so this is weak negative evidence and no basis for an originality claim.

We re-opened the [Perarnau–Serra survey, v3, Section 7.3](https://arxiv.org/html/2409.20160v3#S7.SS3), which studies speed sequences whose successive ratios stay above `1+epsilon` (lacunary sequences). Our distinct positive Fibonacci speeds have successive ratios at least `3/2`, so they lie in that broad class. The displayed theorem requiring every successive ratio to be at least 2 does not directly apply to the full Fibonacci sequence. The survey search found no occurrence of “Fibonacci”; this does not establish absence from the wider literature. No Fibonacci-specific published theorem is adopted here.

Our refined answer is: the original `3+5=8` equality does not identify a universal Fibonacci mechanism, but testing a whole Fibonacci family exposed actual recurrence-dependent constraints and a reproducible pattern worth investigating. The next mathematical question would be to explain or disprove the observed Fibonacci/Lucas plateau formula using interval upper bounds and exact modular witnesses, before widening any computation.
