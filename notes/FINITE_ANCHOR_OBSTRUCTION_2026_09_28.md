# Initial safe laps can miss every prescribed rational anchor

**September 28, 2026.** This answers the next question from the
[common-displacement study](COMMON_DISPLACEMENT_CERTIFICATES_2026_09_28.md).
The sufficient criterion is intact, but its failed requirements can coexist at
every small-denominator anchor. The obstruction is explicit, not found by a
speed scan. A later choice of safe laps supplies a positive lonely interval.

**Claim status:** the concrete rational checks are **OBSERVED / internally
REPRODUCED** within the declared scope. The general obstruction and interval
formulas are supplied **proof candidates** under repository governance. A
separately implemented AI challenge found no defect; external review remains
outstanding. These are claims about a certificate's limitations, not a candidate
proof of the full Lonely Runner Conjecture. No novelty is asserted.

Baseline: `2f15767ef7a5cd78c19a6606f24b2e00a51a6805` on
`research/near-doubling-overlap-2026-09-24`. All runners start together; only
reference speed zero is considered. There are `n=8` total runners and the
threshold remains `delta=1/8`. Equality is safe.

## What the previous rule retains

At an anchor `a/d` with reduced denominator `d<=8`, each positive integer-speed
runner is either colliding with the reference or already safe. In one common
time direction, the rule intersects the current safe interval of each already
safe runner and the first upcoming safe interval of each collider. Let `E` be
the latest entry and `X` the earliest exit. Then `E<=X` supplies a common safe
time. `E>X` rejects only these selected interval occurrences.

The open question was whether the failures at different anchors could coexist.
The following construction answers yes, even when the menu includes every
rational anchor of reduced denominator at most eight and both directions.

## One pair defeats all 44 anchor/direction choices

Take

`{0,1,4,5,6,7,q,8q}`, with `840|q` and `q>0`.

Since `840=lcm(1,...,8)`, the last two runners collide at every anchor in the
menu. Modulo one there are 22 such anchors, including zero. In either direction,
their first safe displacement intervals are

| Runner | First safe displacement interval |
| --- | --- |
| q | [1/(8q), 7/(8q)] |
| 8q | [1/(64q), 7/(64q)] |

The fast runner leaves before the slow runner enters, with strict gap

`1/(8q)-7/(64q)=1/(64q)>0`.

Thus those two intervals are disjoint. No conditions on the other five moving
runners can repair their intersection. This proves simultaneous failure of
all first-lap itineraries in the specified menu, including their endpoints.

The frozen numerical case is `q=840`, hence speeds
`{0,1,4,5,6,7,840,6720}`. Both implementations retain all 44 failed choices and
agree on all 308 individual first-safe intervals. This is one constructed
configuration, not 44 independent examples. Its full speed gcd is one.

The boundary matters: replacing `8q` by `7q` makes the pair's first intervals
touch at displacement `1/(8q)`. At anchor `17/56`, the full configuration then
has a valid isolated local contact `t=2041/6720` for `q=840`. The slow runner
blocks immediately before it and the fast runner immediately after it. This
does not classify the full safe set elsewhere.

## A later lap supplies an explicit interval

The old five-speed core `{1,4,5,6,7}` is safe throughout

`[a,a+1/112]=[17/56,5/16]`, where `a=17/56`,

and strictly safe in its interior. Direct phase bounds verify this: the five
forward exit displacements at `a` are `4/7,37/224,1/14,1/112,3/28` respectively;
only speed seven begins on the lower safety boundary and it immediately moves
into safety.

For any positive multiple `q` of 56, the added runners collide at `a`. On

`I=[a+9/(64q), a+15/(64q)]`,

the slow runner's phase lies in `[9/64,15/64]`, strictly safe, while the fast
runner's lifted increment lies in `[9/8,15/8]`. The fast runner therefore uses
its **second** safe lap, with equality only at the two endpoints. Also
`15/(64q)<1/112`, so the core remains strictly safe. Consequently `I` is a
closed lonely interval, with strict interior and width `3/(32q)`.

For the frozen case,

`I=[5443/17920,1089/3584]`, width `1/8960`.

The fast runner blocks immediately outside either endpoint; all other runners
are strictly safe there. Thus this is a complete local safe component, not
merely three sampled safe times. The threshold-event verifier reconstructs it
in a small neighborhood, without reconstructing the whole period.

This first rescue uses anchor `17/56`, which is outside the frozen menu. It
proves that loneliness survives, but by itself would not show that changing
only the lap choices repairs a menu anchor. The next refinement does.

### Post-protocol refinement: keep the anchor, change the lap

After freezing the construction above, we identified a simpler rescue at the
existing menu anchor `3/8`, moving backward. The core is safe on
`[17/48,3/8]`, strictly inside, because its backward exit displacements from
`3/8` are `1/4,3/32,3/20,1/48,1/14`. Both added runners collide at this anchor.
The interval

`[3/8-15/(64q), 3/8-9/(64q)]`

uses the slow runner's first safe lap and the fast runner's second. Its maximum
backward displacement is less than `1/48` for every constructed `q`. Its width
is again `3/(32q)`, with only the fast runner at equality at the endpoints.
For `q=840`, it is

`[1343/3584,6717/17920]`, width `1/8960`.

