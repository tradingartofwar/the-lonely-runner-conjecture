# Value review: what is useful, what is demonstrated, and when to stop

October 2, 2026. Research baseline: `29e54d32e2ff5349bdb0c3db56fab753a0e44c94`. Separately tasked internal AI value reviewer. The team shares the repository, source material and findings; this is not blind review, external adoption evidence or independent human certification. This report evaluates value claims and experimental choices rather than rechecking every arithmetic result.

## Verdict

The work has produced useful exact examples, inspectable implementations and narrow mathematical proof candidates. It has also demonstrated a valuable research behavior: preserving failed compression rules and reporting two comparisons that do not favor CC. These are legitimate accomplishments even if the underlying principles are known.

The evidence does **not** yet show that CC improves an external workflow, beats a competent existing solver, establishes a new general theory, or advances the full Lonely Runner Conjecture. Another attractive internal demonstration cannot by itself close those gaps. The strongest near-term deliverable is a small, neutral conformance and replication kit, accompanied by one precisely scoped mathematical result. The next marginal unit of work should make an outside person able to check or use those assets, rather than increase the count of internally generated successes.

| Value question | Evidence available | What would justify a stronger claim |
| --- | --- | --- |
| Is there a useful artifact? | Exact fixtures with distinct failure mechanisms; rational physical witnesses; complete interval/point outputs; deterministic reproduction commands. | A compact package that runs from the declared environment, explains its inputs and checks the original question. This is an attainable engineering claim without novelty. |
| Has somebody outside the project benefited? | No external use or measured operational benefit was established in the sources reviewed. An existing-tool adapter is being built in this review. | An actual consumer uses the package to find or prevent a concrete error, finish a task, reduce maintenance effort, or learn a transferable distinction. Record the cost and the counterfactual. |
| Is there research novelty? | Restricted proof candidates, exact counterexamples and informative failures. The prior review records substantial established mathematical context. | Precise statement, targeted priority comparison and appropriate independent proof assessment. Absence of a known citation is insufficient. |
| Does this show a human–AI team can do useful research? | The record shows hypothesis formation, exact implementation, correction, alternate-code checks, frozen comparisons and explicit null results. | It supports this bounded capability. General reliability, unique ability or superiority over another team would require a different comparative evaluation. |

These four questions must not be collapsed into one success score. A known lemma implemented well can have practical value. A mathematically new lemma can have no immediate external application. A polished demo can teach something without establishing either originality or performance advantage.

## What the new evidence changes

**The handoff line has reached a sensible stopping point.** In the first completed pilot, both presentations gave 40/40 requested outputs correctly and made 32 source requests. Strict complete-answer grades were 38/40 and 37/40, but the difference depends on readings of a policy-identity phrase. In run02, CC handoffs gave 17/18 supported complete answers; strong conventional handoffs and full sources gave 18/18 each. Every handoff/query retention check was adequate, and no reader requested recovery. These are small, synthetic, mostly ceiling-level comparisons; they establish neither general equivalence nor conventional superiority. They do remove the current empirical basis for claiming a CC advantage, and do not justify another nearby synthetic study merely to seek one. Token costs were unavailable, so there is no cost-effectiveness result.

The studies nevertheless yielded two useful regressions: an unspecified covering policy need not be a different policy, and uncertainty about a destination audit does not make a fixed backup's contents unknown. Those errors can teach object, version and operation scope without being advertised as a new theory of information.

**The latest interval study improves the representation, not the general existence claim.** Complete interval-and-point sources recovered all 1,197 fresh physical safe sets; the widest source missed 216 cases; dropping isolated points lost `(1,4,13)`. Complete recovery is expected from an exact complete-core construction. Its value is implementation validation and a concrete demonstration of which omissions change the answer. The cost of constructing 140 cores and 3,938 components belongs to this result. Complete-set recovery is not evidence that a compact rule is complete or faster.

The fixed `(1,2,r)` two-source argument has more lasting analytic value than another outer-box enlargement: it combines a positive-width interval with finitely many small exceptions. The mathematical track in the present review also reports a sharper minimum-source argument within the model of **fixed complete connected components of this one core**. That result must be read in the mathematics report and retain its restricted source model; this reviewer has not independently reconstructed it. It would not establish a universal two-source menu or exclude a different one-object representation containing a union.

