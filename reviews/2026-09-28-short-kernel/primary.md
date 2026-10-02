# Primary mixed-kernel audit and exact finite calibration

September 28, 2026. Live baseline supplied and checked by the coordinator:
`bcf959b45a35701f2fd710b1d86ca2cc3152e14c`.

**Status: HYPOTHESIS / proof candidate for the general argument; OBSERVED for
the explicitly frozen exact fixtures.** This is an AI-assisted internal
mathematical audit, not external independent proof certification. No novelty
claim or full Lonely Runner implication is made.

## 1. The discrete exception is real

For one open train

`B = union_m (s+m*p, s+(m+1/4)*p)`,

define

`A(t)=(1/4) sum_(r=0)^3 1_B(t+r*p/4)`.

The four quarter-period shifts visit the four quarter cells modulo p. If
`t-s` lies in `(p/4)Z`, none falls strictly inside `(0,p/4)` modulo p, so
`A(t)=0`. Otherwise exactly one does, so `A(t)=1/4`.

Thus the identity is almost everywhere, and **is not pointwise constant**.
The boundary exception cannot be removed by regarding the open train endpoints
as blocked: those endpoints are safe in the problem's convention. The frozen
calibration explicitly evaluates both kinds of point for each discrete label.

## 2. A continuous factor repairs the exceptional set

Let `P=max_i p_i`, choose a maximizing label k, and take independent variables

`U uniform on [0,P]`,

`D_i uniform on {0,p_i/4,p_i/2,3*p_i/4}` for `i != k`.

Put `X=U+sum_(i!=k) D_i` and

`H=P+(3/4)sum_(i!=k)p_i`.

For label k, conditioning on all the atoms leaves a full-period integral and
gives expectation exactly `1/4`. For another label i, condition on all atoms
except `D_i`. Its discrete average is the function in Section 1 evaluated at
`a+U+constant`. The exceptional U values in the compact interval `[0,P]`
form a finite subset of a translated quarter-period lattice, so have Lebesgue
measure zero. Integrating U therefore again gives exactly `1/4`. Finite sums
and bounded measurable integrands justify conditioning/integration directly.

Consequently, for every real translation a,

`E[M(a+X)] = 1`, where `M=sum_i 1_(B_i)`.

The conclusion is exact at every translation, although its discrete ingredient
is only an almost-everywhere identity. No period commensurability, integrality,
common starting phase, or limiting argument is required.

## 3. Positive density on the whole support interior

The 64 atom choices, with repetitions retained, have shifts T. A convenient
density representative is

`K(t)=(1/(64P)) sum_T 1_(T,T+P)(t)`.

This representative is zero at the support endpoints `0,H`. Begin with the
open interval `(0,P)`. Add one atom factor with step `d=p_i/4`. The four
translates of an interval `(0,L)` are `(r*d,r*d+L)`, `r=0,1,2,3`.
Since `d<=P/4<P<=L`, consecutive intervals overlap strictly. Their union is
therefore `(0,L+3d)`. Repeating for all three discrete factors proves that
the union of the 64 open boxes is exactly `(0,H)`. Hence the displayed K is
strictly positive at every interior point, including each internal box
endpoint, and

`integral_0^H K(t)[M(a+t)-1] dt = 0`.

This positivity statement is analytic. The finite checks additionally verify
the full piecewise-constant density partition for each declared fixture, not
merely a selection of sample locations.

## 4. Span and occurrence consequence

For any actual selected chain of open occurrences, let its union be `(A,B)`.
Right endpoints increase and each old endpoint lies strictly inside the next
occurrence; containment and skipped occurrence indices are allowed.

For at least two occurrences there is an open interval of positive overlap.
If `B-A>=H`, an H-window inside `[A,B]` can be placed so that this overlap
meets its interior. There `M-1>=0`, and it is positive on a nonempty open
subinterval. Section 3 then contradicts the zero integral. A one-occurrence
chain has width at most `P/4<H`. Thus every such chain satisfies `B-A<H`,
including exclusion of equality.

