# Frozen contact-first hybrid recovery — September 29, 2026

Freeze before hybrid target computation or timing. Source branch head:
54f9a2ea0a654afc9326668e4c3bc92e31f31567. This is a development repair of
the known (54,26) phase-screen failure, not a blind or held-out transfer.
Package date follows the maintainer's September 29 local date; execution is
September 30 UTC. No new target, runner count or threshold is introduced.

## Supported question and inputs

One shared closed 1/8 witness for the stationary reference, common start,
speeds zero plus ap+bq for rows (1,0),(0,1),(1,1),(2,1),(3,1),(3,2),
(6,2),(3,8),(54,26). Positive integer p,q; ten distinct speeds iff p!=q
and p!=2q. Preserve auxiliary directions separately. Supplied input is the
36 eight-row safe source segments in the pinned nine-runner stage8 record.
Their earlier discovery is supplied preprocessing, not eliminated work.
Pin all imported code and archived comparison outputs. The latter may only
be used after hybrid construction for regression/comparison, never as an
oracle for choosing a recovery source, lap or point.

## Unchanged first stage

Call the pinned phase screen and coverage compiler unchanged (same module
key adapter, threshold and domain metadata). Retain five-candidate screen,
full residual contact table, leader and greedy menu exactly. Rectangle cap
400. If there is no completed finite reduction, return its scope/geometry
failure; no alternative leader. If complete, no recovery is needed.

## Contact-first recovery

For every uncovered primitive pair in lexicographic (P,Q) order, consult ALL
36 supplied source records in numeric (parent,edge0,edge1,seventh,eighth)
order, stopping at its first successful source/H/lap. No source reranking,
phase-identity enlargement, cross-pair recovered-segment reuse or new menu.

Write a source as A+s(B-A), 0<=s<=1. Project H(s)=Qx(s)-Py(s).
Enumerate integers h from ceil(min H) to floor(max H), increasing.
If H is nonconstant, each h fixes exactly one rational s: check its new-row
raw value using m=floor(raw), accepting iff raw-m is in [1/8,7/8].
If H is constant and integer, retain the entire parameter interval; enumerate
new-row lap bands m from ceil(min raw-7/8) to floor(max raw-1/8), increasing,
intersect each band with [0,1], and take the least parameter of the first
nonempty interval. A constant noninteger H has no contact. Preserve point
sources and equality endpoints. Record failed tests before the first success.

Before recovery, compute a bound over all missing-pair/source combinations:
source integer-H count times max(1, whole-source new-row lap count). Cap the
sum at 4096; report RECOVERY_SCOPE_LIMIT without querying on excess. Charge
all preflight projection and raw-range evaluations, even when early stopping
later avoids that source. The bound overcounts nonconstant-H work on purpose.
Record actual source visits, H tests, point-phase tests and parallel-band
tests separately. Exhaustion means NO_SOURCE_CONTACT for that pair, not
physical nonexistence. No richer parent search or threshold change this run.

The retained output is the original selected screen menu plus a primitive
direction dispatch table of point witnesses. Do NOT treat recovered points
as globally reusable segment candidates. Carry source provenance, local and
original parent-edge parameter, H, all nine torus laps and physical inverse.
Dispatch first on gcd-reduced exception pair; otherwise use the original
screen menu. Unknown unhandled pairs must fail visibly if coverage incomplete.

## Mathematical obligation and comparison

Show that for each fixed primitive pair, contact-first recovery hits iff
some full appended source segment hits, provided the finite exhaustive
search completes. Both operations intersect the SAME source with integer
H and the new safe bands; affine constancy and endpoints require explicit
cases. First witnesses/order may differ. The screen's positive-width leader
covers its infinite tail; successful recovery of all residual misses then
gives a conditional uniform family certificate. General arguments remain
HYPOTHESIS / internally reviewed proof candidates.

After construction, regenerate full clipping/compilation with the pinned
algorithm and compare every field against archived full certificate. Compare
the entire hybrid screen certificate with archived restricted certificate.
Verify recovered points belong to a full candidate with identical inherited
laps, new lap and source-parameter mapping. Recheck all 47 residual directions
using the dispatch output, including nonexception directions. Do not retune.

## Controls and exceptional branches

Physical controls are the earlier 22 pairs, followed by (5,1),(10,2), to
cover the third exception and its gcd scaling. Exact phases, torus/physical
laps, reflection and alternative Bezout recovery for every emitted witness.
Open-source membership and open-source recovery are diagnostic only for the
three exception pairs; no change to the closed rule. Preserve source points:
their parameter interior does not count as geometric relative interior here.

Four small synthetic source queries (kernel only, not physical runner cases)
exercise: nonconstant H with an unsafe first point then a safe later point;
constant integer H with positive-length safe band; constant noninteger H;
singleton safe contact. Plus the zero recovery-budget stop on the actual
preflight. Predetermine fixtures in code before first execution. These test
the new degeneracy/exhaustion branches, not a new target scan.

## Costs and bounded timing

Report source validation, coefficient and boundary checks, full lap attempts,
materialized segments, residual matrix entries, preflight evaluations and
actual recovery tests separately. Do not sum unlike operations as equivalent.
Full baseline is full append clipping plus the unchanged compiler. Hybrid
is screening plus its compiler plus preflight and recovery. Both validate the
same supplied source; input parsing/imports, physical controls, comparison
audits and JSON writes are outside timing. Both retain their native traces.

Use perf_counter_ns: one warmup of each method, then 11 paired measurements,
alternating method order (hybrid first on even rounds). Keep GC default and
record Python/platform and all individual timings, medians and paired ratios.
Stop before the next pair if aggregate elapsed exceeds 30 seconds. Never
extend repeats to improve a result. Timing is implementation/environment
evidence only, not complexity, universal speed or preprocessing-free benefit.
Timing output is retained but excluded from byte-for-byte reproduction.

## Reviews, reproduction, storage and CC checkpoint

Separate geometry, physical and proof AI reviews; arithmetic/physical review
must not import production code. Distinguish independent structure from blind,
external/human or formal verification. Reproduce deterministic outputs once
after review; preserve any correction timing. Hash all artifacts in manifest.
Save to the existing research branch, preserving concurrent visual work.

CC must carry the supported one-witness question, source recovery route,
direction-specific dispatch, affine compatibility and physical inverse.
Assess whether a segment menu and exception points are adequate without
claiming a full safe set, optimum, every reference or arbitrary ten runners.
Reuse the credited affine-segment/integer-orbit framework; no new literature,
novelty or frontier claim. No broader scan, paid compute, unattended task,
outside contact or main merge. Next transfer is proposed only after this
repair is assessed; do not run another target during this experiment.
