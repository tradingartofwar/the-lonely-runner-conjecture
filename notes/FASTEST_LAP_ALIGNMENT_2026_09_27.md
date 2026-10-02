# Fastest laps reveal exact contacts, lost alignment, and phase robustness

September 27, 2026 (Pacific). Baseline `f362f54b8f5077f12579076e815d505bf81cf9a6`. Vance authorized the next six-agent plan and execution after the [fastest-core finding](FASTEST_CORE_CERTIFICATES_2026_09_27.md). The team divided primary computation, independent verification, hostile review, arithmetic, phase experiments, and representation analysis. AI materially contributed the protocol, calculations, proofs, reviews, and writing.

**Main outcome:** the two controls admit a common geometric explanation. During suitable times when the other runners are safe, runner 11's available phases fill an arc. In the tight speed-13 case, that arc exactly fits its blocking arc at the original phase; any nonzero phase shift creates a positive opening. In the speed-16 case, the available phase union is wider than a blocking arc, so every initial phase leaves a uniform amount of clear time. The complete supplied arguments are in [PHASE_ROBUSTNESS_2026_09_27.md](PHASE_ROBUSTNESS_2026_09_27.md).

These are restricted proof candidates for the two fixed speed lists and an explicitly shifted-start family. The original common-start outcomes were already known. Neither the finite experiment nor these arguments proves general Lonely Runner or establishes novelty.

## Fixed plan and completed scope

The [protocol](../reviews/2026-09-27-fastest-laps/protocol.json) was fixed before the new calculations, with hash

`f1d4772133a47a3090c5f9f5f3aa6389b378917c0744a80e3df728790e397d7d`.

Keep eight runners, reference 0, threshold 1/8, and velocities `{0,1,4,5,6,7,11,V}` for exactly V=13 and V=16. The sole core runner is V. Its complete safe laps are

\[
W_m=[(8m+1)/(8V),(8m+7)/(8V)],\quad m=0,\ldots,V-1.
\]

The plan was to reconstruct all 29 laps, compare exact coverage chains and contacts, track shared integer residues, test a bounded rearrangement of runner 11's lap patterns, and independently check everything. That plan is complete. No further speed lists, reference runners, phase grid, or unbounded search were added. The continuous-phase statements were derived analytically during review and are separately labeled.

## 1. The original 29 laps

| Original case | Fully covered laps | Contact-only laps | Positive-duration laps | Total clear duration |
| --- | ---: | ---: | ---: | ---: |
| V=13 | 9 | 4 | 0 | 0 |
| V=16 | 12 | 0 | 4 | 39/4928 |

All 29 optimal six-vertex tree bounds equal the actual duration. This checks the earlier fastest-core argument in its one-runner-core form. It does not make zero duration equivalent to complete blocking.

For V=13, laps 1,4,8,11 contain exactly the four valid points `1/8,3/8,5/8,7/8`. The first and last are interior contacts where the full blocking envelope touches without crossing. The middle two lie on fastest-lap boundaries. Counting internal touches alone would miss half the valid points.

For V=16, the four surviving intervals are

| Lap m | Allowed interval | Duration |
| ---: | --- | ---: |
| 4 | [17/56,39/128] | 1/896 |
| 7 | [41/88,15/32] | 1/352 |
| 8 | [17/32,47/88] | 1/352 |
| 11 | [89/128,39/56] | 1/896 |

Each has a directly checked strict midpoint witness. The full allowed sets, endpoint controllers, strict blocker intervals, moments, maximizing trees, residue lifts, and scan records are archived.

## 2. A small exact decomposition explains the difference

The six unchanged residual speeds `{1,4,5,6,7,11}` jointly leave four isolated odd eighths and these four positive intervals:

\[
[17/56,5/16],\ [41/88,15/32],\
[17/32,47/88],\ [11/16,39/56].
\]

Their total duration is `29/1232`. Speed 13 strictly covers all four positive intervals while preserving the four isolated contacts. Speed 16 blocks all four old contacts, preserves the middle two intervals, and truncates the outer pair to the intervals in the table.

