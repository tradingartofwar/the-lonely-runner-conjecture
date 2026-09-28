# Adversarial review of the adaptive reflected pair

September 28, 2026. Scope: the frozen `protocol.json`, eight distinct
runners `{0,1,4,5,6,7,11,V}`, positive integer
`V not in {1,4,5,6,7,11}`, reference 0, threshold `delta=1/8`.
Only speed 11 starts with phase theta. All statements are modulo one in
phase and use time in `[0,1]`. Material AI involvement: independent
mathematical derivation, endpoint review, and writing. General arguments
retain **HYPOTHESIS / proof-candidate** status under `CLAIM_STATUS.md`;
no literature or novelty claim is made.

**Review outcome:** the prescribed adaptive pair has exact best distance
1/8 for every admissible V and every theta. It never supplies a strict
witness at either of its two times. Nevertheless, when 8 divides V, a
directed interval beside an appropriately chosen pair time is strict in
its interior, uniformly over theta. The weaker branch must not be called
a classification of globally contact-only configurations.

## 1. The arithmetic and its endpoint controllers

Let `a=17/56`, `b=5/16`, and let t be the protocol's chosen time. For every
unchanged integer speed v, the distances at t and 1−t agree. The fixed
speeds `1,4,5,6,7` are safe on `[a,b]` and strictly safe in its interior.
Their phases at a are

`(17/56,3/14,29/56,23/28,1/8)`.

Runner 11's two phases differ by `22t` modulo one, so their circular
separation is `d=||22t||`. This separation is unchanged by adding the same
theta to both phases.

| Branch | Unchanged-runner facts at t | Exact separation d |
| --- | --- | ---: |
| 8 does not divide V | Speeds 1 and 7 are at opposite threshold endpoints; V has a nonzero eighth residue | 1/4 |
| 8 divides V, 56 does not | Put V=8m with 7 not dividing m. V has phase r/7 for some r in 1..6; only speed 7 is at equality | 9/28 |
| 56 divides V | V>=56, `t=a+1/(8V)` lies strictly inside `[a,b]`, and V has phase 1/8; only V is at equality | `9/28−11/(4V)` |

In the first branch V may add an equality controller when its residue is
1 or 7 modulo 8; it does not remove the opposing controllers 1 and 7.
In the second branch V's distance is at least 1/7, strictly greater than
1/8. In the last branch the fixed five are all strict, while V is exactly
at its lower safe endpoint.

The final separation uses the correct circular branch. Here

`22t = 6+19/28+11/(4V)`.

For V>=56 its fractional part lies strictly between 1/2 and 3/4. Thus
the distance to the nearest integer is the displayed complement, rather
than the raw fractional part. In particular,

`d >= 61/224 > 1/4`.

All three branches exhaust the declared positive integer domain. The six
excluded speeds remain excluded even though a shifted start could make
coincident velocities a different mathematical problem.

## 2. Exact pair performance, not only an infimum

Let `x=||11t+theta||` and `y=||11(1−t)+theta||`. Circular triangle
inequality gives `max(x,y)>=d/2`. The common unchanged-runner cap at both
times is exactly delta, due to the equality controllers above. Therefore
the full best-of-pair distance is

`max(min(delta,x),min(delta,y)) = min(delta,max(x,y)) = delta`

for every theta, since every branch has d>=1/4. This is pointwise
constancy; it is stronger than identifying the worst-phase value and
simultaneously rules out strictness at the pair times themselves.

The successful time can depend on theta. For the directed-interval
argument below, select the time with larger runner-11 distance, breaking
ties in either direction. An arbitrary time that merely attains the full
pair margin 1/8 is not an adequate selector: both full minima can equal
1/8 while only one time has the runner-11 slack used by the argument.

There is an explicit endpoint obstruction to the wrong selector. In the
second branch, set theta=15/28. At a, runner 11 is at phase 7/8 while
speed 7 is at phase 1/8; their opposing directions isolate that time.
At 1−a, runner 11 has distance 11/56>1/8. Both full minima still equal
1/8. This is a direct symbolic check within the branch, not an additional
speed diagnostic or a phase scan.

## 3. Strict intervals when 8 divides V

At t, the unique unchanged equality controller enters its safe lap as time
increases: it is speed 7 in the second branch and speed V in the third.
At 1−t that controller is at its upper endpoint and enters the safe lap
as time decreases. Every other unchanged runner is strict at the center.
The selected runner-11 distance is at least d/2>1/8.

Thus the selected time has a strict one-sided neighborhood. A particularly
simple sufficient width, valid in both branches, is

`epsilon(V)=1/(56V)`.

Select the interval `[t,t+epsilon]` if the first time has larger runner-11
distance, and `[1−t−epsilon,1−t]` otherwise. All constraints are safe on
the closed interval and strict in its interior. Here are explicit checks
preventing this conclusion from resting only on continuity.

For V=8m with 7 not dividing m, the five fixed runners remain safe to the
right of a until b, a distance 1/112. The V phase is r/7, with
`7/8−r/7 >= 1/56`; its phase advance over epsilon is exactly 1/56.
Since V>=8, epsilon is below 1/112. Runner 11 has distance slack at least
`9/56−1/8=1/28`. Its distance can decrease by at most
`11 epsilon=11/(56V)<1/28`. Interior strictness follows, with a possible
V equality only at the far endpoint.

