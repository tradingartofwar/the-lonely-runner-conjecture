# Primary calculation schema (version 1)

This file fixes serialization before the primary calculation. Scope and selection
come only from `protocol.json`, SHA256
`578ad79f2d65ffe7309e3b1ae576de98e24ccaab1c23d3ea2600cedb5a9636a2`.
All runner indices are original zero-based indices into the eight velocities;
reference 0 is omitted from core and residual lists. Cores are the 35 numerical
lexicographic triples from 1 through 7. Their complete closed components are
ordered by increasing numerical `(left,right)`; singleton components are kept.
All rational numbers are reduced `str(Fraction(...))`, including `"0"` and `"1"`.

## Canonical component digest

For each component append the following JSON array, serialized with
`json.dumps(row,separators=(',',':'))`, then exactly one LF, encoded as UTF-8,
to that core's SHA256 stream:

```
[left,right,reduced_optimal_bound,actual_duration,
 vanished_original_indices,
 all_nonreflexive_containment_edges_original_indices,
 retained_original_indices]
```

Every list of indices is increasing; directed edges `[i,j]` are lexicographic
and mean the strict blocker of i on this CLOSED window is a subset of that of
j, including empty-set containments. Both directions appear for equal sets.
Point membership, including threshold contacts and singleton windows, is part
of the map. Retained indices are the smallest original index from each
inclusion-maximal nonempty equality class. No time sampling is used.

Full and reduced optimal bounds are computed separately and compared on every
component; their equality and slack identities are reported as mismatch counts
(which must be zero). The independent verifier should reproduce the digest,
all counts and extrema, selected Q certificate, and full allowed components.

## Tree and selection conventions

An edge is the increasing pair of original runner indices. Every spanning tree
is represented by its lexicographically sorted list of edges. Among equally
weighted optimal trees, the primary code selects the lexicographically smallest
edge list. For zero or one vertex the tree edge list is empty. The full tree
has all four residual vertices, including vanished ones. Bounds are not clipped
at zero. Q considers only positive-length components and sorts by greatest
reduced bound, fewest retained blockers, greatest width, lexicographically
smallest numerical core tuple, earliest left endpoint. Actual allowed duration
is not a selection input. `selected_certificate` always reports this Q winner;
`selection_outcome` is positive_tree, endpoint_fallback, or inconclusive.

## JSON structure

Top-level `results.json` has `schema_version`, `status`, `protocol_sha256`,
`script_sha256`, `core_order`, `cases` (in protocol order), and `totals`.
Each case has `id`, `velocities`, `reference_index`, `integer_denominator`,
`full_allowed_components`, `full_allowed_duration`,
`full_positive_component_count`, `full_isolated_points`, `global_witness`,
`time_one_eighth_distances`, `summary`, `cores`, `selected_certificate`,
`selection_outcome`, `endpoint_fallback`, and `strict_all_core_failure`.
`global_witness` and selected witness objects have `time`, `distances`
(in original index order 1..7), and `kind` (strict or equality).
Full allowed components are closed endpoint pairs; isolated points also appear
in that component list. Witness is null only when no allowed point exists.

Each per-core entry has `core`, `residual`, `component_sha256`, `summary`, and
`q_best` (null only if no positive-length component). `q_best` contains
`component_index` (zero-based), `window`, `bound`, `actual_duration`,
`retained`, `tree_slack`, and `tree_edges`. The summary fields are:

- `components`, `singleton_components`, `positive_bound_components`,
  `positive_actual_components`, `positive_actual_tree_misses`;
- `positive_bound_without_reduction`, `positive_bound_without_nonempty_containment`,
  `windows_with_vanished`, `windows_with_nonempty_proper_containment`,
  `windows_with_equal_nonempty`, `windows_with_reduction`;
- `retained_count_histogram` (five counts indexed 0..4),
  `vanished_count_histogram` (five counts indexed 0..4);
- `full_reduced_bound_mismatches`, `allowed_set_reduction_mismatches`,
  `slack_identity_mismatches` (all computed and required to be zero);
- `exact_tree_components`, `positive_slack_components`,
  `sum_tree_slack`, `maximum_tree_slack`, `minimum_bound`, `maximum_bound`.

Case `summary` sums counts and histograms across 35 cores, sums slack, takes
global extrema, and adds `positive_cores` (cores with positive bounds).
Top-level totals sum case counts and histograms, sum slack, take extrema,
and sum `positive_cores`.

The selected certificate adds `core`, `residual`, `core_speeds`,
`residual_speeds`, `full_bound`, `full_tree_edges`, `vanished`,
`containment_edges`, `proper_nonempty_containment_edges`,
`equal_nonempty_classes`, `retained`, `removed_cover`,
`strict_blocker_components`, `single_durations`, `pair_durations`,
`intersection_durations`, `active_state_durations`,
`slack_by_active_components`, `allowed_components`, and `witness` to the
`q_best` fields. Moment lists use original runner indices:
`single_durations` rows `[i,duration]`, `pair_durations` rows `[i,j,duration]`,
`intersection_durations` and `active_state_durations` rows
`[sorted_active_indices,duration]` for all 16 subsets, ordered by increasing
bit mask in residual order. Intersection of no sets has window duration.
`slack_by_active_components` rows `[induced_component_count,duration]`
include zero mass rows for counts 0..4, for the full selected optimal tree;
the slack is sum of `max(count-1,0)*duration`.
Strict blocker components are `[i,[[left,right,left_closed,right_closed],...]]`.
`removed_cover` gives each removed nonempty index and its lowest retained
container. `equal_nonempty_classes` includes classes of size at least two.
Selected allowed components are closed pairs, preserving isolated points.
`endpoint_fallback` is null when Q has positive bound; otherwise it contains
`tested_count`, `candidate_count`, and `witness` (first valid sorted endpoint,
or null); tests stop at the first valid endpoint.

`--write` creates results; default or `--check` recomputes everything and
compares loaded JSON without modifying files. Script SHA256 pins implementation;
only the protocol hash and this schema are needed by an independent algorithm.

## Postcalculation diagnostic

After the initial six-case calculation, the coordinator requested an additional
summary of the already calculated cores containing the maximum absolute speed.
This does not alter scope, Q selection, or any component digest. Each case's
`fastest_core_diagnostic` has `fastest_runner_index`, `cores`, `components`,
`exact_components`, `nonexact_components`, and `maximum_slack`, derived from
those per-core summaries. The proposed explanation (under separate review) is
that a core containing the fastest speed restricts every remaining blocker to
one interval or the empty set on each complete core-safe component.
