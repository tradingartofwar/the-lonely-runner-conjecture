# CC handoff authoring study — prepared, not run

October 1, 2026. This package asks whether a CC-informed authoring procedure preserves consequential information when compressing a longer source history. The completed [earlier pilot](../2026-10-01-cc-handoff-pilot/RESULTS_REPORT.md) tested different presentations of identical selected facts and found no robust advantage.

The new design uses six synthetic histories of 1,194–1,260 words, eighteen questions hidden from authors, and two equally limited authoring methods. Both methods write the same three-field format with a 220-word cap. Their method instructions each contain 112 whitespace-separated words. This controls visible instruction length, not token cost.

Each recipient answers from the handoff first. Only after that answer is preserved can it request the full history. Eighteen separate full-source controls diagnose task/recipient limitations. The proposed run contains twelve author contexts and fifty-four recipient/control contexts, with at most thirty-six recovery followups. These calls are **UNRUN**; no participant outputs or comparative findings exist.

| File or directory | Purpose |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | Treatment, controls, budgets, first-answer endpoint, review gates and limits |
| [SCORING.md](SCORING.md) | Separate requested correctness, exposed support, source faithfulness and recovery |
| [histories/](histories/) | Six complete synthetic source histories; no private records |
| [evaluator/QUESTIONS_AND_KEY.json](evaluator/QUESTIONS_AND_KEY.json) | Eighteen hidden queries, proposed semantic key and evidence references |
| [author_common.txt](author_common.txt), [method_conventional.txt](method_conventional.txt), [method_cc.txt](method_cc.txt) | Common output contract and matched authoring instructions |
| [recipient_common.txt](recipient_common.txt) | Common recipient response contract |
| [CONFIG.json](CONFIG.json) | Fixed preparation scope, runtime assumptions and explicit unrun status |
| [prepared/AUTHOR_INPUTS.json](prepared/AUTHOR_INPUTS.json) | Twelve exact author prompts, hashes and fixed dispatch order; deliver only prompt strings |
| [prepared/RECIPIENT_SCHEDULE.json](prepared/RECIPIENT_SCHEDULE.json) | Fifty-four fixed evaluation/control cells |
| [prepared/QUESTION_PROMPTS.json](prepared/QUESTION_PROMPTS.json) | Questions without answer keys for runtime assembly |
| [materials.py](materials.py) | Deterministic construction, strict output validation, common rendering and source followup assembly |
| [validate_materials.py](validate_materials.py), [PREFLIGHT.json](PREFLIGHT.json) | Same-author structural/arithmetic checks and dummy schema checks |
| [REVIEW_INSTRUCTIONS.md](REVIEW_INSTRUCTIONS.md) | Separate source-first key review and materials/recorder review, pending |
| [ORACLE_REVIEW_PROMPT.txt](ORACLE_REVIEW_PROMPT.txt) | Source-first review prompt without the designer's expected answers |
| [PREPARATION_MANIFEST.json](PREPARATION_MANIFEST.json) | Preparation hashes; explicitly not an execution freeze |

The hidden questions cover current decisions, evidence distinctions and modest changes within each advertised task family. Sources are available by one complete-history recovery, but their availability cannot repair the already-scored first answer. Common formatting reduces presentation differences without proving that every outcome difference is caused by fact selection alone. The retention audit checks that mechanism explicitly.

## Static reproduction

From the repository root:

~~~bash
python reviews/2026-10-01-cc-handoff-authoring/materials.py build
python reviews/2026-10-01-cc-handoff-authoring/validate_materials.py
python reviews/2026-10-01-cc-handoff-authoring/materials.py verify
~~~

Only after intentional pre-execution edits, regenerate the preparation manifest with:

~~~bash
python reviews/2026-10-01-cc-handoff-authoring/materials.py pin
~~~

The checks establish fixed scope, valid event references, absence of exact question text in author packets, balanced author order, arithmetic agreement with transcribed primitives, and schema/word-limit behavior. They do not establish source-key semantic correctness, unbiased difficulty, secure isolation, or comparative utility. All materials and checks currently share the designer's authorship.

**Next:** separately review the source-derived key, implement and rehearse the bounded recorder, complete materials review, and publish an execution freeze before running the comparison. The current package contains no live orchestration driver. Exact provider metadata and actual token accounting must be checked again before freezing; unavailable values remain unavailable and block token-efficiency claims.

AI-assisted preparation. No new mathematical result, empirical handoff advantage, novelty, external utility, or proof-status promotion is claimed.
