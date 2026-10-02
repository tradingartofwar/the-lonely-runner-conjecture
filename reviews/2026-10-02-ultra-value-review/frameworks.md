# Framework review: make CC replaceable and compare the actual operation

2026-10-02 UTC. Reviewed repository HEAD `29e54d32e2ff5349bdb0c3db56fab753a0e44c94`; the working tree was initially clean. AI-assisted internal assessment. No solver experiment, mathematical search, independent proof verification, installation, or external application was performed. Proposed tests below are **UNRUN**. Existing finite results remain **OBSERVED**; unbounded arguments retain their recorded proof-candidate status.

## Assessment

The strongest near-term use of CC is as a **replaceable, question-specific interface between models and independently checked answers**. Its concrete assets are exact counterexamples, explicit physical recovery, and a record of which compression failed. The record does not establish a new general calculus or an advantage over strong conventional reasoning. The completed authoring comparison supplies no observed CC advantage; that result should affect investment, not merely be acknowledged.

The October 2 repair already moves toward an established representation: exact closed intervals on the physical orbit, plus isolated points and all clock lifts. Calling that representation CC adds no computational guarantee. Recovering the omitted continuous choices is a substantive improvement: all 36 old sheets miss `(1,2,40)`, while the physical interval contains `25/152`. Similarly, the fresh `(1,4,13)` failure of positive-only sources shows why endpoint semantics cannot be optional. These facts favor keeping several interoperable representations, with the simplest one responsible for each operation.

This is a broad map of relevant framework families, **not a claim to have considered every possible LTCM**. “Language That Carries Models” is a useful project umbrella; no precise universe of such languages is specified here, so literal exhaustive coverage would be undefinable. In particular, model expressiveness, effective computation, a small certificate, readable explanation, and human usefulness are different comparison axes.

## A common semantic contract

For fixed integer moving speeds `v_i`, a selected reference, common start, threshold `δ∈(0,1/2]`, and one unit period, exact feasibility is

`∃ t∈[0,1], ∃ m_i∈Z: δ ≤ v_i t − m_i ≤ 1−δ for every i`.

This formula is mixed linear integer/real arithmetic **when the speeds are fixed constants**. It preserves one shared time and closed equality automatically. Rational offsets can be added as constants, but that changes the physical problem and must be labelled. When both `v_i` and `t` are unknown, `v_i*t` is bilinear; the fixed-instance encoding does not become a uniform Presburger proof of a parameter family. No finite solver comparison proves all instances without a separately justified reduction.

The output contract must separately request existence, one time, optimum, all maximizers, or the complete feasible set. A `sat` witness is not a complete safe set. An empty selected menu is not `unsat`; a timeout is neither. Whatever language produces a candidate, substitute its exact time into **the original** speeds, phases and requested point constraints. Preserve the source pin and mapping: a safe time for another phase point does not answer a requested point-recovery question.

## Framework map

### 1. Exact rational intervals and event arrangements — default reference representation

**Translation and retained information.** For positive `v`, a fixed lap gives the closed interval `[(m+δ)/v,(m+1−δ)/v]`; intersect finite unions over runners on `[0,1]`. Keep singleton intersections and endpoint flags. This is the mathematical baseline already present in the repository, now also embodied by the orbit-interval construction. It represents the complete physical safe set, hence existence and a recoverable time. A separate piecewise-linear maximum calculation addresses optimization.

**Omissions and comparator.** A list for one input does not explain a uniform family or yield a speed-independent operation bound. Event count and rational bit lengths matter. Mature exact arithmetic and geometry libraries can supply primitives; CGAL documents exact rational number types [P1], but a general two-dimensional arrangement package is unnecessary for a one-dimensional interval oracle. The strongest comparator is a short independently structured rational band-intersection implementation, already used in this project.

**Small failure test.** Require exact union equality, not just one witness, on `(1,4,13)`, `(1,2,40)`, and a nonprimitive case with several clock lifts. Deliberately drop singleton components or one lift and require the comparison to identify the lost set. This tests an adapter; repeating previously successful agreement is not a new scientific outcome.

### 2. Polyhedra, integer lattices and fixed tori — direct mathematical predecessors

