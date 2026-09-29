# Compatibility Calculus: what survives the seventh constraint?

September 29, 2026. Base research commit:
`a9a9c2746bd39740888ecd4ae48ed8f5d47b4dcd`.

**Result:** the exact parent-child map is complete for the fixed six/seven-form
models. It exposes three consequential failures of compressed records: keeping
only the old global optimizers loses even existence of a surviving witness;
keeping only points on the old edges loses some final maximizing times; and
keeping separate orbit/phase ranges can invent a witness. Closed conditional
phase intervals on the same integer orbit slice preserve the needed relation.

**Status:** REPRODUCED for the explicit finite geometry and q=3,4,10 controls;
HYPOTHESIS / proof candidate for the general transfer reasoning within these
fixed forms. This is a coordinator continuation using reviewed code and a
separately structured countercheck, not another independent team review or a
formal certificate. AI supplied the derivation, implementation and writing.
No novelty or general Lonely Runner result is claimed.

## Scope and the question being tested

Return explicitly to the original **A ray**, with six moving speeds

\[
U_q=(1,q,q+1,q+2,q+3,2q+3)
\]

and append the seventh speed 2q+5 to obtain A_q. Together with stationary
reference 0 these are seven and eight total common-start runners. The previous
B_q=V(q,1) review remains separate.

Use x={t}, y={qt}, fold x<=1/2, and keep

\[
H_q=qx-y\in\mathbb Z.
\]

The first six coefficient rows are
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2); the appended row is (5,2).
Both models retain **the same floor z>=1/8**. The variable z remains the
separation being optimized. We do not begin at the six-coordinate problem's
natural threshold 1/7 and assume its feasible cells exhaust the 1/8 model.

For a parent lap vector m, let P_m be its closed six-band polytope. Put
S=5x+2y. Its child with seventh lap k is exactly

\[
C_{m,k}=P_m\cap\{k+z\le S\le k+1-z\},\qquad k=0,\ldots,6.
\]

This intersection identity is elementary. The research question is what
information a smaller parent record can discard while still recovering the
desired child result: a value, one witness, every maximizer, or every safe time.

## 1. Complete fixed parent-child map

Exact reconstruction gives eight parent tetrahedra, 32 vertex occurrences and
48 edge occurrences. Every parent has one peak at height 1/6. Applying all
56 possible parent/seventh-lap pairs yields ten nonempty children and 46 empty
branches. No parent loses all its children at the 1/8 floor.

Parent indices below are local to this note; child indices agree with the
original seven-form certificate. A child lap is only its last label k; its
first six labels are the parent labels.

| Parent | Six labels | Child indices and seventh laps | Effect |
| --- | --- | --- | --- |
| P0 | (0,0,0,0,0,0) | C0: k=0; C1: k=1 | Singleton plus clipped tetrahedron |
| P1 | (0,0,0,0,0,1) | C2: k=1 | Entire parent survives unchanged |
| P2 | (0,0,0,0,1,1) | C3: k=2 | Collapses to a singleton |
| P3 | (0,0,0,1,1,1) | C4: k=2 | Entire parent survives unchanged |
| P4 | (0,0,0,1,1,2) | C5: k=2; C6: k=3 | Singleton plus clipped tetrahedron |
| P5 | (0,0,1,1,1,2) | C7: k=3 | Clipped to a six-vertex polytope |
| P6 | (0,0,1,1,2,2) | C8: k=3 | Entire parent survives unchanged |
| P7 | (0,0,1,1,2,3) | C9: k=4 | Clipped tetrahedron |

The children have 33 vertices and 45 edges, exactly matching the frozen
seven-form data. Of their vertices, 27 are inherited parent vertices and six
are new intersections on parent edges. Five parent vertices disappear. The
one removed peak is (1/3,1/6,1/6): its seventh form S=2 is an integer, so
the added distance is zero. This was P2's entire ambient optimal face, yet
P2 still has a nonempty singleton child below it. Retaining only each
parent's ambient optimal face would lose that child.

