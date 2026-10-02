# Skeptical audit: real phases, critical tilings, and the compactness bridge

Date: 2026-09-28. Pinned baseline: `5871f2b6c57552b5bd55fd4caa82d0c61307b10e`.

Scope: four positive speeds and arbitrary real phases, threshold `delta=1/8`.
The common-start positive-integer setting is a special case. All general
implications below remain **HYPOTHESIS / proof candidates**, materially
AI-derived and internally reviewed; no external review or novelty claim.
No speed scan, phase scan, or new physical configuration was performed.

## 1. A fixed real-phase input cannot cover a half-line

Write

`I(i,m)=((m-1/8-alpha_i)/v_i,(m+1/8-alpha_i)/v_i)`

for open blocking occurrences, and use the existing continuous periodic
primitive `H` with `H'=M-1` away from thresholds. The function `H` is bounded.
Its dependence on the four phases is continuous.

There are times `t_n -> infinity` such that all four `v_i t_n` approach
integers modulo one. One elementary justification is simultaneous
pigeonhole approximation: arbitrarily accurate positive integer return
times exist; if these times remain bounded along a subsequence, a positive
exact common period exists and its multiples give unbounded return times.
Consequently

`H(t_n+s) -> H(s)`

for every fixed real `s`.

Suppose the open blocking sets cover `[0,infinity)`. Then `M>=1`, so `H` is
nondecreasing there and, being bounded, converges to a limit `ell`. Applying
the return sequence gives `H(s)=ell` for every `s>=0`. Hence `M=1` almost
everywhere on the half-line. This contradicts open coverage: an occurrence
containing any sufficiently positive time has a finite right endpoint; an
open occurrence covering that endpoint overlaps the first one on a positive
interval, forcing `M>=2` there.

The argument also shows that **closed** occurrence coverage of a half-line
forces `M=1` almost everywhere. Threshold times form a locally finite set,
so closed versus open membership differs only at isolated times. Recurrence
then extends multiplicity one to all real times: a strict overlap or strict
gap anywhere would recur arbitrarily far to the right. Thus a weakly covered
half-line produces an exact tiling of the whole line, up to tile boundaries.

### Consequence for real-phase projection iterations

There is no Zeno exception for a fixed positive-speed input. Every advancing
projection ends at a new occurrence right endpoint. The endpoint set is a
finite union of arithmetic progressions and is locally finite. Therefore an
infinite advancing chain would have right endpoints tending to infinity.
Its strict consecutive overlaps would openly cover a half-line, just ruled
out. Every fixed real-phase input therefore has only finitely many advances.

This qualitative argument does not supply an arithmetic overlap quantum or
an effective bound. It does not by itself imply a uniform bound over inputs.

## 2. Why naive compactness is insufficient

At an occurrence's left endpoint, equality is safe. The next-safe map fixes
that endpoint, but points immediately to its right may jump almost the whole
occurrence width. Thus the next-safe map is discontinuous in exactly the
direction relevant to a touching tiling.

A sequence of longer strict chains could a priori converge to a family of
touching occurrences. In the limit the touching times are joint witnesses,
and the limit algorithm may stop immediately. Compactness alone does not
turn the approximating chains into an infinite strict chain. This is a
logical loophole, not an asserted construction of such a sequence.

What compactness legitimately supplies is **weak coverage**. Normalize the
slowest speed to one, absorb the starting time into the phases, and suppose
all speeds are at most `D`. A selected chain with final endpoint `T` has at
most `4DT+8` distinct occurrence right endpoints. Hence unbounded move counts
force `T -> infinity`. A convergent subsequence of speed/phase tuples then
weakly covers every fixed interval `[0,A]`. Section 1 implies an exact
limiting tiling. A separate local obstruction at such tilings is essential.

## 3. Independent classification of exact four-train tilings

This classification is a useful cross-check, although Section 4 only needs
periodicity of the limiting tiling.

Let `B(x)=1_{||x||<1/8}`. Its nonzero-frequency coefficient is

`c_n = sin(pi*n/4)/(pi*n)`.

For an exact tiling, `sum_i B(v_i t+alpha_i)=1` almost everywhere. Long-time
Fourier averaging at a frequency `lambda` therefore gives

`sum_{i: lambda/v_i is a positive integer} c_(lambda/v_i)
 exp(2*pi*i*(lambda/v_i)*alpha_i) = 0`.

This follows directly by splitting the integral into runner periods; a
runner contributes zero unless the frequency is its integer harmonic.

Let `a=min(v_i)`. At frequency `a`, only runners of speed `a` contribute.
A single minimum-speed runner is impossible.

* Four minimum-speed runners: the first three phase power sums vanish.
  Newton's identities force the four phase factors to be a rotated set of
  fourth roots of unity. All speeds are `a`, with quarter-spaced phases.
