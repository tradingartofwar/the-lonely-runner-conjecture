# Independent physical review: different supporting boundary

**PASS.** Reviewed on September 30, 2026 UTC against the frozen September 29
protocol. No production defect was found. This is internal AI review using
previously pinned independent arithmetic primitives, not blind, external human,
or formal verification.

## Inputs and reconstruction

`physical_review.py` verifies the protocol SHA256
`2ea70d567b25185bbd3bf48b4b53fe78d022e0c70fb9dcdc2f8695ebf8f2be0b`
and all 18 SHA256/Git-blob identities in `INPUTS.json` before reconstruction.
The only imported project module is the pinned independent physical reviewer
from `cc-hybrid-recovery`; its row binding is explicitly changed from target
(54,26) to (78,50). Production modules are never imported. Source and parent
geometry are read from pinned inputs; no supplementary external input is used.

The declared rows are the six core rows, (6,2), (3,8), and (78,50), with
stationary reference zero and common start. Arithmetic uses exact fractions.
Times are recovered independently through coordinate-lap congruences, then
checked by direct speed multiplication. Both physical and torus lap labels,
all nine moving phases, reflection, and two alternative Bezout representatives
are checked. The threshold is closed 1/8.

For positive integer parameters, the primary domain is p!=q and p!=2q:
ten distinct speeds including the stationary reference. The four auxiliary
controls (1,1), (2,1), (2,2), and (4,2) instead have nine distinct speeds.
Those cases remain separately labelled and do not count as ten-distinct-speed
examples.

## Physical checks and finite comparison

All 24 frozen controls pass for each method, comprising 20 primary controls
and four auxiliaries. Every recorded control witness has minimum distance
exactly 1/8. All 28 union-direction hybrid dispatches pass independently,
including 26 primary directions and two auxiliary directions.

| Check | Each 24-control method | 28 hybrid union dispatches |
|---|---:|---:|
| Moving phases | 216 | 252 |
| Physical lap entries | 216 | 252 |
| Reflected phase entries | 216 | 252 |
| Reflected physical lap entries | 216 | 252 |
| Alternative Bezout recoveries | 48 | 56 |

The reviewer also checks 76 dispatched points against their labelled full
safe records, recovering local and original parent-edge parameters. Every
screened record is identical to its corresponding full record. JSON roundtrip
dispatch agrees on all 52 hybrid invocations and all 24 full invocations.
Six gcd scaling pairs pass for each method, for 12 comparisons total.

All 2,268 full-candidate contacts (81 records x 28 pairs) and all 280
screened-candidate contacts (10 records x 28 pairs) are independently recomputed.
There are no screened-class losses or dispatch coverage mismatches. The screen
endpoint band audit checks 180 row/endpoint combinations. The independent
finite-reduction check confirms the leader widths alpha=1/12 and beta=1/8,
the 77-pair bounding rectangle, and the 28 residual primitive directions.
The claim outside the residual union relies on the positive leader-width
argument; the finite table alone is not a parameter scan establishing a
universal theorem. Universal coverage remains an internally reviewed proof
candidate within the declared rows, reference, threshold, and input assumptions.

## Selected singleton and witness differences

The hybrid chosen menu contains four nondegenerate segments followed by
singleton `P4:E0-1:K3:L5:M54`, at (3/8,1/2). The only first-time difference
among the 24 controls is (p,q)=(1,4): hybrid time 3/8 versus full time 1/8.
The hybrid speeds are (1,4,5,6,7,11,14,35,278), with phases
(3/8,1/2,7/8,1/4,5/8,1/8,1/4,1/8,1/4), so this witness is physically valid.

The already checked contact matrix shows that the singleton is the only
chosen-menu record contacting (1,4). Removing it therefore loses this
direction from that particular menu. The entire screened candidate class has
three contacting records:

- `P4:E0-1:K3:L5:M54`, the selected singleton;
- `P4:E0-3:K3:L5:M54`, a second provenance of the same point;
- `P7:E0-1:K4:L8:M79`, a nondegenerate segment.

Thus singleton necessity is specific to the selected menu. It is not
necessity for the whole screened class or for physical existence. This
distinction uses existing checked contacts and endpoint equality, without
another parameter scan. No opening of the selected menu was evaluated.

## Empty diagnostics and limits

The screen already covers every residual direction. There are no exception
directions, source queries, exception dispatches, or source-recovery work.
The raw open-source status `COMPLETE_EXCEPTION_RECOVERY` is consequently
vacuous: its exception/query/uncovered lists and preflight rows are empty,
and all source/H/phase/band counters are zero. No original-source endpoint was
removed in an evaluated case; no physical open-source witness was checked.
It supports no claim about opening this selected menu.

The actual zero-budget preflight is `PASS` with work bound zero; it does not
exercise a budget stop. The full-source diagnostic is `NOT_TRIGGERED`.
There is no old-time-failure assertion for this target. Generic degeneracy
kernels retain their inherited pinned evidence, with no new synthetic case.
No benchmark, new target, broader parameter scan, or parent-interior search
was run by this reviewer.

## Reviewer correction record

The first adapted reviewer run stopped before physical comparisons with an
`IndexError`: an inherited JSON-string assertion indexed the first exception
point even though this trial has no exceptions. The assertion was changed to
inspect a screened-candidate endpoint instead. The complete reviewer then
passed. A subsequent run added the requested singleton interpretation from
the same contact table and passed. This was a reviewer adaptation correction;
it changed no production code, frozen input, mathematical result, trial, or
benchmark. `physical_review.py` writes deterministic JSON to stdout, saved as
`physical_review.json` for independent reproduction.
