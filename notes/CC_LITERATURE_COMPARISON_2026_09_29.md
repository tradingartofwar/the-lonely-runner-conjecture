# Compatibility Calculus: what the two-parameter certificate adds

September 29, 2026. Targeted primary-source comparison of the proof candidate
at `b81d63f6e3a9355bc18bf990ed48f669d07ff7ca`. Working branch inspected at
`a6a11e909ca1c2a062ed0ed137f476725b0198c8`.

**Conclusion:** the existence guarantee for our entire family is already
covered by the inspected eight-runner literature result. Our deliverable is
an explicit elementary construction candidate: two safe segments, a complete
exception argument, and physical time/lap recovery. A close published precedent
also exists for the segment-intersection mechanism. Originality of the specific
compact certificate remains OPEN.

This is a source comparison and an internal AI team assessment. It does not
reproduce another author's computational proof or promote our construction to
an externally verified theorem. The mathematical packages remain unchanged.

## 1. The exact claim being compared

Our family has seven moving speeds

\[
V(p,q)=(p,q,p+q,2p+q,3p+q,3p+2q,5p+2q),\qquad p,q>0,\quad p\ne q,
\]

with integer parameters, a common start, stationary selected reference, and
closed target distance 1/8. The [construction](CC_TWO_PARAMETER_WITNESS_2026_09_29.md)
returns one time. Its minimum distance is exactly 1/8; no optimum is asserted.

| Question | Result of this comparison |
| --- | --- |
| Does some safe time exist for every pair? | Already implied by Rosenfeld's inspected seven-moving-speed theorem. |
| Does the closest six-form analysis contain our first six coordinates? | Yes, exactly, with no coordinate permutation required. |
| Does six-form safety automatically survive the added seventh coordinate? | No; the archived (1,4) example supplies a direct failure. |
| Is the finite-exception segment mechanism without precedent? | No; Jain–Kravitz Proposition 7.1 contains a directly related argument. |
| What does our package explicitly supply? | A sufficient two-segment menu, two exceptional primitive pairs, closed endpoint handling, and time/lap recovery for the full positive domain. |
| Is that particular certificate original? | OPEN. The inspected sources and limited searches do not decide priority. |

The last five speeds strictly increase, exceeding the first two; p!=q makes
the first two distinct. Thus all seven are distinct positive integers. This
checks the general theorem's hypotheses directly, without a special symmetry
or a new reference-runner argument. The change from the A/B rays to arbitrary
positive parameters extends our explicit construction, rather than the
existence domain already covered in the literature.

## 2. Primary sources and the limits of the reading

