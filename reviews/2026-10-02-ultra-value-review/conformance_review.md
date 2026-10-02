# Independent internal audit of the five conformance examples

October 2, 2026 UTC. Delegated AI review of the root-built `examples/compatibility-conformance/{check.py,fixtures.json,results.json}`. A separately tasked AI reader checked source extraction. This is an internal code/arithmetic review with independently structured checks, not independent human certification or a security audit. The reviewer did not edit the example package or source archives.

**Final verdict: PASS for the five explicitly declared development diagnostics, including the two labeled adaptations.** All corrected reference outcomes and intentionally faulty outcomes reproduce. All eleven final input-corruption controls reject, in normal and optimized Python. Source-bound inputs, archived numerical results, exact arithmetic, and declared query scopes agree. No arithmetic defect remains identified within this scope.

## Versions and executed evidence

Source baseline: `29e54d32e2ff5349bdb0c3db56fab753a0e44c94`.

| Reviewed artifact | Final SHA-256 |
| --- | --- |
| `examples/compatibility-conformance/check.py` | `3b64b495dc323cab7041bfe1a5c4987f6cc0360b3f1bbef0ea2600ea172eae5e` |
| `examples/compatibility-conformance/fixtures.json` | `d6b94135aa6e040f96659998bcae394143be085096cce48bef8dd07e3910f0a7` |
| `examples/compatibility-conformance/results.json` | `47d827c46bd98e48659cebabca8032bfe5db76afe96418489b781555a0989667` |

The final saved result, fresh normal-Python result, and fresh `python -O` result are byte-identical. The reviewer also ran the complete mutation/arithmetic audit under normal and optimized Python; those two audit outputs are byte-identical. An AST inspection found zero `assert` nodes in the example checker. Its `require` checks remain active with optimization.

The three source files' bytes equal both their fixture SHA-256 pins and their `git show <baseline>:<path>` contents. Thus the named commit association was checked independently, rather than inferred from a matching label. The package's runtime trusts its checked code and fixture pins; it is not claimed secure against coordinated malicious edits to code, sources, and pins.

## Query and source preservation

| Diagnostic | Exact source inspected | Preserved question or declared adaptation | Outcome |
| --- | --- | --- | --- |
| `same_point` | `discovery.json → diagnostics.false_marginal` | Original segment with fixed `z=7/8`; rates `[1,2,6]`, both endpoints and both relations match | Separate relation successes occur at segment parameters `0` and `3/4`, with no shared parameter. Direct physical time: UNSAT; mutant: SAT |
| `complete_relations` | `diagnostics.unsaturated_false_point.raw_hit.point`, raw and saturated relations | Exact archived false-point membership diagnostic, specializing its containing edge. It is not the whole-edge query; final adaptation field says so | Raw relation values `[-1,0]`, complete values `[-1,1/2]`. Direct physical time: UNSAT; mutant: SAT |
| `clock_lifts` | `diagnostics.lost_clock_lift`, its recovered point/time, and original sheet description | Exact recovered-phase-point query, narrower than the original safe-band recovery request. Final adaptation field explicitly states this | Canonical `3/16` gives third phase `15/16`; recovered `11/16` gives `7/16`. Reference: SAT; first-clock mutant: UNSAT |
| `isolated_points` | Orbit `RESULTS.cases[3]`, core `1,4`, primary component `1`; `VERIFICATION.compression_failure_unions[0]` | Original closed `1/8` phase-band existence question on the fixed input, with complete-set output additionally checked | Exact set `{1/8,3/8,5/8,7/8}`. Reference: SAT; positive-width-only mutant: UNSAT |
| `widest_only` | Orbit `RESULTS.cases[7]`, core `1,6`, primary component `2`; `VERIFICATION.compression_failure_unions[1]` | Original fixed-input closed-band existence question; archived selected primary interval is now explicitly bound | All ten full-set components agree. Widest interval `[17/56,127/408]` fails the new band; `3/16` survives elsewhere. Reference: SAT; widest-only mutant: UNSAT |

The two nine-rate lists equal the archived family `[p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r]`. Both have threshold `1/8`, and equality is safe. The reference event decomposition includes `t=1` in its finite boundary set while the displayed question uses `[0,1)`; this makes no difference for these positive thresholds because all phases at `t=1` are zero and therefore unsafe.

