# Adversarial review: shared pair-occurrence containment

September 28, 2026 UTC. Baseline
`d578e9f75b73d841c58577c435dfbbcf763f09e4`. Frozen protocol SHA-256
`52cdd98452f9e47c082bb53703b1a20dc07fa9e47860bc7bbf0e2eb1d00378f3`.
Scope is exactly the selected target pair, the fixed strict16 and tight13
comparison pairs, all six doubling112 diagnostic pairs, and the target
reflection. This is AI-assisted internal review, not independent human
mathematical validation. This reviewer edits only this report.

## Logical content and direction

Write

`B_v={t in J: ||vt||<1/8}` and `Safe_v=J\B_v`.

Equality is safe. Therefore

`B_a intersect B_b subset Safe_c intersect Safe_d`

has the correct direction and implies both
`B_a intersect B_b intersect B_c=empty` and
`B_a intersect B_b intersect B_d=empty`. The corresponding inclusive
triple moments are zero; here “inclusive” means that a triple moment includes
the four-way state, not that threshold endpoints count as blocking.

Conversely, for these finite unions of relatively open strict-blocking
intervals, zero duration of either triple implies that its strict triple set
is empty. A nonempty relatively open triple set would have positive length,
including when it meets a window endpoint. Thus, in the present runner
setting, the shared containment is logically exactly the conjunction of the
two zero-triple occurrence statements.

This is a consequential limit on interpretation. The displayed containment
is one compound certificate, but every base-pair component still needs two
separate complement checks. It shares the construction of `B_a intersect
B_b`; it does not turn two mathematical predicates or two zero bits into one.
Calling it “one query” is justified only under an explicitly defined oracle
that returns the compound answer.

The pair is also an input, not an output. On the target it was selected by
the prior coordinate-subset study after the four physical triples were known.
This experiment can validate and compress the verification of that frozen
pair. It does not discover the pair from raw speeds, total/single/pair
moments, or a generally applicable speed rule. Cheap pair selection remains
open.

## Endpoint and phase semantics

Strict blocking makes ordinary blocker boundaries safe. A pair component may
therefore have excluded threshold endpoints, while a window endpoint belongs
to the pair when both base runners block there strictly. The implementation
must retain these membership flags if it presents a point as a counterexample.
A complement that blocks strictly at an excluded component endpoint still
forces a nearby interior violation by continuity, but the endpoint itself is
not a pointwise witness to the pair premise. A rational interior point or
violating subinterval removes the ambiguity.

Testing the complement phases on the closure of each component is a valid
sufficient test and, by continuity and closedness of the safe set, does not
lose a true containment. If an unwrapped phase crosses an integer, the common
lap must be changed before comparing it with `[1/8,7/8]`. Checking only the
two circular endpoint distances without a common-lap or partition condition
is invalid; the earlier fixed-containment work already preserves a concrete
failure of that shortcut.

An independent exact precheck gives the following acceptance values:

| Case | Base-pair component and laps | Complement phase ranges |
| --- | --- | --- |
| target | `(63/304,5/24)`, laps `(3,8)` | speed 61: `[195/304,17/24]`; speed 100: `[55/76,5/6]` |
| strict16 | `(31/88,17/48)`, laps `(2,4)` | speed 7: `[41/88,23/48]`; speed 16: `[7/11,2/3]` |
| tight13 | `(31/88,17/48)`, laps `(2,4)` | speed 7: `[41/88,23/48]`; speed 13: `[51/88,29/48]` |
| reflected target | `(19/24,241/304)`, laps `(12,30)` | speed 61: `[7/24,109/304]`; speed 100: `[1/6,21/76]` |

All displayed complement ranges lie in `[1/8,7/8]`. The reflection values
are forced by `t -> 1-t`; they are a symmetry check, not another selected
configuration or independent example.

## Prior-work boundary

The certificate form is prior project work. The four-blocker study already
reconstructed every `56/113` pair-overlap piece and proved speed 64 safe on
each by exact phase ranges. The uniform-triangle continuation replaced that
finite reconstruction with an algebraic family argument. The strict16 note
already records the single `6/11` component and speed-16 phase range. The
fixed-window containment study already requires a common lifted lap and
retains threshold endpoint contacts. No novelty claim for pair-occurrence
phase containment is supportable here.

