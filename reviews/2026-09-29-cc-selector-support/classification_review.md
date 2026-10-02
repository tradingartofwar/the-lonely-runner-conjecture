# Separately structured review: exact selector classification

September 29, 2026. This is an AI review of the frozen protocol, not external
human review or a formal proof certificate. The argument remains an internally
reviewed proof candidate. No coordinator code is imported.

**Result:** the exact first-integer computation gives **T = T_all = R** for
positive integer seventh rows. Each has the prior **42 residue classes**.
The smaller actual selector support does not enlarge coefficient membership.
The 174 rejected cells each have a directly reconstructed failure with eight
distinct physical speeds, including the stationary reference. These are
failures of this fixed selector, not counterexamples to loneliness.

## Prerequisites checked before enumeration

Write delta = A − 2B, M = Q + 2P and h = ceil((2Q−3P)/8). Directly solving
Qx−Py=h on y=7/8−2x gives

\[
x=\frac{8h+7P}{8M}=\frac14+\frac{\rho}{8M},
\qquad \rho=8h-(2Q-3P)=(-P-2M)\bmod8.
\]

The last expression is the representative in {0,...,7}. Leader membership
is precisely rho≤M. When no leader contact exists, the sole primitive case
is (P,Q)=(1,2), where the fixed output is C=(1/8,1/4). The program implements
the original projected interval rounding directly and verifies this support
formula as an equality; it does not use that formula to choose the point.

The seventh value on a leader contact is

\[
\frac{7B+2\delta}{8}+\frac{\delta\rho}{8M}.
\]

Let a=(7B+2delta) mod8. The left endpoint is itself selected at (2,3),
so a=0 is an immediate genuine distinct-speed failure. For all other a,
its fractional value is a/8 with 1≤a≤7.

### Large slopes: T implies |delta|≤13

Take P=1 and Q=4j−2 for integers j≥2. This is primitive, P≠Q, M=4j,
and rho=7. The displacement from the left endpoint is 7/(32j). Put
D=|delta|>0. If delta>0 and a=7, any integer j≥2 with j>7D/8 has drift strictly
between 0 and 1/4, hence a seventh value inside the open forbidden band
(7/8,9/8), relative to the left endpoint's lap. If delta<0 and a=1,
the same choice enters (−1/8,1/8). In both cases sufficiently large j
therefore fails.

Otherwise the first forbidden band gives these **open** intervals for j:

| Sign | Remaining a | Forbidden j interval |
| --- | --- | --- |
| delta>0 | 1≤a≤6 | (7D/[4(9−a)], 7D/[4(7−a)]) |
| delta<0 | 2≤a≤7 | (7D/[4(a+1)], 7D/[4(a−1)]) |

Their lengths are respectively

\[
\frac{7D}{2(9-a)(7-a)},\qquad
\frac{7D}{2(a+1)(a-1)}.
\]

Each is at least 7D/96. If D≥14 this exceeds 1 strictly. The lower endpoint
is at least 7D/32>3. Therefore floor(lower)+1 is an integer strictly inside
the interval and is an admissible j≥4. It gives an unsafe selected seventh
phase. Equality at safe-band boundaries has not been discarded: the
forbidden interval is open, and the width>1 estimate places j strictly inside.
This proves the cutoff, rather than extrapolating it from a coefficient scan.

For this obstruction, p=P=1, q=Q=4j−2. The six core speeds are distinct and
safe at the selected time. An unsafe seventh speed cannot equal any of them,
since equal speeds have equal phases at that same time. It is also positive,
so it cannot equal the stationary reference. Thus the obstruction applies to
the actual eight-distinct-speed scope as well as the labelled coefficient
contract. The left-endpoint failure uses the same reasoning at (p,q)=(2,3).

### The complete tail after the cutoff

Assume |delta|≤13, a≠0, and exclude the outward boundary cases
(delta>0,a=7) and (delta<0,a=1). For every M≥91,

\[
\left|\frac{\delta\rho}{8M}\right|
\le \frac{7|\delta|}{8M}\le\frac18.
\]

If delta>0 then a≤6, and if delta<0 then a≥2. The drift of at most 1/8
therefore stays in the same closed safe band. For delta=0 the phase is
constant. This proves the tail, including equality at M=91. The bounded
check also includes M=91, an innocuous overlap with the tail.

The derived cutoff and tail proof were sent to the coordinator before this
reviewer ran the finite enumeration. The initial enumeration then used only
the frozen M and coefficient domains.

## Exact complete finite reduction

Coefficient periodicity follows pointwise: adding (16,8) to (A,B) adds 7
to the seventh value on L and 4 at C. Hence membership depends only on
delta and B mod8. The 216 cells use delta=−13,...,13 and the positive
representative B=b+8, A=2B+delta for b=0,...,7. These representatives have
A≥3 and B≥8. The same membership applies to every other positive row in
the residue class, including smaller B, since the value changes by an integer.

