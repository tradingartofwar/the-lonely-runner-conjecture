# Frozen changed-seventh-row transfer — September 29, 2026

**PASS for the one predeclared change (5,2) -> (6,2).** The unchanged coverage
rule selects different geometry and produces a complete sufficient certificate
for positive p!=q. This is evidence of one-case portability. The universal
construction remains an internally reviewed proof candidate, without a novelty,
general portability or new existence claim.

Start with [the synthesis](../../notes/CC_CHANGED_COEFFICIENT_TRANSFER_2026_09_29.md).
Input commit: `50d0379628f4a1097d30bbc55d38c581c4338f02`.
The parent geometry, original compiler and all predecessor packages remain
unchanged. The changed row was frozen before its outcome was calculated.

| File | Role |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | Fixed row, ranking, bounds, controls and conditional diagnostic |
| [INPUTS.json](INPUTS.json) | Source hashes verified against the pinned Git tree |
| [transfer.py](transfer.py) | Parameterized clipping; imports unchanged compiler/evaluator |
| [regression.json](regression.json) | Exact old-row geometry and coverage regression |
| [certificate.json](certificate.json) | Changed-row candidates, rankings, finite domain and complete contact table |
| [run.json](run.json) | 18 changed-family physical controls and menu-endpoint checks |
| [geometry_review.md](geometry_review.md) | Separate line/band reconstruction and coverage argument |
| [geometry_review.py](geometry_review.py) / [output](geometry_review.json) | Exact reconstruction without production imports |
| [physical_review.md](physical_review.md) | Separate physical recovery and information-loss review |
| [physical_review.py](physical_review.py) / [output](physical_review.json) | Coordinate-lap recovery; full-candidate and menu endpoint checks |
| [EXECUTION_RECORD.md](EXECUTION_RECORD.md) | Trial history, review scope and untriggered diagnostic |
| [reproduce.py](reproduce.py) / [REPRODUCTION.json](REPRODUCTION.json) | Five exact output reproductions |
| [MANIFEST.json](MANIFEST.json) | Final hashes, excluding the manifest itself |

From the repository root, using standard-library Python without `-O`:

```sh
python3 reviews/2026-09-29-cc-coefficient-transfer/reproduce.py
```

This reruns the single transfer, verifies regression/certificate/run output
byte-for-byte, reruns the two reviewers and compares their stdout to archived
JSON, then writes REPRODUCTION.json. The reviewer scripts themselves print
JSON. Preserve the linked predecessor packages when copying this directory.

The new menu uses a descending leader and a vertical fallback. Only (1,2)
misses the leader; the fallback supplies time 1/(8d) for original pair (d,2d).
Opening this two-segment menu loses five of the 18 tested contacts, while
opening all 24 candidates loses none of those contacts. The affected
representation and operation are recorded separately.

No residual pair remains uncovered, so the frozen parent-interior diagnostic
did not execute. This successful experiment supplies no observed diagnostic
repair and no evidence of failure on some untested row. The online evaluator
is a consumer of generated data, not a full untrusted-certificate validator
or formal proof checker. Separate AI reconstruction does not change that limit.
