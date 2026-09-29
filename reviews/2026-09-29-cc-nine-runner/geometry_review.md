# Separate nine-runner geometry and coverage review

September 29, 2026. **PASS:** the separate exact reconstruction matches
**5,985 scalar fields** of the reached production output. This includes every
candidate, both added lap labels, clipping counts, ranking, leader, residual
pair, contact, greedy choice, raw and primary status, untriggered diagnostic
status and the complete pinned Stage A source geometry. Physical controls are
reviewed separately.

This is an internally performed AI review. It imports no production or prior
clipping/compiler code. It is not blind, human, external or formal review.
The reviewer read the frozen protocol and pinned inputs, reconstructed Stage A
before production output became available, and shared the resulting counts
and menu with the coordinator. The first production comparison passed without
changing the independent geometric or selection calculation.

## Independent construction

The review computes both lap ranges from each oriented source edge, enumerates
their Cartesian product and intersects **all eight labelled safety bands at
the same segment parameter**, together with the stored parent halfspaces and
the fold. This is an independent full-inequality implementation of the joint
clipping obligation. The two rows never receive separate parameter choices.
It retains singleton records and provenance duplicates and checks all eight
bands at each emitted endpoint.

Integral contacts are reconstructed by enumerating the integers in each exact
projected interval. Ranking and greedy steps are rebuilt using the declared
extended provenance `(parent,edge_start,edge_end,seventh_lap,eighth_lap)`.
All ties preserve that order. The review does not import the production sort
key, clipping function, compiler or selector.

| Quantity | Stage A result |
| --- | --- |
| Threshold | 1/8 |
| Parent floor edges | 24 |
| Joint edge/lap-pair attempts | 38 |
| Jointly safe candidate records | 36 |
| Singleton records | 4 |
| Endpoint band checks | 576 |
| Descending candidates | 22 |
| Leader rectangle | 49 pairs, within the frozen 400 cap |
| Primitive residual pairs | 17 |
| Candidate/residual contacts | 612 |
| Selected menu records | 3 |
| Raw status | `COMPLETE_COVER_CERTIFICATE` |
| Primary status | `PRIMARY_COMPLETE` |

The 38 attempts are below the declared 2,048 preprocessing cap. The distinction
between 38 attempts and 36 surviving records matters: the shared edge parameter
must satisfy both added bands simultaneously. Having separate nonempty clips
does not suffice.

## Coverage and domain

The leader `P5:E0-3:K3:L7` runs from `(1/4,7/8)` to `(3/8,3/4)`.
Its projected interval for a positive primitive `(P,Q)` is

\[
\left[\frac{2Q-7P}{8},\frac{3Q-6P}{8}\right],
\qquad\text{width}=\frac{P+Q}{8}.
\]

Every closed interval of length at least one contains an integer. The leader
therefore covers all primitive directions with `P+Q>=8`. The complete remaining
set consists of 17 positive coprime pairs with `P+Q<8`; the full 36 by 17 matrix
tests exactly the complement needed by this argument. The leader misses only
`(1,1),(1,4),(2,1)`.

The first fallback, `P2:E0-1:K2:L2`, is the segment from `(7/24,1/4)` to
`(55/168,1/7)`. It covers `(1,4)` and `(2,1)`. The second fallback,
`P2:E0-3:K2:L3`, runs from `(1/4,3/8)` to `(31/104,29/104)` and covers the
remaining `(1,1)` direction. Thus the emitted full-domain table is complete;
this run does not need the protocol's auxiliary-only-miss deduction to reach
`PRIMARY_COMPLETE`.

For nine distinct speeds, the primary domain excludes both `p=q` and `p=2q`.
Indeed, the core has distinct speeds when `p!=q`, each added speed exceeds
every core speed, and the two added speeds are equal exactly when
`6p+2q=3p+8q`, or `p=2q`. Hence `(1,1)` and `(2,1)` are auxiliary directions
here. The first two emitted records suffice on the primary domain as a
deduction from the unchanged full output. The third record must remain in the
compiler artifact; no smaller-menu or minimality search was performed.

The extra safety is visible directly on the selected geometry. On the leader,
the `(6,2)` row has phase `4x-3/4`, ranging from `1/4` to `3/4`; the `(3,8)`
phase is `2-5x`. On the first fallback, the `(6,2)` phase is constantly `1/4`
and the `(3,8)` phase is `7-21x`. These are simultaneous labelled phases at the
same point. A safe point with integral primitive orbit contact can then be
recovered physically through the inherited gcd and Bezout map; that recovery
must remain attached to the geometric certificate.

Stage A already certifies `1/8`, which is stronger than the required `1/9`
distance for nine runners. This does not prove a general nine-runner theorem:
the claim concerns the stated structured speed family and stationary reference.
It neither identifies optimum values nor certifies every reference runner.

## Continuity and limits

The prior [row-(3,8) coefficient classification](../../notes/CC_ROW38_COEFFICIENT_RANGE_2026_09_29.md)
already says that `(6,2)` succeeds under this same row-(3,8) selection rule for
every `p!=q`. Because that rule already makes `(3,8)` safe at its selected
point, the earlier result already implied simultaneous primary-domain
existence for this combined family. The present experiment supplies a frozen
**two-label compiler reconstruction** of that guarantee. It should not be
presented as first establishing the family's existence coverage. It also
recovers a different auxiliary fallback that handles `p=q`, where the prior
compact auxiliary choice failed the `(6,2)` row.

The success makes Stage B at `1/9` and the richer-parent diagnostic
`NOT_TRIGGERED`. Their code paths are unexecuted and are not validated by this
run. The review's Stage B implementation uses line-pair intersections as a
separate reconstruction route if reached; it was not executed. No new rows,
control pairs, alternative leaders, enlarged budgets or additional scans were
tried. The three archived single-row regressions are separate coordinator
checks, and the 20 frozen physical controls belong to the physical review.

The conditional infinite argument remains an internally reviewed proof
candidate. The experiment supports the current representation for this
specific joint operation; it does not classify all added-row combinations or
demonstrate universal compiler portability. Closed endpoints, shared labels,
provenance, collision conditions and physical recovery remain consequential.

## Reproduction and execution record

After `stage8.json` is present, from the repository root:

```sh
python3 reviews/2026-09-29-cc-nine-runner/geometry_review.py > /tmp/cc-nine-geometry.json
cmp /tmp/cc-nine-geometry.json reviews/2026-09-29-cc-nine-runner/geometry_review.json
```

The first independent execution produced the final geometry, counts, ranking,
menu and statuses before the production output was available. After it
appeared, the comparison adapter was added to compare the independently
reconstructed fields with the production serialization. This added metadata
and comparison code, with no changes to clipping, ranking, contact enumeration,
greedy choices or reached domain. The first comparison passed. The final
script hash and production output hash are retained in the JSON.