**Rosenfeld.** *The lonely runner conjecture holds for eight runners*,
[arXiv:2509.14111v2](https://arxiv.org/abs/2509.14111v2), revised October 16,
2025; [PDF](https://arxiv.org/pdf/2509.14111v2). Section 1's positive-speed
formulation and Theorem 1 supply the 1/8 existence assertion for seven moving
speeds. Sections 4 and 6 explain its computer-assisted proof. We inspected
those passages, but did not reproduce the implementation or proof dependencies.

The version history, PDF title date, and HTML title date differ; the review
records them separately. Indexed AMS publisher content also reports electronic
publication on August 10, 2026, [DOI 10.1090/mcom/4243](https://doi.org/10.1090/mcom/4243).
Direct publisher access failed, so the theorem comparison uses the inspected
arXiv PDF and does not claim a journal-version comparison. Details are in
[general_coverage.md](../reviews/2026-09-29-cc-literature-comparison/general_coverage.md).

**Jain–Kravitz.** *Relative Lonely Runner spectra*, Combinatorial Theory
6(1), paper 1, published April 20, 2026,
[DOI 10.5070/C66165688](https://doi.org/10.5070/C66165688),
[published PDF](https://escholarship.org/content/qt3mx8w3js/qt3mx8w3js.pdf).
Section 6 uses our first six forms; its U^7 is a label for a six-coordinate
torus. Theorem 1.1 provides a general relative-spectrum description for a
proper two-dimensional torus. Proposition 7.1 and its forward proof, printed
page 45, link two nonparallel segments in the optimal locus to intersection
with all sufficiently long primitive orbits and finiteness of the relative
spectrum. Those definitions, statements and the relevant proof mechanism
were inspected; no full-paper audit is claimed.

**Cordella.** *Odd denominators in the Lonely Runner spectrum for six speeds*,
[arXiv:2609.03444v2](https://arxiv.org/html/2609.03444v2), September 8, 2026.
Section 5 treats exactly the six-form vector below with coprime parameters;
Theorem 5.3 states its near-tight consequence under ML<1/6. We inspected the
parameter definition, decomposition argument and theorem; its finite
computations were not reproduced. The seventh-coordinate obligation is not
included in that six-coordinate result. Appearances of 5A+2B in contact or
denominator expressions must not be read as an additional speed.

**Beck–Hoşten–Schymura.** *Lonely Runner Polyhedra*, Integers 19 (2019), A29,
published June 3, 2019,
[journal PDF](https://math.colgate.edu/~integers/t29/t29.pdf).
Section 2, equation (5) and Proposition 1 give the physical-lap polyhedron
and integer-point formulation. The separate scope reviewer also checked its
Bezout illustration and interval-contact precedent. We use the explicit
translation below, without importing unverified sufficient hypotheses from
other parts of that paper.

## 3. What translates exactly, and what does not

The first-six map is

\[
(x,y)\longmapsto(x,y,x+y,2x+y,3x+y,3x+2y)\pmod1.
\]

Its generators in both closest sources are (1,0,1,2,3,3) and
(0,1,1,1,1,2). For our original p,q, set d=gcd(p,q), A=P=p/d, B=Q=q/d.
The source's primitive clock tau becomes t=tau/d for the original speeds.
Their distance convention is D=1/2−ML; our threshold is D<=3/8. The technical
coordinate count in these sources is the number of moving speeds, so the
total runner count is one larger.

The appended phase is 5x+2y, the sum of the fourth and fifth forms. This
algebraic dependence does not make its distance constraint redundant. If
F6(t) is the old minimum, the new minimum is

\[
F7(t)=\min\bigl(F6(t),\|(5p+2q)t\|\bigr),
\]

so maximizing F6 does not ensure F7 safety. In the preserved (p,q)=(1,4)
control, t=4/13 gives first-six phases (4,3,7,11,2,5)/13, whose minimum
distance is 2/13. The seventh speed is 13 and its phase is zero. This uses
an archived example, not a new optimizer or parameter scan.

Appending (5,2) gives a proper two-dimensional torus in seven coordinates.
The first two coordinates ensure both injectivity of the parameter map and
a saturated lattice: an integral vector in the real span has integral first
two coefficients. Thus the general relative-spectrum framework is available
for a future stronger question, but its six-coordinate worked result cannot
be substituted for the seven-coordinate calculation.

Our physical certificate also maps directly to the polyhedral formulation.
Let v be the seven-speed vector, f the selected phase vector and ell the
physical lap vector. The retained identity gives

\[
tv=\ell+f,\qquad f\in[1/8,7/8]^7,\qquad
\ell\in\mathbb Z^7\cap\bigl(\mathbb Rv-[1/8,7/8]^7\bigr).
\]

This is our explicit construction of an integer certificate in an established
framework. It is the same witness translated into physical lap coordinates,
not an independent second proof.

## 4. Adapting the segment argument with the right guarantee

The following is our elementary threshold-level specialization of the
intersection mechanism, with the published precedent credited above.
The detailed proof is in
[scope_review.md](../reviews/2026-09-29-cc-literature-comparison/scope_review.md).

Suppose a supplied closed segment is jointly safe for fixed integer forms and
lap labels, and its endpoint increments are (alpha,−beta), with alpha,beta>0.
For positive primitive P,Q, projection by H=Qx−Py produces an interval of width

\[
\alpha Q+\beta P.
\]

Width at least one supplies an integer contact by rounding the lower endpoint.
Interpolation gives a point on that same safe segment; the primitive recovery
map gives its time and laps. The remaining possible exceptions satisfy

\[
\alpha Q+\beta P<1,
\qquad P<1/\beta,\quad Q<1/\alpha,
\]

a finite positive domain. Width below one does not mean failure: each remaining
interval must still be tested. Actual misses need separate fallback evidence.
The argument does not guarantee that a suitable safe segment exists in another
coefficient model. Horizontal, vertical, or increasing segments need not give
this finite exceptional domain in positive directions.

For our P3 segment, alpha=1/8 and beta=1/4 recover exactly Q+2P<8. The prior
proof already exhausts that triangle and repairs the two misses using P1.
This abstraction changes neither the physical coverage nor the old output.

The source's finite-spectrum conclusion requires optimal-locus segments.
Here that hypothesis actually fails. A post-protocol symbolic comparison
at the ambient point (x,y)=(1/6,1/6) gives seven phases

\[
(1,1,2,3,4,5,1)/6,
\]

with minimum 1/6. Both retained segments instead have minimum exactly 1/8,
so neither belongs to the ambient optimal locus. This calculation establishes
only a larger ambient value; it does not claim an ambient optimum or a new
distinct-speed physical case. It prevents a mistaken transfer of the spectral
theorem while allowing the intersection argument to be reused.

| Adaptation field | Current record |
| --- | --- |
| Source mechanism | Jain–Kravitz Proposition 7.1, forward proof: transverse segment width versus orbit spacing |
| Modification | Threshold-safe segment; positive primitive directions; explicit affine width and exception inequality |
| Preserved conclusion | Integer contact outside a finite exceptional domain, conditional on the supplied safe geometry |
| New obligations | Prove seven-band safety, cover every actual exception, preserve equality, recover time and laps |
| Unavailable conclusion | Finiteness of the optimal spectrum from these nonoptimal segments |
| Cost | Fixed segment tests plus parameter-dependent gcd/Bezout work and bit lengths |

## 5. Significance and the information-loss checkpoint

There are two material updates to the research narrative. First, a compact
construction and new existence coverage are different claims. Rosenfeld was
already listed in this repository's sources; carrying that fact into the
latest certificate's interpretation prevents progress in our construction
from sounding like a newly resolved LRC case. Second, the segment mechanism
has a closer published precedent than our previous notes explicitly credited.
This comparison supplies that attribution without rewriting the historical
proof packages.

The useful result we can show a reviewer is concrete: a short proposed
family-specific argument with exact exceptions and recoverable witnesses.
We have not established that its particular segment menu, rounding formulas,
or presentation have no earlier equivalent. Formula searches had weak recall;
failure to find a written match is not evidence of priority. Publication
metadata, theorem scope, computational reproduction, and certificate originality
remain separate evidence fields.

CC's role here is to carry the supported question, shared point, orbit,
divisor, labels, equality, recovery map, attribution and changed guarantees
when representations are compressed or adapted. The existing two-coordinate
model remains adequate for one witness. A complete spectrum or changed
reference would require a richer analysis.

## 6. Next bounded task

Make the parent-only discovery procedure emit a **two-parameter coverage
certificate**: a descending safe segment, its exact finite exceptional domain,
the integer contact table and verified fallbacks, plus physical recovery.
Start only with the already preserved parent geometry and 27 clipped records.
This is a development example whose successful segments are already known;
do not describe it as blind discovery or a new family test.

The procedure should report a specific limitation when it fails: no suitable
descending segment in its candidate class, or a named uncovered primitive
pair. Either result concerns that certificate class and indicates when richer
geometry is needed. It does not imply failed loneliness. Freeze choices and
resource bounds before a new run; the literature comparison itself ran no
discovery algorithm, broad physical scan, or optimizer.

The [review package](../reviews/2026-09-29-cc-literature-comparison/) contains
the protocol, three separately tasked reports, source metadata, search limits
and hashes. The coordinator independently opened the primary passages used
in this synthesis. External mathematical review and compact-certificate
originality remain open.
