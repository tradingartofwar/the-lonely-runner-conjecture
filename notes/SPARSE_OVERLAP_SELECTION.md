# Two arithmetic checks select a useful overlap graph

September 25, 2026. Baseline `c1cc625a2ee77d6a85da17dffb427c1ac2024e77`.

**Question:** Can we retain enough occurrence information to choose a useful overlap graph without reconstructing every lap of a variable-speed runner?

**Outcome:** yes for the fixed family `{0,1,4,5,6,7,11,w}`. Two tests for whether a triple can occur, combined with single/pair durations, select a graph that certifies positive clear duration in the fixed window J for every admissible positive integer w except 3,10,13,26. Those four retain valid equality times. The rule uses a bounded number of rational arithmetic operations regardless of w; integer bit costs still grow.

**Scope and status:** all runners start together; eight total runners; stationary selected reference 0; integer `w>0`, distinct from `{1,4,5,6,7,11}`; threshold `1/8`. Finite checks are OBSERVED/REPRODUCED results. The written tail and family synthesis are an AI-assisted proof candidate awaiting independent review. No novelty or general Lonely Runner proof is claimed.

Existence for this exact family was already covered more simply in [VARIABLE_SPEED_FAMILY.md](VARIABLE_SPEED_FAMILY.md). The contribution here is a compact overlap-certificate selection rule and a local duration classification. It does not add an uncovered family to our results. The elementary duration-discrepancy bound was already used in [TWO_VARIABLE_SPEEDS.md](TWO_VARIABLE_SPEEDS.md); its reuse is explicit below.

## 1. The information to retain

Keep the previously selected window `J=[9/32,3/8]`, where speeds 1,4,5 are safe. Within J the strictly blocked sets for 6,7,11 have the following interval endpoint values:

| Runner | Blocking interval endpoints in J |
| --- | --- |
| 6 | `(5/16,17/48)` |
| 7 | `[9/32,17/56)` |
| 11 | `[9/32,25/88)` and `(31/88,3/8)` |

The bracket choices follow strict blocking at threshold; duration ignores isolated endpoints. Runners 6 and 7 never block together in J. Their only overlaps with runner 11 are

$$P=(31/88,17/48),\quad |P|=1/528;\qquad
Q=[9/32,25/88),\quad |Q|=1/352.$$

Therefore only two triple types can occur among the four extra runners: `{6,11,w}` and `{7,11,w}`. Four-way blocking is impossible.

For any positive-length interval with endpoint values a,b, runner w has a positive-duration blocking intersection with it exactly when an integer m satisfies

$$wa-1/8<m<wb+1/8.$$

Equivalently,

$$\lfloor wa-1/8\rfloor+1<wb+1/8.$$

Apply this once to P and once to Q. The two yes/no answers determine which triangle cycles must be broken in an overlap graph. This is occurrence compatibility expressed without enumerating the fast runner's laps. A failed strict inequality allows no positive triple duration; possible endpoint contacts remain outside the duration calculation.

## 2. Choose the graph from those two answers

The possible positive pair edges are

`(6,11), (7,11), (6,w), (7,w), (11,w)`.

Enumerate their at most 32 subsets. If the P-test says the first triple can occur, forbid graphs containing all three of its edges. Do the corresponding test for Q. No other cycle restriction is needed: any four-vertex cycle would require both 6 and 7 active, which is impossible, and any other triangle contains that disjoint pair.

Choose the admissible graph G with the greatest sum of pair-overlap durations. Every induced active graph is then a forest almost everywhere. The previously recorded graph inequality gives

$$U_J\ge |J|-D_6-D_7-D_{11}-D_w+\sum_{ij\in G}O_{ij}.$$

This uses the existing elementary forest counting argument from [LR2_REVIEW_PRIORITIES.md](LR2_REVIEW_PRIORITIES.md), with established graph-sieve context in S18. The general graph inequality is not new.

| w | Triple 6,11,w possible? | Triple 7,11,w possible? | Selected edges | Clear lower bound |
| --- | --- | --- | --- | ---: |
| 13 | No | No | 6–11, 7–11, 6–13, 7–13 | 0 |
| 14 | Yes | Yes | 6–14, 7–14, 11–14 | 1/112 |
| 15 | No | No | 6–11, 7–11, 6–15 | 1/112 |
| 16 | No | No | 6–11, 7–11, 6–16, 11–16 | 1/896 |
| 17 | Yes | No | 7–11, 6–17, 7–17, 11–17 | 1/112 |

These five bounds equal the actual durations. At w=14 the best ordinary runner tree already suffices. At w=17 the best ordinary tree gives `15/2464>0`, but retaining the impossible 7/11/17 triangle recovers the full `1/112`. At w=16 an ordinary tree still gives the negative bound `-23/29568`; the additional triple-exclusion information is essential for this runner-level graph certificate.

Thus the previous w=14/17 failures were failures of the **fixed chosen triangle-with-leaf graph**, not failures of every runner-level graph. The earlier note correctly left other graphs unsearched; this continuation closes that limited question.

## 3. Obtain the durations without listing fast laps

Define, for real x,

$$A(x)=\frac14\lfloor x+1/8\rfloor+
\min\bigl(\{x+1/8\},1/4\bigr).$$

