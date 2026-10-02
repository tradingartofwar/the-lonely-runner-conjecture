# Compatibility Calculus: sparse selector support has the same coefficient range

September 29, 2026. Source head:
`78c6b25cc4e96d35c6a60595120deb754bd90187`.

**Result:** the first-integer selector visits only a closed, countable subset
of its leading segment, with one accumulation point. Nevertheless, for
positive integer seventh-row coefficients, requiring safety at every actual
output gives **exactly the same 42 residue classes** as requiring the whole
leading segment plus the used fallback point to be safe. The earlier
whole-segment condition loses no coefficient rows for this precise operation
and coefficient domain.

Status: **HYPOTHESIS / internally reviewed complete proof candidate**.
The argument and exact implementations are materially AI-generated, with
separately tasked support and arithmetic reviews. This is not external human
or formal certification. The [prior literature comparison](CC_LITERATURE_COMPARISON_2026_09_29.md)
and existence/novelty limits remain unchanged; no new priority claim is made.

## 1. The question and quantifiers

Keep the [previous construction](CC_COEFFICIENT_RANGE_2026_09_29.md):
L is y=7/8−2x, 1/4≤x≤3/8; C=(1/8,1/4) handles the sole missed primitive
direction (1,2). The first six rows are (1,0),(0,1),(1,1),(2,1),(3,1),(3,2).
The seventh row (A,B) has positive integer entries. The threshold is closed 1/8.

Let R be the previous whole-L-plus-C safety contract. Define T to require
seventh safety at this selector's output for every positive integer p≠q.
Define T_all by also including the repeated-speed p=q auxiliary. The result is

\[
\boxed{T=T_{\rm all}=R.}
\]

This is a coefficient-membership equality, not an equality between the
geometric supports. It concerns this deterministic first-integer rule and
this positive integer coefficient domain. It does not classify arbitrary
real rows, alternative contact rules, all witnesses or optimal times.

For eight distinct total speeds, including reference 0, retain

\[
p\ne q,\qquad (A-a)p+(B-b)q\ne0
\quad ((a,b)\in\{(1,1),(2,1),(3,1),(3,2)\}).
\]

This restriction does not hide any T failure: the first six speeds are
distinct and safe whenever p≠q. An unsafe seventh phase cannot equal the
phase of a coincident core speed at the same time. Therefore every failed
T output automatically has eight distinct speeds. Conversely the four
identically repeated core rows have empty distinct-speed domains and remain
explicitly labelled as such. A failed selector is not failed loneliness.

## 2. Exactly which points are selected

Normalize d=gcd(p,q), P=p/d, Q=q/d, and write **M=Q+2P**. This M is
distinct from the integer part N used in physical recovery. Put

\[
h=\left\lceil\frac{2Q-3P}{8}\right\rceil,\qquad
\rho=8h-(2Q-3P)=(-P-2M)\bmod8\in\{0,\ldots,7\}.
\]

The projected leader interval has width M/8. Its first integer is present
exactly when ρ≤M, and its point is

\[
(x,y)=\left(\frac14+\frac{\rho}{8M},
            \frac38-\frac{\rho}{4M}\right).
\]

Thus all leader outputs are exactly the points given by
M≥3, 1≤P<M/2, gcd(P,M)=1, Q=M−2P, ρ=(-P−2M) mod8 and ρ≤M.
Both directions of this parametrization follow directly from positive
primitive P,Q. Only (1,2) misses L and uses C.

Excluding p=q removes precisely D=(7/24,7/24), the output of (1,1).
To check uniqueness, D requires ρ/M=1/3, hence (ρ,M)=(k,3k), 1≤k≤7.
The congruence gives P≡k mod8; 0<P<3k/2 forces P=k, and gcd(P,M)=1
then forces k=1. This point really is removed from the support; it is not
silently supplied by another primitive direction.

