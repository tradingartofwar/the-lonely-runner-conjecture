# Primary proposal: simultaneous last-runner coverage bands

Date: 2026-09-29. Parent: `f3c26e709fa1cd8945968dcd585bd012430c7243`.
Status: pre-evaluation design; no mathematical executable evaluation has been run.
The coordinator must freeze the case list and output scope before execution.

## Proposed bounded scope

Use exactly these inherited six-constraint cores, at threshold 1/8 on [0,1]:

1. `C611={1,4,5,6,7,11}`: archived widest width 1/112, so the only
   potentially zero-duration last speeds satisfy `11<d<=28`.
2. `C3724={1,4,5,3,7,24}`: archived widest width 3/448, so the only
   potentially zero-duration last speeds satisfy `24<d<=112/3`.
3. `C566472={1,4,5,56,64,72}`: reconstruct its exact safe components;
   derive the cap from their widest width before any last-speed evaluation.
   If the cap is at most72, record an empty remainder rather than evaluating
   any final speed. The old112/113 controls need no new numerical evaluation
   if a width certificate already applies to every d>72.

The first two caps are deductions from already archived rational widths.
This is a one-variable speed-domain audit for three fixed inherited cores,
not a scan of a,b,c triples or the outstanding finite four-speed region.

## Exact mathematical interface

Reconstruct the closed core-safe set using successive intersections of exact
closed safe laps, merging touching pieces and retaining isolated points.
For each nonempty component I=[l,r], l>0, and lap m, strict coverage by d
means

`d*r-1/8 < m < d*l+1/8`, equivalently
`(m-1/8)/l < d < (m+1/8)/r`.

For weak coverage by closed blockers, replace both strict inequalities by
non-strict ones. This retains the boundary cases where final safe duration
vanishes but equality witnesses remain.

Let w be the largest positive core-component width and U=1/(4w).
Any d>U leaves positive final duration, and d=U cannot strictly cover the
widest closed component. Thus all speed-domain calculations can use
`D=(max(C),U]`. If D is empty, every faster speed has positive duration.
For every component and every d in D, candidate laps are among
`m=0,...,ceil(U)`; this bound follows from0<t<1 and threshold1/8.

Calculate three different sets of real speeds within D:

- F: every closed component, including singleton components, is contained
  in an OPEN blocker. This means no final safe point in the first core period.
- P: every POSITIVE closed component is contained in an OPEN blocker;
  singleton core components are ignored. This tests precisely the
  information discarded by retaining only positive components.
- Z: every POSITIVE closed component is contained in a CLOSED blocker;
  singleton core components are ignored. This is equivalent to zero final
  safe duration, and does not imply absence of safe points.

These sets satisfy F subset P subset Z. For integer d, periodicity makes
the [0,1] result a full-period classification. For noninteger real d, it is
only a first-core-period classification; no global absence claim follows.

## Proposed outputs

- Exact reconstructed components, isolated points, safe measure, widest
  component, all widest ties, w, U, and the analytically implied cap.
- For each mode, rational speed bands with endpoint inclusion flags and
  compatible lap-label vectors. Empty bands and singletons are handled
  exactly; no floating-point sampling or midpoint-only containment test.
- A deterministic prefix trace, adding time components in increasing-left-
  endpoint order, to show exactly which cross-window restrictions remove
  a formerly feasible speed interval. Keep each entire union of bands.
- Integer points in each mode, obtained from band endpoints rather than
  a loop over a preassigned speed box. This distinguishes strict full cover,
  cover after discarding core singletons, and zero-duration outcomes.
- Exact full final safe sets ONLY for the integer points in Z and the two
  already designated diagnostics d13 and d16 for C611. These sets retain
  equality-only witnesses. This is a data-dependent output already specified
  by the mathematical classification, not a post hoc expansion of speed scope.
- Source/protocol/output hashes; all arithmetic uses Fraction.

The independent implementation should reconstruct the core by threshold
events, obtain speed breakpoints from endpoint threshold equations, and
classify all open cells plus boundary points. It should not import this
primary implementation or read its result before freezing its own output.

## Limits

General equivalences are proof candidates pending external review; finite
exact outputs are OBSERVED. No novelty claim is proposed. The existing
adaptive reflected-pair result already covers every admissible final speed
for C611; this audit explains simultaneous containment and endpoint loss.
No all-reference, arbitrary-phase, new tuple, or broad speed scan is proposed.
