# Ultra team brief: what is useful beyond Lonely Runner?

Prepared September 30, 2026 at Vance's request. **Status: review brief, not a
completed assessment.** This document makes no new application or novelty claim.

Repository: `tradingartofwar/the-lonely-runner-conjecture`.
Branch: `research/near-doubling-overlap-2026-09-24`.
Review the research through immutable source commit
`52c4912a89e4c314201e66e7fa94da7fa3366964`.
The accompanying [source index](../reviews/2026-09-30-ultra-transfer-brief/SOURCE_INDEX.json)
lists every tracked file and its Git identity at that checkpoint. Later work,
if consulted, must be dated and separated from this baseline.

## The question from Vance

Go through our work up to this point and ask:

> What have we learned that could be useful in any other human endeavor?
> Could a result, method, failure, representation, or way of working help
> with another known problem or an unanswered question? Did we find anything
> useful even if it does not lead to a Lonely Runner proof?

Interpret this generously in scope and strictly in evidence. Consider
mathematics, computation, science, engineering, organizational decisions,
communication, learning, and human–AI collaboration. Look for unexpected
connections as well as obvious ones. Do not confine the review to the latest
two- and three-parameter experiments, or to defending Compatibility Calculus.

The desired product is a candid assessment of transferable value, including
specific opportunities worth testing. A familiar principle with a useful
implementation, teaching example, or diagnostic can have value without being
novel. Finding no demonstrated external application is an acceptable result.
Do not make a famous open problem the price of admission for usefulness.

## Evidence and working method

Begin with AGENTS.md, CLAIM_STATUS.md, README.md, HANDOFF.md, RESEARCH_PLAN.md
and notes/CC_REPRESENTATION_RULES.md at the pinned commit. Historical LTCM
names belong to the record; the current language is Compatibility Calculus
(CC). Its working purpose is to carry the question, joint constraints,
consequential distinctions, evidence, and recovery maps across representations.
Assess whether that purpose is actually fulfilled; do not treat the name as
evidence that a new mathematical framework exists.

Inventory the entire research trajectory before choosing highlights. Use the
source index and handoff to locate code, frozen protocols, proof candidates,
corrections, exact outputs, reviews, inquiries and visual explanations.
Follow claims back to their evidence. A review note is not a substitute for
its underlying argument or counterexample when the claim matters.

Maintain a coverage ledger: which research clusters were examined directly,
which were inspected only through summaries, which computations were rerun,
and what remains unexamined. Do not say every artifact was independently
verified merely because its filename appears in the index.

If team delegation is available, use complementary first passes: mathematical
mechanisms and prior art; algorithms and possible engineering transfer;
representation/decision/information-loss lessons; and an adversarial reviewer
challenging each proposed application. Allow findings outside those tracks.
Reconcile disagreements explicitly. Disclose actual models, tools, shared
sources and dependencies; agreement among AI reviewers is not human or formal
certification. This brief does not itself launch or impersonate an Ultra team.

## Entry points across the full trajectory

These are navigation aids, not a preselected verdict or an exhaustive reading
list. Check the surrounding packages and historical corrections.

