# Orbit-aligned interval sources and a two-source family construction

October 2, 2026 UTC. AI-generated **proof candidates awaiting independent review**, supported by exact development checks. No novelty, arbitrary-runner, all-reference, or general Lonely Runner proof claim.

## Supported question and representation

Retain the ten distinct common-start speeds

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r)
\]

for positive integers. The chosen stationary runner is the reference and the closed target is 1/8, stronger than this ten-runner configuration's required 1/10. Only the last coordinate is free of the first two parameters; arbitrary mixed-r constraints are outside scope.

The prior source class retained a finite set of pair-orbit contacts for fixed p,q. Its exact failure at (1,2,40) motivates sources aligned with the actual pair orbit. We adapt the repository's exact physical phase-band representation into reusable labelled components. Their construction depends on p,q and the first eight constraints, before any r query. It costs a complete core-safe-set computation, which is charged and recorded. It is not free geometric preprocessing or a claimed efficiency improvement.

Normalize (p,q,r)=g(A,B,C), with gcd(A,B,C)=1. Put d=gcd(A,B), P=A/d, Q=B/d. Then gcd(P,Q)=gcd(d,C)=1. Build the complete primitive pair-clock core

\[
K_{P,Q}=\{u\in[0,1]:1/8\le\{(a_iP+b_iQ)u\}\le7/8
\text{ for all eight fixed rows }(a_i,b_i)\}.
\]

K is a finite union of disjoint closed rational intervals and isolated points. The source compiler enumerates every phase-boundary event (j+1/8)/v and (j+7/8)/v for each of the eight positive primitive speeds v. Between consecutive events, every band's membership is constant, so one exact midpoint decides the open interval. Test event points separately, retain closed boundaries, then merge touching safe pieces. This is an exact event decomposition, not approximate time sampling. Empty, positive-only, mixed and isolated-only sets remain distinct.

The inherited alternate checker instead intersects complete safe-band unions one speed at a time. Agreement between these algorithms checks implementation. The elementary event/band formulations are established methods already used in this repository; this package claims no new general geometry language.

## Turning a component into a sheet

For I=[l,u] in K, all eight physical core laps are constant on I, including its endpoints. A safe component cannot cross any integer phase wrap because phases near zero violate the positive threshold. Let Lp,Lq be the first two laps. Set

\[
S_I=\{(Pu-L_p,Qu-L_q):u\in I\}\times[1/8,7/8].
\]

Here u is the running variable in I. Each old row keeps torus lap Li-ai Lp-bi Lq. Endpoint band checks certify the whole affine base. Positive-width I gives a two-dimensional sheet; singleton I gives a vertical segment. The record preserves interval endpoints, width, lap labels, xy endpoints and pair clock. An isolated point must not be discarded merely because its width is zero.

Every physical occurrence of I in the normalized time period has a lift

\[
\tau\in[(l+j)/d,(u+j)/d],\qquad j=0,\ldots,d-1,
\quad t=\tau/g.\tag{1}
\]

The added phase is {C tau}. Keeping every lift is essential. This explicit inverse clock enforces the actual orbit; it does not admit the extra components caused by unsaturated raw relations. The union of all components and all lifts covers exactly the first-eight safe times in one full period of the normalized configuration.

## Exact one-runner extension

For a lifted interval J=[L,U], the added runner's closed safe bands are

\[
B_k=[(k+1/8)/C,(k+7/8)/C],\quad k\in\mathbb Z.
\]

The first band whose right endpoint reaches L has

\[
k=\lceil CL-7/8\rceil,\qquad
\tau_* = \max\{L,(k+1/8)/C\}.\tag{2}
\]

There is a compatible time in J exactly when tau_*<=U. By the definition of k, the band's right endpoint is at least L, and its left endpoint is no larger than its right endpoint, so tau_* also lies in that band. Earlier bands end before L; later bands cannot give an earlier contact. Thus failure rejects that lifted component exactly. Formula (2) applies to singletons as well as intervals and retains equality.

Apply (2) to each lift in order, recovering t=tau_*/g, its primitive core clock u=d tau_*-j, phases and physical laps. If every lift fails, that source rejects r. If every core component fails, the full configuration has no 1/8-safe time. This equivalence assumes a complete K; a compressed subset supplies only a sufficient search, not a complete nonexistence test. A negative result at 1/8 does not itself imply failure at 1/10.

## Sufficient coverage and finite reduction

Two consequences clarify when compression to one source is safe.

**Multiple lifts, d>=2.** At any fixed core point u, the added phases from j=0,...,d-1 are

\[
\{C(u+j)/d\}.
\]

