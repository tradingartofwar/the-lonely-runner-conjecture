# Scope review: what simultaneous last-runner containment adds

September 29, 2026. Pinned research parent
`f3c26e709fa1cd8945968dcd585bd012430c7243`.

**Status:** analytic HYPOTHESIS / proof candidates with supplied arguments.
This is a separate internal AI review, not external mathematical certification.
No executable mathematical evaluation, new speed scan, or literature frontier
claim was made for this report.

## 1. The actual question, and the already available machinery

Let `A` be the complete closed safe set in `[0,1]` of the six integer,
common-start core speeds `{1,4,5,a,b,c}` at threshold `delta=1/8`.
Its positive components and isolated points both belong to A. The last runner
with integer speed d prevents any selected-reference lonely time exactly when

`A subset {t: ||dt||<1/8}`.

The existing exact-interval note already determines complete containment in a
safe lap by midpoint/halfwidth or integer endpoint inequalities, including
finite unions. Reversing that calculation for an open blocking lap is a useful
interface, but is not a new general interval theorem. The existing fastest-core
note likewise supplies an exact representation of uncovered duration under its
conditioning. Exact representation does not force a nonempty uncovered set.

At a **fixed d**, whole-core blocking is simply the conjunction of the exact
component predicates and isolated-point predicates. There is no further hidden
compatibility variable after d and its common-start phase are fixed: any lap
label fitting a nonempty component is unique because distinct blocker laps are
disjoint. Simultaneous containment becomes a substantive parameter restriction
when **d varies**, or when a **single shared phase varies**. One then intersects
all allowable parameter sets; components cannot independently choose speeds or
phases.

This distinction matters for the next result. An empty intersection of
allowable integer-d sets is a genuine exclusion of a last-runner family. Merely
rewriting the conjunction is not an existence argument. A general proof would
still have to force such exclusion for every admissible core.

The adaptive reflected-pair note already covers the entire physical family
`0,1,4,5,6,7,11,V`, and even an arbitrary phase of runner 11. Its tight13 and
strict16 records are therefore diagnostics of a representation, not new
existence coverage. The selected variable runner in that result is important:
varying runner 11's phase is not the same assertion as varying the final
runner's phase.

## 2. A reflection-symmetric phase dichotomy

For an integer d define the compact circle set

`P = {dt mod 1: t in A}`.

The common-start integer core gives `t in A iff 1-t in A`. Integrality of d
then gives `P=-P`. The prior two-time note proves at this threshold that
feasibility for **every** phase of the last runner is equivalent to two points
of P having circular separation at least `1/4`.

For this symmetric P there is a sharper, useful scope statement:

> All-phase feasibility is equivalent to feasibility at both phases 0 and 1/2.

Here feasibility means that at least one time in the complete A is safe for
the selected last-runner phase. The two successful times need not coincide.

**Proof.** Suppose there is no pair of P separated by at least `1/4`.
For every x in P, also `-x` belongs to P, so

`||2x|| < 1/4`.

Consequently every x lies in one of the two open arcs

`B0=(-1/8,1/8) mod1`,  `Bh=(3/8,5/8) mod1`.

Any point of B0 and any point of Bh have circular distance strictly greater
than `1/4`. Therefore P cannot meet both arcs and must lie wholly in one.
If `P subset B0`, phase0 blocks every point. If `P subset Bh`, phase1/2
blocks every point. Conversely either such strict containment makes that
particular phase infeasible. The two-time completeness lemma supplies the
equivalence between absence of a separated pair and absence of all-phase
feasibility. This proves the statement, retaining equality as safe.

An immediate consequence separates the two mathematical objectives cleanly:

> If common-start safety survives but no all-phase two-time certificate exists,
> every core-safe time has last-runner distance strictly greater than `3/8`.

Indeed the only remaining obstruction to robustness is `P subset Bh`.
Thus failure to obtain a robustness certificate need not be a hard
common-start case: it may correspond to the last runner being uniformly far
from the reference on every core opening.

There are two elementary routes to a two-time certificate in this symmetric
setting. A point with `||x|| in [1/8,3/8]` supplies the reflected pair x,-x.
If no such point exists but P meets both B0 and Bh, take one point from each
arc; this pair need not come from reflected times. Restricting all certificates
to reflections can therefore miss an available pair. The abstract symmetric
set `{0,1/2}` illustrates the distinction: every reflected pair coincides,
while the two distinct points are a half-circle apart. This is a circle-set
example, not an asserted six-core realization.

This dichotomy is an application of the existing two-time geometry plus the
integer reflection symmetry. It is not asserted as a novel theorem or as a
universal robustness guarantee for the present family.

## 3. Real d on one core period is not the global problem

For integer d, `[0,1]` is a common period and the containment test on A decides
global feasibility. For noninteger real d, an interval of allowed d values
obtained from A describes **only that observation period**. The core repeats
after time1 while the last runner acquires a different phase.

In fact the global noninteger-d problem here has a direct finite certificate.
Assume the integer core has any safe time `t0`, and let

`beta=||d||>0`,  `m=floor(1/(4 beta))+1`.

Then

