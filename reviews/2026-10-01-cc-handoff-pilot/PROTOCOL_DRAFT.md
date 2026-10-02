# Controlled handoff comparison — preparation record

Prepared October 1, 2026. **Status: source cards, proposed answer key and trial order prepared; independent review and model experiment UNRUN.** This is not the final execution freeze.

The maintainer selected the handoff question after the September 30 transfer-value review: can a CC-informed handoff preserve consequential distinctions better than an equally concise, well-written conventional handoff? This takes priority over the earlier proposed extraction of software regression fixtures. That extraction remains a separate unrun proposal.

Research/source baseline: `bbdf1b7c3f699eda46e4cd4bc9aac9a7a486a970`. Origin: `reviews/2026-09-30-ultra-transfer-value/information_transfer.md`, "Smallest useful test — specified and unrun." Original design is preserved unchanged.

## Question and interpretation

The first pilot evaluates how a recipient uses a supplied handoff and recovers relevant source records. It does not evaluate how an author constructs a handoff from a long conversation, naturally occurring context loss, long-term retention, different models, or organizational outcomes.

Both conditions will contain the same underlying factual information, receive the same neutral summary and source access, and be capped at 120 words. The conventional condition must be competent: facts, assumptions/limits, dated sources and next action. The CC condition uses supported question/output, scope/joint identity, retained/omitted information, dated source and recovery trigger. Labels and organization are the intended treatment; extra truth or a hidden answer in one arm would be a confound.

This is deliberately a narrow comparison. If matching facts also makes the two handoffs equally good, that is a legitimate null result. It would not show that every possible application of CC fails. Giving CC more relevant facts would answer a different question and is prohibited in this pilot.

## Fixed material and sequence

1. `SOURCE_CARDS.json` expands the original ten cards into standalone source records. The original contrasts and neutral summaries remain intact. Expansion notes identify resolved cross-references and endpoint notation; no actual business records are used.
2. `ANSWER_KEY_DRAFT.json` records the proposed answers. `validate_materials.py` checks them through direct joins, exact interval membership, validation partitions and report availability. This is a same-author semantic preflight, **not independent oracle review**.
3. Obtain a separate oracle review **before drafting either arm's condition text**, as the original design requires. If a card or key needs correction, preserve the draft and record a new revision before any respondent sees it.
4. After that review, draft both arms. Review for factual equivalence, matched retrieval access, word counts, answer leakage and an intentionally weakened comparator. Make within-pair handoffs identical apart from opaque source identities wherever the retained information is identical.
5. Save both exact handoffs, common instructions, final rubric, independent reviews and exposed runtime configuration. Commit an execution freeze before the first model answer. Source-material pins alone do not complete this gate.
6. Execute the already generated 80-trial schedule: ten cards × two arms × four blocks. Seeds are `20261001`, `20261002`, `20261003`, `20261004`. Each answer starts in a fresh context. Do not reuse one respondent across cards or arms.
7. Save every request, source response, final answer, status and score. Report all ten card-level outcomes and the paired comparison. Stop after the fixed pilot; no adaptive harder cards or rewritten prompts.

## Isolation and retrieval

The intended available mechanism is a fresh agent context with no conversation fork. It should receive only the common instructions, neutral summary, one handoff, the query and its source catalog. It must not read repository files, the answer key, condition labels, trial schedule, other answers, or the project conversation.

Use mediated retrieval: the respondent requests a source alias in its response; the coordinator returns exactly that card's source text, or its declared unavailable status. Limit to two source requests per answer. The source catalog lists aliases and synthetic dates equally in both arms; the unavailable latest report in V2 is not fabricated. Retrieval failures count toward the limit and remain in the transcript.

No retrieval is intrinsically better. S1 and S2 deliberately have adequate summaries; unnecessary retrieval incurs cost without improving their answers. K/T/M/V paired cases require distinctions not present in the neutral summaries.

Each response is blind to the CC name and the study hypothesis where possible. Trial IDs are opaque, and source aliases do not encode the correct answer. Infrastructure/system instructions may still be shared across fresh contexts; disclose this limitation.

## Budget, measurements and runtime limitations

Retain the original limits: 80 answers, at most 160 source requests, and one hour wall-clock for respondent execution. The clock begins at the first respondent invocation, after preparation and final freeze. On a stop, retain completed and unexecuted cells separately; do not impute answers or selectively rerun failures.

The original design also specifies a 600-output-token cap, an identified fixed model/runtime, and a success gate requiring median total-token cost no more than 20% greater. Available agent tools do not expose a provider model snapshot, hard output-token control, or reliable total-token accounting. No model/API invocation has been made to probe outcomes.

Before execution, either use an authorized backend that exposes those controls or explicitly freeze the following limited adaptation:

- use one inherited agent configuration with no model/reasoning overrides for every trial; record the exposed configuration and timestamp, while marking the provider snapshot unknown;
- request concise answers, but record the original 600-token hard cap as unenforceable rather than claiming compliance;
- record exact visible characters/words, source requests and elapsed time as descriptive measures only;
- mark total-token cost and the original 20% gate **UNASSESSABLE**; do not replace them with a word/character proxy or claim the full original success criterion was met.

This adaptation permits a bounded accuracy/retrieval pilot, not a fully measured cost-effectiveness test. It must be accepted in the final pre-execution record, not invented after results. No paid API, new subscription or external data transfer is authorized by this preparation record.

## Decision rule

Primary: correct complete requested output, correct scope/status, and no unsupported approval. The fixed rubric is in `SCORING_DRAFT.md`; finalize it after oracle review and before the execution freeze.

The original continuation criterion is fewer consequential errors than the conventional condition, zero unsupported approvals, and at most 20% greater median total-token cost. If total-token usage remains unavailable, the full criterion cannot be evaluated. A lower error count would be an accuracy observation only. Equal/ceiling accuracy establishes no incremental accuracy benefit; a null must be retained without changing the test.

Four repeats of the same ten cards do not constitute eighty independently sampled situations. Report descriptive counts, per-card differences, unavailable results and protocol deviations. Do not extrapolate statistical or operational significance from this synthetic pilot.

## Current execution/permission state

The current session permits subagent spawning only after an explicit request for agent/delegated work. The present request selects the handoff question but does not explicitly request new respondent agents. No new agents have been launched for this pilot. The cards, draft key, schedule and preflight are prepared so that the request to authorize fresh review/respondent agents concerns a concrete bounded experiment.

The independent oracle review, arm drafting and fresh-context execution remain pending in that order. Do not silently treat an old completed Ultra review as authorization to launch a new group of experimental respondents. Do not edit AGENTS.md to create permission for this test.
