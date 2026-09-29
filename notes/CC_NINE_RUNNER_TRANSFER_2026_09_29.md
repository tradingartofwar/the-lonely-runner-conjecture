# Compatibility Calculus: the nine-runner joint transfer

September 29, 2026. Initial source eee207819d61043e6f49cc44cba7ed9472865a91.

**Result:** the frozen joint compiler succeeds at the stronger threshold 1/8
for the family

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q).
\]

For positive integer parameters, nine distinct speeds require p!=q and p!=2q.
All runners start together; the selected reference is stationary. The output
constructs one time, not an optimum, full safe set or all-reference result.
The conditional 1/9 experiment was **NOT_TRIGGERED**. Success at 1/8 implies
the required 1/9 bound for this family.

**Status:** exact computation is OBSERVED / REPRODUCED in the frozen scope;
the universal construction remains HYPOTHESIS / internally reviewed proof
candidate. Material reasoning, implementation and reviews were AI-assisted.
Separate AI reviews are not blind, external human or formal verification.
No new existence-coverage or originality claim is made.

## What this experiment actually adds

The previous [coefficient-range result](CC_ROW38_COEFFICIENT_RANGE_2026_09_29.md)
already accepts (6,2) for every primary output of the fixed (3,8) selector.
Both conditions therefore hold at the same selected point, and primary joint
coverage was already a consequence of that result. This connection was made
explicit after the frozen joint run; it was not used to bypass clipping or
choose the emitted menu. Presenting the run as newly established family
existence would lose relevant prior information.

The new evidence concerns the compiler: can it construct a certificate while
carrying two added lap labels simultaneously? It can. The first two selected
segments match the prior (3,8) geometry, while the auxiliary p=q fallback
changes. The old auxiliary point (1/8,1/8) makes 6x+2y=1 and fails; the new
third segment supplies (7/24,7/24). The primary domain and its auxiliary
extension have different obligations.

## Frozen input and output

The [protocol](../reviews/2026-09-29-cc-nine-runner/PROTOCOL.md) was frozen before
target computation, SHA256
`6ac956e7fd36524c6168dd626548619b5cc07afd28f4ce951de6f4283db9940f`.
Seven pinned files matched the live source tree. Three archived one-added-row
certificates, for (5,2),(6,2),(3,8), were reproduced before the joint trial.

The joint clipper intersects both closed lap bands at one edge parameter.
Provenance now includes both laps. The imported ranking, first-leader rule,
400-pair rectangle limit, complete residual table and greedy fallback rule
are unchanged. The clipping budget is explicitly enlarged from 256 single-row
attempts to 2,048 joint lap-pair attempts; only 38 were needed. Domain metadata
and physical distinctness are explicitly adapted for nine runners.

| Output | Exact count |
| --- | ---: |
| Original parent floor edges | 24 |
| Joint edge/lap-pair attempts | 38 |
| Candidate records | 36 |
| Point records, with provenance retained | 4 |
| Descending candidates | 22 |
| Leader exception rectangle | 49 |
| Residual primitive pairs | 17 |
| Candidate/contact entries | 612 |
| Emitted menu entries | 3 |
| Uncovered labelled directions | 0 |

The raw result is COMPLETE_COVER_CERTIFICATE, hence also PRIMARY_COMPLETE.
No auxiliary restriction was needed to turn an incomplete output into success.
Neither full-parent recovery nor threshold-floor regeneration was triggered.
Their conditional implementations are not validated by this successful run.

## The construction and finite reduction

The emitted menu, in order, is:

| Identity | Segment | Eight torus lap labels |
| --- | --- | --- |
| P5:E0-3:K3:L7 | y=9/8-x, 1/4<=x<=3/8 | (0,0,1,1,1,2,3,7) |
| P2:E0-1:K2:L2 | y=9/8-3x, 7/24<=x<=55/168 | (0,0,0,0,1,1,2,2) |
| P2:E0-3:K2:L3 | y=7/8-2x, 1/4<=x<=31/104 | (0,0,0,0,1,1,2,3) |

Every labelled phase lies in [1/8,7/8] at both endpoints, hence throughout
each segment by affinity. In particular, the newly combined (6,2) phase
on the leader is 4x-3/4 in [1/4,3/4], and on the first fallback it is
identically 1/4. This is a direct same-point safety explanation.

Write d=gcd(p,q), P=p/d, Q=q/d. A torus point lies on the primitive physical
orbit exactly when H=Qx-Py is an integer. On the leader its image is

