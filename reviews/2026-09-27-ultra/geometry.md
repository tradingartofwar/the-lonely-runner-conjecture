# Geometry/contact review — September 27, 2026

Pinned API snapshot: `e94a87f650264826569cae63412c43a5175f5ae4`. This is an AI-assisted independent derivation and exact check, not human review, proof certification, or a novelty claim. No original notes or archives were edited. General arguments below remain **HYPOTHESIS / proof candidates** under the repository policy; the expressly checked cases are **OBSERVED / REPRODUCED**. No external literature claims are made or independently audited here.

## Findings

1. A useful contact selector exists **conditional on already knowing the local clear duration is zero**. Opposing threshold phases impose a stronger arithmetic condition than divisibility of the unreduced speed sum. Their times form explicit arithmetic progressions indexed by the pair gcd.
2. In the entire `1680h` family, only the fixed pairs `{3,5}` and `{4,28}` qualify. Their candidate times in J are exactly `9/32` and `3/8`. Thus the duration certificate plus pair arithmetic selects two candidates without constructing the fast runner's events. Direct phase evaluation then decides parity.
3. The same family disproves a further tempting compression: **complete opposing-contact schedules plus all equality-controller labels/directions still do not determine feasibility**. At `9/32`, speeds 4 and 28 remain the opposing controllers for both 1680 and 3360; the latter's phase 0 strictly violates safety. One must check every other constraint, including constraints that are not equalities.
4. A signed vertex-minus-edge channel repairs the loss at the level of exact inclusion-exclusion. It counts closed allowed components. It is mathematically useful as a representation audit; computing it by listing all strata is another exact coverage algorithm, not an efficient general selection theorem.

## 1. Verification of a supplied time is already small

Assume positive integer constraint speeds `v_i`, `n>=3`, `delta=1/n`, a closed bounded window J, and common starts. For a selected reference, negative relative speeds can first be replaced by their absolute values; retain the original n if constraints coincide. Rational speeds can be scaled to integers with the time domain scaled accordingly. We do not extend the arithmetic claims to arbitrary real speeds.

Given a proposed time `t0`, calculate `theta_i=frac(v_i*t0)`. Existence is certified by the k inequalities

`delta <= theta_i <= 1-delta`.

If all hold, put `m_i=floor(v_i*t0)` and intersect the closed safe-lap intervals:

`L=max(left(J), max_i (m_i+delta)/v_i)`,

`R=min(right(J), min_i (m_i+1-delta)/v_i)`.

Then `[L,R]` is the complete allowed component containing t0. Each runner has a strictly blocked gap between consecutive safe laps, so a connected allowed component cannot change any lap label. This gives an O(k) arithmetic verification of the entire supplied component; it does not tell us which t0 to supply.

For an interior t0, the local classification has four cases. All constraints must first be safe:

| Actual active phase pattern | Local allowed set |
| --- | --- |
| No active equality | An open neighborhood |
| One or more phases delta, none 1-delta | An interval begins |
| One or more phases 1-delta, none delta | An interval ends |
| Both phase types | An isolated point |

This is the one-dimensional tangent-cone calculation: a lower-face equality requires displacement `h>=0`, an upper-face equality requires `h<=0`, and strict constraints tolerate sufficiently small h of either sign. The closed window contributes its own one-sided constraint at a window endpoint. Speed magnitudes determine the safe neighborhood size, but only the two actual phase signs determine its direction.

This is not a classification from two arbitrarily chosen runners. All active equalities must be included, and every remaining runner must pass safety. A violated constraint is not an equality controller.

### Required negative controls

The standalone verifier reconstructs the complete allowed sets by direct intersections, then checks these cells:

| Speeds apart from reference 0 | t0 | Lower-phase equalities | Upper-phase equalities | Complete component |
| --- | --- | --- | --- | --- |
| 6,12,18,25,31,37,43 | 3/8 | 43 | 37 | `{3/8}` |
| 6,12,18,25,31,35,43 | 3/8 | 35,43 | None | `[3/8,55/144]` |
| 35,70,105,141,1119,807,1923 | 5/24 | 1119,807 | 105 | `{5/24}` |

The first two preserve the earlier identical frozen snapshot but change actual crossing directions. In the third, looking only at the two exceptional runners predicts a right-opening interval; the active core runner 105 removes its right side. The supplied-time procedure correctly identifies the third controller.

A separate clipping control uses `n=3`, speeds `(1,3)`, and `J=[0,4/9]`. Its local allowed set is `{4/9}` although only speed 3 has phase 1/3 there: the full-period component is `[4/9,5/9]`. Therefore a singleton *in J* need not be globally isolated or have opposing runner controllers.

