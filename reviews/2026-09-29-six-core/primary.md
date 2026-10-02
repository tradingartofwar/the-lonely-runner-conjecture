# Stronger-threshold deletion and extension

September 29, 2026. Parent `da05361310a6e0d5607fdd7565ad226f637c8305`.

**HYPOTHESIS / proof candidate.** This is a proposed elementary implication
from a supplied stronger-threshold witness. It does not itself establish
that witness. Any use of a seven-total-runner theorem must be credited to
the primary source separately inspected by the literature reviewer.
Material AI involvement: derivation, endpoint audit, and writing.

## 1. General lemma

Let a finite nonempty core have speeds `v_i`, let `M=max |v_i|>0`, and
suppose some real time `t0` satisfies

`||v_i t0 + phi_i|| >= beta` for every i,

where `0<alpha<beta<=1/2`. The phases may be arbitrary in this auxiliary
lemma. Distance to the integers is 1-Lipschitz, so on the closed interval

`W=[t0-(beta-alpha)/M, t0+(beta-alpha)/M]`

every core runner is safe at threshold alpha. Its width is
`L=2(beta-alpha)/M`.

Add one runner of positive speed d and any phase. Its open unsafe
components have length `B=2 alpha/d`. A connected closed interval covered
by their union must lie inside one such open component. Consequently W
contains a jointly safe point whenever

`L>=B`, equivalently `d>=alpha M/(beta-alpha)`.

Equality is included: a closed interval with the same width as an open
blocker cannot be contained in it. At equality the implication only
guarantees a point, not positive safe duration.

For `d>alpha M/(beta-alpha)`, the usual one-train clipping argument also
gives a positive common-safe component of width at least

`min((1-2 alpha)/d, (L-2 alpha/d)/2)`.

The strict conclusion presumes alpha<1/2, already forced by alpha<beta.
This lemma concerns a supplied core window and one added runner; it is
not the conjecture for an arbitrary number of runners.

## 2. Seven-total to eight-total specialization

The physical core is `{1,4,5,a,b,c}`, with distinct positive integer
residuals a<b<c outside `{1,4,5}`. Thus c>=6 and c is its largest speed.
Conditional on a witness at threshold 1/7, put beta=1/7 and alpha=1/8.
The margin is `beta-alpha=1/56`, giving

`W=[t0-1/(56c),t0+1/(56c)]`, `width(W)=1/(28c)`.

The last runner cannot cover W when **d>=7c**. At strict inequality a
closed positive safe component has width at least

`min(3/(4d),1/(56c)-1/(8d))`.

Because the core includes speed 1, a witness selected in [0,1] lies in
`[1/7,6/7]`; the displayed W also lies in [0,1]. No clipping at the
period boundary is needed in this physical application.

Together with the inherited sufficient certificates, an uncertified
integer tuple would therefore obey

`a<=34, b<=47, c<=1565, d<7c`, hence **d<=10954**.

This last conclusion is conditional on the six-core 1/7 existence input
and on the prior proof candidates. It is a finite reduction, not a finite
verification: the remaining tuples have not been enumerated or certified.
No novelty claim is made for deleting a runner and using the threshold
margin to reinsert a sufficiently fast one.

## 3. Rational witness and exact final projection

For common-start positive integer core speeds and rational beta in
`(0,1/2]`, the stronger safe set over [0,1] is the intersection of finite
unions of closed rational bands

`[(j+beta)/v,(j+1-beta)/v]`, `j=0,...,v-1`.

If nonempty, it has a smallest point t0, which is rational. At beta=1/7
this point is a band endpoint `(7j+1)/(7v)` or `(7j+6)/(7v)` for some
core speed v. A finite intersection procedure can construct it exactly,
retaining singleton components. The theorem guarantees existence; this
description supplies an exact constructive selection without floating
point approximation. It does not imply efficient runtime for arbitrary
large speeds.

Given a rational W=[L,R] for the core, the final common-start runner is
handled without enumerating its complete schedule. Set `m=floor(dL)`
and `x=dL-m`:

- If `alpha<=x<=1-alpha`, choose t=L.
- If `x<alpha`, choose `t=(m+alpha)/d`.
- If `x>1-alpha`, choose `t=(m+1+alpha)/d`.

This is the earliest last-runner-safe point at or after L. If L is
unsafe, the projection advances strictly less than `2 alpha/d`.
Therefore `R-L>=2 alpha/d` guarantees t<R; if L is already safe,
t=L. All threshold comparisons are non-strict on the safe side.

