# Compatibility Calculus: two complementary coefficient ranges

September 29, 2026. Source head `64bda7a065abcff312ab0cac17f5b12a49b91221`.

**Result:** the fixed rule discovered for row (3,8) works on 205 infinite
coefficient classes. Requiring its whole leader and only its two actually
used fallback points is exact for this operation: T=R. Requiring the entire
first fallback segment is substantially stronger, admitting only 21 positive
rows. Including repeated-speed p=q changes the answer too: T_all admits 178
classes, excluding 27 classes that work for every p!=q.

The old and new coefficient sets have an exact finite intersection of 10
rows, four of which identically repeat core speeds. Neither range contains
the other; explicit infinite progressions lie exclusively in each. Class
counts 205 and 42 use different periods and must not be compared as set sizes
or evidence of containment.

These are **HYPOTHESIS / internally reviewed proof candidates**, supported
by exact complete reductions and separately structured AI reviews. Material
AI work is disclosed. No external human/formal certification, new Lonely
Runner existence coverage or originality claim is made. The
[frozen protocol](../reviews/2026-09-29-cc-row38-range/PROTOCOL.md) fixes the
questions, proposed reductions, coefficient cells and physical controls.

## 1. Freeze the rule before changing its seventh coefficient

The first six moving speeds remain p,q,p+q,2p+q,3p+q,3p+2q, with a common
start and stationary reference 0. The seventh is now Ap+Bq for positive
integers A,B. Normalize d=gcd(p,q),P=p/d,Q=q/d. The rule inherited from the
[row-(3,8) transfer](CC_ROW38_COMPILER_TRANSFER_2026_09_29.md) first selects
the smallest integral H=Qx-Py available on

\[
L:\quad y=9/8-x,\qquad 1/4\le x\le 3/8.
\]

Only three primitive directions miss L. Direction (1,4) selects
F=(17/56,3/14); direction (2,1) selects G=(9/28,9/56). Both belong to
the preserved first fallback S: y=9/8-3x,7/24<=x<=55/168. The repeated-speed
auxiliary (1,1) selects C=(1/8,1/8) on the third emitted segment.
The time-selection rule and all its geometry stay fixed during classification.

| Contract | Required seventh-row safety | Exact accepted set |
| --- | --- | --- |
| W | Every point of L and every point of S | 21 positive coefficient rows |
| R | Every point of L, plus F and G | 205 classes under +(56,56) |
| T | Every actual output for all positive p!=q | The same 205 classes: T=R |
| T_all | T plus actual p=q output C | 178 classes under +(56,56) |

None of these contracts asks for the entire auxiliary third segment to be
safe. Its only actual use is C. A failed time is not failed loneliness.

For eight distinct speeds retain p!=q and
(A-a)p+(B-b)q!=0 for (a,b)=(1,1),(2,1),(3,1),(3,2). These four coefficient
rows have empty distinct-speed domains and are labelled explicitly. They
remain valid labelled-safety rows. Any seventh failure at p!=q automatically
has eight distinct speeds, because it cannot duplicate one of the six safe
core phases at the same time. Thus the domain restrictions cannot hide a
rejection of T.

## 2. The exact coefficient criterion

For positive integer A,B, the new fixed rule succeeds for every p!=q exactly
when there is one integer m such that

\[
8m+1\le\min(2A+7B,3A+6B)
\le\max(2A+7B,3A+6B)\le 8m+7,
\]

and the two residues obey

\[
(17A+12B)\bmod 56\in\{7,\ldots,49\},\qquad
(18A+9B)\bmod 56\in\{7,\ldots,49\}.
\]

The first line requires both leader endpoint values to occupy the same safe
lap band. Independently safe endpoint residues in different laps would not
suffice. The second line is exactly the safety test at F and G.
To extend the guarantee to p=q, add (A+B) mod 8 !=0.

With delta=A-B, the full accepted residue table lives in
classification.json. Its counts are:

| delta | Accepted B mod 56 for T=R, count | Count for T_all |
| --- | ---: | ---: |
| -6 | 4 | 0 |
| -5 | 9 | 9 |
| -4 | 11 | 8 |
| -3 | 19 | 19 |
| -2 | 19 | 15 |
| -1 | 22 | 22 |
| 0 | 37 | 32 |
| 1 | 22 | 22 |
| 2 | 19 | 15 |
| 3 | 19 | 19 |
| 4 | 11 | 8 |
| 5 | 9 | 9 |
| 6 | 4 | 0 |
| Total | 205 | 178 |