**Translation and retained information.** With `Bδ=[δ,1−δ]^k`, the lap vector satisfies `m∈(R v−Bδ)∩Z^k`; physical recovery additionally keeps `tv=m+f`. This is the threshold-generalized form of Beck–Hoşten–Schymura's equation (5)/Proposition 1, read here in §2 [P2]. For a coefficient family `v=A p`, fixed safe cells in phase coordinates and the exact subtorus/orbit constraints separate geometry from parameter arithmetic. Keep the **full saturated** integer relation lattice and the inverse clock/lap map. SageMath supplies integer-matrix saturation and Smith/Hermite operations [P3]; those are candidates to replace bespoke relation machinery, with adapter tests.

**Omissions and comparator.** Geometry without the actual orbit proves only relaxed feasibility. Marginal projection intervals discard the common point; an unsaturated relation set admits extra components. Jain–Kravitz's fixed-torus relative-spectrum framework is a close predecessor [P4]. Its Proposition 7.1 concerns segments in the *ambient optimal locus*; CC's merely threshold-safe segments do not inherit its finite-spectrum conclusion. PPL already supplies rational polyhedra, congruence grids, finite powersets/products and exact-arithmetic mixed integer optimization [P5]. Replacing custom clipping with a tested PPL adapter is a real engineering change; renaming a polytope is not.

**Small failure test.** Rebuild one supplied cell and one append operation with the existing exact inequalities. Compare complete vertices/faces or feasible unions, including zero-dimensional pieces. Then reject the archived false orbit point `(1/4,7/8,1/8)` for rates `(2,3,1)`: its two raw relations pass, but `−x+y−z=1/2` fails the required relation. Report adapter work and dependencies, not only clipping time.

### 3. Quotient zonotopes and covering radii — relevant when the quantifier changes

**Translation and retained information.** Project `Bδ` to `R^k/Rv`, carrying the projected integer lattice and any offset. An integer hit of the appropriate projected translate corresponds to physical feasibility; retain a lift to recover `t`. Requiring every offset to work becomes a lattice covering question. Henze–Malikiosis supply the view-obstruction/zonotope connection [P6]; the recent Alcántara–Criado–Santos paper reports a computational shifted-runner application [P7].

**Omissions and comparator.** A covering radius addresses all translations, a stronger quantifier than this project's common-start existence question. A numerical radius or projected point does not retain a clock witness. Dimension and covering computations can be expensive. Use the existing zonotope literature or implementations only when a covering bound can discharge a stated obligation; do not import a shifted result into an unrelated common-start construction.

**Small failure test.** For two tiny fixed speed vectors, reconstruct the quotient lattice and verify both directions of the projected-point/physical-time mapping, including an offset and a boundary hit. Stop if this produces only the same certificate with more machinery. Neither cited paper's algorithm or certificates were run here.

### 4. SMT, Presburger sets, and constraint programming — complementary tools, different domains

**Translation and retained information.** Direct-time SMT uses the common contract above. Z3's mathematical integer/real arithmetic is a mature comparator [P8]. It can replace custom fixed-input feasibility search; retain its model as a candidate and verify it directly. For fixed-coefficient integer constraints on lap labels, residual directions and residue classes, isl offers exact set/relation operations and affine integer-division notation [P9]. CP-SAT is suitable for the *finite source-selection problem*: Boolean `z_j` selects source `j`, and `Σ_{j covers c} z_j≥1` enforces each explicitly enumerated case `c` [P10].

**Omissions.** A pure integer time grid requires a proved sufficient denominator/event reduction; arbitrary discretization loses isolated or narrow solutions. CP-SAT's integer variables do not directly model arbitrary continuous time. Plain Presburger constraints do not allow a free parameter times a free time/lap variable. Solvers may return unknown or hit budgets, and one witness does not prove a full atlas or all-parameter coverage.

**Small failure test.** Compare direct-time and phase-coordinate SMT on the three archived distinct compatibility regressions, with their exact requested points/segments intact. The known lost lift must distinguish `3/16` from `11/16`. For one finite contact table, ask CP-SAT for a minimum source menu and verify coverage and the claimed lower bound independently; a greedy menu comparison alone does not establish optimality. Use the prior 72-case proposal only if there is a real adapter to validate.

### 5. Timed automata and temporal logic — useful for sequences or dwell time, unnecessary for one instant

**Translation and retained information.** A fixed rational-rate phase can be represented by a clock measuring time since its last wrap, reset each period; scale all rational guard constants exactly. Reachability of a state where all phase predicates hold asks for a simultaneous instant. A duration requirement instead needs the whole interval to remain safe; sequences, resets, deadlines and recurring obligations require genuinely richer state/temporal semantics.

