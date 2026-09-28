# A common displacement makes joint timing compatibility explicit

September 28, 2026. Baseline: the preserved relational brief at `38550bfe709df46bdf00f50c6b41e1d328131698`, following `4a18e30f`. This is the interactive continuation; hourly research remains paused.

**Question.** Can a small piece of configuration-level timing information force an opening without reconstructing the complete allowed set?

**Answer within a declared certificate class.** Yes. At a rational anchor whose reduced denominator does not exceed the number of runners, every moving runner is either safe or exactly colliding with the reference. In either time direction, compare the latest entry into a runner's first available safe lap with the earliest exit from those safe laps. If the latest entry precedes the earliest exit, their shared interval is a certificate.

This is a general arithmetic sufficient condition, supplied with a proof below and checked on four existing controls. It does not prove that a suitable anchor or direction exists for every configuration. Interval intersection, directional endpoint reasoning and adaptive rational witnesses are prior ingredients; no novelty or new frontier result is claimed.

**Status:** HYPOTHESIS / supplied proof candidate under repository governance; OBSERVED / REPRODUCED for the finite exact checks. One coordinating AI wrote the argument and two algorithm structures. No separate agents or independent human reviewer participated.

## 1. Relation to the new research brief

[The preserved brief](inquiries/2026-09-28-configuration-relational-information.md) asks what facts belong to relationships among runners and disappear when individual or pair summaries are retained.

Here the relevant object is a collection of intervals on the **same displacement axis**. A runner's entry and exit are individual data. Whether every runner allows the same displacement is a configuration-level compatibility statement. It is determined by the full input; it is not an additional physical influence.

The useful inequality is

\[
\boxed{\text{latest entry}\ \le\ \text{earliest exit}.}
\]

Its two controlling runners need not be the same. Recording only which runners can eventually become safe would lose their common timing.

The earlier cross-window phase/orbit constraints are already explicit in [fastest-lap alignment](FASTEST_LAP_ALIGNMENT_2026_09_27.md). This increment does not repeat that phase-shift experiment. It derives a direct parameterized certificate from the existing arithmetic anchors. It is a smaller step toward the existence milestone, not a proof of the proposed global cross-window obstruction.

## 2. General arithmetic statement

Take `n>=3` common-start runners with distinct speeds `0,v_1,...,v_(n-1)`, the moving speeds positive integers. Select reference 0 and set `delta=1/n`.

Choose an anchor `t0=a/d` in lowest terms with `1<=d<=n`. Write

\[
p_i=\{v_i t_0\}.
\]

Every nonzero `p_i` lies in `[1/d,1-1/d]`, which is contained in `[delta,1-delta]`. Therefore a runner is either already safe or has `p_i=0`, an exact collision. Put `Z={i:p_i=0}`.

Choose one common direction `sigma in {+1,-1}` and write `t=t0+sigma*s`, `s>=0`. For each runner define its first safe displacement interval `[e_i,x_i]`:

\[
e_i=\begin{cases}\delta/v_i,&i\in Z,\\0,&i\notin Z,\end{cases}
\]

and

\[
x_i=\begin{cases}
(1-\delta)/v_i,&i\in Z,\\
(1-\delta-p_i)/v_i,&i\notin Z,\ \sigma=+1,\\
(p_i-\delta)/v_i,&i\notin Z,\ \sigma=-1.
\end{cases}
\]

Set `E=max_i e_i`, `X=min_i x_i`.

- If `E<X`, the interval between `t0+sigma*E` and `t0+sigma*X` is valid, with every runner strictly safe in its interior. Its duration is `X-E`.
- If `E=X`, that time is a valid threshold witness. Further endpoint information is needed before calling it isolated.
- If `E>X`, these **particular first safe laps** have no common displacement. Later safe laps, another anchor or another direction may still succeed.

For `Z` nonempty, `E=1/(n m)`, where `m=min_{i in Z}v_i`. If `Z` is empty, `E=0` and the anchor itself is already valid.

