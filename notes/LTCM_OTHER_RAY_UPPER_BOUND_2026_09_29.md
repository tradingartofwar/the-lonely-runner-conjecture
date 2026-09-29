# A matching contact-cell upper bound for the other LTCM ray

September 29, 2026. Base commit: `44bd7854cd14c15cc52d991a0c61a22295af1234`.

**Status: HYPOTHESIS / complete proof candidate with an exact finite polyhedral
certificate.** This closes the upper-bound gap identified in the
[frozen recovery note](LTCM_OTHER_RAY_RECOVERY_2026_09_29.md). It does not promote
the result to an independently reviewed theorem. AI materially supplied the
argument, implementation, checking, and writing. No novelty claim is made.

## Statement and scope

Select the stationary reference in eight common-start runners and put

$$
B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2),\qquad q\in\mathbb Z,\quad q\ge2.
$$

This is the ray V(q,1), after permuting its first two coordinates, in

$$
V(p,q)=(p,q,p+q,2p+q,3p+q,3p+2q,5p+2q).
$$

Define

$$
M_B(q)=\max_{0\le t\le1}\min_{v\in B_q}\|vt\|.
$$

The complete candidate result is

$$
M_B(q)=F_B(q)=
\begin{cases}
\dfrac{2q}{3(4q+1)},&q\equiv0\pmod6,\\[4pt]
\dfrac{5q+2}{6(5q+3)},&q\equiv2\pmod6,\\[4pt]
\dfrac{q}{3(2q+1)},&q\equiv5\pmod6,\\[4pt]
\dfrac16,&q\equiv1,3,4\pmod6.
\end{cases}
$$

Exactly two times in [0,1] maximize the separation: t(q) and 1-t(q), where

| q mod 6 | t(q) |
| --- | --- |
| 0 | \((4q/3+1)/(4q+1)\) |
| 2 | \((5q+8)/[6(5q+3)]\) |
| 5 | \(2q/[3(2q+1)]\) |
| 1,3,4 | \(1/6\) |

The earlier recovery supplies complete symbolic phase and physical-lap
certificates proving M_B(q)>=F_B(q). This note supplies the matching universal
upper bound and the maximizing-time classification. The original ray
A_q=V(1,q) and its previously reviewed five-branch spectrum are unchanged.

## 1. Keep the actual orbit when changing the parameter ray

Use the same fixed coefficient rows as the original geometric model:

$$
\mathcal A=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2)).
$$

For the present ray the phase coordinates are

$$
x=\{qt\},\qquad y=\{t\}.
$$

The corresponding seven forms are x, y, x+y, 2x+y, 3x+y, 3x+2y, 5x+2y.
Their distances give B_q's objective, up to its first-two-coordinate permutation.
The actual orbit condition is now

$$
H_q(x,y)=x-qy\in\mathbb Z. \tag{1}
$$

This is an exact condition: if 0<x,y<1 and (1) holds, take the physical time
t=y. Then {qt}=x and every form gives the required physical phase. An arbitrary
safe ambient point without (1) would be insufficient.

Reflection t -> 1-t sends (x,y) to (1-x,1-y) at positive separation, preserves
all distances, and sends H_q to 1-q-H_q. Therefore we can fold **x** to x<=1/2.
We are not restricting the physical time y to its first half-period. This
distinction is necessary for the residue-5 witness below.

For an ambient lap vector m, define the polytope

$$
P_m=\{(x,y,z):z\ge1/8,\ x\le1/2,
\quad m_i+z\le a_i x+b_i y\le m_i+1-z\text{ for all }i\}. \tag{2}
$$

The first two labels are zero; their constraints imply
z<=x<=1/2 and z<=y<=1-z. All relevant labels satisfy 0<=m_i<a_i+b_i.

## 2. The fixed-cell lemma and its finite certificate

The [original cell table](LTCM_EXACT_SPECTRUM_2026_09_29.md) applies unchanged,
because neither the forms nor (2) depend on which parameter is fixed. It has:

- ten nonempty cells, including three singletons;
- 33 vertex occurrences and 45 edge occurrences;
- ambient maximum z=1/6;
- every other vertex at height at most 1/7;
- seven peak vertices, one in each nonsingleton cell, with 21 incident edges.

For this continuation, the cells were reconstructed from the inequalities,
without importing the original geometry code. There are 48 possible boundary
planes: z=1/8, x=1/2, and the two band boundaries for each of the 23 permitted
coordinate/lap combinations. All 17,296 plane triples were solved exactly.
Feasible intersections were grouped by their uniquely determined lap labels.
The resulting vertices and reconstructed edge adjacency agree with the pinned
original certificate in every cell.

Why this is exhaustive: every nonempty cell is bounded, so it has a vertex.
A vertex of a three-dimensional inequality system, including a lower-dimensional
cell, has three linearly independent active constraint normals. All such
boundaries occur in the enumerated list. Positive z makes its lap labels unique.
Thus no additional cell or vertex can be missed by this procedure. The resulting
cells have dimension zero or three; in the latter, two vertices are adjacent
exactly when their common active normals have rank two. These ranks are checked.

This is a finite exact computation establishing a fixed lemma, not an inference
from finitely many q values. The universal proof below depends on that lemma.

## 3. Why only the peak edges can control an improvement

Fix a cell and an integer h, and intersect it with H_q=h. If the slice is
nonempty, the linear objective z has an optimizing vertex P of the slice.
Let F be P's minimal face in the original cell. P lies in its relative interior.
If dim F>=2, the linear equation H_q=h has a nonzero tangent direction within F;
a small segment through P would remain in the slice. This contradicts P's
extremality. Hence P is an original vertex or belongs to an original edge.

There are only finitely many relevant integer h for each q, because the cells
are bounded. Therefore an optimizer over all cells and all physical slices can
be chosen in that way. This is an existence statement about an optimizer, not
an assertion that every maximizing point of every slice is a vertex or edge.

The already established lower witnesses satisfy F_B(q)>1/7 for every q>=2.
At heights above 1/7, the fixed-cell lemma leaves only a peak vertex or an edge
incident to one. Write an outward peak edge as

$$
(x,y,z)=(x_0+\alpha e,\ y_0+\beta e,\ 1/6-e),\qquad e\ge0. \tag{3}
$$

The complete peak data are:

| Peak | (x_0,y_0) | Outward directions (alpha,beta) |
| --- | --- | --- |
| A | (1/6,1/6) | (-1,2), (1/5,-1), (1,-1) |
| B | (1/6,1/3) | (-1,1), (-1,4), (1,-2) |
| C | (1/2,1/6) | (-3,5), (0,-1), (0,1/2) |
| D | (1/2,1/3) | (-1,2), (0,-1/2), (0,1) |
| E | (1/3,5/6) | (-2,1), (0,1), (1,-2) |
| F | (1/2,2/3) | (-1,2), (0,-1), (0,1/2) |
| G | (1/2,5/6) | (-3/5,1), (0,-1/2), (0,1) |

All these edges have 0<=e<=1/24 except E's (-2,1) direction, which ends at
e=1/42. Their directions and lengths are reconstructed from the vertices.

## 4. Integer compatibility forces a minimum loss

Along (3),

$$
H_q=h_0+d_qe,\qquad h_0=x_0-qy_0,\quad d_q=\alpha-q\beta. \tag{4}
$$

Each d_q is nonzero with constant sign on q>=2. Since 6y_0 is integral,
rho={h_0} depends only on q mod 6. If rho>0, reaching an integer requires

$$
e\ge
\begin{cases}
\rho/(-d_q),&d_q<0,\\[2pt]
(1-\rho)/d_q,&d_q>0.
\end{cases} \tag{5}
$$

This is the first integer encountered in the specified outward direction;
later integer hits have larger loss. Extending an edge indefinitely only
relaxes feasibility, so (5) is a valid lower bound on loss even if that first
hit would lie beyond its endpoint.

Direct peak congruences give:

| q mod 6 | Compatible peak vertices |
| --- | --- |
| 0 | none |
| 1 | A |
| 2 | none |
| 3 | C and G |
| 4 | E |
| 5 | none |

For residues 1,3,4 the ambient upper bound 1/6 is attained and closes the proof.
For the other residues, minimize (5) over the three directions at each peak.
The following table shows **six times** that minimum required loss:

| Peak | q=0 mod 6, q>=6 | q=2 mod 6, q>=2 | q=5 mod 6, q>=5 |
| --- | --- | --- | --- |
| A | \(1/(2q+1)\) | \(1/(q+1)\) | \(2/(2q+1)\) |
| B | \(1/(4q+1)\) | \(3/(4q+1)\) | \(3/(4q+1)\) |
| C | \(3/(5q+3)\) | \(1/(5q+3)\) | \(4/(5q+3)\) |
| D | \(3/(2q+1)\) | \(2/q\) | \(2/q\) |
| E | \(2/(q+2)\) | \(2/(2q+1)\) | \(1/(q+2)\) |
| F | \(3/(2q+1)\) | \(1/(2q+1)\) | \(1/(2q+1)\) |
| G | \(15/(5q+3)\) | \(2/q\) | \(10/(5q+3)\) |

The unique global winning directions are therefore:

| Residue | Peak and direction | Minimum loss e_*(q) |
| --- | --- | --- |
| 0 | B, (-1,4) | \(1/[6(4q+1)]\) |
| 2 | C, (-3,5) | \(1/[6(5q+3)]\) |
| 5 | F, (-1,2) | \(1/[6(2q+1)]\) |

These comparisons hold on whole unbounded domains. For example, in residue 0,
the B-to-C comparison reduces to 3(4q+1)-(5q+3)=7q>0. In residue 5, comparing
F with E reduces to (2q+1)-(q+2)=q-1>0. All denominators are positive.

For a full audit, write each loss as n_i/(a_i q+b_i) and the winner as
n_*/(a_* q+b_*). The required comparison is the affine inequality

$$
(n_i a_*-n_*a_i)q+(n_i b_*-n_*b_i)\ge0. \tag{6}
$$

The script records all 63 comparisons, not just the seven-row reduction.
Every slope is nonnegative and every value at the smallest allowed q is
nonnegative. For each nonwinning edge that starting value is strictly positive.
Another 63 comparisons validate the within-peak minima printed in the table.
Ties between nonwinning directions, such as at q=2 within peak D, do not affect
the unique global winner.

Subtracting e_* from 1/6 gives exactly F_B(q). If a better time existed, an
optimizing slice vertex above F_B>1/7 would have to be on a listed peak edge;
(5)-(6) would then force its height back to at most F_B. This proves the
matching upper bound, conditional only on the fixed-cell lemma already checked.

## 5. The winning contacts are real physical witnesses

The largest winning losses occur at the first q in each residue domain:
1/150 for residue 0, 1/78 for residue 2, and 1/66 for residue 5. All are smaller
than 1/42 and lie inside their winning edges' length 1/24. This both preserves
the >1/7 height used above and checks the finite-edge endpoint issue.

Set e=e_*(q) in the following points:

| Residue | x | y | H_q=x-qy | Selected physical time |
| --- | --- | --- | --- | --- |
| 0 | \(1/6-e\) | \(1/3+4e\) | \(-q/3\) | y |
| 2 | \(1/2-3e\) | \(1/6+5e\) | \((2-q)/6\) | y |
| 5 | \(1/2-e\) | \(2/3+2e\) | \((1-2q)/3\) | 1-y |

Each H_q is integral in its prescribed residue class. Substituting e into the
last column recovers exactly the earlier t(q). The residue-5 chart naturally
lies in the second half of physical time; reflection supplies the earlier
first-half witness. The contacts are, respectively, (q,3q+1), (2q+1,3q+2),
and (3q+1,3q+2).

For completeness, the physical lap transfer in the unpermuted coefficient
order is now

$$
\ell_i=m_i-a_iH_q,
\qquad (a_iq+b_i)y=a_i x+b_i y-a_iH_q.
$$

