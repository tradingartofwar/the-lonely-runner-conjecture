# Changed-row geometry and coverage review

September 29, 2026. Separately tasked AI review of the frozen `(6,2)` transfer.
**Result: PASS; no result-level defect found.** This is internal review, not
external human review or formal certification.

Reproduce from the repository root:

```bash
python3 reviews/2026-09-29-cc-coefficient-transfer/geometry_review.py > reviews/2026-09-29-cc-coefficient-transfer/geometry_review.json
```

## Reconstruction and scope

The review adapts the preceding geometry review's supporting-line method; it
imports no production discovery or compiler code. It first reconstructs the
old `(5,2)` input and compares all 27 candidates and coverage fields against
the preserved certificate. Only after that regression passes does it evaluate
the single predeclared new row `(6,2)`.

The changed geometry is reconstructed by intersecting each of the 24 original
floor-edge supporting lines with every labelled boundary and checking the
closed segment and all seven joint bands. This differs from the production
edge-parameter clipping. The global folded box gives `1 <= 6x+2y <= 19/4`,
so laps `1,2,3,4` are complete; the preflight has 96 edge/lap attempts, below
256. There are 1,120 line/boundary intersection evaluations and 672 endpoint
band inequalities. No other changed row or parameter domain was evaluated.

The independent reconstruction matches every candidate field, all 14 ranked
descending records, the 21-pair bounding rectangle, all eight residual pairs,
all 192 matrix entries, and the complete greedy selection history. All 24
candidate records are positive-length segments. The selected menu is:

| Role | Record | Segment | Labels |
| --- | --- | --- | --- |
| Leader | `P2:E0-3:K2` | `y=7/8-2x`, `1/4<=x<=3/8` | `(0,0,0,0,1,1,2)` |
| Fallback | `P0:E0-1:K1` | `x=1/8`, `3/16<=y<=1/4` | `(0,0,0,0,0,0,1)` |

The fallback is vertical. Descending geometry is required for the infinite
coverage leader, not for every candidate that can resolve a finite exception.
The selection rule correctly preserves that distinction.

## Conditional infinite argument

For a closed safe segment with endpoint increments `(alpha,-beta)`, where
`alpha,beta>0`, the primitive orbit functional `H=Qx-Py` has interval width
`alpha*Q+beta*P`. Width at least one supplies an integer contact by taking the
ceiling of the lower endpoint and interpolating. Endpoint safety implies
safety of the entire segment because all labelled inequalities are affine.

If width is less than one, positivity implies `P<1/beta` and `Q<1/alpha`.
Thus every remaining primitive direction belongs to the declared finite
rectangle. This is a sufficient-contact argument, not a claim that width
less than one precludes a contact. The matrix correctly checks integer
contacts there exactly. The physical interpretation also requires the
normalization and clock map, reviewed separately.

For the emitted leader, the orbit interval is

`[(2Q-3P)/8, (3Q-P)/8]`, with width `(Q+2P)/8`.

Hence it covers every positive primitive direction with `Q+2P>=8`. Its full
primitive complement and actual first contacts are:

| `(P,Q)` | Leader orbit interval | First integer contact |
| --- | --- | --- |
| `(1,1)` — repeated-speed auxiliary | `[-1/8,1/4]` | `0` |
| `(1,2)` | `[1/8,5/8]` | none |
| `(1,3)` | `[3/8,1]` | `1` |
| `(1,4)` | `[5/8,11/8]` | `1` |
| `(1,5)` | `[7/8,7/4]` | `1` |
| `(2,1)` | `[-1/2,1/8]` | `0` |
| `(2,3)` | `[0,7/8]` | `0` |
| `(3,1)` | `[-7/8,0]` | `0` |

The fallback covers `(1,2)` at its endpoint `(x,y)=(1/8,1/4)`, with `H=0`.
The complete matrix leaves no uncovered direction, so the conditional richer
geometry diagnostic is correctly **NOT_TRIGGERED**. The proof candidate for
all positive `p!=q` follows from the finite reduction and physical recovery,
not from the 18 finite physical controls alone.

## Equality and information retained

The review also independently checks the 18 emitted **chosen-menu** endpoint
controls. Opening the menu's endpoints loses contact for `(1,2)`, `(1,3)`,
`(2,3)`, `(3,1)`, and `(4,6)`; the last normalizes to `(2,3)`. These controls
concern the selected menu and do not establish that every other candidate
also fails when opened. Closed equality remains consequential.

The method changed its selected geometry while keeping ranking, finite
reduction and greedy rules fixed. It returned to the pinned parent source and
recomputed the complete original floor-edge candidate class under the changed
seventh band, as required by the CC transfer rules. It did not reconstruct
full child regions or search parent interiors: the conditional diagnostic
was not triggered. The old selected menu alone would not establish the
changed-family claim. The new menu carries its own joint labels and
recoverable contacts.

This result supplies evidence of transfer to **one predeclared coefficient
change**. It does not establish general portability, optimum values, every
witness, other reference runners, novelty, or new existence coverage. There
was no candidate-class failure in this experiment, so it supplies no observed
example of the conditional richer-geometry diagnostic repairing such a failure.

## Execution record

The first independent numerical run passed. A second run added a comparison
of the already emitted chosen-menu endpoint controls and passed. This added
review check did not change the frozen candidate generation, selection rule,
row, resource limits, or production output. No production correction was
requested. `geometry_review.json` contains the exact reconstruction and hashes.

## Coordinator synthesis check

Read `notes/CC_CHANGED_COEFFICIENT_TRANSFER_2026_09_29.md` after the numerical
review. Its segment equations, phase formulas, primitive residual table,
fallback role, normalization, and stated scope agree with this reconstruction.
The reported 24 production edge/lap attempts use per-edge projection bounds;
the separate review's global lap bound gives 96 attempts. These are distinct
accounting quantities, not inconsistent candidate counts. The synthesis
correctly says the full-parent diagnostic was not triggered. No new
computations or expanded domain were requested for this synthesis check.
