# What a failed escape certificate leaves open

**OBSERVED, separate adversarial box, November 26, 2026.** For weights **(260, 264, 1567, 2101)** the first-arc certificate abstains at every reciprocal anchor from 1/2 through 1/16. Five of its rejected endpoints actually reach the target. At **1409/4224** the physical minimum is **1/16**, attained only by speed 264. Changing the order of the same certificate tests cannot recover this lineup.

All checks use the stationary reference, common starts, the fifteen nonempty subset sums of four positive integer weights and inclusive clearance of 1/16. Every constructed input has smallest weight at least 257. The replay reads neither the trial panel nor its generator. The adversarial examples were selected after exploration and are separate from the sealed comparison.

## The step from 1/3

The colliding speeds are 264, 1827, 2091, 2361 and 2625. Their first common opportunity occurs after a shift of 1/4224, when 264 reaches the threshold. Moving forward, speed 3932 reaches the upper edge of its initial safe arc after just 13/188736. By the proposed endpoint its unwrapped phase is 1687/1056 and it is safe again. Speeds 3668, 3928 and 4192 also pass through an entire blocked arc and return. Moving backward by the same amount leaves speed 1567 inside a blocked arc.

| Anchor and direction | Colliders | Returned endpoint under examination | Actual minimum | Limiting speed |
|---|---:|---:|---:|---:|
| 1/3 forward | 5 | 1409/4224 | 1/16 | 264 |
| 1/3 backward | 5 | 469/1408 | 53/1408 | 1567 |
| 1/16 forward, archived ranking | 1 | 4193/67072 | 2625/67072 | 1567 |
| 1/16 backward | 1 | 4191/67072 | 1567/67072 | 2625 |

The complete list of safe earliest-escape choices on this lineup is 3 forward, 5 forward, 10 forward, 10 backward and 12 backward. The single collider at the archived choice of 1/16 makes a shorter escape than the five at 1/3. Both 1/16 endpoints fail.

## Why checking the final extrema can give a false positive

**DISPROVEN.** Checking the exact endpoint distances of the smallest and largest speed in every occupied residue class always suffices. For **(257, 258, 1543, 2070)** at **1/5 + 1/8240 = 1649/8240**, all of those representatives pass, including both collider extremes. The sole unsafe speed is **3613**, an interior member of residue 3. This class contains 258, 1543, 2058, 2328, 3613 and 4128.

| Speed in residue 3 | Endpoint distance |
|---|---:|
| 258, smallest | 1519/4120 |
| 3613, interior | **317/8240**, below 515/8240 |
| 4128, largest | 52/515 |

This defeats the proposed shortcut for handling wraparound. In the original first-arc inequalities the fastest speed in each nonzero class still bounds the first crossing for that entire class.

## Boundary and collider controls

- **Equality at the noncollider edge.** For (258, 261, 522, 1453) at 1/3 forward, speed 258 reaches 1/16 exactly as speed 2494 reaches 15/16. The common bound is 1/4128. Both limit the valid time 459/1376.
- **Collider equality and empty noncollider set.** At 1/2 all speeds in the scaled binary control (258, 516, 1032, 2064) collide. The maximum collider 3870 equals 15 times the minimum 258. At 2065/4128 these two tie at 1/16. This explicitly nonprimitive control exercises equality and an unbounded noncollider headroom.
- **Colliders can wrap too.** Set `L = lcm(2,…,16) = 720720` and use (257, 271, L, 17L). For every denominator the collider set contains L and 17L, forcing failure of the ratio bound. At 1/5 forward its colliders are L, 17L and 18L. Their displacements are 1/16, 17/16 and 18/16. The archived predictor returns 461261/2306304, with exact clearance 1/16 at L and 17L. Thus the first-arc selector can lose an earlier success on a primitive superincreasing lineup. This constructed control lies outside the stretch-middle shape.

## Bounded soundness attack and replay

For each `a = 257,…,260`, `x = 1,…,16`, `j = 0,…,15`, `k = 0,1`, take `b=a+x`, `c=a+b+4a+j`, `S=a+b+c`, and `d=16(floor(2S/16)+1+k)−S`. Retain gcd(a,b,c,d)=1. These four nested loops exhaust 1,769 primitive stretch-middle lineups outside the four sampling bands. On every denominator with a collision, test both directions even when the lineup has a clear reciprocal elsewhere. Compute the certificate with class extrema using integer cross-products. Independently compute the modular distance of every physical speed at the endpoint.

| Box result | Count |
|---|---:|
| Signed shifts inspected | 47,760 |
| Certified shifts | 11,549 |
| Certified shifts that returned an unsafe time | 0 |
| Safe shifts declined by the certificate | 2,294 |
| Lineups with a clear reciprocal | 1,408 |
| Additional lineups with a certified shift | 360 |
| Lineups with no certified return | 1 |

The sufficiency argument uses closed arcs. For minimum collider m the step has magnitude 1/(16m). Every collider with speed at most 15m lands in its first closed safe arc. In each nonzero residue class all speeds start at the same phase and the fastest reaches the directional edge first. A step no longer than that crossing time keeps the class in its initial closed safe arc. The bounded test found no failure of this implication. It gives no population success-rate estimate.

From the repository root run the following standard-library replay.

```sh
python observatory/escape_trial/challenge.py
```

**OPEN.** Can a predictor use membership in selected speed intervals within a residue class to certify re-entry while still issuing one time? The interior-speed counterexample gives a falsification test for that extension. AI-assisted challenger work, independent of the trial scoring.