## 3. Proof and endpoint meaning

At a collision, moving either forward or backward takes the phase from an integer toward the first safe arc. It enters at displacement `delta/v_i` and exits at `(1-delta)/v_i`. Equality is safe at both endpoints.

For an already-safe phase `p_i`, the current lifted safe lap lasts forward until `p_i+v_i s=1-delta`, and backward until `p_i-v_i s=delta`. This gives exactly the displayed exit times. A phase initially on the outward-facing boundary supplies the singleton displacement interval `{0}`, which must not be discarded.

The common intersection of the closed intervals `[e_i,x_i]` is exactly `[E,X]` when `E<=X`, and empty otherwise. Each positive speed is strictly inside its allowed phase interval whenever `E<s<X`. This proves the claimed certificates.

All integer-speed configurations are periodic with period 1. If a backward certificate has negative times, translate the whole interval by an integer to obtain nonnegative times with identical distances.

If `E>X`, choose a runner attaining `E` and one attaining `X`. The former requires `s>=E`; the latter requires `s<=X` to stay in its chosen safe lap. This is an exact incompatibility certificate for that itinerary. It is not evidence against loneliness at other times.

The general conclusion rests on these inequalities, not on the four finite examples. Given an anchor, the formula uses a number of rational operations linear in the number of runners; this is not a uniform bit-cost or comparative runtime claim. Anchor discovery is not solved.

## 4. An explicit sufficient class with all speeds allowed to vary

For `t0=1/n`, forward direction, let `r_i=v_i mod n`. Suppose `Z={i:r_i=0}` is nonempty and `m=min_{i in Z}v_i`.

The conditions

\[
v_i\le(n-1)m\quad (r_i=0),\qquad
v_i\le(n-1-r_i)m\quad (r_i\ne0) \tag{1}
\]

imply `X>=E=1/(nm)`. Consequently

\[
t=\frac1n+\frac1{nm}
\]

is a valid lonely time for the selected reference. If every inequality in (1) is strict, a positive interval follows.

This is immediate on multiplying each exit inequality `x_i>=1/(nm)` by `n v_i m`. It allows all moving speeds to vary; it does not assume a fixed three- or six-runner core. Conversely, residue `n-1` makes the forward condition impossible, correctly recording an outward-facing boundary at the anchor. The backward condition exchanges `n-1-r_i` for `r_i-1`.

This corollary is an explicit sufficient class, not a classification of lonely configurations or a claim of new mathematical coverage relative to the literature. Some specializations are elementary speed-ratio witnesses; the earlier fixed-core/affine candidates cover other scopes. No published novelty audit was performed.

## 5. Frozen controls and exact outcomes

[protocol.json](../reviews/2026-09-28-common-displacement/protocol.json) declares four existing common-start configurations, anchors `1/8` and `2/7`, and both directions before calculation. All use reference 0 and threshold 1/8:

- small-gcd: `{0,1,4,5,56,64,72,113}`;
- doubling: `{0,1,4,5,56,64,72,112}`;
- tight13: `{0,1,4,5,6,7,11,13}`;
- strict16: `{0,1,4,5,6,7,11,16}`.

The anchors are development choices from prior arithmetic, not a blinded selection experiment: `2/7+1/56=17/56`, the old six-runner opening endpoint.

| Control | Forward from 1/8 | Forward from 2/7 | Backward checks |
| --- | --- | --- | --- |
| 56/113 | `[57/448,119/904]`, width `223/50624` | `[129/448,167/576]`, width `1/504` | Both first-band itineraries fail |
| 56/112 | `[57/448,17/128]`, width `5/896` | `[129/448,167/576]`, width `1/504` | From 2/7, `[145/512,127/448]`, width `1/3584`; from 1/8 fails |
| tight13 | Valid instant `1/8` | First-band itinerary fails | From 1/8 the same instant; from 2/7 fails |
| strict16 | First-band itinerary fails | `[17/56,39/128]`, width `1/896` | Both first-band itineraries fail |

