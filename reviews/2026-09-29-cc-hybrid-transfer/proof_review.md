# Separate proof review: hybrid transfer with an invalidated old witness

September 29 maintainer date / September 30, 2026 UTC. This is a separately
tasked internal AI proof/design review, not blind replication, external human
review or formal certification. The preliminary review was written before
target computation. No target search, coefficient scan or production import
was performed for it.

Frozen protocol SHA256, verified from disk:
`a9ad5edbf140ee15bffc2ad4cf2a47de5c9884c7875172cc33f3a2a37f077f3d`.
Input head: `e1fe57ac5521ab8147c4ceeee3bc5ecb0aad54ac`.
The target changes from (54,26) to (102,50); the 36 supplied source records,
threshold 1/8 and mathematical selection/recovery rule stay fixed.

## 1. What a data-only adaptation must preserve

The active target must be consistent across coefficient screening, point
phase tests, preflight lap ranges, full clipping, certificate rows and physical
recovery. In the pinned implementation, this requires changing:

- hybrid.TARGET and hybrid.ROWS;
- the captured target default in bounds;
- the captured target default in query, preserving its opened=False and
  prepared=None defaults;
- the physical module's ROWS and ADDED.

Python binds a default argument when the function is defined. Rebinding the
module's TARGET alone does not change bounds.__defaults__ or query.__defaults__.
An incomplete adapter could therefore screen the new row while checking
recovery contacts against the old row. Directly recording and checking the
active defaults is necessary, in addition to output validation.

The phase module's screen and full_clip receive the target explicitly; their
unused module-level old TARGET is not an active input to those calls. The
compiler receives the adapted rows explicitly. No old target may remain on
an active implicit-argument path. Unrelated old constants preserved in pinned
source files are provenance, not necessarily an adapter defect.

Before/after function-code hashes establish body identity, but do not by
themselves establish unchanged semantics: globals and defaults also affect
execution. The recorded allowed binding changes, unchanged function bodies
and complete old-target regression together support the claimed data-only
adaptation. Source order, H order, lap order, screen predicate, ranking,
rectangle/recovery/clipping caps and dispatch semantics must remain fixed.

The old-target regression is appropriately performed before binding the new
input. It reconstructs the complete old hybrid and full certificate plus
the declared24 dispatch records and four existing kernel fixtures. This
checks the adapter path, not a new physical target or an old timing rerun.
For the changed row, hybrid construction must precede the full baseline;
later comparison data must not choose a recovery source, lap or point.

## 2. Inherited mathematical obligations

The sufficient boundary screen remains valid whenever u-v=8k*c and the core
raw value is fixed at m_c+1/8 or m_c+7/8. The new raw value differs from
the safe v value by the integer8k*m_c+k or8k*m_c+7k, respectively. The
new lap changes by that same amount. Staying in the declared progression
preserves this possible mechanism; it does not establish that all needed
source segments satisfy the screen or that the screen alone covers all inputs.

For any fixed source Z(s), fixed positive primitive pair(P,Q), and appended
row u, both full clipping and contact-first recovery seek

    {s in[0,1]: Qx(s)-Py(s) is integral,
                u dot Z(s) belongs to a closed safe lap band}.

When H(s)=Qx(s)-Py(s) is nonconstant, every integer in its projected interval
determines one parameter; testing the unique floor lap is exhaustive. When
H is a constant integer, intersect all possible new-row bands with the
source. Constant noninteger H has no contact. This includes point sources
and closed equality endpoints. The earlier proof applies to the changed
row because its affine and integer hypotheses remain true; success on the
new row is still a matter for the frozen computation.

This equivalence is relative to the supplied source class, and requires
completed recovery search. A resource stop is not exhaustion, and a completed
source-class miss does not prove physical nonexistence. First witnesses may
differ because the two algorithms order intersections differently.

The screen leader's positive projection width supplies an infinite tail;
its completed residual table isolates every unresolved primitive direction.
Recovering every such direction yields a complete hybrid certificate using
the original screen menu and a primitive-direction point table. Recovered
points are not automatically reused as a new global segment menu.

