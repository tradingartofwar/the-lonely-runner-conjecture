# Fixed-cell geometry review for the other CC ray

Date: September 29, 2026. Assigned scope: the fixed geometry used for
`B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2)`, which is `V(q,1)` after permuting
its first two coordinates, integer `q>=2`, selected stationary reference.
Frozen research head supplied by the protocol:
`12d08824ead7b772032ba240d0e858250fbd183c`.

**Verdict: the fixed-cell lemma is reproduced with no defect or counterexample
found.** A fresh exact incremental clipping construction gives all ten cells,
33 distinct vertex occurrences, 45 edge occurrences, three singleton cells,
ambient maximum `1/6`, and exactly seven peak vertices with 21 incident edges.
The remaining vertex heights are `1/8` (25 occurrences) and `1/7` (one).
Every peak direction and finite edge length in the written statement matches.
Subsequent comparison with the archived `ambient.json` agrees on every lap
label, vertex, edge, and base vertex.

This is a separately assigned, internally authored AI review and exact
reproduction, not independent human review, formal certification, or promotion
of the full spectrum candidate to an established theorem.

## Construction from the inequalities

The only mathematical inputs to construction are the coefficient rows

`((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2))`

and the displayed inequalities

`z>=1/8`, `x<=1/2`, `m_i+z<=a_i*x+b_i*y<=m_i+1-z`.

The reconstruction does **not** enumerate triples of the 48 boundary planes.
It does not consume an existing cell list or an existing vertex or edge list.
All arithmetic uses Python's standard-library `fractions.Fraction`.

1. **Exact starting hull.** With the first two labels zero, the first two bands
   and fold give `1/8<=z<=1/2`, `z<=x<=1/2`, and `z<=y<=1-z`.
   This is a rectangular pyramid: four vertices at `z=1/8`, with
   `x in {1/8,1/2}` and `y in {1/8,7/8}`, and apex `(1/2,1/2,1/2)`.
   At each height its rectangle corners move affinely to the apex, proving
   that this seed hull is the entire feasible starting polytope. The redundant
   upper band `x+z<=1` is also retained in the constraint representation.

2. **Complete lap branching.** Because positive safety gives `0<x,y<1`, each
   remaining form has `0<a_i*x+b_i*y<a_i+b_i`; hence every feasible lap label
   lies in `0,...,a_i+b_i-1`. The first two labels are necessarily zero.
   The product of the five remaining lap counts is `2*3*4*5*7=840`.
   Branches are pruned only after their exact intersection is empty, so they
   cannot become feasible after adding further inequalities.

3. **Exact clipping without an adjacency oracle.** Each new halfspace retains
   all old vertices on its feasible side, including equality. It also
   intersects the new boundary with every pair of old vertices having strictly
   opposite signs. The true newly created vertices occur where old edges cross
   the cutting plane, so this superset includes all of them. Each extra
   intersection is nevertheless feasible, being a convex combination of old
   vertices on the new boundary.

4. **Remove only nonvertices.** A feasible point is a vertex exactly when its
   active constraint normals span three-dimensional space. If they do not,
   a nonzero null direction preserves the active equations, and sufficiently
   small displacements in both directions preserve every inactive inequality;
   the point is therefore nonextreme. If they do, the active equations have a
   unique solution, so the point is extreme. This criterion applies also to
   lower-dimensional bounded intersections. The clipping step therefore leaves
   exactly the vertices of the new polytope, preserving the induction.

5. **Recover every edge from faces.** For two final vertices, collect all
   constraints active at both and then collect the complete vertex set
   satisfying those common equalities. This is the minimal face containing the
   pair. The pair is an edge precisely when that face has exactly those two
   vertices. Thus the edge construction does not use the note's rank-two
   adjacency test as its oracle. As a subsequent consistency check, every
   recovered edge does have common active-normal rank two.

The successive nonempty branch counts are `2,3,5,8,10`. Only 101 lap-branch
attempts are needed after exact prefix pruning (`2+6+12+25+56`); this is an
exhaustive implementation of the finite 840-label product, not a sampling rule.

## Recovered cells and equality cases

All labels below are in the displayed coefficient order. The JSON contains
every exact coordinate, every active constraint, and every edge endpoint pair.

| Lap vector | Dimension | Vertices | Edges | Peak |
| --- | ---: | ---: | ---: | --- |
| `(0,0,0,0,0,0,0)` | 0 | 1 | 0 | none |
| `(0,0,0,0,0,0,1)` | 3 | 4 | 6 | A |
| `(0,0,0,0,0,1,1)` | 3 | 4 | 6 | B |
| `(0,0,0,0,1,1,2)` | 0 | 1 | 0 | none |
| `(0,0,0,1,1,1,2)` | 3 | 4 | 6 | C |
| `(0,0,0,1,1,2,2)` | 0 | 1 | 0 | none |
| `(0,0,0,1,1,2,3)` | 3 | 4 | 6 | D |
| `(0,0,1,1,1,2,3)` | 3 | 6 | 9 | E |
| `(0,0,1,1,2,2,3)` | 3 | 4 | 6 | F |
| `(0,0,1,1,2,3,4)` | 3 | 4 | 6 | G |

The three singleton points are, respectively,
`(1/8,1/8,1/8)`, `(3/8,1/8,1/8)`, and `(3/8,1/2,1/8)`.
No one- or two-dimensional final cells are found; they were not excluded by an
assumption or a dimension filter. All weak inequalities remain weak throughout.

