# Ultra review: turn exact failures into something another person can use

October 2, 2026 UTC. Review baseline `29e54d32e2ff5349bdb0c3db56fab753a0e44c94`. Five main AI review tracks covered mathematics, alternative frameworks, external applications, information/evidence, and adversarial value assessment. Additional code checks and a working demonstration followed. This is a broad, source-linked review with declared reading limits, not an exhaustive audit of every repository artifact or every possible model language.

**The most credible immediate value is an executable example of preserving a problem's meaning across representations. We built it.** It includes five exact regression cases from the research and a ten-case adapter for SymPy's documented periodic-inequality workflow. A separate mathematical review also sharpens the current family result: exactly two fixed connected-component sources are necessary and sufficient for the entire admissible `(1,2,r)` family, within that explicitly restricted source model.

Open the [offline demonstration](../examples/compatibility-conformance/index.html), read its [reproduction instructions](../examples/compatibility-conformance/README.md), or inspect the [team reports](../reviews/2026-10-02-ultra-value-review/README.md). These are inspectable products of the collaboration. They do not establish external adoption, a new general solver, better AI memory, comparative productivity, or a solution to general Lonely Runner.

## What changed because of this review

| Result | Evidence earned | Limit |
| --- | --- | --- |
| Existing-tool integration example | SymPy 1.14.0 adapter: 10/10 complete-set agreements, 65 exact events, 120 original-predicate checks, deterministic replay and separate AI review | Known development cases; no external defect, consumer or performance advantage |
| Reusable conformance cases | Five archived failures extracted with exact physical references and executable source binding; eleven corruptions rejected; normal/optimized Python outputs match | Two point queries deliberately specialize archived source questions; faulty rules are teaching mutations |
| Stronger small mathematical statement | Reconstructed complete `(1,2)` core; speeds 6 and 8 prove no one-component menu suffices; existing interval-plus-point construction supplies two | Internally reviewed proof candidate for this source class and one reference; novelty unassessed |
| Sharper investment decision | Mature frameworks can supply or replace most required machinery; two completed handoff studies did not establish CC superiority | Useful local artifacts do not yet demonstrate benefits in an outside workflow |

## A real software contract, with a small working example

