# Separate physical review of the ten-runner transfer

September 29, 2026. **PASS within the frozen scope.** The reviewer imports no
production code. It adapts the prior coordinate-lap method to nine moving
rows and independently checks the old failed selection, every reached physical
control, and both endpoint-contact operations. This is internal AI review,
not blind, human or formal proof.

The protocol hash and all pinned SHA-256 and Git blob identities are verified.
The first complete reviewer run passed; no execution-driven correction or
additional trial was required.

## Scope and domain

The rows are
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),(38,18).
Every row is evaluated at one shared selected point and physical time. All
three added laps remain attached to that point.

For positive p,q, the new speed 38p+18q strictly exceeds every earlier speed.
The only possible repeated-speed conditions remain p=q and p=2q. Direct
cardinality agrees with the primary condition p!=q and p!=2q at all controls.
The frozen 22 pairs comprise 18 ten-distinct-speed cases and four auxiliaries
with nine distinct speeds: (1,1),(2,1),(2,2),(4,2).

The review runs no additional parameter scan. It reconstructs the one declared
motivating failure at (1,20), then evaluates exactly the 22 protocol controls
for the reached stage. The archival failure comparison retains only its
corresponding rows; it does not confuse the prior seven-moving-runner record
with the expanded nine-moving-runner configuration.

## Independent recovery

For d=gcd(p,q), P=p/d, Q=q/d and integral H=Qx-Py, solve

\[
Q i\equiv-H\pmod P,\quad 0\le i<P,\qquad
j=(Qi+H)/P,\quad \tau=(x+i)/P,\quad t=\tau/d.
\]

Use i=0 when P=1. The physical lap of row (a,b) with torus lap m is m+ai+bj.
Direct products of the actual speeds and t independently recover each phase
and floor. Production Bezout identities, clock floor, reflected time 1-t,
two alternative Bezout choices and Euclidean division counts also agree.

The reviewer derives the first closed integral contact directly from each
segment and compares the selected identity, interval, integer, parameter and
point. It verifies all fixed-lap endpoint bands. Their affinity ensures safety
throughout each closed candidate. Five scaling comparisons retain points,
primitive times, phases and laps, with the correct inverse scaling of actual
time; the new comparison is (2,40) with (1,20).

## Repaired motivating failure

The old nine-runner menu chooses t=7/24 at (p,q)=(1,20). The expanded moving
speeds are (1,20,21,22,23,43,46,163,398). Direct multiplication reproduces
phase 1/12 for the added speed 398, while all eight preceding phases are safe
at 1/8. That particular selected time fails both thresholds 1/8 and 1/10.

| Construction | Time | New speed's phase and distance | Overall minimum |
| --- | --- | --- | --- |
| Old selected time | 7/24 | 1/12 | 1/12 |
| New emitted menu | 63/176 | 41/88 | 1/8 |
| New menu, scaled pair (2,40) | 63/352 | 41/88 | 1/8 |

The new witness comes from P2:E0-3:K2:L2:M16. Its point is
(63/176,7/44), orbit integer 7, ninth torus lap 16 and ninth physical lap 142.
All nine rows are safe simultaneously. The scaled configuration preserves
these phases and laps. This repairs the failed input; the uniform assertion
also requires the separately reviewed coverage argument.

## Reached stage and counts

Only Stage A at 1/8 was reached. Its certificate covers all labelled positive
directions, including auxiliaries. All 22 physical controls have attained
minimum exactly 1/8.

| Check | Count |
| --- | ---: |
| Parameter controls and safe witnesses | 22 |
| Primary ten-distinct-speed witnesses | 18 |
| Auxiliary repeated-speed witnesses | 4 |
| Selected phase checks | 198 |
| Selected physical lap checks | 198 |
| Reflected phase checks | 198 |
| Reflected physical lap checks | 198 |
| Alternative Bezout recoveries | 44 |
| Candidate endpoint-band checks | 936 |

The endpoint-band count covers nine rows at both endpoints of all 52
candidates. These are exact finite checks; they are not themselves an infinite
coverage proof or a claim of optimality.

## Endpoint information now matters to the full candidate class

Opening both endpoints of every selected menu segment removes all contacts
at (1,2),(1,3),(3,1), three primary controls. Opening all 52 supplied
candidates still removes all contacts at (1,2). Thus every supplied candidate's
open interior misses that orbit. This differs from the preceding nine-runner
control outcome, where the complete candidate class retained an open contact
at each tested pair.

The distinction is precise: the compact menu loses three contacts, while the
full supplied open-candidate class loses one. Neither statement establishes
that every physical witness must lie on one of those candidate endpoints.
The actual protocol uses closed candidates and accepts equality, so the
emitted closed cover remains valid.

Point candidates have no open interior. A nondegenerate segment with constant
integral projection retains interior contacts. The review implements both
cases explicitly rather than applying one endpoint convention to both.

## Untriggered conditional paths and limits

The complete Stage A primary guarantee implies the weaker 1/10 requirement.
Stage B is therefore **NOT_TRIGGERED**, and no stage10.json is present. The
full-parent diagnostic is also **NOT_TRIGGERED**. No threshold-1/10 geometry,
parent-interior diagnostic or direct physical-time diagnostic was executed.

The independent conditional diagnostic code intersects physical safe-lap
interval unions for the single declared diagnosed primitive pair. It respects
the frozen sum-of-speeds cap 10,000 and total interval/band-test cap 200,000.
Each next row's full comparison count is checked before its evaluation.
A capped review preserves a scope stop and never reports exhaustion. Those
conditional code paths were not exercised by this result and earn no
execution-validation claim.

From the repository root, reproduce the deterministic review JSON with:

```sh
python3 reviews/2026-09-29-cc-ten-runner/physical_review.py
```

The saved physical_review.json retains input identities, the old failure,
repair comparison, all physical records, scaling checks, endpoint-band and
open-contact results, and untriggered paths. The universal construction remains
an internally reviewed proof candidate. No claim is made about arbitrary
ten-runner speed sets, other references, complete safe sets, optimum times,
general compiler portability, new existence coverage or originality.