The complete bounded primitive domain is obtained without a sampled p,q box:
for 3≤M≤91, use every 1≤P<M/2 with Q=M−2P>0 and gcd(P,Q)=1. It contains
1,275 records. One is the repeated-speed auxiliary (1,1), and one is the
fallback (1,2); the other records use the leader. There are 387 distinct
leader points in this bounded domain. The JSON preserves every direction,
its interval, first integer, point, role, rho and auxiliary flag. Direction
order is increasing M, then P.

For every coefficient cell the checker evaluates exact Fraction phases at
all those points. It retains T and T_all separately, the tail prerequisite
verdict, bounded failure count, first failure and its full physical recovery.
In this complete domain every failed tail prerequisite also has a bounded
failure; an assertion checks that no rejection is left without its declared
physical certificate. The tail proof, not that empirical coincidence, covers
all omitted M.

All 42 accepted cells lie at |delta|≤6 and match the prior R table exactly.
The whole-L condition is separately recomputed from real interval containment
in one closed lap band, then compared to the archived R table. Every one of
the 216 T and T_all verdicts equals that R predicate. There is no accepted
class outside R, so the protocol's conditional extra 18 positive checks do
not trigger.

## Physical counterexamples and preserved scope

For a selected primitive point with Qx−Py=h, solve

\[
Qi\equiv-h\pmod P,\quad 0\le i<P,\qquad
j=(Qi+h)/P,\qquad \tau=(x+i)/P.
\]

For P=1 use i=0. Then P tau=x+i, Q tau=y+j, and 0<tau<1. For
p=dP,q=dQ recover t=tau/d. If m=floor(ax+by), the physical lap of
ap+bq is m+ai+bj. The reviewer checks these laps against direct floor(vt),
and checks the phases against both the torus expression and vt modulo one.
This differs from the coordinator's Bezout-based physical recovery.

For each of the 174 rejected coefficient classes, the first bounded failure
with P≠Q is recovered this way. Every case has the six core phases safe,
the seventh phase unsafe, and exactly eight distinct speeds including zero.
The JSON retains row, pair, selected point, time, seven speeds, torus laps,
physical laps, phases and reflected data. The proof above extends the genuine
failure interpretation to |delta|≥14 and to any positive representative of
each residue class; the recorded certificates themselves are only the 174
chosen representatives.

The first six positive speeds are p,q,p+q,2p+q,3p+q,3p+2q. They are
distinct exactly when p≠q. Positive A,B make Ap+Bq exceed p and q. The
remaining four noncollision requirements are still
(A−a)p+(B−b)q≠0 for (a,b)=(1,1),(2,1),(3,1),(3,2).
The four coefficient rows equal to those core rows have empty
eight-distinct-speed domains. They remain valid labelled safety cases;
neither T=T_all nor the class count converts them to nonempty eight-runner
families. For any other coefficient row, the finite excluded ratios do not
exhaust the positive p,q domain.

## Reproduction and crosscomparison

Run from the repository root, after coordinator outputs exist:

```sh
python3 reviews/2026-09-29-cc-selector-support/classification_review.py
```

The only positive physical controls are the prior archived 54 progression
configurations. All 972 shared archive fields match (18 fields per case).
No new positive coefficient trial was added. The 174 negative cases are
classification-derived certificates, not held-out trials.

After producing its own geometry, classification and physical records, the
reviewer read the coordinator's output JSON and compared keyed records:

| Comparison | Exact field matches |
| --- | ---: |
| All 1,275 bounded direction records | 7,650 |
| All 216 coefficient cells | 1,944 |
| 174 negative certificates plus 54 archived positive controls | 4,332 |

The coordinator had received this reviewer's prerequisite derivation and
initial result counts before the final crosscomparison. This is separately
structured parallel work, not blind replication. The reviewer did not read
or import coordinator implementation code.

One implementation correction is preserved: the first reviewer run used
reflection time 1/d−t, which is a valid equivalent primitive-period reflection,
but the archive uses 1−t. At the nonprimitive (4,6) case its fractional phases
agreed while its reflected time and integer laps differed. The archive-field
assertion caught this. The reviewer changed to the archival 1−t convention
before producing the final JSON. Selection, classification, original witness
times and safety verdicts were unaffected. This is exactly why phase
agreement alone is insufficient for a lap-bearing record.

## Information-loss check

The actual selected support, the whole segment, and all integer contacts are
different sets. This review establishes equality of their **declared
coefficient safety contracts only in the specified comparison T/T_all/R**;
it does not identify the sets themselves. The support result does not imply
density. The matching coefficient classes depend on positive integer rows,
the eighth-grid left phase, the first-integer rule and the fixed threshold.
Changing any of those requires a fresh applicability argument.

No independent human validation, new existence coverage or priority claim is
made. Prior literature attribution remains unchanged. No result-level defect
was found in the frozen reduction; the reflection convention correction is
recorded above.
