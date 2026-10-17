# Exception-focused selection transfers; gap search shows no advantage

October 17, 2026. **OBSERVED:** four bounded exact comparisons and two semantic
controls. **HYPOTHESIS / proof candidates:** all-admissible-r consequences of
the supplied finite-reduction argument. AI materially generated the rule,
implementations and report; alternate algorithms share the same AI author.

Both the unsafe-gap selector and a simple lazy interval selector found the
**same minimum two-component menus** as exact cover in all four configurations,
with the predetermined widest component required. The gap view supplied fixed
repair times, but did not improve selection over the conventional interval
baseline. The operational result is to concentrate discovery on the exceptions
to a certified leader, while retaining the richer geometry for recovery.

## Frozen question and domain

The [rule](RULE.md) was committed before selecting these cases. The
[protocol](PROTOCOL.md), configuration, code and dependency hashes were then
committed before computing their geometry or contacts.

Use p=1, q=16,17,18,19 and the eight core speeds
`(p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q)`. Add stationary reference 0 and a
positive integer r absent from the core. All start together; n=10, d=1/10,
period [0,1]. These four consecutive q values include both parities and lie
outside the earlier orbit study's [1,15]^3 box. This is a deterministic transfer,
not a random sample or a general claim of unexposed data.

For the widest core component L, derive R=ceil(2d/width(L)) and check every
admissible r<R. Its width handles every r>=R. Let F be the exact finite list
that defeats L. The gap rule seeks the earliest **one common time** safe for
the core and every r in F. The lazy rule seeks the first component providing
**some time for each r**, allowing those times to differ. Both run before the
full component-by-speed table is constructed.

## Exact results

| q | Complete components | Widest ID | Cutoff R | Finite cases | Complete exception list F | Selected IDs, all three methods | Common repair time |
| ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| 16 | 46 | 3 | 33 | 27 | {7,20} | {3,4} | 31/160 |
| 17 | 54 | 15 | 35 | 29 | {3,6} | {0,15} | 51/400 |
| 18 | 66 | 16 | 42 | 35 | {3,6,34} | {1,16} | 17/140 |
| 19 | 56 | 14 | 39 | 33 | {3,6,9} | {2,14} | 51/410 |

All 124 complete child sets are nonempty. Every selector returned a certificate;
no budget or unsupported status occurred. All exact minima and lexicographic
choices agree with alternate subset enumeration.

| q | Widest interval L | Selected repair interval J |
| ---: | --- | --- |
| 16 | [191/1310,199/1310] | [31/160,69/350] |
| 17 | [61/180,479/1390] | [51/400,179/1390] |
| 18 | [61/190,479/1470] | [17/140,179/1470] |
| 19 | [501/1550,509/1550] | [51/410,199/1550] |

For each row the resulting dispatcher uses the fixed repair time when r is in
F, otherwise the existing exact first-contact formula on L. Each F is nonempty,
so L alone is insufficient; a successful two-menu is minimum with L required.
This study does **not** decide whether another single component, without L,
could work for every admissible r. It also does not address other reference
runners or arbitrary q.

The q=16 exception list {7,20} rules out simply carrying forward the earlier
special treatment of speed 3. The frozen selection procedure handled the new
exceptions without tuning. The all-r conclusion depends on the exact finite
domain, complete core certificates and width argument, not on sampling large r.

## What was gained, and what was not

| q | Leader tests, shared preprocessing | Gap point probes | Gap jumps | Lazy interval tests | Full reference contacts |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 27 | 7 | 4 | 6 | 1,242 |
| 17 | 29 | 2 | 0 | 2 | 1,566 |
| 18 | 35 | 6 | 1 | 6 | 2,310 |
| 19 | 33 | 9 | 2 | 9 | 1,848 |
| Total | 124 | 24 | 7 | 23 | 6,966 |

Each standalone selector requires the leader classification plus its own column
of probes/tests. The executed study shares that classification. The lazy method
visited 10 components across the four cases; gap search visited 11, including
the already-known failing leader in q=16 as specified by its frozen rule.

These are counts of different exact operations, not interchangeable runtime
units. Both methods also require complete core construction: 1,196 input bands
produce 222 components across the four cores. The full reference evaluator
reconstructs those cores again as a certification check, computes all child
sets, and runs its DP. Verification and replay add work. The study actually
performed that reference work; it has not measured end-to-end savings or a
general speed advantage.

The full table is an optimality oracle, not the only competent baseline. The
lazy selector already obtains the same result with 124 leader predicates and
23 additional interval contacts. The gap method has **no demonstrated selection
advantage over that baseline**.

