# Independent verification: archived collective-only windows

Status: OBSERVED/REPRODUCED for the exact frozen finite domain. This separately
authored AI implementation is not independent human mathematical validation.

`verify.py` imports neither the primary implementation nor its LP helper. It
uses only Python's standard library and exact fractions. Its two independent
parts are a rational threshold-event sweep for geometry and an exact two-phase
simplex with Bland's pivot rule for optimization. Unlike the primary's numeric
support proposal followed by exact certification, every simplex operation here
is rational. The verifier produces its own feasible primal and dual vectors,
checks their equal objectives, and compares only the resulting optimum values
with the primary certificates; optimizers may choose different valid vectors.

## Domain recovery and completeness

The pinned source archive has five cores whose stored summary reports positive
duration missed by their reduced optimal tree. The verifier reconstructs only
these five cores' complete closed safe components from threshold events,
including singleton components. These are 209 locator components and 1,505
locator cells. It computes singles, pairs, endpoint-aware vanishings and
containment, then a Kruskal maximum spanning tree. Locator actual durations
come from the pinned archived full-allowed components. All five complete
component digests match the source archive exactly, including bounds, actual
durations, containment data, retained labels, and component order.

The stored miss counts are 8 for Fibonacci core labels124, 2 for squares125,
2 for squares134, 2 for prime-powers234, and 4 for perturbed-chain124. Their
sum is the archived total18. The full 16-state mass reconstruction is then
restricted to those selected18 windows, using 262 exact cells. Every actual
duration, moment, and state mass matches the primary result. No new speeds,
cores, windows or subdivisions were selected. Locator event cells are an
arithmetic representation of those same source components, not new research
windows.

## Independently solved result

The verifier solves 58 new-case LPs: 18 pair-only problems and four
cover-constrained individual-triple problems on each of the 10 zero-baseline
windows. Its own 1,006 exact tableau pivots supply exact primal/dual
certificates for every problem. All optimum values agree with the primary:

| Classification | Labelled windows |
| --- | ---: |
| Positive pair-only minimum | 8 |
| Zero pair-only minimum, some positive individual-triple minimum | 8 |
| Zero pair-only minimum, every individual-triple minimum zero | 2 |

There are 18 distinct physical windows by configuration and interval; no
identical physical interval appears under two of these labelled cores. The
two collective-only windows are related by reflection and are not two
independent configurations.

For common-start velocities {0,7,8,15,23,38,61,100}, stationary reference0,
threshold1/8, core {7,8,23}, residuals {15,38,61,100}, the windows are

- [33/184,39/184], with safe positive cells [3/16,151/800] and
  [153/800,23/120];
- [145/184,151/184], the reflected window, with safe positive cells
  [97/120,647/800] and [649/800,13/16].

Each has actual duration1/600 and reduced tree bound−107161/31988400. Its
pair-only minimum is zero. Each of the four inclusive triples separately has
minimum zero over the compatible complete-cover distributions. Exact
nonnegative distributions witnessing these separate minima are retained in
`verification.json`. They need not be the same distribution: the conclusion
is “for each triple, some compatible cover avoids it,” not “one cover avoids
all triples simultaneously.” These abstract distributions are not asserted
to be realizable by a second set of common-start runners.

The actual triple moments, in local masks7,11,13,14 order, are0,0,1/48800,
119/231800; the four-way moment is0. These are diagnostics reconstructed only
after selection. No combined higher-order statistic or physical-triple query
was added to the frozen rule. The result shows that the zero-individual-minima
obstruction occurs for actual positive-duration runner windows; it does not
establish a replacement certificate or a general selection theorem.

## Endpoint handling and controls

Strict blockers use distance<1/8; equality belongs to the safe set. Event
points are evaluated separately from open-cell mass and are included in the
containment check. The selected-window output retains safe threshold points
along with positive safe cells, so zero-measure contacts cannot be mistaken
for positive duration.

All three earlier controls are separate from the18-window domain. The verifier
reconstructs their74 cells, solves their11 pair/triple problems independently,
and checks all12 archived primal/dual certificates, including the strict16
one-bound repair. It recovers strict16's forced {6,11,16} triple1/896,
doubling112's positive pair minimum761/32256, and tight13's zero pair/triple
minima. For tight13, exact distances at3/8 are safe; runner11 blocks immediately
left, while runners5 and13 block immediately right. Thus the archived endpoint
is isolated equality, not positive duration.

## Reproduction and limits

```bash
python -B reviews/2026-09-28-collective-window-audit/verify.py --check
```

This read-only replay checks pinned source hashes, complete five-core locator
digests, independent LP certificates, equality handling, and comparison with
the primary archive. Its evidence is selected-reference and selected-window
only. It checks no all-reference result, arbitrary-speed guarantee, practical
speedup, or novelty claim. The five miss-bearing cores were located using the
source archive's already-complete summaries; the other205 cores were not
recomputed in this study.
