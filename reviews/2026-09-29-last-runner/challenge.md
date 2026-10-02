# Adversarial review: simultaneous last-runner containment

September 29, 2026. Parent `f3c26e709fa1cd8945968dcd585bd012430c7243`.
**HYPOTHESIS / internally reviewed proof candidates.** This report uses analytic
arguments and reads existing exact records. It runs no executable mathematical
evaluation and introduces no physical speed scan. AI review is not external
mathematical certification.

## 1. Exact maximum and strict endpoint audit

Let `||x||=dist(x,Z)`, `I=[x-h,x+h]`, `h>=0`, `d>0`, and `delta=1/8`.
The exact numerical maximum is

`max_{t in I} ||dt|| = min(||dx||+d*h, 1/2)`.

The upper bound follows from Lipschitz continuity and the range of circular
distance. From the midpoint, move in the direction toward the nearest
half-integer on the ascending side of the triangular distance function.
The distance increases at unit rate until reaching1/2. This attains the
displayed bound, including midpoint cusps and intervals spanning several laps.

Consequently the following are equivalent, without an extra width assumption:

1. Every point of the **closed** I is strictly blocked by d.
2. `||dx||+d*h<delta`.
3. There is an integer m with `d*r-delta<m<d*l+delta`, where `l=x-h,r=x+h`.

For (3), the connected lifted interval `[dl,dr]` must lie in one connected
open blocker `(m-delta,m+delta)`; conversely those inequalities give that
containment. The relevant m, when it exists, is unique. Since delta<1/2,
the numerical cap in the maximum does not alter the sign test in (2).
It must still be included if the maximum itself is reported numerically.

For positive width w, strict coverage automatically implies `d*w<1/4`.
Thus equality at `d=1/(4w)` prevents coverage of the closed interval and
supplies a valid final-safe point. The integer candidates are
`d<=ceil(1/(4w))-1`; replacing this by `floor(1/(4w))` loses strictness when
the reciprocal is an integer.

For `0<l<=r`, solving (3) for real d yields the open band

`( (m-1/8)/l, (m+1/8)/r )`.

The formula includes singleton components `l=r`. The fixed speed1 keeps
physical core components inside `[1/8,7/8]`, so division by zero is not an
issue here. A generic interval lemma including l=0 needs a separate case.

## 2. Three different endpoints of the investigation

Let S be the complete closed core safe set. Let S_pos be the union of its
positive **closed** components, and let Q be its isolated points. Put

`M_all(d)=max_{t in S} ||dt||`,
`M_pos(d)=max_{t in S_pos} ||dt||`.

The six-core positivity argument guarantees S_pos is nonempty in the current
physical setting. Then:

- A final safe point exists exactly when `M_all(d)>=1/8`.
- Positive final safe duration exists exactly when `M_pos(d)>1/8`.
- All positive closed components are strictly covered exactly when
  `M_pos(d)<1/8`.

For the second statement, a strict final margin at a component endpoint
persists just inside the component, where every core runner is strictly
safe. Conversely a final-safe interval contains a point away from the
finitely many final-runner equality events, giving a strict final margin.
Here d>0 and nonzero physical core speeds matter. At `M_pos=1/8`, the
surviving points can be isolated and the positive components are not
strictly covered.

Elementary auxiliary fixture: with d=2, I=[7/16,9/16] maps to
[7/8,9/8]. Its interior is blocked, but its endpoints are safe at equality.
This is a lemma fixture, not a new physical core.

The inherited physical tight case is an even stronger warning about Q.
For C={1,4,5,6,7,11}, the existing exact core record gives two positive
components in the first half:

`I1=[17/56,5/16]`, `I2=[41/88,15/32]`,

their reflections, and isolated points1/8,3/8,5/8,7/8. At d=13,

`13*I1-4=[-3/56,1/16]`,
`13*I2-6=[5/88,3/32]`.

Both closed image intervals lie strictly inside(-1/8,1/8). Integer-speed
reflection covers the other two positive components. Nevertheless the
four isolated points have final distances3/8,1/8,1/8,3/8 and all survive.
Thus strict coverage of every positive closed component does **not** imply
full failure. No new evaluation is needed for this calculation; the core
components are read from `reviews/2026-09-29-six-core/primary_six_core.json`.

## 3. Relative center and lap differences lose absolute phase

For component i with center x_i and halfwidth h_i, define
`epsilon_i=1/8-d*h_i`. Strict coverage requires epsilon_i>0 and

`|d*x_i-m_i|<epsilon_i`

