# A Lipschitz correction turns the midpoint feature into a sufficient component certificate

September 28, 2026 UTC. Baseline `ad7f51f6d367449d517695aa668f3b71ae63cb7f`, draft PR #3. Material AI involvement: one coordinating agent, one exact-calculation agent, one separately structured verification agent, and one adversarial-review agent. This is internal AI error control, not independent human mathematical validation.

**Question.** On the unchanged minimum-component ties, can the previous midpoint feature be corrected into a valid whole-component complement-safety certificate without constructing the complement threshold schedules?

**Outcome.** Yes, on the frozen finite scope. Subtracting the maximum phase drift `v|I|/2` turns the point sample into a rigorous lower bound over the whole base component. The corrected score is `51/484` for the fitted successful squares pair `{25,121}` and `-1/52` for failed `{25,169}`. The former is certified; the latter is correctly left uncertified. All selected Fibonacci controls and `strict_16` are also certified. Across all sixteen tied pair-label instances, all fourteen containing pairs have nonnegative score and both failed reflected labels have negative score.

This removes the two false positives of the uncorrected midpoint sign in this archive. It does **not** establish a general selector: the only success/failure tie is fitted development data, all archival tied controls contain, reflections are dependent, and every tied pair in scope has one component.

**Status.** The elementary Lipschitz implication is proved below. Scores, choices, archive comparisons and cost counts are **OBSERVED** on the frozen finite scope. No prospective validation, necessary condition, runtime improvement, whole-configuration conclusion, new existence coverage or novelty claim is made.

## 1. Frozen contract

The [protocol](../reviews/2026-09-28-lipschitz-component-margin/protocol.json), SHA256 `3903410dec2f61deda37c9fe7d03fb6ae24034fc80c78f8426faa9e81f4cae0c`, was frozen before control calculation. It retains exactly:

- reflected `squares:1,2,5:12/:39` as development data;
- the four tied Fibonacci labels and `strict_16` as archival controls;
- `doubling_112` and `tight_13` as dispatch controls;
- the same physical speeds, windows, eligible pairs and minimum-component ties;
- no fallback query, endpoint rescue, alternate window, new domain, broad scan or `+7/+9` work.

Before scoring, the primary projects the pinned archives to ids, speeds, windows, dispatch values, eligible pairs, potential slacks and component counts. It reconstructs only base-pair components and samples complement phases only at their prescribed midpoints. Containment answers, violations, actual duration and mechanism labels are reloaded only after scores, choices and certificate decisions are immutable.

## 2. Whole-component lemma

Let `I=(l,r)` be a positive component of `B_a intersect B_b`, and let

`t_I=(l+r)/2`.

For a complementary speed `v>0`, define

`L(v,I)=||v t_I||-1/8-v(r-l)/2`,

where `||x||=distance(x,Z)`. The distance to a closed set is globally 1-Lipschitz, so for all real `x,y`,

`| ||x||-||y|| | <= |x-y|`.

This remains true across the cusps of nearest-integer distance. Composing with `t -> vt` gives

`||v t|| >= ||v t_I||-v|t-t_I|`.

Every `t` in the closure of `I` satisfies `|t-t_I| <= (r-l)/2`. Therefore

`||v t||-1/8 >= L(v,I)`.

If `L(v,I)>=0`, speed `v` is nonblocking throughout the closed component. Equality is safe because blocking is strict (`distance<1/8`). Taking the minimum over both complement speeds and every positive base component therefore gives a sufficient certificate for

`B_a intersect B_b subset Safe_c intersect Safe_d`.

A negative bound is only inconclusive: the actual component may still be safe.

## 3. Frozen rule and outcomes

For each pair tied at the minimum component count, compute the minimum corrected margin over both complement speeds and all components. Maximize this pair score; break an exact score tie by physical lexicographic order. Issue a certificate only if the selected score is nonnegative.

| Representative | Corrected scores | Selected pair | Result |
| --- | --- | --- | --- |
| squares development `:12` | `{25,121}: 51/484`; `{25,169}: -1/52` | `{25,121}` | certified; failed tie refused |
| Fibonacci `:1` | `{21,55}: 3/28`; `{21,89}: 103/712` | `{21,89}` | certified |
| Fibonacci `:11` | `{21,55}: 1/84`; `{21,89}: 95/712`; `{21,144}: 151/1152` | `{21,89}` | certified |
| `strict_16` | `{6,11}: 5/24`; `{11,16}: 5/64` | `{6,11}` | certified |

