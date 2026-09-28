# The minimum-component selector transfers across the archive—but its tie-break is doing real work

September 28, 2026 UTC. Baseline `6cb881ad661fd2c268a19c4418a6624e17969326`, draft PR #3. Material AI involvement: one coordinating agent, one exact-calculation agent, one separately structured verification agent, and one adversarial-review agent. This is internal AI error control, not independent human mathematical validation.

**Question.** On the eighteen already archived positive-duration windows missed by tree certificates, does the unchanged positive-slack/minimum-floor-sum-component rule find a valid shared-pair containment with one query and no fallback? When the largest-slack comparator fails, is that a ranking failure or a failure of every eligible containment certificate?

**Outcome.** The minimum-component policy exits on the eight labels with positive pair-only bounds and certifies all ten remaining active labels. Excluding the two development labels, this is eight exits plus eight active certifications on the sixteen transfer labels. The largest-slack comparator has the same eight exits, certifies four active transfer labels, and fails four. Its two development labels also fail. The postselection oracle finds another certifying eligible pair in every comparator failure, so all six are ranking failures and none is a certificate-class failure.

The result is finite and fragile. The sixteen transfer labels are eight reflection pairs whose complete geometry was already archived, not sixteen independent examples and not prospective held-out data. More sharply, on the reflected `squares:1,2,5` windows the eligible pairs `{25,121}` and `{25,169}` both have the minimum component count one, but only `{25,121}` contains its blocking set in both complement safe sets. The frozen physical-lexicographic tie-break happens to choose `{25,121}`. Component count alone therefore does **not** predict containment even in this archive.

**Status.** Every selector outcome, rational bound, exact violation, reflection match, and operation ledger below is **OBSERVED** on the frozen archive. This is not a general selector theorem, new Lonely Runner existence coverage, a whole-configuration claim, a runtime result, or a novelty claim.

## 1. Frozen contract and information barrier

The [protocol](../reviews/2026-09-28-selector-transfer-audit/protocol.json), SHA256 `ccfdb403abef15f9c2cd9e08ac086232f4842b450f48308ba5a5992f8c3f9c17`, was frozen before calculation. It fixes:

- exactly the eighteen labelled windows in the collective-window archive, grouped into nine reflection pairs;
- the target `perturbed_chain:1,2,4:4` and its reflection `:19` as development labels, never transfer evidence;
- pair-only positive exit before selector work;
- for pair-only-zero records, eligibility `C_0-O_cd>0`;
- minimum exact floor-sum component count and physical-speed lexicographic ties;
- largest potential slack, with the same tie convention, as comparator;
- at most one compound containment query per rule and record, reused when both rules choose the same pair, with no fallback or retuning;
- an all-eligible-pair oracle only after decisions are immutable, solely to classify failures;
- exact integer/rational arithmetic, with no new speeds, windows, references, alternate-window campaign, broad scan, or `+7/+9` work.

The primary immediately projects the archived source to record id, residual speeds, window, pair summaries, and supplied pair-only minimum, then deletes the full source object. Archived geometry, classifications, actual answers, and reflection groups are reloaded only after both rule outcomes and every oracle classification are fixed. This repairs an information-barrier issue found during hostile review without changing any choice or outcome.

## 2. Frozen-rule results

The active transfer labels reduce by reflection to four mechanisms. Results below count both labels first and reflection mechanisms in parentheses.

| Frozen branch | Minimum components | Largest slack |
| --- | ---: | ---: |
| Pair-only positive exit, no selector query | 8 (4) | 8 (4) |
| Active transfer labels certified | 8 (4) | 4 (2) |
| Active transfer labels failed, no retune | 0 | 4 (2) |
| Development labels certified | 2 (1) | 0 |
| Development labels failed, no retune | 0 | 2 (1) |
| Ranking failures after oracle classification | 0 | 6 (3) |
| Certificate-class failures | 0 | 0 |

The five active reflection mechanisms are:

| Representative record | Eligible pairs | Minimum-component choice | Result | Largest-slack choice | Result |
| --- | ---: | --- | --- | --- | --- |
| `fibonacci:1,2,4:1` | 6 | `{21,55}`, count 1, bound `61/31680` | certified | `{89,144}` | ranking failure |
| `fibonacci:1,2,4:11` | 6 | `{21,55}`, count 1, bound `797/443520` | certified | `{21,144}` | certified |
| `squares:1,2,5:12` | 3 | `{25,121}`, count 1, bound `1/2028` | certified | `{49,169}` | ranking failure |
| `squares:1,3,4:9` | 2 | `{9,121}`, count 1, bound `1/2028` | certified | `{9,121}` | certified |
| development `perturbed_chain:1,2,4:4` | 2 | `{15,38}`, count 1, bound `49/524400` | certified | `{61,100}` | ranking failure |

