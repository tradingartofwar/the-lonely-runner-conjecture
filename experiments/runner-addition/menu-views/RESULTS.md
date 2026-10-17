# Two-component menus and the meaning of the bits

October 17, 2026. **OBSERVED:** exact finite results below. **HYPOTHESIS / proof candidates:** their all-admissible-speed implications using the supplied finite reduction. AI materially generated the derivations, code and report; both algorithms have the same AI author. Independent proof review and novelty assessment remain open.

The representation proposal is now implemented as [one exact model with several views](MODEL.md). The [frozen protocol](PROTOCOL.md) completes the two pending minimum-menu decisions and compares coverage, interval placement and per-runner time states. It preserves the complete geometry behind every summary.

## The minimum menus are both two

The eight moving core speeds are:

- (p,q)=(1,8): `(1,8,9,10,11,19,22,67)`;
- (p,q)=(1,10): `(1,10,11,12,13,23,26,83)`.

Add stationary reference 0 and a positive integer speed r absent from the core. All runners start together; n=10, threshold d=1/10, reference 0, physical period [0,1]. This does not address the other references.

| Pair | Complete core components | Selected IDs | Widest component I=[a,b] | Second component J | Finite cutoff |
| --- | ---: | --- | --- | --- | ---: |
| (1,8) | 26 | 0,7 | [231/670,39/110] | [31/220,99/670] | 21 |
| (1,10) | 34 | 0,9 | [41/130,269/830] | [11/100,29/260] | 23 |

Both minimum menus containing the prechosen widest component have size **two**. The complete finite remainders contain 14 and 17 admissible speeds respectively; all 31 full child sets and selected-menu covers are nonempty. The width argument handles every admissible r at or above the cutoff: an unsafe phase gap has length 2d, so it cannot strictly contain a closed scaled interval of length at least 2d. Equality is safe.

The [prior placement study](../placement/RESULTS.md) supplies an explicit admissible blocker for each of the 60 complete core components. Combining those lower bounds with these two-component covers also gives minimum two **without requiring the widest component**, within the class of fixed connected core-component menus. Any smaller connected core-safe interval lies inside one of those components and inherits its blocker. This says nothing about a minimum description in arbitrary representations or about intrinsic incompressibility.

## A small dispatcher and an explanation of its exception

Each widest interval fails only at **r=3**, after accounting for the full finite remainder and the width tail. The second component supplies a fixed repair time:

| Pair | Widest width | Widest failures | Second-component failures within the leader remainder | Fixed repair time for r=3 |
| --- | --- | --- | --- | --- |
| (1,8) | 36/3685 | {3} | {7,14} | 31/220 |
| (1,10) | 47/5395 | {3} | {9,18} | 11/100 |

The second-component failure sets in this table are **restricted to the leader's finite remainder**, not global failure classifications. Their intersection with {3} is empty.

Consequently a witness dispatcher is: return the fixed repair time if r=3; otherwise use the widest interval's first contact. For I=[a,b], set

\[
j=\left\lceil ra-(1-d)\right\rceil,\qquad
t=\max\left(a,\frac{j+d}{r}\right),\qquad d=\frac1{10}.
\]

The certified contact ensures t<=b. This is a constructive rule for the two stated families, not a new formula for arbitrary q or a measured speed improvement.

The center/half-width view explains the failure locations. With c=(a+b)/2 and h=(b-a)/2, contact is equivalent to `distance(r*c, integers)+r*h >= d`. Failure identifies an integer m whose **open** unsafe time gap `((m-d)/r,(m+d)/r)` contains the whole component.

For r=3 both widest intervals lie strictly inside **(3/10,11/30)**, centered at **1/3**. The predicate values are 7/110 and 7/130, each below 1/10. The alternative components escape that gap. Their recorded failures instead lie in gaps centered at **1/7** for speeds 7,14 and **1/9** for speeds 9,18. This explains the complementary failures in the tested remainders. Width certifies the tail; placement locates the exceptions; coverage selects a sufficient collection.

## A concrete limit of existential coverage bits

The composition diagnostic found an example in each core where a component supports each of two added speeds separately, but never both at the same time within that component.

| Pair and component | First added speed and surviving times | Second added speed and surviving times | Separation |
| --- | --- | --- | --- |
| (1,8), I2=[111/670,19/110] | 17: [111/670,29/170] | 18: [31/180,19/110] | 29/170 < 31/180 |
| (1,10), I3=[31/230,119/830] | 8: [11/80,119/830] | 14: [31/230,19/140] | 19/140 < 11/80 |

