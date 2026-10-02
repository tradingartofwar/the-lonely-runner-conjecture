# Independent challenge: fixed anchor menus and bounded lap choices

September 28, 2026. Baseline supplied by coordinator:
`2f15767ef7a5cd78c19a6606f24b2e00a51a6805`.

This review was derived without reading the coordinator's new calculation or
implementation. It checks the displayed common-displacement criterion in
`notes/COMMON_DISPLACEMENT_CERTIFICATES_2026_09_28.md` and attacks the completeness
question it explicitly leaves open. It does not find a defect in that sufficient
criterion. The defect is in a possible stronger claim that the frozen anchor
menu must always contain a successful first-lap itinerary.

Status: supplied mathematical proof candidate under repository governance;
exact reproduced computation for the one declared numerical construction.
This is internal AI review, not independent human validation. No novelty or
published-frontier claim is made.

## 1. Every small-denominator anchor can fail simultaneously

Use eight common-start runners, reference speed zero, threshold `delta=1/8`,
and speeds

`{0,1,4,5,6,7,q,8q}`, where `q` is a positive multiple of 840.

There are 22 distinct rational anchors modulo one with reduced denominator at
most eight. Since `840=lcm(1,...,8)`, both `q` and `8q` collide at every anchor.
In either time direction their first closed safe displacement intervals are

`q: [1/(8q),7/(8q)]`,

`8q: [1/(64q),7/(64q)]`.

The first entry of the slower runner exceeds the first exit of the faster one
by `1/(64q)>0`. Thus the pair already has empty first-lap intersection. Adding
the remaining five constraints cannot repair it. All 44 anchor/direction
choices fail, including all equality endpoints. This is a strict incompatibility,
not the disappearance of a duration while an endpoint survives.

The ratio condition for this pair mechanism at eight runners is more generally
`fast/slow>7`. At ratio seven the first bands touch, so replacing the strict
comparison by a non-strict one would lose the endpoint distinction.

This disproves completeness of the finite menu with first safe laps, assuming
the supplied construction and argument survive review. It does not disprove the
criterion as a sufficient condition, and it says nothing against loneliness of
the constructed configuration.

## 2. Direct positive component, with every endpoint checked

Let `a=17/56`. The five fixed moving speeds `1,4,5,6,7` are safe throughout

`[a,5/16]=[a,a+1/112]`.

At `a` their phases are respectively

`17/56, 3/14, 29/56, 23/28, 1/8`.

Their forward exit displacements from their current safe laps are

`4/7, 37/224, 1/14, 1/112, 3/28`.

Therefore all five are strictly safe for `0<s<1/112`. This statement follows
from direct lifted phase inequalities; it assumes no result about the final
seven moving runners.

For any positive multiple `q` of 56, both variable runners collide at `a`.
Set

`I=[a+9/(64q), a+15/(64q)]`.

On this interval the slow runner's phase lies in `[9/64,15/64]`, strictly
inside `[1/8,7/8]`. The fast runner traverses the second safe lap, with lifted
increment in `[9/8,15/8]`. Its phase is exactly `1/8` and `7/8` at the left
and right endpoints, and strictly safe between them.

Since every positive multiple of 56 is at least 56,

`0<9/(64q)<15/(64q)<1/112`.

The fixed core is strictly safe on the entire closed interval. Hence `I` is a
valid closed lonely interval, its interior is strict, and its width is
`3/(32q)>0`. In fact it is a complete local connected component of the full
safe set: immediately outside either endpoint the fast runner is unsafe,
while all other moving runners have positive safety margin there.

The lower-bound condition before imposing divisibility is `q>105/4`; thus the
positive-multiple-of-56 assumption is more than enough. No claim that it is a
necessary condition is intended.

At the sole numerical control `q=840`,

`I=[5443/17920,1089/3584]`, of width `1/8960`.

## 3. Fixed finite lap budgets have the same obstruction

The coordinator proposed the following extension after this review's first
derivation; I checked it symbolically rather than adding a numerical scan.

Let a finite rational anchor menu be prescribed, and permit at most the first
`B` safe laps of each runner after an anchor, where integer `B>=1` is fixed in
advance. Take `q` to be a positive common multiple of 56 and every reduced
anchor denominator, and use the family

`{0,1,4,5,6,7,q,8Bq}`.

At each anchor both special runners collide, in either direction. Even the
last of the fast runner's first `B` safe laps ends at

`(B-1/8)/(8Bq)=1/(8q)-1/(64Bq)`.

This is strictly before the slower runner first becomes safe at `1/(8q)`.
Consequently no choices among the permitted laps can produce a common time.
This applies whether one intersects corresponding ordinal laps or permits
arbitrary mixtures among the first `B` laps. Endpoints do not close the strict
gap. Runner-specific finite budgets are covered by taking their fixed maximum.

Yet the same configuration has the explicit positive component

