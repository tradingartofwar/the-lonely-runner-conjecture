# Geometry audit of the shorter mixed averaging kernel

Date: 2026-09-28. Pinned live baseline from `TEAM_BRIEF.md`:
`bcf959b45a35701f2fd710b1d86ca2cc3152e14c`.

**Status: HYPOTHESIS / complete proof candidate.** This is an independent
AI-assisted derivation and endpoint audit within the same research team; it is
not external mathematical review or a novelty claim. The audit found no gap in
the proposed span bound, its 31-move consequence, or the subsequently supplied
23-move refinement under the assumptions below.
No computational experiment, scan, or optimization was performed.

The scoped checkout supplied `AGENTS.md`, `CLAIM_STATUS.md`,
`CONTRIBUTING.md`, and `TEAM_BRIEF.md`, which were read along with the preceding
39-move note at `../lr-explicit-bound/notes/EXPLICIT_CHAIN_BOUND_2026_09_28.md`.
The `README.md` and `HANDOFF.md` requested by `AGENTS.md` were absent from this
scoped checkout; that was reported to the coordinator before continuing.

## 1. Precise setting and conclusion

There are four positive periods `p_i` and arbitrary real phases `s_i`. The
blocked sets are the open trains

`B_i = union_(m in Z) (s_i+m p_i, s_i+(m+1/4)p_i)`.

Write `b_i=1_(B_i)` and `M=sum_i b_i`. Choose any largest-period label, relabel
it as 0, and put

`P=p_0=max_i p_i`,

`Q=(3/4)(p_1+p_2+p_3)`,

`H=P+Q=(3/4)sum_i p_i+(1/4)P <= 13P/4`.

A finite selected chain consists of occurrences `I_j=(L_j,R_j)` with strictly
increasing right endpoints and

`L_(j+1)<R_j<R_(j+1)`.

The claims audited here are:

1. A probability density supported on `[0,H]` is positive everywhere on
   `(0,H)` and satisfies `E[M(a+X)]=1` for every real translation `a`.
2. Every such selected chain has union span strictly below `H`.
3. Label 0 occurs at most three times; the inherited three-label bound of seven
   then gives at most 31 selected occurrences. The structural refinement in
   Section 7 lowers this consequence to 23.
4. Every closed interval of length `H` contains a point outside all four
   blocked trains.

Containment, tied periods, arbitrary phases, and skipped occurrence indices are
all allowed. No common period or integrality is assumed.

## 2. The discrete identity and the exceptional set

For a single open quarter-period train with period `p` and phase `s`, set
`delta=p/4`. Directly partitioning one period into its four open quarters gives

`sum_(k=0)^3 b(z+k delta) = 1` if `z-s` is not in `delta Z`,

`sum_(k=0)^3 b(z+k delta) = 0` if `z-s` is in `delta Z`.

At a quarter-grid point, all four sample positions are quarter-grid points and
none lies in the open blocked quarter. Away from that grid, exactly one sample
lies in the blocked quarter. In particular, the average is always at most
`1/4`, and equals `1/4` off a discrete exceptional set.

Take independent random variables

`U ~ Uniform[0,P]`,

`D_i ~ Uniform{0,p_i/4,p_i/2,3p_i/4}` for `i=1,2,3`,

and set `X=U+D_1+D_2+D_3`.

For label 0, condition on the three discrete variables. Averaging `b_0` over
the remaining full period `U` gives exactly `1/4`, for every conditional shift.

For label `i` in `{1,2,3}`, first condition on `U` and the other two discrete
variables and average over `D_i`. The preceding identity gives `1/4` except
when

`a+U+sum_(j!=i) D_j-s_i` belongs to `(p_i/4) Z`.

For every fixed `a` and fixed values of the other two discrete variables, the
exceptional values of `U` form a finite subset of `[0,P]`. Their probability is
zero. Thus the remaining continuous average equals `1/4`, and

`E[M(a+X)]=1` for **every** real `a`.

The statement is not merely an almost-everywhere identity in the external
translation `a`: the null-set argument applies separately at each fixed `a`.
All integrands are bounded, all discrete sums are finite, and the sole
continuous integral is over a finite interval; exchanging the indicated sums
and integrals is therefore legitimate.

There is also a useful shorter route for the span argument alone. The discrete
quarter-average is at most `1/4` pointwise, including every endpoint. Together
with the exact full-period average for label 0, this immediately gives
`E[M(a+X)]<=1`. That inequality already suffices for the contradiction below.
Consequently the strict span conclusion does not depend on overlooking or
discarding an exceptional quarter-grid point.

## 3. Positivity throughout the support

