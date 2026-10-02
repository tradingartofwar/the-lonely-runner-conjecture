# Adaptive reflected pair: exact arithmetic schema v1

Frozen before generating diagnostics. Protocol SHA256:
`55d73b9e425f4ad8fa74441029cb88569f2091fcb3bdf3494c4cca656d92f7f7`.
Only the eight prescribed values13,16,32,56,88,112,120,56000000000000 are
substituted. No speed-dependent enumeration, phase grid or full safe-set
reconstruction is used. Fractions are reduced strings.
General branch implications remain HYPOTHESIS/proof candidates; diagnostics
are exact finite certificates, not a mechanical proof of an infinite domain.

## Branch and selection conventions

IDs are `nonmultiple8`, `multiple8_not56`, `multiple56`, in protocol order.
Unchanged distance/phase vectors use speeds [1,4,5,6,7,V], in that order.
The two times are [t,1-t]. Equalities and safe-lap rows identify runners by
speed, not by original index. `right` and `left` indicate the direction into
the current closed safe lap at a threshold endpoint.

For the full pair envelope, c is the common unchanged minimum and d is the
circular separation of the two speed11 phases. Exact minimum is min(c,d/2),
maximum is c; constancy is c<=d/2. Triangle inequality and its attained
midpoint equality prove these values. The diagnostic records the equality
phase of the raw speed11 pair as `raw_pair_minimizer_theta`.

For the directed-interval consequence, choose the candidate maximizing
**speed11's distance**, taking t on a tie. Do not choose by full margin: both
full margins can equal1/8 even when one selected-runner endpoint is unsuitable.
For8|V use R=1/(56V), move right from t or left from1-t. The candidate closed
intervals are [t,t+R] and [1-t-R,1-t]; at least the interval attached to the
chosen speed11 maximizer is allowed, with strict open interior. This is not
an assertion that both intervals are safe for every phase.

## Top-level structure

`schema_version`, `protocol_sha256`, `script_sha256`, `status`,
`unchanged_speed_order`, `symbolic_branches`, `directed_selection_rule`,
`diagnostics`, `diagnostics_sha256`, `summary`.
The symbolic records are concise formula dictionaries, with fields
`id`,`condition`,`time_formula`,`unchanged_phase_formulas`,
`unchanged_distance_formulas`,`equality_controller_rule`,
`selected_phase_at_t_formula`,`separation_formula`,`half_separation_formula`,
`half_separation_slack_formula`,`envelope_minimum_formula`,
`envelope_maximum_formula`,`constant_in_phase`,`unchanged_inward_direction`,
`directed_radius_formula`,`directed_radius_slack_formula`.
Vector formula positions use the stated unchanged speed order; r=V mod8,
q=V/8, k=(17q mod7) where applicable. Formula strings are symbolic records
for review, not claims that Python proves their unbounded quantifiers.

## Diagnostic fields

Each diagnostic has:

- `V`,`branch`,`times`,`unchanged_speeds`, `unchanged_phase_vectors`,
  `unchanged_distance_vectors` (two rows in time order), `unchanged_cap`;
- `equality_controllers` (two sorted speed lists),
  `equality_controller_directions` (two lists of `[speed,direction]`);
- `selected_phase_pair`,`selected_phase_separation`,`half_separation`,
  `half_separation_slack` (=d/2−1/8), `raw_pair_minimizer_theta`;
- `pair_envelope_minimum`,`pair_envelope_maximum`,`constant_in_phase`;
- `safe_laps`: one row per unchanged speed, in speed-vector order, with
  `speed`,`at_t`,`at_reflection`. Each time object has `lap` (integer),
  `interval` (closed endpoint pair), `phase`, `distance`,
  `left_clearance`,`right_clearance`, and `controller_direction`
  (`right`,`left`,or null).
- `directed_certificate`: null when8 does not divideV. Otherwise object
  with `radius`, `core_room`, `variable_room`, `selected_room`, `minimum_room`,
  `radius_within_room`, `selected_distance_lower_bound_at_radius`,
  `selected_slack_at_radius`, `candidate_intervals`,
  `unchanged_phase_segments`, `unchanged_endpoint_distances`, and
  `strict_open_interior_verified`.

The three rooms are b−t, `(7/8-frac(Vt))/V`, `(d/2−1/8)/11`, with b=5/16.
For multiples56 the second simplifies to3/(4V).
`candidate_intervals` are closed pairs in the order described above.
`unchanged_phase_segments` rows `[speed,start_phase,end_phase]` use the
unwrapped phase on [t,t+R] in the same lap. All must satisfy
1/8<=start<end<=7/8, which certifies strict interior without sampling.
`unchanged_endpoint_distances` gives the two unchanged distance vectors at
t+R and1−t−R. Reflection preserves these distances and reverses direction.
The selected-runner lower bound is d/2−11R and its slack subtracts1/8.
Strict selected persistence follows from its positive recorded slack.

`summary` records `diagnostic_count`, `branch_counts`,
`all_pair_envelopes_constant_threshold`, `directed_certificate_count`,
`all_directed_checks_pass`. Null directed certificates do not claim failure
of strictness elsewhere; branch1 has opposing unchanged endpoint controllers.

## Digest and replay

Hash each complete diagnostic in protocol order with sorted-key compact JSON
plus one LF, UTF-8, concatenated into `diagnostics_sha256`.
`--write` creates results.json; default/`--check` recomputes and compares the
loaded JSON without writing. The independent verifier may read this schema,
protocol and output, but must not read/import the primary implementation.
