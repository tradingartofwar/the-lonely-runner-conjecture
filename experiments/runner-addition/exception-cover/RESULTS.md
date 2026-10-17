# A working exact constructor that searches only exceptions

October 17, 2026. **OBSERVED:** four exact family comparisons and seven supplied
interval controls. **HYPOTHESIS / proof candidates:** the correctness and all-r
arguments in [DESIGN.md](DESIGN.md) pending independent review. AI materially
generated the code, arguments and report; both verification paths have the same
AI author. No novelty or general LRC claim is made.

The constructor is implemented in [constructor.py](constructor.py). It queries
the required leader, searches only its exceptions, reuses prior contacts when
more coverage is needed, and returns a minimum menu plus a guarded witness
dispatcher. A shared repair time is optional. The complete four-family
certificates are available in [CERTIFICATES.json](results/CERTIFICATES.json).

## Family results

Use common-start speeds 0, the eight core speeds
`(p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q)`, and an added positive integer r absent
from the core. Reference is 0, n=10 and d=1/10. All four pairs are primitive,
so the original physical period [0,1] applies; two pairs go beyond p=1.

| Pair | Core components | Cutoff R | Finite cases | Leader exceptions F | Minimum IDs including leader | Fixed repair time |
| --- | ---: | ---: | ---: | --- | --- | --- |
| (1,20) | 64 | 42 | 36 | {3,6,9} | {3,17} | 201/1630 |
| (1,21) | 64 | 48 | 41 | {3,6,9,37,40} | {7,16} | 41/210 |
| (2,21) | 74 | 53 | 46 | {3,6,9,38,41} | {1,29} | 101/1740 |
| (3,20) | 68 | 46 | 40 | {9,18} | {1,4} | 31/490 |

The leaders have IDs 17,16,29,4 respectively. The constructor matches both the
minimum cardinality and lexicographic choice of the full exact reference in
every case. All 163 complete child-safe sets are nonempty. Each family uses
the lazy two-component step; **none naturally reaches the residual DP fallback**.
The optional search finds a shared repair point in each selected repair interval.

For each row, use the stored repair time for r in F and first contact on the
leader otherwise. The complete finite domain covers admissible r<R; the width
argument covers r>=R. These give all-admissible-r proof candidates for the
selected stationary reference. The minima require the predetermined widest
component. No minimum among menus omitting it, other-reference result, or
arbitrary-pair theorem has been established.

## What the implementation changes

| Pair | Leader contacts | Lazy repair contacts | New residual contacts | Total constructor contacts | Full reference contacts |
| --- | ---: | ---: | ---: | ---: | ---: |
| (1,20) | 36 | 12 | 0 | 48 | 2,304 |
| (1,21) | 41 | 28 | 0 | 69 | 2,624 |
| (2,21) | 46 | 9 | 0 | 55 | 3,404 |
| (3,20) | 40 | 4 | 0 | 44 | 2,720 |
| Total | 163 | 53 | 0 | **216** | **11,052** |

These columns count the same first-contact primitive. An unqueried entry remains
absent, rather than being mistaken for a failure. The optional shared-point
search adds 15 point predicates, accounted for separately. The core construction
uses 1,445 input bands and returns 270 components; the reference then rechecks
those cores and computes complete child sets. Verification and replay add work.
The study actually performs the full reference work and has not measured an
end-to-end runtime advantage.

Let N be the finite domain size, M the component count and f=|F|. Unique
constructor contacts are bounded by `N+(M-1)*f`, rather than the full matrix's
`M*N`, because all nonleader queries concern exceptions and each pair is cached.
The lazy step can stop earlier. When f=N this bound gives no reduction; the
residual cover problem can still require substantial DP work. Budgets remain
necessary. This is an algorithmic consequence of the stated query discipline,
not a measured general speedup or a claim about intrinsic problem complexity.

The certificate retains 15 exception entries across these families. Dispatching
all 163 finite cases requires 148 new first-contact calls, since exception times
are already stored; the 15 tail controls need 15 more. Every output carries
exact time, component, phases and laps. Certificate construction/storage and
physical checking remain charged, even when dispatch uses a cached time.

## The fallback and failure controls matter

The seven controls are supplied finite interval problems, not complete physical
cores or newly discovered Lonely Runner configurations.

| Control | Verified behavior |
| --- | --- |
| Leader already sufficient | Exact one-component menu |
| Three components with a tie | Residual DP returns lexicographically first minimum {0,1,2} |
| Separate witnesses, no common time | Exact two-menu survives optional NO_COMMON_REPAIR_POINT |
| No supplied component covers a query | NO_SUFFICIENT_MENU identifies speed 3 |
| Zero contact budget | UNKNOWN_BUDGET before any contact; no infeasibility claim |
| Zero DP-transition budget | UNKNOWN_BUDGET after residual completion; no infeasibility claim |
| Zero optional-search budget | Exact two-menu and individual-witness recovery remain valid |

