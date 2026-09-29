# Pre-validation symbolic derivation
Written after the fixed ambient arrangement, before evaluating any physical q family case in this cycle.

Candidate exact maximum, q>=2:
- q=4: M=1/8, t=1/8.
- q divisible by3: M=q/[3(2q+1)], t=2M.
- q=1 or2 (mod6): M=1/6, t=1/6.
- q=4 (mod6),q>=10: M=(q-1)/[3(2q+1)], t=2M.
- q=5 (mod6): M=(q+1)/[2(3q+5)], t=3M.

## Upper-bound mechanism
The exact ambient construction has 10 cells: 3 singleton cells at z=1/8, six tetrahedra, and one six-vertex polytope. There are33 vertex occurrences and45 edge occurrences. The ambient maximum is1/6. Every nonmaximal vertex has z<=1/7.
For any actual-orbit plane qx-y=h, a slice optimum above1/7 occurs on an edge incident to a1/6 vertex (or at that vertex). Write such an edge (x,y,z)=(x0+alpha e,y0+beta e,1/6-e), e>=0. Integrality requires h=h0+(q alpha-beta)e with h0=qx0-y0.
Let rho={h0}. A decreasing projection requires e>=rho/|q alpha-beta|; an increasing projection requires e>=(1-rho)/|q alpha-beta|, unless rho=0 when e=0 is already available. Dropping the finite edge length only enlarges possibilities, so these are valid upper estimates for the maximum.

Peak vertices and outward directions(alpha,beta):
A=(1/6,1/6):(-1,2),(1/5,-1),(1,-1).
B=(1/6,1/3):(-1,1),(-1,4),(1,-2).
C=(1/2,1/6):(-3,5),(0,-1),(0,1/2).
D=(1/2,1/3):(-1,2),(0,-1/2),(0,1).
E=(1/3,5/6):(-2,1),(0,1),(1,-2).
F=(1/2,2/3):(-1,2),(0,-1),(0,1/2).
G=(1/2,5/6):(-3/5,1),(0,-1/2),(0,1).

All edge loss budgets are1/24, except E direction(-2,1), whose budget is1/42.
Discarding upward choices at C,D,F,G is justified for an optimum above1/7: their smallest nonzero losses exceed1/42.
Best losses per A,B:
A min({(q-1)/6}/(q+2),(1-{(q-1)/6})/(q+1));
B min({(q-2)/6}/(q+4),(1-{(q-2)/6})/(q+2));
with zero loss if either relevant rho=0.
C dominates D,F,G: C loss=5/[6(3q+5)] for evenq,1/[3(3q+5)] for oddq.
E min({(2q-5)/6}/(2q+1),(1-{(2q-5)/6})/(q+2)).
Comparison by q mod6 yields candidate M for q!=4; minima equal1/42 at q3 andq10, and below1/42 otherwise except the exact1/6 branches.
For q4 the above truncation is insufficient. Use the entire ten-cell table: qx-y integer meets only the baseline vertex(1/8,1/2,1/8) and singleton(3/8,1/2,1/8) on x<=1/2. Reflection gives the four original tight witnesses.

## Original-time lower bound obligation
Verify the listed t directly for ALL seven speed expressions, on each residue class, retaining integer lap parts. This remains an algebraic obligation before promoting the formula.
For multiples3 and q=4 mod6,q>=10, the witness is on E's (-2,1) edge with e<=1/42.
For q=1,2 mod6 it is exactly A orB.
For q=5 mod6 it is on C's (-3,5) edge with e<=1/24.
Thus the exact ambient certificate already supplies membership and actual-orbit integrality, but a separate phase table will make the original-time proof transparent.

## Permitted finite validation remains unchanged
q2,...,25 direct complete one-dimensional maxima; q100003,100004 witness checks only.
No data from these cases has been used to infer the formula.