A compact certificate consists of rational t0; core lap labels j_v
satisfying `beta<=v t0-j_v<=1-beta`; the rational window endpoints;
and the last-runner projection t with its lap label and `L<=t<=R`.
The Lipschitz implication verifies core safety on the whole window;
an independent implementation can additionally evaluate exact distances
at t and the endpoints. These are certification steps, not a search over
all reference runners.

## 4. Proposed bounded calibration, before executable evaluation

At the initial drafting of this section, no mathematical code had been
executed. The coordinator subsequently approved the separate direct
six-core protocol recorded in Section 6. The proposed final-speed
fixtures below were not selected or evaluated.

The inherited core `{1,4,5,6,7,11}` serves both archived final cases
d=13 (tight equality) and d=16 (positive opening). Hand interval algebra
gives its earliest stronger-threshold witness `t0=15/49`, in the
1/7-safe component `[15/49,13/42]`:

- The first core-1/4/5 interval at threshold 1/7 is `[1/7,6/35]`.
  Runner 6 leaves at most its left endpoint, which runner 7 blocks.
- The next core-1/4/5 interval begins at `2/7`. Runner 6 remains safe
  until `13/42`, runner 7 first becomes safe at `15/49`, and runner 11
  is safe throughout `[15/49,13/42]`.

The resulting conservative window is
`[1313/4312,1327/4312]`, of width `1/308`.
Neither d=13 nor d=16 meets the sufficient cutoff d>=77; they calibrate
the distinction between a window guarantee and final existence. For
example t=3/8 is a full safe equality witness for the archived tight13
case, but is blocked by runner 16 in the other case.

If the coordinator chooses one explicitly derived boundary fixture,
d=77 (=7c) tests equality of window width and blocker width; d=78 is an
optional strict-inequality fixture. These have not been evaluated, and
must not silently enter an inherited-only protocol.

## 5. Verification questions

1. Does the literature theorem actually supply six relative constraints
   at 1/7, rather than a different runner-count convention or a strict
   inequality? Non-strict 1/7 suffices for this bridge.
2. Does exact band intersection retain singleton stronger witnesses?
3. Does an independent endpoint partition reconstruct the same earliest
   t0 and all relevant safe components?
4. Does the final projection treat phase alpha and 1-alpha as safe?
5. Is an unproved positive-duration claim avoided at equality d=7c?
6. Are finite reduction, bounded calibration, and exhaustive coverage
   reported separately?

The general bridge is elementary but remains an internally supplied
proof candidate under the repository's evidence vocabulary. An exact
bounded implementation agreement would not certify the imported
literature proof or the full finite reduction externally.

## 6. Subsequently approved direct six-core verification

The coordinator froze and explicitly approved `PROTOCOL.json` before
the following executable evaluation. Its SHA-256 is
`25c818133f6e78054d14e82bf4b0f0c6b63c9dd7d1ca9a12071d83f878b891a2`.
The protocol fixes 36 (a,b) branches, c<=62, the exact inequality
`1/(4b)+1/(2c)>=w_a`, divisibility by 6 and 7 among the residuals,
and the specified one-sided eighth-anchor obstruction. It does not use
the later unique-seven-divisor pruning or tailored family windows.

The frozen formula generates exactly 27 triples. Successive exact
closed-band intersections at threshold 1/8 found positive components
for every row. The output contains 190 positive components and 50
isolated points. The minimum largest-component width is 3/448, attained
at (3,7,24), and the largest sufficient last-speed cutoff is 38. No
final d values were evaluated, and no other residual triples or phases
were included.

`primary_six_core.py` SHA-256:
`a47873db2bd515ddd2c383c324f9bc82a8647db890f2fdc977d2127023a65e32`.

`primary_six_core.json` SHA-256:
`f4718e3c3257efcd594111cbd0a363775e4eaa61ae62bea8ecead4b4678ffdc0`.

The independent verifier froze its output before opening the primary
code or output; only the intended field schema had been shared. The
comparison report records the subsequent field-by-field check. The
complete primary domain, all components, all widest ties, endpoint and
midpoint distances, and cutoff certificates are in the JSON;
`PRIMARY_TABLE.md` is its human-readable summary.

The table also separates two useful quantities. Core (6,7,11) has total
safe measure 29/1232 and largest component 1/112, while (3,7,24) has
larger total measure 53/1680 but smaller largest component 3/448. The
position and fragmentation of collective openings affect the final
runner's guaranteed window, even when total clear measure improves.
This is an observation on declared outputs, not a new evaluated domain.
