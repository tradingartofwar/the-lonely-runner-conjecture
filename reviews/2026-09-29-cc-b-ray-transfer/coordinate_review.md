# B-ray coordinate and logical transfer review

Date: September 29, 2026. Author: separately tasked internal AI reviewer
`b_coordinate_review`. Status: mathematical audit of a proof candidate; not
external human review, formal verification, or a novelty assessment.

## Read order and independence boundary

Before this derivation I read AGENTS.md, CLAIM_STATUS.md, CONTRIBUTING.md and
this package's PROTOCOL.md, followed by the current portions of README.md and
HANDOFF.md and the CC representation rules. I have not read new coordinator
output, selected B candidates, a new B witness list, or B optimum formulas.
The following derivation is saved before inspecting the frozen discovery
implementation. The inherited conversation identifies the general project
and previously proposed coordinate map, so this is not a blinded review.

## Pre-implementation derivation

Write the original seven row vectors as (a,b), namely
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2). The physical B-ray speed in this
row order is aq+b. If t lies in (0,1), set u=t and v={qt}. Then
g=qu-v=floor(qt) is an integer, and the original torus coordinates are
x=v, y=u. In particular H=x-qy=-g. Conversely any point with 0<u,v<1 and
integer g=qu-v has physical time t=u and v={qt}; no additional phase or
clock choice is necessary.

For every original row, aq*t+b*t = a(v+g)+bu. If m is its original torus
lap, its phase is av+bu-m, and its physical lap is ell=m+a*g=m-a*H.
Thus (a,b) becomes (b,a) as a coefficient vector in (u,v), while labels
and parent/vertex IDs remain attached to the same original row or object.
The added row becomes (2,5). Native row order gives speeds
(q,1,q+1,2q+1,3q+1,3q+2,5q+2). Only the first two entries are exchanged
for the conventional displayed B_q order, and the same permutation must
be applied to phases and lap certificates.

Every original inequality normal (A,B,C) in (x,y,z) becomes (B,A,C)
in (u,v,z), with unchanged right-hand side and incidence. The fold x<=1/2
therefore becomes v<=1/2. It does not imply u<=1/2, and imposing that extra
constraint would discard permissible physical witnesses. Coordinate swap is
a bijection on the entire parent geometry and on its closed seventh-band
clippings; preservation of parent and endpoint IDs makes this checkable
without assuming unchanged discovery ranking.

Reflection gives t'=1-t. Since every selected phase lies in [1/8,7/8],
no phase is zero. The reflected phase is 1-phase, its physical lap is
speed-1-ell, and (u,v,g) becomes (1-u,1-v,q-1-g). The reflected point need
not remain inside v<=1/2; physical verification of the reflected witness
does not require it to remain in the folded candidate atlas.

## Tail and finite-prefix logic

Orient a segment lexicographically in (u,v), with endpoints (u0,v0) and
(u1,v1), and put du=u1-u0, dv=v1-v0. For du>0 the projected difference
in g is q*du-dv. At

    Q=max(2,ceil((1+dv)/du))

and every integer q>=Q this difference is at least one. The image of the
closed segment is then a closed interval of length at least one and contains
an integer. This proves tail coverage, including equality; it is a sufficient
width cutoff, not a claim that Q is the earliest actual all-q coverage point.

For every q in the finite prefix 2,...,Q-1, project both endpoints and sort
their two values. Exact feasibility is ceil(lower)<=floor(upper). When
endpoint projections differ, the affine interpolation parameter
(ceil(lower)-g0)/(g1-g0) recovers a point of the same compatible segment.
If projections coincide, feasibility requires that common value to be an
integer and either endpoint is a valid witness; the implementation must
handle this case without dividing by zero. A zero-length segment is covered
by this same equality case. Segments with du=0 have no increasing-width tail
certificate but remain legitimate finite-prefix alternatives.

Selecting a candidate with least Q and a fixed provenance tie-break proves
tail coverage by that chosen candidate. A greedy finite cover then succeeds
if and only if the union of candidate coverage sets covers every remaining
prefix integer: each nonempty remaining union supplies a positive-gain
candidate, so greedy cannot become stuck while a cover exists. This is a
completeness statement for this finite candidate class, not all safe geometry.
The Q>26 guard is an execution boundary: encountering it is a reported scope
limit, not a mathematical failure or permission to extend a scan.

All seven closed affine bands at both endpoints imply the same bands along
the whole segment, hence universal physical safety after the above recovery.
This proof uses no B-ray optimal values or pre-existing optimum witnesses.
The online count is bounded by the number of selected segments; integer and
rational bit complexity may grow with q.

## Adequacy checkpoint

This adapter retains joint phases, labels, incidences, equality, integer orbit,
physical clock and reflection. Candidate orientation and projected coverage
are ray-dependent and must be recomputed; a geometric bijection alone cannot
transport A-ray chosen segments or its coverage table. Face interiors, all
safe times and optima are omitted. The output supports one threshold witness
only. A failed prefix cover would require recovery of richer geometry before
an existence conclusion, and cannot refute loneliness.

## Implementation audit and result

