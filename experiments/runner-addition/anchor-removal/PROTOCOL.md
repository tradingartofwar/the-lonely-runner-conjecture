# Paired removal of the shared 1/10 anchor

October 17, 2026. Source: `8431549e6ed30729e9d208bb26e51bb5c9791042`.
Freeze config, code and manifest before any perturbed-core geometry or contacts.

## Question and deterministic pairing

Do at most two connected safe components still suffice, with the predetermined
widest component required, after each of the eight preceding cores loses its
safe time 1/10? Preserve exact minima of one, two, three or more, physical
no-cover outcomes, and unsupported/budget statuses. This tests the necessity
of that particular anchor on these perturbed cores, not all rational anchors
or a general two-component theorem.

Use the eight input lists in the pinned outside-template/config.json, in its
original order. For each list S, consider every replacement v -> m where
v belongs to S and m is a positive multiple of 10 at most max(S)+10. Require
m absent from S, gcd of the new eight distinct speeds one, and exclusion of
the earlier exact p,q template. Select the least tuple (abs(m-v),m,v).
This finite arithmetic rule chooses nearby perturbations without geometry.
Config records the chosen speeds and replacement; both implementations must
reconstruct the selection. If no eligible replacement exists, stop with an
input error; do not substitute a different rule or core.

All old speeds avoid multiples of 10, so the old core is safe at t=1/10.
The inserted speed has phase zero there, making the new core unsafe. Retain
seven speeds exactly; use the same common start, reference 0, n=10 after one
admissible positive integer r is added, d=1/10 and [0,1] clock.

The changed core may have different components, widest interval, admissible
added speeds and finite cutoff. This is a paired perturbation, not a clean
causal isolation of one feature. Component IDs are local to each core and
must not be identified across the pair. Former repair points may survive even
when 1/10 does not; check this rather than assume it.

## Inherited exact work

Reuse outside-template/run.py's family wrapper, exception-cover constructor,
full study.evaluate reference, dispatcher and all contact/tail rules unchanged.
Choose widest positive component, earliest start on ties. Let R=ceil(2d/width);
test every admissible 1<=r<R, then use the width tail for r>=R. Universal
implications remain same-author proof candidates awaiting independent review.
Compute the constructor and its optional shared-point query before the full
table. Optional common-point failure never invalidates separate witnesses.
Dispatch finite cases and the inherited large-speed controls, and test guards.

The alternate verifier reuses outside-template/verify.py's complete event-set,
subset-minimum, query-trace, witness and dispatcher audits without editing them.
Old baseline results and their PASS verification are pinned by hash and reused,
not rerun or counted as fresh validation. No changed rule is fitted to outcomes.

## Frozen paired diagnostics

For each successfully evaluated new core, record:

- Old/new minimum status and IDs, leader intervals, cutoffs and failure lists.
- The complete intersection of the two core safe sets, preserving singleton
  and closed endpoints, plus old/new/intersection measures. Verify the complete
  intersection separately as the event-safe set for the union of their speeds.
  Measure is only a descriptive statistic; zero measure is not nonexistence.
- The common finite added-speed domain. On that domain, list identical versus
  changed complete child sets. Retain the full source sets on both sides.
  Do not compare differently admissible queries as if they were matched.
- The previous optional repair time (when present), which new core speeds
  block it, and which new leader exceptions block it. No replacement point is
  searched by this diagnostic. No old optional point is NOT_APPLICABLE.
- Direct physical failure of 1/10 under the new core, and its absence from
  the complete new geometry. The old source must retain that time.

These diagnostics are specified before exposure and do not feed selection.
They preserve relationships that a menu-size summary would omit. The complete
union-speed diagnostic is an intersection question at fixed d=1/10, not an
additional runner-count claim about LRC. Additional audit cost: eight event
sets of the union-speed constraints, separate from the eight new core sets.

## Budgets and stopping

Keep inherited caps per new case: speed sum600, components600, cutoff256,
constructor contacts100000, DP states100000/transitions2000000, optional
probes20000, alternate subset combinations1000000. Primary, verifier and one
replay each have a 240s command cap. The full reference retains its inherited
one-operation DP cap overrun convention; constructor caps are strict.

Run exactly eight new cases once, alternate verification, one byte-identical
primary replay. Checkpoint every completed case; preserve any failed/unknown
outcome and stop on discrepancies. Do not tune inputs or silently fix frozen
code. Report unresolved scope if stopped. Do not rerun the old semantic controls.

Count core construction, unique contacts by stage, cache reuse, optional point
probes, DP instrumentation, dispatcher calls, full reference and extra paired
audit work. No runtime superiority follows from contact counts.

## Representation and evidence limits

Supported output: one witness per admissible added speed and the minimum
number of complete connected source components containing the fixed leader.
Different speeds may need different times. Preserve exact equality and original
source IDs; recover complete source sets for changed questions. No unrestricted
minimum, all-reference, optimum-distance or general LRC result is requested.
The prior model record and derivations remain applicable under these stated
assumptions. This uses ordinary interval, residue and finite-cover methods.
Both implementations share an AI author; verification is not independent human
review, formal proof certification, or a novelty claim.