**Older value should not disappear behind the latest language.** The 23-advance mixed-kernel candidate permits arbitrary positive real periods and phases, giving it a broader mathematical domain than the integer common-start examples. It remains a candidate about common safe points for four open quarter-duty blockers. Its equality fixture leaves zero safe duration, and its shorter width condition certified no additional window in the archived twelve-window comparison. It is a credible target for mathematical review, not demonstrated scheduling utility.

## Ranked recommendation

### 1. Finish one small conformance and replication kit now

Use ordinary mathematical and software names in the public interface. The package should expose the declared input, supported output, exact expected result and a direct physical check. Preserve the original affine segment and fixed third coordinate, exact phase target and alternative clock lift of the archived examples. Broad safety bands would change those questions.

The current proposed addition—a bounded SymPy periodic-set adapter—is a reasonable destination because it responds to an actual documented software contract. The official SymPy 1.14 documentation says that trigonometric inequality outputs are restricted to a periodic interval and describes reconstructing further solutions by period shifts. Its inequality solver documentation also records unsupported cases. This supports a contract-aware adapter; it does not establish a SymPy defect.[S1–S2]

The agreed development scope is ten structured cases using atoms `f(pi*(a*t+b)) relation c`, where `f` is sine or cosine, `a` is positive rational, `b` is rational, and `c` belongs to the declared five-value set. A finite rational horizon and explicit endpoint semantics make an exact phase-band oracle feasible. Solve each periodic atom alone, restore that atom's shifts, then intersect and clip the horizon. Periodicizing a result already truncated by nonperiodic bounds can lose valid solutions before recovery begins.

Acceptance should require complete set equality with the separately structured rational oracle, plus original-predicate checks on every boundary and intervening cell. A witness alone cannot certify that no other components were omitted. Empty, singleton, positive-width and unsupported/error outcomes must remain distinguishable. Include the already specified negative horizon, horizon beyond the principal period, mixed periods and strict/closed boundary cases. Principal-period-only misuse is a teaching mutation, not a competitive baseline; detecting it is not an external bug discovery.

The package should have one short command, dependency/version information, the original fixture queries, expected outputs, a machine-readable result and a brief explanation of why each failure occurs. A clean reproduction by a person or process that did not construct the package is the next useful check. Existing source hashes and a same-checkout rerun are useful integrity evidence, but are weaker than that reproduction.

**Stop condition:** finish the declared small corpus and its necessary correctness checks. A clean pass is a release result, not a reason to expand to fifty cases, add a general parser, invent a solver product or claim fresh transfer. If no actual consumer needs the adapter, keep it as a documented example and regression artifact.

### 2. Extract one reusable exact lemma, then seek the right review

The best small building block is the interval-to-periodic-band contact rule, with explicit threshold, rate, horizon and endpoint assumptions. Its positive-width tail criterion yields a finite remainder for one fixed supplied core. The two-source `(1,2,r)` construction is a compact concrete instantiation. These are useful interfaces for proof checking and software contracts even if their mathematics is elementary or already known.

A formalization would add value by checking quantified arithmetic and boundary conventions, not by making the supplied core complete automatically. Keep the statement small; separately certify core endpoints and the finite exceptions. Do not start by formalizing the entire historical repository. The older 23-move candidate is the stronger standalone research-review target, but requires more substantial analytical review and a separate priority check.

**Stop condition:** one complete statement and proof/checker obligation, with a clear success or identified gap. If a prior theorem supplies the result directly, cite and instantiate it. Do not compensate for a known result by broadening the claim. Do not resume larger `(p,q,r)` boxes until a concrete new sufficiency criterion or comparative cost question exists.

### 3. Make the kit usable for teaching; evaluate learning only if that becomes the goal

Three short exercises are enough: separate satisfiable constraints with no shared witness; identical duration summaries with different local nonemptiness; and a valid witness recovered only after restoring a clock lift. The physical examples and exact answers are the distinctive assets. Add the backup-uncertainty regression as an optional nonmathematical parallel, without claiming mathematical exactness transfers to prose.

