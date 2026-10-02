# Parent-only segment discovery: frozen protocol

September 29, 2026. Base `b72f21f88113a87728de55b8fb2ecdd3332d0cde`.
Coordinator continuation; no new agent team or independent review. The previous
two-segment answer is already known. This is a reproducible discovery rule on
a development example, not a blinded test, novelty claim or held-out validation.

## Scope and pre-execution reasoning

Review the previous proof candidate, then derive one 1/8-safe physical witness
for every integer q>=2 on A_q=(1,q,q+1,q+2,q+3,2q+3,2q+5), selected stationary
reference among eight common-start runners. Keep equality and physical recovery.
Read only the six-form parents from the frozen atlas as mathematical input;
append row (5,2) explicitly. Do not read child cells, the previous selector or
the optimum spectrum to make discovery choices. The coordinator has seen those
records, so this is a dependency boundary, not an ignorance claim.

For an oriented compatible segment with endpoint differences dx>0 and dy,
the orbit H=qx-y has signed endpoint difference q*dx-dy. Thus
Q=max(2,ceil((1+dy)/dx)) guarantees interval width >=1 for every q>=Q.
This gives a finite prefix q=2,...,Q-1. The known P3 edge would have Q=6;
whether it wins the declared selection rule is not yet computed.

## Fixed discovery rule

1. Extract all parent edges whose two endpoints have z=1/8. Use the stored
   labels and incidence; do not choose parents by their previously known success.
2. On every such edge, enumerate precisely the seventh integer laps whose
   closed band can intersect the edge. Clip by k+1/8 <= 5x+2y <= k+7/8.
   Retain point intersections, vertical segments and their provenance.
3. Sort records by (parent index, original vertex-index pair, seventh lap).
   Orient each clipped pair lexicographically by (x,y).
4. For every dx>0 candidate compute Q above. Select the smallest Q, breaking
   ties by that fixed provenance order. If none exists, report no certificate.
5. Check this chosen tail segment on q=2,...,Q-1. On the uncovered prefix,
   greedily add the candidate covering the most remaining q's, with the same
   fixed tie-break. Stop if covered, or report the uncovered inputs honestly.
   No retuning or claim of global minimum-cardinality coverage.
6. At evaluation time test the selected segments in discovery order: round
   the lower H endpoint, test the closed upper endpoint, interpolate at that
   same integer H and recover t=x and physical laps m_i+b_i H. A constant H
   segment is usable only if that value is integral. No q-sized lap scan.

## Verification and stopping rules

- Reproduce the prior selector's two saved outputs; audit affine band safety,
  coverage, ceil signs, equality, the physical lap map and cost quantifiers.
- Pin a parent-only input file. Confirm it matches the frozen atlas fields.
- Check all generated endpoints and closed bands exactly. A second program
  should reconstruct clipped parent floor polygons and recover their parts on
  the original boundary, without importing discovery code; compare candidates.
- Check the selected tail inequality for its whole unbounded domain and every
  member of the derived finite prefix. If Q>26, record a scope limit instead
  of expanding the physical input range without a revised protocol.
- Use only archived q=2,...,25 for direct witness/reflection checks. Include
  q=4 as an endpoint-removal negative control; no optimizer or new q scan.
- Record fixed geometry/preprocessing cost separately from online selection.
  Failure of this restricted candidate class is not a counterexample to LRC.
- Save the procedure, output, review, limits, reproduction hashes and live
  handoffs. Preserve old packages. No new family/reference, external contact,
  literature sweep, main merge, paid or unattended work.
