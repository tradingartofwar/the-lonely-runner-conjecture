# Separate proof and scope review: joint nine-runner transfer

September 29, 2026. This is a separately tasked internal AI review, not blind
replication, external human review or formal certification. I derived the
width, domain and regeneration requirements before target computation, then
read the frozen protocol, implementation and emitted stage8 records. I did
not run an additional target trial or import production code for this review.

Protocol SHA256, verified from disk:
`6ac956e7fd36524c6168dd626548619b5cc07afd28f4ce951de6f4283db9940f`.
Its pinned source head is `eee207819d61043e6f49cc44cba7ed9472865a91`.
The inspected result is full `COMPLETE_COVER_CERTIFICATE` at 1/8; the
primary-domain guarantee follows as well. Stage1/9 and the richer diagnostic
are `NOT_TRIGGERED`. Their mathematical design is reviewed below, but this
run supplies no execution evidence for those conditional paths.

## 1. Joint question and exact domain

The eight moving rows are

    (1,0), (0,1), (1,1), (2,1), (3,1), (3,2), (6,2), (3,8).

With positive integer p,q and stationary reference0, both added speeds are
strictly greater than each core speed. The core speeds are pairwise distinct
exactly when p!=q. The two added speeds coincide exactly when
6p+2q=3p+8q, equivalently p=2q. Therefore nine distinct total speeds are
equivalent to p!=q and p!=2q. The only excluded primitive directions are
(1,1) and (2,1). Each has eight distinct total speeds, with a differently
located repeated speed; the labels must remain separate.

The fixed threshold1/8 is stronger than the nine-runner requirement1/9.
The claim concerns a safe time for this stationary selected reference, with
all runners starting together. It does not assert one time isolating every
runner, optimal separation or the complete safe-time set.

Joint clipping at one common affine edge parameter is necessary: separate
witnesses for (6,2) and (3,8) would not establish simultaneous safety. The
implementation intersects both parameter intervals before emitting a record
and retains both lap labels. Point records and provenance duplicates remain
valid candidates; a point cannot serve as a descending leader.

## 2. Width reduction and compiler scope

Write a descending segment as endpoints (x0,y0),(x1,y1), with
alpha=x1-x0>0 and beta=y0-y1>0. For positive primitive P,Q, the projection
H=Qx-Py has closed width alpha*Q+beta*P. Width at least1 guarantees an
integer contact, including equality. Every possible miss therefore has

    P <= ceil(1/beta)-1,  Q <= ceil(1/alpha)-1,
    alpha*Q+beta*P < 1.

The rectangle and its full primitive subdomain are thus proved bounds, not
empirically selected cutoffs. Given a complete matrix, any uncovered pair
misses every supplied candidate. A clipping or rectangle budget stop cannot
support that exhaustion claim.

The frozen adaptations are explicit: a second lap in the provenance key,
the larger declared joint-attempt cap, corrected domain metadata and a
nine-runner physical wrapper. Ranking by rectangle size, choosing only the
first leader, the 400-pair rectangle cap, complete residual enumeration and
greedy gain/tie order remain inherited. Three old single-row regressions
precede the key replacement. This is a controlled adaptation, not a claim
that all transfer code is unchanged.

If the raw compiler had been incomplete only on (1,1),(2,1), its emitted
menu would still cover every primary direction: the width argument covers
the infinite exterior and the completed matrix covers the remaining primary
directions. `PRIMARY_COMPLETE` would be a correct separate deduction, with
the raw incomplete status and auxiliary misses preserved. Here the stronger
full coverage result was obtained, so this conditional distinction is not
needed to rescue the result.

## 3. The emitted symbolic construction

The stage8 record selects these three segments, in order:

| Role | Geometry | Eight torus labels |
| --- | --- | --- |
| Leader P5:E0-3:K3:L7 | y=9/8-x, 1/4<=x<=3/8 | (0,0,1,1,1,2,3,7) |
| First fallback P2:E0-1:K2:L2 | y=9/8-3x, 7/24<=x<=55/168 | (0,0,0,0,1,1,2,2) |
| Auxiliary fallback P2:E0-3:K2:L3 | y=7/8-2x, 1/4<=x<=31/104 | (0,0,0,0,1,1,2,3) |

Subtracting those labels gives the following eight affine phases:

| Segment | Fractional phases, in row order |
| --- | --- |
| Leader | x; 9/8-x; 1/8; x+1/8; 2x+1/8; x+1/4; 4x-3/4; 2-5x |
| First fallback | x; 9/8-3x; 9/8-2x; 9/8-x; 1/8; 5/4-3x; 1/4; 7-21x |
| Auxiliary fallback | x; 7/8-2x; 7/8-x; 7/8; x-1/8; 3/4-x; 2x-1/4; 4-13x |

Direct endpoint substitution places every phase in [1/8,7/8]; affine
dependence proves the same throughout each closed segment. The seventh
phase on the leader is 4x-3/4 in [1/4,3/4], and on the first fallback it
is constantly1/4. On the third segment its range is [1/4,9/26], while the
eighth phase ranges from3/4 down to1/8. The constant phases1/8,1/8,7/8
on the respective segments show that each selected point has minimum
separation exactly1/8. This is the value at the constructed time, not an
assertion that a better time cannot exist.

Normalize d=gcd(p,q), P=p/d,Q=q/d. On the leader the projected interval is

    [(2Q-7P)/8, (3Q-6P)/8], with width (P+Q)/8.

