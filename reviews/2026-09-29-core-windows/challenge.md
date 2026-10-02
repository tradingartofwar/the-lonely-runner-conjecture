# Adversarial audit: four-runner core and three residuals

September 29, 2026. Scope: selected stationary reference 0; eight common-start
runners with distinct positive integer moving speeds
`{1,4,5,a,b,c,d}`, where `a<b<c<d` are outside `{1,4,5}`.
Threshold is `1/8`; equality is safe. This is internal AI mathematical review,
not independent human review or a novelty assessment. General deductions
remain **HYPOTHESIS / proof candidates** under the repository conventions.

Read: current `AGENTS.md`, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, current README
and HANDOFF material, `TEAM_BRIEF.md`, and the September 28 short-kernel note.
No numerical speed, phase, or word scan was performed for this audit.

## 1. The three-residual width budget survives the challenge

Put `P=1/b >= q=1/c >= r=1/d`. An advancing chain consists of whole open
blocked occurrences, with strictly increasing right endpoints, each old
endpoint strictly inside the next occurrence. Consecutive selected labels
cannot be equal: distinct occurrences of one label are disjoint, with a gap.
Each transition obeys `0<R_next-R_old<p_destination/4`.

For two labels of periods `u>=v`, a return to `u` could contain at most one
intervening `v`, and would advance by less than `(u+v)/4<=u/2`, contradicting
the separation of two occurrences of `u`. Thus `u` occurs at most once and
`v` at most twice. In three labels, choose two consecutive `P` occurrences
if a return is alleged. Their intervening `q,r` chain has at most one `q`
and two `r` occurrences, so their endpoints would differ by less than
`(P+q+2r)/4<=P`, again impossible. Hence the whole triple chain has at most
one `P`, two `q`, and four `r` occurrences.

Consequently its union width is strictly smaller than

`T3 = P/4 + q/2 + r = 1/(4b) + 1/(2c) + 1/d`.

For a chain of at least two occurrences, consecutive strict overlaps make
the union length strictly smaller than the sum of occurrence lengths, which
is at most `T3`. For a single occurrence, its width is itself strictly below
`T3`, since all three periods are positive. Containment, skipped laps, tied
periods in the auxiliary statement, or a non-greedy selected occurrence do
not invalidate these arguments. Occurrence caps do not assert that all
three caps can be attained simultaneously for arbitrary periods.

If a closed window `[L,R]` contains no residual-safe point, its open blocked
cover can be followed from an occurrence containing `L` by successive
occurrences containing each current right endpoint. The next right endpoint
must be larger. The preceding caps prohibit an infinite chain, so it must
eventually pass `R`; otherwise a purported stopping endpoint at or before
`R` is safe or supplies another advance. This yields a chain of width
strictly larger than `R-L`. Therefore `R-L>=T3` suffices for a safe point.
In particular **equality in the width condition is valid**. The conclusion
is existence of a point, not positive safe duration. This lemma permits
arbitrary residual phases, so restricting it to a translated core window
does not silently introduce a common-start assumption for the residual
argument.

## 2. Positive core measure uses a different, explicit assumption

Let `C={1,4,5,a}`, `M=max C`, and let `m(t)` count strict blocked core
constraints. For integer speeds, each has blocked measure `1/4` over the
common period `[0,1]`, hence `integral m=1`. The common start forces all four
constraints to be blocked on the circle arc `||t||<1/(8M)`, of measure
`1/(4M)`. Thus

`measure{m=0} = integral_{m>=1}(m-1) >= 3/(4M) > 0`.

This follows from the exact identity `integral(m-1)=0`; negative excess is
exactly `-1` on the uncovered set. Threshold endpoints are measure zero.
The positive-measure conclusion is false for arbitrary phases in general:
four quarter-duty trains can tile up to safe endpoints. Accordingly one
must keep common start and integer periodicity in this core lemma, while
the three-residual lemma may remain phase-general.

