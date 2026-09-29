# Separate review: actual support, topology and finite reduction

September 29, 2026. Materially AI-generated review, not external human or
formal certification. The reviewer did not import production code, inspect
the new classification output, perform a coefficient enumeration, or run
new physical trials. Initial findings were sent to the coordinator before
this note was written. The conclusions remain part of an internally reviewed
proof candidate.

Inputs inspected: AGENTS.md, README.md, the current HANDOFF.md research
entry, CLAIM_STATUS.md, CONTRIBUTING.md, the frozen protocol and the preceding
coefficient-range note. The mathematical source head in the protocol is
`78c6b25cc4e96d35c6a60595120deb754bd90187`.

| Input | SHA256 |
| --- | --- |
| PROTOCOL.md | `be10097639d5742d17da199ae34166965e4a5b41af60f4052b4a289c1c0c6594` |
| notes/CC_COEFFICIENT_RANGE_2026_09_29.md | `1d7e358c4d275a591b4b82899c4cc4ac15f0a52c4cb86902b28e45777b6e3a2a` |

## 1. Exact support and the missing repeated-speed point

Write positive primitive parameters as P,Q, and put M=Q+2P. Then M>=3,
1<=P<M/2 and gcd(P,M)=1. Conversely every such (M,P) gives the positive
primitive pair (P,Q)=(P,M-2P). The leader projection has lower endpoint

\[
 a_0=(2Q-3P)/8=(2M-7P)/8
\]

and width M/8. Define h=ceil(a_0) and rho=8(h-a_0). The ceiling gives
rho in {0,...,7}, and

\[
 \rho\equiv-2M+7P\equiv-P-2M\pmod8.
\]

The first integer h is in the closed projected interval exactly when
rho<=M. Solving Qx-Py=h on y=7/8-2x gives

\[
 (x,y)=\left(\frac14+\frac{\rho}{8M},
                  \frac38-\frac{\rho}{4M}\right).
\]

Thus the following parametrized set is an exact description, with both
necessity and sufficiency, of all leader outputs when p=q is allowed:

\[
 S_{\rm all}=\left\{
 \left(\frac14+\frac{\rho}{8M},\frac38-\frac{\rho}{4M}\right):
 M\ge3,\ 1\le P<M/2,\ \gcd(P,M)=1,
 \ \rho=(-P-2M)\bmod8,\ \rho\le M\right\}.
\]

For M>=7 every rho passes. The smaller primitive possibilities are
(P,Q)=(1,1),(1,2),(1,3),(1,4),(2,1). Their (M,rho) pairs are respectively
(3,1),(4,7),(5,5),(6,3),(5,4). Exactly (1,2) misses; it uses
C=(1/8,1/4). This agrees with the longer complement table in the source.

Excluding p=q excludes exactly the primitive pair (1,1), whose output is
D=(7/24,7/24). No other primitive pair selects D. Indeed D requires
rho/M=1/3, so rho=k, M=3k for an integer 1<=k<=7. The congruence requires
P congruent to k modulo 8. The bounds 0<P<3k/2 force P=k: k-8<=0 and
k+8>3k/2 throughout this range. Then gcd(P,M)=k, so k=1. Therefore

\[
 S=S_{\rm all}\setminus\{D\}
\]

is the exact leader support for p!=q. The complete supports of the two
contracts are S union {C} for T, and S_all union {C} for T_all. The removal
of p=q cannot be dismissed as a duplicate parametrization or limit case.

## 2. Closure and accumulation

The left endpoint E=(1/4,3/8) belongs to S: choose (P,Q)=(2,3), giving
M=7 and rho=0. Every support point at x>=1/4+epsilon has

\[
 M\le\frac{\rho}{8\epsilon}\le\frac7{8\epsilon}.
\]

There are only finitely many admissible pairs below this bound. Consequently
every leader support point other than E is isolated, and E is the only
possible accumulation point. It is an actual accumulation point: for every
j>=2 take P=1,Q=4j-2, so M=4j, rho=7 and

\[
 (x_j,y_j)=\left(\frac14+\frac7{32j},
                         \frac38-\frac7{16j}\right)\longrightarrow E.
\]

The points are distinct and all have p!=q. Both S_all and S are therefore
countably infinite closed subsets of L; their derived set is exactly {E}.
Removing D preserves closedness because D is isolated. Adding C, which
lies off L, adds one isolated point and leaves the derived set unchanged.
All these supports are compact. They are not dense in L and are not the
whole segment. This concerns the first-integer selector; replacing it by
all integer contacts would change the operation and its support.

## 3. The proposed large-slope obstruction is valid

Let delta=A-2B and let a=(7B+2delta) mod8. On the selected leader point the
seventh value, modulo its left-endpoint integer part, is

