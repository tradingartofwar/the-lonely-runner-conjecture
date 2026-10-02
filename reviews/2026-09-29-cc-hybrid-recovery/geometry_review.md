# Separate hybrid recovery geometry review

**PASS — 30,427 scalar fields agree.** This is a known-answer development
review of the frozen `(54,26)` repair. It imports no production code, makes no
new target or threshold trial, and does not rerun the benchmark. It is internal
AI arithmetic review, not blind, external human or formal verification.

| Compared record | Scalar fields |
| --- | --- |
| Complete hybrid construction, preflight and closed recovery | 3,658 |
| Audit geometry, open recovery, fixtures and dispatch | 3,807 |
| Complete summary and counters | 125 |
| Archived restricted certificate | 2,046 |
| Archived full certificate | 20,791 |
| **Total** | **30,427** |

The review reconstructs the screen and compiler, rather than accepting their
chosen records as input. It uses only the pinned 36 eight-row safe sources
until construction is complete; afterward it checks the archived restricted
certificate and independently regenerates the full certificate for comparison.
Every source's eight labelled bands is checked at both endpoints: 576 checks.
All inherited/ninth labels and mapped original-edge parameters are retained.

## Independent contact check

The review checks each visited query with a differently ordered calculation:
first intersect the new safe lap bands with the source parameter, then project
each surviving interval and enumerate integral orbit contacts. It sorts these
contacts by `H`, lap and parameter to identify the canonical first witness.
Separately it reconstructs the declared contact-first trace, including failed
tests, and requires exact agreement with that band-first witness or exhaustion.
No production query or clipping function is imported.

For nonconstant `H(s)`, each integer fixes a unique parameter. Testing its
new phase is equivalent to membership in one of the disjoint closed safe lap
bands. For constant noninteger `H`, neither order can find a contact. For
constant integer `H`, the problem reduces to nonemptiness of the new lap-band
intersection with `[0,1]`; increasing lap order and its least surviving
parameter implement the frozen convention. A source point is checked as a
closed geometric point, and has no open geometric interior. These cases
establish the contact equivalence without assuming two separately chosen
witnesses coincide.

## Preflight, recovery and dispatch

The 108 missing-pair/source combinations yield 108 charged projections and
108 new-row raw ranges. Their integer-H upper bound is 17, and the declared
overestimate of contact work is 33, below 4,096. Every preflight row and bound
matches production, including sources never reached after early stopping.

Closed recovery visits 11 sources and performs three H tests and three point
phase tests, with no parallel-band tests on this target. Its direction-specific
records are:

| Primitive pair | Source | Local parameter | Original edge parameter | Point | H | Ninth lap |
| --- | --- | --- | --- | --- | --- | --- |
| `(1,2)` | `P0:E0-1:K1:L2` | `1` | `1` | `(1/8,1/4)` | `0` | `13` |
| `(1,4)` | `P1:E0-1:K1:L4` | `1` | `1` | `(1/8,1/2)` | `0` | `19` |
| `(5,1)` | `P0:E0-1:K1:L2` | `1/5` | `4/5` | `(1/8,9/40)` | `-1` | `12` |

All three belong to the independently regenerated full candidates with equal
inherited/new laps and correct original parameters. They remain exception
points keyed by primitive direction; the review does not treat them as reusable
global segment candidates. Dispatch geometry agrees on every one of the 47
residual directions and all 24 frozen physical control inputs, including gcd
scalings. The separate physical review checks physical times, physical laps,
phases and reflection; those fields are excluded from this geometric dispatch
comparison.

The original screen leader still covers every positive primitive direction
with `Q+2P>=18`, and its complete finite complement has 47 directions. The
unchanged menu handles all but the three listed misses. Successful primitive
dispatch repairs those three rays and therefore completes the conditional
uniform construction. This concerns one witness for the specified stationary
reference and structured family, not all safe times, optimum values or general
ten-runner inputs. Ten distinct speeds still require `p!=q` and `p!=2q`.

## Endpoint and kernel branches

The open-source diagnostic also recovers all three directions. It visits 47
sources and performs eight H/point-phase tests. The first two closed witnesses
are source endpoints, so opening forces different sources and points; the
third already lies in its source interior. This is an endpoint diagnostic,
not a replacement for the retained closed dispatch.

All four frozen synthetic kernels and every trace field agree: unsafe first
point followed by a safe later point; constant integral projection with a
positive-length safe band; constant nonintegral projection with no contact;
and a safe singleton. These are query-kernel fixtures, not additional physical
runner families. The zero-budget check returns `RECOVERY_SCOPE_LIMIT` with
zero source queries or recovered exceptions. Neither resource stop nor
source-contact exhaustion is a physical nonexistence certificate.

## Evidence, cost and execution record

The saved result is a successful development repair of an already diagnosed
screen loss. Full source geometry was supplied, and the preflight evaluated
all 108 source/pair combinations even though recovery visited only 11 sources.
These operations, screen work, compiler contacts and earlier source discovery
remain distinct costs. This arithmetic review gives no timing or complexity
claim. The production timing run was not repeated or used as correctness
evidence. No richer parent search, predicate expansion, additional row or new
threshold was tested. Universal arguments remain internally reviewed proof
candidates.

The first complete comparison stopped on synthetic-fixture input serialization:
the review represented integer endpoint literals as exact fraction strings,
while production retained JSON integers. The fixture output representation was
adjusted to preserve the original literals; internal calculations remain exact
fractions. No arithmetic, recovery, ordering, fixture values or target result
changed. The subsequent full comparison passed. This was a review-harness
correction, not a production correction.

Reproduction from the repository root:

```sh
python3 reviews/2026-09-29-cc-hybrid-recovery/geometry_review.py > /tmp/cc-hybrid-geometry.json
cmp /tmp/cc-hybrid-geometry.json reviews/2026-09-29-cc-hybrid-recovery/geometry_review.json
```

The compact JSON retains hashes, field counts, preflight/actual counters,
exception records and kernel evidence. Complete traces remain in the compared
production artifacts, whose identities are pinned in that report.
