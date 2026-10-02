# Independent review of the twelve-window cap-39 replay

September 28, 2026. Geometry agent's review of the coordinator's
`replay.py`, `replay_protocol.json`, and `replay_results.json`.

**Finding:** no defect found in the requested scope. This is an internal
AI source-and-artifact review, not external certification. The general
bound remains a **HYPOTHESIS / proof candidate**. The twelve recycled
diagnostics remain **OBSERVED**, with no new configuration or held-out claim.
The reviewer did not rerun the solver, oracle, or a parameter enumeration.

## Scope and provenance

The twelve case records, including speeds, core labels, windows, and auxiliary
classification, agree on inspection with the inherited
`lr-chain-termination/reviews/2026-09-28-chain-termination/protocol.json`.
The two giant-speed lift windows are preserved exactly.

File hashing confirms all three recorded identities:

- Frozen protocol:
  `563cefe2f0d36df46795a598e11a0c73dde1ff1e24e38b0481a9fb2d97b5ac5b`.
- Reviewed replay source:
  `13af61661dd5977f5a2d0ab57cf3d6fd196a201152d7c00eeec2c06717e73a4a`.
- Inherited threshold verification artifact:
  `e6a395db885bf8585dee3e2276391a1876f389a7b225f43176c6f980a4ab3295`.

The review also read the archived `verify.py`. That verifier computes safe
components by a complete local threshold partition, explicitly retaining
safe threshold points and testing every intervening cell. Its projection
uses fractional-part cases rather than the primary ceiling expression. It
checks its terminal verdict and time against the first threshold-derived
safe component. No primary solver or primary saved answer is imported there.

## Projection and stopping semantics

Write `v*t=k+r`, with `k` integer and `0<=r<1`.
For `r<=7/8`, `ceil(v*t-7/8)=k`; otherwise the ceiling is `k+1`.
Consequently `max(t,(meeting+1/8)/v)` advances precisely when `r<1/8`
or `r>7/8`. Both `r=1/8` and `r=7/8` remain stationary and safe.
The integer ceiling helper is valid also for negative rational arguments.

Each moving call records the correct open occurrence and asserts that its
input is strictly inside. Subsequent moving inputs equal the previous
moving right endpoint, because intervening stationary calls preserve time.
The asserted strict inclusion therefore certifies exactly the required
selected-chain adjacency. Early exit uses `t>R`, so equality `t=R` remains
eligible as a witness. Each projection preserves every possible later safe
time and cannot pass the earliest joint-safe time.

Initial joint safety is tested before starting a round, and joint safety is
tested at each completed-round boundary. Every round starting unsafe must
move: if it did not, its unchanged input would have been tested by all four
labels and therefore would be jointly safe. Hence the candidate 39-move
bound permits at most 39 unsafe-start rounds, or `39*11=429` calls. A further
all-stationary confirmation round is unnecessary with these explicit safety
checks. The loop rejects an unsafe 40th round; it does not silently return
a false answer on cap exhaustion. A clipped empty exit can occur partway
through the final started round.

## Geometric assertions and window criterion

For nonempty selected lists, the computed union endpoints are the minimum
selected left endpoint and the final selected right endpoint. Strictly
increasing right endpoints and the overlap assertions make this the actual
connected union. The exact check is its full length `< sum(1/v_i)`;
no first-interval overlap is lost through clipping to the supplied window.

Speeds are sorted, so runner zero has maximal period. `slow_count<=4` checks
the asserted occurrence count for that label. The `gaps` list correctly
includes each maximal contiguous chain segment on the remaining three
labels, including initial and terminal segments and empty segments.
`max(gaps)<=7` and `N<=8*slow_count+7` match the analytic reduction.

The width flag uses the sufficient condition `S<=R-L`, where `S=sum(1/v_i)`.
Including equality is mathematically correct. The averaging/strict-chain
argument supplies a residual-safe point within a closed interval of length
`S`; a projection from its left endpoint cannot overshoot it. Equivalently,
an initially unsafe start lies strictly inside the first selected occurrence,
so a completed chain of union length `<S` ends at distance `<S` from that
start. An initially safe start is returned immediately.

Each core certificate fixes the lap at `L` and verifies
`1/8<=vL-lap<=vR-lap<=7/8`. Linearity then certifies the entire closed core
window, including equality endpoints. This is sufficient for combining the
residual width guarantee with core safety. A false width flag makes no
negative feasibility claim.

**Coverage qualification:** no one of these twelve windows satisfies the
exact numerical equality `S=R-L`. The inclusive width comparison is reviewed
analytically; it is not an independently exercised equality fixture in this
replay. Equality witnesses at the supplied right boundary are retained by
`tight_13`, `aux_condition_equality`, and the extended lift. In particular,
the name `aux_condition_equality` must not be interpreted as a test of
`S=R-L`.

## Oracle comparison and observed results

The new solver constructs all twelve rows before reading the archived
verification artifact. It then compares the complete trace, earliest time,
final time, scalar-call count, move count, selected occurrences, and union
span, plus the verdict, for eight top-level comparisons per case and 96
overall. Nested trace and interval objects are compared in full; 96 is a
count of top-level comparisons, not a count of individual rational scalars.
The use of the archived independent oracle is a recycled check, not a newly
independent sample or a new implementation of the mathematical proof.

Inspection of the result rows confirms the stated totals: 12 windows,
199 scalar calls, 32 moves, maximum 7 moves, 11 earliest witnesses, and one
clipped empty window. The five width-guaranteed cases are `doubling_112`,
`small_gcd_113`, `affine_309`, `affine_310`, and `affine_320`.
The clipped lift still exits at call 23; the extended lift still reaches
the same seventh moving endpoint and finishes the prescribed full round at
call 33. No case approaches the proposed 39-move cap, so these data cannot
establish or stress-test that cap.

The review is adequate for this frozen replay. No additional execution,
fixture, scan, or code change was needed.
