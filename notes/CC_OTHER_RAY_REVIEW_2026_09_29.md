# Compatibility Calculus: adversarial review of the other ray

September 29, 2026. Reviewed research head:
`12d08824ead7b772032ba240d0e858250fbd183c`.
The upper-bound package was introduced at
`219646c0808e35f8d9e0d840afa637d2d92802bd`.

**Status: HYPOTHESIS / internally reviewed complete proof candidate.** Five
separately tasked AI reviewers found no result-level defect in the displayed
value formula or its two-maximizer conclusion. Fresh exact implementations
reproduce the geometry, unbounded arithmetic comparisons, and the declared
bounded physical calculations. Two proof sentences need explicit quantifiers.
A simpler top-cap formulation is justified below. AI supplied the review,
code, reconciliation and writing; this is not independent human certification,
formal verification, a novelty determination, or a general Lonely Runner proof.

The scope remains eight common-start runners, selected stationary reference 0,
and seven moving speeds

\[
B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2),\qquad q\in\mathbb Z,\ q\ge2.
\]

This is V(q,1) after permuting its first two coordinates. It is distinct from
the previously reviewed A_q=V(1,q) ray. The four-row mod-6 formula and the
times t(q), 1-t(q) in the [upper-bound note](LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md)
are unchanged. Historical proof packages and their manifests remain frozen;
this supplement clarifies their current interpretation.

## Review findings and their scope

The [protocol](../reviews/2026-09-29-cc-other-ray-review/PROTOCOL.md) fixed the
assignments before the checks. Full reports preserve read order and dependencies.

| Review | Result | What it does not establish |
| --- | --- | --- |
| [Geometry](../reviews/2026-09-29-cc-other-ray-review/geometry_review.md) | Fresh exact halfspace clipping reconstructs 10 cells, 33 vertices, 45 edges, all 3 singletons and all 21 peak directions/lengths. Subsequent archived-data comparison agrees. | The physical orbit or all-q arithmetic by itself. |
| [Arithmetic](../reviews/2026-09-29-cc-other-ray-review/arithmetic_review.md) | All 63 global comparisons pass on their entire residue domains; all 60 nonwinning comparisons are strict. Another 63 verify the within-peak table. All 42 phase identities, 84 band inequalities, 42 lap transfers and 42 reflection identities pass. | Completeness of the supplied geometry. |
| [Proof logic](../reviews/2026-09-29-cc-other-ray-review/proof_logic_review.md) | Slice-vertex reduction and global uniqueness survive scrutiny, with the quantifiers stated below. | Independent reconstruction of every cell or a formal proof. |
| [Physical time](../reviews/2026-09-29-cc-other-ray-review/physical_review.md) | A fresh tent-segment optimizer recovers every maximum and all maximizing times for q=2,...,25: 48 isolated time occurrences, no maximizing intervals. Closed-band intersection agrees. | An all-q result from finite testing. |
| [Representation](../reviews/2026-09-29-cc-other-ray-review/representation_review.md) | The actual-orbit and witness distinctions survive the review. A top-cap interval is sufficient for this upper bound; full cell data remain necessary for broader threshold questions. | Universal adequacy of CC or a general runner-extension rule. |

The six large inputs q=100002,...,100007 received **witness-only** checks at
both supplied times: 84 runner-distance records. Their optima and complete
maximizer sets were not exhaustively computed. The physical implementation
uses neither ambient cells nor the residue formula to perform optimization.

Geometry and arithmetic reviewers authored their checkers before reading any
original mathematical implementation. The geometry reviewer consulted the
archived geometry only after its fresh reconstruction passed. The arithmetic
and physical reviewers never read original mathematical code or saved outputs.
The proof-logic reviewer did read the original upper checker and its saved
geometry. All reviewers knew the written statement; the work was not blind
discovery and shares AI, source, and software dependencies.

## Two quantifier clarifications

First, the sentence about heights above 1/7 must read:

> Every vertex of a physical slice at height greater than 1/7 is either a
> peak vertex or lies on an original edge incident to a peak.

