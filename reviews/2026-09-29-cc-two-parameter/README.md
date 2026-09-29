# Two-parameter witness package

Main derivation: [CC_TWO_PARAMETER_WITNESS_2026_09_29.md](../../notes/CC_TWO_PARAMETER_WITNESS_2026_09_29.md).
Status: HYPOTHESIS / complete proof candidate with internal AI team review.
One selected stationary-reference witness for every positive integer p!=q in
the fixed seven-form family; no optimum, all-reference or novelty claim.

## Reproduce

Python 3 standard library, exact fractions. From the repository root:

```sh
python3 reviews/2026-09-29-cc-two-parameter/reproduce.py
```

This runs the coordinator selector and the three separately authored review
programs, verifies all four output files byte-for-byte, compares the 18 declared
controls across implementations, and writes `REPRODUCTION.json`. The selector
alone writes JSON to stdout; the three review programs write their corresponding
JSON files and print summaries. No optimizer or broad parameter scan is used.

## Contents

| File | Role |
| --- | --- |
| PROTOCOL.md | Scope, frozen controls, intended falsifiers and work split |
| CORRECTIONS.md | Failed proposed negative fixture and analytic replacement |
| FROZEN_INPUTS.json | Pinned source files and hashes |
| selector.py / selector.json | Coordinator implementation and fixed controls |
| orbit_review.md / orbit_checks.py / orbit_checks.json | Primitive/nonprimitive orbit and physical recovery |
| coverage_review.md / coverage_checks.py / coverage_checks.json | Affine safety, infinite region and complete finite complement |
| physical_review.md / physical_checks.py / physical_checks.json | Direct physical checks and separate congruence recovery |
| reproduce.py / REPRODUCTION.json | Deterministic reproduction and cross-implementation comparison |
| MANIFEST.json | Package and main-note content hashes, excluding itself |

The infinite result is supported by the explicit proof candidate: width covers
Q+2P>=8, eight primitive pairs exhaust the complement, and the two misses have
closed P1 contacts. Finite agreement alone is not the proof. The (1,1) control
is a labelled repeated-speed auxiliary, leaving 17 distinct-speed cases.

The existing frozen A/B discovery algorithms and outputs remain intact. This
package extends the analytic coverage of their two existing segments and adds
gcd/Bezout recovery. The constant segment-test count does not make the complete
arithmetic algorithm constant-cost. Separate AI review is not external, human
or formal certification; literature/novelty assessment remains OPEN.