**Omissions and comparator.** UPPAAL's ordinary symbolic semantics increments every clock at unit rate [P11]. Encoding phase directly as a clock with arbitrary derivative is not an automatic use of that exact symbolic engine; its statistical/hybrid path uses numerical simulation and has different guarantees. A true statement such as “eventually all safe” also depends on the specified run/time semantics. Ordinary instant feasibility does not justify a claim about scheduling jobs or tolerating jitter.

**Small failure test.** Encode the equality-only `(1,4,13)` case twice: instantaneous reachability should succeed; any positive dwell-time claim at threshold `1/8` should fail. Require exact trace-to-time translation. Adopt this framework only if a real question adds ordering, duration or reset behavior that the direct-time formula lacks.

### 6. Abstract interpretation and refinement — distinguish overapproximation from missing witnesses

**Translation and retained information.** An abstraction can carry a relation between concrete physical states and cheaper abstract objects, together with proved sound operations. Polyhedra/grids offer relational abstract domains [P5,P12]. CC's independent marginal intervals are an overapproximation: they can admit a spurious compatible point. Its safe source menu is an underapproximation: it can miss real witnesses. These have opposite failure directions.

**Omissions and comparator.** Classical CEGAR refines a spurious abstract counterexample in a suitable verification model [P13]. Restoring omitted safe intervals is not automatically that algorithm, and its termination/completeness theorems are not inherited. A serious adaptation must define concretization, soundness and the actual refinement operation. Calling all recovery “CEGAR” obscures the very distinctions CC seeks to retain.

**Small failure test.** Use one marginal false positive and `(1,2,40)` as a paired test. The system must reject the false point in the first and restore a missed witness in the second, without declaring physical infeasibility on menu exhaustion. Adopt a new abstract domain only if it makes one of these operations cheaper or mechanically sound.

### 7. Query determinacy, relational data and provenance — existing semantics for the handoff contract

**Translation and retained information.** For a source `d`, summary `S`, and query `Q`, adequacy means `S(d1)=S(d2) ⇒ Q(d1)=Q(d2)`. This is the determinacy idea studied by Nash–Segoufin–Vianu [P14]. Store occurrence IDs, source versions, uncertainty, and relation keys, not disconnected marginal facts. PROV-DM can represent entities, derivations and revisions [P15]. Exact relational joins can enforce a common occurrence; they cannot infer that missing evidence is false.

**Omissions and comparator.** Determinacy does not guarantee an efficient rewriting in a chosen language. A provenance graph says where a statement came from, not that it is true or adequate. The best comparator for user-facing summaries remains a well-designed ordinary handoff with identical source access and budgets. The completed studies have not shown CC superiority; more renamed fields or ontology layers are not evidence of improvement.

**Small failure test.** Preserve the physical 1680/3360 pair: identical duration summaries, different local nonemptiness. The answer must say the summary is insufficient or recover endpoints. Separately preserve “a witness exists” versus “a different witness exists,” the observed handoff error. Run another human/AI study only on a concrete workflow deficit with a new outcome, not to seek a better CC score.

### 8. Proof assistants and certifying computation — strengthen trust in a narrow kernel

**Translation and retained information.** Formalize exact input semantics and prove `checker accepts ⇒ original physical predicate`, with explicit representation/decoding obligations. Alkassar et al. distinguish checker correctness, abstraction correctness and the witness property [P16]. Lean, Isabelle/HOL or Rocq can host such a development; Lean's official documentation explains kernel-checked proof terms and trust boundaries [P17]. A mathematical witness generator can remain untrusted.

**Omissions and comparator.** Formalizing the wrong threshold, reference or quantifier proves the wrong theorem. A formal checker for one time does not prove the producer complete or a family covered. Native evaluation and admitted axioms require a declared trust boundary. Formalizing the entire evolving CC stack before isolating a stable contract risks expensive proof maintenance.

**Small failure test.** Prove soundness of a rational time/lap checker and a separate normalized-clock recovery lemma. It must reject corrupted laps, a wrong clock, missing required runner data, and open/closed-boundary changes. Pin the toolchain and audit axioms. A complete replayable theorem is the payoff; a tactics transcript with gaps is not.

