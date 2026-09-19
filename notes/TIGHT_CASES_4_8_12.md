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

## Next useful question

Why does accelerating relative speed `6` to `12` preserve every bottleneck in the eight-runner case, when the other 178 tested changes create room above the threshold? Compare its allowed-time intervals directly with the original speed-6 intervals, then relate that difference to the known acceleration criterion of Goddyn and Wong cited in S1. Do not infer that matching a few peak times is by itself sufficient to preserve the global maximum.
