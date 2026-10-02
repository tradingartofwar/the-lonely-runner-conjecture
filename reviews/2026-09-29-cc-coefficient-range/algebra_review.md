# Independent algebra review: fixed leader and role-specific fallback

September 29, 2026. Status: separately structured AI review of an internally
generated proof candidate. This is not external human review, formal proof
certification, or a novelty determination.

## Verdict and review method

The two proposed geometric contracts are soundly separable and exactly
classifiable within the frozen scope. The independent calculation finds:

- W has exactly **31 positive integer coefficient rows**, from the complete
  **147-case** finite reduction.
- R has exactly **42 residue classes**, specified by delta=A−2B and B mod 8,
  subject to A>0 and B>0. Each accepted class supplies infinitely many rows.
- W is a proper subset of R. Row (22,10) is an explicit witness to properness.
- The closed threshold and a shared lap on each complete segment are essential.
- These results classify the two declared geometric contracts. They do not
  classify all coefficients for which some other menu, parent interior, or
  every actually selected deterministic output could be safe.

`algebra_review.py` imports only the Python standard library and does not
import coordinator, compiler, transfer, or physical-recovery implementations.
It computes each affine image directly from coordinate endpoints and rejects
it when that closed interval intersects an open forbidden band
(n−1/8,n+1/8), n integer. This is separate from testing the coordinator's
scaled-integer containment predicates. Its full record is
`algebra_review.json`.

Reproduce from the repository root:

```sh
python3 reviews/2026-09-29-cc-coefficient-range/algebra_review.py
```

## Necessity and sufficiency from connected images

The safe real set is the disjoint union of closed intervals
[m+1/8,m+7/8], m integer. A connected interval is entirely safe if and only
if it is contained in one such interval. If it met two different components,
it would also contain the unsafe gap between them. For an affine function
on a segment, its image is precisely the closed interval between its endpoint
values. Thus safe endpoint residues with *different* integer laps do not
certify a safe segment.

Let u=2A+3B, v=3A+B, w=A+2B. On the leader
L: y=7/8−2x, 1/4≤x≤3/8, the endpoint values are u/8 and v/8.
The full leader is safe exactly when one integer m satisfies

    8m+1 ≤ min(u,v) ≤ max(u,v) ≤ 8m+7.

On the fallback F: x=1/8, 3/16≤y≤1/4, its image is
[u/16,(u+B)/16], because B>0. The full fallback is safe exactly when one
integer n satisfies

    16n+2 ≤ u ≤ u+B ≤ 16n+14.

The upper endpoint C=(1/8,1/4) has value w/8. It is safe exactly when
w modulo 8 belongs to {1,2,3,4,5,6,7}. Its lap is floor(w/8).
Consequently the first two containment conditions characterize W, and the
leader condition plus the C residue condition characterize R. Every safe
segment has a unique integer lap. This seventh lap must be recomputed for the
new row; it is not an invariant of the segment's provenance.

The first-six lap labels remain sound independently of the seventh row.
At L's two endpoints the six fractional phases, in eighths, are
(2,3,5,7,1,4) and (3,1,4,7,2,3), with laps (0,0,0,0,1,1).
At F's two endpoints the six fractional phases, in sixteenths, are
(2,3,5,7,9,12) and (2,4,6,8,10,14), with all six laps zero.
Every entry is in the relevant closed safe band. Affinity certifies each
whole segment for the core rows.

## Exact finite reduction for W

Write delta=A−2B. The leader image has length |delta|/8, so containment in
a safe component of length 3/4 implies |delta|≤6. The fallback image has
length B/16, implying B≤12. Positivity gives B≥1 and 2B+delta>0.
Therefore every W row lies in the protocol's 12×13 rectangle; removal of
5+3+1 nonpositive-A positions leaves exactly 147 cases. There is no
unexamined positive coefficient row outside these proved bounds that could
satisfy W. The width bounds alone are necessary, not sufficient.

The complete accepted list is:

| B | Accepted A values for W |
| --- | --- |
| 1 | 1, 2, 3, 4 |
| 2 | 3, 6, 7 |
| 3 | 5, 6, 8, 9 |
| 4 | 5, 7, 11 |
| 5 | 4, 10, 11, 13 |
| 6 | 9, 10, 16 |
| 7 | 9, 15, 16 |
| 8 | 14, 15, 21 |
| 9 | 20 |
| 10 | 19 |
| 11 | 25 |
| 12 | 23 |

The absolute leader bound is attained in W by (A,B)=(4,5), delta=−6,
whose L image is [17/8,23/8]. Its endpoints attain both closed safe-band
edges. The fallback bound is attained in W by (23,12), whose F image is
[41/8,47/8], again attaining both edges. Opening either of these bands would
incorrectly reject these coefficients.

A nuance matters: W has no delta=+6 row. With delta=6, leader safety forces
B≡3 modulo 8. Under B≤12 these are B=3 and B=11; their F images fail the
single-component test. Thus |delta|≤6 is sharp as an absolute bound, but
its two signs are not both attained in W. R does attain delta=+6, as its
table shows. Do not call the W coordinate bounds sufficient or claim
symmetric attainment.

## Complete residue reduction for R

For fixed delta,

    u=7B+2delta, v=7B+3delta, w=4B+delta.

