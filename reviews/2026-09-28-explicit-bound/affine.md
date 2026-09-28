# Affine review: a positive averaging certificate replaces finite feasibility

September 28, 2026. Pinned live baseline:
`99a4e77a369ff0dd520138605b0339deb263ae39`.

**Status: HYPOTHESIS / proof candidate, pending external review.** This note
is materially AI-derived. The convolution argument was proposed by the
geometry agent and independently checked here. The finite rational checks
below are bounded calibration, not external proof certification or evidence
of novelty. Arbitrary phases and positive real periods are auxiliary scope;
common-start integer runners are included as a special case.

## 1. Explicit conclusion

For four trains

\[
I_{i,m}=(s_i+m p_i,s_i+(m+1/4)p_i),\qquad p_i>0,
\]

every strictly overlapping, increasing-right-endpoint selected chain has
at most **39 occurrences**. This is independent of all periods and phases,
including periods outside the comparable interval `[1/4,1]`. Stationary
projection calls are not selected occurrences.

The analytic span bound is stronger than the counting statement:

\[
\left|\bigcup_{j=1}^{N} I_{i_j,m_j}\right|
< S,\qquad S=\sum_{i=1}^{4}p_i. \tag{1}
\]

The union here is connected because each selected right endpoint lies
strictly inside the next selected interval. Containment is allowed;
irreducibility of a cover is not assumed.

## 2. The positive averaging certificate

Let `b_i(t)` be the indicator of the open blocked train of label i, and put

\[
g_i(t)=b_i(t)-1/4,\qquad
f(t)=\sum_i g_i(t)=M(t)-1.
\]

Each `g_i` is bounded, `p_i`-periodic and has integral zero over every
interval of length `p_i`. Define the nonnegative averaging kernels

\[
B_i(u)=p_i^{-1}\mathbf 1_{[0,p_i]}(u),\qquad
K=B_1*B_2*B_3*B_4.
\]

Endpoint conventions in the kernels do not change their integrals. Direct
integration gives `g_i*B_i=0` at every real argument. Compact support of the
kernels and boundedness of the functions justify Fubini and associativity,
even though the periodic functions need not be integrable on the full line.
Thus

\[
f*K=\sum_i(g_i*B_i)*\mathop{*}_{j\ne i}B_j=0. \tag{2}
\]

The kernel is supported on `[0,S]` and is strictly positive on `(0,S)`.
One direct positivity check: for `u` in that open interval the point
`u_i=u p_i/S` has every coordinate strictly between 0 and `p_i` and has
coordinate sum u. A small neighborhood in three coordinates still places
the fourth coordinate strictly inside its interval, giving positive volume
in the convolution integral.

Let the selected union be `(L,R)`. On this union `M>=1`, hence `f>=0`.
If `N>=2`, any selected handoff supplies an open interval on which two
selected trains overlap; there `f>=1`. Suppose `R-L>=S`. One can choose a
length-S window contained in `[L,R]` with some point of that overlap in its
interior. Evaluating (2) at the right endpoint of this window integrates a
nonnegative function against K, with strict positivity on a set of positive
measure. Its integral is positive, contradicting (2). This proves (1) for
`N>=2`. If `N=1`, its width `p_i/4` is already strictly below S.

This is an analytic nonnegative certificate. It needs no phase grid,
occurrence-word enumeration, irrational-return estimate, compactness limit,
or determinant bound. The crucial identity is the total duty `4*(1/4)=1`.

## 3. From span to 39 selected occurrences

Choose a label of maximum period P. Its selected intervals are distinct,
and their right endpoints differ by positive integer multiples of P.
If it occurs q times, the distance from the left endpoint of its earliest
selected interval to the right endpoint of its latest is at least

\[
(q-1)P+P/4.
\]

By (1), this is strictly below `S<=4P`; therefore `q<=4`.

For completeness, the earlier three-label bound is also checked here.
Order three available periods `p_b>=p_c>=p_d`. A chain using only c,d has
at most one c: between consecutive selected c occurrences there can be at
most one d, whose width is insufficient to bridge the c-safe gap. There
are at most three selected intervals in total. Their union length is at
most `(p_c+2p_d)/4`; if there is more than one interval, strict overlaps
make the sum-of-widths bound strict.

Two selected b occurrences in a b,c,d chain would require the intervening
c,d subchain to cover the entire b-safe gap, whose length is at least
`3p_b/4`. Its available union length is strictly insufficient because
`(p_c+2p_d)/4<=3p_b/4`. Hence b appears at most once, with at most three
selected intervals on each side. Every three-label chain has at most seven
occurrences, regardless of skipped laps.

