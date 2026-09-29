# Slice-edge selector review

Date: 2026-09-29. Assigned frozen candidate: `8a967b30fcd73abd814e4c8f7f53f216c4b3f61e`.

**Assessment:** no mathematical failure found in the selector, its treatment of degeneracies, or its transfer to physical time. The proposed bound of 33 vertex checks plus 45 edge selections follows from the fixed-cell certificate. The main recommended change is a more precise, dimension-independent statement and proof of the slice-vertex lemma. The original full optimum formulas are unchanged; every proposed correction here concerns precision of exposition, not those formulas or their claim status.

This is separately tasked internal AI review, not independent human review or formal verification. The package remains a proof candidate under the repository's evidence rules.

## Scope and actions

Read the repository instructions and relevant continuity, the new review protocol, the spectrum note, the original protocol and pre-validation derivation, and the selector/edge-extraction source in `verify.py` and `ambient.py`. Inspected the archived vertex/edge data relevant to the bound. No mathematical program, new physical case, symbolic toy calculation, broad scan, or source-package regeneration was run. No original file or continuity document was edited.

This report supplies a self-contained theoretical argument and a static implementation review. It does not independently reconstruct all fixed cells, prove all residue inequalities, or re-evaluate the physical maxima. The numerical cell inventory is an explicit premise here and is assigned separate review.

## 1. A precise lemma covering degeneracies

**Lemma.** Let \(P\subset\mathbb R^d\) be a nonempty bounded polytope, possibly of lower affine dimension, and let \(H,L\) be affine real-valued functions. For an integer \(h\), if
\[
S_h=P\cap\{H=h\}
\]
is nonempty, then \(L\) has a maximizer on \(S_h\) which is either a vertex of \(P\), or lies in the relative interior of an edge of \(P\) on which \(H\) is nonconstant.

**Proof.** The nonempty compact polytope \(S_h\) has a vertex maximizing \(L\); choose one, \(p\). Let \(F\) be the minimal face of \(P\) containing \(p\), so \(p\) belongs to the relative interior of \(F\). If \(\dim F\ge2\), the linear part of \(H\), restricted to the direction space of \(F\), has a nonzero vector \(u\) in its kernel. Relative interior then gives some \(\varepsilon>0\) for which both \(p+\varepsilon u\) and \(p-\varepsilon u\) belong to \(F\cap\{H=h\}\). This contradicts the extremality of \(p\) in \(S_h\). Thus \(\dim F\le1\). Dimension zero means that \(p\) is an original vertex. Dimension one means that \(F\) is an original edge. In this second case \(H\) cannot be constant on \(F\), since then \(p\) would again be interior to a segment in \(S_h\). This proves the claim.

The proof uses relative faces and works without a full-dimensionality, simplicity, general-position, or transverse-intersection assumption. It covers a point polytope, a segment, a planar polygon embedded in three dimensions, and the full-dimensional cells in this package.

If the slicing plane contains an entire face, its interior does not become a new slice vertex. If the plane contains the whole polytope, the slice is the original polytope and original vertices suffice. Redundant or coplanar defining constraints do not affect the argument.

The note's active-facet explanation is correct in its intended setting but less robust as wording: for lower-dimensional polytopes, “facet” can mean a facet relative to the affine hull, and merely counting ambient facet normals then obscures the argument. The minimal-face proof avoids that ambiguity.

**Quantifier correction:** the necessary statement is that *there exists* an optimizing slice vertex of the stated kind. An arbitrary optimizing point need not lie on an original vertex or edge in the general lemma, because an optimal face can contain other points. The upper-bound sentence should therefore read: “If a slice has optimum strictly above \(1/7\), it has an optimizer at a \(z=1/6\) vertex or on an edge incident to such a vertex.” No proof of uniqueness is required.

## 2. Exact integer selection on one edge

For an edge \([P,Q]\), write
\[
A=H(P),\quad B=H(Q),\quad C=L(P),\quad D=L(Q).
\]
If \(A\ne B\), set
\[
n_- = \lceil\min(A,B)\rceil,
\qquad n_+ = \lfloor\max(A,B)\rfloor.
\]
The edge meets an integer plane exactly when \(n_-\le n_+\). On that edge,
\[
L=C+s(H-A),\qquad s=\frac{D-C}{B-A}.
\]
Choose \(n=n_+\) for \(s\ge0\), and \(n=n_-\) for \(s<0\). Then
\[
R=P+\frac{n-A}{B-A}(Q-P)
\]
maximizes \(L\) over **all** integer-plane intersections with this edge.

This argument includes negative values of \(A,B\), reversed endpoint order, integer endpoints, a single feasible integer, and \(C=D\). For a horizontal edge in the objective, every feasible integer intersection ties; either extreme gives an attaining point. Closed rounding preserves equality witnesses.

If \(A=B\notin\mathbb Z\), the edge supplies no feasible point. If \(A=B\in\mathbb Z\), the whole edge is feasible and an endpoint with maximal \(L\) suffices. Its endpoints are already covered by the original-vertex checks, so this extra endpoint evaluation is optional. A singleton cell is handled exclusively by its vertex check.

The statement that the selected extremal integer uses one floor or ceiling is valid as a selection description. The implementation computes both interval bounds to check nonemptiness. Thus “one selection per edge” should not be interpreted as a literal claim of only one rounding operation in that implementation. Prefer the operational wording: “Compute the ceiling of the lower endpoint and the floor of the upper endpoint; if the resulting interval is nonempty, choose its objective-favored endpoint.” This does not affect the fixed bound.

