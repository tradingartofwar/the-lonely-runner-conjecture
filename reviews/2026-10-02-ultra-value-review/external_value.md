# External value scout and bounded SymPy demonstration

October 2, 2026. Local source baseline
`29e54d32e2ff5349bdb0c3db56fab753a0e44c94`. AI-assisted targeted review;
no external contacts, operational deployment, large benchmark, spending or
solver-defect search. Status: **OBSERVED** for the bounded artifact below;
**OPEN** for external adoption, superiority and operational benefit.

The strongest accessible destination is SymPy's documented periodic inequality
workflow. Its ordinary inequality API returns a principal-period set. A caller
asking for all solutions in a wider or shifted finite horizon has a real
translation obligation: retain the period, restore each atom's shifts, then
intersect at the same time. That is a named existing tool and documented scope
boundary, rather than a made-up device application. No outside user has asked us
for this adapter, and its existence does not establish demand.

## Ranked candidates

| Rank | Existing problem/tool | Small reproducible artifact | Value, success and stop rule |
| --- | --- | --- | --- |
| 1 | SymPy 1.14.0: complete finite-horizon solutions from principal-period trig inequality results | Completed ten-case adapter in `examples/compatibility-conformance/sympy_periodic/`; preserves periods, offsets, open/closed ends, isolated points and common-time intersection | Bounded correctness utility: ten complete-set agreements plus exact original-expression checks. An advantage would require a real downstream error avoided or lower cost versus ordinary correct period expansion; neither was demonstrated. Stop at this integration example after a clean pass. |
| 2 | TSNKit 0.3.0: validate serialized time-aware-shaper schedules against input traffic and native simulator | Conditional one-instance format/conformance checker covering one supplied small schedule, physical transmission duration, route timing, gate windows, deadlines and declared jitter semantics | A concrete benefit would be an independently confirmed mismatch in an actual supported translation, or useful coverage missing from the native checker. Agreement alone is bounded conformance. Do not run the full published benchmark; stop if endpoint, queue or jitter semantics cannot be pinned. **UNRUN.** |
| 3 | JSON Schema Draft 2020-12 / official Test Suite: retain same-instance constraints, numeric endpoints and dialect identity | Reuse the official numeric and `allOf` tests when a real schema-to-constraint adapter is proposed; carry source schema/dialect alongside results | Useful only if it catches an actual adapter error or supplies a needed unsupported-query certificate. The official suite already serves conformance; no need to create a competing CC validator. Without a concrete adapter gap, stop at the mapping. **UNRUN.** |

The third candidate is deliberately outside periodic clocks. The transferred
content is same-instance conjunction, equality and source-version scope; clock
lifts do not apply. The first two candidates should not be multiplied into claims
about broad real-world impact.

## What was actually built and observed

The SymPy package contains a frozen ten-case specification, executable adapter,
independent rational event oracle, deterministic JSON output, and reproduction
records. The input is a structured single sine/cosine atom, not an expression
parser: `f(pi*(a*t+b)) op c`, positive rational `a`, rational `b`, one of four
inequality relations, and threshold in `{-1,-1/2,0,1/2,1}`. The horizon and all
endpoint flags are explicit. Rational inputs and enumeration have finite size
limits; floats and unsupported symbolic results are not infeasibility verdicts.

All ten declared development cases passed complete-set comparison. All 120 exact
checks at phase events and intervening cell midpoints agreed with original trig
substitution. These checks cover entire event cells by the fragment's fixed sign
between consecutive boundary events; they are not a numerical time grid. The
examples were chosen from known hazards and one documentation example, so this
is an exposed development corpus, not fresh or representative workload evidence.

The frozen first source passed and reproduced byte-for-byte. AI static review then
found an unexecuted-path protocol discrepancy: the runner recorded unsupported
or error outcomes but continued. The final runner stops there and requires all
ten requested cases for success. Initial records and the correction remain in
`INITIAL_REPORT.json`, `INITIAL_REPRODUCTION.json`, `DEVELOPMENT_LOG.md`, and
`FREEZE.json`; `INITIAL_DEMO.py` preserves the exact frozen source. The final report
pins its own source and a separate AI reviewer reproduced it byte-for-byte. No case, mathematical adapter
or oracle was tuned after the first run. The timeout is imposed by the documented
external command. Error branches are not newly validated by the ten positive
execution records.

For `cos(pi*t)<1/2` on `[2,4)`, the complete answer is `(7/3,11/3)`; the
principal-only result has no contact with that horizon. For the opposite weak
sine inequalities on `[0,2]`, the answer is exactly `{0,1,2}`. These demonstrate
changed output scope and equality retention without importing a runner-count
theorem. The principal-only diagnostic is intentionally narrower, **not a fair
baseline or a SymPy failure**. The candidate is itself ordinary correct period
expansion and set intersection; CC supplies no distinct algorithmic advantage.

## Transfer contract and what does not transfer

