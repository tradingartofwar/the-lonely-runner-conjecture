# Counting pair components as lap-band lattice points

September 28, 2026 UTC. Baseline `bf5795ed41c06fc45be02f7b7c3a2c273de27749`, draft PR #3. Material AI involvement: one coordinating agent, one exact-calculation agent, one separately structured verification agent, and one adversarial-review agent. This is internal AI work, not independent human mathematical validation.

**Question.** Can the fewest-components selector obtain the number of positive components of `B_a intersect B_b` directly from speeds and the window, without constructing the two blocking-interval lists or their intersection intervals?

**Outcome.** Yes, as an exact integer-lattice count. On all 24 physical pairs in the four frozen windows, the formula count equals the archived interval-derived component count. It reproduces every prior selector decision:

| Case | Formula counts relevant to selection | Formula choice | Prior outcome |
| --- | --- | --- | --- |
| target | `{15,38}:1`, `{61,100}:3` | `{15,38}` | containment holds; `49/524400` |
| strict16 | `{6,11}:1`, `{11,16}:1` | `{6,11}` by physical lex tie | containment holds; `1/896` |
| doubling112 | `2,3,6,3,5,4` for its six pairs | diagnostic `{56,64}` | containment fails; pair-only exit remains positive |
| tight13 | no positive-slack pair | none | isolated equality `t=3/8` only |

No new complement-containment query was issued. This recovers the previous rule in a different representation; it is not new evidence that the rule predicts unseen cases.

**Status.** The 24 exact matches are OBSERVED. The general lap-band identity below is an AI-assisted elementary proof candidate under its stated domain. No novelty check was performed, and no novelty is claimed.

## 1. Frozen contract

The [protocol](../reviews/2026-09-28-lap-band-component-count/protocol.json), SHA256 `9053ebb58fa30a1841e03bb1aba686fb51631b01480186772f751df63bda1165`, was saved before calculation. It fixes:

- positive integer speeds `a<b`, one rational window `J=[L,R]`, and threshold `delta=1/8`;
- strict blocking `B_v={t in J: ||vt||<delta}`;
- the same four windows, positive-slack eligibility, minimum-count rule, and physical-speed lexicographic ties as the prior study;
- an arithmetic lap-band counter that receives only speeds, windows, and moments before selection;
- an access/dependency barrier: the pinned joint archive is parsed and irreversibly projected to speeds, window, and moments before calculation; component fields, selector choices, containment outcomes, and control roles are not accessed or used until postselection;
- no new containment query, pair fallback, speed, window, reference, alternate-window campaign, or `+7/+9` work.

The primary implementation is forbidden to construct blocking-interval lists or pair-intersection intervals. The independent verifier deliberately does reconstruct exact threshold cells and components.

## 2. Candidate lemma and derivation

For speed `v>0` and lap label `q in Z`, write

`I_(v,q)=J intersect ((q-delta)/v,(q+delta)/v)`.

This clipped occurrence has positive length exactly when

`vL-delta < q < vR+delta`.

For laps `m` of speed `a` and `n` of speed `b`, the two uncut open intervals overlap with positive length exactly when

`|b*m-a*n| < delta*(a+b)`.

The two lap-window inequalities say that each open lap interval meets `J` positively. The band inequality says that the two lap intervals meet each other positively. Three intervals on the real line have a positive common intersection whenever all three pairwise intersections have positive length: their greatest lower endpoint and least upper endpoint come from a pair that overlaps strictly. Thus these three strict inequalities are equivalent to a positive occurrence of `B_a intersect B_b` inside `J`.

Because `delta<1/2`, a strictly blocked time has a unique nearest integer lap label for each speed. Distinct `(m,n)` labels cannot overlap or join through a threshold point, and each surviving labelled intersection is itself an interval. Therefore positive lap pairs and positive connected components are in bijection. A common divisor may repeat determinant patterns at translated times, but the translated lap labels remain distinct components. Equal speeds are outside the frozen `a<b` domain.

For each participating `m`, define

`lower=max(bL-delta,(b*m-delta*(a+b))/a)`,

`upper=min(bR+delta,(b*m+delta*(a+b))/a)`.

The compatible integer `n` labels satisfy `lower<n<upper`, so their number is

`max(0,ceil(upper)-floor(lower)-1)`.

Summing this over the candidate `m` labels of the smaller speed gives the exact pair-component count.

All bounds remain strict. Band equality represents threshold contact and contributes no positive duration. A lap ending exactly at the left window endpoint contributes nothing, while a lap beginning there may contribute immediately to the right; the strict participation inequalities handle both cases.

