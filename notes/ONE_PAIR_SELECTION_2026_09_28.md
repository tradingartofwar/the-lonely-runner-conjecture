# One overlap query: useful selection and a preserved failure

September 27, 2026 Pacific / September 28 UTC. Baseline `539dd899ac8ceea5b50d46b72c0fa28cec7a354e`. This continues the [small-gcd distinction review](SMALL_GCD_DISTINCTION_REVIEW_2026_09_27.md), after the [adaptive reflected-pair result](ADAPTIVE_REFLECTED_PAIR_2026_09_28.md).

**Outcome:** a frozen policy using four individual blocking durations and at most one pair-overlap query certifies the first three existing controls. One prescribed endpoint rescues the next two, once as an isolated contact and once as a positive interval. The sixth control defeats the policy, and the campaign stops there without changing the rule. The failure separates choosing a pair poorly from asking a single-pair certificate to do something no pair can do on the selected window.

**Status:** OBSERVED/REPRODUCED for the exact frozen diagnostics. General algebraic implications remain HYPOTHESIS/proof candidates, with material AI derivation, implementation, and internal review. No independent human certification, novelty, arbitrary-speed existence guarantee, or empirical runtime speedup is claimed. These are design-informed known controls, not held-out validation.

## What was actually missing from the previous work

The repository already evaluated all pairs and trees over complete core windows in [CORE_TRANSFER.md](CORE_TRANSFER.md). It also already has bounded-operation selection rules for special families in [SPARSE_OVERLAP_SELECTION.md](SPARSE_OVERLAP_SELECTION.md) and [TWO_SPEED_SPARSE_TRANSFER.md](TWO_SPEED_SPARSE_TRANSFER.md). Repeating those searches would not supply a new selection mechanism.

The narrower question here is whether **individual concentration can guide one overlap query**, after a window has been selected without consulting the residual schedules. The policy receives a prescribed three-speed core. It selects a window, not the core itself. It cannot read the full seven-runner allowed set or the six pair overlaps before deciding which pair to query.

All cases have eight common-start runners, stationary reference 0, distinct positive integer nonreference speeds, threshold δ=1/8, and original unit time period. There is no arbitrary starting phase in this round.

## Frozen rule and information budget

The [protocol](../reviews/2026-09-28-one-pair-selector/protocol.json), SHA256 `36ef24405de801a114e11325d30fe0b5f2d855e71441e5c4478047aa15b82d8e`, predates the new computations. It declares the six inputs, their order, tie rules, endpoint fallback, and stopping condition.

1. Construct the supplied core's complete closed allowed set. Choose its widest positive-length component J=[α,β], taking the earliest component on a tie. Retain and count singleton components, although this rule does not select one.
2. Compute only the four individual residual blocking durations D_i on J. Put L=β−α and E=ΣD_i−L.
3. Rank pairs by decreasing `min(D_i,D_j)`, with numerical speed-pair order breaking ties. This number is an **upper cap** on overlap, not an estimate or lower bound.
4. If E<0, singles already certify positive duration. If the largest cap is at most E, skip the pair query because no one-pair bound can be positive. Otherwise evaluate exactly the first ranked pair's overlap O and test O−E>0.
5. If no positive duration certificate resulted, test only β against all seven speeds. At a valid endpoint, intersect its seven containing safe laps to retain a positive interval or an isolated contact. If β is invalid, return uncertified and stop the campaign. Never change the pair, window, or endpoint after a failure.

Core discovery and overlap evaluation have their own costs. “One pair query” is an information budget, not a constant-time complexity claim. The algorithm constructs no full seven-runner allowed set. The later benchmarks read existing archives and do not feed selection.

## A useful impossibility test before querying any pair

For any measurable blockers inside the selected J,

\[
O_{ij}\le\min(D_i,D_j),\qquad
C=\max_{i<j}\min(D_i,D_j).
\]

C is the second-largest individual duration. Therefore

\[
\max_{i<j}(O_{ij}-E)\le C-E.
\]

If C≤E, **every one-pair duration certificate fails on this window**, regardless of how intelligently the pair is chosen. This does not imply no opening exists. It establishes a limit of this certificate form from information already available before querying an overlap.

Conversely, C>E is only available capacity. For the selected pair the exact score is

\[
O-E=(C-E)-(C-O).
\]

The first term can be positive while the second consumes more than all of it. Two runners blocking a large amount individually need not block together sufficiently often. The timing relationship is still consequential.