Thus one menu anchor was useful all along; the first/first assignment hid its
opening. This is explicitly a post-protocol analytical refinement on the same
speeds. Both the original certificate and the failed itineraries are retained.

## No fixed number of early laps fixes this certificate class

The following quantifiers are essential: **for every finite rational anchor
menu A chosen independently of the input speeds, and every fixed positive
integer early-lap budget B**, there is a configuration where the permitted
itineraries all fail although a positive lonely interval exists.

Choose `q` to be a positive multiple of the least common multiple of 56 and all
reduced denominators in A. Use

`{0,1,4,5,6,7,q,8Bq}`.

At every prescribed anchor both added runners collide. In either direction,
the last of the fast runner's first B safe intervals ends at

`(B-1/8)/(8Bq)=1/(8q)-1/(64Bq)`.

This precedes the slow runner's first entry `1/(8q)` strictly. Therefore no
choice among the first B intervals of each runner can align even this pair.
The failure permits arbitrary combinations within the budget; it does not
assume matching ordinal labels. Fixed runner-specific finite budgets are also
covered by taking their maximum.

Nevertheless, at `a=17/56` the explicit interval

`I_B=[a+(8B+1)/(64Bq), a+(8B+7)/(64Bq)]`

is lonely. The slow phase ranges from `1/8+1/(64B)` to `1/8+7/(64B)`, strictly
inside safety. The fast lifted increment ranges from `B+1/8` to `B+7/8`, so
its safe-lap ordinal is `B+1` (zero-based index B). The upper displacement is
at most `15/(64q)<1/112`, protecting the whole core. The width is
`3/(32Bq)>0`. This symbolic argument supplies the unbounded implication.

The post-protocol backward interval at `3/8` generalizes by replacing the two
displacements by `(8B+7)/(64Bq)` and `(8B+1)/(64Bq)`. This rescues the original
small-denominator menu for every B. An arbitrary other menu need not contain
`3/8`; no such claim is needed for the obstruction.

The predeclared `B=10^12,q=840` diagnostic checks the formulas with large exact
integers and no lap enumeration. The coordinator verifies full lifted interval
containment for both displayed intervals. The separate reviewer checks the
early-lap gap and three exact points of the original interval; its written
phase argument supplies the interval-wide step. This diagnostic is not evidence
of exhaustive coverage of B values or a runtime theorem.

## What this changes, and what was already known

The [earlier fixed-time study](TIME_TEMPLATE_CLASSIFICATION_2026_09_27.md)
already explained why a denominator multiple defeats any fixed rational menu
of witness times. That observation alone does not defeat a displacement rule,
which may move away from an anchor. Here the two colliders' speed ratio makes
their **allowed displaced intervals** incompatible. The new point in this
research sequence is that adaptive time within a fixed number of early laps
does not remove that obstruction.

All constructed speeds belong to the existing
[two-variable family](TWO_VARIABLE_SPEEDS.md). Its earlier argument already
supplies selected-reference existence for every admissible pair. These examples
add no new family coverage. They explain a limitation of the proposed
representation and give a direct certificate in a constructed subfamily.

In the language of the [relational brief](inquiries/2026-09-28-configuration-relational-information.md),
the missing object was a compatible choice of **which safe occurrences share
one time**. Separate first intervals do not retain that choice. This is a
pair-level timing obstruction inside a full configuration; it does not show
that genuinely higher-order information is necessary in every case. The full
speed vector still determines everything, and no new invariant is claimed.

The result does **not** rule out speed-dependent anchors, an input-dependent
lap budget, or a fixed number of intelligently selected distant lap candidates.
For this family the useful fast index is B and is available by arithmetic;
there is no need to inspect the B skipped laps. Computing large integers still
has bit cost. No algorithmic lower bound, universal selector, all-reference
claim, or solution of the conjecture follows.

## Reproduction, review, and next question

From the repository root, using only the Python standard library:

```bash
python reviews/2026-09-28-anchor-obstruction/check.py --check
python -S -B reviews/2026-09-28-anchor-obstruction/verify.py
python reviews/2026-09-28-anchor-obstruction/compare.py
```

The [protocol](../reviews/2026-09-28-anchor-obstruction/protocol.json) freezes
the construction, controls, and scope. The
[results](../reviews/2026-09-28-anchor-obstruction/results.json) record every
failed itinerary and lifted certificate. The
[separate challenge](../reviews/2026-09-28-anchor-obstruction/challenge.md)
and [verifier](../reviews/2026-09-28-anchor-obstruction/verify.py) were written
without importing the primary implementation or results. They reconstruct all
308 first bands from threshold events, preserve both rescued local components,
and check the ratio-seven isolated contact. The comparison checks the actual
saved outputs, rather than relying on agreement between prose summaries.
This is internal AI review, with both implementations and limitations disclosed.

**Next bounded question:** can a useful combination of lap labels be selected
directly from speed/window arithmetic, without adding fitted anchors or
enumerating every intervening lap? Audit the existing adaptive-time,
lap-band/floor-sum, and fastest-core results before proposing another method.
The constructed family is already solved explicitly; a next result must state
what additional configurations or guarantee it addresses. The broader question
of forcing a useful certificate for arbitrary configurations remains open.

Hourly research stays paused. This interactive continuation used one separately
tasked reviewer; no broad speed scan, all-reference scan, paid compute, outside
outreach, main merge, or parked `+7/+9` work was started.
