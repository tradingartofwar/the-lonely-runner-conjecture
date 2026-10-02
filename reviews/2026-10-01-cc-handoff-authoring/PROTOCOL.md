# Long-history handoff authoring: execution protocol

October 1, 2026. **PRE-EXECUTION PROTOCOL; collection status is recorded separately in run/STATUS.json.** The historical preparation manifest belongs to commit d03d3e0277541dd77e579fb418e4c76fec793174. EXECUTION_MANIFEST.json pins the reviewed inputs and recorder for this run; its containing commit must be published before author collection.

## Question and scope

Does an authoring procedure informed by CC retain more consequential information from a longer history than a strong conventional handoff procedure, under the same explicit length and exposure limits?

The completed [presentation pilot](../2026-10-01-cc-handoff-pilot/RESULTS_REPORT.md) supplied identical statements to both formats. This study instead lets authors select facts from the same history. Its primary outcome is recipient performance **before source recovery**. Recovery is measured separately so that rereading the complete source cannot conceal an inadequate handoff.

These are six newly authored synthetic histories of roughly 1,200 words, not actual long conversations, sampled organizations, external deployments, or tests of context-window limits. The domains deliberately exercise distinctions developed in this project. The cases are new instances, not new conceptual families or unseen domains. H06 is a straightforward control with a sufficient final synopsis. Several histories also restate decisive primitives near the end. No known hard case is a guaranteed failure, and easy or ceiling outcomes are valid.

## Fixed scope

| Item | Planned count |
| --- | ---: |
| Histories | 6 |
| Authoring methods per history | 2 |
| Author realizations per method/history | 1 |
| Fresh author contexts | 12 |
| Hidden questions per history | 3 |
| Handoff-only recipient contexts | 36 (18 per method) |
| Full-source control contexts | 18 |
| Total primary-study fresh contexts | 66 |
| Maximum recovery followups | 36, in the same recipient contexts |
| Maximum active contexts | 5 |

There are six paired history clusters, not 36 independent authoring examples. Three questions reuse each generated handoff; question outcomes are correlated. The single author realization per method/history leaves author stochasticity unresolved. This is a small descriptive pilot, with no significance test, population effect estimate, claim of novelty, or universal continuation threshold.

## Author treatment and common output

Each author receives only the common author instructions, one method instruction, and one complete history. Both methods receive the same history byte for byte, the same task family, one response opportunity, a 220-word limit, identical output schema, and the same inherited model configuration. They do not receive evaluation questions, answer keys, condition names, previous pilot results, competing outputs, or reviewer notes.

The conventional instruction explicitly includes current decisions, evidence, dependencies, assumptions, exceptions, uncertainty, dated sources, and changed circumstances. It is not a generic weak request to summarize. The CC-informed instruction emphasizes supported uses, linked conditions, omitted distinctions, scope changes, and recovery. Both require accurate concise work. The method directives have matched whitespace word counts; this is a visible-length control, not equal model-token accounting.

Both must return a JSON object with exactly three nonempty string fields, in this order: "status", "evidence", "next". The sum of whitespace-separated words in the decoded string values must not exceed 220. The field labels are fixed overhead in both conditions. No attachments, extra keys, encoded appendices, or tool use are permitted. Source event identifiers may be included naturally and count against the cap. Standard mathematical notation is allowed; the cap is a visible word constraint, not an information-theoretic bit budget.

Recipients see the same deterministic rendering of these fields. This reduces a layout confound. It cannot force identical phrasing or eliminate every presentation effect; the causal comparison is between the two authoring instructions as implemented. A later claim that any difference came specifically from information selection also requires the separate retention audit, rather than attribution from answer counts alone.

An overlength or malformed author output is preserved as AUTHOR_PROTOCOL_ERROR. Do not edit, shorten, coach, retry, or generate a replacement. Its three downstream cells are marked AUTHOR_PROTOCOL_ERROR and assigned primary 0, without pretending three recipients answered incorrectly. No recipient is launched for those cells. An infrastructure failure is different: its dependent cells are missing, never scored 0 as model errors or counted successful. Report both explicitly.

## Hidden questions and source access

Each history has one current-decision question, one evidence-scope question, and one changed-use question. The complete exact question text, including hypothetical changes, is committed in evaluator materials before any author is called, but excluded from all author prompts. Authors know the broad task family from the history; they do not need to anticipate arbitrary unrelated facts.

All twelve author responses must be collected and sealed before any evaluation recipient is launched. Commit raw responses, valid rendered handoffs, delivery records, schema/word checks, and an output manifest at that boundary. The experiment coordinator must not inspect interim comparative correctness or select better author outputs.

For each handoff question:

1. Spawn a fresh recipient with only the common recipient instructions, that question, and the rendered handoff. The first response is a committed handoff-only answer with a boolean recovery request.
2. Save that first response before serving any source. Do not erase or revise its primary score after recovery.
3. If recovery is requested, provide the complete same history verbatim in one followup to the same recipient. The second answer is the post-recovery answer. The history is always available in this controlled interface; unavailable facts within a history remain unavailable facts.
4. If recovery is not requested, carry the first answer forward as the post-recovery answer. Do not give unsolicited hints or extra evidence.

