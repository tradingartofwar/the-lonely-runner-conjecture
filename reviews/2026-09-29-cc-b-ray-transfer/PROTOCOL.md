# Frozen-rule transfer to the B ray

September 29, 2026. Research input base:
`6b2b9316dbc87499a1cb5184aadbd6614d4d6c32`.
The maintainer requested team work. Separate AI reviewers will audit coordinates,
discovery arithmetic and physical recovery; this is internal AI review, not
independent human certification, formal verification or a novelty assessment.

## Question and fixed scope

Apply the A-ray parent-only discovery rule unchanged to the already studied
B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2), integer q>=2, selected stationary reference
among eight common-start runners. Select one physical 1/8-safe time with a
q-independent number of arithmetic selection operations. No optimum or full
witness-set claim; no new family, reference, physical q range, optimizer,
literature sweep, outside contact, main merge or unattended work.

The coordinator and reviewers know previous B-ray optimum work exists. That
spectrum and its witnesses may be used for comparison only after discovery,
not to choose candidates, ranking, exceptions or the selected time.

## Coordinate translation fixed before execution

Original torus rows remain (1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2).
For B, x={qt}, y={t}, H=x-qy integral, physical clock t=y.
Use canonical selector coordinates u=y, v=x and g=q*u-v=-H. Then every
original row (a,b) becomes (b,a), its speed is b+a*q, and its physical lap
is m+a*g=m-a*H. The first two speeds must be permuted only for display as
B_q; all labels and phases must follow the same permutation.

Retain the original fold x<=1/2 as v<=1/2. Do not silently replace it by
u<=1/2 or assume physical time t<=1/2. All generated points still have
0<u,v<1. Reflection is t -> 1-t, with physical laps speed-1-lap.

Swap the two coordinate entries in all input vertices and constraint normals;
swap row components, including the added row to (2,5). Preserve parent and
original vertex IDs, incidence, lap labels and canonical provenance order.
Orient candidates lexicographically in the new (u,v) coordinates, exactly as
the frozen algorithm orients its clock/orbit coordinates. Generate all closed
clippings, compare Q=max(2,ceil((1+dv)/du)) where du>0, choose the least cutoff
with the same provenance tie-break, then use the same greedy prefix rule.
This coordinate adapter is the entire authorized change. Do not retune.

The previously frozen Python discovery functions may be imported without
editing their file. Bind their added-row constant to (2,5) and pass the
transformed parent input. Call the pure discovery/cover/witness functions;
their A-specific reporting main is not the B-ray checker. Record this boundary.

## Checks fixed before execution

1. Independently derive the clock, orbit sign, lap and reflection maps; audit
   fold semantics, endpoint orientation and display permutation.
2. Compare the transformed geometric candidates with the frozen A candidates
   after undoing the coordinate swap. The safe geometry should be unchanged;
   coverage and chosen records may differ. No child-cell/optimum input to choices.
3. Separately implement coverage/ranking from parent geometry and integer
   intervals without importing the coordinator adapter. Certify the unbounded
   tail inequality and every member of the derived finite prefix. Preserve the
   original Q>26 scope guard instead of expanding a physical scan.
4. After freezing selected segments/times, check only archived q=2,...,25,
   and their reflections, directly in physical time. Add a polynomial/residue
   or endpoint proof for universal phase safety; finite samples alone do not
   establish the all-q claim. No fresh optimum search.
5. Test the consequential wrong-clock/wrong-lap alternatives on these same
   controls if they expose a real failure; report the exact input and failure.
   Do not tune the selector to avoid its own failed cases.
6. Each reviewer saves a report with read order, dependencies, authorship,
   results and limits. Coordinator reconciles and reproduces outputs, updates
   the representation record, and preserves old and concurrent repository work.

If the rule fails, preserve the failure and distinguish an uncovered candidate
class from failed loneliness. Any repair or scope change must be recorded as
post-protocol work rather than silently folded into the frozen transfer.
