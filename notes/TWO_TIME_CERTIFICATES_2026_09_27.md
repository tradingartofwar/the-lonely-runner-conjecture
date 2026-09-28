# Two fixed times can certify every phase of one runner

September 27, 2026 (Pacific). Baseline `0d67b3077af417f8b3e365b18bb2a6cb92b76189`. A supplied argument from the [phase-projection study](PHASE_PROJECTION_2026_09_27.md), with material AI derivation, separate internal review, and exact finite checks.

**Outcome:** in `{0,1,4,5,6,7,11,16}`, one of the two times **7/15 or 8/15** has every distance from reference 0 at least **2/15**, for every starting phase of runner 11. This is strictly greater than the eight-runner threshold 1/8. It requires checking two times and one phase separation; it does not require constructing the full joint safe set.

For `{0,1,4,5,6,7,11,13}`, the analogous pair **1/8 and 7/8** guarantees at least 1/8 for every phase of runner 11. Those two times always have unchanged runners at equality, so that pair does not certify strictness.

**Status:** HYPOTHESIS / proof candidates with independently checked exact constants and internal mathematical review. No novelty, general Lonely Runner proof, or globally optimal choice of times is claimed. Only runner 11's starting phase varies; phase zero is the original common-start problem.

## The two-time lemma

Fix two times t1,t2. Suppose every runner other than a selected runner has distance at least c from the reference at **both** times. Let the selected runner's unshifted phases at the two times be a,b, and let their circular separation be `d=||a-b||` in `[0,1/2]`.

For every phase shift theta, the circle triangle inequality gives

\[
\|a+\theta\|+\|b+\theta\|\ge\|a-b\|=d.
\]

At least one of the selected runner's two distances is therefore at least d/2. At that time every runner is separated from the reference by at least

\[
q=\min(c,d/2).
\]

If q is at least 1/n, this is a valid lonely instant. If q is greater than 1/n, it is strict. The argument checks the unchanged constraints at both times because the winning time can depend on theta. A good unchanged margin at only one time would not suffice.

This is a sufficient certificate. It does not claim that every feasible configuration admits such a pair, or that a pair failing this test implies no valid time exists elsewhere. The certificate can be tested by finitely many exact inequalities without reconstructing the complete safe set.

## The speed-16 certificate

Use `t1=7/15` and `t2=8/15=1-t1`. Integer unchanged speeds give equal circular distances at these reflected times:

| Unchanged speed | Distance at either time |
| ---: | ---: |
| 1 | 7/15 |
| 4 | 2/15 |
| 5 | 1/3 |
| 6 | 1/5 |
| 7 | 4/15 |
| 16 | 7/15 |

Thus c=2/15. Runner 11 has phases `2/15` and `13/15`, with circular separation d=4/15. The lemma yields q=2/15 for every theta, exceeding 1/8 by 1/120.

There is an exact further statement about this specific certificate. Speed 4 has distance exactly 2/15 at both chosen times, so the best full-configuration minimum among these two times can never exceed 2/15. The lemma reaches that ceiling for every theta. Therefore the **best-of-these-two-times margin is identically 2/15**, even though the total available duration changes with theta. This is not the maximum margin over all possible times.

The same substitutions give a positive-duration certificate without constructing the full safe set. Circular distance for speed v is v-Lipschitz in time. At the chosen winning time, runner 11 has excess margin at least 1/120, giving safe radius at least `1/(120*11)=1/1320`. For every unchanged runner, its directly computed excess margin divided by its speed is at least 1/480. Hence the closed interval of radius 1/1320 around the winning time is safe, and its interior is strict. Both candidate times are far from 0 and 1, so this interval stays in the observation period. Consequently

\[
D_{16}(\theta)\ge1/660
\]

from the two-time certificate alone. This is a deliberately compact lower bound. The preceding [phase-image argument](PHASE_ROBUSTNESS_2026_09_27.md) gives the larger bound 1/176, and the full projection study determines the exact minimum. These answer different quantitative questions with different amounts of information.

## The speed-13 certificate and its limit

Use `t1=1/8` and `t2=7/8`. The unchanged speeds `1,4,5,6,7,13` have distances

\[
(1/8,1/2,3/8,1/4,1/8,3/8)
\]

at both times, so c=1/8. Runner 11's phases are 3/8 and 5/8, separated by d=1/4. The lemma gives q=1/8 for every phase.

