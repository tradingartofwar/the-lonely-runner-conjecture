# Adversarial review of the mixed quarter-period kernel

September 28, 2026. Review against the supplied live-baseline brief for
`bcf959b45a35701f2fd710b1d86ca2cc3152e14c` and the prior full 39-move note.

**Status: HYPOTHESIS / proof-candidate review.** This is an AI-assisted internal
mathematical attack, not independent human review, a literature check, or a
proof certificate. No speed/phase/word scan or executable fixture evaluation
was performed. The supplied workspace is a scoped copy, not a Git checkout;
its README and HANDOFF are absent. The brief, AGENTS, CLAIM_STATUS,
CONTRIBUTING, and prior full 39-move proof were read.

## Finding

I found no defect in the mixed-kernel argument for 31 advancing moves, 31
checked rounds / 341 calls, or the non-strict sufficient window condition
`H <= width(W)`. The exceptional quarter-grid values do require an explicit
argument. The retained continuous average repairs them completely: the final
convolution identity holds for every translation, including translations at
the critical chain boundary.

The claims below retain arbitrary real phases, all positive periods, equal
periods, skipped laps, containment, and exact safe endpoints. They apply to
the actual selected strict-overlap chain, not an irredundant replacement.

## 1. Endpoint attack: the discrete identity is not pointwise

Write `f_i=1_(B_i)`, `q_i=p_i/4`, and let `D_i` give weight `1/4` to each of
`0,q_i,2q_i,3q_i`. Directly from the open-interval convention,

`(D_i*f_i)(t) = 1/4` if `t` is not in `s_i+q_i Z`, and is `0` otherwise.

Here convolution denotes averaging forward shifts; the sign convention is
immaterial if used consistently. At a quarter-grid point, all four sampled
phases are endpoints or outside the open blocked quarter. Away from that
grid, exactly one sampled phase lies inside it.

Therefore a proof that writes `D_i*f_i=1/4` pointwise is false. A concrete
failure is four equal periods `p_i=1`, equal shifts `s_i=0`, and four discrete
averages with no continuous factor. At translation zero every resulting
sample lies on the quarter-grid, so its multiplicity is zero and the average
is zero, not one. This is an analytic endpoint counterexample to that stronger
claim, not a counterexample to the proposed mixed kernel.

Choose a largest-period index `m` and put `P=p_m`. Let `U` be independent
uniform measure on `[0,P]`; use `D_i` for the other three labels. Their product
convolution is the distribution `K` of

`X=U+sum_(i != m) D_i`.

For label `m`, condition on the three discrete variables. Integration over
its own full period gives `E[f_m(a+X)]=1/4` for every real `a`.

For a label `i != m`, first average its own discrete variable. Conditional on
the other two discrete variables, the exceptional values of `U` lie in a
translate of `s_i+q_i Z`, a countable set of Lebesgue measure zero. Thus the
remaining continuous average gives exactly `1/4`, for every `a` and every
choice of the other discrete variables. All functions are bounded, and the
discrete sums are finite, so this rearrangement of averages needs no limiting
argument or delicate Fubini hypothesis.

Summing gives the required pointwise-in-translation statement

`E[M(a+X)] = 1` for every real `a`.

In particular, this equality remains valid when `a` equals a union endpoint,
a blocked endpoint, or a phase-dependent quarter-grid point. The values of
`M` at countably many points never alter the final integral.

## 2. Positivity attack: finite atoms must not leave holes

Set

`H=P+(3/4)sum_(i != m) p_i=(3/4)S+(1/4)P`.

The mixed distribution has a density: it is the equally weighted sum of 64
uniform densities, each supported on a translate of `[0,P]`. It has no point
masses. Its support is `[0,H]`.

More than support containment is needed. To establish positivity throughout
the interior, begin with a density positive on `(0,L)`, initially `L=P`.
Convolution with `D_i` sums its four translates, positive respectively on

`(0,L), (q_i,q_i+L), (2q_i,2q_i+L), (3q_i,3q_i+L)`.

Because `0<q_i<=P/4<L`, adjacent open intervals strictly overlap. Their union
is precisely `(0,L+3q_i)`. Induct over the three discrete factors. This proves
that a natural representative of the final density is positive at every point
of `(0,H)`, including internal jump locations that might have been problematic
had translates only touched. Positivity almost everywhere would already
suffice for the later contradiction.

No commensurability, generic phase, distinct-period assumption, or continuity
of the final density is being used.

## 3. Critical span equality is excluded

Let the selected chain have union `(A,B)` and at least two occurrences. Its
strict transition inequality supplies an open overlap interval on which
`M>=2`. Pick `y` inside that overlap. If `B-A>=H`, the interval

`[A,B-H]` intersects `(y-H,y)`.

Indeed its left endpoint is strictly below `y`, and its right endpoint is
strictly above `y-H`; these inequalities follow from `A<y<B`. Choose `a` in
the intersection. Then `(a,a+H)` lies in the chain union and contains a
positive-length part of the overlap. Consequently `M-1>=0` on the interior,
and is positive on a nonempty open subinterval where the kernel is positive.
This contradicts