Of the 45 child edges, 36 lie along old parent edges. The other **nine lie
inside parent faces** and are created by the added band. There is no
contradiction in all new vertices lying on old edges while some new edges
lie inside old faces: the cut joins those vertices across a face.

The singleton children are C0=(1/8,1/8,1/8), C3=(3/8,1/8,1/8), and
C5=(3/8,1/2,1/8). Their existence in the ambient model does not establish
their physical compatibility for a particular q.

The [saved primary certificate](../reviews/2026-09-29-cc-six-seven-transfer/verification.json)
retains every parent/child label, vertex, edge, defining inequality, empty
branch, and minimal parent-face dimension. The construction reuses the
reviewed exact clipping code. A separate 34-plane, 5,984-triple reconstruction
recovers all eight parents and 32 vertices using cross products rather than
clipping. All children also match the archived seven-form certificate.

Completeness uses the finite lap ranges, not physical sampling. There are
2*3*4*5=120 possible six-form label combinations after the first two zero
labels. All cells are bounded by the first two bands. Every nonempty cell has
a vertex with three independent active normals, so the exhaustive boundary
plane enumeration detects it, including a lower-dimensional cell. Empty
parent branches cannot become nonempty by adding another constraint. Positive
z makes the lap labels unique; all band endpoints remain closed.

## 2. Old global optimizers do not supply surviving witnesses

Only the declared controls q=3,4,10 were physically optimized. The new
six-coordinate maxima and the previously archived seven-coordinate maxima
are reproduced exactly by both a tent-envelope algorithm and a separately
written opposing-contact algorithm.

| q | Six-coordinate maximum | All six-coordinate maximizing times | Distance to added runner at those times | Seven-coordinate maximum |
| --- | --- | --- | --- | --- |
| 3 | 2/13 | 6/13, 7/13 | 1/13 | 1/7 |
| 4 | 2/13 | 4/13, 9/13 | 0 | 1/8 |
| 10 | 4/25 | 8/25, 17/25 | 0 | 1/7 |

Every old global optimizer fails the final 1/8 threshold in these three
controls. At q=4 and q=10, the added runner is exactly coincident with the
reference at both old best times. The final system nevertheless has witnesses.
Thus the record “old optimal value plus **all** old optimizing times” is
insufficient even to find a surviving 1/8 witness in these examples.

The complete final maximizer sets are:

| q | All seven-coordinate maximizing times in [0,1] |
| --- | --- |
| 3 | 1/7, 2/7, 3/7, 4/7, 5/7, 6/7 |
| 4 | 1/8, 3/8, 5/8, 7/8 |
| 10 | 1/7, 2/7, 3/7, 17/35, 18/35, 4/7, 5/7, 6/7 |

At q=4 the equality information is particularly concrete. The six-coordinate
1/8-safe set consists of the four isolated points above, plus four positive
intervals. The two intervals in the first half-period are

\[
[17/56,5/16],\qquad[41/88,15/32],
\]

and the other two are their reflections. Adding speed 13 removes all four
positive intervals and preserves exactly the four isolated points. A model
that stores only positive-duration windows therefore returns no witness here.
This calculation deletes/restores the appended speed 13. It is distinct from
the earlier inheritance counterexample that deleted speed 5=1+4.

## 3. A new maximizing contact can lie inside an old face

For q=10, consider t=17/35. Its folded point at the final optimum is

\[
(x,y,z)=(17/35,6/7,1/7),\qquad H_{10}=4.
\]

It belongs to parent P7 with labels (0,0,1,1,2,3). Among the six parent bands,
only y+z=1 is active. The floor and fold are strict. This point is therefore
in the relative interior of a **two-dimensional parent face**, not on any
old parent edge. The seventh band adds the active equality S-z=4, creating
the child edge through it. Its reflection t=18/35 is also a global maximizer.

The change can be verified with two short contact certificates. In the same
parent physical slice, the old constraints from speeds 10 and 23 are

\[
10t+z\le5,\qquad -23t+z\le-11.
\]

