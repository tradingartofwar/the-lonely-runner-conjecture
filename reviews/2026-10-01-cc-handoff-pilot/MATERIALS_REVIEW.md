# Internal handoff-materials review — October 1, 2026

**Conclusion: PASS for the bounded materials/recorder review. The initial recorder findings were addressed before execution; no remaining blocker was found under the final coordinator procedure. The final manifest/commit freeze remains a separate pre-execution gate.** This is internal AI review, not external/human review, a respondent trial, or evidence of CC benefit. This reviewer edited only this report.

## Matched content and comparator

All ten cards carry exactly the same five statement atoms in both arms: summary, supported scope, limits, source metadata and recovery action. I reconstructed each arm from those atoms and compared it with the stored text. No additional arm-specific statement is present. Field labels, grouping and order differ intentionally: the conventional arm puts summary and supported scope together; the CC-informed arm separates and reverses those items.

| Cards | Conventional words | CC-informed words |
| --- | ---: | ---: |
| K1, K2 | 46 | 46 |
| T1, T2 | 42 | 42 |
| M1, M2 | 56 | 56 |
| V1, V2 | 60 | 60 |
| S1 | 56 | 56 |
| S2 | 57 | 57 |

Counts use whitespace splitting, include labels, match the stored counts, and are below the 120-word handoff cap. They are not token counts. The cap applies to the handoff, not the complete stimulus.

The conventional comparator is operationally strong: it states the facts and supported scope, identifies the same omissions, supplies the same dated aliases, and gives the identical useful next action. It does not suppress a caveat, remove a retrieval cue, or substitute an unhelpful action. Both versions use concise, somewhat telegraphic prose; this audit does not certify that either is the best possible writing. There is no apparent deliberate weakening of the comparator.

This is a narrow presentation-and-recovery comparison using supplied handoffs. Shared statements already encode the critical reasoning distinctions and explicitly say when to retrieve. Common instructions also demand scoped evidence, counts and witnesses. Accordingly, a result cannot establish better summarization generation, spontaneous discovery of recovery needs, general CC superiority, natural long-context retention, or operational effectiveness. A ceiling/null result is valid and must remain a null for incremental accuracy on these cards.

## Within-pair leakage, stimuli and schedule

For K1/K2, T1/T2, M1/M2 and V1/V2, the neutral summary, question, aliases/dates and each arm's handoff are byte-identical within the pair. Their initial prompts are therefore identical within an arm; only the subsequently retrieved source distinguishes the outcomes. In particular, the V handoff says availability is not carried, rather than leaking V2's unavailable status. Opaque aliases do not encode the pair member or answer. S1/S2 intentionally retain enough facts to answer without retrieval; that is the adequate-summary control, not unintended leakage.

I reconstructed all 80 stored stimuli from the common instructions, summaries, handoffs, catalogs and questions, and verified exact prompt equality and every stored SHA-256. There are 12 distinct initial prompt texts. Prompts do not contain the arm identifier, trial ID, answer key, schedule or CC name. Formatting can reveal the presentation condition, so this is not complete blinding to format.

The complete schedule parses as 80 unique trial IDs: ten cards × two arms × four repetitions. Every block contains each card/arm exactly once, positions 1–20, with the specified seed 20261001–20261004. I checked this coverage and order metadata, not the randomization generator or statistical randomness. Repetitions remain repeated fixed situations, not 80 independent sampled scenarios.

## Query, evidence and scoring coherence

The final rubric implements the oracle's consequential clarifications and matches the common instructions: both T outputs; a witness for affirmative eligibility/feasibility; observed-pass/failure/untested counts and case identity for M; version/accessibility and uncertainty for V. The sources support these requested distinctions. K concerns the listed builds; T preserves included versus excluded endpoints; M preserves frozen P and failure versus untested status; V preserves earlier observed results versus inaccessible later content.

V2's question remains linguistically ambiguous, but the frozen semantic rule fairly accepts a scoped accessible-evidence “no” alongside unknown latest status. It does not require a particular leading label. M2 similarly permits “not established” without converting an untested case into an observed failure. S1/S2 can score correctly without retrieval. No unrequested extra substantive output appears necessary under the final rubric.

Correct unsupported guesses fail the primary score, consistent with testing successful handoff use. The unsupported-approval flag separately catches broader approval/all-clear claims; an invented unavailable failure can be a primary error without being an approval. Missing final answers are not successful zero-approval responses. These distinctions are coherent, but require semantic grading of the actual exposed transcript, not merely matching the key or trusting the evidence array. Evidence labels alone cannot establish that a source was received. The separately tasked checker is condition-label-hidden, not demonstrably format-blind if it sees prompts.

## Recorder findings and resolution

I identified an initial deadline gap, third-request undercount, possible concurrent-write races and premature treatment of queued text as delivered. The coordinator corrected these before any trial. I reread the complete revised recorder, `PROTOCOL.md` and `RUNTIME.json` and confirmed:

- `reply()` now retains post-deadline messages as excluded late responses and ends the trial as an infrastructure stop. The final protocol starts the clock at `init`, requires elapsed-time checks before spawn/followup, stops active contexts at one hour, and permits no further continuation. It explicitly discloses the conservative recording-time cutoff.
- A third read now increments the request counter before rejection and is never served. The protocol requires reporting that violation, so attempted requests may exceed the permitted-request ceiling without being hidden.
- Prompts/sources begin as queued. Successful spawn/registration or same-agent followup/delivery acknowledgement marks exposure. Only delivered user messages count as exposed evidence/input size; failed delivery remains an infrastructure stop.
- The final protocol requires a sole coordinator serializing every mutation, including `delivered`. This supplies the concurrency control absent from the JSON recorder itself.

Residual limits are operational, not new blockers: isolation is instruction-based; the recorder cannot prove tool abstention, fresh contexts, matching runtime or delivery correctness. Keep frozen files immutable, since replies reload source cards and hash checking occurs at init/begin. Forward only the prompt/source-response text, not recorder metadata. Grade actual exposed facts rather than trusting evidence labels; basic JSON parsing is not semantic validation. The final protocol recognizes these responsibilities and the fresh-context/no-overrides configuration.

At the static-check stage no manifest or `run/` existed. Final hashes/commit must still be frozen before launch. `PROTOCOL.md` now supersedes historical pending/unrun language while preserving the draft. Provider snapshot, hard 600-token control and actual total-token usage remain unavailable; the original 20% cost gate is **UNASSESSABLE**. Words/characters and orchestration time cannot substitute for it.

## Inspection limits and provenance

Fully inspected: `SOURCE_CARDS.json`, `ORACLE_REVIEW.md`, `HANDOFFS.json`, `RESPONDENT_INSTRUCTIONS.md`, `SCORING.md`, both reviewed versions of `run_support.py`, `build_handoffs.py`, `PROTOCOL_DRAFT.md`, final `PROTOCOL.md`, `RUNTIME.json`, and the coordinator's `HARNESS_CHECK.json` report. All rows of `TRIAL_SCHEDULE.json` and `STIMULI.json` were checked programmatically; representative schedule rows and all unique handoff forms were also read. I read `AGENTS.md`, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, current README/HANDOFF sections and relevant initial representation rules. A combined historical-context read was truncated; I do not claim complete inspection of those historical appendices.

This reviewer invoked no respondent, delegated no agent, executed no recorder initialization/mutation, and did not run the builder. Checks were read-only Python assertions and code inspection. I inspected, but did not independently rerun, the coordinator's four reported temporary-fixture checks (late response, third request, queued exposure, normal delivered round trip). The answer key was not separately re-reviewed here; consistency was checked against source cards and the oracle review. I did not independently verify the historical baseline/expansion or oracle-before-arm chronology. Local `git status` returned “not a git repository,” so live branch/commit identity and final persistence are not certified here.

The following hashes identify the final inspected versions. The initial recorder finding concerned SHA-256 `daa9e183c1319749e192cfb3eacf705bd5fbadc8db67dc85962f625b1348d346`; its corrected version is pinned below.

| File | SHA-256 |
| --- | --- |
| `SOURCE_CARDS.json` | `fbffdc8a67e3377f238feb435138babe116b737c2c7c36f1772730bc25015266` |
| `ORACLE_REVIEW.md` | `e83b0260741abc6a30b096c519715d1246df1aa979250541be276dd909a689b8` |
| `HANDOFFS.json` | `96ed17e25dedc8672aead8f1a5b1251adad6a383c3e1b72f2603ba3e5449d39a` |
| `RESPONDENT_INSTRUCTIONS.md` | `fe87135d18a799990a645db06c1e8b2ba0231aa3682e33ba8f00395d14a9c70d` |
| `SCORING.md` | `9318db99d5c3c22f3540feb22d352bd56be0988ebae2d37c512867d01bd7016f` |
| `TRIAL_SCHEDULE.json` | `0d7719ae75b7b46fe55a8121ad85ab7a4b5dacdc5b70c6a8086253d62828903b` |
| `run_support.py` | `cc41d9696810919df92d164949ec5f9cdf10a72e9f37e3df2efc339cea30a276` |
| `build_handoffs.py` | `de74ece9bbdcd0727f78a6add96622d7f51d1cc797b1dfdcf2308275f0e63f5c` |
| `PROTOCOL_DRAFT.md` | `fc8eaf87b22dac9650cd97b70328e5a72466732ef336028fbcf3a70ba3055e44` |
| `STIMULI.json` | `2aebe24f333ec75b34e1137518bc4c1e204699dffd6e13ca39009c2f6652edb5` |
| `PROTOCOL.md` | `c8a673d217781cb27be24dbd0fa4108725cbe92bb19da4469435f158e0604c77` |
| `RUNTIME.json` | `02992384e18e71ab9e5fe332228e369f836dfcfdbb9e675315790e34dbdd110e` |

Information-loss check: these materials preserve same-build identity, endpoint membership, frozen-policy status, version/accessibility and adequate-summary controls through explicit recovery. Their availability does not make the summaries lossless. The proposed trial can inspect whether a recipient follows these supplied recovery instructions, with the operational and runtime limits above; it cannot support a broader claim.
