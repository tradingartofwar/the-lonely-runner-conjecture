# Compatibility Calculus: two parent segments select a safe time

September 29, 2026. **Status: HYPOTHESIS / complete proof candidate with exact
internal checks.** This is coordinator-authored AI mathematics and code, not
independent mathematical review, formal verification or a novelty claim.

For the original ray

\[
A_q=(1,q,q+1,q+2,q+3,2q+3,2q+5),\qquad q\in\mathbb Z,\ q\ge2,
\]

two fixed edges of the six-coordinate parent model suffice to select one
physical time at which all seven moving runners are at distance at least
\(1/8\) from the selected stationary reference. There are eight total runners,
all starting together. The selector uses at most two integer roundings and
two interval feasibility tests, with no enumeration growing with \(q\).

The first edge succeeds for every \(q\ne5\); the second supplies \(q=5\).
Every returned time has separation exactly \(1/8\), so this solves the requested
one-witness question, not optimization. The already known seven-form spectrum
is not a premise of the proof.

## 1. Coordinates and a sufficient segment certificate

Use the fixed coefficient rows

\[
(a_i,b_i)= (1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2).
\]

At physical time \(t=x\), require \(h=qx-y\in\mathbb Z\), with
\(0<x\le1/2\) and \(0<y<1\). If the torus lap for a row is \(m_i\), then

\[
(a_i+b_iq)t=(m_i+b_i h)+(a_i x+b_i y-m_i).
\]

Thus the physical lap is \(\ell_i=m_i+b_i h\). It suffices to keep every
fractional form \(a_i x+b_i y-m_i\) in the closed band \([1/8,7/8]\).
This is a joint condition on one point; separate marginal ranges would not
suffice.

The elementary reusable operation is as follows. Suppose a labelled segment
\(y=c-dx\), \(x\in[l,u]\), satisfies all seven bands and \(q+d>0\).
Its actual-orbit values form the interval

\[
I(q)=[(q+d)l-c,(q+d)u-c].
\]

Choose \(h=\lceil\inf I(q)\rceil\). If \(h\le\sup I(q)\), the same segment
contains the physical point

\[
x=t=\frac{h+c}{q+d},\qquad y=c-dx.
\]

An interval of length at least one always contains this first integer.
The operation is sufficient for a supplied segment; it does not assert that
such segments exist for arbitrary runner configurations.

## 2. Two segments and their complete phase charts

Both segments lie at \(z=1/8\). The parent indices and labels are from the
[frozen six-to-seven atlas](CC_SIX_SEVEN_TRANSFER_2026_09_29.md) at commit
`a3be4b53111fc173c55c453de6e2bb28ebd7c389` (unchanged at the current base
`326347eafa512d2b49fb12bbcfd9a624a018ef6e`). The theorem below needs only the
displayed segments and band checks, not completeness of that atlas.

| Segment | Six-form parent laps | Seventh lap | Parameter interval | Line |
| --- | --- | --- | --- | --- |
| \(E_1\), parent P1 | \((0,0,0,0,0,1)\) | 1 | \(1/8\le x\le5/24\) | \(y=7/8-3x\) |
| \(E_2\), parent P3 | \((0,0,0,1,1,1)\) | 2 | \(3/8\le x\le1/2\) | \(y=9/8-2x\) |

The seven fractional forms, after subtracting those laps, are:

| Form | On \(E_1\) | On \(E_2\) |
| --- | --- | --- |
| \(x\) | \(x\) | \(x\) |
| \(y\) | \(7/8-3x\) | \(9/8-2x\) |
| \(x+y\) | \(7/8-2x\) | \(9/8-x\) |
| \(2x+y\) | \(7/8-x\) | \(1/8\) |
| \(3x+y\) | \(7/8\) | \(1/8+x\) |
| \(3x+2y\) | \(3/4-3x\) | \(5/4-x\) |
| \(5x+2y\) | \(3/4-x\) | \(1/4+x\) |

The endpoint values in that order are:

| Endpoint \((x,y)\) | Seven fractional forms |
| --- | --- |
| \(E_1:(1/8,1/2)\) | \((1/8,1/2,5/8,3/4,7/8,3/8,5/8)\) |
| \(E_1:(5/24,1/4)\) | \((5/24,1/4,11/24,2/3,7/8,1/8,13/24)\) |
| \(E_2:(3/8,3/8)\) | \((3/8,3/8,3/4,1/8,1/2,7/8,5/8)\) |
| \(E_2:(1/2,1/8)\) | \((1/2,1/8,5/8,1/8,5/8,3/4,3/4)\) |

Every entry lies in the closed band. Affinity proves the same for every point
on both segments. The fifth form on \(E_1\), or fourth on \(E_2\), fixes the
minimum distance at exactly \(1/8\). Relevant endpoints are retained.

## 3. Universal integer coverage and the selector

On \(E_1\), the actual-orbit interval is

\[
I_1(q)=\left[\frac{q-4}{8},\frac{5q-6}{24}\right],\qquad
|I_1(q)|=\frac{q+3}{12}.
\]

Consequently every \(q\ge9\) succeeds. For the remaining seven inputs, the
first integer and upper endpoint give a complete finite reduction:

| \(q\) | Lower endpoint | \(h_1=\lceil(q-4)/8\rceil\) | Upper endpoint | Accept? |
| --- | --- | --- | --- | --- |
| 2 | \(-1/4\) | 0 | \(1/6\) | yes |
| 3 | \(-1/8\) | 0 | \(3/8\) | yes |
| 4 | 0 | 0 | \(7/12\) | yes, lower endpoint |
| 5 | \(1/8\) | 1 | \(19/24\) | no |
| 6 | \(1/4\) | 1 | 1 | yes, upper endpoint |
| 7 | \(3/8\) | 1 | \(29/24\) | yes |
| 8 | \(1/2\) | 1 | \(17/12\) | yes |

For \(E_2\),

\[
I_2(q)=\left[\frac{3(q-1)}8,\frac{4q-1}8\right].
\]

At the sole remaining input \(q=5\), this is \([3/2,19/8]\), containing
\(h_2=2\). Recovery gives \(t=25/56\). Its physical laps are
\((0,2,2,3,3,5,6)\), and its physical phases are
\((25,13,38,7,32,45,39)/56\), all in \([7,49]/56\).

The complete selector can therefore be written:

```python
from fractions import Fraction

def safe_time(q):                 # precondition: integer q >= 2
    h = (q + 3) // 8
    if 24*h <= 5*q - 6:
        return Fraction(8*h + 7, 8*(q + 3))
    h = (3*q + 4) // 8
    if 8*h <= 4*q - 1:
        return Fraction(8*h + 9, 8*(q + 2))
    raise ArithmeticError("coverage certificate failed")
```

The preceding argument proves that the error branch is unreachable on the
stated domain. Closed tests preserve \(q=4,t=1/8\) and \(q=6,t=5/24\).
The [implemented selector](../reviews/2026-09-29-cc-bounded-selector/selector.py)
also returns the common point, orbit integer and physical laps from the
segment data. Reflection gives \(1-t\) with laps \(v_i-1-\ell_i\).

This proves the stated one-witness theorem candidate. The arithmetic-operation
count is bounded independently of \(q\); bit lengths, multiplication/division
costs and rational normalization are not constant-time claims. There is no
claim that two segments are minimal.

## 4. Exact checks and their limits

The [protocol](../reviews/2026-09-29-cc-bounded-selector/PROTOCOL.md) and
[prevalidation derivation](../reviews/2026-09-29-cc-bounded-selector/PREVALIDATION_DERIVATION.md)
were saved before executing the new code. The parent atlas had already been
inspected, so this is not a blinded discovery exercise.

- The geometry/coverage checker confirms both parent edges, 56 endpoint band
  inequalities, the width identity, the seven small cases and eight unbounded
  residue certificates. For \(q=8a+r\), the primary upper-end margin multiplied
  by 24 is \(16a+5r-6-24\epsilon_r\), where \(\epsilon_r=1\) for \(r\ge5\).
  On the successful residue domains its minima for \(r=0,\ldots,7\) are
  \(10,15,4,9,14,11,0,5\). The only omitted admissible input is \(q=5\).