The sparse selector is related but not identical. It uses two different fixed
overlap regions and two arithmetic occurrence tests to choose a maximum-weight
graph in a special family. The two-speed transfer converts analogous tests to
two-dimensional lap-lattice questions and dispatches between two windows.
Those selection and alternate-window results are prior. The present target
has one preselected pair and no graph, pair, or window selection.

The subsequent arithmetic is also prior. Once the two zero triples are
available, the lower bound

`U >= C_0-O_cd-T_abc-T_abd`

is the existing five-edge `K_4`-minus-one-edge correction. The bounded
increment can only be the exact application to this target and the measured
reuse of one base-pair decomposition.

## Cost-accounting requirements

A fair ledger must keep three comparisons separate:

1. two naive, uncached triple reconstructions that each rebuild the base pair;
2. two zero-triple checks with competent caching/common-subexpression
   elimination of the base-pair components;
3. the old sparse arithmetic compatibility tests, which answer a related
   occurrence question without constructing the same interval data.

Only comparison 1 necessarily duplicates the base-pair work. Against
comparison 2, the shared certificate is chiefly a packaging and traversal
choice: it still performs two phase predicates on every component. Therefore
an observed factor-of-two saving against an uncached implementation is not an
intrinsic information or complexity theorem.

The ledger must also state whether it counts generated blocker pieces or
pieces merely read from an archive; candidate pair intersections or only
positive components; comparison primitives or higher-level range tests;
cached schedules per case or fresh work per diagnostic pair; and all
doubling112 witnesses or first-failure short-circuiting. Exact rational
operation counts are implementation counts. No uniform bound in the speeds
follows from four finite controls.

## Required controls

Strict16 should reproduce old facts: the `6/11` pair is automatically safe
from 7 because 6 and 7 do not overlap, and its safety from 16 is the archived
triple exclusion. Tight13 must show that the same shared containment can hold
while positive lonely duration fails; `t=3/8` remains a separate valid
isolated equality point. Therefore the containment alone is not a positive
certificate until the known five-edge arithmetic is evaluated.

Doubling112 already exits through a positive pair-only bound and must not be
used to select a post-result base pair. All four of its physical inclusive
triple durations are positive, so every one of the six possible base-pair
containments must fail. One explicit interior violating point or interval per
pair is enough to falsify the conjunction; retaining both complement failures
is stronger but not required by the protocol.

## Completed artifact review

Reviewed `primary.py`, `results.json`, `verify.py`, `verification.json`, and
`verification.md`. The final read-only commands pass:

```bash
python -S -B reviews/2026-09-28-shared-pair-containment/primary.py --check
python -S -B reviews/2026-09-28-shared-pair-containment/verify.py --check
```

The final primary SHA-256 is
`81992c0c9a38c5b5cedea1146dd1a5bea087c950228d10dc795839a7ab319c7d`,
and the primary results SHA-256 is
`478b6caf2c654af7eef83c1d6f2388933d737df6a78ab0f306b801053fe2ff5b`.
The separately authored verifier SHA-256 is
`7912f4432a3a8312a0131ba231488c0e135788d9472ba412b33c695c77b2a87d`.

The primary uses direct lap-labelled interval joins and unwrapped phase
ranges. The verifier imports none of its functions. It reconstructs complete
threshold-event state partitions, checks three exact probes per open cell and
every event point, and only afterward compares mathematical output with the
primary. A schema mismatch found during hostile review initially skipped the
selected-case comparison and could not read the doubling attempts; it was
fixed before the final artifacts. The final comparison checks all three
selected containments, bounds, components, laps, endpoint membership, and
cost-relevant counts, plus all six doubling failures and witnesses.

The four original windows contain 91 open cells and 95 event points. The
reflection adds 17 cells and 18 event points. Independently reconstructed
atoms, moments, blocker pieces, and the historical control laps match the
pinned archives.

During review, a semantic-review subagent accidentally invoked the primary
writer once instead of its read-only check. The primary owner subsequently
inspected and regenerated `results.json` from the finalized primary source.
The hashes above and both final read-only checks postdate that incident. The
accidental run is not counted as independent evidence.

