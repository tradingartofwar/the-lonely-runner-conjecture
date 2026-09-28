# What the lap inventory forgets

September 27, 2026 Pacific research date; written September 28 UTC. Scope: the two speed lists and the 29 speed-11 offsets in `protocol.json`, SHA256 `f1d4772133a47a3090c5f9f5f3aa6389b378917c0744a80e3df728790e397d7d`. Materially AI-assisted. The formulas below are direct derivations; no additional literature search, speed configuration, or phase search was performed for this note. General deductions are supplied proof candidates under `CLAIM_STATUS.md`.

**The missing information is the alignment of each runner's pattern with the others at the same lap and within-lap time.** A common phase shift merely moves along the same trajectory. Shifting runner 11 alone changes a relative phase constant while preserving each runner's separate inventory. This is a physically realizable shifted-start comparison, not a counterexample to the common-start Lonely Runner conjecture.

## The exact coupled representation

Let `V=13` or `16`, `I=[1/8,7/8]`, and write a fastest-safe time as

\[
t=(m+u)/V,\qquad m\in\mathbb Z/V\mathbb Z,\quad u\in I.
\]

For a residual speed v put `r_v(m)=v*m mod V`. Its circle phase is

\[
x_v(m,u)=\frac{r_v(m)+vu}{V}\pmod1.
\]

Its normalized strict blocker is therefore exactly

\[
K_v(m)=\{u\in I:\ |r_v(m)+vu-Vq|<V/8
                         \text{ for some integer }q\}.
\]

Since the fastest-lap width is no greater than the safe gap of any residual runner, `K_v(m)` is an interval or empty. Its endpoints and inclusion flags retain what its length alone discards.

The complete lap residue vector is

\[
r(m)=m(1,4,5,6,7,11)\pmod V.
\]

This is an injective cyclic orbit because speed 1 records m itself. In particular,

\[
r_v(m)-v\,r_1(m)\equiv0\pmod V
\]

for every residual label. These congruences completely characterize this orbit: they are more information than six separate multisets of residues. For a single v, its inventory visits the multiples of `gcd(v,V)`, each with that multiplicity. That marginal fact does not say which patterns occur together.

Moving runner 11's pattern from `m+s` into lap m changes the joint residue vector to

\[
r^{(s)}(m)=r(m)+11s\,e_{11}\pmod V.
\]

Thus `r_11-11*r_1` becomes the constant `11s mod V`; every other displayed congruence remains zero. Since 11 is coprime to both V values, the offsets enumerate V different relative phase constants. They are V different translates of the original orbit, not V permutations of the same joint records.

In continuous phase notation the original relation is `x_v(t)=v*t mod1`. After the shift, `x_11(t)=11*t+theta mod1`, where `theta=11s/V mod1`. Consequently

\[
x_{11}-x_4-x_7\equiv x_{11}-x_5-x_6\equiv\theta\pmod1.
\]

The velocity identities `11=4+7=5+6` persist. Their **phase-relation constants** change. This is the concrete role of a torus translation here; a general analogy to independent coordinates would erase the constraint we need to examine.

## What the frozen shifts preserve

| Quantity | Shift runner 11 alone | Shift every residual by the same lap offset |
| --- | --- | --- |
| Each runner's multiset of complete normalized interval patterns, including endpoints | Preserved | Preserved |
| Each runner's total blocking duration restricted to fastest safety | Preserved | Preserved |
| Joint patterns of the five unchanged residual runners | Preserved | Reindexed together |
| Runner-11/fastest joint time statistics over the full period | Preserved | Preserved |
| Joint patterns or pair durations involving 11 and another residual | Not guaranteed preserved | Reindexed together |
| Total allowed duration and isolated-contact count | Not guaranteed preserved | Preserved |
| Common-clock residue relations with zero affine constants | Changed for 11 unless s=0 | Preserved |