- A separately structured physical checker imports neither the selector nor
  the atlas. It writes speed, time numerator/denominator and physical laps as
  integer polynomials in \(a\), then checks 112 closed-band inequalities on the
  full eight residue domains, plus the exceptional \(q=5\) witness. The phase
  inequalities reduce to affine polynomials with nonnegative slope and value
  at the stated lower endpoint. This is same-author verification, not an
  independent review.
- Direct physical checks reuse only archived \(q=2,\ldots,25\). All 24 selected
  times and their reflections pass, giving 336 exact distance evaluations;
  the two implementations select the same times. Archived optimum values are
  comparison data only. No new optimizer or larger physical scan was run.

Reproduce from the repository root:

```bash
python reviews/2026-09-29-cc-bounded-selector/verify.py
python reviews/2026-09-29-cc-bounded-selector/countercheck.py
```

Outputs, input hashes and reproduction checks are in the
[certificate directory](../reviews/2026-09-29-cc-bounded-selector/).
The universal claim rests on the displayed finite reduction or polynomial
certificates, not extrapolation from those 24 physical controls.

## 5. Representation adequacy and the next question

**Representation and version:** CC two-segment witness carrier, version 1.

**Question and requested output:** one physical \(1/8\)-safe time for every
integer \(q\ge2\) on the A ray, using a bounded number of rational operations.

**Domain, assumptions and next operation:** eight common-start runners, the
selected stationary reference, the ordered coefficient rows above, and closed
threshold \(1/8\). Next operation: round the projected orbit interval, retain
the same segment and invert to physical time and laps.

**Retained information:** two labelled parent segments, all seven joint phase
bands, integer compatibility, endpoint equality, universal coverage and the
inverse map. The seventh constraint is checked at the same point as the first
six; this avoids the prior marginal-range false positive.

**Omitted information:** all other cells and points, optimal values, most
maximizers and the complete safe set. These cannot be reconstructed from the
two-segment record alone. For example it selects \(7/40\) at \(q=2\), of
separation \(1/8\), while the archived optimum is \(1/6\). At \(q=4\) it selects
\(1/8\); even adding reflection does not recover the other isolated witnesses
\(3/8,5/8\). The \(q=10\) parent-face maximizers from the prior transfer remain
absent. None defeats this narrower one-witness claim.

**Richer source and recovery:** the pinned parent atlas and seven-form
certificate remain unchanged. To ask for all safe points or optimization,
recover all labelled parent/child polytopes and impose \(qx-y\in\mathbb Z\),
then use \(t=x\) and \(\ell_i=m_i+b_i h\). Source availability supplies a recovery
route; it does not make this compressed record lossless.

**Evidence, dependencies and limits:** the self-contained proof candidate
above, exact continuous endpoint checks and unbounded arithmetic certificates,
plus the declared finite physical controls. It establishes a sufficient
selected-reference family result, not a general Lonely Runner theorem,
optimality or independent certification.

**Failure test or trigger:** a violated joint band, an uncovered admissible
integer, an invalid physical inverse or a lost equality case refutes the
corresponding claim. Changing the ray, coefficients, reference, threshold, or
asking for all witnesses requires recovery and rechecking before reuse.

**Framework choice:** this modifies the current CC carrier from a full family
of conditional intervals to a two-segment sufficient cover for this question.
It uses elementary affine convexity and integer-interval rounding, rather than
requiring a new formal language. These are standard methods, not claimed CC
inventions. The source provenance and prior-art discussion in the
[original spectrum note](LTCM_EXACT_SPECTRUM_2026_09_29.md) and
[review](LTCM_ULTRA_REVIEW_2026_09_29.md) remain applicable context; no external
author's theorem is imported or altered here, and no fresh literature or
novelty assessment was performed. Existing frameworks remain candidates for
reuse or revision under the [working rules](CC_REPRESENTATION_RULES.md).

**Next bounded question:** review this small certificate, then ask how to
discover a sufficient collection of compatible segments from parent data.
The interval-width lemma explains why a supplied segment covers all sufficiently
large \(q\) on this ray; it does not force a suitable segment collection in a
new family. No further family or reference expansion is part of this result.
