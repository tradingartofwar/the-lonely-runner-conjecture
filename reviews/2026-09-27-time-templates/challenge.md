# Challenge review: template classes are not robustness classes

September 28 UTC, for the September 27 Pacific protocol. Scope:
`{0,1,4,5,6,7,11,V}`, positive integer V outside `{1,4,5,6,7,11}`,
reference 0, eight total runners, threshold 1/8. Only speed 11's starting
phase theta varies. The four tested times are exactly those frozen in the
protocol; no additional template search, speed list, or phase grid is used.
Material AI involvement: mathematical review and writing. General arguments
are supplied **HYPOTHESIS / proof candidates** under repository rules.

**Independent classification:** the four-time menu has margin 2/15 on 96
residue classes modulo 120, exactly 1/8 on 21 classes, and fails on three
classes. The failures are `V=0,32,88 mod120`. These statements describe the
menu, not the fraction of Lonely Runner inputs solved or the actual status
of every configuration in a residue class.

## 1. Each pair's margin is constant, not merely bounded below

For a fixed reflected pair of times, let c be the minimum unchanged-runner
distance at either time. It is the same at both times because unchanged
speeds are integers. Let d be the circular separation of runner 11's two
phases, and write

`M(theta)=max_i min(c,||11t_i+theta||)`.

The triangle inequality gives
`max_i ||11t_i+theta|| >= d/2`. In both frozen templates, c<=d/2 for
every V. Therefore

`M(theta)=min(c,max_i||11t_i+theta||)=c`

for **every** theta. The unchanged constraints also supply the upper bound
c at both times. This establishes pointwise constancy rather than only a
worst-phase guarantee.

For the eighth pair `1/8,7/8`, the five fixed unchanged speeds have distances

`(1/8,1/2,3/8,1/4,1/8)`.

Runner 11's phases are 3/8 and 5/8, so d=1/4. Consequently

`M8(theta)=min(1/8,||V/8||)`.

Since V is an integer, this is zero if 8 divides V and exactly 1/8 otherwise.
The pair never gives a strict witness: unchanged speeds 1 and 7 remain at
threshold independently of V and theta.

For the fifteenth pair `7/15,8/15`, the fixed unchanged distances are

`(7/15,2/15,1/3,1/5,4/15)`.

The chosen phases are 2/15 and 13/15, so d=4/15. Thus

`M15(theta)=min(2/15,||7V/15||)`.

The only failing phase residues of 7V are 0,1,14 modulo 15. Multiplication
by the inverse 13 of 7 gives:

| V modulo 15 | Constant pair margin |
| --- | ---: |
| 0 | 0 |
| 2 or 13 | 1/15 |
| Every other residue | 2/15 |

The last row is strict because 2/15>1/8. There is no equality-only case for
this template: its discrete possible caps jump from 1/15 to 2/15 across
the required threshold.

## 2. Union counts, exact failures, and admissibility

The best margin over all four times is the maximum of these two constants.
Hence no new phase-dependent rescue appears merely by combining the pairs.
That conclusion uses pointwise constancy; for arbitrary nonconstant pair
profiles, union coverage need not equal the union of their robust classes.

| Pair results | Classes modulo 120 | Four-time result |
| --- | ---: | --- |
| Both pass | 84 | Strict, margin 2/15 |
| Only fifteenth pair passes | 12 | Strict, margin 2/15 |
| Only eighth pair passes | 21 | Equality-level menu margin 1/8 |
| Neither passes | 3 | Fails the threshold at all four times |

The Chinese remainder calculation for the failures is short. Put V=8k.
The condition `V=0,2,13 mod15` gives `k=0,4,11 mod15`, hence
`V=0,32,88 mod120`. Their least positive admissible representatives are
120,32,88, respectively. All three are distinct from the six excluded speeds.

At the failed classes, all four candidate times fail for **every** theta,
already because of unchanged runner V. The four-time margin is zero on
`V=0 mod120` and 1/15 on the other two classes. This is stronger than an
inconclusive all-phase lower bound, but remains failure of these four times.

The 21 equality-level classes are not 21 classes of tight configurations.
Other times may be strict even when this menu's best separation remains
exactly 1/8. Likewise the three failures do not establish absence of some
other robust pair, a phase-specific witness, or a common-start solution.

Period 120 is sufficient because it preserves all four fixed-time phases.
It is not asserted minimal. The forbidden values 1,4,5,6,7,11 remove six
individual integers, not their whole residue classes; each class still has
admissible positive representatives. V is a parameter and need not be the
fastest speed for the smallest admissible values.

## 3. A distance margin does not give a V-independent time width

On every strictly covered class, a winning fifteenth-pair time has every
distance at least 2/15. The excess over threshold is 1/120. Circular
distance for speed v is v-Lipschitz, so the closed radius

`r(V)=1/(120 max(V,11))`

around that time is safe, with strict interior. Both candidate times are
far enough from the observation endpoints that these intervals lie in
[0,1]. Consequently this compact certificate gives

`D_V(theta) >= 1/(60 max(V,11))`

for all theta on the strictly covered classes.

A sharper form uses the actual residue distance `d_V=||7V/15||`. The
unchanged runners have safe symmetric radius