The safe core set is a finite union of closed intervals and possibly
isolated points. Positive measure guarantees at least one positive-length
closed component. Because 0 and 1 are strictly blocked, no safe component
crosses the chosen `[0,1]` cut. A component may lie outside the old window
`J=[9/32,3/8]`; a conclusion about the full period must not be rewritten as
a guarantee within J.

Two quantitative analytic lower bounds are available without a finite
speed evaluation:

1. There are `a+10` elementary blocked arcs on the circle. The four arcs
   containing 0 belong to one component, so their union has at most `a+7`
   components. The safe complement has at most that many components.
   Therefore some safe component has width at least
   `3/[4M(a+7)]`. Isolated safe contacts only reduce the number of positive
   components available to carry the safe measure; they do not spoil this
   lower bound.
2. Let `D(a)=max_{v,w in C} lcm(v,w)`, allowing `v=w`. Every finite safe
   component endpoint has form `(8k+1)/(8v)` or `(8k-1)/(8v)` for some core
   speed v. The difference of two such endpoints is an integer multiple
   of `1/[8 lcm(v,w)]`. Every positive component therefore has width at
   least `1/[8D(a)]`. For `a>=6`, `D(a)<=5a`, so the bound is `1/(40a)`;
   for `a=2,3`, `D(a)=20`, so the bound is `1/160`.

The second observation does not establish which interval is widest. An
exact component enumeration can substantially improve these conservative
bounds, but it is not needed merely to obtain a finite upper bound on b.

## 3. Initial reduction: finite only in the two slow coordinates

The prior H-width result implies that a failure of that sufficient test has
`a in {2,3,6,...,34}`. Absorbing that a into the common-start core is valid.
For any certified core window width `w_a>0`, ordered residual speeds give

`T3 <= 7/(4b)`.

Hence `b >= 7/(4w_a)` suffices (with an integer ceiling where desired).
Using the arithmetic bound above, `b>=70a` suffices for `a>=6`, and
`b>=280` suffices for `a=2,3`. Distinctness actually makes the comparison
`T3<7/(4b)`, but that strict improvement is unnecessary for the closed-window
implication and must not be used to round a nonintegral cutoff carelessly.

Any unhandled cases thus have finitely many possible `(a,b)`, but **c and d
remain unbounded**. This is not an exhaustive finite reduction of all
seven-speed configurations. A table of exact widest core windows would
sharpen b's bound only; a further argument is needed to control the two
remaining coordinates or treat their infinite families analytically.

Speed exclusions matter when enumerating b: it must exceed a and avoid
1,4,5. The subset a=2,3 is allowed, although these numbers are smaller than
some named core speeds. The labels a,b,c,d order only the four residual
speeds and must not be described as the globally four smallest or largest
moving speeds. The selected-reference positive-speed scope does not extend
automatically to another reference, where signed relative velocities and
duplicate absolute speeds can occur.

The later five-core argument reviewed in Section 6 supplies the further
argument bounding c. The statements above describe the first deduction,
not the final stopping point of this continuation.

## 4. Static protocol and implementation audit

Read `PRIMARY_PROTOCOL.md` and `primary_core_windows.py` before their
declared evaluation. They implement exactly the 31 values requested. The
lap-safe interval formula is correct over `[0,1]`; closed intersections and
merging only overlapping or touching pieces preserve the entire safe set,
including isolated contacts. The full-component containment assertion for
every individual runner supplies an actual interval check, in addition to
the reported endpoint and midpoint certificates. The earliest widest tie
rule, exact rational ceiling for `B_a`, and strict minimality check for that
ceiling are internally consistent. Reflection is valid because all core
speeds are integers and common-start.

No implementation defect was identified in this static review. It is not a
separately computed numerical comparison. The protocol correctly excludes
all b,c,d evaluation and the optional integer-separation refinement. At the
time read, its status remained "awaiting coordinator approval"; an explicit
coordinator freeze must precede evaluation. The final theorem and any
finite numerical results remain to be audited once supplied.

The present audit establishes no numerical table, executes no undeclared
finite check, and makes no sharpness claim.

## 5. Second pass: the analytic b >= 48 theorem

Read `peeling.md` after the coordinator requested its adversarial review.
No defect was found in the strongest b cutoff.