Its derivative away from the finitely many boundary points per period is the indicator of `||x||<1/8`. Thus the blocked duration of speed w on an interval `[a,b]` is exactly

$$D_w([a,b])=\frac{A(wb)-A(wa)}w.$$

Evaluate this on J and on the four fixed blocking intervals above. This supplies D_w and the three variable pair overlaps. The other two pair overlaps are the fixed lengths of P and Q. There are five interval evaluations, two integer-existence tests, and at most 32 graph masks; none grows in number with w. The verification script separately reconstructs finite schedules to test the formula, but the certificate generator does not use those schedules.

## 4. Why only finitely many speeds need checking

The star with centre w and leaves 6,7,11 is always admissible. Let

$$S=D_6+D_7+D_{11}=331/3696.$$

For any interval I,

$$\left|D_w(I)-\frac{|I|}{4}\right|\le\frac{3}{16w}.$$

One direct derivation uses `A(x)-x/4`: its range is `[1/32,7/32]`, of width `3/16`. Taking a difference at the two endpoints gives the displayed estimate. This is the same periodic boundary allowance used in our earlier two-variable note, now applied in both directions.

In the star bound there is one whole-window D_w term and four fixed-interval terms making up its pair overlaps. Using the estimate five times gives

$$\begin{aligned}
U_J&\ge |J|-S-D_w(J)+O_{6w}+O_{7w}+O_{11w}\\
&\ge \frac34(|J|-S)-\frac{15}{16w}
=\frac{31}{9856}-\frac{15}{16w}.
\end{aligned}$$

This is positive whenever `w>9240/31`, hence for every integer `w>=299`. At 299 it is `29/2946944>0`. The selected maximum-weight admissible graph is at least as strong as this star. The unbounded tail therefore rests on an inequality, not on extrapolation from computations.

## 5. Complete finite branch and counterchecks

Check `1<=w<=298`, omitting the six fixed speeds: exactly 292 admissible values. The sparse graph rule gives 288 positive lower bounds. Its four zero results have actual zero duration, with these complete valid sets inside J:

| w | Valid times in J |
| --- | --- |
| 3 | `{3/8}` |
| 10 | `{5/16,3/8}` |
| 13 | `{3/8}` |
| 26 | `{5/16,3/8}` |

Hence every admissible w is certified in this same window, using positive duration or an equality witness. The fixed family, selected reference, and integrality assumptions are essential to this statement.

The sparse bound equals the exact duration in 79 of the 292 finite cases. It remains a lower bound elsewhere. For example, w=28 gives `3/352` against actual `1/112`; w=42 gives `1/672` against actual `1/336`. Thus success on the first five cases does **not** extend to exact duration recovery in general. The smallest positive finite certificate is `1/896`, at w=16.

Reproduce:

```bash
python -B reviews/2026-09-25-lr2/check_sparse_overlap.py --check
```

[Script](../reviews/2026-09-25-lr2/check_sparse_overlap.py) and [exact results](../reviews/2026-09-25-lr2/sparse_overlap.json). Standard-library rational arithmetic; no project imports. The JSON records the script hash, all 292 finite rows, selected graphs, bounds, and equality exceptions. A separately structured direct threshold partition verifies all finite durations, pair integrals, both triple tests, and endpoints. Logical active-state checks verify the selected graph inequality. The formula is also exercised at 299, `10^12`, and `56*10^12`; prior-family witnesses are evaluated directly for those cases, and no complete large-speed schedule is enumerated. The tail proof itself awaits independent mathematical review.

An additional session check used the existing `lonely_runner.checker.feasible_intervals` routine for w=3,10,26,28,42. It agreed on the three additional equality-only cases and the two displayed non-exact lower-bound controls. The previous lap-labelled verifier still passes; its evidence files were not altered.

## 6. What follows from the LTCM experiment

The occurrence representation revealed what the compressed graph omitted. For this fixed family, we can return to the small runner graph and retain only **two additional compatibility answers** beyond its pair totals. Complete lap lists and full triple durations are unnecessary for this successful lower-bound rule.

This is a concrete example of choosing which distinctions a model must carry. It is not a numerical measure of information-theoretic synergy, a physical field, or proof that every speed family admits such a small summary.

**Next useful test:** transfer the selection mechanism to a setting where a second speed varies, without re-proving the already-covered two-variable existence family. Use the known `{16,23}` cooperative-cover example from TWO_VARIABLE_SPEEDS.md as a required failure control for reusing the old small opening. Determine which fixed interval structure and triple checks survive, and when selecting a different window becomes necessary. General core/window selection and bounds with several independently growing speeds remain OPEN.

**Transfer completed:** [TWO_SPEED_SPARSE_TRANSFER.md](TWO_SPEED_SPARSE_TRANSFER.md) retains the two triple tests, implements their lap-lattice constraints, and supplies a prescribed choice between J and the earlier alternate H. The unbounded certificate uses the known fast branch, 27 small-speed tail bounds, four x=3 controls, and 819 reduced finite cases. The original 16/23 pair closes the small I but leaves a positive interval in J; `(3,8m)` genuinely empties J and requires another window. This refines certificates for an already-covered family; it does not add a new family or settle arbitrary-speed selection.
