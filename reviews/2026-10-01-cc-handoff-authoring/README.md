# CC handoff authoring study — execution package

October 1, 2026. This package asks whether a CC-informed authoring procedure preserves consequential information when compressing a longer source history. The completed [earlier pilot](../2026-10-01-cc-handoff-pilot/RESULTS_REPORT.md) tested different presentations of identical selected facts and found no robust advantage.

The new design uses six synthetic histories of 1,194–1,260 words, eighteen questions hidden from authors, and two equally limited authoring methods. Both methods write the same three-field format with a 220-word cap. Their method instructions each contain 112 whitespace-separated words. This controls visible instruction length, not token cost.

Each recipient answers from the handoff first. Only after that answer is preserved can it request the full history. Eighteen separate full-source controls diagnose task/recipient limitations. The proposed run contains twelve author contexts and fifty-four recipient/control contexts, with at most thirty-six recovery followups. At the execution-freeze boundary all participant calls were **UNRUN**. Current collection state is in run/STATUS.json; any later findings require a separate result report.

| File or directory | Purpose |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | Treatment, controls, budgets, first-answer endpoint, review gates and limits |
| [SCORING.md](SCORING.md) | Separate requested correctness, exposed support, source faithfulness and recovery |
| [histories/](histories/) | Six complete synthetic source histories; no private records |
| [evaluator/QUESTIONS_AND_KEY.json](evaluator/QUESTIONS_AND_KEY.json) | Eighteen hidden queries, proposed semantic key and evidence references |
| [author_common.txt](author_common.txt), [method_conventional.txt](method_conventional.txt), [method_cc.txt](method_cc.txt) | Common output contract and matched authoring instructions |
| [recipient_common.txt](recipient_common.txt) | Common recipient response contract |
| [CONFIG.json](CONFIG.json) | Fixed scope and zero-call state at the freeze boundary |
| [prepared/AUTHOR_INPUTS.json](prepared/AUTHOR_INPUTS.json) | Twelve exact author prompts, hashes and fixed dispatch order; deliver only prompt strings |
| [prepared/RECIPIENT_SCHEDULE.json](prepared/RECIPIENT_SCHEDULE.json) | Fifty-four fixed evaluation/control cells |
| [prepared/QUESTION_PROMPTS.json](prepared/QUESTION_PROMPTS.json) | Questions without answer keys for runtime assembly |
| [materials.py](materials.py) | Deterministic construction, strict output validation, common rendering and source followup assembly |
| [validate_materials.py](validate_materials.py), [PREFLIGHT.json](PREFLIGHT.json) | Same-author structural/arithmetic checks and dummy schema checks |
| [REVIEW_INSTRUCTIONS.md](REVIEW_INSTRUCTIONS.md) | Review procedure; completed reviews are in review/ |
| [ORACLE_REVIEW_PROMPT.txt](ORACLE_REVIEW_PROMPT.txt) | Source-first review prompt without the designer's expected answers |
| [PREPARATION_MANIFEST.json](PREPARATION_MANIFEST.json) | Historical preparation hashes at d03d3e0; not the live execution verifier |

The hidden questions cover current decisions, evidence distinctions and modest changes within each advertised task family. Sources are available by one complete-history recovery, but their availability cannot repair the already-scored first answer. Common formatting reduces presentation differences without proving that every outcome difference is caused by fact selection alone. The retention audit checks that mechanism explicitly.

## Verification and provenance

The preparation package and original 23-file manifest remain recoverable at commit d03d3e0277541dd77e579fb418e4c76fec793174. That historical manifest is intentionally not regenerated to describe later execution. Its preparation-only verifier is not the live execution check.

~~~bash
python reviews/2026-10-01-cc-handoff-authoring/run_support.py check
python reviews/2026-10-01-cc-handoff-authoring/run_support.py status
~~~

The separate source-first review agrees with all eighteen substantive answers. SCORING.md adopts its item-level clarification that unasked explanatory details remain optional. Review provenance, recorder rehearsal and materials review are in review/. Static PREFLIGHT.json retains the preparation checker's limited scope; its pending review fields are superseded by the separate review records, not evidence of a semantic review by that checker.

EXECUTION_GUIDE.md governs the single-writer recorder and exact-message envelopes. RUNTIME.json records available controls and unavailable metadata. EXECUTION_MANIFEST.json pins the protocol, inputs, keys, reviews and recorder before any author call. After author collection, all author outputs must be committed before any recipient/control is launched. The owner checks remote publication at both gates.

Collection and later grading remain descriptive internal AI work on six paired synthetic histories. No token-efficiency, broad operational-benefit, novelty or mathematical-proof claim is supported by this package alone.
