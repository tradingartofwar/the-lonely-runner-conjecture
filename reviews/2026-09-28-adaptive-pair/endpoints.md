# Directed endpoint review of the adaptive pair

**HYPOTHESIS / proof candidate:** for every admissible positive integer V
divisible by 8, the frozen adaptive pair supplies an allowed one-sided
interval of length `1/(56V)` for every initial phase theta of runner 11.
Its open interior is strictly safe for all seven nonreference runners.
Thus, writing D(theta) for actual allowed duration in [0,1],

`D(theta) >= 1/(56V) > 0` whenever `8 | V`.

This is a supplied algebraic argument, not an extrapolation from the finite
diagnostics. It was materially generated and reviewed by AI, remains subject
to independent review, and carries no novelty or general Lonely Runner claim.
The scope is exactly `protocol.json`: eight runners
`{0,1,4,5,6,7,11,V}`, reference 0, threshold 1/8, and only speed 11 shifted
by theta. No new template search or full safe-set reconstruction is used.

The prescribed pair itself still has full distance margin exactly 1/8.
Equality at those two points does **not** imply that their surrounding
configuration has only isolated allowed times. Direction at the equality
controller is decisive here.

## The fixed core has a strict interior

Put `a=17/56`, `b=5/16`, and `I=[a,b]`, of width `1/112`.
The five unchanged speeds 1,4,5,6,7 remain in the following safe laps:

| Speed | Phase at a | Phase at b |
| ---: | ---: | ---: |
| 1 | 17/56 | 5/16 |
| 4 | 3/14 | 1/4 |
| 5 | 29/56 | 9/16 |
| 6 | 23/28 | 7/8 |
| 7 | 1/8 | 3/16 |

Each phase varies affinely between its displayed endpoints without wrapping.
All five runners are strictly safe throughout `(a,b)`. At a only speed 7
is at threshold, with increasing phase 1/8, so moving right makes it strict.
At b speed 6 reaches phase 7/8. Reflection maps this core interval to
`[1-b,1-a]` and reverses the safe direction.

For a frozen adaptive time t, the two speed-11 phase points are `11t` and
`11(1-t)` modulo 1. Their circular separation is `d=||22t||`. For every theta,
at least one of the two has distance at least d/2 from zero: otherwise their
distances to zero would sum to less than their mutual circular separation.
Choose such a pair member; choosing the larger of the two speed-11 distances
is a deterministic option. Define its guaranteed speed-11 excess by
`e=d/2-1/8`.

This selection must use the **raw speed-11 distance**, not a tie in the full
seven-runner margin. For example, in branch 2 at theta=15/28, speed 11 has
phase 7/8 at `t=17/56`, so moving right immediately blocks it. At the
reflected time its phase is `11/56`, strictly farther from zero. The full
pair margins can both equal 1/8, while only the latter meets the raw-distance
selection requirement. This exact phase is an algebraic endpoint
countercheck, not a phase-grid or additional-template search.

We move right from t, or left from `1-t` if the reflected member is chosen.
The speed-11 distance changes by at most `11h` after a displacement of size h,
regardless of theta. For the unchanged integer speeds, reflection satisfies
`||v(1-t-h)||=||v(t+h)||`, so the same rightward bounds establish the reflected
leftward interval. No symmetry of the shifted speed-11 phase is assumed.

## Branch 2: `8 | V`, `56` does not divide V

Here `t=a`. Write `V=8m`. The fractional part of `Va=17m/7` is `k/7` for
some k in `{1,2,3,4,5,6}`. In particular, V is strictly safe at a with
distance at least 1/7. The only unchanged threshold controller is speed 7.

The exact rightward V-safe clearance is

`((floor(Va)+7/8)/V)-a = (7/8-k/7)/V >= 1/(56V)`.

The pair separation and selected speed-11 excess are

`d=9/28`, `d/2=9/56`, `e=1/28`.

Take `R=1/(56V)`. Since V>=8,

