# Frozen independent third-parameter test

September 30, 2026. Source commit 968a4aadda0dacf32116f7e6456150bc8a00e179.
Freeze this protocol, both executable algorithms, and source pins in Git
before executing any target discovery, control, or physical oracle.

## Question and independence

Replace the last moving speed of the previous ten-runner trial by free r:

    (0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r).

p,q,r are independent positive integer parameters, with common start and
stationary selected reference. The coefficient matrix contains the three
unit rows, determinant 1, and has rank three. There is no prescribed
r=ap+bq relation. Individual integer-speed instances have rational rank one
and a one-dimensional periodic orbit; the ambient family is a three-torus.
This is not a test of rationally independent irrational velocities. Ten
distinct speeds require p!=q, p!=2q and r unequal to each prior moving speed.
The family remains structured: eight moving rows use p,q and only one uses r.
This is the smallest controlled rank increase, not arbitrary rank-three rows.

Use closed 1/8 safety, unchanged from the predecessor, as the structural
target. A real 1/8 witness implies ten-runner 1/10 loneliness. Failure at
1/8 does not imply failure at 1/10. No optimum or all-reference claim.

## Frozen source and competing representations

Read only the 36 safe eight-row segment records in the pinned
cc-nine-runner/stage8.json. Retain endpoints, all eight labels, parent,
source-edge provenance and degenerate records. Validate all endpoint bands.
Their discovery is supplied preprocessing, not a newly discovered result.

In coordinates (x,y,z), compare these classes, both declared before outcomes:

1. EDGES: each source S at z=1/8 and z=7/8, giving 72 records of dimension
   at most one. This is a deliberately restricted, natural boundary lift;
   it is not every possible segment in the three-dimensional safe set.
2. SHEETS: S x [1/8,7/8], giving 36 records of dimension at most two.
   A degenerate S gives a vertical segment. All nine labels are retained,
   the final label being zero. Sheets include their closed edges.

These are ordinary affine polyhedral objects. CC carries the supported
question, common point, integral relations, labels, provenance and recovery;
it does not claim to invent polyhedra, Bezout arithmetic or integer lattices.
The earlier segment-width argument and literature attribution are pinned.
Its two-dimensional finite-exception theorem is NOT transplanted to rank three.

## Orbit criterion and exact discovery

Normalize (p,q,r)=g(A,B,C), gcd(A,B,C)=1. Set d=gcd(A,B),
P=A/d, Q=B/d. Extended Euclid gives aP+bQ=1 and cd+eC=1.
Use the two integral forms

    H1=Qx-Py,
    H2=C(ax+by)-dz.

Their row cross product equals (A,B,C). The proposed orbit criterion is
H1,H2 both integral at the SAME point. Recover
tau={c(ax+by)+ez}, t=tau/g, and verify all nine physical phases and laps
by direct multiplication. This explicitly retains the extra clock lifts
lost by choosing the old pair clock's j=0 branch. The raw forms Bx-Ay and
Cx-Az can generate an unsaturated sublattice and are diagnostic only.

For each object parameterize xy=S(s), 0<=s<=1, z in its closed interval.
Enumerate H1 integers in increasing order. If H1 varies, solve for s,
then take the least available H2 integer in the z interval. If H1 is
constant nonintegral, miss. If constant integral, project all rectangle
corners through H2 and interpolate between its lexicographically first
minimum and maximum corners to reach the least available integer. Preserve
point, s,z,H1,H2, normalization, Bezout data and both lap systems.
No projection-marginal test may substitute for a common-point intersection.

Candidate order: numeric (parent, edge endpoints, seventh lap, eighth lap),
then low/high z for EDGES. No deduplication of provenance records.
For each class greedily choose the record with greatest gain on uncovered
TRAIN directions, tie by candidate order. Stop at full train coverage, no
gain, or eight records. No special leader, post-run reranking, repair or
threshold change is allowed in discovery. This is a declared new rank-three
compiler, not the unchanged old two-dimensional compiler.

