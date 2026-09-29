# Orbit, gcd and physical recovery review — September 29, 2026

**Status:** separately tasked AI review of a proof candidate. No result-level
defect was found in the orbit equivalence or proposed recovery formula. This is
not human certification, formal verification or a novelty determination.
The finite checks below verify only the 18 inputs frozen in `PROTOCOL.md`.
The proofs in this note, rather than those controls, support the unbounded claim.

**Scope:** the stationary selected reference, common start, positive integer
parameters and coefficient rows `(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2)`.
This review inspects arithmetic compatibility and physical recovery; it does
not certify all other reference runners, an optimum or the complete safe set.
The coordinator's frozen protocol pins source branch head
`1696035e73bb53764f431237794cfca342dad002` and mathematical predecessor
`e37858ffd238a668682289280ee26c6c5e8a0646`.

## 1. Primitive orbit: necessity and sufficiency

Let positive coprime integers `P,Q` be fixed and let `0 <= x,y < 1`.
The point `(x,y)` is of the form `({P*tau},{Q*tau})` if and only if

\[
h=Qx-Py\in\mathbb Z.
\]

For necessity write `P*tau=x+A`, `Q*tau=y+B` with integers `A,B`.
Then `Qx-Py=PB-QA` is an integer. For sufficiency choose integers `r,s`
such that `rP+sQ=1`, and put

\[
T=rx+sy,\quad N=\lfloor T\rfloor,\quad \tau=T-N.
\]

The two exact identities are

\[
PT=x-sh,\qquad QT=y+rh.
\]

Consequently

\[
P\tau=x-sh-PN,
\qquad Q\tau=y+rh-QN.
\]

The terms after `x` and `y` are integers, and the coordinate convention
`0 <= x,y < 1` therefore proves the required fractional parts. It also gives
the physical base-speed laps exactly:

\[
L_P=-sh-PN=\lfloor P\tau\rfloor,
\qquad L_Q=rh-QN=\lfloor Q\tau\rfloor.
\]

The primitive clock is unique modulo one. If two clocks have the same point,
both `P*(tau-tau')` and `Q*(tau-tau')` are integral; their combination with
coefficients `r,s` makes `tau-tau'` integral. Safe points have `x,y >= 1/8`,
so their representative `tau` cannot be zero.

## 2. Physical laps, including the sign and floor correction

For a coefficient row `(a,b)` let `w=aP+bQ`, and suppose the ambient label
`m` gives the phase `f=ax+by-m` in `[1/8,7/8]`. Then

\[
w\tau=f+\ell,
\qquad
\ell=m+(-as+br)h-(aP+bQ)N.
\]

This follows by adding `a` and `b` times the identities above. Since `f`
is strictly between zero and one, the integer `ell` equals
`floor(w*tau)`. Both the sign of the `s` term and the floor correction
`-wN` are necessary. In particular, `T` need not be nonnegative:
the declared control `(P,Q)=(2,3)` has `(r,s)=(-1,1)`,
`T=-15/56`, `N=-1`, and `tau=41/56`.

Every Bezout pair is of the form `(r+kQ,s-kP)` for an integer `k`.
Indeed, differences satisfy `P*delta_r=-Q*delta_s`, and coprimality
forces `delta_r=kQ`, `delta_s=-kP`. Under this change,

\[
T'=T+kh,\qquad N'=N+kh,\qquad \tau'=\tau.
\]

The added `k*w*h` in the lap coefficient cancels the added `w*k*h`
in `w*N'`. Thus both time and physical laps are independent of the
chosen Bezout pair, not merely equivalent after forgetting labels.

## 3. Nonprimitive parameters

For general positive `p,q`, let `d=gcd(p,q)`, `P=p/d`, `Q=q/d`.
The physical orbit has the same image as the primitive one because
`(p*t,q*t)=(P*(d*t),Q*(d*t))`. Its correct compatibility condition is

\[
Qx-Py\in\mathbb Z,
\quad\text{equivalently}\quad
qx-py\in d\mathbb Z.
\]

After recovering the primitive clock `tau`, take `t=tau/d`.
For every original speed `v=ap+bq=d*w`, one has `v*t=w*tau`, so the
primitive physical lap formula applies unchanged. More generally,
the `d` preimages in `[0,1)` are `(tau+j)/d`, `j=0,...,d-1`, with laps
`ell+w*j`. The proposed selector needs only the representative `j=0`.

**Preserved failed fixture.** The frozen proposed negative-control point
`(x,y)=(7/16,1/4)` for `p=2,q=4` is safe on P3, but its raw orbit value is
`4x-2y=5/4`. It fails even the naive integer condition, so it does not
distinguish that condition from membership in `2Z`.

**Analytic replacement.** For `(p,q)=(2,4)`, choose on the same P3 segment

\[
(x,y)=(13/32,5/16).
\]

With the P3 labels `(0,0,0,1,1,1,2)`, its seven phases are

