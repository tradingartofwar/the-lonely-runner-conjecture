# Adversarial review: one-containment selector

September 28, 2026 UTC. I reviewed the frozen protocol, the pinned joint-moment and cover-obligation archives, the preceding shared-containment note and archive, and the earlier sparse-selection result. This is an internal AI review, not independent mathematical validation.

## Verdict

I found no fatal algebraic or endpoint defect in the frozen experiment. The two rules answer a narrow, reproducible selection question provided the final note makes the information and cost distinctions below explicit. The largest-slack rule must remain a preserved target failure. The component-count rule's target success is a finite development-case observation, not evidence of a generally reliable or cheaper selector.

## Exact hostile checks

For blockers `a,b,c,d`, inclusion-exclusion gives

`U = C_0 - T_abc - T_abd - T_acd - T_bcd + Q`.

Since `T_acd+T_bcd-Q <= O_cd`,

`U >= C_0-O_cd-T_abc-T_abd`.

Thus `C_0-O_cd>0` is exactly the potential five-edge slack for base pair `{a,b}`, and the compound containment `B_a intersect B_b subset Safe_c intersect Safe_d` sets the two displayed triple durations to zero. Eligibility is sufficient for a positive certificate *if* containment holds; it does not predict containment.

Recomputing every slack and component count from the pinned exact archive gives:

| Case | Eligible pair | Potential slack | Positive base-pair components |
| --- | --- | ---: | ---: |
| target | `{15,38}` | `49/524400` | 1 |
| target | `{61,100}` | `3071/2781600` | 3 |
| strict16 | `{6,11}` | `1/896` | 1 |
| strict16 | `{11,16}` | `1/896` | 1 |
| doubling112 diagnostic | `{56,64}` | `1013/32256` | 2 |
| doubling112 diagnostic | `{56,72}` | `61/2016` | 3 |
| doubling112 diagnostic | `{56,112}` | `1039/32256` | 6 |
| doubling112 diagnostic | `{64,72}` | `769/32256` | 3 |
| doubling112 diagnostic | `{64,112}` | `109/3584` | 5 |
| doubling112 diagnostic | `{72,112}` | `1039/32256` | 4 |

Tight13 has `C_0=0`; its two zero-overlap complementary pairs give slack zero, not strictly positive, and all other slacks are negative. It therefore has no eligible base pair and makes no containment query.

The frozen decisions follow without ambiguity:

- On the target, largest slack selects `{61,100}` and fails. The chronologically first positive violation is speed 38 on `(55/304,29/160)`, with exact midpoint `1101/6080`. Speed 15 separately meets the base pair on `(159/800,97/488)`, of duration `1/48800`. Either rejects containment. No second pair may be queried.
- On the target, fewest components selects `{15,38}` and its already archived containment in `Safe_61 intersect Safe_100` holds, yielding `49/524400`.
- On strict16, both rules tie on slack and component count and therefore select `{6,11}` by physical-speed lexicographic order. The archived containment holds and yields `1/896`. The unused eligible pair `{11,16}` must not be queried in this experiment.
- Doubling112 exits first with the archived pair-only minimum `761/32256`. As diagnostics only, largest slack selects `{56,112}` after its exact tie with `{72,112}` and fails against speed 72 on `(175/576,39/128)`; fewest components selects `{56,64}` and fails against speed 112 on `(183/512,321/896)`. These queries do not repair, replace, or strengthen the prior pair-only certificate.
- Tight13 retains only the separately archived isolated valid point `t=3/8`; the lack of an eligible pair is not a positive-duration failure of the configuration.

## Required reporting corrections and limits

### 0. Independent-verifier schema must pass before publication

At first review run, `primary.py --check` passed but `verify.py --check` failed because its comparison layer did not recognize the primary archive's `frozen_rule_results` key or its selected-pair/query/bound field names. This was a schema/interface defect rather than a disagreement in the reconstructed mathematics. The verifier owner corrected the aliases, expanded comparison across all 24 pair records, and the final read-only run passes on 142 critical fields with zero mismatches. This correction trace matters: merely creating `verification.json` would not have established agreement.

### 1. Charge all selector geometry, not just the selected table

The component-count rule is not a one-table selector. Before its one containment query it must obtain counts for every eligible candidate: two target pairs, two strict16 pairs, and, for the labelled doubling diagnostic, all six pairs. The final ledger should charge those ten pair-component counts (with any schedule caching described) separately from the selected compound queries. A query budget is not a runtime or total-information bound.

There is no prohibited complement-outcome leak in the frozen definition: a count uses only the two runners named as that candidate base pair and does not inspect their joint alignment with either complementary runner. However, on the target the two eligible candidates are complementary pairs. The selection therefore reads occurrence complexity from *both sides*, `{15,38}` and `{61,100}`. It would be misleading to describe the rule as using only the eventual selected base geometry or only pair moments.

### 2. Preserve the failed capacity rule without reranking

The largest-slack score maximizes the lower bound conditional on a containment that has not yet been checked. It need not maximize the chance that containment is true, and the target demonstrates exactly that distinction: the larger conditional bound chooses the physically false containment. Do not report the successful second rule as a post-failure repair by a two-stage policy; they are two separately frozen rules, each with one logical query.

### 3. Endpoint semantics are sound but must stay explicit

`B_v={t in J: ||vt||<1/8}` is relatively open in the nondegenerate closed window `J`, while `Safe_v` includes equality. Hence any point violating the compound containment lies in a relatively open triple-blocking intersection and supplies positive duration, even when the point is a window endpoint. Conversely containment makes both relevant inclusive-triple durations zero. Threshold equality is safe and must not be recorded as a violation. The result should retain interval openness and endpoint membership rather than infer containment from duration-only interval endpoints.

### 4. Empty-base semantics are valid but untested

An eligible base pair with zero positive components would win the fewest-components rule. Its containment is vacuous and the five-edge bound is still legitimate. None of the eligible pairs in this batch is empty, so that branch is specified but not exercised. It should not be counted as a tested behavior. Similarly, strict blocking prevents a nonempty isolated interior component; the explicit "positive-length" qualifier mainly avoids confusing duration with endpoint-only safe contacts.

### 5. This is not held-out selector validation

The rule was frozen before the present calculation, which prevents within-run retuning. But the target, the successful pair `{15,38}`, and its one-component occurrence table were already visible in the preceding archive when this question was queued. The controls are also familiar design cases. Therefore the component-count success is not held-out predictive evidence and must not be called a validated selector, success rate, or general selection theorem.

### 6. Keep scope and prior-work boundaries narrow

All conclusions concern four supplied selected-reference windows, one of which exits before selection and one of which has no eligible pair. A reflected target is the same symmetry check, not a second configuration. Nothing here establishes loneliness for every reference runner or adds whole-configuration coverage.

The five-edge inequality, the strict16 triple exclusion, the fixed-family sparse two-test selector, and its alternate-window dispatch are already present in the repository. The bounded increment is the exact comparison of two newly frozen ranking rules on this archived target and controls. Component counting has a larger and differently structured information contract than the earlier moment-only slack rule; this experiment does not prove it cheaper than the known sparse arithmetic tests or scalable when speeds and component counts grow.

## Interpretation after corrections

The defensible finite conclusion is a clean distinction. Maximizing hypothetical certificate capacity fails on the target, while minimizing eligible base-pair occurrence complexity selects the already known shared containment there and the old strict16 containment. The same component rule is unnecessary and diagnostically false on doubling112, and it has no duration branch on tight13. This supports the next question of whether occurrence counts can be bounded or ordered arithmetically without enumerating all candidate components; it does not yet supply such a formula or a general geometric exclusion.
