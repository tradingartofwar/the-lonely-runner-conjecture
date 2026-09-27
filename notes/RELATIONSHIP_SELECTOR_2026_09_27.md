# Relationship maps simplify certificates, but do not determine openings

September 27, 2026. Baseline `6c66a3d7727b6ff3ce03d46d58faee86ebac52b5`. This performs the experiment proposed in [FIXED_WINDOW_CONTAINMENT_2026_09_27.md](FIXED_WINDOW_CONTAINMENT_2026_09_27.md) and the [broader inquiry](inquiries/2026-09-27-relationships-and-independence.md). Vance proposed learning the runners' relationships and authorized the test. AI materially designed the protocol, calculations, independent implementation, and writing.

**Outcome:** the relationship map gives a lossless reduction of the constraints on each tested window. It also misses information that determines whether an opening exists. Two physical configurations have the same nontrivial map on the same window, yet one window is empty and the other has positive lonely duration. The frozen rule that chooses the fewest remaining constraints fails on every case in this batch. Adding retained single/pair durations gives a successful strict certificate in all four strict cases; a separate endpoint check preserves the tight control.

A useful additional finding is that the x=19,y=45 countercontrol has a containment we had not used: on the selected J, B19 is contained in B45. Replacing the old tree edge 7–19 with 45–19 makes that tree exact. Failure of one proposed containment did not establish absence of every useful containment.

Finite calculations and counterexamples are OBSERVED / independently REPRODUCED in the declared scope. The qualitative rule's universal-success interpretation is DISPROVEN by the finite failures. The general reduction and tree-invariance arguments supplied below remain proof candidates under [CLAIM_STATUS.md](../CLAIM_STATUS.md). No novelty, new Lonely Runner family coverage, general selector theorem, or computational speedup is claimed.

## The question and the frozen protocol

Can a map of guaranteed relationships help select a useful core-safe window, using only declared inputs rather than the actual allowed set?

The [protocol](../reviews/2026-09-27-lr2/relationship_selector_protocol.json) was written and hashed before calculating the new maps and selector outcomes:

`0e2d4a37dcd2c0276ca8d7dd68938d1bfe7bdbf1a32012a19a8ac15e39ae7dfb`.

These are previously studied controls; their known behavior informed the design. This is not a held-out or externally preregistered study. The rules below were not revised after their failures became visible.

Keep eight distinct common-start speeds `{0,1,4,5,6,7,x,y}`, reference 0, threshold 1/8. Use five pairs `(x,y)`: `(11,13)`, `(11,44)`, `(11,45)`, `(11,46)`, and `(19,45)`. Use exactly two cores, `{1,5,6}` and `{1,4,6}`, and every complete closed core-safe component in `[0,1]`. Both cores have eight components, producing 80 calculations. No extra core, tailored subinterval, other reference, or parameter scan was added. Reflections are retained and the 80 calculations are not independent samples.

On a component W, the four residual roles are `(4 or 5, 7, x, y)`. Record:

- Every strict-set containment `B_i intersect W subset B_j intersect W`, written as a directed edge i -> j. Equivalently, j safe implies i safe on W.
- Every vanished blocker, whose strict blocking set on the closed W is empty.
- Equality classes of nonempty blocking sets.
- One smallest-index representative of each inclusion-maximal nonempty class.

All tests include event vertices as well as open cells. The runner count and threshold stay at eight and 1/8 even when constraints are removed from the local calculation.

## The two rules and the equality fallback

**G, qualitative selection:** choose the positive-length component with the fewest retained blockers; break ties by greater window length, lexicographic numerical core tuple, then earlier left endpoint. G uses the map and this geometry, with no duration or actual allowed-set input. Evaluate its certificate only after selection.

**Q, quantitative selection:** for every positive-length component, compute

\[
Q(W)=|W|-\sum_{i\in R}D_i+
\max_T\sum_{(i,j)\in T}O_{ij},
\]

where R is the retained set, `D_i=|B_i intersect W|`, and `O_ij=|B_i intersect B_j intersect W|`. T is a spanning tree on R. With zero retained blockers use `Q=|W|`; with one use `Q=|W|-D_i`. Choose the greatest bound, using G's tie-breakers afterward. The actual uncovered duration and allowed set never enter the selection keys.

The tree expression is a lower bound because, at any time with s>0 active blockers, their induced subgraph has at most s-1 edges. Thus `1-s+(number of active tree edges)<=0`, the true uncovered indicator at that time. When no blocker is active, both expressions equal 1. Integrating proves the bound for each tree; maximizing retains a valid bound.

If the maximum Q is nonpositive, test the sorted distinct endpoints of all complete core components against all seven original constraints. A passing endpoint is a valid witness; no passing endpoint means this procedure is inconclusive. This fallback is not asserted complete for arbitrary configurations. A positive Q supplies a strict witness from the retained constraints, then verifies it directly against all seven original constraints.