After saving the preceding derivation I read frozen `discover.py` and its
parent input. `coordinate_checks.py` then applied its own coordinate adapter
and called the frozen candidate, cover and witness functions. The output was
saved before reading the new coordinator's `transfer.py` or `transfer.json`.
It uses no new coordinator module and no B optimum data. Because it imports
the frozen discovery functions, it is not an independently implemented
discovery enumeration; the separate discovery reviewer addresses that layer.

The frozen implementation passes the specific hazards identified above:
`select_on` sorts projected endpoints, tests closed feasibility, and handles
equal projections with parameter zero. `candidates` lexicographically orients
the translated clock/orbit coordinates and preserves provenance iteration.
`build_cover` uses the least certified cutoff and stable provenance ties,
then exact finite-prefix coverage with the unchanged Q>26 guard. The pure
`witness` routine uses the second coefficient of the supplied row for laps;
with a swapped row (b,a), this is exactly the required coefficient a.
Its A-specific reporting `main` is not invoked.

The separately run adapter recovered 27 geometric candidates. Undoing the
swap recovers every old candidate endpoint, label, source parameter and ID.
It checked 448 transformed parent-vertex inequalities and 378 closed endpoint
phase bands, and verified the tail-width condition for every eligible record.
The resulting selection is:

| Use | Candidate | (u,v) endpoints | Exact coverage needed |
| --- | --- | --- | --- |
| Tail/primary | P1:E1-3:K1 | (1/4,5/24), (1/2,1/8) | q>=4 by width; q=3 directly |
| Prefix/fallback | P3:E0-1:K2 | (1/8,1/2), (3/8,3/8) | q=2 |

Both candidates have certified cutoff 4, so provenance order picks P1 first.
The prefix is exactly {2,3}; all 54 candidate/prefix membership entries are
retained in `coordinate_checks.json`. Primary projection is
[(6q-5)/24,(4q-1)/8], with width (3q+1)/12. At q=3 it contains g=1;
at q=2 its interval [7/24,7/8] contains no integer. The fallback at q=2
has interval [-1/4,3/8], contains g=0, and returns t=u=9/40. Thus coverage
of all integers q>=2 follows from the proved tail and this complete prefix.
There is no inference from a finite sample to an unbounded claim.

On the primary, v=7/24-u/3, giving
g=ceil((6q-5)/24)=floor((q+3)/4) and
t=(24g+7)/(8(3q+1)). The universal phase identity derived above and the
endpoint bounds certify all seven phases for every selected q. All 24 archived
q=2,...,25 controls and their reflections pass direct physical checks, including
the native/display permutation and lap identities. No additional q values,
optimizer calls, external references, or future-family conclusions were used.

After producing that result I inspected the coordinator adapter. Its only
discovery-side changes are swapping vertices, normals and rows, and binding
the added row to (2,5). It keeps source objects, IDs and iteration order, calls
the same pure functions, and freezes choices before reading the old A output
for geometric comparison. Its checks use t=u, native speed aq+b and synchronized
display permutation. I found no result-level defect in this boundary.

## Exact hazards preserved

- **Wrong physical clock:** at q=2 the selected point is (u,v)=(9/40,9/20).
  Correct time is 9/40. Using v=9/20 as time gives distance 1/10 for speed 2,
  below 1/8. A safe torus point does not license choosing the old A clock.
- **Wrong lap coefficient:** at q=3 the primary returns u=31/80 and g=1.
  For original row (1,0), speed 3 has physical position 93/80 and correct
  lap 1. Reusing coefficient b in m+b*g gives lap 0 and phase 93/80.
- **Wrong orbit sign:** the same row with m+a*H instead of m-a*H gives lap
  -1 and phase 173/80. The original H is -g.
- **Wrong fold:** although the selected pair happens to have u<=1/2, this
  is not inherited from the parent fold. At the already declared q=2,
  candidate P6:E0-1:K3 supplies (u,v)=(41/56,13/28), g=1. It obeys v<=1/2
  and all bands by the audited segment certificate, but fails u<=1/2.
  Replacing the fold would remove a genuinely safe candidate. This example
  does not claim that the selected two-candidate cover would itself fail.

## Reproduction, outcome and limits

Run from the repository root:

    python reviews/2026-09-29-cc-b-ray-transfer/coordinate_checks.py

Frozen input SHA-256:
`53779c7cf3303e71635b5ba4dd1d9a4dc485612b6a87e1556df80703438f5f62`.
Frozen discovery SHA-256:
`67e5c1b187bfdcfae57ad5993e330048c20a108c63ed0a8c8e0d1bafcdfd2f5f`.

**Outcome:** no defect found in the coordinate, lap, reflection, fold,
tail/prefix or one-witness scope of the frozen B transfer. The preceding
derivation supplies its mathematical justification; the exact executable
checks support their stated finite and symbolic obligations. This remains
internal AI review of a proof candidate. A-ray and B-ray discovery now both
use the same safe geometry under an explicit coordinate isomorphism; this
does not test changed coefficient geometry or establish arbitrary-ray or
all-reference success. Candidate discovery and universal coverage remain
distinct from optimality and complete witness-set recovery.
