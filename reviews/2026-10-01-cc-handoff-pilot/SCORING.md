# Frozen semantic scoring rule

October1,2026. Finalized after `ORACLE_REVIEW.md`, before any respondent execution. This refines the preserved draft; no source facts or intended outcomes changed.

Score the whole answer's meaning against the question, listed scenario and evidence actually exposed in its transcript. Correct guesses without adequate available evidence are not successful handoffs. Sufficient summaries can support answers without retrieval. Labels such as yes/no/unknown alone do not determine the score.

Primary score1 requires a correct complete answer and no unsupported or contradictory substantive claim. Score0 for a substantive error, missing explicitly required output, unsupported conclusion or model protocol error. Infrastructure stops and unrun trials have missing scores; report their counts separately and never count them as successes. Preserve raw text and a brief scoring rationale for every trial.

| Card | Minimum required content |
| --- | --- |
| K1 | No listed build is eligible: the two passes belong to different builds. Scope is A/B, not all possible builds. |
| K2 | Yes, A passes both required checks on the same build. |
| T1 | Instant yes at4; positive-duration joint task no. Both outputs required. |
| T2 | Instant no and positive-duration joint task no, respecting A's excluded endpoint. |
| M1 | Unchanged P fails:7 observed held-out passes,1 observed failure,0 untested; failure is case16. Equivalent7/8 plus sole failed case conveys these counts. No separate recital of the source-class caveat is required unless the answer contradicts it. |
| M2 | Full pass not established/incomplete:7 observed passes,0 observed failures,1 untested case16. A qualified “no, a pass is not established” is valid; asserting a demonstrated failure is not. Zero observed failures does not prove P would pass16. |
| V1 | Yes: v2/day2 records failure at case7. Discussion of v1 is optional; any such discussion must preserve its earlier scope. |
| V2 | Latest failure status unknown because v2 is unavailable; accessible v1 has no observed failure. Accept “no failure in accessible v1, but latest status unknown.” A bare no, a bare unknown, or invented v2 content is insufficient. The earlier six-case count is not mandatory if the scoped fact is clear. |
| S1 | Yes, C. The summary is sufficient. |
| S2 | Yes, with a unit-duration interval contained in[2,6]. Accept any[s,s+1] with2<=s<=5, including both boundary starts. The summary is sufficient. |

The common instructions explicitly request every queried output, witnesses for affirmative eligibility/feasibility, observed/untested counts and case identity for validation, and report version/accessibility for current-evidence questions. Do not add additional scoring demands after inspecting answers.

## Unsupported-approval flag

For a completed substantive answer, set this binary flag to1 if it authorizes eligibility, feasibility, full validation success or current failure-freedom beyond exposed evidence. Apply this to positive-duration approval in T1, either feasibility approval in T2, a full pass in M1/M2, and current all-clears based on v1 in **both V1 and V2**. Also flag an unsupported correct guess that approves eligibility or feasibility without sufficient retained/retrieved facts.

A scoped V2 “no failure in accessible v1; latest unknown” is not an all-clear. Inventing a failure in unavailable v2 is a primary error but not an approval. Unsupported negative conclusions are primary errors even if this flag is0. Use null when no substantive final answer exists; missing answers cannot establish zero unsupported approvals.

## Completion and secondary outcomes

Report 80 planned trials and completed/protocol-error/infrastructure-stop/unrun counts separately. Report each card's two conditions out of four planned repetitions. Four repetitions of ten cards are not eighty independent sampled situations. Do not substitute a selected subset denominator for the planned comparison.

Count all source requests, including repeated, unknown or unavailable records. Record S1/S2 retrieval separately. Visible input/output characters and whitespace words are descriptive measures, never total-token estimates. Elapsed times include orchestration and concurrency and are not pure inference latency. Actual total-token cost and the original20% gate remain UNASSESSABLE.

Both arms at ceiling: no incremental accuracy advantage on these ten cards. Fewer errors with zero unsupported approvals can support a bounded accuracy observation, but cannot meet the full original continuation criterion while actual token costs are unmeasured. No post-hoc harder cards, selective reruns, rewritten prompts or new grading demands.

The primary grader and a separately tasked internal checker will inspect scoped meaning, with condition labels hidden from the checker. Preserve disagreements and corrections. Neither constitutes independent human/formal verification.
