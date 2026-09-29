# Compatibility Calculus: a coefficient decision with a physical certificate

September 29, 2026. Mathematical source head:
`57997d4220226b44b9a89d8d8139926f15cca90c`.

**Result:** the [reusable checker](../lonely_runner/cc_coefficients.py) now
implements the existing exact coefficient classification. It returns either
the fixed selector's witness guarantee or an explicit positive p≠q where
that selector fails. Every rejection includes the physical time, seven speeds,
phases and laps, and verifies that the speeds, together with reference 0,
are distinct.

This is an implementation of the [previous proof candidate](CC_SELECTOR_SUPPORT_2026_09_29.md),
not a new coefficient classification or new Lonely Runner existence result.
The universal argument remains **HYPOTHESIS / internally reviewed proof
candidate**. Material AI implementation and separate AI reviews are disclosed.
The software is neither a formal prover nor a generic untrusted-certificate
validator. Existing literature attribution and originality limits are unchanged.

## 1. Using the checker

From the repository root, with Python 3 and its standard library:

```sh
python3 -m lonely_runner.cc_coefficients 6 2
python3 -m lonely_runner.cc_coefficients 5 2
python3 -m lonely_runner.cc_coefficients 6 2 --p 4 --q 6
python3 -m lonely_runner.cc_coefficients 68 27
```

Each command prints JSON. The Python API is:

```python
from lonely_runner.cc_coefficients import check_coefficients, evaluate_selector

decision = check_coefficients(6, 2)
physical = evaluate_selector(6, 2, 4, 6)
```

The module needs no archived proof-output file at runtime. Python integers
and rational calculations remain exact; rational output fields are strings.
JSON consumers must also preserve large integer fields exactly rather than
convert them through binary floating point.

| Outcome | Meaning | Supplied evidence |
| --- | --- | --- |
| ACCEPTED | This fixed first-integer L/C construction is uniformly safe for the positive integer coefficient row | Shared leader lap and band, safe C phase, recovery recipe, proof source and distinct-speed domain |
| REJECTED | The same construction fails on a concrete input | p,q, selected point/time, actual speeds, exact phases/laps, strict seventh failure and checked distinctness |
| INVALID_INPUT, CLI only | A coefficient or optional physical parameter is invalid | Input error; no mathematical conclusion |

The Python API raises `ValueError` for invalid input. It requires positive
Python integers and rejects booleans, floats, strings and implicit coercions.
The CLI accepts decimal integer text and requires `--p` and `--q` together.
Valid mathematical outcomes, including REJECTED, exit 0; invalid input exits 2.
Internal arithmetic inconsistency raises an error and never becomes a
REJECTED coefficient verdict. Production checks remain active under `-O`.

Optional p,q evaluates that requested physical configuration independently
of the global coefficient verdict. A rejected row can still be safe at that
particular pair. For example row (5,2) is rejected through (p,q)=(2,3), but
the requested pair (1,3) has a safe selected time. Both facts remain in the
same output under separate fields.

## 2. What acceptance preserves

The fixed leader is L: y=7/8−2x, 1/4≤x≤3/8, with fallback C=(1/8,1/4).
For u=2A+3B, v=3A+B and w=A+2B, acceptance uses exactly the old condition

\[
\exists m\in\mathbb Z:\quad
8m+1\le\min(u,v)\le\max(u,v)\le8m+7,
\qquad w\not\equiv0\pmod8.
\]

The returned record retains the common leader lap m and C's separately
recomputed lap. It does not combine endpoint residues from different laps.
The previous coverage and actual-selector necessity proof supplies uniformity;
the output identifies that proof by its commit and note.

For p,q>0, the physical family is

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,Ap+Bq).
\]

Eight distinct speeds require p≠q and
(A−a)p+(B−b)q≠0 for (a,b)=(1,1),(2,1),(3,1),(3,2). These conditions are
serialized explicitly. Rows (1,1),(2,1),(3,1),(3,2) receive ACCEPTED for
labelled safety but carry an **empty distinct-speed domain** flag: they
duplicate a core speed identically. A requested repeated-speed case remains
labelled, even when its phases are safe.

The actual clock still uses d=gcd(p,q), primitive P,Q, and Qx−Py=h in Z.
For rP+sQ=1, N=floor(rx+sy), τ=rx+sy−N and t=τ/d. Each row (a,b) with
torus lap m has physical lap m+(−as+br)h−(aP+bQ)N. The implementation
checks these quantities by direct multiplication with the actual speeds.
Reflection is the archived unit-period choice 1−t, with zero-phase handling
preserved for rejected cases. Every accepted selected minimum is exactly 1/8.

## 3. A total rejection procedure

Let δ=A−2B, D=|δ| and a=u mod8. After the acceptance test, the checker uses
the following fixed precedence from the [protocol](../reviews/2026-09-29-cc-coefficient-checker/PROTOCOL.md):

| Reason | Failed input or construction |
| --- | --- |
| FALLBACK_COLLISION | w≡0 mod8; choose (p,q)=(1,2), time 1/8 |
| LEADER_START_COLLISION | a=0; choose (2,3), time 1/8 |
| OUTWARD_BOUNDARY | δ>0,a=7 or δ<0,a=1; use j=max(2,floor(7D/8)+1), then (1,4j−2) |
| LARGE_SLOPE | D≥14; let c=7−a for δ>0, or c=a−1 for δ<0; choose j=floor(7D/[4(c+2)])+1, then (1,4j−2) |
| BOUNDED_DIRECTION | D≤13 after preceding exclusions; take the first failure in the preserved 11-direction list |