For P+Q>=8 the interval contains an integer. Its entire possible complement
has the 17 positive primitive directions P+Q<8 already enumerated in the
source transfer and retained in the current complete matrix. The only leader
misses are (1,1),(1,4),(2,1).

The first fallback has projected interval

    [(7Q-6P)/24, (55Q-24P)/168].

At (1,4) this is [11/12,7/6], selecting H=1 and point(17/56,3/14).
At (2,1) it is [-5/24,1/24], selecting H=0 and point(9/28,9/56).
The third segment, needed only at (1,1), has projected interval
[-1/8,1/52], selecting H=0 and point(7/24,7/24).

Thus the preserved three-segment rule supplies a safe contact for every
positive primitive pair, including both repeated-speed directions. Its first
two segments already suffice whenever p!=q, which is stronger than their
required primary domain p!=q,p!=2q. This is a deduction from the unchanged
emitted menu, not a new minimal-menu or retuned compiler claim.

## 4. Recovery of one physical time

At a selected point let h=Qx-Py be the selected integer and choose rP+sQ=1.
Put T=rx+sy, N=floor(T), tau=T-N, t=tau/d. The identities

    P*T = x-s*h,  Q*T = y+r*h

show that pt and qt have the required fractional coordinates. For any of
the eight rows (a,b), with retained torus lap m, the physical lap is

    m+(-a*s+b*r)*h-(a*P+b*Q)*N.

It is an integer and satisfies
(ap+bq)t=physical_lap+(ax+by-m). Hence the eight safety inequalities occur
at the same recovered physical time. Since the p-coordinate phase is at
least1/8, tau cannot be0; therefore 0<t<1/d. Integer speeds also make
reflection1-t safe, with phase1-f and lap v-1-lap for every safe phase f.
Changing Bezout coefficients to (r+Q,s-P) changes T by h and preserves tau.

At the auxiliary p=q=d the new selected time is7/(24d). This differs from
the old row-(3,8) selector's auxiliary time1/(8d); the latter gives the
(6,2) row an integral phase and cannot certify joint safety there.

The resulting theorem candidate can be stated directly: for every positive
integer p,q there is the explicitly recovered rational time t such that all
eight moving speeds are at distance at least1/8 from the stationary
reference. When p!=q and p!=2q, all nine speeds are distinct, so this also
supplies their selected-reference1/9 guarantee. The general argument remains
an internally reviewed proof candidate.

## 5. Continuity: primary coverage was already implied

This is a consequential logical deduction from the prior coefficient-range
result, not a newly discovered family-level existence fact. The previous
row-(3,8) rule made the core and (3,8) row safe at every output for p!=q.
The completed range analysis accepted (6,2) in that same rule's T contract.
That acceptance guarantees safety of (6,2) at the same selected point, so
the conjunction already implied joint primary1/8 coverage before this run.

There is no illegitimate combination of separate existential witnesses in
this deduction: both statements quantify over one identical deterministic
selector. The new computation makes the joint edge clipping, eight labels,
coverage menu and physical checks explicit. It also chooses different
auxiliary geometry and repairs p=q, which the prior row-(3,8) auxiliary
selector failed for (6,2).

Calling the run a new primary family existence result would lose the prior
T contract's exact same-point meaning. Calling it unchanged generic compiler
portability would omit its explicit two-lap adaptation and larger attempt
cap. The warranted finding is successful simultaneous-constraint transfer
and explicit auxiliary repair under the frozen protocol.

## 6. Unexecuted regeneration and richer diagnostic

For any threshold z in the declared range, every safe physical point can
be reflected, if needed, into the folded box [z,1/2] x [z,1-z]. Reflection
(x,y)->(1-x,1-y) preserves every integer-row circle distance. For a row
(a,b) with nonnegative entries, its raw extrema over the box are
(a+b)z and a/2+b(1-z). Therefore all possible safe lap labels are exactly
within the exhaustive range

    ceil((a+b)z-(1-z)) ... floor(a/2+b(1-z)-z).

The first two labels are zero. Enumerating all remaining core-label tuples
and intersecting their closed bands with the box is a complete construction
of the six-form threshold floor. Convex polygons, line segments and singletons
must all be retained. The code's exact clipping and hull canonicalization
are consistent with this specification; the arithmetic implementation of
this conditional path has not been exercised by the present experiment.

For any diagnosed primitive pair, the global projection range is
[Qz-P(1-z), Q/2-Pz]. Exhausting its integer H values, all complete parent
regions and both added lap ranges covers the full folded joint safe set for
that pair and threshold. Substitution y=(Qx-H)/P turns every halfplane into
a one-dimensional bound or a constant feasibility test. A found interval
provides a same-point witness; bounded exhaustion has only the stated pair
and threshold scope. At1/8 even genuine nonexistence for a primary pair
would not refute the weaker nine-runner1/9 requirement.

These completeness arguments justify the proposed recovery route. They do
not turn `NOT_TRIGGERED` into tested success. Neither regeneration at1/9 nor
the richer parent diagnostic was needed or executed here.

## Finding

PASS for the width reduction, exact collision domain, simultaneous labelled
construction, closed endpoint handling, physical recovery and stated scope.
The 1/8 full certificate implies the declared nine-distinct-speed result and
also handles both auxiliary directions. The primary same-point consequence
of the prior T classification must be preserved in the result narrative.
No new literature or originality conclusion follows from this review; the
recorded attribution remains in force, and eight-runner literature is not
extended to nine merely by analogy.