The cap is sharp for abstract measurable events with only these four individual durations prescribed: nested sets of those sizes attain every pair cap. This does not assert that the nested arrangement is realizable by common-start runners. Additional speed geometry can constrain it.

## Exact outcomes

The selected window for core {1,4,5} is J=[9/32,3/8]. For core {1,3,5}, it is [17/40,23/40]. For core {1,2,4}, it is [9/32,7/16]. These follow from the core alone, before evaluating residual concentration.

| Supplied core | Four residual speeds | Selected pair | Pair-stage result | Final policy outcome |
| --- | --- | --- | --- | --- |
| 1,4,5 | 56,64,72,113 | 56,113 | O−E=1223/911232>0 | Positive duration certified |
| 1,3,5 | 56,64,72,113 | 56,72 | O−E=2169/202496>0 | Positive duration certified |
| 1,4,5 | 56,64,72,112 | 56,64 | O−E=59/16128>0 | Positive duration certified |
| 1,4,5 | 6,7,11,13 | 6,11 | O−E=−421/32032 | Endpoint 3/8 is valid and isolated |
| 1,2,4 | 3,5,6,8 | 3,5 ranked first; no query | C−E=0 rules out all positive one-pair bounds | Endpoint gives [17/40,7/16], length1/80 |
| 1,4,5 | 6,7,11,16 | 6,11 | O−E=−171/9856 | Endpoint 3/8 fails; policy stops uncertified |

The two endpoint successes are separate certificate paths. They do not turn the failed or skipped pair stages into successful pair bounds. A skipped overlap is unqueried, not zero. None of these six selected windows has E<0, so the singles-only early exit is not exercised by this batch.

This batch does **not** exhibit a window where the selected pair fails but another pair succeeds. The first three selected pairs succeed; in the last three windows every one-pair bound fails. Consequently the test refutes completeness of the overall frozen policy, but does not decide whether its cap ranking always finds a successful pair whenever one exists on its chosen window. The known controls are too limited to establish that stronger selection claim.

### The changed-core case selects a different relationship

For core {1,3,5}, the selected window admits no positive overlap of 56 and113: the earlier near-doubling phase gate is zero throughout it. But the four actual individual durations rank 56 and72 first. Their overlap is 23/2016, exceeding E=1271/1822464. The policy therefore succeeds without querying the original preferred pair or learning all six overlaps.

This is a useful bounded transfer. It does not establish that the largest individual caps generally identify the useful pair, or that the widest core opening generally provides one.

### The one-pair ceiling is detected without measuring overlaps

For core {1,2,4} with residuals3,5,6,8, the durations are

\[
(D_3,D_5,D_6,D_8)=(1/12,1/20,1/24,1/32),
\quad E=C=1/20.
\]

Hence the cap test rules out every positive one-pair bound before any overlap query. The old archive gives a stronger post-selection comparison: the best actual pair has O=1/24 and bound −1/120, while a tree gives exact duration11/480. The frozen endpoint fallback instead finds the smaller interval [17/40,7/16] directly. It neither computes that tree nor reconstructs the entire allowed set.

### The final failure is not repaired by choosing another pair

For the speed-16 control, the selected pair6,11 overlaps for1/528 and E=569/29568. Their negative difference is −171/9856. At β=3/8, speed16 is at integer position6, so the only permitted endpoint fallback fails.

The old exact records nevertheless contain the interval [17/56,39/128], of length1/896. They also show that no single pair gives a positive bound on J; even the best tree gives −23/29568. Thus choosing another pair cannot repair the prescribed-window one-pair policy. Its failure is local: other windows and stronger certificates were already successful in the earlier work.

The [September25 review](ULTRA_REVIEW_2026_09_25.md) supplies an even sharper limit. An abstract complete-cover arrangement has the same four individual durations and all six pair totals as this physical example. Consequently a generic inequality using only those totals cannot force the actual positive opening. That arrangement is not another runner realization. The real speed geometry excludes the triple6,11,16 on J; retaining that extra information makes the all-pair inclusion-exclusion calculation exact. These are prior findings reused to diagnose the frozen failure, not new full-set reconstructions.

## Exact overlap from a short arithmetic description

After choosing a<b, the evaluator chooses h∈{1,2} minimizing `(abs(b−ha),h)` and sets r=b−ha. This choice only controls how the one selected overlap is evaluated. It does not rank candidate pairs or impose a small-residual cutoff.

Write x=at−j. Joint blocking is equivalent, away from measure-zero boundaries, to

\[
-\delta<x<\delta,
\qquad m-\delta<hx+rt<m+\delta
\]

