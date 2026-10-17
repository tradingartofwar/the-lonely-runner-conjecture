# Removing the shared anchor preserves small menus

October 17, 2026. **OBSERVED:** all eight paired perturbations exclude time
1/10, yet each still has a sufficient menu of at most two connected components
containing the predetermined widest component. Two require one component and
six require two under that requirement. No fallback, no-cover or budget limit
was reached. Thus that particular shared anchor is unnecessary for success
on these altered cores; no general two-component theorem follows.

The Fibonacci-derived core becomes simpler: replacing speed 21 by 20 removes
the anchor but enlarges its widest interval enough to make a second source
unnecessary. All 84 complete child safe sets in the common finite comparison
domains change, while seven of eight menu sizes remain unchanged. Complete
geometry and the size of a sufficient witness menu are different measurements.

Execution freeze: `b98c55e6bb3ef84d410d26754be5597d60058af2`, 24 pinned files.
Source: `8431549e6ed30729e9d208bb26e51bb5c9791042`.
[Protocol](PROTOCOL.md), [config](config.json), [runner](run.py),
[alternate verifier](verify.py), [manifest](manifest.json).

## Paired design and decisions

The baseline is the preceding [eight-core study](../outside-template/RESULTS.md).
Its results and PASS verification are pinned and reused, not rerun or counted
as fresh validation. Within each baseline core, replace one speed by a positive
multiple of 10 at most max(speed)+10. Minimize (absolute change, replacement,
removed speed) among choices retaining eight distinct positive speeds, gcd one
and exclusion of the old exact p,q template. This input-arithmetic rule was
frozen before new geometry. All changes are one or two speed units.

Labels name the baseline, not the mathematical type of the altered sequence.
For example, the modified prime list contains 10 and the modified Fibonacci
list contains 20. Seven core speeds remain unchanged in each pair.

| Baseline label | Replacement | Old minimum | New minimum | New complete components | New cutoff R | New finite cases |
|---|---|---:|---:|---:|---:|---:|
| Consecutive | 8 -> 10 | 1 | 1 | 8 | 11 | 2 |
| Odd | 9 -> 10 | 2 | 2 | 14 | 10 | 5 |
| Primes | 11 -> 10 | 2 | 2 | 20 | 12 | 6 |
| Squares | 9 -> 10 | 2 | 2 | 42 | 16 | 12 |
| Powers of two | 8 -> 10 | 2 | 2 | 64 | 37 | 30 |
| Fibonacci | 21 -> 20 | 2 | 1 | 16 | 9 | 3 |
| Clustered | 11 -> 10 | 2 | 2 | 28 | 11 | 9 |
| Irregular | 89 -> 90 | 2 | 2 | 58 | 30 | 25 |

Every row has reference 0, common start and threshold d=1/10. Adding a positive
integer r absent from its eight-speed core gives ten distinct runners. Minima
require that row's predetermined widest component, with earliest start on
ties; they are not unrestricted minima. Components and their IDs belong to
their own source geometry and are not identified across a pair.

R=ceil(2d/width), with all admissible 1<=r<R checked exactly. All 92 complete
new child sets are nonempty. The width tail supplies r>=R; combined all-r
conclusions remain **same-author proof candidates awaiting independent review**.
Large-speed controls are checks, not the justification for the infinite tail.

## Selected geometry and repairs

| Baseline label | New leader ID | New leader interval | New leader failures | Selected IDs | Optional common repair |
|---|---:|---|---|---|---|
| Consecutive | 0 | [11/100,9/70] | none | [0] | not attempted |
| Odd | 3 | [31/130,13/50] | 4,8 | [0,3] | 11/100 |
| Primes | 6 | [41/170,49/190] | 4,8 | [0,6] | 11/170 |
| Squares | 19 | [291/640,299/640] | 2,13 | [0,19] | 41/360 |
| Powers of two | 0 | [71/640,149/1280] | 9,18 | [0,2] | 21/160 |
| Fibonacci | 5 | [91/340,99/340] | none | [5] | not attempted |
| Clustered | 0 | [1/100,9/310] | 1,2,3 | [0,2] | 21/190 |
| Irregular | 28 | [291/620,219/460] | 2,17,19 | [4,28] | 71/900 |

Every menu matches the full reference minimum and lexicographic tie-break.
All selected components now have positive width. The full new cores retain
four isolated components, all in the squares-derived case; equality was never
discarded. Each optional common time is a selected component's left endpoint,
and no gap jump was needed. This still does not establish an advantage for
common-point search over ordinary separate contact checks.

### Why the Fibonacci-derived menu shrinks

The old leader is [91/340,59/210], width 19/1428, with cutoff 16 and sole
admissible exception 11. Speed 34 controls its left boundary and speed 21 its
right boundary. After replacing 21 with 20, the leader becomes
[91/340,99/340], width 2/85. Speed 34 now controls both boundaries; speed 20
is safe throughout the larger interval. The cutoff falls to 9, and the finite
remainder {4,6,7} is covered. Speed 11 is now in the width-certified tail.

This endpoint interpretation is a deduction from the saved exact component
certificates, not a predeclared prediction. Removing a known witness time
does not imply a harder problem: replacing a constraint can open other times.

### Old witnesses do not all transfer in the same way

| Baseline label | Old repair time | Safe for new core? | Covers every new leader exception? |
|---|---|---|---|
| Consecutive | none | not applicable | not applicable |
| Odd | 1/10 | no, speed 10 blocks | yes, but unusable because core fails |
| Primes | 11/170 | yes | yes |
| Squares | 1/10 | no, speed 10 blocks | yes, but unusable because core fails |
| Powers of two | 11/80 | yes | yes |
| Fibonacci | 1/10 | no, speed 20 blocks | vacuous: no exceptions remain |
| Clustered | 1/10 | no, speed 10 blocks | yes, but unusable because core fails |
| Irregular | 11/270 | yes | no, new exception 2 blocks |