### 9. Other plausible paradigms — retain them as conditional leads

Finite SAT/BDD encodings can represent a proved finite event partition or contact table, and category-theoretic language can describe commuting translations. Neither supplies the missing partition, saturation, recovery or covering theorem merely by naming it. Fourier/Diophantine methods and relative spectra may supply structural inequalities; the earlier Ultra assessment already found examples where valid short-relation bounds added no useful restriction. Probabilistic/factor-graph marginals are especially poor substitutes for exact zero-measure witnesses. Simulation, optimization heuristics and AI search can propose candidates, followed by exact certification.

The common small test for an additional paradigm is demanding: translate one declared query in both directions, reproduce its known counterexample and deliver **one new bound, simpler proof, verified operation, reduced total cost, or measured user benefit**. Otherwise it remains an analogy. No quantum, causal, information-theoretic or universal-compositional advantage follows from this record.

## Ranked next directions — three, with stopping rules

| Rank | Concrete work and nontrivial payoff | Cost and falsifiable gate |
| --- | --- | --- |
| 1 | Extract the three exact adapter regressions, preserving their original queries; pair a direct-time rational oracle with one solver-backed adapter. CC becomes replaceable. Useful payoff: find an actual translation defect, remove custom machinery while retaining semantics, or give a downstream frontend a reusable conformance test. | Start with the prior proposed four-person-hour implementation cap, one pinned solver, no broad benchmark. Charge parsing, source construction, recovery and checking. A clean three-case pass is bounded conformance, not superiority. Stop at the small pack if there is no real consumer or simpler replacement. |
| 2 | Review the two-source `(1,2,r)` argument, then turn the small-source question into an explicit finite coverage problem under a proved tail rule. Compare exact optimization with greedy selection. Useful payoff: a source-relative minimality result or a reusable sufficient criterion retaining phase alternatives. | For one supplied interval width `w>0`, `r*w≥2δ` guarantees contact with a closed safe band: an unsafe open gap has length `2δ/r`. At `w=1/95,δ=1/8`, the tail starts at `r=24`. Require a declared leader, solve the finite lower-r contact table including singletons, and prove optimality only under that source/leader contract. This elementary reduction is an adaptation, not claimed new mathematics. Stop after a bounded derivation/challenge cycle if it only reproduces a known menu without a stronger guarantee. |
| 3 | Formalize one stable physical-witness/recovery kernel in an existing proof assistant; keep discovery independent. Useful payoff: independently replayable soundness of an exported certificate format, with semantic mutation controls. | Higher upfront cost; scope to one lemma and checker, not all historical proofs. Freeze a time budget before implementation. Pass requires complete proof, decoded statement review and trust/axiom audit. Stop or shrink if infrastructure dominates and no reusable theorem is completed. |

The second track concerns research; the first and third concern reliability and reuse. They should not be aggregated as progress toward arbitrary-runner LRC. A new diagram, another successful tuple, or a larger held-out box alone passes none of these gates. Human empowerment here means a person can inspect the claim, run or replay the check, understand its limits, and replace the machinery without losing the result.

## Reading and verification limits

Read AGENTS, CLAIM_STATUS and CONTRIBUTING; reviewed the current README/HANDOFF sections, LR4_HANDOFF, all numbered CC representation-rule sections, the September 29 assessment and LTCM review, September 30 transfer assessment, and both October 2 sheet/interval notes. README/HANDOFF are long cumulative histories: current sections and relevant historical entries were inspected, not every old paragraph. RESEARCH_PLAN, MATHEMATICAL_BASELINE and SOURCES were consulted selectively. Some initial combined reads were truncated; later focused reads recovered the representation rules and current findings. No claim of exhaustive repository reading, code audit, certificate reproduction, or full-paper proof review is made.

The report's mathematical translations and proposed test designs are the reviewer's deductions. Literature sources support the named comparators; they do not establish CC's correctness or novelty. All external sources below were checked on **2026-10-02 UTC** using primary papers, authors' pages, standards or official documentation. Mutable documentation is a capability snapshot, not a pinned executable release. No cited software was installed or benchmarked.

## Primary sources and inspected scope