If the largest-period label appears h times, its first full occurrence and
last endpoint imply

`B-A >= (h-3/4)P`.

The lower bound is non-strict, which is sufficient. Combining it with
`B-A<H<=13P/4` yields `h<4`, hence `h<=3`. The inherited three-label bound
of seven then gives the intermediate bound `N<=8h+7<=31`.

The coordinator and separate geometry/challenge agents subsequently supplied
an **analytic post-protocol sharpening to 23**, using restrictions on the
three-label blocks when h=3. That sharpening is documented in their reviews
and the coordinator's main note. It did not alter this frozen computational
scope, and these fixtures do not test sharpness of 31 or 23.

The same strict-span argument gives a common-safe point in every closed
window of length H: an openly covered closed H-window would yield a finite
strict chain whose union starts before the window and ends after it, contrary
to the span bound. Openness and local finiteness of the four positive-period
trains supply that finite chain. Isolated safe endpoints are retained.

## 5. Frozen scope and primary implementation

The coordinator approved `protocol.json` before implementation/evaluation.
Its SHA256 is
`6cda7c02943bf88fbb315cba9adda3c318f367c26d8c381498d27c6fc8387f8b`.

Exactly the prior three auxiliary tiles and three prior perturbations are
used. For each of these nine fixtures the maximizing anchor is the least
index in a tie, atom multiplicity is retained, and translations are exactly
`0,1/7,H,H+1/7`.

`primary.py` sums exact rational lengths of intersections between each
translated P-box and the finitely many blocked occurrences meeting that box.
Dividing by `64P` produces each train expectation. It computes density by
direct open-box membership counts at every cell midpoint and every interior
breakpoint of the full 64-box endpoint partition. It separately evaluates
each non-anchor label's discrete average at `s_i` and `s_i+p_i/8`.

The only additional case is the predeclared auxiliary equality window:
all periods are `4/13`, starts are `0,1/13,2/13,3/13`, and `W=[0,1]`.
Here `H=1=width(W)`. The blocked trains tile the open intervals between
consecutive `j/13`; their common-safe points are exactly `j/13`,
`j=0,...,13`. Thus the guaranteed safe set may have zero duration even at
exact width equality. This case has only the declared event checks, with no
additional kernel samples or integrals. It is not a new common-start,
distinct-speed physical configuration.

The primary run passed:

| Check | Exact count and outcome |
| --- | --- |
| Per-train integrals | 144, all `1/4` |
| Multiplicity totals | 36, all `1` |
| Complete density cells | 219, all strictly positive |
| Interior density breakpoints | 210, all strictly positive |
| Support endpoints | 18, all `0` |
| Discrete boundary/interior points | 27 with value `0`, 27 with value `1/4` |
| Equality-window points | 14, all common-safe |
| Equality-window cells | 13, each multiplicity `1` |
| Equality-window safe duration | `0` |

Reproduce from the repository root:

```bash
python reviews/2026-09-28-short-kernel/primary.py
```

The script checks the frozen protocol hash before evaluating. The output
records its own code hash and exact rational values. The independent verifier
uses periodic occupancy primitives for train integrals and a signed event
sweep for density, rather than primary intersection summation and box counts.
`compare.py` subsequently matched every shared field: **1,943 numerical
fields, 14 Boolean fields, and 82 text fields**, plus nine mapped count fields,
the shared protocol hash, and the primary self-hash. `comparison.json` records
the script and output hashes. The verifier's 228 CDF endpoint values are
recorded separately as its internal normalization check; there is no primary
CDF calculation or cross-implementation CDF comparison.

```bash
python reviews/2026-09-28-short-kernel/verify.py
python reviews/2026-09-28-short-kernel/compare.py
```

There was no adaptive case, new physical configuration, speed/phase/word scan,
broader replay, publication, paid computation, outreach, main merge, or hourly
resumption. The exact fixtures calibrate the formulas and endpoint handling;
the universal claims rest on their proposed analytic arguments and still
require external mathematical review.
