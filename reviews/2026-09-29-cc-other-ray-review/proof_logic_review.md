# Proof-logic review of the other-ray candidate

September 29, 2026. Assigned frozen research head:
`12d08824ead7b772032ba240d0e858250fbd183c`.

**Verdict:** no result-level logical defect found in the proposed value or the
two-maximizer conclusion, conditional on the stated fixed-cell lemma and the
strict directed-loss comparisons. The minimal-face reduction is valid, including
lower-dimensional cells. The uniqueness argument can be made fully rigorous
without claiming that every maximizing point is an original vertex or edge.
Two sentences should receive explicit quantifiers in the review supplement;
their unqualified readings have concrete counterexamples within this same
family. Neither counterexample refutes the intended theorem.

This is a separately assigned same-platform AI review, not external human
certification, a formal proof, a novelty determination, or an endorsement of
claims beyond the displayed selected-reference integer family. Status remains
HYPOTHESIS / internally reviewed proof candidate.

## Inputs and limits

Read before reaching the verdict:

- `AGENTS.md`, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, and the current September 29
  portions of `README.md` and `HANDOFF.md`;
- this review directory's `PROTOCOL.md`;
- `notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md` and
  `notes/LTCM_OTHER_RAY_RECOVERY_2026_09_29.md`;
- the complete original upper checker,
  `reviews/2026-09-29-ltcm-other-ray-upper/verify_upper.py`;
- the `geometry` field of that checker's saved `verification.json`.

The written argument was read before the implementation. The saved geometry was
then consulted to locate a particularly simple counterexample to an overbroad
quantifier; its singleton property is proved directly below. Two stated small
diagnostics were evaluated with standard-library `Fraction` arithmetic using
the seven coefficient rows. No physical parameter scan, new family, literature
search, original-file edit, or remote mutation was performed. No original lower
checker or previous Ultra mathematical implementation was read or run.

This working copy has no `.git` directory. The original-spectrum note was
absent at my attempted read; the coordinator subsequently reported materializing
it. Neither that note nor the historical `ambient.json` was consulted for this
review. I did not independently verify the commit identity or rerun the upper
program end to end. The coordinator separately reported verifying the frozen
remote head and source hashes, including the historical geometry file. This
report neither imports the earlier ray's verdict nor reconstructs all ten cells:
that finite lemma is an explicit dependency, subject to the separately assigned
geometry review.

## 1. The actual orbit and folding are exact with the stated hypotheses

Write the coefficient rows as
`(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2)`.
For an integer `q >= 2`, a positive-separation physical point has
`x={qt}`, `y={t}` with `0<x,y<1` and

\[
H_q=x-qy=-\lfloor qy\rfloor\in\mathbb Z.
\]

Conversely, if `0<x,y<1` and `H_q` is integral, setting `t=y` gives
`qy=x-H_q`, hence `{qt}=x`. Every row then represents the physical speed
`aq+b`, since `(aq+b)y=ax+by-aH_q` and `aH_q` is an integer. The first-two-row
permutation produces exactly `B_q`. There is no missing congruence, orbit
component, or extra choice of time for this ray. The presence of the speed-one
coordinate makes `y` the physical time in the open unit interval.

Simultaneous reflection sends `(x,y)` to `(1-x,1-y)` and
`H_q` to `1-q-H_q`. Integral `q` and integral coefficient rows are essential to
this statement. It preserves the actual orbit and all seven distances. Folding
only `x`, while leaving `y` unchanged, would fail. For example, the `q=2`
witness at `t=10/13` has `(x,y)=(7/13,10/13)`. Replacing just `x` by `6/13`
would give `H_2=-14/13`; reflecting both coordinates gives
`(6/13,3/13)` and `H_2=0`.

The folded domain is consequently `x<=1/2`, not `y<=1/2`. At `x=1/2` the
closed folded domain can retain both members of a reflection pair; it is not
a unique representative system on that boundary. This is correctly relevant
at residue 3: peaks C and G have `y=1/6,5/6`. They give two physical times, not
four. In the three nonconstant branches the winning `x` is strictly below
`1/2`, so each reflection pair has exactly one folded representative.

The physical-lap transfer is also correct. If
`R_i=a_i x+b_i y-m_i` is in `[z,1-z]`, it is strictly between zero and one.
Thus `ell_i=m_i-a_i H_q` is the actual floor of `(a_i q+b_i)y`.
Reflection gives `ell_i' = v_i-1-ell_i`, with no endpoint ambiguity at positive
separation. Common-start, integral speeds, and the chosen stationary reference
must remain part of the statement; no arbitrary-phase or all-reference result
follows from this transport.

## 2. Finite labels, slices, and lower-dimensional cells

The first two labels must be fixed to zero, as the note explicitly says.
Their inequalities and `x<=1/2` imply

\[
1/8\le z\le x\le1/2,\qquad z\le y\le1-z.
\]

