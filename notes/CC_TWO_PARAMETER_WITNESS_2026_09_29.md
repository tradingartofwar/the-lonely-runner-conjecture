# Compatibility Calculus: two segments cover the positive two-parameter family

September 29, 2026. Source branch snapshot:
`1696035e73bb53764f431237794cfca342dad002`; mathematical predecessor:
`e37858ffd238a668682289280ee26c6c5e8a0646`.

**Status: HYPOTHESIS / complete proof candidate with internal AI team review.**
The derivation and implementations are materially AI-generated. Finite exact
controls do not replace the infinite argument. Human/formal verification and
literature/novelty assessment remain OPEN.

For every pair of positive integers p != q, the construction below supplies
a time t at which the selected stationary runner is at distance at least 1/8
from all seven common-start runners with speeds

\[
V(p,q)=(p,q,p+q,2p+q,3p+q,3p+2q,5p+2q).
\]

There are eight distinct speeds including zero. The selected minimum distance
is exactly 1/8. This extends our witness certificate from the A and B rays to
the positive two-parameter family. It supplies one witness for the stationary
reference; it does not give the optimal separation, all maximizing times, all
safe times, other reference runners, or arbitrary seven relative speeds.

The two existing safe segments suffice. The change required by the larger
domain is the arithmetic that links a torus point to physical time.

## 1. Primitive compatibility and recovery

Write d=gcd(p,q), P=p/d, Q=q/d. First work with the primitive clock tau and
coordinates x={P tau}, y={Q tau}, with 0<=x,y<1. Then

\[
(x,y)\text{ is on the primitive orbit}
\quad\Longleftrightarrow\quad h=Qx-Py\in\mathbb Z.
\tag{1}
\]

Necessity follows by cancelling PQ tau: h=P floor(Q tau)-Q floor(P tau).
For sufficiency, choose integers r,s with rP+sQ=1 and put

\[
T=rx+sy,\qquad N=\lfloor T\rfloor,\qquad \tau=T-N,\qquad t=\tau/d.
\tag{2}
\]

Indeed, the Bezout identity and (1) give

\[
PT=x-sh,\qquad QT=y+rh,
\]

so P tau=x-sh-PN and Q tau=y+rh-QN. These have fractional parts x,y.
For the original speeds, pt=P tau and qt=Q tau, proving recovery. All selected
points have x>0, so tau is nonzero and 0<t<1/d.

For a row (a,b), let m be its stored torus lap and f=ax+by-m its phase.
The physical speed is v=ap+bq=d(aP+bQ), and its physical lap is

\[
\ell=m+(-as+br)h-(aP+bQ)N.
\tag{3}
\]

Then vt=ell+f exactly. Because every retained f lies in [1/8,7/8], ell is
the actual floor of vt, and the distance from the stationary reference is
min(f,1-f)>=1/8. Negative Bezout coefficients, h, or N cause no problem.

All Bezout choices have the form (r+kQ,s-kP). This shifts T by kh and N by
the same integer. Thus tau is unchanged, and the changes in (3) cancel.
The primitive time is unique modulo one: if two times give the same x,y,
their difference times P and Q is integral, so their difference is integral
by Bezout. The original times are (tau+j)/d modulo one, 0<=j<d; our selector
chooses j=0. Their laps differ from (3) by (aP+bQ)j.

Reflection at the original time t gives 1-t, phases 1-f and laps v-1-ell.
The reflected point need not satisfy the stored fold x<=1/2; this fold is a
geometric storage convention, not a restriction on physical time.

## 2. The same two joint-safe segments

Keep the native rows in order:

\[
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2).
\]

The two segments already preserved in the
[parent-only discovery](CC_SEGMENT_DISCOVERY_2026_09_29.md) and
[B-ray transfer](CC_B_RAY_TRANSFER_2026_09_29.md) have the following data.
Their parent provenance is P3:E0-1:K2 and P1:E1-3:K1 respectively.

| Segment | Closed native coordinates | Torus laps |
| --- | --- | --- |
| P3, tested first | 3/8<=x<=1/2, y=9/8-2x | (0,0,0,1,1,1,2) |
| P1, fallback | 1/8<=x<=5/24, y=7/8-3x | (0,0,0,0,0,1,1) |

For P3 the seven fractional phases are

\[
x,\quad 9/8-2x,\quad 9/8-x,\quad 1/8,\quad
1/8+x,\quad 5/4-x,\quad 1/4+x.
\tag{4}
\]

For P1 they are

