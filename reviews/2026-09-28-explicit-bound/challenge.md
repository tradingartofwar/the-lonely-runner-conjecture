# Adversarial audit of numerical extraction

Date: September 28, 2026. Pinned live baseline:
`99a4e77a369ff0dd520138605b0339deb263ae39`.

**Status: HYPOTHESIS / proof-candidate review.** This is materially
AI-derived internal review, not independent external certification. Scope:
four positive real periods, arbitrary phases, open intervals of width one
quarter of the corresponding period, strict increasing-right-endpoint
selected chains. Common-start integer residual speeds are a special case.
No speed, phase, or word scan and no new physical fixture was run.

## 1. What survived the initial challenge

I checked the previous main note and the affine local argument directly.
No defect was found in these particular points:

* A strict selected chain has connected open union even when an occurrence
  extends left of a preceding occurrence. The integral excess budget applies
  on the union of the whole occurrences. It therefore permits charging every
  whole selected slow interval; no first-interval clipping error occurs.
* The two-color and three-color bounds concern actual selected chains.
  Removing selected slow occurrences leaves contiguous selected subchains,
  so `N <= 8 N_a + 7` does not silently replace the actual chain by an
  irredundant covering chain.
* In the square-free argument, a length-|W| window from a chosen appearance
  in the first W to its matching appearance in the second has exactly the
  cyclic counts `q_i` as its destination counts. Skipped laps increase the
  same-label displacement. Maximizing `q_i p_i` therefore yields the stated
  contradiction even with containment.
* After normalizing the slowest speed to one, translating the left endpoint
  of the whole union changes the phases and leaves them on a compact torus.
  It does not preserve zero phase, and the proof correctly allows the
  resulting arbitrary phases.
* An unbounded endpoint count forces unbounded union length. Weak limit
  coverage, bounded recurrent potential, and exact tiling are compatible
  with safe equality contacts. They do not require continuity of the
  next-safe projection map.
* The maximal-cycle calculation needs a prepared anchored cycle for every
  possible maximizing label. The stated finite contact-neighborhood proof
  does this. Full coverage of each contact neighborhood, rather than coverage
  at the old contact alone, forces strict overlap after perturbation.

The high-ratio occupancy estimate is also consistent at its delicate
boundary: `x=n+3/4` minimizes `f(x)/x`, and its smallest value for `n>=1` is
`1/7` at `x=7/4`. The inclusive condition `d>=4a` causes no endpoint loss.

## 2. Audit of the explicit local radius

For a fixed anchored template the affine note uses
`rho=gamma/336`, where its minimum width satisfies `gamma>=1/12`.
The numerical implications are valid:

* Perturbed periods lie in `(1/6,3/2)` and the chosen shifts have absolute
  value below 2.
* Any occurrence meeting `[-1,3]` has label `|m|<=40` under that gauge.
* Each endpoint changes by less than
  `(40+1/8+1) rho < gamma/8`.
* A nominal nonadjacent successor starts at least `gamma` after the current
  nominal right endpoint, and nominal earlier right endpoints have spacing
  at least `gamma`. Both exclusions survive the endpoint errors.

Thus only the next nominal tile can be a moving successor. The buffered
horizon retains the consecutive labels throughout two cycles. The local
8, 12, 12 occurrence bounds follow. The weaker common radius
`rho*=1/4032` works for all three displayed templates, after normalization,
translation, label adjustment, and cyclic order choice.

This last phrase is substantive: a parameter tuple must be close in the
specified period-and-shift coordinates to an appropriate anchored template.
Raw phase differences modulo one and raw shift differences are not
interchangeable without an explicit gauge conversion. Likewise a translated
starting time changes the local phases. Neither the radius nor the local
move count establishes coverage of all normalized parameter space.

## 3. The numerical bridge that remains necessary

The preceding qualitative proof is not already an extraction algorithm.
In particular, the following shortcuts would be invalid without additional
lemmas:

1. Declare the three explicit template neighborhoods to cover all tuples.
   They cover only neighborhoods of exact tilings.
2. Replace qualitative convergence to a tiling by a numerical assertion that
   a sufficiently long finite cover lies in one such neighborhood, without
   deriving a threshold.
3. Infer near-disjointness or near-tiling from a small *average* overlap while
   allowing an uncontrolled local concentration of overlap in the horizon
   used by the contact argument.
4. Promote a bounded check of the known templates to a complete enumeration
   of all finite-window occurrence arrangements.

An explicit theorem can instead prove a finite-horizon stability modulus,
or an exact finite linear reduction whose coefficient and determinant bounds
are written down. This review will audit any proposed numerical bridge and
constant separately; the prior local radius alone is insufficient.

## 4. A quantitative return estimate available to the bridge

Here is an independently derived useful intermediate statement. Normalize
speeds as `1=v_a<=v_b<=v_c<=v_d<=4`. Let `R,Q` be positive integers. Divide
the three-dimensional phase torus for `(v_b,v_c,v_d)` into `Q^3` equal cubes,
and consider the `Q^3+1` points at times `jR`, `0<=j<=Q^3`.
Two lie in one cube, so their positive difference `tau` satisfies

`R <= tau <= R Q^3`,

and every speed phase displacement has circular distance at most `1/Q`
from zero; the `v_a=1` phase displacement is exactly zero.

The centered scalar primitive has circular Lipschitz constant `3/4`.
Consequently the four-runner potential obeys the conservative bound

`|H(t+tau)-H(t)| <= (3/(4Q)) sum_i p_i <= 3/Q`.

If a strict selected-chain union contains `[t,t+R Q^3]`, then `M>=1` there
apart from harmless threshold points and `H` is nondecreasing. Therefore

`integral_[t,t+R] (M-1) <= H(t+tau)-H(t) <= 3/Q`.

This provides *total* overlap control on the required fixed initial
horizon. It is uniform in phases and avoids an unquantified recurrence
rate. To use it, the interval must lie inside the open chain union; an
interior translation or harmless padding is required. It still needs a
quantified rigidity lemma converting that overlap control and full coverage
to an applicable template neighborhood or a direct contradiction.

The estimate is supplied as a proof candidate, with no numerical experiment
or assertion that it completes extraction.

## 5. New direct convolution argument: independent audit

The coordinator subsequently supplied the geometry agent's substantially
stronger argument. The numerical bridge above is no longer needed if this
argument survives external review. I independently derived it in the
following cube-integral form, without the qualitative tiling reduction.

Let `B_i` be the full periodic blocking set of label i, and write

`f(t) = sum_i (1_B_i(t)-1/4) = M(t)-1`,

`S = p_1+p_2+p_3+p_4`.

For every real t, Fubini's theorem and the exact mean of each periodic
indicator give

`integral_[0,p_1] ... integral_[0,p_4]
 f(t-u_1-u_2-u_3-u_4) du_4 ... du_1 = 0`.

Indeed, expand the finite sum defining f, and for summand i integrate in
`u_i` first. Its argument traverses one complete period, so that integral
is exactly zero for every fixed choice of the other three coordinates.
Endpoint values do not affect the integral.

Suppose a connected strict selected-chain union U has length at least S.
Choose `[x,x+S]` inside its closure, so `(x,x+S)` lies in U, and take
`t=x+S`. Then every integrand in the interior of the four-dimensional box
is nonnegative, because its time argument belongs to U and `M>=1` there.

There must be a nonempty open interval J inside `(x,x+S)` on which `M>=2`.
For an explicit endpoint proof, choose an occurrence containing the
midpoint. Its width is `p_i/4<S`, so at least one of its endpoints is
strictly inside `(x,x+S)`. Another selected open occurrence covers that
endpoint. Their interiors consequently overlap on a nonempty interval
inside `(x,x+S)`, and this interval can be used as J.

