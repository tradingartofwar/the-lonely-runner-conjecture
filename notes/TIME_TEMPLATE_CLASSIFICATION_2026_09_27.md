# Two fixed time pairs: exact coverage and the need for adaptation

September 27, 2026 (Pacific research date). Baseline `e7dc510cc157a3d8e8c1ee81cca3922f48270bc1`. The coordinating agent and six workers supplied the classification, separately structured verification, bounded diagnostics, mathematical challenge, prior-coverage review, and writing. This continues [the phase-projection study](PHASE_PROJECTION_2026_09_27.md) and its [two-time certificate](TWO_TIME_CERTIFICATES_2026_09_27.md).

**The two prescribed pairs certify every phase of runner 11 in exactly 117 of 120 residue classes of the variable speed. Their three missed classes expose a limitation of fixed rational test times.** These counts concern one fixed family and one four-time certificate, not a proportion of the Lonely Runner Conjecture. The precise infinite-family implications below are supplied proof candidates; the finite exact classification is independently reproduced.

## Scope and the frozen plan

Consider eight runners with velocities

\[
\{0,1,4,5,6,7,11,V\},\qquad
V\in\mathbb Z_{>0}\setminus\{1,4,5,6,7,11\}.
\]

Reference 0 and threshold 1/8 remain fixed. Only runner 11's initial phase theta may vary. The other runners start at 0. Theta=0 is the original common-start problem; robustness to all theta is a stronger auxiliary question.

The two pairs were chosen in the preceding study:

\[
T_8=\{1/8,7/8\},\qquad
T_{15}=\{7/15,8/15\}.
\]

The [protocol](../reviews/2026-09-27-time-templates/protocol.json), SHA256 `0932c23c6c65dd8faaae4d319770ae0bca583237c0f92fee9c5ae7f8ce474f02`, was frozen before this classification. It permits exact substitutions in all 120 coefficient classes modulo `lcm(8,15)`, followed by diagnostics at the least admissible representative of each missed class, with a cap of six representatives. It permits no additional time-template search, phase grid, or all-reference scan. Templates are not selected from their eventual allowed-time sets.

## 1. Exact performance of each pair

At a prescribed time t, measure the smallest distance from reference 0 among all seven other runners. For a pair, take the larger of the two such distances. Write this best-of-pair value as M(theta;V). It is an absolute distance, not its excess above 1/8.

Integer unchanged speeds have equal distances at t and 1−t. If their common minimum is c, and runner 11's two unshifted phases have circular separation d, the earlier circle inequality gives

\[
\max(\|11t+\theta\|,\|11(1-t)+\theta\|)\ge d/2.
\]

When c<=d/2, at least one time reaches c for every theta. Neither time can exceed c as a full-configuration minimum, because an unchanged runner attains that cap. Thus M is identically c, rather than merely having infimum c.

For the eighth pair, the unchanged fixed speeds `1,4,5,6,7` have distances

\[
(1/8,1/2,3/8,1/4,1/8).
\]

Runner 11's phases are 3/8 and 5/8, separated by 1/4. Including V gives the exact constant

\[
M_8(\theta;V)=\min(1/8,\|V/8\|)
=\begin{cases}0,&8\mid V,\\1/8,&8\nmid V.\end{cases}
\]

For the fifteenth pair, the unchanged fixed distances are

\[
(7/15,2/15,1/3,1/5,4/15).
\]

Runner 11's phases are 2/15 and13/15, separated by 4/15. Consequently

\[
M_{15}(\theta;V)=\min(2/15,\|7V/15\|)
=\begin{cases}
0,&V\equiv0\pmod{15},\\
1/15,&V\equiv2,13\pmod{15},\\
2/15,&\text{otherwise}.
\end{cases}
\]

Both formulas hold pointwise for every theta. The winning time can change with theta; the best distance within each pair does not.

## 2. Combining the pairs

The best value among all four prescribed times is `max(M8,M15)`. Therefore:

| Template | Exact condition for a valid time at every phase | Strongest distance guaranteed by that template |
| --- | --- | --- |
| T8 | V is not divisible by 8 | Exactly 1/8; this pair cannot be strict |
| T15 | V modulo 15 is outside `{0,2,13}` | Exactly 2/15, with strict excess 1/120 |
| Union of the four times | V modulo120 is outside `{0,32,88}` | 2/15 where T15 succeeds; otherwise 1/8 |

