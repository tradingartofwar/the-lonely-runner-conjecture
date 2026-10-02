# Computation and engineering transfer review

September 30, 2026. Research baseline: `52c4912a89e4c314201e66e7fa94da7fa3366964`, `tradingartofwar/the-lonely-runner-conjecture`. This is a static evidence review and an **unrun** test design. No solver experiment, numerical rerun, target scan or benchmark was performed for this review.

The computational work has produced useful exact examples and disciplined software interfaces inside this project. It has not yet demonstrated an external application or a new general-purpose solving method. The most credible small export is a modular-feasibility conformance corpus: concrete cases in which separate marginal checks, incomplete integer relations, or a prematurely chosen clock lose the requested answer. The coefficient checker is a good application of established certifying-computation practice. The hybrid is a useful special-purpose change in intersection order, whose measured advantage has only been shown on supplied geometry and three informed inputs.

## Ranked assessment

| Rank | Candidate | What the record establishes | External status and next use |
| --- | --- | --- | --- |
| 1 | Exact counterexamples and recovery records for modular-feasibility frontends | Three different, explicit rank-three translation failures, with physical recovery and saved alternate-code checks | **Supported diagnostic adaptation.** Package as regression cases for a shared-clock/periodic-constraint frontend. No evidence of a bug in an existing external solver or improved real-world scheduling. |
| 2 | Question-specific decision records and source-bound certificates | Reusable exact coefficient checker distinguishes a fixed rule's universal guarantee, its concrete failure, requested-pair behavior, invalid inputs and internal inconsistency | **Known technique, useful implementation example.** Reuse certifying-computation and standard solver-status language. The acceptance guarantee still depends on an internally reviewed mathematical proof candidate. |
| 3 | Contact-first recovery after a sufficient screen | Exact source-relative one-witness recovery, two nonempty recovery cases, one complete-screen case, and bounded timings | **Conditional computational hypothesis.** Try only where reusable source geometry already exists and few queries need recovery. No general solver, complexity, or end-to-end speedup claim. |

Recommendation for the overall review: export the failure examples and evidence contract; do not start a new solver project. The optional test below is appropriate only if a concrete modular frontend is being built or changed. A practical summary/recovery comparison from another track may have higher immediate value than implementing this adaptation solely to test it.

## What was recovered from code and certificates

### Operational support and quantifiers

`notes/CC_SELECTOR_SUPPORT_2026_09_29.md` supplies a nontrivial adequacy result: the old deterministic selector visits a closed countable, nondense subset of a segment, yet its positive-integer coefficient acceptance set equals the whole-segment-plus-fallback condition. The proof candidate uses an analytic large-slope counterexample and safe tail before the finite 216-cell check; density is not the reason. The implementation in `reviews/2026-09-29-cc-selector-support/selector.py` explicitly carries the tail predicate and bounded support. This does not license the same compression for arbitrary real coefficients or another selector.

The new-selector record is a useful correction to any slogan that more geometry always means a better certificate. `notes/CC_ROW38_COEFFICIENT_RANGE_2026_09_29.md` distinguishes the 205 operational classes, 178 auxiliary-inclusive classes and just 21 positive rows satisfying whole-fallback safety. Row `(59,64)` is safe at actual primary outputs but not at an unused interior fallback point; `(6,2)` is primary-safe but fails the repeated-speed auxiliary. That note and the corresponding working-rule discussion were read; its complete classification code and every certificate were **not** reaudited here. The 205 and 42 old/new counts have different periods and are not a set-size comparison.

There are three different questions: `for every input, this fixed policy works`; `for each input, some policy works`; and `this particular requested input works`. A policy dispatcher selected once for a coefficient row does not prove the stronger point-by-point mixture. These are standard quantifier distinctions, made useful here by concrete counterexamples and executable records.

### The coefficient checker is narrower than a general proof checker

I read all of `lonely_runner/cc_coefficients.py` and `tests/test_cc_coefficients.py`. Acceptance checks a **shared** lap band for both leader endpoints, plus the used fallback. It does not merely compare residues separately. Rejection goes through an explicit branch construction and then `evaluate_selector`, which checks the actual speeds, phases, physical laps, core safety, strict seventh failure and distinctness before returning `REJECTED`. Failed invariants use explicit `_require` exceptions, which remain active under optimized Python. Invalid inputs use `ValueError`; the CLI alone serializes `INVALID_INPUT`.

The status meanings matter. `(5,2)` can be globally rejected through `(p,q)=(2,3)` while its requested `(1,3)` evaluation succeeds. Accepted identically repeated core rows carry an empty distinct-speed-domain flag. An arithmetic inconsistency is not a mathematical counterexample. These distinctions are present in code, not only in a narrative.

