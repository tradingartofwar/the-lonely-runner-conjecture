# Completed handoff-authoring comparison

October 2, 2026 UTC. **OBSERVED: bounded synthetic study, completed.** AI-generated materials and participants; owner grading followed by a separate internal AI review. This is not independent human validation.

The frozen comparison is complete. CC-authored handoffs produced **17/18 supported complete first answers**, strong conventional handoffs **18/18**, and full-source controls **18/18**. No recipient requested source recovery, so final answers and scores are identical. The separate retention review found adequate source-true support for all 18 questions in each authoring condition. This study therefore shows **no observed CC authoring advantage**, and no information-selection advantage. One CC recipient misapplied uncertainty about destination verification to the contents of a fixed backup. A single response does not establish that the authoring method caused this error or that conventional authoring is generally superior.

## Completed scope and primary results

The [frozen protocol](PROTOCOL.md) tests six development-informed synthetic histories, three hidden questions per history, and one author realization per method/history. Both authoring instructions have 112 whitespace words; the same history, common schema, 220-word decoded-value cap and inherited configuration apply to both. Recipients receive one handoff or the full history, one exact query, a common instruction and a 160-word answer cap. The conventional method explicitly tracks sources, versions, dependencies and uncertainty.

| Outcome | CC handoff | Conventional handoff | Full source |
| --- | ---: | ---: | ---: |
| Completed recipient contexts | 18/18 | 18/18 | 18/18 |
| Correct requested outputs | 17/18 | 18/18 | 18/18 |
| Supported complete first answers | 17/18 | 18/18 | 18/18 |
| Supported complete final answers | 17/18 | 18/18 | 18/18 |
| Answers with unsupported assertions | 1 | 0 | 0 |
| Unsupported approvals | 0 | 0 | 0 |
| Source recovery requested / served | 0 / 0 | 0 / 0 | 0 / 0 |
| Handoff/query retention checks adequate | 18/18 | 18/18 | Not applicable |

Primary success requires protocol validity, every requested output correct, support in the evidence actually exposed, and faithfulness to the complete source under the query's explicit hypothetical. These are semantic judgments; they are not produced by keyword matching. Optional key explanations are not extra requirements. The [item-level optionality review](review/ORACLE_COMPARISON.md) controls grading. Volunteered assertions are still checked.

| Paired history | CC first / final | Conventional first / final | Full source | CC minus conventional |
| --- | ---: | ---: | ---: | ---: |
| H01 Rook readiness | 3/3 | 3/3 | 3/3 | 0 |
| H02 Canal timing | 3/3 | 3/3 | 3/3 | 0 |
| H03 Juniper acceptance | 3/3 | 3/3 | 3/3 | 0 |
| H04 Harbor archive | 2/3 | 3/3 | 3/3 | -1 |
| H05 Cedar resource allocation | 3/3 | 3/3 | 3/3 | 0 |
| H06 Orchid straightforward control | 3/3 | 3/3 | 3/3 | 0 |

“First / final” has one displayed fraction because the two scores are identical. There are six paired history clusters, not 36 independent authoring examples. Current-decision questions score 6/6 for each method; evidence-scope questions score CC 5/6 and conventional 6/6; changed-use questions score 6/6 each. Full-source controls score 6/6 in each category. The six correct acknowledgments of source-level uncertainty (two per condition, H01-Q2 and H02-Q3) are separately tagged and remain successes.

All twelve authors completed with valid outputs. CC handoffs used 186–203 decoded words (mean 194.17); conventional handoffs used 194–212 (mean 202.5). Equal caps and directive word counts do not mean identical realized length, information content or token cost. All 54 recipient outputs were protocol-valid. There were no missing trials, infrastructure failures, protocol errors, budget stops or observed deviations in this restart.

## One clear failure and preserved sensitivities

**R010 / Q035, CC, H04-Q2:** the question asks how many distinct stored backup objects two labels establish and whether the stored backup includes the post-M0 addition K97 revision 1 and revision change K12 revision 2. Both labels name one fixed object, object-amber, containing M0: K1–K96 revision 1. Neither later change is in that backup.

