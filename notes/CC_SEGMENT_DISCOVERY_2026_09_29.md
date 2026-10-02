# Compatibility Calculus: discovering the two-segment certificate

September 29, 2026. **HYPOTHESIS / complete proof candidate with exact internal
checks.** Same-coordinator review and development; no independent mathematical
review, formal verification, new family coverage or novelty claim.

A fixed procedure applied to the six-coordinate parent model and the added
seventh band recovers the two previously selected segments. It chooses their
order by an explicit coverage criterion: P3 first covers every integer
\(q\ge6\), and P1 fills the only gaps, \(q=2,4\). The remaining prefix cases
\(q=3,5\) already succeed on P3. The procedure uses no child-cell or optimum
data to make its choices.

This closes the discovery question on this development example. The useful
mechanism is an eventual integer-width guarantee plus a finite prefix check.
It does not establish that suitable parent-edge segments exist in every model.

## 1. Scope and review of the preceding result

The family remains

\[
A_q=(1,q,q+1,q+2,q+3,2q+3,2q+5),\qquad q\in\mathbb Z,\ q\ge2,
\]

with seven moving runners, a selected stationary reference, common start and
closed threshold \(1/8\). Coordinates are \(x=\{t\}\), \(y=\{qt\}\), with
actual orbit \(h=qx-y\in\mathbb Z\). Recover time \(t=x\) and physical laps
\(\ell_i=m_i+b_i h\) for coefficient row \((a_i,b_i)\).

The [preceding proof](CC_BOUNDED_SELECTOR_2026_09_29.md) at frozen commit
`b72f21f88113a87728de55b8fb2ecdd3332d0cde` was reviewed against these obligations:

| Obligation | Review finding |
| --- | --- |
| Every point of each chosen segment satisfies seven joint bands | The affine charts and their closed endpoint values are correct. |
| Primary coverage for all integers, not a finite extrapolation | Width \((q+3)/12\ge1\) for \(q\ge9\), plus the seven small cases, leaves exactly \(q=5\). |
| Ceiling sign and endpoint cases | The negative lower endpoints at \(q=2,3\) round to zero. Equality at \(q=4,6\) is included. |
| Fallback and physical recovery | \(q=5,t=25/56\), integer orbit and all seven physical laps/phases agree. |
| Claim and cost quantifiers | One witness, bounded arithmetic-operation count; neither optimality, all witnesses nor constant bit-time is asserted. |

No result-level defect was found in this same-author review. Both prior
checker outputs reproduce byte for byte, recorded in
[PRIOR_REPRODUCTION.json](../reviews/2026-09-29-cc-segment-discovery/PRIOR_REPRODUCTION.json).
This does not promote the candidate to an independently established proof.
The prior package remains unchanged.

## 2. From a supplied segment to a finite coverage decision

Let \(p=(x_0,y_0)\), \(r=(x_1,y_1)\) be endpoints of one labelled closed segment
on which all seven phase bands hold. Orient it so that
\(\Delta x=x_1-x_0>0\); put \(\Delta y=y_1-y_0\). Its signed orbit difference is

\[
H_q(r)-H_q(p)=q\Delta x-\Delta y.
\]

Define

\[
Q(p,r)=\max\left(2,\left\lceil\frac{1+\Delta y}{\Delta x}\right\rceil\right).
\]

For every integer \(q\ge Q\), this difference is at least one. Therefore the
closed orbit interval contains an integer. Round its lower endpoint upward,
and interpolate on the same segment to recover the physical point.

For a finite list of safe segments containing at least one with
\(\Delta x>0\), let \(Q_*\) be the least such cutoff. One chosen segment covers
every \(q\ge Q_*\). Consequently:

> The entire supplied segment list contains a physical witness for every
> integer \(q\ge2\) if and only if it covers each integer
> \(2\le q<Q_*\).

The forward implication is immediate. For the reverse implication, the chosen
segment handles the unbounded tail and the checked list handles the finite
prefix. This is a complete finite reduction **relative to the supplied segment
class**, under the stated nonvertical-segment hypothesis. It does not assert
that this class represents every safe point.

Vertical segments and points remain available for prefix coverage. If both
endpoint orbit values coincide, the segment is usable exactly when that value
is integral; choose either endpoint. If no nonvertical segment exists, this
particular tail reduction returns no certificate, not a loneliness failure.