## Exact finite findings

The acceptance values in the endpoint table above match both implementations.
The target has one base-pair component, and both 61 and 100 are safe on its
closure. It therefore certifies the two distinct upper bounds
`T_(15,38,61)<=0` and `T_(15,38,100)<=0`. Substitution into the prior
five-edge inequality gives

`U >= 49/524400 > 0`.

This rules out every abstract complete-cover arrangement satisfying the
archived total/single/pair moments and these two exclusions. That implication
comes from the prior exact dual/five-edge inequality; the geometric work here
explains why the two selected exclusions hold simultaneously in the actual
runner configuration.

The controls behave as required:

| Case | Containment | Raw five-edge bound | Interpretation |
| --- | --- | ---: | --- |
| target | holds | `49/524400` | positive duration certified |
| strict16 | holds | `1/896` | old positive repair reproduced |
| tight13 | holds | `-1/182` | no duration repair; isolated `3/8` remains |
| doubling112 | all six pairs fail | not applied | positive pair-only route already exits |

Every doubling112 failure includes an exact positive open cell, midpoint,
violating complement runner, and base laps. This is stronger than an excluded
endpoint report. All four physical triple durations are positive, and the six
failed pair containments agree with that independent archived fact. No pair is
selected after seeing these failures.

The reflected target has the exact reversed cell sequence and equal moments.
The original selected pair is merely transported by common-start integer-speed
symmetry. It contributes a consistency check, not a second success count or a
second selection experiment.

## Cost result and its limit

For the target, the shared implementation enumerates three base-runner
blocking pieces, performs two pair-join steps, finds one positive component,
performs two complement phase-range checks, needs no internal threshold
partition, and records 95 charged exact rational comparisons. Its two
explicitly naive triple comparators enumerate 13 blocker pieces, rebuild the
base pair twice, and record 188 comparisons. Strict16 gives 92 versus 139;
tight13 gives 92 versus 129.

Those ratios are implementation observations, not intrinsic savings. The
naive comparator both duplicates the base schedule and constructs each
complement runner's complete blocking schedule, while the shared method uses
phase ranges only on the already-found pair component. A cached pair of
zero-triple tests can reuse the same base decomposition and still must perform
the same two complement predicates. Relative to that competent baseline, the
new result is shared preprocessing and a compact presentation, not logical
compression. The archive now states one cached pair-occurrence table, two
complement predicates, no one-bit claim, no pair selection, and no runtime
claim.

The old sparse comparison remains separate: on its two applicable controls it
uses four multiplications, six additions/subtractions, two floors, and two
strict comparisons for its two archived arithmetic occurrence tests. That
special-family rule also selects a graph; the present target procedure does
not. Comparing these counts directly would mix different inputs and outputs.

The six doubling diagnostics total 2,322 primary comparisons, 93 enumerated
base pieces, 23 pair components, 66 complement range checks, and ten internal
partitions. This is a full audit with each base schedule rebuilt for each of
six pairs, not an optimized cached all-pairs implementation and not a
first-violation short circuit. Each of the four schedules is therefore rebuilt
three times. The verifier instead reconstructs the case once and applies all
six predicates; its operation total is deliberately not equated with the
primary ledger.

## Verdict

No fatal arithmetic, endpoint, containment-direction, reflection, control, or
finite-scope defect remains in the final artifacts. The accepted bounded claim
is:

> On the frozen target window, the supplied `15/38` pair has one occurrence
> component, throughout which both 61 and 100 are safe. This one cached
> occurrence table verifies two distinct zero-triple predicates; together
> with the already-known five-edge correction they certify uncovered duration
> at least `49/524400`.

What genuinely advances target understanding is the concrete shared-clock
explanation of the previously selected two-coordinate repair and its exact
finite work record. It replaces no selection theorem and adds no new existence
coverage. The certificate form, strict16 mechanism, graph inequality, sparse
tests, and alternate-window dispatch are prior work. General pair selection,
uniform cost in growing speeds, and novelty remain open; internal AI agreement
is not independent mathematical validation.