for integer m_i. Subtraction gives the necessary pair restrictions

`|d*(x_i-x_j)-(m_i-m_j)|<epsilon_i+epsilon_j`.

These restrictions alone do not retain the common-start phase. Even fully
consistent pair lap differences can pass while all absolute inequalities
fail.

Explicit auxiliary countermodel: take d=2 and two intervals with centers
1/4 and3/4, each halfwidth1/64. Their epsilon values are3/32, and their
center-image difference is the integer1. Every pair-difference restriction
therefore passes with m_2-m_1=1. But both center phases are1/2, and their
entire images have circular distance at least15/32; neither interval is
blocked at phase0. Adding the common phase1/2 blocks both intervals.

The same relative geometry therefore permits a shifted cover while
forbidding the prescribed common-start cover. This auxiliary union is not
asserted to be the safe set of an admissible six-core. Its role is to refute
an invalid implication about the proposed representation.

Any subtraction-based system must retain at least one absolute anchor or
the original absolute inequalities. No claim is made here that pairwise
phase-arc feasibility is incomplete at this small threshold; the prior
two-time theorem already controls that separate all-phase question.

## 4. Reflection and observation-period limits

For integer d at phase0,

`||d*(1-t)||=||d*t||`.

Thus reflected core components have redundant last-runner tests. For a
shift theta, the reflected test instead corresponds to phase -theta:
`||d*(1-t)+theta||=||d*t-theta||`. Redundancy requires additional phase
symmetry (theta=0 or1/2 modulo1 is sufficient); arbitrary shifts do not
inherit it.

For noninteger real d, even phase0 need not respect reflection. As an
auxiliary example, d=13/2 at t=4/13 has distance0, while at1-t it has
distance1/2. Hence a real-d band calculation must keep reflected components
unless it supplies a different justification.

More fundamentally, a real-d cover on[0,1] is only a cover on that observed
period. The integer-speed core repeats each unit, but the final phase changes
by d. It does not follow that the complete configuration is globally blocked.

In fact the existing two-time lemma immediately disposes of global failure
for any **noninteger** d once this integer core has a safe point. Let
`s=||d||>0`, `N=ceil(1/(4s))`. If s>=1/4 then N=1; otherwise
`1/4<=N*s<1/2`. In either case `||N*d||` lies in[1/4,1/2]. For any core-safe
t, both t and t+N are core-safe. Their final phases are separated by at
least1/4, so at least one final distance is at least1/8. This argument
reuses the prior two-time lemma and claims no new existence result.

Physical integer d makes the entire system unit-periodic. Only in that
case does strict coverage of the complete S in one period mean global
failure for the selected reference.

## 5. Relationship to the previous results

`EXACT_INTERVAL_CRITERION_2026_09_28.md` already gives the exact minimum
distance on an interval, its safe-lap reformulation and finite-union
extension. The maximum formula above is the corresponding elementary
strict-blocking version. It is useful bookkeeping but should not be
presented as a new general interval-intersection theory or an existence
guarantee.

`TWO_TIME_CERTIFICATES_2026_09_27.md` already proves the equivalence between
one-runner all-phase robustness and an appropriate two-time certificate
at this threshold. Rephrasing the image as phase arcs or pairwise phase
separations is not additional existence coverage. Common-start success is
weaker than all-phase robustness and must retain its absolute phase.

The actual next structural obligation is to show that integer d cannot
satisfy all the strict band constraints for every component and singleton
of an admissible core, or to reduce that obligation through an explicit
arithmetic argument. Merely constructing the exact feasible set for a
supplied core is an exact reformulation of the question, not its universal
resolution.

## 6. Review disposition

The strict lap criterion, midpoint maximum with cap, real-d bands, and
integer-d reflection are accepted as internally reviewed derivations with
the scope stated above. Principal failure modes are:

- replacing strict coverage inequalities by weak ones;
- discarding isolated core points;
- equating zero final duration with an empty final set;
- retaining relative lap differences while losing the phase0 anchor;
- applying integer reflection or unit-period completeness to arbitrary
  real d or shifted phases;
- treating a reexpression of an existing interval/two-time test as the
  missing universal arithmetic obstruction.

No new universal obstruction or full remaining-region exhaustion is claimed
by this review.

## 7. Follow-up audit: endpoint residues and controller slack

The structure report's reduced-denominator assertion is correct: a threshold
has odd numerator over8v, so reduction removes no factor2 and its reduced
denominator q remains divisible by8. The allowed strict-blocking residues
are precisely `dp mod q in {-(q/8-1),...,q/8-1}` modulo q.