\[
\left[(2Q-7P)/8,\ (3Q-6P)/8\right],
\]

of width (P+Q)/8. A closed interval of width at least one contains an integer.
Thus P+Q>=8 is covered without parameter enumeration. The remaining positive
coprime P+Q<8 give exactly 17 pairs in the 7-by-7 rectangle. The full 612-entry
matrix shows that the leader misses precisely (1,1),(1,4),(2,1).

The first fallback repairs (1,4) and (2,1), at points
(17/56,3/14) and (9/28,9/56). The third repairs (1,1) at (7/24,7/24).
Both (1,1) and (2,1) are excluded from the nine-distinct-speed domain.
Consequently the first two entries suffice there, as a deduction from the
unchanged output. No minimality or retuned-compiler claim follows.

For a contact (x,y,H), choose integers r,s with rP+sQ=1 and put

\[
N=\lfloor rx+sy\rfloor,\quad \tau=rx+sy-N,\quad t=\tau/d.
\]

For row (a,b), labelled lap m and physical speed v=ap+bq, the retained identity is

\[
vt=\underbrace{m+(-as+br)H-(aP+bQ)N}_{\text{physical lap}}
  +\underbrace{ax+by-m}_{\text{phase}}.
\]

All eight phases are safe together. The first two rows ensure 0<t<1/d.
The core speeds after p,q strictly increase for positive parameters; both added
speeds exceed the core, and their equality is 3p=6q. This proves the stated
collision conditions. The construction also works for the labelled auxiliary
inputs, without calling them nine distinct speeds.

## Controls and review

Twenty frozen physical controls all pass with minimum exactly 1/8: sixteen
have nine distinct speeds, while (1,1),(2,1),(2,2),(4,2) are auxiliaries with
eight distinct speeds. Gcd scaling, direct products, both lap representations,
reflection 1-t and alternate Bezout recovery are retained.

At (p,q)=(1,4), the nine speeds are (0,1,4,5,6,7,11,14,35), and the common
witness is t=17/56. The added speed 14 has phase 1/4 and speed 35 has phase
5/8; the full minimum is 1/8.

Opening the chosen segments loses contact at (1,2),(2,3),(4,6): three tested
configurations, two primitive directions, all primary. Opening the entire
candidate class loses none of the twenty. These statements concern the
specified representations and controls, not every possible open segment.

Separate geometry reconstruction matches 5,985 scalar fields. The physical
review independently checks twenty coordinate-lap recoveries, 160 selected
and 160 reflected phases and their laps, forty alternate Bezout recoveries,
576 endpoint-band checks and four gcd comparisons. The proof review passes.
All five exact output files reproduce byte-for-byte. Review reports and a
hash manifest are included; conditional paths remain explicitly unexecuted.

Reproduce from the repository root:

```sh
python3 reviews/2026-09-29-cc-nine-runner/reproduce.py
```

## CC adequacy and continuity checkpoint

**Representation:** joint closed parent-edge segments with eight lap labels,
integer orbit contact and physical recovery. **Question:** one stationary
reference witness in this positive two-parameter family. **Retained:** both
added constraints at the same point, provenance, endpoints, gcd, exact phases,
laps and collision conditions. **Omitted:** parent interiors, new boundaries
created by added bands, optima and other reference runners. The pinned full
parent bands provide a conditional recovery route, not losslessness of edges.

This operation needs an extra lap label and the corrected parameter domain;
it does not require a replacement CC model. The inherited finite-exception
segment mechanism and lap-polyhedron translation remain useful existing
frameworks, credited in the pinned [literature comparison](CC_LITERATURE_COMPARISON_2026_09_29.md).
The eight-runner literature theorem is not silently extended to nine.

The material information loss was in planning: remembering that (6,2) and
(3,8) each worked while overlooking that the latest classification already
placed them on the same primary selector. Recovering that relation changes
the interpretation from new coverage to a joint compiler and auxiliary test.
This is exactly why continuity checks belong alongside arithmetic checks.

## Next proposed experiment

A more discriminating increase is a frozen ten-runner transfer adding
(38,18), an archived row outside the current selector's range. At the already
recorded primitive pair (1,20), that selector chooses 7/24; the added speed
398 has phase 1/12, below the ten-runner target 1/10. Thus simply reusing the
current selected time will fail. Another menu might repair it.

No ten-runner geometry or compiler run has been performed. Freeze its source,
threshold and budgets before testing. The coefficient-aware dispatcher remains
a separate pending implementation. Do not infer broad portability from this
informed nine-runner success.