For 56 dividing V, the fixed five remain safe to the right of t for

`b−t=1/112−1/(8V)>epsilon`.

Runner V starts at phase 1/8 and can advance through its safe lap for time
`3/(4V)>epsilon`. Runner 11 has distance slack at least

`eta(V)=d/2−1/8=1/28−11/(8V)`.

This exceeds `11 epsilon`, since the inequality reduces to V>44 and here
V>=56. Every runner is therefore strict for every positive displacement
smaller than epsilon. Both intervals lie inside `[0,1]`.

For the reflected choice, unchanged integer speeds have the same phases
up to sign along reversed time, so their interval checks transfer. The
runner-11 check is a direct Lipschitz bound from its selected center and
does not assume reflection symmetry at fixed theta. In fact reflection
of the whole shifted configuration sends theta to −theta:

`||11(1−s)+theta|| = ||11s−theta||`.

Consequently the supplied argument gives the uniform-in-theta sufficient
duration bound

`D_V(theta)>=1/(56V)` whenever 8 divides V.

The distance cap at the center is still exactly 1/8. The positive interval
comes from its direction, not from turning equality into an imaginary
strict center margin. The width depends on V and is not claimed optimal.

## 4. Negative implications that must remain visible

When 8 does not divide V, each prescribed time is isolated already in the
unchanged-safe set. At t=1/8, speed 1 requires movement to the right for
strict safety, while speed 7 requires movement to the left. Their
reflection has the reversed conflict. A directed strict-neighborhood
argument at these pair times is therefore impossible, irrespective of
theta or V's phase.

This proves a limitation of the prescribed pair, not absence of strict
times elsewhere. The archived V=13 common-start control is actually
contact-only, while its nonzero phases have positive duration. Other
values with 8 not dividing V already have strict fixed-pair certificates
in the prior classification. Do not describe this branch as all globally
tight inputs or conclude that the positive-duration criterion is
equivalent to divisibility by 8.

Likewise, the earlier fixed-menu failures `V=0,32,88 mod120` must remain
archived. They were true failures of those four fixed times at every
theta. The adaptive pair succeeds on them because its times change; no
prior calculation or failure is retracted. Each failed class consists
of multiples of 8, so the present directed argument treats every member
of those classes without extrapolating the old three representative
diagnostics.

## 5. Scope and evidence limits

Original common-start existence for this entire family was already
covered in `notes/VARIABLE_SPEED_FAMILY.md`. Its adaptive witness is the
current t. The additional conclusion reviewed here is robustness to every
initial phase of speed 11, plus a sufficient strict-duration result on
the divisible branch. It does not handle arbitrary phases of the other
runners, arbitrary speed configurations, real V, or every reference.

The eight frozen diagnostics are finite checks of the prescribed formulas
and endpoint implications. The all-V and all-theta conclusions rest on
the supplied branch arguments and exact circle geometry, not on their
number or the inclusion of a very large V. A fixed number of rational
operations also does not mean constant bit cost for unbounded V.

The denominator-multiple obstruction to a finite fixed rational menu is
respected: in the last branch the time itself depends on V. No new
template search, broad speed or phase scan, or full safe-set reconstruction
is part of this review. The small-gcd selection question and parked +7/+9
extension remain separate.

## 6. Final artifact and synthesis review

Reviewed `schema.md`, `results.json`, `endpoints.md`, `coverage.md`, and
`notes/ADAPTIVE_REFLECTED_PAIR_2026_09_28.md` against the derivation above.
The primary has exactly the eight frozen values, with branch counts
1,4,3 in protocol order. All eight recorded pair envelopes have minimum
and maximum 1/8. The seven divisible inputs have the prescribed radius,
safe-lap clearances at least that radius, and strictly positive guaranteed
runner-11 slack at the far endpoint. Equality-controller lists agree with
the three branches. The canonical diagnostic digest in the inspected
primary output is
`31ad1dc6bf4c5b8d4345147cfa2fbc16f25a69702d98d81a384b378f342e4540`.

The synthesis correctly uses the larger runner-11 distance for selection,
reflects only the unchanged constraints, and bounds runner 11 directly
with its actual theta. Its branch-3 phase range and circular complement,
the two positive endpoint reserves `(2V−11)/(56V)` and `(V−44)/(28V)`,
and the closed-interval duration conclusion agree with this review. The
theta=15/28 countercheck preserves the failure of selection by tied full
margins. No remaining mathematical, endpoint, or quantifier correction was
identified in these artifacts.

This report's evidence is an independent analytic derivation and inspection
of the declared output fields. The separate verifier performs the finite
reconstruction; its status is recorded in its own archive rather than
treated here as verification of an infinite theorem. No new diagnostic
configuration, time template, phase grid, or full-set reconstruction was
introduced by this review. The proposed return to small-gcd selection is a
future task, with distinct hypotheses and evaluation-cost questions.
