# Compatibility Calculus: the compiler repairs a rejected coefficient row

September 29, 2026. Source head:
ae6aeaf09780c93df99eba1757dedf7df2c31c02.

**Result:** the unchanged compiler produces a complete safe menu for seventh
row (3,8), which the prior fixed L/C selector rejects. The known failed pair
(p,q)=(1,4) receives a different, safe physical time. This is a successful
transfer to one deliberately chosen input outside that selector's range.
It does not establish arbitrary-coefficient portability or new existence
coverage. The universal construction remains an internally reviewed proof
candidate, with material AI implementation and separate AI reviews disclosed.

The [frozen protocol](../reviews/2026-09-29-cc-row38-transfer/PROTOCOL.md)
was fixed before new-row clipping, ranking or physical evaluation. Row (3,8)
was chosen because it is the first rejected representative in the preceding
ordered table. This was an informed challenge, not a blind trial. No alternate
row, new ranking, larger budget or extra candidate class was tried afterward.

## 1. The family and the concrete repair

For positive integer p,q, the speeds including the stationary reference are

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,3p+8q).
\]

All runners start together. The closed target distance is 1/8. Eight speeds
are distinct exactly when p!=q; the auxiliary p=q case remains labelled.
The guarantee concerns one safe time for this selected reference.

At (p,q)=(1,4), the moving speeds are (1,4,5,6,7,11,35):

| Construction | Time | Seventh phase | Seventh distance | Minimum over seven moving runners |
| --- | --- | --- | --- | --- |
| Old fixed L/C rule | 5/16 | 15/16 | 1/16 | 1/16; fails |
| New emitted menu | 17/56 | 5/8 | 3/8 | 1/8; passes |

The new exact phases are
(17/56,3/14,29/56,23/28,1/8,19/56,5/8), and physical laps are
(0,1,1,1,2,3,10). Thus this comparison changes the actual time and repairs
the physical failure. It does not reinterpret the old rejected output as safe.

## 2. What the unchanged procedure emitted

The runtime imports the prior parameterized edge clipper and the original
compile_records/select functions without editing them. Two regressions first
reproduce every non-provenance field of the archived (5,2) and (6,2)
certificates; no old physical controls are rerun. The new selection inputs are
the same six-form parent geometry, row (3,8) and threshold 1/8.

The declared box gives 11/8<=3x+8y<=17/2, hence seventh laps 1..8.
The 24 floor edges have at most 192 possible edge/lap attempts, within the
unchanged 256 cap. The actual run needs 38. Its 49-pair leader rectangle is
below the unchanged 400-pair budget. The first complete run needs no
implementation correction.

| Quantity | Emitted result |
| --- | --- |
| Clipped candidate records | 38, including five point records |
| Descending candidates eligible to lead | 22 |
| Selected leader | P5:E0-3:K7 |
| Bounding rectangle | 49 lattice pairs |
| Primitive residual domain | 17 pairs |
| Complete candidate/residual matrix | 646 contacts |
| Leader misses | (1,1), (1,4), (2,1) |
| First fallback repairs | (1,4), (2,1) |
| Second fallback repairs | (1,1), repeated-speed auxiliary |

The emitted menu, in its preserved order, is:

| Role | Closed geometry | Seven torus laps |
| --- | --- | --- |
| Leader P5:E0-3:K7 | y=9/8-x, 1/4<=x<=3/8 | (0,0,1,1,1,2,7) |
| Fallback P2:E0-1:K2 | y=9/8-3x, 7/24<=x<=55/168 | (0,0,0,0,1,1,2) |
| Auxiliary fallback P0:E0-1:K1 | x=1/8, 1/8<=y<=3/16 | (0,0,0,0,0,0,1) |

Five point records represent three distinct geometric points with repeated
provenance. They are retained as records; no point is eligible to lead and
none is selected in the final menu. The vertical third segment is a valid
fallback even though it cannot lead the descending-width argument.

## 3. Why the certificate covers infinitely many inputs

On the leader, the seven labelled fractional phases are

\[
x,\quad 9/8-x,\quad 1/8,\quad x+1/8,\quad
2x+1/8,\quad x+1/4,\quad 2-5x.
\]

On the first fallback they are

\[
x,\quad9/8-3x,\quad9/8-2x,\quad9/8-x,\quad
1/8,\quad5/4-3x,\quad7-21x.
\]

On the auxiliary fallback they are
(1/8,y,1/8+y,1/4+y,3/8+y,3/8+2y,8y-5/8).
Every listed phase lies in [1/8,7/8] at both endpoints and is affine;
therefore each entire closed segment is safe. A constant phase 1/8 also
makes the minimum distance exactly 1/8 on each selected segment.

Normalize d=gcd(p,q), P=p/d, Q=q/d. The leader projects under H=Qx-Py to

\[
I(P,Q)=\left[\frac{2Q-7P}{8},\frac{3Q-6P}{8}\right],
\qquad |I(P,Q)|=\frac{P+Q}{8}.
\]

For P+Q>=8 this closed interval contains an integer. The rule rounds its
lower endpoint upward and recovers the point

\[
h=\left\lceil\frac{2Q-7P}{8}\right\rceil,\qquad
x=\frac{8h+9P}{8(P+Q)},\qquad y=9/8-x.
\]

The exact complement consists of the following 17 positive coprime pairs
with P+Q<8. This domain follows from the width bound, not an empirical scan:

| (P,Q) | Leader interval | First integer | Contact? |
| --- | --- | --- | --- |
| (1,1), auxiliary | [-5/8,-3/8] | 0 | no |
| (1,2) | [-3/8,0] | 0 | yes |
| (1,3) | [-1/8,3/8] | 0 | yes |
| (1,4) | [1/8,3/4] | 1 | no |
| (1,5) | [3/8,9/8] | 1 | yes |
| (1,6) | [5/8,3/2] | 1 | yes |
| (2,1) | [-3/2,-9/8] | -1 | no |
| (2,3) | [-1,-3/8] | -1 | yes |
| (2,5) | [-1/2,3/8] | 0 | yes |
| (3,1) | [-19/8,-15/8] | -2 | yes |
| (3,2) | [-17/8,-3/2] | -2 | yes |
| (3,4) | [-13/8,-3/4] | -1 | yes |
| (4,1) | [-13/4,-21/8] | -3 | yes |
| (4,3) | [-11/4,-15/8] | -2 | yes |
| (5,1) | [-33/8,-27/8] | -4 | yes |
| (5,2) | [-31/8,-3] | -3 | yes |
| (6,1) | [-5,-33/8] | -5 | yes |

The first fallback projects to
[(7Q-6P)/24,(55Q-24P)/168]. At (1,4) this is [11/12,7/6], containing
h=1 and producing point (17/56,3/14). At (2,1) it is [-5/24,1/24],
containing h=0 and producing (9/28,9/56), primitive time 9/56.
The final fallback contains (1/8,1/8), resolving (1,1).

It follows directly from this emitted table that the first two segments
already cover every positive primitive P!=Q. The third serves only P=Q=1,
which scales to repeated-speed p=q. This is a post-run deduction about the
declared domain, not a retuned two-segment run or proof of minimality. Keep
all three entries in the compiler artifact and the original ranking intact.

For each integral orbit contact choose rP+sQ=1 and put
N=floor(rx+sy), tau=rx+sy-N, t=tau/d. A row (a,b) with torus lap m has
physical lap m+(-as+br)h-(aP+bQ)N. This is the inherited recovery identity;
the seventh speed and lap are recomputed for (3,8).

## 4. Verification and equality

All 18 frozen parameter pairs yield physical witnesses: 17 distinct-speed
configurations and one labelled auxiliary. Every minimum is exactly 1/8.
Direct phases/laps, reflection 1-t and alternative Bezout recovery agree.
These are new configurations under (3,8), not old physical reproductions.
The two archived certificate regressions remain a separate check.

The geometry reviewer reconstructs candidates using all labelled inequalities
and all stored parent halfspaces, with no production imports. It checks 532
endpoint band incidences, 1,064 parent-halfspace incidences and every reached
coverage field; 5,339 scalar field comparisons agree. The physical reviewer
uses coordinate-lap congruences and direct speed multiplication rather than
the production Bezout clock. All 18 physical records pass, including 126
checks in each selected/reflected phase/lap category and 36 alternate Bezout
recoveries. All five exact output files reproduce byte-for-byte. Detailed
results are retained in the
[review package](../reviews/2026-09-29-cc-row38-transfer/README.md).

Opening both endpoints of every selected segment loses contacts on
(1,1),(1,2),(2,3),(5,2),(4,6) among the 18 controls. Removing the auxiliary
and identifying scaled duplicates leaves three distinct-speed primitive
directions: (1,2),(2,3),(5,2). Opening the full 38-candidate set loses none
of the 18 contacts. The selected menu needs equality for these selections;
the larger candidate set supplies other contacts. No conclusion about all
physical witnesses requiring endpoints follows.

The complete menu leaves no uncovered primitive pairs. Therefore the richer
parent-interior diagnostic is NOT_TRIGGERED. This run does not exercise or
validate that conditional repair path. No broader scan or optimizer was used.

Reproduce the frozen results from the repository root:

```sh
python3 reviews/2026-09-29-cc-row38-transfer/reproduce.py
```

## 5. CC information-loss checkpoint and next question

The old fixed selector is sufficient for its declared coefficient range,
but its rejection cannot answer whether another edge menu succeeds. That
next operation requires the richer parent-edge records. Recovering those
records was enough here: the two-coordinate model, parent atlas and compiler
selection rule all remain adequate for this one-witness task. No new model
or changed discovery rule is needed for this transfer.

The auxiliary (1,1) case affects the emitted menu size, even though it is
outside the eight-distinct-speed target. Five point records are not five
distinct points. Opening a compact menu and opening all candidates are
different operations. Preserve these distinctions when compressing the result.

The unchanged compiler has now repaired a known failure of the old fixed
selector by choosing different geometry. This is evidence of portability to
this specific challenging row; it neither classifies all compiler inputs nor
shows that its successful-input set contains every row in the old 42 classes.
Preprocessing data and online costs also differ: at most three menu tests
(two on the distinct-speed domain), plus variable-cost gcd/Bezout arithmetic.
No optimal-menu or constant-time claim is made.

The [existing literature comparison](CC_LITERATURE_COMPARISON_2026_09_29.md)
continues to govern attribution: the threshold segment mechanism adapts the
Jain–Kravitz precedent, and prior eight-runner existence coverage was already
recorded through Rosenfeld. No new external source audit or originality claim
was undertaken here. The advance is an explicit, reviewable construction.

**Next proposed:** freeze a coefficient-range analysis for this newly emitted
rule on the distinct-speed domain. Separate whole-segment safety from safety
at the actual selected points, and retain the fallback's two used contacts.
Compare the resulting range with the old selector only after those quantifiers
are fixed. No further coefficient classification or transfer has been run.
