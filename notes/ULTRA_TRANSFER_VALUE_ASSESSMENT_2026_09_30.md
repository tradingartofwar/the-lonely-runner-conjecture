# Ultra team assessment: useful beyond Lonely Runner?

September 30, 2026. Research reviewed through immutable commit `52c4912a89e4c314201e66e7fa94da7fa3366964`. Prepared in response to the [review brief](ULTRA_TRANSFER_VALUE_REVIEW_PROMPT_2026_09_30.md). Supporting [reports and coverage ledger](../reviews/2026-09-30-ultra-transfer-value/README.md) distinguish reading from verification.

**Yes: the work has produced reusable exact counterexamples, a working certificate-checking example, and narrowly stated mathematical mechanisms.** These can support software regression tests, teaching, and more careful scientific handoffs. We have not demonstrated better outcomes in another application, a new general theory of information, or a new implication for another open problem. Much of the transferable discipline is established elsewhere; its value here is the concrete examples, implementations and explicit failure records.

The best immediate export is small: package the three distinct clock-compatibility failures as source-bound, machine-readable regression fixtures with a direct physical-time verifier. Do not build a new solver merely to manufacture an application. A broader 72-case adapter test is specified below and remains unrun; it becomes worthwhile when an actual modular frontend needs validation.

## Ranked opportunities

Rank measures readiness for reuse, not mathematical originality or eventual importance.

| Rank | Candidate | What we actually have | What remains unproved |
| --- | --- | --- | --- |
| 1 | Exact conformance examples and source-bound witness checking | Three distinct translation failures; rational witnesses; an implemented coefficient checker; explicit distinctions between policy failure, incomplete discovery, invalid input and internal error | No external software defect found, deployment benefit measured, general solver advantage or new certification architecture |
| 2 | Query-specific summary and recovery contract | Physical examples with identical summaries and different answers; a working record of supported questions, missing relations, source versions and recovery | Better AI memory, scientific handoffs or organizational decisions; a matched conventional checklist may work equally well |
| 3 | Periodic point-feasibility certificates | Older mixed-kernel/23-advance proof candidate, exact interval margins, and a two-window placement certificate | External proof/priority assessment; applicability to ordinary job scheduling, dwell time or clock jitter; performance advantage |

These are three useful directions, not three commissioned projects. Exact examples already have diagnostic content. Their teaching effectiveness and operational value are separate empirical questions.

## The strongest recovered lesson: a complete summary for one question can fail another

The older [contact-moments note](CONTACT_MOMENTS_2026_09_27.md) supplies actual common-start configurations, not merely abstract event diagrams:

\[
V_1=\{0,1,3,4,5,10,28,1680\},\qquad
V_2=\{0,1,3,4,5,10,28,3360\}.
\]

At threshold `1/8`, relative to stationary runner 0, in the same closed window `J=[9/32,3/8]`:

| Output or summary | V1 | V2 |
| --- | --- | --- |
| Every labelled subset blocking-duration moment (128 including the empty subset) | Identical | Identical |
| All 21 pair gcds among the seven nonzero speeds | Identical | Identical |
| Total safe duration in J | 0 | 0 |
| Complete safe set in J | `{9/32}` | Empty |
| A strict safe time outside J | `11/64` | `11/64` |

The last witness has minimum distance `9/64>1/8`. Thus this is a failure to determine **local nonemptiness**, not global loneliness or total duration. Inclusion–exclusion still recovers total safe duration from all moments. Including `gcd(0,y)` or the raw changed speed would distinguish the inputs; those are explicitly absent from the matched summary.

The mechanism is inspectable: fixed blockers leave only endpoints in J; for `y=1680h`, the left endpoint survives exactly for odd h, while the right is always blocked. The duration primitive has equal corrections at the relevant phases 0 and 1/2, so it cannot distinguish the endpoint's survival. The finite archived examples retain OBSERVED status; the whole-family argument remains a proof candidate. The information reviewer inspected both calculation structures and the stored comparison, without rerunning them.

Two counterweights matter. In a different, more constrained family `(6,7,3,y)`, the reduced denominator of one duration statistic does identify endpoint survival. More detail is therefore not automatically needed. Separately, examples `y=672m` and `672m+1` have different endpoint outcomes while their maximum moment difference tends to zero as `3/[128(672m+1)]`: exact distinguishability and numerical robustness are different properties.