If teaching effectiveness is claimed, compare the material with a good static explanation on an unseen problem. Completing the provided examples or enjoying an animation is not transfer of understanding. A small user test can establish a local benefit; it cannot establish general pedagogy.

**Stop condition:** one short entry point and reusable exercises. Do not enlarge the visual system until someone actually uses it or a specific comprehension problem is observed.

### 4. Defer further workflow and solver superiority experiments until there is demand

The next experiment should begin with a real task somebody already has, not another synthetic world designed around the vocabulary. Possible demand is an existing periodic-constraint frontend, a numerical/symbolic teaching course, or a maintainer wanting regression coverage. No outside contact is authorized by this report; selecting and approaching a consumer remains a separate human decision.

Stop generic CC-versus-checklist trials on nearby synthetic histories. Stop method branding as a substitute for a measurable output. Stop treating increasing archival volume, larger deterministic boxes or multi-agent agreement as increasing evidence of external impact.

## The hardest useful comparative test

The hard test is **whether an independent consumer can complete a pre-existing task more reliably or economically using the artifact than with competent ordinary practice**. It should be allowed to conclude that the artifact is only a clear example collection.

For a periodic frontend, freeze the user's actual predicate class, horizon semantics and required output before choosing cases. Compare the kit with a correctly implemented baseline that follows the official period-restoration contract or uses direct exact interval arithmetic. Give both the same source access and budget. Have someone other than the adapter author choose the bounded acceptance cases, including negative and equality cases, and preserve all unknown/error outcomes. Known source regressions remain development cases. Deliberately broken adapters may test diagnostics but cannot be the sole comparator.

Evaluate two levels separately:

1. **Correctness:** exact full-set agreement, valid original-coordinate witnesses, no false infeasibility, and explicit rejection of unsupported inputs. Any disagreement blocks the correctness claim until explained. Passing is bounded conformance, with no efficiency implication.
2. **Incremental benefit:** a real missed distinction exposed, reduced total integration/debugging time, an accepted regression or documentation change, or better performance on the consumer's own task. Charge translation, preprocessing, dependency/setup work, source recovery and failed attempts. Preselect the useful outcome; do not choose a favorable metric afterward.

One independently reproduced accepted fixture establishes one adoption event, not population-wide superiority. A timing claim needs equal output obligations and repeated measured runs; a user-time claim needs recorded task work, not script execution time. If a correct direct method is equally accurate and simpler, use it. The examples can remain valuable while the adapter is unnecessary.

For the current internal demonstration, no such outside evaluation has occurred. Ten well-chosen cases plus archived fixtures can establish that the team understands and implements a documented contract in that scope. That is an honest way to show what the collaboration can do.

## Information-loss check and actual coverage

This review keeps artifact utility, operational benefit, novelty and capability evidence separate. It retains the handoff nulls, compact-menu failures, complete-source construction cost, equality points, same-author verification limits and the distinction between a valid witness and complete-set correctness. It omits most historical proof detail because the decision here is allocation of further work, not proof certification. The cited source packages are the recovery route.