If both screen and full compiler reach complete finite reductions, the union
of their residual domains contains every possible coverage difference.
Outside that union both safe leaders have projection width at least1 and
therefore an integer contact. Inside, compare full candidate-class contacts
with hybrid dispatch. This tests coverage, separately from equality of
chosen times. Missing finite-reduction prerequisites permit only a reached
bounded comparison, not a global claim.

The old full-baseline wrapper may report NO_DESCENDING_SEGMENT after the
full clipper returns no records because of a cap. The adapter must preserve
the original clipping scope status, rather than interpret the wrapper's
derived geometry status as mathematical candidate-class failure.

## 3. Physical domain and deliberate stress

The new row dominates every earlier moving row. The exact collision domain
therefore remains p!=q and p!=2q for ten distinct total speeds, with the two
excluded primitive directions retained as nine-distinct-speed auxiliaries.
The same Bezout/contact inverse map applies, provided physical recovery uses
the new coefficient rows and retained new lap.

The predeclared old-time failure at(5,1) is exact: the new speed is560, and
560*(9/40)=126. Its phase is0. It invalidates that old selected point for
the new row, not every safe physical time. If the failure record includes
reflection, phase0 stays0 and its reflected lap must be computed accordingly;
the safe-witness shortcut1-phase does not apply at zero.

This input was selected analytically to defeat an old recovery point while
remaining within u=(6,2)+8k*(2,1). Thus it is an informed prospective stress
transfer. It is not blind, unrelated held-out data or evidence for arbitrary
coefficient portability. A replacement contact, if found, would demonstrate
that recovery adapts to this deliberately invalidated earlier witness.

Open-source diagnostics delete original geometric endpoints and point
sources by convention. A singleton's mathematical relative interior is the
singleton itself; the diagnostic convention is a different operation. New
safe phase bands remain closed, and no diagnostic point changes the retained
closed selector. The inherited synthetic fixtures remain old regression
evidence, not new-row physical branch coverage.

## 4. Benchmark gating and evidence limits

Benchmarking only if both new methods emit complete certificates avoids
comparing different delivered guarantees. If either is incomplete or capped,
NOT_TRIGGERED with its exact reason is the appropriate timing result.
Even then, reached cost counts remain useful if stated with their scope.

If triggered, the unchanged warmup and11 alternating paired rounds provide
bounded implementation/environment evidence. They must retain source
validation, native trace construction, preflight work and failed recovery
tests within the measured construction. Discovery, imports, parsing, physical
controls, audits and serialization remain explicitly outside it. No rerun to
improve the result, new cap or added target is justified by an unfavorable
outcome. Timings are not complexity proofs or universal speed guarantees.

## Preliminary finding

PASS for the frozen data-adaptation obligations, inherited source-relative
completeness, finite coverage-comparison scope, physical-domain reasoning,
within-progression interpretation and benchmark gate. Reached target outcomes
and the final review remain to be appended after execution. General statements
retain the repository's internally reviewed proof-candidate status.

## 5. Final adapter and execution review

Read-only review of transfer.py, adapter.json, adapter_regression.json,
hybrid.json, full.json, audit.json, summary.json and timing.json supports the
declared adaptation. No imported production function body is changed. The
active target globals, row lists and both captured defaults agree. The
adapter records identical before/after source SHA256 maps for all 14 tracked
functions and asserts exact identity of their Python code objects.

The first run already asserted code-object identity but recorded one shared
source-hash map. During review, the coordinator augmented the adapter evidence
with separate before/after maps to satisfy the frozen wording literally.
Only adapter.json and its nested counterpart in adapter_regression.json were
regenerated by module binding. This is a recorded provenance-metadata
correction, not an algorithm correction or a new target or timing run.

The old-row adapter regression reports exact agreement on 3,658 hybrid scalar
fields, 20,791 full-certificate scalar fields, all 24 old physical records
(2,036 scalar fields), and the four inherited kernel fixtures. The new hybrid
construction precedes the new full baseline in the execution path. There is
no baseline-informed branch in recovery. Component scope statuses, including
the full clipping status, are retained separately.