For recovery of one witness at each of the 124 finite inputs, first-contact
calls are gap 114, lazy 124, exact-menu earliest-contact policy 248. The gap
dispatcher reuses its fixed point for the ten exception inputs. There are 15
distinct tail controls across cores, requiring 15,15,30 calls respectively.
This is a difference between recorded dispatch policies: an exact-menu result
could also retain leader classifications or cache repair points. It is not an
inherent cost disadvantage of exact cover. All policies additionally compute
physical phase/lap evidence; caching and preprocessing are not free.

A consequential post-run observation: **every returned common point is the
left endpoint of its repair component, and every gap jump leaves its current
component**. Thus the validation did not demonstrate a need to search inside a
component. No endpoint-only selector was separately frozen or benchmarked here.
The common-point requirement caused no validation misses, so these four cases
do not establish how often that stronger requirement becomes costly or fails.

## Preserve the distinction between separate and common witnesses

The fixed control I=[111/670,19/110] has a safe part [111/670,29/170] for speed
17 and [31/180,19/110] for speed 18 at d=1/10. These parts are disjoint. Gap
search correctly reports no common repair point; the lazy interval test
correctly accepts separate feasibility. This previously exposed **local interval
control** is not a new complete-core failure or an eleven-runner LRC claim.

The other control uses [3/10,2/5], speeds 1,2 and d=1/3. Two open unsafe gaps
touch at 1/3, which remains safe for both. Gap search and the alternate complete
set retain that isolated point. Merging the open gaps into a closed obstruction
would have lost the existence answer.

These controls expose opposite risks: separate existential bits cannot certify
a common time, while demanding a common time can reject a component that is
adequate for choosing a different witness in each case. The representation and
the quantifiers must follow the requested operation. The [shared model
record](../menu-views/MODEL.md) and [rule record](RULE.md) preserve those meanings
and source-recovery routes.

## Interpretation and next question

The demonstrated advance is a working transfer of **exception-focused
discovery**: derive what the leader fails to handle, then examine alternatives
only for those cases. Ordinary exact interval operations suffice here; the
gap interpretation helps explain and certify a common repair but has not
earned preference as the discovery method. No new LTCM, novelty, intrinsic
complexity, or general mathematical breakthrough is established.

**Next proposed:** implement an exact exception-only menu constructor with the
lazy two-component search as its first step and a residual set-cover fallback
when two do not suffice. Treat a common fixed repair point as an optional extra
certificate, never a requirement for a valid menu. Freeze a comparison that
includes the known separate-versus-common control and a different core domain,
checking minimum menus and charging construction plus recovery. This follow-up
has not run; do not silently extend the current four-case study.

## Verification and reproduction

Rule freeze: `d73f644eb237260dc3062d5c76dc878b474ff8cb`.
Execution freeze: `d814392178a113e8d9e41ebb771e9e2e4d6eb0aa`.
The [manifest](manifest.json) pins 12 files. No frozen code changed after
execution. All arithmetic uses exact fractions; all command budgets held.

The alternate path reconstructs sets from threshold events and verifies minima
by subset enumeration. It checked **4 complete cores, 124 complete child sets,
4 complete common-repair sets, 6,966 component contacts, 680 physical witness
records, and 222 minimum-search subsets**. It also verified both semantic
controls, gap/lazy traces, finite domains, dispatch policies and their operation
counts. DP state/transition counters are bounded execution instrumentation,
not independently reproduced by the subset algorithm. Both code paths share
the same AI author; independent human or formal proof review remains open.

From the repository root at the results commit:

```sh
timeout 120s python experiments/runner-addition/gap-selection/run.py --freeze d814392178a113e8d9e41ebb771e9e2e4d6eb0aa --output /tmp/gap-selection-primary.json
timeout 120s python experiments/runner-addition/gap-selection/verify.py --input /tmp/gap-selection-primary.json --output /tmp/gap-selection-verification.json
timeout 120s python experiments/runner-addition/gap-selection/run.py --freeze d814392178a113e8d9e41ebb771e9e2e4d6eb0aa --output /tmp/gap-selection-replay.json
cmp /tmp/gap-selection-primary.json /tmp/gap-selection-replay.json
```

Output paths refuse overwriting existing artifacts; choose unused output paths
when reproducing again. The committed original outputs remain available for comparison.
Exactly one primary replay was run, and its bytes match.

Artifacts: [results](results/RESULTS.json), [verification](results/VERIFICATION.json),
[replay](results/REPLAY.json). Result SHA-256:
`b96cac4b997fc83a8a6de0449b83e819b6d149b38a23c3262c100f46e0c9adc6`.
