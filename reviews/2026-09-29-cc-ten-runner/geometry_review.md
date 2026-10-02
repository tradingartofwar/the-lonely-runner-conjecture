# Separate ten-runner geometry and coverage review

September 29, 2026. **PASS:** the independently reconstructed Stage A output
matches **18,731 scalar fields** of the production record. The comparison
includes every candidate and all three added laps, clipping counts, ranking,
leader, residual direction, contact, greedy step, raw and primary status,
untriggered diagnostic status and complete pinned source geometry. Physical
controls and the motivating old-selector failure are reviewed separately.

This is an internal AI review, not blind, human, external or formal review.
No production or historical clipping/compiler module is imported. The reviewer
adapted its own preserved nine-runner checker to three simultaneous added rows,
leaving that earlier script unchanged. The first independent reconstruction
preceded the production output and already returned the final geometry, counts,
menu and statuses. Its first comparison against production passed without a
mathematical or selection correction.

## Independent construction and bounded output

For every oriented parent floor edge, the review derives all three integer
lap ranges from endpoint extrema, enumerates their Cartesian product and
intersects **all nine safety bands at the same parameter**, together with the
stored parent halfspaces and fold. Each retained endpoint is checked against
all nine labelled bands. It preserves singletons and duplicate geometry with
different provenance. Candidate ordering is the frozen numeric
`(parent,edge_start,edge_end,seventh_lap,eighth_lap,ninth_lap)` order.

Contacts are independently reconstructed by enumerating integers in each
projected closed interval and interpolating the first one. The review rebuilds
every ranking and greedy gain, retaining the extended provenance order in ties.
It does not import the production sort key or use a stored chosen identity as
a selection input.

| Quantity | Stage A result |
| --- | --- |
| Threshold | 1/8 |
| Parent floor edges | 24 |
| Joint edge/lap-triple attempts | 78 |
| Jointly safe candidate records | 52 |
| Singleton records | 4 |
| Endpoint band checks | 936 |
| Descending candidates | 31 |
| Leader rectangle | 8 by 17 = 136 pairs |
| Primitive residual directions | 47 |
| Candidate/residual contacts | 2,444 |
| Selected menu records | 4 |
| Raw status | `COMPLETE_COVER_CERTIFICATE` |
| Primary status | `PRIMARY_COMPLETE` |

Both reached resource checks pass: 78 attempts are below the frozen 2,048 cap,
and the 136-pair rectangle is below the unchanged 400 limit. The difference
between 78 attempts and 52 surviving records records a real compatibility
condition: individually possible lap bands need not share an edge parameter.

## Conditional infinite coverage argument

The selected leader is `P2:E0-3:K2:L2:M16`, from `(33/104,25/104)` to
`(3/8,1/8)`, lying on `y=7/8-2x`. For positive primitive `(P,Q)`, its integral
orbit projection is

\[
H\in\left[\frac{33Q-25P}{104},\frac{3Q-P}{8}\right],
\qquad\text{width}=\frac{3(Q+2P)}{52}.
\]

A closed interval of length at least one contains an integer. Since `Q+2P`
is an integer, the leader covers every primitive direction with `Q+2P>=18`.
The entire remaining domain is exactly the 47 positive coprime directions
with `Q+2P<=17`. The 8 by 17 rectangle is a valid bound for this complement;
the strict-width and coprimality filters give the 47 retained directions.
Therefore the full 52 by 47 contact matrix checks the entire finite complement
required by the infinite argument, rather than a sample of small inputs.

The leader misses 11 directions:
`(1,1),(1,2),(1,4),(1,5),(1,8),(2,3),(2,5),(2,11),(4,1),(5,1),(5,4)`.
The exact greedy additions are:

| Added record | Closed endpoints | Newly covered directions |
| --- | --- | --- |
| `P2:E0-3:K2:L3:M16` | `(1/4,3/8)` to `(31/104,29/104)` | `(1,1),(1,5),(1,8),(2,3),(2,11),(4,1)` |
| `P2:E0-1:K2:L2:M15` | `(7/24,1/4)` to `(41/128,21/128)` | `(1,4),(2,5),(5,4)` |
| `P0:E1-3:K1:L2:M9` | `(1/8,1/4)` to `(11/72,5/24)` | `(1,2),(5,1)` |

No residual pair remains. The raw certificate is fully complete; it does not
need the auxiliary-only-miss rule to derive `PRIMARY_COMPLETE`. Retain all
four emitted menu records, the original ranking and the complete greedy table.
No alternate-leader, reordered-menu or minimality test was run.

Same-point compatibility is explicit. On the leader the three added phases
with their retained laps are

\[
2x-\frac14,\qquad5-13x,\qquad2x-\frac14.
\]

They are safe on the stated common interval. The equal first and third phases
do not mean equal speeds or laps: the `(6,2)` row has lap 2 and the `(38,18)`
row has lap 16 there. Their raw values differ by 14 along this line. The exact
label distinction is needed for physical recovery. All candidate endpoint
inequalities, including the other segments, are checked by the independent
implementation and compared against production.

For ten distinct speeds, positivity and the strictly increasing core sums leave
the two exclusions `p=q` and `p=2q`. The latter is equality of `6p+2q` and
`3p+8q`. The newest row `(38,18)` strictly dominates every earlier coefficient
row and introduces no additional collision. Thus the stated primary domain
is correct, while the full certificate also retains both auxiliary primitive
directions `(1,1)` and `(2,1)`.

An integral primitive orbit contact has to be combined with gcd normalization
and the physical inverse map to produce a real time. Safe ambient geometry
alone is insufficient. The separate physical review checks the recovered times,
phases, laps, distinctness and reflected controls. The `1/8` construction is
stronger than the `1/10` ten-runner target for this structured family and selected
reference. It is not an arbitrary ten-runner theorem or an optimum claim.

## Conditional paths, information and claim limits

Stage A is complete, so the frozen condition prevents the `1/10` Stage B run.
There is also no primary uncovered pair, so the richer-parent diagnostic is
`NOT_TRIGGERED`. Neither conditional path was executed or validated. The review
retains a line-pair-intersection implementation for regeneration if reached,
but does not claim that unexecuted code has been tested by this result.

The known failure at `(1,20)` only rejected the previous chosen time. This
successful recomputation shows that the larger retained edge representation
can support a different common menu. The run does not exhibit an edge-class
exhaustion or prove that parent interiors/new added-band boundaries are needed.
It also does not show general portability or classify all possible additional
rows. Prior results and their exact hypotheses must still be consulted before
describing what family coverage was already implied.

No extra coefficient, threshold, parameter scan, alternative leader, increased
budget or diagnostic candidate was tried. The archived nine-runner regression
is a separate coordinator check. The frozen 22 physical pairs are a separate
physical review obligation. All universal claims remain internally reviewed
proof candidates, without a new originality or literature-frontier claim.

## Reproduction and execution record

With production `stage8.json` present, from the repository root:

```sh
python3 reviews/2026-09-29-cc-ten-runner/geometry_review.py > /tmp/cc-ten-geometry.json
cmp /tmp/cc-ten-geometry.json reviews/2026-09-29-cc-ten-runner/geometry_review.json
```

The original independent output was written before production became available.
The already-present production comparison adapter was enabled afterward and
matched on its first run. No candidate, lap, interval, ranking, contact,
coverage, menu or domain calculation changed. The final script and production
hashes are recorded in `geometry_review.json`.