Both new methods reach complete certificates. Full clipping uses 89 of the
256 permitted source/lap attempts; recovery's preflight bound is 48 under the
unchanged cap of 4,096. The reached target result requires no cap increase,
alternative leader, changed source order or broadened screen predicate.

## 6. Reached coverage and exact replacement

The five screened records are identical members of the 89-record full class.
The screen selects three segments, and its only uncovered primitive directions
are (1,2), (1,4) and (5,1). Both compilers select the leader
P2:E0-3:K2:L2:M44, with endpoints (33/104,25/104) and (3/8,1/8).
Along y=7/8-2x its projection is

    H(x) = (Q+2P)x - 7P/8,
    width = 3(Q+2P)/52.

For integral positive P,Q, width at least 1 follows exactly when Q+2P>=18.
Every potentially uncovered direction therefore satisfies Q+2P<=17. The
recorded completed finite reduction contains its 47 primitive pairs inside
the permitted 8-by-17 rectangle. This supplies the infinite-domain argument;
the physical controls alone would not do so.

All three recovered records have an integer H, retain all old lap labels,
and add a safe new-row lap at the same point:

| Primitive pair | Source | Point | H | New torus lap | Original edge parameter | Primitive physical time |
| --- | --- | --- | ---: | ---: | --- | --- |
| (1,2) | P0:E0-1:K1:L2 | (1/8,1/4) | 0 | 25 | 1 | 1/8 |
| (1,4) | P1:E0-1:K1:L4 | (1/8,1/2) | 0 | 37 | 1 | 1/8 |
| (5,1) | P0:E1-3:K1:L2 | (19/136,31/136) | -1 | 25 | 3/17 | 31/136 |

Their appended-row phases are respectively 1/4, 3/4 and 11/17. Their original
parameters lie in the corresponding full-clipped intervals [49/50,1],
[9/10,1] and [0,5/18], with equal complete label lists. Thus the full-membership
checks preserve the source map, not just an unlabelled geometric coincidence.

The (5,1) trace actually tests and rejects the old point (1/8,9/40) in
P0:E0-1:K1:L2: H=-1, local parameter 1/5, raw torus value 24 and phase zero.
It then continues in the frozen source order and accepts the later source
P0:E1-3:K1:L2 at local parameter 9/17, original parameter 3/17. There the
new torus raw value is 436/17=25+11/17. With Bezout coefficients (0,1),
the primitive physical time is y=31/136. Speed 560 then has raw value
2170/17=127+11/17. The failed physical raw value 126 and failed torus raw
value 24 must remain distinct, as must the accepted physical lap 127 and
torus lap 25. At input (10,2), gcd scaling gives time 31/272.

The replacement's nine phases are (19/136,31/136,25/68,69/136,11/17,7/8,
5/17,33/136,11/17), so the minimum circle distance is 1/8. The time 31/136
was already present in the previous full-menu evidence. This transfer tests
the fixed hybrid's ability to recover it after rejecting its own old point;
it does not establish a previously unknown physical time.

Both completed finite reductions have the same 47-direction residual domain.
Every comparison there finds a hybrid witness and a full-class contact, with
zero mismatches. Outside this union the safe leaders guarantee both contacts.
The recorded ALL_POSITIVE_PRIMITIVE_DIRECTIONS comparison therefore has its
required hypotheses. Scaling extends selected-reference coverage to positive
integer p,q; restricting to p!=q and p!=2q gives ten distinct speeds. The two
excluded primitive directions remain valid repeated-speed auxiliaries.

The retained hybrid is the original three-segment screen menu plus three
points dispatched only on their keyed primitive directions. It is not a
six-segment global menu, and it does not encode the complete physical safe
set or every maximizing time.

## 7. Diagnostics, costs and benchmark limits

All 24 frozen physical controls pass for both methods: 20 primary controls
and four repeated-speed auxiliaries. The audit also retains physical recovery
on all 47 comparison directions. These support the stored inverse maps and
labels; the general coverage conclusion uses the preceding finite reduction.

