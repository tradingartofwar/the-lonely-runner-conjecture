# A center-dependent width criterion for one universally sufficient interval

October 17, 2026. Rule version 1, to be committed before choosing the new
validation families. Source branch head: `72c7c67ec8a92537e9c1c65b73e876ed8fccaf73`.
**HYPOTHESIS / proof candidate awaiting independent review.** The derivation
and proposed implementation were developed with AI. No novelty claim.

## Question and inherited work

When does one fixed core-safe interval supply a possibly different safe time
for every admissible positive integer added runner speed? The earlier
[placement theory](../placement/THEORY.md) already supplies an exact obstruction
predicate and a sufficient low-denominator rational-anchor rule. Its validation
explains the three original successful families and retains two failures of
that sufficient class. Those are exposed development results, not fresh tests.

This refinement separates the width needed by all possible added speeds from
the width permitted by a particular core. It uses modular arithmetic and
interval geometry; it is not a new language. It does not assume the core's
complete safe set has first been constructed.

## 1. Definitions

Let `0<d<1/2` and let `c=u/v` be reduced, with `0<c<1`, `v>0`.
Write `||x||` for distance to the nearest integer. Define the nonnegative
phase deficit and its required half-width by

    D_d(c,j) = max(0, d-||j*c||),
    H_d(c) = max_{1<=j<=v} D_d(c,j)/j.

For a nonempty finite set S of distinct positive integer core speeds, define

    G_{S,d}(c) = min_{s in S} (||s*c||-d)/s.

H is a minimum required HALF-width, while G is a maximum permitted HALF-width.
Neither is the total interval width. In particular `H>=d/v>0`, from j=v.

For a closed interval `I=[c-h,c+h]`, with h>=0 and I contained in [0,1]:

1. **Universal contact:** I meets the d-safe set for every positive integer
   added speed exactly when `h>=H_d(c)`.
2. **Core safety:** I is wholly d-safe for every s in S exactly when
   `h<=G_{S,d}(c)`.
3. **Combined criterion:** I is a core-safe universal source exactly when
   `H_d(c)<=h<=G_{S,d}(c)`. A source centered at c exists exactly when
   `H_d(c)<=G_{S,d}(c)`; the core condition itself then keeps its endpoints
   inside (0,1).

For the Lonely Runner application, include stationary reference 0 and common
start, let `n=|S|+2`, use `d=1/n`, and exclude r in S as added speeds. Once I
is core-safe, excluded core speeds already have safe contact throughout I.
Thus checking all positive integer r is equivalent to checking only admissible
r for this question. A blocking r for a core-safe I cannot belong to S.

## 2. Proof of the universal-contact criterion

The existing exact obstruction gives

    I meets a safe band for r iff ||r*c||+r*h >= d,

including equality. This is equivalent to `h>=D_d(c,r)/r`.
For any positive integer r, take its least positive residue j modulo v,
so `1<=j<=v`, `r=j+q*v` with q>=0. Then

    ||r*c|| = ||j*c||,
    D_d(c,r)/r = D_d(c,j)/(j+q*v) <= D_d(c,j)/j.

The largest requirement in each residue class therefore occurs at its least
positive representative. Taking the maximum proves both necessity and
sufficiency. This is a finite symbolic criterion valid for arbitrary rational
centers, not merely the three earlier families.

If j* attains the maximum and h<H, then
`||j* c||+j* h<d`; j* is an explicit blocker. At h=H, that same constraint
touches a safe boundary. Shrinking a successful critical interval produces a
counterexample with a specified blocking speed; equality must not be discarded.

## 3. Proof of core safety and direct construction

A connected interval is wholly safe for speed s precisely when its phase
interval stays within one closed safe band. The distance from s*c to the
nearest unsafe gap boundary is `||s*c||-d`, so the necessary and sufficient
condition is

    s*h <= ||s*c||-d.

Intersecting these inequalities over S proves h<=G. A positive integer core
speed is unsafe at every integer time, so such a core-safe interval cannot
cross 0 or 1 when its center lies strictly between them.

For fixed c,d,h, the eligible individual core speeds form the finite palette

    P(c,d,h) = {s>=1 : ||s*c|| >= d+s*h},
    s <= floor((1/2-d)/h).

