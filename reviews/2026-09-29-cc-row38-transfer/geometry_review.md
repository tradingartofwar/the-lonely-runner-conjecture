# Separate geometry and coverage review — September 29, 2026

**Result: PASS.** The reviewer reconstructed the frozen seventh-row `(3,8)`
experiment using standard-library exact rational arithmetic and no production
imports. All **5,339 scalar fields** of the reached production geometry and
coverage certificate agree, excluding its provenance wrapper. This is a
separately implemented AI review, not blind, external human or formal review.
The reviewer read the prior implementation to establish the frozen interface;
results and findings were shared with the coordinator after the protocol froze.

## Method and scope

The review first checked the pinned protocol and all eight input hashes. For
each of the 24 parent floor edges, it enumerated only seventh laps 1 through 8,
then intersected the segment parameter with all fourteen labelled inequalities
and every stored parent halfspace. This reconstructs the full seven-row safety
condition rather than importing the production clipping function. Every output
endpoint was checked against all seven bands and all stored parent halfspaces.

For each candidate and each reached residual pair, the review enumerated the
integers in the exact projected interval, interpolated the first contact, and
rebuilt ranking, the strict exception rectangle, primitive residual domain,
complete contact matrix and all greedy gains. Numerical provenance order is
retained for both ranking ties and greedy ties. The comparison covers the full
candidate records, not only endpoints or final selected identities.

The exact outcomes are:

| Item | Result |
| --- | --- |
| Floor edges | 24 |
| Actual edge/lap attempts and candidates | 38 each |
| Singleton candidates | 5 |
| Descending candidates | 22 |
| Leader rectangle | 7 by 7 = 49 pairs, below the unchanged 400 budget |
| Primitive residual pairs | 17 |
| Candidate/residual contacts | 646 |
| Endpoint band checks | 532 |
| Endpoint parent-halfspace checks | 1,064 |
| Reconstructed and compared certificate fields | 5,339 |
| Final status | `COMPLETE_COVER_CERTIFICATE` |

No other changed row, new control pair, alternative leader or retuned rule was
tried. The old archived-row regressions belong to the coordinator record.

## Conditional infinite argument

The chosen leader is `P5:E0-3:K7`, with endpoints
`(1/4,7/8)` and `(3/8,3/4)`. Its integral-orbit projection is

\[
H=Qx-Py\in\left[\frac{2Q-7P}{8},\frac{3Q-6P}{8}\right],
\]

which has width `(P+Q)/8`. Every closed real interval of length at least one
contains an integer, so this segment covers every positive primitive direction
with `P+Q>=8`. The remaining positive primitive directions satisfy `P+Q<8`;
they form precisely the 17 retained residual pairs. The strict individual
bounds `P<=7,Q<=7` are a valid enclosing rectangle, and the exact width filter
removes its unnecessary pairs before building the matrix. Thus the finite
matrix addresses the entire complement required by the infinite argument.

The leader misses exactly `(1,1),(1,4),(2,1)`. The next chosen record,
`P2:E0-1:K2`, has endpoints `(7/24,1/4)` and `(55/168,1/7)` and covers the latter
two. The last chosen record, `P0:E0-1:K1`, is the vertical segment from
`(1/8,1/8)` to `(1/8,3/16)` and covers the remaining auxiliary `(1,1)`.
The complete residual matrix and greedy steps are reproduced in
`geometry_review.json`.

Leader eligibility and fallback eligibility are different: the leader needs
strict positive horizontal and descending vertical widths to obtain a finite
complement; a fallback only needs an actual integral contact. Vertical segments
and singleton records may therefore be valid fallbacks. All five singletons
are retained and checked in the matrix. Their closed endpoints are not discarded.

The emitted three-record menu stays intact. Its third record is needed only
for the deliberately retained repeated-speed auxiliary. For the intended
eight-distinct-speed domain `p!=q`, the first two records already suffice as a
deduction from this same output, without rerunning or altering the compiler.

Actual integer orbit contact supplies a physical time only with the pinned
primitive normalization and recovery map. The separate physical review checks
that step; ambient endpoint safety alone is not a physical certificate.

## Diagnosis and model adequacy

No uncovered primitive pair remains, so the richer-parent diagnostic is
`NOT_TRIGGERED`. Nothing in this run establishes insufficiency of the supplied
edge class. The earlier L/C selector's failure was repaired by selecting other
retained edge geometry. The present compressed carrier is adequate for this
one-witness construction, with closed bands, shared labels, provenance and
physical recovery attached. It does not carry optimal times, the complete safe
set or universal portability to all other coefficient rows.

This review supports the conditional universal construction argument as an
internally reviewed proof candidate. It adds neither a priority claim nor new
general eight-runner existence coverage.

## Reproduction and execution record

From the repository root, after the coordinator certificate is present:

```sh
python3 reviews/2026-09-29-cc-row38-transfer/geometry_review.py > /tmp/cc-row38-geometry.json
cmp /tmp/cc-row38-geometry.json reviews/2026-09-29-cc-row38-transfer/geometry_review.json
```

The first independent reconstruction ran after the protocol freeze and before
the coordinator output was available. It already returned the final counts,
leader, menu and empty uncovered set. Once the production certificate appeared,
the first full comparison passed without a mathematical or algorithmic fix.
At the coordinator's request, the review harness was then changed from writing
its own JSON and printing a short summary to printing the entire deterministic
JSON report. This output-only change enables capture and byte comparison;
the final script hash is recorded in the JSON. No candidate, interval, ranking,
contact, selection or comparison rule changed.
