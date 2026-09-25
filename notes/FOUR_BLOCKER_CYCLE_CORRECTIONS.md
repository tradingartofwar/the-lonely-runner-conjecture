# Four blockers: when compatibility needs a duration

September 25, 2026. Baseline: `91561c35751f1281c5b6920a8022f2f6653672bb`. **OBSERVED:** eight prescribed configurations, all previously studied. The general counting arguments below are self-contained **HYPOTHESIS/proof candidates pending independent review** under the repository convention. No new inequality, family coverage, or general conjecture result is claimed. AI materially supplied the reasoning, code, and writing.

Throughout, eight runners start together, the selected reference has speed 0, and equality at distance `1/8` counts. The fixed core is `{1,4,5}` and its safe window is

\[
J=[9/32,3/8],\qquad |J|=3/32.
\]

The other four speeds are the blockers. A blocked time has distance **strictly less** than `1/8`. Duration statements ignore individual endpoints; actual endpoint membership is checked separately.

## 1. What transferred, and what did not

The preceding [two-speed study](TWO_SPEED_SPARSE_TRANSFER.md) relied on blockers 6 and 7 being disjoint on J. Here all six pair overlaps are positive in each of the five fast configurations. That simplifying assumption disappears.

Compatibility information still helps. It improves the best tree bound in five of the eight cases. However, if all four blockers overlap for positive duration, every graph satisfying the **active induced graph is a forest** condition must itself be a forest. Within that certificate class, no choice of compatibility bits can beat the maximum tree. This is a limit of that sufficient condition, not an impossibility theorem for all inequalities based on pair data.

Two existing inputs exhibit this limit: `{56,64,72,112}` and `{309,320,328,619}`. A duration correction lets a cycle survive in both. The best connected graph with one cycle, corrected by its one cycle-intersection duration, improves the tree in seven of eight cases. The remaining case already has an exact tree certificate. All configurations were already known to have a valid time; this comparison improves local bounds and explains information loss.

## 2. An exact count explains the correction

Let `S(t)` be the active blocker set. For a graph G on the four blockers, write `e_G(S)` for its induced edge count and `c_G(S)` for its number of connected components, including isolated active vertices. Set `c_G(empty)=0`. Its cycle rank is

\[
\beta_G(S)=e_G(S)-|S|+c_G(S).
\]

With individual durations D_i and pair durations O_ij, define

\[
P_G=|J|-\sum_iD_i+\sum_{ij\in E(G)}O_{ij}.
\]

The pointwise identity `1-|S|+e_G(S)-beta_G(S)=1-c_G(S)` gives

\[
U\ge P_G-\int_J\beta_G(S(t))\,dt,
\]

and the exact remaining gap is

\[
U-\left(P_G-\int_J\beta_G(S(t))\,dt\right)
=\int_{S(t)\ne\varnothing}(c_G(S(t))-1)\,dt.
\]

Thus cycles cause overcounting, while disconnected active sets explain the remaining underestimate after correction. Both are counts in the representation. They are not physical interactions between runners.

For a connected graph with exactly one cycle C, the rank is simply `1` when every vertex of C blocks and `0` otherwise. Only one higher-order duration is needed:

\[
U\ge P_G-T_C.
\]

A triangle with a leaf uses a triple duration. A four-cycle uses the four-way duration Q. A proven upper bound on T_C also suffices; exact reconstruction is not required by the inequality. Adding an edge to a tree creates one such cycle, and its gain after correction is `O_new-T_C>=0`, since the cycle intersection is contained in that edge's pair intersection.