This differs from the original ray's transfer formula. After permuting the
first two coordinates it agrees with B_q's physical ordering. Reflection at
positive separation sends a physical lap ell_i to v_i-1-ell_i and complements
the fractional phase. The earlier recovery's direct physical-lap certificates
already incorporate that choice of t(q).

The script checks the winning time and value identities symbolically after
q=6k+r, verifies integral H_q coefficients, and reruns all 42 phase identities
and 84 safety inequalities from the lower-bound package.

## 6. Exactly two maximizing times

For residues 0,2,5, every other peak edge has strictly greater required loss.
The unique winning edge meets an integer plane at e_*, at one folded point.
There is no compatible peak. Thus any maximizing vertex of any physical slice
must be that point. An optimal face is the convex hull of its optimal vertices;
it cannot contain a segment or a different point when it has just this one
vertex. The folded optimizer is unique. Undoing reflection gives precisely
t(q) and 1-t(q).

For residues 1,3,4 the objective is the ambient maximum. Each nonsingleton cell
has exactly one height-1/6 vertex and no other point of that height. The peak
congruence table therefore exhausts its physical optimizers. Their y values,
together with reflection, are exactly 1/6 and 5/6. This proves the same
two-maximizer statement in the remaining branches.

## 7. Reproduction, provenance, and remaining limits

From the repository root, using only standard-library Python:

```bash
python3 reviews/2026-09-29-ltcm-other-ray-upper/verify_upper.py > /tmp/ltcm-other-ray-upper.json
```

The [script](../reviews/2026-09-29-ltcm-other-ray-upper/verify_upper.py),
[saved exact output](../reviews/2026-09-29-ltcm-other-ray-upper/verification.json),
[scope record](../reviews/2026-09-29-ltcm-other-ray-upper/PROTOCOL.md), and
[manifest](../reviews/2026-09-29-ltcm-other-ray-upper/MANIFEST.json) preserve:

- a fresh global reconstruction of all ten cells, 33 vertices, and 45 edges;
- all 21 peak directions and their directed integer losses;
- 63 unbounded-domain upper comparisons and 63 explanatory-table comparisons;
- peak congruences, strict winner separation, and finite-edge feasibility;
- symbolic matching to the physical-time and lower-bound certificates;
- a fixed-cell slice selector compared against the previously frozen physical
  maxima and full maximizing-time sets for q=2,...,150, with zero discrepancies.

The slice selector does not scan q-many integer planes: on an edge H_q and z
are affine, so only the first/last feasible integer projections can improve the
edge maximum. Constant projections and empty integer ranges are handled
explicitly. It uses the existing 33-vertex/45-edge geometry. It reproduced both
maximizing times in all 149 saved cases without rerunning their physical
optimizer or adding new q values. Those comparisons are counterchecks of the
implementation and parameter transfer; the infinite conclusion rests on the
finite-cell lemma and symbolic argument, not extrapolation.

The coordinator inspected the original geometry and Ultra upper-check code
before writing the new program. The newly structured reconstruction and the
older physical calculation are useful checks, but are not independent authorship
or external mathematical review. No proof assistant or new literature search
was used. Existing fixed-torus and polyhedral precedents remain credited in the
original spectrum note and its Ultra review; novelty is unresolved.

The reusable object in this step is the fixed geometry together with an explicit
integer-orbit equation. Changing that equation transfers the model to a second
structured ray and changes which contact wins. This demonstrates a concrete
transfer between these two families; it does not establish a bounded model for
arbitrary velocities or a universal extension rule.

The earlier recovery note and its hash manifest remain frozen as the record
of the previously open gap. This supplement and the updated handoffs supersede
that gap's status. The original A_q proof and Ultra review remain unchanged.

The next bounded review target is the complete B_q argument, especially the
folded-coordinate transfer, slice-vertex completeness, and uniqueness step.
A broader two-parameter classification or a general runner-extension rule is
not established here. This is a selected-reference result for the displayed
seven speeds, not a proof for arbitrary speeds or all reference runners.