Acceptance serializes supporting inequalities and a reference to the universal proof candidate; it does not independently validate an arbitrary external proof of that universal theorem. The archived 480 decisions and optimized-mode tests are prior evidence, not tests rerun in this review. The bounded branch count also does not make arbitrary-precision integer arithmetic constant-time.

### A sufficient screen omits real answers; recovery changes the operation

The screen's identity is `u-v=8kc` on a source whose `c` value is constantly an appropriate eighth-boundary. This proves safety of the entire accepted source. The `(54,26)` trial emits five sources but all five collectively miss `(1,2),(1,4),(5,1)`, while the full appended class has 61 records and covers them. At `(1,2)`, the omitted contact `(1/8,1/4)` is safe even though its source is not on the required constant boundary. `NO_SCREEN_CERTIFICATE` is therefore not unsafety.

I read the operative `bounds`, `preflight`, `query`, `recovery`, build and dispatch functions in `reviews/2026-09-29-cc-hybrid-recovery/hybrid.py`. They exhaust integer contacts on each supplied affine segment, including constant-integer, constant-noninteger and singleton cases, then check the new row. In set notation both operations decide nonemptiness of

`S ∩ {Qx-Py ∈ Z} ∩ U⁻¹(⋃m [m+1/8,m+7/8])`.

The intersections commute, but early stopping, storage and costs do not. Completeness is relative to the supplied source class, provided enumeration and its budget finish. A finite residual reduction is separately necessary for the uniform infinite-family conclusion. The return states keep a scope limit apart from exhausted source search. The resulting segment menu and direction-keyed points are different record types; neither is a full safe-set representation.

The stored summaries retain 108 preflight projections and 108 raw-range checks in the first two cases. Actual recovery visits 11 sources/3 contacts for `(54,26)` and 14/4 for `(102,50)`. The latter rejects the stale `(5,1)` time `9/40` and finds `31/136`. At `(78,50)`, recovery work is zero: this tests the screen's changed geometry, not the unexecuted recovery branch. Archived medians favor the hybrid, but omit atlas production and do not demonstrate whole-pipeline savings. Smaller materialized output is not by itself lower cost.

### Rank-three failure is useful evidence, not a success after repair

The saved `discovery.json` and summary preserve exactly eight held-out misses: `(1,2,8)`, `(1,4,8)`, `(1,7,4)`, `(2,3,8)`, `(3,2,7)`, `(5,1,7)`, `(5,7,4)`, `(5,7,8)`. Four sheets cover 89/89 training and 310/318 held out. All 36 sheets cover 407/407; the 72 boundary objects cover 90/407. The all-class fallback did not repair the frozen four-sheet menu. Its stop was complete training coverage at four objects, not the eight-object cap. No conclusion about the best possible four-sheet menu follows.

I read `lattice`, `intersect`, `witness`, `compile_menu` and the split construction in `discover.py`, together with the alternate checker's function structure and saved verification summary. Integer `h` slices are tested jointly with `n` on the same slice. The two relation rows are built through two gcd/Bezout levels; the recovered physical time is checked by multiplying the actual speeds. The training menu is compiled before held-out contacts are built. These checks support the stated mechanism, not an independent formal verification of every branch.

Three saved diagnostics are especially portable:

| Loss | Exact archived example | Why a common engineering shortcut is inadequate |
| --- | --- | --- |
| Shared point | `(1,2,6)`, source `[(1/8,1/4),(11/72,5/24)]`, `z=7/8`; both relation ranges contain 0 but require different source parameters | Nonempty marginal projections do not imply one feasible joint state. |
| Complete integer relations | `(2,3,1)`, point `(1/4,7/8,1/8)` passes `3x-2y∈Z` and `x-2z∈Z`, but `-x+y-z=1/2` | A nonprimitive relation lattice admits extra orbit components; safe ambient coordinates do not bind a witness to the actual clock. |
| Clock alternatives | `(2,4,5)`, point `(3/8,3/4,7/16)`; time `3/16` fails, time `11/16` works | A canonical inverse for the old coordinates may discard a lift needed after a new constraint. |

This raises coefficient-family rank, while every fixed integer instance still has a one-dimensional periodic orbit. The geometry retains product structure and only one independent `r` row. There is no automatic generalization to arbitrary mixed-r families, irrational clocks, or a uniform finite-exception theorem.

## Transfer record A: conformance cases for a modular-feasibility frontend

