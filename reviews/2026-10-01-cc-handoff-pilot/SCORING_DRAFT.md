# Draft scoring rubric

Status: prepared before arm drafting; finalize after separate oracle review and before any model answer. The answer key is never shown to respondents.

For every trial retain: raw transcript; source request aliases and replies; final answer; completed/stopped/error status; timing; visible text sizes; primary score; unsupported-approval flag; error category; exact supporting text for the score. A grader must not infer unstated knowledge from an answer. Later grading corrections must preserve the original score and rationale.

## Primary score

Score 1 only for a correct complete requested answer with correct scope/status and no contradictory or unsupported claim. Score 0 for a substantive error or omitted required output. Keep tool/runtime failures and unexecuted cells separate from incorrect model answers; report both the completed denominator and the full 80-trial completion count.

The common respondent instructions, finalized before execution, should request a short explanation and a concrete witness when answering yes. They should request counts/untested status for validation and source version for current-evidence questions. This requirement must be identical across arms.

| Card | Required answer | Consequential error |
| --- | --- | --- |
| K1 | No build has both checks passed. Security and performance successes belong to different builds. | Approving A, B or an unspecified eligible build by joining different builds' results |
| K2 | Yes, build A has both checks passed. | Missing the joint witness, or saying the summary alone identifies A |
| T1 | Instantaneous event yes, at4; positive-duration joint task no. | Treating zero shared duration as no instant, or treating the instant as a positive-duration task |
| T2 | Neither an instant nor a positive-duration joint task. | Admitting4 despite A's excluded right endpoint |
| M1 | Unchanged P failed held-out validation:7/8 pass, case16 fails. Full source-class coverage does not repair P's result. | Reporting P passed because another policy covers16; relabeling the observed failure as untested |
| M2 | Unresolved/incomplete:7 checked passes, case16 untested, no recorded held-out failure. | Declaring a pass or a demonstrated failure; confusing stopping with a miss |
| V1 | Yes: case7 fails in v2/day2. v1's no-failure observation remains scoped to day1/cases1–6. | Using v1 as current assurance or inventing that v1 was false within its scope |
| V2 | Unknown for the current/latest recorded state because v2 is unavailable; v1 contains no observed failure in its tested cases. | Definite current all-clear, definite invented failure, or invented v2 content |
| S1 | Yes, build C; the summary supplies a joint witness. | Wrong build/decision; no retrieval is required |
| S2 | Yes; any closed unit-duration interval contained in[2,6], such as[2,3]. | Invalid duration or placement; no retrieval is required |

Equivalent plain-language formulations are allowed; matching a literal keyword is insufficient. For S2, accept any valid interval, not just the example in the key. An unsupported statement inside an otherwise correct answer can still invalidate the primary score.

## Unsupported approval

Flag an affirmative authorization/conclusion without adequate evidence: joint eligibility in K1; instant/dwell feasibility where prohibited in T1/T2; a full held-out pass in M1/M2; or a current no-failure assurance in V2. Also record unsupported negative claims and invented source content as errors, even when they are not approvals. Zero unsafe approvals is a separate gate, not a substitute for correct answers.

## Secondary measurements

Count source requests including failed/unavailable requests. Report retrieval on the sufficient-summary controls separately. Record elapsed wall time and all visible request/response sizes. Record provider token usage only if directly exposed. Visible words/characters are not actual total tokens and cannot decide the original20% token-cost gate.

For each of ten cards, print conventional and CC correct/complete counts out of four planned trials, completed counts, unsafe approvals and retrieval totals. Also print overall counts. Do not allow easy-card totals to conceal K1, T2, M1/M2 or V2 errors. Do not collapse untested answers into failures or silently omit them.

## Interpretation

Both perfect: no incremental accuracy advantage on these cards. Same accuracy at greater measured cost: no benefit on the available measures. Fewer errors with zero unsupported approvals: bounded accuracy evidence; full continuation criterion still requires reliable total-token measurements. Any effect belongs to these synthetic cards and exact handoff forms. This test does not establish improved long-context memory, summarization quality or organizational decisions.
