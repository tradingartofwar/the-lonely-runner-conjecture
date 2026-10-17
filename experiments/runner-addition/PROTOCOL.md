# Frozen protocol v1

Date: October 17, 2026. Authorized bounded investigation on a separate branch.

## Questions and scope

For each of the three exposed pairs and thresholds 1/8 and 1/10:

1. What are all connected components of the eight-constraint core-safe set?
2. Which added speeds defeat the fixed widest component, and which alternatives
   repair each failure? Preserve isolated points and equality.
3. Does the widest component plus one other component suffice for every
   admissible positive integer r? If more are required, find the exact minimum
   among menus containing this leader, or report the budget-limited UNKNOWN.
4. How do those answers change at the actual ten-runner threshold?

The configurations and reference are defined in README.md and protocol.json.
Pairs and many finite instances have been exposed in earlier work: this is a
development/family-completion study, not a held-out statistical trial.

## Frozen construction and finite domain

Build each complete core using the unchanged `feasible_intervals` routine in
`lonely_runner/checker.py`. Order components by increasing left endpoint;
choose the widest, breaking ties by earliest left endpoint. A singleton counts
as one component; a disconnected union cannot be renamed one component.

For positive leader width w at threshold d, set R=ceil(2d/w). Its tail guarantee
is r>=R. For each pair use the same matched finite domain at both thresholds:
all integers 1<=r<max(R_1/8,R_1/10), excluding the eight core speeds. Each record
also marks its own necessary finite remainder r<R. No evaluation of added r
occurs during input preparation. Publish and read back the input/protocol commit.

If a core is empty or isolated-only, or any preparation cap is exceeded, stop
that preparation with an explicit status; do not invent a tail or enlarge scope.

## Evaluation and explanations

For each finite r, the primary method uses an exact ceiling formula for first
contact on every core component. It also computes the complete child-safe set
using the existing checker, recording per-component surviving pieces and
earliest witness phases/laps. Every rejected source has a first-band candidate
beyond its right endpoint; this is an exact source rejection, not nonexistence
unless the source list is complete.

Record leader-only, all-positive-components, and complete-core successes.
Find a minimum additional cover of the leader's finite misses by exact dynamic
programming over incidence bitmasks. Ties use lexicographically smallest sorted
component IDs. The leader certifies all larger r, so this is a complete reduction
for the leader-constrained menu. A full-core miss certifies no witness at that
specific threshold/input, contingent on verification; preserve it and continue
the independently specified other threshold. No claimed LRC counterexample is
inferred from failure at 1/8.

Tail implementation controls are the first admissible speeds at or above R,
R+1, 10^6+1, and 10^18+1 (advance past repeated core speeds; deduplicate). Check
one exact contact and all physical phases, without enumerating huge periods.
These controls test implementation; the proof of all-r coverage is the width
argument plus exhaustive finite remainder, not those few large examples.

## Verification

Write a separate verifier without importing primary study functions or the
checker. Reconstruct core and finite child sets by exact threshold-event
decomposition: membership is constant between threshold events, and each event
is checked separately. Compare complete unions and component contact witnesses.
Verify core endpoint/lap inequalities and all stored witness phases.

Verify minimum menu size independently by cardinality-ordered subset enumeration
over the finite incidence table, including lexicographic tie selection. Preserve
the distinction between finite minimality, all-r sufficiency, and mathematical
novelty. Use explicit checks rather than Python `assert` in the verifier.

Predeclared semantic controls: `(1,2)` at 1/3 has only {1/3,2/3}; at 2/5 has no
safe time; `[7/8,9/8]` at threshold 1/8 for added speed 1 has exact-width boundary
contacts. The last control tests the tail's open-unsafe/closed-safe convention.

Publish code and dependency SHA-256 hashes before running the study. Require
all hashes to match. Run primary evaluation once, separate verification, then
one deterministic primary replay in scratch and compare result bytes. Preserve
failures; do not silently repair frozen code/results and call it the same run.

## Budgets and stop rules

Per core: sum of speeds<=600, components<=600, R<=128. Per menu decision:
100,000 DP states and 2,000,000 transitions. Per independent minimum check:
1,000,000 combinations. Per command: 60 seconds; at most one replay.

A budget stop is UNKNOWN for the affected claim. An implementation/verification
disagreement stops claim promotion. No new pairs, threshold, parameter boxes,
all-reference checks, language construction, benchmark campaign, or external
application is added to this run. End after the two follow-ups plus the control
and matched-threshold comparison. A further study needs a stated question earned
by these outcomes, such as a symbolic placement criterion or a demonstrated
representation limitation.

## Representation record

Retained: complete rational core components, closed boundaries, common physical
time, exact speeds, lap/phase recovery, added-speed identities and full finite
child sets. Omitted by a menu: other core components; the frozen full core is its
recovery source. A menu supports one witness, not every safe time or the optimum.
Costs: report core construction size, contact queries, set-cover work and verifier
work separately. Component count is a declared model cost, not a lower bound for
all possible algorithms. No formal proof checker or independent human audit is
performed. Same-author alternate algorithms check implementation, not novelty.
