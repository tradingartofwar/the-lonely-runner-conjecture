# CC handoff pilot: correct decisions in both formats, with an identity caveat

October 1, 2026. **Claim status: OBSERVED, within ten fixed synthetic cards.** All 80 trials completed. Both formats produced every requested decision, witness and count correctly and used the same number of source requests. Strict full-answer grading gives CC 38/40 and conventional 37/40 because five M2 explanations add an unsupported distinction between policy identities. That one-answer difference is wording-sensitive and does not establish a reliable CC presentation advantage.

| Outcome | CC-informed | Strong conventional |
| --- | ---: | ---: |
| Completed / planned | 40/40 | 40/40 |
| Adjudicated full-answer primary successes | 38/40 | 37/40 |
| Requested outputs correct, diagnostic | 40/40 | 40/40 |
| Unsupported approvals | 0 | 0 |
| Source requests | 32 | 32 |
| Retrievals on sufficient-summary controls | 0 | 0 |

The requested-output diagnostic does not replace the frozen primary endpoint, which also excludes unsupported substantive claims. Actual total-token costs are unavailable, so the original cost-effectiveness gate is **UNASSESSABLE**. Source requests and visible words are not substitutes for tokens.

## What was tested

The [protocol](PROTOCOL.md), prompts, source cards, semantic rubric, budgets and failure rules were published before any respondent execution at commit `c27323948d29c8fb25a6a45726c08bb3fe23b2d7`. A source-first internal oracle review preceded handoff construction; a separate materials review checked information matching and the recorder. The ten cards were each tested in both formats in four seeded blocks, using 80 fresh agent contexts and at most five active trial contexts.

Each format carried the same five statements with exactly matched whitespace word counts (42–60 words per handoff). Labels, grouping and order differed. Both received the same explicit instructions and source access. This tests recipient use of a presentation. It holds the choice of facts constant and leaves summary authoring, long-history memory and broad real-world transfer untested.

## Per-card results

| Card and required distinction | CC primary | Conventional primary | Requests, CC / conventional |
| --- | ---: | ---: | ---: |
| K1: separate passing checks do not make one eligible build | 4/4 | 4/4 | 4 / 4 |
| K2: A passes both checks | 4/4 | 4/4 | 4 / 4 |
| T1: instant at 4, no positive-duration overlap | 4/4 | 4/4 | 4 / 4 |
| T2: excluded endpoint removes even the shared instant | 4/4 | 4/4 | 4 / 4 |
| M1: frozen P has 7 passes,1 failure,0 untested | 4/4 | 4/4 | 4 / 4 |
| M2:7 passes,0 failures,1 untested; identity caveat below | 2/4 | 1/4 | 4 / 4 |
| V1: latest available v2 records case 7 failure | 4/4 | 4/4 | 4 / 4 |
| V2: v1 has no observed failure; unavailable v2 leaves latest status unknown | 4/4 | 4/4 | 4 / 4 |
| S1: sufficient summary gives eligible build C | 4/4 | 4/4 | 0 / 0 |
| S2: sufficient summary gives unit interval [2,3] | 4/4 | 4/4 | 0 / 0 |

Every non-control trial requested exactly one appropriate source. The eight unavailable v2 responses were intentional evidence conditions, not infrastructure failures. All sixteen sufficient-summary controls answered without retrieval.

## The qualification that changed grading

The primary coordinator and condition-masked reviewer initially read all 80 answers as successful. The reviewer then flagged “another policy” in five M2 explanations. After a countermodel discussion, the adjudicated strict reading marks those answers 0 under the frozen no-unsupported-substantive-claim rule. The full [adjudication](ADJUDICATION.md), [review](GRADING_REVIEW.md), initial grades and final grades preserve that correction.

M2 establishes that **a policy** in the source class covers case 16. It does not establish a policy **different from P**. A source class containing only P, with P actually covering 16 but its held-out evaluation stopping before 16, satisfies the supplied facts and refutes the extra distinctness claim. In M1, P is observed to fail 16, so a covering source policy really must be different. The same phrase therefore has different support in the two cases.