The set of box points for which `t-sum u_i` lies in J has positive
four-dimensional volume. To see positivity without appealing to a density
formula, take any `z=t-y` with `y in J`; then `0<z<S`, and the interior
point `u_i=z p_i/S` has coordinate sum z. A sufficiently small ball about
this point stays inside the box and has its sum in `t-J`.

The cube integral is therefore strictly positive, contradicting its exact
zero value. This proves the candidate span bound

`length(U) < S`.

The equality case `length(U)=S` is included: the support-window endpoints
can coincide with the two boundary points of U, but those are null sets;
the constructed positive-volume contribution lies strictly inside.

Equivalently, the convolution kernel formed from four normalized box
kernels is positive at every interior point of its support `[0,S]` and
annihilates f. There is no orientation problem: using `t-sum u_i` places
its time arguments exactly in `[x,x+S]` when `t=x+S`.

## 6. Audit of the numerical consequence 39

Put `p_max=max_i p_i`, and choose a label a with that period. Selected right
endpoints of a are distinct members of one arithmetic progression, so

`(N_a-1) p_max <= R_last,a-R_first,a < length(U) < S <= 4 p_max`

when `N_a>=1`. Thus `N_a-1<4`, and integrality gives `N_a<=4`.
The case `N_a=0` is immediate. Combining with the previously audited actual
subchain inequality yields

`N <= 8 N_a+7 <= 39`.

There is no accidental conclusion `N_a<=3`: the strict bound controls
`N_a-1`, not `N_a`. There is likewise no lost first occurrence in `N`.
The numerical statement bounds selected occurrences and hence advancing
scalar projections, irrespective of stationary calls and skipped laps.

For the stipulated eleven-call round, each completed round that begins
unsafe contains at least one advancing call. Checking joint safety at each
round's endpoint certifies termination within 39 rounds, or 429 scalar
calls: if the endpoint of round 39 were still unsafe, a fortieth round would
produce a forbidden fortieth advance. If certification instead requires an
additional unchanged round, 40 rounds or 440 calls is a conservative bound.
These are different stopping rules. Neither bound controls arithmetic bit
complexity or forces a witness inside an arbitrary supplied core window.

No defect was found in this direct argument after checking equality,
containment, kernel orientation and positivity, normalization, and the
`N_a` count. It is still an internal proof-candidate audit, not external
mathematical certification or a novelty assessment.

## 7. Independent exact calibration of the convolution identity

After the coordinator froze the nine-fixture protocol, I implemented
`challenge_verify.py`. Its protocol SHA256 is
`63d509f00dd73cfc54094030ed942d0e929215213a5e20604305dc4e99192d06`.
It imports no primary implementation and does not use the primary method's
alternating-subset quartic CDF. Instead it represents a cropped periodic
indicator by exact rational polynomial pieces and applies each normalized
box convolution by

`(U_p*f)(x) = [F(x)-F(x-p)]/p`, where `F'=f`.

Every crop contains the complete input support `[x-S,x]` of every declared
evaluation. Polynomial integration, coordinate translation, and all
coefficients use `fractions.Fraction`. The same recurrence, starting from
one box density, independently constructs the kernel's polynomial pieces.

The declared run succeeded:

* Nine inherited auxiliary fixtures; no additional fixture or scan.
* All 144 individual train integrals equal exactly `1/4`.
* All 36 summed multiplicity integrals equal exactly `1`.
* All 63 declared interior kernel values are strictly positive.
* All 18 declared endpoint kernel values equal exactly zero.
* The integral of each reconstructed kernel equals exactly one.

Reproduce from the repository root with

`python reviews/2026-09-28-explicit-bound/challenge_verify.py`.

Results are in `challenge_verification.json`. These are **OBSERVED** finite
calibration results. The unbounded-parameter claims rest on the analytic
argument, and successful program agreement is not external proof review.
