# Fixed-cell geometry review

Date: 2026-09-29. Candidate: `8a967b30fcd73abd814e4c8f7f53f216c4b3f61e`.

**Result:** no counterexample or completeness gap was found in the assigned fixed-cell geometry. Fresh exact reconstruction recovers precisely the ten listed cells, all 33 vertices, all 45 edges, and the claimed 48-plane exhaustive arrangement. The three zero-dimensional cells survive without a tolerance or positive-volume requirement. There are no other zero-, one-, or two-dimensional cells.

This is a separately tasked internal AI review, not independent human review, formal verification, or a claim of novelty. The overall spectrum remains a proof candidate under the repository's evidence vocabulary. This report addresses its finite geometry, not the global residue comparisons, all-reference scope, or prior art.

## Inputs and independence

I read `AGENTS.md`, the relevant current entries of `README.md`, `HANDOFF.md`, `RESEARCH_PLAN.md`, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, the review protocol, and `notes/LTCM_EXACT_SPECTRUM_2026_09_29.md`. The snapshot did not contain `notes/MATHEMATICAL_BASELINE.md`; no argument here depends on that unavailable file.

The working directory is a connector-backed file snapshot without `.git`. The frozen commit above is specified by the review protocol; the coordinator reports separately verifying the live branch SHA, the note's Git blob, and all nine archived manifest hashes. I did not independently retrieve that remote provenance.

Before opening `ambient.py`, `audit.py`, or their output files, I wrote and ran `geometry_check.py` using only the coefficient rows and inequalities in the note. Its first construction clips a **three-dimensional vertex representation**, unlike the original two-dimensional base-polygon clipping followed by local triple enumeration. Every crossing pair of vertices is considered; exact active-normal rank discards any resulting nonextreme chord intersections. Its second construction enumerates the global boundary planes with Cramer's rule. Only after these two constructions agreed did I read the original implementations and add a comparison against `ambient.json`.

The comparison checks the entire label-to-vertex-set map and every edge as an unordered pair of exact coordinates, not merely their totals. It passes. The note's displayed ten-row vertex table also agrees with the reconstructed values.

Dependencies are not overstated: both new constructions use Python `Fraction`, the same seven coefficient rows, and shared small dot/cross/determinant helpers. The global reconstruction shares the original audit's mathematical exhaustive-plane argument; its determinant arithmetic differs from that audit's Gaussian elimination, but resembles the original `ambient.py` linear solver. The new three-dimensional clipping route is the main implementation-structure countercheck. No project Python module is imported or executed, and the archived output is read only after both reconstructions finish. All new files are in the review directory.

## Why the search is exhaustive

Write a point as `p=(x,y,z)`. For a label `m` the cell inequalities are

\[
z\ge1/8,\qquad x\le1/2,\qquad
m_i+z\le a_i x+b_i y\le m_i+1-z,
\]

with coefficient rows

\[
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2).
\]

The first two labels are zero. Their inequalities imply

\[
1/8\le z\le x\le1/2,\qquad z\le y\le1-z.
\]

Thus every candidate cell is closed and bounded. Also `0 < a_i x+b_i y < a_i+b_i`; hence `0 <= m_i < a_i+b_i` is exhaustive. The five nontrivial lap domains have sizes `2,3,4,5,7`, so there are 840 complete coarse label vectors before pruning. No label is inferred from a numerical sample.

The initial polytope is the pyramid over the rectangle with corners `(1/8,1/8,1/8)`, `(1/8,7/8,1/8)`, `(1/2,1/8,1/8)`, `(1/2,7/8,1/8)`, with apex `(1/2,1/2,1/2)`. Its vertex list is additionally recovered from all triples of its six defining inequalities. Each later half-space intersection has vertices among the retained old vertices and intersections of the new plane with old edges. Considering **all** crossing vertex pairs includes those edges. A feasible point is a vertex exactly when its active inequality normals span all of `R^3`; this remains true for a singleton or any lower-dimensional polytope. Consequently the clipping procedure cannot discard an isolated surviving point or a nonempty line/plane cell.

The retained prefix counts after rows `(1,1),(2,1),(3,1),(3,2),(5,2)` are respectively `2,3,5,8,10`. The corresponding counts of attempted bands are `2,6,12,25,56`; a discarded prefix can have no feasible extension.

The separate global plane list is

\[
z=1/8,\quad x=1/2,\quad
 a_i x+b_i y-z=m,\quad a_i x+b_i y+z=m+1
 \quad(0\le m<a_i+b_i).
\]

There are `2+2(1+1+2+3+4+5+7)=48` distinct planes. This is an exhaustive candidate list, not a claim that each plane supports a surviving cell. All `C(48,3)=17,296` triples are solved: 4,880 are singular and 12,416 nonsingular. Exactly 90 nonsingular triple occurrences give points satisfying the closed modular bands; duplicates collapse to 33 points. The floor of each phase supplies its unique label because `z>=1/8` keeps the phase strictly away from integers.

