# Compatibility Calculus: recover contacts only where the screen fails

September 29, 2026 local / September 30 UTC. Source:
54f9a2ea0a654afc9326668e4c3bc92e31f31567.

**Result:** the frozen hybrid recovers all three directions lost by the
boundary-phase screen for row (54,26). It keeps the screen's original
three-segment menu and adds three direction-specific point witnesses.
Recovery visits 11 supplied sources and checks three integer contacts and
three new-row phases. It never materializes the 61 full clipped candidates.
The unchanged screen still builds its five-candidate, 235-entry contact table.

This is a development repair of a known failure, not a held-out portability
test or a new existence result: the previous full compiler already covered
this family. The new evidence concerns a different discovery operation,
preserved coverage and measured implementation cost.

**Status:** finite rational outputs are OBSERVED / REPRODUCED after the
recorded reproduction. Source-relative completeness and uniform coverage
remain HYPOTHESIS / internally reviewed proof candidates. AI implementation
and separate structured reviews are disclosed; they are not blind, external
human or formal certification. No novelty, optimum, arbitrary ten-runner or
all-reference claim is made.

## Scope and frozen change

The speeds are

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,54p+26q),
\]

with positive integer p,q, common start, stationary reference and closed
threshold 1/8. There are ten distinct speeds iff p!=q and p!=2q. Auxiliary
repeated-speed directions remain labelled and checked separately. Threshold,
runner count, target row, screen, leader selection and fallback menu are
unchanged. The 36 previously discovered eight-row safe segments are supplied
preprocessing; their production cost has not disappeared.

The [protocol](../reviews/2026-09-29-cc-hybrid-recovery/PROTOCOL.md) was frozen
before hybrid execution, SHA256
`eb3a894b8d2c411b177ef26f3916a0138adad975f9848a590aaaf1ee11723ccf`.
Seven source files are pinned, including imported algorithms and archived
comparison records. Archived answers are read for audits only after the hybrid
construction. Known prior outcomes informed the experiment; this separation
does not make it blind.

## Change the order of intersection

Full discovery first clips each source by the new runner's safe lap bands,
then asks which primitive directions reach the resulting segments. The hybrid
first identifies the screen's uncovered primitive directions. For each one,
it intersects the original sources with the integer-orbit condition

\[
H=Qx-Py\in\mathbb Z,\qquad (P,Q)=(p,q)/\gcd(p,q),
\]

then checks the new runner only at those contacts. Sources, integer H values
and, where needed, lap bands have frozen numerical ordering. Each direction
stops at its first accepted contact; recovered points are not injected into
a new greedy menu or reused to cover other primitive directions.

For a source A+s(B-A), a nonconstant H fixes one exact parameter for each
integer in its endpoint range. Set m=floor(54x+26y) and test whether the
fractional phase lies in [1/8,7/8]. Constant integer H instead retains a whole
source interval, requiring new-row lap-band intersection. Constant noninteger
H has no contact. Singleton sources and equality endpoints remain eligible.

The actual three recoveries use the nonconstant branch. Separate predetermined
kernel fixtures exercise unsafe-then-safe contact order, constant integer H,
constant noninteger H and a singleton. Those fixtures are not runner-family
experiments and do not turn unvisited target branches into target evidence.

## The source-relative completeness argument

Let S be any supplied closed safe source segment, U(x,y)=54x+26y and
B the union of its closed new-row bands [m+1/8,m+7/8]. For a fixed primitive
direction, full clipping and contact-first recovery both test

\[
S\cap\{Qx-Py\in\mathbb Z\}\cap U^{-1}(B).
\]

The order of these intersections does not change nonemptiness. The affine
cases above exhaust the integer contacts; lap ranges exhaust the new bands.
Consequently the recovery search, when completed, finds a witness exactly
when the full appended source class has one for that direction. It need not
choose the same witness or preserve the entire safe set.

The inherited screen leader is

\[
y=7/8-2x,\quad33/104\le x\le3/8,
\]

with projected width 3(Q+2P)/52. It covers Q+2P>=18. The remaining 47 positive
coprime directions have Q+2P<=17. The screen menu covers 44; the exact three
exceptions are recovered below. This gives the conditional uniform family
certificate. More generally, if this finite reduction and every recovery
search complete, the hybrid preserves the full source class's coverage even
when a pair is reported uncovered. A scope stop is not an exhaustion result.

## Recovered exception witnesses

| Primitive (P,Q) | Supplied source | Point (x,y) | H | New torus lap | Primitive time |
| --- | --- | --- | ---: | ---: | --- |
| (1,2) | P0:E0-1:K1:L2 | (1/8,1/4) | 0 | 13 | 1/8 |
| (1,4) | P1:E0-1:K1:L4 | (1/8,1/2) | 0 | 19 | 1/8 |
| (5,1) | P0:E0-1:K1:L2 | (1/8,9/40) | -1 | 12 | 9/40 |