`R(V)=min(1/480,(d_V-1/8)/V)`,

and runner 11 has guaranteed radius `rho=1/1320`. Its safe lap has width
3/44, greater than 2R(V), so it cannot truncate both sides of the unchanged
interval. This yields

`D_V(theta) >= R(V)+min(R(V),rho)`.

At V=16 the expression recovers the earlier compact bound 1/352. As V
grows within a fixed residue class, the V-runner's time margin generally
shrinks like 1/V. The constant **distance** margin 2/15 must not be turned
into a uniform positive **time** width by ignoring that speed. These are
sufficient local widths; they do not identify the true minimum duration.

## 4. How to interpret the three representative diagnostics

The diagnostic question is independent of the fixed-time classification.
Let A_V be the complete safe set of unchanged speeds and P_V its image
under `11t mod1`. For nonempty compact P, the supplied criterion is
`c(P)>=1/4` for all-phase existence. With B the closure of its positive
interval support, all-phase positive duration is equivalent to B being
nonempty and `c(B)>1/4`. The weak inequality for points and strict inequality
for positive duration are essential; replacing either by the other loses
the equality case.

The completed `diagnostics.json` and separately reconstructed
`diagnostics_verification.json` agree on all three prescribed inputs:

| V | c(P)=c(B) | Common-start duration | Prescribed common-start witness | Its minimum distance |
| ---: | ---: | ---: | ---: | ---: |
| 120 | 183/224 | 53/3360 | 821/2688 | 53/384 |
| 32 | 1387/1792 | 9/896 | 1097/3584 | 73/512 |
| 88 | 183/224 | 37/2464 | 437/1408 | 97/704 |

In each case P=B. All 38 unchanged-safe components across the three cases
have positive length; none is an isolated time. Each covering length is
strictly greater than 1/4, so the supplied criterion certifies positive
duration for every phase of runner 11 at each representative. Thus all
three are actual failures of the frozen menu despite having the stronger
robust property. The common-start witnesses have minimum distance strictly
above 1/8 and follow the frozen midpoint selection rule. The primary and
verification summaries disclose no endpoint or quantifier discrepancy.

This review independently derives the template formulas and audits the
reported diagnostic implications. The numerical full-set reconstruction
is the separate verifier's reproduced result; it was not rerun here and
no extra representatives or phase evaluations were introduced.

These tests can show whether a missed representative has some other robust
pair, by the previously supplied pair-completeness argument. They do not
find that pair or supply a new arithmetic selection rule. A directly
checked common-start witness answers only theta=0; it must not be used as
evidence for all theta.

Most importantly, period 120 applies only to the four template evaluations.
It does **not** make A_V, P_V, B_V, actual duration, or phase robustness
periodic in V. Results for 120,32,88 cannot classify every integer in the
corresponding missed residue classes without another argument.

The two-time completeness result has the right conditional scope: if a
configuration is robust to all phases at this threshold, some suitable
pair exists. It does not say that one of the two particular templates must
be that pair. Failed-template diagnostics therefore cannot falsify that
general geometric argument.

## 5. Existing coverage and the obstruction to another fixed rational menu

The archived `notes/VARIABLE_SPEED_FAMILY.md` already supplies a common-start
witness for every admissible V. The fixed-window tail argument in
`notes/CORE_EXCHANGE_NEIGHBORS_2026_09_27.md` supplies positive common-start
duration for every V>=29. Every admissible member of each missed class is
in that tail. This covers their whole classes at theta=0 by an existing
analytic argument; it does not extend the three new all-phase diagnostics
to those classes. The old speed-11 containment is a common-start relation
and cannot simply be reused after shifting that runner.

The variable-speed note also already records the decisive obstruction to
any finite fixed menu of rational times. A sufficiently large common
multiple of their reduced denominators is an admissible positive integer V
that collides with reference 0 at every menu time. It defeats that menu for
every phase of runner 11. For these four times, denominator multiple 120
accounts directly for the residue-zero failure. Appending finitely many
fixed rational pairs can move this obstruction but cannot remove it over
all admissible V.

This statement is restricted to finite rational menus independent of V;
it makes no claim about irrational menus or adaptive choices. The useful
next certificate question is a V-dependent arithmetic pair-selection rule
for the stronger all-phase property. Pair completeness is conditional on
that property holding, and does not establish it or construct the pair.
Selecting a pair from a fully reconstructed safe set is a retrospective
certificate, not yet the desired selection rule. This is a next question,
not an additional investigation in the current protocol.

## 6. Evidence boundaries

The symbolic classification above uses only the four prescribed substitutions
and the circle triangle inequality. Its unbounded conclusion rests on those
formulas and integer residues, not on checking 120 independent physical
configurations. The residue counts are an exact description of two templates
within one fixed family, not a probabilistic success rate or a portion of
the Lonely Runner Conjecture.

The current small-gcd 56/113 priority is a separate preserved inquiry. This
classification should not be described as resolving arbitrary four-fast-runner
placement or reviving the parked +7/+9 investigation. Existing common-start
coverage of this family should be compared before claiming new existence
coverage; the all-phase quantifier and compact certificate are the distinct
targets here.
