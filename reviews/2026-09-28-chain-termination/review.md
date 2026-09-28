# Review and exact comparison record

September 28, 2026. Baseline `dd5b3bce9a7a3fb22474a724161438f24e35fb41`.

**Outcome:** the finite replay passes; the general termination and robust-lift
arguments remain **HYPOTHESIS / proof candidates**, pending external review.
No novelty or full Lonely Runner claim is made.

## Roles and isolation

The coordinator audited the pinned repository instructions, previous chain
note, fourth-runner counterexample, and endpoint-discrepancy work. The
`chain_bound` agent derived the overlap-budget termination bound and supplied
a separate final mathematical audit. The `chain_obstruction` agent attempted
a parameterized long-chain construction, preserved its unsuccessful simple
construction, and supplied the robust common-start transfer argument.

After those analytical derivations, the coordinator froze twelve diagnostic
window records before new replay calculations. The coordinator wrote the
primary ceiling-projection implementation. The structural challenger then
wrote the verifier from protocol inputs without reading primary code or
saved outputs. It uses direct phase cases for projections, full local
threshold partitions for feasibility, and both cell integration and interval
clipping for excess coverage. The coordinator read the resulting code and
ran the field-by-field comparison. All of these are internal AI contributions;
agreement between them is not external proof certification.

## Results

| Check | Exact scope/result |
| --- | --- |
| Frozen window records | 12; nine distinct full physical configurations plus two auxiliary inputs, with two windows on the same physical lift |
| Witness versus empty | 11 witnesses; one clipped empty window |
| Scalar projection calls compared | 199 |
| Nonzero moves / selected occurrences | 32 |
| Compared fields | 1049, including all trace inputs, outputs and runner labels |
| Local threshold events used by the verifier | 1085 across the window records |
| Excess-integration cells | 75 on full selected unions; 63 from supplied starts |
| Maximum started rounds in this replay | 3; not a general maximum |
| Small-gcd113 first component | `[129/448,167/576]` |
| Tight13 first component | `{3/8}` |
| Lifted clipped window | Empty; call23 exceeds its right endpoint |
| Lifted extended window | Right-endpoint singleton; call23 reaches it, calls24–33 are stationary |

`comparison.json` records source/output SHA-256 values. The frozen protocol
hash is `134f1825868d1bde006f3cf7f1d523047fc89410d3acaf8da5add4ec658608c0`.
Every replay satisfies both analytic move bounds and all strict overlap
inequalities. Actual excess agrees with both independent geometric integrals
and the endpoint-potential differences. No broad scan, new physical speed
configuration, all-reference calculation, or unrelated test campaign was run.

## Mathematical challenge and limits

The coordinator independently checked the primitive coefficients, its existing
appearance in `OVERLAP_PLACEMENT.md` Section 8, the selected-union excess
identity, and the phase-bound case where an occurrence starts exactly at L.
`bound_review.md`, `proof_audit.md`, and `verification_review.md` preserve the
agents' derivations and challenges. No defect was found under the stated
assumptions. In particular:

- A selected union can extend left; the set-union identity still charges its
  overlap correctly. Full multiplicity dominates selected multiplicity only
  on that covered union, which is exactly where it is integrated.
- Q is the **maximum** pairwise lcm, not an asserted common lattice denominator.
  The proof needs only the lower bound `eta=1/(8Q)` on each positive overlap.
- Open boundaries prevent a touching endpoint from being used as a strict
  chain continuation. Equality points remain valid in the feasibility check.
- At most M(L) selected occurrences contain L; an occurrence starting at L
  does not contain it, and its charged overlap lies to the right of L.
- Every unsafe-start round visits all runners and must advance. K bounds the
  moves and hence rounds, whereas `11K` bounds all scalar calls in this order.
- The robust common-start lift preserves the stated strict endpoint
  comparisons, with an explicit sufficient scale. It excludes cross-runner
  equality ties and requires every itinerary-determining comparison to appear
  in the finite certificate.

The largest fixture uses seven moves but has phase bound 475427840573787.
This result certifies eventual stopping; it is not a sharp cost estimate.
Growing upper bounds do not prove unbounded actual cost. Neither a universal
speed-independent bound nor a counterfamily to every such bound was obtained.

The full eight-runner system has seven constraints, so its mean blocked
multiplicity is 7/4 at this threshold; the four-residual cancellation no longer
applies to that full system. Residual termination does not guarantee that the
terminal time lies inside a core-safe window. Hourly research remains paused.
