# Unrestricted sources: one imposed restriction mattered, five two-source minima remain

October 17, 2026. **OBSERVED:** the complete component classification resolves
all six selected altered cores. The odd-derived core has two symmetric choices
of a single sufficient component. The other five cores have an exact blocking
speed for every component. Combined with their existing two-component upper
bounds, this gives unrestricted minima of one and two respectively **within
fixed connected core-safe component menus**.

The widest-interval requirement had imposed an unnecessary second component
in one case. The earlier required-widest result remains correct for its stated
question. Removing that requirement changes the minimum for the odd-derived
core and strengthens the lower bound for the other five.

All-r sufficiency and unrestricted minimum conclusions remain **same-author
proof candidates awaiting independent review**. These are not intrinsic
description lower bounds or a general Lonely Runner result.

Execution freeze: `422c1aad5a4930bcb917a76d0aa67f986c0551df`, 18 pinned files.
Source: `20a112c135740d8af881bbb6539b2419e0ee0c42`.
[Protocol](PROTOCOL.md), [derivation](DERIVATION.md), [config](config.json),
[runner](run.py), [alternate verifier](verify.py), [manifest](manifest.json).

## Complete decisions

Core labels refer to the preceding [anchor-removal study](../anchor-removal/RESULTS.md),
whose complete geometry and verified two-source certificates are pinned.
No speed list changed in this study. Reference is 0, common start, threshold
d=1/10, and adding a positive integer speed absent from the core gives n=10.

| Core label | Eight core speeds | Components | Universal single components | Blocked components | Unrestricted minimum candidate |
|---|---|---:|---|---:|---:|
| Odd-derived | 1,3,5,7,10,11,13,15 | 14 | IDs 0,13 | 12 | 1 |
| Primes-derived | 2,3,5,7,10,13,17,19 | 20 | none | 20 | 2 |
| Squares-derived | 1,4,10,16,25,36,49,64 | 42 | none | 42 | 2 |
| Powers-of-two-derived | 1,2,4,10,16,32,64,128 | 64 | none | 64 | 2 |
| Clustered-derived | 10,12,13,17,19,23,29,31 | 28 | none | 28 | 2 |
| Irregular-derived | 3,8,14,27,35,46,62,90 | 58 | none | 58 | 2 |

All 226 components were classified, including four isolated points. None
remained UNKNOWN. The two successful components are reflections under t->1-t,
not two unrelated mechanisms. All 224 other components have saved blockers.

## A narrower interval answers the broader question

For the odd-derived core the required widest interval was

    L = [31/130,13/50], width 7/325, cutoff 10.

It fails at added speeds 4 and 8. Its entire interval lies strictly inside
both unsafe gaps (9/40,11/40) for speed 4 and (19/80,21/80) for speed 8,
each centered at time 1/4. Width alone does not capture this placement.

The earlier menu paired L with component 0. That former repair component is
already sufficient by itself:

    I = [11/100,19/150], width 1/60, cutoff 12.

The admissible finite remainder below 12 is exactly {2,4,6,8,9}. Speeds 10
and 11 are already in the core and therefore excluded as added speeds.

| Added speed | A certified time in I |
|---|---|
| 2,4,6,8 | 11/100 |
| 9 | 11/90 |

For every r>=12, the interval width is at least the unsafe-gap width 2d/r,
so some safe contact exists, including equality. The inherited first-contact
formula supplies that time. This proves the sufficiency candidate using I's
own cutoff, without borrowing L's tail guarantee. It is one fixed interval,
not one fixed time for every added speed.

Its reflected partner is [131/150,89/100], component 13, with the same width
and cutoff. Both were checked rather than deduplicated by assumed symmetry.
Their finite/tail witnesses, phases and laps are saved. The endpoint and gap
interpretation above is a deduction from those exact records, not a separately
frozen predictive rule.

The useful distinction is now explicit: the widest interval has the shortest
width-based tail cutoff, but that does not minimize the number of components
needed for all admissible speeds. Interval placement and excluded core speeds
can make a narrower interval the better answer.

## Why five cores still need two connected sources

For a closed component [a,b], a recorded blocker r has an integer m satisfying

    r*b-d < m < r*a+d.

Thus every time in that component lies inside the same open unsafe gap for r.
Equality at distance d is preserved, so a boundary contact cannot be mistaken
for a blocker. Every component in each of the five remaining complete cores
has such a certificate. Any smaller connected core-safe interval lies inside
one of these maximal components and inherits its blocker.