\[
 a/8+\delta\rho/(8M).
\]

If a=0, the actual selected point E is unsafe. Suppose a is in {1,...,7}
and delta is nonzero; write D_0=|delta|. Along the sequence in Section 2,
the magnitude of the drift is 7D_0/(32j).

If delta>0 and a=7, any integer j>7D_0/8 with j>=2 gives drift strictly
between 0 and 1/4, landing in the open forbidden interval (7/8,9/8).
If delta<0 and a=1, the same choice lands in (-1/8,1/8). These are the
outward boundary cases; they fail for every nonzero slope of the indicated
sign, not only large slopes.

Otherwise put c=7-a when delta>0 and c=a-1 when delta<0. In either case
1<=c<=6. The first forbidden interval in the direction of movement is hit
whenever

\[
 \frac c8<\frac{7D_0}{32j}<\frac{c+2}{8},
 \qquad\text{equivalently}\qquad
 \frac{7D_0}{4(c+2)}<j<\frac{7D_0}{4c}.
\]

This open interval has length

\[
 \frac{7D_0}{2c(c+2)}\ge\frac{7D_0}{96}.
\]

For D_0>=14, its length is strictly greater than 1, and its lower endpoint
is at least 7D_0/32>=98/32>3. Taking the floor of that lower endpoint and
adding 1 produces an integer strictly inside the interval. Thus j>=4,
so the proposed positive primitive direction is admissible. Endpoints of
the safe bands cause no ambiguity because both inequalities are strict.
The resulting selected point has an unsafe seventh phase. This proves
the necessary bound |delta|<=13 for T, and hence also for T_all.

No assertion that this bound is sharp is needed for the finite reduction.

## 4. Tail bound and the exact reduced domain

Reject a=0 and the outward boundary cases first. For delta>0 the remaining
residues have 1<=a<=6, leaving positive safe margin (7-a)/8>=1/8. For
delta<0 the remaining residues have 2<=a<=7, leaving negative safe margin
(a-1)/8>=1/8. For delta=0 the left residue is constant everywhere on L.

When |delta|<=13 and M>=91, every selected point satisfies

\[
 \left|\frac{\delta\rho}{8M}\right|
 \le\frac{7\cdot13}{8\cdot91}=\frac18.
\]

The drift therefore remains within the same closed safe band. Equality
at M=91 is allowed. Checking all primitive 3<=M<=91 after these necessary
rejections, together with C, is consequently sufficient and necessary;
M=91 is a harmless overlap of the finite part and the proved tail. The
finite directions are exactly 1<=P<M/2, gcd(P,M)=1, Q=M-2P; exclude P=Q
for T and retain it for T_all. The leader-miss direction is handled only
through C, never through the formula for a point outside the segment.

Finally (A,B)->(A+16,B+8) changes seventh raw values by 7 on L and 4 at C,
so it preserves every tested phase. Reducing B modulo 8 and delta to
[-13,13] gives 216 cells. Positive representatives B=b+8,
A=2B+delta are valid in every cell (the smallest A is 3). This is a proved
finite reduction; classification totals still require the separate exact
enumeration and are not supplied by this review.

## 5. Physical scope and adversarial checks

For p!=q the first six positive speeds p,q,p+q,2p+q,3p+q,3p+2q are
distinct. Their phases are safe at every selected leader or fallback point.
If the seventh speed equalled any one of them, its phase at the same
recovered time would equal that safe core phase. Thus an unsafe seventh
phase at a p!=q selector output proves that the seventh speed differs from
every core speed. Positivity makes it different from the stationary
reference as well. Every failure certificate for T is therefore a genuine
eight-distinct-speed failure of this fixed selector. It says nothing about
the existence of a different lonely time.

The same inference does not apply to a T_all failure supported only at
p=q: that auxiliary already has repeated core speeds. Conversely the four
coefficient rows (1,1),(2,1),(3,1),(3,2) duplicate a core speed identically;
they are safe on all selector outputs but have empty eight-distinct-speed
domains. General noncollision conditions remain necessary when presenting
an accepted row as a nonempty physical family.

The main attempted failure modes all survive checking: the ceiling residue
has the correct sign; rho<=M retains closed endpoint hits; D has no second
primitive preimage; the support does not become dense when denominators
grow; both slope signs use open forbidden intervals; the large-slope
integer exists away from excluded small directions; and M=91 equality is
safe. No result-level defect was found in the protocol's proposed reduction.

The consequential CC distinction is that an operational support can be
closed, countable and very far from its ambient segment. Safety on that
support may have different obligations from safety on the connected
segment. The proof above establishes the exact question and reduction;
whether it enlarges the coefficient set remains the classification's task.
