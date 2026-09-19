# Exact checker and first demonstration

**Date:** September 19, 2026

**Evidence class:** implemented reference checker, bounded regression verification, and a three-case demonstration. No novelty or general-proof claim.

**Base repository revision:** `bb0e6c71ccd6fb1cf62b9bb1180a1953f0aec2a0`. The implementation revision is the commit containing this note.

## What was built

- [Exact checker](../lonely_runner/checker.py): integer/rational original velocities, selectable reference runner, denominator and gcd normalization, original runner count retained, closed allowed-time intervals, original-time witnesses, and exact maxima with all attaining times.
- Method A intersects closed rational intervals, keeping singleton equality points. Method B independently partitions at triangle-wave corners and enumerates affine crossings. It directly evaluates all candidate distances. They share validation and rational arithmetic, not their search algorithms. This is algorithmic crosschecking within one codebase, not external review or formal verification.
- [CLI](../lonely_runner/__main__.py): one/all references, optional threshold, optional feasibility-only mode, and exact JSON output.
- [Offline demonstration](../demo/index.html): third speed 2/3/4, reference selection, play/pause, time scrubbing, exact-peak stepping. All nine results are generated into [cases.json](../demo/cases.json). Rounded motion never supplies certification.

## Reproduction and observed results

Run from the repository root using Python 3.10 or later. The actual Python execution used 3.12.14.

```bash
python -m unittest discover -s tests -v
python -m scripts.build_demo --check
python -m lonely_runner --velocities 0 1 4 --all-references
```

Observed: **25 tests passed**. Generated demonstration files matched the checker and templates. The CLI returned exact feasible intervals and maximum-separation witnesses for all three reference runners in `(0,1,4)`.

Coverage includes all eight planned fixture situations, the nonconsecutive tight case `(1,3,4,7)`, isolated equality moments, the impossible artificial threshold `2/5` for `(1,2)`, sign/permutation/translation/scaling invariance, rational time conversion, duplicate absolute constraints without changing `n`, rejected inputs, explicit resource-limit errors, and CLI JSON/error paths.

The independent-method regression domain is every strictly increasing subset of `{1,...,8}` with size 1 through 4: **162 speed sets**, without gcd filtering. Each is checked at Method B's exact maximum and `1/1000` below and above it. At the maximum, Method A's entire feasible set must equal all Method B peak points. Twenty seeded four-runner rational configurations additionally verify every reference's witnesses directly in original coordinates (seed `19092026`). These bounded tests establish implementation evidence, not an unbounded theorem.

## Starting comparison

Track circumference is one lap; speeds are laps/minute; the reference here is A at speed 0. All runners start together.

| Original speeds | Exact maximum gap | All peak times in the first minute | Allowed times at the required 1/3-lap gap |
| --- | --- | --- | --- |
| `(0,1,2)` | `1/3` lap | 20 and 40 seconds | Exactly 20 and 40 seconds |
| `(0,1,3)` | `1/2` lap | 30 seconds | Closed interval `[80/3,100/3]` seconds |
| `(0,1,4)` | `2/5` lap | 24 and 36 seconds | Closed intervals `[20,25]` and `[35,40]` seconds |

Increasing C's speed in these three examples does not monotonically increase A's greatest separation. This is a comparison of three elementary cases, not a discovered general law. Switching reference runners gives different maxima and may give different qualifying times.

## Display checks and limits

JavaScript syntax and generated placeholders were checked. All nine reference selections, exact-peak stepping, preview scrubbing, play/pause, and stopping at the period boundary passed executable DOM interaction checks with Node 24.19.0 and jsdom 30.1.0:

```bash
# Optional development dependency; the Python checker and demo do not require it.
npm install --no-save --package-lock=false jsdom@30.1.0
node scripts/check_demo_dom.cjs
```

**Rendered browser layout is not verified in this environment.** The standard Chromium download timed out/failed, and an alternative local browser binary could not execute (`EACCES`). The DOM checks do not provide pixels, measure real text, or verify responsive rendering. No browser smoke-test pass or screenshot inspection is claimed.

The optional [browser smoke script](../scripts/check_demo.cjs) is included for an environment with Playwright and Chromium. It covers the interactions plus 320/360/784-pixel layout and label bounds:

```bash
npm install --no-save --package-lock=false playwright@1.62.1
npx playwright install chromium
node scripts/check_demo.cjs
```

`DEMO_CHROMIUM_PATH` may specify an existing executable. `DEMO_SCREENSHOT_DIR` optionally writes QA images. The script was attempted here but did not reach browser execution.

## Boundaries and next action

The core is Python standard library only. Original velocities must be distinct and exact (integers, `Fraction`, or integer/fraction strings); irrational or floating-point input is not silently approximated. All inputs use a common initial position.

Intervals and peak times cover one normalized period `[0,1]`, with the full scaling map back to original time. That is a period of the selected runner's relative distances; absolute track positions need not repeat over it. The CLI can compute arbitrary rational configurations within the explicit small-case budgets. Method A caps the sum of unique normalized speeds at 20,000; Method B also caps its estimated segment/pair work at 2,000,000. A budget error yields no certificate.

The visual currently offers only the three chosen presets. Arbitrary-speed browser input, distance-curve plots, atlas generation, frontier computations, and formal verification remain future work. No hosted site, scheduled process, or external publication was created.

Next: explore `(0,1,4)` near 24 seconds and ask which runner limits the stationary runner just before and just after that peak.