`integral_0^H K(x)(M(a+x)-1) dx=0`.

If `B-A=H`, the allowed choice is exactly `a=A`. It is valid by the
pointwise-in-translation identity in Section 1. Both integration endpoints
have measure zero, regardless of whether they are safe. A one-occurrence
chain has width at most `P/4<H`. Thus every selected chain has `B-A<H`.

Exact tilings with only endpoint contacts do not contradict this argument:
they provide no positive overlap, and their contact points remain safe.

## 4. The 31 conversion uses interval width, not just endpoint separation

Suppose the largest-period label occurs `h>=1` times, with first selected
right endpoint `r_1` and last `r_h`. Increasing right endpoints imply increasing
occurrence indices even when laps are skipped, so

`r_h-r_1 >= (h-1)P`.

The whole union contains the full first occurrence, whose left endpoint is
`r_1-P/4`, and contains the last right endpoint as its boundary or interior
limit. Hence

`B-A >= r_h-(r_1-P/4) >= (h-3/4)P`.

Combine this with `B-A<H<=13P/4`. It follows that `h<4`, hence `h<=3`.
The weak inequality in the lower span estimate is enough; it must not be
silently replaced by an unsupported strict inequality.

Deleting these occurrences leaves at most `h+1` contiguous three-label
chains, each bounded by seven by the prior pair/triple argument. Therefore

`N <= h+7(h+1)=8h+7 <=31`.

If the largest-period label is absent, the entire chain is already a
three-label chain and has at most seven occurrences. This also handles ties:
choose any largest-period label, present or absent.

## 5. Calls and checked rounds

The repeated order `a,b,c,d,c,d,b,c,d,c,d` visits every label. Any round that
starts unsafe makes at least one advancing projection: otherwise its state
would never change, all visited labels would be safe at that unchanged state,
and its starting state would have been safe.

After 31 unsafe-start rounds, there have been at least 31 advances. If the
state were still unsafe, the next round would force a 32nd, contradicting the
chain bound. Thus a joint-safety check at each round boundary certifies success
by the end of round 31, after at most `31*11=341` scalar projection calls.
Completing the rest of the successful round is harmless because projections
at a jointly safe state are stationary. An initial boundary check permits
immediate termination with zero calls if the start is safe.

This count does not include the work of the separate safety checks and is not
an arithmetic bit-complexity bound. If the operational stop rule instead
requires a whole extra unchanged round, retain the separate cap of 32 rounds /
352 calls. Do not describe 31 as a bound on raw projection calls or claim that
the actual implementation uses checked boundaries without inspecting it.

## 6. The window condition includes equality

Suppose a closed interval `[L,R]` with `R-L>=H` had no point safe for all four
trains. Start with a blocking occurrence containing `L` strictly. Whenever the
current right endpoint is at most `R`, it too is unsafe and lies strictly
inside some blocking occurrence with a larger right endpoint. Continue.

Only finitely many occurrence endpoints lie in the bounded range needed for
this construction, because the four periods are positive. It therefore
produces a finite strict chain whose union starts strictly before `L` and ends
strictly after `R`. Its span exceeds `R-L>=H`, contradicting Section 3.

Thus every closed interval of length at least `H` contains a jointly safe
point. The argument does not discard singleton endpoint witnesses. For a
closed core-safe window `W`, the sufficient test is exactly

`(3/4)sum_(residual i)1/v_i + (1/4)max_(residual i)1/v_i <= width(W)`.

For positive residual speeds all at least `v_min`,

`H <=13/(4v_min)`.

On the inherited core window `[9/32,3/8]` of width `3/32`,
`v_min>=104/3` suffices; hence positive integer residual speeds at least 35
suffice. This is a sufficient threshold, not an optimal threshold or a
necessary condition. Failure of this test says nothing by itself about whether
the core window contains a witness.

## Remaining review limits

The argument does not establish sharpness of 31, novelty of the kernel method,
general core-window existence, any all-reference conclusion, or the full
eight-runner conjecture. The operational call claim is conditional on the
stated check convention. Implementation, inherited fixture certificates, and
external mathematical review remain separate checks.

## Follow-up: adversarial audit of the proposed 23-move improvement

The coordinator supplied a subsequent analytic strengthening, using a
structural restriction on long three-label chains. I find that strengthening
valid under the same assumptions. It supersedes 31 as the best bound reviewed
in this note; the earlier endpoint and mixed-kernel audit remains necessary.
No additional executable evaluation or scan was used.

Write the four periods in nonincreasing order `P>=q>=r>=s>0`. First consider a
three-label chain on periods `q,r,s` with at least six occurrences. The prior
triple argument shows that `q` occurs at most once. It must occur once here,
because a chain using only `r,s` has at most three occurrences. Split at its
single occurrence. The two remaining pair pieces have lengths at most three,
and their total length is at least five. Consequently one has length three
and the other has length at least two.

