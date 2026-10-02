# Scope and representation audit

September 29, 2026. Separately tasked internal AI review of
`notes/CC_TWO_PARAMETER_WITNESS_2026_09_29.md`, under this directory's protocol.
The mathematical package at `b81d63f6e3a9355bc18bf990ed48f669d07ff7ca`
is preserved. This review adds no parameter scan, optimizer run, new reference
runner analysis, or external contact.

**Finding:** the two-segment package states its supported output accurately.
Its useful accomplishment is a short constructive certificate for a specified
two-parameter family. It does not by itself establish an originality claim,
optimality, all-reference loneliness, or general availability of such a
certificate. Standard affine geometry, integer contact and Bezout recovery
already express its mathematical operations. CC remains useful here as an
explicit record of what those operations preserve and require.

**Reconciled literature finding:** the completed
[general coverage review](general_coverage.md), with its primary source also
checked by the coordinator, establishes that Rosenfeld's Theorem 1 in
arXiv:2509.14111v2 already implies existence for all seven distinct positive
integer speeds, hence for this entire family. The contribution here is the
explicit compact construction candidate, not new existence coverage. Its
originality remains OPEN. This reviewer read that comparison; the source
theorem and computational verification are not independently reproduced here.

## 1. Claims that must remain separate

| Possible claim | What the package actually establishes as a proof candidate |
| --- | --- |
| Existence for this seven-form family | One common-start stationary-reference time with all seven distances at least 1/8, for every positive integer p != q. |
| Constructive selection | A fixed pair of closed, jointly safe segments; primitive normalization; at most two interval tests; explicit recovery of a physical time and all laps. |
| Exact separation | The selected time has minimum distance exactly 1/8 because one retained coordinate is on its band boundary. |
| Optimal separation | Not claimed: a selected value of 1/8 does not rule out another time with greater minimum distance. |
| Every runner in the displayed eight-runner configuration | Not established by this package. Subtracting a different reference speed changes the seven relative forms; applicability of the present segment certificate would require another argument. |
| Every physical safe time or every maximizer | Deliberately omitted. The two segments are a sufficient subset, not the full feasible set. |
| New existence coverage for this family | Not supported: Rosenfeld's inspected general theorem already implies this existence statement; see the reconciled comparison above. |
| Originality of the compact family-specific certificate | OPEN; prior existence coverage neither establishes nor rules out originality of these specific segments and recovery construction. |
| New mathematical machinery | Not claimed. The operations used are elementary affine and integer arithmetic. |
| Universal discovery procedure | Not established. The construction depends on safe segments whose existence and relevant directions were verified in this particular model. |

Positivity, integrality, common start, the selected reference and the closed
threshold are consequential hypotheses. The main statement excludes p=q
because the first two displayed speeds coincide there. The auxiliary primitive
pair (1,1) can remain in the finite arithmetic reduction without becoming an
eight-distinct-runner example. Scaling by a common gcd supplies original
integer pairs only after the physical time is divided by that gcd.

An existing six-coordinate lower bound cannot establish the seven-coordinate
claim merely because 1/8 is a weaker threshold than 1/7. The extra coordinate
must be safe at the same recovered time. Rosenfeld's general theorem does
imply the seven-coordinate existence statement, as the separate review now
establishes. The explicit two-segment certificate can still have explanatory
or computational value; that value is different from new existence coverage.

## 2. Exact translation into an established polyhedral framework

