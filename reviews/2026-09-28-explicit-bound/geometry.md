# An explicit geometric bound from period averaging

September 28, 2026. Pinned live baseline:
`99a4e77a369ff0dd520138605b0339deb263ae39`.

**Status: HYPOTHESIS / proof candidate, pending independent review.**
Materially AI-derived by the separately tasked geometry agent. This note is
an analytic derivation, with no parameter scan, word enumeration, new physical
fixture, or claim of novelty. It uses the auxiliary arbitrary-phase model of
four positive-period trains, each with duty `1/4`. It includes the physical
common-start integer-speed case but does not prove the full Lonely Runner
Conjecture or successful existence inside an arbitrary prescribed core window.

**Candidate conclusion:** every strictly overlapping, increasing-right-endpoint
selected chain has at most **39 occurrences**. This applies to all positive
period ratios, so it also supplies an explicit comparable-period bound.
The numerical constant is conservative and is not asserted sharp.

## 1. Definitions

For `i=1,2,3,4`, fix a period `p_i>0` and a shift `s_i`. Let

`I_(i,m)=(s_i+m p_i, s_i+(m+1/4)p_i)`, for integer `m`,

be the open blocked occurrences. Write `B_i` for their union,
`M(t)=sum_i 1_(B_i)(t)`, and `S=sum_i p_i`. The endpoints are safe for their
own train. Since each period is positive, only finitely many occurrences
intersect a bounded interval.

A selected chain is a finite sequence of occurrences `I_1,...,I_N`, with
right endpoints `R_1<...<R_N`, such that `R_j` is strictly inside `I_(j+1)`
for each `j<N`. Consecutive selected intervals have an intersection of
positive length. Their union `U` is an open interval `(L,R_N)`, where
`L=min_j L_j`. In particular, `M>=1` at every point of `U`.

## 2. Exact period averaging

Let `X_i` be independent uniform random variables on `[0,p_i]`, and put
`X=X_1+...+X_4`. For every real `a`,

`E[M(a+X)]=1`.                                                    (1)

Indeed, for each fixed label `i`, condition on all `X_j` with `j!=i`.
Integrating its periodic indicator over the remaining interval of length
`p_i` gives exactly its duty `1/4`, irrespective of the conditioned shift.
Summing the four expectations proves (1). Endpoint values have zero measure.

The distribution of `X` has a density `K` supported on `[0,S]` that is
strictly positive throughout `(0,S)`. This can be seen without an explicit
formula: the convolution of two densities positive on the interiors of
`[0,u]` and `[0,v]` is positive at every `x` in `(0,u+v)`, because
`(0,u)` and `(x-v,x)` overlap in an interval of positive length. Apply that
observation three times. Consequently (1) is equivalent to

`integral_0^S K(x) [M(a+x)-1] dx = 0` for every `a`.               (2)

This is a finite averaging identity. It does not use recurrence,
commensurability, rational periods, compactness, or limiting phases.

## 3. A strict chain spans less than the sum of its periods

**Lemma.** The union length `T=R_N-L` of any selected chain satisfies

`T<S`.                                                          (3)

If `N=1`, this follows from `T=p_i/4<S`. Suppose `N>=2` and, for a
contradiction, `T>=S`. Choose a point `y` in the positive-length intersection
of two consecutive selected occurrences. Thus `y` belongs to `U` and has an
open neighborhood on which `M>=2`.

There is a real `a` for which `(a,a+S)` lies in `U` and contains `y`:
choose `a` in `[L,R_N-S]` and in `(y-S,y)`. These intervals have a common
point because `L<y<R_N` and `R_N-L>=S`. When equality holds, `a=L` works.

On `(a,a+S)`, `M-1>=0`. On a nonempty open subinterval containing `y`,
`M-1>=1`. The density `K(t-a)` is strictly positive in this whole interior,
so the integral in (2) is strictly positive, a contradiction. This also
excludes the equality `T=S`, since neither boundary value enters the integral.

