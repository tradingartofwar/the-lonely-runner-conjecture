# CC other-ray review: representation, information loss, and a smaller proof model

September 29, 2026. Frozen research head:
`12d08824ead7b772032ba240d0e858250fbd183c`.

**Status:** internal AI representation review of the B-ray proof candidate.
This report does not promote the candidate, establish novelty, or certify CC
as an adequate model for arbitrary runner configurations. Its geometric
simplification below is conditional on the fixed-cell lemma and peak-edge
data being correct; the assigned mathematical reviewers audit those premises.

## Finding

The current B-ray note preserves the distinctions needed to connect its fixed
geometry to actual runners. Its central compression is adequate for the
stated problem: seven fixed coefficient forms, a parameter-dependent integer
orbit equation, and explicit recovery of physical time. The same geometry
can serve two rays without their spectra, clocks, lap-transfer formulas, or
review verdicts being interchangeable.

For this B-ray upper bound, the representation can be smaller still. Because
the lower witnesses have separation strictly greater than `1/7`, only the
seven closed caps above that height matter. Each cap has a triangular
horizontal section. Projecting that triangle through `H_q=x-qy` gives a
single interval whose endpoints determine the first integer hit. This retains
the information needed for the optimum and, when extremizer identities and
strict comparisons are retained, every maximizing time. A scalar ambient cap
`z<=1/6` alone cannot do that in residues 0, 2, and 5.

The full cell certificate remains the provenance for cap completeness. The
low cells, singleton cells, and equality information must remain available:
the smaller model does not handle A_4's optimum `1/8`, a general threshold
query, or an unproved six-to-seven-coordinate transport rule.

## Sources and independence limits

Read before forming this report:

- `AGENTS.md`, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, the current README and
  HANDOFF entries, and this review's `PROTOCOL.md`;
- `notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md`, especially Sections 1–6;
- `notes/LTCM_OTHER_RAY_RECOVERY_2026_09_29.md`, including the symbolic lap
  certificates, finite-check scope, and correction of the ray identity.

After the initial model inspection, read the coordinator-materialized frozen
copies of `notes/LTCM_EXACT_SPECTRUM_2026_09_29.md` and
`notes/LTCM_ULTRA_REVIEW_2026_09_29.md`, and the current `LR2_HANDOFF.md` entries.
The original spectrum note supplied its printed full vertex table, edge
directions, A_4 exception, and precise stronger-threshold inheritance failure.
The coordinator reports that these copies match the frozen remote tree. This
reviewer did not independently fetch or verify remote blobs.

**No original mathematical program or saved JSON output was read or run.**
No new physical family, parameter scan, external source search, or
six-coordinate computation was performed. The cap reformulation is a direct
deduction from the printed geometry, not a separately reconstructed geometry
certificate. Literature statements below are reported as provenance in the
existing notes; their sources were not re-audited here. AI materially supplied
this review and its proposed reformulation.

## Distinctions that must survive compression

| Distinction | Required retained information | What would be lost by merging it |
| --- | --- | --- |
| A ray versus B ray | A_q=V(1,q); B_q=V(q,1), with only B's first two displayed speeds permuted | They have different optima: the recovery records A_2=1/6 versus B_2=2/13 and A_4=1/8 versus B_4=1/6. The earlier Ultra verdict concerns A. |
| Total runners versus moving coordinates | Eight common-start runners; selected stationary reference 0; seven relative speeds | A seven-coordinate calculation is not a seven-total-runner claim. No result for other reference runners follows. |
| Coordinate forms versus parameterized speeds | Fixed rows `(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2)` and their ordering | Reusing the coefficient table does not make the parameter rays interchangeable. |
| Ambient safety versus physical safety | Closed bands plus the exact integer-orbit equation | A safe point in the two-dimensional ambient square need not lie on the physical one-dimensional orbit. |
| Folded phase versus physical clock | For B, `x={qt}`, `y={t}`, fold `x<=1/2`, recover `t=y` before an optional reflection | Restricting `y<=1/2` in the folded chart can remove the residue-5 witness. |
| Ambient labels versus physical laps | Ambient `m_i`, integral `h=x-qy`, and `ell_i=m_i-a_i*h` before permutation/reflection | Directly interpreting `m_i` as a physical lap produces the wrong phases. |
| Closed equality versus positive duration | Weak band inequalities and zero-dimensional cells | A safe instant and a positive safe interval are different claims. The A_4 control requires isolated equality points. |
| Value versus optimizer set | Upper and lower bounds establish the value; strictness and geometric support establish uniqueness | An optimum-selecting algorithm is not automatically an enumeration of all maximizing times. |
| Fixed operation count versus bit complexity | A bounded number of rational operations for this fixed geometry, with input-dependent integer sizes | Neither residue selection nor `33+45` candidates means constant bit-time. |
| Reproduction versus proof scope | Exact finite checks, fixed finite geometry completeness, and symbolic unbounded comparisons have separate roles | The 149 checked B inputs or large witness checks do not establish the infinite upper bound by extrapolation. |

