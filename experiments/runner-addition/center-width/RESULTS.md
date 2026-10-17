# Generalization test: required width versus core allowance

October 17, 2026. **OBSERVED:** the frozen rational-center criterion agrees with
all 1,307 independently checked candidate-interval decisions. Its constructed
arm supplies 36 successful critical-interval certificates for 35 distinct
runner configurations. Its independent challenge arm supplies **no successful
single component in any of twelve selected cores**: all 1,199 components have
exact blockers. The deliberately weaker denominator-only shortcut fails in ten
of eighteen center/threshold rows.

The transferable result is an exact criterion and a conditional construction,
not a claim that arbitrary cores possess a universal interval. Its general
mathematical implications remain **same-author proof candidates awaiting
independent review**. The finite evidence and those implications are distinct.

Rule committed before case selection:
`6ea4ca25250d070380f174665d7ad9dfc7824e32`.
Execution freeze: `c2db06c6daa43cd71297fd78acf6bad702c5567d`, 11 pinned files.
[Rule and derivation](RULE.md), [protocol](PROTOCOL.md), [inputs](config.json),
[primary](run.py), [alternate verifier](verify.py), [manifest](manifest.json).

## 1. The mathematical relationship

For a reduced rational center c=u/v and threshold 0<d<1/2, define

    H_d(c) = max_{1<=j<=v} max(0,d-||j*c||)/j.

For fixed positive integer core speeds S, define

    G_{S,d}(c) = min_{s in S} (||s*c||-d)/s.

The proposed exact criterion for the closed interval `[c-h,c+h]` is

    H_d(c) <= h <= G_{S,d}(c).

Here h is HALF-width. H is the minimum room needed to escape every added-speed
unsafe gap. G is the maximum room the fixed core permits without crossing one
of its unsafe gaps. Their overlap supports a universal core-safe source.

The first maximum is finite because the phase deficit repeats modulo v, while
division by the added speed only makes a later occurrence less demanding. A
maximizing speed supplies a blocker whenever h<H. The core inequality checks
every constraint on the same interval. Once core safety holds, core-speed
duplicates are automatically harmless to the contact criterion; they remain
excluded when describing distinct-runner configurations.

This goes beyond fitting the original three cases: the derivation applies to
arbitrary rational centers and positive integer cores under its stated
hypotheses. It neither proves that H<=G somewhere for every core nor establishes
the general Lonely Runner conjecture. A useful formula need not be a uniform
guarantee of success.

The simplest exposed original success, S={1,2,3,4,5,7,10,19} at d=1/10,
has leader midpoint 159/1330. H=15/2128 is controlled by added speed 8;
G=6/665 is controlled by core speeds 7 and 19. The positive difference 3/1520
explains why the interval has enough room. This was development evidence used
before the freeze, not counted again as validation.

## 2. Constructed families: what the positive evidence means

For six new centers and n=8,10,12, the rule computes a critical interval at
h=H. It then lists every positive integer speed safe throughout that interval,
up to the analytic limit floor((1/2-d)/H), with d=1/n. Any n-2 distinct speeds
from the same eligible list give a conditional n-runner family after adding
one distinct positive integer speed to reference 0.

| Center | Eligible speeds at n=8 | At n=10 | At n=12 | Denominator-only shortcut fails at n |
|---|---:|---:|---:|---|
| 2/11 | 12 | 17 | 23 | none |
| 3/13 | 12 | 21 | 27 | 8 |
| 5/17 | 14 | 31 | 35 | 8 |
| 7/19 | 15 | 28 | 41 | 8,10 |
| 9/23 | 10 | 16 | 20 | 8,10,12 |
| 11/29 | 12 | 20 | 28 | 8,10,12 |

All eighteen rows have enough eligible speeds. The frozen smallest/largest
selection gives 36 labeled core/interval instances and 35 distinct (n,core)
configurations: the n=8 core {1,2,4,6,7,9} occurs twice at different centers.
Every critical interval succeeds. All 36 half-width reductions h=H/2 fail at
the recorded critical speed while remaining core-safe. Of the 36 shortcut
intervals h=d/v, sixteen succeed and twenty fail, corresponding to the ten
failing center/threshold rows above.

