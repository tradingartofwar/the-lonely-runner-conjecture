# Compatibility Calculus: repairing the ten-runner transfer

September 29, 2026. Source d38f6f5cc5bfdc1c7e848c946e7bf8ff3a6ae0ea.

**Result:** the frozen compiler repairs the known selector failure and
constructs a simultaneous **1/8** witness for the structured ten-runner family

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,38p+18q).
\]

Parameters are positive integers. Ten distinct speeds require p!=q and
p!=2q; the last row dominates all preceding speeds. All runners start together
and the selected reference is stationary. The stronger 1/8 certificate implies
the required 1/10 bound. The conditional 1/10 stage was **NOT_TRIGGERED**.

**Status:** exact bounded computation is OBSERVED / REPRODUCED; universal
construction is HYPOTHESIS / internally reviewed proof candidate. Material
AI assistance includes derivation, implementation and separate reviews.
This is not a general ten-runner theorem, a uniform optimality result, an
all-reference result, a literature-frontier claim or an originality claim.
A separate post-protocol deduction below determines the optimum of one input.

## The failure and its repair

At the already archived pair (p,q)=(1,20), the prior nine-runner menu selects
t=7/24. The added speed 398 has phase 1/12, below both 1/8 and 1/10. The other
eight moving speeds remain safe. This rejects that selected time; it does
not reject every available segment or every physical time.

The frozen joint compiler now chooses t=63/176. At this time all nine moving
speeds are safe, with minimum 1/8. The added speed 398 has phase 41/88, as does
speed 46 from row(6,2). The gcd 2 control (2,40) chooses 63/352 with identical
phases. The unchanged old failure and the new shared-time witness are both
retained in the package.

Unlike the nine-runner experiment, the previous coefficient classification
did not already establish this guarantee under the same selector: (38,18)
is outside that selector's range. Its acceptance under a different old rule
does not imply compatibility with the current added rows. The present result
is a repaired uniform construction within our research record; we make no
claim that existence for this family is absent from the literature.

## Frozen procedure and exact outcomes

[PROTOCOL.md](../reviews/2026-09-29-cc-ten-runner/PROTOCOL.md) was frozen before
new target clipping, ranking or controls, SHA256
`7d380e243a06de179fa2b456a86ebbeee35f8b8de75fc5ead6ebf8d15684f506`.
Eight input files matched the live source tree. The entire archived nine-runner
stage8 output, including its twenty controls, was reproduced before the trial.
The motivating selected-time failure was reproduced against its earlier record.

All three added lap bands are clipped at one common edge parameter. The key
now retains seventh, eighth and ninth laps. The imported coverage compiler
keeps its ranking, first-leader choice, 400-pair rectangle cap, full residual
table and greedy rule. The joint-attempt cap remains 2,048. Domain metadata
and physical recovery explicitly use nine moving rows. Prior packages are
unchanged; the whole adapter is not described as unchanged code.

| Reached Stage A quantity | Exact value |
| --- | ---: |
| Threshold | 1/8 |
| Parent floor edges | 24 |
| Edge/lap-triple attempts | 78 |
| Candidate records | 52 |
| Point records with provenance | 4 |
| Descending records | 31 |
| Exception rectangle | 8 by 17 = 136 |
| Residual primitive pairs | 47 |
| Candidate/contact entries | 2,444 |
| Emitted segments | 4 |
| Uncovered labelled pairs | 0 |

The raw status is COMPLETE_COVER_CERTIFICATE, also giving PRIMARY_COMPLETE.
All 22 frozen controls pass: eighteen ten-distinct-speed configurations and
four auxiliaries with nine distinct speeds. Every selected minimum is 1/8.
Stage B geometry regeneration and the richer-parent diagnostic were not
triggered; their implementations remain unvalidated by this run.

## Why the new leader works

The new leader lies on

\[
2x+y=7/8,\qquad 33/104\le x\le3/8.
\]

Here the new row and an already safe row differ by

\[
(38,18)-(6,2)=16(2,1),\qquad
(38x+18y)-(6x+2y)=16(2x+y)=14.
\]

Their unwrapped values differ by an integer, so their phases are identical.
With retained torus laps 16 and 2, both phases equal2x-1/4. This also holds on
the first fallback, which is another part of the same supporting line.

The identity is conditional on that line. It is not a global redundancy of
the added constraint. On the previous leader y=9/8-x the same difference
varies with x; the archived failure remains valid. The compiler's declared
geometric ranking finds a segment on which the new obligation is satisfied
through this exact relation. It did not explicitly search for that identity.

## Four segments and the infinite-tail argument

| Menu entry | Geometry and x interval | Nine torus labels |
| --- | --- | --- |
| P2:E0-3:K2:L2:M16 | y=7/8-2x; [33/104,3/8] | (0,0,0,0,1,1,2,2,16) |
| P2:E0-3:K2:L3:M16 | y=7/8-2x; [1/4,31/104] | (0,0,0,0,1,1,2,3,16) |
| P2:E0-1:K2:L2:M15 | y=9/8-3x; [7/24,41/128] | (0,0,0,0,1,1,2,2,15) |
| P0:E1-3:K1:L2:M9 | y=7/16-3x/2; [1/8,11/72] | (0,0,0,0,0,0,1,2,9) |

All nine labelled phases lie in[1/8,7/8] at each endpoint, hence throughout
each segment by affinity. A core phase is exactly1/8 or7/8 on each segment,
so the constructed minimum equals1/8. This does not rule out better times.

