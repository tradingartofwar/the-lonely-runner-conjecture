# Exception-cover constructor v1: frozen validation

October 17, 2026. Freeze this protocol, design, config, code and manifest before
any new geometry, contact outcomes or controls execute. Source commit:
`353531ad1035010a4acdb78994614753d36977d1`.

## Family domain

Use exactly (p,q)=(1,20),(1,21),(2,21),(3,20), d=1/10. Eight core speeds are
`(p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q)`. These primitive pairs include two
cases beyond p=1; gcd(p,q)=1 keeps the original [0,1] clock. Add stationary
reference 0 and an admissible positive integer r absent from the core, n=10,
common start. This is a bounded deterministic transfer, not a random sample.

Construct each complete core once for the constructor. Choose its widest
positive component, earliest left endpoint on ties. Derive the complete finite
domain and width tail exactly as in DESIGN.md. Empty/zero-width cores are
UNSUPPORTED; a size/cutoff cap is UNKNOWN. Do not substitute a different pair.

Run the constructor and optional repair query BEFORE the full matrix oracle.
Then use unchanged parent study.py to reconstruct complete child sets and exact
minimum menus. It rechecks the core, charged as additional audit work. Compare
minimum size and lexicographic IDs, not merely successful witness production.
Save every full contact/set for alternate verification, using compact JSON.

For successful certificates, dispatch all finite inputs and the existing tail
seeds R,R+1,10^6+1,10^18+1, skipping core duplicates and repeated seeds. Check
physical phases/laps and selected-interval membership. Cache-table construction
uses no additional contacts; recovery of r in F uses optional common point if
found, otherwise its saved individual witness. Other r use the leader formula.

## Seven supplied-interval controls

These exercise finite constructor semantics; they are not complete physical
cores or newly discovered LRC examples. Exact inputs and expectations are in
config.json. All intervals are closed; source IDs follow time.

1. leader_only: an already sufficient leader, minimum one.
2. three_with_tie: leader fails speeds 2,3 at d=1/3; singleton alternatives
   separately cover them, requiring three components total. Two optimal menus
   exist; the smallest IDs must win. This must exercise residual fill and DP.
3. separate_not_joint: leader [53/1000,61/1000] fails 17,18; repair interval
   [111/670,19/110] covers each separately but has no common point. Menu size
   two must remain valid when its optional common-point search returns empty.
4. no_cover: one query has no covering supplied component; report its speed.
5. contact_budget: zero contact budget on the three-component control must
   return UNKNOWN, never infeasible.
6. dp_budget: zero DP-transition budget on that same control must return
   UNKNOWN after all residual contacts, never infeasible.
7. optional_budget: zero optional-probe budget on separate_not_joint must
   leave the exact two-menu and individual-witness dispatcher valid.

The controls are chosen analytically before execution. They are expected
behavior checks, not evidence that the four family cases reach those branches.
For each control, also compute the complete finite contact matrix and exact
reference minimum with the ordinary full-budget oracle.

## Verification and limits

The alternate verifier imports neither constructor.py nor the primary checker.
Use the pinned event-based verifier to reconstruct complete family cores and
child sets, or intersect event sets with supplied control intervals. Compare
all reference contacts, every actually queried contact, cache uniqueness,
absence of nonleader/nonexception queries, short-circuit order, full residual
completion, selected minima/ties and all stored/recovered witnesses.

Verify optional common points or emptiness using complete event sets on the
selected interval and the pinned alternate trace verifier. Unknown statuses
remain unresolved, and all family-wide arguments remain proof candidates.
Check budget controls and invalid dispatcher guards without expanding research
inputs: reject r=0, a repeated core speed, and a non-domain control query.

Budgets per family/control: core speed sum600, components600, cutoff128,
unique contacts100000, DP states100000/transitions2000000, optional point
probes20000, alternate subset combinations1000000; command120 seconds.
Control-specific zero budgets override only the named constructor stage.
No timeout or budget stop is a mathematical failure. Record any discrepancy,
preserve frozen outputs and version fixes separately. No silent changes.

Run primary once, alternate verification, and one byte-identical replay. End
after these four families and seven controls. Report which fallback branches
were reached naturally versus only by controls, costs by operation, shared
dependencies, and a concrete next question. No general runtime, novelty,
unrestricted minimality, new-language or general LRC claim.