Thus if h>=H, any selected set of distinct speeds from this SAME palette
inherits the same universal interval. For an n-runner statement at d=1/n,
there must be at least n-2 distinct eligible speeds. An insufficient palette
is a failure to construct that n-runner family, not a physical counterexample.
The rule does not permit a separate center or interval for each core runner.

This gives a construction from speeds and a proposed center: calculate H and
G, compare them, and retain any h in [H,G]. Finding a favorable center remains
a separate search problem; no guarantee is claimed for every core.

## 4. Exact evaluation, witness recovery and budgets

Evaluate `D_d(c,j)/j` in increasing j from 1 to v, retaining the maximum M and
the first maximizing j. Once M>0 and `d/(j+1)<=M`, evaluation may stop: for
every later integer k, `D_d(c,k)/k<=d/k<=d/(j+1)<=M`. This bound is valid even
without the residue reduction. Rationality guarantees a positive term by j=v.
A budget stop before the denominator limit or that inequality is UNKNOWN,
not a decision. The exact criterion itself has no experimental search cap.

Given a certified interval [a,b] and an admissible r, physical recovery uses
the inherited first-contact formula

    lap = ceil(r*a-(1-d)),
    t = max(a,(lap+d)/r).

Its band reaches a and universal contact guarantees t<=b. Check the core and
added-runner phases at the SAME t. The witness can move with r; retaining only
the midpoint or endpoints is not an adequate substitute.

## 5. Simplest exposed success

The original (p,q)=(1,2) core is S={1,2,3,4,5,7,10,19}, at d=1/10. Its
published leader `[21/190,9/70]` has

    c = 159/1330, h = 6/665,
    H_d(c) = 15/2128, attained at added speed 8,
    G_{S,d}(c) = 6/665, controlled by core speeds 7 and 19,
    G-H = 3/1520 > 0.

The lower requirement and upper allowance overlap. This explains the success:
the core permits enough room around this center to escape every added-speed
unsafe gap. The maximum is reached by speed 8, and the early-stop bound closes
after 14 terms. These calculations use an already exposed development case;
they do not count as new validation.

The old anchor construction offers another sufficient description of this
same example, via time 1/8 and the interval [9/80,1/8]. The new midpoint rule
does not replace that simpler witness formula when it is adequate. Its added
capability is an exact threshold and blocker for any rational midpoint.

## 6. Claims to attack in validation

Primary claim: the complete criterion and direct core-safety condition hold on
new families, with exact agreement against independently structured interval
and phase calculations. Search for false positives and false negatives.

A deliberately weaker proposed shortcut is also to be tested:

    H_d(u/v) = d/v for every reduced rational center.

Only j=v gives the right-hand side; other residue classes may demand more
room. This shortcut is not a theorem or a prediction of the full criterion.
Actively seek a concrete counterexample rather than assuming the divisibility
case is always controlling. Also test h=H exactly and smaller core-safe
intervals, where the recorded critical speed should block them.

## 7. Validation and representation commitments

Commit this rule BEFORE choosing new families. Then freeze a bounded protocol,
inputs, implementations, budgets and failure criteria before executing them.
Use both families built from the sufficient palette and separately selected
core families that were not chosen for satisfying it. Palette successes check
the conditional construction; they are not evidence that arbitrary cores meet
its hypotheses. Keep those two arms separate.

Compare against direct safe-band intersection and the width-tail finite
reduction, without importing the new H evaluator into the alternate verifier.
Verify complete core geometry where a conclusion quantifies over every
component. Preserve singleton failures, equality witnesses, exclusions, search
limits and any disagreement. For a rejected interval, separately ask whether
the complete core has another witness at its blocker; source failure is not
physical nonexistence. Do not modify this rule in response to validation;
preserve any needed revision as a later version with a fresh validation domain.

The supported outputs are a one-interval decision, a critical blocker or an
all-r witness rule, and conditional families of suitable cores. The record
retains c,h,d, S, the shared-time relation, exact maximum/argmax certificate,
core margin and physical recovery. It omits full safe sets, optimal loneliness,
other reference runners and multi-component minima. Recover the pinned exact
interval model for those questions. Complete component enumeration is needed
only for claims about every possible interval in a core, not for checking a
specified center and interval.

All general implications remain proof candidates under repository governance.
Finite checks can refute an implementation or proposed statement; they cannot
by themselves establish the unbounded mathematical claim. No statistical
held-out guarantee, intrinsic complexity, runtime superiority, general Lonely
Runner proof or novelty assertion follows.
