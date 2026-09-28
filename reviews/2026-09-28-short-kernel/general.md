# General duty-one kernel and a 23-move count candidate

September 28, 2026. Review of the live short-kernel proposal, using the
39-bound note as the prior proof. **HYPOTHESIS / proof candidate.** This note is
AI-generated mathematical reasoning, not independent external review. It adds
no computational scan, new physical configuration, publication, or novelty
claim.

## 1. The general mixed kernel is valid

Fix an integer `m>=2`, positive periods `p_1,...,p_m`, and arbitrary shifts.
The open blocked intervals of label i have width `p_i/m`. Write `P=max_i p_i`
and choose one label with period P. Let U be uniform on `[0,P]`; for each other
label i let `D_i` be uniform on

`{0,p_i/m,2p_i/m,...,(m-1)p_i/m}`.

All variables are independent. Put `X=U+sum_i D_i`, where the sum excludes the
selected P label, and

`H=P+((m-1)/m) sum_(i != P) p_i`.

For any real a and total blocking multiplicity M,

`E M(a+X)=1`.                                                  (1)

For the selected P label, condition on the discrete variables and average over
U: this is exactly its full-period mean `1/m`. For another label i, averaging
over its m grid translates is `1/m` except at the grid boundary congruence
class, where it is zero because both interval endpoints are excluded.
Conditioning on every variable except U and D_i, the continuous U assigns
probability zero to that exceptional discrete set. Thus this label also has
expectation exactly `1/m`. Finite summation/Fubini justifies summing the labels.
The pointwise grid average alone is not claimed to be identically `1/m`.

The density K of X is supported on `[0,H]` and positive at every point of
`(0,H)` for the natural open-interval representative. Start with the density
of U, positive on `(0,P)`. If a density is positive on `(0,L)`, convolution
with an m-point grid of spacing `delta=p_i/m<=P/m<P<=L` is positive on the union
of `(j*delta,j*delta+L)` for `j=0,...,m-1`. These open intervals overlap and
their union is `(0,L+(m-1)*delta)`. Induction proves the assertion. Tied periods
and overlapping discrete atoms cause no problem.

Every selected strict chain has union `(A,B)` with

`B-A<H`.                                                       (2)

For a one-occurrence chain, its width is at most `P/m<H`. For a longer chain,
there is a positive open overlap on which `M>=2`, whereas `M>=1` throughout
the chain union. If `B-A>=H`, one can place an interval `[a,a+H]` inside
`[A,B]` with that overlap meeting its interior. Positivity of K then makes
`E[M(a+X)-1]>0`, contradicting (1). This is the same strict-span argument as
the prior full-period kernel, with H replacing S. Endpoints have measure zero;
endpoint-only contacts are not strict chain transitions.

## 2. Whole occurrences give h<=m-1

Suppose the selected P label occurs h times. Its first and last selected right
endpoints differ by at least `(h-1)P`; skipped laps only increase this. The
first whole occurrence starts a further `P/m` to the left, so

`B-A >= (h-1+1/m)P`.

Meanwhile

`H <= [1+(m-1)^2/m]P = (m-1+1/m)P`.

Combining with (2) gives `h<m`, hence `h<=m-1`. Equality in the span lower
bound is allowed; the strict kernel upper bound supplies the contradiction.
Containment or additional earlier left endpoints strengthen the lower bound.
This is a whole-interval span argument, not just an endpoint-span argument.

## 3. A general finite count recurrence

Let B_m bound the number of occurrences in any m-label chain of duty `1/m`.
One label has at most one occurrence, so take `B_1=1`. After deleting the h
occurrences of a largest-period label, there are at most `h+1` contiguous
pieces on at most `m-1` labels, still at duty `1/m`.

To invoke B_(m-1), enlarge each remaining interval to width `p_i/(m-1)` by
moving its left endpoint left and retaining its right endpoint. This yields
another periodic train with a changed shift. It preserves every strict chain
transition and endpoint order. The larger-duty count therefore bounds the
original piece. Missing labels can be supplied with arbitrary phases and do
not affect the selected chain.

Consequently

`B_m <= (m-1)+m B_(m-1)`.

Taking this recurrence literally gives `B_m=2*m!-1`. It is conservative. For
four quarter-duty labels, the sharper elementary triple bound of seven gives
`3+4*7=31`. The additional immediate return inequalities below improve that
four-label constant to 23. Using 23 as the m=4 base in this same enlargement
recurrence gives `B_m=m!-1` for `m>=4`; this is a corollary conditional on the
23-count proof below, with no sharpness claim.