This review itself recovered a continuity error waiting to happen. September 25's audit had not found a physical duration/existence collision in its tested domain. September 27 supplied one. Repeating only the older summary would lose a consequential correction. Keeping dates, scope and supersession attached to findings has immediate value in this project; it does not yet prove a general AI-memory benefit.

## Transfer record 1: modular-constraint conformance

| Required field | Assessment |
| --- | --- |
| Origin/status | [Rank-three test](CC_THREE_PARAMETER_TEST_2026_09_30.md), saved discovery/verification records and [coefficient checker](CC_COEFFICIENT_CHECKER_2026_09_29.md). Exact finite observations and implementation evidence; general derivations retain proof-candidate status. |
| Mechanism | Keep the same point across constraints, use all integer relations needed to characterize the physical orbit, retain required clock lifts, and substitute the recovered time into every original constraint. |
| Destination | A frontend translating a common periodic clock into modular phase constraints: for example, one simultaneous trigger instant for three devices. This is an instantaneous feasibility problem, not a job schedule. |
| Translation | Rates become device frequencies, safe phase bands become operating windows, and the recovered physical time becomes the trigger. Offset phases require relations on `phase-offset`. Preserve rates, offsets, endpoint flags, source identity and witness. Other times and optima may be discarded because the query asks for one instant. |
| Inherited/new obligations | Affine identities and direct substitution survive. A new parser, correct offset conversion, complete relation basis, window semantics and faithful source translation must be checked. Old menu coverage, finite-tail reductions and atlas completeness do not transfer automatically. |
| Existing approach | Direct exact mixed integer/real SMT constraints and rational interval intersection. Certifying computations already separate witness checking from the producer; solver standards already distinguish logical results from unknown/error. |
| Added value | Explainable regression cases for modeling and recovery mistakes; a concrete contract example. No claim that established solvers are defective or that the new representation is simpler. |
| Failure test | A claimed feasible time violates an original constraint; a definitive infeasibility verdict contradicts the exact interval oracle; a candidate-class miss is mislabeled as full infeasibility. |
| Smallest test | The [computation report](../reviews/2026-09-30-ultra-transfer-value/computation_transfer.md) fixes a 72-case, two-encoding comparison with an independent rational interval oracle. All inputs and budgets are specified; executable/version hashes and implementations must be frozen before execution. It is UNRUN. |
| Assessment | Supported diagnostic adaptation. External engineering benefit remains a hypothesis. |

The three source regressions are different:

1. **Same-point loss:** for `(p,q,r)=(1,2,6)`, source `[(1/8,1/4),(11/72,5/24)]` with `z=7/8`, the two relation ranges each contain zero but require different parameters along the segment.
2. **Incomplete integer relations:** for `(2,3,1)`, `(x,y,z)=(1/4,7/8,1/8)` passes `3x-2y∈Z` and `x-2z∈Z`, but the required relation `-x+y-z=1/2` is not integral.
3. **Lost clock lift:** for `(2,4,5)`, old pair time `3/16` violates the third phase, whereas `11/16` realizes the compatible point `(3/8,3/4,7/16)`.

The proposed 72 cases use six declared rate triples, three offset tuples and four window tuples. Compare the phase-coordinate frontend with direct-time SMT on the same pinned solver and an independently structured exact interval oracle. Require 72/72 definitive agreement and valid positive witnesses; record unknown/error separately. Budget: four person-hours implementation, one CPU process, 1 GiB memory, five seconds per SMT query and twenty minutes execution. Existing diagnostics are reused development material, not fresh holdout evidence. A clean pass demonstrates bounded adapter correctness, not superiority. No need for a lattice adapter has yet been identified outside this research.

## Transfer record 2: scientific and AI handoffs