The recipient correctly answers “one” but says the changes' presence is unresolved because destination ingestion and verification are not established. That transfers uncertainty between different objects and operations. The incomplete destination audit does not make the fixed backup contents unknown. The delivered S09 handoff retains M0's contents, the shared object identity, and both later deltas. Its object-to-snapshot relation is compressed into adjacent clauses; the review accepts that ordinary contextual relation while preserving the stricter omitted-edge objection. Neither reading rescues the requested backup-content answer. The preferred classification is a recipient scope error despite adequate retained information, without claiming that its psychological cause has been established. No source recovery was requested.

This supplies a concrete regression: an uncertainty claim must remain attached to the particular object, version and operation whose evidence is incomplete. Cautious language can itself be unsupported. The fixed source is H04 events H02–H03 and H08–H12; the exact exposure and response remain in the masked packet and Q035 trial. The regression does not require a new framework or imply novelty.

**R040 / Q002, CC, H04-Q3:** after two specified comparisons hypothetically succeed, the recipient correctly gives 95/97 current revisions verified, refuses retirement and identifies the two remaining deltas. Its final sentence, “The planned work remains unexecuted,” is supported if it refers to the immediately discussed remaining delta work. Read broadly as all originally planned work, it contradicts the two completed comparisons. Before unmasking, owner and reviewer retained the contextual pass and explicitly fixed the broader-reading sensitivity:

| Reading | CC primary | Conventional primary | Full-source primary | Requested-output scores |
| --- | ---: | ---: | ---: | --- |
| Preferred contextual reading | 17/18 | 18/18 | 18/18 | 17/18, 18/18, 18/18 |
| Broad “all planned work” reading | 16/18 | 18/18 | 18/18 | Unchanged |

Under the broad reading CC has two unsupported-assertion answers and H04 falls to 1/3. No unsupported approval is introduced. This sensitivity is an alternative judgment of the same text, not an extra trial.

**S12 / A002, conventional, H01:** “no booking completion is recorded” can refer to an uncompleted station-selection booking, or broadly deny an existing room booking. Only the narrower reading is supported. No recipient repeats that optional clause; all three technical queries remain supported and all three answers pass. Retain this author-wording caveat without inventing a downstream error or certifying lossless compression.

The [separate grading review](grading/GRADING_REVIEW.md) examines all 54 answers and the strongest defenses of R010. The [retention audit](grading/RETENTION_AUDIT.json) provides 36 query-level records with 81 exact handoff passages, source event IDs and derivations. All quoted passages were mechanically matched to the saved handoffs. The [adjudication](grading/ADJUDICATION.md) and final grades were written before method unmasking; no numerical initial grade changed.

## Execution, preservation and audit

The original attempt's [zero-delivery closeout](../2026-10-01-cc-handoff-authoring/RESULTS_REPORT.md) remains unchanged. Its first uppercase worker name was rejected and collection stalled before any participant received a prompt. The reason for the subsequent pause is not established. This restart used the same reviewed substantive materials, a new identity and clocks, corrected lowercase dispatch instructions, owner progress monitoring, and a successful real dummy dispatch/capture check outside the study. There were no participant outcomes to select or discard from the earlier attempt.

| Gate | Published commit or record |
| --- | --- |
| Original failed attempt preserved | `a5f1500d1361b0d4823cd5c85f85c0ee3ddc0218` |
| Run02 execution freeze, before authors | `379403bbc6dfad30e68a02d18d69eabf0dc65404` |
| All authors sealed, before readers | `874379c4a0e60707c292b59f5bb3a8fd3b694baa` |
| Closed collection, initial grades and audit | `e4f701095719f0dce2f8b5179b4383b0c6a418ff` |
| Final grades and reviewer reports | This report's result commit; resolve with `git log -1 --format=%H -- reviews/2026-10-01-cc-handoff-authoring-run02/RESULTS_REPORT.md` |

Authors ran from 00:17:41.761840 to 00:34:12.687486 UTC on October 2: 990.93 seconds against 1,200. Readers ran from 00:36:02.322060 to 01:18:31.477953: 2,549.16 seconds against 3,300. The 109.63-second publication interval between phases, preparation and semantic review are outside collection clocks. Wall times include orchestration and are not inference-time or cost measurements. Maximum recorded concurrent study contexts was three, within the cap of five.

