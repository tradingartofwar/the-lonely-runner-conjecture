# Finite-horizon periodic inequalities with SymPy

This small adapter completes a documented SymPy workflow: restore all required
period shifts of each trig inequality before intersecting them at one common
time. It returns the entire bounded solution set, including isolated equality
points. It is ordinary exact period expansion and set intersection; no new solver
or CC-specific advantage is claimed.

**Observed:** all ten exposed development cases agree with a separately structured
`Fraction` phase-event oracle, and all 120 exact original-expression substitutions
agree. The cases include mixed periods, offsets, negative time, strict endpoints,
closed horizon ends, and singleton-only results. The JSON reports retain original
inputs, complete sets, per-atom principal seeds and lift ranges, and source hashes.

## Run

Use Python 3 with the pinned dependencies in `requirements.txt`. From the repository
root, using the installed dependency directory used for this review:

```sh
PYTHONPATH=/tmp/lr-ultra-deps timeout 120 python examples/compatibility-conformance/sympy_periodic/demo.py
```

For a fresh environment, install `requirements.txt` into an isolated environment
and run the same script with that interpreter. The external `timeout 120` wrapper
enforces the two-minute budget. `--output PATH` writes a comparison report without
replacing `report.json`. The script exits nonzero on failed or unsupported work.

Read `PROTOCOL.md` for the supported rational trig fragment and size limits.
Floating-point input, arbitrary trig expressions, operational scheduling and
general symbolic completeness are outside this package. A period is required to
equal `2/frequency`, justified for the declared single sine/cosine atom. The
general-purpose `periodicity` API alone is not being treated as a proof oracle.

## Two examples

All displayed times use the exact normalized variable `t=x/pi`.

| Question | Complete answer |
| --- | --- |
| `cos(pi*t)<1/2`, `2<=t<4` | `(7/3,11/3)` |
| `sin(pi*t)>=0` and `sin(pi*t)<=0`, `0<=t<=2` | `{0,1,2}` |

Intersecting the first question's unshifted principal result with `[2,4)` gives
the empty set. That uses a narrower result for a broader query: it is **not a
SymPy defect or a fair comparator**. The ordinary correctly expanded method is
the adapter itself. The lesson is to carry the API's scope, period, endpoint
conventions and source identity into the next operation.

## Evidence and limits

`FREEZE.json` binds the initial protocol, cases and code. `INITIAL_REPORT.json`
and `INITIAL_REPRODUCTION.json` preserve the first successful run and replay.
`INITIAL_DEMO.py` preserves the exact initial code bytes and matches the frozen
hash; to replay that version, restore it as `demo.py` in a temporary package copy
so its provenance filenames still refer to the code actually being executed.
`DEVELOPMENT_LOG.md` records the later unexecuted error-control correction;
`report.json` binds the final source, and `REPRODUCTION.json` records its replay.
No case or successful-case algorithm changed after the initial freeze.

The event oracle works directly from rational phase boundaries and does not use
SymPy's inequality solution or set operations. Original trig substitution is a
separate check but shares SymPy with the adapter. SymPy's general solver contains
numerical fallback paths; this package's bounded evidence comes from agreement
with the independent rational event construction, not from a claim that every
SymPy internal operation is formally exact. All checks are AI-authored; separate
AI review is not external or formal certification.

No external user request, deployment, defect, speed advantage, adoption, or
learning benefit was measured. The immediate product is a reproducible example
of a documented integration obligation. Stop at that scope unless a downstream
tool supplies a concrete additional need.

## Source

SymPy 1.14.0 documentation, updated April 27, 2025 and consulted October 2, 2026:
[periodic inequality limitation](https://docs.sympy.org/latest/guides/solving/reduce-inequalities-algebraically.html#not-all-results-are-returned-for-periodic-functions)
and [inequality API](https://docs.sympy.org/latest/modules/solvers/inequalities.html).
The installed 1.14.0 inequality implementation's period/domain branch and the
`periodicity` API contract were also inspected; their exact hashes appear in the
report. Dependencies are SymPy 1.14.0 and mpmath 1.3.0.
