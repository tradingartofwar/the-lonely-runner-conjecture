# Independent arithmetic review: row (3,8) selector coefficient range

September 29, 2026. Algebraic reductions were checked before enumeration.
The independent frozen classification and coordinator field comparisons
are complete and pass.

This is a separately structured AI review, not human or formal certification.
It imports no coordinator implementation. Findings are shared during work;
no blind-replication claim is made.

## Contracts derived before enumeration

The frozen leader has endpoints (1/4,7/8), (3/8,3/4).
Its seventh raw values are (2A+7B)/8 and (3A+6B)/8.
Whole leader safety requires these values to occupy one common closed band
[m+1/8,m+7/8]. Their difference is (A-B)/8, so |A-B|<=6.

The first fallback has endpoints (7/24,1/4), (55/168,1/7).
Its seventh endpoint values are (7A+6B)/24 and (55A+24B)/168.
Their difference is (A-3B)/28. Whole-fallback safety therefore implies
|A-3B|<=21. Together with |A-B|<=6 and positivity, this gives 2B<=27,
hence 1<=B<=13. The exact W domain is finite before any enumeration.
Independent endpoint residues cannot replace the common-band obligation.

The actual fallback contacts are F=(17/56,12/56) and G=(18/56,9/56).
R requires whole-leader safety and residues of 17A+12B and 18A+9B modulo56
in the inclusive interval [7,49]. With delta=A-B, the shift
(A,B)->(A+56,B+56) changes raw phases by 63 on the entire leader,
29 at F and 27 at G. Thus it preserves all relevant fractional phases.
Every reduced representative B=b+56,A=B+delta is positive for b=0,...,55
and delta=-13,...,13. The auxiliary C=(1/8,1/8) has safety condition
(A+B) mod8 !=0; this is an extra obligation for T_all, not part of T.
The full third segment is not classified by T_all.

## Actual support and analytic truncation

For positive primitive P,Q put M=P+Q and h=ceil((2Q-7P)/8).
The leader hits when h<=(3Q-6P)/8. Then
rho=8h-(2Q-7P)=(P-2M) mod8 and
x=1/4+rho/(8M), y=7/8-rho/(8M).
The direct interval derivation requires 1<=P<M, gcd(P,M)=1 and rho<=M.
The known finite complement sends (1,4),(2,1) to F,G, and (1,1) to C.
Removing p=q therefore removes C without changing the leader support.

E=(1/4,7/8) is itself selected at (P,Q)=(2,3).
For P=1,Q=4j, j>=2, one has M=4j+1,rho=7. These distinct selected
points converge to E. For each epsilon>0, x>=1/4+epsilon forces
M<=7/(8epsilon), so E is the sole accumulation point. The support is
countable and closed, rather than dense in the full leader.

At a leader point the seventh value is
(9B+2delta)/8 + delta*rho/(8M).
Write a=(9B+2delta) mod8. If a=0 then E fails. Positive delta at a=7,
or negative delta at a=1, leaves the safe band along the displayed
sequence for sufficiently large j. In all other nonzero-slope cases,
let c=7-a for positive delta, c=a-1 for negative delta, so 1<=c<=6.
Writing D=|delta|, a sequence point lies strictly inside the first
forbidden band whenever

    (7D/(c+2)-1)/4 < j < (7D/c-1)/4.

This open interval has length 7D/[2c(c+2)]>=7D/96>1 for D>=14.
Its lower endpoint is at least (7D/8-1)/4>=45/16>2.
Hence floor(lower)+1 is a valid integer j>=3 strictly inside the interval.
This gives an actual selector failure and proves T implies |delta|<=13.

For the remaining inward cases the directed margin is at least1/8.
When M>=91, |delta|rho/(8M)<=13*7/(8*91)=1/8, so every such leader
point is safe. Thus all positive coprime P,Q with P+Q<=91, together
with the explicit tail exclusions above, exhaust the necessary finite
checks. The boundary M=91 may overlap the finite part harmlessly.

## Comparison with the old selector

The old theorem implies epsilon=A-2B lies in [-6,6]. The new necessary
bound gives delta=A-B in [-13,13]. Consequently a common row has
B=delta-epsilon<=19 and A=2delta-epsilon<=32, with both positive.
This is a proved finite intersection domain before the output is known.
If later T=R, the domain sharpens to B<=12,A<=18.
The old period is (16,8), whereas the new period is (56,56); comparing
raw numbers of residue classes as if they measured the same partition
would lose consequential information.

The known safe old progression (6+16k,2+8k) has new delta=4+8k,
which exceeds13 for k>=2. The known safe new progression
(3+56k,8+56k) has old epsilon=-13-56k, always outside the old bound.
Thus neither selector range contains the other, independently of any
new enumeration. Exact intersection and exclusive examples will be
reported after the frozen computation.

## Independent frozen result

After protocol SHA256
`95811494876e2c62d6c288c21f8ba42b2983e486a25eb6e7b7633a0e0fc8a26a`
was frozen, the reviewer implemented direct segment projection, first integer
contact, and open forbidden-band intersection. The computation uses only
standard-library rational/integer arithmetic and no production imports.

The first complete independent run succeeded without implementation
correction. It gives 2,551 primitive directions, 2,550 primary directions,
2,548 leader directions and 404 distinct leader points in the finite reduction.
All 1,512 reduced coefficient cells were evaluated against every primary
support record. The result is T=R with 205 classes, while T_all has178 classes.
Exactly27 classes are safe for all p!=q and fail the auxiliary C. The 1,307
rejected T cells all have explicit finite primary failures. None requires
replacing a tail rejection with an unsupported finite claim.

The declared148 whole-segment cases give21 positive W rows:

| B | Accepted A |
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

All422 declared comparison cases give exactly10 common coefficient rows:
(1,1),(2,1),(3,1),(3,2),(6,2),(3,3),(6,3),(5,4),(8,5),(11,5).
The first four identically repeat core rows and have empty eight-distinct-speed
domains. The six others are genuine overlapping families, subject to the
explicit distinctness exclusions. No set-containment claim follows from
205 versus42 residue classes; the separate infinite progressions prove both
exclusive directions.

The final old-predicate regression agrees on all216 cells of the protocol-pinned
selector-support classification. During comparison preparation the reviewer
noticed its initial regression had instead read the earlier104-cell
coefficient-range archive; that initial comparison also passed. The final
script now uses the pinned216-cell source. This source-adapter correction
changed no predicate, new trial domain, computed membership or certificate.
The initial shared comparison passed; extending it to all requested shared
fields required only schema adapters for F/G role names and lap fields.

The final comparison matches32,810 fields:15,306 support fields and3 support
counts;15,120 coefficient fields and64 classification summary fields;
1,036 whole-segment fields and3 summary fields;1,266 overlap fields and12
summary fields. A list-valued field is counted once, not once per element.
The independently computed full supports, coefficient table, whole-segment
table and overlap table are retained in `arithmetic_review.json`.
The physical reviewer separately handles recovery and rejection certificates.

Reproduce the arithmetic review after the four coordinator outputs exist:

```sh
python3 reviews/2026-09-29-cc-row38-range/arithmetic_review.py --compare
```

The script writes deterministic JSON to stdout and imports no production code.
There was no mathematical implementation correction, trial expansion, threshold
change or retuned selector. Agreement remains a separately structured AI
review of a proof candidate, not external or formal certification.