The stored-record audit passes for all 35 frozen files, 66 trials, 66 unique fresh-context identities and 66 raw responses. It checks exact prompts, individual/aggregate agreement, message hashes, raw envelopes, decoded validation counts, first/final consistency, recorded deadlines/order, all checkpoints, and author bytes against their published seal. No source followup occurred. All 145 run files pinned by COLLECTION_SEALED.json remain unchanged. That additional seal was generated after initial grading; collection had already closed before grading, but the seal is not represented as a prospective pre-grading certificate.

The result manifest pins package files, including the preserved reviews, exact source and response records, grades and descriptive outputs. The manifest omits only itself and Python cache files. Frozen preparation files still describe their original pre-execution boundary; this report and run/STATUS.json give the completed status. Do not rewrite a frozen README or rerun collection to make its tense current.

## Interpretation and limits

The evidence supports a completed, mostly ceiling-level descriptive comparison. It supplies no observed CC benefit for these histories and no loss of query-critical information in either set of handoffs. It does not establish general equivalence, general conventional superiority, or the absence of useful CC applications. One author per method/history and one reader per cell leave stochastic variation unresolved; three related questions share each handoff. No inferential test or population effect estimate is reported.

The six histories are synthetic, about 1,200 words, and deliberately exercise distinctions already developed in the project. They are not sampled real conversations, unseen conceptual domains, or context-limit stress tests. H06 is deliberately easy; several histories repeat decisive primitives near the end. The conventional comparison is strong, and differences in wording remain possible despite a shared rendering and cap. Adequate retention alone does not isolate why one reader erred.

All participants used fresh no-history-fork contexts with inherited settings and no model/reasoning overrides. Evaluator exclusion and tool bans are instructions in a shared environment, not technical access controls. The audit verifies stored records, not provider-side telemetry or proof of inaccessible files. The separate reviewer had initial grades and source truth but no condition map, method prompts or run records; style may reveal method. Owner masking is partial because the owner knows the design and earlier materials. These are internal AI checks, not secure blinding or independent human certification. Provider snapshot, actual tokens and hidden compute are unavailable; no token-efficiency or cost-effectiveness claim follows. Zero recovery requests do not test the recovery branch's effectiveness.

## Representation checkpoint and next work

The supported use is answering the 18 frozen task-family queries from a short handoff and each explicit hypothetical. Both methods retained the needed version, identity, denominator, common-offset, shared-resource and boundary relations on contextual review. Most chronology and optional detail were omitted; that omission has not been shown safe for arbitrary new questions. The richer source is each pinned history, recovered through complete-source delivery and event IDs. R010 exposes misuse of an available object/stage relation; R040 and S12 expose ambiguous scope in optional wording. Preserve those limits rather than label a handoff globally lossless or treat every uncertainty statement as faithful.

The present comparison is finished. Do not extend it opportunistically to seek a favored result. A future authoring claim would need separately designed cases, repeated realizations and a new freeze.

The recommended next substantive task returns to the [rank-three mathematical study](../../notes/CC_THREE_PARAMETER_TEST_2026_09_30.md): derive a coverage criterion for a sheet's joint integer-contact image. Four selected sheets covered 89/89 training cases but only 310/318 held-out cases; all 36 supplied sheets covered 407/407. The eight misses are compact-selection failures, not Lonely Runner counterexamples. Use them as development counterexamples, retaining shared-point geometry, lap labels, two saturated integer relations and physical recovery. Then freeze a new selection rule and genuinely fresh validation domain. Repairing the old holdout is not new transfer evidence. No such derivation, new mathematical run or optional software export was launched as part of this comparison.

## Reproduce the saved-record checks

From the repository root:

```bash
python reviews/2026-10-01-cc-handoff-authoring-run02/run_support.py check
python reviews/2026-10-01-cc-handoff-authoring-run02/analyze_results.py audit
python reviews/2026-10-01-cc-handoff-authoring-run02/analyze_results.py summarize
python reviews/2026-10-01-cc-handoff-authoring-run02/summarize_sensitivity.py
```

These reproduce stored-record checks and descriptive arithmetic from semantic grades; they do not re-create the AI responses or independently certify the judgments. Do not rerun the one-time mask command. Inspect INITIAL_GRADES, FINAL_GRADES, ADJUDICATION, GRADING_REVIEW and RETENTION_AUDIT together. The result manifest can be checked by hashing each named relative path with SHA-256.