`I_B=[a+(8B+1)/(64Bq), a+(8B+7)/(64Bq)]`, `a=17/56`.

The slow phase is in `[1/8+1/(64B),1/8+7/(64B)]`, strictly safe. The fast runner
uses safe lap ordinal `B+1`, with increment `[B+1/8,B+7/8]`. The upper time
displacement is at most `15/(64q)<1/112`, so the fixed five-speed core remains
strict. The width is `3/(32Bq)>0`, with only the fast runner at equality at
the two endpoints. This is a symbolic family, not a search over `B` or `q`.

The exact negated assertion is that some prescribed finite rational menu and
fixed speed-independent finite lap budget suffice universally for all positive
integer configurations. The construction does not exclude an adaptive budget,
speed-dependent anchors, or arithmetic selection of noninitial lap labels.

## 4. Anchor and cost qualifications

The rescue anchor `17/56` lies outside the original denominator-at-most-eight
menu. Therefore the phrase "second lap repairs the frozen menu" would be
inaccurate if it suppressed that anchor change.

There is a precise way to state the rescue using the already allowed anchor
`2/7`. Since `17/56=2/7+1/56`, the slow runner uses zero-based safe-lap index
`q/56`, and the fast runner uses index `Bq/7+B`, relative to its colliding lap
at `2/7`. All fixed-core runners use the same current or first safe laps as in
the old common-displacement construction. The interval above is obtained by
intersecting these arithmetic choices. The labels grow with the input, so this
is not a finite uniform budget rescue.

Computing these explicit integer labels requires no traversal of the skipped
laps. That is an implementation/property-of-this-formula observation, not a
uniform constant bit-complexity claim. Arithmetic cost still depends on the
bit lengths of `B` and `q`; finding useful labels for arbitrary configurations
remains open.

### Post-protocol analytical refinement: an anchor already in the menu

After freezing the initial construction, the coordinator identified a simpler
same-menu rescue. I checked it separately. At anchor `3/8`, moving backward, the
fixed core's exit displacements are

`1/4, 3/32, 3/20, 1/48, 1/14` for speeds `1,4,5,6,7`.

Thus the entire core is strictly safe for backward displacements `0<s<1/48`,
inside the closed common safe interval `[17/48,3/8]`. Both variable runners
collide at this anchor whenever `8|q`, as for every positive multiple of 840.
The interval

`[3/8-(8B+7)/(64Bq), 3/8-(8B+1)/(64Bq)]`

is therefore a positive lonely component of width `3/(32Bq)`. The upper
displacement is at most `15/(64q)<1/48` when `q>45/4`, so the constructed
family satisfies the core condition strictly. The slow runner uses its first
safe lap and the fast runner uses ordinal `B+1`; both endpoint equalities
belong only to the fast runner. For `B=1`, changing the fast runner to its
second safe lap repairs this one menu anchor with no anchor change.

This strengthens the diagnosis without changing the physical input. It is a
post-protocol analytical refinement, not a prediction from the frozen first
calculation. The original `17/56` certificate is retained. For arbitrary finite
menus not containing `3/8`, no claim that this rescue anchor belongs to them is
intended.

## 5. What changed conceptually

The old fixed-witness obstruction only makes a runner collide at each
prescribed rational witness. By itself it does not refute the newer method,
whose actual witness time may move away from the anchor.

Here both colliding runners are allowed to move. Their speed ratio makes their
selected future safe intervals incompatible. Thus adaptive displacement within
initial laps does not remove the denominator-multiple obstruction. A valid
opening can require a different combination of lap labels, even when a small
calculation locates those labels directly.

This is an answer about completeness of a certificate class, and an explicit
selected-reference lonely interval in a constructed family. It neither proves
nor disproves the full Lonely Runner Conjecture, nor establishes every reference
runner's condition in this family.

## 6. Independent reproduction

Run `python -S -B reviews/2026-09-28-anchor-obstruction/verify.py` from the
checkout root. The file imports only Python's standard library. It reconstructs
safe components by evaluating rational threshold events and every intervening
cell, preserving isolated endpoints. It does not import the sufficient-condition
formula or the coordinator's implementation.

The main fixed numerical scope is `q=840`, `B=1`: all 22 anchors, both directions,
all 308 individual first components, plus a direct threshold-cell reconstruction
of a small neighborhood around the proposed positive component. It also checks
endpoint equality/strictness and relative lap labels from `2/7`. The same physical
input verifies the post-protocol `3/8` rescue locally. The frozen ratio-seven
boundary diagnostic verifies an isolated local contact, while `B=10^12` verifies
the last-early-lap gap and three exact points of the written later interval with
no lap enumeration. The symbolic arguments above, rather than those finite
counts or three point checks, supply the unbounded and interval-wide steps.

No broad speed search, all-reference search, full-period safe-set reconstruction,
outside outreach, publication-status promotion, or hourly automation was used.
