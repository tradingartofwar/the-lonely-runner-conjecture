# A runner window realizes the collective-only obstruction

September 28, 2026 UTC. Baseline `60f1665e92b54c3117fd73f5b83542c424dc9f21`, draft PR #3. Material AI involvement: a coordinating agent and three complementary agents supplied the primary calculation, a separately structured exact verifier, and adversarial review. This is internal AI work, not independent human mathematical validation.

**Question.** Among the eighteen already archived positive-duration windows missed by tree certificates, is there a common-start runner window whose total, single and pair durations admit an abstract complete cover, although no one inclusive triple is compulsory in every compatible cover?

**Outcome.** Yes. Two archived records are reflections of one mechanism. For

`{0,7,8,15,23,38,61,100}`,

with reference `0`, threshold `1/8`, core `{7,8,23}`, and residual blockers `{15,38,61,100}`, the windows

`[33/184,39/184]` and `[145/184,151/184]`

each have actual lonely duration `1/600`. Their pair-only minimum uncovered duration is nevertheless zero, and each of the four inclusive triples has a separately attained zero minimum on the compatible cover face.

The four minimizing covers need not be the same. The result supplies a physical runner window with the requested summaries and positive opening; it does **not** assert that any of the alternative complete-cover mass tables is itself realizable by another runner configuration.

**Status.** OBSERVED/REPRODUCED in the frozen finite scope. This is not new existence coverage, an all-reference result, a general selector, a novelty claim, or an independent proof certification.

## 1. Frozen domain and charged reconstruction

The [protocol](../reviews/2026-09-28-collective-window-audit/protocol.json), SHA256 `0e418826e58e36b106eb82da9f19754795fb64c76b623e9974635d9984974052`, was saved before calculation. It adds no speed, core, window, or subdivision to the September 27 six-case archive.

The old archive stores per-core counts and component digests rather than an explicit list of its eighteen missed rows. The frozen locator therefore uses the five archived miss-bearing cores only, reconstructs their 209 complete components, matches all five historical digests, and then applies the old predicate: actual duration positive and reduced optimal-tree bound nonpositive. The located counts are:

| Configuration | Core labels | Components checked | Misses retained |
| --- | --- | ---: | ---: |
| Fibonacci | 1,2,4 | 34 | 8 |
| Squares | 1,2,5 | 52 | 2 |
| Squares | 1,3,4 | 46 | 2 |
| Prime powers | 2,3,4 | 53 | 2 |
| Perturbed chain | 1,2,4 | 24 | 4 |
| **Total** | five archived cores | **209** | **18** |

This reconstruction is charged explicitly. The other 205 source cores and their windows were not recalculated. All eighteen retained records form nine reflection pairs; they are not eighteen independent configurations.

## 2. Frozen information test

On each selected closed window, the four residual strict blocking events give sixteen nonnegative exact-state masses. Retained inputs are the window length `L`, four singles `D_i`, and six pairs `O_ij`. The uncovered mass is `U=x_empty`. For a triple `K`, `T_K` is inclusive: its exact-three atom plus the four-way atom.

The rule was fixed as follows:

1. minimize `U` from total, single and pair moments;
2. only when that optimum is zero, impose `U=0` and separately minimize all four `T_K`;
3. call the physical window a collective-only counterpart exactly when its actual `U` is positive, the pair-only optimum is zero, and all four cover-constrained triple minima are zero.

No combined statistic, retuned window, or post-result geometry query enters selection. Actual higher moments are retained only as diagnostics.

The eighteen labelled windows split exactly as follows:

| Pair/triple classification | Labelled windows |
| --- | ---: |
| Pair-only minimum positive | 8 |
| Pair-only minimum zero; at least one individual triple forced positive | 8 |
| Pair-only minimum zero; all four individual triple minima zero | 2 |

The last two records are one reflection class.

## 3. Exact counterpart

On the first representative window `J=[33/184,39/184]`, the complete physical safe set has two positive components:

`[3/16,151/800]` and `[153/800,23/120]`.

Their lengths sum to `1/600`. The reflected window has the reflected components. Threshold endpoints remain valid and were checked separately from open-cell duration.

For both records:

| Quantity | Exact value |
| --- | ---: |
| Window length | `3/92` |
| Actual uncovered duration `U` | `1/600` |
| Best tree bound | `-107161/31988400` |
| Pair-only minimum `U` | `0` |
| Four cover-constrained triple minima | `0,0,0,0` |
| Pair inclusion-exclusion constant `C` | `6121/2781600` |
| Actual four-way duration `Q` | `0` |
| Actual corrected burden `H=sum T-Q` | `99/185440` |

The actual inclusive triple durations, ordered as `{15,38,61}`, `{15,38,100}`, `{15,61,100}`, `{38,61,100}`, are

`0, 0, 1/48800, 119/231800`.

The identity `U+H=C` checks exactly. On an abstract compatible cover `U=0`, so every cover has collective burden `H=C>0`; nevertheless, four exact nonnegative cover certificates show that each named triple can separately have duration zero.

This is the same quantifier distinction as the earlier abstract symmetric model, now attached to an actual positive-duration common-start runner window. The alternative cover certificates are abstract measurable state distributions, not runner realizations.

## 4. Consequence for one-triple escalation

These windows disprove completeness of a rule that escalates only when one individual triple is compulsory. More strongly, no physically valid **upper bound on one inclusive triple alone** can eliminate every abstract cover compatible with the pair moments: for whichever triple is chosen, an archived compatible cover attains `T_K=0`, and therefore satisfies every valid nonnegative upper bound.

This statement is deliberately narrow. It does not exclude an exact measured equality, a lower bound, two or more simultaneous restrictions, a different higher-order statistic, pointwise placement information, a core exchange, or another window. The sparse triple-exclusion repair and alternate-window certificates were already known in this repository; this audit neither rediscovers nor replaces them.

## 5. Exact verification

Artifacts are under [reviews/2026-09-28-collective-window-audit/](../reviews/2026-09-28-collective-window-audit/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-collective-window-audit/primary.py --check
python -S -B reviews/2026-09-28-collective-window-audit/verify.py --check
```

The primary archive contains 58 exact rational primal/dual certificates: eighteen pair baselines and forty triple minima on the ten zero-baseline windows. The independent verifier imports no primary function and uses exact threshold-event geometry, Kruskal trees, and its own rational two-phase simplex. It matches all five source digests, 262 selected-window cells, all moments and atoms, and all 58 optima. It also independently solves eleven LPs for the three prior controls and checks the archived strict16 repair certificate.

The controls retain their distinct roles: strict16 forces one triple by `1/896`; doubling112 already has positive pair-only minimum `761/32256`; tight13 has zero pair/triple minima but only the valid isolated equality at `3/8`. They are calibration cases, not part of the eighteen-window count.

The [adversarial review](../reviews/2026-09-28-collective-window-audit/challenge.md) found no fatal defect within scope. It emphasizes reflection dependence, endpoint handling, quantifier order, abstract-versus-runner realizability, and the fact that diagnostic `H` was not added as a selection query.

## 6. Next bounded question

Freeze one representative window, its four physical triple upper bounds, and the existing pair moments. Before calculation, order all proper subsets of simultaneous triple upper bounds and test which, if any, force `U>0`. Preserve every compatible cover countermodel. This asks for the smallest joint geometric exclusion in the actual counterpart without adding speeds or windows.

If no proper subset succeeds, record that all four coordinate upper bounds are necessary within this contract and compare them with one directly bounded collective quantity. Do not infer a cheap general selector, broaden references, restart `+7/+9`, or repeat the already-known sparse/alternate-window repairs.