For the all-runner control, replacing m by `m+s mod V` is time translation `t -> t+s/V mod1`; fastest safety is invariant under that translation. Therefore full lap records are permuted. This proves the required invariance without assuming stochastic independence.

An arbitrary independent permutation of each inventory need not be a consistent fixed-velocity phase model. The protocol avoids that problem: cyclic shifts correspond to the explicit physical phase above.

## The duration profile is a cyclic cross-correlation

Define `F_m(u)` to be the safe indicator for residual speeds 1,4,5,6,7, and `H_m(u)` to be the safe indicator for speed 11, on fastest lap m. Their values include equality endpoints. For offset s the global allowed duration is

\[
D(s)=\frac1V\sum_{m=0}^{V-1}\int_I
                 F_m(u)H_{m+s}(u)\,du.
\]

Thus each runner's inventory can remain unchanged while D changes: it is the *relative cyclic arrangement* of H against the joint five-runner pattern F that is measured. Averaging over every permitted offset gives the exact identity

\[
\frac1V\sum_{s=0}^{V-1}D(s)
 =\frac1{V^2}\int_I
       \left(\sum_mF_m(u)\right)
       \left(\sum_jH_j(u)\right)\,du.
\]

The average loses the nonconstant cyclic correlations. It is not evidence that the runners are independent, and it does not privilege s=0. Even the pointwise inventories in this formula are finer than merely recording each runner's total blocked duration.

There is an additional exact control. Reflecting time sends `t -> 1-t`, `m -> V-1-m`, and `u -> 1-u`. It changes phase `+11s/V` to `-11s/V` while leaving the unshifted constraints unchanged. Hence the complete allowed sets satisfy

\[
A_s=\{1-t:t\in A_{-s}\},
\qquad D(s)=D(V-s).
\]

The number of isolated contacts also agrees. The equality is a set identity, not a conclusion drawn from the duration formula. The singleton `t=0,1` period-boundary issue cannot create a discrepancy here because the unshifted speed-1 runner blocks both endpoints.

## Local chains and cross-lap coverage are different questions

On each lap the interval scan detects coverage, gaps, and surviving touches. Its advancing right endpoint must be checked with endpoint inclusion: two strict blockers can touch while leaving their common boundary safe, or another blocker can cover that boundary. Exact Hunter-tree duration counts the length of the gaps, but cannot distinguish complete coverage from isolated contacts when that length is zero.

At a fixed u define the finite cyclic residue set

\[
C_v(u)=\{m\in\mathbb Z/V\mathbb Z:\ u\in K_v(m)\}.
\]

Runner 11's shift replaces `C_11(u)` by `C_11(u)-s`. Complete blocking of all fastest-safe times means that these residue sets cover all m **for every u**, including the finitely many boundary values where strict membership changes. Positive duration requires an uncovered m on a positive-length interval of u. This is a precise finite covering formulation. The sets generally comprise residue ranges pulled back by multiplication by v, not single congruence classes; no covering-congruence theorem is being invoked.

A qualitative ordering/containment summary can omit the distance from one right endpoint to the next left endpoint and the fate of a pairwise contact. A third blocker can cover a pairwise contact; a genuine interior touch in the complete sorted-union envelope already accounts for all earlier blockers and survives in this interval setting. The frozen grouping in `results.json` finds four status-collision groups: two compare covered versus contact-only laps, and two compare covered versus positive-duration laps. These comparisons have different fastest speeds and windows; the declared summary does not retain their exact window geometry. By contrast, the permitted phase shifts test loss from a different summary: even the **full separate per-runner inventory** omits which runner-11 pattern is paired with a given five-runner pattern.

## The two unshifted controls

An exact call to the existing rational checker reproduced the six fixed residual runners' safe set:

\[
\{1/8,3/8,5/8,7/8\}
\ \cup\ [17/56,5/16]\ \cup\ [41/88,15/32]
\ \cup\ [17/32,47/88]\ \cup\ [11/16,39/56].
\]

