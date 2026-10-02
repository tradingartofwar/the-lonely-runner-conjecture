# A midpoint margin ranks the fitted tie—but does not certify containment

September 28, 2026 UTC. Baseline `9ef34894a8657d91f1276a0a6fff32322b3e64da`, draft PR #3. Material AI involvement: one coordinating agent, one exact-calculation agent, one separately structured verification agent, and one adversarial-review agent. This is internal AI error control, not independent human mathematical validation.

**Question.** When several eligible base pairs tie for the minimum positive-component count, can one exact complement-safety sample at each component midpoint distinguish the successful and failed compound containments without performing another containment query?

**Outcome.** The frozen maximin midpoint rule ranks the known successful squares pair `{25,121}` above the known failed pair `{25,169}` and selects a containing pair on all seven active labels. On the fitted development tie this is the same pair already chosen by physical lexicographic order, so it adds an ordering explanation but no new certification outcome. More importantly, the failed pair's midpoint score is still positive: `23/1352`. Its complement blocks away from the midpoint. Therefore the feature's sign is not a geometric exclusion or containment certificate.

The four Fibonacci control labels and `strict_16` all succeed under the selected rule. That does not supply negative validation: every tied control pair contains. The candidate changes the old lexicographic choice on all four Fibonacci labels while remaining inside an all-success set.

**Status.** Scores, choices, exact containments, false-positive counts, costs and dispatch outcomes are **OBSERVED** on the frozen development and archival controls. No general selector, containment theorem, runtime result, whole-configuration result, new Lonely Runner existence coverage or novelty claim is made.

## 1. Frozen information contract

The [protocol](../reviews/2026-09-28-tie-midpoint-discriminator/protocol.json), SHA256 `e62d116b764aa0869788dffb36785935d08e3de1ddb38d3e0ca11ca23ba3f2e3`, was frozen before control calculation.

It fixes:

- the reflected `squares:1,2,5:12/:39` success/failure tie as **development data**;
- the four tied Fibonacci labels and `strict_16` as archival controls;
- `doubling_112` and `tight_13` as dispatch controls;
- no new speeds, windows, cores, references, broad scan, alternate-window campaign or `+7/+9` work;
- exact rational arithmetic, physical-speed lexicographic fallback, one selected compound containment query and no fallback;
- a separately charged all-tied-pair oracle only after scores and choices are immutable.

The primary immediately projects the pinned transfer archive to ids, speeds, windows, pair-only minima, eligible pairs, slacks and floor-sum component counts, then deletes the full source object. Pinned containment answers, violations, actual duration and mechanism labels are reloaded only after midpoint scores, candidate choices, selected queries and the separately calculated all-tied oracle are immutable. A later hardening prevents even diagnostic eligible/component fields from crossing the projection after `doubling_112`'s pair-only exit.

## 2. Candidate rule

For every eligible pair `{a,b}` tied at the minimum exact component count, reconstruct each positive component `I=(l,r)` of `B_a intersect B_b` and sample only

`t_I=(l+r)/2`.

For complement speed `v`, define the signed midpoint margin

`M(v,I)=||v t_I||-1/8`,

where `||x||` is distance to the nearest integer. Positive means strictly safe at the midpoint; zero is also safe because blocking is strict; negative means blocked at that sampled time. The pair score is

`M(a,b)=min M(v,I)`

over both complement speeds and all positive components. Maximize this score, then use physical lexicographic order for an exact tie.

This rule is intentionally not a containment query. It sees no complement threshold schedule away from the prescribed midpoints and cannot search for violations before selection. After selection it receives the inherited single compound query `B_a intersect B_b subset Safe_c intersect Safe_d`.

## 3. Exact outcomes

The seven active labels represent four reflection mechanisms: one squares development mechanism, two Fibonacci control mechanisms, and `strict_16`.

| Representative | Tied minimum pairs and exact midpoint scores | Frozen choice | Postselection geometry |
| --- | --- | --- | --- |
| squares development `:12` | `{25,121}:1475/13068`; `{25,169}:23/1352` | `{25,121}` | first contains; second fails |
| Fibonacci `:1` | `{21,55}:127/770`; `{21,89}:247/712` | `{21,89}` | both contain |
| Fibonacci `:11` | `{21,55}:25/231`; `{21,89}:239/712`; `{21,144}:5/24` | `{21,89}` | all three contain |
| `strict_16` | `{6,11}:59/264`; `{11,16}:13/128` | `{6,11}` | both contain |