The clipping lemma is valid: if a closed interval does not contain a whole
safe gap, it cannot meet two distinct blocked occurrences, since the closed
gap between them would then be contained. At most one blocked interval of
width B can therefore remove length from the given interval, leaving at
most two safe components. This yields `min(S,(L-B)/2)` with the claimed
closed endpoints and without a sampling or generic-position assumption.

Applied to J, the lower bound
`min(3/(4a),3/64-1/(8a))` is correctly directed. For 11<=a<=21 it is at
least `min(1/28,25/704)=25/704`, which strictly exceeds the residual budget
at `(b,c,d)=(48,49,50)`. For a>=22, the inherited H estimate is at most
`65/704<3/32`. Each of the seven explicit small-a intervals lies inside
one fixed-core component and a single safe lap band for a. The narrowest
listed width is `7/160`, also above `25/704`.

In fact this proves b>=48 for **every** admissible a: the a>=22 range has
no upper bound. The inherited a>=35 result is needed to describe remaining
uncertified cases, not as an assumption of the b>=48 implication itself.

The obstruction to lowering this combined sufficient cutoff to 47 is
correctly scoped. At `(a,b,c,d)=(21,47,48,49)`, direct common-denominator
arithmetic gives `H-3/32=335/442176>0` and
`T3-1/28=95/221088>0`. No interval safe for speed21 alone exceeds1/28.
Thus these two specified width tests cannot certify that tuple. This does
not determine the actual common-safe set and is not a loneliness
counterexample.

## 6. Second pass: Q(v), five-core positivity, and the c cutoff

Read `scope.md`. Its uniform `Q(v)<=1/6` argument survives review.
The six displayed fixed-core intervals have total measure3/8. A primitive
of the speed-v blocker indicator minus1/4 has range3/(16v), giving the
interval discrepancy bound exactly as stated. Summing six intervals gives
`Q(v)<=3/32+9/(8v)`, which at v=16 is `21/128<1/6` and decreases thereafter.

I separately checked each of the twelve scaled intersections in the
displayed table by hand, including endpoint-only contacts. The q_A, q_B,
q_C entries and the resulting Q values are all correct. This is a manual
arithmetic audit, not an executed independent numerical comparison. The
coordinator's authorized primary31 computation can additionally recover
these Q values as `3/8 - measure(safe{1,4,5,v})`.

For the five-constraint core, deleting the two blocked subsets from S costs
at most1/3 in measure, so at least1/24 survives. The component estimate
`K=a+b+6` is conservative but valid. Removing one connected open blocked
interval can increase the number of positive components by at most one;
speed v contributes v circular arcs. On `[0,1]`, the two pieces of its arc
through0 only clip boundaryward ends and cannot each split a component.
Consequently the wraparound cut does not create an extra-count problem.
Isolated safe points carry zero measure and do not invalidate the positive
component pigeonhole bound.

Thus a closed five-core window of width at least `1/(24K)` exists. The
two-residual chain has occurrence counts at most1 for c and2 for d, giving
strict span below `T2=1/(4c)+1/(2d)`. Because d>c,
`T2<3/(4c)`, and `c>=18K` suffices, including the threshold equality.
Combining the inherited a cutoff and the b theorem gives

`a<=34, b<=47, K<=87, c<=1565`

for configurations still uncertified by these sufficient routes. The last
inequality is `c<18K<=1566` with c integral. This is a finite set of slow
triples, **not** a finite set of full configurations: d remains unbounded.
No enumeration of those triples has been performed or authorized by this
audit, and the mere finite parameter bound does not verify their cores.

The secondary route in `scope.md` also checks out. Deleting c from a
five-core safe set of measure at least1/24 and at most K components leaves
measure at least `(c-6K)/(32c)`. For c>6K, dividing by the valid component
bound K+c gives the displayed positive core-six width. A single speed d
cannot strictly block an entire closed interval of width at least1/(4d).
The resulting sufficient inequality
`d>=8c(K+c)/(c-6K)` is correct. It does not settle the regime c<=6K.

