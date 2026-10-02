# Bounded missed-class diagnostic schema, version 1

Written before diagnostic computation. Protocol SHA256:
`0932c23c6c65dd8faaae4d319770ae0bca583237c0f92fee9c5ae7f8ce474f02`.
Primary output: `diagnostics.json`; primary implementation: `diagnose.py`.
The independent verifier must not import or inspect the implementation.

## Selection and scope

Read the failed residue classes from `classification.json`. Order them by
increasing residue in 0..119. For each, select the least positive V in that
class outside `{1,4,5,6,7,11}`. Check this minimality arithmetically; do not
select using any allowed set or phase projection. If more than six classes
fail, set `diagnostics_performed=false`, `stop_reason` to
`more_than_six_failed_classes`, and leave `cases` empty. No speed diagnostics
are then performed. With at most six failures, `stop_reason` is null and
`cases` follows increasing residue order.

The diagnostic conclusions concern only these representatives, not every V
in their residue classes. The chosen shifted speed is 11. The unchanged
speeds are `[1,4,5,6,7,V]`; original positive-speed order for common-start
witnesses is `[1,4,5,6,7,11,V]`. Reference 0, n=8, threshold 1/8, time [0,1].
No full phase multiplicity or duration profile is computed.

## Rational, time, and circle conventions

Every rational is the reduced `str(Fraction(...))`, including `"0"` and
`"1"`. All time components are closed endpoint pairs `[left,right]`, sorted
by increasing endpoints and merged when they overlap or touch. Singleton
components are retained.

Phase sets use maximal connected pieces in the cut interval [0,1), encoded
as `[left,right,left_closed,right_closed]`. Phase 1 is identified with phase
0 and is never stored as a singleton. A component ending at 1 has
`right_closed=false`; every other endpoint is closed. A wrapped circle arc
may have two pieces. Empty sets use an empty list.

The primary builds unchanged-safe A using intersections of each runner's
closed safe laps. P is the exact image of all A components under `11t mod1`.
B is the closure on the circle of images of only positive-length A
components. Thus isolated A times can contribute to P without contributing
to B. `extra_isolated_projection_points` lists, in increasing phase order,
the points in P absent from B; repeated images are counted once.

## Top-level structure

`schema_version`, `status`, `protocol_sha256`, `classification_sha256`,
`script_sha256`, `failed_residues`, `selected_representatives`,
`diagnostics_performed`, `stop_reason`, `cases`, and `totals`.

`selected_representatives` is a list of `{residue,V}` objects. The status
distinguishes exact bounded calculations from the supplied general covering
criteria. Hashes are SHA256 of the exact corresponding file bytes.

## Per-case structure

Each case contains:

- `residue`, `V`, `velocities`, `unchanged_speeds`;
- `A_components`, `A_duration`, `A_positive_component_count`,
  `A_isolated_times`;
- `P_components`, `B_components`, `extra_isolated_projection_points`;
- `P_metrics`, `B_metrics`;
- `all_phase_decisions`;
- `common_start_components`, `common_start_duration`,
  `common_start_positive_component_count`, `common_start_isolated_times`,
  `common_start_status`, `common_start_witness`;
- `case_sha256`.

Each metrics object has `nonempty`, `measure`, `maximum_circular_gap`,
`minimum_covering_arc_length`, and `maximal_gap_arcs`. Gap rows are
`[start_mod1,end_mod1,length]`, sorted by their numerical start. A full
circle has maximum gap 0 and no gap rows. A singleton has one gap of length
1 whose start and end both equal that point. For an empty set use measure
0, maximum gap 1, covering length 0, and no gap rows. For a nonempty set
the covering length is exactly one minus the maximum circular gap.

`all_phase_decisions` has:

- `nonempty_for_every_phase`: P nonempty and its minimum covering arc
  length is at least 1/4;
- `positive_duration_for_every_phase`: B nonempty and its minimum covering
  arc length is strictly greater than 1/4;
- `nonempty_covering_margin`: c(P)-1/4;
- `positive_duration_covering_margin`: c(B)-1/4;
- `criterion_status`: the fixed string
  `"supplied covering criteria; general proof-candidate status retained"`.

The distinction between `>=` and `>` retains equality contacts and prevents
positive-duration claims from isolated projected points. These are all-phase
decisions for the shifted-speed comparison. The following common-start data
use phase zero only.

`common_start_status` is `strict` if positive duration exists, `contacts` if
the set is nonempty with zero duration, and `empty` otherwise.
`common_start_witness` is null for an empty set. Otherwise, select the
midpoint of the longest positive component, breaking ties by the earliest
left endpoint. If there is no positive component, select the earliest
isolated time. Store `{time,kind,phases,distances,minimum_distance}` in
original positive-speed order. `kind` is `strict` or `equality`. Check all
seven distances directly; equality at 1/8 passes.

## Totals and digests

Totals sum `cases`, `A_components`, `A_positive_components`,
`A_isolated_times`, `common_start_components`,
`common_start_positive_components`, and `common_start_isolated_times`, and
count `all_phase_nonempty_cases`, `all_phase_positive_duration_cases`,
`common_start_strict_cases`, `common_start_contact_cases`, and
`common_start_empty_cases`. Every count is zero if diagnostics stop.

For `case_sha256`, omit that field, serialize the remaining case object with
sorted keys and compact separators, append one LF, encode UTF-8, then SHA256.

`python -B reviews/2026-09-27-time-templates/diagnose.py --write` creates the
archive. Default or `--check` recomputes and compares it without modifying
files. The implementation does not import project calculation code.