Every reflection has the same scores, choices and outcomes and is not counted as an independent example. The candidate changes the inherited physical-lexicographic choice from `{21,55}` to `{21,89}` on all four Fibonacci labels. Both choices contain, so this is a ranking change without outcome separation.

Across all tied pair labels, postselection truth gives:

| Midpoint-sign classification | Label count | Reflection mechanisms |
| --- | ---: | ---: |
| True positive | 14 | 8 |
| False positive | 2 | 1 |
| False negative | 0 | 0 |
| Score-order inversion | 0 | 0 |

The false positives are the reflected `{25,169}` failure. On the first window, its only base component is `(271/1352,21/104)` with midpoint `34/169`. Complement speed 49 has midpoint distance `24/169`, hence the positive margin `24/169-1/8=23/1352`. Nevertheless, speed 49 blocks on the nonempty subinterval `(79/392,21/104)`. A safe center therefore does not control the component edge.

This is the consequential distinction: **a pointwise ranking feature is not an interval exclusion**. The development ordering is correct, but the positive score cannot rule out the complete-cover arrangement required by the failed containment.

## 4. Dispatch and cost scope

- `doubling_112` exits before scoring or containment with its prior pair-only lower bound `761/32256`.
- `tight_13` has no eligible positive-slack pair, makes no duration query, and retains the valid isolated equality `t=3/8` separately.
- No second query, endpoint rescue or alternate window is used.

Preselection reconstructs 16 tied pair-components, samples 16 midpoints, and makes 32 complement phase/distance evaluations. Every tied pair-label instance in this scope has exactly one component, so the frozen minimum-over-components aggregation is untested beyond the singleton case. Reconstruction uses 57 base blocking pieces and 143 lap candidates; this is a bounded information ledger, not a uniform runtime claim.

The frozen candidate issues seven selected containment queries covering 99 open cells and 106 unique threshold events including window endpoints. The postselection oracle separately issues 16 tied-pair queries covering 232 open cells and 248 unique threshold events. Oracle work is not part of the one-query rule.

## 5. Verification

Artifacts are under [reviews/2026-09-28-tie-midpoint-discriminator/](../reviews/2026-09-28-tie-midpoint-discriminator/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-tie-midpoint-discriminator/primary.py --check
python -S -B reviews/2026-09-28-tie-midpoint-discriminator/verify.py --check
```

The final primary SHA256 is `65cefe76849a46ddfc6538f17e806dd92f6cbb0d33f83bffe038ddc1ad721b0d`; `results.json` is `720ef7a31bc933d16b598525cc84a4e928b4cc1dc8bbcd524aa5ecbd1c372eb8`. The verifier imports no primary code. It independently reconstructs threshold events, components, midpoint phases, choices, selected containments, all-tied oracle outcomes, reflections and dispatch. It compares 491 scalar fields with zero disagreement. Its final `verification.json` SHA256 is `64996ddd202b27a16cc8287c9c10b3e0193b3b4dcb51fb166d7eaac27d926cd4`.

All 25 repository tests pass. Three complementary AI agents performed the primary calculation, independent implementation and hostile review. Their agreement is not independent mathematical validation.

## 6. Remaining uncertainty and next bounded step

The midpoint margin gives the desired development ordering but does not supply the missing exclusion. The controls cannot tell whether that ordering transfers to a genuine tied success/failure because all their tied pairs contain. The finite result therefore narrows the proof obligation: control variation over the whole component, not one representative phase.

The next bounded step should freeze the natural **Lipschitz-corrected midpoint lower bound** on the same tied pairs:

`M_Lip(v,I)=||v t_I||-1/8-v|I|/2`.

Distance to the nearest integer is 1-Lipschitz, so `M_Lip>=0` is a valid whole-component complement-safety certificate without constructing the complement threshold schedule. Test this exact sufficient condition unchanged on the squares development tie, Fibonacci controls and `strict_16`; preserve every negative or inconclusive score. Do not add speeds, windows, references, fallback queries, broad search, alternate-window work or `+7/+9`.
