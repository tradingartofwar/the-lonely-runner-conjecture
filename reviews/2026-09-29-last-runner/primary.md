# Primary exact last-runner audit

Date: 2026-09-29. Parent: `f3c26e709fa1cd8945968dcd585bd012430c7243`.
Status: **OBSERVED** on the frozen finite input domain. General coverage
equivalences and their structural consequences remain proof candidates.
Material AI assistance supplied the code, deductions, and this report.

The approved immutable protocol has SHA-256
`660a3a7f27f6a1e7b2c0c68aeea22b42366c7a946d5612e967c6f355999d5aae`.
The exact implementation is `primary_last_runner.py`, source SHA-256
`e9188a0366e940029ad3d13899dc61e45a2d0cb080b7455e518e372681c65cde`.
Output `primary_last_runner.json` has SHA-256
`852ed22888e61c61ec86b12811a9088d66040b278485dcfba6fafaf7054fecb5`.

## Method and scope

The primary reconstructs each closed core-safe set by successive exact safe-lap
intersections, retaining isolated points. For each positive component [l,r],
the widest width w supplies the analytically sufficient cutoff U=1/(4w).
Only the domain D=(max(core),U] is considered. This is an exact rational
speed-domain construction for three inherited cores, not a tuple scan.

For each fixed phase theta in{0,1/2}, each component and each relevant lap m
contributes the strict speed band

`((m-theta-1/8)/l,(m-theta+1/8)/r)`.

Closing both ends gives the weak-band condition used for zero duration.
Every band is clipped to D. Exact intersections and unions carry explicit
open/closed endpoint flags; a zero-width band survives precisely when both
ends are closed. Per-component bands retain their lap labels separately.
Canonical component-prefix intersections display the shared-speed
compatibility restrictions. Integer speeds are extracted from these bands.

The modes are those frozen in the protocol: F covers every closed core
component with strict blockers; P discards isolated core points but strictly
covers every positive closed component; Z covers every positive component
with closed blockers, exactly the zero-final-duration condition.
For noninteger real d, every assertion concerns the first core period[0,1].

## Exact output

| Core | Largest width | Cap U | Components / isolated |
| --- | ---: | ---: | ---: |
| 1,4,5,6,7,11 | 1/112 | 28 | 8 / 4 |
| 1,3,4,5,7,24 | 3/448 | 112/3 | 8 / 0 |
| 1,4,5,56,64,72 | 5/504 | 126/5 | 50 / 0 |

The third domain is empty because126/5<72. Its largest core window is
already too wide for any faster final runner to cover, at any phase.

For core1,4,5,6,7,11 at phase0:

- F is empty;
- P is `(220/17,196/15)`;
- Z is `[220/17,196/15]`;
- the integer points of P and Z are both{13}.

This exactly matches the pre-execution hand prediction recorded in
`PRIMARY_PREDICTIONS.md`. The four positive components have compatible
covering laps(4,6,7,9) throughout that P interval. The isolated core point
1/8 remains safe there, so covering all positive components still does not
erase the full safe set.

For the same core at phase1/2, F and P are empty, while Z is the singleton
speed{18}. This is a band-intersection result; no extra full final-safe-set
reconstruction at d18 was added to the frozen diagnostic scope.

For core1,3,4,5,7,24, F,P,Z are all empty at both fixed phases even for
real d in D. In particular, all admissible integer d>24 retain positive
duration at both phases. A stronger hand-check for common start already
comes from the single widest component: its six possible lap-band closures
all lie strictly between consecutive integers.

## Designated diagnostics and equality retention

| Core and final speed | Exact final duration | Isolated final points |
| --- | ---: | --- |
| 1,4,5,6,7,11; d13 | 0 | 1/8,3/8,5/8,7/8 |
| 1,4,5,6,7,11; d16 | 39/4928 | none |
| 1,4,5,56,64,72; d112 | 53/448 | none |
| 1,4,5,56,64,72; d113 | 214673/2278080 | none |

These are the four designated phase0 diagnostic speeds. No other final
speed was supplied to the final-safe-set reconstruction.

The records contain66 core components, including62 positive components and
four isolated points,18 mode records,380 per-component band rows, and380
prefix rows. The minimum endpoint-arithmetic strict-coverage caps across
positive components are19,32,24 in the same core order. These are necessary
integer-strict-cover caps, not sufficient coverage criteria.

The separately structured verifier received only the agreed schema before
freezing its own result. Its comparison is recorded separately; agreement
does not constitute external proof certification or a novelty assessment.

## Reproduction and limits

```bash
python reviews/2026-09-29-last-runner/primary_last_runner.py
```

The script verifies the frozen protocol hash before evaluation. Arithmetic
uses Python Fraction only. No phase grid, additional tuple input,
all-reference work, or scan of the remaining finite region was performed.
Prior coverage of the C611 family remains prior work; this calculation
exposes its joint lap restrictions and the information lost by dropping
isolated points. A finite list of successful cores is not a universal
last-runner theorem for all{1,4,5,a,b,c} cores.
