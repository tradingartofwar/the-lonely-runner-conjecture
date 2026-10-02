# Exact sheet coverage and a limit of the supplied source class

October 2, 2026 UTC. AI-derived argument, **proof candidate awaiting independent review**. Exact development checks support the declared cases; they do not promote the unbounded statements to an established theorem. The frozen finite validation will be reported separately.

## Scope and inherited representation

We retain the ten distinct common-start speeds

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r)
\]

for positive integers, selected stationary reference, and closed threshold 1/8. This exceeds the required ten-runner distance 1/10. It is a structured rank-three coefficient family, not arbitrary ten-runner data or all reference runners. Sources are the same 36 labelled rational xy segments/points, lifted through z in [1/8,7/8], pinned from the earlier rank-three study.

Normalize (p,q,r)=g(A,B,C). Write d=gcd(A,B), P=A/d, Q=B/d and choose aP+bQ=1, cd+eC=1. These exist because gcd(A,B,C)=1. The inherited saturated orbit conditions are

\[
h=Qx-Py\in\mathbb Z,\qquad n=C(ax+by)-dz\in\mathbb Z.
\]

They apply at the same point. With w=ax+by, recover tau={cw+ez} and physical time t=tau/g. The identities Pw=x-bh, Qw=y+ah, d(cw+ez)=w-en and C(cw+ez)=z+cn prove that the recovered phases are x,y,z. This reuses the prior recovery argument and all physical lap checks. It does not replace the joint relation by two marginal ranges.

## Necessary and sufficient criterion for one sheet

Let (x(s),y(s))=(x0,y0)+s(dx,dy), 0<=s<=1. Let h(s)=h0+s*Delta_h and w(s)=w0+s*Delta_w. There must first be an integer h between the two endpoint h values, inclusive.

If Delta_h is nonzero, each such integer fixes s exactly. On that same slice, the second projected coordinate ranges over

\[
[Cw(s)-7d/8,\ Cw(s)-d/8].\tag{1}
\]

The sheet succeeds exactly when at least one of these intervals contains an integer. Recovery uses n=ceil(Cw(s)-7d/8) and z=(Cw(s)-n)/d. Closed interval arithmetic retains equality and point witnesses.

There are two useful cases:

1. **d>=2:** (1) has length 3d/4>=3/2. Every nonempty first integer slice succeeds, regardless of C. Thus the first integer-contact interval alone decides coverage. This conclusion depends on the full vertical safe slab and the saturated normalization; it is false for a fixed z edge or an unsaturated replacement relation.
2. **d=1:** (1) contains an integer exactly when {Cw(s)} lies in [1/8,7/8]. The first integer condition alone is insufficient. The eight archived menu failures are all in this case.

If Delta_h=0, a noninteger constant h rejects the sheet. For integer constant h, the complete connected rectangle in (s,z) maps onto

\[
[\min(Cw0,Cw1)-7d/8,\ \max(Cw0,Cw1)-d/8].\tag{2}
\]

Integer containment in (2) is necessary and sufficient. Interpolating between its extremizing corners recovers an actual point. Its length is C|Delta_w|+3d/4; length at least one is sufficient, not necessary. This also handles point bases, where Delta_w=0. It avoids treating a continuum of first contacts as one arbitrary endpoint.

## Coprime case as exact modular counting

For Delta_h!=0 and d=1, write

\[
Cw(h)=\alpha h+\beta=(u h+v)/M
\]

with integral u,v, positive M and common factors removed. Let L=ceil(min(h0,h1)), U=floor(max(h0,h1)), N=U-L+1. The inclusive safe residues are

\[
\ell=\lceil M/8\rceil,\qquad q=\lfloor7M/8\rfloor.
\]

If N<=0 or ell>q there is no contact. Otherwise set b=uL+v. For j=0,...,N-1, the exact indicator that (uj+b) mod M belongs to [ell,q] is

\[
\left\lfloor\frac{uj+b+M-\ell}{M}\right\rfloor
-\left\lfloor\frac{uj+b+M-q-1}{M}\right\rfloor.\tag{3}
\]

To check (3), write uj+b=Mk+r with 0<=r<M. Each shifted floor is k plus the indicator of r reaching its threshold; subtracting gives precisely the inclusive range indicator. Summing (3) gives the number of successful integer slices. A positive count decides coverage; binary search on prefix counts returns the first successful h. This keeps phase compatibility without scanning each h individually.