Every cell is therefore closed and bounded. Since all coefficient entries are
nonnegative, `0<ax+by<a+b`; its only possible label is an integer in
`0,...,a+b-1`. There are only finitely many label vectors. Positive `z` makes
the label unique even at a safe-band endpoint: the form never equals an
integer. In fact different label cells cannot share a point anywhere in this
positive-threshold model. Apparent double counting on the fold boundary is a
reflection issue, not a shared-label-cell issue.

The global boundary-plane enumeration has a valid completeness principle.
Every nonempty bounded polytope has a vertex. At a vertex, the active normals
of its defining inequalities span the whole ambient space, even if the
polytope itself has dimension zero, one, or two. Otherwise a nonzero vector
orthogonal to all active normals gives a sufficiently short feasible segment
in both directions; the finitely many inactive inequalities have positive
slack. This contradicts extremality. Hence some three active normals are
independent and a three-plane enumeration can find that vertex. One must not
discard rank-three systems merely because the resulting cell has dimension
less than three. The supplied algorithm does not do so.

For fixed `q`, physical points satisfy `-q<H_q<1`, so only the integers
`1-q,...,0` can occur. Thus there are finitely many compact slices, including
singleton slices and any tangential intersection. This finiteness establishes
existence; it is not a claim that explicitly visiting every slice takes a
constant number of operations.

## 3. What the minimal-face argument actually proves

Let `Q=P_m intersect {H_q=h}` and let `u` be **any vertex of Q**. Let `F` be
the minimal face of `P_m` containing `u`. Then `u` is in the relative interior
of `F`. If `dim F>=2`, the linear functional `H_q` has a nonzero kernel vector
on the tangent space of `F`, whose dimension is at least two. A short segment
through `u` in this direction stays in both `F` and the slicing plane. This
contradicts the fact that `u` is a vertex of `Q`. Therefore `dim F<=1`.

This proves that **every slice vertex** lies on an original vertex or edge.
Compactness then gives at least one optimizing slice vertex. It does not say
that every slice point, or every point of an optimal face, lies on an original
edge. If the slicing plane contains an original edge, its interior points
are not vertices of the slice; this degeneracy is already covered by the same
argument.

The sentence in Section 3 beginning “At heights above 1/7” should therefore
read:

> A slice vertex of height greater than 1/7 is either a peak vertex or lies on
> an original edge incident to a peak.

Here the fixed-cell lemma supplies the endpoint heights. A linear function on
an edge cannot exceed both endpoint heights, so an edge with both endpoints
at height at most `1/7` is excluded.

The restriction to slice vertices is substantive. At `q=2`, take

\[
(x,y,z)=\left(\frac{37}{80},\frac{37}{160},\frac3{20}\right),
\qquad H_2=0.
\]

Its labels are `(0,0,0,1,1,1,2)`, and the seven fractional forms, in the
unpermuted row order, are

\[
\frac1{160}(74,37,111,25,99,136,124).
\]

Their minimum distance is `24/160=3/20>1/7`. Exactly one cell inequality is
active: the upper band for row `(3,2)`. The floor and fold inequalities are
strict. Hence this actual-orbit point lies in the relative interior of a
two-dimensional face, not an original edge. It is not a maximizer: the supplied
`q=2` witness gives `2/13>3/20`. This is a counterexample only to the unqualified
all-high-points reading, not to the proof's required slice-vertex claim.

## 4. Strict edge losses do classify all global maximizers

Assume the finite lemma and full strict comparisons have been checked. The
lower witness and upper argument first establish the global value `F_B>1/7`.
For residues 0, 2, and 5 there is no compatible peak. Every slice vertex at
height `F_B` must therefore lie on a listed peak edge. All nonwinning edges
require strictly greater loss than `e_*`, hence have height strictly below
`F_B` at every compatible point. On the unique winning edge, height `F_B`
fixes `e=e_*`; it identifies a single point `u_*`. Nonzero projection change
ensures that this point lies on exactly one integer plane.

Now let `u` be an arbitrary **global maximizing folded point**, not assumed
to be a slice vertex. Put it in its cell and physical slice `Q`. The set

\[
G=Q\cap\{z=F_B\}
\]

is a nonempty exposed face of the compact polytope `Q`. Every vertex of `G`
is a vertex of `Q` at the global height `F_B`; the preceding paragraph forces
every such vertex to be `u_*`. Since a polytope is the convex hull of its
vertices, `G={u_*}` and consequently `u=u_*`. This also rules out an optimal
segment in a higher-dimensional original face. Applying the argument to the
cell and slice of each proposed optimizer handles the union of slices; no
convexity of that union is assumed.

For residues 1, 3, and 4, the same exposed-face reasoning applies directly to
each original cell at height `1/6`. Its unique peak is its only point at that
height. Singleton cells are below that height. The compatible peak list gives
A for residue 1, C and G for residue 3, and E for residue 4. Reflection yields
exactly `1/6,5/6`, accounting for the boundary duplication already discussed.

For the nonconstant branches, `u_*` has `x<1/2`, and its `y` value and its
reflection are precisely the two displayed times. They are distinct: in
residues 0, 2, and 5, respectively, the selected first-half times satisfy
`2(4q+3)<3(4q+1)`, `2(5q+8)<6(5q+3)`, and `4q<3(2q+1)` on their prescribed
domains. All these inequalities are strict. The constant branches plainly
have two distinct times as well.

