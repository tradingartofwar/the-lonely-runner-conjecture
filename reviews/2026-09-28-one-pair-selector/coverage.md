# One-pair selection: archived comparisons and what the failure means

September 28, 2026. Baseline `539dd899ac8ceea5b50d46b72c0fa28cec7a354e`; [protocol](protocol.json) SHA256 `36ef24405de801a114e11325d30fe0b5f2d855e71441e5c4478047aa15b82d8e`. Eight common-start runners, reference 0, threshold 1/8, and only the six prescribed core/residual inputs. Material AI involvement includes archive extraction, comparison, and writing. General implications remain **HYPOTHESIS / proof candidates**; exact archived finite facts retain their stated **OBSERVED / REPRODUCED** scope. No novelty or new Lonely Runner coverage is claimed.

**The final strict-16 control separates a failed ranking from an insufficient certificate form. On its selected window every single-pair bound fails, and even the best ordinary tree bound is negative. A stronger compatibility graph already in the record certifies its positive interval.** The campaign's stop therefore does not justify reranking the same six pairs until one succeeds.

## 1. Provenance and separation from selection

[benchmarks.json](benchmarks.json) contains only comparisons extracted from pre-existing archives. Each source has its exact byte SHA256, archive date and baseline, and each value has a zero-based JSON Pointer. The sources are:

| Source key | Archive | Fields used |
| --- | --- | --- |
| `pairs` | [experiments/pair_selection.json](../../experiments/pair_selection.json) | Complete local allowed sets, all pair overlaps, best-pair and best-tree records for four frozen inputs |
| `placement` | [experiments/overlap_placement.json](../../experiments/overlap_placement.json) | Independent archived 56/112 selected-pair bound and local duration |
| `cycles` | [four_blocker_cycles.json](../2026-09-25-lr2/four_blocker_cycles.json) | Local moments, best tree, compatibility graph, clear cells and valid boundaries for doubled-112 and strict-16 |
| `sparse` | [sparse_overlap.json](../2026-09-25-lr2/sparse_overlap.json) | Separate strict-16 record confirming actual duration, tree bound, compatibility certificate and two absent triples |
| `ultra_root` | [root_checks.json](../2026-09-25-ultra/root_checks.json) | Physical and abstract zero-uncovered state tables with matching all-single/all-pair moments for strict-16 |

No benchmark value was supplied to the primary selector or used to choose a window, pair, or endpoint. The independent campaign selected the expected windows before the coordinator confirmed the match: `[9/32,3/8]` for core `{1,4,5}`, `[17/40,23/40]` for `{1,3,5}`, and `[9/32,7/16]` for `{1,2,4}`. Matching their archived counterparts afterward is a comparison step.

Extraction copied existing fields, took maxima of archived pair weights where necessary, and formed `best overlap−E` from archived singles and window length. Right-endpoint facts come from membership in the archived complete local allowed sets, with the cycle archive's valid-boundary list as a crosscheck. No new seven-runner safe set, pair moment, tree optimization, or speed scan was constructed.

## 2. Exact archived comparisons on the selected windows

Write E for summed single-blocking duration minus window length. The best-pair column is `max O_ij−E`, not the policy's selected-pair result.

| Frozen case | Actual local duration U | Best-pair bound | Best ordinary tree | Right endpoint in old allowed set |
| --- | ---: | ---: | ---: | --- |
| `fast_113` | 6193/260352 | 1495/303744 | 58073/3644928 | Invalid |
| `changed_core` | 1923/50624 | 2169/202496 | 49663/1822464 | Invalid |
| `doubling_112` | 53/1792 | 97/8064 | 761/32256 | Invalid |
| `tight_13` | 0 | −131/13728 | −1/528 | Isolated 3/8 |
| `one_pair_ceiling` | 11/480 | −1/120 | 11/480 | End of `[17/40,7/16]` |
| `strict_16` | 1/896 | −169/14784 | −23/29568 | Invalid |

The largest archived overlap and its achieving pair(s) are:

| Case | Pair(s) | Largest overlap |
| --- | --- | ---: |
| `fast_113` | 72,113 | 395/65088 |
| `changed_core` | 56,72 | 23/2016 |
| `doubling_112` | 56,112 | 11/896 |
| `tight_13` | 7,13 | 1/182 |
| `one_pair_ceiling` | 3,6 | 1/24 |
| `strict_16` | 6,16 and 11,16 | 1/128 |

The four `pairs` archive locations are respectively `/cases/0/components/1`, `/cases/2/components/3`, `/cases/1/components/1`, and `/cases/9/components/1`. Doubled-112 and strict-16 use `cycles` locations `/cases/0` and `/cases/7`; their additional checks use `placement:/cases/0` and `sparse:/finite_results/9`. The JSON records field-level pointers and exact derivations.

All six [primary output](results.json) windows now match these baseline benchmarks. The completed policy produces three positive one-pair bounds, one isolated endpoint contact, one positive endpoint interval, then the strict-16 uncertified stop. It makes five overlap queries and three endpoint tests; the ceiling case's skipped overlap remains unqueried. Those are policy outcomes on known controls, not a success-rate estimate or new existence coverage.

## 3. Distinctions the ordered outcomes must retain

The first three controls possess positive one-pair certificates on the frozen windows. Their best pairs need not coincide with the cap-ranked pair. A smaller positive selected bound still certifies the required outcome; failing to maximize the bound is not failure of the selector's stated existence target.

The changed-core example preserves an older limitation: 56/113 has zero overlap on this central window, despite `113−2·56=1`. Pair 56/72 works there. The new concentration ranking must be evaluated as frozen; a residual-phase eligibility filter added after observing an answer would be a different selector.