Both individual incidence bits are 1, while the joint surviving set is empty. In logical terms, `(exists t: A(t)) and (exists t: B(t))` does not imply `exists t: A(t) and B(t)`. Recovering the exact surviving intervals makes the invalid composition detectable and supplies the correct intersection operation.

This is a local-component diagnostic at fixed threshold 1/10. Adding both speeds gives eleven runners, whose LRC threshold would be 1/11. We have neither tested that different question here nor claimed that the full core lacks a common time. The example also does not invalidate the menu calculation, which asks about one added speed at a time.

## Per-runner time states explain the boundaries

The single preselected case (p,q,r)=(1,8,3) uses ordered speeds `(1,8,9,10,11,19,22,67,3)`. Its exact trace contains 294 event points and 293 open cells. Decoding the all-true records recovers all **22** complete safe components, agreeing with the interval calculation and the prior saved child set.

| Boundary | Exact time | Condition changing | Are all nine moving runners safe at the boundary? |
| --- | --- | --- | --- |
| Widest interval starts | 231/670 | Speed 67 becomes safe | No: speed 3 is unsafe |
| Widest interval ends | 39/110 | Speed 11 becomes unsafe immediately afterward | No: speed 3 is unsafe |
| Repair interval starts | 31/220 | Speed 22 becomes safe | Yes |
| Repair interval ends | 99/670 | Speed 67 becomes unsafe immediately afterward | Yes |

Speed 3 stays unsafe throughout the widest interval. The repair interval has every condition true; speed 22 opens that opportunity and speed 67 closes it. These are exact local boundary descriptions, not a general classification of limiting runners.

Event points are separate from open cells so equality and isolated opportunities survive. The semantic fixture `(1,2)` at threshold 1/3 retains exactly the isolated times `{1/3,2/3}`, although no open cell is all true.

## What the representation comparison adds

The [model record](MODEL.md) declares each view's question, valid operations, omissions and recovery route. Endpoint-to-center conversion is reversible. Existential coverage discards where witnesses occur; it supports choosing a menu but needs recovery before combining added constraints. Time-state bits preserve simultaneous truth on their exact clock cells and can reconstruct the complete safe set, but detailed phases still require the original speeds and clock.

This study delivers a simpler two-case dispatcher, an explicit failed composition, and a boundary explanation. It does not measure human readability, establish general superiority, or require a new LTCM. The distinctions are compatible with the repository's existing Compatibility Calculus rules and ordinary interval, Boolean and modular mathematics.

**Next proposed:** use these exposed cases to formulate a menu-selection rule based on unsafe-gap locations, then freeze that rule and a different validation domain before evaluation. Compare its selected menu and recovery cost with exact minimum cover, preserving misses. The question is whether placement can help discover sufficient components, beyond explaining a menu already found. No such new-domain test has run.

## Reproduction and verification

Source: `a74bf46a4d96e554b50e71ea191cc8223253beb5`. Execution freeze: `d1c700e86d0494a3688ed647efe3ed75a9ec4612`. The [manifest](manifest.json) pins 14 source/dependency files; no frozen code was changed after execution. Exact arithmetic uses Python `Fraction`.

From the repository root at the results commit:

```sh
timeout 60s python experiments/runner-addition/menu-views/run.py --freeze d1c700e86d0494a3688ed647efe3ed75a9ec4612
timeout 60s python experiments/runner-addition/menu-views/verify.py
timeout 60s python experiments/runner-addition/menu-views/run.py --freeze d1c700e86d0494a3688ed647efe3ed75a9ec4612 --output /tmp/menu-views-replay.json
cmp experiments/runner-addition/menu-views/results/RESULTS.json /tmp/menu-views-replay.json
```

The alternate algorithm reconstructs complete sets from threshold events and checks minimum covers by subset enumeration. It verified **2 cores, 31 child sets, 942 component contacts, 71 physical witnesses, 60 minimum-search subsets, all 60 prior single-component blockers, and 5,283 runner predicates across 587 time records**. Open-cell predicates are checked through whole-band containment or empty interior intersection, not a second sample. Both composition diagnostics and singleton semantics pass. One primary replay is byte-identical; all execution budgets were respected.

Artifacts: [exact results](results/RESULTS.json), [alternate verification](results/VERIFICATION.json), [replay record](results/REPLAY.json). Results SHA-256: `f9fb3650c214c84f1ad272ec6b41c33ccaf1ead836b3a67238ec894c54726621`.

These checks support the computations. The finite-reduction and family-wide arguments remain same-author proof candidates awaiting independent review; no general Lonely Runner, novelty, or external-application claim follows.