All other delta values are rejected. Preserve A=B+delta>0 and B>0 when
interpreting residue classes. Shifting (A,B) by (56,56) adds raw seventh
values 63 on L,29 at F,27 at G and 14 at C. Fractional phases and selected
times persist; seventh torus and physical laps must still be recomputed.
This is not a period on the entire first fallback S.

## 3. Why sparse actual outputs have this exact range

Put M=P+Q and rho=(P-2M) mod 8. A leader contact exists iff rho<=M, and

\[
(x,y)=\left(\frac 14+\frac{\rho}{8M},
             \frac 78-\frac{\rho}{8M}\right).
\]

All primitive directions are parameterized by M>=2,1<=P<M,gcd(P,M)=1,
Q=M-P. For x>=1/4+epsilon, M<=7/(8epsilon), so only finitely many points
occur away from E=(1/4,7/8). E is selected at (2,3), and (1,4j),j>=2,
gives rho 7,M=4j+1 and distinct points converging to E. The selected leader
support is closed and countable, with E its sole accumulation point; it is
not dense. Excluding p=q removes only C and no leader point.

The raw seventh value is

\[
\frac{9B+2\delta}{8}+\frac{\delta\rho}{8M}.
\]

If a=(9B+2delta) mod 8 is 0, E already fails. If delta>0,a=7 or delta<0,a=1,
the displayed sequence gives small nonzero motion into an unsafe band.
For all remaining nonzero slopes let D=|delta| and c=7-a for positive
delta, or a-1 for negative delta. Then 1<=c<=6. The first open forbidden
band is reached at a sequence point when

\[
\frac{7D/(c+2)-1}{4}<j<\frac{7D/c-1}{4}.
\]

The interval length is at least 7D/96. For D>=14 it exceeds 1, with lower
endpoint at least 45/16. Its floor plus 1 is therefore an admissible integer
j>=3 and produces a strict physical failure. Thus T implies |delta|<=13.

After the endpoint/outward cases are excluded, the available safe margin
is at least 1/8. For |delta|<=13 and M>=91, the drift is at most
7*13/(8*91)=1/8, including closed equality. It suffices to check the
complete finite support M<=91 and the joint period. This yields:

- 2,551 primitive directions, including one p=q auxiliary;
- 2,550 primary directions and 404 distinct finite leader points;
- 27*56=1,512 coefficient cells, using B=b+56,A=B+delta;
- 1,307 primary rejections, each with an actual failed physical certificate.

Every failed endpoint/outward gate already has a witness in this finite
domain: E has M=5; for D<=13 the chosen outward witness has M<=49.
The exact computations find T=R on every cell and no accepted |delta|>6.
The analytic obstruction handles all larger slopes, and the tail handles all
larger directions. These reductions, reviewed before enumeration, supply
the universal argument; a finite successful scan alone would not.

## 4. Two consequential distinctions

**The full first fallback is an unnecessary requirement for this rule.**
W additionally demands a shared safe lap for S's endpoint numerators
49A+42B and 55A+24B over denominator 168, with offsets 21 through 147.
Its width bounds give |A-B|<=6 and |A-3B|<=21, hence B<=13.
The complete 148 positive cases leave exactly these 21 rows:

| B | Accepted A for W |
| --- | --- |
| 1 | 1,2,3,5 |
| 2 | 3,6 |
| 3 | 3,6,7 |
| 4 | 3,5 |
| 5 | 2,5,8,11 |
| 6 | 8 |
| 7 | 7 |
| 8 | 3,13 |
| 9 | 9 |
| 11 | 14 |

For example (59,64) is the phase-preserving lift of (3,8). It passes T and
R, but at the strict interior point(43/133,165/1064) of S its seventh raw
value is 29, hence its seventh phase is 0. All six core phases are safe there.
This is an ambient counterexample to whole-S safety; no claim is made that
this point is selected by the rule. The used fallback points remain safe.

**Adding a repeated-speed auxiliary changes the coefficient question.**
Row (6,2) works for every p!=q under both old and new selectors. But the new
rule chooses C at p=q=1, giving seventh speed 8, time 1/8 and seventh phase 0.
There are only seven distinct speeds in that auxiliary configuration. Its
failure cannot exclude the row from the eight-distinct-speed target. In
total 27 accepted classes fail only this added auxiliary obligation. W and
T_all impose different requirements; neither should silently replace T.

