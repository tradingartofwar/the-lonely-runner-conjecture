# Primary exact core-window protocol

Status: declared before evaluation; awaiting coordinator approval.

Base context: research branch pinned by the coordinator at
`db2867ed65c4df3668f5275878f21ba400faff2b`, 2026-09-29.
Scope is the analytically reduced one-parameter core domain, not a residual
speed-tuple search.

## Frozen input and mathematical convention

- Exactly 31 integers: `a = 2, 3, 6, 7, ..., 34`.
- For each `a`, use common-start positive-speed core `{1,4,5,a}`,
  selected stationary reference 0, threshold `1/8`, and time domain `[0,1]`.
- Safety means `||v*t|| >= 1/8`; equality is included.
- All arithmetic uses Python `fractions.Fraction`; no floating-point decisions.

## Primary construction

For each core speed `v`, its complete closed safe set on `[0,1]` is the
union, for integer `j=0,...,v-1`, of bands

`[(8*j+1)/(8*v), (8*j+7)/(8*v)]`.

Begin with `[0,1]` and successively intersect with those unions in the fixed
order `1,4,5,a`. Canonicalize after each intersection: order by left and right
endpoint and merge all overlapping or touching closed intervals. Keep zero-width
intervals; the final output separates them as isolated safe points. This yields
the complete maximal closed connected components, not sampled times.

Among positive-width components, select maximum width `w_a`. If several have
this width, select the component with smallest left endpoint (the earliest
widest component). Record every tied widest component as well as the selection.

## Frozen output

For each `a`, record:

1. all positive-width maximal closed components and all isolated safe points;
2. the selected earliest widest component and its exact rational width `w_a`;
3. all widest ties and their count;
4. `B_a = ceil(7/(4*w_a))`;
5. exact endpoint safety distances for the selected component and each core
   speed, plus a midpoint safety certificate;
6. exact total safe measure and positive/isolated component counts.

The JSON additionally records exact domain, arithmetic, algorithm, tie rule,
source SHA-256 hashes, and the evaluation command. A Markdown table mirrors the
selected interval, width, and `B_a`. No threshold minimization using the stronger
integer separations is included in this primary evaluation.

## Threshold implication and limit

For sorted residual integers `a<b<c<d`, the proposed three-train span theorem
uses `T3 = 1/(4*b)+1/(2*c)+1/d`. Since `c,d>=b`,
`T3 <= 7/(4*b)`. Therefore `b>=B_a` is a sufficient core-window condition,
conditional on that theorem. Equality is accepted because the supplied
core-safe component is closed and the strict blocking-chain span is smaller
than `T3`.

The stronger separations `c>=b+1`, `d>=b+2` could replace the upper bound by
`1/(4*b)+1/(2*(b+1))+1/(b+2)`, but they will not be evaluated unless the
coordinator separately approves a frozen amendment. No `b,c,d` tuples, phases,
words, all-reference cases, or wider `a` values are evaluated.

## Checks and stopping rule

Primary internal assertions check sorted disjoint final components, positive
selected width, exact tie selection, component/point safety, reflection under
`t -> 1-t`, threshold ceiling inequalities, and certificate consistency.
These checks verify implementation invariants; a separately structured
coordinator-controlled check is needed for independent numerical comparison.

Stop after this finite domain, complete output, and independent comparison.
The table is **OBSERVED** exact finite arithmetic. Its implication for all
remaining fast residuals is a **HYPOTHESIS / proof candidate** conditional on
the span argument and pending independent mathematical review. No novelty,
all-reference, or full-conjecture claim is made. Material AI involvement is
explicit.
