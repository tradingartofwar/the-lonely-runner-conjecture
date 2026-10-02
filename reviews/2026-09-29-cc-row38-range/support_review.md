# Separate support and finite-reduction review

September 29, 2026. Materially AI-generated mathematical review. This is a
separately tasked and structured internal review, not external human review
or a formal proof certificate. The coordinator supplied the proposed formulas
and bounds. I checked their derivations before coefficient enumeration or new
physical trials; the analysis below does not assume an enumeration outcome.

Sources inspected: `notes/CC_ROW38_COMPILER_TRANSFER_2026_09_29.md` and
`notes/CC_SELECTOR_SUPPORT_2026_09_29.md`, together with repository evidence
and contribution rules. The former describes the emitted row-(3,8) menu and
its fixed ordering; the latter supplies the earlier selector's comparison
method, not a theorem automatically transferable to the changed geometry.

After preflight, I inspected the frozen `PROTOCOL.md`, source input head
`64bda7a065abcff312ab0cac17f5b12a49b91221`, and verified its SHA256 as
`95811494876e2c62d6c288c21f8ba42b2983e486a25eb6e7b7633a0e0fc8a26a`.
The protocol uses the correct 1,512 cells. Its initial count typo was
corrected before enumeration, without changing the declared coefficient
domain; no result depends on the superseded count.

## 1. Exact support and the auxiliary distinction

Normalize the physical parameters by d=gcd(p,q), P=p/d, Q=q/d. Put M=P+Q.
The leader is y=9/8-x, 1/4<=x<=3/8. Its orbit projection is

    [(2Q-7P)/8, (3Q-6P)/8]

and has width M/8. The selector takes the least integer h at or above the
lower endpoint if that integer belongs to the closed interval. Since
2Q-7P=2M-9P, define

    rho = 8h-(2M-9P) = (P-2M) mod 8,  0<=rho<=7.

The contact exists exactly when rho<=M and is then

    x=1/4+rho/(8M),  y=7/8-rho/(8M).

Consequently the complete leader support is parametrized, in both directions,
by M>=2, 1<=P<M, gcd(P,M)=1, rho=(P-2M) mod8 and rho<=M; set Q=M-P.
For M>=8 contact is automatic. The already archived exhaustive M<8 table
has precisely the misses (1,1), (1,4), (2,1). No new search is needed to
establish these exceptions.

The unchanged first fallback selects F1=(17/56,3/14) at (1,4), with h=1,
and F2=(9/28,9/56) at (2,1), with h=0. Substitution gives Qx-Py=h in
each case. The auxiliary fallback selects C=(1/8,1/8) at (1,1), also h=0.

For any epsilon>0, a leader output with x>=1/4+epsilon has
M<=7/(8epsilon), leaving only finitely many parameter pairs and hence points.
The endpoint E=(1/4,7/8) is selected at (P,Q)=(2,3). Moreover the primitive
directions (P,Q)=(1,4j), j>=2, give M=4j+1 and rho=7, yielding distinct
points approaching E from the right. Thus the leader support is countably
infinite, is closed, and has E as its only accumulation point. Its other
points are isolated; it is not dense in the leader segment.

F1 and F2 are distinct and off the leader. C is off the leader and distinct
from both fallbacks. Adding those finite points preserves closedness and the
unique accumulation point. In contrast to the old selector, excluding p=q
removes no leader point: its sole primitive direction (1,1) never reaches
the leader. The only support point removed is C. Therefore equality between
the primary and auxiliary-inclusive coefficient contracts must be checked;
it does not follow from equality of their supports.

## 2. Analytic bound on A-B, with both signs

Let delta=A-B, D=|delta|, u=2A+7B=2delta+9B, and a=u mod8. At a selected
leader point the seventh raw value is

    u/8 + delta*rho/(8M).

