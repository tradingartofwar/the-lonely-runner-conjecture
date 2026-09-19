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

Planning and handoff only. No research software, visual lab, experiment dataset, new theorem, or counterexample has been produced here. Proposed implementations in the plan are not completed work.

Start with small, comprehensible examples and an exact checker; then study tight configurations. The frontier research is recorded in Sources, with reported results separated from our own verification. Do not assume that an arbitrary bounded search proves a fixed-runner case.

This repository owns this exploration. It does not change Mission Control, Performance, any other project, or the earlier decision against adding new operating systems. No recurring tasks or background processes are established.
