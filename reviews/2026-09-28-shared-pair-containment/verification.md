# Independent exact verification

Status: **OBSERVED/REPRODUCED** for the frozen finite cases. This
separately authored AI verification is not independent human mathematical validation.

`verify.py` imports neither `primary.py` nor its helpers. It reconstructs exact
rational threshold events, checks every open cell and every event point, and only
then compares the resulting mathematical claims with the primary output.

## Result

| Case | Shared pair containment | Five-edge raw bound | Duration conclusion |
| --- | --- | ---: | --- |
| `collective_target` | True | 49/524400 | positive duration |
| `strict_16` | True | 1/896 | positive duration |
| `tight_13` | True | -1/182 | no positive-duration certificate |

The target containment simultaneously certifies the two supplied zero triples;
logically these remain **two zero-triple predicates over one preselected shared pair**.
The certificate is neither a one-bit-information claim nor a pair selector. The pair
is fixed by the frozen protocol before this calculation.
A competent cached triple comparator can also reuse that one pair-occurrence table;
the shared traversal still evaluates two complement-safety predicates. Thus the
uncached two-reconstruction comparison is an implementation ledger, not an intrinsic
factor-of-two information or runtime theorem.
Its five-edge correction gives `49/524400`. The fixed strict-16 containment gives
`1/896`. Tight-13 also has the containment, but its raw five-edge value is `-1/182`;
it therefore does not convert the valid isolated point `t=3/8` into positive duration.

All six diagnostic base pairs in doubling-112 fail. Each failure in
`verification.json` retains an exact positive open interval, its midpoint witness,
the violating complement runner, and the threshold-event state.

## Exact scope and checks

The four original windows contain **91 open cells** and
**95 cut/event points including window endpoints**. The reflected target adds
**17 open cells** and
**18 cut/event points including endpoints**. Exact state reconstruction
agrees with the pinned joint geometry (atoms, moments, blocker pieces), and the three
controls also agree with the separately archived blocker/lap lists.

The reflected target is the exact reversed cell sequence with identical masses and
moments; it is not re-selected or counted as an independent example. At tight-13's
endpoint, runner 11 blocks immediately to the left while runners 5 and 13 block
immediately to the right.

Source SHA-256 values are checked before use. The old sparse replacement-16 bound
`1/896` and replacement-13 nonnegative bound `0` are reproduced as comparisons;
the old sparse edge tests are not conflated with the present shared certificate.

## Reproduction and limits

```bash
python -B reviews/2026-09-28-shared-pair-containment/verify.py --check
```

The check is read-only and verifies protocol/source/primary hashes, exact geometry,
containments, six explicit failures, reflection, endpoint semantics, arithmetic, and
the committed JSON and Markdown bytes. The result proves only these supplied finite
windows and fixed pairs. It gives no general pair-selection theorem, no new speed or
window coverage, and no novelty claim. Positive-duration statements remain distinct
from isolated equality; archived abstract measurable covers are not runner realizations.