E is actually selected, so a=0 fails at (2,3). Suppose first delta>0 and
a=7, or delta<0 and a=1. Along the j sequence above the drift has absolute
size 7D/[8(4j+1)]. For sufficiently large j this is strictly between 0 and
1/4, which lies in the first open forbidden band on the respective side
of the closed safe interval. For example any integer j>=2 and j>7D/8 is
sufficient. These outward-boundary cases fail at actual selector outputs.

Otherwise, for delta!=0 and a!=0, define c=7-a if delta>0 and c=a-1 if
delta<0. After the outward exclusions, 1<=c<=6. The first open forbidden
band is reached when

    c/8 < 7D/[8(4j+1)] < (c+2)/8,

equivalently

    (7D/(c+2)-1)/4 < j < (7D/c-1)/4.

The interval length is 7D/[2c(c+2)]>=7D/96. If D>=14 this is strictly
greater than one. Its lower endpoint is at least 7D/32-1/4>=45/16, so the
integer floor(lower)+1 is at least 3 and lies strictly inside the interval.
This is an allowed j>=2 and supplies an actual failed primitive direction
(1,4j). Hence uniform primary safety implies |A-B|<=13. The old proof's
claim j>=4 is not copied: here the guaranteed lower bound is j>=3.

These are strict forbidden-band tests. For positive drift the raw value is
strictly between (8m+7)/8 and (8m+9)/8; for negative drift it is strictly
between (8m-1)/8 and (8m+1)/8, using u=8m+a. Both have circle distance
strictly below 1/8. No endpoint of an allowed closed band is rejected.

## 3. Safe tail and finite residue reduction

After rejecting a=0 and the outward cases, the permitted drift direction
has at least 1/8 of safe margin. With |delta|<=13 and M>=91,

    |delta*rho/(8M)| <= 13*7/(8*91) = 1/8.

Thus all such leader contacts remain in the same closed safe band. The
boundary M=91 is valid, including equality. Checking all primitive
2<=M<=91 gives a finite part with a harmless overlap at M=91; add both
used fallback contacts, and add C only to the auxiliary-inclusive contract.
This bound was derived before counting or classifying the finite cases.

At fixed delta, (A,B)->(A+56,B+56) changes the raw seventh values by the
following integers:

| Location | x+y | Raw-value increment |
| --- | --- | --- |
| Any point of the leader | 9/8 | 63 |
| F1 | 29/56 | 29 |
| F2 | 27/56 | 27 |
| C | 1/4 | 14 |

Therefore exact fractional phases, including all boundary equalities, depend
only on delta and B modulo56. This produces 27*56=1512 finite residue cells
for the necessary range |delta|<=13. Positive representatives can be chosen
with B=b+56, A=B+delta, b=0,...,55. These reductions apply to the actual
selector, the leader-plus-used-contacts contract, and their C-inclusive
versions. They do not assert a period for an entire fallback segment: x+y
varies on that segment.

Whole-leader safety itself is exactly the condition that the two raw
endpoint numerators 2A+7B and 3A+6B belong to one interval [8m+1,8m+7].
The interval must be shared: safe endpoint residues in different laps do
not certify the intervening segment. The used fallbacks require the phases
of (17A+12B)/56 and (18A+9B)/56 to be safe. C requires A+B not divisible
by8. Whether these conditions lose any rows compared with the actual sparse
support is a question for the subsequent complete finite classification,
not a consequence of the support topology.

## 4. Physical recovery and the distinct-speed domain

The six core rows remain safe at every selected point because the newly
emitted menu is core-safe throughout each closed segment, independently of
the substituted positive coefficient row (A,B). For p,q>0 with p!=q the
six core speeds are pairwise distinct and positive. The positive seventh
speed can coincide with a core speed only through

    (A-a)p+(B-b)q=0,
    (a,b) in {(1,1),(2,1),(3,1),(3,2)}.

It cannot coincide with p or q, since Ap+Bq>=p+q. Therefore impose these
inequalities, as well as p!=q, when speaking of eight distinct speeds.
The four rows identical to those core rows have empty distinct-speed domains
and must be explicitly labelled.

