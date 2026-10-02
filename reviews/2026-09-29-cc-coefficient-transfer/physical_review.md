# Changed-row physical and representation review — September 29, 2026

**Result: PASS within the frozen scope.** The emitted two-segment certificate
recovers safe physical times for all 18 declared parameter pairs after changing
the seventh row from (5,2) to (6,2). These are newly evaluated configurations,
not reproductions of the former 18 physical instances. Seventeen have eight
distinct speeds including the stationary reference; (1,1) remains the labelled
repeated-speed auxiliary. This is a separately structured internal AI review,
not independent external, human or formal certification.

## Method and exact comparisons

`physical_review.py` imports no production compiler, selector or clipping code.
Its primary clock is recovered through coordinate laps. For d=gcd(p,q),
P=p/d and Q=q/d, compute H=Qx-Py and require it to be an integer. Solve
Q*i=-H (mod P), with 0<=i<P, and set j=(Q*i+H)/P. Then

\[
\tau=(x+i)/P,\qquad t=\tau/d,\qquad
\ell_{a,b}=m_{a,b}+ai+bj.
\]

Direct multiplication of every physical speed by t agrees with both the
retained torus phase ax+by-m and that coordinate-lap formula. The checker
independently chooses the first integer contact on the emitted menu and
compares the chosen ID, test count, point, H, primitive clock, physical clock,
speeds, phases and laps with `run.json`. It also checks reflected time 1-t,
reflected phases and laps, and two alternative Bezout choices per witness.

The first and only execution of the physical review passed. There was no
result-driven revision of its physical arithmetic or contact rule. Its code
was adapted from the earlier separately structured physical checker before
changed-row output existed, with the row changed and the old exact-minimum
assumption removed. Output-schema comparisons were added before execution.

Counts: 18 physical witnesses; 126 selected and 126 reflected phase checks;
126 selected and 126 reflected lap checks; 36 alternative Bezout recoveries;
336 labelled endpoint-band checks across all 24 candidate records. The two
scaling controls (4,6) versus (2,3), and (6,10) versus (3,5), have the same
primitive point, phases and laps, and physical times divided by their gcd.
No parameter scan or additional coefficient trial was run. The conditional
restored-parent diagnostic was **not triggered**.

For general p,q>0 the speeds p+q,2p+q,3p+q,3p+2q,6p+2q strictly increase and
exceed both p and q. Therefore distinctness, including the zero reference,
is equivalent to p!=q. This domain check does not depend on the finite controls.

## Selected geometry and equality

The selected leader is P2:E0-3:K2:

\[
1/4\le x\le3/8,\qquad y=7/8-2x,
\qquad m=(0,0,0,0,1,1,2).
\]

Its H interval is [(2Q-3P)/8,(3Q-P)/8], of width (Q+2P)/8.
The fourth phase is identically 7/8. Its seventh phase is
6x+2y-2=2x-1/4, which lies in [1/4,1/2]. The new seventh safety condition is
therefore explicitly checked, not inferred from its relation to the fifth row.

The fallback is P0:E0-1:K1:

\[
x=1/8,\qquad3/16\le y\le1/4,
\qquad m=(0,0,0,0,0,0,1).
\]

Its first phase is identically 1/8. It supplies (P,Q)=(1,2) at (x,y)=(1/8,1/4),
H=0 and physical t=1/8. The seven phases there are
(1/8,1/4,3/8,1/2,5/8,7/8,1/4). Every emitted witness has exact minimum 1/8,
and the two constant-extremal rows explain this for the entire selected menu.
These are attainment claims, not optimum claims.

Opening segment endpoints is a separate operation from changing the safety
threshold. On the frozen controls it has the following effects:

| Parameter pairs | Open selected menu | Open full 24-candidate class |
| --- | --- | --- |
| (1,2),(1,3),(2,3),(3,1),(4,6) | No integer contact | A contact remains |
| Other 13 declared pairs | A contact remains | A contact remains |

Thus deleting endpoints damages this compact menu but does **not** establish
failure of the complete candidate class at those pairs. For example, (1,2)
still meets the open interiors of P1:E0-3:K1 and P1:E1-3:K1. The exact closed
and open candidate IDs for every pair are preserved in `physical_review.json`.
The counts concern these 18 pairs only; no universal claim about the opened
candidate class follows.

## CC adequacy, information loss and cost

The frozen procedure changed its chosen geometric carrier while preserving
joint bands, provenance, closed contact, primitive normalization and physical
recovery. That supplies evidence of portability to **this one predeclared
changed row**. It does not establish universal portability or a theorem that
suitable descending segments always exist.

The smaller menu supports one closed-threshold witness. It omits other
candidates, parent interiors, complete safe sets, optimum values and all
maximizers. The endpoint experiment exposes a consequential distinction:
menu failure after an operation can coexist with success in the richer
candidate record. Before concluding that new parent geometry is required,
check which representation was actually exhausted. The retained 24-candidate
record is already an adequate richer source for those five endpoint cases.
No restored-parent diagnostic was justified by this successful frozen run.

This physical checker does not establish the infinite coverage argument; the
separate geometry review checks the width bound, complete residual domain and
contact matrix. In the emitted record, preprocessing has 24 floor edges,
24 candidates, 14 descending candidates, a 21-pair rectangle, eight residual
primitive pairs and 192 candidate/residual contacts. Online witness selection
uses at most two segment tests plus gcd and modular-inverse/Bezout arithmetic
with parameter-dependent bit lengths and iteration counts. Compact geometric
storage is not constant arithmetic cost.

Attribution and status remain those of the literature comparison: the segment
contact argument has an established precedent; prior eight-runner existence
coverage is separate from our explicit construction; no optimal-spectrum
conclusion is inherited. No fresh originality claim, external review or claim
status promotion is supplied by this computation.

Reproduce from the repository root:

```sh
python3 reviews/2026-09-29-cc-coefficient-transfer/physical_review.py
```

The emitted JSON records source/output hashes and every physical control.