The adversarial zero-length control `a=3,b=5,m=1,n=2` has

`|5*1-3*2|=1=delta*(3+5)`.

The open laps touch only at `t=3/8`, where both distances equal `1/8`; the strict band correctly rejects it.

## 3. Exact finite results

In physical-speed lexicographic pair order, the formula gives:

| Window | Six pair counts |
| --- | --- |
| target `{15,38,61,100}` | `1,1,1,2,2,3` |
| strict16 `{6,7,11,16}` | `0,1,1,1,0,1` |
| doubling112 `{56,64,72,112}` | `2,3,6,3,5,4` |
| tight13 `{6,7,11,13}` | `0,1,1,1,1,0` |

Every value matches the pinned interval archive. Representative certificates include:

- target `{15,38}`: only `(m,n)=(3,8)`;
- target `{61,100}`: `(11,18),(12,20),(13,21)`;
- strict `{11,16}`: candidate `m=3` contributes none and `m=4` contributes `n=6`;
- doubling `{56,112}`: `(m,2m)` for `m=16,...,21`;
- tight `{11,13}`: two candidate `m` rows, neither containing an integer `n`.

The positive-slack eligibility rule remains essential. Ineligible zero-count pairs in strict16 and tight13 cannot bypass it.

## 4. Cost and information distinctions

Across all 24 validation pairs, the formula processes 63 candidate rows and counts 41 compatible integer lap pairs. The active selector needs four positive-slack pairs—two target and two strict16—using seven rows and four compatible lap pairs. Doubling112 adds six explicitly diagnostic pairs, 39 rows, and 23 lap pairs after its pair-only-positive exit. The remaining fourteen pairs are ineligible audit comparisons.

Equivalently, the ten positive-slack pairs across active and diagnostic cases require 46 rows and contain the same 29 positive components reported previously. The primary materializes the integer `n` labels as review certificates, although the numerical formula needs only their count.

This is arithmetic overlap geometry, not absence of geometry. The row count is on the order of `a*(R-L)+O(1)` for the chosen smaller speed `a`; it can grow with speeds and window length. A cached interval implementation may also reuse one runner's occurrence list across several pairs, while this pairwise formula may rescan its `m` labels. The experiment therefore establishes exact representation recovery and reduced object construction, not constant time, uniform cheapness, lower runtime, or asymptotic improvement.

The sparse triple-exclusion work already uses arithmetic lap compatibility, and the earlier lap-labelled note already treats clipped occurrences as the relevant objects. This result is an elementary algebraic restatement and cost refinement of that existing representation, not a new selection mechanism.

## 5. Controls and interpretation

- **Target:** the arithmetic count reproduces the already known development-case ordering `1<3`. It is not held-out validation of the heuristic.
- **Strict16:** both eligible pairs count one, so the frozen physical-speed lexicographic tie selects `{6,11}`. The old triple exclusion and `1/896` repair remain prior work.
- **Doubling112:** all six counts are diagnostics. Its pair-only minimum `761/32256>0` exits before selector use; the diagnostic `{56,64}` containment still fails.
- **Tight13:** no pair has strictly positive slack, so no decision or containment query occurs. The valid point `3/8` is isolated and has zero positive duration.

These are selected-reference window statements, not every-reference or whole-configuration conclusions. Abstract cover models and runner-realizable geometry remain distinct.

## 6. Verification and delegation

Artifacts are under [reviews/2026-09-28-lap-band-component-count/](../reviews/2026-09-28-lap-band-component-count/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-lap-band-component-count/primary.py --check
python -S -B reviews/2026-09-28-lap-band-component-count/verify.py --check
```

The independent verifier imports no primary code and does not use the per-lap band-row formula. It reconstructs all 24 exact pair-intersection lists from 311 threshold events and 287 open cells, matches every count and frozen decision, and compares 28 critical primary fields. All 25 repository tests also pass.

Three complementary AI agents performed the primary calculation, separate event reconstruction, and hostile proof/cost review. Agreement among them is useful error control, not independent mathematical validation.

## 7. Next bounded question

The formula eliminates interval-object construction but not the speed-dependent row loop. Freeze a new investigation on these same 24 pairs: replace the per-`m` scan by an exact Euclidean/floor-sum lattice counter, prove that it preserves the strict open boundaries, and compare its arithmetic-operation count with both the current row formula and cached interval enumeration. Preserve a slower or more complicated outcome. Add no speeds, windows, references, complement queries, broad scans, or `+7/+9` work.