| Required field | Assessment |
| --- | --- |
| Origin/status | Contact-moment collision, occurrence-labelled examples, changed-constraint failures and [CC representation rules](CC_REPRESENTATION_RULES.md). Exact diagnostics plus a working discipline; no external workflow experiment. |
| Mechanism | For source class D, summary S and query Q, adequacy requires `S(d1)=S(d2) => Q(d1)=Q(d2)`. A counterexample refutes that specific adequacy claim. Record the supported operation and trigger source recovery when use changes. |
| Destination | A handoff used to answer a later question about a common build, specimen, time or current evidence state. |
| Translation | Occurrence identity becomes build/run/version identity; local existence becomes a decision query; richer source geometry becomes the original records. Retain scope, joint keys, boundaries, evidence status, version and recovery route. Omit irrelevant detail deliberately. |
| Inherited/new obligations | The logical collision test transfers. Runner-specific exactness, completeness and physical recovery do not become guarantees about prose. Destination truth, uncertainty, source availability, retrieval accuracy and cost require their own evidence. |
| Existing approach | Database view/query determinacy and source provenance; a competent facts/assumptions/sources/next-action checklist is the practical comparator. |
| Added value | Explicit unsupported uses and retrieval triggers, backed by concrete counterexamples. This may simply be good conventional note taking expressed carefully. |
| Failure test | Unsupported joint approval, zero duration treated as emptiness, stale evidence treated as current, or unchanged accuracy at higher cost than the checklist. |
| Smallest test | The [information report](../reviews/2026-09-30-ultra-transfer-value/information_transfer.md) specifies ten synthetic cards, including two adequate-summary controls, matched 120-word records and equal retrieval budgets; 80 fresh-context answers, one fixed runtime, one-hour cap. Require fewer consequential errors, zero unsupported approvals and at most 20% greater median token cost. Cards, oracle, arm wording and runtime must be frozen before execution. UNRUN; not the recommended next project. |
| Assessment | Supported practical hypothesis, with established formal foundations. No organizational or AI-memory improvement demonstrated. |

The formal criterion is established query determinacy [P1]. A recoverable summary is not intrinsically lossless; provenance [P3] does not establish that the retained facts answer the new question. The worthwhile question is whether the extra record prevents consequential mistakes more economically than an ordinary good checklist.

## An older mathematical result worth preserving

The [short-kernel candidate](SHORT_KERNEL_BOUND_2026_09_28.md) studies four open periodic blocked trains

\[
B_i=\bigcup_{m\in\mathbb Z}(s_i+mp_i,\ s_i+(m+1/4)p_i).
\]

For largest period P and other periods q,r,s, put `H=P+3(q+r+s)/4`. Its averaging argument and occurrence count give a candidate bound of **23 advancing moves**, and a safe point in every closed interval of width at least H. The stated mathematics permits arbitrary positive real periods and arbitrary phases; it does not need common start, integer speeds, a source atlas or the later two-parameter structure. The implementation is rational, and a move is not a raw projection call: the archived eleven-call ordering allows up to 253 calls, with arithmetic costs separate.

This is the strongest standalone mathematical extraction identified by the review. Existing shifted-runner and interval-chain precedents are credited in the [mathematics report](../reviews/2026-09-30-ultra-transfer-value/math_transfer.md); priority of the mixed kernel and bound remains unresolved. The shorter H did not certify additional windows in the archived twelve-window comparison.

Its own equality fixture limits the application: periods `4/13`, shifts `i/13` for `i=0,1,2,3`, and window `[0,1]` leave only the fourteen points `j/13`. There is no positive available duration. Making the blackouts half-open fills every gap. Adding a positive job duration or clock jitter expands the forbidden sets and loses the original critical-duty guarantee. This is an exact periodic point-feasibility candidate, not a general scheduling theorem.

A separate [two-window certificate](LAST_RUNNER_COMPATIBILITY_2026_09_29.md) retains widths and placement: hull span D, gap G and larger width w with `G<=3w` and disturbance speed `d>=1/(4D)` prevent a quarter-duty train from strictly covering both supplied windows at any phase. Strict inequalities give positive residual duration, without a guaranteed job length. The archived pair has `D=5/224`, `G=1/96`, `w=3/448`; every real `d>56/5` leaves positive duration. Supplying the initial windows remains a separate obligation.

## What should change in our interpretation and practice?

