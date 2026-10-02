# Physical-time adversarial check of the CC other ray

September 29, 2026. **REPRODUCED within the declared finite scope.**

The fresh exact calculation found no discrepancy in the maximum or complete
maximizer set for **exactly q=2,...,25**. Every case has precisely the two times
claimed in `notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md`: 48 isolated
maximizer occurrences across 24 cases, with no positive-length maximizing
component. Direct witness checks at **exactly q=100002,...,100007** also pass.
Those six large cases received no exhaustive optimization or uniqueness check.

The scope is eight common-start runners, stationary selected reference 0,
moving speeds

`B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2)`,

and the physical time domain `[0,1]`. No other speed family, reference runner,
or initial phase was evaluated.

## Method and completeness

For each speed v, the function `||v t||` is a triangular wave with all corners
at `j/(2v)`, `j=0,...,2v`. Form the union of these corners and sort it exactly.
On every closed interval between consecutive corners, each of the seven
distance functions is one affine function `L_i(t)`.

For each i, intersect that interval with all six inequalities
`L_i(t)<=L_j(t)`. This produces its entire closed dominance interval, possibly
empty or a singleton. These intervals cover the base interval because at least
one of finitely many lines attains the minimum at each time. The code verifies
that coverage in every base interval. On each resulting piece the physical
objective is exactly the corresponding affine line.

Maximize each affine piece at its appropriate endpoint. If its slope is zero,
retain the whole piece. Union and merge every component attaining the global
maximum. This procedure enumerates the complete maximizing set, including
endpoints, coincident contacts, and any possible flat component. It does not
assume that optimizers are unique up to reflection, discard singletons, restrict
time to half a period, or stop after locating one witness.

The optimizer receives only the seven speeds. It uses no claimed formula,
residue branch, proposed time, ambient cell, orbit slice, peak data, or
opposing-contact enumeration. For each small q, it completes optimization and
the secondary reconstruction below **before** the claimed formula and times
are evaluated for comparison. Arithmetic throughout is Python
`fractions.Fraction`; no floating-point tolerance is used.

## Counterchecks and boundary handling

A separately structured check constructs each runner's closed safe intervals
at the independently computed maximum M:

`[(j+M)/v, (j+1-M)/v]`, `j=0,...,v-1`.

It intersects those interval unions directly. The result equals the complete
maximizing set from the lower envelope in all 24 cases. This check preserves
isolated equality times. It verifies the level set at M; the primary optimizer,
not the threshold check alone, supplies maximality.

Additional exact internal checks establish:

- each constructed affine runner segment agrees with direct distance-to-integer
  evaluation at both endpoints and the midpoint;
- every nonempty dominance piece agrees with direct evaluation of the complete
  physical minimum at its endpoints and midpoint;
- the domain endpoints 0 and 1 are included in the audit, with membership in
  the returned maximizing set checked explicitly;
- all returned isolated maxima have direct seven-runner distance records;
- three synthetic affine/interval controls preserve a flat optimal interval,
  an endpoint optimum with duplicate lines, and touching-interval unions.
  These are helper controls, not additional physical runner inputs.

The program returned exit status 0 on its first run. No failure was suppressed
or repaired by changing the stated q domain or expected formulas.

The aggregate counts below are sums of the per-case counts. In particular,
"distinct corners" means distinct within each q, then summed across q; it is
not a count of globally distinct rational times across the whole batch.

| Check or object | Count |
| --- | ---: |
| Exhaustively optimized physical cases | 24 |
| Tent-corner occurrences before deduplication | 10,272 |
| Distinct tent corners, summed per case | 9,712 |
| Base intervals / complete-envelope coverage checks | 9,688 |
| Evaluated dominance inequalities, with early empty-set exits | 211,578 |
| Nonempty dominance pieces | 17,826 |
| Singleton dominance pieces retained | 3,358 |
| Direct affine-segment distance checks | 203,448 |
| Direct full-objective checks on dominance pieces | 53,478 |
| Physical domain-endpoint checks | 48 |
| Direct checks on returned maximizing components | 144 |
| Closed threshold bands generated | 5,052 |
| Complete threshold-set comparisons | 24 |
| Isolated maximizing-time occurrences | 48 |
| Positive-length maximizing components | 0 |
| Seven-runner records at small-q maximizing times | 336 |
| Large-q witness cases / times / runner records | 6 / 12 / 84 |
| Discrepancies | 0 |