It would still be incorrect to describe all five as unchanged original full-source tasks. The two point adaptations are mathematically valid diagnostic extractions and now transparently labeled. The clock adaptation preserves the particular archived failure mechanism: on the original sheet, the first lift's third phase is outside the safe band and the recovered lift's phase lies inside it. The narrower point result does not establish equivalence for arbitrary sheet queries.

## Reference independence and additional arithmetic checks

The new reference path imports only standard-library modules and does not import archived relation, lattice, source-selection, or recovery code. For a phase point it exhausts integer laps of the first coordinate and evaluates every phase directly. For the fixed-z segment it exhausts third-coordinate laps, then checks geometric membership. Its computation of shared relation parameters is a separate comparison, not the reference's time-recovery method.

For closed bands, the new reference partitions physical time at every exact threshold event, checks endpoints and intervening cells, and merges the closed safe pieces. The reviewer compared both resulting complete safe sets against the older verifier's successive closed-band intersections. This checks the same result by a different decomposition. Both comparisons agree exactly, including all isolated points. The reviewer also enumerated the two phase-point cases using the **third** coordinate rather than the reference's first coordinate: no time reaches the unsaturated false point, and exactly `11/16` reaches the clock-lift point.

The two false-positive and three false-negative counts describe deliberately faulty rules. They are not defects found in an external solver, not a comparison with mature conventional implementations, and not held-out validation of CC. The existing source cases are development evidence. This package's useful output is a compact, inspectable regression/teaching artifact with pinned recovery routes.

## Initial findings, fixes, and final corruption controls

The first reviewed checker (`ee560688c993617c9ecd6f59f2e9e5a22ddcb4165435bf93d4cc6257874509c2`) produced correct arithmetic but only checked source-file hashes. It did not resolve each source selector or bind fixture fields to source rows. A wrong selector, wrong claimed source commit, and unknown query kind passed. The primary-interval check established that the interval was a core component, not that it was the archived widest/primary selection; the separate source reader demonstrated that a different core singleton could preserve the claimed failure. The two narrowed point queries also lacked explicit adaptation labels.

Those findings were sent promptly to the package author. The author added `validate_source_links`, fixed-schema/baseline/case-identity/source-pin checks, exact source-field extraction including `core.primary`, and the adaptation labels. These are transparent development-audit fixes, not changes to a frozen experiment. Initial outputs remain in the `conformance_review_initial_*` files; no initial failure was rewritten as a clean first pass.

The final checker rejects every following alteration before emitting a successful package result:

1. Wrong expected source digest.
2. Wrong expected recovered clock time.
3. Removing an isolated point from the expected full set.
4. Nonexistent source selector.
5. Wrong claimed source commit.
6. Changed same-point rates without a matching source update.
7. Unknown query kind.
8. Replacing the widest primary interval with the different safe core singleton `[11/24,11/24]`.
9. Unknown mutant label.
10. Missing source pin.
11. Duplicate case identity.

These checks exercise the public package `run` path. Its internal arithmetic helpers are not separately advertised as a generic validated-input API. Narrative question/title/lesson prose remains authored text, not a formally checked natural-language specification; the inspected prose agrees with the explicit numerical/query contract. The small corruption set is sufficient for the reported repaired risks, not exhaustive parser fuzzing.

## Reproduction and coverage

From the repository root:

```bash
python examples/compatibility-conformance/check.py --out reviews/2026-10-02-ultra-value-review/conformance_review_normal.json
python -O examples/compatibility-conformance/check.py --out reviews/2026-10-02-ultra-value-review/conformance_review_optimized.json
python reviews/2026-10-02-ultra-value-review/conformance_review_checks.py
python -O reviews/2026-10-02-ultra-value-review/conformance_review_checks.py
```

`conformance_review_checks.py` uses temporary fixture copies and never changes checked-in example or source files. It checks pinned Git bytes, four additional arithmetic comparisons, and eleven input corruptions. `conformance_review_checks.json` records the final checker/fixture hashes and every outcome. `conformance_review_reproduction.json` records the fresh/saved output equality, optimized audit equality, and absence of assert statements. The normal/optimized outputs and initial audit outputs are preserved separately.

Direct coverage: the complete initial and final checker, complete fixtures/results, selected source diagnostic/core/verification rows, source hashes and pinned Git blobs, and the older physical-time helper implementations actually used for the two complete-set comparisons. The original entire mathematical studies were not rerun, and their universal proof candidates were not re-reviewed. No participant/learning test, external adapter integration, benchmark, novelty claim, or outside defect follows from this audit.