- the core's rightward room `1/112` is greater than R;
- V remains safe on `[a,a+R]` and strict on `(a,a+R)`;
- speed 11 remains strictly safe even at displacement R, since
  `e-11R=(2V-11)/(56V)>0`.

Consequently the chosen directed closed interval is allowed and its open
interior is strict. The far endpoint may be at V's threshold when k=6; that
does not reduce its duration. At V=16 this bound gives exactly the familiar
directed interval `[17/56,39/128]`, of width `1/896`, without reconstructing
the full allowed set.

## Branch 3: `56 | V`

Here `t=a+1/(8V)` and V>=56. The core is already strictly safe because
`a<t<b`. Since Va is an integer, the phase of V at t is exactly 1/8.
Only V is an unchanged threshold controller, and moving right makes it
strict. Its exact rightward safe clearance is `3/(4V)`.

The speed-11 separation has no ambiguous wrapping in this range:

`d=9/28-11/(4V)>1/4`,

so

`e=1/28-11/(8V)>0`.

Again take `R=1/(56V)`. The three needed clearances are

| Constraint | Available rightward displacement | Comparison with R |
| --- | --- | --- |
| Fixed five-speed core | `1/112-1/(8V)` | At least R when V>=16; strict here |
| V-safe lap | `3/(4V)` | Greater than R |
| Speed 11 from its guaranteed excess | `1/308-1/(8V)` | At least R when V>=44; strict here |

All comparisons hold because V>=56. Equivalently, at the far endpoint the
guaranteed remaining speed-11 excess is

`e-11R=(V-44)/(28V)>0`.

Thus the chosen directed closed interval is allowed and all its points
except the initial equality endpoint are strict, including its far endpoint.
In particular its open interior has length R. Reflection gives the same
conclusion to the left of `1-t`.

These branchwise estimates prove the stated uniform duration bound. They
are conservative: no claim is made that R is the longest available interval
or the minimum actual duration over theta.

## Branch 1: opposing threshold directions give local isolation

If 8 does not divide V, the prescribed time is `t=1/8`. Speeds 1 and 7 are
both at threshold, but their safe directions oppose one another. For
`0<h<1/56`,

`||1*(1/8-h)||=1/8-h<1/8`,

whereas

`||7*(1/8+h)||=1/8-7h<1/8`.

Therefore every sufficiently nearby time to the left is blocked by speed 1,
and every sufficiently nearby time to the right is blocked by speed 7.
Whenever the selected endpoint is allowed by the other constraints, it is
locally isolated. Reflection gives the same statement at `7/8`.

The two phase points of speed 11 now have separation 1/4, so the pair still
guarantees threshold existence for every theta, but it supplies no strict
one-sided neighborhood. This local conclusion does not determine whether
strict times occur elsewhere. The previously reconstructed V=13, theta=0
control remains contact-only, with exactly `{1/8,3/8,5/8,7/8}` and zero
duration, as recorded in the
[prior exact phase archive](../2026-09-27-fastest-laps/phase_results.json).
It must not be replaced by an all-V positive-duration claim.

The other unchanged constraints are safe at these branch-1 times:
`||V/8||>=1/8` when 8 does not divide V, while speeds 4,5,6 have distances
1/2,3/8,1/4. Thus the raw pair separation really does certify an allowed
point; the obstruction described above concerns nearby strict time.

The distinction is therefore precise: the adaptive rule supplies all-phase
threshold witnesses in all branches; this directed review supplies a
positive-duration strengthening for every `8 | V`; and opposing contacts
in branch 1 remain compatible with the retained tight control. No conclusion
about global strictness of every branch-1 input is inferred from the pair.

## Review limits

The unchanged safe-lap inequalities and speed-11 Lipschitz estimates establish
the entire directed interval, including its endpoint behavior. They do not
use a time grid, phase grid, additional template, numerical optimizer, or
full allowed-set computation. The positive-duration statement is an
unbounded supplied proof candidate; finite arithmetic checks in the primary
and independent archives corroborate their declared cases only. The earlier
V=13 control is reused as an OBSERVED / independently REPRODUCED bounded
result, not newly reconstructed here.