Full-source controls are fresh recipients who receive the same question and complete history from the start, with no generated handoff or method instruction. They get one answer and no recovery. They diagnose whether questions remain answerable by this recipient configuration even without compression. Do not use control answers as the truth oracle or remove difficult questions after seeing a control fail.

All recipients return JSON with exactly "answer" (a string) and "recover" (a boolean). At most 160 whitespace words in the decoded answer. For controls and post-recovery turns, recover must be false. The answer must supply all requested outputs as far as exposed evidence supports them, identify unresolved gaps, and avoid guessing. A first-turn request without an answer is a protocol error, not a free way to skip the primary endpoint.

Fresh contexts use no conversation-history fork and no model/reasoning overrides. Instructions forbid tools, files, internet, other agents, or inspection of nearby materials. This is instruction-based isolation in a shared environment, not a technical security sandbox. Publicly committed evaluator files are hidden only by their absence from authorized participant prompts. Actual full source exposure or key leakage is a recorded deviation; it is not excused by a clean prompt file.

## Runtime and recording

Use one recorder writer. Dispatch the committed author order, then the committed recipient/control order. Maximum five active contexts. Wall-clock collection budgets are 20 minutes for the author phase and 55 minutes for the recipient/control phase, beginning immediately before their respective first dispatches. Review and the between-phase commit are outside these limits and must be reported separately. No call begins after its phase deadline; replies recorded after the deadline remain raw records excluded from scored collection. Undispatched cells are UNRUN.

Record every exact delivered prompt, source followup, response, participant identity, parent/fork configuration, ordering, timestamp, parse result, word count, and status. Record delivery success separately from a queued prompt. Checkpoints after every four completed authors and every twelve completed recipient/control contexts contain raw outcomes and status only, without grading. There are no selective reruns or extensions. A transport retry is allowed only after confirming the original delivery did not succeed; retain it as a deviation. An uncertain completed delivery is not blindly repeated.

The single-writer recorder is run_support.py; EXECUTION_GUIDE.md specifies mediated delivery and exact-message capture. The dummy rehearsal and review are preserved in review/. No fabricated dummy answers may enter study result records. The owner verifies remote publication at both phase gates; the recorder verifies hashes, not remote publication.

Exact provider snapshot, actual token usage, sampling controls, and hard token limits were unavailable in the earlier runtime. Confirm availability again before the execution freeze. If still unavailable, record null; do not substitute word counts or elapsed orchestration time for actual token cost. Identical inherited settings, explicit response opportunities, common word caps, and wall budgets are the enforceable budget controls. They do not establish equal hidden reasoning compute. No paid API, external account, or additional compute purchase is part of this design.

## Outcomes and comparison

Apply SCORING.md and the separately reviewed key to preserved answers and actual evidence exposure. Report:

- Handoff-only supported complete answers out of 18 planned per method, with statuses and missingness.
- Requested-output correctness, unsupported assertions, unsupported approvals, and justified abstentions separately.
- Post-recovery supported answers and changes from first answers; requested/served recoveries and source exposure.
- Per-history three-question totals, paired history differences, and the three question types.
- H06 control performance and all eighteen full-source control outcomes.
- Handoff adherence and a condition-masked retention audit: which required distinctions are supported by the handoff, require source recovery, or are misstated.

A correct requested answer can still contain an unsupported explanation. Conversely, a truthful acknowledgment of missing handoff information can be grounded while not conveying the complete source answer. Keep those outcomes distinct.

Do not declare a winner from a single wording-sensitive grade. Report strict whole-answer and requested-output views side by side and preserve adjudication sensitivities without replacing the frozen primary endpoint. If both methods are at ceiling, conclude no observed incremental benefit on these cases. If control failures, major leakage, or missingness obstruct interpretation, preserve the comparison as limited or inconclusive. New cases or revised prompts require a new study; repairs here are not held-out validation.

## Review and freeze gates

1. A separate source-first reviewer receives histories and questions, answers them without the proposed key, then compares to the key. Check source sufficiency, ambiguity, hypothetical changes, numerical thresholds, and unasked grading demands.
2. A separate materials reviewer checks the strong comparator, common schema and caps, prompt leakage, fixed schedule, scoring, runtime feasibility, and dummy recorder rehearsal.
3. Resolve review issues without any participant outcome data; preserve changes and review provenance. Internal AI review is not independent human or formal certification.
4. Commit the final execution protocol, inputs, reviews, runtime declaration, driver, and SHA-256 manifest before author execution. Name that commit in every run record.

No respondent agents were launched during the original preparation checkpoint. Separate internal review and recorder rehearsal are preserved for the execution freeze. Collection results and status are separate artifacts; frozen configuration counters describe the zero-call freeze boundary. Nothing here authorizes additional purchases or claims unavailable token telemetry.

## Representation checkpoint

The supported question is bounded downstream use of a 220-word handoff for the stated task family. The history is the richer source; event identifiers and complete-history recovery provide the mapping. The handoff intentionally omits most chronology and may omit needed facts. Source availability does not make it lossless. Frozen source identity, first-answer preservation, exact question changes, and separate unknown/error states are retained in the experiment record. A wrong or unsupported first answer, unnecessary abstention on an adequate handoff, failed recovery, or missing changed-use relation is a concrete failure to inspect. This protocol adapts the project's CC rules without claiming a new theory of summarization.
