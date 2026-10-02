# Pre-execution materials review

Date: October 1, 2026. Reviewer: separate internal AI context `/root/authoring_materials_review`.

**Final disposition: PASS for execution freeze, after the B1 repair verified below.** The study design, comparator, prepared exposure, order, clarified scoring, and repaired recorder pass this review. The initial recorder finding and its resolution are preserved. No change to a history, question, method prompt, or substantive answer was needed. No participant trial was run in this review, and the study `run/` directory did not exist when checked. The owner must still complete the administrative freeze/publication gates below before dispatch.

## Scope and evidence

I inspected the protocol, scoring, configuration, common/method instructions, prompt assembly and validators, all prepared schedules/question text, recorder, dummy rehearsal, execution guide, runtime declaration, and the source-first comparison. The prepared author packets were checked against their complete source histories byte for byte by the static validator. This is a materials/implementation review, not a second source-first derivation of the eighteen answers.

The review was conducted against working files based on preparation commit `d03d3e0277541dd77e579fb418e4c76fec793174`. The owner reported that prepared-status labels and the separate execution manifest would be finalized after review. I have therefore not treated their expected pending state, or disagreement with the historical preparation manifest, as a newly discovered study-design defect. The historical manifest remains provenance, not execution authorization.

I reran `validate_materials.main()` with its report write redirected to an in-memory object, and `rehearse_recorder.main()` with its report destination redirected to a temporary directory. The former passed; the latter passed all eighteen existing dummy checks. No package input was changed by these checks. I also rebuilt the three prepared objects in memory and obtained exact equality with the committed objects. One focused dummy response containing leading/trailing whitespace, a newline inside its answer, a backslash, and Unicode round-tripped exactly through both the immutable incoming envelope and the trial message. No model call, external network request, or additional agent was used.

The source-first report's actual SHA-256 matches the comparison's sealed value: `d5654b914164b7e5a9f6ee70db6df16bd2043da5bebbd39cc902ffea707afb71`.

## Initial blocking defect — subsequently resolved

**B1 — per-response validation/count record is incomplete.** `materials.validate_recipient()` returns an object, decoded-answer word count, and raw digest. `run_support.reply()` retains the object but discards the word count. Its response message stores raw content, time, file, and digest, but no parse/schema result or decoded answer count. Consequently the first and recovery turns do not have the separately recorded counts promised by PROTOCOL.md. `finish()`'s `visible_output_words` is a different quantity: it counts the complete raw JSON text across responses, including framing, and must not be substituted for the 160-word decoded-answer measure. For invalid outputs the trial has a terminal error reason, but no per-response validation record; a recovery error should remain distinct from the successful first response's validation.

Required repair: add a validation record for every captured response, carrying its stage, parse/schema/limit outcome, decoded capped-field word count when computable, and error or explicit unavailable reason otherwise. Preserve the existing raw string and first-answer records unchanged. Retain separate validation results for first and recovery turns, including when the latter fails. A focused dummy check should demonstrate both valid turns' counts and an invalid second turn without overwriting the first. Valid author counts already exist at trial level; their per-response representation should follow the same auditable convention. Late responses may be explicitly marked excluded/not validated, with a null count if no validation is performed.

This is a bounded recording repair. The raw material needed to reconstruct counts is already retained; the defect does not presently suggest corrupted study observations, because none have been collected.

## Passed checks

| Area | Finding and evidence |
| --- | --- |
| Conventional comparator | Strong. It explicitly requests decisions, measured evidence, dependencies, corrections, dates/versions, assumptions, exceptions, uncertainty, source pointers, and foreseeable scope changes. It is not merely a generic summarization request. |
| Common exposure and effort | Each pair receives the same complete history, common instructions, one opportunity, identical ordered `status/evidence/next` fields, and a 220-word decoded-value cap. Both method instructions have 112 whitespace words. The deterministic field rendering is shared. |
| Prompt isolation | Author assembly delivers common text, one procedure, and one history. Exact later questions and key paths are absent. Recipient assembly uses only the question catalogue and the selected rendered handoff or full source; it does not read the semantic key. Condition mappings stay in coordinator records. |
| Fixed schedule | The seeded builder reproduces all prepared objects. Twelve authors cover six paired histories; each method is first on three histories. The 54 reader/control cells contain exactly one of each method/control for each of eighteen questions. `begin()` checks the next ID and active-context cap. |
| First-answer endpoint | Raw response is copied before parsing or source queuing. A valid first answer is saved before a source prompt is returned. A second answer requires recorded delivery, and no additional recovery is accepted. Declining recovery carries the first answer forward. |
| Failure propagation | An invalid author prevents its dependent recipients and produces `AUTHOR_PROTOCOL_ERROR`; an unavailable author produces `AUTHOR_UNAVAILABLE`. Source delivery failure retains an already saved first answer and does not invent a final answer. Unsent queued prompts do not count as exposure. Undispatched cells become `UNRUN`. |
| Raw capture | Incoming envelopes use exclusive creation, keep the exact final-message string, and have independent raw-message hashes. Repeating a reply after terminal completion is rejected. The focused whitespace/Unicode fixture preserved the exact string. |
| Phase boundary | All authors must close before recipients start. Author trial hashes are sealed and verified on recipient-phase start. Valid authors retain raw, parsed, and rendered versions. Dispatched and unrun cells retain the freeze commit. The owner must separately verify publication. |
| Deadline behavior | The recorder rejects `begin()` after the deadline and retains replies recorded late as excluded `BUDGET_STOP`. The guide requires stopping outstanding contexts, preserving late excluded messages, and no deadline extension or selective rerun. |
| Scoring | Separate requested correctness, exposed support, and full-source faithfulness prevent rewarding unsupported guesses or hiding false handoff claims. SCORING.md explicitly adopts every item-level optionality distinction in ORACLE_COMPARISON.md. Optional omitted explanations cannot become failures; volunteered unsupported assertions remain assessable. |
| Denominators | Planned cells, observed cells, author protocol errors, missing infrastructure outcomes, and recovery-stage failures are distinguished. Six paired history clusters and one author realization per condition/history are explicitly acknowledged. |

