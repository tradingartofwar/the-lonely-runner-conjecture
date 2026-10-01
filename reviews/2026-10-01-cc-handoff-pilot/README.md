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