| Core label | Distinct recorded blocker speeds | Classification checks | Complete children at blockers |
|---|---|---:|---:|
| Odd-derived | 2,4,6,8,9 | 50 | 5 |
| Primes-derived | 1,4,6,8,9 | 64 | 5 |
| Squares-derived | 2,3,5,6,7,8,40 | 134 | 7 |
| Powers-of-two-derived | 3,5,6,7,8,9 | 204 | 6 |
| Clustered-derived | 1,2,3,4,5,7,8,9 | 160 | 8 |
| Irregular-derived | 1,2,4,5,6,7,9 | 198 | 7 |
| **Total** | counted separately per core | **810** | **38** |

All 220 blocked positive-width components encounter a blocker no larger than
9. The four squares-derived singletons use their reduced denominator 40 as an
analytic blocker; it is not claimed to be their smallest blocking speed.
Positive-component cutoffs range up to 2,070, but a found blocker suffices to
reject a component without exhausting its whole finite domain. Universal
components do require exhausting their own finite remainders.

All 38 distinct (core,blocker) child sets are nonempty. Each has an earliest
physical witness and a witness recovered from the prior two-component menu.
The quantifiers remain different: every fixed component can fail somewhere,
while the complete core can still provide a witness elsewhere at that speed.

The existing two-component certificates supply upper bounds. Exhaustive
component blockers supply lower bounds for the five genuine two-source cases.
A disconnected union may be named as one object, and another algorithm may
describe the witnesses differently; these component counts do not constrain
every possible representation or imply intrinsic incompressibility.

## Verification and costs

The primary reuses the unchanged placement classifier, with its optional
rational-anchor search disabled. An `anchor:null` field means unsearched.
It reuses the six pinned complete cores (1,042 original input bands, 226
components); no fresh primary core construction is claimed. The new primary
work includes 810 family obstruction checks, 38 complete child constructions,
18 first-contact witness recoveries for the two universal components, and 28
fresh dispatcher contacts for the 38 old-menu recovery outputs. The remaining
dispatcher outputs use cached exception points.

Five supplied-interval controls pass: empty finite remainder, tail equality,
singleton, ordinary blocker and intentional UNKNOWN from the r cap. They add
7 obstruction checks, 2 blocker certificates and 8 universal witness records.
They are behavior fixtures, not new complete physical cores or new LRC cases.

[Alternate verification](results/VERIFICATION.json) reconstructs all 6 complete
cores and 38 child sets using 16,138 threshold events. It checks all 226
components with safe-band intersections, all 817 obstruction records including
controls, 226 blocker certificates including controls, 26 universal witness
records including controls, and 76 physical repair witnesses. It imports no
primary classifier or checker. Shared prior helper code and the same AI author
mean this is not independent human review or formal certification.

[Replay](results/REPLAY.json) matches byte-for-byte on Python 3.12.14. There
were no post-freeze code changes, execution discrepancies, timeouts, unknown
family components or child-audit budget stops. No global runtime or method
superiority comparison was performed. These inputs were already exposed; this
is an exhaustive new question on them, not held-out validation of a learned rule.

## Reproduction and certificates

From repository root, with fresh output/checkpoint paths:

```sh
timeout 240s python experiments/runner-addition/unrestricted-single/run.py --freeze 422c1aad5a4930bcb917a76d0aa67f986c0551df --output /tmp/unrestricted-results.json --checkpoint-dir /tmp/unrestricted-checkpoints
timeout 240s python experiments/runner-addition/unrestricted-single/verify.py --input /tmp/unrestricted-results.json --output /tmp/unrestricted-verification.json
timeout 240s python experiments/runner-addition/unrestricted-single/run.py --freeze 422c1aad5a4930bcb917a76d0aa67f986c0551df --output /tmp/unrestricted-replay.json --checkpoint-dir /tmp/unrestricted-replay-checkpoints
cmp /tmp/unrestricted-results.json /tmp/unrestricted-replay.json
```

[Complete results](results/RESULTS.json), 175,416 bytes, SHA-256:
`d3d967249534079d0f1f27d2a03bd7f1cb38c9598f115b6c5de0d46e1ed4a9cd`.
[Certificate export](results/CERTIFICATES.json) is a post-verification extraction
bound to that hash. It retains both universal intervals and their finite/tail
witnesses, every component/blocker/integer-gap certificate, and the pinned
two-component upper bounds. Full source geometry remains recoverable from the
results and preceding study; the export is not a lossless copy of all safe sets.

**Next proposed:** turn the simplest genuine two-source case, the primes-derived
core, into a short reviewable obstruction argument: explain how its five
recorded blocking speeds exclude every single connected source and how the
selected pair provides complementary coverage. Use exact gaps, component
boundaries and the existing certificate; distinguish a useful explanatory
compression from any unproved extension to other cores. No new rule, broader
core search or external review has been run here.