| Field | Record |
| --- | --- |
| Origin | Archived same-point/clock-lift diagnostics, September 30's conformance proposal, and October 2's complete interval/isolated-point recovery. |
| Supported destination question | Complete set of common solutions in one bounded horizon for the stated rational trig fragment. This is stronger than one witness, but far narrower than generic symbolic inequality solving. |
| Mapping | Physical-time alternatives become period translates; boundary points become exact finite-set elements; one shared time is retained during intersection; source identity becomes dependency, protocol, case and code hashes. |
| Retained | Original atoms, period, phase, horizon, endpoint flags, every relevant lift, complete solution set and independent checking route. |
| Omitted | General expressions, irrational periods, approximate inputs, optimization, resource scheduling, drift, operational robustness and arbitrary schema translation. |
| Inherited fact | Basic periodicity and standard set-intersection semantics. No LRC coverage theorem, compact-menu completeness, finite-tail argument or runtime advantage is inherited. |
| New obligations | Correct per-atom period/source, exact seed domain, complete finite shift range, exact clipping and common-variable composition. All require checks independent of a claim that the source bytes were hashed. |
| Failure | Wrong complete set, missed isolated point, invalid original-expression witness, unsupported result called empty, or a stale/mismatched source accepted as the tested implementation. |
| Result boundary | Ten-case correctness evidence and executable explanation. No external defect, adopter, new general method, blind review, formal proof certificate or measured economic/operational advantage. |

## Why the TSN lead is deferred

TSNKit publishes stream sizes, periods, deadlines and delay-variance requirements;
links have bandwidth, processing and propagation times. Its output includes gate
start/end/cycle records, routes, offsets and queue assignments [P3]. Its native
simulator checks schedule behavior and reports losses, deadline and jitter
violations; its documented delay definition differs by a processing term from
an algorithm output [P4]. This is an authentic model-translation setting.

It is not legitimate to replace these obligations with an instantaneous common
phase witness. Positive frame transmission duration must fit the relevant gates,
route causality and competing traffic matter, and the documented jitter field is
an end-to-end delay-variance requirement, not automatically a bound on clock
uncertainty. A future one-instance checker must read the pinned code for endpoint
and queue semantics before making a result. No such implementation or input has
been tested here. The project's benchmark documentation itself warns that broad
reproduction is large [P5]; it supplies no reason to launch one for this review.

## Primary sources, versions and reading limits

All sources below were consulted October 2, 2026. This was a targeted scouting
pass, not an exhaustive novelty search or a current bug audit.

| ID | Source/version and URL | Inspected and limit |
| --- | --- | --- |
| P1 | SymPy **1.14.0**, guide footer updated April 27, 2025: https://docs.sympy.org/latest/guides/solving/reduce-inequalities-algebraically.html#not-all-results-are-returned-for-periodic-functions | Periodic result restriction, integer-shift instruction, examples and adjacent limitations. The `latest` URL is mutable; tested dependency version and source hashes are fixed in the artifact. |
| P2 | SymPy **1.14.0** API: https://docs.sympy.org/latest/modules/solvers/inequalities.html ; installed `sympy/solvers/inequalities.py` and `sympy/calculus/util.py` | API contract, periodic/domain branch and `periodicity` contract read locally. Source inspected around the solver's numerical fallback; not a full SymPy correctness audit. The adapter checks the returned period against `2/a`; a general returned period is not assumed fundamental or formally certified. |
| P3 | TSNKit **0.3.0** docs: https://tsnkit.readthedocs.io/en/stable/dataprep.html | Input/output field definitions read. A doc line describes both start and end as opening times, so code inspection is needed before choosing endpoint semantics. No package, schedule or native algorithm executed. |
| P4 | TSNKit **0.3.0** docs: https://tsnkit.readthedocs.io/en/stable/simulation.html | Simulator purpose, timing/jitter outputs, native delay-definition caveat, supported-model limitations. No simulator source audit or packet validation. |
| P5 | TSNKit **0.3.0** docs: https://tsnkit.readthedocs.io/en/stable/benchmark.html | Supplied benchmark/debug pathways and resource warning. No dataset fetched; no full workload or outcome claims. |
| P6 | JSON Schema validation **Draft 2020-12**, `draft-bhutton-json-schema-validation-01`, June 16, 2022: https://json-schema.org/draft/2020-12/json-schema-validation | Sections 4.2 and 6.2: unbounded decimal precision, multipleOf and strict/inclusive numeric limits. No full validator or dialect audit. |
| P7 | Official JSON Schema Test Suite, mutable `main`: https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/main/README.md ; https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/main/tests/draft2020-12/allOf.json | README purpose/format/coverage and an allOf-plus-anyOf/oneOf example. No immutable commit pinned or suite run; any later trial must pin its own exact suite revision. |

Repository coverage: AGENTS, README, CLAIM_STATUS and CONTRIBUTING read; HANDOFF
current-state excerpts read; September 30 assessment and computation-transfer
report read in scoped excerpts (some large combined outputs truncated, then
relevant sections recovered); October 2 orbit-interval note read in full. Older
archived mathematical computations were not reexecuted by this scout. The actual
new execution is only the ten-case SymPy package and its bounded reproductions.

Recommendation: preserve this small integration example and use established
methods directly. An additional external test becomes justified when a named
downstream translator or workload requires it; the current clean pass alone does
not justify expanding the project.