Each pair piece contains exactly one `r`: there is at most one by the prior
pair argument, while without any `r` it would contain at most one `s`.
The three-occurrence piece is necessarily the word `s,r,s`. Its two selected
`s` right endpoints differ by at least `s`, whereas the strict transition
inequality makes that difference strictly less than `(r+s)/4`. Therefore

`r>3s`.

Now compare the two selected `r` occurrences, one in each pair piece. The
single `q` lies between them. Within either pair piece, at most one `s` can
appear on either side of its single `r`: adjacent selected occurrences of one
label are impossible. Thus there are at most two `s` occurrences between the
two `r` occurrences in the full triple chain. This includes both orientations
of a length-two piece, `r,s` and `s,r`; either orientation can only reduce the
number of intervening `s` occurrences from its upper bound of two.

The two selected `r` right endpoints differ by at least `r`. Summing the strict
transition inequalities from the first to the second gives an upper bound
strictly below `(q+2s+r)/4`. Hence

`q+2s>3r`.

Since `s<r/3`, these inequalities imply

`q>3r-2s>7r/3`, so `r<3q/7` and `s<q/7`.

In particular, every three-label chain of length at least six forces

`q+r+s<11q/7<=11P/7`.

Return to the full four-label chain and let `h` count its selected `P`
occurrences. The mixed-kernel argument already gives `h<=3`. If `h<=2`,
deletion into three-label pieces gives directly

`N<=h+7(h+1)<=23`.

If `h=3`, the whole union has span at least `(3-3/4)P=9P/4`. Combining this
with the strict mixed-kernel span bound yields

`9P/4 <= B-A < P+(3/4)(q+r+s)`, hence `q+r+s>5P/3`.

No three-label piece can now have length at least six, because that would also
give `q+r+s<11P/7`, and `11/7<5/3`. Each of the at most four pieces therefore
has length at most five, giving

`N<=3+4*5=23`.

This proof handles empty pieces and the case of an absent largest-period
label. Ties create no loophole: every ordering inequality is weak except the
strict inequalities supplied by positive overlap. Indeed the long-triple
conditions themselves rule out relevant ties. Skipped occurrence indices
only increase the lower bounds on same-label endpoint separations, so cannot
invalidate the contradiction. Containment does not affect the strict
transition inequality or the deletion into contiguous pieces.

Under the checked-round convention already audited above, this strengthening
gives **23 rounds / 253 scalar projection calls**. The extra unchanged-round
convention instead gives **24 rounds / 264 calls**. The mixed-kernel window
criterion is unchanged. These remain proof-candidate claims, with sharpness,
external mathematical review, and novelty review pending.

## Final follow-up: general-m induction audit

I also read the supplied `general.md` and checked its extension to `m>=2`
trains of duty `1/m`. The same endpoint repair and shifted-support positivity
argument applies to the m-point grids. Its support bound and whole-occurrence
estimate are

`H_m=P+((m-1)/m)sum_(others)p_i <=(m-1+1/m)P`,

`B-A >=(h-1+1/m)P`.

Together with the strict span bound these correctly imply `h<m`, hence
`h<=m-1`. There is no lost endpoint equality in this calculation.

The induction's interval enlargement is valid. For an original train
`(s_i+j*p_i, s_i+(j+1/m)*p_i)`, set

`s_i'=s_i+p_i/m-p_i/(m-1)`.

The duty-`1/(m-1)` train with shift `s_i'` retains every original right
endpoint and moves each left endpoint left. Thus every selected strict
transition, increasing endpoint order, and skipped occurrence index is
preserved. After deleting the largest-period label, the at most `m` contiguous
pieces may be bounded using this enlarged-duty theorem; missing labels can
be included without changing the selected sequence.

The full-duty base deserves a separate statement: `B_1=1` is correct because
consecutive open intervals of one duty-one train only touch at their
endpoints, so no strict chain transition is possible. Its one-occurrence span
equals its period. Therefore the strict span lemma would be false at `m=1`.
`general.md` correctly restricts that lemma and its mixed-kernel derivation to
`m>=2`; the induction from `m=2` uses only the separately valid count `B_1=1`.

Accordingly `(B_m+1)<=m(B_(m-1)+1)` is valid. Starting from `B_4=23=4!-1`
gives the upper bound **`B_m<=m!-1` for every integer `m>=4`**. These are
chosen valid upper bounds, not assertions of optimal chain lengths.

The scope is correctly distinguished: duty `1/m` means symmetric distance
threshold `1/(2m)` for m moving constraints. It is not the full `(m+1)`-runner
threshold `1/(m+1)`. For total runner count `n=2m`, it may be applied to m
residual constraints inside a window already safe for the other `m-1`
constraints relative to the selected reference. Existence of that core window
and its sufficient width are still separate requirements. No new gap was
found in this final analytic audit; the external-review and novelty limits
remain unchanged.