Multiplying by 23 and 10 and adding gives 33z<=5. Equality is feasible at
t=16/33, z=5/33; this is the old optimum of that parent slice. The added
speed 25 has distance 4/33<1/8 at that time. Its relevant new lower band is

\[
-25t+z\le-12.
\]

Combining this with 10t+z<=5 gives 35z<=5. Equality now occurs at
t=17/35, z=1/7, and all other bands are satisfied. The saved countercheck
verifies every phase and both linear certificates.

Two precise compression failures follow. Simply retaining the surviving
points of the old edge set misses these two final maximizing times. Retaining
only each parent slice's old optimizing face misses this point too: its own
parent slice previously attained the larger value 5/33 somewhere else.
Neither example says that those smaller records fail to find **any** final
optimizer at q=10; other maximizing times remain available.

In fact, conditional on the previously reviewed A-ray formula, its selected
witnesses for every q>=2 lie on the old parent one-skeleton. The constant
branches use parent peaks; q=4 uses the vertex in P1; the E charts lie on
P5's edge with direction (-2,1); and the C chart lies on P3's edge with
direction (-3,5). Their certified loss intervals are contained in those
parent edges. Thus a record adequate for selecting **one** optimal witness
can still be inadequate for recovering **every** optimal witness.

For full child reconstruction, retaining the parent facets and their cuts is
sufficient. At these heights the lower and upper new band planes cannot both
be active: that would force z=1/2, above the parent maximum 1/6. Every new
child edge consequently comes from a new band plane cutting a parent face.
The atlas explicitly records those nine new edges rather than assuming the
old one-skeleton remains complete.

## 4. Separate marginal ranges can manufacture compatibility

Another compression fails even when it stores ranges rather than maxima.
Take q=4, parent P2, and z=1/8. The section is the triangle with vertices

\[
(1/4,3/8),\qquad(1/3,1/8),\qquad(3/8,1/8).
\]

Its separate projection ranges are

\[
H_4=4x-y\in[5/8,11/8],\qquad
S=5x+2y\in[23/12,17/8].
\]

The H range contains the integer 1, and the S range reaches the safe-band
endpoint 2+z=17/8. Treating those two facts as joint feasibility produces a
false positive. The only child point in this parent is (3/8,1/8,1/8), whose
H_4=11/8 is not an integer.

On the **actual H_4=1 section**, the two endpoints instead are

\[
(17/56,3/14),\qquad(5/16,1/4),
\]

so the conditional S interval is

\[
[109/56,33/16].
\]

It lies strictly between the safe upper endpoint 15/8 below the integer 2
and the safe lower endpoint 17/8 above it. This entire actual-orbit section
is blocked by the seventh runner. The false pair (H,S)=(1,17/8) belongs to
the product of the marginal intervals but not to the joint image of the
parent section.

## 5. Exact conditional-interval transfer

For a fixed parent P_m, integer h and height z, define

\[
J_{m,h}(z)=\{5x+2y:(x,y,z)\in P_m,\ qx-y=h\}.
\]

The set is empty or a closed interval [L,U], possibly a single point,
because the parent section is compact and convex. A surviving physical point
exists in that section **if and only if**, for some k in {0,...,6},

\[
\max\{L,k+z\}\le\min\{U,k+1-z\}. \tag{1}
\]

To prove sufficiency and recover the witness, choose any S in the intersection.
The simultaneous coordinate change is invertible:

\[
x=\frac{S+2h}{2q+5},\qquad
y=\frac{qS-5h}{2q+5},\qquad t=x. \tag{2}
\]

The definition of J supplies membership in the same parent, rather than in
two unrelated projection ranges. The integer h supplies {qt}=y. The new
inequality supplies the seventh safety band. Necessity follows by reading
H, S and k from any surviving physical point. This proves the equivalence
for every integer q>=2 within these fixed forms, conditional on the parent
description; it is not extrapolated from the three controls.

The old physical laps are ell_i=m_i+b_i h, and the added physical lap is
ell_7=k+2h because (2q+5)t=S+2h. Reflection sends t to 1-t and a physical
lap ell_i to v_i-1-ell_i at positive separation. Weak inequalities in (1)
retain singleton intersections and isolated equality times.

