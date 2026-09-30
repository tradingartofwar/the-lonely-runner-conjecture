# Separate physical review of the (102,50) hybrid transfer

Experiment date September 29, 2026; execution September 30 UTC. **PASS within
the frozen scope.** The first complete review execution passed without an
implementation or arithmetic correction. No additional target, parameter scan
or benchmark was run by this reviewer.

## Reused independent structure and explicit adaptation

This review imports only the pinned independent physical checker from the
preceding hybrid-recovery package, not production code. Its coordinate-lap,
contact, physical-output comparison and JSON-dispatch helpers are reused with
their ROWS binding explicitly changed from last row (54,26) to (102,50).
New local source-band intersection and source-membership routines use the
explicit TARGET=(102,50). No old target default is used by these routines.

All 14 input SHA-256 and Git blob identities, including the independent checker
and original parent geometry, are verified before use. This is inherited
independent structure, not blind replication or an independent human/formal
review. The adaptation and hashes are included in physical_review.json.

## Domain, shared point and exact inverse

The nine moving rows are
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),(102,50), at closed threshold
1/8. The new row dominates the earlier rows. Ten distinct speeds including
the reference are equivalent to p!=q and p!=2q.

Every selected witness uses one point, one physical time and all nine joint
lap labels. Direct cardinality gives 20 primary cases and four nine-distinct-
speed auxiliaries in each 24-control branch. The 47 union directions contain
45 primary directions and two primitive auxiliaries. The lists overlap;
they are not claimed to be distinct configurations across review groups.

The independent inverse solves Q*i=-H modulo P, with 0<=i<P, after normalizing
d=gcd(p,q), P=p/d, Q=q/d. Put j=(Q*i+H)/P, tau=(x+i)/P and t=tau/d. For P=1
use i=0. The physical lap of row (a,b) with torus lap m is m+ai+bj.
Direct speed products agree with these laps and phases. Reflection 1-t,
two alternative Bezout choices, Euclidean division counts and six gcd-scaling
comparisons per method are also checked.

The separate loaded-JSON selector checks the gcd-reduced exception direction
first, otherwise uses the preserved screen menu. Recovered exception points
are not promoted into globally reusable candidate segments.

## Exact review counts

| Check | Hybrid controls | Full controls | Hybrid union dispatch |
| --- | ---: | ---: | ---: |
| Physical records | 24 | 24 | 47 |
| Primary records | 20 | 20 | 45 |
| Selected phase checks | 216 | 216 | 423 |
| Selected physical lap checks | 216 | 216 | 423 |
| Reflected phase checks | 216 | 216 | 423 |
| Reflected physical lap checks | 216 | 216 | 423 |
| Alternative Bezout recoveries | 48 | 48 | 94 |

Every selected minimum is exactly 1/8. All 95 dispatches match a full safe
candidate and its original parent-edge parameter. The separate JSON consumer
reproduces 71 hybrid dispatches and 24 full dispatches after a fresh roundtrip
of the string-valued rational records. These checks do not assert arbitrary
malformed-certificate validation.

All 4,183 full-candidate/union contacts agree with the saved comparison lists.
The screened records are identical full-candidate members. The unchanged
positive-width leader, its finite reduction and complete exception dispatch
are checked conditionally; the uniform argument remains an internally
reviewed proof candidate.

The three open-source diagnostic witnesses add 27 checks each of selected
phases, selected laps, reflected phases and reflected laps, plus six alternate
Bezout recoveries. The old failed-time record is separate and adds nine direct
phase/lap checks and nine reflected phase/lap checks.

## The invalidated witness and its replacement

For (p,q)=(5,1), the changed new speed is 560. At the previous hybrid time
9/40 its product is 126, so its phase is zero. The other eight moving phases
remain safe at 1/8. Thus only the ninth moving runner fails at that selected
time; this is not a physical nonexistence statement.

Zero-phase reflection is explicitly checked. At reflected time 31/40, speed
560 has product 434 and phase zero. Its reflected lap is 560-126=434, without
the extra subtraction appropriate to a nonzero phase.

Both new methods replace that time with **31/136**. The new runner has phase
11/17 and distance 6/17; another row fixes the overall minimum at 1/8. The
scaled configuration (10,2) uses 31/272 and retains the same phases and laps.

The hybrid changes source from P0:E0-1:K1:L2 to **P0:E1-3:K1:L2**. Its point
is (19/136,31/136), local source parameter 9/17, original parent-edge parameter
3/17, orbit integer -1 and ninth torus lap 25. The ninth physical lap is 127.
The point belongs to the full candidate P0:E1-3:K1:L2:M25 with matching labels.

The other exception points remain (1/8,1/4) for (1,2) and (1/8,1/2) for
(1,4), with ninth laps changed to 25 and 37. The independently recovered source
visit total is 14. The production point-query count is reviewed separately
from our band-intersection implementation; unlike operations are not equated.

Unlike the preceding development result, hybrid and full-menu selected times
agree on all 24 controls in this transfer. This observed agreement is kept
separate from source/provenance identity and from coverage equivalence. It is
not a claim that all future first witnesses must agree.

## Source endpoint diagnostic

Only the original supplied eight-row safe source endpoints are removed by
this diagnostic. Singleton sources have empty open interiors, while the new
row's safe lap bands remain closed. This is not the same operation as opening
the appended clipped segments.

| Exception pair | Closed selected point | First open-source point | Open-source time |
| --- | --- | --- | --- |
| (1,2) | (1/8,1/4) | (7/40,7/20) | 7/40 |
| (1,4) | (1/8,1/2) | (17/56,3/14) | 17/56 |
| (5,1) | (19/136,31/136) | same point | 31/136 |

The first two closed points are source endpoints. The open diagnostic uses
alternative sources P1:E1-3:K1:L3 and P2:E0-1:K2:L2, with local parameters
11/15 and 1/3. The third closed point already has local parameter 9/17 in the
interior of its nondegenerate source. All three open recoveries are physically
safe and members of full safe candidates, with both source maps verified.
The diagnostic does not alter the retained closed selection rule.

## Scope and reproduction

The result shows that the same declared representation and recovery operation
can recover after this deliberately invalidated earlier witness. The transfer
is within the informed progression; it does not establish arbitrary-row
portability, optimality, every witness, another reference or a speed advantage.

Generic degeneracy fixtures, production function-body identity and benchmark
measurements are reviewed elsewhere. This physical review neither reruns the
benchmark nor imports the production adapter. No richer parent search or
threshold change is performed.

From the repository root:

```sh
python3 reviews/2026-09-29-cc-hybrid-transfer/physical_review.py
```

The deterministic physical_review.json preserves the failed old time,
replacement clocks, complete declared physical records, union contacts,
source maps, endpoint diagnostics and explicit reviewer inheritance. Universal
coverage remains an internally reviewed proof candidate; finite physical
checks are not substituted for its finite-reduction argument.
