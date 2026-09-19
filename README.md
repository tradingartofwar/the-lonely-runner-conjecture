# the-lonely-runner-conjecture

A curiosity-led exploration by Vance and his AI partner. The aim is to understand the problem, enjoy the investigation, and see whether intuition plus exact computation can produce something worth knowing. A breakthrough is an aspiration, not an expectation or a promised result.

**Start a new thread with [HANDOFF.md](HANDOFF.md).** It is self-contained and includes a copyable opening message and project instructions.

## The question

Start `n` runners together on a circular track of circumference 1, with distinct constant velocities. Does each runner eventually have a moment when every other runner is at least `1/n` of the track away? The moments can differ between runners.

Our first research question: **What structure makes a collection of speeds barely achieve that separation?**

## Reading map

| File | Purpose |
| --- | --- |
| [HANDOFF.md](HANDOFF.md) | Resume in a new conversation without reconstructing the origin |
| [RESEARCH_PLAN.md](RESEARCH_PLAN.md) | Strategy, proposed stages, experiments, and success criteria |
| [notes/MATHEMATICAL_BASELINE.md](notes/MATHEMATICAL_BASELINE.md) | Definitions, exact checks, normalization, and test fixtures |
| [notes/SOURCES.md](notes/SOURCES.md) | Dated research starting points and verification limits |
| [AGENTS.md](AGENTS.md) | Instructions for AI collaborators working here |

## Status — September 19, 2026

The first exact checker and a minimal three-case visual demonstration are implemented. Python's standard-library `Fraction` certifies closed feasible intervals (including isolated equality times) and exact maximum separation. Two independently structured algorithms crosscheck the answers. This is a small reference implementation, not a general proof or a frontier search.

The tests cover the planned fixtures, normalization and reference changes, rejected inputs, and method agreement across 162 bounded speed sets. [Validation and scope](notes/CHECKER_VALIDATION.md) records the commands and what these checks establish.

## Try it

Python 3.10 or later, with no third-party packages required:

```bash
python -m lonely_runner --velocities 0 1 2
python -m lonely_runner --velocities 0 1 4 --all-references
python -m lonely_runner --velocities=-1/2,0,1/2 --reference 1 --json
python -m unittest discover -s tests -v
```

`--reference` is the zero-based index in the supplied velocity list. Inputs are exact integers or fractions such as `3/2`; floats and decimal strings are rejected. A custom `--threshold 2/5` changes the requested separation, while the output retains the original conjecture threshold `1/n`. `--feasibility-only` skips maximum calculation. Large normalized inputs fail with an explicit resource-limit error, not a false counterexample.

JSON output includes the original runner count, signed relative speeds, denominator/gcd normalization, complete time-scaling map, all closed feasible intervals over one relative-distance period, a witness, and maximum-separation times with limiting runner identities. All rational quantities are strings.

## Visual demonstration

Open [demo/index.html](demo/index.html) locally in a browser after downloading or cloning the repository; GitHub's file view shows source. It works offline, without a server or installation. Change runner C between 2, 3, and 4 laps/minute, watch any runner, play/pause, scrub time, or step through exact peaks. The demo starts paused at a verified peak. Playback stops after one relative-distance period; it does not run in the background.

The three preset cases have all nine reference-runner results precomputed by the Python checker in [demo/cases.json](demo/cases.json). Ordinary motion is labeled approximate; exact peak labels use those checked rational results. Coincident dots are offset radially for visibility. The shaded arc is the part of the track at least `1/3` lap from the watched runner.

```bash
python -m scripts.build_demo
python -m scripts.build_demo --check
```

The browser currently offers these three presets, not arbitrary speed entry. The exact CLI supports general rational configurations within its small-case limits. Distance-curve plots, a bounded atlas, and frontier computation remain unbuilt. Optional browser smoke checks are described in the validation note.

The original demonstration explores why `(0,1,4)` reaches `2/5` for the stationary runner, between the first two examples' `1/3` and `1/2`. The current comparison is below; frontier research remains recorded separately in Sources.

## Exact comparison: 4, 8, and 12 runners

The [threshold-touching study](notes/TIGHT_CASES_4_8_12.md) follows Vance's request to double and triple the four-runner example. It records three consecutive-speed tight cases, reproduces a known uneven eight-runner case, and checks 179 specified single-speed changes with exact interval arithmetic. The scope is bounded; this is not a new proof or a classification of all tight cases.

```bash
python -m scripts.compare_tight_cases
```

The [rational output](experiments/tight_cases_4_8_12.json) includes the search domain, all results, exact peak times and limiting runners, all-reference summaries for the four tight configurations, and polygon data for the comparison plots.

The continuation in the same note explains the speed-6-to-12 replacement through exact interval coverage, records the spacing pattern and its twelve-runner exception, and tests nearby replacements. Reproduce it with `python -m scripts.analyze_eight_runner_replacement`; [continuation evidence](experiments/eight_runner_replacement.json) preserves the calculations. The next proposed comparison is the known eight-runner example where two speeds change together.

This repository owns this exploration. It does not change Mission Control, Performance, any other project, or the earlier decision against adding new operating systems. No recurring tasks or background processes are established.