This is an exact factorization of the two outcomes. Computing the six-runner safe set already uses their full joint timing, so this explanation must not be advertised as a general consequence of marginal counts.

## 3. Qualitative chains still omit consequential information

Before computing outcomes, the primary schema fixed a qualitative summary: vanished blocker labels, left-endpoint order of the remaining blockers, and the strict containment map. It deliberately omits metric positions, endpoint flags, and comparisons between left and right endpoints. The 29 laps form 21 summary groups, including four groups with different allowed-set statuses. Those four groups are two reflection-paired mechanisms, not four independent tests.

For example, V=13 lap 3 and V=16 lap 4 both retain speeds 4,11,7 in that left-to-right order, have the same vanished blockers and containment map, and even have the same overlap/overlap scan junction types. The former is completely covered; the latter leaves length 1/896. The difference is where the final right envelope ends relative to the lap boundary.

A second pair, V=13 lap 4 and V=16 lap 5, has matching qualitative data but respectively a valid boundary contact and complete coverage. Endpoint inclusion distinguishes them. These comparisons have different windows and widths; they do not strengthen the earlier same-window counterexamples. They show exactly the insufficiency of this declared compression.

A touch of the *full* sorted union envelope is different from a touch of an arbitrary pair. A third interval can hide a pairwise contact; if it extends through that point, the complete envelope has already passed it. All two recorded internal full-envelope touches survive, and separate boundary checks retain the other two original contacts.

## 4. Identical individual inventories can have different joint outcomes

Normalize each lap by `u=Vt-m`, so every window becomes `[1/8,7/8]`. Shift only speed 11's normalized blocker pattern from lap `m+s mod V` into lap m, for every s from 0 to V-1. This preserves the entire multiset of endpoint-aware normalized patterns for each individual runner across the V laps.

The rearrangement is physically equivalent to giving speed 11 initial phase `theta=11s/V mod1`. Only s=0 is the original common-start input. There are 29 offset arrangements and 425 lap records, all separately reconstructed from direct shifted phase equations. As a control, shifting all six residual patterns together merely permutes the original lap records; every one of the 29 controls preserves duration and contact count.

| Case | Offset s | Runner-11 phase | Total clear duration | Isolated contacts |
| --- | ---: | ---: | ---: | ---: |
| V=13 | 0 | 0 | 0 | 4 |
| V=13 | 1 | 11/13 | 1517/48048 | 3 |
| V=16 | 0 | 0 | 39/4928 | 0 |
| V=16 | 1 | 11/16 | 193/2688 | 0 |

For V=13, every nonzero prescribed offset has positive duration. For V=16, every prescribed offset has positive duration. All 29 remain globally nonempty. Thus this experiment demonstrates loss of duration and local existence information, and a change from contact-only to strict behavior; it does **not** supply a global nonempty-versus-empty collision.

One explicit local change occurs in V=13 lap 5: its original speed-11 pattern covers the portion surviving the other five residual runners. Offset 1 imports an empty speed-11 pattern and creates `[25/56,47/104]`, of length 1/182. In V=16 lap 4, the same offset closes the original opening while larger openings appear elsewhere. Local and global changes must remain separate.

Pair overlaps are not preserved. Across all fastest safe laps, for V=13 the speed-1/speed-11 pair overlap changes from `5/143` to `6/143` under offset 1, although their individual durations stay `5/26` and `27/143`. This is an individual-inventory counterexample, not a collision of all pair summaries.

## 5. What links the laps

The residues `r_v(m)=vm modV` are not six independently chosen phase offsets. They belong to the single cyclic orbit

\[
m(1,4,5,6,7,11)\pmod V.
\]

Because speed 1 is present, its residue identifies m. In particular, `r11-11*r1=0 modV`. Shifting only speed 11 replaces that invariant by `11s modV`; shifting all residuals together reindexes the original orbit.

In continuous phase language, common start gives `x11=x4+x7=x5+x6 mod1`. A speed-11 phase change adds the same constant theta to both relationships. The velocity relations persist; their phase constants change. An inventory that forgets which patterns share a lap loses that alignment information.

