# One occurrence table certifies two target exclusions

September 28, 2026 UTC. Baseline `d578e9f75b73d841c58577c435dfbbcf763f09e4`, draft PR #3. Material AI involvement: a coordinating agent, a primary calculation agent, a separately structured verification agent, and an adversarial-review agent with two read-only subreviews. This is internal AI work, not independent human mathematical validation.

**Question.** Can the selected zero bounds on `{15,38,61}` and `{15,38,100}` be verified as one shared geometric containment without reconstructing all four triple durations?

**Outcome.** Yes, after the pair `{15,38}` is supplied. On the archived target window,

`B_15 intersect B_38 = (63/304,5/24)`.

This is one lap-labelled occurrence, with laps `(3,8)`. Throughout its closure the complementary phase ranges are

| Complement runner | Fractional phase range |
| --- | --- |
| `61` | `[195/304,17/24]` |
| `100` | `[55/76,5/6]` |

Both ranges lie strictly inside the safe phase interval `[1/8,7/8]`. Therefore

`B_15 intersect B_38 subset Safe_61 intersect Safe_100`,

which simultaneously verifies the two distinct facts

`T_(15,38,61)=0` and `T_(15,38,100)=0`.

Substituting them into the previously known five-edge correction gives

`U >= C_0-O_(61,100)=49/524400>0`.

This rules out every complete-cover mass arrangement compatible with the archived total, single and pair moments plus these two geometric exclusions.

**Status.** OBSERVED/REPRODUCED for one frozen selected-reference window, its reflection check, and three named controls. The containment is one compound geometric certificate, but logically it remains two complement-safety predicates over one preselected pair. It is not one bit, a pair selector, a new graph inequality, new existence coverage, or an intrinsic runtime improvement.

## 1. Frozen contract

The [protocol](../reviews/2026-09-28-shared-pair-containment/protocol.json), SHA256 `52cdd98452f9e47c082bb53703b1a20dc07fa9e47860bc7bbf0e2eb1d00378f3`, was saved before calculation. It fixes:

- the collective target and supplied base pair `{15,38}`;
- the prior sparse-family comparison pair `{6,11}` for strict16 and tight13;
- all six possible base pairs in doubling112 as a diagnostic only, with no post-result selection;
- exact strict-blocking endpoint semantics;
- a lap-interval primary method and an independently structured threshold-event verifier;
- an explicit work ledger and comparisons with naive separate triple reconstruction and the prior sparse arithmetic tests.

No LP search, new speed, core, window, reference, pair retuning, broad scan, alternate-window campaign, `+7/+9` work, or paid computation was added.

## 2. Exact target certificate

Within `J=[33/184,39/184]`, the two base blockers have only these pieces:

`B_15=(23/120,5/24)`,

`B_38=(55/304,3/16) union (63/304,39/184]`.

Their sole positive intersection is `(63/304,5/24)`, of duration `1/912`. The endpoint phase ranges displayed above have no integer or threshold crossing, so checking their exact lifted endpoints certifies each complementary runner on the whole interval. The excluded base-pair endpoints are threshold contacts; both complement runners are safely interior there, so the closure test is stronger than required.

The reflected target interval `[145/184,151/184]` has the reversed component `(19/24,241/304)`, base laps `(12,30)`, and complement ranges

- speed `61`: `[7/24,109/304]`;
- speed `100`: `[1/6,21/76]`.

It is the exact common-start reflection, not another selected configuration or independent success.

## 3. What was compressed—and what was not

The selected target certificate enumerates three blocking pieces for the two base runners, performs two pair-join steps, finds one shared component, and performs two complement phase-range checks. It never constructs the target’s seven complementary blocking pieces. The complete archived four-runner schedule has ten blocking pieces.

The primary implementation records 95 exact rational comparisons for this route. Its deliberately naive two-triple comparator rebuilds the base schedules twice, constructs each complement’s full schedule, and records 188 comparisons. Those numbers describe these implementations only. The difference combines common-subexpression reuse with a different phase-range method; it is not an intrinsic factor-of-two or uniform complexity theorem.