An equivalent formulation is that no open blocked component can contain
a chain whose union reaches length `S`. A large integer-time recurrence
bound or an explicit neighborhood of one of the three critical tilings is
unnecessary for this conclusion.

## 4. Elementary two- and three-label chain bounds

For completeness, the inherited bounds are independently derived here using
only destination widths and strict endpoint increments.

For any consecutive portion of a selected chain, its total endpoint
increment is strictly smaller than the sum of the destination interval
widths. This follows at every transition from

`0<R_(j+1)-R_j<p_(label(j+1))/4`.                                (4)

A chain on one label has at most one occurrence: its different occurrences
are separated by positive gaps.

Now use two labels of periods `p>=q`. If the period-`p` label appeared twice,
take consecutive selected appearances of that label. Between them are only
period-`q` occurrences and hence at most one. The two period-`p` endpoints
differ by at least `p`, while (4) bounds their difference strictly from above by
`(p+q)/4<=p/2`. This is impossible. Thus the period-`p` label occurs at most
once, with at most one period-`q` occurrence on either side. The pair-chain
bound is `3`, and the period-`p` and period-`q` occurrence counts are at most
`1` and `2`, respectively.

Next use three labels of periods `p>=q>=r`. If the period-`p` label appeared
twice, choose consecutive such appearances. Their intervening two-label
subchain contains at most one period-`q` occurrence and at most two
period-`r` occurrences. Their period-`p` endpoint difference is at least `p`;
(4) instead makes it strictly smaller than

`(p+q+2r)/4<=p`,

a contradiction. Therefore the largest-period label occurs at most once,
with pair-only chain pieces on its two sides. Every three-label chain has
at most `1+3+3=7` occurrences. Equal periods are allowed, because the
strict inequality in (4) retains the contradiction.

## 5. The explicit constant 39

Let `p_max=max_i p_i`, choose one label attaining it, and let `N_max` be
its number of selected occurrences. If this label is absent, `N<=7`.
Otherwise its first and last selected right endpoints differ by at least
`(N_max-1)p_max`, since occurrence indices strictly increase. They both lie
between the union's extreme endpoints, giving

`(N_max-1)p_max < T < S <= 4p_max`.

Hence `N_max<=4`. Removing those occurrences partitions the chain into at
most `N_max+1` contiguous subchains on the other three labels. Each has
at most seven occurrences, by Section 4. Thus

`N <= N_max+7(N_max+1) = 8N_max+7 <= 39`.                         (5)

The proof handles omitted labels, repeated equal periods, arbitrary phase
shifts, skipped occurrence indices, nested selected occurrences, and
arbitrarily large period ratios. It never assumes that the selected chain
is an irredundant cover. No stationary scalar call is counted as a chain
occurrence.

For the repeated eleven-call schedule that visits all four labels, every
round beginning at an unsafe time makes at least one advancing call.
Consequently (5) bounds the number of such unsafe-start rounds by 39. With
joint-safety tests initially and at each completed-round boundary, at most
39 rounds or 429 scalar calls suffice; no additional stationary round is
needed. The scheduling deduction is optional; the main result is the bound
on advancing moves, not arithmetic bit complexity or core-window existence.

## 6. Audit targets and limits

The proof uses a fourfold period average, and all four duty fractions
sum exactly to one. The kernel's positivity and the positive-length overlap
are both used. Mere endpoint contact does not create a strict transition;
an exact tiling is compatible with (2) because it has `M=1` almost everywhere.
Thus the proof does not incorrectly exclude the critical equality tilings.

The key review targets are (1), the placement of the length-`S` support
inside the chain union even when `T=S`, and the actual-chain three-label
bound. No quantitative tiling classification or finite scan remains hidden
inside the numerical constant. Independent line-by-line review is still
required. Agreement among AI agents will remain an internal check, not an
external certificate or a novelty determination.