The implementation's elementary boundary controls separately collapse the seed
to a two-dimensional face, then an edge, then its apex, then an empty set. A
truncation control also confirms that extra pair-intersection candidates are
removed without losing the eight vertices of the resulting frustum. These
controls directly exercise the equality and degeneracy behavior needed here.

Each nonsingleton cell has exactly one vertex at `z=1/6`. Each such vertex has
three incident edges. Writing the edge displacement as
`(alpha*e,beta*e,-e)` reproduces all 21 displayed directions. Twenty edges have
`0<=e<=1/24`; E's `(-2,1)` edge has `0<=e<=1/42`.

## Attack on the original completeness argument

The written 48-plane argument survives the following checks.

- The permitted lap ranges cover every point at positive safety, including the
  folded boundary `x=1/2`. Their total is
  `1+1+2+3+4+5+7=23`, giving 46 band planes plus the floor and fold planes.
- Every nonempty cell is bounded: its first bands give bounded `x,y,z`.
  Every nonempty bounded polyhedron has a vertex, including a singleton.
- At a vertex, three linearly independent active normals are necessary even
  when the entire cell has lower dimension, by the null-direction argument
  above. Thus enumeration of independent plane triples cannot miss a
  lower-dimensional nonempty cell.
- With `z>=1/8>0`, different lap labels for the same form have disjoint safe
  bands. Grouping feasible intersections by their uniquely determined lap
  labels therefore cannot merge different cells.
- Once the final dimensions are checked to be zero or three, the stated
  common-active-normal rank-two criterion for two distinct vertices is a valid
  edge criterion. The separate face-vertex construction agrees with it.

No correction to the fixed-cell statement is indicated. The new clipping
construction supplies a different exhaustive route to the same certificate;
it shares the elementary active-normal characterization of vertices with the
written argument, a dependency made explicit rather than hidden.

The geometric conclusion that linear maxima occur at vertices is sufficient
to certify the ambient height. It does not assert that every point above `1/7`
lies on a peak edge. Interior high points exist. Any later reduction of a
physical slice optimum to a peak edge needs the separate slice-vertex
argument; this review does not replace that argument.

## Read order, dependencies, and reproduction

Read first: `AGENTS.md`, the current `README.md` and `HANDOFF.md` entry-point
sections, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, the review `PROTOCOL.md`, and the
written target note. No original mathematical Python source was read or
imported at any point in this review.

The incremental clipping code was written and successfully run **before**
opening `reviews/2026-09-29-ltcm-spectrum/ambient.json`. The first construction
already passed all listed counts, singleton, height, direction, and length
assertions. The initial code SHA-256 was
`3dda72a31f64c3ec421077b42fa51f670f77105734c578843cab7f3bf7dd28b2`.
Only afterward was the archived JSON schema inspected and an optional
comparison routine added. The reconstruction body has the same canonical
SHA-256 before and after that addition:
`2fa500c35f5ff3c94c31c064199b7cbfb43fd7dcc6e170a00548122011ff669b`.

The archived data are a comparison target, never a construction input. In a
comparison run, they are opened only after reconstruction and all written
statement checks finish. Omitting `--compare-archive` reproduces the geometry
without reading that archive.

From the repository root:

```bash
python3 reviews/2026-09-29-cc-other-ray-review/geometry_check.py --compare-archive > reviews/2026-09-29-cc-other-ray-review/geometry_check.json
```

The program requires only standard-library Python and completes in under one
second in the review environment. It checks assertions without suppressing
exceptions; run it normally, not with Python's `-O` option.

Input/output provenance:

| Object | SHA-256 |
| --- | --- |
| Written target note | `1bbbbe1471c3363893bfdb7b1803c597b684022613777d17ad363fe04c7ee8ab` |
| Archived `ambient.json` | `af1a620e08e9407b7d01d0f444a0041f81e5be3e02c673f891f033c3a680f736` |
| Final `geometry_check.py` | `29b790b3044afd185a462d93fb64d50d4506fb29723b0dd1acbaf8882b68fe7c` |

The local working directory is a file snapshot without `.git`; this reviewer
could not verify a local Git HEAD. The frozen revision is the protocol's
identifier. The coordinator separately reported verifying the remote head,
tree, and input Git blob hashes. The SHA-256 values above were computed from
the actual local files used here.

## Information retained and limits

The certificate retains full `(x,y,z)` coordinates, complete lap vectors,
active constraints, incidence, dimensions, and exact endpoint equalities.
The omitted continuum of each cell is recovered as the convex hull of its
listed vertices. Singleton cells therefore remain represented rather than
being erased by a positive-volume representation. The `x=1/2` fold boundary
also remains explicit. Reducing this data to only peak heights would lose the
edge directions needed by the later orbit arithmetic; the JSON retains them.

This fixed geometry is independent of physical `q`, and no physical `q` scan,
new velocity family, other selected reference, or literature/novelty check was
performed. Directed integer losses, unbounded residue comparisons, physical
lap transfer, and the proof that there are exactly two maximizing physical
times are outside this assigned geometry check. Ordinary Python execution is
not a proof-assistant certificate; shared written inputs and expected outputs
also limit epistemic independence. The full candidate remains subject to the
other review assignments and external mathematical assessment.