The conjunction of all endpoint residue tests, singleton tests, and the
strict cap `d*w_max<1/4` is **complete**, not just necessary. Two blocked
endpoints in distinct laps have phase separation greater than3/4, whereas
the width cap makes their separation less than1/4. They therefore occupy
the same lap, which contains their entire interval. The residue tests alone
and the separate slack bounds alone remain only necessary.

For left/right threshold controllers v,w, the controller orientations in
the report are correct. The positive left numerator

`d*(8k+1)-v*(8m-1)`

is divisible by g=gcd(d,v), and after division has fixed residue
`(d+v)/g` modulo8. Its minimum positive value is consequently at least
`g*R8((d+v)/g)`. The right endpoint has the same form with w. These
prove the reported gcd-slack inequality, including its non-strict final
comparison. Multiple controllers may each supply a necessary bound.

One strength qualification is essential: this controller bound need not
dominate the reduced-denominator bound. At t=1/8 controlled from the left
by v=9, d=16 gives reduced-denominator slack1/8 but controller slack1/72.
The entering endpoint is compatible with core{1,4,5,9,10,11}. Conversely
the controller bound can be stronger in other cases. The valid combined
bound at each endpoint is the maximum of its reduced-denominator bound
and every applicable controller bound. They are complementary deductions.

The single-component certificate for C={1,4,5,3,7,24} was also checked by
hand: for I=[25/56,29/64], d>24, the only possible real covering bands
have m=11,...,16. Their endpoints lie strictly between the stated
consecutive integers. Their **closed** versions are also integer-free,
so this I actually supplies positive final duration for every integer
d>24. This is an explicit fixed-core certificate, not a universal claim.

## 8. Follow-up audit: two openings force phase robustness

Let two disjoint positive closed core-safe intervals be
`I=[l,r]` and `K=[u,v]`, with r<u. Define

`D=v-l`, `G=u-r`, and `w=max(r-l,v-u)`.

If `G<=3w`, every real `d>=1/(4D)` and every common phase theta of the
final runner has a safe point in I union K. To prove this, suppose the
two intervals are strictly blocked. Each lies in one open blocking lap.
If both lap labels are equal, their joint hull is blocked, requiring
`dD<1/4`. If the labels differ, the intervening gap must span more than
the safe gap between consecutive laps, so `dG>3/4`. But coverage of the
widest interval gives `dw<1/4`, contradicting `dG<=3dw<3/4`. The shared
phase cancels from the subtracted inequalities, so it is unrestricted.

There is a strict-duration version. If `G<3w` and `d>1/(4D)`, positive
final duration survives on these intervals for every final phase. Suppose
instead that both intervals lie in the final runner's **closed** blockers.
Same-lap coverage requires `dD<=1/4`. Different-lap coverage requires
`dG>=3/4`, while the width bound gives `dw<=1/4`, contrary to
`dG<3dw<=3/4`. Thus some point has final distance strictly greater than
1/8; moving slightly into a positive core component if needed gives a
strict common-safe interval.

Both strict qualifications matter. At dD=1/4 a hull can exactly fill a
closed blocker and leave only equality endpoints. At G=3w two equal-width
components can exactly fill adjacent closed blockers when dw=1/4.

For C={1,4,5,3,7,24}, the inherited intervals

`I=[25/56,29/64]`, `K=[89/192,15/32]`

give `D=5/224`, `G=1/96`, `w=3/448`, with `G<3w`. Thus the supplied
core has a final-safe witness for every real d>=56/5 and every phase,
and positive final duration for d>56/5. This is a stronger auxiliary
scope than the single-window integer/common-start calculation. The
physical specialization d>24 is included. The certificate acts within
the supplied core period, so no global periodicity assumption on real d
is being made. This is a concrete application of prior phase/two-time
geometry; external review and novelty assessment remain pending.

## 9. Follow-up audit: phase0/half dichotomy and short integer relations

The scope report's nonempty all-phase dichotomy is accepted. For integer
d, the complete core phase image P is symmetric under x -> -x. If no
pair is separated by at least1/4, reflected pairs force P into the union
of the open quarter arcs about0 and1/2. A cross-arc pair would have
distance greater than1/4. Hence P lies entirely in one of those arcs,
and phase0 or phase1/2 completely blocks it. Together with the existing
two-time completeness lemma, feasibility at those two phases is therefore
equivalent to feasibility at every phase.