At a fixed height, union over the parent labels, feasible integer h and
seventh labels k gives the complete folded safe set. Equation (2) and
reflection recover all physical times. Different parents must retain separate
interval records: replacing their disconnected union by one enclosing
interval would again invent points.

This is an exact representation and recovery rule. It does **not** yet supply
a short rule that guarantees one of the intersections (1) is nonempty without
checking relevant slices, nor an induction for arbitrary runner counts.
Explicitly listing h may grow with q. A bounded arithmetic selector needs
additional support/rounding arguments; invertibility alone is not that argument.

## 6. Information-loss checkpoint

| Stored information | What the present evidence permits | Failure or limitation |
| --- | --- | --- |
| Old global maximum and all old maximizing times | Describes the smaller system's optimum | All those times fail 1/8 safety after addition in each declared control |
| Only positive 1/8-safe time intervals | Describes positive duration | At q=4 all such intervals disappear while four isolated points survive |
| Surviving points on old parent edges | Can still select the previously certified A-ray witness | Misses t=17/35 and 18/35 among q=10's final maximizers |
| Each parent slice's old optimal face | Retains more than the single global optimum | Misses the q=10 point inside an old nonoptimal face |
| Separate H and S ranges | Records two individual feasibility tests | Gives a false positive in P2 at q=4, z=1/8 |
| Parent facets with child cuts, or exact conditional J intervals with labels/maps | Preserves the joint geometry, closed endpoints and physical recovery | Does not itself force existence or bound the number of integer slices to inspect |

CC therefore needs to state which question its compressed object answers.
Preserving a scalar value, selecting one witness, classifying every maximizer,
and recovering the whole safe set impose different requirements. In this step,
the needed enrichment is specific: retain the joint orbit/phase dependence and
permit new contacts inside parent faces. More stored detail is useful only
where it restores those consequential distinctions.

**Next bounded question:** turn the conditional-interval description into a
selection certificate for these fixed forms. Identify which parent face and
integer slice must supply a surviving point, with explicit support changes
and rounding rules, while preserving equality. Derive that certificate from
the parent data rather than treating the already known seven-form spectrum
as its proof. General existence for arbitrary configurations remains outside
the present result.

## Reproduction, dependencies and preservation

The [protocol](../reviews/2026-09-29-cc-six-seven-transfer/PROTOCOL.md) was saved
before the new calculation. From the repository root, with standard-library
Python and assertions enabled:

```bash
python3 reviews/2026-09-29-cc-six-seven-transfer/verify_transfer.py > /tmp/cc-transfer.json
python3 reviews/2026-09-29-cc-six-seven-transfer/countercheck.py > /tmp/cc-transfer-countercheck.json
```

The first program intentionally imports the preceding review's clipping and
tent-envelope implementations. The second imports no project implementation:
it reconstructs parent vertices by global planes and optimizes the six declared
physical configurations by opposing contacts and individual tent peaks. It
compares with the primary output only after constructing its own results.
The coordinator already knew those methods; this is separately structured
checking, not independent authorship. Exact closed-band intersections also
recover all maximizing sets and all 1/8-safe components for the controls.

The scripts, exact outputs and [manifest](../reviews/2026-09-29-cc-six-seven-transfer/MANIFEST.json)
preserve the source hashes and scope. The atlas is a fixed finite certificate;
the physical computations cover only q=3,4,10 and their six-form prefixes.
There was no wider q scan, new coefficient family, other reference runner,
large-q test, new agent delegation, main merge, outside contact or unattended
research. Earlier proof packages and manifests are unchanged.

The first six forms' established relative-spectrum and polyhedral context
remains credited in the [original spectrum note](LTCM_EXACT_SPECTRUM_2026_09_29.md)
and its [review](LTCM_ULTRA_REVIEW_2026_09_29.md). No external theorem is used
as a new six-coordinate premise here, no source was newly audited, and no
novelty assessment is made. Independent mathematical review remains open.