| Research cluster | Primary entry points under `notes/` | What to investigate |
| --- | --- | --- |
| Original cross-domain translations | DOMAIN_CONNECTIONS.md; MATHEMATICAL_BASELINE.md; SOURCES.md | Which translations preserve the actual question, and which only change notation? |
| Overlap and local placement | BLOCKING_OVERLAPS.md; LOCAL_OVERLAP.md; OVERLAP_PLACEMENT.md; SPEED_RATIOS.md | Why aggregate amount or global redundancy can fail to locate a useful opening. |
| Distinctions and summary collisions | DISTINCTION_AUDIT_2026_09_25.md; CONTACT_MOMENTS_2026_09_27.md; inquiries/2026-09-28-configuration-relational-information.md | Same summaries with different arrangements; question-specific sufficiency and irrelevant detail. |
| Occurrences, compatibility and equality | LAP_LABELLED_CONSTRAINTS.md; LOCAL_TILING_RULE.md; FOUR_BLOCKER_CYCLE_CORRECTIONS.md | Shared occurrences, same-point constraints, boundary witnesses and misleading relaxations. |
| Exact selection and its failures | EXACT_INTERVAL_CRITERION_2026_09_28.md; DIRECT_LAP_PROJECTION_2026_09_28.md; FOUR_RUNNER_PROJECTION_LIMIT_2026_09_28.md; FINITE_ANCHOR_OBSTRUCTION_2026_09_28.md | Constructive selection, failed fixed-step extrapolation and recoverable certificates. |
| Chain, averaging and termination arguments | BLOCKING_CHAIN_TERMINATION_2026_09_28.md; UNIFORM_CHAIN_BOUND_2026_09_28.md; EXPLICIT_CHAIN_BOUND_2026_09_28.md; SHORT_KERNEL_BOUND_2026_09_28.md | Whether any mechanism transfers under its actual duty, phase and interval hypotheses. |
| Structural limits and prior assessments | CORE_WINDOW_REDUCTION_2026_09_29.md; LAST_RUNNER_COMPATIBILITY_2026_09_29.md; ULTRA_ASSESSMENT_2026_09_29.md | Missing existence-to-selection bridges, overly strong requirements and previously identified portable mechanisms. |
| Fixed geometry, spectrum and arithmetic | LTCM_EXACT_SPECTRUM_2026_09_29.md; LTCM_ULTRA_REVIEW_2026_09_29.md; CC_TWO_PARAMETER_WITNESS_2026_09_29.md; CC_LITERATURE_COMPARISON_2026_09_29.md | Compact exact objects, integer compatibility, physical recovery, and established precedents. |
| Discovery, compression and transfer | CC_COVERAGE_COMPILER_2026_09_29.md; CC_SELECTOR_SUPPORT_2026_09_29.md; CC_ROW38_COEFFICIENT_RANGE_2026_09_29.md | Operational support, quantifier changes, finite certificates and failed selector transfer. |
| Restricted discovery and selective recovery | CC_PHASE_SCREEN_2026_09_29.md; CC_HYBRID_RECOVERY_2026_09_29.md; CC_HYBRID_TRANSFER_2026_09_29.md; CC_BOUNDARY_TRANSFER_2026_09_29.md | Soundness versus completeness, restoring omitted alternatives, and costs of recovery. |
| Independent third parameter | CC_THREE_PARAMETER_TEST_2026_09_30.md and its review package | Joint lattice contact, clock lifts, higher-dimensional objects, and the failed held-out compact menu. |
| Communication and collaborative process | CC_REPRESENTATION_RULES.md; CC_VISUAL_PRESENTATION_PLAN_2026_09_29.md; inquiries/README.md; `visuals/compatibility-calculus/` | What explanations or workflows make evidence easier to inspect, and what remains only an attractive narrative. |

## Questions the review should answer

1. What are the strongest actual lessons, including negative findings? Give
   exact examples and their limits. Recover older useful results that recent
   momentum or compression may have obscured.
2. Which ideas are established elsewhere, useful adaptations, possible new
   results, explanatory devices, or unsupported speculation? Separate usefulness,
   correctness, novelty, scalability and significance instead of combining them
   into one favorable judgment.
3. What survives after removing Lonely Runner's special assumptions? Identify
   precisely which mechanisms need common start, periodicity, integer speeds,
   low-rank coefficient structure, convexity, closed boundaries, exact arithmetic,
   or a pre-existing source atlas. State what breaks when each is removed.
4. Could any mechanism address a concrete problem in another domain? Name the
   task, the present obstacle, and the change our approach might make. A loose
   analogy is a lead, not an application.
5. Could it illuminate a named unanswered question? Verify that question's
   current status from primary sources. Explain whether our work supplies an
   exact reformulation, a conditional lemma, a diagnostic, a heuristic, or an
   actual new implication. Show the missing bridge rather than implying a proof.
6. What should we stop doing, simplify, replace, or combine with an established
   method? Actively consider alternatives to CC and the possibility that the
   most useful result is a small tool or discipline rather than a new language.

Possible places to look, after extracting the mechanisms from the record,
include constraint solving, scheduling, verification, model reduction,
scientific summaries, knowledge management and AI context retention. These
are search leads only. Do not force a match or limit the review to this list.

## Required evidence for a proposed transfer

For each serious candidate provide a compact transfer record:

| Field | Required content |
| --- | --- |
| Origin | Exact source file, claim, certificate or counterexample in this repository; status and assumptions. |
| Mechanism | A precise statement of what does the work, stripped of project-specific names. |
| Destination | A concrete external task or precisely stated unanswered question. |
| Translation | Map source objects, operations, constraints and requested outputs to the destination. Identify any information discarded. |
| Inherited and new obligations | Which guarantees survive the map, and which require another argument or evidence? |
| Existing approach | The closest established method or result, with primary sources and an honest account of what was read. |
| Added value | A specific expected benefit: reliability, computation, explanation, recoverability, or a new restriction. Say when it merely restates the baseline. |
| Failure test | A counterexample or observable outcome that would defeat the proposed transfer. |
| Smallest useful test | Fixed inputs, comparator, budget, success measure and failure interpretation, declared before execution. |
| Assessment | Demonstrated utility, supported hypothesis, analogy only, known technique, or rejected lead; state uncertainty plainly. |

The key demand is a checkable bridge from this record to another task.
Preserving joint feasibility in a mathematical toy does not establish better
real-world decisions. Faster runtime on our inputs does not establish general
complexity. A lossless answer for one question may be inadequate for the next.

Browse primary literature when checking external claims, novelty, technical
comparators or the current status of open problems. Give exact versions and
reading limits. If access is unavailable, label the connection unverified;
do not turn a remembered resemblance into a sourced conclusion.

## Distinctions that must not be lost in this review

- Duration, existence, topology, location and equality cases are different
  outputs. Complete joint durations can determine total uncovered duration
  without retaining where it occurs. Some archived obstructions are abstract
  event arrangements; others are actual common-start runner configurations.
- A sound sufficient screen may be incomplete. A failed selected menu, a miss
  by its whole candidate class, physical nonexistence, and budget exhaustion
  require different conclusions.
- One witness, every witness, an optimum and the complete safe set have
  different information requirements. Stronger auxiliary obligations can
  unnecessarily reject a valid answer to the original question.
- The last test raised coefficient-family rank to three by adding free r;
  each fixed integer instance still has a one-dimensional orbit. It retained
  product geometry and did not test arbitrary mixed-r families.
- Four sheets covered 89/89 training and 310/318 held-out cases; all 36 sheets
  covered all 407. Preserve the eight menu failures. Do not describe a repaired
  menu or the larger source class as success of the frozen compact transfer.
- Frozen protocols, separate implementations, exact reproduction, independent
  reviewers and external/formal verification are different evidence levels.
  The latest three-parameter checker shares the author's provenance.
- An empty successful diagnostic does not validate an unexecuted branch.
  Repeated summaries must not silently promote proof candidates to theorems.

Challenge these formulations if the underlying record warrants correction.
Preserve the correction and its source rather than harmonizing it away.

## Requested deliverables and decision

Return a short plain-language assessment to Vance first: what appears useful,
what has actually been demonstrated, and what should be tested next. Be direct
if the useful lessons are primarily known methods, disciplined practice, or
educational examples rather than new mathematical results.

Provide a ranked table of the strongest candidates. Favor three to five
well-supported candidates over a long list; return fewer if fewer qualify.
Include at least one practical task if a credible candidate exists, and
consider a named open question only if a precise connection can be supported.
For the best one or two candidates, provide the transfer records above and a
small reproducible demonstration or an explicit unrun test design. Freeze any
new test before running it. Keep reused data separate from fresh validation.

Also include the coverage ledger, prior-art map, rejected/weak connections,
important disagreements, any missed information recovered from older work,
and the strongest reason the preferred proposal might fail. Recommend one
next action proportional to the evidence and expected value. Do not propose
several large new projects merely to keep momentum going.

Suggested result path:
`notes/ULTRA_TRANSFER_VALUE_ASSESSMENT_2026_09_30.md`, with supporting files
under `reviews/2026-09-30-ultra-transfer-value/`. This is a requested future
output, not a file or review that already exists. Preserve original research
packages and use the existing research branch. No outside messages, paid
compute, broad unattended searches, main merge or public claims elsewhere.

The final assessment should let us distinguish three honest answers:
**already useful in a specific way; promising enough for a specified test;
or interesting, but no demonstrated practical or theoretical transfer yet.**
