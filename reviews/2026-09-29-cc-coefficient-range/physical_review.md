# Role-aware coverage and physical recovery review

September 29, 2026. Separately tasked AI review, using exact rational
arithmetic and coordinate laps. No production implementation is imported.
This is internal review of a proof candidate, not external mathematical or
formal certification. The protocol and prior changed-coefficient package
are the inputs; earlier packages remain unchanged.

The initial reviewer reconstruction and 54-case run preceded the coordinator's
implementation. The coordinator subsequently read this reviewer code before
writing its own implementation; the later comparison is therefore a separately
structured arithmetic check, not a claim of blind independent implementation.

**Result:** no equation or scope defect was found in the role-aware contract
R, its physical recovery, the proposed progression, or the two predeclared
negative controls. The direct controls pass for all 54 declared progression
configurations. The k=0 outputs reproduce the archived changed-row outputs
for all 18 parameter pairs, including reflection and physical laps.

## 1. Why R is enough for the stated task

The first six phases on L are

\[
x,\quad 7/8-2x,\quad 7/8-x,\quad 7/8,\quad
x-1/8,\quad 3/4-x,
\qquad 1/4\le x\le3/8.
\]

They are affine with both endpoint values in the closed band [1/8,7/8].
At C=(1/8,1/4), the first six phases are
(1/8,1/4,3/8,1/2,5/8,7/8). Thus the fixed core is safe on every required
point of R. These checks retain equality.

For positive p,q, divide by d=gcd(p,q) and put P=p/d,Q=q/d. The orbit
functional H=Qx-Py increases along L, from (2Q-3P)/8 to (3Q-P)/8.
Its width is (Q+2P)/8. If this is at least 1, the ceiling of its lower
endpoint belongs to the closed interval. The exact finite complement
Q+2P<8 consists of the eight primitive pairs recorded in
`physical_review.json`; only (1,2) has no integer contact. At that pair,
H(C)=0. All other directions therefore use L, and the sole remaining
primitive direction uses C.

Consequently whole-L seventh safety and seventh safety at C suffice for
one safe time in every positive direction. No assumption about F away
from C enters this implication. The complete integer-contact complement,
not a finite physical sample, is what makes this coverage argument uniform.
This does not assert that R is the largest set on which every actual
selected point happens to remain safe.

For row (A,B), L's raw seventh values at its endpoints are
(2A+3B)/8 and (3A+B)/8. A continuous real interval can stay in the periodic
safe set only if it stays in one of its disconnected closed bands
[m+1/8,m+7/8]. The same-lap endpoint test in the protocol is therefore
necessary and sufficient for whole-L safety. At C the value is (A+2B)/8,
whose phase is safe exactly when A+2B is nonzero modulo 8. Thus R's two
declared obligations are exact, while the resulting physical guarantee
is a sufficient construction criterion.

## 2. Independent physical clock and lap reconstruction

Given a selected point (x,y) and integer h=Qx-Py, choose the unique
integer i with 0<=i<P satisfying Qi=-h modulo P; at P=1 use i=0.
This exists because gcd(P,Q)=1. Set

\[
j=(Qi+h)/P,\qquad \tau=(x+i)/P,\qquad t=\tau/d.
\]

Then P\tau=x+i and Q\tau=y+j. Since 0<x<1, this gives 0<\tau<1.
For any coefficient row (a,b), with recomputed torus lap m and phase
f=ax+by-m, its physical speed obeys

\[
(ap+bq)t=(aP+bQ)\tau=(m+ai+bj)+f.
\]

Thus its physical lap is m+ai+bj. This route uses coordinate congruences,
rather than the production Bezout clock. Direct multiplication by every
physical speed checks the result. Reflection uses t'=1-t, as in the
archive, so each safe phase becomes 1-f and each lap becomes
(ap+bq)-(m+ai+bj)-1. Using a primitive-period reflection would give a
different physical time for nonprimitive inputs, so the archive convention
is kept explicit.

## 3. Exact distinct-speed domain

The core speeds p,q,p+q,2p+q,3p+q,3p+2q are all positive. Its last four
strictly increase and exceed p and q. Its only possible core collision is
p=q. For positive integers A,B, Ap+Bq exceeds p and q, but it can coincide
with one of the four remaining core speeds. Therefore the eight-speed
claim, including reference speed 0, requires exactly

\[
p\ne q,\qquad
(A-a)p+(B-b)q\ne0
\quad\text{for }(a,b)\in\{(1,1),(2,1),(3,1),(3,2)\}.
\]