| Trial | Blind ID | Format | Strict primary |
| --- | --- | --- | ---: |
| R019 | U020 | Conventional | 0 |
| R071 | U025 | Conventional | 0 |
| R032 | U037 | Conventional | 0 |
| R044 | U064 | CC-informed | 0 |
| R018 | U070 | CC-informed | 0 |

All five correctly preserve P's incomplete validation,7 observed passes,0 observed failures and untested case 16. None gives a full-pass approval. U025/U064 explicitly assert another policy covers 16. The other three embed the phrase in a non-entailment explanation, allowing a more incidental or conditional reading. Treating the phrase as incidental throughout gives 40/40 in both arms; penalizing only the two explicit assertions gives 39/40 in both. These are post-collection interpretation sensitivities, not replacement endpoints. The adopted strict primary remains 38/40 versus 37/40. No presentation advantage should be claimed from that fragile one-answer difference.

## Execution and verification

Collection ran from 14:40:24.830 to 15:33:42.458 UTC, lasting 3,197.63 seconds (53m17.6s), within the one-hour budget. There were 80 completions and zero model protocol errors, infrastructure stops, unrun cells, late exclusions or respondent reruns. Logs record 80 spawns and 64 same-agent followups, yielding 144 raw responses. Completed records were checkpointed in Git at 20,40 and 60 trials without interim grading.

The [collection audit](COLLECTION_AUDIT.json) confirms unchanged frozen hashes, prompt/source consistency, raw/transcript equality, invocation-hash consistency, recomputed request and character/word counts, ascending dispatch order, the five-context cap and agreement with all published checkpoints. Every recorded response met the 150-word target. This audits saved records; it is not independent provider telemetry or inspection of hidden context.

One recording deviation is preserved in [TRANSPORT_NOTES.json](run/TRANSPORT_NOTES.json): shell framing added a newline to the first two captures. Exactly those framing bytes were removed, affected character totals corrected, and before/after lengths recorded. Pre-correction files were not retained; the extra byte is reconstructible from the record. No respondent wording or frozen material was changed.

The model configuration was inherited without overrides; an exact provider snapshot, actual token usage and a hard output-token cap were unavailable. Isolation was by fresh contexts and instructions, not a technical security sandbox. Grading is internal AI review, including the documented reviewer discussion. Four repetitions of ten cards do not provide eighty independent situations or a population reliability estimate.

## What survives, and what remains open

Both presentations supported the requested distinctions and appropriate source recovery on these cards. Their framing alone did not establish a robust advantage. The useful additional lesson is narrower: an answer can retain the correct uncertainty about a tested object while inventing a distinction between that object and an unspecified witness. Unknown identity needs to remain unknown. The paired M1/M2 records now provide a concrete regression example for that issue; they establish no novel logic theorem.

The information-loss check preserves source identity, observation versus latent truth, requested decision versus explanatory overstatement, strict versus permissive grading, and completed trial versus successful answer. Missing token telemetry blocks the cost claim. Nothing here promotes an earlier Lonely Runner proof candidate or demonstrates an external application.

The next substantive question is whether CC helps authors select and retain consequential facts when making a handoff from a longer history. A separate study would need its own freeze, strong conventional authors, equal authoring budgets, unseen downstream questions and measured costs. It remains **UNRUN**. Keep the present cases and grades fixed; do not repair these known phrases and call that held-out transfer.

## Records and replay

[RESULTS.json](RESULTS.json) contains arithmetic by card, arm and block. [GRADES.json](GRADES.json) retains initial and reviewed decisions; [BLIND_PACKET.json](BLIND_PACKET.json) and [BLIND_MAPPING.json](BLIND_MAPPING.json) expose the masking/reconciliation. [TRANSCRIPTS.json](run/TRANSCRIPTS.json), individual trial records and raw captures preserve every respondent turn. `RESULT_MANIFEST.json` hashes the result package; older preparation and execution manifests retain their historical scopes.

From the repository root:

```bash
python reviews/2026-10-01-cc-handoff-pilot/run_support.py check
python reviews/2026-10-01-cc-handoff-pilot/analyze_results.py audit
python reviews/2026-10-01-cc-handoff-pilot/analyze_results.py summarize
```

These replay integrity and aggregation over saved records. They do not reproduce stochastic model calls or replace semantic grading.