## Nonblocking limits and operational responsibilities

The common schema and strong comparator may reduce the contrast. Several sources restate decisive facts near the end, and H06 is intentionally easy. These are legitimate design properties and possible ceiling effects; do not weaken cases after observing performance. The study concerns six synthetic, development-informed histories, not a random external sample or context-window stress test. The retention audit remains necessary before attributing an outcome difference specifically to information selection.

Equal instruction words, source bytes, response opportunities, and output caps do not establish equal token consumption or hidden reasoning compute. RUNTIME.json appropriately leaves unavailable provider snapshot, actual token usage, sampling parameters, and hard token cap null. The exposed collaboration interface supports fresh no-fork participants and same-agent followups; five active participants can be used only while enough total runtime slots remain available. Completing 66 contexts within 20/55-minute budgets has not been empirically established by local dummy tests. A deadline producing missing cells is an anticipated result, not grounds to extend the budget.

The recorder is a mediated single-writer tool, not an autonomous provider adapter or security boundary. Correct prompt delivery, actual fork settings, delivery confirmations, pre-call deadline checks, required checkpoint thresholds, remote publication, and absence of unauthorized participant tools remain coordinator/owner responsibilities. In particular, `delivered()` records an asserted successful followup; it cannot independently verify provider telemetry or whether the call began before deadline. The guide supplies the operational restriction. Checkpoint cadence is specified but not automatically scheduled by the recorder.

The guide requires preservation of unsolicited messages, unauthorized tool use, uncertain delivery, and raw messages received after terminal closure as excluded deviations. `reply()` intentionally rejects a terminal trial. Those messages therefore need a separate exact-string deviation record, rather than a retry through `reply()` or modification of sealed author trials. The owner should choose and consistently use an append-only deviation location and include those records in the final audit. This is an operational requirement, not a reason to resume or replace a respondent.

Isolation and masking are partial. Participant access to nearby files is instruction-prohibited, not technically blocked. Actual leakage must be recorded and handled as specified; absence of keys from a prompt alone cannot establish no exposure. Later condition masking cannot conceal every stylistic cue. The coordinator must remain unexposed to the key, review answers, and comparative grades during collection, and collection must close before semantic grading.

## Required freeze closure

1. B1 is resolved and rechecked in the appended resolution below. Pin the repaired recorder and rehearsal, rather than their initial reviewed versions.
2. Finalize the prepared/review/rehearsal status labels and runtime declaration. Preserve zero participant-call counts at the freeze boundary and use mutable run records for subsequent progress.
3. Create the separate execution SHA-256 manifest covering protocol, scoring and controlling oracle notes, inputs, prepared schedules, reviewed driver, guide, runtime, reviews, and rehearsal. Keep the historical preparation manifest at its documented provenance. The freeze commit itself is to be supplied to recorder initialization; do not invent a self-referential commit hash in a file.
4. Verify and publish that freeze before author dispatch. Preserve and publish the author seal before recipient dispatch. All later scoring must use this frozen material, with disagreements and sensitivity retained.

## Review identity and limits

This is separate internal AI review with inherited configuration; an exact provider snapshot and independent provider telemetry were unavailable. It is not independent human review, formal verification, proof of isolation, or evidence that the treatment helps. The dummy checks exercise local recorder paths only and cannot establish delivery reliability or future participant behavior. This reviewer did not generate participant handoffs or recipient answers. No study inputs were edited; the only package artifact authored by the reviewer is this report.

Material hashes at initial disposition: `run_support.py` = `e4b3d095f6393ddd7b83c54ae396da78370af8a6e0bc58e635c4ac0729851f79`; `rehearse_recorder.py` = `f3f606bfd3a189b19ec9e6e20b4ba37df2c15c4aef63dc3a59261ac911992559`; `SCORING.md` = `a0d0f9ed01809a8d8e273119ed9c1ac2426e81e32461115b21f0a5976bde5079`. The final execution manifest must identify any repaired versions.

## B1 resolution and final recheck

The owner added `diagnostics()` and a `validation` object on every captured response. This records strict JSON parse status, decoded cap-unit words when available, schema/cap outcome, and error; valid responses also identify their mode. Invalid JSON has a null decoded count and a parse error. Late responses retain parse/count diagnostics but are explicitly `NOT_ASSESSED_LATE` for schema/cap acceptance. A malformed response's position and delivered-source record identify its stage even where no valid mode was assigned.

I inspected the repair and reran the revised dummy rehearsal with its report redirected to a temporary directory: **PASS, nineteen checks**. It now asserts valid first/recovery decoded counts, the rejected author's count of 221, and malformed-output parse failure. I separately exercised a malformed recovery response and verified that the original first answer and its entire original response message, including validation, remained exactly equal; the second message separately recorded parse/schema failure and no final answer was invented. The study `run/` directory remained absent. The package diff also passed whitespace checking.

**B1 is closed. No blocking materials or recorder defect remains within the reviewed scope.** Reviewed repaired hashes: `run_support.py` = `005e2ad008cbb3c077c5f51e0278ab83dba6dce421d9c32a67206f8d01f0a728`; `rehearse_recorder.py` = `3f9b9b634eb37e07a836a2c9637506f3b51a8bdfde4080a5a34827d3fb768dee`. The nonblocking limitations and owner/coordinator responsibilities above still apply. This pass is not a run result and does not establish an advantage for either condition.