`1/4 < m beta <= 1/2`, hence `||md||=m beta>1/4`.

To check the upper bound: if beta>1/4 then m=1; otherwise
`m beta<=1/4+beta<=1/2`. Because each core speed is integer, both t0 and
`t0+m` are core-safe. Their last-runner phases are separated by `||md||`,
regardless of the last runner's initial phase. The existing two-time lemma
therefore guarantees a safe time among this pair for **every** last-runner
phase.

If the core has a positive safe interval, choose t0 in its strict interior.
The strict phase separation gives a strictly safe winning time and hence a
positive final safe interval. This uses no density theorem and no numerical
evaluation.

Thus, for the global problem with an integer core, the only difficult last
speeds are integers. A real-d band can be a useful algebraic aid to excluding
integer d, but it must not be described as a global failure family for
noninteger d. The integer-translation pair generally uses a time outside the
first unit interval; that is precisely why it does not contradict a local
one-period containment.

## 4. Compact exclusion certificates and their limit

For an a priori bounded d interval, all relevant component lap labels range
over finite sets. Inside one branch where those labels are fixed, each
component contributes an open lower/upper bound on d. Their intersection is
an open interval, possibly empty. An empty real intersection is witnessed by
an active lower bound meeting or exceeding an active upper bound; these may
come from at most two component constraints. A nonempty real interval can
still contain no integer, which requires a separate strict integer-endpoint
check.

This is ordinary one-dimensional interval intersection. It supplies a compact
certificate **after the lap branch has been fixed**. It does not imply that
two core components universally eliminate every lap branch, or that a single
two-component obstruction covers all admissible d. The original allowable
sets are unions of intervals. Branching and linked integer lap choices must
remain visible in any claimed compressed certificate.

For a fixed d, a single supplied core-safe time that survives its blocker is
already a complete common-start witness. For a d family, the useful advance
would be an arithmetic rule selecting a bounded collection of witnesses, or a
finite parameter partition with an explicit valid witness on each cell. That
would add an actual exclusion mechanism beyond a full-set reconstruction.

## 5. Endpoint and interpretation checks

- A positive component too wide for one open blocker rules out full strict
  coverage. Equality of widths also prevents covering both closed endpoints.
- A final safe singleton is enough for the conjecture but not for positive
  duration. Isolated core points can be decisive and must stay in A and P.
- Covering all positive core components while missing an isolated point is
  not full-core blocking.
- Proving a candidate d lies in no component-band intersection certifies that
  some actual core time survives. Merely proving that all-phase robustness
  fails does not decide the original common-start problem.
- The reflection dichotomy requires an integer common-start core and integer
  d. A shifted core, a clipped nonsymmetric observation window, or a
  noninteger final d need not have the same symmetry inside `[0,1]`.
- No new Lonely Runner existence coverage, external review, or full finite-box
  verification is supplied here. Hourly research remains paused.

## 6. Positive duration: the closed-arc analogue

The stronger analogue also holds for integer d:

> Positive final safe duration for every phase is equivalent to positive
> final safe duration at both phase0 and phase1/2.

Define `A_pos` as the union of all positive-length **closed** core-safe
components, omitting isolated components. Set

`B={dt mod1: t in A_pos}`.

Equivalently, B is the closure of the images of the interiors of the positive
core components. The finite-interval structure makes B compact; core reflection
and integer d give `B=-B`. If there are no positive core components, B is empty
and the final safe duration is zero for every phase, so both sides of the
claimed equivalence are false.

For nonempty B, positivity at a given phase theta is equivalent to

`B not subset {x: ||x+theta||<=1/8}`.                         (P)

Indeed a point outside this **closed** blocker arc has strict last-runner
safety. If its preimage is a component endpoint, approximate it by interior
core-safe times; strictness persists. Interior core times are strictly safe
for every nonzero core speed. Continuity then gives a positive final interval.
Conversely, a positive final safe interval contains a point away from the
finitely many core and last-runner threshold events, yielding strict safety
and a point of B outside the closed blocker arc. Merely touching that arc's
boundary can preserve equality instants, but does not imply positive duration.

Suppose now that every pair of points of B has circular separation at most
`1/4`. The reflected pairs yield `||2x||<=1/4`, so

`B subset C0 union Ch`,

where `C0=[-1/8,1/8] mod1` and `Ch=[3/8,5/8] mod1` are closed.
If B meets both arcs, write the respective points as `+/-a` and `1/2+/-b`,
with `0<=a,b<=1/8`. Reflection supplies both signs. One resulting cross-pair
has circular separation

`1/2-|a-b| >= 3/8 > 1/4`,

a contradiction. Hence B is wholly contained in C0 or wholly in Ch.
By (P), one of phases0 and1/2 then has zero positive duration.

Taking the contrapositive, positivity at both distinguished phases supplies
two points of B separated **strictly more** than `1/4`. Approximate their
preimages by interiors of positive core components; their separation remains
strictly greater than `1/4`, and all core distances at both times are strictly
greater than `1/8`. The inherited strict two-time lemma gives a strictly safe
winning time for every last-runner phase. Continuity gives positive duration
at each phase. The converse follows by selecting phases0 and1/2.