Open-original-source recovery succeeds for all three exceptions, using 29
source visits and eight H/phase tests. In particular, its (1,4) alternative
is (17/56,3/14) on P2:E0-1:K2:L2, rather than the retained endpoint witness.
The diagnostic deletes original geometric endpoints and singleton sources
under its declared convention, while keeping new-row phase bands closed.
It says neither that all safe phases are strict nor that all directions have
open-source witnesses. It does not replace the retained closed dispatch.
The zero-budget diagnostic correctly returns RECOVERY_SCOPE_LIMIT with the
48-work preflight requirement, not a geometric failure.

| Operation | New hybrid | New full baseline |
| --- | ---: | ---: |
| Supplied source records | 36 | 36 |
| Inherited endpoint/band validations | 576 | 576 |
| Materialized candidate records | 5 | 89 |
| Residual matrix entries | 235 | 4,183 |
| Selected screen/full segments | 3 | 5 |
| Recovery preflight projections / raw ranges | 108 / 108 | 0 / 0 |
| Recovery integer-H upper count / work bound | 17 / 48 | not used |
| Actual recovery source visits | 14 | 0 |
| Actual recovery H tests / phase tests | 4 / 4 | 0 / 0 |
| Actual recovery parallel-band tests | 0 | 0 |
| Full source/lap attempts | 0 | 89 |

The hybrid additionally performs 48 coefficient-pair tests and 36 boundary
checks; preflight includes every source/exception pair despite first-success
stopping during actual recovery. Four phase tests include the rejected old
contact. No target recovery reaches the constant-H branch. Its validity rests
on the inherited generic argument and old fixture regression, not new target
branch coverage. These operation types should not be combined into one
purportedly equivalent work count.

Both methods are complete, so the timing gate is satisfied. The recorded
one warmup per method and 11 alternating pairs give medians of 10.746899 ms
for hybrid and 53.053481 ms for full. The median of paired full/hybrid ratios
is 4.911922220540084; it is a separate statistic from the ratio of medians.
All 11 pairs favor hybrid. The unchanged construction timing includes source
validation, native traces, preflight and failed contacts, while excluding
source discovery, imports, parsing, audits, controls and serialization.
This supports an input/implementation/environment-specific advantage, not
asymptotic complexity, arbitrary-row superiority or an established trend in
speed ratios as coefficients grow. No additional timing run was performed
for this review.

## 8. Main-note review and CC interpretation

The draft notes/CC_HYBRID_TRANSFER_2026_09_29.md correctly distinguishes the
old witness's failure from physical nonexistence; source-class completeness
from the complete safe set; torus from physical laps; inherited witness data
from the new recovery operation; and observed timing from general complexity.
Any final reproduced-status sentence remains conditional on the coordinator's
actual deterministic reproduction, which is outside this proof review.

The source-relative contact-first argument survives a deliberately invalidated
retained point. The old compact point table alone does not transfer, while
its pinned source route plus the unchanged recovery operation does on this
input. The useful retained distinctions are failed contact, later source,
closed equality handling, local-to-original parameter map, all nine laps,
physical inverse, completed finite reduction and cost/scope status. Compressing
these into only a final time or a success count would erase the mechanism
being tested.

An off-progression study is a reasonable next proposal, not an executed test.
It should state whether it leaves just this tested progression or every
coefficient relation allowed by the screen. In the latter case absence of a
screen relation already implies an empty screen by definition; that is a
known mechanism limit rather than a surprising empirical failure. A missing
descending leader supplies no inherited finite residual reduction, so the
current hybrid cannot silently continue with a global guarantee. A future
frozen comparison may assess what the full supplied source class retains,
without automatically broadening the predicate or selecting another leader.
No off-progression target was selected or tested in this review.

## Final finding

PASS for the data-only adaptation, recorded rejection and replacement,
closed-source equivalence, complete reached finite reductions, keyed-point
dispatch, physical scope and cost interpretation. This proof review prompted
the disclosed adapter provenance augmentation. General mathematical
claims remain internally reviewed proof candidates. This review performed
no new target computation, coefficient enumeration or timing repetition.