The full coefficient-class accounting is:

| Prescribed choices | Strict classes | Threshold-only performance | Failed classes |
| --- | ---: | ---: | ---: |
| T8 | 0 | 105 | 15 |
| T15 | 96 | 0 | 24 |
| All four times | 96 | 21 | 3 |

Both pairs succeed in 84 classes; only T8 succeeds in21; only T15 succeeds in12. These are classes of fixed-time coefficients, not 120 new complete speed searches. Excluding the six forbidden individual V values preserves distinct runners; it does not remove those residue classes, which have larger admissible members.

For the three missed classes, every one of the four times fails at every theta, because the unchanged variable runner is already too close. The four-time best values are 0 on class0 and1/15 on classes32 and88. This is a concrete failure of the prescribed choices, not merely an inability to prove that they work uniformly.

The period120 governs evaluations at these rational times. It does not imply that complete allowed-time sets, phase projections, actual durations, or phase robustness repeat when V increases by120. We make no minimal-period claim.

## 3. A distance guarantee and a duration guarantee differ

On every class certified by T15, one prescribed time gives every distance at least2/15, an excess of1/120. Since each distance changes at most its speed times the time displacement, a closed neighborhood of radius

\[
\frac1{120\max(V,11)}
\]

is safe. Its interior is strict, giving

\[
D_V(\theta)\ge\frac1{60\max(V,11)}
\]

for this phase family whenever T15 succeeds. This is a sufficient compact bound, not the exact duration.

The separate [challenge review](../reviews/2026-09-27-time-templates/challenge.md) sharpens it. Put `dV=||7V/15||`, `R=min(1/480,(dV−1/8)/V)`, and `rho=1/1320`. The unchanged runners are safe in radius R around either candidate; at the winning center runner11 has guaranteed radius rho. Its safe lap has width3/44>2R, so it cannot truncate both sides of the unchanged-safe interval. Hence

\[
D_V(\theta)\ge R+\min(R,\rho).
\]

This recovers1/352 for V=16. The guaranteed time widths can shrink as V increases, even though the certificate's distance excess remains1/120. A constant separation margin does not imply a constant neighborhood in time when speeds vary without bound.

The21 threshold-only classes describe the performance of these four choices. They do not assert that those complete configurations are tight. Other times can be strictly valid.

## 4. Bounded diagnosis of the missed classes

The protocol selects the least positive admissible V from each failed residue class, in residue order:120,32,88. The classification fixes these diagnostic inputs before any complete safe-time reconstruction.

For each representative, let A be the complete unchanged-safe time set, P its image under `11t mod1`, and B the closure of its positive-length phase support. The primary diagnostic intersects closed safe laps. The independent method partitions at threshold events and checks phase preimages directly, without reading or importing the primary implementation. Every field, endpoint flag, gap, witness, and case digest agrees.

| V | Shortest containing arc c(P)=c(B) | Positive duration at every11 phase? | Common-start duration | Direct common-start strict witness |
| ---: | ---: | --- | ---: | ---: |
| 120 | 183/224 | Yes | 53/3360 | 821/2688 |
| 32 | 1387/1792 | Yes | 9/896 | 1097/3584 |
| 88 | 183/224 | Yes | 37/2464 | 437/1408 |

All three have P=B and `c(B)>1/4`. The supplied covering-arc criterion therefore gives positive duration for every runner11 phase. The common-start witnesses, selected by the protocol's longest-component midpoint rule, independently satisfy every original inequality strictly; they alone would prove only the theta=0 conclusions.

Thus these are genuine failures of the four-time certificate despite robust configurations. The existing two-time completeness argument says some suitable strict pair exists for each representative. This diagnostic did not search for such pairs and does not provide a new arithmetic selection rule.

The archives retain all38 positive components of the three unchanged-safe sets and all14 positive common-start components. There are no isolated components in these particular diagnostics. Equality handling was nevertheless retained by both methods. These conclusions concern V=120,32,88 only, not every integer in the corresponding classes.

## 5. Prior coverage and the obstruction to fixed rational menus

The original common-start family was already covered by a supplied argument in [VARIABLE_SPEED_FAMILY.md](VARIABLE_SPEED_FAMILY.md). Its explicit witness rule is