Every nonempty bounded polytope has an extreme point. At an extreme point, if active normals did not span `R^3`, a nonzero common null direction could be followed a sufficiently small positive and negative distance while retaining all inequalities, contradicting extremality. Thus some three independent active planes determine every vertex, including a singleton. Conversely a feasible intersection of three independent relevant planes is extreme in its uniquely labeled cell. This supplies both directions of the finite-completeness argument.

## Recovered geometry

Cell numbering is the note's order. Dimensions and incidence counts were computed from the new vertices and defining inequalities.

| Cell | Lap label | Dimension | Vertices | Edges | Facets |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 | `(0,0,0,0,0,0,0)` | 0 | 1 | 0 | — |
| 1 | `(0,0,0,0,0,0,1)` | 3 | 4 | 6 | 4 |
| 2 | `(0,0,0,0,0,1,1)` | 3 | 4 | 6 | 4 |
| 3 | `(0,0,0,0,1,1,2)` | 0 | 1 | 0 | — |
| 4 | `(0,0,0,1,1,1,2)` | 3 | 4 | 6 | 4 |
| 5 | `(0,0,0,1,1,2,2)` | 0 | 1 | 0 | — |
| 6 | `(0,0,0,1,1,2,3)` | 3 | 4 | 6 | 4 |
| 7 | `(0,0,1,1,1,2,3)` | 3 | 6 | 9 | 5 |
| 8 | `(0,0,1,1,2,2,3)` | 3 | 4 | 6 | 4 |
| 9 | `(0,0,1,1,2,3,4)` | 3 | 4 | 6 | 4 |

The six four-vertex full-dimensional cells are tetrahedra. Cell 7 has the triangular-prism incidence pattern, with two triangular and three quadrilateral facets. Its nine edges, using its zero-based vertex order in the note, are

`(0,1), (0,2), (0,4), (1,2), (1,3), (2,5), (3,4), (3,5), (4,5)`.

For each full-dimensional cell, the separately assembled facet/edge incidence satisfies `V-E+F=2`. An edge is found when two distinct vertices have common active normals of rank two: those equalities expose a one-dimensional face containing both points. No rank-three common set can contain distinct points. The new and archived edge lists agree exactly.

The 33 vertex occurrences are also 33 distinct points; different labels cannot share a safe point. Their height inventory is 25 at `z=1/8`, one at `z=1/7`, and seven at `z=1/6`. Therefore the ambient maximum is exactly `1/6`, and every vertex below that height is at most `1/7`, as required by the later peak-edge upper-bound argument. The complete output records the vertices, all active constraint indices, all defining inequalities, coordinate ranges, facets, and edges, so these summary claims can be checked without relying on the archived geometry.

## Explicit singleton certificates

The dimension-zero cases deserve more than a volume-based check. Each admits a short exact collapse argument; direct substitution verifies its resulting point against every other cell inequality.

**Cell 0.** Its constraints include `x>=z`, `y>=z`, and `5x+2y+z<=1`. Hence `8z<=1`. Since `z>=1/8`, equality forces `x=y=z=1/8`.

**Cell 3.** Its constraints include

\[
-y+z\le0,\quad2x+y+z\le1,\quad-5x-2y+z\le-2.
\]

Adding the first, five times the second, and twice the third gives `8z<=1`. Equality at `z=1/8` forces equality in each contributing constraint, yielding `(x,y,z)=(3/8,1/8,1/8)`.

**Cell 5.** Its constraints include

\[
x+y+z\le1,\quad-3x-2y+z\le-2,\quad5x+2y+z\le3.
\]

Taking these with positive multipliers `4,3,1` again gives `8z<=1`. Equality forces `(x,y,z)=(3/8,1/2,1/8)`.

These demonstrate directly why strict-threshold or positive-volume filtering would be wrong here. The submitted package and new checker both preserve all three equality cells.

## Finding and limits

No mathematical correction is requested within this assignment. The note's occasional use of “facets” for all defining constraints can be read imprecisely at a singleton, whose relative face structure is not three-dimensional; its decisive completeness statement correctly uses **active planes**, and the actual computation does too. This is a wording clarification, not a defect in the proof candidate.

The finite exhaustive reduction plus exact reconstruction supports the fixed-cell lemma over the entire stated ambient domain. It does not by itself establish the residue formulas, prove every selected-time transfer, or promote the complete spectrum to an externally established theorem. No physical-parameter scan, new family, numerical optimizer, phase grid, external source lookup, or original-script rerun was performed for this review.

Reproduce from the repository root:

```bash
python3 reviews/2026-09-29-ltcm-ultra-review/geometry_check.py
```

The script writes only `geometry_check.json` beside itself. It checks the two reconstructions and the archived label/vertex/edge comparison with exact rational arithmetic. The JSON includes the checker's SHA-256 and the archived comparison file's SHA-256. Material AI involvement includes the derivation, implementation, and this report.