Primary source inspected: Matthias Beck, Serkan Hoşten and Matthias Schymura,
*Lonely Runner Polyhedra*, **Integers 19 (2019), A29**, published June 3, 2019,
[journal PDF](https://math.colgate.edu/~integers/t29/t29.pdf), accessed
September 29, 2026. Inspected §2, especially equation (5) and Proposition 1,
plus the two-speed illustration in §3 and the proof of Theorem 2(a) in §4.
The paper uses k for the number of nonstationary speeds; here k=7.

The source defines the polyhedron

\[
\mathcal P(v)=\mathbb Rv-[1/(k+1),k/(k+1)]^k
\]

and relates a lonely-runner instance to an integer point in that polyhedron.
It distinguishes constructing such a point from proving existence indirectly.
Its two-speed illustration uses Bezout, and Theorem 2(a) uses a segment of
length at least one to obtain an integer point. These establish clear precedent
for the constituent arithmetic and geometric ideas. They are not claims that
the present seven-form family satisfies that paper's separate sufficient
hypotheses; those hypotheses need their own check.

**Our translation, derived here:** let v be our seven speeds and let the
package return time t, physical phase vector f and lap vector ell. Its recovery
identity is

\[
tv=\ell+f,\qquad f\in[1/8,7/8]^7,\qquad\ell\in\mathbb Z^7.
\]

Consequently ell = tv-f is explicitly an integer point of P(v). Since all
speeds and t are positive and 0<f_i<1, the verified physical laps are also
nonnegative. The compact CC construction therefore supplies a concrete
certificate in that established framework. The source's polyhedron lives in
the full physical lap space; our two torus coordinates and segment labels
provide a family-specific route to one point of it. This is a translation of
the same physical witness, not a second independent proof of existence.

The fixed-torus work in the separate source comparison is the closer model
for the parameter-independent seven-form geometry. These two perspectives
can coexist: fixed torus coordinates organize this family, while the
polyhedral lap identity states the final physical certificate in general
speed-vector notation. No replacement of the current geometry is needed for
the stated one-witness output.

## 3. Conditional segment principle — deduction and source comparison

**Status:** elementary proof candidate rederived from the existing argument,
with the closer published precedent identified during this review. No new
instances were searched or computed to formulate it; no originality claim.

Vanshika Jain and Noah Kravitz, *Relative Lonely Runner spectra*,
**Combinatorial Theory 6(1) (2026), #1**, published April 20, 2026,
[published PDF](https://escholarship.org/content/qt3mx8w3js/qt3mx8w3js.pdf),
Proposition 7.1 and its proof on printed page 45, was directly inspected.
Their proof shows that two nonparallel segments in the optimal locus meet
all but finitely many one-dimensional subtori: transverse segment width
eventually exceeds the spacing between orbit leaves.

**Adaptation boundary:** the argument below uses one strictly descending
segment and restricts directions to positive P,Q, obtaining an explicit
width and finite exception inequality. Its segment need only be safe at a
specified threshold; it need not belong to the ambient optimal locus.
Therefore we reuse the contact mechanism but do not inherit Proposition
7.1's finite-optimal-spectrum conclusion. The segment's existence, joint
safety, exception coverage and physical recovery remain separate obligations.

**Post-protocol symbolic applicability check:** at the native ambient point
(x,y)=(1/6,1/6), the seven fractional phases are
(1,1,2,3,4,5,1)/6. Their minimum distance is 1/6, which exceeds the exact
1/8 attained everywhere on either selected segment. Hence neither selected
segment lies in the ambient optimal locus Z(U). Equivalently, the source's
distance satisfies D(U)<=1/3, whereas our segment points have D=3/8.
This independently checked substitution directly blocks that attempted use of
Proposition 7.1. It is an ambient comparison, not a new distinct-speed physical
case, an optimum calculation, or a parameter scan.

Fix integer coefficient rows (a_i,b_i), a threshold 0<delta<=1/2, and a
closed segment S with endpoints

\[
z_0=(x_0,y_0),\qquad z_1=(x_1,y_1)
\]

inside [0,1)^2. Suppose x_1>x_0 and y_1<y_0. Write
alpha=x_1-x_0>0 and beta=y_0-y_1>0. Suppose fixed integer labels m_i make
every phase a_i x+b_i y-m_i lie in [delta,1-delta] on the entire segment.
For a practical exact certificate, rational endpoints and endpoint band checks
suffice, by affinity.

For positive coprime integers P,Q, the primitive compatibility functional
H(x,y)=Qx-Py maps S monotonically onto

\[
I(P,Q)=[Qx_0-Py_0,\ Qx_1-Py_1],
\qquad |I(P,Q)|=\alpha Q+\beta P.
\]

If alpha Q+beta P>=1, set h=ceil(Qx_0-Py_0). Then h belongs to I(P,Q),
including width equality. With

\[
\lambda=\frac{h-(Qx_0-Py_0)}{\alpha Q+\beta P},\quad
(x,y)=(x_0+\lambda\alpha,\ y_0-\lambda\beta),
\]

we have 0<=lambda<=1 and H(x,y)=h. The primitive recovery equations in the
reviewed package supply a physical time with these phases. This yields a
delta-safe time whenever the interpreted speeds a_i P+b_i Q have the
nonzero/distinctness properties required by the chosen physical statement.
Those properties are separate from the segment argument.

The positive primitive pairs outside this guaranteed region satisfy

\[
\alpha Q+\beta P<1,
\qquad P<1/\beta,\qquad Q<1/\alpha,
\]

so they form a finite set determined by the segment. Every such pair can be
tested by the same closed integer interval condition; width less than one is
not itself a failure. If all actual misses are covered by a verified finite
fallback menu, that menu and S give a certificate over the whole stated
positive primitive domain. This last sentence requires coverage evidence for
the exceptions; it is not an automatic consequence of the width inequality.

For the existing P3 segment, alpha=1/8 and beta=1/4, giving exactly
(Q+2P)/8 and the already certified triangle Q+2P<8. Thus this abstraction
does not enlarge current physical coverage or change the previous proof.

**Limits of the abstraction:** strict opposite coordinate directions matter
for this particular finite reduction. A horizontal segment has beta=0, so
its insufficient-width region may contain unbounded P; a vertical segment
has the analogous problem with Q. If both coordinate increments have the
same sign, cancellation in Q Delta x-P Delta y can leave infinitely many
positive primitive pairs below the unit-width guarantee. These observations
do not imply actual physical failure; they show why finite exception coverage
cannot be inferred from an arbitrary nondegenerate segment. The principle
does not assert that any safe segment with the required direction exists in
an arbitrary coefficient model.

## 4. Cost and information audit

The representation correctly separates fixed geometric size from arithmetic
cost. Two interval tests do not eliminate gcd computation, extended Euclid,
or increasing integer bit lengths. Replacing Bezout by a modular inverse is
an alternative implementation of the recovery arithmetic, not a justification
for calling the complete algorithm a constant number of elementary steps.

The retained divisor, primitive orbit and lap map are essential. Without the
divisor, an integral value of qx-py may select the wrong torus component; the
preserved safe point for (p,q)=(2,4) already exposes that error. Without the
recovery map, a valid torus point does not identify its physical clock.
Without closed endpoints, the (1,4) fallback disappears. These are concrete
reasons to enrich the earlier ray record. They are not evidence that the
whole full-cell atlas must remain in the online certificate.

For this output, a smaller sufficient geometry plus the exact arithmetic
bridge is adequate. A switch to optimization or all-reference questions
changes the required retained information and must reopen the representation
assessment. The current certificate's success does not certify CC as a
general-purpose formal language or a universal discovery method.

## 5. A concrete next question

After reconciling the primary-source comparison, ask: **Can the existing
parent-only discovery procedure emit, along with its segment menu, a general
positive-parameter coverage certificate consisting of one descending safe
segment, its exact finite exception domain, fallback contacts and the physical
recovery map?**

The conditional principle above specifies a checkable success condition and
a useful failure output: no suitable descending segment found, or a named
uncovered primitive exception. A failure of that restricted discovery class
would trigger recovery of richer geometry rather than a false counterexample
to loneliness. This is a proposed next task, not work performed in this
review. External mathematical review and any originality claim remain open.