\[
(13,10,23,4,17,27,21)/32.
\]

All lie in `[1/8,7/8]`, whereas `4x-2y=1` is an integer outside `2Z`.
The primitive value is `2x-y=1/2`, so the point is not physically
recoverable. This is a concrete false positive caused by dropping the gcd
normalization. The replacement was derived from P3's line equation;
no scan was used.

## 4. Reflection and coordinate folding

For the original integer speed `v`, if `v*t=ell+f` with
`1/8 <= f <= 7/8`, then

\[
v(1-t)=(v-1-\ell)+(1-f).
\]

Thus reflection preserves all separations and gives the exact reflected
physical lap `v-1-ell`. This formula applies after scaling as well, using
the original speed `v`, not its primitive counterpart `w`.

The stored geometric fold `x <= 1/2` is not a physical-clock fold.
At `(p,q)=(2,3)` the selected point has
`x=13/28`, `y=11/56`, yet physical time is `41/56 > 1/2`.
The reflected time is valid even though the reflected torus point can
leave the stored geometric fold. No additional `t <= 1/2` condition may
be inserted into the recovery argument.

## 5. Distinct speeds and cost

For positive `p,q`, every speed after the first two exceeds both `p` and
`q`, and the remaining displayed speeds are strictly increasing.
Consequently the eight speeds including zero are distinct exactly when
`p != q`. The primitive diagonal consists only of `(1,1)`; the frozen
control on it is labelled as a repeated-speed auxiliary, not an
eight-distinct-runner configuration. Scaling preserves this distinction.

The selector performs at most two segment integer-hit tests after
normalization. The full algorithm also requires gcd reduction and
extended Euclid/Bezout recovery. Those procedures have input-dependent
iteration counts, and rational/integer arithmetic has input-dependent
bit cost. Therefore this extension must not inherit the earlier ray
description as a constant total number of arithmetic operations or as
constant running time. A correct compact statement is: **at most two
segment tests, plus gcd/Bezout computation and exact recovery.**

## 6. Reproducible bounded controls

Run from the repository root:

```sh
python reviews/2026-09-29-cc-two-parameter/orbit_checks.py
```

The separately authored checker uses exact `Fraction` arithmetic and only
the frozen list of 18 pairs: 17 distinct-speed configurations and the
labelled `(1,1)` auxiliary. It imports no coordinator or other reviewer
implementation. It uses the supplied segment-selection formulas as input
to the recovery checks; the general segment-coverage proof belongs to
the separate segment review.

`orbit_checks.json` records 126 selected phase/lap identities, 126
reflected identities, and 18 checks with the alternative Bezout pair
`(r+Q,s-P)`. All pass. The primitive witness at `(2,3)` rescales to
`41/112` for `(4,6)` with exactly the same selected laps; reflection
uses the original speeds and changes the lap list accordingly.

The deliberately wrong clock `t=x` is unsafe in 10 of the 18 controls;
`t=y` is unsafe in 15. They recover the wrong torus point in 12 and 15
controls respectively. A wrong clock can accidentally find another safe
point: at `(4,6)`, `t=x=13/28` is safe but does not recover the selected
point. Therefore testing only the safety of an alleged recovery is weaker
than checking its phase and lap identities.

For an explicit off-axis failure, `(p,q)=(2,3)` has correct time `41/56`,
whereas `t=x=13/28` has minimum distance `1/14`, and `t=y=11/56` has
minimum distance `1/56`. Both are below `1/8`.

## Information-loss checkpoint

Retained: the same torus point, primitive parameter direction, integer
orbit value, gcd scale, ambient row labels, physical laps, closed phase
bands and the source segment. The Bezout identity adds the physical clock
that neither coordinate can supply in the general case.

Omitted by this one-witness carrier: other safe points, all preimage
choices except one, optimum values, maximizing sets and other reference
runners. Those omissions do not affect the supported output. Dropping
the gcd scale, labels, floor correction or geometric/physical fold
distinction can affect the output; the explicit controls above expose
several such failures. Standard gcd, Bezout and affine arithmetic suffice
for the present operation. No new external framework or theorem is
needed, and none of these standard operations is claimed as a CC invention.

## Coordinator-note review

Read `notes/CC_TWO_PARAMETER_WITNESS_2026_09_29.md` after its first complete
draft, with particular attention to sections 1, 5 and 6 and the representation
and cost statements. No required correction was found. Equations (1)–(3)
retain the correct Bezout signs, floor correction and original-time scaling;
the primitive uniqueness statement and the `d` original preimages have the
right quantifiers. The `(2,3)` example agrees with this review's exact record.
The nonprimitive counterexample preserves both joint phase safety and failure
of actual-orbit compatibility. The cost statement explicitly excludes a
constant total arithmetic-operation claim. The theorem remains restricted to
the stationary reference, common start, positive unequal integer parameters,
one witness and the fixed seven rows. No extra computation or scan was used
for this final textual review.