## 4. Immediate quarter-duty sharpening: N<=23

Order the periods `P>=q>=r>=s`. The prior elementary bounds are one occurrence
for a one-label chain, three for a pair, and seven for a triple. In particular,
a q,r,s chain has q at most once, and after deletion of q its two r,s pieces
have r at most once and at most three occurrences each. These statements
include equal periods and skipped laps.

For completeness, their return argument uses the universal transition bound

`0<R_(j+1)-R_j<p_(label(j+1))/4`.                               (3)

A return to the larger of two labels would have separation at least its
period but, with the one possible smaller label in between, strictly less
than half that period. Thus it cannot occur. A return to q in a q,r,s chain
would have intervening weighted period sum at most `r+2s`. Including the
returning q interval gives an endpoint increment strictly below
`(q+r+2s)/4<=q`. That return is also impossible.
Deleting the unique largest occurrence then gives the bounds three and seven.

**Long-triple lemma.** If a q,r,s chain has at least six occurrences, then

`r>3s`, `q+2s>3r`, and therefore `q+r+s<11q/7`.                 (4)

Proof: q must occur exactly once. Its two r,s pieces have total length at
least five and each length at most three, so one is a three-occurrence piece
`s,r,s`, and both contain r. The s-return in this piece, using (3), gives
`s<(r+s)/4`, hence `r>3s`. There are exactly two selected r occurrences.
Between them lie q and at most two s occurrences, since each pair piece has
r at most once and s at most once on either side of r. Applying (3) to the
return to r gives `r<(q+r+2s)/4`, or `q+2s>3r`. Thus

`s<r/3`, `r<(q+2s)/3<(q+2r/3)/3`, so `r<3q/7`.

It follows that `q+r+s<q+4r/3<11q/7`, proving (4). This argument classifies
only the forced placement of the unique q and two r occurrences; no word
enumeration is used.

Now let h be the number of P occurrences in the full four-label chain. By
Section 2, `h<=3`.

* If `h<=2`, the triple bound gives `N<=h+7(h+1)<=23`.
* If `h=3`, the whole first and last P intervals give `B-A>=9P/4`. The mixed
  span bound gives `B-A<P+3(q+r+s)/4`. Hence `q+r+s>5P/3`.
  If any of the four triple-only pieces had length at least six, (4) would
  instead give `q+r+s<11q/7<=11P/7<5P/3`, a contradiction. Each triple-only
  piece therefore has at most five occurrences, and `N<=3+4*5=23`.

Thus **every actual four-label quarter-duty strict chain has N<=23**, under
the mixed-span proof candidate. The assertion concerns actual selected
occurrences and does not assume minimality, irredundancy, or consecutive lap
indices. It is an upper bound only; no attaining example is supplied. Further
optional sharpening is deliberately not pursued in this review.

For the existing eleven-call round order and joint-safety tests at round
boundaries, this means at most **23 advancing moves, 23 rounds, or 253 scalar
projection calls**. Those are different counters. Requiring one additional
unchanged confirmation round would instead give 24 rounds / 264 calls. The
inherited fixture first succeeding on scalar call 23 used only seven advancing
moves, so its call number supplies no lower bound approaching 23 moves.

## 5. Scope relative to Lonely Runner

The general-m result is for m arbitrary-phase constraints with duty `1/m`,
equivalently symmetric distance threshold `1/(2m)`. It also yields a
common-safe point in every closed interval of length H, by the prior
strict-chain cover argument. It does not assert that a shorter supplied core
window contains a common-safe point.

For the original common-start Lonely Runner convention, n is total runners
and k=n-1 is the number of constraints relative to a selected reference.
At threshold `1/n`, each blocked train has duty `2/n`, so all k constraints
have total duty `2(n-1)/n`, greater than one for n>2. The identity (1) and its
sign contradiction do not apply to that whole set. For n=8, the intended
application uses four residual quarter-duty trains inside a window already
safe for the other three constraints. This remains a selected-reference
conditional statement; neither core-window existence nor all-reference
coverage nor the full conjecture is established.

The prior note already credits the basic shifted `1/(2m)` existence theorem
to Schoenberg via Beck--Hosten--Schymura. No new literature search was needed
for this internal derivation, and novelty of the kernel, span, or finite
count is not claimed. Independent mathematical and novelty review remain
pending.