| ID | Source/version and URL | Reading limit and use |
| --- | --- | --- |
| P1 | CGAL, *Number Types* manual, displayed 6.2.1: <https://doc.cgal.org/latest/Number_types/index.html> | Exact-number-type description; no library build or geometry benchmark. |
| P2 | Beck, Hoşten, Schymura, *Lonely Runner Polyhedra*, Integers 19 (2019), A29: <https://math.colgate.edu/~integers/t29/t29.pdf> | §2, equation (5), Proposition 1, adjoining projected-lattice construction; not the whole proof package. |
| P3 | SageMath integer matrix reference: <https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html> and <https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_sparse.html> | Saturation and Smith-form API descriptions; no claim about a particular installed release. |
| P4 | Jain, Kravitz, *Relative Lonely Runner spectra*, Combinatorial Theory 6(1) (2026), #1: <https://escholarship.org/content/qt3mx8w3js/qt3mx8w3js.pdf> | Abstract, §7 Proposition 7.1 and its forward proof, printed p.45; §6 context from prior repository reviews. No whole-paper reproduction. |
| P5 | BUGSENG, PPL official description: <https://www.bugseng.com/ppl/>; technical capability page <https://support.bugseng.com/ppl/> | Polyhedra/grids, powersets/products and exact MIP capabilities. Historical support-page news is not a current release claim. |
| P6 | Henze, Malikiosis, *On the covering radius of lattice zonotopes…*, arXiv:1609.01939; journal Aequationes Math. 91 (2017): <https://arxiv.org/abs/1609.01939> | Abstract; the exact quotient relation here also checked in P2 §2. No covering theorem proof audited. |
| P7 | Alcántara, Criado, Santos, *Covering radii of 3-zonotopes and the shifted Lonely Runner Conjecture*, arXiv:2506.13379, initially 2025-06-16: <https://arxiv.org/abs/2506.13379> | Abstract and reported application/algorithm only; no certificate or executable audit. |
| P8 | Official Z3 guide, *Arithmetic*: <https://microsoft.github.io/z3guide/docs/theories/Arithmetic/>; SMT-LIB logic catalog <https://smt-lib.org/logics.shtml> | Integer/real sorts, linear fragments and nonlinear boundary; no performance guarantee. |
| P9 | Sven Verdoolaege, isl manual, displayed version 0.28: <https://libisl.sourceforge.io/user.html> | Set/relation description, affine integer-division input, projection and parametric-vertex descriptions; not all manual sections. |
| P10 | OR-Tools, *CP-SAT Solver*: <https://developers.google.com/optimization/cp/cp_solver/> | Integer-only modeling and distinct solver statuses; exact continuous-time reduction is our additional obligation. |
| P11 | UPPAAL, *Semantics*: <https://docs.uppaal.org/language-reference/system-description/semantics/> and *Locations*: <https://docs.uppaal.org/language-reference/system-description/templates/locations/> | Unit-rate delay semantics, SMC limitations and hybrid-clock warning; no model executed. |
| P12 | Patrick and Radhia Cousot, POPL 1977, authors' abstract/overview: <https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml> | Summary and section outline; no full abstraction proof imported. |
| P13 | Clarke et al., *Counterexample-guided Abstraction Refinement*, CAV 2000: <https://web.stanford.edu/class/cs357/cegar.pdf> | Abstract, introduction, finite-state setup and abstraction statement; no automatic transfer of guarantees to CC. |
| P14 | Nash, Segoufin, Vianu, *Views and Queries: Determinacy and Rewriting*, ACM TODS 35(3), July 2010: <https://cs.uwaterloo.ca/~gweddell/cs798/a21-nash.pdf> | Abstract and introductory determinacy/rewriting distinction; no current open-problem-status claim. |
| P15 | W3C, *PROV-DM*, Recommendation 2013-04-30: <https://www.w3.org/TR/2013/REC-prov-dm-20130430/> | Entity/activity, derivation and revision definitions; provenance is not semantic certification. |
| P16 | Alkassar et al., *Verification of Certifying Computations* (2011): <https://www.mpi-inf.mpg.de/~mehlhorn/ftp/VerificationCertComps.pdf> | Abstract, introduction and §2 checker/abstraction/witness obligations. |
| P17 | Lean official reference, *Validating a Lean Proof*: <https://lean-lang.org/doc/reference/latest/ValidatingProofs/> and *Tactic Proofs*: <https://lean-lang.org/doc/reference/latest/Tactic-Proofs/> | Kernel acceptance, assumptions/axioms and native-evaluation trust caveats; pin a release before any implementation. |