This is an explicit bounded selection procedure. It still constructs all candidate components and their maps. It is not a claimed method whose cost is bounded independently of the speeds.

## Results of the frozen rules

G chooses `W0=[3/16,7/32]` from core `{1,4,6}` in every case. Only blocker 5 remains. However,

\[
5W_0=[15/16,35/32]\subset(7/8,9/8),
\]

so runner 5 blocks the entire closed window. The tree bound and actual allowed duration are both zero, and there is no equality point there. A single remaining obstacle can be sufficient to block everything.

Q makes these choices:

| x,y | Q core | Q window | Retained speeds | Q bound | Actual local duration |
| --- | --- | --- | --- | ---: | ---: |
| 11,13 | 1,4,6 | [3/16,7/32] | 5 | 0 | 0 |
| 11,44 | 1,4,6 | [9/32,5/16] | 7 | 1/112 | 1/112 |
| 11,45 | 1,4,6 | [9/32,5/16] | 7,45 | 1/210 | 1/210 |
| 11,46 | 1,4,6 | [9/32,5/16] | 7,46 | 1/184 | 1/184 |
| 19,45 | 1,5,6 | [17/40,23/48] | 7,19,45 | 49/3420 | 1/60 |

The four positive cases give directly checked strict witnesses `69/224`, `257/840`, `57/184`, and `41/90`, respectively. The last selected bound has slack `2/855`; quantitative usefulness does not require exactness.

For `(11,13)`, no Q window has positive bound. The endpoint fallback finds `t=1/8`, outside the selected empty W0. Independent reconstruction gives the full allowed set `{1/8,3/8,5/8,7/8}`. The zero-duration control remains a successful Lonely Runner configuration.

All five inputs already admit `t=1/8`, since none of their seven positive integer speeds is divisible by 8. The experiment therefore adds no existence coverage. Its target is selecting and explaining positive-duration certificates in the strict cases while preserving the equality distinction. The endpoint fallback reproduces an already-known witness.

## The same nontrivial map can hide a different answer

Compare `(x,y)=(11,13)` and `(11,45)` on the identical core `{1,4,6}` and window

\[
J=[9/32,5/16].
\]

Both maps have vanished blocker 5 and the sole nontrivial containment `B11 subset B7`. All other nontrivial directed containment tests agree as false. In both, the retained roles are 7 and y. The geometry, vanished labels, equality classes, and inclusion map are identical on corresponding runner roles. Numerical y is part of the original input, but is deliberately absent from this compressed map.

| Property | y=13 | y=45 |
| --- | --- | --- |
| Core and window | 1,4,6 on J | 1,4,6 on J |
| Retained roles | 7,y | 7,y |
| Fixed remaining interval S | [17/56,5/16] | [17/56,5/16] |
| y blocking within S | Entire S | (37/120,5/16] |
| Allowed portion of J | Empty | [17/56,37/120] |
| Actual clear duration | 0 | 1/210 |

This is an exact physical matched-map counterexample. No function of this local qualitative map and window geometry alone can correctly determine local existence for both inputs. The claim concerns this summary on this window; it does not rule out a selector that uses information from other windows or retains more of the speed data. Both complete configurations satisfy Lonely Runner.

The missing quantitative inputs are visible explicitly. In both cases `|J|=1/32`, `D7=5/224`, and `D11=O7,11=1/352`. The variable quantities are

| Quantity | y=13 | y=45 |
| --- | ---: | ---: |
| D_y on J | 3/208 | 7/720 |
| O_7,y on J | 1/182 | 1/180 |
| Exact reduced expression | 1/32 - 5/224 - 3/208 + 1/182 = 0 | 1/32 - 5/224 - 7/720 + 1/180 = 1/210 |

Across the batch there are 16 groups of matching local maps. Eight groups differ in actual duration; six differ in whether the local allowed set is empty. These counts include reflections. Adding all single durations leaves four matching groups, none differing in allowed sets; adding pairs leaves the same four. This small outcome does not establish single-duration sufficiency. Earlier [moment-collision examples](RESIDUE_COLLISIONS_2026_09_27.md) already show why stronger summaries can fail in other scopes.

## The countercontrol reveals a different containment

The previous x=19,y=45 control refuted the necessity of `B_x subset B7` for a positive value of the fixed star tree centered at 7. That statement remains correct.

The new map checks every residual pair. On J it finds

\[
B_{19}\cap J=(47/152,5/16]
\subset B_{45}\cap J.
\]

The second blocking interval of 45 begins at `37/120<47/152`. Therefore the useful safety implication is “45 safe implies 19 safe.” Remove 5, which vanishes, and then remove 19 because of this containment. Only 7 and 45 remain.

The old fixed tree `(5,7),(7,19),(7,45)` has value `47/31920`. The tree `(5,7),(7,45),(19,45)` has value `1/210`, exactly the actual duration. The improvement is `1/304`.

