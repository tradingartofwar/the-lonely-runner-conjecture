# Separate proof and scope review: ten-runner transfer

September 29, 2026. This is a separately tasked internal AI review, not
blind replication, external human review or formal certification. I reviewed
the proposed bounds and scope before target computation, then inspected the
frozen protocol, implementation and emitted records. I ran no additional
target trial and did not import production code for this review.

The protocol's SHA256, checked from disk, is
`7d380e243a06de179fa2b456a86ebbeee35f8b8de75fc5ead6ebf8d15684f506`.
Its input head is `d38f6f5cc5bfdc1c7e848c946e7bf8ff3a6ae0ea`.
The reached outcome is full `COMPLETE_COVER_CERTIFICATE` at1/8. Both the
conditional1/10 stage and the richer parent diagnostic are `NOT_TRIGGERED`.

## 1. Domain, quantifiers and the prior failure

With stationary reference0, the nine moving rows are

    (1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),(38,18).

For p,q>0, the last row strictly dominates all earlier rows. The core has
a duplicate exactly when p=q, and the (6,2),(3,8) speeds coincide exactly
when p=2q. Therefore ten distinct total speeds are equivalent to p!=q and
p!=2q. The auxiliary primitive directions (1,1),(2,1) each have nine
distinct total speeds. There is no other collision condition.

The target is one safe time for the stationary selected reference, under a
common start. It is not a claim about all reference runners, arbitrary
ten-runner families, optimal separation or the complete witness set.
A uniform1/8 guarantee is stronger than the requested ten-runner1/10 bound.

At (p,q)=(1,20) the prior nine-runner rule selected t=7/24. The added speed
is398, and 398*(7/24)=116+1/12. This failed both declared thresholds at that
specific time. Its prior eight moving phases were safe. Neither this failure
nor the prior rejection of (38,18) by that selector excluded another common
safe time or exhausted the richer parent-edge geometry.

Unlike the nine-runner step, the previous T classification did not already
give this joint guarantee: it rejected (38,18) for the selector that made
(6,2) and (3,8) jointly safe. Acceptance of (38,18) under a different selector
cannot be joined to the first two rows' safety without one shared point.
The new joint computation retains all three added lap labels and intersects
all three bands at one common edge parameter.

## 2. General finite reduction and controlled adaptation

For any descending segment with coordinate increments alpha>0 and -beta<0,
the projection H=Qx-Py has width alpha*Q+beta*P. Its closed interval contains
an integer whenever the width is at least1. Every possible miss lies inside

    P<=ceil(1/beta)-1, Q<=ceil(1/alpha)-1,
    alpha*Q+beta*P<1.

This gives a proved finite residual domain. The inherited400-pair rectangle
cap bounds work, not truth. Clipping and rectangle resource stops would not
show candidate-class exhaustion. A completed candidate/residual matrix does.
If only excluded primitive directions remained uncovered, a separate
`PRIMARY_COMPLETE` deduction would be valid while retaining the raw result.
Here the emitted certificate is fully complete, so that weaker interpretation
is unnecessary.

The explicit adaptation adds the third lap to clipping, labels, provenance
and physical recovery. Ranking, first-leader-only selection, full positive
primitive matrix, greedy maximum gain and provenance ties are unchanged.
The2,048 joint-attempt cap was retained, and the larger diagnostic cap was
declared before execution. The archived nine-runner stage was reproduced
before installing the three-lap key. No alternate leader or retuned budget
was needed. Four point records remain candidates but cannot be descending
leaders; preserving duplicate geometry does not multiply physical points.

## 3. Four jointly safe segments

The emitted menu, in order, is:

| Name | Geometry | Nine torus labels |
| --- | --- | --- |
| L: P2:E0-3:K2:L2:M16 | y=7/8-2x, 33/104<=x<=3/8 | (0,0,0,0,1,1,2,2,16) |
| B: P2:E0-3:K2:L3:M16 | y=7/8-2x, 1/4<=x<=31/104 | (0,0,0,0,1,1,2,3,16) |
| C: P2:E0-1:K2:L2:M15 | y=9/8-3x, 7/24<=x<=41/128 | (0,0,0,0,1,1,2,2,15) |
| D: P0:E1-3:K1:L2:M9 | y=7/16-3x/2, 1/8<=x<=11/72 | (0,0,0,0,0,0,1,2,9) |

Subtracting the retained labels produces these nine phases in row order:

| Segment | Affine fractional phases |
| --- | --- |
| L | x; 7/8-2x; 7/8-x; 7/8; x-1/8; 3/4-x; 2x-1/4; 5-13x; 2x-1/4 |
| B | x; 7/8-2x; 7/8-x; 7/8; x-1/8; 3/4-x; 2x-1/4; 4-13x; 2x-1/4 |
| C | x; 9/8-3x; 9/8-2x; 9/8-x; 1/8; 5/4-3x; 1/4; 7-21x; 21/4-16x |
| D | x; 7/16-3x/2; 7/16-x/2; 7/16+x/2; 7/16+3x/2; 7/8; 3x-1/8; 3/2-9x; 11x-9/8 |

Endpoint substitution puts every phase in [1/8,7/8], and affinity proves
the same throughout each closed segment. On C, the new ninth phase runs
from7/12 down to1/8. On D it runs from1/4 to5/9. On L and B, it equals
the seventh phase. The constant core phases7/8,7/8,1/8,7/8 respectively
make the minimum separation exactly1/8 at every point of the corresponding
segment. This is the separation at the constructed witness, not optimality.

The equality of the seventh and ninth phases has a precise explanation:

    (38,18)-(6,2)=16*(2,1).

On L and B, 2x+y=7/8, so the raw values differ by14. Their retained torus
laps16 and2 differ by the same integer. This is a line-specific identity;
it neither holds throughout the torus nor by itself supplies the finite
exception cover.

## 4. Infinite tail and the complete residual cover

For the leader L the projection is

    [(33Q-25P)/104, (3Q-P)/8],
    width = 3*(Q+2P)/52.

Hence all primitive directions with Q+2P>=18 are covered. The exact remaining
domain is Q+2P<=17 with positive coprime P,Q. It lies in P<=8,Q<=17, giving
the declared136-pair rectangle; the filtered domain has47 pairs. This is
the complete necessary finite check, not a chosen sample. The matrix finds
precisely11 leader misses:

    (1,1),(1,2),(1,4),(1,5),(1,8),(2,3),(2,5),(2,11),
    (4,1),(5,1),(5,4).

The other three projection intervals are

    B: [(2Q-3P)/8, (31Q-29P)/104],
    C: [(7Q-6P)/24, (41Q-21P)/128],
    D: [(Q-2P)/8, (11Q-15P)/72].

Their selected integer contacts cover the misses in the emitted order:

| Segment | Newly covered primitive pairs | Corresponding first integers H |
| --- | --- | --- |
| B | (1,1),(1,5),(1,8),(2,3),(2,11),(4,1) | 0,1,2,0,2,-1 |
| C | (1,4),(2,5),(5,4) | 1,1,0 |
| D | (1,2),(5,1) | 0,-1 |

These integers belong to the displayed closed intervals. The retained full
matrix provides every candidate/contact decision; the separate arithmetic
review reconstructs that computation. The width argument plus the complete
residual cover proves the proposed uniform contact guarantee. The22 physical
controls alone would not establish it.

At the motivating input (1,20), the new leader interval is
[635/104,59/8]. Its first integer is7, yielding
(x,y)=(63/176,7/44) and physical time63/176. The new speed398 has phase41/88,
and the minimum across all nine moving speeds is1/8. The scaled input(2,40)
uses time63/352, with identical fractional phases. This is a different
physical selection that repairs the known failure.

## 5. Physical recovery and theorem candidate

Normalize d=gcd(p,q), P=p/d,Q=q/d. At any selected integer contact
h=Qx-Py choose rP+sQ=1 and set T=rx+sy, N=floor(T), tau=T-N, t=tau/d.
Then P*T=x-s*h and Q*T=y+r*h. For a row(a,b) with torus lap m,

    physical_lap = m+(-a*s+b*r)*h-(a*P+b*Q)*N

is an integer and gives
(ap+bq)t=physical_lap+(ax+by-m). All nine safety constraints therefore
hold at this same time. The positive first phase implies tau!=0, so
0<t<1/d. Integer speeds make the reflected time1-t safe as well; changing
the Bezout pair by(Q,-P) changes T by h and preserves its fractional part.

The theorem candidate is consequently: for every positive integer p,q, the
four-segment rule supplies a rational time when all nine moving speeds

    p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,38p+18q

are at distance at least1/8 from the stationary reference. For p!=q and
p!=2q all ten speeds are distinct, providing their selected-reference1/10
guarantee. The full-labelled result also covers both repeated-speed
auxiliaries. This is an internally reviewed proof candidate, not an external
or formal certification.