The floor-sum primitive F(N,M,u,b)=sum floor((uj+b)/M) is standard, not a CC invention. [AtCoder Library's official math documentation](https://atcoder.github.io/ac-library/production/document_en/math.html), inspected October 2, 2026, specifies this sum and logarithmic arithmetic-operation complexity. Our Python routine uses signed quotient/remainder reductions and Euclidean reciprocity with arbitrary-size integers; it does not inherit the library's fixed-width overflow behavior. The adaptation is the sheet-to-residue translation and witness recovery above, which require their own checks. This is a targeted primitive attribution, not a literature review establishing novelty.

The Euclidean loop first extracts the integer parts of u/M and b/M, adding their sums. For the remaining 0<=u,b<M, if uN+b<M the remaining sum is zero. Otherwise exchanging the axes of the lattice-point count replaces (N,M,u,b) by (floor((uN+b)/M),u,M,(uN+b) mod M). The positive modulus strictly decreases after reduction. Prefix bisection uses logarithmically many counts; these are arithmetic-operation descriptions, not bit-complexity or measured runtime claims. The small fresh box may provide little practical benefit over enumeration.

Development checks compare 35,721 signed floor sums and 8,019 inclusive residue counts/first hits against direct loops. All 14,652 sheet bits on the exposed 407-case archive agree; all 4,582 successful contacts recover physically safe witnesses. Six auxiliary geometric inputs check constant h, points, rejection and equality. Some auxiliary speeds repeat; these test the contact kernel only and are excluded from physical LRC denominators.

## Why the eight old misses occur

The old four-sheet menu is source indices [27,17,6,21]. Every failed case has d=1. Below are all phases at the available first integer contacts of those four sheets; the remaining selected sheets have no first integer contact. None of these listed phases is in [1/8,7/8]. Exact per-sheet h intervals, contacts and the archived successful alternatives are in DEVELOPMENT.json.

| (p,q,r) | Third-runner phases at selected pair contacts |
| --- | --- |
| (1,2,8) | 0 |
| (1,4,8) | 0 |
| (1,7,4) | 1/16, 31/34 |
| (2,3,8) | 0 |
| (3,2,7) | 39/40 |
| (5,1,7) | 47/48 |
| (5,7,4) | 1/24, 55/58 |
| (5,7,8) | 1/12, 26/29 |

The same maximum-gain/provenance-tie greedy algorithm, now trained on all 407 exposed cases, selects [27,21,12,6,8,4,10], with gains [350,31,17,3,3,2,1]. It covers the development set using seven sheets. The four-sheet prefix covers 401/407; the old four cover 399/407. This is a refit on exposed data, not validation. The criterion is extensionally equivalent to the old exact contact solver: it does not itself create new coverage. Any fresh coverage change comes from different selection and, for the seven-sheet menu, a larger realized menu. Fresh validation must retain those distinctions.

## A constructed obstruction to every menu drawn from these 36 sheets

For p=1,q=2, the first eight moving speeds are (1,2,3,4,5,7,10,19). Intersecting their pair orbit (x,y)=({t},{2t}) with **every supplied source** gives exactly three physical times modulo one:

\[
T=\{1/8,\ 7/40,\ 3/8\}.
\]

This finite enumeration is complete: all source coordinates have 0<x<=1/2, so x=t in that half of the period. A nonpoint source has nonzero Delta_h for h=2x-y, and each integer h in its closed range gives exactly one intersection; point sources are checked directly. DEVELOPMENT.json records the complete 36-source list. Reflection adds the three reflected times but does not repair the obstruction below.

Every denominator divides 40. Thus **r=40k, integer k>=1**, gives {rt}=0 at all available times, including reflections. Every supplied sheet fails, whatever subset or ordering a compiler selects. The same conclusion holds for nonprimitive common scalings by rescaling physical time. This is a limitation of this source class, not of all possible sheets.

There are nevertheless real 1/8-safe times. The first eight speeds are safe throughout

\[
I=[25/152,\ 7/40],\qquad |I|=1/95.
\]

The saved fixed physical lap labels and both endpoint band checks certify the full interval by affinity. At r=40, t=25/152 has moving phases

\[
(25/152,25/76,75/152,25/38,125/152,23/152,49/76,1/8,11/19).
\]

All are in [1/8,7/8]. A separate physical-time implementation finds no sheet contact and computes the complete safe union [25/152,11/64] union [53/64,127/152]. This is a constructed development counterexample outside the fresh validation box.

For the whole family r=40k, the longest connected unsafe gap for the added runner on the real time line has length 1/(4r). Since 1/95>1/(160k), I cannot fit inside such a gap. An explicit recovery is: put l=25/152, j=ceil(rl-7/8), and

\[
t_k=\max\{l,(j+1/8)/r\}.
\]

The j-th closed safe band ends at or after l. If its start is after l, the wait is less than 1/(4r), so t_k remains in I. Otherwise l itself is in the band. This gives a safe time for every positive k, with equality conventions explicit. A demand for phase exactly 1/2 would be stronger and can miss a short valid interval; recovery uses the full safe band.

More generally, a finite rational set of pair-contact times is defeated by an added speed divisible by their denominator lcm. This conditional statement does not apply when a representation retains a continuous interval of pair-orbit contact. A direction-aligned base segment {(t,2t):t in I}, crossed with the safe z interval, would retain the successful alternatives here. That richer/adapted source is not silently added to the frozen 36-sheet comparison. Uniform construction for other p,q remains open.

## Representation checkpoint

Supported output: one actual time from one supplied safe sheet, or exact rejection of that sheet, under the stated product structure. The criterion retains simultaneous integer contact, saturation, closed boundaries, source labels and the inverse clock. Marginal ranges alone are inadequate. It omits the rest of the safe xy region and every source not in the selected menu. The richer pinned source class repairs the old eight menu misses, but the r=40 construction proves that even this class omits consequential alternatives. The full physical safe interval provides a recovery map for that example and motivates direction-aligned or full-cell sources. The finite test below evaluates transfer of selected menus only; no uniform coverage, optimum, all-witness, arbitrary-family or novelty claim follows.
