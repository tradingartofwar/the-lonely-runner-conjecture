# CC handoff pilot: completed results

October 1, 2026. **OBSERVED:** all 80 trials completed. Both formats returned 40/40 correct requested outputs with 32 source requests. Strict full-answer grading gives CC 38/40 and conventional 37/40 because five M2 explanations add unsupported policy distinctness; the initially permissive interpretation gives 40/40 each. This wording-sensitive difference does not establish a robust CC presentation advantage. The original token-cost gate is unassessable.

Start with [RESULTS_REPORT.md](RESULTS_REPORT.md), [RESULTS.json](RESULTS.json), [ADJUDICATION.md](ADJUDICATION.md) and [GRADING_REVIEW.md](GRADING_REVIEW.md). All outcomes, including the five strict-reading errors, are preserved.

| Record | Purpose |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md), [SCORING.md](SCORING.md), [RUNTIME.json](RUNTIME.json) | Frozen design, semantic rule and runtime limits |
| [FROZEN_MANIFEST.json](FROZEN_MANIFEST.json) | Execution-input hashes published at c273239 before any respondent |
| [ORACLE_REVIEW.md](ORACLE_REVIEW.md), [MATERIALS_REVIEW.md](MATERIALS_REVIEW.md) | Pre-execution internal source and material reviews |
| [HANDOFFS.json](HANDOFFS.json), [STIMULI.json](STIMULI.json) | Matched statements and 80 exact prompts |
| [TRANSCRIPTS.json](run/TRANSCRIPTS.json), [INVOCATIONS.jsonl](run/INVOCATIONS.jsonl) |80 trial records and 144 invocation records |
| [PRIMARY_GRADES.json](PRIMARY_GRADES.json), [CHECK_GRADES.json](CHECK_GRADES.json), [GRADES.json](GRADES.json) | Initial grading, masked review and adjudication |
| [BLIND_PACKET.json](BLIND_PACKET.json), [BLIND_MAPPING.json](BLIND_MAPPING.json) | Normalized evidence packet and condition reconciliation |
| [COLLECTION_AUDIT.json](COLLECTION_AUDIT.json), [TRANSPORT_NOTES.json](run/TRANSPORT_NOTES.json) | Integrity checks and the documented framing-byte correction |
| [RESULT_MANIFEST.json](RESULT_MANIFEST.json) | Result-package file hashes |

The run closed within 53m17.6s with no protocol errors, infrastructure stops, late exclusions or unrun cells. Raw captures live in `run/incoming/`; individual records in `run/trials/`; ungraded terminal-record checkpoints at 20/40/60 trials remain in `checkpoints/`. The replay commands in the report check stored evidence and arithmetic, not stochastic model reproduction.

Historical preparation manifests and statuses below describe their original pinned stage. The final protocol, result report and result manifest govern the completed pilot.

## Preserved preparation record

The following describes the earlier preparation commit `dea5e09`; its pending-authorization/review statements are historical.

# CC-informed versus conventional handoffs: pilot preparation

October 1, 2026. **No model answers have been collected.**

The maintainer selected the small handoff comparison proposed in the September30 information-transfer review. This directory prepares its ten fixed synthetic cards, proposed answer key and80-trial order. It preserves the independent-review-before-arm-drafting gate.

| Artifact | Status |
| --- | --- |
| [PROTOCOL_DRAFT.md](PROTOCOL_DRAFT.md) | Design, gates, budgets, scope and exposed runtime limitations |
| [SOURCE_CARDS.json](SOURCE_CARDS.json) | Ten fixed cards, neutral summaries, exact source records and queries |
| [ANSWER_KEY_DRAFT.json](ANSWER_KEY_DRAFT.json) | Proposed answer key; separate review pending |
| [TRIAL_SCHEDULE.json](TRIAL_SCHEDULE.json) | Four fixed shuffled blocks,80 planned answers; all UNRUN |
| [SCORING_DRAFT.md](SCORING_DRAFT.md) | Per-card correctness, unsafe approval and cost interpretation |
| [PREFLIGHT.json](PREFLIGHT.json) | Same-author static semantic/structure checks passed; no respondent results |
| [MATERIAL_PINS.json](MATERIAL_PINS.json) | Stage1 input identities; not a complete execution freeze |
| [prepare_materials.py](prepare_materials.py) | Deterministic material construction; no model calls |
| [validate_materials.py](validate_materials.py) | Static preflight only; no model calls |

Reproduce preparation checks from the repository root:

```bash
python reviews/2026-10-01-cc-handoff-pilot/prepare_materials.py
python reviews/2026-10-01-cc-handoff-pilot/validate_materials.py
```

The preflight recovers four pairs with identical neutral summary/query text and different correct answers: K1/K2, T1/T2, M1/M2, V1/V2. That is a property of the designed data, not a comparative result for CC. It confirms that summary-only answers lose a relevant distinction in those pairs, while S1/S2 are sufficient-summary controls.

The experiment must ask whether the handoff helps a recipient recognize that loss and recover the needed source, against a strong conventional baseline. It does not test whether extra facts help by secretly giving one arm more information.

**Next:** obtain explicit authorization for fresh review/respondent agents, then review the oracle, draft and audit the matched arms, publish the final execution freeze, and run the bounded comparison. The session currently requires explicit authorization before launching new subagents. No new agents, API calls, paid compute or model trials were launched for this preparation. Total-token cost and exact provider-model identity are unavailable from the exposed agent interface; preserve these limitations before any execution.