Speeds 1 and 7 are exactly at threshold at both times, and their safety directions oppose. Thus these are isolated valid times whenever runner 11 permits them. The best-of-two margin is identically 1/8; no phase produces a strict witness within this fixed pair.

This does not contradict the supplied result that every nonzero phase of runner 11 creates a positive interval elsewhere. A certificate can remain at equality while the actual configuration becomes strict. Its reported margin is a guaranteed achievement by that certificate, not a complete description of the configuration.

## Completeness for one-runner phase robustness

The initial argument showed sufficiency. Subsequent general review supplies a stronger, carefully scoped statement: **at threshold 1/8, some two-time certificate exists if and only if the configuration remains feasible for every phase of the selected runner.** The two times need not be a preselected pair or reflections of one another.

Let A be the unchanged runners' compact safe-time set, P its image under the selected runner's phase map, and c(P) its minimum containing closed circular-arc length. Nonemptiness for every selected-runner phase is equivalent to `c(P)>=2delta`: complete blocking requires P to fit inside an open arc of length `2delta`.

For any nonempty compact circle set P and `0<a<=1/3`,

\[
c(P)\ge a\quad\Longleftrightarrow\quad
\text{some }x,y\in P\text{ have }\|x-y\|\ge a.
\]

Here is the endpoint-sensitive proof. If every pair has distance less than a, rotate one point to zero. The compact set then has unique lifts in `(-a,a)`. Let L and R be the extreme lifts and w=R-L. We have `w<2a<=1-a`. If w were at least a, the extreme pair's distance `min(w,1-w)` would also be at least a, a contradiction. Thus all of P fits in an arc of length w<a. Conversely, a pair separated by at least a cannot fit inside a closed arc shorter than a. Compactness ensures the extreme lifts exist.

Apply this with `a=2delta=1/4` and lift the two phase points back to two times in A. Every unchanged runner is safe at both times, and the selected phases are separated by at least 1/4. The two-time lemma then supplies the required certificate. This is a statement about **existence of a pair**, not a procedure that finds it from the speeds without further reasoning.

There is also a strict version for `0<2delta<1/3`, including our threshold. In the finite, nonzero-speed setting, let B be the closure of the images of positive-length unchanged-safe intervals. Positive duration at every phase is equivalent to `c(B)>2delta`. If all pair distances were at most `a<1/3`, the same lift argument gives `w<=2a<1-a`, hence `w<=a` and `c(B)<=a`. Therefore `c(B)>a` supplies two phase points separated by more than a. Approximate their preimages by interior times of positive-length safe intervals, avoiding the finitely many unchanged-runner equality times. Separation remains greater than a, while every unchanged runner now has distance strictly greater than delta at both times. Their minimum unchanged margin c satisfies c>delta, and the pair lemma gives `min(c,d/2)>delta` uniformly in phase. The converse follows directly from that lemma and continuity in time.

The non-strict statement permits `2delta=1/3`; the strict argument here requires `2delta<1/3`. Empty A or B is handled separately and cannot supply the corresponding robustness. These supplied implications have separate internal mathematical reviews in [challenge.md](../reviews/2026-09-27-phase-projection/challenge.md) and [arithmetic.md](../reviews/2026-09-27-phase-projection/arithmetic.md). They remain proof candidates; the exact finite checkers do not constitute a formal proof of this general geometry.

## The general obstacle left open

The pair lemma turns useful relational information into a small witness set: both times jointly satisfy the unchanged constraints, and the selected runner cannot be too close at both because its two positions are separated.

What remains unproved generally is that arbitrary required configurations admit the necessary joint safety and phase spread. The completeness argument shows that two times suffice whenever this stronger, all-phase property holds at our threshold; it does not establish that the property must hold. Original common-start Lonely Runner asks only for the prescribed phase, so requiring robustness to every phase is an additional burden. A proof strategy must not silently replace the original objective with that stronger statement.

The present pair choices were motivated by symmetry and exact arithmetic, then checked. They were not obtained through an exhaustive time-pair search and are not asserted globally optimal. A useful next test is to derive the exact arithmetic conditions under which these two fixed templates transfer across the existing one-parameter speed family, retaining the residue classes they fail to certify rather than calling them failures of loneliness.

Exact constants, finite phase verification, and review are preserved in [certificates.md](../reviews/2026-09-27-phase-projection/certificates.md), [arithmetic.md](../reviews/2026-09-27-phase-projection/arithmetic.md), and [challenge.md](../reviews/2026-09-27-phase-projection/challenge.md). The main study records all reproduction commands and dependencies.