## 2. Opposing-pair arithmetic selects equality candidates

Let u and v be positive integers, and seek

`frac(u*t)=1/n`, `frac(v*t)=1-1/n`.

Write `g=gcd(u,v)`, `a=u/g`, `b=v/g`, so gcd(a,b)=1. The complete criterion and solution are

`n | (a+b)`, and then `t=(j+c/n)/g`, `j in Z`,

where `c=a^(-1) mod n`, chosen in `{1,...,n-1}`.

The inverse exists because n divides a+b and gcd(a,b)=1. Reversing the orientation interchanges a and b and replaces c by n-c. Since n>=3, the lower and upper phases are distinct.

**Derivation.** Set x=g*t. Opposing phases imply `(a+b)*x` is an integer and `a*x` equals 1/n modulo 1. Equivalently, writing `a*x=p+1/n` and `b*x=q-1/n`, subtraction after cross-multiplication gives

`n*(b*p-a*q)=-(a+b)`,

so n divides a+b. Conversely, with this divisibility and `a*c=1 mod n`, x=c/n gives `a*x=1/n mod 1` and `b*x=-1/n mod 1`. The joint phase period is 1 in x because a and b are coprime, so these are exactly all solutions modulo that period. One can also obtain uniqueness by Bézout: two solutions differ by a number whose products with a and b are integers.

For example, `8+16` is divisible by 8, but the reduced sum is 3; these speeds never have opposite threshold phases at delta=1/8. Unreduced sum divisibility is necessary but insufficient.

For each unordered pair we can therefore reject it arithmetically, or retain its two explicit oriented progressions. This uses at most `binomial(k,2)` pair classes. It does not enumerate every single-runner threshold event.

### Conditional completeness

Let `U=|F_J|` and suppose an exact argument already certifies `U=0`. The allowed set is a finite union of closed intervals and points; hence only finitely many points remain. Each interior surviving point must have both phase types, by the tangent-cone argument. Thus it occurs in one of the opposing-pair progressions. Window endpoints must additionally be tested because of the clipping caveat.

Consequently the following is a complete zero-duration decision procedure:

1. Retain the two window endpoints.
2. Add all opposing-pair progression points inside J.
3. Evaluate every runner's safety at each retained time, removing duplicates.

It certifies an empty window when all candidates fail, **provided the zero-duration premise was established**. Without that premise it can miss every solution: speeds `(1,3)` at n=3 have no opposing pair, and both full-period endpoints fail, yet the allowed interval is `[4/9,5/9]`.

The pair classes are few, but their progression points need not be. In `[0,1]`, a qualifying unordered pair contributes exactly 2g points. At fixed n=4, the distinct, globally gcd-1 speeds `(1,q,3q)` with q>=2 have 2q pair candidates from `(q,3q)`. Thus this is not a speed-uniform constant-size candidate theorem. Keeping progressions symbolically defers the task to solving the remaining modular inequalities in j; it does not make those inequalities disappear.

## 3. Application: a bounded selector for every 1680h

Take the current seven constraints `(1,3,4,5,10,28,1680h)`, n=8, J=`[9/32,3/8]`. Among the fixed speeds the only qualifying pairs are `{3,5}` and `{4,28}`:

- `{3,5}` has g=1, reduced pair `(3,5)`, and times 3/8 and 5/8 modulo 1.
- `{4,28}` has g=4, reduced pair `(1,7)`, and times `(8j+1)/32` or `(8j+7)/32`.

The variable speed y is divisible by each fixed speed v. Its reduced pair with v is therefore `(1,1680h/v)`. The second entry is either 0 modulo 8, or a multiple of 4 modulo 8. Adding 1 can never give 0 modulo 8. **No pair involving y qualifies, for any positive h.**

Restricting both fixed progressions to J gives precisely its two endpoints. The current duration proof supplies U=0 for all h, so the conditional selector is complete:

`y*(3/8)=630h` blocks the right endpoint;

`y*(9/32)=945h/2` preserves the left endpoint exactly when h is odd.

The existing cover-chain proof and this selector are different ways to establish completeness: the former proves the fixed blockers cover the interior; the latter uses U=0 and the fact that no other interior point can have opposing threshold phases. No events of y need be constructed. The work is bounded independently of h, aside from integer bit complexity.

The exact tests reproduce all 128 duration moments for h=1,2,3,4 and confirm their equality, while direct closed-interval intersections give the alternating allowed sets. Additional h=1,000,000 and 1,000,001 checks evaluate pair classes and the two contact cells only; they do not enumerate their threshold events. These large cases illustrate the symbolic derivation, not an exhaustive infinite verification.

### An additional insufficiency result