These are checks of a conditional construction, not an unbiased estimate of
success on arbitrary inputs. The symbolic implication for every eligible
subset depends on the proof; the combinations were not enumerated. Physical
witnesses retain the selected source interval and allow time to depend on r.

### A concrete counterexample to the shortcut

Take c=7/19, d=1/10 and the constructed core
S={1,2,4,5,6,7,9,10}. The denominator-only guess gives

    h0 = 1/190,    I0 = [69/190,71/190].

The admissible added speed r=8 blocks the entire interval:

    ||8c|| + 8h0 = 9/95 < 1/10.

Equivalently I0 lies strictly inside the unsafe gap (29/80,31/80).
The correct critical half-width is instead

    H = 9/1520,    I = [29/80,569/1520].

At the left endpoint 29/80, speed 8 is exactly distance 1/10 from an integer;
the core is safe there too. The extra half-width 1/1520 restores the equality
witness. A nonzero residue class, rather than the denominator-divisible case,
sets the required room. This is an exact failure mechanism, not a sampling
anomaly. The full criterion was not changed after observing it.

### A capability beyond the earlier sufficient anchor class

The same successful interval lies strictly between 1/3 and 3/8. Any rational
A/B strictly between those neighbors must have B>=11: the positive integers
3A-B and 3B-8A satisfy

    B = 8(3A-B) + 3(3B-8A) >= 11.

Consequently I contains no allowable anchor with denominator <=10 for the
earlier d=1/10 anchor rule. The new criterion certifies this particular interval
even though that old certificate cannot. This does not claim that the entire
core lacks a different interval admitting an old anchor.

This comparison is a retrospective interpretation of an existing validated
row, preserved in the [certificate export](results/CERTIFICATES.json). It is
not a separately frozen prediction or an additional validation family.

## 3. Independently selected cores: the negative evidence

The twelve challenge inputs were chosen arithmetically after the rule freeze,
without evaluating whether they met its hypotheses. All use j=1,...,8, d=1/10,
stationary reference 0 and a distinct positive integer added speed.

| Core recipe | Offset k | Complete components | Universal single components | Distinct recorded blocker inputs within this core |
|---|---:|---:|---:|---:|
| j+k | 2 | 4 | 0 | 2 |
| j+k | 7 | 8 | 0 | 3 |
| j+k | 17 | 22 | 0 | 4 |
| j^2+k | 1 | 44 | 0 | 8 |
| j^2+k | 3 | 52 | 0 | 10 |
| j^2+k | 7 | 58 | 0 | 11 |
| j^2+j+k | 1 | 57 | 0 | 10 |
| j^2+j+k | 3 | 61 | 0 | 8 |
| j^2+j+k | 7 | 71 | 0 | 11 |
| j^3+k | 1 | 260 | 0 | 12 |
| j^3+k | 3 | 266 | 0 | 12 |
| j^3+k | 7 | 296 | 0 | 14 |
| **Total** | | **1,199** | **0** | **105** |

All components have H greater than their permitted half-width G. This includes
24 isolated components; equality structure was retained. The critical blocking
speed is at most 17 on this domain, and H evaluation terminates after at most
19 terms. Those numerical limits are bounded observations, not new universal
bounds. A critical speed need not be the smallest blocker for the actual
component.

Because every connected core-safe subset lies in a maximal component and
inherits its blocker, no fixed connected source works for all added speeds
in these twelve cores. This does not establish a two-component upper bound;
no minimum-menu calculation was performed here. Every one of the 105 checked
challenge blocker children has a safe witness elsewhere. The constructed arm's
36 blocker-child records are nonempty as well. These finite child checks do
not imply all-r full-core coverage for the challenge families.

The absence of successful single components is evidence against extending the
original three successes to arbitrary cores. It is consistent with the exact
criterion, which predicts failure when required room exceeds available room.
The criterion has not made every problem simple; it has made the conditions
and the boundaries of one useful simplification explicit.