The positive-duration analogue is also accepted, after discarding isolated
core points from this particular image. Let B be the phase image of the
union of the positive **closed** core components. It is compact and
reflection-symmetric. Positive duration at phase theta is equivalent to
B not lying in the closed blocker arc centered at -theta.

If every pair of B has separation at most1/4, reflected pairs put B in
the two closed quarter arcs C0 and Ch. It cannot meet both: write one
phase as +/-a and another as1/2+/-b, where0<=a,b<=1/8. Reflection provides
both signs, and one cross separation is `1/2-|a-b|>=3/8`, a contradiction.
Thus B lies entirely in C0 or Ch, causing zero duration at phase0 or
phase1/2. Conversely, positive duration at both phases forces a pair
separated by more than1/4. Approximate its preimages by strict core
interior times and use the prior two-time lemma to obtain strict safety
for every phase. If B is empty, positive duration fails at every phase.

Finally, the short integer relation claim is correct under its stated
common-start integer-d assumptions. For integer h_i,q with
`sum h_i*t_i=q`, strict blocking gives

`d*q-sum h_i*m_i=sum h_i*e_i`, with `|e_i|<1/8`.

For nonzero h with L1 norm at most8, the right side has magnitude below1
and the left side is an integer, so both vanish. With weak blocking and
L1 norm below8 the conclusion is unchanged. At norm8 the exceptional
values +/-1 are possible only if every nonzero-coefficient point is at
final threshold and all products h_i*e_i have the same sign. Those
points are already valid final-safe witnesses.

For a shifted final phase theta, retain the additional term
`theta*sum h_i`; it cancels when `sum h_i=0`. Omitting that term for
general relations would silently change the common-start hypothesis.
For two points separated by reduced p/q with q<=4, the zero-sum relation
has norm2q<=8 and correctly forces q|d under simultaneous strict
blocking. These are necessary relations, not an assertion that every
core possesses a useful relation or that the relations suffice for cover.

## 10. Final static review of the integrated note

Read `notes/LAST_RUNNER_COMPATIBILITY_2026_09_29.md` after integration,
together with the frozen protocol and independent verification report.
No executable mathematical evaluation or new scan was performed for this
review. The mathematical deductions pass this internal static audit:

- The two-window existence theorem uses G<=3w and dD>=1/4 correctly.
  Its positive-duration theorem uses the needed strict inequalities
  G<3w and dD>1/4, with closed blockers in the contradiction.
- The definitions F, P and Z correctly distinguish empty final safe set,
  strict cover of positive closed core components, and zero final safe
  duration. F is contained in P, and P in Z; endpoint-only witnesses and
  isolated core points are retained.
- The phase0/half reflection criterion is scoped to the full symmetric
  core period and integer final d. The positive-duration version uses
  the positive-component image rather than isolated points.
- At the cap d=28, the first tight-core component maps to[1/2,3/4]
  modulo1 and its reflection to[1/4,1/2]. Their union is a half-circle,
  so no closed quarter-circle blocker can contain it.
- The post-protocol exceptional-phase calculation is correct and is
  explicitly identified as a subsequent analytic deduction.

For the last item, at d=13 the first two half-period components map to
`[-3/56,1/16]` and `[5/88,3/32]` modulo1. Adding their negatives merges
the image to `[-3/32,3/32]`; hence its containment in the closed blocker
arc occurs exactly when `||theta||<=1/32`. At d=18, the first component
and its reflection alone have union[3/8,5/8]; the other two images are
subsets of this arc. Its length is exactly1/4, so closed blocking is
possible only at theta=1/2 modulo1. The isolated images are four equally
spaced quarter-circle points for d=13 and an antipodal pair for d=18;
they guarantee a surviving point at every phase even when duration is
zero. These are hand consequences of the inherited components, not a
new phase evaluation.

Two scope wording corrections were requested from the coordinator:

1. Restrict the statement that the existence conclusions fall within
   previously credited theory to the common-start integer specializations.
   The arbitrary-phase real-speed extension needs the explicit certificate
   supplied here; the cited ordinary eight-runner theory alone does not
   establish that stronger quantifier. This makes no novelty assertion.
2. Describe the input reuse as no new core or designated physical diagnostic,
   rather than no new physical configuration whatsoever. The declared
   event-cell verification evaluates varying final speeds within its frozen
   domain; those derived values are not extra input fixtures or a broad scan.

Subject to those scope clarifications, no substantive mathematical error
was found in the integrated note. This remains internal AI review, not
external certification or an exhaustive check of the finite remainder.