Every selected point with x≥1/4+ε has M≤7/(8ε), so only finitely many
such points exist. The left endpoint E=(1/4,3/8) is selected at (2,3).
The sequence P=1,Q=4j−2, j≥2, gives M=4j,ρ=7 and distinct points

\[
(x_j,y_j)=\left(\frac14+\frac7{32j},
                \frac38-\frac7{16j}\right)\longrightarrow E.
\]

Consequently both leader supports are closed and countably infinite, with
**E their sole accumulation point**. Every other point, including D, is
isolated. Adding the off-leader point C adds one isolated point. These
supports are not dense in L. A density argument could not prove T=R.

## 3. A finite reduction that does not assume whole-L safety

Set δ=A−2B and a=(7B+2δ) mod8. At a leader output the seventh raw value is

\[
\frac{7B+2\delta}{8}+\frac{\delta\rho}{8M}.
\]

The left endpoint has phase a/8. If a=0 it already fails at physical
(P,Q)=(2,3). If δ>0,a=7 or δ<0,a=1, moving slightly into L leaves the
closed safe band. The displayed j sequence supplies actual failed outputs:
any integer j>7|δ|/8 with j≥2 has nonzero drift less than 1/4.

For the remaining nonzero-slope cases let D_0=|δ| and put c=7−a when
δ>0, or c=a−1 when δ<0. Then 1≤c≤6. The j sequence hits the first open
forbidden band whenever

\[
\frac{c}{8}<\frac{7D_0}{32j}<\frac{c+2}{8},
\quad\text{or}\quad
\frac{7D_0}{4(c+2)}<j<\frac{7D_0}{4c}.
\]

This interval has length 7D_0/[2c(c+2)]≥7D_0/96. If D_0≥14 the length
is greater than one, and its lower endpoint is at least 7D_0/32>3.
The floor of the lower endpoint plus one lies strictly inside, giving an
admissible j≥4 and a concrete failed direction (1,4j−2). This handles both
signs with strict forbidden-band inequalities. Therefore **T implies |δ|≤13**.
This is an intermediate bound, not a claim of sharpness.

After rejecting a=0 and the outward boundary cases, the available safe
margin in the direction of motion is at least 1/8. For |δ|≤13 and M≥91,

\[
\left|\frac{\delta\rho}{8M}\right|
\le\frac{7\cdot13}{8\cdot91}=\frac18.
\]

Every such leader output remains in the same closed safe band. Thus it
suffices to check all primitive 3≤M≤91, plus the fallback C already present
at (1,2). The equality M=91 overlaps the finite part and proved tail harmlessly.
There are **1,275 primitive directions**, including the single p=q auxiliary,
and **387 distinct leader points** in this finite reduction.
Removing D leaves 386 distinct leader points for the primary p≠q contract.

Finally (A,B)↦(A+16,B+8) changes raw seventh values by 7 everywhere on L
and by 4 at C. It preserves every phase, so membership depends only on δ
and B mod8. The complete reduced coefficient domain has **27×8=216 cells**.
Representatives B=b+8 and A=2B+δ are positive in all of them.

The [protocol](../reviews/2026-09-29-cc-selector-support/PROTOCOL.md) fixed these
proposed reductions before enumeration. Separate review checked their proofs
before the finite results were used. Neither the coefficient bound nor the
direction bound was inferred from a successful scan.

## 4. Exact classification and failure certificates

Both implementations check every reduced cell. T and T_all each accept 42,
and both lists equal the prior R list. All δ outside [−6,6] are rejected;
the accepted residues are:

| δ | B modulo 8 |
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

Always retain B≥1 and A=2B+δ≥1. Equivalently, the previous simple criterion
is now necessary as well as sufficient for this exact selector:

\[
\exists m\in\mathbb Z:\quad
8m+1\le\min(2A+3B,3A+B)\le\max(2A+3B,3A+B)\le8m+7,
\qquad A+2B\not\equiv0\pmod8.
\]