It does not describe every high point of a cell. For example, at q=2 the
actual-orbit point (x,y,z)=(37/80,37/160,3/20) satisfies H_2=0 and has only one
active cell inequality. It is in a two-dimensional face, with z>1/7, but is
not a slice vertex or a global optimizer. The full exact phase record and
active-constraint argument are in the logic report.

The minimal-face proof applies to **every slice vertex**: if its smallest
original face had dimension at least two, the slicing equation would leave
a nonzero tangent direction through it, contradicting extremality. Compactness
then guarantees an optimizing slice vertex. This is the needed upper-bound
reduction.

Second, “any maximizing vertex of any physical slice” must mean:

> Any vertex of any physical slice whose height equals the global value
> F_B(q) must be the winning point, in residues 0, 2 and 5.

A vertex maximizing only its own slice can lie lower. At q=11, the singleton
cell with labels (0,0,0,0,1,1,2) is (3/8,1/8,1/8), with H_11=-1. It is its
slice's optimizer but has height 1/8<11/69=F_B(11). This refutes only the
unqualified local reading.

Here is the complete uniqueness step. Given any global folded optimizer u,
take its own cell slice Q. The set Q intersect {z=F_B} is an exposed face of
Q. Every vertex of that face is a slice vertex at the global value. Strict
loss comparisons force all those vertices to be the single winning point.
A bounded polytope is the convex hull of its vertices, so the whole optimal
face is that point. This argument is applied within each cell slice; it does
not assume their union is convex. The nonconstant winning points have x<1/2,
so undoing reflection gives exactly two distinct physical times.

In the constant branches, height 1/6 occurs only at the certified peaks.
Compatibility leaves A for residue 1, C and G for residue 3, and E for
residue 4. Their y values and reflections give exactly 1/6 and 5/6. The closed
fold x<=1/2 retains both C and G on its boundary; reflection does not create
four different times.

## A smaller sufficient representation for this upper bound

This reformulation depends on the same certified cell geometry. It replaces
the slice-vertex narrative, not its geometric premises.

Each three-dimensional cell has one peak P=(x_0,y_0,1/6), with three incident
rays r_i=(alpha_i,beta_i,-1). Every incident edge reaches at least loss 1/42.
The tangent cone of the cell at P is generated by those rays. Its portion
with 0<=e=1/6-z<=1/42 is

\[
\operatorname{conv}\{P,\ P+r_1/42,\ P+r_2/42,\ P+r_3/42\}.
\]

All four displayed vertices belong to the original cell by the finite-edge
lengths. Convexity and tangent-cone containment therefore show that this is
exactly the cell's closed cap z>=1/7. At a fixed loss e its section is the
triangle with vertices P+e r_i. For the actual-orbit functional H_q=x-qy,
its image is the closed interval

\[
I_P(e)=[h_P+e\,d_-(q),\ h_P+e\,d_+(q)],\qquad
h_P=x_0-qy_0,
\]

where d_- and d_+ are the minimum and maximum of alpha_i-q beta_i.
The section contains a physical point exactly when this interval contains
an integer. The exact extrema, for every q>=2, are:

| Peak | d_-(q) | d_+(q) |
| --- | --- | --- |
| A | -2q-1 | q+1 |
| B | -4q-1 | 2q+1 |
| C | -5q-3 | q |
| D | -2q-1 | q/2 |
| E | -q-2 | 2q+1 |
| F | -2q-1 | q |
| G | -q-3/5 | q/2 |

The third projected direction is strictly between these endpoints in every
row. Thus fourteen directional candidates suffice for this optimization;
the full twenty-one-direction certificate remains the audit source. If h_P
is nonintegral and rho={h_P}, first contact requires

\[
e_P=\min\left\{\frac{\rho}{-d_-(q)},\frac{1-\rho}{d_+(q)}\right\}.
\]

