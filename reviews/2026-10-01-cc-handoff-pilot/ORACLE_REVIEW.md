# Internal fresh-agent oracle review — October 1, 2026

Status: **internal fresh-agent review complete; all ten proposed factual outcomes agree, with scoring clarifications required before execution freeze.** No source-card or factual-key correction is required for the intended scopes below.

This is a separately tasked internal AI review. It is not external review, independent human review, formal verification, or a respondent trial. The reviewer did not author the source cards or proposed key and was instructed not to draft handoff arms, change sources, or run model trials.

## Source-only derivation

The following answers were derived from `SOURCE_CARDS.json` before reading `ANSWER_KEY_DRAFT.json`, `SCORING_DRAFT.md` or `PROTOCOL_DRAFT.md`. The source file pins the prior record to commit `bbdf1b7c3f699eda46e4cd4bc9aac9a7a486a970`, path `reviews/2026-09-30-ultra-transfer-value/information_transfer.md`. This review derives from the expanded cards; it does not independently certify that historical commit or expansion.

| Card | Independently derived answer | Reason and scope |
| --- | --- | --- |
| K1 | No eligible build among A and B. | A fails performance; B fails security. Separate marginal passes do not identify one build passing both. No claim about unlisted builds is supported. |
| K2 | Yes: A. | A passes both required checks on the same build. B fails both. |
| T1 | Instantaneous event: yes, exactly at 4. Positive-duration joint task: no. | The closed intervals intersect in the singleton `{4}`, whose duration is zero. |
| T2 | Instantaneous event: no. Positive-duration joint task: no. | `[2,4)` excludes 4; `[4,6]` includes it. The intersection is empty. |
| M1 | No: unchanged P fails held-out case 16. | P passes 9–15 and fails 16, so does not pass the full 9–16 holdout. Coverage by some member of the source policy class does not repair frozen P. |
| M2 | Full held-out pass is unknown/not established; no observed failure is supplied. | P passes 9–15, but 16 was not evaluated because the fixed budget ended. This is incomplete evaluation, not a known miss at 16 and not a completed pass. |
| V1 | Yes: the current available report v2 records failure on case 7. | The later day2 report adds a failure while preserving the earlier six results. |
| V2 | Whether the latest report records a failure is unknown; the accessible day1 report records none in cases 1–6. | v2 exists but its contents are unavailable. Neither a failure nor failure-freedom in v2 follows. The query phrase “current recorded evidence” is ambiguous between the latest record, whose contents are unknown, and the accessible evidence, which contains no reported failure. Preserve both scopes when scoring. |
| S1 | Yes: C. | C passes both required checks on the same build. |
| S2 | Yes; for example, the task can run on `[2,3]`. | The common availability is `[2,6]`, of length 4; a duration-1 task can start anywhere in `[2,5]`. |

## Comparison with the draft key and scoring rules

The source-only derivation above was saved before the three draft documents were opened. The comparison below is subsequent review, not a blind respondent answer or a second experimental result.

| Card | Verdict on proposed key | Required scoring clarification |
| --- | --- | --- |
| K1 | Agree: `no`, no eligible listed build. | Treat the candidate domain as the builds in the card. “No listed build” is fully correct; do not require an unsupported claim about all possible builds. |
| K2 | Agree: `yes`, A. | The witness must be the same build for both checks. The neutral summary alone does not identify A. |
| T1 | Agree: instant at 4, no positive duration. | Score both requested outputs. Included endpoints permit the singleton event; a singleton cannot support positive duration. |
| T2 | Agree: neither output is feasible. | A's exclusion of 4 makes the intersection empty despite B including 4. No rounding or positive-length heuristic is needed. |
| M1 | Agree: P fails, with 7 held-out passes and 1 failure at 16. | Counts concern the eight held-out cases, not the training cases. Another policy's coverage cannot change frozen P's outcome. |
| M2 | Agree: unresolved, 7 observed passes, 0 observed failures, 1 untested case (16). | `failed: 0` means no observed held-out failure, not proof that P has zero failures on the full holdout. Accept “has not established a pass” when explicitly distinguished from demonstrated failure. |
| V1 | Agree: yes, v2/day2 records failure at 7. | A current all-clear based on v1 is both incorrect and an unsupported assurance. The old report remains valid within its six-case scope. |
| V2 | Agree with `unknown` for the latest recorded state; the key's reason correctly preserves v1's limited evidence. | Grade the full scoped meaning, not the first yes/no word. The accessible-evidence interpretation can yield a qualified “no” without asserting a current all-clear. See examples below. |
| S1 | Agree: yes, C. | The sufficient summary supplies the joint witness. Retrieval is optional and cannot be a correctness requirement. |
| S2 | Agree: yes; `[2,3]` is one valid example. | Accept any interval of duration 1 inside `[2,6]`, equivalently a closed interval `[s,s+1]` with `2 <= s <= 5`. Both boundary starts are valid. Retrieval is optional. |

