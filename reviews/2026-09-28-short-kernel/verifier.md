# Independent mixed-kernel verifier

2026-09-28. **HYPOTHESIS / proof-candidate review.** This is an
AI-assisted, separately structured mathematical and exact-arithmetic check,
not external mathematical review. The inherited 39-bound note, local rules,
and team brief were read. `README.md` and `HANDOFF.md` were not present in this
local review snapshot. No broad speed, phase, or word search is authorized.

The mathematical review below precedes execution. Bounded evaluations will
use only the coordinator's frozen protocol. No primary implementation will
be imported.

## 1. Independent formulas

Let `P=max_i p_i`, choose one label attaining the maximum, and give it a
continuous uniform average on `[0,P]`. For the other three labels use
independent uniform choices in `{0,p_i/4,p_i/2,3p_i/4}`. Write `T` for the sum
of these three choices, counting all 64 choices with multiplicity, and let

`H=P+(3/4) sum_(i other) p_i`.

The density is represented almost everywhere by

`K(x)=#{T : T<x<T+P}/(64 P)`.

The independent implementation will form its piecewise-constant cells by
sorting the signed events `(T,+1)` and `(T+P,-1)` with multiplicity. Integrating
the resulting slopes constructs a piecewise-linear CDF. This is separate
from evaluating train integrals by a primary box-overlap method.

For each train of period `p`, left-end phase `s`, define for all real `t`

`q=floor((t-s)/p)`, `r=t-s-p q`,

`A_(p,s)(t)=q p/4+min(r,p/4)`.

Here `0<=r<p`, including negative `t-s`. This continuous primitive has
derivative equal almost everywhere to the open train indicator. Its endpoint
values give the correct Lebesgue integrals regardless of open endpoint
conventions. The independently computed train average at anchor `a` is

`sum_T [A_(p,s)(a+T+P)-A_(p,s)(a+T)]/(64 P)`.

No primary function, train-overlap integration routine, or CDF formula is
needed for this calculation.

## 2. Discrete exceptions and the exact average

For a train with period `p`, the four equally spaced samples give average
`1/4` unless their base point lies in `s+(p/4) Z`. At such a base point all
four values are zero: the potentially occupied quarter has its two endpoints
excluded, and the remaining two samples lie outside it. Thus the discrete
average is pointwise at most `1/4`, and equals `1/4` almost everywhere.

Conditioning on all variables except this train's discrete variable and the
continuous variable leaves a finite sum of continuous uniform translates.
Each exceptional grid is countable, hence has probability zero. The
discretely averaged label consequently has expectation exactly `1/4`.
The label receiving the continuous average has expectation `1/4` directly
from averaging over its full period. Therefore `E M(a+X)=1` for every real
anchor, arbitrary real phases, and positive real periods. Ties for the
maximum are harmless: choose any tied label continuously and retain its
continuous variable for the measure-zero argument.

## 3. Positivity and endpoint handling

Start with the positive density on `(0,P)`. Adding one discrete variable of
step `d=p_i/4<=P/4` averages four translates of the current density. If its
current positive interval is `(0,L)`, where `L>=P`, the four intervals
`(j d,j d+L)`, `j=0,1,2,3`, overlap strictly, since `d<L`. Their union is
`(0,L+3d)`. Induction proves positivity at every interior point for the
open-box density representative, and in particular on every nonempty
piecewise-constant cell. The density's values at finitely many event points
do not affect integrals. No rationality assumption enters this proof.

For a strict selected chain with union `(A,B)`, positive overlap of two
successive intervals makes `M>=2` on an open subinterval. If `B-A>=H`, a
translate of `[0,H]` can be placed inside `[A,B]` with an overlap point in its
interior. Then `K(M-1)` is nonnegative almost everywhere and positive on an
open subinterval, contradicting its zero integral. This also excludes
`B-A=H`. The one-occurrence chain has span at most `P/4<H` directly.

Every closed window of length at least `H` contains a safe point: otherwise
the open blocking cover of the closed window produces a finite strict chain
whose union begins before its left endpoint and ends after its right
endpoint. That chain has span greater than or equal to `H`, a contradiction.
An endpoint or isolated equality point is safe when no other train blocks
it; treating blocked intervals as closed would invalidate this conclusion.

## 4. Count and physical-window corollaries checked algebraically

If the maximum-period label occurs `h` times, the span from its earliest
selected left endpoint to its latest selected right endpoint is at least
`(h-1)P+P/4=(h-3/4)P`, even with skipped laps. This subinterval lies within
the whole chain union. Hence

`(h-3/4)P<=B-A<H<=13P/4`,

so `h<4` and `h<=3`. Deleting those appearances leaves at most `h+1`
three-label pieces. The inherited three-label bound of seven then gives
`N<=h+7(h+1)<=31`. If the largest-period label is absent, the three-label
bound already applies.

