# Separate proof review: transfer to a different supporting boundary

September 29 maintainer date / September 30, 2026 UTC. This is an internal
AI proof/design review, separate from the geometry and physical reviewers.
It is not blind replication, external human review or formal certification.
The preliminary sections below were written before target outputs were
available. No target screening, clipping, contact enumeration or recovery was
performed for this review.

Frozen protocol SHA256, read from disk:
`2ea70d567b25185bbd3bf48b4b53fe78d022e0c70fb9dcdc2f8695ebf8f2be0b`.
Declared source head: `d37865cc7aca3b6092466b986de6afcd9385b9d2`.
INPUTS.json was not yet present at the first preliminary read; its pin
verification is therefore a later execution obligation, not asserted here.

## 1. What this transfer asks

The input changes the ninth moving row from (102,50) to (78,50), while
retaining the 36 supplied eight-row source records and closed threshold 1/8.
The chosen identity is

    (78,50) - (6,2) = 24(3,2) = 8*3(3,2).

On a source where 3x+2y=m+1/8, the new raw value exceeds that of row (6,2)
by the integer 24m+3. On a source where 3x+2y=m+7/8, the difference is
24m+21. Thus the sufficient screen's phase and lap argument remains valid.
This changes the supporting core row from (2,1) to (3,2), rather than merely
changing the multiple along the earlier tested progression.

An allowed coefficient identity does not guarantee a retained segment,
positive descending width, an affordable residual rectangle, complete
coverage, or a speed advantage. Those are distinct outcome questions. The
choice is informed and remains inside the screen's allowed identity family;
it is neither blind nor evidence for arbitrary-row portability. No earlier
selected time is presumed to fail for this new row.

The new row strictly dominates every earlier moving row for positive p,q.
The previous collision domain therefore stays unchanged: ten distinct total
speeds exactly when p!=q and p!=2q. The two excluded primitive directions
remain repeated-speed auxiliaries. The question concerns one safe time for
the stationary reference, not every runner as reference, an optimum or the
complete safe set.

## 2. Data binding and inherited operations

The imported prior bind function must consistently change hybrid TARGET and
ROWS, bounds.__defaults__, query.__defaults__, and physical ROWS/ADDED. Python
captures default arguments when functions are defined; changing TARGET alone
would leave recovery tests pointed at the old row. The query defaults must
preserve opened=False and prepared=None. Screen and full clipping receive the
target explicitly, and the compiler receives explicit adapted rows.

Equal before/after source hashes plus exact code-object identity establish
unchanged function bodies. The recorded global/default bindings are needed
as well, since unchanged bodies do not imply unchanged runtime inputs. The
old-target regression must compare the complete previous hybrid and full
records and both sets of 24 physical dispatches. It does not authorize an
old benchmark or new physical cases.

Removing the preceding orchestration's special assertion about speed 560 at
time 9/40 is an appropriate declared data/output adaptation. It must not alter
source-class kernels, ranking, screening, stopping order or dispatch rules.
The new hybrid must be constructed before the full baseline, so later full
contacts cannot guide its source or witness selection.

## 3. Source-relative exactness, including degenerate projections

For a fixed supplied segment Z(s), s in [0,1], define

    H(s)=Qx(s)-Py(s),   U(s)=(78,50) dot Z(s).

Full clipping followed by integer contact, and integer contact followed by
new-row phase testing, both seek the set of s for which H(s) is integral
and U(s) belongs to some closed band [m+1/8,m+7/8]. Intersections commute;
the required implementation cases remain:

- Nonconstant H: enumerate all integers between its exact endpoint extrema.
  Each integer determines one source parameter, and floor(U) is the only
  possible safe lap because 0<1/8<7/8<1.
- Constant integral H: intersect the source with every possibly meeting
  new-row band, including singleton intersections and equality endpoints.
- Constant nonintegral H: the source has no orbit contact.
- Singleton source: its one point remains a valid closed candidate if both
  conditions hold.

The conservative preflight bound is the sum over source/direction pairs of
the integer-H count times max(1, possible-lap count). It dominates both the
point and constant-projection branches but is not the actual first-success
work. A bound above 4,096 is a scope stop, not exhausted search. A completed
NO_SOURCE_CONTACT result is exhaustion only within the supplied source class,
not physical nonexistence or a conclusion about richer parent interiors.