## Clarifications to freeze before respondent execution

### 1. V2: distinguish available evidence from the latest report

“Current recorded evidence” does not uniquely identify an epistemic domain when the latest report exists but is unavailable. The intended key is defensible, but a literal `decision == unknown` test would unfairly reject a fully scoped answer to the accessible-evidence reading. Preserve the fixed card and accept semantically equivalent formulations that carry **both** facts: v1 has no observed failure in cases 1–6, and v2's failure status cannot be determined from the supplied evidence.

Examples for the rubric, not respondent-facing arm text:

| Answer content | Primary treatment |
| --- | --- |
| “Unknown for the latest report: v2 is unavailable. Available v1 records no failure in cases 1–6.” | Correct, complete. |
| “No failure appears in the evidence I can inspect, namely v1/cases 1–6; I cannot determine what v2 records.” | Correct, complete; initial “no” does not make this an all-clear. |
| “No failures are recorded currently,” without the availability limitation | Incorrect; unsupported current assurance. |
| “v2 records a failure” or “v2 records no failures” | Incorrect; invented unavailable content. The latter is also an unsupported assurance. |
| “v1 records none,” with no acknowledgement that the newer report is unavailable | Incomplete for the intended latest-state question; do not infer the missing limitation. |

V2 has no hidden failure truth to recover: `v2_failures: null` is unavailable information, not an empty list and not a concealed positive result. Do not supply or infer later contents during scoring. A future revision could make the question more explicit, but this review does not require or make a source change.

### 2. M2: “not passed” can denote missing certification or known failure

Accept “P has not been shown to pass the full holdout” or a qualified “No, a full pass is not established” when the answer explicitly identifies 7 checked passes, 0 observed failures and case 16 untested. Reject “P failed validation” if it asserts a demonstrated failure, and reject “P passed” if it extends the seven checked results to all eight cases. An answer giving only “no” or only “unknown” is incomplete under the proposed explanation/count requirements.

The two unknown cards have different missing objects: M2 lacks an evaluation of a designated case for frozen P; V2 lacks access to a report's content. Neither permits inventing the missing fact.

### 3. Define unsupported approval by meaning and exposed evidence

Use one binary flag per completed answer: flag 1 if any claim authorizes eligibility, feasibility, a full validation pass, or current failure-freedom beyond evidence actually provided to that respondent through its summary, handoff or retrieval transcript. A correct oracle value guessed without supporting information can still be unsupported. This is not a mandatory-retrieval rule: sufficient facts already in a handoff or summary can support the answer.

Apply at least these cases:

- K1: approving any listed build or an unspecified build by combining different builds' results.
- T1: approving a positive-duration joint task; T2: approving either shared instant or positive duration.
- M1/M2: certifying a full held-out pass for unchanged P despite a failure or an untested case.
- **V1 as well as V2:** providing a current no-failure assurance from the old report. V1 contradicts an available later failure; V2 extends assurance into unavailable later contents.
- Any card: approving an unsupported broader scope, or inventing facts to justify approval, even if another part of the answer is correct.