| Field | Record |
| --- | --- |
| Origin | The three diagnostics above, the eight held-out misses, `CC_THREE_PARAMETER_TEST_2026_09_30.md`, `discovery.json`, `verify.py`. Finite exact observations; the general derivation remains a same-author checked proof candidate. |
| Mechanism | Preserve the joint affine constraint set, a saturated integer relation basis, all required clock lifts, and a direct physical witness check. |
| Destination | Validate a frontend that translates a shared periodic clock into modular phase constraints, e.g. finding one common maintenance-trigger instant inside three devices' allowed phase windows. This is an instantaneous feasibility task, not a duration, robustness, latency or optimal-schedule claim. |
| Translation | Speeds become device rates; phases become allowed operating windows; a physical time becomes the trigger instant. Offset phases require applying relations to `phase-offset`. A menu becomes a cached candidate subset. Its exhaustion says nothing about the full task unless the source class is exhaustive. |
| Retained/discarded | Retain all original rates, offsets, windows, endpoint conventions, relation identities, source ID and a recovered time. A single witness deliberately discards other times and any optimum. |
| Inherited/new obligations | Exact affine identities and physical multiplication transfer. New obligations are the offset translation, each target window, full versus candidate-restricted coverage, and parser/serialization correctness. Old LRC finite-tail and screen guarantees do not transfer. |
| Existing approach | Direct mixed integer/real constraints in SMT, or exact interval intersection over one common period. Z3 already represents mathematical integers/reals and mixed arithmetic; it is a strong baseline rather than something CC replaces. |
| Added value | A small, explainable suite that catches frontend modeling and witness-recovery mistakes. No established solver defect, new decision procedure or speedup has been found. |
| Failure test | Any adapted `SAT` witness that fails direct physical substitution, or a definitive `UNSAT` when the independent exact oracle is nonempty, defeats the adaptation. If an existing frontend already passes and the examples reveal no useful gap, marginal utility is educational/regression coverage only. |
| Smallest useful test | The completely specified unrun test below. |
| Assessment | Supported diagnostic adaptation; no demonstrated external operational utility. |

### Optional test A — frozen specification, not executed

Test **existence of one instant** `0 <= t < 1` satisfying `l_i <= {v_i t + phi_i} <= u_i` for all three devices. All endpoints are exact rationals and closed; only the horizon's upper endpoint is open. Inputs are the Cartesian product of these lists, in the order written (72 cases):

* Rates: `(1,2,6)`, `(2,3,1)`, `(2,4,5)`, `(3,5,7)`, `(4,6,9)`, `(5,7,11)`.
* Offsets: `(0,0,0)`, `(0,1/8,1/4)`, `(1/16,3/16,5/16)`.
* Three-window tuples: `([1/8,7/8],[1/8,7/8],[1/8,7/8])`; `([1/4,1/4],[7/8,7/8],[1/8,1/8])`; `([3/8,3/8],[3/4,3/4],[7/16,7/16])`; `([0,1/16],[7/16,9/16],[15/16,15/16])`.

The first three rates and two pointed window choices are informed by archived diagnostics; they are not fresh holdout evidence. Nonzero offsets and the other rates provide additional synthetic transfer cases, not a representative industrial workload. Keep the original three source-geometry diagnostics in a separately labelled regression group; do not inflate the 72-case denominator with them.

**Comparator 1:** ordinary direct-time SMT encoding: one real `t`, three integer laps `m_i`, the horizon, and `l_i <= v_i*t + phi_i - m_i <= u_i`. Use the same pinned Z3 executable for both SMT encodings, no optimization objective and no floats.

**Candidate:** a phase-coordinate encoding with all three window variables, the two saturated integer relations applied to `(x_i-phi_i)`, then the archived two-level Bezout recovery generalized to the shifted coordinates. A returned point must recover an instant and pass direct original-input substitution. Do not substitute independent marginal feasibility. Do not use any training-selected menu.

**Independent ground truth/comparator 2:** a separate exact rational implementation constructs each clock's intervals `[(m+l_i-phi_i)/v_i,(m+u_i-phi_i)/v_i]` for integers `m=0,...,v_i`, clips to `[0,1)`, and intersects the three unions with endpoint flags. This finite range exhausts these declared inputs. It imports neither candidate relation code nor solver results. Preserve the complete interval union as the case-level oracle and check every emitted witness independently.

**Budget and freeze:** at most four person-hours of implementation, one CPU process, 1 GiB memory, 5 seconds per SMT query, 20 minutes total execution. Before first execution, save the 72 input records, exact implementation source, executable/version hashes, dependency lockfile and this protocol; solver version selection may not depend on test results. A missing dependency or budget stop is `UNRUN`/`UNKNOWN`, never mathematical `UNSAT`. No additional rates, window tuning, benchmark sweep or reranking follows failures in this trial.

