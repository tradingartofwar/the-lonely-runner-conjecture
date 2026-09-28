# Fixed-time residue classification schema, version 1

Frozen before the primary classification archive is generated. Protocol SHA256:
`0932c23c6c65dd8faaae4d319770ae0bca583237c0f92fee9c5ae7f8ce474f02`.
Only substitutions at the four prescribed times are used. No allowed-time sets,
additional time pairs, speed search, or failure diagnostics enter this script.
Fractions are reduced strings. Residues are ordered0..119.

## Algebraic certificate

For each template t,1-t, integer unchanged speeds have equal distances at both
times. Let c be their common minimum distance. Let a,b be the speed11 phases
at the two times and d their circular separation. Circle triangle inequality
gives max(||a+theta||,||b+theta||)>=d/2 for every theta; equality is attained
when the translated midpoint of the shorter arc is0. Therefore the full
best-of-pair margin is `min(c,max(||a+theta||,||b+theta||))`. Its minimum is
min(c,d/2), maximum is c, and it is constant precisely when c<=d/2.
All constant conclusions must be checked by this criterion, not presumed.
The union of four times takes the maximum of the two constant pair margins.
120 is a sufficient denominator period, with no claim of minimality.

## JSON fields

Top-level `schema_version`, `status`, `protocol_sha256`, `script_sha256`,
`period`, `threshold`, `excluded_V`, `unchanged_runner_indices`,
`templates`, `residue_rows`, `residue_rows_sha256`, `summary`,
`failed_residue_classes`, `failure_representatives`.
`unchanged_runner_indices` is [1,2,3,4,5,7] in the original velocity order
[0,1,4,5,6,7,11,V]. All unchanged distance vectors use this order.

Each `templates` entry has `id`, `times`, `selected_speed`, `selected_phases`,
`circular_separation`, `half_separation`, `half_separation_attained_at_theta`.
The attaining theta is the negative midpoint of the shorter signed arc from
the first selected phase to the second, reduced modulo1. This directly checks
the sharp triangle lower bound without constructing a phase grid.

Each residue row has `residue`, `least_admissible_V`, `templates`, `union`.
The row's `templates` is an object keyed by the two template IDs. Each value:

- `unchanged_distance_vectors`: two six-entry fraction lists, in time order;
- `unchanged_cap`: their common minimum;
- `minimum_best_margin`, `maximum_best_margin`;
- `constant_in_phase`: boolean from cap<=half separation;
- `status`: `strict` if minimum>1/8, `threshold` if minimum=1/8,
  `failure` if minimum<1/8.

`union` contains `minimum_best_margin`, `maximum_best_margin`,
`constant_in_phase`, and `status`. The row's representative is the least
positive V in that residue class outside{1,4,5,6,7,11}. Distances are computed
at that admissible representative and checked to equal residue substitutions.
Every larger integer in the same class has identical fixed-time coefficients.

`summary` has `residue_count`, `templates` (each ID maps to counts for
`strict`,`threshold`,`failure`), `union` (same counts), and
`all_pair_margins_constant`. `failed_residue_classes` is the increasing list
of residues whose union status is failure. `failure_representatives` is the
corresponding ordered list of objects `{residue,V}`. These are diagnostic
inputs only; this script does not evaluate their complete allowed-time sets.

## Canonical digest and replay

Serialize each complete residue row with sorted keys and compact separators,
append one LF, encode UTF-8, and concatenate in increasing residue order for
`residue_rows_sha256`. Other fields are compared directly by the verifier.
The JSON file itself uses compact separators plus one terminal LF.
`--write` creates `classification.json`; default/`--check` recomputes and
compares JSON without writing. The separately structured verifier must not
read/import the primary implementation.
