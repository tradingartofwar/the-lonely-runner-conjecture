# First runner-addition study — October 17, 2026

**Outcome:** the two pending leader-constrained decisions both succeed with two
components at 1/8. At the actual ten-runner threshold 1/10, one fixed interval
suffices in each of the three selected families, subject to the finite-reduction
argument. Exact finite computations pass alternate verification and one
byte-identical replay. Universal statements remain **proof candidates**;
novelty is unassessed.

## Scope and answers

The common-start speeds are
`(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r)`, with `(p,q)` fixed to
`(1,2)`, `(1,4)`, or `(1,6)`. The added speed r ranges over positive integers
distinct from the eight fixed positive speeds. We investigate only reference 0.

The leader is the widest connected component of the eight-constraint core,
breaking ties by earliest start. A menu is a fixed set of these components and
must include that leader. A singleton counts as a component. This is the class
in which minimum menu size is computed.

| Pair | Threshold | Core components (positive / isolated) | Matched finite cases | Leader tail starts at r | Leader misses below tail | Minimum menu size |
| --- | --- | --- | ---: | ---: | --- | ---: |
| (1,2) | 1/8 | 6 (2 / 4) | 15 | 24 | 6, 12 | 2 |
| (1,2) | 1/10 | 10 (10 / 0) | 15 | 12 | none | 1 |
| (1,4) | 1/8 | 8 (4 / 4) | 27 | 35 | 3, 10, 13, 26 | 2 |
| (1,4) | 1/10 | 16 (14 / 2) | 27 | 18 | none | 1 |
| (1,6) | 1/8 | 14 (10 / 4) | 25 | 33 | 3, 10, 13, 26 | 2 |
| (1,6) | 1/10 | 26 (22 / 4) | 25 | 17 | none | 1 |

Every complete core succeeds on every tested addition. Across the two thresholds
there are 134 matched finite queries, including all 91 queries in the six
necessary finite remainders. The additional matched queries permit comparisons
on the same r inputs; they are not needed to establish tail coverage.

The chosen menus are explicit:

| Pair | Threshold | Leader interval | Extra component |
| --- | --- | --- | --- |
| (1,2) | 1/8 | [25/152, 7/40] | {1/8} |
| (1,4) | 1/8 | [17/56, 87/280] | {1/8} |
| (1,6) | 1/8 | [17/56, 127/408] | [3/16, 23/120] |
| (1,2) | 1/10 | [21/190, 9/70] | none |
| (1,4) | 1/10 | [1/10, 39/350] | none |
| (1,6) | 1/10 | [3/10, 53/170] | none |

The result does not require a large or opaque explanation here. At 1/8 the
leader fails at an explicit finite speed in each family, so a menu containing
only that leader is insufficient. The displayed extra component repairs all
its misses. At 1/10 the displayed leader already covers the full remainder.
These facts establish finite minimality in the stated class; the tail argument
extends sufficiency to all admissible r.

## Why finite calculations address every added speed

For an interval [a,b] of width w at threshold d, each open unsafe gap for speed r
has width 2d/r. If r >= ceil(2d/w), a closed interval of width w cannot fit inside
an unsafe gap, including the equality case. Therefore the leader handles every
speed at or above the displayed cutoff. Below that cutoff, all admissible r
were checked with exact rational arithmetic.

A witness is recovered by `j=ceil(r*a-(1-d))` and
`t=max(a,(j+d)/r)`. A component succeeds precisely when t <= b. The saved record
contains complete finite safe sets, each component's surviving pieces and first
contact, and exact witness phases and laps. See the frozen
[derivation](DERIVATION.md) for assumptions and proof obligations.

## What this teaches us about the representation

**The requested output matters.** Lowering the threshold increases the complete
core's component count from 6 to 10, 8 to 16, and 14 to 26, respectively. Yet the
smallest tested-class explanation sufficient to produce one witness shrinks
from two components to one. Complete geometric detail and sufficient witness
description are different measures. This is evidence about these examples,
not a complexity lower bound or a claim of incompressibility.

