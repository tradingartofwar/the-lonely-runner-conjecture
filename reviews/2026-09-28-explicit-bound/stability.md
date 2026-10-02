# Quantitative stability route and the stronger convolution shortcut

September 28, 2026. Baseline supplied in `TEAM_BRIEF.md`:
`99a4e77a369ff0dd520138605b0339deb263ae39`.

**Status: HYPOTHESIS / proof candidates, pending external review.** This is
an AI-assisted analytic review. No parameter, word, or speed scan was run;
no executable enumeration is used. The assigned task was to quantify the
compactness-to-critical-tiling step. A period-convolution argument supplied
by the geometry agent supersedes that step and gives the much smaller
candidate bound 39. I independently checked the kernel positivity and
support-placement details below. No novelty claim is made.

## 1. Independent audit of the convolution argument

Let the four open periodic blocked trains have periods `p_i>0`, arbitrary
phases, and interval widths `p_i/4`. Write `b_i` for their indicator
functions, `M=sum_i b_i`, and

\[
g_i=b_i-\tfrac14,\qquad
u_i(s)=p_i^{-1}{\bf1}_{[0,p_i]}(s),\qquad
K=u_1*u_2*u_3*u_4,\qquad S=\sum_i p_i.
\]

The mean-zero, `p_i`-periodic function `g_i` satisfies `u_i*g_i=0` at every
point. Each other kernel is integrable and each `g_i` is bounded, so Fubini
and associativity give

\[
K*(M-1)=\sum_i K*g_i=0. \tag{1}
\]

No common period, integrality, phase alignment, or recurrence estimate is
required.

### Positive interior of the kernel

The support of `K` is contained in `[0,S]`, and `K(s)>0` for every
`0<s<S`. Here is an explicit induction, avoiding any appeal to an informal
picture of a smoothing kernel. Suppose the convolution of the first `j`
boxes is positive on `(0,S_j)`, where `S_j=sum_{i<=j}p_i`. For
`0<s<S_j+p_{j+1}`, the interval

\[
(0,p_{j+1})\cap(s-S_j,s)
\]

is open and nonempty. Its integrand in the convolution formula is
positive, so the convolution is positive. The first box is already
positive in its support interior. Endpoint values of the boxes and of
the blocked indicators do not affect any integral.

### Placement inside a strict chain

The union of a finite strictly overlapping selected chain is an open
interval `U=(A,B)`. On U one has `M>=1`, apart from irrelevant endpoint
conventions; in fact open coverage holds pointwise. If the chain has at
least two occurrences, consecutive occurrences have an open intersection,
so `M-1>=1` on a nonempty open interval `J` contained in U.

Suppose `B-A>=S`. Choose any `t` in J. There is some

\[
x\in[A,B-S]\cap(t-S,t).
\]

To check this directly, if `B-A=S`, use `x=A`; then `A<t<B=A+S`.
If `B-A>S`, the intervals have an intersection because `t>A` and
`t-S<B-S`, and one can avoid either excluded endpoint of `(t-S,t)`.
Thus `[x,x+S]` lies in `[A,B]` and contains t in its interior.

In the convolution `(K*(M-1))(x+S)`, the integrand is nonnegative almost
everywhere. On a sufficiently small open subinterval of J around t, its
factor `K(x+S-y)` is strictly positive and its factor `M(y)-1` is at least
one. The integral is therefore strictly positive, contradicting (1).

A one-occurrence chain cannot have span at least S, because its width is
`p_i/4<S`. Consequently every strict chain satisfies the global bound

\[
\boxed{B-A<\sum_i p_i.} \tag{2}
\]

The proof even handles the equality case `B-A=S`; there is no lost
endpoint margin. Containment of some selected intervals causes no
difficulty because the proof uses the full blocked multiplicity.

### Implication for occurrence count

Let `p_max` be the largest period and let `N_a` count selected occurrences
of that label. Their distinct increasing right endpoints are separated by
at least `p_max`. Since (2) gives `B-A<4p_max`, we get `N_a<=4`.
The inherited three-label chain bound is 7, so deleting those occurrences
leaves at most `N_a+1` pieces, each of length at most 7. Thus

\[
N\le N_a+7(N_a+1)\le39.
\]

The inherited subcritical bound remains a separate premise of this
numerical improvement. The convolution argument itself establishes (2)
directly, including for arbitrary positive periods and arbitrary phases.

## 2. Optional generalization from the same argument