In A's chart, `x={t}`, `y={qt}`, the orbit equation is `qx-y in Z`,
the physical clock is `t=x`, and the physical laps are `m_i+b_i*(qx-y)`.
For B the coefficient-order speed is `a_i*q+b_i`; the displayed B order swaps
the first two entries. Reflection at positive separation sends a physical
lap to `v_i-1-ell_i`. These are coordinate maps, not optional notation.

For a concrete clock check using an already declared case, at B_5 the winning
folded point is `(x,y)=(16/33,23/33)`, while the selected first-half time is
`10/33=1-y`. At q congruent to 3 modulo 6, the compatible peaks C and G both
have `x=1/2` and are reflections of each other. Unfolding these two chart
points produces two physical times, not four. The fold boundary is therefore
relevant to counting, even though it does not change the maximum.

The current upper note already supplies the necessary repairs: its Section 3
explicitly states optimizer-on-edge **existence**, and Section 6 separately
uses all optimal vertices to exclude another maximizing point. Those two
steps should remain separate in any abbreviated account.

## Separate the claims CC is being asked to support

| Task | Sufficient certificate in this family | Additional conclusion not supplied by it alone |
| --- | --- | --- |
| Existence at `1/8` | One physical witness whose seven exact distances are at least `1/8` | The optimal value or every witness |
| Optimization | Lower witnesses plus complete ambient coverage and integer-hit lower bounds on loss | Uniqueness of physical maximizers |
| Witness selection | The residue rule, contact point, clock map, and physical safety certificate | A universal rule for discovering suitable contacts in arbitrary families |
| Every maximizing time | Strict global winner separation, unique supporting point or the complete compatible peak list, and reflection bookkeeping | The complete `1/8`-safe set or its duration |
| A-to-B transport | Reuse fixed cells while changing the orbit equation and recovery maps | An unchanged spectrum or inherited A-ray review verdict |
| Six-to-seven transport | A new same-threshold parent/child certificate with the seventh constraint and orbit carried explicitly | A runner-count induction or preservation of a six-coordinate optimizer |

In particular, the scalar function `F_B(q)` and a selected time are a useful
output representation, but they do not hold the proof. The proof's compact
record must still explain why omitted locations cannot do better and how
the selected point reaches the physical orbit.

## A smaller B-ray proof representation: seven peak caps

Write `u_ji=(alpha_ji,beta_ji,-1)` for the three printed outward edge
directions at peak `P_j=(x_j,y_j,1/6)`. Let `e0=1/42`, so that
`1/6-e0=1/7`. The fixed-cell data say:

1. Every nonsingleton cell has one peak, with exactly those three incident
   edges; every other vertex has height at most `1/7`.
2. Every incident edge extends to at least `e=e0`; the E edge with direction
   `(-2,1)` ends exactly there.
3. The three singleton cells have height `1/8`.

It follows that the closed part of the cell at height at least `1/7` is

\[
K_j=\operatorname{conv}\bigl(P_j,\ P_j+e_0u_{j1},
P_j+e_0u_{j2},\ P_j+e_0u_{j3}\bigr).
\]

For example, one may obtain its vertices by cutting the certified polytope
with `z>=1/7`: only the peak and the intersections of its incident edges with
the cut survive. Equivalently, the cell lies inside its peak tangent cone,
while the four displayed feasible points fill the truncated cone. Equality
at `e=e0` is retained in this statement. The six-vertex E cell therefore
requires no special shape below the cut in the B-ray proof.