\[
t(V)=\begin{cases}
1/8,&8\nmid V,\\
17/56,&8\mid V\text{ and }56\nmid V,\\
17/56+1/(8V),&56\mid V.
\end{cases}
\]

The [core-exchange argument](CORE_EXCHANGE_NEIGHBORS_2026_09_27.md) also supplies strict common-start duration for every admissible V>=29. Every member of each of our three failed classes lies in that tail. Thus their common-start success is already covered for the entire classes; the new classification concerns the fixed certificate's stronger one-runner phase robustness.

The earlier variable-speed note also preserves an exact limitation: any finite fixed list of rational times is defeated by a sufficiently large integer multiple of all their reduced denominators. At that speed the variable runner collides with reference0 at every listed time. Choose a sufficiently large multiple to preserve distinctness from the fixed speeds.

For the present list the common denominator is120, giving the first failed class directly. Adding more fixed rational choices cannot remove this obstruction for every admissible integer V. This statement concerns finite rational lists independent of V; it is not a claim about arbitrary irrational choices or times allowed to depend on V.

The useful next direction is therefore an arithmetic rule that moves its candidate times with V. The old common-start witness already has that form. Extending such a rule to two unchanged-safe times with sufficient runner11 phase separation would address the stronger robustness question. The two-time completeness argument guarantees that a suitable pair exists when robustness holds; it does not construct a speed-based rule.

A concrete next candidate is the existing t(V) together with its reflection `1−t(V)`. The next protocol should test their runner11 separation `||22t(V)||>=1/4`, in addition to the unchanged safety already supplied by the old witness. Common-start feasibility by itself does not establish that separation. Threshold witnesses must remain distinct from strict ones; the old formula often lands on equality. This proposed adaptive-pair test is not part of this round's verified results and adds no new time search here.

## 6. Verification and limits

The primary classification uses substitutions and the circle triangle inequality. Its verifier constructs the clipped distance functions directly as affine pieces in theta, inserts every kink, cap crossing, and envelope crossing, and checks all resulting cells and endpoints. It neither reads nor imports the primary implementation.

All120 classification rows and their canonical digest agree. The independent calculation covers240 pair envelopes and120 four-time envelopes, with3,982 open algebraic cells and4,342 event-point evaluations. All envelopes are constant. Separate closed-safe-arc checks retain threshold equality, and exact integrality of120 times each prescribed time proves the sufficient period.

The classification archive has SHA256 `80684a9da574a5676e4d5b7c8f05812432bac56d2991813f3ced992173d6f652`. The [classification schema](../reviews/2026-09-27-time-templates/schema.md), [diagnostic schema](../reviews/2026-09-27-time-templates/diagnostics_schema.md), [challenge review](../reviews/2026-09-27-time-templates/challenge.md), and [coverage review](../reviews/2026-09-27-time-templates/coverage.md) state assumptions and exact scope.

The diagnostic archive has SHA256 `cb9f66ebcf533c92a213e4cf2165fe0f80e231c877b35b427ae9c68881b8e15a`. Its separate reconstruction checks1,290 open time cells,1,296 time vertices, and71 phase cells with their71 event points. Those counts overlap logically and are not independent proof replications. The [manifest](../reviews/2026-09-27-time-templates/manifest.json) pins all files and dependencies. All four executable checks use Python's standard library and passed in read-only mode.

Read-only reproduction commands are:

```bash
python -B reviews/2026-09-27-time-templates/classify.py --check
python -B reviews/2026-09-27-time-templates/verify_classification.py --check
python -B reviews/2026-09-27-time-templates/diagnose.py --check
python -B reviews/2026-09-27-time-templates/verify_diagnostics.py --check
```

The finite classifications and diagnostics are OBSERVED/REPRODUCED within their declared scope. General deductions remain HYPOTHESIS/proof candidates under [CLAIM_STATUS.md](../CLAIM_STATUS.md). Separate AI derivations and code implementations are not independent human proof certification. No novelty, arbitrary-speed Lonely Runner proof, or new original common-start family coverage is claimed.

The [small-gcd priority](SMALL_GCD_DISTINCTION_REVIEW_2026_09_27.md) remains related through the shared question of arithmetic certificate selection. The56/113 setting and this variable-V family have different fixed cores and constraints; their sufficient conditions must not be transferred silently. The +7/+9 extension and broad speed searches remain parked.