**Equality still carries consequential information.** At 1/8, all positive-width
core components fail for `(p,q,r)=(1,2,6),(1,2,12),(1,4,13)`; isolated core points
are necessary there. The (1,6) family needs no isolated source. Removing points
would therefore change some answers while leaving others intact. At 1/10 no
tested addition needs an isolated source, although two of those cores still
contain isolated components. These thresholds were reconstructed separately.

**Recovery is operation-specific.** The displayed menus support finding one
safe time for the specified family. They do not recover every safe time, the
optimal loneliness value, another reference runner, or a new pair. The pinned
full cores in `inputs.json` and full child sets in `results/RESULTS.json` retain
the richer detail. Recover those sources before changing the operation.

This implementation combines ordinary rational interval intersection, event
decomposition, and finite set cover. It required no new mathematical language.
Another LTCM or adaptation remains an option when a concrete operation exposes
something these representations cannot adequately carry.

## Verification and cost record

The protocol and inputs were committed as
`d1430f7be8e490d79f12dd6a349547fddf930bf5`. The evaluator, verifier, and dependency
hashes were committed before execution as
`91c2cbafa358c98502e7b26648fd05fcc9605c5e`. Both programs check local frozen files
against that commit, including the manifest itself.

- Primary method: exact first-band contact plus the unchanged repository
  band-intersection checker; finite minimum cover by bitmask dynamic programming.
- Alternate method: exact threshold-event decomposition and cardinality-ordered
  subset enumeration; it imports neither the primary study nor the checker.
- Agreement: 6 complete core sets, 134 complete child sets, 1,888 component
  contacts, and 291 stored witness records, including 23 tail controls.
- Verifier work: 28,272 event positions across reconstructed sets and 31 menu
  combinations; all six minima verified. Three predeclared semantic controls pass.
- Primary menu work: 70 DP transitions; maximum five stored states. The six core
  reconstructions contain 80 components in total. Core speed sums are 51, 83,
  and 115; this setup cost is not hidden by the small selected menus.
- One deterministic primary replay is byte-identical. No study execution or
  verification failure occurred; no frozen code was changed after execution.

Both algorithms were written by the same AI author. Their agreement checks
implementation through a different calculation; it is not independent human
review, a formal proof certificate, a performance benchmark, or a novelty check.
The families are exposed development cases, not a held-out sample. Scope stops
at these six records; no wider scan or all-reference investigation was run.

Machine-readable records:
[results](results/RESULTS.json), [verification](results/VERIFICATION.json),
[replay](results/REPLAY.json), and [frozen manifest](manifest.json).

## Reproduce

Use Python 3.12 with the standard library. From a checkout of this branch that
includes the execution-freeze commit, write to a fresh temporary directory:

```bash
run_dir=$(mktemp -d)
timeout 60s python experiments/runner-addition/study.py \
  --freeze 91c2cbafa358c98502e7b26648fd05fcc9605c5e \
  --output "$run_dir/RESULTS.json"
timeout 60s python experiments/runner-addition/verify.py \
  --input "$run_dir/RESULTS.json" --output "$run_dir/VERIFICATION.json"
cmp experiments/runner-addition/results/RESULTS.json "$run_dir/RESULTS.json"
```

Programs refuse to overwrite existing outputs. The primary result SHA-256 is
`a37150ec0c3c000f360e5d011a28e4dfe500870febfcbcab138c3b146c9d69c9`.

## Direction earned by this study

The next useful question is **when interval placement, together with width,
makes one source sufficient at the actual threshold**. Derive a symbolic
criterion that exposes which small added speeds could block an interval, then
ask whether it applies to a parameterized family. Carry excluded repeated
speeds, closed endpoints, and the physical clock explicitly.

First seek a reviewable derivation using these development examples; select and
freeze fresh validation inputs only after stating the proposed rule. A larger
scan or another language should answer a specific remaining question. The
incremental gain here is already concrete: two pending decisions are resolved
within their specified class, and three simpler 1/10 family certificates are
available for mathematical review.