**Success measure:** 72/72 agreement on definitive existence verdicts, every positive certificate physically valid, separate recording of unknown/errors, and exact source bindings. Record time and output size only descriptively; do not count a speed win as the goal. The candidate must be compared with the unmodified direct-time baseline, not with deliberately broken marginal/lattice/lift encodings. Mutants may later be educational controls, but cannot establish superiority. A clean pass establishes bounded translation correctness; an existing-code defect fixed by these cases would establish a concrete additional benefit. Otherwise stop at a regression/teaching artifact.

## Transfer record B: question-bound certificates and selective recovery

| Field | Record |
| --- | --- |
| Origin | `cc_coefficients.py`, `CC_SELECTOR_SUPPORT_2026_09_29.md`, `CC_PHASE_SCREEN_2026_09_29.md`, `hybrid.py` and the three stored transfer summaries. |
| Mechanism | Give each result a named predicate and domain; return physical evidence for a violated fixed policy; distinguish no certificate, candidate-class exhaustion, full infeasibility and resource failure; recover omitted candidates from a pinned source when the query changes. |
| Destination | Exact feasibility services or configuration-policy validators which currently conflate “this proposed setting fails” with “no setting exists,” or reuse a cached witness after adding a constraint. |
| Translation | Coefficient row becomes policy/configuration; requested pair becomes deployment input; selector becomes fixed policy; physical witness becomes a checked execution/configuration; source atlas becomes the full candidate database. The source must really cover the declared task before exhaustion implies infeasibility. |
| Inherited/new obligations | The design discipline transfers. The domain-specific coefficient theorem does not. A new witness predicate, source-to-runtime translation, complete oracle and error/status contract are required. |
| Existing approach | Certifying algorithms, SMT-LIB result/status conventions, exact constraint solving. Lazy constraints share delayed materialization but differ from restoring an underapproximated witness set. |
| Added value | A compact implemented example of contract design and recoverability; potential maintenance reliability. It largely restates established practice, with unusually clear counterexamples. |
| Failure test | A stale witness remains accepted after a violated new row; a source omission is reported as full infeasibility; a malformed certificate or budget error is reported as a mathematical rejection; or source reconstruction omits a relevant constraint. |
| Smallest useful test | Reuse test A's original-input check and explicit statuses as the smallest concrete exercise. Do not launch a second project just to demonstrate a known interface pattern. An external service needs its own representative workload before cost claims. |
| Assessment | Known technique with a useful local implementation and diagnostic record. External reliability benefit remains unmeasured. |

## Prior-art map and reading limits

All web sources were consulted September 30, 2026. Exact URLs are given for review and reuse. This was a targeted comparator check, not an exhaustive novelty search.

| Primary source | Read and warranted comparison | Limit |
| --- | --- | --- |
| Alkassar, Böhme, Mehlhorn, Rizkallah, *Verification of Certifying Computations* (2011), <https://www.mpi-inf.mpg.de/~mehlhorn/ftp/VerificationCertComps.pdf> | §2's checker/abstraction/witness obligations; §4 checker contract and §4.4's discovery that a matching checker omitted the source-subgraph condition. Exact precedent for source-bound certificates. | Their formal assurance does not transfer to this Python code. Rejecting a bad certificate need not refute the underlying mathematical claim. |
| *SMT-LIB Standard* 2.7, release 2025-07-07, <https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf> | Response grammar/status passages and subagent's §§4.1.2, 4.2.5–4.2.6 reading: `sat`, `unsat`, `unknown`, errors and current assertion context. | Different taxonomy from this checker; source hashes do not prove faithful assertion translation. Not a full standard or solver audit. |
| Official Z3 Guide, Arithmetic, <https://microsoft.github.io/z3guide/docs/theories/Arithmetic/> | Mathematical integer/real sorts, mixed arithmetic, and arithmetic-fragment overview. Supports direct-time SMT as the baseline. | Documentation is not a measured benchmark or proof of a frontend. No Z3 run performed. |
| `isl` manual version 0.28, <https://libisl.sourceforge.io/user.html> | Introduction, Sets and Relations, exact values/gcd, Error Handling. Existing sets/relations under affine constraints are the relevant vocabulary. | Integer sets are not automatically an encoding of continuous-time phase geometry; no direct backend implementation or performance comparison was attempted. |
| Gurobi `Model.cbLazy`, <https://docs.gurobi.com/projects/optimizer/en/current/reference/python/model.html#Model.cbLazy> | The callback contract and delayed-constraint discussion; read with subagent. An established model for withholding materialization while retaining a complete check. | Numerical MIP and cutting off relaxed candidates differ from CC's safe underapproximation and restored witnesses. No inherited exactness or speed guarantee. |
| Clarke et al., *Counterexample-guided Abstraction Refinement* (CAV 2000), <https://web.stanford.edu/class/cs357/cegar.pdf> | Introduction/spurious-counterexample refinement, with subagent's §§3–5 reading. | **Analogy only.** CEGAR refines an overapproximation to remove spurious behavior; the phase screen is an underapproximation that must restore omitted valid witnesses. Do not identify them as the same algorithm. |