TRAIN: all distinct-speed primitive triples in [1,6]^3, lexicographic order.
HOLDOUT: all such triples in [1,9]^3 with max coordinate >6. Compile menus
using TRAIN only, then evaluate HOLDOUT without changing them. This is a
frozen finite-domain extrapolation test, not random or blind sampling, and
not a proved finite reduction of the infinite three-parameter domain.

Extra scaling controls, outside coverage denominators: both w and 2w for
w=(2,3,4),(2,5,3),(4,3,5),(6,4,3),(3,6,4),(5,4,7).
Report them separately even where their primitive case is already in a box.

## Budgets and diagnostics

Caps, fixed before execution: 729 raw cube tuples; 108 candidate records;
100,000 candidate/triple contacts including scaling controls; at most 64
H1 integers per contact; 5,000,000 total actual H1 attempts; eight selected
objects per class. Budget exhaustion is SCOPE_LIMIT, never an exhausted miss.
No benchmark, parameter enlargement, other coefficient family, new source
discovery, or unrestricted search follows a disappointing result.

After menus and contact tables are saved, a separately structured verifier
(no production imports) checks every EDGES and SHEETS hit/miss by working
directly in physical time: fixed z events for edges; p/q wrap intervals
and line/segment intersection for sheets. It checks all saved certificates,
source bands, reflected times, torus/physical laps and scaling controls.
This is alternate-code checking by the same AI author, not an independent
human, blind or formal review.

Only then compute the complete physical safe-time interval union on [0,1]
at 1/8 for every frozen triple, by intersecting each runner's closed safe
time bands. If empty, compute the 1/10 union. Cap 1,000 safe bands per tuple
per threshold and 2,000 distinct event endpoints in any negative-result
cross-check. Check negative unions separately at every exact boundary and
every adjacent open interval's midpoint. This exact event decomposition is
not a floating time grid. The oracle cannot feed the menus or their ranking.

Preserve first lexicographic examples, if present, of: edge-class loss repaired
by a sheet; sheet-menu loss repaired by another supplied sheet; full sheet-class
loss with a physical 1/8 witness; impossible 1/8 with possible 1/10; independent
projection marginals giving a false positive; unsaturated relations giving a
false physical point; canonical pair-clock failure repaired by another lift.
Use the same frozen rows/candidates for these diagnostics, no new search box.
Physical diagnostics preserve exact intervals, points, all phase/lap labels
and source membership. A point outside the source sheets may motivate new
faces or a full three-dimensional lap cell, but does not establish that a
volume or any particular object dimension is mathematically minimal.

## Success, failure and claim status

COMPACT_TRAIN means <=8 objects cover every TRAIN direction. COMPACT_TRANSFER
additionally requires that unchanged menu cover every HOLDOUT direction.
Record every partial coverage count and raw menu stop reason. A valid sheet
witness when all tested edges fail establishes gain over this edge class,
not impossibility of any segment-based method. Safe geometry without an
orbit contact is not a physical witness. INVALID_CERTIFICATE halts success.

Distinguish: menu-cap or greedy failure; supplied-candidate-class miss;
threshold obstruction; physical 1/10 miss; budget stop; implementation defect.
Keep all exact misses and controls. Do not force a complete certificate by
adding oracle witnesses. Analyze what survived and what relationship was lost.

Reproduce deterministic outputs once in a temporary sparse repository and
compare exact bytes; retain every correction with its timing. Finite results
are OBSERVED/REPRODUCED. New general orbit or coverage arguments remain
HYPOTHESIS/proof candidates. No novelty, optimum, general LRC or infinite
three-parameter coverage claim. Update the CC information-loss checkpoint
and research handoff, preserving the postponed parameterized two-coordinate
certificate as a separate pending item. Publish on the existing research
branch, without a main merge or outside communication.
