# Coefficient checker implementation and validation

September 29, 2026. See
[CC_COEFFICIENT_CHECKER_2026_09_29.md](../../notes/CC_COEFFICIENT_CHECKER_2026_09_29.md)
for usage, mathematical scope and branch reasoning.

The standard-library runtime is
[lonely_runner/cc_coefficients.py](../../lonely_runner/cc_coefficients.py).
It returns ACCEPTED with a fixed-selector guarantee or REJECTED with a
physically checked failed p,q. Invalid API inputs raise ValueError; the JSON
CLI reports INVALID_INPUT with exit 2. The runtime does not read this review
package. The universal classification remains an internally reviewed proof
candidate, not formal certification or a new existence result.

```sh
python3 -m lonely_runner.cc_coefficients 6 2 --p 4 --q 6
python3 -m lonely_runner.cc_coefficients 5 2
python3 -m lonely_runner.cc_coefficients 68 27
```

Rejections require six safe core phases, seventh distance strictly below
1/8 and eight distinct total speeds. They concern this selector, not absence
of other lonely times. Acceptance retains the distinct-speed conditions
and identifies four repeated core rows with empty distinct-speed domains.
Requested-pair behavior remains separate from the global coefficient decision.

| File | Purpose |
| --- | --- |
| PROTOCOL.md | Frozen interface, rejection precedence and controls |
| INPUTS.json | Pinned mathematical and package inputs |
| ../../tests/test_cc_coefficients.py | Five test methods covering the frozen scope |
| validate.py / validation.json | Exact runtime outputs, CLI results and provenance |
| audit.py / audit.json / audit.md | Separate interval/congruence reconstruction |
| contract_review.md | Pre-code totality reasoning and static runtime review |
| EXECUTION_RECORD.md | Execution order, corrections and scope |
| reproduce.py / REPRODUCTION.json | Exact reproduction of both output files |
| MANIFEST.json | Hashes of this package, runtime, tests and main note |

From the repository root, with Python 3 and without `-O` for the harness:

```sh
python3 reviews/2026-09-29-cc-coefficient-checker/reproduce.py
```

The harness separately runs all nine CLI controls under normal and optimized
Python. Production checks use explicit errors rather than assertions.
Validation covers 480 coefficient cases (84 accepted, 396 rejected), 62
direct physical cases, 15 invalid API cases and 18 CLI records. The 480 are
216 old representatives, 216 prescribed shifts and 48 analytic large-slope
controls, not 480 newly classified families. All 54 archived physical outputs
reproduce, and all five rejection branches occur.

The arithmetic audit agrees on 27,401 fields and retains 40 intended changes
to baseline failure directions due to the new precedence. Both output files
reproduce byte-for-byte. validation.json uses compact JSON to retain every
exact record without indentation overhead; the note and reports supply the
readable account. No generic untrusted-certificate validator is claimed.

The existing general checker and its tests are unchanged; no broader suite
result is claimed. The arithmetic reviewer imports no production code.
Findings are shared, with no blind, human or formal review claim. No changed
discovery rule, geometry or transfer is run in this package.
