# Frozen one-pair selector schema, version 1

Fixed before computing the ordered campaign. Protocol SHA256:
`36ef24405de801a114e11325d30fe0b5f2d855e71441e5c4478047aa15b82d8e`.
Only supplied-core safe sets are reconstructed. Primary selection never reads
benchmark durations, full seven-speed allowed sets, or all-pair overlaps.
All fractions are reduced strings; speed pairs/lists are numerical ascending.

## Policy and semantic records

Top-level `schema_version`,`protocol_sha256`,`script_sha256`,`status`,
`cases`,`stopped_at_uncertified`,`unrun_case_ids`,`summary`.
Each case has `semantic`,`semantic_sha256`,`evaluation`,`cost`.
`semantic` contains:

- `id`,`core`,`extras`,`core_components` (closed pairs, including singletons),
  `selected_window`,`window_width`;
- `single_durations` rows `[speed,duration]`, `total_single_duration`,
  `excess`, `pair_ranking` rows `{pair,cap}` in frozen ranking order;
- `stage` (`singles_positive`,`cap_ceiling`,or`queried_pair`),
  `selected_pair` (null if not queried), `queried_overlap` (null if unqueried),
  `duration_lower_bound` (−E from singles if unqueried, O−E if queried),
  `one_pair_cap_class_failure`, `selected_query_failure`;
- `endpoint_fallback` (null if a duration bound succeeded),
  `outcome` (`positive_duration`,`endpoint_interval`,`endpoint_contact`,
  or`uncertified`). No other window, pair, or endpoint is tried.

Fallback has `time`,`distances` rows `[speed,distance]`, `valid`,
`failed_speeds`, `safe_laps`, `shared_safe_interval`, `shared_safe_width`,
`equality_controllers`. The last four are respectively empty list/null/null/
empty list if invalid. A valid fallback constructs exactly one closed safe
lap for each of the seven speeds, with rows `{speed,lap,interval}`.
Their intersection contains the tested endpoint. Equality controllers are
`[speed,direction]` where `right` means the endpoint enters safety rightward
(phase1/8) and `left` means it enters leftward (phase7/8).
The shared interval has positive width for endpoint_interval and zero width
for endpoint_contact. No additional witness time is selected or tested.

Hash `semantic` alone using sorted-key compact JSON plus one LF, UTF-8.
The verifier independently rebuilds semantic fields; evaluation/cost fields
are separate explanatory certificates, not hidden inputs to policy selection.

## Endpoint-primitive evaluation data

`evaluation.single_evaluations` has four rows with `speed`,`arguments`
([w*A,w*B]), `primitive_values` ([C(w*A),C(w*B)]), and `duration`.
C(z)=floor(z)/4+min(frac(z),1/8)+max(0,frac(z)−7/8).

`evaluation.overlap` is null without a query. Otherwise it contains `pair`,
`h`,`r`,`residual_range`, `m_range`, `candidate_strips`,`positive_cells`,
`phase_area`,`endpoint_correction`,`overlap`.
Canonical h minimizes (abs(b−h*a),h) over h=1,2; r=b−h*a.
For r!=0, m_min=floor(min(r*A,r*B)−(h+1)/8),
m_max=ceil(max(r*A,r*B)+(h+1)/8), inclusive. For r=0 only m=0 is used.
Each candidate strip has `m`,`breakpoints`, `positive_cell_count`.
Breakpoints are A,B and all strictly interior solutions of
r*t=m±(h+1)/8 or r*t=m±(h−1)/8, deduplicated and sorted.
The evaluator examines every consecutive breakpoint cell and retains it iff
ell(t)<u(t) throughout its open interior, with
ell=max(−1/8,(m−1/8−r*t)/h), u=min(1/8,(m+1/8−r*t)/h).
Constant endpoint wins an exact source tie; r=0 is handled without division.

Each positive cell has `m`,`interval`, `lower`,`upper`,`area`,
`endpoint_correction`,`overlap`. Each lower/upper record contains
`slope`,`intercept`,`source` (`constant` or `affine`), `frequency`,
`primitive_arguments` at the cell's two endpoints, `primitive_values`, `W`.
For endpoint f(t)=s*t+d, frequency=a−s is a or b/h and is strictly positive.
P(z)=frac(z)*(frac(z)−1)/2 and
W=[P((a−s)*B−d)−P((a−s)*A−d)]/(a−s).
Cell overlap=area+W(upper)−W(lower). These are duration formulas; endpoint
membership remains the separate strict-distance fallback calculation.

## Explicit cost counters

Each `cost` has `core_laps_by_speed` rows `[speed,count]`, `core_laps_total`,
`core_event_vertices` (distinct generated threshold endpoints plus0,1),
`core_components`, `core_intersection_iterations` (two-pointer comparisons
across the three sequential intersections, numerical core order),
`single_duration_evaluations`=4, `single_primitive_calls`=8, `pair_caps`=6,
`exact_overlap_queries`=0or1, `residual_strip_candidates`,
`residual_event_candidates` (four per candidate m when r!=0, zero when r=0;
counts before endpoint filtering/deduplication), `residual_cells_examined`,
`positive_strip_cells`, `overlap_W_calls`=2 per positive cell,
`overlap_P_calls`=4 per positive cell, `endpoint_tests`=0or1,
`endpoint_distance_evaluations`=7 per fallback, `safe_lap_constructions`=7
only for a valid fallback.

`single_primitive_operand_bits` and `overlap_primitive_operand_bits` separately
record `maximum_numerator_bits`,`maximum_denominator_bits` among the exact
C/P arguments actually evaluated; the overlap object is null with no P calls.
`reported_fraction_bits` records these maxima among all fraction strings in
semantic/evaluation data. These are reported operands, not a bound on every
transient arithmetic operation or a runtime-speedup claim.

Top-level summary has `processed_cases`,`outcome_counts` (all four outcome
keys), `cap_class_failures`,`selected_query_failures`,`exact_overlap_queries`,
`endpoint_tests`, and `positive_duration_certificates` (positive bounds plus
positive shared endpoint intervals). Unrun cases are not evaluated.
`--write` creates results; default/`--check` replays all authorized policy
steps and compares JSON without writing. No benchmark is an input dependency.