The irregular case distinguishes core safety from coverage of the current
query obligations. The old point remains physically valid for all eight new
core speeds, but it cannot replace the new repair point because the leader's
exception list changed. Reusing an old witness requires both checks.

## Full-set comparison and equality

The complete old/new core intersections are saved and separately
reconstructed using threshold events for the union of their speed sets.
Every anchor-removal claim is checked both by physical phases and exact set
membership. On the common finite added-speed domains, all 84 full child sets
differ: counts by row are 1,1,5,11,29,3,9,25. This does not cover unmatched
finite inputs or the infinite tails. The removed and inserted speeds change
admissibility, so they are not silently treated as the same test domain.

The primes-derived pair exposes a precise information loss in using measure
alone. Its old core and its intersection with the new core both have measure
709162/8083075, yet the intersection is strictly smaller: the four old isolated
times {1/10,3/10,7/10,9/10} disappear. The saved intersection equals exactly
the old positive-width components. Equal measures therefore cannot certify
set equality or preservation of every valid witness. The verified complete
sets retain the distinction that their length summaries omit.

The pairing changes an actual speed constraint, so geometry, the widest
component and the query domain can all change together. This is not causal
isolation of anchor removal. It establishes the observed robustness of small
menus under these particular perturbations, with one simplification.

## Work, verification and reproduction

| Baseline label | Leader contacts | Lazy contacts | Constructor total | Full reference contacts |
|---|---:|---:|---:|---:|
| Consecutive | 2 | 0 | 2 | 16 |
| Odd | 5 | 2 | 7 | 70 |
| Primes | 6 | 2 | 8 | 120 |
| Squares | 12 | 2 | 14 | 504 |
| Powers of two | 30 | 3 | 33 | 1920 |
| Fibonacci | 3 | 0 | 3 | 48 |
| Clustered | 9 | 4 | 13 | 252 |
| Irregular | 25 | 10 | 35 | 1450 |
| **Total** | **92** | **23** | **115** | **4380** |

These first-pass counts are not a runtime benchmark or all work performed.
Core construction uses 1,166 input bands and produces 250 components (246
positive-width, four isolated). The full reference reconstructs these cores
and all 92 child sets. No constructor residual fill, cache reuse or DP occurs;
the reference DP performs 805 transitions, peak states per case 1,3,4,4,4,1,5,5.
DP counters remain instrumentation rather than an independent trace proof.

Optional searches add 14 point probes. Certificates retain 14 exception
witnesses. Dispatch emits 92 finite and 30 tail-control witnesses, requiring
78 and 30 fresh leader contacts; all 16 invalid-input guards reject. Both
reference/audit work and one replay were actually performed and remain charged.
Earlier semantic controls and old baseline computations were not rerun.

[Verification](results/VERIFICATION.json) passes 8 new complete cores, 92 child
sets, 4,380 reference contacts, 115 constructor contacts, 336 physical witness
records, 228 subset-minimum checks and 6 optional common sets. The paired
audit additionally reconstructs 8 union-speed sets with 2,626 threshold events.
The alternate code imports neither constructor nor primary checker; it uses
the prior event/subset helpers. Both implementations have the same AI author,
so this is not independent human or formal proof review.

[Replay](results/REPLAY.json) is byte-identical on Python 3.12.14. No execution
discrepancy, timeout, budget stop or frozen-source modification occurred.
[Complete results](results/RESULTS.json) are 675,865 bytes, SHA-256:
`06f4fb8f4f9de3cc18250863c947ceccc180024f818e306cae352c8954bde01b`.
[Certificates](results/CERTIFICATES.json) are a post-verification extraction
bound to that hash. Baseline results SHA-256:
`021dc797d191b5b5d2d5c40004b0944d45872c6878058d9af45a35c7a8d46f4c`.

From repository root, with fresh output and checkpoint paths:

```sh
timeout 240s python experiments/runner-addition/anchor-removal/run.py --freeze b98c55e6bb3ef84d410d26754be5597d60058af2 --output /tmp/anchor-removal-results.json --checkpoint-dir /tmp/anchor-removal-checkpoints
timeout 240s python experiments/runner-addition/anchor-removal/verify.py --input /tmp/anchor-removal-results.json --output /tmp/anchor-removal-verification.json
timeout 240s python experiments/runner-addition/anchor-removal/run.py --freeze b98c55e6bb3ef84d410d26754be5597d60058af2 --output /tmp/anchor-removal-replay.json --checkpoint-dir /tmp/anchor-removal-replay-checkpoints
cmp /tmp/anchor-removal-results.json /tmp/anchor-removal-replay.json
```

## What to ask next

The forced-widest requirement is still a possible source of the two-component
answer. **Next proposed:** freeze an unrestricted single-component decision
for these six altered cores currently requiring two with the leader. For each
candidate component, use its own width cutoff, or an exact blocker for a
singleton, and preserve failure/budget outcomes. The existing two-component
certificate supplies an upper bound. Either a different single component
works, or blockers for every component justify the lower bound two without
forcing the widest. The leader's cutoff alone cannot certify an arbitrary
alternative component's infinite tail. No such decision has been run here.

This sharpens the question before adding more speed lists: are two components
necessary for the physical witness task in these families, or necessary only
because our construction insists on a particular first component? Neither
answer implies intrinsic incompressibility, an optimal formula, a new LTCM,
novelty, all-reference coverage or a general LRC result.
