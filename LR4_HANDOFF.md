# LR 4 — recovered research state

October 1, 2026. AI-assisted continuity audit and next-step recommendation.

**Later LR 4 update:** the [long-history authoring study](notes/CC_HANDOFF_AUTHORING_STUDY_2026_10_01.md) now has a concrete protocol, six synthetic histories, eighteen hidden questions, matched authoring instructions, fixed schedules and a passing same-author static preflight. All model trials remain UNRUN. The next step is separate source-first key review and recorder preparation, then materials review and an execution freeze. The earlier recommendation below is preserved as its starting point.

## Resume here

The final LR 3 handoff experiment **finished and was saved**. Its result commit is `9cfe6cb7d52a81e56357c0e11a0f44743e4dcbf2`, published at 08:47:48 America/Los_Angeles on October 1. Do not resume collection from an intermediate 20/40/60-trial checkpoint or rerun the completed pilot.

The active research branch is `research/near-doubling-overlap-2026-09-24`. The canonical `main` branch was still at `c8a287f52ef0066d2ba6247094bdeba023825081` when this audit began; inspecting only `main` would miss the subsequent research. The branch is saved remotely but has not thereby been merged into `main`.

Start with the [pilot result report](reviews/2026-10-01-cc-handoff-pilot/RESULTS_REPORT.md), [grading adjudication](reviews/2026-10-01-cc-handoff-pilot/ADJUDICATION.md), and [longer research handoff](HANDOFF.md).

## What the interrupted work established

The question was whether CC-informed handoffs help recipients preserve consequential distinctions better than equally concise, strong conventional handoffs. The frozen pilot gave both formats identical factual statements and source access. It varied labels, grouping and order, then tested ten synthetic cases in four repetitions per format.

| Outcome | CC-informed | Conventional |
| --- | ---: | ---: |
| Completed trials | 40/40 | 40/40 |
| Correct requested decisions, witnesses and counts | 40/40 | 40/40 |
| Strict full-answer successes | 38/40 | 37/40 |
| Unsupported approvals | 0 | 0 |
| Source requests | 32 | 32 |

The strict difference comes entirely from five M2 explanations that say **another policy** covers a case when the evidence establishes only **a policy**. The policy might be the very one whose evaluation is incomplete. All five answers correctly retain the requested validation counts and uncertainty. A permissive reading gives 40/40 in each format; penalizing only explicit distinct-existence assertions gives 39/40 each. Preserve the strict primary score and these sensitivities together.

**Conclusion:** this pilot does not establish a robust CC presentation advantage. It does not establish that CC is useless. It leaves summary authoring from longer histories untested. Ten cases repeated four times are not eighty independent situations. Actual token costs and an exact provider model snapshot are unavailable, so the original cost-effectiveness gate remains unassessable.

The useful additional regression example is the distinction between an unspecified witness and a witness known to be different from the tested object. Correct requested outputs do not guarantee that the accompanying explanation contains no unsupported assertion.

## Preservation and verification

The LR 4 audit used a fresh checkout of the remote research branch at the result commit. It reproduced the saved-record checks and aggregation:

```bash
python reviews/2026-10-01-cc-handoff-pilot/run_support.py check
python reviews/2026-10-01-cc-handoff-pilot/analyze_results.py audit
python reviews/2026-10-01-cc-handoff-pilot/analyze_results.py summarize
```

- Frozen execution-input hashes pass unchanged.
- All 80 individual trial records match the aggregate transcript; all 144 raw responses and invocation records pass the stored-record audit.
- All 267 files named in `RESULT_MANIFEST.json` exist, match their SHA-256 hashes, and are tracked in Git.
- The audit and aggregation reproduce the committed files byte for byte and leave the checkout clean.
- The final result, strict/permissive grading distinction, and next unrun question already appear in `README.md`, `HANDOFF.md`, `RESEARCH_PLAN.md`, and the pilot note.

This verifies stored evidence and arithmetic, not a fresh model experiment, independent semantic certification, or provider telemetry. Retrieved conversation context reached an intermediate collection update; it did not supply a complete verbatim LR 3 transcript or a verified final delivered message. No missing research artifact was identified in the recovered work. An unavailable old runtime's unsaved scratch state cannot be certified from this checkout. This note is a research resumption record, not a conversation transcript.

## Earlier recommendation — preparation now recorded above

**Test whether CC helps an author select and preserve consequential information while compressing a longer history.** This addresses the remaining mechanism directly: the completed pilot supplied the same selected facts to both formats, so it could not test information selection.

The next concrete step is a separate, bounded authoring-study protocol:

1. Supply both authoring methods the same longer histories and equal explicit budgets. Use a strong conventional method with normal source, uncertainty and version-tracking practices.
2. Keep downstream questions and answer keys hidden from authors. Use new evaluation cases; the present ten cards and identity counterexample are development evidence.
3. Let fresh recipients answer from the generated handoffs under identical source-recovery rules. Score correct decisions, lost relationships, unsupported assertions and justified recovery; distinguish unavailable evidence from a negative result.
4. Freeze materials, scoring, budgets, stopping rules and handling of ties before running. Treat no advantage as an acceptable outcome. Measure actual token costs only if the authorized runtime exposes them; otherwise declare that endpoint unavailable before execution, with no token-efficiency claim.

This is a recommendation, not an execution freeze or a launched benchmark. No new respondent agents, trials, mathematical search, paid compute, or external application were run during this continuity audit.

## Mathematical work remains available

The [rank-three test](notes/CC_THREE_PARAMETER_TEST_2026_09_30.md), committed at `52c4912`, found that four selected sheets cover 89/89 training cases but only 310/318 held-out cases. All 36 supplied sheets recover physical witnesses in all 407 cases. Keep the eight compact-menu failures: they are failures of that frozen selection, not counterexamples to Lonely Runner.

If the next priority returns to mathematics, the saved next question is to derive a coverage criterion for a sheet's joint integer-contact image, use the eight misses as development counterexamples, and then freeze a new rule with a fresh validation domain. The [transfer-value assessment](notes/ULTRA_TRANSFER_VALUE_ASSESSMENT_2026_09_30.md) also preserves the optional export of three exact compatibility regressions. These are separate pending directions, not work silently launched alongside the recommended authoring study.

Earlier universal arguments retain their recorded proof-candidate status. This recovery does not promote a mathematical claim or demonstrate external utility.
