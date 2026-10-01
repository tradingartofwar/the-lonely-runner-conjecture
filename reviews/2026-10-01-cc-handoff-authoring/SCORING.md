# Proposed semantic scoring and retention audit

**Preparation version; review required before execution.** Freeze after source-first review and before any author sees a history.

The source histories establish scenario truth. A query's explicit hypothetical replaces only the named assumptions for that question. The proposed key identifies relevant evidence and expected outputs. Grade meaning rather than keywords, JSON formatting aesthetics, field placement, or the use of CC terminology. Event citations are helpful but are not required; a faithful sufficient summary can support a decision without reproducing every primitive or source identifier.

## Separate dimensions

For each substantive answer at each stage, record:

| Field | Values and interpretation |
| --- | --- |
| requested_outputs_correct | 1 if all outputs actually requested by the query are correct relative to the complete scenario and query; otherwise 0 |
| supported_by_exposure | 1 if every substantive assertion in the answer follows from the evidence actually delivered plus the explicit query; otherwise 0 |
| source_faithful | 1 if every substantive assertion is also supported by the complete source and explicit query, or accurately describes an actual exposure gap; otherwise 0 |
| primary | 1 only if all three previous fields are 1 and the response respects the protocol; otherwise 0 |
| unsupported_assertion | 1 if any substantive assertion exceeds exposed evidence or complete-source support, whether positive or negative; record which failed |
| unsupported_approval | 1 if an unsupported assertion specifically approves readiness, validation, retirement, or feasibility |
| abstention | none / justified_exposure_gap / unnecessary / source_itself_underdetermined |
| error_mechanism | missing_fact / lost_relation / stale_scope / false_claim_in_handoff / recipient_error / protocol / ambiguous; explanatory, not a replacement score |

A correct guess from an inadequate handoff may have requested_outputs_correct=1 but primary=0. A faithful statement that the handoff does not establish the source's known answer can have supported_by_exposure=1 but primary=0. H01-Q2's unknown packet performance, by contrast, is the correct full-source answer and can earn primary=1. Uncertainty is not automatically a failure or automatically success.

Source-grounding has two levels. A recipient may reasonably follow a claim in its handoff even when that claim was authored incorrectly. Its local exposure-support flag can be 1 while source_faithful is 0, even if the requested decision happens to be right. Strict primary then remains 0 and the author retention audit records the false claim. Do not attribute every downstream error to the recipient. If a handoff explicitly states a current, source-supported conclusion, the recipient can use it without recreating the entire underlying calculation.

The key's required items are a semantic checklist for the question, not permission to impose unasked details. Numerical fields support arithmetic verification; do not require a number the query never asks for merely because it appears in a rationale. For example, H01-Q2 does not require reciting A's old 99/100 value, only its old-firmware scope and lack of a new result. H03-Q1's correct counts and scoped rejection do not additionally require the phrase "at least eleven." Accept exact equivalent fractions, finite decimals, and sensibly rounded percentages (within 0.1 percentage point for requested rate displays). Query-required counts and resource totals must be exact.

Optional explanations remain substantive evidence claims. A correct decision with an invented distinction, observation, identity, completion, or external requirement loses strict primary credit. An explicitly conditional statement that does not assert its antecedent is not an unsupported factual assertion. If wording genuinely has both readings, preserve the competing readings and score sensitivity, resolving without condition labels where possible. Do not invent additional obligations after seeing outputs.

## Status and denominator rules

Keep 18 planned handoff questions per method and 18 planned full-source controls. AUTHOR_PROTOCOL_ERROR gives its three dependent primary scores 0 with the author-error status; no recipient answers are invented. A recipient protocol error gives primary 0. Actual infrastructure failures, phase deadline stops, leakage-excluded cells, and never-dispatched cells have missing scores, with counts and reasons. For incomplete collection, show correct/planned and correct/observed alongside missingness; do not turn missing outcomes into ordinary semantic errors or drop them silently.

If a valid first answer is saved before a recovery-stage infrastructure failure, retain its primary score. Its final outcome is missing; do not pretend recovery succeeded. If the recipient declines recovery, the valid first answer is also the final answer. A second request or malformed recovery response is a post-recovery protocol error without erasing the first answer.

## Retention audit

After collection closes, give a reviewer each generated handoff, its history, and that history's questions, with condition name and author identity replaced by opaque IDs. For each query, identify whether the handoff:

1. Supports every requested output using source-true statements and the query's allowed hypothetical.
2. Leaves a specific fact or relationship to recover.
3. States a source-false or unsupported fact.

Record exact handoff passages and source event identifiers, not keyword counts. A valid cached decision can be adequate for a current question and inadequate for a changed-use question. No event-reference requirement or CC-specific schema earns extra credit. This audit supplies a plausible account of selection failures; it does not statistically isolate every wording or reasoning effect.

## Review procedure and reporting

Grade only after all scheduled collection closes. Prepare a condition-masked packet containing the question, delivered handoff/history, original first answer, any source followup and final answer. Mask method names, trial mapping and author identities; do not rewrite the substantive handoff text to disguise style. Masking is partial because style may reveal a method. A separate internal reviewer checks initial grades. Preserve initial grades, disagreements, adjudication, and any sensitivity in the report.

Report history-level paired differences before a single aggregate. Keep current-decision, evidence-scope and changed-use outcomes distinct. The 18 per-method answers arise from six handoffs, with one author realization each. Full-source controls measure recipient execution on these tasks, not an infallible oracle. Token efficiency, broad practical superiority, novelty, and external deployment benefit remain outside the available evidence.