- **Use established methods where they fit.** Query determinacy, exact interval intersection, SMT, certifying computations and provenance give useful existing vocabulary and implementations. CC is currently a working language for carrying questions, joint constraints, evidence and recovery across representations; it has not been established as a new general mathematical framework.
- **Preserve the latest failure.** Four sheets cover 89/89 training and 310/318 held-out cases; all 36 cover all 407. The eight frozen menu misses remain failures. Family rank three still has one-dimensional fixed integer orbits and product geometry, not arbitrary mixed-r motion. No infinite-domain reduction was proved.
- **Keep recovery conditional.** The hybrid's reordered exact intersections recovered missed witnesses from supplied geometry. Its completeness depends on that source class and finished enumeration; its timings exclude atlas production. Classical CEGAR [P4] removes spurious behaviors from an overapproximation, whereas this safe screen restores witnesses omitted by an underapproximation. The connection is architectural, not an inherited theorem.
- **Stop promoting analogy to application.** Phase notation supplies no quantum advantage or physical interaction; no formal information-theoretic synergy quantity was established. Exact visual correctness is distinct from measured learning. No new implication for another named open problem emerged. Classical integer pinwheel scheduling's `5/6` conjecture is already proved [P5], and its perpetual task assignment is not the common-point problem here.

## Disagreements, coverage and one next action

The mathematics track prioritized the older kernel candidate; the information track prioritized summary contracts. The computation and adversarial tracks favored conformance examples, with an important demand condition: direct-time constraints may already solve the destination more simply. The coordinator ranks the corpus first because its errors and answers can be stated exactly, while preserving the others as credible, narrower leads. These are priority differences, not unanimous evidence of a new application.

The review involved a coordinator, four separately tasked AI reviewers, and one delegated literature subreview. Runtime configuration was inherited; a distinct Ultra model identity was not established. Reviewers shared sources and exchanged findings, so this was not blind or external certification. The full 1,126-file research inventory was available; all 105 Markdown notes were indexed and their openings skimmed, then selected arguments, code and archived evidence were read in depth. **No research computation, solver test, benchmark or user study was run.** Detailed reading limits appear in the [coverage ledger](../reviews/2026-09-30-ultra-transfer-value/COVERAGE_LEDGER.md). Original research packages and claim statuses remain unchanged.

**One recommended next action:** extract the three archived compatibility diagnostics into a small machine-readable conformance pack, retaining exact source inputs, expected outcomes, physical recovery and a direct-time verifier. Preserve the first fixture's affine segment and fixed z, the second's exact target phase point, and the third's requested phase triple and alternative lift. Broad safety bands alone would change the questions. This is a reusable regression/teaching artifact, with no claim to solve a new problem. Stop at that scope unless an actual frontend needs the separately specified 72-case validation. Do not launch the scheduling and handoff pilots simultaneously.

The strongest reason even this proposal may add little is that ordinary direct-time SMT plus physical substitution already preserves the necessary distinctions. The contribution may be a clear collection of examples rather than a better algorithm. That is a legitimate useful outcome, and the test must be allowed to say so.

## Primary comparisons

Consulted September 30, 2026; targeted comparisons, not a novelty census. Full section/version/reading limits are in the four supporting reports.

- **P1:** Nash, Segoufin, Vianu, *Views and Queries: Determinacy and Rewriting* (2010), introduction and definitions: <https://cs.uwaterloo.ca/~gweddell/cs798/a21-nash.pdf>. Used for query-specific determinacy, not current open-problem status.
- **P2:** Alkassar et al., *Verification of Certifying Computations* (2011), checker/abstraction/witness obligations: <https://www.mpi-inf.mpg.de/~mehlhorn/ftp/VerificationCertComps.pdf>. Also [SMT-LIB 2.7, 2025-07-07](https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf) and [official Z3 arithmetic documentation](https://microsoft.github.io/z3guide/docs/theories/Arithmetic/). These establish comparators, not correctness of our checker.
- **P3:** W3C *PROV-DM*, Recommendation April 30, 2013: <https://www.w3.org/TR/2013/REC-prov-dm-20130430/>. Provenance vocabulary does not certify semantic adequacy.
- **P4:** Clarke et al., *Counterexample-guided Abstraction Refinement* (CAV 2000): <https://web.stanford.edu/class/cs357/cegar.pdf>. Finite-model and property hypotheses remain attached to its guarantees.
- **P5:** Kawamura, *Proof of the Density Threshold Conjecture for Pinwheel Scheduling* (STOC 2024), definition and Theorem 1: <https://www.kurims.kyoto-u.ac.jp/~kawamura/pinwheel/paper_e.pdf>. The computer certificates were not reproduced in this review.