For h=1 and h=2, every opposing-pair progression is identical, even on the entire unit period, since all qualifying pairs are fixed. At `t=9/32`, the equality labels and orientations are identically 4 at phase 1/8 and 28 at phase 7/8. No other runner is at a threshold in either configuration. Yet y is at phase 1/2 for h=1 and at phase 0 for h=2.

Therefore the existing moment/gcd collision continues to collide after adding the **entire opposing-contact schedule and its complete threshold-controller list**. The missing bit is the safety of a runner that is not on a boundary. A list called “feasible contacts” would already include this safety check; a list called “all active constraints at contacts” might not. The distinction should be made explicit in the next specification.

Once the two-candidate argument is in hand and the right candidate is eliminated, one extra bit — safety of y at 9/32 — is sufficient and necessary to distinguish these two outcomes. This is a minimal repair relative to this family and this binary target, not a universal minimal representation theorem.

## 4. A topology channel that survives points

There is an elementary stratified alternative to Lebesgue integration. Partition J at all threshold events, retaining every vertex and every intervening open edge. For a union A of these strata define

`E(A) = number of included vertices - number of included open edges`.

This is independent of subdivisions: inserting an interior vertex into an included edge replaces one edge contribution -1 by `-1+1-1=-1`. It gives 1 on a point or closed interval, -1 on an open interval, and 0 on a half-open interval. This is the compactly supported Euler-characteristic convention in one dimension; ordinary component counting on nonclosed sets would not obey the same addition rule.

For closed F_J, `E(F_J)` equals the number of connected components, including singleton points. Thus nonemptiness is exactly `E(F_J)>0`. Applying pointwise inclusion-exclusion to each signed stratum gives

`E(F_J) = sum_(A subset runners) (-1)^|A| E(intersection_(i in A) B_i)`,

with the empty intersection J contributing 1. The equation has the same subset structure as duration inclusion-exclusion but a different valuation. No new physical state or interaction has been added.

The verifier computes this channel by an independent common event partition, while direct safe-lap intersections supply the actual components. For the contact family:

| h | Duration U | E(F_J) | E(B_y) |
| --- | ---: | ---: | ---: |
| 1 | 0 | 1 | -157 |
| 2 | 0 | 0 | -314 |
| 3 | 0 | 1 | -472 |
| 4 | 0 | 0 | -629 |

All 128 Euler moments are archived, along with all duration moments. The Euler inclusion-exclusion and direct component counts agree. Negative Euler values for blocking sets are intentional, not negative probabilities.

This is useful for specifying what a boundary-aware representation should preserve. It does **not** show that Euler moments are cheaper to determine, nonnegative quantities suitable for the old duration inequalities, or sufficient to reconstruct component locations and lengths. Taking E(F_J) itself as a new summary would simply encode the answer. Constructing all strata likewise re-expresses exact event enumeration. A useful future result would compute or bound the required signed correction from a bounded arithmetic certificate, as the two-candidate selector already does for this family.

An equivalent existence-only formulation combines ordinary length with atoms at the selected pair candidates and window endpoints: `mu(A)=|A|+number(A intersect C)`. Then `mu(F_J)>0` iff F_J is nonempty. This positive measure exposes the necessary extra information, but its atom support depends on the speed configuration and may be large. It is a model audit, not a new existence proof.

## 5. Reproduction, scope, and proposed next check

Run:

```sh
python -B reviews/2026-09-27-ultra/geometry_check.py
```

The standard-library script writes only `geometry_check.json` beside itself, pins its own SHA-256 and the supplied baseline, and imports no project code. The archive includes:

- 8,192 exact oriented-pair comparisons: n=3..10, u,v=1..32, including u=v, comparing the congruence formula with independently enumerated lower-threshold times;
- four complete 1680h controls, all 128 duration/Euler moments each, and independently intersected local allowed sets;
- two large-h direct candidate/cell controls;
- the frozen 35/37, third-controller, clipped-endpoint, and three-runner tight controls;
- the insufficient unreduced-sum condition, unsafe-third-runner, missing-positive-interval, and growing-candidate-count counterchecks.

The finite checks are diagnostic; they do not mechanically prove the symbolic arguments. Neither a full-conjecture result, all-reference result, literature priority, nor a uniformly small selector for arbitrary integer inputs is claimed.

The next focused falsifiable task is to compare the pair-congruence candidate count with full threshold-event count across the **already archived equality-only components**, and test whether a small fixed collection of arithmetic pair classes suffices after the existing duration bounds vanish. Preserve endpoint clipping and all-runner safety in that comparison. If the candidate classes repeatedly have large gcd, formulate the resulting modular feasibility problem explicitly rather than calling the progression representation a solved selection problem.