For m active labels, all with duty `1/k`, where `k>=2` and `1<=m<=k`, use the product
of their m period kernels. It annihilates `M-m/k`. On a covered interval,
`M-m/k>=1-m/k`. When `m<k`, this is positive throughout the interval;
when `m=k`, a strict chain supplies the positive-overlap interval used
above. Thus its span is again less than the sum of its active periods.

The largest-period label can occur at most m times. If `B_m` bounds
chains on m labels with this fixed duty and `B_0=0`, deletion gives

\[
B_m\le m+(m+1)B_{m-1},\qquad B_m\le(m+1)!-1.
\]

This supplies a general explicit bound `(k+1)!-1` at duty `1/k`. For
k=4 it gives 119 by itself; the stronger inherited three-label bound gives
39 instead. This is a deduction, not an attribution to the literature.

## 3. Superseded quantitative-stability deductions

The following route was developed before the convolution shortcut arrived.
It is recorded to preserve the actual progress and its scope; it is not
needed for (2) or 39. It avoids extracting proximity to the three complete
phase templates, using an approximate periodic ordering instead.

Normalize `1/4<=p_i<=1`. Suppose an openly covered window `[0,136]`
has excess

\[
E=\int_0^{136}(M-1)\,dt\le\varepsilon=1/2048.
\]

Every pair intersection lying in this window has length at most
epsilon. For periods `p<=q`, take q-starts `z` in `[2,134]`, and reduce
each modulo the phase of the p-train to a coordinate `y` in `[0,p)`.
The prior and next p-occurrences lie wholly in the window. Since
`p/4<=q/4<=p`, the pair-intersection bound forces

\[
\frac p4-\varepsilon\le y\le p-\frac q4+\varepsilon. \tag{3}
\]

For the lower inequality, an earlier y gives intersection with the
current p-block longer than epsilon. For the upper inequality, the
q-block reaches the next p-block by more than epsilon. The hypothesis
`q/4<=p` uses only `q<=1` and `p>=1/4`.

The allowable arc in (3) has length
`A=(3p-q)/4+2epsilon`. If `q<=p+8epsilon`, the periods are already
within `1/256`. Otherwise `A<p/2`. Consecutive reduced q-starts differ
by `q-np` for some integer n. Since `[-A,A]` has length less than p,
there is at most one possible n: every consecutive difference is the
same. There are at least 129 consecutive q-starts in this padded window,
and hence

\[
|q-np|\le\frac A{128}<\frac p{256}\le\frac1{256}.
\]

Nonemptiness of the arc also yields `q<=3p+8epsilon`, so that
`n` belongs to `{1,2,3}`. Pairing every period with
`h=min_i p_i` gives integers `m_i` in `{1,2,3}` with

\[
|p_i-m_i h|\le1/256. \tag{4}
\]

There is also an elementary start-separation bound. If two interior
occurrences have starts `a<b`, pair intersection at most epsilon and
both widths at least `1/16>epsilon` imply

\[
b-a\ge1/16-\varepsilon=127/2048=:d.
\]

Containment is impossible, and the right endpoints occur in the same
order as the starts. Open coverage therefore makes successive interior
starts into a strict increasing-right-endpoint chain.

Set `P=6h` and `r_i=6/m_i`. Advancing a start of label i by r_i
periods defines `F(s)=s+D_i`, with

\[
D_i=r_i p_i,\qquad |D_i-P|\le6/256=3/128=:z,
\qquad 2z<d.
\]

This map preserves the interior start order, since two starts are at
least d apart. It also preserves consecutive adjacency: a start w
strictly between `F(a)` and `F(b)` would have inverse start
`w-D_label(w)` in `(a-2z,b+2z)`. If a,b were consecutive, the
separation bound permits only a or b there, whose images are the
excluded boundary points. This is a contradiction.

Choosing an initial start in `[4,5]` leaves ample padding for two
applications of F because `1.5<=P<=6`. The ordered labels then repeat
one complete block twice, contrary to the inherited square-free-word
lemma. This suggests every openly covered 136-window must have
excess greater than `1/2048`.

Together with the inherited total-excess bound `3/4`, this route would
give span less than `136*1537=209032` and the conservative occurrence
bound `3344520` from `N<=16T+8`. It was not pursued further once the
shorter convolution proof gave the much stronger result. The steps above
are analytic deductions, not a computational certificate or an externally
reviewed stability theorem. In particular they do not establish explicit
phase distance to one of the three named tiling templates; they bypass
that phase-classification target.
