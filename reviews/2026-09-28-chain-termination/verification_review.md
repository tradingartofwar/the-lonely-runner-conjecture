# Independent replay and mathematical review

September 28, 2026. Internal AI review by the structural challenger, subsequently
tasked with independent verification. Baseline
`dd5b3bce9a7a3fb22474a724161438f24e35fb41`.

## Provenance and finite outcome

The verifier read only the frozen protocol inputs and the analytical bound
note. It did not read or import primary code or saved primary answers.
`verify.py` derives projections from fractional-part cases and blocking
occurrences, rather than the primary ceiling expression. It independently
reconstructs every feasible closed component of each supplied window using
all local threshold points, tests threshold equality directly, and checks
that the stated physical core is safe throughout the window.

All 12 frozen windows pass this replay: 11 contain a witness and the clipped
lifted window is empty. These are reused diagnostic windows, including two
windows on the same lifted physical configuration. They are not held-out or
independent random samples. The full repeated traces use 199 scalar calls,
of which 32 move, and at most three started rounds. The extended lifted
window retains its right-endpoint-only witness. The original tight control
also retains its isolated endpoint.

For each trace, the verifier checks the selected occurrence labels are
distinct and successive moving occurrences strictly overlap by at least the
claimed quantum. It reconstructs their union and excess directly from interval
lengths. Actual multiplicity minus one is integrated on both the full union
and the interval from the supplied start to the final iterate. Two independent
local methods agree: threshold-cell integration and clipped blocking lengths.
Those answers also agree with the potential differences. Both global and
start-dependent move bounds hold in every frozen replay.

Reproduction:

```bash
python -S -B reviews/2026-09-28-chain-termination/verify.py
```

The parent must compare the recorded numerical fields and traces to the
separately generated primary answers before claiming implementation agreement.
This review does not substitute a pass flag for that comparison.

## Analytical challenge

No gap was found in the supplied termination argument under its stated
common-start positive-integer assumptions:

1. The primitive differentiates to blocked multiplicity minus one because
   exactly four blockers each have density one quarter. The potential is
   continuous at threshold points, so integrating across those points is valid.
2. Every moving projection starts strictly inside its selected open occurrence.
   The next moving occurrence therefore overlaps the preceding one by positive
   length. A boundary contact cannot continue the chain because equality is
   safe.
3. Adding a new selected interval charges at least its overlap with the previous
   union to excess multiplicity. Integrating full multiplicity dominates this
   selected excess; pairwise overlap sums are not substituted for it.
4. The pairwise lcm argument bounds a positive overlap from below. The number
   `Q=max pairwise lcm` need not be a common multiple of every pairwise lcm;
   `1/(8Q)` is a lower bound on positive overlaps, not necessarily one common
   lattice spacing for all endpoints. The proof uses only the lower bound.
5. In the start-dependent bound, at most `M(L)` selected open occurrences can
   contain L. Each remaining selected occurrence lies to the right of or
   starts at L, so its charged overlap is retained after clipping at L.
6. Every finite prefix obeys the move bound. This rules out infinitely many
   moving calls without assuming beforehand that a witness exists. A bounded
   round visiting every runner converts the move bound into a round bound;
   unrestricted fair scheduling alone does not bound stationary-call delays.

The existing `OVERLAP_PLACEMENT.md` Section 8 already supplies the primitive
and its `3/16` allowance. The proposed added implication is the charge from
successive blocking occurrences to that allowance, with the arithmetic
positive-overlap lower bound. It should not be presented as discovery of a
new primitive.

The theorem remains a **HYPOTHESIS / supplied proof candidate** with internal
AI review. The tests certify only their stated finite windows. The result
does not prove a speed-independent bound, show that large bounds are attained,
force a successful core window, or establish new full Lonely Runner coverage.
