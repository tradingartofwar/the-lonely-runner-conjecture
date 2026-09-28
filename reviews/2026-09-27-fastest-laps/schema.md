# Original common-start fastest-lap schema, version 1

Fixed before calculating the 29 lap records. Protocol SHA256:
`f1d4772133a47a3090c5f9f5f3aa6389b378917c0744a80e3df728790e397d7d`.
This primary archive contains ONLY the two common-start configurations.
All runner labels are original indices 1..7; fastest runner is 7.
Every rational is reduced `str(Fraction(...))`, including `"0"` and `"1"`.
Closed components are ordered numerical endpoint pairs, retaining singletons.
Strict interval encoding is `[left,right,left_closed,right_closed]`.

## Declared qualitative compression

Before inspecting outcomes, a lap's qualitative signature is fixed as
`[vanished_indices,left_order,nonreflexive_containment_edges]`.
`left_order` lists all nonempty blockers in increasing left endpoint order,
then decreasing right endpoint, then increasing original label.
Containment edges `[i,j]` mean the strict blocker of i is a subset of that of j
on the CLOSED lap; include empty-set containment and both directions of equality.
Edges are lexicographic. This summary deliberately discards exact lengths,
endpoint inclusion flags, gaps/touch distinctions, and cross-order comparisons
between one blocker's left endpoint and another's right endpoint.
Group all 29 laps by this exact signature (including runner labels), report
all groups and mark a collision only if statuses differ within a group.
No collision is presumed. Status is `covered` (no allowed points), `contacts`
(nonempty allowed set of duration zero), or `strict` (positive duration).

## Tree convention

All 1,296 labelled six-vertex spanning trees are enumerated independently of
the verifier's tree algorithm. Maximize sum of pair overlap durations; among
ties choose lexicographically smallest sorted original-label edge list.
The full six-vertex tree includes empty blockers. Bounds are not clipped.

## Archive and canonical digest

Top-level: `schema_version`, `status`, `protocol_sha256`, `script_sha256`,
`fixed_residual_speeds`, `fixed_safe_components`, `fixed_safe_duration`,
`cases`, `qualitative_groups`, `summary`.
Each case: `id`, `velocities`, `V`, `integer_denominator`, `laps`,
`lap_records_sha256`, `full_allowed_components`, `full_allowed_duration`,
`full_isolated_points`, `global_witness`, `summary`.
For each case, hash each complete lap record (the dictionaries below) in
increasing m order with `json.dumps(record,sort_keys=True,separators=(',',':'))`
plus exactly one LF, UTF-8. The record itself does not contain its hash.
The independent verifier can compare every field and then this digest.

Each lap record has:

- `m`, `window`, `width`, `residues` (rows `[index,v*m % V]`),
  `residue_lifts` (rows `[index,(v*m)//V]`).
- `blockers`: six records, original label order, each with `index`, `speed`,
  `collision_lap` (integer, null if empty), `interval` (strict encoding or
  null), `normalized_interval` (same flags with u=V*t-m, or null).
- `vanished`, `containment_edges`, `qualitative_signature` as above.
- `single_durations` rows `[index,duration]`; `pair_durations` rows
  `[i,j,duration]` in lexicographic pair order; `tree_edges`, `tree_weight`,
  `tree_bound`, `actual_duration`, `tree_slack`, `union_duration`.
- `allowed_components`, `isolated_points`, `status`, `witness`.
- `allowed_endpoint_controllers`: one row `[t,sorted_indices]` for every
  distinct allowed-component endpoint, ordered by t; index is included iff
  its direct circular distance at t equals 1/8, including fastest runner 7.
- `coverage_scan`: one record per nonempty blocker in `left_order`, with
  `index`, `junction` (`first`, `overlap`, `touch`, `gap`),
  `frontier_before` and `frontier_after` (null initially, otherwise
  `[right,right_closed]`), `advances` (strictly extends right coordinate),
  `touch_survives` (null except for touch, then directly tested boolean),
  `touch_controllers` (empty except for touch, then direct equality labels).
  Frontier is the greatest right endpoint seen so far; ties combine inclusion
  by OR. This describes the advancing right envelope even across gaps.
- `scan_initial_gap`, `scan_final_gap`: endpoint pairs only for a positive
  gap between W's boundary and the first/last blocker frontier, else null.
- `scan_touch_points`: rows `[t,survives,controllers]` for distinct touching
  frontier junctions in increasing t order.

`witness` and `global_witness` are null for covered sets; otherwise objects
with `time`, `distances` in original index order1..7, and `kind` (`strict` or
`equality`). Pick the midpoint of the first widest positive component,
or the earliest isolated point when no positive component exists.
Contacts are all explicitly present in `allowed_components`, including any
isolated points coexisting with positive components.

Case summaries have `laps`, `covered_laps`, `contact_only_laps`, `strict_laps`,
`positive_tree_laps`, `exact_tree_laps`, `isolated_point_count`,
`positive_component_count`, `touch_junction_count`, `surviving_touch_count`,
`maximum_tree_slack`. Top-level summary sums all count fields, takes the max
slack, and adds `qualitative_groups`, `qualitative_status_collision_groups`.
Each qualitative group record has `signature`, `members` (rows `[case_id,m]`
in protocol case/lap order), `statuses` (sorted distinct strings), and
`status_collision`.

`--write` creates the archive. Default/`--check` recomputes and compares loaded
JSON without writing. Scripts are self-contained and arithmetic is exact.

Serialization clarifications fixed before the run: first scan record has
`advances=true`; an empty scan has `scan_initial_gap=W` and
`scan_final_gap=null`. Summary touch counts count scan touch records, including
repeated junction coordinates, while `scan_touch_points` deduplicates them.
Residues/lifts contain only residual indices1..6. Qualitative groups are sorted
by compact JSON serialization of their signature (lexicographic string order).