## 6. Conditional paths and information loss

The declared1/10 regeneration is mathematically complete in design: reflection
permits the folded box [z,1/2] x [z,1-z]; each nonnegative row(a,b) has raw
extrema (a+b)z and a/2+b(1-z), giving the protocol's exhaustive integer lap
range. Intersecting all bounded core-label tuples with all closed bands
retains the full six-core floor, including segments and singletons.

For a diagnosed primitive pair, all integer H in
[Qz-P(1-z),Q/2-Pz], all complete parent regions and all three added lap
ranges exhaust the folded joint safe set at that threshold. Substituting
y=(Qx-H)/P gives exact one-dimensional halfplane bounds, including constant
constraints. A single diagnostic witness would not replace a uniform
certificate or cancel the next stage; a capped diagnostic would not be an
exhaustion result. Failure at1/8 would not refute the1/10 target.

Neither path was reached because Stage A was fully complete. The run does
not validate execution of1/10 regeneration or a parent-interior recovery.
No enrichment beyond the existing edge class was needed here. That fact is
specific to this controlled three-row transfer, not general portability.

The CC checkpoint is that a compact failed selection required recovery of
alternative jointly labelled edges. Those alternatives repaired the failure
and yielded a uniform menu. The line-specific phase identity explains part
of the repair while preserving its restricted domain and changed laps.
The previous selector failure was never a claim of joint nonexistence.

## Finding

PASS for the collision domain, width reduction, all-three-label same-point
construction, closed endpoint handling, complete residual cover and physical
inverse map. The construction is stronger than the declared1/10 target for
this fixed family. The result does not establish arbitrary ten-runner
coverage, optimality, all-reference loneliness or originality. No fresh
literature/frontier determination was made; the repository's pinned
attribution and proof-candidate status remain in force.

## Post-protocol interpretation: an interior optimum at an existing control

This section was added after the frozen run and its endpoint-opening results.
It is a hand-derived consequence at the already declared control (p,q)=(1,2),
not a new frozen prediction, computational trial or modification of recorded
outputs. The coordinator proposed the observation and I checked it by hand.

The moving speeds at that input are

    1,2,3,4,5,7,10,19,74.

Their residues modulo6 are1,2,3,4,5,1,4,1,2. Therefore t=1/6 gives minimum
circle separation exactly1/6, strictly larger than1/8. The optimum is also
at most1/6: for any real t, consider the six circle points0,t,2t,...,5t.
If any coincide, one of speeds1,...,5 has distance0. Otherwise their six
cyclic gaps sum to1, so one gap is at most1/6. Its endpoints have an index
difference k in{1,...,5}; the corresponding circle distance ||kt|| is no
greater than that gap. Since all speeds1,...,5 are present, the overall
minimum cannot exceed1/6. Thus this configuration's exact optimum is1/6.

The torus point is (x,y)=(1/6,1/3), with H=2x-y=0. Every labelled phase
is strictly between1/8 and7/8, and x<1/2. Consequently this witness lies
away from the original threshold-floor edges, inside the joint safe region.
The reported failure of the opened edge candidates at this control is
therefore a limitation of that restricted representation, not an intrinsic
requirement that physical witnesses attain threshold equality. By continuity,
this strictly safe time also has nearby safe times at threshold1/8.

This analytical deduction answers the optimum question for this one input.
It does not determine every maximizing time, the complete safe-time set, or
optima for the full two-parameter family.

## Proposed next operation: sufficient boundary phase screening

This proposal is not implemented or tested in the present package. Suppose
an additional coefficient row u and an already safe row v satisfy

    u-v = 8k*c,

where k is an integer and c is a core row. On a labelled boundary with
c dot(x,y)=m+1/8, their raw-value difference is8km+k; on a boundary with
c dot(x,y)=m+7/8, it is8km+7k. Both are integers. Thus u and v have equal
fractional phases there, and the new torus lap follows by the same explicit
integer shift. This exactly explains the observed relation
(38,18)-(6,2)=16*(2,1) on the first two supporting segments.

The relation could guide candidate preselection before expensive joint
clipping. It is sufficient, not necessary: safe new rows need not have an
equal phase to an existing row, and other useful edges could be discarded.
Any such change needs a separately frozen rule, budget and transfer test,
with the richer candidate source retained as the recovery route and coverage
loss reported separately from resource savings. Changing ranking or candidate
scope does not inherit the old compiler's guarantee without checking its
hypotheses and full residual certificate. No future input or outcome is
selected or claimed by this review.
