# Two ways a reciprocal anchor can fail

**OBSERVED, opened panel.** Nine of the ten earlier-only successes had a clear reciprocal `1/q` with `2 ≤ q ≤ 16`. One needed a shift. On a different lineup the earlier predictor chose a shift in the wrong place and returned an unsafe time. Its opposite shift also failed. Changing the denominator recovered a valid equality time on that opened example.

These checks concern the stationary reference, sixteen common-start runners, the fifteen nonempty subset sums of the four weights, and inclusive clearance of `1/16`. Search scope was the twelve `stretch_middle` rows of the archived panel. “First” refers to one-based row order in the original 60-row panel. The two failures below are each unique in their respective groups, so changing the within-group order cannot produce a smaller counterexample. The archived 60-row ledger reproduced byte for byte and its controls passed. The nearby shifts reported here were explored after seeing the twelve rows.

## A reciprocal can miss an earlier success

**DISPROVEN.** Every earlier-only success among the twelve has a clear reciprocal with denominator at most 16. Row 42, `(41,80,435,564)`, is the unique exception. In order of denominator `q = 2,…,16`, one divisible speed for each is

```
80, 435, 80, 80, 564, 476, 80, 999, 80, 121, 564, 1040, 476, 435, 80
```

At `1/9` the sole colliding speed is 999. Moving backward by `1/15984` brings it to distance `1/16`. The nearest noncollider edge in that direction lies `7/98640` away, beyond the shift. Moving forward by the same amount pushes 1079 inside the blocked arc. The two signs have identical clearance at the colliding runner, so that runner alone cannot select the sign.

## A single chosen anchor can fail in both directions

**DISPROVEN.** Moving just far enough to free the slowest collider at the earlier predictor's chosen anchor always supplies a witness in one of the two directions. Row 12, `(3,5,28,60)`, is the sole unsafe earlier return among these twelve. At `1/16` speed 96 collides. Speeds 31 and 63 already lie on the forward edge of their safe arcs. Speeds 33 and 65 lie on the backward edge. Each noncollider moves less than `1/16` during the chosen shift, so none can cross the full blocked arc and regain safety.

| Opened row | Anchor and move | Earliest noncollider edge, with speed(s) | Proposed time | Actual minimum, with speed(s) |
| --- | --- | --- | --- | --- |
| 42 | `1/9 − 1/15984` | `7/98640` at 685 | `1775/15984` | `1/16` at 999 |
| 42 | `1/9 + 1/15984` | `7/155376` at 1079 | `1777/15984` | `697/15984` at 1079 |
| 12 | `1/16 + 1/1536` | `0` at 31, 63 | `97/1536` | `11/512` at 63 |
| 12 | `1/16 − 1/1536` | `0` at 33, 65 | `95/1536` | `31/1536` at 65 |
| 12 | `1/10 + 1/960` | `1/640` at 88 | `97/960` | `1/16` at 60 |

The last row is a **post-hoc alternative**. At `1/10` speed 60 is the sole collider and it reaches the threshold before speed 88 reaches its nearest forward edge. The independent denominator-32 grid found `2/23`, with minimum `2/23` at 68, 91 and 93. Both times work. The archived earlier prediction and four-weight abstention keep their original scores.

## What information distinguishes the shifts?

Write `δ = 1/16`, `C = {v : q divides v}` with `C` nonempty, and `h = δ/min(C)`. For each other speed `v`, its initial phase is `r/q`, where `r = v mod q`. For `2 ≤ q ≤ 16` all those phases are already in the closed safe arc `[δ, 1−δ]`. The two times until the first noncollider reaches the relevant edge are

\[
H_+ = \min_{v\notin C}\frac{1-\delta-r/q}{v},\qquad
H_- = \min_{v\notin C}\frac{r/q-\delta}{v}.
\]

An empty minimum gives infinite room. For direction `s`, the two checks `h ≤ H_s` and `δ ≤ vh ≤ 1−δ` for every `v ∈ C` suffice. The first keeps each initially safe speed within its current arc. The second places each colliding speed in its first safe arc after the collision, in either direction. With this choice of `h`, the second check reduces to `max(C) ≤ 15 min(C)`. Equality is admissible in both checks.

There is a limit to interpreting the first check. At row 11, `(3,6,31,72)`, consider `1/10 + 1/640`. The sole collider 40 reaches `1/16`. Speed 109 first exits after `3/8720`, crosses the whole blocked arc, and re-enters by `t = 13/128`, when its phase is `9/128`. The actual minimum is `1/16` at 40. An exceeded headroom certifies a departure during the shift. The endpoint can still be safe. If all noncolliders satisfy `v < 2 min(C)`, then `vh < 1/8`, the width of the blocked arc. In that regime a speed which exits cannot re-enter by the endpoint. Rows 42 and 12 at the primary anchors above satisfy this bound.

**OPEN for the next assignment.** Can a frozen selector recover earlier unsafe rows on unopened inputs using the least and greatest subset sums in each occupied residue, while issuing at most one time? At fixed nonzero residue the numerator in each headroom expression is constant, so the greatest speed represents the first exit. At residue zero the least and greatest determine the collider check. One testable choice is to retain clear reciprocals first, then try denominators in increasing order and accept the first certified direction, forward first on ties. Count denominators processed and final times evaluated separately. Preserve all abstentions, including examples where a runner leaves and re-enters. This is a proposal for follow-up and has no fresh-panel score in this report.

## Replay

From the repository root run `python observatory/study/challenger.py`. It reads the archived panel and ledger, rebuilds all fifteen physical speeds on each middle-gap row, calls the earlier predictor, and checks each endpoint's modular distance with integer arithmetic. It prints all twelve clear-denominator lists, returned times, limiting speeds, and the signed-shift checks above. The panel SHA-256 is `8b68c80e3af724ccdd4436e682e052d357bba6e8b477922a00430abdda9e9830`. The earlier predictor SHA-256 is `8871781f9185eba62d0ab158b4fccf7a5cca1d658bde8d9e9bda5052c86f7651`.

AI-assisted challenger analysis. No general Lonely Runner or novelty claim is made.