Six of the sixteen labelled checks supply positive intervals, two supply the same tight equality instant, and eight fail within the declared itinerary. None of these counts is independent evidence for a universal selector.

### What happens in the small-gcd case

At 1/8, speeds 56,64,72 collide and the other four are safe. The last collider to enter safety is 56:

`E=1/448`.

The first current safe lap to end is runner 113's:

`X=(7/8-1/8)/113=3/452`.

Thus `X-E=223/50624>0`. Runner 113 leaves enough shared time after the three colliders clear. The proof uses their common timing and the residues; it does not need a large gcd or the special near-doubling residual.

This interval lies outside the old `J=[9/32,3/8]`, so it is a different witness, not an improvement of the original local overlap bound. The second-anchor interval lies inside J and supplies an explicit subinterval there. The old overlap-placement explanation and its restricted family arguments remain prior results.

The 56/112 control also succeeds, although the selected-pair gcd changes from 1 to 56. This confirms that a large gcd is not a necessary ingredient of **this** certificate; it does not make gcd irrelevant to other representations.

### Tightness and the preserved failure

At tight13's anchor 1/8, all seven moving runners are safe. Speed 7 ends safety immediately to the right; speed 1 ends safety immediately to the left. The incompatible directions isolate the valid point. The two labelled checks do not count as two distinct witnesses.

For strict16 at 1/8, speed 16 requires `E=1/128`, while those same unchanged boundary runners force `X=0` in each direction. The first-safe-lap policy fails. At 2/7, speed 7 requires `E=1/56`, while speed 16 first exits at `X=17/896`; the remaining `1/896` is exactly the already-known strict interval. Changing the anchor changes the **joint orientation and timing** while leaving the speeds and global blocking fractions unchanged.

This is a preserved counterexample to inferring global failure from one anchor. It also prevents treating the successful 56/113 condition as a universal explanation.

## 6. Verification and prior-work boundary

The candidate uses residues and rational comparisons only. After the predictions are fixed, a separate threshold-state sweep over one displacement lap per runner reconstructs its first safe component, including singleton components. All 112 individual-band comparisons agree. All valid certificate endpoints and threshold cells are then checked directly: 14 endpoint/event checks and six positive cells. Outputs and exact conflicting entry/exit controllers are in [results.json](../reviews/2026-09-28-common-displacement/results.json).

Reproduce:

```bash
python -S -B reviews/2026-09-28-common-displacement/check.py --check
```

These are independently structured algorithms by one author, not independent human mathematical review.

The ingredients build on [variable-speed witnesses](VARIABLE_SPEED_FAMILY.md), [local endpoint directions](CORE_TRANSFER.md), [adaptive reflected pairs](ADAPTIVE_REFLECTED_PAIR_2026_09_28.md), and [closed safe-lap cells](LAP_LABELLED_CONSTRAINTS.md). Strict16's interval and tight13's equality were already known. The contribution of this increment is the explicit general residue/entry/exit condition, its all-variable sufficient corollary, the matched exact reconstructions, and the preserved failure of the first anchor. No new literature result is claimed.

## 7. What is now open

The entry/exit representation is small and sufficient **once an anchor is given**. It does not prove that the two development anchors, all anchors with denominator at most n, or any other finite prescribed menu must succeed with the first safe laps.

The earlier finite-rational-menu obstruction concerns fixed witness times. Here the time adapts through `E`, so that obstruction does not directly refute the method. Conversely, adaptivity alone does not establish completeness.

The next structural task is to study how the failed entry/exit inequalities at different anchors can coexist under the same speed residues. Ask whether an explicit arithmetic hypothesis rules out all such failures simultaneously, or construct an exact compatible failure showing that later safe laps or a different certificate class are necessary. The first step must audit the existing residue/adaptive-family results; it should not add more fitted anchors merely to rescue each known failure.

The shared-clock cross-window existence milestone remains unresolved. Broad speed searches, all-reference scans and the parked +7/+9 campaign remain outside this increment, and hourly research remains paused.
