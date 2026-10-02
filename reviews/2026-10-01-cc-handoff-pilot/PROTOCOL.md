# Execution protocol: matched handoff presentation and source recovery

October1,2026. This final protocol supersedes the preparation draft for execution; original drafts, cards and their pins are preserved. The user authorized fresh review/respondent agents. `ORACLE_REVIEW.md` completes a source-first internal AI answer-key review; `MATERIALS_REVIEW.md` records the separate material/recorder review.

## Frozen question and treatment

Can a CC-informed arrangement of a handoff help recipients answer a changed query and retrieve required source information, compared with a strong conventional arrangement containing the same information?

`HANDOFFS.json` contains exactly the same five factual/operational statements in both arms for each card. Field labels, order and grouping differ. The conventional record uses facts/scope, assumptions/limits, dated source links and next action. The CC record uses supported query, retained facts, scope/omissions, dated source and recovery trigger. Word counts match exactly per card (42–60 words, below the120-word cap). Paired cards have identical handoff text within each arm. Source alias/date catalogs contain no availability/outcome field. Neutral summaries, questions, common instructions and retrieval access match.

This isolates a narrow presentation/use effect. It does not test whether CC helps an author discover omitted facts, generate summaries, remember a long conversation, or solve arbitrary real-world decisions. Explicit instructions and simple cards may produce ceiling accuracy. Do not weaken the comparator or add harder cards after observing a ceiling.

## Inputs, answers and order

Use the ten cards in the unchanged `SOURCE_CARDS.json`, the final semantic rubric `SCORING.md`, and internally reviewed `ANSWER_KEY.json`. The stage1 source-card status field describes its historical preparation; current review/execution status is carried here and in the execution record.

Preserve the80-trial `TRIAL_SCHEDULE.json`: four seeded shuffled blocks, ten cards and two arms per block. Dispatch starts in ascending scheduled trial order. Permit at most five active trial contexts concurrently; completion/source-followup order can differ. Never reuse a context for another card, arm or repetition. Save all cases including errors and unrun cells. No selection by early result.

## Respondent interface and masking

Every respondent is a fresh `collaboration.spawn_agent` with `fork_turns="none"`; use the frozen prompt in `STIMULI.json` verbatim. No model or reasoning overrides. Task names use only opaque trial IDs. The prompt does not name CC, the comparison hypothesis, condition, source-card ID or answer key.

Respondents are instructed to use no tools/files/network/other agents and to request sources by a JSON response. This is instruction-based isolation, not a separate filesystem/security sandbox. Fresh contexts may share provider infrastructure and generic system/developer instructions. Neither concealed reasoning nor hidden runtime context is recorded or claimed to be absent.

The execution coordinator may read the schedule, prompts, source cards and recorder. It must not read the answer key, scoring decisions or aggregate correctness while trials run. It supplies only `run_support.py`'s returned source-response text through `followup_task`; it adds no hints or corrections. A source request is an intermediate response in the same trial context, not a new independent answer. The primary coordinator may monitor completion but must not alter stimuli or source responses.

## Recording and stopping

Use `run_support.py init FREEZE_COMMIT` immediately before first dispatch. The one-hour budget starts at init, slightly before the first respondent invocation. `begin` enforces ascending order, the five-context cap and unchanged material hashes. Save the raw text of every respondent message, then process it with `reply`. `register` records the actual agent path. All source replies come from the fixed source cards. No key-dependent operation occurs in this recorder.

One execution coordinator is the sole recorder writer. Serialize every init/begin/register/reply/stop/close operation; do not run recorder mutations in parallel. The current JSON recorder has no multi-writer locking. Other agents and the primary coordinator may inspect status read-only during collection.

`begin` queues the initial prompt; successful spawn followed by `register` records its delivery. Source responses are queued by `reply`, then marked delivered with the recorder's `delivered` command only after a successful same-agent `followup_task`. A delivery failure ends as an infrastructure stop and retains queued/undelivered text distinctly. Only delivered messages count as exposed evidence or visible input cost. Serialize `delivered` as well. Count an attempted third request in the recorded request total, but do not serve it; report that budget violation rather than hiding it behind the allowed-request cap.

Each trial may make at most two source requests, including unavailable/repeated/unknown aliases. One JSON source alias per request. An optional surrounding `json` code fence is accepted; other malformed responses end as `MODEL_PROTOCOL_ERROR`. Missing final fields or a third request also end as a model protocol error. Do not coach, replace, restart or selectively rerun such trials. A transient tool transport retry is allowed only for the same operation/agent after checking that it did not already succeed; record it separately. A provider/agent infrastructure failure is an `INFRASTRUCTURE_STOP`, not a wrong mathematical answer.

At the one-hour deadline, stop active respondents and record budget stops; mark undispatched cells UNRUN. The controller must check elapsed time before each spawn/followup. No further model response is solicited after the deadline. `reply` also checks the deadline: a message recorded after it is retained as an excluded late response and produces a budget stop, without a source continuation or scored answer. This conservative recording-time rule may exclude a response delivered slightly earlier; disclose such a case. `close` writes all80 status records and the aggregate transcript file. Do not select the favorable response.

## Predeclared runtime adaptation

Use the inherited agent configuration without model/reasoning overrides throughout. The exposed interface does not identify a provider model snapshot or supply hard output-token control/actual token usage. `RUNTIME.json` records these as unknown/unavailable. The original600-output-token cap is unenforceable; the common prompt requests responses below150 words where possible. Record any excess as a protocol limitation, without selectively discarding the content.

Measure correct scoped answers, unsupported approvals, completion and source requests. Visible input/output characters and whitespace words are descriptive only. Elapsed time includes coordination/concurrency, not pure inference latency. Actual total-token usage and the original requirement of at most20% greater median total-token cost are **UNASSESSABLE**. Thus a complete pass of the original cost-effectiveness criterion cannot be claimed, even if one arm makes fewer errors.

## Grading and interpretation

Apply `SCORING.md` to whole scoped meaning and actually exposed evidence. V2 may begin with a qualified “no” if it distinguishes accessible v1 from unknown v2. M2 may say a pass is “not established” without asserting an observed failure. Grounding and endpoint/version/policy identity matter; literal keyword matching is insufficient.

The primary coordinator grades preserved answers after collection. A separate internal reviewer receives a condition-masked packet of answers, queries, relevant evidence and frozen rules to check the grading. Record disagreements and corrections without altering the trial responses. This is internal AI checking, not independent human/formal certification.

Report ten per-card comparisons plus overall counts, all completion states, source requests and adequate-summary controls. Four repeats do not produce eighty independent source situations. All-perfect outcomes support no incremental accuracy advantage here. Any observed difference remains limited to these cards, these matched statements and this exposed runtime. No new cards, prompt revision, adaptive repetition, benchmark expansion or general CC claim follows within this pilot.