Open-original-source recovery is a separate endpoint-deletion diagnostic;
singleton sources are deleted by its declared convention. A singleton's
mathematical relative interior is itself. New-row phase bands remain closed,
so an interior source parameter need not give strictly safe phases. No open
diagnostic contact replaces the retained closed-rule output.

## 4. Changed leaders and the residual-union argument

For any selected safe descending segment with endpoint differences
alpha=x1-x0>0 and beta=y0-y1>0, the H projection has width alpha*Q+beta*P.
Width at least 1 guarantees an integer contact, including closed equality.
Every potentially uncovered positive primitive direction therefore lies in
the finite set

    R = {(P,Q): gcd(P,Q)=1, P,Q>0, alpha*Q+beta*P<1}.

The enclosing rectangle is P<=ceil(1/beta)-1 and Q<=ceil(1/alpha)-1.
Its size must pass the unchanged 400 cap before enumeration. No prior leader,
47-direction residual table, fallback or exception list can be inherited
merely because the threshold and supplied source class stayed fixed.

If the screen and full compilers have different leaders, use their newly
completed residual sets R_screen and R_full. Outside their union, both
leaders have width at least 1 and give contacts. Inside the union, compare
actual hybrid dispatch against ALL full-candidate contacts; selected times
may differ without a coverage mismatch. Each enclosing rectangle has at most
400 pairs, so the union has at most 800 under completed reductions.

For a global comparison to the full supplied source class, full clipping
must also report PASS, and hybrid recovery must not stop on its cap. A full
compiler status alone does not establish that clipping exhausted all source
lap bands. This explicit full-clipping guard is required in the orchestration.
A completed source-class miss can still be part of a valid global comparison;
global comparison does not mean either method necessarily covers everything.

The unchanged greedy compiler runs until every residual is covered or no
candidate has positive gain. With a completed contact matrix, its uncovered
set is therefore the screened candidate class's uncovered set. Retaining all
screened contacts alongside compiled dispatch is still useful: it keeps the
class/operation distinction explicit and exposes any implementation mismatch.

When a finite reduction is unavailable, reached contacts may be compared on
their declared finite domain, but not promoted to a global conclusion. A
missing descending leader does not imply an empty safe class. Scope limits,
invalid records, missing certificate and exhausted contact search need their
separate statuses; the full clipping scope status must survive any derived
NO_DESCENDING_SEGMENT from an empty wrapper input.

## 5. Dispatch, diagnostics and costs

Every recovered point must retain its primitive direction, source identity,
all nine lap labels, local parameter and original edge parameter. Its map
back into the corresponding full-clipped source/lap record must agree. These
are direction-keyed points, not an automatically enlarged global segment menu.
The existing Bezout inverse then recovers physical time, with gcd scaling,
reflection and all physical laps verified on the declared controls.

A diagnostic full witness for the first primary full-hit/hybrid-miss pair
must remain diagnostic; inserting it would change the frozen hybrid. Such a
witness would refute a claim of physical nonexistence but need not explain
every source-selection failure. Parent-interior search is outside this trial.

If the screen leaves no uncovered direction, recovery may complete with zero
preflight work, and the zero-budget diagnostic may correctly PASS. An assertion
that zero budget must fail would improperly inherit an earlier outcome. Open
source diagnostics likewise operate only on the newly reached uncovered set.

The benchmark gate requires a complete hybrid certificate and a complete full
certificate with completed clipping, all under unchanged caps. If either
method lacks that guarantee, timing is NOT_TRIGGERED. Bounded cost counts are
still reportable with their reached scope. Supplied discovery, endpoint
validation, screening, clipping, matrix entries, preflight and actual recovery
operations must remain separate; unlike counts are not interchangeable units.

If triggered, the old timing function performs one warmup per method and up
to 11 alternating pairs under the 30-second check between pairs. Preserve
all results, including an early timing scope stop. Validation, native traces,
preflight and failed contact tests remain included. Setup, provenance,
diagnostics, audits and writes remain excluded. One input cannot establish
general complexity, general portability or a universal runtime improvement.

## Preliminary finding

PASS for the frozen design, subject to the stated input-pin verification and
explicit completed-clipping guard. The changed boundary supplies a valid
possible screening mechanism, with leader availability, residual geometry,
recovery outcome and measured cost still unassessed. Final output review will
be appended after execution. General arguments retain internally reviewed
proof-candidate status.

## 6. Final adapter and orchestration review