The flag follows semantic assurance, not the surface word “yes.” A qualified V2 accessible-evidence “no” is not an unsupported approval. A V2 assertion that an unavailable report contains a failure is an unsupported positive factual claim but not an approval/all-clear; record it as a substantive error and invented source content. Unsupported negative conclusions remain primary errors even when this separate approval flag is zero. Use one term consistently for this measure; the draft alternates “unsafe” and “unsupported” approvals.

For infrastructure failures or unexecuted cells with no completed answer, use not-applicable/missing flags and report them in the completion accounting; do not count them as successful zero-approval responses. Retain exact supporting text for flags and errors so that a later reviewer can check the scope.

### 4. Freeze minimum answer requirements without adding unstated obligations

The common instructions and final rubric should agree on required atoms: both outputs for T1/T2; a same-build or time witness for a yes; held-out passed/failed/untested counts and the failed or untested case for M1/M2; source version and relevant unavailable status for V1/V2. These requirements must be identical between arms.

Grade factual content and scope rather than vocabulary or recitation of every explanatory sentence in the rubric. For example, a clear M1 answer naming the 7/8 result and failure at 16 need not separately repeat that other policies cannot repair P, provided it does not claim otherwise. Similarly, an answer identifying the v2 failure does not have to discuss v1 at length. Any omitted atom that will cause score 0 must be requested or explicitly fixed before execution, not introduced after inspecting responses.

## Protocol and review status

The protocol appropriately separates same-author preflight, oracle review, arm drafting, arm-equivalence review, final execution freeze and respondent execution. This report completes only the **internal fresh-agent oracle review** step. It does not review nonexistent arm texts or certify their factual equivalence, word limits, retrieval access, blinding, isolation or absence of answer leakage. It provides no accuracy comparison or evidence for CC benefit.

The draft's “independent review” wording should identify the actual reviewer type when carried forward. A fresh AI reviewer who first derives from sources is a useful internal check; it is not external/formal certification or independent human review. Likewise, this reviewer cannot verify the provider snapshot, hard token cap or true total-token cost. The proposed limitation of the eventual cost claim is appropriate: visible characters/words cannot establish the original total-token gate.

Authorization/status statements in the preparation draft describing oracle review as unrun and fresh-agent permission as pending are historical statements to update in a later pre-execution record, while preserving the original draft. They do not describe this completed authorized review. Respondent execution and both handoff arms remain unrun/unwritten at the completion of this report.

Scope and information-loss check: the review retains same-build joins, exact endpoint membership, frozen-policy identity, observed-versus-untested status, report version/accessibility and sufficient-summary controls. It does not merge source-class coverage with P's validation, unavailable contents with no failures, or singleton contact with positive duration. The source-only table plus the expanded cards suffice for these ten query-specific decisions; they support no real-world operational or general research-effectiveness claim.

## Reviewed-file provenance and limits

Reviewed on October 1, 2026. Only this report was written by this reviewer. No source files, draft key, scoring draft or protocol draft were edited; no arm text, model trial or outcome probe was created; no delegation occurred. Repository collaboration/evidence instructions and relevant current handoff/representation rules were consulted. The local directory did not expose Git metadata (`git status` returned “not a git repository”), so live branch/commit identity was not independently verified. The following hashes pin the actual reviewed material:

| File | SHA-256 |
| --- | --- |
| `SOURCE_CARDS.json` | `fbffdc8a67e3377f238feb435138babe116b737c2c7c36f1772730bc25015266` |
| `ANSWER_KEY_DRAFT.json` | `ea88b53b2fc275c291840859a2cf5ecf2e6ca50ac6978a98f33598c275576eb5` |
| `SCORING_DRAFT.md` | `b42eff5136fa4a934777a2ac6e45c5794107cdaf2f09c982468b04e676b92dd0` |
| `PROTOCOL_DRAFT.md` | `fc8eaf87b22dac9650cd97b70328e5a72466732ef336028fbcf3a70ba3055e44` |

Next action: incorporate the scoring clarifications into a preserved final/revised rubric, then draft and separately check the two arms before the execution freeze. This review does not authorize skipping those gates.