The child reviewer also read Necula's PCC paper/author overview, but it is not needed for the strongest mapping and does not establish the checker's negative-result contract. This report does not infer novelty from a failure to find a closer source.

## Assumptions and failure boundaries

| Source assumption | What changes outside it |
| --- | --- |
| Common start | Rational phase offsets can be translated affinely, but the boundary identities and chosen menu need rechecking. Test A explicitly adds offsets. |
| Positive integer, hence commensurate rates | One finite common period and integer-lap enumeration are available. Irrational rates require a different argument; do not reuse a finite-period completeness claim. |
| Small parameter rank / product sheet geometry | The present contact code exploits a segment times an interval and two saturated relations. Arbitrary mixed-r rows may require richer polyhedra and harder integer feasibility. |
| Closed exact bands | Singleton witnesses count. A positive-duration service operation, clock jitter or strict margin is a stronger task and can invalidate usefulness. |
| Exact rational arithmetic | Equality and strict rejection remain decidable in the implementation. A floating-point port needs an independently justified error policy. |
| Supplied source atlas and finite residual proof | Recovery is complete only relative to that source; atlas construction is real work. Without the width/tail argument, a finite query box gives no universal coverage. |
| Deterministic compact policy | Its failure is informative about that policy only. Eight held-out menu misses do not imply physical nonexistence or impossibility of every equally small menu. |

The strongest reason the preferred diagnostic may add little is that ordinary direct-time SMT plus direct witness substitution already retains these distinctions with a simpler representation. A new lattice frontend may introduce more bugs than it prevents. Reuse the examples where an existing representation change makes them relevant; otherwise stop at documentation and education.

## Coverage ledger and provenance

| Cluster/artifact | Actual examination | Rerun/limit |
| --- | --- | --- |
| Repository guidance / trajectory | AGENTS, README, CLAIM_STATUS, CONTRIBUTING, RESEARCH_PLAN, HANDOFF and representation rules; long combined reads were truncated, then scoped notes recovered | Navigation and evidence vocabulary; not every historical artifact inspected |
| Old operational support | Full note, selector code, supporting proof logic and bounded-support serialization | No computation rerun; no independent universal proof certification |
| New coefficient range | Note's contracts/criterion/support and representation-rule discussion | Full 205-class output and all physical failures not independently audited |
| Coefficient checker | Entire runtime and unit tests; note and substantial contract review | Static review only; archived 480 decisions not reexecuted |
| Phase screen | Full note and stored result interpretation | `compare.py` not fully audited; no target search |
| Hybrid | Full recovery note; operative recovery/dispatch functions; all three summary JSONs and selected proof/contract text | Transfer adapter and timing harness not fully audited; no benchmark rerun |
| Rank-three | Full note; core relation/contact/recovery/menu code; verify structure; saved diagnostics and all eight miss records; summary outputs | Not all 45,252 bits independently recalculated; same-author archived verifier remains same-author evidence |
| Earlier overlap, chain, floor-sum, projection history | Handoff/plan summaries only in this track | Other reviewers' remit; this report makes no independent verification claim |
| Cross-domain utility | Targeted primary-source comparison and explicit unrun design | No external workload, user study, solver benchmark, bug report or practical adoption demonstrated |

Twelve directly used local code/output files were matched to their Git blob IDs in the baseline `SOURCE_INDEX.json`: `cc_coefficients.py`, its unit test, selector `selector.py` and `support.json`, hybrid `hybrid.py`, three hybrid/boundary summaries, and rank-three `discover.py`, `verify.py`, `discovery.json`, `verification.json`. The source tree is a hydrated sparse snapshot rather than a local Git checkout. Baseline notes were additionally available from the coordinator's hash-matched immutable snapshot. Hash matching establishes source identity, not correctness.

Authorship: AI computation-track reviewer with a narrowly delegated primary-literature subtask; all work shares the same repository evidence. This report does not claim an independently identified “Ultra” model, external human review, formal verification or blind replication. Tools used were static file inspection, JSON extraction/hash checks and web retrieval. Hash checks and saved-record extraction are not new research computations.