Its positive duration is `29/1232`. Intersecting it with fastest safety gives:

| Fastest speed | Complete unshifted allowed set | Positive duration |
| --- | --- | ---: |
| 13 | `{1/8,3/8,5/8,7/8}` | 0 |
| 16 | `[17/56,39/128] union [41/88,15/32] union [17/32,47/88] union [89/128,39/56]` | `39/4928` |

This is a bounded reproduction, not an independent proof of the checker. Command: `python -B` importing `feasible_intervals` from `lonely_runner.checker`, with threshold `Fraction(1,8)` and respectively `(1,4,5,6,7,11)`, `(1,4,5,6,7,11,13)`, `(1,4,5,6,7,11,16)`.

The fastest runner's different treatment of the same residual-safe set is already an alignment effect. For 16, all four odd-eighth contacts collide with the fastest runner; some positive residual intervals survive instead. For 13, those contacts survive while every positive residual interval is removed.

## What the frozen shifted outcomes establish

`phase_results.json` records these original and earliest changed arrangements:

| V | Offset s | Runner-11 phase | Global status | Duration | Isolated contacts |
| ---: | ---: | ---: | --- | ---: | ---: |
| 13 | 0 | 0 | Contacts only | 0 | 4 |
| 13 | 1 | `11/13` | Positive duration | `1517/48048` | 3 |
| 16 | 0 | 0 | Positive duration | `39/4928` | 0 |
| 16 | 1 | `11/16` | Positive duration | `193/2688` | 0 |

In both cases s=1 is the earliest offset changing duration, local existence, and local three-way status. Every nonzero V=13 offset has positive duration. Every V=16 offset has positive duration and no isolated contacts. All per-runner inventory checks and all common-shift permutation controls pass in the archive. An additional read-only check in this review reflected every rational interval in each recorded allowed set and compared it with offset `-s`: all 29 complete-set comparisons passed.

These are actual counterexamples to determining duration from separate inventories, and the V=13 pair also separates contact-only from positive-duration behavior with identical inventories. **All 29 global allowed sets are nonempty.** Thus this experiment does not exhibit an empty-versus-nonempty collision of global inventories. It should not be described as proving that this summary fails to decide global existence on these two controls.

## A concrete use of the common-start alignment

At the contacts `t=3/8` and `5/8`, the congruences `13=5 mod8` and `11=-5 mod8` put runners 5 and 13 on the same threshold side and runner 11 on the opposite side when its initial phase is zero. Their allowed sides meet at a point. Changing only runner 11's phase changes that opposition while preserving the underlying velocity relations.

The separately reviewed supplied arguments in [PHASE_ROBUSTNESS_2026_09_27.md](../../notes/PHASE_ROBUSTNESS_2026_09_27.md) make this observation quantitative, for these fixed speed lists and with only runner 11's phase allowed to vary:

\[
D_{13}(\theta)\ge
\min\{\|\theta\|,1/4\}/11\quad(\theta\not\equiv0\pmod1),
\qquad D_{16}(\theta)\ge1/176\quad\text{for every }\theta.
\]

For V=13, a left neighborhood of `3/8` or its reflected right neighborhood of `5/8` survives; their combined phase images give the stronger displayed bound, compared with the earlier one-sided bound `min(1/48,||theta||/11)`. The common-start phase is uniquely contact-only in this one-parameter family. For V=16, two fixed safe intervals have runner-11 phase images whose union has length `5/16`, exceeding its strict blocked arc's length `1/4`; a positive amount must survive every translation. These are direct restricted-family arguments, not extrapolations from the 29 offsets. Their status remains **supplied proof candidates**; they imply no general common-start LRC result or novelty claim.

This also explains the experiment's negative existence result. Nonemptiness here has additional geometric protection. Matching inventories neither supplies that protection nor removes it; the decisive statements use aligned interval locations, their images under the runner-11 phase map, and strict endpoint behavior.