The 174 rejected cells each retain a selected point, physical time, speeds,
phases and laps exhibiting failure. These are derived rejection certificates,
not held-out trials. The periodic identity transfers the same failed direction
to every positive row in that cell. For |δ|≥14 the preceding analytic
construction supplies a failed direction instead. Thus rejection can be
explained by a physical example, rather than a bare coefficient-class verdict.

As a **post-classification compression of the same outputs**, all 174 first
failures occurred among these 11 primitive directions, with M≤10:

| (P,Q) | Selected time | Cells first rejected here |
| --- | --- | --- |
| (1,2) | 1/8 | 28 |
| (1,3) | 3/8 | 24 |
| (1,4) | 5/16 | 30 |
| (1,5) | 15/56 | 26 |
| (1,6) | 23/64 | 2 |
| (1,8) | 23/80 | 2 |
| (2,1) | 7/40 | 34 |
| (2,3) | 1/8 | 6 |
| (2,5) | 47/72 | 8 |
| (3,2) | 7/64 | 10 |
| (4,1) | 23/72 | 4 |

The traversal order is increasing M, then P, excluding p=q for T. This
smaller rejection list was extracted after the frozen full enumeration; no
minimality claim, new physical sampling or new universal finite-menu claim
follows. The large-slope obstruction remains a separate part of the proof.

## 5. Recovery, review and reproduction

For any selected point, h=Qx−Py is an integer. Choose rP+sQ=1 and set
N=floor(rx+sy), τ=rx+sy−N, t=τ/d. For row (a,b) with recomputed torus lap m,
the physical lap is m+(−as+br)h−(aP+bQ)N. This is the prior recovery map;
seventh laps must still be recomputed for the actual row.

The coordinator uses the residue formula for the selected point and Bezout
recovery. The arithmetic reviewer uses direct ceiling/interval contact and
coordinate congruences, followed by physical multiplication. Neither reviewer
imports coordinator code. The support reviewer separately proves topology,
both slope signs, tail equality and the physical distinctness implication.
The work is parallel and separately structured; findings are shared, so no
blind-replication claim is made.

The complete comparisons match 7,650 support fields, 1,944 classification
fields and 4,332 physical fields, plus 972 fields against the archive.
The arithmetic reviewer corrected its initial reflection convention from
1/d−t to the archive's 1−t before emitting its final JSON. The phases agreed,
but nonprimitive reflected times and laps differed. This bookkeeping error
did not affect coefficient classification or original selected witnesses;
the correction is retained in the review record.

All 54 archived progression configurations reproduce exactly, including
selected/reflected phases and laps. The new checks add only rejection
certificates derived from the complete reduction. No outside-R class was
accepted, so the protocol's conditional additional positive controls were
not triggered. Earlier proof packages and visual work remain unchanged.

See the [review package](../reviews/2026-09-29-cc-selector-support/README.md).
From the repository root:

```sh
python3 reviews/2026-09-29-cc-selector-support/reproduce.py
```

## 6. The CC information-loss checkpoint

The operational support omits almost every point of L. That is substantial
geometric information loss, but the proved equality T=R says it does not
alter this particular positive-integer coefficient decision. The simpler
whole-L condition is an adequate carrier for this question.

Three details prevent a misleading shortcut. The support is not dense;
its auxiliary point D really disappears when p=q is excluded; and periodic
safety has disconnected lap bands. None of those facts alone establishes
or refutes equivalence. The large-slope obstruction and exhaustive remaining
classes establish it, with failed physical outputs available for rejection.

This conclusion depends on the coefficient domain, threshold and first-integer
selection rule. A changed rule or real coefficient domain requires a new
adequacy check. No richer ambient model is needed for the present decision.

**Next proposed:** make a reusable coefficient checker that returns either
the existing witness guarantee or a concrete failed p,q for this selector,
including the analytic large-slope cases. Then use those certificates to
choose a controlled change of contact rule or geometry. That implementation
and transfer have not been performed here; external mathematical review
remains open.