## 3. The declared discovery rule

The [protocol](../reviews/2026-09-29-cc-segment-discovery/PROTOCOL.md) was saved
before execution. The old answer was already known, so this is a development
test rather than a blind or held-out discovery.

The mathematical input is an exact extraction of the eight six-form parents
from the frozen atlas, with rows
\((1,0),(0,1),(1,1),(2,1),(3,1),(3,2)\), their lap labels, vertices and incidence.
The discovery program reads this [parent-only input](../reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json)
and explicitly adds row \((5,2)\). It does not read the previous selector,
child atlas or optimum spectrum.

1. Take every parent edge whose endpoints lie at \(z=1/8\).
2. Clip it by every seventh band that can intersect its phase range,
   \(k+1/8\le5x+2y\le k+7/8\). Keep closed points and vertical segments.
3. Order records by parent index, original vertex pair and seventh lap.
4. Select the segment with the smallest tail cutoff \(Q\), using that order
   for ties. Check all integers in its finite prefix.
5. While gaps remain, add the segment covering the greatest number of them,
   with the same tie-break. Stop at coverage or report an uncovered input.

For this bounded run, a cutoff above 26 would produce a scope-limit report
instead of expanding the declared input range. The computed cutoff is six,
so that guard is not reached.

The greedy step is not claimed to minimize the number of segments. If the
candidate list covers every prefix input, it must make progress and terminate
after at most one addition per initially uncovered input. Thus ranking affects
which certificate is produced, but cannot prevent completion when the full
list covers the prefix. A returned gap refutes coverage by this restricted
candidate list, not existence of another physical witness.

## 4. Result and physical selection

The 24 parent floor edges produce 27 labelled, nonempty clipping records:
13 nonvertical segments, five vertical segments and nine point records.
These are provenance records; repeated points on different source edges remain
separate. Of the 13 tail candidates, the least cutoff is \(Q_*=6\).

| Selection order | Source | Segment | Role |
| --- | --- | --- | --- |
| 1 | P3, edge 0–1, seventh lap 2 | \(3/8\le x\le1/2,\ y=9/8-2x\) | Width \((q+2)/8\ge1\) for all \(q\ge6\); also covers \(q=3,5\). |
| 2 | P1, edge 1–3, seventh lap 1 | \(1/8\le x\le5/24,\ y=7/8-3x\) | Covers both remaining prefix inputs \(q=2,4\). |

These are the previous two segments, with the order chosen by the declared
rule. The first one's finite prefix is fully accounted for:

| \(q\) | P3 orbit interval | First integer | P3 succeeds? | Selected time |
| --- | --- | --- | --- | --- |
| 2 | \([3/8,7/8]\) | 1 | no | \(7/40\), from P1 |
| 3 | \([3/4,11/8]\) | 1 | yes | \(17/40\) |
| 4 | \([9/8,15/8]\) | 2 | no | \(1/8\), from P1 |
| 5 | \([3/2,19/8]\) | 2 | yes | \(25/56\) |

For P3, choose \(h=\lfloor(3q+4)/8\rfloor\) and return

\[
t=\frac{8h+9}{8(q+2)}.
\]

For its two failures, P1 chooses \(h=0\) and returns
\(t=7/[8(q+3)]\). The implementation performs the interval tests rather than
hardcoding those exceptional inputs. All selected times have separation
exactly \(1/8\), from the fourth P3 phase or fifth P1 phase. Different safe
times from the old selection order are expected and are not a disagreement.

Preprocessing and online selection are distinct. This fixed example processes
24 edges and 27 clipping records, compares 13 tail cutoffs, checks a
27-by-4 prefix coverage matrix, and makes one greedy addition. Once this
certificate is built, each physical input uses at most two roundings/tests and
one interpolation. Bit complexity depends on \(q\); preprocessing costs can
grow when the input geometry or cutoff changes. No runtime improvement over
the previous selector is claimed.

## 5. Separate reconstruction and equality countercheck

[discover.py](../reviews/2026-09-29-cc-segment-discovery/discover.py) clips
individual edges in one dimension. The separately structured
[countercheck.py](../reviews/2026-09-29-cc-segment-discovery/countercheck.py)
reconstructs two-dimensional floor polygons from the six-form inequalities,
then adds the seventh inequalities and enumerates exact intersections of
boundary lines. It imports no discovery code or previous selector.