Because gcd(C,d)=1, these are a rotated grid with spacing 1/d. The single connected unsafe arc on the phase circle has length 1/4. It cannot contain the whole grid: the shortest arc containing d equally spaced points has length (d-1)/d>=1/2. Hence some lift is safe. Any nonempty core source, even an isolated point, suffices. This is conditional on K being nonempty and all clock lifts being retained.

**One lift, d=1.** If a core interval has width w with Cw>=1/4, it must intersect a safe band: every connected unsafe time gap has length 1/(4C) and is open. A closed interval of at least that length cannot be wholly inside an unsafe gap. Formula (2) constructs the intersection. Width at least 1/(4C) is sufficient, not necessary; shorter intervals require their actual phase placement.

For a fixed original pair p,q, let d0=gcd(p,q) and let w>0 be a known primitive-core interval width. Whenever r is not divisible by d0, primitive normalization leaves d>=2 and the multiple-lift guarantee applies. When r=d0*C, only one distinct lift remains, and C>=ceil(1/(4w)) guarantees coverage by the chosen interval. Therefore the only unresolved r for this one-source guarantee are the finitely many positive multiples d0*C below that cutoff, after distinctness exclusions. Checking those is a finite reduction for this fixed pair and source, not a uniform bound across all p,q.

If the core is isolated-only, no positive-width tail argument is available in the one-lift case. For rational isolated times, added speeds divisible by their denominator lcm can erase every candidate. The exact contact rule still decides each requested r. No real isolated-only core occurred in development; supplied-singleton controls test the relevant code without pretending they represent a complete core.

## Complete two-source construction for p=1,q=2

The first eight moving speeds are (1,2,3,4,5,7,10,19). They are safe on

\[
I=[25/152,7/40],\qquad |I|=1/95,
\]

with fixed laps [0,0,0,0,0,1,1,3]. They are also safe at t0=1/8. For every integer r>=24, r|I|>=24/95>1/4, so (2) supplies a safe time in I.

The admissible positive r<24, excluding the eight repeated speeds, are

\[
6,8,9,11,12,13,14,15,16,17,18,20,21,22,23.
\]

Exact evaluation of (2) shows only r=6 and r=12 fail on I. At t0=1/8 their added phases are 3/4 and 1/2, respectively. Thus the fixed rule

\[
t(r)=\begin{cases}
1/8,&r=6\text{ or }12,\\
\max\{25/152,(\lceil25r/152-7/8\rceil+1/8)/r\},&\text{otherwise}
\end{cases}
\]

gives a 1/8-safe time for every positive integer r distinct from the eight core speeds. It uses one interval sheet and one vertical segment. Common scaling by any positive integer rescales time inversely. This strengthens the previously proposed r=40k repair to the entire fixed-pair r family, as an internally checked proof candidate. It is not arbitrary rank-three coverage or a novelty claim.

The stored development ledger retains all fifteen small cases, the r=24 boundary, r=40 and r=80, and a direct huge-r witness without enumerating its periods. Explicit lift/scaling controls retain the difference between (2,4,1) and the canonical j=0 clock; the successful widest-source witness uses j=1. Five pure band fixtures check safe endpoints, an unsafe subcritical interval, equality-width and a failed singleton. Three supplied-point tests retain both success and failure without claiming a real isolated-only complete core.

## What development says about compression

All 1,050 exposed triples in [1,12]^3 are handled by the complete core representation and agree with full physical band intersection. The core compiler finds 89 distinct primitive pairs, 39 mixed and 50 positive-only, with at most 48 components per pair. Removing isolated components loses exactly (1,2,6) and (1,2,12). Selecting only the widest component, breaking ties by earliest start before r is used, succeeds in 849/1050. Its 201 failures are retained.

These results make a useful boundary explicit: constructing the complete reusable core restores the omitted choices, while choosing one interval by width can lose phase-critical alternatives. The complete representation is not equally compact to a fixed four- or seven-sheet menu, and its construction is not cheaper merely because one extension query is simple. Fresh validation will assess the frozen rule without retuning it.

## Representation checkpoint

Supported use: exact extension of a supplied complete eight-constraint core by one independent runner, or one-witness selection from a declared subset. Retained: continuous core intervals, isolated equality points, fixed labels, all normalized clock lifts and physical inverse. Omitted by the widest shortcut: all other components; source availability is a recovery route, not intrinsic completeness. Richer source: the complete event-derived K, checked against a separate band intersection and preserved in the run record. Failure triggers: a widest miss, isolated-point ablation loss, absent clock lift, core/physical mismatch, or a changed family that introduces new mixed-r constraints. A complete core can be expensive to obtain; uniform core existence, a small sufficient source menu, optimality and external novelty remain open.