The reflected labels have identical scores and are not independent examples. The selected Fibonacci lower bounds remain `3001/1879680` on `:1/:32` and `15733/9868320` on `:11/:22`. The selected squares bound remains `1/2028`; `strict_16` remains `1/896`. These are inherited five-edge consequences once containment is certified, not new inequalities.

The decisive development correction is exact. Failed `{25,169}` has component width `1/676`. Complement speed 49 had positive uncorrected midpoint margin `23/1352`, but its half-width drift allowance is `49/1352`, leaving

`23/1352-49/1352=-1/52`.

For successful `{25,121}`, the component width is `1/3267`. Its limiting complement speed 49 has midpoint margin `1475/13068` and drift allowance `49/6534`, leaving `51/484>0`.

The postselection classification is:

| Corrected-sign class | Pair-label instances | Reflection mechanisms |
| --- | ---: | ---: |
| Nonnegative and containing | 14 | 8 |
| Negative and noncontaining | 2 | 1 |
| Nonnegative and noncontaining | 0 | 0 |
| Negative and containing | 0 | 0 |

The zero false-positive count is required by the proved sufficient implication, not evidence that nonnegative score is necessary. The zero negative-containing count is a bounded observation only.

## 4. Dispatch and cost

- `doubling_112` exits before scoring on its prior pair-only bound `761/32256`.
- `tight_13` has no eligible duration pair and retains the isolated valid equality `t=3/8` separately.
- No selected containment query, fallback pair, endpoint rescue or alternate window is used.

Preselection covers sixteen tied pairs and sixteen components, using 143 lap candidates, 57 base blocking pieces, sixteen widths/midpoints and 32 complement phase, distance, speed-width and corrected-margin evaluations. Nine pair-score comparisons make the seven active choices. This avoids complement threshold schedules, but it still reconstructs the base-pair components and is not cost-free or a uniform runtime result.

The separately charged postselection audit uses sixteen containment queries, 248 unique threshold events including window endpoints, and 232 open cells. None of this audit geometry participates in selection or certification.

## 5. Verification

Artifacts are under [reviews/2026-09-28-lipschitz-component-margin/](../reviews/2026-09-28-lipschitz-component-margin/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-lipschitz-component-margin/primary.py --check
python -S -B reviews/2026-09-28-lipschitz-component-margin/verify.py --check
python -m unittest discover -s tests -v
```

The primary uses exact `fractions.Fraction` arithmetic. The verifier imports no primary code. It reconstructs base components by a separate threshold-event sweep, recomputes all scores and choices, and checks every numeric Lipschitz bound against a direct exact minimum-distance calculation on the closed component. It finds zero defects across 32 evaluations and compares 573 scalar primary fields with zero disagreement. All 25 repository tests pass.

Final SHA256 values before manifest creation:

- `primary.py`: `a93e7b477982d3d916a11f01f34f68cf5b6923b49a2c6e06533be2901784d8b1`
- `results.json`: `4f0da78ff72c83d8c230cde18194cffef9af5af882a167d3d5b17e02f2b4cd59`
- `verify.py`: `ae1f7e39b21361907981a830a3e482a391018c7236fe14f777358d906b1d17c0`
- `verification.json`: `ec809b3ee1cccd40741c0d0ff4c063c37b1f4884df8a2a2c085ff64dc5a99cba`
- `verification.md`: `60b3cdf85011cb1605ec8939d4519f16187c401944d785ff37dc4e141d07fbfa`

## 6. Remaining uncertainty and next bounded step

The corrected rule now supplies a real sufficient exclusion on the frozen ties, rather than a pointwise ranking feature. Its validation limit is the main unresolved distinction: the only mixed success/failure tie was used to formulate the correction, while every archival tied control is an all-success case and every pair has one component.

The adversarial review identified a stronger statement **after** the frozen calculation. If the component has midpoint `m` and radius `h`, then the exact minimum distance of the lifted interval `v*[m-h,m+h]` to the integer lattice is

`max(||v m||-v h,0)`.

This suggests that the **sign** of the corrected margin is not merely sufficient: a negative value should force a strict complement blocker in the component interior, even when the closest closed endpoint is excluded, by continuity. That necessity claim was not part of the frozen candidate, was not used to select or classify outcomes, and is not promoted here. It is a consequential follow-on proof obligation.

The next bounded step should freeze that exact interval-distance/sign-equivalence statement, check its open-endpoint semantics separately, and then apply it unchanged to **all minimum-component selections in the already archived selector-transfer records**, not only ties. This would test whether the midpoint/width calculation exactly replaces the inherited containment query across the ten active labels and would exercise any archived multi-component selections without adding speeds, windows, references or a fallback. Preserve every contradiction or endpoint exception and compare against the pinned postselection oracle only after predictions are immutable.