The reconstruction checks all eight parent floor polygons and their boundary
incidence. Forty parent/lap possibilities require 4,200 line-pair attempts and
give ten nonempty clipped floor polygons. Their intersections with original
parent boundaries reproduce all 27 candidate records. The checker also verifies
all 108 prefix coverage entries, the declared ranking and greedy step, and
the unbounded tail inequality. Both programs are coordinator-authored;
structural separation is not independent authorship.

Only the archived inputs \(q=2,\ldots,25\) receive direct physical checks.
Selected and reflected times pass all 336 exact distance checks, with physical
laps verified. No optimizer or enlarged physical scan was run.

The endpoint-removal control is consequential: at \(q=4\), the closed
candidate class contains the folded physical times \(1/8,3/8\). Removing
point records and every segment endpoint leaves **no candidate witness**.
Thus even this successful compact discovery model must retain equality;
positive segment interiors alone are insufficient in the tight case.

Reproduce from the repository root:

```bash
python reviews/2026-09-29-cc-segment-discovery/discover.py
python reviews/2026-09-29-cc-segment-discovery/countercheck.py
```

The [package](../reviews/2026-09-29-cc-segment-discovery/) contains pinned
inputs, exact outputs, prior reproduction and hash manifests.

## 6. CC adequacy checkpoint and limits

**Representation/version:** parent-edge discovery certificate, version 1.

**Question/output:** discover and certify a fixed list selecting one physical
\(1/8\)-safe A-ray time for each integer \(q\ge2\).

**Domain and next operation:** the same ordered seven forms, stationary
reference and closed threshold. Generate candidate edge portions, certify an
unbounded tail and finite prefix, then use their joint orbit and inverse map.

**Retained information:** source labels and incidence, closed clipping,
endpoint phases, projection width, tail cutoff, complete prefix coverage,
deterministic selection order, physical time and lap recovery. Discovery and
evaluation costs are recorded separately.

**Omitted information:** parent face interiors, child edges newly cut inside
those faces, higher-level geometry and most safe points. This is sufficient
for the certified one-witness output here. It does not carry optimal values,
all maximizers or the complete safe set. The prior \(q=10\) new-face example
still defeats an all-maximizer reading. The \(q=4\) endpoint control defeats
replacing this closed record by positive interiors.

**Richer source and recovery:** the parent atlas at
`b72f21f88113a87728de55b8fb2ecdd3332d0cde` is pinned in the input records.
Recover all parent inequalities and impose the seventh bands and the actual
integer orbit before asking a stronger question. Recover physical time/laps
with the explicit map in section 1; do not substitute marginal feasibility.

**Evidence and limits:** same-author review, a conditional finite reduction,
exact discovery/reconstruction agreement and the declared physical controls.
The complete all-q argument on this family is a proof candidate. The procedure
was designed after seeing a successful example; transfer to a changed ray or
model is untested here. Absence of a suitable tail or prefix cover does not
contradict loneliness.

**Failure/enrichment trigger:** invalid bands, missing point intersections,
incorrect cutoff arithmetic, uncovered prefix inputs or a failed inverse map.
If the restricted edge class fails, recover face interiors or a richer model
before drawing a physical conclusion. A new ray, reference, coefficient set,
threshold or requested output requires its own adequacy check.

**Framework assessment:** standard affine projection, closed polyhedral
clipping and greedy finite covering supply the necessary operations. CC now
records a discovery certificate in addition to a selected witness. This is a
modification of our current representation, not a new formal language or a
claimed invention of those methods. No external theorem is newly imported or
modified; prior attribution remains in the linked spectrum/transfer record.
Other frameworks remain eligible under the
[representation rules](CC_REPRESENTATION_RULES.md).

**Next proposed bounded transfer:** try the frozen rule on the already studied
B ray using its correct orbit \(x-qy\in\mathbb Z\) and clock \(t=y\), with the
coordinate translation derived explicitly and archived controls reused. This
has not been executed here. It would test transfer beyond the example used
to design the rule, while retaining the distinction between a supplied-class
coverage certificate and a general existence theorem.