The outward construction has drift 0<7D/(32j)<1/4 into an open unsafe band.
For the large-slope branch, 1≤c≤6 and the proof gives the strict interval

\[
\frac{7D}{4(c+2)}<j<\frac{7D}{4c}.
\]

Its length is at least 7D/96>1, so the rounded integer exists inside it.
The program retains and checks that interval. The remaining branch uses
the 11 directions extracted from the complete earlier 216-cell reduction,
in increasing M=Q+2P and then P order. Its completeness follows from that
proof, not from an assumption that a fixed finite menu works for arbitrary
slopes. No research scan is launched by the runtime.

Every selected rejection is physically rechecked before return: all six core
phases are safe, the seventh distance is strictly less than 1/8, and there
are eight distinct speeds. A missing bounded certificate or failed identity
raises `ArithmeticError`. There are at most 11 bounded contact tests and one
physical recovery per coefficient decision; optional requested-pair evaluation
adds another recovery. Integer bit cost and gcd/Bezout arithmetic are variable;
this is not a constant-time complexity claim.

Concrete outputs from the frozen validation are:

| Row (A,B) | Coefficient result | Physical pair | Time | Seventh distance |
| --- | --- | --- | --- | --- |
| (6,2) | ACCEPTED | requested (4,6) | 1/16 | 1/4; overall minimum 1/8 |
| (5,2) | REJECTED, leader-start collision | (2,3) | 1/8 | 0 |
| (68,27) | REJECTED, large slope δ=14 | (1,14) | 39/128 | 7/64 |
| (44,29) | REJECTED, large slope δ=−14 | (1,14) | 39/128 | 7/64 |

The two large-slope examples have opposite seventh phases, 57/64 and 7/64,
and the same failed distance. Their chosen integer j=4 lies strictly between
49/16 and 49/12. All these are failures of the designated selector only.

## 4. Frozen validation and separate reviews

The [review package](../reviews/2026-09-29-cc-coefficient-checker/README.md)
retains protocol, exact runtime records, source identities, tests and reviews.
Validation covers:

- 216 old coefficient representatives, all matching the archived 42-class
  decision, and the same 216 shifted by (16K,8K), K=10^20. Decisions,
  rejection directions and fractional phases persist; integer laps change.
- 48 analytically chosen large-slope rows: both signs of 14, 15 and
  10^40+14 across eight B residues. All are rejected with exact physical evidence.
- 54 archived progression configurations reproduced, plus eight named
  repeated-speed, equality and old-failure controls.
- 15 invalid API cases and nine CLI cases in both normal and optimized Python.

The total is **480 coefficient decisions: 84 accepted and 396 rejected**.
There are 62 direct physical records and 18 CLI records. These are bounded
implementation checks of an existing proof, not new family-discovery evidence.
The first complete coordinator run passed without an implementation correction.

The changed rejection precedence deliberately changes 40 of the 174 baseline
failure directions relative to the old first-small-direction output. Verdicts
remain identical. This is a change in certificate identity, not in which
coefficient rows are accepted.

The arithmetic reviewer derives shared-lap acceptance independently and
recovers the clock through coordinate congruences, then multiplies physical
speeds directly. It imports no production code. The contract reviewer derives
branch totality before reading the module, then audits runtime semantics and
the saved tests. Findings are shared; no blind-replication claim is made.
The serialized arithmetic audit passes 27,401 field comparisons. Its first
CLI scope check required aligning two unspecified argument-placement details
with the actual declared commands; no production behavior, trial or protocol
changed. The reviewer preserves that harness correction.

Run the complete frozen reproduction from the repository root:

```sh
python3 reviews/2026-09-29-cc-coefficient-checker/reproduce.py
```

The reusable unit tests can also run alone:

```sh
python3 -m unittest discover -s tests -p test_cc_coefficients.py -v
```

Only the new frozen checker suite is required here. The existing general
Lonely Runner checker and its tests are unchanged; no broader suite result
is claimed. The proof-source commit identifies the mathematical result;
the new manifest's module hash identifies the implementation actually checked.

## 5. CC checkpoint and next experiment

The decision now carries the information needed for its next use. Acceptance
retains domain restrictions, common laps and physical recovery. Rejection
retains the exact failed configuration and distinguishes failure of the rule's
universal guarantee from success or failure at one requested pair. Invalid input and
internal computation errors carry no mathematical verdict. Large-integer
period shifts test that equal phases do not erase changed lap information.

This checker is an adequate representation for coefficient acceptance and a
specific selector counterexample. Its failure does not establish exhaustion
of every contact, every segment, or the fuller parent geometry. Those are
different next operations and require their corresponding records.

**Next proposed:** freeze a compiler transfer for row (3,8), the first rejected
representative in the prior increasing-(δ,B mod8) table. It is a known failure
of the compact fixed selector at (p,q)=(1,4), so this is an informed choice,
not a blind trial. Apply the preserved discovery rule and failure diagnostics
to ask whether another menu repairs the failure. That transfer, changed
geometry and any new physical controls have not been executed here.
