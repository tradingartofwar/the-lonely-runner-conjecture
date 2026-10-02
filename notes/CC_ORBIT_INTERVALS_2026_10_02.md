# CC orbit intervals — continuous choices and isolated points

October 2, 2026 UTC. **OBSERVED** finite results; **HYPOTHESIS / proof candidate** for the parameterized arguments. AI-assisted work; independent proof review and novelty remain **OPEN**.

The new construction retains the entire safe core for the first eight moving speeds as labelled closed intervals and isolated points, then intersects each lifted component with the added runner's bands. This repairs the information lost by the old supplied sheets. The complete construction passed all 1,197 fresh cases; keeping only the widest component passed 981, while dropping isolated points passed 1,196. All three deterministic outputs reproduced exactly.

## A concrete infinite-family candidate

For stationary-reference speeds (0,1,2,3,4,5,7,10,19,r), one fixed interval [25/152,7/40] and the isolated time 1/8 give a candidate construction for every positive integer r distinct from the other speeds. The interval has width 1/95, so it necessarily meets an added-runner safe band for r>=24. Exact checks of all fifteen admissible smaller r leave only 6 and 12, both handled by 1/8. The [derivation](../reviews/2026-10-02-cc-orbit-intervals/DERIVATION.md) gives the explicit rounding formula and scaling rule.

This covers the entire fixed-pair r family, including the prior obstruction r=40k. It is a narrow constructive proof candidate for one selected reference and target 1/8. It is not an arbitrary p,q,r result, a general Lonely Runner proof, or a novelty claim.

## What the fresh test adds

The protocol and code were published and fetched at `1b4c636a68363047566d5f816c4bda661b0e1c9f` before evaluation. The 1,197 primitive distinct-speed triples lie in [1,15]^3 outside [1,12]^3, excluding the three already exposed fixed-family cases (1,2,13), (1,2,14), (1,2,15). Every core was built before any r query, and no selector changed afterward.

| Policy | Fresh coverage |
| --- | ---: |
| One widest component | 981/1,197 |
| All components, including isolated points | 1,197/1,197 |
| All positive-width components | 1,196/1,197 |

The isolated-point loss is (1,4,13). Its entire 1/8-safe set is {1/8,3/8,5/8,7/8}. Retaining positive-width core components alone loses every solution, while the stored singleton supplies t=1/8. This is a fresh equality-sensitive example, distinct from the exposed (1,2,6) and (1,2,12). No analogous necessity is claimed at the weaker 1/10 threshold.

The complete representation also preserves phase alternatives that width ranking loses: at (1,6,13), a shorter interval succeeds at t=3/16 while the widest fails. All 216 widest failures and their full physical safe-time sets are saved.

Alternate exact band intersection matches all 34,364 component contact bits, 1,197 witnesses and complete safe-time unions. There are 140 cores with 3,938 components, including 258 isolated points, and up to 54 components per pair. All 310 cases with multiple normalized clock lifts succeed even with the widest source, consistent with the conditional multiple-lift argument. These are bounded checks with same-author alternate algorithms, not independent proof certification.

## Representation checkpoint

**Question and next operation:** obtain one exact 1/8 witness, or the complete safe set, after appending one independent integer runner to the fixed eight-constraint core.

**Retained:** full continuous intervals, isolated equality points, their shared phase constraints and lap labels, every normalized clock lift, and an explicit physical inverse. The event compiler and the pinned older band-intersection checker are complementary representations of the same safe set.

**Omitted by compression:** the widest policy discards other phase placements; positive-only discards isolated valid times. Neither is intrinsically complete. The full stored core is their explicit recovery source.

**Cost and limits:** complete core construction is charged work, not free input. Full representation/physical agreement does not force the safe set to be nonempty on untested pairs. No empty or isolated-only complete core occurred; conditional full-negative and 1/10 branches remained unreached. No speed advantage, optimum, arbitrary mixed-r extension, universal small-menu guarantee or all-reference result is claimed.

**Next:** independently review the fixed-pair two-source candidate, then derive a small-source sufficiency criterion that preserves the needed phase alternatives before another fresh comparison. A wider box alone would not resolve that question.

The [results report](../reviews/2026-10-02-cc-orbit-intervals/RESULTS_REPORT.md) contains full scope, strata, costs, provenance, execution records and reproduction commands. Earlier frozen studies are preserved unchanged.
