# Frozen comparison: common repair, lazy interval choice, exact cover

October 17, 2026. Rule commit: `d73f644eb237260dc3062d5c76dc878b474ff8cb`.
Execute only after this protocol, configuration, code and manifest are committed.
No validation geometry or contacts were computed during preparation.

## Domain and exposure

Use p=1 and q=16,17,18,19, threshold 1/10, stationary reference 0. Eight moving
core speeds are `(p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q)`; add each admissible
positive integer r absent from that core. All start together; total n=10.
These four consecutive q values include both parities and lie outside the
October 2 orbit study's [1,15]^3 box. They differ from the current development
cores q=2,4,6,8,10. This is a deterministic, bounded transfer, not a random
sample or a claim of globally unexposed repository data.

Construct each complete core at evaluation time. Freeze the widest component
by width then earliest left endpoint, derive its cutoff R=ceil(2d/width), and
evaluate every admissible r below R. The derivation and rule, not a post-outcome
subset, determine the finite domain. Empty/zero-width cores are unsupported;
excess domain size is UNKNOWN_BUDGET. Do not replace a difficult input.

## Operations, sequence and outputs

Run the [frozen rule](RULE.md) and lazy selector using only the core, finite
domain and leader failure list, **before** invoking the full matrix evaluator.
The gap search scans components and exception speeds in ascending order; the
lazy selector skips the already-failing leader and stops each component on
its first failure. Keep complete probe/contact traces and exact gap endpoints.

The pinned parent study supplies full child sets, all contacts and exact DP
minimum containing the leader. Retain that result separately from each selector.
No selector is silently repaired when it fails. Report selected menu sizes,
whether they equal the reference minimum, all misses, and whether a common
point failed despite a successful two-component menu.

Charge shared core construction by its input band count (sum of core speeds)
and output component count, not as free input. Report vectors of operation
counts from RULE.md, including separate discovery and witness-recovery counts.
The two selectors share one computed leader failure list; attribute its tests
to each standalone method, not twice to the executed shared preprocessing.
Record first-contact calls actually performed for one witness per finite case
and the four existing tail-control seeds (R,R+1,10^6+1,10^18+1), skipping repeated
core speeds and duplicate controls. Gap recovery uses the common point for F;
lazy recovery chooses the leader or its selected second interval according to F.
Exact-menu recovery checks all selected intervals and returns earliest contact.
These counts are not a wall-time benchmark or asymptotic cost result.
The baseline evaluator reconstructs the shared core again as a certification
check; that second construction belongs to evaluation overhead. DP state and
transition counters are bounded execution instrumentation, not independently
reproduced by the alternate subset algorithm.

## Controls and alternate verification

Two frozen semantic controls, not validation discoveries:

1. Supplied interval [3/10,2/5], constraints speeds 1,2, threshold 1/3. The only
   common safe time in the interval is 1/3, where two open unsafe gaps touch.
   Gap jumping must retain that equality point.
2. Supplied interval [111/670,19/110], constraints 17,18, threshold 1/10, from
   the preceding study. Each has a witness but their surviving intervals are
   disjoint. Gap search must fail and the lazy interval test must succeed.

The alternate verifier imports only the existing event-based verifier, neither
the primary study nor its checker. Reconstruct complete core and child sets,
compare every contact and surviving piece, verify the first-contact value with
the phase-based method, and verify the exact minimum by subset enumeration.
Reconstruct the complete common-repair set by threshold events for core plus
F; its earliest point independently determines gap-search success and t*.
Validate gap traces, lazy ordering/short circuits, all operation counts, source
identity, complete finite domains, endpoint/lap certificates and every physical
witness. Replay the primary once and require identical bytes.

## Budgets and stop rules

Per core: sum of speeds<=600, components<=600, cutoff<=128, gap point probes
<=20000, lazy contacts<=100000, DP states<=100000 and transitions<=2000000,
minimum-verifier subsets<=1000000. Each command has a 120-second limit. Finite
domain is at most 127 speeds per core; no adaptive expansion or extra threshold.
Record unsupported/UNKNOWN statuses distinctly from mathematical nonexistence.
If verification or execution fails, preserve evidence and stop claim promotion;
any fix needs a separately versioned record, never an overwritten frozen run.

End after four cases, two semantic controls, alternate verification and one
replay. Interpret what the common-point requirement gains or loses, compare
with the competent lazy baseline, and document one earned next question.
Family-wide conclusions remain same-author proof candidates awaiting independent
review. No general LRC, unrestricted menu minimum, new-language, novelty, or
general superiority claim is licensed.