For `d=(d_1,d_2,d_3)` in `{0,1,2,3}^3`, write

`q_d=sum_(i=1)^3 d_i p_i/4`.

A representative of the density of `X` is

`K(x)=(1/(64P)) sum_d 1_(q_d,q_d+P)(x)`.

The endpoints chosen for these interval indicators do not affect their
integrals. Every summand lies in `[0,H]`, and the total integral is one.
Coincident offsets simply contribute their multiplicities.

To prove positivity at **every** point of `(0,H)`, not just almost everywhere,
put `delta_i=p_i/4` and inspect the following ten offsets already present in
the sum:

`0, delta_1, 2delta_1, 3delta_1,`

`3delta_1+delta_2, 3delta_1+2delta_2, 3delta_1+3delta_2,`

`3delta_1+3delta_2+delta_3,`

`3delta_1+3delta_2+2delta_3, Q`.

They increase from 0 to Q in nine steps. Each step is one of the positive
numbers `delta_i<=P/4<P`. Hence consecutive open intervals of length P based
at these offsets strictly overlap. Their union is exactly `(0,Q+P)=(0,H)`.
Every point of this open support therefore belongs to at least one summand,
so `K(x)>=1/(64P)>0` there.

This argument also handles ties and highly unequal periods. No assertion about
the sorted gaps among all 64 offsets is needed. A purely atomic kernel is not
needed: the displayed finite mixture of uniform intervals supplies exactly the
interior positivity used by the proof.

## 4. Strict union span, including equality

The union of a selected chain is the open interval `(A,B)`, where
`A=min_j L_j` and `B=R_N`. This follows inductively because each next occurrence
overlaps the previous one and has the new largest right endpoint. Thus
`M(t)>=1` at every point of `(A,B)`.

For a one-occurrence chain, its span is `p_i/4<=P/4<H`. For any longer chain,
two consecutive occurrences have a nonempty open overlap. Choose `y` in such
an overlap; then `M>=2` on a neighborhood of `y`.

Suppose that `B-A>=H`. There is an `a` in

`[A,B-H] intersect (y-H,y)`.

Indeed, `[A,B-H]` is nonempty, its left endpoint is below `y`, and its right
endpoint is above `y-H`; when `B-A=H`, its sole point `a=A` satisfies both
strict inequalities because `A<y<B`.

The whole open interval `(a,a+H)` lies in `(A,B)` and contains `y`. On it
`M(a+x)-1>=0`, and that difference is at least one on a nonempty open
subinterval of `(0,H)`. Since K is positive throughout `(0,H)`,

`integral K(x)[M(a+x)-1] dx > 0`.

This contradicts the exact averaging identity, or already the inequality
`E[M(a+X)]<=1`. It follows that

**`B-A<H`.**

No mass is placed at 0 or H, so uncovered boundary points of `(A,B)` do not
alter this reasoning. Endpoint contacts between blocked intervals do not count
as selected-chain transitions: the required positive open overlap is exactly
what forces the strict contradiction. Quarter-duty tilings with isolated safe
contact points consequently remain compatible with the argument.

## 5. The largest-period count is at most three

Suppose label 0 appears `h>=1` times. Its selected right endpoints increase by
positive integer multiples of P, so the last minus the first is at least
`(h-1)P`. The union contains the entire first and last selected P-occurrences.
The first occurrence has width `P/4`. Therefore

`B-A >= (R_last-R_first)+P/4 >= (h-3/4)P`.

This lower bound is non-strict; equality is allowed and harmless. Combining it
with the strict upper bound gives

`(h-3/4)P <= B-A < H <= 13P/4`,

and hence `h<4`, or **`h<=3`**. Using only the span of the selected right
endpoints would lose the `P/4` contribution and would not give this conclusion.

For completeness, the inherited seven bound uses the strict transition estimate

`0<R_(j+1)-R_j<p_(label(j+1))/4`.

A one-label chain has at most one occurrence. In a two-label chain with
periods `p>=q`, two consecutive p-occurrences would have at most one intervening
q-occurrence; their right-endpoint separation would be less than
`(p+q)/4<=p/2`, contradicting separation at least p. Thus p occurs at most once,
and q at most twice, giving three occurrences in total.

In a three-label chain with `p>=q>=r`, between consecutive p-occurrences the
q,r-only chain contains at most one q and two r occurrences. Its full endpoint
advance up to the next p-occurrence would be less than
`(p+q+2r)/4<=p`, again impossible. Thus p occurs at most once, with at most three
occurrences on each side, giving seven. The strict transition inequality also
handles equal periods.