## Exact bounded results

The constant branch has maximum `1/6` and precisely the times `1/6,5/6` for
the following tested q values:

`3,4,7,9,10,13,15,16,19,21,22,25`.

The remaining twelve cases are:

| q | Exact maximum | All maximizing times in [0,1] |
| ---: | --- | --- |
| 2 | 2/13 | 3/13, 10/13 |
| 5 | 5/33 | 10/33, 23/33 |
| 6 | 4/25 | 9/25, 16/25 |
| 8 | 7/43 | 8/43, 35/43 |
| 11 | 11/69 | 22/69, 47/69 |
| 12 | 8/49 | 17/49, 32/49 |
| 14 | 12/73 | 13/73, 60/73 |
| 17 | 17/105 | 34/105, 71/105 |
| 18 | 12/73 | 25/73, 48/73 |
| 20 | 17/103 | 18/103, 85/103 |
| 23 | 23/141 | 46/141, 95/141 |
| 24 | 16/97 | 33/97, 64/97 |

The six large-q checks evaluated only the displayed physical witnesses and
their reflections. The saved output includes all laps, fractional phases,
distances, and limiting speeds for both times.

| q | q mod 6 | First supplied time | Directly achieved value |
| ---: | ---: | --- | --- |
| 100002 | 0 | 133337/400009 | 66668/400009 |
| 100003 | 1 | 1/6 | 1/6 |
| 100004 | 2 | 83338/500023 | 83337/500023 |
| 100005 | 3 | 1/6 | 1/6 |
| 100006 | 4 | 1/6 | 1/6 |
| 100007 | 5 | 200014/600045 | 100007/600045 |

Each reflected time has the same achieved value. These are direct lower-bound
witness checks, **not** computed large-q maxima or all-maximizer classifications.

## Reproduction and provenance

From the repository root:

```bash
python3 reviews/2026-09-29-cc-other-ray-review/physical_check.py > /tmp/cc-physical-check.json
cmp /tmp/cc-physical-check.json reviews/2026-09-29-cc-other-ray-review/physical_check.json
```

Only standard-library Python is needed. The output embeds the checker source's
SHA-256. At this review's run, it was
`dc4a50e829a90d535d97d77c57474455abbd78767ca302c164ba6494b273ef7a`.
The protocol identifies the frozen research head as
`12d08824ead7b772032ba240d0e858250fbd183c`; this review's filesystem checkout
did not expose `.git`, so this reviewer did not independently verify that Git
HEAD. The coordinator is responsible for the frozen-input/commit check.

Before authoring, the reviewer read `AGENTS.md`, `CLAIM_STATUS.md`,
`CONTRIBUTING.md`, the current README/HANDOFF prose, this review's protocol,
and the written upper-bound note. Thus the formula, the proposed two times,
and prose reports of earlier successful computations were known. This was
not blind discovery of the statement.

**No prior optimizer source, saved optimizer output, geometry implementation,
or geometry output was read before writing and running the checker. None was
read afterwards either.** The primary implementation and closed-band
countercheck were freshly authored in this review, and the program imports
none of the earlier mathematical code. Both new checks still share one AI
author, Python's rational arithmetic, and the same physical input definition.
Their distinct organization is useful protection against some implementation
errors, not external mathematical certification or complete epistemic
independence. Only `physical_check.py`, `physical_check.json`, and this report
were written by this reviewer; original proof inputs were not edited.

## Information retained, and limits

The physical-time model directly preserves the actual trajectory, integer
phases, every tent corner, closed endpoints, all ties, and the complete
maximizing set. No ambient-to-orbit transport is needed. The saved witness
records retain laps and individual distances rather than just the minimum.
Full nonoptimal envelope pieces are reproducible from the code but are not
all stored in the JSON; their coverage and direct-value check counts are.

This makes the method a useful bounded challenge to folded-coordinate transfer
and the two-time claim. Its work grows with the speed magnitudes. It supplies
neither a q-independent finite reduction nor the universal upper bound or
uniqueness proof for every q>=2. In particular, passing these 24 exhaustive
cases and six witness-only cases does not discharge the fixed-cell lemma or
replace the separate proof-logic and arithmetic reviews. The all-q result
remains a proof candidate at the evidence level specified by the coordinator.