Increasing B by 8 and A by 16 adds 56 to both u and v, shifting the leader
lap by 7; it adds 32 to w, shifting C's lap by 4. Fractional safety on L
and at C is therefore unchanged. This proves periodicity algebraically,
without extrapolating from a long coefficient scan. Conversely every
positive A,B has a definite delta and residue B mod 8, so the 13×8 table
is exhaustive once |delta|≤6 is imposed.

The independent checker evaluates all 104 entries with positive
representatives B=b+8 and A=2B+delta. It retains the full table, including
rejections and offending forbidden-band centers, in JSON. The accepted
residues are:

| delta | Accepted B modulo 8 for R |
| --- | --- |
| −6 | 5 |
| −5 | 0, 7 |
| −4 | 2 |
| −3 | 3, 4, 5, 6 |
| −2 | 0, 1, 5, 6, 7 |
| −1 | 0, 1, 2, 3, 4, 7 |
| 0 | 1, 3, 5, 7 |
| 1 | 0, 1, 4, 5, 6, 7 |
| 2 | 0, 1, 2, 3, 7 |
| 3 | 2, 3, 4, 5 |
| 4 | 6 |
| 5 | 0, 1 |
| 6 | 3 |

Use **both** positivity conditions B≥1 and 2B+delta≥1; a residue is not
a license to include B=0 or A≤0. Equivalently B must exceed
max(0,−delta/2). In particular the first nominal B=2 in the delta=−4
class gives A=0 and is excluded, as is B=1 in the delta=−2 class.
The infinite rays can be written B=b+8j, A=2B+delta, retaining exactly
those integer j satisfying these positivity conditions.

W implies R because C belongs to F. The independent finite check verifies
this for every listed W row and verifies that each finite-domain R verdict
agrees with the residue table. Proper inclusion follows from (22,10).

## Frozen countercontrols and changed laps

For row (22,10), L's image is [37/4,19/2], entirely safe in lap 9.
The two F endpoints have values 37/8 and 21/4; each is individually safe,
but their laps are 4 and 5. At the interior native point (1/8,9/40), the
seventh value is exactly 5, a collision. C has value 21/4 and remains safe.
Thus R accepts (22,10), W rejects it, and checking endpoint residues alone
would make a concrete false-positive claim about the whole fallback. This
is an ambient geometric control, not a physical counterexample.

On the predeclared progression (A,B)=(6+16j,2+8j), j≥0, the added affine
form is j(16x+8y). It equals 7j everywhere on L and 4j at C. Hence the
fractional phases on the *obligated* geometry are exactly preserved, while
the seventh laps become 2+7j on L and 1+4j at C. Retaining old labels 2
and 1 instead would fail phase reconstruction whenever j>0. Away from C
on F, 16x+8y ranges from 7/2 to 4 and is not a constant integer; the
progression does not preserve the whole fallback's safety.

For (4,2), the entire L has seventh value 7/4 and is safe, but C has
value 1 and collides. Leader safety alone therefore cannot discharge the
fallback obligation. For (5,2), L starts at seventh value 2 and is unsafe;
its previously established success on a different menu does not repair
this fixed-geometry contract. Physical time controls are owned by the
separate physical review; this algebra review runs no new physical cases.

## Domain, interpretation, and implementation correction

For positive A,B, Ap+Bq exceeds p and q. Eight distinct total speeds still
require p≠q and separation from p+q, 2p+q, 3p+q, 3p+2q. The four equations
excluded are respectively

    (A−1)p+(B−1)q=0,
    (A−2)p+(B−1)q=0,
    (A−3)p+(B−1)q=0,
    (A−3)p+(B−2)q=0.

The accepted W rows (1,1), (2,1), (3,1), (3,2) duplicate a core coefficient
row identically. Their labelled geometric safety is valid, but their
corresponding eight-distinct-speed domains are empty. This does not change
the contract classification; it must not be compressed into an assertion
that all 31 rows yield genuine eight-distinct-speed instances.

The first execution of the independent script contained an incorrect
expected count of 144 positive cases. Its assertion stopped before an
output file was emitted. The count was corrected to 147=156−(5+3+1), with
no changes to interval predicates, trial domain, selection rules, or result
criteria. This is a reviewer bookkeeping correction, not a mathematical
protocol change or outcome-driven retuning.

A useful CC distinction is now explicit: "whole fallback geometry is safe"
and "the only fallback contact actually needed is safe" are different
proof obligations. The second supports an infinite coefficient range even
when the first finite range is exhausted. This is a change in supported
contract, not newly discovered geometry, a new held-out transfer, or evidence
that rejected coefficients lack Lonely Runner witnesses.

## Cross-comparison with coordinator implementation

After the independently structured interval audit was completed, the coordinator
emitted `classification.json` using scaled-integer safe-band containment.
The review compared the complete datasets, normalizing the different row schemas:

- All 147 finite-domain coefficient rows agree on individual L, F, C safety
  and on both W and R verdicts.
- The complete list of 31 W rows agrees exactly.
- All 104 residue-table R verdicts agree, including every rejection.
- Every accepted residue list agrees, giving the same 42 classes.

No independent core predicate or output JSON changed for this comparison.
The algebra JSON separately reproduces byte-for-byte, with SHA256
`254bde2ee1f570ffbe1b1cb17e47b7976aafc5c3e2b0310ed500cadd6b0026ed`.

The reviewers worked in parallel, but the coordinator received this review's
counts and table before completing the coordinator implementation. The two
methods are independently structured, **not blind**; their agreement is an
internal implementation and mathematical cross-check, not a claim of
independent external validation.