This proof separates the endpoint conventions:

- **Feasibility:** failure means containment of the full core image P in an
  **open** quarter-circle arc; a pair separated **at least** `1/4` suffices.
- **Positive duration:** failure means containment of B in a **closed**
  quarter-circle arc; a pair separated **more than** `1/4` suffices.

The two-time certificate in the positive case also supplies a uniform strict
margin over all phases, once its two interior times have been chosen. No
numerical bound on that margin is asserted here. The statement concerns
integer d and the full core period; it must not be applied to arbitrary real-d
bands on a clipped observation window.

The separate internal challenge reviewer checked this argument and supplied
the cross-pair bound `1/2-|a-b|>=3/8`. This is additional internal review,
not external certification. No further phase evaluations were performed.

## 7. Post-protocol analytic deduction: the exceptional phase sets

**Timing and scope disclosure.** This section was derived after the frozen
last-runner band calculation reported the exceptional zero-duration integer
speeds13 and18 for the core `{1,4,5,6,7,11}`. It is an explicit analytic
follow-up, not a preregistered prediction, a phase scan, or additional
executable evaluation. The exact complete core decomposition supplied by
that calculation has positive components

`A=[17/56,5/16]`,  `K=[41/88,15/32]`,

and their reflections. Its isolated core points are
`1/8,3/8,5/8,7/8`. Here A denotes this one component; the full core-safe set
in the earlier sections is not being renamed.

The following endpoint multiplications were independently checked by hand.
All phase intervals are closed, with signed intervals near zero interpreted
modulo1.

| Last speed | Image of A | Image of reflected A | Image of K | Image of reflected K |
| --- | --- | --- | --- | --- |
| 13 | `[-3/56,1/16]` | `[-1/16,3/56]` | `[5/88,3/32]` | `[-3/32,-5/88]` |
| 18 | `[13/28,5/8]` | `[3/8,15/28]` | `[17/44,7/16]` | `[9/16,27/44]` |

At speed13 the first two intervals unite to `[-1/16,1/16]`.
The K images overlap these intervals because `5/88<1/16`; hence the whole
positive-component image is exactly

`B13=[-3/32,3/32] mod1`.

At speed18 the A and reflected-A images overlap because `13/28<15/28`
and already unite to `[3/8,5/8]`. Both K images lie inside, so

`B18=[3/8,5/8]`.

By the closed-arc characterization (P), zero final duration means that this
entire B lies in the closed quarter-circle blocker centered at `-theta`.
The centered interval B13 has radius3/32 and that blocker has radius4/32.
Its allowable center displacement is therefore at most1/32. B18 already
has the full blocker length, so only one blocker center can contain it.
Consequently the exact zero-duration phase sets are

`d=13: ||theta||<=1/32`,

`d=18: theta=1/2 mod1`.

The inequalities at the boundary are non-strict because this is a
**zero-duration** classification, not strict coverage of every safe point.
All other phases have positive final duration by (P).

Feasibility persists at every phase in both cases. At speed13 the four
isolated core times map to the four odd eighths, which include opposite
points. At speed18 they map to the two opposite points `1/4,3/4`. An open
quarter-circle blocker cannot cover an opposite pair, so at least one of
these core times remains safe at every phase.

Nor should zero duration be described as survival of only the old isolated
core points. At speed13, phase`+1/32` additionally permits the positive-core
endpoint `t=15/32` at last-runner equality; phase`-1/32` permits its
reflection `t=17/32`. At speed18, phase1/2 permits endpoints `t=5/16`
and `t=11/16`. These are threshold contacts of formerly positive core
components, and contribute no positive duration.

**Which runner is shifted matters.** This deduction varies the phase of the
last runner, with speed13 or18, while core1,4,5,6,7,11 stays common-start.
The earlier adaptive reflected-pair family varied **runner11's phase** while
the last runner remained common-start. The two phase questions are different;
this calculation must not be described as a repetition or contradiction of
the earlier phase11 result. No external novelty claim is made.

For extending a finite last-speed calculation by a widest-component bound,
retain one endpoint distinction: component width1/112 excludes full strict
blocking for `d>=28`, whereas width alone excludes zero duration only for
`d>28`. The closed-block case d=28 needs its own recorded equality check or
an additional component obstruction. Here it has a direct one: the images of
A and its reflection at speed28 are `[1/2,3/4]` and `[1/4,1/2]`.
Their union is a half-circle, which no closed quarter-circle blocker can
contain. Therefore speed28 also has positive duration at every final phase.
This is another hand deduction from the same supplied component endpoints,
not an additional numerical scan.

## Read sources within the project

- `notes/EXACT_INTERVAL_CRITERION_2026_09_28.md`
- `notes/TWO_TIME_CERTIFICATES_2026_09_27.md`
- `notes/ADAPTIVE_REFLECTED_PAIR_2026_09_28.md`
- `notes/FASTEST_CORE_CERTIFICATES_2026_09_27.md`
- `notes/SIX_CORE_WINDOW_2026_09_29.md`

The general constructions above are derived explicitly from these internal
arguments. No external novelty or priority inference is made.