Deleting the h appearances of the chosen P-label leaves at most `h+1`
contiguous three-label chains. These are original contiguous pieces; no new
transition is asserted across a deletion. Consequently

`N<=h+7(h+1)=8h+7<=31`.

If h is zero, the whole chain uses three labels and has at most seven
occurrences. The count makes no minimal-cover or irredundancy assumption.

## 6. Closed-window consequence

Suppose a closed window `[L,L+H]` had no point safe for all four trains. Choose
a blocked occurrence containing L. If its right endpoint has not passed
`L+H`, choose a blocked occurrence containing that endpoint and continue.
Each choice is possible by the assumed full coverage; its new right endpoint
strictly increases and is a valid selected-chain transition.

Only finitely many train endpoints lie in the bounded window, because all four
periods are positive. Thus after finitely many choices the chain passes the
right boundary. Its union starts strictly before L and ends strictly after
`L+H`, so its span exceeds H, contradicting the span lemma.

Therefore every closed window of length H contains a common-safe point.
For a core-safe window W, the sufficient condition is

`(3/4)sum_(residual i)(1/v_i)+(1/4)max_(residual i)(1/v_i) <= width(W)`.

With the inherited core `{1,4,5}` and `W=[9/32,3/8]`, its width is `3/32`.
If every residual speed is at least V, then `H<=13/(4V)`. Hence
`V>=104/3` suffices, and integer residual speeds at least **35** meet this
conservative condition. Failure of the condition says nothing about whether a
particular shorter or clipped window contains a witness.

## 7. Independent audit of the 23-move refinement

After the preceding audit was sent, the coordinator requested a direct
challenge of another agent's proposed 23-move refinement. The argument below
rederives its counts and strict inequalities. It introduces no search or new
fixture.

Order the four periods as `P>=q>=r>=s`, and put `T=q+r+s`. A selected chain
using only q,r,s has at most one q occurrence, by the three-label argument.
Suppose such a chain has length at least six. It must have exactly one q,
since without q it has length at most three. Deleting q leaves two contiguous
r,s-only pieces of lengths at most three. Their total length is at least five,
so both have length at least two and one has length exactly three.

Each piece of length at least two must contain r: a one-label chain has length
at most one. By the two-label argument, each piece contains r exactly once.
Thus the original triple chain contains r exactly twice. The piece of length
three has word `s,r,s`, because its r appears once, its s appears twice, and
consecutive occurrences of a single label are impossible.

In that `s,r,s` piece, the s-endpoint separation is at least s. Summing the two
strict transition advances bounds it above by `(r+s)/4`. Therefore

`s < (r+s)/4`, or **`r>3s`**.

Between the two r appearances in the original triple chain, q appears exactly
once. Before q there can be at most one s, and after q there can be at most one
s, since those portions use only label s. Summing all advances from the first
r endpoint through the second bounds the separation strictly above by
`(q+2s+r)/4`. The same-label separation is at least r, so

`r < (q+2s+r)/4`, or **`q+2s>3r`**.

Combining these strict inequalities gives

`q>3r-2s>7r/3`,

and hence

`r<3q/7`, `s<q/7`, and **`T<11q/7<=11P/7`**.

Now consider the full four-label chain and the number h of its P appearances.
If `h=3`, the whole-occurrence lower bound from Section 5 gives

`9P/4 <= B-A < H=P+3T/4`,

which forces **`T>5P/3`**. This is incompatible with the necessary condition
`T<11P/7` for any contiguous q,r,s piece of length at least six, because
`11/7<5/3`.

Therefore, when `h=3`, all four q,r,s pieces have length at most five, yielding

`N<=3+4*5=23`.

When `h<=2`, the inherited count already gives `N<=8h+7<=23`; the absent-label
case `h=0` is included. Thus the combined argument yields **`N<=23`**.

No shorter-span property is assumed for the individual triple pieces beyond
their ordinary chain transitions. The argument needs only necessary conditions
for a long triple piece; it never asserts those conditions are sufficient.
Skipped laps strengthen the lower endpoint separations, and tied periods are
handled by the strict inequalities, so neither creates an omitted case.

## 8. Audit disposition

The kernel identity, its null exceptional sets, density positivity, strict span,
and the decisive whole-occurrence lower bound are mutually consistent. The
largest-period occurrence count of three and the initial 31-move bound follow
under the stated hypotheses. The separately requested long-triple-piece audit
also supports the stronger 23-move consequence. No finite-family testing is
needed to close these analytic steps. The result remains a proof candidate
pending external review; this audit does not establish novelty, all-reference
claims, or the full lonely-runner conjecture.