A competent cached implementation can reuse the same base-pair decomposition and must still evaluate the same two complement predicates. The defensible conclusion is therefore narrower: one occurrence table avoids duplicated base geometry and gives a compact simultaneous proof. It does not reduce two logical facts to one information bit.

Most importantly, this study does not select `{15,38}`. That pair came from the preceding four-coordinate subset audit after the physical triple bounds were available. The sparse selector’s two arithmetic occurrence tests and its alternate-window transfer are prior, special-family selection mechanisms. This target application verifies a supplied pair; cheap general discovery remains open.

## 4. Controls

The frozen controls separate containment from duration and from pair selection:

| Case | Shared base pair | Containment | Five-edge raw bound | Interpretation |
| --- | --- | --- | ---: | --- |
| collective target | `{15,38}` | holds | `49/524400` | positive duration certified |
| strict16 | `{6,11}` | holds | `1/896` | prior repair reproduced |
| tight13 | `{6,11}` | holds | `-1/182` | no duration certificate |
| doubling112 | all six tested diagnostically | all fail | not applied | pair-only route already succeeds |

For strict16 and tight13, `B_6 intersect B_11=(31/88,17/48)`, with base laps `(2,4)`. Speed `7` has phase range `[41/88,23/48]`; speed `16` has `[7/11,2/3]`, and speed `13` has `[51/88,29/48]`. These are the old sparse-family exclusions expressed in the shared-pair language, not new repairs.

Tight13 is the necessary countercontrol: the containment is true, but its five-edge arithmetic is negative. The valid point `t=3/8` remains isolated, with runner `11` blocking immediately left and runners `5` and `13` immediately right. A true containment therefore does not itself imply positive lonely duration.

Doubling112 already has pair-only minimum `761/32256>0`. The diagnostic nevertheless tests every possible base pair. All six containments fail, each with an archived positive rational open interval, midpoint, base laps, and a blocking complementary runner. No pair was selected after these outcomes.

## 5. Prior-work boundary

Pair-occurrence phase containment is already present in the repository’s `56/113` analysis, uniform-triangle continuation, strict16 repair, and fixed-window containment work. The arithmetic inequality

`U >= C_0-O_cd-T_abc-T_abd`

is the prior five-edge `K_4`-minus-one-edge correction. The bounded contribution here is its exact shared-clock realization on the newly preserved collective target and an explicit accounting of which geometric work is reused.

The old sparse selector remains stronger as a selection result in its fixed family: it uses two arithmetic occurrence tests to choose a graph. The present target study starts after pair selection. No novelty claim is made for the containment form, graph correction, strict16 mechanism, sparse tests, or alternate-window dispatch.

## 6. Exact verification

Artifacts are under [reviews/2026-09-28-shared-pair-containment/](../reviews/2026-09-28-shared-pair-containment/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-shared-pair-containment/primary.py --check
python -S -B reviews/2026-09-28-shared-pair-containment/verify.py --check
```

The independent verifier imports neither primary code nor its interval helper. It checks 91 open threshold cells and 95 event points over the four original windows, plus 17 cells and 18 points for the reflection. It reproduces all three selected containments, all six doubling failures, the five-edge arithmetic, archived moments and atoms, the prior sparse `w=13/16` comparisons, reflection, and tight13’s isolated endpoint.

The [adversarial review](../reviews/2026-09-28-shared-pair-containment/challenge.md) found no fatal defect after requiring explicit endpoint membership, correcting a verifier schema comparison, and separating naive reconstruction cost from competent caching. A review subagent accidentally invoked the primary writer once; the primary owner subsequently regenerated the final archive, and that accidental run is not counted as independent evidence.

## 7. Next bounded question

Selection, not verification, is now the consequential gap. Freeze a new investigation before calculation on the same cases: among base pairs with positive potential five-edge slack `C_0-O_cd`, compare two predeclared pair-only rules—largest potential slack and fewest positive base-pair occurrence components, with physical-speed lexicographic ties—then permit only one compound containment query.

The target must be treated as a required counterpressure, not a tuning set: a high potential bound is only capacity and need not correspond to a true containment. Preserve a failed selection without adding another rule or query. This tests whether a small occurrence-complexity record can help choose the compact certificate from speeds and pair summaries; it adds no new speeds, windows, references, or broad search.