Each reflected label has the exactly reflected result and is not counted as an independent example. Across the ten active labels there are 38 eligible pair scores. The two rules make 20 logical selected queries but only 18 unique physical queries because one selected query is shared on each `squares:1,3,4` reflection. No second or fallback query is issued.

The six largest-slack failures have explicit positive violation intervals. For example, in `fibonacci:1,2,4:1`, the selected pair `{89,144}` is blocked by complement speed 55 throughout `(3/88,25/712)`, with witness `271/7832`. The development target retains its known violation `(55/304,29/160)` for selected pair `{61,100}`. These are failed local containments, not failed loneliness: every archived source window has positive lonely duration.

## 3. What the postselection oracle does—and does not say

Only after both selections were fixed, the oracle tested all 38 eligible pair containments. Every active label has at least one successful eligible pair. Therefore the comparator's six failures are ranking failures; the shared-pair certificate class itself does not fail on this finite archive.

The oracle cannot be folded into the one-query policy and was charged separately. It also supplies counterpressure against overinterpreting the positive result:

- on `squares:1,2,5:12` and its reflection, `{25,121}` and `{25,169}` tie at one component, yet the first contains and the second fails;
- minimum-count ties on the four active Fibonacci labels happen to be all successful, so that family does not reveal the distinction;
- larger component count is not equivalent to failure: the `squares:1,3,4` pair `{9,169}` has two components and also contains successfully.

Thus low occurrence count is a useful frozen ranking signal here, but neither a sufficient geometric exclusion nor a monotone explanation. The lexicographic secondary rule is part of the observed success.

## 4. Controls, prior work, and cost scope

The three frozen controls retain their distinct roles:

- `strict_16`: pair-only minimum zero; both selectors choose `{6,11}` and reproduce the positive `1/896` containment certificate;
- `doubling_112`: pair-only lower bound `761/32256`; the policy exits before any active selector query;
- `tight_13`: no eligible positive-slack pair, no duration query, and the valid isolated equality `t=3/8` remains separate from positive duration.

Postselection comparison recovers eight pair-only-positive labels, eight labels where an individual triple is forced under cover, and the two development labels forming the collective-only counterpart. The sparse triple-exclusion repair, alternate-window dispatch, five-edge correction, and target containments are prior repository results, not discoveries of this audit.

The floor-sum validation computes all 108 physical pair diagnostics, while only 38 scores belong to active eligibility. Selected containment work covers 18 unique physical queries, 26 positive base components, 290 unique threshold events including window endpoints, and 272 open cells. The postselection oracle covers 38 queries, 60 components, 628 threshold events, and 590 open cells. Unlike primitives are kept separate; no wall-clock or asymptotic inference is made.

## 5. Verification

Artifacts are under [reviews/2026-09-28-selector-transfer-audit/](../reviews/2026-09-28-selector-transfer-audit/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-selector-transfer-audit/primary.py --check
python -S -B reviews/2026-09-28-selector-transfer-audit/verify.py --check
```

The primary script SHA256 is `d8b8984a70d78f805f001bfc7b6d6763eed51f975839cb084c050c48a39ce416`; the result artifact SHA256 is `bc6c3c87803057632e80d85f74af40a6a7f83bebce27b19f0dc3fce9e4e11615`. A separately structured verifier imports no primary code, reconstructs 280 exact threshold events and 262 open cells, checks dispatch, selections, containments, reflections, failure classes, and controls, and agrees on 848 compared critical fields with zero disagreements. Its `verification.json` SHA256 is `4b0a6c49556c524231e555b57593c9b18813f2cf20a5c6dc703623fbe5f82e7a`. Adversarial review found and caused repairs to verifier exit eligibility and the primary's literal information barrier before finalization. All 25 repository tests pass.

Three complementary AI agents performed exact calculation, independent reconstruction, and hostile review. Their agreement is not independent mathematical validation.

## 6. Remaining uncertainty and next bounded step

The audit upgrades the minimum-component rule from one development mechanism and three controls to a perfect result on this finite archival set. It still does not answer why the lexicographic minimum-count pair should contain, and the tied one-component success/failure pair proves that component count alone cannot answer it.

The next bounded study should therefore freeze a **tie-only discriminator** on the already archived eligible pairs, without adding any containment query to the policy. Use the `squares:1,2,5` tied pair `{25,121}` versus `{25,169}` as development data; use the tied Fibonacci pairs and `strict_16` as controls. Before reading their containment answers, predeclare one speed/window-arithmetic secondary feature derived from lap labels or complement phase range, then ask whether it distinguishes the tied success and failure under unchanged physical lexicographic fallback. Preserve a failed discriminator and every counterexample. Add no speeds, windows, references, broad scan, alternate-window campaign, or `+7/+9` work.