| Source | What this reviewer examined | Not established by this review |
| --- | --- | --- |
| `AGENTS.md`, `CLAIM_STATUS.md`, `CONTRIBUTING.md` | Full instruction/status/contribution text. | No permission to publish externally or promote proof status. |
| `README.md`, `HANDOFF.md`, `RESEARCH_PLAN.md` | Current entry summaries, selected recent/historical state and strategy sections. Large combined reads were partly truncated; no claim to every historical line. | No complete repository audit. |
| September 30 Ultra assessment, supporting README, coverage ledger and adversarial report | Full value synthesis and adversarial/coverage reports. | Other tracks' source coverage is attributed, not silently adopted as this reviewer's independent reading. |
| Both completed handoff `RESULTS_REPORT.md` files | Full reports, outcomes, sensitivities, limitations and next-work statements. | Raw trials, frozen prompts and grades were not re-adjudicated or rerun. |
| October 2 sheet and interval result reports; interval `DERIVATION.md` | Full reports and interval derivation, including fixed-pair proof candidate and lift/finite-tail rules. | No rerun of case matrices or full code audit. |
| `SHORT_KERNEL_BOUND_2026_09_28.md`, `EXACT_INTERVAL_CRITERION_2026_09_28.md` | Full written arguments and recorded limitations. | No formal proof check, novelty census or independent execution. |
| New mathematical-review minimum-source finding | Received from the separately tasked mathematics reviewer. | Not independently reconstructed by this reviewer. |
| New conformance package | Read the complete five-case standard-library `check.py`, and the SymPy `PROTOCOL.md` and `cases.json` before the adapter implementation appeared. Original archived queries and a separately structured direct-time reference are retained. | No independent execution by this reviewer; the five-case script is a bounded fixture checker, not a general-purpose solver. |
| SymPy adapter | Read the complete `demo.py`, declared schema, all ten case definitions and official contract. Checked per-atom solving/lifting order, rational sine phase arcs, strict/equality semantics, complete boundary partition and endpoint-aware union merging by inspection. | No generic symbolic completeness or outside adoption follows. The oracle and producer still share an author, and original substitution reuses SymPy. |

Executed by this reviewer: file inspection, targeted primary-document retrieval and one bounded rerun of the ten new SymPy development cases, recorded below. No historical research computation, workflow trial, performance benchmark or outside-user study was run. There is no claim to have reviewed every possible LTCM, technology, paper or file.

Release detail from the code inspection: the five-case checker verifies hashes against historical source files elsewhere in the repository. Its reproduction instructions must therefore use the repository checkout or include those dependencies explicitly. Copying only the example directory is not yet an independently runnable replication bundle.

The SymPy static review found no correctness blocker in the declared ten-case implementation. It did identify a dormant protocol mismatch: the first implementation recorded an unsupported/error case and continued, while the protocol said to stop. The author corrected that control flow, retained the original total in the success condition, and preserved `INITIAL_REPORT.json` and the development log. This is a source change after the first successful run, not unchanged-code first-run evidence. The two-minute budget is an external `timeout 120` invocation, not an internal timer. No unsupported/error branch or timeout occurred in the passing ten-case runs; they do not themselves exercise those branches.

After the correction, this reviewer ran:

```bash
PYTHONPATH=/tmp/lr-ultra-deps timeout 120 python examples/compatibility-conformance/sympy_periodic/demo.py --output /tmp/lr-ultra-redteam-sympy-report.json
```

All ten cases passed, with zero errors or unsupported outcomes. The complete sets agree, and all 120 original-predicate checks across 65 event points and their intervening cells agree. The resulting JSON is byte-identical to the package's `report.json`, SHA-256 `b2e04505570e8a50e8989a1e97780460f3620d7212313baa46c9cf68a08422a1`. This is a separate-reviewer rerun of the same implementation, declared inputs and shared environment. It is not a fresh clone, a newly authored oracle, a new holdout or outside adoption. No additional case was added or searched. The full set differs from the deliberately unlifted principal-only result in nine cases; that is a scope illustration, not a nine-bug finding.

## Primary sources checked in this review

- **S1:** SymPy 1.14.0, [Reduce One or a System of Inequalities for a Single Variable Algebraically](https://docs.sympy.org/latest/guides/solving/reduce-inequalities-algebraically.html), section “Not All Results Are Returned for Periodic Functions”; accessed October 2, 2026. Read the documented periodic-output limitation and example, not the whole solver implementation.
- **S2:** SymPy 1.14.0, [Inequality Solvers](https://docs.sympy.org/latest/modules/solvers/inequalities.html), `solve_univariate_inequality` notes, exceptions and examples; accessed October 2, 2026. Supports contract and unsupported-case distinctions, not an assertion that the new adapter is correct.
- **S3:** SymPy 1.14.0, [Calculus](https://docs.sympy.org/latest/modules/calculus/index.html), `periodicity` API description and examples; accessed October 2, 2026. Checked as a potential adapter obligation. The narrow proposed affine sine/cosine schema avoids a claim to solve arbitrary symbolic period discovery.

Earlier literature comparisons remain attributed to the September 30 reports. This review performed no new comprehensive priority search.