* Three minimum-speed runners: their phase factors form a rotated set of
  third roots of unity. The sole remaining speed `d` must be an integer
  multiple of `a`, because its own fundamental must be cancelled by a slow
  harmonic. The first nonzero combined slow harmonic is `3a`, forcing
  `d=3a`. After a time shift, phases are `(0,1/3,2/3,1/2)`.
* Two minimum-speed runners: their phases differ by `1/2`. At frequency
  `2a`, their combined coefficient has magnitude `1/pi`. Only a remaining
  runner of speed `2a` can contribute at this frequency. A single such
  runner contributes magnitude `sqrt(2)/(2*pi)<1/pi`, so both remaining
  speeds must be `2a`. After a time shift, phases are
  `(0,1/2,3/8,5/8)`.

Consequently the only speed multisets, up to scale and permutation, are

`(1,1,1,1)`, `(1,1,1,3)`, and `(1,1,2,2)`.

The displayed phase choices can also be checked directly by their tile
widths and centers. Every shared boundary is safe because blocking is open.
These are auxiliary shifted-phase tilings, not common-start physical
counterexamples.

An alternative to this classification is enough for the next argument.
Any pair of occurrence trains in a tiling has disjoint interiors. If their
period ratio were irrational, the difference set of their occurrence
centers would be dense and some pair of interiors would intersect.
Therefore all period ratios are rational and the tiling has a common
period `P`.

## 4. The missing local bridge is valid

This section independently audits the maximal-cycle-period formulation
communicated by the geometry and occurrence agents. It repairs the endpoint
loophole in Section 2 without claiming that the selector itself is
continuous.

Fix an exact tiling with common period `P`. For color `i`, let its period be
`p_i=1/v_i`, and let `q_i=P/p_i` be its positive integer number of occurrences
per tiling period. Fix a compact interval spanning at least three periods,
with a little padding. We only use contacts strictly inside that interval.

At every tile contact, exactly two occurrences meet: one ends there and the
next starts there. A third positive-width occurrence through that contact
would overlap one of them on an open interval. Since there are finitely many
contacts in the fixed compact interval, choose small contact neighborhoods
with the following properties:

1. Each neighborhood meets only its two adjacent limiting occurrences.
2. The two relevant endpoints are in the central part of the neighborhood.
3. Every other occurrence stays a positive distance away.

These properties persist for all sufficiently nearby speed/phase tuples.
Only finitely many lap labels can enter a fixed compact interval when the
speeds remain in a compact positive range, so no unseen distant label can
invalidate the third condition.

If a nearby tuple **openly covers the whole compact interval**, its left
and right occurrences at every selected contact must strictly overlap.
Otherwise the interval between the shifted right and left endpoints, or
their common endpoint if equal, remains uncovered inside that contact
neighborhood. Checking coverage only at the unshifted contact would not
suffice; coverage of its whole neighborhood is what proves this step.

Now retain the tiling's cyclic occurrence word. Under the perturbation,
write `p'_i` for the new period, and set

`s_i=q_i*p'_i`.

Select a color `r` attaining `max_i s_i`. The three-period window includes
a full cyclic word beginning with an occurrence of color `r` and ending at
its corresponding occurrence one original tiling period later. The latter
has lap label larger by exactly `q_r`, so its left endpoint is translated
by `s_r`. The intervening cycle contains `q_i` occurrences of each color.
Each occurrence has width `p'_i/4`; all successive handoffs strictly overlap.
Telescoping widths minus overlaps therefore gives

`s_r < sum_i q_i*p'_i/4 = (s_1+s_2+s_3+s_4)/4 <= s_r`,

a contradiction.

Thus every exact tiling has a neighborhood of parameter space in which no
input can openly cover this fixed finite interval. This is precisely the
extra fact missing from naive compactness. It rules out the proposed
arbitrarily long chains converging to a touching tiling when speed ratios
remain bounded.

### Compact-regime conclusion

For every fixed `D<infinity`, some finite constant `C(D)` bounds the number
of advances in every strict increasing-endpoint chain with
`1<=v_i<=D`, with arbitrary phases and starting time. Otherwise the sequence
from Section 2 would converge to a tiling and contradict its local
neighborhood obstruction.

This proof is nonconstructive: it supplies neither a numerical `C(D)` nor an
efficient way to compute it. It bounds arbitrary selected strict chains and
therefore applies to the specified repeated projection word, without needing
that word to reproduce the limiting tile order. The order forced locally is
the order of **all relevant occurrence intervals**, obtained from coverage.

## 5. Independent audit of the square-free occurrence rule

The occurrence agent's stronger relational statement is valid under the
stated actual-chain assumptions: a strict, increasing-right-endpoint chain
of at most four duty-`1/4` trains cannot contain a consecutive repeated word
`WW` of runner labels.