For `tight_13`, every valid local time is the singleton 3/8. Negative pair/tree bounds are compatible with that equality witness. Its archived contact directions are blocking ending for speed 11 and beginning for speeds 5 and 13. The endpoint route supplies joint point information that duration summaries cannot recover.

For `one_pair_ceiling`, the marginal cap test can reject the entire one-pair certificate class without an overlap query. The old best-pair bound is indeed negative, while the old tree is exact and positive. The frozen right endpoint instead belongs to the positive interval `[17/40,7/16]`. Success through its safe-lap intersection is a distinct endpoint certificate, not a repaired pair inequality. The interval has length 1/80; the full local duration is the larger 11/480.

For `strict_16`, the full local allowed interval was already recorded as `[17/56,39/128]`, of length 1/896. Every single-pair bound is nonpositive, so the selected pair's failure cannot be repaired by choosing another pair on this window. The right endpoint 3/8 is invalid, and the best ordinary tree also fails.

The old sparse certificate uses edges `(6,11),(6,16),(7,11),(11,16)` and the absence of triples `{6,11,16}` and `{7,11,16}`; it reaches 1/896. This is a previously available stronger certificate, not a second query or fallback executed by the new policy.

There is also an older, stronger information obstruction. The [September 25 Ultra review](../../notes/ULTRA_REVIEW_2026_09_25.md), §1, and `ultra_root:/tree_limitation` retain an abstract complete-cover event arrangement with the same four single durations, all six pair totals, and total window length. Its uncovered mass is zero. Thus these totals alone cannot force positive uncovered measure through a universally valid event inequality. The alternative is not claimed to be another physical runner configuration. The new campaign neither constructs this countermodel nor solves a new moment optimization; it uses the already-recorded distinction between physical geometry and its moment summary.

Thus the final failure concerns a positive opening already inside the selected window. It is not evidence that another window was necessary, that the input is non-lonely, or that the old all-phase adaptive-pair result failed. The frozen one-pair campaign must retain this uncertified result and stop.

## 4. What selection and cost work was already complete

[CORE_TRANSFER.md](../../notes/CORE_TRANSFER.md), §§6–8, already evaluates all six pair overlaps and all sixteen trees on 72 complete core components. Its best pair certifies 32 of 38 positive components; its best tree certifies all 38 in that bounded collection. It also preserves 18 isolated-only components. Repeating exhaustive local ranking is not a new selection result.

[SPARSE_OVERLAP_SELECTION.md](../../notes/SPARSE_OVERLAP_SELECTION.md), §§1–5, already gives a compact one-variable graph selector: five endpoint-primitive interval evaluations, two integer-existence tests for triples, and at most 32 masks. The operation count does not grow with that variable speed, while integer bit costs do. Its family argument uses 292 finite cases and an analytic tail from 299.

[TWO_SPEED_SPARSE_TRANSFER.md](../../notes/TWO_SPEED_SPARSE_TRANSFER.md), §§2–6, already supplies a speed-dependent two-window dispatch. The fast branch and x=3 use the alternate H; otherwise x<=33 bounds the occurrence counts in J, and y's laps are never enumerated. The synthesis retains 27 tail profiles and 819 reduced finite pairs. Its success rests on the fixed blockers' disjointness and known safe alternate window. The later four-blocker correction study does not inherit this bounded occurrence count: its intersection moments use speed-dependent lists.

The present distinction is the **frozen one-pair query budget after marginal ranking**, with a specified core-window rule and one endpoint fallback. One query is not automatically cheap. Core construction, residual-strip construction, every primitive call, and rational operand sizes remain real costs. The signed-residual evaluator can avoid listing fast laps, but its strip count depends on residual drift across the window; the [arithmetic review](arithmetic.md) states that dependence. No uniform or empirical speedup follows from query count alone.

## 5. What to do with the failure

Do not tune another pair-ranking score to strict-16: the archived best-pair ceiling already rules that out on this window. First report the certificate hierarchy exposed by the frozen test: some inputs permit one-pair positivity; an endpoint can recover either equality or a positive interval; one-pair and ordinary-tree information can still miss a positive opening that an existing compatibility certificate detects.

A useful bounded next question is theoretical: **given a declared local information set, can a rule choose a geometric exclusion or quantitative intersection bound that rules out every compatible complete-cover arrangement?** Eliminating just one displayed countermodel is insufficient. The input contract must distinguish supplied data from requested queries. If it supplies all six pair totals, their acquisition cost is charged and the study no longer has the present one-query budget; if it keeps only one pair, it must respect the larger class of compatible event arrangements.

Use only already archived diagnostic requirements: strict-16 has a valid exclusion, doubled-112 has actual positive triples and four-way overlap so those events cannot be declared absent, and tight-13 requires an equality route. The old sparse rule and known strict-16 repair are comparison targets, not the new result. The deliverable should be a sufficient selection condition with explicit discovery cost, or a proof that the declared inputs cannot justify the decision. Merely attaching the known triple test after this known failure, or fitting another ranking to the six cases, would not supply that condition. No new numerical campaign is required to formulate or challenge it. If no statement beyond the existing fixed-family mechanism survives, record that limitation rather than extend the special case indefinitely.

This remains the separate [small-gcd selection priority](../../notes/SMALL_GCD_DISTINCTION_REVIEW_2026_09_27.md): the original 56/113 bound was already repaired by exact concentration plus overlap placement, and restricted small-gcd family arguments already exist. The remaining issue is useful selection under stated speed assumptions and explicit evaluation cost. No general existence theorem, arbitrary core selector, further cutoff polishing, or +7/+9 work follows from this bounded campaign.