At fixed `0<=e<=e0`, the horizontal section is the triangle

\[
(x,y)=(x_j,y_j)+e\sum_{i=1}^{3}\lambda_i(\alpha_{ji},\beta_{ji}),
\qquad\lambda_i\ge0,\quad\sum_i\lambda_i=1.
\]

Put `h_j=x_j-q*y_j`, `d_ji=alpha_ji-q*beta_ji`. Its exact image under
`H_q=x-qy` is the closed interval

\[
I_j(e)=[h_j+e d_j^-,\ h_j+e d_j^+],\qquad
d_j^- = \min_i d_{ji},\quad d_j^+ = \max_i d_{ji}.
\]

Thus a physical point exists in this section precisely when
`ceil(h_j+e*d_j^-) <= floor(h_j+e*d_j^+)`. This is a projection of a
**connected convex section**. Replacing a disconnected union of cells by
its total projection interval would not be justified; each cap remains
separate.

For every q>=2 the extrema are strict and have the following identities:

| Peak | `h_j` | `d_j^-` and direction | `d_j^+` and direction | Discarded middle direction and projection |
| --- | --- | --- | --- | --- |
| A | `(1-q)/6` | `-(2q+1)`, `(-1,2)` | `q+1`, `(1,-1)` | `(1/5,-1)`, `q+1/5` |
| B | `(1-2q)/6` | `-(4q+1)`, `(-1,4)` | `2q+1`, `(1,-2)` | `(-1,1)`, `-(q+1)` |
| C | `(3-q)/6` | `-(5q+3)`, `(-3,5)` | `q`, `(0,-1)` | `(0,1/2)`, `-q/2` |
| D | `(3-2q)/6` | `-(2q+1)`, `(-1,2)` | `q/2`, `(0,-1/2)` | `(0,1)`, `-q` |
| E | `(2-5q)/6` | `-(q+2)`, `(-2,1)` | `2q+1`, `(1,-2)` | `(0,1)`, `-q` |
| F | `(3-4q)/6` | `-(2q+1)`, `(-1,2)` | `q`, `(0,-1)` | `(0,1/2)`, `-q/2` |
| G | `(3-5q)/6` | `-(5q+3)/5`, `(-3/5,1)` | `q/2`, `(0,-1/2)` | `(0,1)`, `-q` |

These entries follow by direct substitution into the printed directions;
each middle projection is strictly between the two endpoints on q>=2.
The middle edge can therefore be omitted from the **B-ray integer-hit
optimization**, while retaining it in the certified geometry. This leaves
14 directed alternatives instead of 21. The original all-edge comparisons
already include the retained alternatives; this report does not claim a new
executed comparison count.

Since `d_j^-<0<d_j^+`, the intervals expand from `h_j`. If
`rho_j={h_j}` is nonzero, their first possible integer hit is at

\[
e_j=\min\left\{\frac{\rho_j}{-d_j^-},
\frac{1-\rho_j}{d_j^+}\right\}.
\]

If `rho_j=0`, the peak is already compatible. A first hit beyond `e0` is
only a relaxed lower bound on the required loss, not a feasible cap witness.
The certified B winners have `e<=1/66<1/42`, so this endpoint issue does not
arise for their lower witnesses.

This formulation explains both optimization and uniqueness without asserting
that every slice optimizer must initially lie on an edge. Before `e_j`, the
**whole section** misses every integer. At a uniquely winning loss, its first
integer touches one interval endpoint; because that endpoint's projection
extremizer is strict, only the corresponding triangle vertex is compatible.
It is the original winning edge point. The existing strict comparisons
exclude every other cap. For residues 1, 3, and 4, retain the complete
compatible peak list and its reflection map instead.

The data needed for this proof are therefore the completeness of the seven
caps, the seven base values `h_j`, the two extremal projections per cap,
their geometric identities, and the time/reflection map. Keeping only the
numerical interval endpoints would still suffice to decide value feasibility,
but would lose the contact point and its physical recovery unless those
identities were reconstructible.

### What the simplification deliberately does not answer