For integrated exposition, `peeling.md`'s final paragraph about the next
five-core obstruction should be marked as superseded by this Q argument.
The genuine next universal question concerns positive six-core measure.

## 7. Second pass: residual gcd >= 7 gives positive duration

Read `arithmetic.md`. No defect was found in its gcd theorem, which does
not depend on the chain bound.

The universal core-hitting property for a translated g-grid is valid for
g=7,8,9,10. For7, the three open bad arcs each remove at most two points.
For8 and10, the selected parity class has the controlling core runner at
distance at least1/4; the other two runners remove at most1 of4 or2 of5
points respectively. Coprimality needed for these grid permutations is
present. For9, if speed1 blocks three points, their middle lift satisfies
`|x|<1/72`, so speeds4 and5 also block it. That forced triple overlap lowers
the potential union count by two and prevents a cover. The closed interval
J gives the result for every g>=11. Open blocker endpoints are essential
in the exact four-point count and have been handled correctly.

The supplied cosets for g<=6 all avoid the fixed-core safe set, so the
claimed exact limit of the universal grid-hitting property is also correct.
Those cosets are auxiliary obstructions to a certificate; they are not
realized residual-safe configurations or failures of loneliness.

Let `g=gcd(a,b,c,d)` and `T=1/g`. Every residual blocker has measure T/4
on a T-period. The common-start all-four overlap at its two ends has total
length1/(4d), producing excess integral at least3/(4d). Since total mean
multiplicity is1, residual safe measure in one period is at least3/(4d).
The overlap neighborhoods are disjoint because d>=g.

Residual safety repeats under every j/g translation. Integrating the
core-safe hit count over one residual period yields the full common-safe
measure, and this count is at least1 for every phase when g>=7. The lower
bound `measure(full safe set)>=3/(4d)>0` therefore follows. Finite rational
threshold sets turn that positive measure into a positive-length interval.
This uses all fixed-core windows, rather than promising a point in J.

The additional q=3,7,8 anchor filters and their stated small-gcd limitations
are also correct. They remain sufficient certificates and do not replace
the missing argument for every remaining d.

## 8. Adversarial verdict and evidence boundary

The b>=48 implication, uniform Q bound, positive five-core window, c cutoff,
conditional d cutoff, and gcd>=7 positive-duration route survive this
internal analytic challenge. No fatal defect or endpoint counterexample
was identified. All remain proof candidates pending the repository's
required outside review and novelty assessment. The finite Q arithmetic
has additionally been reconciled with the already authorized primary31
outputs by the coordinator-controlled comparison. This reviewer read the
comparison record but did not execute a domain evaluation.

## 9. Final synthesis review

Read `notes/CORE_WINDOW_REDUCTION_2026_09_29.md` and the existing primary
approval, primary report/table, and independent comparison output. The
integrated mathematical claims and scope survive the static review. In
particular, the headline `a<=34,b<=47,c<=1565` is the uncertified-case bound,
whereas `c>=1566` is the sufficient global cutoff after the first two
reductions. Neither claims a finite bound on d.

The synthesis's anchor1/6 strengthens the earlier displayed anchor1/3
without a gap: core speeds1,4,5 are nonzero modulo6, and every integer
speed not divisible by6 has distance at least1/6 at time1/6. Thus absence
of residual multiples of6 supplies a witness. The stated6,7,8 divisibility
restrictions are valid necessary conditions only for failure of these
particular certificates.

Two small exposition edits were sent to the coordinator: explicitly say
`a>=3` when first applying the clipping lemma to J, since its hypothesis
L>B fails for a=2; and say that S consists of A,B,C plus their reflections,
so the reflected intervals are not grammatically placed in the first
half-period. All actual uses of the clipping formula already satisfy its
hypothesis, and a=2 has an explicit separate interval.

The comparison output records1,932 matched numerical fields,12 matched Q
values, and zero disagreements. Its source and output names match the
primary report. I did not rerun it or independently recalculate its aggregate
counts. At this review, the coordinator had already marked the comparator
command rename and manifest creation as pending packaging steps; these do
not affect the mathematical verdict.
