# Fixed-geometry coefficient range — September 29, 2026

Frozen before enumeration or new physical checks. Live input head:
`9e72fb318d83a4556f9063553da5a0b207aec72c`; mathematical input is the changed-row
certificate at `b2404d0d8ab43373a07c45d67bf4a432a2ddbc9d`.

## Questions and fixed data

Keep the first six coefficient rows and closed threshold 1/8. Fix the newly
selected leader L: y=7/8-2x, 1/4<=x<=3/8, with first-six laps(0,0,0,0,1,1),
and fallback F: x=1/8, 3/16<=y<=1/4, with first-six laps all zero.
The leading first-integer rule misses only primitive (1,2); its fallback is
the fixed point C=(1/8,1/4). Use the same primitive orbit and physical recovery.
The proposed seventh row (A,B) ranges over positive integers. Seventh laps
must be recomputed, rather than preserving labels 2 and 1 from row(6,2).

Distinguish two exact geometric proof contracts:

1. W: the entire closed L and entire closed F satisfy the seventh safety band,
   with a single integer lap on each connected segment.
2. R: the entire closed L satisfies the band and the single used fallback
   point C is safe. F away from C is outside this second contract's obligation.

Both contracts suffice for one safe time for every positive p,q under the
existing coverage and recovery proof. Classifying R is not a claim to find
the largest coefficient set on which every output of the deterministic selector
is safe; necessity outside these declared geometric contracts remains separate.
No re-clipping, new menu discovery, optimization or parent-interior search.

## Proposed symbolic reduction to check

Let u=2A+3B, v=3A+B, w=A+2B. Leader endpoint values are u/8,v/8.
Connected safety requires one k with 8k+1<=min(u,v)<=max(u,v)<=8k+7.
For F, endpoints are u/16 and (u+B)/16, requiring one ell with
16ell+2<=u<=u+B<=16ell+14. At C, safety requires w mod8 !=0.
Prove necessity as well as sufficiency for each segment contract; individually
safe endpoint residues with different laps do not establish segment safety.

With delta=A-2B, leader width is |delta|/8. Thus |delta|<=6 is necessary.
For W the fallback width is B/16, so B<=12. After proving these bounds,
enumerate only B=1..12 and delta=-6..6 with A=2B+delta>0: at most156 cases.
That is an exhaustive finite reduction, not an empirical coefficient-box scan.

For R, u=7B+2delta,v=7B+3delta and w=4B+delta. Membership depends on delta
and B mod8. Enumerate the complete13-by8 residue table using positive
representatives B=b+8, b=0..7, A=2B+delta. Prove periodicity under
(A,B)->(A+16,B+8), not by sampling a long coefficient sequence. Report all
accepted residue classes, positivity conditions and W subset R.

## Physical domain and exact controls

The labelled construction may include coincident speeds. For an actual
eight-distinct-speed statement require p!=q and Ap+Bq distinct from the
six core speeds. For positive A,B it exceeds p,q automatically; retain the
four remaining linear noncollision conditions. Do not silently inherit
p!=q as the whole distinctness test from the earlier specific row.

Before numerical checks, examine the analytically motivated progression
(A,B)=(6+16k,2+8k), k>=0. On L, 16x+8y=7; at C it equals4. Test whether
this preserves fractional seventh phases with changed integer laps.
Only k=0,1,2 receive direct physical controls, using exactly the preceding
18 parameter pairs for each: (1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
(1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10).
Total54 coefficient/parameter configurations, including three repeated-speed
auxiliaries. k=0 must reproduce the archived changed-row outputs. No broad scan.

Fixed boundary controls derived analytically before enumeration:
- (22,10) at native F point (1/8,9/40): test the proposed seventh collision,
  both endpoint residues and their different laps, and the safe used point C.
  This is an ambient geometric control, not a physical counterexample.
- (4,2) with (p,q)=(1,2): test whether leader safety alone misses fallback
  safety; check the proposed selector time directly without a loneliness claim.
- (5,2) with (p,q)=(2,3): test leader-boundary failure for this fixed geometry;
  preserve the earlier successful different-menu result as a scope distinction.
- Verify that W's coefficient bounds and closed equality cases are exact,
  and that stale seventh labels fail to recover the correct phases/laps.

No other coefficient trials, physical pairs or algorithm tuning. Corrections
must preserve timing and impact. An exact class rejection is a rejection of
its declared geometric contract, not of the entire Lonely Runner configuration.

## Review and interpretation

Coordinator writes the derivation and exact classification. Separate AI reviews
check (a) segment connectedness, bounds, residue completeness and boundary
controls; (b) the role-aware proof, physical recovery, noncollision domain and
information-loss interpretation using a different arithmetic route.
All coefficient tables and physical outputs must reproduce exactly.

This is a symbolic applicability analysis of fixed geometry, not another
held-out compiler transfer. Finite checks support implementation; the general
claims require the algebraic reduction. Existing literature attribution and
prior eight-runner existence coverage remain as recorded. The particular
construction/range argument is an internally reviewed proof candidate;
no novelty, external human review, formal certification, optimum or spectrum
claim is intended. No extra literature-priority conclusion follows.