Let `W` have length `m`, with `q_i` appearances of label `i`, and put
`p_i=1/v_i`. Choose a label `r` maximizing `q_i*p_i`; absent labels have
`q_i=0`. Match any appearance of `r` in the first copy to the corresponding
appearance `m` positions later in the second. The `m` destination intervals
between these two appearances contain exactly `q_i` occurrences of each
label. In particular there are `q_r` new selected occurrences of `r` after
the first endpoint and up to the last. Since right endpoints strictly
increase, their lap labels increase by at least one each. Thus the total
right-endpoint displacement `D` is at least `q_r*p_r`.

For consecutive selected intervals, write `g_j=R_j-L_(j+1)>0`. Their right
endpoint increment is `width_(j+1)-g_j`. Summing over these `m` moves gives

`0 < sum g_j = sum_i q_i*p_i/4 - D
             <= sum_i q_i*p_i/4 - max_i(q_i*p_i) <= 0`,

a contradiction. With fewer than four labels the last inequality is only
stronger. Containment and skipped lap labels do not defeat the calculation;
the required assumptions are the actual strict handoffs and increasing
right endpoints. The lemma restricts the occurrence word but does not, by
itself, prove a finite bound on word length.

It can also replace the maximal-anchor calculation in Section 4. Near an
exact periodic tiling, contact neighborhoods force two consecutive copies
of its tile word to have strict handoffs and increasing endpoints, which
the square-free lemma forbids. The direct maximal-anchor proof remains
useful because it exposes the same width-versus-period contradiction.

## 6. Independent audit of the noncompact speed-ratio bound

The geometry agent's `geometry.md`, Sections 3–4, supplies the needed
quantitative bound when `d>=4a`. The following details were checked
separately after Sections 1–4 were written.

For two ordered colors `c<=d`, two consecutive selected `c` occurrences
would require a `d` subchain to bridge a safe gap of length at least
`3/(4c)`. A chain using only `d` has at most one interval of width `1/(4d)`,
so this is impossible. Hence a pair chain has at most one `c`, with at most
one `d` on either side: at most three selected intervals.

For three ordered colors `b<=c<=d`, a subchain between consecutive selected
`b` occurrences uses only `c,d` and has span at most
`1/(4c)+1/(2d)<=3/(4b)`, with strict inequality when all three widths are
needed because its handoffs strictly overlap. With fewer intervals the
inequality is also strict. It cannot bridge the `b`-safe gap. Thus a triple
chain has at most one `b` and at most two pair subchains: at most seven
selected intervals. Skipping laps only enlarges the safe gap in these
arguments.

Writing `N_a` for the number of selected `a` occurrences gives

`N <= N_a + 7*(N_a+1) = 8*N_a+7`.

A full `a` occurrence has length `1/(4a)`. Put `x=d/(4a)>=1`. The exact
minimum measure of overlap with the whole `d` train is

`[floor(x)/4 + max(0, frac(x)-3/4)]/d`.

On each cell `x=n+r`, `n>=1`, the ratio of the bracketed expression to `x`
is minimized at `r=3/4`, where it equals `n/(4n+3)>=1/7`. Thus every
selected `a` occurrence charges at least `1/(28a)` of excess coverage.
Selected `a` occurrences are pairwise disjoint, and the inherited budget is
at most `3/(4a)`. Consequently `N_a<=21` and

`N<=175` whenever `d>=4a`.

The budget applies to the union of the **whole selected occurrences**, so
there is no error from clipping the first occurrence at the initial time.
The lower overlap bound is with the entire fastest train; those overlapping
fast occurrences need not themselves be selected. No arithmetic overlap
quantum or integer-speed assumption is needed.

Combining this audited noncompact bound with Section 4's compact-regime
argument supplies a complete proof candidate that some absolute finite
advancing-move bound exists for arbitrary real speeds and phases. It still
does not supply a numerical universal bound, because `C(4)` is qualitative.

## 7. Scope and remaining review

A uniform advancing-move bound gives a uniform number of rounds only because
the specified round visits all four colors. It is not a bound on arithmetic
bit complexity, and it does not force a witness inside a supplied core-safe
window. The four-residual result is not the full Lonely Runner Conjecture.

Endpoint conditions requiring explicit preservation in a final synthesis:

* Blocking occurrences are open; equality at distance `1/8` is safe.
* Weak coverage enters only in the limiting argument; strict overlap is
  recovered from actual open coverage of contact neighborhoods.
* The compactness normalization requires positive speeds bounded above and
  below, and absorbs the varying initial time into four phase coordinates.
* A selected chain cannot repeat an occurrence or have finite endpoint
  accumulation for any fixed input.
* The limiting tiling may have equal speeds even when every original
  physical input has distinct positive integer speeds.

No contradiction was found in the square-free rule, the numerical
noncompact bound, or the local compactness bridge after these conditions
were made explicit. This is internal mathematical audit, not an independent
external proof certification. No finite computational check is presented as
a proof of the unbounded parameter statements.