The final review read transfer.py, INPUTS.json, adapter.json, regression.json,
screen.json, hybrid.json, full.json, audit.json, summary.json and timing.json.
All 18 input SHA256 pins now match the supplied local files. The protocol hash
is unchanged. Both old- and new-target adapter records contain equal
before/after source-hash maps and preserve exact code-object identity for the
14 tracked functions. The active globals and captured defaults change from
(102,50) to (78,50) consistently; physical rows change with them.

The previous-target regression compares the entire hybrid record (3,689
scalar fields), full record (30,125 fields), and both 24-control dispatch
sets (4,076 fields) exactly. The new orchestration constructs hybrid before
full, then runs the separate screen diagnostic and audits. The former
old-time-failure assertion is absent, as declared, without replacing it by
an invented failure for this row. No imported algorithm is changed.

The final global-scope guard explicitly requires both completed reductions,
full clipping PASS, and recovery status COMPLETE_EXCEPTION_RECOVERY or
NO_SOURCE_CONTACT. It excludes a recovery scope stop. Full and screened
candidate-class contacts are recorded separately from actual dispatch, and
the first full-witness diagnostic is never fed back into the hybrid. The
complete-versus-complete benchmark gate additionally requires full clipping
PASS. These meet the preliminary review's guard obligations.

## 7. Reached closed coverage

The target screen finds the declared (3,2) identity and retains ten of the
36 source records, including two singleton records. Eight are descending.
The first-ranked leader is P4:E0-1:K3:L4:M54, with endpoints
(29/72,11/24) and (35/72,1/3). Its line and projection are

    3x+2y=17/8,
    H(x)=(Q+3P/2)x-17P/16,
    width=Q/12+P/8=(2Q+3P)/24.

The width tail is therefore 2Q+3P>=24; its strict complement is
2Q+3P<=23. The new completed finite reduction records 28 primitive directions
inside the 7-by-11 rectangle, size 77, under the unchanged cap of 400.
This differs from the earlier leader and 47-direction domain as intended.

The screen's five selected records, in operational order, are:

| Role | Record | New torus lap |
| --- | --- | ---: |
| Leader | P4:E0-1:K3:L4:M54 | 54 |
| First fallback | P3:E0-3:K3:L3:M48 | 48 |
| Second fallback | P0:E1-3:K1:L2:M22 | 22 |
| Third fallback | P1:E0-3:K1:L3:M28 | 28 |
| Singleton fallback | P4:E0-1:K3:L5:M54 | 54 |

The leader misses nine residual directions. The first fallback adds six;
the next two add (1,2) and (3,1); the final singleton (3/8,1/2) adds (1,4).
The recorded final uncovered set is empty. The singleton is an ordinary
candidate in the closed screen menu, not a direction-keyed point recovered
by the hybrid's exception procedure. In particular, this output is a
five-record closed menu, containing four nondegenerate segments and one point.
This describes the emitted menu, not a necessity for the whole screened
class: the stored (1,4) comparison also lists the nondegenerate screened
record P7:E0-1:K4:L8:M79, as well as both P4 singleton provenance records.
The result therefore does not show that singleton records are physically
necessary or that a different nondegenerate menu is impossible. No reranking
or replacement-menu trial was performed.

The full baseline finishes all 81 source/lap attempts under its cap of 256,
producing 81 records, of which four are singleton and 42 descending. It
selects the same leader and the same complete 28-direction residual domain,
but its five-record menu uses different later fallbacks. Agreement on a
leader or coverage need not mean agreement on the selected menu or times.

Every screened record is an identical full member. All 28 union comparisons
find screened-class contacts, hybrid dispatch and full-class contacts, with
no screen-class lost pair or dispatch mismatch. Outside this union both safe
leaders guarantee contacts by width. Thus the ALL_POSITIVE_PRIMITIVE_DIRECTIONS
scope is justified by its completed reductions and clipping, rather than by
extrapolating physical controls. The screen alone supplies complete closed
selected-reference coverage; recovery is not needed on this target.

Both methods pass all 24 controls, comprising 20 primary and four
repeated-speed auxiliaries; every hybrid control takes the SCREEN_MENU route.
The audit also retains hybrid physical witnesses on the 28 union directions.
The standard integer-contact/Bezout inverse and gcd scaling connect this
primitive-domain certificate to positive integer p,q. The ten-distinct-speed
claim retains p!=q and p!=2q.

## 8. Empty diagnostics and honest costs

