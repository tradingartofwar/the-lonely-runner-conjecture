# Separate physical review of contact-first hybrid recovery

Experiment date September 29, 2026; execution September 30 UTC. **PASS within
the frozen scope.** This reviewer imports no production code. It reconstructs
source/orbit intersections by safe parameter bands, recovers physical time
through coordinate laps, and consumes the saved string-valued hybrid JSON
through a separate selector implementation. This is internal AI review, not
blind, human or formal certification.

The frozen protocol and original INPUTS.json identities are verified. The
additional REVIEW_INPUTS.json pins the six-core PARENT_INPUT.json solely for
independent original parent-edge parameter validation. This supplementary
review dependency does not change the frozen construction inputs or protocol.

## What was checked

The nine moving rows are
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),(54,26), at closed threshold
1/8. Ten distinct speeds require p!=q and p!=2q. All nine phases are checked
at the same point and physical time, with all three added lap labels retained.

The 24 frozen physical controls contain 20 primary cases and four auxiliaries
with nine distinct speeds. The 47 residual directions contain 45 primary
cases and two primitive auxiliary directions. The two lists overlap; they
are not described as 71 distinct physical configurations.

| Check | 24 controls | 47 residual dispatches |
| --- | ---: | ---: |
| Safe recovered witnesses | 24 | 47 |
| Selected phase checks | 216 | 423 |
| Selected physical lap checks | 216 | 423 |
| Reflected phase checks | 216 | 423 |
| Reflected physical lap checks | 216 | 423 |
| Alternative Bezout recoveries | 48 | 94 |

Every minimum is exactly 1/8. There are also 71 full-candidate membership and
original-parameter checks, 71 independent JSON-roundtrip dispatch checks, and
90 endpoint-band checks on the five screened candidates. The three open-source
diagnostic witnesses and three full-menu comparison witnesses are retained
separately, with 27 checks each for phases, selected laps, reflected phases
and reflected laps, and six alternative Bezout recoveries in each group.

The initial complete physical review passed. Before finalizing, the requested
full-menu witness comparison and all-dispatch membership records were added,
and the supplementary parent-input dependency was pinned and verified. All
regenerations passed. No production correction, failed mathematical check,
new target, added parameter case or benchmark rerun occurred.

## Independent physical inverse and JSON dispatch

For d=gcd(p,q), P=p/d, Q=q/d and H=Qx-Py, choose i in 0,...,P-1 with
Q*i=-H modulo P, then j=(Q*i+H)/P. Set tau=(x+i)/P and t=tau/d. For P=1
use i=0. A row (a,b) with torus lap m has physical lap m+ai+bj.

Direct multiplication of every actual speed by t agrees with the corresponding
phase and floor. Reflected time is the preserved convention 1-t. Two separately
constructed shifted Bezout pairs yield the same primitive time and laps.
Six scaling comparisons pass, including the new (10,2) versus (5,1) control.

The independent selector first normalizes the input by gcd and checks its
primitive direction against the exception table. If absent, it uses the
original selected screen-menu order and derives the first integral contact.
It does not treat exception points as globally reusable candidates.

All 24 controls and all 47 residual pairs match the production dispatch route,
source where applicable, selected point, phase/lap data and physical clock.
A fresh JSON serialization/deserialization preserves those independently
computed outputs. The separate selector parses rational strings as exact
fractions. This checks the review implementation against the emitted record;
it is not a general validation claim about arbitrary malformed certificates.

## Source recovery and witness order

The independent source query intersects the new safe lap bands with the source
parameter's exact orbit point or orbit line. This differs from the production
nonparallel query, which first locates the orbit point and then checks its
fractional phase. Only the three declared exception directions are queried.
The recovered source order, local parameters, original parameters and laps
match the saved dispatch table:

| Primitive pair | Source | Local parameter | Original parent-edge parameter | Hybrid time |
| --- | --- | --- | --- | --- |
| (1,2) | P0:E0-1:K1:L2 | 1 | 1 | 1/8 |
| (1,4) | P1:E0-1:K1:L4 | 1 | 1 | 1/8 |
| (5,1) | P0:E0-1:K1:L2 | 1/5 | 4/5 | 9/40 |

Each original parameter is checked twice: through the supplied source's
parameter interval and against the actual parent-edge vertices. Each recovered
point belongs to a full appended candidate with exactly matching inherited
and ninth laps. For (5,1), that candidate is P0:E0-1:K1:L2:M12, whose original
parameter interval [3/4,23/26] contains 4/5.

All 71 reviewed dispatches also belong to their corresponding full safe
candidate, and their points agree with the original parent-edge maps.

The full greedy menu chooses the same physical times for (1,2) and (1,4), but
it chooses **31/136** for (5,1), whereas the hybrid chooses **9/40**. Both
recoveries are safe. Contact existence agrees without requiring witness order
or identity to agree. The scaled hybrid input (10,2) gives time 9/80.

## Opening sources is a different diagnostic

The open diagnostic excludes the endpoints of the supplied eight-row safe
source segments. It does not open the appended ninth-row clipped segments.
The new safe lap bands remain closed. Singleton sources have empty open
interiors even if their formal parameter interval could contain interior
parameter values.

The first two retained closed exception points lie at source endpoints; the
third is already interior. Repeating the diagnostic with the source endpoints
excluded still recovers all three directions:

| Pair | Closed selected point | First open-source point | Open-source time |
| --- | --- | --- | --- |
| (1,2) | (1/8,1/4) | (7/40,7/20) | 7/40 |
| (1,4) | (1/8,1/2) | (41/88,19/22) | 41/88 |
| (5,1) | (1/8,9/40) | same point | 9/40 |

The first two open recoveries use alternative sources P1:E1-3:K1:L3 and
P7:E0-1:K4:L8. Their local parameters are 11/15 and 3/11; their original
parameters are 3/5 and 2/11. All three open recoveries are strictly interior
to nondegenerate supplied sources, physically safe, and contained in full
appended safe candidates. The independently reconstructed source visit totals
agree: 11 closed visits and 47 open visits.

Thus the retained closed witness identities use equality at two source
endpoints, but these three directions do not require those endpoints when
all supplied sources are available. This does not establish an open-source
coverage theorem for every direction or characterize all physical witnesses.
The closed dispatch rule remains unchanged.

## Conditional completeness and limits

The independent check reconstructs the screen leader's positive widths,
its 136-pair bounding rectangle, the 47 coprime residual directions and the
three menu misses. The exception table equals those misses exactly. The
leader's closed projection covers the remaining directions once its width
is at least one. Endpoint bands certify the entire selected segments, while
the reviewed exceptions certify the remaining directions.

This supplies a conditional uniform-construction argument on the declared
positive integer family; it remains an internally reviewed proof candidate.
Finite physical checks are not substituted for that argument. Unknown inputs
with neither an exception nor a screen contact fail visibly in the separate
selector rather than producing an unchecked time.

The separate geometry/proof reviews cover the generic query equivalence,
preflight and synthetic kernel fixtures. This physical review did not rerun
timing, add synthetic fixtures, recover richer parent interiors or change the
threshold. No speed, optimality, complete-safe-set, general portability,
other-reference, novelty or arbitrary ten-runner claim follows.

From the repository root:

```sh
python3 reviews/2026-09-29-cc-hybrid-recovery/physical_review.py
```

The deterministic output is physical_review.json. It preserves both evidence
levels: the screen menu supplies a uniform tail, while direction-specific
exception points carry provenance and the exact physical inverse needed to
complete this one-witness construction.