\[
x,\quad 7/8-3x,\quad 7/8-2x,\quad 7/8-x,\quad
7/8,\quad 3/4-3x,\quad 3/4-x.
\tag{5}
\]

At both endpoints every entry of the appropriate list lies in [1/8,7/8].
Each is affine in x, so the entire closed segment is safe. P3's fourth phase
is 1/8 and P1's fifth is 7/8; hence every recovered witness has minimum exactly
1/8. This is a simultaneous seven-band assertion at the same point, with all
lap labels retained. No completeness of the full cell atlas is needed to prove
that these two segments are safe.

## 3. P3 covers all but two primitive pairs

Project P3 by h=Qx-Py. Its image is the closed interval

\[
I_3(P,Q)=\left[\frac{3(Q-P)}8,\frac{4Q-P}8\right],
\qquad |I_3|=\frac{Q+2P}{8}.
\tag{6}
\]

If Q+2P>=8, its width is at least one. The integer

\[
h=\left\lceil\frac{3(Q-P)}8\right\rceil
\tag{7}
\]

therefore lies in the interval. The same reasoning includes width equality.
Solving on the segment gives

\[
x=\frac{8h+9P}{8(Q+2P)},\qquad y=\frac98-2x.
\tag{8}
\]

If Q+2P<8, positivity forces P<=3. For P=1, Q<=5; for P=2, Q<=3;
for P=3, Q<=1. Coprimality leaves exactly the eight rows below.

| (P,Q) | I3 | First integer | Outcome |
| --- | --- | --- | --- |
| (1,1) | [0,3/8] | 0 | Safe; repeated-speed auxiliary only |
| (1,2) | [3/8,7/8] | 1 | Miss; use P1 |
| (1,3) | [3/4,11/8] | 1 | Safe |
| (1,4) | [9/8,15/8] | 2 | Miss; use P1 |
| (1,5) | [3/2,19/8] | 2 | Safe |
| (2,1) | [-3/8,1/4] | 0 | Safe |
| (2,3) | [3/8,5/4] | 1 | Safe |
| (3,1) | [-3/4,1/8] | 0 | Safe |

This table is the complete residual domain of a proved finite reduction,
not a parameter-box search. For positive p,q, the seven speeds are pairwise
distinct precisely when p!=q: after the first two, the displayed values
strictly increase and exceed both. Primitive (1,1) is excluded from the main
eight-distinct-runner statement, though the same phase certificate is valid
for the labelled repeated-speed auxiliary.

## 4. P1 closes the two gaps

P1 projects to

\[
I_1(P,Q)=\left[\frac{Q-4P}8,\frac{5Q-6P}{24}\right],
\qquad |I_1|=\frac{Q+3P}{12}.
\]

At (1,2), this is [-1/4,1/6], containing h=0. At (1,4), it is [0,7/12],
again containing h=0. Recover the same point through

\[
x=\frac{8h+7P}{8(Q+3P)},\qquad y=\frac78-3x.
\tag{9}
\]

The primitive times are 7/40 and 1/8 respectively (r=1,s=0). For the
original scaled pairs, divide these times by d. In particular (1,4) uses
P1's endpoint x=1/8. Removing endpoints would erase its only integer contact
on P1, and P3 has no contact at all for that pair. Closed equality is essential.

Equations (1)–(9), the eight-row table, and the affine safety argument complete
the proposed proof for all positive integer pairs in the stated scope.

## 5. A physical example away from both coordinate rays

For (p,q)=(2,3), P3 gives h=1 and (x,y)=(13/28,11/56). Choose r=-1,s=1.
Then T=-15/56, N=-1 and t=41/56. The seven speeds are
(2,3,5,7,9,12,16), and their fractional phases are

\[
\frac1{56}(26,11,37,7,33,44,40).
\]

Every entry lies in [7,49]/56 and the fourth realizes 1/8. This example has
x<=1/2 but t>1/2; neither identifying the fold with a time cutoff nor setting
t=x or t=y is justified. Reflection supplies time 15/56 as another safe time.

## 6. What the model had to retain

The exact nonprimitive compatibility condition is

\[
qx-py\in d\mathbb Z,
\tag{10}
\]

not just membership in Z. On the safe P3 point (x,y)=(13/32,5/16), take
(p,q)=(2,4). Then 4x-2y=1 is integral, but 2x-y=1/2 is not. Its seven
ambient phases are (13,10,23,4,17,27,21)/32, all safe; nevertheless it cannot
be a point of the physical (2,4) orbit. For that orbit, {4t}={2{2t}},
which here would require y=13/16, not 5/16. The lost divisor creates a false
physical witness even when joint geometric safety is intact.

