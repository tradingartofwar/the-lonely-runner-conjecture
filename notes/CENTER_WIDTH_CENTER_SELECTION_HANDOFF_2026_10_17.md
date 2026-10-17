# Center-width criterion and next center-selection question

Recorded October 17, 2026, from Mission Control discussion. This note is a research handoff, not an independently reviewed theorem. Primary source: [center-width RULE.md](../experiments/runner-addition/center-width/RULE.md) and [RESULTS.md](../experiments/runner-addition/center-width/RESULTS.md).

## Exact mathematical representation

Let S be a nonempty finite set of distinct positive integer core speeds, 0<d<1/2, and c=u/v in (0,1) a rational center in lowest terms. Write ||x|| for the distance to the nearest integer.

For a closed interval I=[c-h,c+h], h>=0, define

    H_d(c) = max_{1 <= j <= v} max(0, d - ||j*c||)/j

    G_{S,d}(c) = min_{s in S} (||s*c|| - d)/s.

H is the **required half-width** for the interval to contact a d-safe band for every positive integer added speed; G is the **maximum permitted half-width** for the entire interval to remain d-safe for the core. Under the stated hypotheses (and I within [0,1]), the proposed exact criterion is

    H_d(c) <= h <= G_{S,d}(c).

Thus a core-safe universally contacting interval centered at c exists exactly when

    H_d(c) <= G_{S,d}(c).

In the common-start stationary-reference Lonely Runner application, n=|S|+2, d=1/n, and the added positive integer speed r is distinct from S. A possibly different time t in the same interval may witness each r; this is NOT a single time shared across all r.

## Center-selection problem

Define the margin

    M_{S,d}(c) = G_{S,d}(c) - H_d(c).

The next question is to find (or completely reject) a rational center c in (0,1) satisfying

    M_{S,d}(c) >= 0,

**without first constructing the complete core-safe set**. A bounded, complete candidate-selection/rejection method should be compared against full safe-set construction on a separately frozen domain. Investigate whether core constraint boundaries or finite structural conditions yield a complete candidate set, rather than assuming a heuristic is complete.

The criterion evaluates a *supplied* rational center; it does not establish that every core has a qualifying center. Failure of this single-interval source class is not failure of the general Lonely Runner property. Preserve equality, exact blocker speeds, excluded repeated speeds, physical-time witness recovery, and the distinction between one component and multi-component menus.

## Exposed example

For S={1,2,3,4,5,7,10,19}, d=1/10, c=159/1330:

    H_d(c) = 15/2128   (controlling added speed 8)
    G_{S,d}(c) = 6/665 (controlled by core speeds 7 and 19)
    M_{S,d}(c) = 3/1520 > 0.

This example was used in developing the rule, not fresh validation.

## Research handoff

1. Seek independent mathematical review of the short derivation in RULE.md. Same-author alternate algorithm agreement is not independent proof review.
2. Derive a bounded, complete method for selecting or rejecting candidate rational centers from core constraints; state its domain and proof obligations before experiments.
3. Compare with full safe-set construction on separately frozen inputs; actively seek counterexamples and retain failures.
4. Preserve distinction between a certified universal single interval, a finite multi-component menu, and existence of a Lonely Runner witness.
5. Evaluate transferable mathematical and representational value without assuming a general proof, novelty, or speed advantage.

Status: research direction / proof candidates; no new center-selection algorithm or independent review claimed by this note.