For original (p,q)=d(P,Q), divide the primitive time by d. The first two
points are source endpoints. The third is interior to its supplied source:
local parameter 1/5 maps to original parent-edge parameter 4/5. All three
maps and all inherited laps are retained. Their minimum physical separation
is 1/8. For (10,2), the third witness scales to 9/80.

The (5,1) example makes the inverse map consequential. Its point is
(1/8,9/40), but the physical time is 9/40, not its x coordinate. The new
runner has speed 296, so its physical lap is 66 and phase 3/5; the torus lap
is 12. A reduced coordinate or phase alone would lose these distinctions.
The full greedy menu selects a different safe time, 31/136, at (5,1).
Preserving the one-witness answer does not require preserving the selected
time or every available witness.

The dispatch output has two kinds of record: the original three-segment
screen menu for nonexception directions, and three keyed points for the
exception rays. It is not a six-segment universal menu. The retained audit
also keeps all five screened candidates and their complete contact table.

## Work and measured timing

| Count | Hybrid | Full discovery |
| --- | ---: | ---: |
| Supplied eight-row source segments | 36 | 36 |
| Source endpoint band validations | 576 | 576 |
| Coefficient-pair tests | 48 | 0 |
| Source boundary tests | 36 | 0 |
| New-row full clipping lap attempts | 0 | 61 |
| Materialized new-row segment records | 5 | 61 |
| Residual candidate/contact entries | 235 | 2,867 |
| Recovery preflight projections | 108 | 0 |
| Recovery preflight raw ranges | 108 | 0 |
| Actual recovery source visits | 11 | 0 |
| Actual recovery integer H tests | 3 | 0 |
| Actual recovery point-phase checks | 3 | 0 |
| Actual recovery parallel-band tests | 0 | 0 |

Preflight covers all 3x36 source/pair combinations even though early stopping
visits only 11. It bounds 17 integer contacts and 33 work units, below the
frozen 4,096 cap. These work units are a conservative search bound, not a sum
of equivalent operations or a runtime estimate. The actual three H tests
and three phase checks describe the same three contacts at two stages.

The frozen benchmark performs one warmup per method and eleven alternating
paired measurements, from the same parsed sources. Median computation times
are **10.074 ms hybrid** and **37.902 ms full**; median paired full/hybrid
ratio is **3.784**. All eleven pairs favor the hybrid in this environment.
Both measurements include source validation and native traces, and exclude
earlier source discovery, imports, input parsing, physical controls, audits
and file writes. This is evidence of a faster implementation on this input
and machine, not a general complexity improvement or a free preprocessing
claim. Every individual timing and environment detail is preserved.

## Endpoint diagnostic and scope

Opening the original source segments still permits all three exception
directions, using alternative source records for (1,2) and (1,4). The first
two closed-rule witnesses being endpoints does not make endpoints physically
necessary for those directions. The diagnostic preserves the new-row safe
bands as closed: it does not establish strict separation greater than 1/8.
Opening original sources also differs from opening every newly clipped
candidate. Singleton sources are empty under the diagnostic convention.
No open-source witness changes the frozen closed output.

## Validation and CC checkpoint

The screen certificate equals the archived restricted certificate exactly;
the regenerated full certificate equals its archived counterpart exactly.
All three recovered points belong to full candidates with matching labels
and original parameters. Every one of the 47 residual dispatches and all
24 physical controls succeeds. Twenty controls have ten distinct speeds;
four are repeated-speed auxiliaries. Three separate reviews and exact
reproduction are recorded in the linked package.

The separate geometry reconstruction matches 30,427 scalar fields, including
the complete preflight and recovery traces, archived certificates and kernel
fixtures. Physical review checks direct speeds/phases and both lap systems
with an independent serialized dispatcher. Its supplementary parent-geometry
input is pinned separately from construction inputs. Exact reproduction checks
all five deterministic output files byte-for-byte against seven construction/
comparison pins and one supplementary review pin. The production selector
also reproduces all 71 declared dispatch records after JSON loading. The
benchmark is preserved without being rerun.

Compatibility Calculus here carries a supported question, compatible local
constraints, an explicit richer source, a recovery operation and a physical
inverse. The segment-only shortcut was inadequate for complete discovery.
A segment menu plus direction-specific exceptions is adequate for this
one-witness task under the reviewed conditions. It omits other safe points,
optimal values and alternative selectors; source availability is a recovery
route, not a losslessness claim. The inherited affine-segment/integer-orbit
framework remains useful, with attribution pinned in the literature note.

**Next proposed:** freeze a different tenth-row input and run the same hybrid
rule and budgets against full discovery. That tests transfer beyond the known
repair, including whether recovery work stays small. Select the input before
its outcomes and preserve failures or scope stops; do not tune the rule after
seeing them. No new target has run. The coefficient-aware old/new selector
dispatcher remains a separate pending task.