For the inherited core window of width `3/32`, four positive residual
speeds all at least `104/3` give `H<=13/(4 v_min)<=3/32`. Thus integer
residual speeds at least 35 suffice under this candidate. This is a
sufficient condition, not an emptiness test when it fails, and it makes no
all-reference or full-conjecture claim.

## 5. Post-freeze analytic count refinement to 23

The coordinator supplied this refinement after freezing the finite protocol.
It requires no new fixtures or numerical evaluation. The reasoning below was
independently checked, preserving the status **HYPOTHESIS / proof candidate**.

Order the three remaining periods `q>=r>=s`. Suppose a strict three-label
piece contains at least six occurrences. The inherited three-label proof
makes the q label occur at most once. It must occur once, since a two-label
piece has length at most three. Its two flanking r,s pieces have combined
length at least five, each has length at most three, and hence both have
length at least two and one has length three.

Each r,s piece of length at least two contains the r label exactly once.
The length-three piece must have order `s,r,s`. The right-endpoint difference
between its two s occurrences is at least s. Applying the strict transition
bound to its two transitions gives

`s<(r+s)/4`, hence `r>3s`.

There are two r occurrences, one on each side of the q occurrence. Between
them there is at most one s occurrence before q and at most one s occurrence
after q. Their right-endpoint separation is at least r, but the strict
transition bound gives

`r<(q+r+2s)/4`, hence `q+2s>3r`.

Consequently `q>3r-2s>7r/3`, so `r<3q/7`; together with `s<r/3` this yields

`q+r+s<q+(4/3)r<11q/7<=11P/7`.

On the other hand, if the maximum-period label P occurs three times in the
full four-label chain, its union span is at least `9P/4`. The strict span
bound gives

`9P/4<H=P+(3/4)(q+r+s)`, hence `q+r+s>5P/3`.

These inequalities are inconsistent because `11/7<5/3`. Thus, when `h=3`,
every one of the at most four remaining three-label pieces has length at
most five; then `N<=3+4*5=23`. When `h<=2`, the inherited seven bound gives
`N<=h+7(h+1)<=23`. The zero-appearance case is included. This strengthens
the original 31 consequence without changing the kernel, width criterion,
or frozen exact-check scope. It does not claim sharpness.

## 6. Frozen execution scope and results

The coordinator approved the protocol before implementation/evaluation.
`protocol.json` is pinned by SHA256
`6cda7c02943bf88fbb315cba9adda3c318f367c26d8c381498d27c6fc8387f8b`.
It contains the three inherited tiles crossed with the exact, first-period
plus `1/1000`, and first-start minus `1/1000` variants. Each of these nine
fixtures has anchors `0`, `1/7`, `H`, and `H+1/7`; the convention is `a+X`.

`verify.py` imports only standard-library modules. It reads only the pinned
protocol, calculates train averages using the periodic primitive, constructs
all density cells and breakpoint values by signed-event sweep, and separately
generates threshold events for the sole auxiliary equality fixture. It never
imports primary code. `verifier_results.json` was written before reading the
primary output or implementation.

Reproduce from the review snapshot root:

```bash
python reviews/2026-09-28-short-kernel/verify.py
```

The exact finite results are **OBSERVED** within this declared scope:

| Check | Count | Result |
| --- | ---: | --- |
| Train integrals from periodic primitives | 144 | all `1/4` |
| Multiplicity expectations | 36 | all `1` |
| Complete open density cells | 219 | all positive |
| Interior density breakpoints | 210 | all positive |
| Support endpoint density values | 18 | all zero |
| Discrete boundary and interior averages | 54 | respectively `0` and `1/4` |
| CDF values at every density event | 228 | integrated total `1` in each fixture |
| Auxiliary equality-window event points | 14 | all safe |
| Auxiliary equality-window open cells | 13 | multiplicity exactly one |

The equality fixture has periods all `4/13`, starts `0,1/13,2/13,3/13`,
and window `[0,1]`, with `H=width=1`. Its safe points are precisely `j/13`,
`j=0,...,13`, and its safe duration is zero. The check evaluates only its
threshold events and intervening cells, as frozen; no kernel evaluation or
additional train integrals are run for this fixture. It is an auxiliary
arbitrary-phase case, not a physical common-start distinct-speed input.

The CDF values are a deterministic byproduct of integrating the authorized
density cells, not extra evaluation anchors. No adaptive fixture, scan,
physical speed configuration, or wider replay was added. Primary/verifier
comparison is performed separately by the primary investigator. These exact
checks calibrate algebra and endpoint conventions; the general identity,
positivity, count 23, and sufficient window theorem rest on their arguments
and remain proof candidates pending external review.