If e_P exceeds 1/42 there is no contact in this cap. If h_P is integral the
peak itself is compatible. The previous strict comparisons select the same
winning edge for each nonconstant residue. At its first contact only one
endpoint of the winning interval reaches an integer, and the extremal
direction is unique. The preimage in the section triangle is consequently
one vertex, giving the same folded uniqueness conclusion directly.

The lower witnesses prove F_B>1/7, so these caps contain everything needed
for this family's global upper bound. They do **not** retain the full
1/8-safe set, the singleton cells, or lower local maxima. In particular,
discarding those objects would be invalid for the original ray's tight q=4
case or a general equality-preserving extension question. The full geometry
and physical lap charts remain preserved alongside the simpler explanation.

## Information-loss checkpoint and the next bounded question

The present CC state needs at least: the coefficient rows, ordered parameter
substitution, actual-orbit equation, folding/recovery map, threshold, lap or
phase recovery data, quantifiers, and evidence scope. Merely retaining a
spectrum table would lose distinctions that have already mattered here.

In particular, x={qt}, y={t}, H=x-qy in Z belong to B_q. The earlier A_q uses
x={t}, y={qt}, H=qx-y in Z. Fold x by **simultaneously** reflecting both
coordinates. The physical clock for B_q is y; its residue-5 folded winner
lies in the second half of physical time. The lap transfer is
ell_i=m_i-a_i H in coefficient order, followed by the first-two-coordinate
permutation and any physical reflection. All of this remains recoverable.

The next proposed investigation retains the original A ray and its orbit
qx-y in Z. It is a same-threshold comparison between the first six forms and
the model after adjoining 5x+2y. These are six and seven
moving coordinates: respectively seven and eight total runners after adding
the stationary reference. Freeze the threshold at 1/8 for the transport
comparison, rather than silently changing it with the runner count.

Reconstruct parent cells from the first six forms and intersect each with
every allowed closed band of 5x+2y. Record surviving, split, empty and
lower-dimensional children, together with parent labels and actual-orbit
compatibility. Use the original ray's q=4 equality case as a mandatory
control. Retain full safe sets: six-coordinate optimizers alone need not
contain the seven-coordinate optimum. The bounded target is an exact
parent-child map and a falsifiable transport statement, not a broader scan
or a claimed universal rule.

The earlier tight13 counterexample deletes speed 5=1+4, not the appended
seventh speed 13. It refutes a broad stronger-safe-cell inheritance principle;
it has not already classified this particular six-to-seven-form transport.
The distinction is preserved in the representation report. This next
investigation was proposed, not executed during the present review.

## Reproduction and preservation

From the repository root, with standard-library Python and assertions enabled:

```bash
python3 reviews/2026-09-29-cc-other-ray-review/geometry_check.py --compare-archive > /tmp/cc-geometry.json
python3 reviews/2026-09-29-cc-other-ray-review/arithmetic_check.py > /tmp/cc-arithmetic.json
python3 reviews/2026-09-29-cc-other-ray-review/physical_check.py > /tmp/cc-physical.json
python3 reviews/2026-09-29-cc-other-ray-review/reconcile.py > /tmp/cc-reconciliation.json
```

The corresponding JSON files in the review directory are the saved outputs.
The coordinator reran all three checks and compared their output bytes, checked
the two quantifier counterexamples, and reconciled the cap argument with the
geometry and arithmetic certificates. [REPRODUCTION.json](../reviews/2026-09-29-cc-other-ray-review/REPRODUCTION.json)
records that audit; [MANIFEST.json](../reviews/2026-09-29-cc-other-ray-review/MANIFEST.json)
pins the new artifacts and frozen inputs.

The coordinator verified the remote frozen branch head, tree and mathematical
input blob hashes. The local directory is a file snapshot, not a Git checkout.
The existing recovery and upper-bound manifest hashes continue to match.
The review is saved on the existing research branch; original proof packages
and the original A_q review are unchanged. No main merge, new literature
search, outside contact, new parameter family, other reference runner or
unattended computation is part of this review. Independent mathematical
assessment and novelty remain open.