Deleting the q maximum-period labels in a four-label chain leaves at most
`q+1` three-label chains. Therefore

\[
N\leq q+7(q+1)=8q+7\leq39. \tag{3}
\]

The maximum-period label need not actually appear; then `q=0` and the same
argument gives the three-label bound. Strictness is used at the correct
places: a point where intervals merely touch is safe and is not a handoff.
Endpoints have zero measure in (2), but the contradiction comes from an
open positive-overlap region, not from deleting an equality point.

## 4. Exact bounded implementation check

The coordinator approved and froze `protocol.json` before implementation.
It reuses the three prior exact tilings and, for each, only the already
declared `period_first_up` and `start_first_down` perturbations. There are
nine auxiliary fixtures in total, with no new physical configuration.

Protocol SHA-256:

`63d509f00dd73cfc54094030ed942d0e929215213a5e20604305dc4e99192d06`

Primary implementation SHA-256, pinned before execution:

`007934302e57c2cda04d25e247158b3702743d194b8bd57e81e58b2498fe5160`

The primary uses rational inclusion-exclusion formulas for K and its CDF:

\[
K(t)=\frac{1}{6\prod_i p_i}
\sum_{A\subseteq\{1,2,3,4\}}(-1)^{|A|}
(t-\sum_{i\in A}p_i)_+^3,
\]

\[
F_K(t)=\frac{1}{24\prod_i p_i}
\sum_{A\subseteq\{1,2,3,4\}}(-1)^{|A|}
(t-\sum_{i\in A}p_i)_+^4.
\]

For each train, only its finitely many open occurrences intersecting
`(x-S,x)` contribute. Each interval `(L,R)` contributes exactly
`F_K(x-L)-F_K(x-R)` to `(b_i*K)(x)`. The implementation does not use the
known value `1/4` to evaluate these integrals; it asserts equality afterward.

Run from this worktree root:

```bash
python reviews/2026-09-28-explicit-bound/primary.py
```

All declared checks passed, using `fractions.Fraction` throughout:

| Declared check | Count | Result |
| --- | ---: | --- |
| Train integrals at `x=0,1/7,S,S+1/7` | 144 | Exactly `1/4` |
| Four-train total at those arguments | 36 | Exactly `1` |
| Kernel values at `S*j/8`, `j=1,...,7` | 63 | Strictly positive |
| Kernel values at `0,S` | 18 | Exactly zero |

`results.json` records exact values, the compact-support occurrence ranges,
and both hashes. These samples calibrate the finite formulas and boundary
handling. The analytic proof above, rather than the samples, is the proposed
reason the bound applies to all positive real periods and all shifts.

The challenge agent separately implemented rational piecewise-polynomial
integration and successive box-convolution antiderivative differences,
without importing the primary code or using its alternating-subset formula.
The declared comparison also passed:

```bash
python reviews/2026-09-28-explicit-bound/challenge_verify.py
python reviews/2026-09-28-explicit-bound/compare.py
```

`comparison.json` records **459 exact numerical comparisons**: 36 periods,
36 starts, nine support lengths, 36 convolution arguments, 144 train
integrals, 36 totals, 81 kernel arguments, and 81 kernel values. Ten metadata
comparisons are recorded separately (nine normalized fixture identifiers
and the shared protocol hash). The comparison artifact includes SHA-256
hashes for the protocol, both implementations, the comparison script, and
both input result files. The primary result file was not modified during
comparison. Agreement remains an internal computational check, not external
review of the general proof.

## 5. Superseded finite-affine route and remaining status

Before the positive-kernel deduction, this assignment investigated a finite
affine feasibility route: use an exact endpoint-order polyhedral cover,
quantify a positive minimum excess away from the explicit tiling
neighborhoods, and combine a rational determinant bound with a simultaneous
phase-return estimate. No feasibility enumeration or LP was executed, and
no global numerical constant was obtained from that route. The direct
certificate (2) makes that machinery unnecessary for this goal.

The proposed 39 bound concerns advancing occurrences, not scalar no-op
calls, arithmetic bit complexity, or the number of complete physical
configurations solved. No assertion that 39 is sharp is made. Prior known
shifted-threshold existence remains credited in the main research record;
novelty of this deduction is not established. The full eight-runner
core/window existence question remains open.
