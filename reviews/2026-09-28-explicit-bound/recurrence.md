# Effective recurrence and an independent audit of the convolution bound

September 28, 2026. Pinned live baseline supplied by the coordinator:
`99a4e77a369ff0dd520138605b0339deb263ae39`.

**Status: HYPOTHESIS / proof candidates pending independent mathematical
review.** This is an AI-assisted analytic review. No speed, phase, word, or
parameter scan was performed. The convolution idea was supplied by the
coordinator and geometry agent; this note independently checks its analytic,
endpoint, and occurrence-count steps. No novelty assertion is made.

## 1. The quantitative recurrence deduction, and its limit

Normalize the largest period to one, and suppose all four periods lie in
`[1/4,1]`. Write `b_i(t)` for the indicator of the open blocked train of
period `p_i` and width `p_i/4`, and put `M=sum_i b_i`.
The inherited continuous periodic primitive has the form

`H(t)=sum_i p_i h(t/p_i+alpha_i)`,

where `h` is periodic, has Lipschitz constant `3/4`, and satisfies
`H'=M-1` almost everywhere. For any positive integers `L,Q`, the elementary
simultaneous pigeonhole argument applied to `L/p_i` gives an integer
`1<=n<=Q^4` such that

`||n L/p_i|| <= 1/Q` for every `i`.

Consequently `q=n L` lies in `[L,L Q^4]` and

`|H(q)-H(0)| <= (3/(4Q)) sum_i p_i <= 3/Q`.

If the entire interval from zero to `L Q^4` is openly covered, then `H` is
nondecreasing there. It follows that

`integral_[0,L] (M-1) <= 3/Q`.

Thus a sufficiently long open cover has arbitrarily small excess on a
specified initial horizon, with an explicit bound. This deduction alone
does **not** exclude an open cover: positive overlaps can be arbitrarily
small near an exact tiling, and safe equality contacts must not be erased.
A separate quantitative rigidity argument would be needed to complete this
route. Work on such a bridge was stopped once the coordinator supplied the
stronger convolution argument below.

## 2. Finite-support convolution gives an explicit span bound

This argument permits arbitrary positive real periods and arbitrary phase
shifts; comparability is unnecessary. Define

`f(t)=M(t)-1=sum_(i=1)^4 (b_i(t)-1/4)`

and let

`u_i(t)=1_[0,p_i](t)/p_i`,

`K=u_1*u_2*u_3*u_4`,

`S=p_1+p_2+p_3+p_4`.

Convolution means `(f*K)(x)=integral f(x-y) K(y) dy`. Since every train has
duty exactly `1/4`, averaging `b_i-1/4` over any interval of length `p_i`
gives zero. Hence

`(b_i-1/4)*u_i=0` identically.

All functions involved are bounded or integrable with compact support, so
Fubini justifies reassociation with the remaining averaging kernels.
Linearity therefore gives the exact identity

`f*K=0` identically.                                             (1)

The kernel is nonnegative, supported on `[0,S]`, and strictly positive at
every point of `(0,S)`. For the last assertion, convolution of two
nonnegative interval densities is positive on the interior of the sum of
their supports; induction gives the statement for four factors. Equivalently,
for `0<y<S`, the interior point with coordinates `y p_i/S` belongs to the
slice whose coordinate sum is `y`, and a neighborhood within that slice has
positive three-dimensional measure. In particular `K` is a genuine density,
not just a distribution concentrated at a few times.

Let the union of a finite strict increasing-right-endpoint selected chain be
`U=(A,B)`. Successive selected intervals overlap, so this union is one open
interval. If the chain has only one occurrence then its span is `p_i/4<S`.
Otherwise choose a point `z` in a positive-length overlap of two successive
selected intervals. Then `z` lies in `U`, `f>=0` everywhere on `U`, and
`f>=1` on a nonempty open neighborhood of `z`.

Suppose for contradiction that `B-A>=S`. There is a real `c` such that

`[c,c+S] subseteq [A,B]` and `c<z<c+S`.

Indeed one can select `c` from
`[A,B-S] intersect (z-S,z)`, which is nonempty, including when `B-A=S`.
Apply (1) at `x=c+S`. The integrand

`f(c+S-y) K(y)`

is nonnegative almost everywhere on `[0,S]` and strictly positive on an
open subinterval of `(0,S)`. Its integral is positive, contradicting (1).
Thus

**Every finite strict selected chain has union span strictly less than**

`S=sum_i p_i`.                                                  (2)

Endpoint audit: the kernel endpoints have measure zero, so no assumption
about coverage at `A` or `B` is used. Strictness is supplied by an actual
positive-length overlap in the selected chain. Exact touching tiles give
no such overlap and are not a counterexample to the proof. Neither a weak
limit, a positive minimum overlap, nor a Diophantine recurrence bound is
needed.

## 3. Independent occurrence-count audit: at most 39

Put `P=max_i p_i`, and call any one label with period `P` the largest-period
label. Selected right endpoints belonging to that label are distinct and
separated by at least `P`; skipped occurrences only enlarge the separation.
By (2), all selected endpoints lie in an interval of span less than
`S<=4P`. Five occurrences of this label would have first-to-last endpoint
separation at least `4P`. Therefore its selected occurrence count is at
most four.

For completeness, the inherited bound of seven for three labels has the
following direct strict-chain proof. In a two-label chain, take the
larger-period label. Two of its occurrences would require a single
occurrence of the other label to bridge its safe gap of length at least
three quarters of its period. The other interval's width is at most one
quarter of that period. This is impossible. There is at most one occurrence
of the larger-period label, and at most one other-label occurrence on
either side. Thus every two-label chain has at most three occurrences.

Now let a three-label chain use periods `P_1>=P_2>=P_3`. Between two
successive selected occurrences of the largest-period label there would
be a nonempty two-label chain. Such a chain contains at most one
`P_2`-occurrence and at most two `P_3`-occurrences, so its union span is at
most

`P_2/4+P_3/2 <= 3 P_1/4`.

To bridge the two `P_1` occurrences, however, its first left endpoint must
precede the first `P_1` right endpoint, and its last right endpoint must
follow the next `P_1` left endpoint. Its span would therefore be strictly
greater than the intervening safe gap, which is at least `3P_1/4`.
This is impossible. Hence there is at most one largest-period occurrence,
with two-label chains of length at most three on either side, giving seven.
This argument also handles tied periods and skipped train occurrences.

Finally, if `N_P` is the number of selected occurrences of the chosen
largest-period label in a four-label chain, deleting them partitions the
remaining moving word into at most `N_P+1` contiguous three-label chains.
Each has length at most seven. Therefore

`N <= N_P+7(N_P+1) = 8N_P+7 <= 39`.                            (3)

The count concerns selected occurrences, equivalently advancing calls in
the projection-chain interpretation; stationary calls are not counted.
The deduction does not require irredundancy, equal period ratios, integer
speeds, or common starting phases. It does not address the full
eight-runner core-window existence question.

The central pending review targets are the exact convolution identity and
its conversion to (2), followed by the inherited three-label decomposition.
All three steps have an explicit argument above; no numerical experiment is
being presented as their proof.