The [representation review](../reviews/2026-09-27-fastest-laps/representation.md) makes this precise with a cyclic cross-correlation formula. That formula evaluates the alignment once the joint safe patterns are supplied; it does not force a favorable alignment in arbitrary configurations.

## 6. Two continuous-phase certificates

The supplied proofs go beyond the finite offsets without adding an empirical phase scan. With only runner 11's phase varying,

\[
D_{13}(\theta)\ge\frac{\min(\|\theta\|,1/4)}{11},
\qquad D_{16}(\theta)\ge\frac1{176}.
\]

For V=13, the other six constraints are safe on `[17/48,3/8]` and its reflection. Their speed-11 phase images fill exactly the arc `[-1/8,1/8]`, of width 1/4. A displaced blocker of the same width cannot cover that entire arc in measure. At theta=0 its exact alignment covers the arc interior; the original isolated contacts remain valid. The common-start phase is therefore uniquely zero-duration in this particular one-parameter family.

For V=16, the other six constraints are safe on `[25/56,15/32]` and its reflection. Their speed-11 phase images fill an arc of width 5/16. A blocker of width 1/4 leaves phase measure at least 1/16, hence time at least 1/176, at every phase. The union of phase images is used; overlapping images are not counted twice.

The complete phase projection in the V=13 control is also determined: `[-1/8,1/8] union {3/8,5/8}` on the circle, for times safe for the other six runners. This follows from the certified intervals together with the previously known tight allowed set; it does not independently establish the tight result. Its two arc endpoints and two isolated projected points account for the four original contacts.

See [the self-contained proof candidates](PHASE_ROBUSTNESS_2026_09_27.md), [arithmetic review](../reviews/2026-09-27-fastest-laps/arithmetic.md), and [challenge review](../reviews/2026-09-27-fastest-laps/challenge.md). These are specific geometric certificates using already established safe intervals. They do not show that arbitrary speed configurations provide the same phase spread.

## Verification, preservation, and limits

```bash
python -B reviews/2026-09-27-fastest-laps/calculate.py --check
python -B reviews/2026-09-27-fastest-laps/phase_experiment.py --check
python -B reviews/2026-09-27-fastest-laps/verify_independent.py --check
python -B reviews/2026-09-27-fastest-laps/arithmetic_check.py --check
python -B reviews/2026-09-27-fastest-laps/challenge_check.py --check
```

The primary calculation uses exact interval intersections and all 1,296 labelled six-node trees. Its separately structured verifier uses event-state reconstruction and Kruskal, without reading or importing either primary implementation. All 29 original records match field by field and digest; all 29 shifted arrangements, 425 lap records, endpoint inventories, witnesses, and control digests also match. Additional scripts check arithmetic and review claims. The [manifest](../reviews/2026-09-27-fastest-laps/manifest.json) records source/artifact hashes and exact scope.

Finite calculations are OBSERVED / independently REPRODUCED in this declared scope. General arguments are HYPOTHESIS / proof candidates under repository rules. Neither AI agreement nor repeated checks constitute outside review. No historical code or data was modified, no broad regression suite or new literature frontier audit was run, and no external contact, paid compute, main merge, or novelty claim occurred.

## Next question

The useful configuration-level object is the set of phases a chosen runner visits during times when all the other runners are safe. Its interval width and placement can obstruct complete blocking; its isolated points can preserve equality-only solutions. Exact duration additionally depends on how many safe-time preimages each phase has.

The next bounded investigation should extend the known V=13 projection to a complete endpoint-aware projection for V=16, and record safe-time preimage multiplicities for both controls. Compare which smaller summaries preserve existence, strictness, and duration. Then seek a sufficient arithmetic condition that forces a projected interval to be wider than a blocking arc, or exposes a protected contact, without first computing the entire joint safe set. This extension is proposed, not executed here. The missing general step is still an existence guarantee for arbitrary required configurations; +7/+9 remains parked.