Let d=gcd(p,q), P=p/d,Q=q/d. The orbit condition is H=Qx-Py an integer.
The leader projects to

\[
\left[(33Q-25P)/104,\ (3Q-P)/8\right],
\qquad\text{width}=\frac{3(Q+2P)}{52}.
\]

Every closed interval of width at least one contains an integer. Since
Q+2P is integral, all Q+2P>=18 are covered. Every possible miss lies in
1<=P<=8,1<=Q<=17 with gcd(P,Q)=1 and Q+2P<=17: exactly 47 pairs. This bound
is proved from the segment width, not chosen from successful sampling.

The leader misses eleven residual pairs:
(1,1),(1,2),(1,4),(1,5),(1,8),(2,3),(2,5),(2,11),(4,1),(5,1),(5,4).
The fixed greedy rule adds three fallbacks with gains 6,3,2. The full 2,444-entry
matrix verifies every candidate/pair contact. The four-entry menu covers all
labelled positive directions, including auxiliaries. All four entries are
used on primary physical controls; no minimality search was performed.

At a selected contact choose rP+sQ=1, then

\[
N=\lfloor rx+sy\rfloor,\quad \tau=rx+sy-N,\quad t=\tau/d.
\]

For row(a,b), torus lap m and speed v=ap+bq, the physical lap is

\[
\ell=m+(-as+br)H-(aP+bQ)N,
\qquad vt=\ell+(ax+by-m).
\]

The identity retains all nine phases at one physical time, with 0<t<1/d.
The reviewers independently reconstruct it through coordinate-lap congruences
and direct multiplication. Reflection 1-t, alternate Bezout choices and five
gcd-scaling comparisons are retained.

## Equality exposes a new sensitivity

Opening every chosen segment loses the tested contacts at (1,2),(1,3),(3,1).
Opening all 52 candidate records still loses(1,2). This differs from the
nine-runner experiment, where opening the complete candidate class lost none
of the frozen controls. Point records have empty interiors; nondegenerate
constant integral projections are handled separately.

This is a failure of the opened edge representation at one primary direction.
The frozen richer diagnostic is triggered by closed candidate failure, so it
correctly remained unrun. Its trigger was not expanded after seeing this case.

**Post-protocol analytic deduction, separately hand-reviewed:** for the same
already frozen input (1,2), the ten speeds are (0,1,2,3,4,5,7,10,19,74).
At t=1/6, their moving phases are

\[
\frac{1}{6}(1,2,3,4,5,1,4,1,2),
\]

so the minimum is 1/6. Conversely, among the six circle points
0,t,2t,3t,4t,5t some cyclic gap is at most 1/6. Its index difference is one
of the present speeds 1,...,5, forcing some runner distance at most 1/6.
Thus this fixed input's optimum is exactly 1/6, which exceeds the constructed
1/8 value.

The torus point (x,y)=(1/6,1/3), H=0, is strictly inside every safety band at
threshold 1/8. Its labels are (0,0,0,0,0,1,1,3,12); it is in a parent-floor
interior, rather than one of the retained floor edges. This locates the lost
information directly. The analytic deduction changes no frozen output or
trial and is not a claim that the conditional diagnostic was executed. It
does not enumerate the complete safe-time set or all maximizers.

## CC checkpoint and scope

**Representation:** closed core-floor edges with three added lap labels,
integer orbit contact, finite coverage table and physical inverse map.
**Question:** one witness for this positive two-parameter family and selected
reference. **Retained:** same-point bands, all labels, provenance, equality,
domain, gcd and exact clocks. **Omitted:** parent interiors and new added-band
boundaries, optimum and full safe set, other references. Pinned full parent
halfspaces provide conditional recovery; storing them does not make edges
lossless for other operations.

The compact old selector was inadequate for this added constraint, but
recovering alternative edges was enough. The new leader's exact phase
identity explains one way a changed representation can restore compatibility.
CC needs the third lap label and domain update here; no replacement model
was required. The inherited segment mechanism and lap-polyhedron translation
remain credited in the pinned [literature comparison](CC_LITERATURE_COMPARISON_2026_09_29.md).
No eight-runner literature guarantee is extended by analogy.

## Reproduction and next question

Separate geometry reconstruction agrees on 18,731 scalar fields. Independent
physical review checks 22 witnesses, 198 selected and 198 reflected phases
and their laps, 44 alternative Bezout recoveries, 936 endpoint-band checks,
five gcd comparisons and the motivating failure/repair. The proof review
passes, including the separately labelled analytic deduction. All six exact
output files reproduce byte-for-byte against eight pinned inputs.

The package contains the frozen inputs, motivating failure, complete output,
separate geometry/physical/proof reviews, execution record and hash manifest.
From the repository root:

```sh
python3 reviews/2026-09-29-cc-ten-runner/reproduce.py
```

**Next proposed:** turn the phase identity into an explicit sufficient rule
for choosing promising existing edges before full clipping. If a new row
differs from a safe row by 8k times a core row, then on a boundary where that
core row has phase 1/8 or 7/8 their raw values differ by an integer. This
predicts equal phases on that supporting line. It does not say every useful
edge has that form, or that a full cover must exist.

Freeze a comparison of this restricted rule with full edge discovery on a
different declared input before testing it. Neither that implementation nor
another transfer has been run. The coefficient-aware dispatcher remains
separate pending work. The full safe-time set at (1,2) is also uncomputed;
its optimum is already settled by the displayed fixed-case argument.
