# Separate review before execution

This file describes work that remains pending. No review response or agreement is implied by its presence.

## Source-first oracle review

Use a fresh reviewer context with ORACLE_REVIEW_PROMPT.txt, the six histories, and the eighteen question texts from prepared/QUESTION_PROMPTS.json. Initially withhold evaluator/QUESTIONS_AND_KEY.json and all method instructions. Do not deliver this entire coordinator guide during the first stage: the designer's risk notes below contain expected conclusions and are available only after the reviewer's source-derived answers are sealed.

For each question, derive an answer, cite source events, identify any unresolved ambiguity, and state whether the query changes only a specified assumption. Check numerical equality, signed clock conversion, current versus snapshot versions, and all required denominators directly from the histories. Check whether a different reasonable interpretation changes the answer. Do not rely on the designer's arithmetic checker as independent evidence.

Only after preserving those answers may the reviewer compare the proposed key. Record agreements and discrepancies, including correct answers whose proposed rubric unnecessarily requires additional details. Questions that need facts absent from the supplied history must be repaired before execution, with the correction and reason retained. Do not use participant responses to repair questions.

Specific review risks identified by the designer:

- H01's readiness is technical; transport availability is separate. C's exact threshold values pass. A's missing current test does not become an observed packet failure.
- H02's offset is signed and shared. The uncertain-offset hypothetical replaces the exact calibration, and database insertion is a different event.
- H03's prior exclusions, observed failures, untested cases, and candidate switch have distinct denominators.
- H04's 94 verified snapshot revisions become 93 verified current revisions after K12 changes. The two unaudited keys and the two delta keys have different evidence states.
- H05's proposals change named capacities only; all three resources are simultaneous.
- H06 is intentionally easy and sufficient. Do not invent an unstated safety gate or reject equal capacity.

Record reviewer identity/configuration if available, prompt exposure, response text, source version, and review limitations. Separate internal AI review is not independent human certification.

## Materials and implementation review

A different fresh reviewer may inspect the entire preparation package, after the oracle review is resolved. Check that the conventional method is strong and that CC does not receive more source facts, more response opportunities, a different schema, or a larger word allowance. Matched whitespace words do not prove matched tokens.

Trace exactly what reaches an author and each recipient. The coordinator-only schedule has condition mappings; deliver only the prompt string. Confirm no question/key exposure to authors, no competing handoff exposure, no prior-history fork, and no oracle access by the runtime delivery path. Verify the full-source controls are independent recipient contexts. Shared filesystem access is only instruction-prohibited, not technically impossible; disclose the limitation.

Review whether the common final schema may itself benefit both methods and thus reduce the measured contrast. This is intentional: the baseline is strong, and a tie is acceptable. Review whether the synthetic sources' explicit rules and final restatements create a ceiling; do not weaken them after observing one. The six histories are development-informed cases, not a random external sample.

Before approving an execution freeze, require a single-writer recorder implementation and dummy rehearsal. Exercise initial delivery, failed delivery, schema/length errors, author failure propagation, first-answer preservation, no-recovery completion, one recovery, attempted extra recovery, deadline stopping, and immutable raw capture. Dummy records must be clearly separated from study records. The existing materials validator covers prompt/schema preparation, not those execution properties.

Verify final hashes, exact runtime limits, order, checkpoint frequency, and the author-output sealing step before any recipient. Report blockers, recommended pre-execution changes, and passed checks separately. Review completion is not experiment completion.