- The ambient bound `1/6` alone is enough for the constant branches once
  actual lower witnesses are given. It loses the directed mismatch and edge
  slopes needed for the nonconstant branches.
- The seven caps do not represent safe points below `1/7`, the complete
  `1/8`-safe schedule, or A_4. They must not replace the full stored cells.
- Explicit stored ambient lap labels are not logically indispensable for the
  value once cap completeness is certified: they can be reconstructed by
  flooring the fixed forms at a point with positive separation. But integer
  orbit compatibility and the distinction between ambient and physical laps
  cannot be dropped. Retaining labels is useful for audit and transport.
- The full geometry itself is fixed only because these coefficients are
  fixed. A changed coefficient set may change the number, shape, and heights
  of the cells; another orbit may change which projections are extremal.
- This is a task-specific sufficient representation. Its failure at a lower
  threshold would not refute the full cell model, and success here does not
  establish universal CC adequacy.

## Concrete next target, proposed only: same-threshold six-to-seven transport

Keep the already studied A ray `V(1,q)`, q>=2, selected reference 0, and the
same coefficient order. Let `P_m^(6)` be the fixed cells for the first six
forms, defined at the **same variable height z>=1/8** used by the seven-form
model. Study the single operation

\[
P_{m,k}^{(7)}=P_m^{(6)}\cap
\{k+z\le5x+2y\le k+1-z\},\qquad k\in\mathbb Z,
\]

while retaining `qx-y in Z`. This is a concrete parent-to-child map of
closed cells, with finite label ranges from the fixed ambient bounds. Its
basic intersection identity is exact, but that identity alone supplies no
useful selection or forcing theorem.

One bounded deliverable would be a complete parent/child table for these
fixed forms, including singleton children, marking which A-ray winning
contacts survive unchanged, are cut away, or are created where the seventh
band meets a previously nonoptimal face. The testable compression question
is: **what information about each six-coordinate cell, beyond its optimum
and one selected witness, suffices to recover the seven-coordinate winning
value and contact?** Begin by testing six-coordinate optimal-face data;
preserve a failed sufficiency claim if a required child comes from a
nonoptimal parent face. Enrich only by the needed boundary or label data.

Use only already archived A-ray controls for numerical comparison, with
q=4's isolated `1/8` witnesses and q=3,10's `1/7` boundary cases compulsory.
The fixed symbolic transport table is the target; a wider q scan, new
coefficient family, arbitrary reference runner, or a full two-parameter
classification is not part of this proposal. The existing literature context
for the first six coordinates must remain credited; its printed results
should be mapped explicitly before being used as proof premises.

Two safeguards are consequential:

1. Do not retain only cells feasible at the smaller problem's natural `1/7`
   threshold and then expect them to describe all final `1/8` witnesses.
   Same-threshold clipping avoids that unjustified restriction.
2. The archived stronger-threshold inheritance counterexample deletes
   **speed 5=1+4** from tight13, not the appended seventh speed 13. It
   falsifies the broader inheritance-only rule, but is not itself the
   requested first-six-to-seventh transport classification. Preserve that
   distinction when choosing the next test.

No part of this proposed six-coordinate investigation was executed here.

## Evidence and handoff assessment

The upper note's current status supersedes the lower recovery note's
historically open B upper bound. The README/HANDOFF place those older entries
under preserved-history headings; a future compact account should carry the
supersession explicitly rather than copy the old `OPEN` sentence in isolation.
The A-ray review remains a separate historical review, and this review does
not retroactively change it.

Keep three levels visible: exact checks on named finite physical inputs;
a fixed finite certificate intended to be exhaustive for the ambient model;
and symbolic reasoning over every admissible q. Their combination supports
an internally reviewed proof candidate if the mathematical audits pass.
Neither reviewer agreement nor the number of candidate times is a new proof
certificate, and no literature novelty assessment was performed.

The useful conclusion for CC is limited and testable: this fixed geometry
plus an explicit orbit map supports compact selection and exact optimization
on the two stated rays. The proposed cap record is smaller and adequate for
the current B optimization task. Whether a comparably small record can
survive addition of the seventh constraint is a precise next question, not a
consequence already obtained.