The hybrid recovery record has empty exceptions, queries, uncovered list and
preflight rows, with every recovery count zero. COMPLETE_EXCEPTION_RECOVERY
here means completion of an empty task. It provides no new target evidence
for point-phase rejection, constant-H handling, source traversal, or recovery
after screen loss. Those branches retain their earlier proof/regression scope.

The open-original-source diagnostic also receives the empty exception list.
Its COMPLETE_EXCEPTION_RECOVERY status is vacuous: it does not test opening
the five-record menu, deleting the selected singleton, or recovering any
direction after endpoint deletion. No open-coverage or strict-loneliness
conclusion follows. Zero-budget preflight correctly reports PASS with work
bound zero; this is not a target test of budget rejection. The full-source
lost-witness diagnostic is NOT_TRIGGERED because no triggering miss exists.

| Recorded operation | Hybrid | Full baseline |
| --- | ---: | ---: |
| Supplied source records | 36 | 36 |
| Inherited endpoint/band validations | 576 | 576 |
| Materialized safe candidate records | 10 | 81 |
| Descending candidates | 8 | 42 |
| Rectangle pairs | 77 | 77 |
| Primitive residual directions | 28 | 28 |
| Residual contact-matrix entries | 280 | 2,268 |
| Selected menu records | 5 | 5 |
| Recovery preflight projections / raw ranges | 0 / 0 | 0 / 0 |
| Actual recovery source / H / phase / band tests | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Full source/lap attempts | 0 | 81 |

Hybrid screening additionally uses 48 coefficient-pair tests and 36 boundary
checks. These are separate operation types, not interchangeable work units.
The source discovery cost remains supplied preprocessing. No result here
establishes that ten retained records preserve every safe point represented
by the 81 full records; the supported comparison is contact existence for
positive primitive directions.

The complete-certificate timing gate is satisfied. All 11 alternating paired
rounds finish, after one warmup per method. Recorded medians are 8.892101 ms
hybrid and 34.464508 ms full; the median paired full/hybrid ratio is
3.9165826601469744. Every pair favors hybrid in the recorded Python 3.12.14 /
Linux x86_64 environment. The ratio of medians and median of ratios are
different statistics. Included/excluded work follows the frozen scope.
These are measurements for this row, corresponding to k=3 in the new
progression. They do not establish a ratio, runtime bound or compiler-cost
law for other k. No timing or target computation was repeated for this review.

## 9. Proposed analytic continuation and CC checkpoint

A parameterized fixed-menu certificate is a well-motivated next analytic
question. Let u_k=(6,2)+8k(3,2) for positive integer k. On a retained source
with (3,2) raw value m_c+epsilon, epsilon in {1/8,7/8}, a proposed new lap is

    m_u(k)=m_(6,2)+8k*m_c+8k*epsilon.

The last term is k or 7k, hence integral. Subtracting this lap would leave
exactly the safe (6,2) phase at every point on that source. The selected menu's
recorded boundary data suggest the respective lap formulas 3+17k, 3+15k,
1+7k, 1+9k and 3+17k in the operational order above; they specialize to this
run's 54,48,22,28,54 at k=3.

The proposed next certificate should pin the five source records, verify
these symbolic equalities and all inherited bands, and carry their already
fixed contact geometry and physical inverse for every declared k. Its domain
and distinctness conditions must be explicit. That would be a fixed-menu
sufficiency argument, not a classification of every admissible coefficient
row, full safe set, or optimal menu. Additional relations at other k could
change a fresh compiler's candidate set or choices; identical automatic
outputs should not be claimed merely from the fixed-menu identity. Runtime
and full-clipping caps also do not transfer from the single measured input.
No further k has been tested, and this review does not publish the proposed
parameterized extension as a completed classification.

The CC checkpoint separates four facts now visible in one trial: a supported
coefficient identity exists; its changed boundary retains a useful descending
leader; this closed menu already covers the entire reduced domain; physical
recovery succeeds. Here recovery's source-class completeness is inherited but
unused. Empty diagnostic successes must not collapse into empirical evidence
about the branches they never exercised. The retained singleton, exact laps,
leader geometry, menu order, new residual domain and raw statuses are material
to understanding why this transfer succeeds.

## Final finding

PASS for the inherited data/default adapter, new orchestration, completed
closed coverage, residual-union comparison, explicit empty diagnostics and
bounded cost/timing interpretation. No production correction was needed in
the reviewed target run. General arguments remain internally reviewed proof
candidates. This reviewer performed no new target search, contact enumeration,
coefficient trial or timing run.
