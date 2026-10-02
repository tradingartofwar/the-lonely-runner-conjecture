# Exact phase projection schema, version 1

Frozen before profile computation. Protocol SHA256:
`8eba9a06595a2014095f84cc22c6b91d65d6f9fd71771912e0af368293bdff17`.
Only the two prescribed velocity lists are evaluated. The chosen speed is 11;
A uses the unchanged speeds1,4,5,6,7,V. Fractions are reduced strings.

## Circle and interval conventions

All phase points lie in [0,1), identifying 1 with0. General interval pieces
are `[left,right,left_closed,right_closed]`, ordered by numerical endpoints.
An interval ending at1 always has right_closed=false; a needed phase0 point
appears at0 instead. Pieces are maximal connected pieces in this cut interval;
wraparound circle components can therefore occupy two pieces. Closed TIME
components are endpoint pairs, retaining isolated points. Time0 and1 never
belong to A because speed1 is unchanged.

## Algebraic partition (declared before outcomes)

Phase events E are {0} union every fractional part of11 times an A-component
endpoint. N is computed by explicit branches t=(j+x)/11, j=0,...,10: exact
preimages at events and branch integers on every open cell. This captures
all multiplicity changes and isolated image points.

Theta partition events are {0} union {(1/8-e) mod1,(7/8-e) mod1:e in E}.
These are a complete finite candidate set, not necessarily all genuine slope
changes. On each intervening open cell, D has slope
`(N((1/8-theta) mod1)-N((7/8-theta) mod1))/11`, evaluated on the constant
phase cells reached by any interior theta. Periodic prefix integration fixes
the intercept. Unweighted support uses indicators N>0 in the same formula.
No slope or continuum claim is inferred from a sampled grid.
A status change can occur only at the same generated theta events: moving safe
arc endpoints cross neither a projected endpoint nor an isolated point inside
a partition cell. Exact midpoint evaluation identifies this constant status.

## Archive structure

Top-level `schema_version`, `status`, `protocol_sha256`, `script_sha256`,
`prior_archive` (`path`,`sha256`), `cases` in protocol order.
Each case has `id`,`velocities`,`V`,`unchanged_speeds`, `A_components`,
`A_duration`,`A_isolated_times`, `phase_events`,`phase_points`,`phase_cells`,
`P_components`,`B_components`,`extra_isolated_projection_points`,
`P_metrics`,`B_metrics`,`multiplicity_integral`,`maximum_point_multiplicity`,
`maximum_bulk_multiplicity`, `critical_phases`,`theta_points`,`theta_cells`,
`duration_extrema`,`support_estimate_extrema`,`underestimate_extrema`,
`duration_plateaus`,`phase_status_sets`,`prior_phase_checks`, and
`case_sha256`.

`phase_points` rows are objects `{x,count,preimages}` with sorted distinct
exact time preimages. `phase_cells` rows are objects
`{left,right,count,preimage_branches}`; branches are increasing j integers and
mean the complete explicit list of affine preimages `(j+x)/11` throughout the
OPEN cell. The final right endpoint is1. P includes event points with count>0
and cells with count>0. B closes only positive-length occupied cells on the
circle. `extra_isolated_projection_points` lists P points absent from B.
`multiplicity_integral` equals11*A_duration.

Both P/B metric objects have `measure`, `maximum_circular_gap`,
`minimum_covering_arc_length`, and `maximal_gap_arcs` rows
`[start_mod1,end_mod1,length]`, ordered by their numerical start. Only arcs of
maximum gap length are listed; zero-length gaps are omitted. Both sets are
nonempty in this fixed experiment. Gap length is the supremum gap length;
its endpoints lie in the closed set. Minimum covering arc length is1-gap.

`theta_points` rows have `theta`,`duration`,`support_estimate`,`status`,
`contact_times`. `theta_cells` rows have `left`,`right`,`slope`,`intercept`,
`support_slope`,`support_intercept`,`status`,`contact_times`.
Coefficients describe D(theta)=slope*theta+intercept on the OPEN cell.
Statuses are `strict` (positive time duration), `contacts` (nonempty time set
of zero duration), or `empty`. `contact_times` is null when duration is positive;
otherwise it is the complete sorted list of allowed times (empty if no times).
For a zero-duration cell this list is constant throughout that open cell.

Each extrema object has `minimum`,`maximum`,`minimizer_set`,`maximizer_set`,
with sets encoded by the general phase interval convention. Underestimate is
D minus the unweighted support estimate. `duration_plateaus` lists every
positive-length constant-value portion, grouped by value in numerical order:
objects `{value,phase_components}`. Redundant candidate partition boundaries
are merged, with endpoint membership retained. `phase_status_sets` maps the
three status names to exact phase interval pieces. Circle phase1 is never
stored as a second point.

## Prior finite-offset comparison

Pinned prior file: `reviews/2026-09-27-fastest-laps/phase_results.json`, SHA256
`612cd4320fc3083476b352f8ce058e345cf2f88a418a36e87228cdbad29c8692`.
For each prior s in0..V-1, `prior_phase_checks` records
`{s,theta,duration,status,isolated_times,full_allowed_components}` in s order,
where theta=(11s/V) mod1. The primary reconstructs allowed times by intersecting
the safe phase arc with each explicit pushforward branch and pulling back.
It checks exact full allowed sets, durations, status, and isolated times
against the pinned archive; no new offsets or speed configurations are added.

## Digests and replay

For each case, remove `case_sha256`, serialize the remaining complete case
object with sorted keys and compact separators, append one LF, encode UTF-8,
and SHA256. The independent verifier can compare all fields and this digest.
`--write` creates results; default/`--check` recomputes and compares JSON
without writing. No abstract example or two-time certificate is implemented
in this primary script; those have separately assigned ownership.