## 5. Compare the two infinite families exactly

The old accepted range lies near A=2B: |A-2B|<=6. The new range lies near
A=B: |A-B|<=6 after classification. Their differing directions explain why
neither is a general replacement for the other.

Before enumeration, the proved new bound 13 and old bound 6 put every shared
positive row inside B<=19,A<=32. The frozen 422-case comparison finds exactly

\[
\{(1,1),(2,1),(3,1),(3,2),(6,2),(3,3),(6,3),(5,4),(8,5),(11,5)\}.
\]

The first four rows identically repeat a core. The remaining six are the
shared coefficient rows with nonempty eight-distinct-speed domains.
No infinite common family is omitted by this proved finite intersection.

Both set differences are infinite. The old-safe progression
(6+16k,2+8k) has new delta=4+8k>13 for k>=2. The new-safe progression
(3+56k,8+56k) has old A-2B=-13-56k, outside the old range for all k>=0.
These symbolic identities prove noncontainment without comparing incompatible
residue counts or running more coefficient trials.

The declared old-only example(38,18) at(p,q)=(1,20) illustrates the reverse
repair: the new rule selects 7/24 with minimum 1/12, while the old rule selects
47/176 with minimum 1/8. The earlier(3,8) example supplied the other direction.

## 6. Exact checks, provenance and limits

The [review package](../reviews/2026-09-29-cc-row38-range/README.md) retains
the protocol, seven pinned source identities, every coefficient decision,
the complete finite support, all rejected physical records and reviews.
The first complete coordinator classification run passes without a code
correction. A pre-enumeration draft typo in the cell count was corrected
from 3,080 to 1,512 without changing its declared ranges; the execution record
retains the timing and both protocol identities.

The frozen physical scope comprises 54 records for rows(3,8),(59,64),(6,2)
on the archived 18 pairs, plus four repeated-core controls. All 18 archived
(3,8) physical records reproduce. The period lift preserves phases and times
while changing laps. Six analytic large-slope controls cover both signs of
14,15 and 10^12+14. The old-only comparison adds one declared pair. The
conditional outside-R controls are not triggered because T=R.

The support reviewer checks topology, both slope signs, tail equality and
the comparison bounds before enumeration. The arithmetic reviewer reconstructs
the selected support through interval projection and checks coefficient
safety through exact forbidden-band tests, without production imports.
The physical reviewer uses coordinate-lap congruences and direct speed
multiplication, preserving zero-aware reflection, gcd and distinctness.
The 1,307 primary and 27 auxiliary rejection certificates are derived from
the complete classification, not held-out experiments. Findings are shared;
separate implementation does not mean blind, human or formal review.

The arithmetic comparison agrees on 32,810 shared fields. The physical
review agrees on 96,202 scalar fields across 1,400 physical records. Each
physical record checks all seven selected/reflected phases and laps; there
are 2,800 alternate Bezout recoveries. All 35 exact result files reproduce
byte-for-byte. These counts describe checks of the same mathematical record,
not additional independent proofs. The review reports preserve a correction
to the archived comparison source and a failure-shard filename assumption;
neither changed mathematical output or expanded the frozen domain.

From the repository root, with standard-library Python 3 without -O:

```sh
python 3 reviews/2026-09-29-cc-row38-range/reproduce.py
```

The prior source packages, compiler rules and selected menu are unchanged.
The existing literature attribution and prior eight-runner existence context
in [CC_LITERATURE_COMPARISON_2026_09_29.md](CC_LITERATURE_COMPARISON_2026_09_29.md)
remain in force; no fresh literature-frontier or originality audit occurred.

## 7. CC checkpoint and next operation

Whole-leader safety exactly preserves the actual selector's coefficient
answer, despite the sparse support. Whole-fallback safety does not: it tests
unused points and discards valid operational coefficients. Adding the p=q
auxiliary also discards valid primary coefficients. The model is adequate
when its obligations track the domain and the role each geometric piece
actually plays. More geometric coverage or a larger input domain does not
automatically preserve the original question.

The two constructions supply complementary infinite coefficient families.
**Next proposed:** build one coefficient-aware dispatcher that checks the
two exact predicates, selects a certified old or new rule, and returns its
physical witness and domain conditions. That would automate their proved
union. A point-by-point combination might reach beyond that union, but it
would change the quantifiers and needs a separate investigation. Neither
combined implementation nor that stronger coverage question has been run here.