for the relevant integer m. Thus the allowed x-range is bounded by

\[
\ell(t)=\max(-\delta,(m-\delta-rt)/h),\qquad
u(t)=\min(\delta,(m+\delta-rt)/h).
\]

Split J at the finitely many points rt=m±(h+1)δ and rt=m±(h−1)δ. On each positive strip, these endpoints are affine. With the old periodic primitive

\[
P(z)=\tfrac12\{z\}(\{z\}-1),\qquad
W(f;A,B)=\frac{P((a-s)B-d)-P((a-s)A-d)}{a-s},
\quad f(t)=st+d,
\]

the exact overlap is

\[
O=\sum_{[A,B]}\left[\int_A^B(u-\ell)\,dt
+W(u;A,B)-W(\ell;A,B)\right].
\]

Both endpoint frequencies are positive: they are a or a+r/h=b/h, including when r<0. The r=0 case uses a constant strip. This extends the previously used endpoint calculation directly to the signed h=1,2 descriptions needed by the frozen policy; no novelty is asserted.

The queried pair6,11 exercises negative residual r=−1. The input containing112 selects56,64, so no selected query in this batch exercises r=0. That branch has an algebraic derivation and code review, not a new finite diagnostic here.

The number of strip candidates is O(1+|r||J|). This can avoid enumerating all fast meetings when |r| is small, but it is not uniformly bounded for arbitrary pairs. The exact correction retains alignment that phase area alone discards. The independent verifier checks the chosen overlaps by direct interval intersections instead.

## Reproduction and interpretation

The [schema](../reviews/2026-09-28-one-pair-selector/schema.md), [primary records](../reviews/2026-09-28-one-pair-selector/results.json), [independent verification](../reviews/2026-09-28-one-pair-selector/verification.json), and [post-selection benchmarks](../reviews/2026-09-28-one-pair-selector/benchmarks.json) preserve all stages and their sources. The [manifest](../reviews/2026-09-28-one-pair-selector/manifest.json) records commands, exact counts, hashes, dependencies, and limits.

```bash
python -B reviews/2026-09-28-one-pair-selector/select.py --check
python -B reviews/2026-09-28-one-pair-selector/verify.py --check
```

Both read-only checks pass. Independent reconstruction matches all six semantic records and digests, evaluation certificates, and cost counters:35 core components,24 individual durations,five selected overlaps,ten positive strip contributions,and three prescribed endpoints. The primary constructs56 core safe laps and performs71 interval-intersection comparisons; it evaluates48 single-duration primitive endpoints and40 overlap-primitive endpoints. The changed-core overlap alone uses24 of the40 overlap-primitive calls, while each other query uses four. These totals include repeated core construction without caching. Thus even within this small batch, equal query counts do not mean equal evaluation work.

The first uncertified case is the sixth and last prescribed input, so the stopping rule is enforced but produces no early-stop savings here. Source archives for the later comparisons are pinned separately; they are not generator or independent-verifier inputs. Primary result SHA256: `07de386d85fbd27cfbba45ce53f4006a7d2ac9c08249d2050b616ed598faf2ba`. Independent verification SHA256: `e969ffc28e3ccd554595789c8686faeb845ceca31adfc9822f0ab9c20c46f9a5`.

Internal reviews are preserved in [arithmetic](../reviews/2026-09-28-one-pair-selector/arithmetic.md), [structure and cost](../reviews/2026-09-28-one-pair-selector/structure.md), [challenge](../reviews/2026-09-28-one-pair-selector/challenge.md), and [prior coverage](../reviews/2026-09-28-one-pair-selector/coverage.md). Their agreement is not independent human proof certification.

The useful conclusion is not a success percentage. It is a separation of three questions: whether a single-pair certificate could possibly succeed, whether the chosen pair actually supplies enough overlap, and whether another certificate type can explain the opening. The cap test answers the first negatively in one control; actual overlap is still needed for the second; the final control requires information or a window beyond the frozen policy.

**Next proposed:** use the retained speed-16 failure to formulate a decision about which additional information to request. With an explicitly larger input contract, such as supplied all-pair totals, identify a speed-derived fact that rules out every compatible abstract complete-cover arrangement, not merely one displayed countermodel. The existing strict16,112,and tight controls respectively require a justified exclusion, respect for higher intersections that really occur, and an equality route. The known triple-exclusion and alternative-window repairs are comparison targets, not discoveries to repeat. State the selection condition and discovery cost before adding cases or fitting another score. The broader small-gcd objective remains a general selection condition. No new speed search or +7/+9 extension is proposed.