One wording correction is needed in Section 6. “Any maximizing vertex of any
physical slice” must mean:

> Any vertex of any physical slice whose height equals the global value
> `F_B(q)` must be the winning point.

A vertex maximizing only its own slice need not attain the global value. For
an exact counterexample in a nonconstant branch, use `q=11` and
`m=(0,0,0,0,1,1,2)`. Its cell is the singleton
`(x,y,z)=(3/8,1/8,1/8)`, compatible with `H_11=-1`. To see the singleton
directly, its inequalities include

\[
z\ge1/8,\quad y\ge z,\quad 2x+y\le1-z,\quad 5x+2y\ge2+z.
\]

The last two imply `7z+y<=1`; together with the first two they force
`z=y=1/8` and then `x=3/8`. That point satisfies all remaining bands. It is
therefore the maximizing vertex of its cell's physical slice, but its value
`1/8` is below the supplied witness value `11/69`. This disproves the local
interpretation of the sentence while leaving the global interpretation intact.

## 5. Simpler presentation and retained distinctions

A shorter proof can avoid choosing a global optimizer across a union at the
outset. Given an allegedly better physical time, maximize `z` on just its own
compact cell slice. A slice vertex at least as high then contradicts the edge
loss bound. After establishing the value, apply the exposed-face argument
above to an arbitrary global maximizing point. This separates the two required
steps: an optimizing vertex exists; all optimal points are exhausted only after
the optimal vertices have been classified.

The essential finite geometric dependency is stronger than “there are seven
peaks”: it must also exhaust the nonpeak vertex heights and all incident edges.
The winning edge must be feasible up to `e_*`; minimizing losses along
indefinitely extended edges is sufficient for an upper bound but would not by
itself prove attainment. The note separately checks feasibility and transfers
the physical witnesses, so it does not make that mistake.

No information loss affecting this candidate remains after preserving: physical
time versus folded `x`; simultaneous reflection and its boundary duplicates;
ambient labels versus physical laps; all slice vertices versus all slice
points; local slice optima versus the global value; and finding one optimizer
versus classifying every optimizer. The generic edge selector should still be
described as a value/witness selector. Its full maximizing-time interpretation
in this candidate depends on the additional strict-loss and exposed-face
argument, not on endpoint enumeration alone.

## 6. Assessment of the proposed peak-cap simplification

After drafting the review, the coordinator relayed the representation reviewer's
suggestion to replace slice optimization by projecting the part of each cell
above height `1/7`. This is valid conditional on the certified peak/edge data;
the following tangent-cone argument makes the extra implication explicit.

For one three-dimensional cell, write its peak as `P` and its three incident
edge directions as `r_j=(alpha_j,beta_j,-1)`. The tangent cone at a polytope
vertex is generated by its incident edge rays, so the entire cell is contained
in `P+cone(r_1,r_2,r_3)`. All three edge lengths in the loss coordinate are at
least `c=1/42`, since `1/6-1/7=1/42`. The three points `P+c*r_j` therefore lie
in the cell. As every ray has last coordinate `-1`, the portion of this cone
with `z>=1/7` is precisely

\[
T=\operatorname{conv}\{P,P+c r_1,P+c r_2,P+c r_3\}.
\]

Cone containment gives `P_m intersect {z>=1/7} subset T`; convexity and the
four displayed feasible vertices give the reverse inclusion. Thus the cap is
exactly this tetrahedron. This proof avoids assuming without justification that
all original vertices on the cutoff plane must already be adjacent to `P`.

At a fixed positive loss `e<=c`, every cap point has the form
`P+e sum_j lambda_j r_j`, with nonnegative `lambda_j` summing to one. Hence

\[
H_q\in[h_0+e\,d_{\min},\ h_0+e\,d_{\max}],
\qquad d_j=\alpha_j-q\beta_j.
\]

If the peak is not compatible, the first possible downward integer hit has
loss `rho/(-d_min)` when `d_min<0`; the first upward hit has loss
`(1-rho)/d_max` when `d_max>0`. Omit any unavailable direction. Only these two
extreme rays need remain in the explanatory comparison, at most fourteen
candidates across seven peaks. This is a reorganization of the already bounded
certificate, not a new scan or a theorem about arbitrary families.

For uniqueness, an endpoint of this projected interval has a unique preimage
in the cross-sectional triangle exactly when its extreme `d_j` is unique.
Tied extreme rays can produce an entire edge of contacts, so a claim that
projection endpoints automatically identify one point would be false. Here the
existing strict separation of all nonwinning directed losses excludes such a
tie at the winning first contact, as well as ties with other cells or the
opposite direction. Consequently the cap proof can establish both the upper
bound and the unique folded optimizer. Compatible-peak branches are handled
at `e=0` exactly as before.

The cap argument is a sound optional simplification. The scoped slice-vertex
lemma and the two quantifier corrections above remain valid and should remain
in the record rather than being obscured by the shorter presentation.
