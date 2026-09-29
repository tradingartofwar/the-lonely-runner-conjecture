# Frozen nine-runner joint transfer — September 29, 2026

Frozen before target clipping, enumeration or controls. Initial live source
commit eee207819d61043e6f49cc44cba7ed9472865a91. This is an informed combination
of two previously successful added rows, not a blind portability test.

## Question and scope

Use core rows (1,0),(0,1),(1,1),(2,1),(3,1),(3,2), then (6,2),(3,8).
For positive integers p,q, speeds are (0,p,q,p+q,2p+q,3p+q,3p+2q,
6p+2q,3p+8q). Nine distinct speeds require p!=q and p!=2q. Common start,
stationary selected reference, one exact witness; no optimality or all-reference
claim. Equality is safe. Repeated-speed directions are labelled auxiliaries.

Stage A uses threshold 1/8 and the pinned 24 parent floor edges. Jointly clip
both added rows at the SAME edge parameter, retaining both integer laps.
If this produces a complete primary-domain guarantee, stop: it also implies
1/9 safety. Otherwise run exactly one Stage B at 1/9, rebuilding the six-form
floor geometry from its defining bands. A failed 1/8 test is not a failed
nine-runner loneliness test. Never substitute two separate witnesses.

## Frozen geometry, selection and budgets

Before either target run, reproduce the archived (5,2),(6,2),(3,8)
geometry/coverage certificates, excluding provenance wrappers. Import the
unchanged single-row clipper and coverage compiler for these regressions.
Record all input hashes and check their Git blob identities against live source.

For each oriented source edge, compute each added lap range from endpoint
extrema: ceil(min(raw)-(1-z)) through floor(max(raw)-z). Enumerate their Cartesian
product and intersect the closed affine parameter intervals with [0,1]. Keep
point records and provenance duplicates. Preflight cap: 2,048 edge/lap-pair
attempts and candidates per stage, raised explicitly from the one-row 256 cap
for the larger input. Do not change it after seeing results.

Import compile_records unchanged but replace its provenance key in this module
instance with (parent,edge_start,edge_end,seventh_lap,eighth_lap). Ranking,
first-leader-only choice, 400-pair rectangle budget, full positive coprime
residual matrix, greedy maximum gain and tie ordering remain unchanged. The
inherited domain text is replaced with the actual nine-runner domain. The
selector's inherited p!=q flag is not used; recover and check direct speed
distinctness in a nine-runner wrapper. These are explicit adaptations, not a
claim that the entire transfer code is unchanged.

If the full matrix is incomplete but every uncovered pair has P=Q or P=2Q,
record PRIMARY_COMPLETE as a deduction from the emitted menu, preserving the
original incomplete status and all auxiliary misses. Do not retune the menu.
NO_DESCENDING_SEGMENT, SCOPE_LIMIT, CLIPPING_SCOPE_LIMIT, INVALID_CANDIDATE,
UNCOVERED_PRIMITIVE_PAIRS and coverage are distinct outcomes.

Stage B only: start with [z,1/2] x [z,1-z]. First two labels are zero; for each
other core row enumerate labels ceil((a+b)*z-(1-z)) through
floor(a/2+b*(1-z)-z). Cap 1,024 label tuples before enumeration. Intersect the
rectangle with all closed core bands using exact rational halfplane clipping.
Canonicalize convex polygons by sorted vertices and cyclic convex hull;
preserve segments and points. Sort surviving cells by labels, vertices
lexicographically, and edges by index pair. These are newly generated floor
edges at 1/9, not the old 1/8 atlas. The same joint clip and compiler then run.

## Controls and conditional richer diagnostic

Frozen pairs: (1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
(1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10).
Add collision/scaling controls (2,2),(4,2), for 20 per reached stage.
For a primary-complete menu use that menu for primary controls; for auxiliary
controls use it if full-complete, otherwise all candidates. For other partial
outcomes use all candidates in provenance order. Retain misses separately.
For every emitted witness verify original gcd, phases, torus/physical laps,
reflection 1-t, alternate Bezout and direct speed cardinality. Record open-end
contact losses for chosen menu and all candidates on these same controls.

On UNCOVERED_PRIMITIVE_PAIRS with a primary miss only, diagnose the first
lexicographic primary missed pair using complete six-form floor regions,
both added bands and integer H=Qx-Py. Use the existing parent's labelled
halfspaces at Stage A, generated bands at Stage B. Global added lap ranges
come from the rectangle, H from [Q*z-P*(1-z),Q/2-P*z]. Preflight cap is 20,000
parent/lap/lap/H tuples. In numeric parent/laps/H order substitute
y=(Qx-H)/P, solve the exact interval in x, and stop at the first nonempty
interval; select its midpoint or singleton and recover physical evidence.
If exhausted, record exact finite exhaustion for this direction and threshold
only. If capped, record resource stop. Do not add diagnostic geometry to or
rerun the compiler. A successful diagnostic exposes the edge restriction;
it does not by itself prove a replacement uniform certificate.

## Review, reproduction and representation checkpoint

Separate AI reviewers reconstruct joint clipping/contact decisions and physical
recovery without importing production code. A proof review checks the finite
reduction, threshold change, collision conditions and scope. These are internal
reviews, not blind, human or formal proof. Reproduce deterministic outputs once;
preserve corrections with timing. Record if conditional paths were unexecuted.

CC retains same-point compatibility, both labels, equality, source provenance,
parameter domain and recovery. The edge class omits parent interiors and new
edges created by added bands; the conditional diagnostic can recover them.
The output is a sufficient construction or a diagnosed limitation, not general
portability. Assess whether enrichment is needed for the next operation.

The pinned literature comparison credits the Jain–Kravitz segment mechanism
and Beck–Hoşten–Schymura lap polyhedra. Their reusable structures are considered
here; eight-runner existence results are not extended to nine by assumption.
No fresh literature-status or originality claim, broad speed search, outside
contact, main merge or unattended run. Universal arguments stay HYPOTHESIS /
internally reviewed proof candidates. Save the work on the research branch.