## 4. Verification, work and reproduction

[Alternate verification](results/VERIFICATION.json) is PASS, with no observed
false positives or false negatives, no unresolved family cases and no frozen
source edits. The intentional one-term budget control correctly remains UNKNOWN;
the equality control succeeds at its closed endpoint. [Replay](results/REPLAY.json)
is byte-identical on Python 3.12.14. No execution discrepancy or timeout occurred.

| Work or verification | Count |
|---|---:|
| Primary family H terms, excluding supplied controls | 10,214 |
| Primary eligible-speed predicates | 934 |
| Challenge core input bands / resulting components | 5,800 / 1,199 |
| Complete blocker-child constructions | 141 |
| Candidate witness recoveries: finite / tail controls | 434 / 204 |
| Alternate exact H certificates, including equality control | 1,218 |
| Alternate critical-width band queries | 10,201 |
| Alternate candidate decisions / band queries | 1,307 / 5,486 |
| Alternate reconstructed core sets / child sets | 12 / 141 |
| Alternate threshold events | 155,948 |
| Alternate checked strict blockers / physical witnesses | 1,255 / 780 |

The 141 child records are counted per selected core/center instance, not as
globally deduplicated physical configurations. The 780 witness checks include
638 candidate recoveries, 141 child witnesses and one equality control. The
replay repeats primary work. These counters do not establish an efficiency or
runtime advantage. Constructed intervals require direct core-margin checks;
the complete constructed core is not built unless a blocker child is needed.

The verifier imports the older threshold-event helpers, never the new H
evaluator or primary interval checker. It validates each critical-width interval
with safe-band intersections plus a width tail, and a tight critical gap shows
that any smaller half-width fails. It separately verifies all actual interval
decisions, palettes, complete challenge geometry, children and physical phases.
Term bookkeeping is reproduced in ordinary rational arithmetic; this is
distinct from the alternate decision check. Both implementations have the same
AI author, so agreement is not independent human or formal proof review.

From repository root, using fresh output/checkpoint paths:

```sh
timeout 240s python experiments/runner-addition/center-width/run.py --freeze c2db06c6daa43cd71297fd78acf6bad702c5567d --output /tmp/center-width-results.json --checkpoint-dir /tmp/center-width-primary
timeout 240s python experiments/runner-addition/center-width/verify.py --input /tmp/center-width-results.json --output /tmp/center-width-verification.json
timeout 240s python experiments/runner-addition/center-width/run.py --freeze c2db06c6daa43cd71297fd78acf6bad702c5567d --output /tmp/center-width-replay.json --checkpoint-dir /tmp/center-width-replay
cmp /tmp/center-width-results.json /tmp/center-width-replay.json
```

[Complete results](results/RESULTS.json): 772,721 bytes, SHA-256
`ac7221a90224b8c547eb159e343efa45ef61271daedc9ef8ed5e692fa4c7783e`.
The export is bound to these bytes. No broader case scan or post-outcome refit
was performed.

## 5. What transfers, what remains open

Retained distinctions are the required half-width H, permitted half-width G,
their controlling speeds, whole-interval core validity, equality, admissible
speed domain and same-time witness recovery. The small record supports a
specified-center decision and conditional core construction. It does not
preserve every safe time, optimal distance, every reference or a minimum menu.
Recover the exact source before asking those questions.

The general criterion is a mathematical proof candidate; the eighteen
construction rows and twelve challenge cores are its finite stress test.
Neither the earlier three successes nor the constructed successes establish a
universal single-source theorem. The negative arm explicitly blocks that leap.

**Next proposed:** investigate a bounded, complete way to select or reject
candidate centers directly from core constraints, then compare that method
with full safe-set construction on a separately frozen domain. The current
criterion tests a supplied center; it does not yet solve that selection problem.
Independent review of the short derivation remains open. No new center-selection
algorithm, broader validation, external review or outreach has run.