This changes the edge we use, not the underlying single/pair data. The maximum-tree calculation already contains the better certificate; the relationship map explains it. Q ultimately chooses another component with a larger positive lower bound, as the table above records.

## What the reduction preserves and what it cannot improve

If a blocker is contained in another, removing it preserves the union pointwise. Removing empty blockers and retaining maximal representatives therefore preserves the complete local allowed set, including equality points. Both implementations verify that identity on all 80 windows.

The reduction also preserves the **optimal tree bound**. Here is the supplied general argument for finite measurable blocking sets. Suppose `B_i subset B_j`. Then `O_ij=D_i` and `O_ik<=O_jk` for every other k. The edge i–j has maximum weight among all edges incident to i, so a maximum spanning tree can be chosen to contain it: insert it into an optimal tree and remove an edge on the resulting cycle incident to i, whose weight is no greater. Contract i–j. Every edge from i to another vertex is dominated by the corresponding edge from j, so the contracted optimum is the optimum after deleting i. Thus

\[
\operatorname{MST}_{\rm full}=D_i+\operatorname{MST}_{\rm without\ i},
\]

and the added `D_i` cancels the deleted single duration. Empty blockers have zero incident weights and can also be removed without changing the bound. Iterate to obtain the reduction. This is a proof candidate, separately corroborated on the finite batch.

This distinguishes simplifying the representation from strengthening an already optimal tree inequality. A previously fixed tree can improve, as the 19/45 example shows; the maximum over all trees is unchanged by deleting the redundant vertices.

| Retained blockers | Windows | Positive actual duration | Positive tree bound | Tree bound equals actual duration |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 40 | 2 | 2 | 40 |
| 2 | 10 | 8 | 8 | 10 |
| 3 | 2 | 2 | 2 | 0 |
| 4 | 28 | 18 | 4 | 4 |

There are 30 windows with positive actual duration but only 16 with a positive tree certificate. Q succeeds by selecting among the available windows; it does not make the tree exact or sufficient everywhere. No new LP calculation was performed to determine whether the other misses can be repaired by a stronger pair inequality.

After the maps are known, the sum of retained single/pair input counts is 362, versus 800 for all four residual labels on every window. This is a description-size comparison, not a measured runtime improvement. Discovering the maps itself has a cost; the implementation computes all full moments for verification.

## Verification and artifacts

The primary implementation uses closed safe-interval intersections for core components and allowed sets, exact event vertices/cells for strict maps and state masses, and exhaustive labelled tree enumeration. G and Q have explicit selection keys that do not read the actual allowed sets.

The separate verifier imports no project code. It represents strict blocking intervals with endpoint flags, tests containment by intersection with another runner's closed safe laps, obtains state masses through all-subset intersections and Boolean inversion, finds representative sets by exhaustive domination tests, and computes maximum-tree values with Kruskal's algorithm. It independently rebuilds complete allowed sets from threshold vertices/cells, replays choices and fallback, and compares matched summaries pairwise. Every claimed witness passes all seven original constraints.

Strict and measure-only containment maps happen to agree in all 80 windows. Both were calculated separately; this observation is not permission to drop endpoint checks in other configurations.

```bash
python -B reviews/2026-09-27-lr2/check_relationship_selector.py --check
python -B reviews/2026-09-27-lr2/crosscheck_relationship_selector.py --check
```

- [Frozen protocol](../reviews/2026-09-27-lr2/relationship_selector_protocol.json)
- [Primary calculation](../reviews/2026-09-27-lr2/check_relationship_selector.py)
- [Exact maps, witnesses, choices, and collision groups](../reviews/2026-09-27-lr2/relationship_selector.json)
- [Independent verifier](../reviews/2026-09-27-lr2/crosscheck_relationship_selector.py)
- [Independent comparison record](../reviews/2026-09-27-lr2/relationship_selector_crosscheck.json)
- [Package manifest](../reviews/2026-09-27-lr2/relationship_selector_manifest.json)

No previous checker or evidence archive was modified. No broader regression suite, all-reference enumeration, external outreach, literature/novelty review, or main merge was performed.

## What this changes and the next question

The proposed relationship map now has a demonstrated role and a demonstrated limit: it explains redundant constraints, while remaining quantitative coverage determines whether the surviving constraints leave room. Fewer retained constraints is not a sufficient criterion for choosing a successful window.

The strongest small next test is transfer without retuning: carry the fixed quantitative rule to an existing control where the common `1/8` witness fails, such as `{0,1,4,5,6,7,11,16}`, with the same two cores. Check whether it selects a strict certificate, and inspect the relation that helps or the counterexample that defeats it. This proposed transfer has not been run here. It would remain a bounded test, not establish arbitrary-speed selection.

For eventual generality, the missing question is why a useful quantitative certificate or contact must exist in every required configuration. This experiment does not supply that bridge. The +7/+9 extension remains parked.