The triangle-with-leaf bound was already recorded in [LR2_REVIEW_PRIORITIES.md](LR2_REVIEW_PRIORITIES.md). Its chordal-graph context is [S18](SOURCES.md#s18--graph-sieves-beyond-trees); the four-cycle argument here is supplied by the count above, not attributed to the chordal theorem. No new literature audit or novelty conclusion was undertaken.

For four vertices, the best four-cycle has a particularly small selection formula. Its omitted edges form one of three perfect matchings:

\[
B_4=|J|-\sum_iD_i+\sum_{i<j}O_{ij}
-\min(O_{12}+O_{34},O_{13}+O_{24},O_{14}+O_{23})-Q.
\]

This selects among three cycles using six pair weights and one four-way duration or upper bound. It need not beat every tree: the original `{6,7,11,16}` example needs a triangle with a leaf instead. The best of all 15 connected four-edge graphs permits both cycle types.

## 3. The 113 case: a shared-clock exclusion

For extras `{56,64,72,113}`, no triple `{56,64,113}` occurs. This can be checked without reconstructing the full seven-speed schedule. The already-known six 56/113 overlap pieces carry laps `(j,2j)`, j=16 through 21. On each piece, speed 64's fractional phase stays strictly inside the safe range:

| Laps of 56 and 113 | Overlap interval endpoints | Fractional phase range of 64 |
| --- | --- | --- |
| 16, 32 | 127/448, 257/904 | 1/7 to 22/113 |
| 17, 34 | 135/448, 273/904 | 2/7 to 37/113 |
| 18, 36 | 143/448, 289/904 | 3/7 to 52/113 |
| 19, 38 | 151/448, 305/904 | 4/7 to 67/113 |
| 20, 40 | 159/448, 321/904 | 5/7 to 82/113 |
| 21, 42 | 167/448, 337/904 | 6/7 to 97/113 |

All these ranges lie inside `(1/8,7/8)`. Hence the triple is empty, and so is the four-way intersection. The other three triples have positive durations `1/576`, `25/50624`, and `1/4608`, respectively for `{56,64,72}`, `{56,72,113}`, and `{64,72,113}`.

The best compatibility graph is the four-cycle with edges `{56,64}`, `{56,72}`, `{64,113}`, `{72,113}`. Its only cycle requires all four blockers; Q=0 suffices to retain it. We do not need to exclude the other triples.

| Certificate | Lower bound on clear duration |
| --- | ---: |
| Best tree | 58073/3644928 |
| Best compatibility graph / corrected one-cycle graph | 72311/3644928 |
| Best five-edge graph, with its two triangle corrections | 11369/520704 |
| Actual duration, diagnostic reconstruction | 6193/260352 |

The five-edge winner omits edge `{64,72}`. Its triangle corrections are `{56,64,113}` (zero) and `{56,72,113}` (`25/50624`). Thus one excluded triple and one nonzero triple duration improve on the four-cycle. It still misses exactly `1/512` of the actual duration.

This is a concrete LTCM result: the lap/phase model uses the shared clock to supply an intersection restriction alongside the pair totals. The earlier 6/7/11/16 abstract-distribution control already demonstrated that pair totals alone can lose decisive compatibility information; no new impossibility claim about all pair-data inequalities for this 113 input is needed here.

## 4. Changing 113 to 112 changes the information needed

For `{56,64,72,112}`, all four blockers are simultaneously active on

\[
(335/896,3/8],\qquad Q=1/896.
\]

The right endpoint is a collision for all four; the left is a threshold equality for speed 112. Every triple also has positive duration. Therefore no globally cyclic graph meets the uncorrected active-forest condition.

The four-cycle with edges `{56,72}`, `{56,112}`, `{64,72}`, `{64,112}` is nevertheless useful after subtracting Q:

| Certificate | Lower bound on clear duration |
| --- | ---: |
| Best tree / best compatibility graph | 761/32256 |
| Best one-cycle graph, subtracting Q=1/896 | 851/32256 |
| Best five-edge graph, subtracting two triple durations | 911/32256 |
| Actual duration | 53/1792 = 954/32256 |

The five-edge winner omits `{56,64}`. Its two triple corrections total `1/252`, and its remaining gap is `43/32256`.

This controlled comparison does not say 113 is harder or easier overall. Both inputs already had positive certificates. It shows why a yes/no overlap language can stop helping even when a small quantitative correction still helps substantially.

## 5. What a five-edge graph still loses

A four-vertex graph missing only edge ij contains exactly two triangles. For this graph, subtract their two triple durations. The cycle-rank identity remains exact even on the four-way state: its rank is two, so both triangles must be subtracted there.

Every nonempty induced graph is connected except the state in which **exactly i and j** block. Therefore the corrected bound has the simple exact gap

\[
U-B_{K_4-ij}=\bigl|\{t:S(t)=\{i,j\}\}\bigr|.
\]

Choosing the best of the six such graphs minimizes that omitted-pair-only mass. This explains the remaining `1/512` in the 113 case and `43/32256` in the 112 case. All six pair-only masses are positive in each of the five fast inputs, so no five-edge graph is exact for those inputs.

Keeping all six edges and all higher intersections recovers ordinary inclusion-exclusion:

\[
U=|J|-\sum D_i+\sum O_{ij}-\sum_{i<j<k}T_{ijk}+Q.
\]

That is exact reconstruction from complete joint information, not a new sparse existence proof.

## 6. Bounded results and reproducibility

The first seven inputs are exactly the archived cases in [OVERLAP_PLACEMENT.md](OVERLAP_PLACEMENT.md). The eighth is the original Ultra-review tree failure. No speed scan was added.

| Extra speeds, sorted | Four-way duration Q | Compatibility beats tree? | One corrected cycle beats tree? |
| --- | ---: | --- | --- |
| 56, 64, 72, 112 | 1/896 | No | Yes |
| 56, 64, 72, 113 | 0 | Yes | Yes |
| 6, 7, 11, 13 | 0 | Yes, reaches zero | Yes, reaches zero |
| 6, 7, 8, 11 | 0 | No, tree exact | No, tree exact |
| 309, 320, 328, 619 | 1/63757 | No | Yes |
| 310, 320, 328, 621 | 0 | Yes | Yes |
| 320, 328, 336, 641 | 0 | Yes | Yes |
| 6, 7, 11, 16 | 0 | Yes, exact | Yes, exact |

The tight `{6,7,11,13}` case still has zero clear duration and the valid singleton `t=3/8`. A zero lower bound alone does not certify that singleton. Every finite case was already included in the research record, and these comparisons are not new independent runner configurations.

```bash
python -B reviews/2026-09-25-lr2/check_four_blocker_cycles.py --check
```

[Standalone script](../reviews/2026-09-25-lr2/check_four_blocker_cycles.py) and [exact archive](../reviews/2026-09-25-lr2/four_blocker_cycles.json). Two-pointer intersections of lap-labelled blocking intervals compute all 15 nonempty moments per case. A separately structured rational phase partition crosschecks all 120 moments and endpoint membership. All 64 graph masks are checked in every case, including the cycle-rank count on all 16 logical states and the exact corrected gap. The archive includes all 15 one-cycle options, all six five-edge options, higher-intersection lap witnesses, and direct state masses.

The 8,192 graph/state checks repeat the same algebra across eight inputs; they are not independent proofs. The 512 corrected graph comparisons use the same eight state distributions. A separate session check with the existing `feasible_intervals` routine confirmed all eight local clear durations and the tight singleton. Its source SHA-256 was `ba240664c273d254d0ab8d2da053dc1248dd0b0a88cd5f1c4ed35a3f6c579971`. The standalone archived command has no project imports and does not rerun that additional checker.

The finite diagnostic constructs interval lists; its work grows with the speeds. A fixed number of reported moments does **not** make their computation uniformly bounded. The earlier two-variable window rule obtained such a bounded occurrence count from its special fixed-core assumptions. No comparable reduction has been established here.

## 7. Next question

The useful target is now quantitative: under a stated speed relation, can we bound just the intersection belonging to a chosen cycle tightly enough to guarantee positive slack, without constructing every blocking interval? The four-cycle needs only an upper bound on Q; the triangle-with-leaf needs one on its triple. Keep both choices, since neither motif wins in every existing control.

Start from the already-preserved near-doubling family and compare any proposed estimate with its existing simpler one-pair certificate. Improvement in a bound must be distinguished from genuinely wider coverage. A successful arbitrary-speed core/window rule, an equality route beyond the known controls, and independent review remain OPEN.

**Continuation completed:** [The uniform triangle certificate](UNIFORM_TRIANGLE_CERTIFICATE.md) proves the proposed exclusion `T_(q,q+8,2q+1)=0` directly from phase bounds. Six fixed affine strips evaluate the needed pair durations; an analytic tail and finite remainder certify the local opening for every q>=28 and arbitrary distinct v>=q in this structured family. Neighboring offsets +7 and +9 retain positive triple overlap and become the next quantitative controls. The new certificate's occurrence count does not grow with q or v; the full diagnostics in this earlier note still do.