The initial protocol proposed a different point whose raw orbit value is
5/4, so it failed the intended integer premise. That failed fixture and the
analytic replacement above are preserved in
[CORRECTIONS.md](../reviews/2026-09-29-cc-two-parameter/CORRECTIONS.md).

| Representation field | Why the extension needs it |
| --- | --- |
| Primitive pair and original gcd | Distinguish the true orbit from extra components of the raw integer condition |
| Bezout coefficients, floor N, and time scaling | Recover physical time and correct all seven laps |
| Joint segment and lap labels | Keep safety and integer contact at one point |
| Closed endpoints | Retain the (1,4) fallback |
| Separate geometry and arithmetic costs | Prevent the ray's constant selection count from becoming a false whole-algorithm claim |

Two segment tests still suffice after normalization. Gcd computation and
extended Euclid are additional operations with parameter-dependent iteration
counts; this note does not claim a constant number of elementary arithmetic
operations for the complete two-parameter algorithm. The certificate size is
fixed apart from integer bit lengths. The source fold is preserved, while time
is recovered modulo one and then scaled.

## 7. Evidence, provenance, and limits

The [frozen protocol](../reviews/2026-09-29-cc-two-parameter/PROTOCOL.md)
declares the theorem scope, proof obligations, all controls and failure tests.
The coordinator's
[selector.py](../reviews/2026-09-29-cc-two-parameter/selector.py) is a usable
exact implementation: `select(p,q)` returns the selected segment, point,
primitive clock, physical time, speeds, phases and laps. Its main routine
checks only 18 declared pairs: 17 distinct-speed configurations and the
labelled (1,1) auxiliary. It uses no optimizer or broad physical scan.

Three separately tasked AI reviewers found no result-level defect in the orbit,
coverage and physical recovery arguments. Their
reports and exact outputs are in
[the review directory](../reviews/2026-09-29-cc-two-parameter/).
All four exact outputs reproduce byte-for-byte. Three implementations agree on
the 18 selected times, points, phases, laps and reflections; a coordinate-lap
congruence independently recovers all 18 times. The direct physical reviewer
checks 126 selected and 126 reflected distances, with 36 alternative Bezout
recoveries. The coverage reviewer verifies 56 endpoint band inequalities and
all eight residual primitive pairs. See
[REPRODUCTION.json](../reviews/2026-09-29-cc-two-parameter/REPRODUCTION.json).
These counts reuse the same controls rather than adding configurations.
The general argument is the derivation
above, including the complete finite triangle; the controls check implementation
and translation. Agreement among AI reviewers is not human or formal proof.

This reuses the existing two geometric segments; it does not alter or rerun
the frozen discovery ranking, whose B output still contains two segments.
P3 alone remains sufficient on B, and the two old packages remain unchanged.
The A/B exact-spectrum results are not premises of this witness proof.

Standard affine convexity, integer interval rounding and elementary Bezout
arithmetic provide the needed complementary framework. The CC modification
is to retain the primitive orbit and arithmetic recovery record explicitly;
none of these standard operations is claimed as a CC invention. No external
theorem or other author's altered hypotheses is imported. Prior six-form
literature recorded in the earlier source notes does not by itself establish
this appended-seven-form claim. A targeted literature comparison of this
precise family remains OPEN; no novelty claim is made.

### Representation record

- **Question/output:** one physical 1/8-safe time for the selected stationary
  reference, positive integer p!=q, fixed seven coefficient rows, common start.
- **Retained/operation:** two closed segments, row/lap identity, primitive
  normalization, integer contact, Bezout clock, lap map, reflection and costs.
- **Omitted:** other safe points, exact optimum, all maximizers and other
  reference runners. These cannot be recovered from the two segments alone.
- **Richer source/recovery:** pinned parent input and existing full seven-form cell
  atlas via the predecessor packages. Restore that geometry before changing
  the output to optimization or complete safe sets. Equations (1)–(3) attach
  the current family's actual orbit and physical map to any recovered point.
- **Evidence/limits:** complete elementary proof candidate plus exact finite
  controls and internal AI review. Neither a universal discovery theorem nor
  a general Lonely Runner result follows.
- **Failure tests:** omitted gcd, wrong clock/laps, lost endpoints, uncovered
  primitive pair, or a changed coefficient/threshold/reference. Recheck the
  model when any of these changes; do not transplant the old clock.

**Next proposed step:** assess the broader significance of this exact family
against existing results and perform an adversarial line-by-line review of
the two-parameter proof. That comparison and any change of selected reference
are separate tasks. No new reference-runner analysis is performed here.