## 3. Completeness over all integer planes and the bound

The set \(P\cap H^{-1}(\mathbb Z)\) is compact; also, boundedness of \(H(P)\) implies that only finitely many integer planes intersect \(P\). If this set is nonempty, take a global maximizing slice and apply the lemma. An original vertex is explicitly checked. An interior edge point is weakly improved by that edge's selected extremal integer point. Every produced candidate is feasible, so the maximum among these candidates equals the maximum over all integer slices.

Apply this argument separately to every ambient cell, with \(H(x,y,z)=qx-y\) and \(L(x,y,z)=z\). Given the certified inventory of 33 vertex occurrences and 45 edge occurrences, at most 33 vertex integrality checks and 45 edge selections suffice. The number of candidate evaluation occurrences is at most 78, including repeated endpoints; duplicates do not threaten completeness or the upper bound.

This is a bound for recovering the maximum and at least one attaining witness. It does **not** assert that one chosen integer per edge lists every maximizing time. In particular, horizontal objective edges can have many tied integer intersections. The archive appropriately names its selector output `ambient_selected`; the separate direct method supplies `all_maximizers`. The note attributes the complete tight13 witness set and retained direct ties to that separate calculation.

The bound is independent of the number of physical lap labels and of the magnitude of \(q\). It is an arithmetic-operation/candidate bound, not a constant bit-time claim. Endpoint projections, chosen integers, and reconstructed lap labels grow with \(q\); the note explicitly acknowledges growing arithmetic bit lengths.

## 4. Static source review

`verify.py:ambient` implements the formulas above correctly: signed rational ceiling/floor; an empty-range check; the objective slope relative to \(H\), rather than endpoint order; interpolation by \((h-H(P))/(H(Q)-H(P))\); and a separate constant-projection branch. When the objective slope vanishes it chooses the upper feasible integer, which is sufficient for the maximum. Original vertices are tested independently. Its assertions enforce integer \(H\) and physical safety of each added point.

The edge-extraction criterion in `ambient.py` is also appropriate in dimension three: two distinct vertices sharing active constraints whose normals have rank at least two lie on a face of affine dimension at most one. Since that face contains the segment joining two distinct vertices, it is one-dimensional and hence an edge. Conversely, every edge of a bounded three-dimensional inequality representation has active-normal rank two, including the affine-hull constraints if the represented polytope has lower dimension. Singleton cells have no vertex pairs. Redundancy alone does not create a false diagonal by this criterion.

This is a review of the criterion and code logic, not a separate computation certifying the archived 45 edges.

## 5. Physical orbit and lap reconstruction

The selected point has \(x\in[1/8,1/2]\), \(y\in[1/8,7/8]\), and \(h=qx-y\in\mathbb Z\). Put \(t=x\). Then \(y\) is exactly the fractional part of \(qt\). Since each physical speed is \(v_i(q)=a_i+b_iq\),
\[
v_i(q)t=a_ix+b_iy+b_ih.
\]
For a point in the cell with ambient label \(m_i\), its phase after subtracting \(\ell_i=m_i+b_ih\) lies in \([z,1-z]\). Because \(z\ge1/8>0\), this interval is contained in \((0,1)\), so \(\ell_i\) is the actual floor/lap label, not merely an arbitrary integer representative. The reconstructed physical time therefore attains separation at least \(z\) for all seven speeds.

Conversely, any physical time with separation at least \(1/8\) can be reflected into the half-period, since all speeds are integers. Its \(x,y,z\) and unique ambient labels then satisfy the cell inequalities and integer-plane equation. Thus the geometry neither adds a spurious physical orbit nor discards an equality-safe physical time.

Integrality of \(q\), integer coefficient rows, common start, and the selected reference are genuine assumptions of this transfer and the reflection reduction. The argument does not extend the result to real \(q\), arbitrary phases, or every reference without additional work.

## 6. Threshold logic is not circular

The fixed cells encode only separations \(z\ge1/8\). Unconditionally, the selector exactly optimizes this restricted feasible set, or reports that it is empty. Calling its output the unrestricted physical optimum additionally requires a physical witness at or above \(1/8\).

Section 4 supplies that witness independently through explicit phase and integrality identities for each branch; the exceptional \(q=4\) has an explicit \(t=1/8\) witness. It does not assume that the selector has already found the global optimum. After these lower bounds, restriction to the fixed cells loses no maximum. The forward reference in Section 2 is therefore legitimate.

The upper-bound argument above \(1/7\) is likewise sound: if the claimed value \(m(q)\ge1/7\) were exceeded, the hypothetical larger maximum would be above \(1/7\), so the peak-edge reduction would apply. This remains valid when \(m(q)=1/7\); no strict lower-bound assumption is needed at \(q=3,10\). The separate full-cell treatment of \(q=4\) is necessary because its proposed maximum is below that cutoff.

For readability, the note could state the conditional selector lemma first and discharge its nonemptiness condition immediately after the witness construction. No mathematical change is required.

## Recommended disposition

Retain the selector and 33+45 bound. Replace the facet-count explanation by the minimal-face lemma, use existential language for the maximizing point, and keep the distinction between an optimum/witness selector, enumeration of all maximizers, and bit complexity explicit. No adverse result-level finding arose in this assigned scope.