If the seventh phase is unsafe while the core phases at the same selected
time are safe, the seventh speed cannot equal any core speed. Every failed
primary output thus automatically supplies an eight-distinct-speed example.
This establishes equivalence between uniform primary safety and the same
guarantee restricted to the row-dependent distinct-speed domain; an accepted
identically repeated row is separately vacuous on that restricted domain.

For every contact h=Qx-Py is integral. Given rP+sQ=1, put
N=floor(rx+sy), tau=rx+sy-N and t=tau/d. Then pt=x-sh-PN and
qt=y+rh-QN. Hence a row (a,b) with torus lap m has physical lap

    m+(-a*s+b*r)*h-(a*P+b*Q)*N.

This validates the inherited recovery formula at the changed menu. The
seventh torus lap must be recomputed for each new coefficient row; preserving
fractional phases under the period does not preserve its integer laps.

## 5. The four frozen contracts and complete comparison

The protocol's contracts are correctly distinguished: W uses whole L and
whole first fallback S; R uses whole L but only its two actual fallback
contacts F1,F2; T uses actual outputs on p!=q; T_all adds the actual p=q
point C. Thus W implies R implies T, while T_all implies T. No other
inclusion or equality follows merely from these definitions. In particular,
W excludes the auxiliary geometry by declaration and need not imply T_all.

For W the leader variation is |A-B|/8 and the fallback variation is
|A-3B|/28. A connected interval inside the periodic safe set must lie in
one closed safe band, whose length is 3/4. Therefore W implies
|A-B|<=6 and |A-3B|<=21. Writing delta=A-B yields
2B=delta-(A-3B)<=27, hence B<=13 for integral positive B. The protocol's
B=1,...,13, delta=-6,...,6, A=B+delta>0 is therefore exhaustive.
Fallback endpoints have raw numerators 49A+42B and 55A+24B over168, and
the common closed safe band is [168m+21,168m+147]. These are exactly the
declared endpoint tests, including equality.

For T/R/T_all, the residue reduction in section3 is complete. A rejection
by the left-endpoint or outward-boundary gate already appears in the finite
direction list: E uses M=5, and for 1<=D<=13 the displayed outward witness
has j<=12, hence M=4j+1<=49<91. Thus the protocol's requirement to retain
a finite failed contact for every failed tail gate is justified in advance.

The old accepted predicate implies epsilon=A-2B in [-6,6]; new T implies
delta=A-B in [-13,13]. Hence every intersection row has
B=delta-epsilon<=19 and A=B+delta<=32. Enumerating the protocol's
B=1,...,19 and delta=-13,...,13 with A>0 is complete for the overlap,
despite the different period directions. If a later exact result tightens
the new delta bound, a smaller comparison box would be a deduction from
that result and is not needed for this completeness argument.

The old progression (A,B)=(6+16k,2+8k), k>=0, has old endpoint
numerators 18+56k and20+56k in the same safe band, and old fallback
numerator 10+32k not divisible by8. Thus every row is old-accepted. Its
new delta=4+8k is at least20 for k>=2, outside the proved necessary new
bound. Conversely (A,B)=(3+56k,8+56k) has new endpoint numerators
62+504k and57+504k in a shared safe band, fallback phases5/8 and1/4,
and auxiliary phase3/8. Thus it satisfies R and T_all for every k>=0.
Its old epsilon=-13-56k violates the old necessary bound. These identities
establish infinite differences in both directions without comparing unlike
residue-class counts or assuming an enumeration outcome.

## Preflight finding

PASS for the proposed exact support, both-sign large-slope obstruction and
M>=91 tail. Preserve two differences from the old proof: p=q removes only
the off-leader auxiliary point, and the large-slope construction guarantees
j>=3 rather than j>=4. No enumeration results or new physical trials were
used in this preflight review. Equality or inequality of the final coefficient
contracts remains open at this stage.

Frozen-protocol follow-up: PASS for the four distinct contracts, finite W
bound, finite overlap domain, and both infinite set differences. The hash
above was checked from disk. No coefficient enumeration or new physical
trials were performed in this support review.
