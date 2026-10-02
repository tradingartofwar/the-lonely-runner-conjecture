# Separate geometry review: a different supporting boundary

**PASS — 58,814 scalar fields agree.** The unchanged screen and compiler
complete the new `(78,50)` case directly. No exception recovery is needed.
The comparison uses the newly derived 28-direction residual domain, not the
47-direction domain from earlier trials.

This is internal AI arithmetic review with disclosed inheritance, not blind,
external human or formal certification. It imports only the two pinned prior
independent review modules. No production module is imported. The inherited
independent arithmetic changes only row data and the captured target defaults
of its source-bound and query helpers; those function bodies stay identical.
The report retains both old/new bindings and their source hashes.

Production adapter records are checked statically against the pinned source:
the before/after function-source hashes and all changed bindings agree, and
the inherited adapter assigns only the declared attributes. The runtime
code-identity assertion is production evidence corroborated by this static
check; the reviewer does not claim to execute production modules independently.

| Compared evidence | Scalar fields |
| --- | --- |
| Old `(102,50)` hybrid and entire full record | 33,814 |
| Old controls, both methods' dispatch geometry | 1,196 |
| Old regression metadata and new adapter | 272 |
| New complete screen decisions, relations and candidates | 934 |
| New hybrid record | 2,418 |
| New full certificate and clipping trace | 17,606 |
| New candidate/dispatch comparison, controls and diagnostics | 2,502 |
| Complete target summary | 72 |
| **Total** | **58,814** |

The old physical field-count metadata is reproduced from its archive, while
the actual geometric choices for both sets of 24 old controls are independently
reconstructed. Physical clocks, physical laps and reflected phases remain the
separate physical review's obligation. No old benchmark or new synthetic
fixture was rerun.

## New boundary and complete screen

Among the frozen 48 coefficient tests, the only relation is

\[
(78,50)-(6,2)=24(3,2).
\]

It has safe-row index 6, core-row index 5 and `k=3`. The screen tests this
relation on all 36 supplied source records. Ten records pass, including two
point records; eight are descending. All acceptance/rejection predicates,
derived ninth laps, endpoint bands and original parent-edge parameters agree
with production. Omitted records remain uncertified by this sufficient screen,
not declared unsafe.

The selected leader `P4:E0-1:K3:L4:M54` has endpoints
`(29/72,11/24)` and `(35/72,1/3)`, with inherited edge parameters `2/9,8/9`.
It lies on `3x+2y=17/8`. Thus the new row differs from `(6,2)` by raw integer
`24*(17/8)=51` along the whole leader, preserving its phase while changing
its torus lap from 3 to 54.

For positive primitive `(P,Q)`, its orbit interval and width are

\[
\left[\frac{29Q-33P}{72},\frac{35Q-24P}{72}\right],
\qquad\text{width}=\frac{2Q+3P}{24}.
\]

Every closed interval of length at least one contains an integer, so the
leader covers the infinite tail `2Q+3P>=24`. The complete remaining primitive
domain is `2Q+3P<=23`: 28 directions inside the valid 7 by 11 rectangle.
The 77-pair rectangle is below the frozen 400 cap.

The leader misses nine of the 28 directions. Greedy additions cover six,
then one, then one, then one, producing this preserved five-record menu:

| Record | Newly covered residual directions |
| --- | --- |
| Leader `P4:E0-1:K3:L4:M54` | All except the nine retained misses |
| `P3:E0-3:K3:L3:M48` | `(2,1),(2,3),(2,5),(3,2),(3,4),(5,1)` |
| `P0:E1-3:K1:L2:M22` | `(1,2)` |
| `P1:E0-3:K1:L3:M28` | `(3,1)` |
| `P4:E0-1:K3:L5:M54` | `(1,4)` |

The final record is the **singleton `(3/8,1/2)`**. It is a valid pre-screened
geometric fallback, although a singleton cannot lead the positive-width
argument. It is not a newly recovered direction-specific exception point.
This run makes retention of source points operationally consequential.

## Full comparison and exact costs

The full branch emits 81 records from 81 lap attempts, including four points,
42 descending records and a five-record selected menu. Its complete residual
matrix has 2,268 entries. The screen's matrix has 280 entries. Both branches
choose the same new leader and have the same 28-direction residual domain.
All ten screened records are identical full members, including labels,
endpoints and source parameters.

Inside the fresh residual union, the review checks hybrid dispatch against
every full candidate and retains every screened-candidate contact separately.
There are no dispatch coverage mismatches and no screen-class losses. Outside
the union, both safe leaders have width at least one. The reached finite
reductions therefore justify a conditional comparison over **all positive
primitive directions**, rather than a finite-sample extrapolation.

The screen itself is `COMPLETE_COVER_CERTIFICATE`. Its exception list is empty,
so hybrid recovery has zero source/pair projections, raw-range evaluations,
work bound, source visits, H tests, phase tests and parallel-band tests.
This does not make supplied preprocessing or screening free: both methods
still validate the 36 sources with 576 endpoint-band checks, and the screen
still performs 48 coefficient tests and 36 boundary tests. The counts describe
different operations and are not interchangeable timing units.

The raw open-recovery status is `COMPLETE_EXCEPTION_RECOVERY` **vacuously**:
it receives an empty exception list and performs no target open-source query.
This is not evidence that deleting endpoints preserves the new construction.
Likewise the zero-budget preflight returns `PASS` because its actual work
bound is zero; it does not exercise a resource rejection. The richer full-
source diagnostic is `NOT_TRIGGERED`. No point-recovery or open-query kernel
branch is newly tested by this target.

## Scope and execution record

The family still has ten distinct speeds exactly when `p!=q` and `p!=2q`,
with auxiliaries labelled. This is a closed `1/8` witness construction for the
specified stationary reference, stronger than its `1/10` target. It is not an
optimum, a full safe-set description, all-reference coverage or arbitrary
ten-runner existence. The trial supports one informed change of supporting
boundary; it does not establish arbitrary-row portability or a general
parameterized family. No further family was computed here.

The first complete independent reconstruction and comparison passed. No
mathematical, kernel, selection or serialization correction was needed. A
read-only inventory initially used the previous package's regression filename;
the new package correctly stores it as `regression.json`, which this checker
reads. This had no effect on calculations. The benchmark was not rerun and is
not used as correctness evidence. General arguments remain internally reviewed
proof candidates.

Reproduction from the repository root:

```sh
python3 reviews/2026-09-29-cc-boundary-transfer/geometry_review.py > /tmp/cc-boundary-geometry.json
cmp /tmp/cc-boundary-geometry.json reviews/2026-09-29-cc-boundary-transfer/geometry_review.json
```

The compact report pins all compared artifacts, inherited review code,
bindings, counts, new leader and vacuous-diagnostic interpretation.
