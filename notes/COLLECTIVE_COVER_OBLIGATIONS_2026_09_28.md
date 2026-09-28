# Collective burden can hide behind zero individual minima

September 28, 2026 UTC. Baseline `e94a3a84ba39a8227941d3e5aa2d1d63df149e37`, draft PR #3. Material AI involvement: a coordinating agent and three complementary agents supplied calculation, separately structured verification, and adversarial/prior-coverage review. This is internal AI work, not independent human mathematical validation.

**Question.** Can pair-compatible complete coverage require positive higher-order overlap even though every individual triple can be absent in some compatible complete cover?

**Outcome.** Yes, for an explicitly abstract four-event model. The distinction is the order of quantifiers:

\[
\text{for every triple }K\text{ there exists a cover with }T_K=0,
\]

but

\[
\text{there is no cover with the full higher-order correction }H=0.
\]

The same total, single and pair moments admit both complete-cover arrangements and an arrangement with uncovered mass `1/7). Thus individual cover-constrained minima lose a genuinely collective obligation.

**Status.** The exact finite model and certificates are OBSERVED/REPRODUCED in the frozen scope. The elementary identities are supplied proof candidates for review. This is not a common-start runner realization, a new Lonely Runner family, an existence result, a novelty claim, or a general certificate selector.

## 1. Frozen abstract contract

The [protocol](../reviews/2026-09-28-collective-obligations/protocol.json), SHA256 `0f9ca99436288f53989732f4d642992a80e2c7433ec3a8ec897dd52a981d6425`, was saved before calculation. There are four abstract blocking events and sixteen exact-state masses `x_S >= 0`. Retained inputs are only

\[
L=\sum_Sx_S,qquad
D_i=\sum_{S\ni i}x_S,qquad
O_{ij}=\sum_{S\supseteq\{i,j\}}x_S.
\]

Write

\[
U=x_\varnothing,qquad
T_{ijk}=\sum_{S\supseteq\{i,j,k\}}x_S,qquad
Q=x_{1234}.
\]

The proposed collective correction is

\[
H=\sum_{i<j<k}T_{ijk}-Q.
\]

Ordinary inclusion–exclusion gives the exact identity

\[
\boxed{U+H=C},qquad
C=L-\sum_iD_i+\sum_{i<j}O_{ij}.
\]

The subtraction of `Q` matters: the raw triple sum counts a four-way state four times, while the correction required by inclusion–exclusion counts it three times.

The frozen rule first minimizes `U` from total/single/pair moments. If that minimum is zero, it enters the cover face `U=0`, minimizes each `T_ijk` separately, and also minimizes `H`. No rule is changed after seeing an answer.

## 2. Symmetric paired model

The main retained moments are

\[
L=1,qquad D_i=\frac37,qquad O_{ij}=\frac17
\]

for every label and pair. Hence `C=1/7`.

Let `q=x_1234`, and let `y_K` be the exact-state mass on the four states having exactly three active events. Möbius inversion reduces the full feasible pair-moment polytope to

\[
u+\sum_K y_K+3q=\frac17,
\qquad u=U,\qquad u,y_K,q\ge0.
\]

All remaining exact pair and singleton masses are then determined and nonnegative. On the cover face `u=0`,

\[
H=\sum_Ky_K+3q=\frac17.
\]

The inclusive triple indexed by `K` is `T_K=y_K+q`. For each one, choose `q=0`, put all `1/7` of exact-three mass into a *different* triple, and obtain `T_K=0`. Therefore

\[
\min_{U=0}T_K=0\quad\text{for all four }K,
\qquad
\min_{U=0}H=\frac17.
\]

Equivalently,

\[
\sum_K\min_{U=0}T_K=0
\quad\text{but}\quad
\min_{U=0}\left(\sum_KT_K-Q\right)=\frac17.
\]

This is the precise compression failure. The separate optimizers are different covers. Combining their four zero values silently treats them as though one cover attained all four zeros simultaneously.

### No proper subset of triple types is compulsory

With `q=0`, the cover face contains the entire simplex

\[
y_K\ge0,qquad \sum_Ky_K=\frac17.
\]

For any proper subset of the four triple types, put all mass on an omitted type. Every queried member of the subset then vanishes. Consequently no summary-only policy that merely asks whether a fixed proper subset of triples must occur can expose this cover burden. The symmetric pair summaries contain no preferred label.

This is an information-budget statement about the abstract model. A physical speed configuration may supply asymmetry or arithmetic structure not present in these summaries.

## 3. Explicit paired countermodels

The algebra is accompanied by exact nonnegative arrangements.

**Open arrangement.** Put mass `1/7` on the empty state and on each of the six exact pair states. All other masses are zero. It has the prescribed `L,D_i,O_ij`, with

\[
U=\frac17,qquad H=0.
\]

**Covered arrangements.** Choose any one exact triple state and put mass `1/7` on it. Put mass `1/7` on each of the three exact pairs joining the omitted label to the triple, and on each singleton belonging to the triple. These seven masses sum to one and reproduce the same retained moments. They have

\[
U=0,qquad H=\frac17.
\]

Cycling the chosen exact triple gives four covers. Each is a witness that the other three inclusive triples can vanish; together they show why no individual triple is compulsory.

These are abstract measurable event distributions. They are not claimed to come from runner speeds, common starts, or intervals on a shared clock.

## 4. Frozen controls

### Zero-burden partition

Set `L=1`, `D_i=1/4`, and every pair moment to zero. Pair zeros forbid every higher state. Complete coverage is uniquely realized by four singleton masses `1/4`, so

\[
U=H=T_{ijk}=Q=0.
\]

The collective rule correctly produces no positive obligation.

### Four-way correction

Put `x_1234=1/4` and each singleton mass equal to `3/16`. Then

\[
D_i=\frac7{16},qquad O_{ij}=\frac14,qquad C=\frac34.
\]

Each inclusive triple has duration `1/4`, giving raw sum `1`, while

\[
Q=\frac14,qquad H=1-\frac14=\frac34=C.
\]

This rejects replacing `H` by the uncorrected triple sum.

## 5. What the result means—and its sharp limit

The previous [cover-obligation selector](COVER_OBLIGATION_SELECTION_2026_09_28.md) asks for one triple when every compatible cover must use that triple. The symmetric model proves that this rule can end with four zero individual minima even though every compatible cover carries positive higher-order burden.

The natural repair is a collective query. But in this four-event representation,

\[
H=C-U
\]

is exactly the inclusion–exclusion deficit. Proving `H<C` is algebraically equivalent to proving `U>0`. The abstract result therefore identifies missing information; it does **not** yet make that information cheap to obtain from speeds. Evaluating four triple intersections and `Q` exactly may approach reconstruction of the quantity being sought.

Pointwise, `H` is also the cycle rank of the complete graph induced by the active blockers: it is zero for zero, one or two active events; one for three; and three for four. This connects the collective correction to the already-recorded graph-cycle accounting in [FOUR_BLOCKER_CYCLE_CORRECTIONS.md](FOUR_BLOCKER_CYCLE_CORRECTIONS.md). It is a reformulation and diagnostic extension, not a newly claimed graph inequality.

The useful negative conclusion is narrower:

> Pair summaries can make higher-order burden compulsory without making any named triple compulsory. A selector limited to separate mandatory-triple tests is incomplete, even in a four-event abstract model.

## 6. Reproduction and verification

Artifacts are under [reviews/2026-09-28-collective-obligations/](../reviews/2026-09-28-collective-obligations/). The primary calculation records exact rational primal/dual certificates. The independent verifier uses direct Möbius reconstruction and logical-state evaluation rather than importing primary functions. The adversarial review checks quantifiers, prior coverage, and the tautology/cost limit.

Both standard-library-only readback commands pass:

```bash
python -S -B reviews/2026-09-28-collective-obligations/primary.py --check
python -S -B reviews/2026-09-28-collective-obligations/verify.py --check
```

The primary replay checks 19 exact rational primal/dual certificates on sixteen logical states: three pair-baseline minima, twelve cover-constrained individual-triple minima, three cover-constrained collective minima, and the main `H<=0` repair. Each archived primal is nonnegative and satisfies its exact moments and side constraints; every dual satisfies all sixteen column inequalities; the objectives agree exactly.

The independent verifier imports no primary functions and uses no optimizer. It derives the complete Möbius parameterization

\[
x_i=\sum_{j\ne i}y_j+2q,\qquad
x_{ij}=u+y_i+y_j+2q,\qquad
u+\sum_i y_i+3q=\frac17,
\]

then checks every archived certificate, the open model, all four concentrated covers, the unique zero-burden cover, and the quadruple correction. The [adversarial review](../reviews/2026-09-28-collective-obligations/challenge.md) separately audits the quantifiers, the identity's tautological role, the cost claim, prior graph accounting, and the draft's scope. The manifest records artifact hashes and the exact limits. AI agreement is not independent mathematical certification.

## 7. Next bounded question

Return to already archived runner windows, not a new speed search. Freeze the existing finite list of local positive windows missed by tree certificates, and test whether any has:

1. pair-only minimum `U=0`;
2. zero cover-constrained minimum for every individual triple;
3. actual positive lonely duration.

Such a window would be a runner-realizable counterpart of the collective-only obstruction. If none exists in the frozen archive, preserve that negative result. Do not enlarge the domain, infer all-reference coverage, restart the parked `+7/+9` work, or treat the abstract construction itself as physical evidence.