In the three-component control, d=1/3 and D={2,3}. Leader
[1/1000,1/100] fails both speeds. Singleton alternatives at 1/3 and 2/3 cover
speed 2; the singleton at 1/2 covers speed 3. Two minimum menus exist, and the
constructor chooses IDs {0,1,2}. After five lazy repair contacts, residual fill
reuses those five entries and evaluates only one missing contact. Including
the two leader checks, all eight possible contacts are computed once. The DP
uses four states and seven transitions. This verifies fallback, ties, cache
reuse and equality-point retention; it does not show a natural family needs
three components or a contact-count reduction on this control.

In the separate-witness control, leader [53/1000,61/1000] fails 17 and 18 at
d=1/10. The second interval [111/670,19/110] supplies time **111/670** for speed
17 and **31/180** for speed 18, but their surviving pieces are disjoint. The
constructor returns the valid two-menu and both individual times even when
the optional common-point search is empty or stopped by its budget.

This implements the needed distinction: a separate time for each added-speed
case is sufficient. Asking all alternative added speeds to work at one shared
time is an extra convenience, not a condition for accepting the menu.

## Interface, scope and recoverable information

`construct(core, leader, domain, d, cfg)` supports the finite supplied-source
question. Its output records the menu, query trace, missing speeds or budget
status, and a certificate when successful. `dispatch(certificate, r)` returns
time, component ID and the number of fresh contact calls. It rejects nonpositive
speeds, out-of-domain finite requests and, for attached family contexts, repeats
of core speeds. Family contexts are attached by the runner only after exact core
construction and complete finite-domain derivation; the raw finite constructor
does not independently establish that extension.

The compact [certificate export](results/CERTIFICATES.json) is a post-verification
extraction from the frozen results, with their SHA-256 recorded. It adds no new
evaluation. The full results preserve source geometry, all reference contacts
and complete child sets. Recover those sources before asking for every safe
time, optimum, a changed threshold, changed core or another reference. A cached
witness is not transferable merely because its numeric time is still available.

## What this earns next

We now have a working exact constructor and checked fallback rather than only
a comparison of selection policies. The latest family cases still share the
same coefficient template and all stop at two components. That is a limitation
of the evidence, not a reason to assume two always suffice.

**Next proposed:** freeze a small set of eight-speed cores outside the current
p,q construction and use this constructor to test whether two components remain
sufficient with the widest component required. Preserve natural fallback,
no-cover and budget outcomes, and compare with complete event geometry. This
would test the apparent structural pattern, rather than extend the same q
sequence again. No such new domain has been selected or run here.

## Verification and reproduction

Execution freeze: `8a4f84dfd11afa63bbbb32993bc8c63b3acc203f`.
The [manifest](manifest.json) pins 14 files. No frozen code changed after
execution; no execution discrepancy or timeout occurred. Both implementations
use exact fractions and preserve closed endpoints and singleton sources.

Alternate verification checks **4 complete cores, 163 complete child sets,
11,089 reference contacts, 245 constructor contacts, 526 physical witness
records, 296 minimum-search subsets and 6 optional common-point sets**. Counts
include the controls where applicable: the family-only contact counts are
11,052 and 216. Query-order accounting replays the specification using independently
computed event hits; minimum verification uses subset enumeration instead of
the primary DP. DP counters are execution instrumentation. Both algorithms
share the same AI author, so this is not independent human or formal proof review.

All seven controls pass their declared outcomes, including intentionally
UNKNOWN and no-cover results. Exactly one primary replay is byte-identical.
Use unused output paths from the repository root:

```sh
timeout 120s python experiments/runner-addition/exception-cover/run.py --freeze 8a4f84dfd11afa63bbbb32993bc8c63b3acc203f --output /tmp/exception-cover-primary.json
timeout 120s python experiments/runner-addition/exception-cover/verify.py --input /tmp/exception-cover-primary.json --output /tmp/exception-cover-verification.json
timeout 120s python experiments/runner-addition/exception-cover/run.py --freeze 8a4f84dfd11afa63bbbb32993bc8c63b3acc203f --output /tmp/exception-cover-replay.json
cmp /tmp/exception-cover-primary.json /tmp/exception-cover-replay.json
```

Artifacts: [complete compact JSON results](results/RESULTS.json),
[verification](results/VERIFICATION.json), [replay](results/REPLAY.json).
Result SHA-256: `6d9d2a17e22729c3be82833d263c9ada0a567d654dc0bbac4fcc5eb81433bb81`.