The construction is still a labelled safety construction when a collision
is present; that does not make the configuration eight distinct runners.
In particular the coefficient class and the physical distinctness domain
must remain separate records. For the progression below the seventh speed
exceeds 3p+2q, so p!=q alone suffices there. The three progression cases
with (p,q)=(1,1) are explicitly repeated-speed auxiliaries.

## 4. Uniform progression, and the bounded numerical controls

For (A,B)=(6+16k,2+8k), k>=0,

\[
Ax+By=(6x+2y)+k(16x+8y).
\]

On L, 16x+8y=7. The original seventh phase is 2x-1/4, in [1/4,1/2],
and the new torus lap is 2+7k. At C, 16x+8y=4; its phase remains 1/4
and its torus lap is 1+4k. This proves the progression satisfies R for
every k>=0. It is an algebraic invariance statement, not extrapolation
from the three tested values of k.

The point and coordinate laps i,j depend only on p,q. On each role, with
c=7 on L or c=4 at C, the physical seventh lap changes by

\[
k(c+16i+8j).
\]

This follows from the recovery identity and is an integer. It also shows
why equal fractional phases do not authorize retaining old seventh laps.
For every one of the 36 controls with k=1,2, subtracting the stale torus
lap produces a claimed phase greater than 1, instead of the true safe
phase. Reducing this wrong value modulo 1 would hide the incorrect lap.

The program evaluates only k=0,1,2 and exactly the 18 protocol parameter
pairs for each. All 54 have minimum distance exactly 1/8. There are 51
distinct-speed configurations and three repeated-speed auxiliaries. It
checks 378 selected phase values, 378 selected laps, 378 reflected phase
values and 378 reflected laps. All 18 k=0 cases match the preserved
changed-coefficient archive on 15 physical fields.

## 5. Controls that distinguish the contracts

For (A,B)=(22,10), the raw seventh values at F's endpoints are
37/8=4+5/8 and 21/4=5+1/4. Both endpoint residues are safe, but their laps
differ. At the declared interior point (1/8,9/40), the raw value is 5,
so the seventh phase is 0. Whole-F safety therefore fails. C is the safe
upper endpoint, and the role-aware selector only uses that point of F;
the progression argument proves this row satisfies R. The bad point is
an ambient segment control, without any extra physical parameter pair
being tested. It is not a failure of the role-aware physical selector.

The predeclared two physical negative controls both fail exactly:

| Seventh row | (p,q) | Selected role and point | Selected time | Seventh speed and phase |
| --- | --- | --- | --- | --- |
| (4,2) | (1,2) | C=(1/8,1/4) | 1/8 | speed 8; phase 0 |
| (5,2) | (2,3) | L at (1/4,3/8) | 1/8 | speed 16; phase 0 |

For (4,2), the entire leader has phase 3/4, but the necessary fallback
point collides. For (5,2), the fixed leader starts at a collision. Both
physical configurations have distinct speeds. These are failures of this
fixed certificate, with no claim that the corresponding configurations
lack other lonely times. In particular the archived original-row (5,2)
construction uses a different menu and remains intact.

## 6. CC information-loss check and reproduction

Whole-F safety imposes information about unused points. R retains the
specific conditional relation between the exceptional orbit and the used
fallback point, making its obligation smaller without losing the stated
one-witness guarantee. Conversely forgetting the fallback role entirely
fails at (4,2), and forgetting lap labels fails on the progression. Equal
endpoint residues do not preserve connected-segment safety when laps
change. The smallest adequate representation depends on the operation.

Run from the repository root:

```sh
python3 reviews/2026-09-29-cc-coefficient-range/physical_review.py
```

The output is `physical_review.json`. No expanded coefficient or physical
scan, re-clipping, new menu discovery, optimization, or literature-priority
claim is part of this review. The symbolic argument remains an internally
reviewed proof candidate.

## 7. Coordinator-output comparison

After the independent output was written, `witnesses.json` was compared
against it by the intersection of each paired record's keys. All 19 shared
fields on each of 54 progression cases agree (1,026 field comparisons),
and all 18 shared fields on each of two negative controls agree (36 more).
All six shared summary counts agree. This includes selected points,
primitive and physical times, seven physical speeds, torus and physical
laps, direct and reflected phases, reflected laps and times, role, minimum,
and distinctness. The reviewer-only coordinate laps remain a separate
recovery record; the coordinator records its Bezout route instead.

The original reviewer program and JSON were unchanged for this comparison.
The provenance caveat at the start applies: the coordinator had read the
reviewer's implementation before writing its separately structured route.