[SymPy's documentation](https://docs.sympy.org/latest/guides/solving/reduce-inequalities-algebraically.html#not-all-results-are-returned-for-periodic-functions) explicitly says that trigonometric inequality results are restricted to a periodic interval and must be extended by integer period shifts. That is enough information for a caller to reconstruct the full answer, provided the caller carries the period into the next operation.

The new example accepts a narrow structured fragment `f(pi*(a*t+b)) op c`, with rational positive frequency, rational phase, stated thresholds, exact endpoint flags and a bounded time horizon. It solves each atom separately, restores all required shifts, then intersects at the same time. A separately structured rational phase-event calculation supplies the complete-set reference. Exact substitution into the original trigonometric expressions checks every boundary and intervening cell representative; this is a finite event decomposition, not approximate time sampling.

Two results explain the use clearly:

| Asked question, in the normalized time variable t | Complete answer |
| --- | --- |
| `cos(pi*t)<1/2` with `2<=t<4` | `(7/3,11/3)` |
| `sin(pi*t)>=0` and `sin(pi*t)<=0` with `0<=t<=2` | `{0,1,2}` |

The first principal-period answer has no contact with the requested later horizon. Restoring its period recovers the interval. The second answer has no positive duration but contains three valid times. These are the same consequential distinctions encountered in the runner investigation, translated into an existing tool's documented contract.

This is ordinary correct period expansion and set intersection. The unexpanded output is a deliberately incomplete use of the API, not a fair competing algorithm or a SymPy bug. The useful deliverable is the scoped adapter, exact examples and checks. Whether it prevents an actual downstream mistake or saves anyone time remains to be measured.

The original ten-case implementation passed and reproduced. Review then caught an unexercised control-flow discrepancy: the protocol required stopping on unsupported/error, while the runner continued recording later cases. The corrected source, initial source, both reports and the development log are preserved. The final report also reproduced byte for byte in a separate AI review. No mathematical algorithm or case was retuned, and no final-source pristine-freeze claim is made.

## The research has a precise mathematical payoff

For the stationary-reference family

\[
(0,1,2,3,4,5,7,10,19,r),
\]

the first eight moving runners' complete closed 1/8-safe core is

\[
\{1/8,3/8,5/8,7/8\}\cup I\cup(1-I),
\qquad I=[25/152,7/40].
\]

Define one source to be one connected component of this fixed core, crossed with the added runner's safe phase interval. A source menu is fixed before r is known and contains no hidden fallback.

| Added speed | The two interval components | The four isolated components |
| --- | --- | --- |
| r=6 | Both fail | All succeed |
| r=8 | Both succeed | All fail |

Every one-component choice therefore fails for an admissible speed. The interval I together with the point 1/8 suffices for all admissible positive integer r: the point handles every r not divisible by 8; I handles 8 and 16; its width 1/95 handles every r>=24 because the added runner's open unsafe gap is at most 1/(4r). Thus **two is the exact minimum in this declared component-source class**.

This is a short counterexample-and-construction argument, not an extrapolation from a large box. Counting an arbitrary disconnected union as one source changes the question. The statement remains a proof candidate with separate AI review; it has not received independent human/formal certification or a novelty determination. The [mathematical report and standalone checker](../reviews/2026-10-02-ultra-value-review/math_audit.md) preserve its complete derivation and assumptions.

The review also found no fatal gap in the older 23-advance kernel argument. Its potential export is exact point feasibility for four open quarter-duty periodic blockers with arbitrary phases and real positive periods. Positive dwell time, jitter and ordinary scheduling change its hypotheses. Formalizing that narrow result is a possible future mathematical product, not a completed application.

## Which languages and technologies deserve a role?

LTCM means a language that carries models. There is no defined finite universe of all such languages, so the team compared nine relevant families rather than claiming exhaustive coverage. The [framework report](../reviews/2026-10-02-ultra-value-review/frameworks.md) records primary sources, translations and failure tests.

| Framework | Appropriate role | Boundary that matters here |
| --- | --- | --- |
| Exact intervals/event arrangements | Complete finite safe sets and reference checking | Construction cost grows; singleton points must survive |
| Polyhedra, integer lattices and tori | Shared constraints, lap geometry, actual-orbit relations | Saturation and physical recovery are essential |
| Quotient zonotopes/covering radii | Structural geometry when offset/covering quantifiers are relevant | All-offset coverage is stronger than common-start existence |
| SMT, Presburger sets, constraint programming | Fixed-input feasibility; exact finite source selection | Free speed times free time is not linear arithmetic; a time grid needs proof |
| Timed automata/temporal logic | Ordering, resets, deadlines and duration requirements | One simultaneous instant is not a job schedule |
| Abstract interpretation/refinement | Track sound approximations and repair a specific information loss | Marginal false positives and missing-source false negatives need different treatment |
| Relational queries/provenance | Shared identities, versions, dependencies and query adequacy | Provenance is not truth; a good SQL/type baseline is already strong |
| Proof assistants/certifying computation | Replayable soundness for a stable witness/recovery kernel | Correct source semantics and a small scope remain necessary |
| Other symbolic/probabilistic/geometric languages | Candidate generation or a specifically justified new bound | An analogy or new notation alone supplies no result |

CC should be allowed to disappear into simpler conventional machinery whenever that preserves the question better. The SymPy adapter is an example: it uses established operations directly. The contribution is a concrete checked bridge and failure explanation, not ownership of the underlying mathematics.

## What to try next, and what to stop

**First: test usefulness with one actual consumer task.** Give a technically interested reader the runnable example and ask for one periodic-condition task they already need to solve. Pin its raw input, requested output, a competent ordinary period-expansion/direct-interval baseline, and a time budget before evaluation. Measure correct complete answers, unsupported claims, setup/debugging burden and whether a specific error is prevented. A clean synthetic pass is not this test. No outside person was contacted in this review.

**Second, if pursuing mathematics: make a finite selection decision with a proved tail.** On already exposed pairs `(1,4)` and `(1,6)`, retain the current widest component and decide whether one additional component covers every low-r exception. Their width cutoffs give tails at 35 and 33. An exact finite coverage table can prove or refute this leader-constrained two-source claim; ordinary set-cover methods suffice. Stop after those two decisions unless the result yields a symbolic structural criterion. This proposal is unrun.

**Third, if assurance is the goal: formalize one stable lemma.** A physical witness-checker soundness lemma or the quarter-duty point-feasibility kernel would be useful if it is completely replayable in an established proof assistant. Do not attempt to formalize the whole evolving research archive at once. This is also unrun.

Stop generic CC-versus-checklist reruns: the presentation pilot did not show a robust advantage, and the authoring comparison gave CC 17/18 versus 18/18 for both strong conventional and full-source controls. Preserve the null evidence. Stop larger speed boxes without a structural question, new language layers without a needed operation, and instantaneous timing demonstrations presented as robust schedules. Real TSN schedule checking is a plausible future application only after duration, queues, routes, deadlines and jitter semantics are modeled; it was not attempted here.

## What this demonstrates about the partnership

The reproducible sequence is the product: a person directs an inquiry, a model makes a checkable claim, exact counterexamples expose omissions, established tools supply better representations, implementations are challenged by separate reviewers, and corrections remain visible. A reader can inspect the evidence and repeat the checks without trusting an assistant's confidence.

That is a bounded demonstration of what this collaboration accomplished. It does not show that the result was impossible for one person, that AI caused a measured productivity gain, or that another user has benefited yet. The next useful advance is another person's successful use or a sharper independently reviewed theorem. The current artifact makes either possible without requiring a grander claim.
