# Fixed-geometry coefficient range

September 29, 2026. Complete argument and scope:
[CC_COEFFICIENT_RANGE_2026_09_29.md](../../notes/CC_COEFFICIENT_RANGE_2026_09_29.md).

Result: W has 31 positive coefficient rows; R has 42 infinite residue classes.
W requires the entire fixed leader and fallback; R requires the leader and
only the fallback point used for primitive direction (1,2). Both support the
stationary-reference 1/8 witness construction, with the declared physical
distinctness conditions. Four accepted rows duplicate core rows identically.

This package is a symbolic applicability analysis of fixed geometry. It is
not another held-out compiler transfer, a classification of all successful
deterministic outputs, global existence discovery, or a novelty certificate.
The general argument remains an internally reviewed proof candidate. Material
AI generation and separate AI review are disclosed in the reports.

| File | Purpose |
| --- | --- |
| PROTOCOL.md | Frozen questions, reductions and controls |
| INPUTS.json | Source head and SHA-256 / Git blob identities |
| classify.py | Integer-band predicates and Bezout physical recovery |
| classification.json | Full 147-case finite and 104-cell residue tables |
| witnesses.json | Frozen progression and negative physical controls |
| algebra_review.py / .json / .md | Separate forbidden-band intersection check and derivation |
| physical_review.py / .json / .md | Separate coordinate-congruence recovery and proof review |
| EXECUTION_RECORD.md | Ordering, corrections and review limits |
| reproduce.py / REPRODUCTION.json | Four exact output reproductions and full cross-comparison |
| MANIFEST.json | SHA-256 identities of this package and its main note |

Run from the repository root, with Python 3 and its standard library:

```sh
python3 reviews/2026-09-29-cc-coefficient-range/reproduce.py
```

Run without `-O`, since the exact checkers use assertions. Reproduction reruns
only the frozen reductions and controls. It checks source hashes, compares all
four output files byte-for-byte, and compares complete contract classifications
plus 1,062 shared physical fields and six shared counts across implementations.
It overwrites the same deterministic JSON outputs locally.

Direct physical controls are exactly k=0,1,2 for (A,B)=(6+16k,2+8k), with
the prior 18 p,q pairs: 54 configurations, 51 distinct and three repeated
auxiliaries. k=0 reproduces all 18 archived controls. Both negative physical
controls fail at seventh phase zero; all 36 nonzero-k stale-label controls
fail phase reconstruction as intended. The (22,10) interior F collision is
an ambient geometric control, not a failed role-aware selector.

Earlier proof packages and the concurrently developed visual companion remain
unchanged. The two reviewer programs import no production implementation.
Their first outputs preceded the coordinator's implementation, but the
coordinator then read them: the comparison is separately structured and
parallel, not blind. External mathematical assessment remains open.
