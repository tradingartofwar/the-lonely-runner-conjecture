# Lonely Runner — new-thread handoff

**Prepared:** September 19, 2026  
**Repository:** https://github.com/tradingartofwar/the-lonely-runner-conjecture  
**Canonical branch:** `main`  
**Suggested ChatGPT project/thread title:** Lonely Runner — Vance + AI

This file is intended to stand alone when opened in a new conversation or uploaded to a project folder. The live repository remains authoritative if this copy becomes old. Creating the repository documents does not itself create a ChatGPT project or attach its files.

## Why we are here

Vance asked whether there were well-known unsolved problems that he and AI could work on together, just for fun. The Lonely Runner Conjecture appealed because it offers concrete motion, rhythm, and phase relationships alongside exact mathematics and computational experiments. Vance then created this repository and asked for a plan, strategy, and handoff.

This is a chosen place for exploration, not a promise to solve the conjecture. It does not activate the parked observation-as-intervention design or create a new Mission Control system. No recurring schedule or external coordination is established.

## The problem in ordinary language

Runners start at the same point on a circular track and keep different constant speeds. For `n` total runners, does each runner eventually get at least `1/n` of the track away from every other runner? Each runner may get that moment at a different time. Equality counts.

In our notation, selecting one runner as stationary leaves `k=n-1` relative speeds. Many papers count these `k` speeds instead of total runners. Confusing the conventions changes the threshold and the apparent frontier.

## Working strategy

Start by understanding the configurations that only barely meet the bound. Use a circular track, distance-versus-time curves, and exact allowed-time intervals as three views of one input.

The proposed sequence is: one understandable example -> exact checker with independent crosschecks -> small visual lab -> bounded atlas -> one evidence-led research question. The full strategy is in RESEARCH_PLAN.md.

Vance supplies direction, intuitive questions, and reactions to what becomes visible; AI contributes its own reasoning and carries the mathematical and technical work. Neither intuition nor a confident AI answer is a proof. Keep it playful and let examples correct us.

## Research baseline and limits

The frontier source in notes/SOURCES.md reports a computer-assisted result through 13 total runners. We have not independently audited that proof or run its code. Treat 14 total runners as a provisional frontier target to reassess, not the first assignment.

Start all runners together: shifted-start variants are different. Use exact rational arithmetic for certification. A plot, time grid, or large batch of passing examples cannot prove the general conjecture. A valid equality time can be an isolated point, invisible to a coarse animation.

## What exists now

- Repository overview, working instructions, research plan, and versioned source pointers.
- `lonely_runner/checker.py`: exact rational normalization, Method A closed-interval feasibility, and Method B piecewise-linear maximum with an interval crosscheck.
- `python -m lonely_runner`: readable or JSON output for one or all reference runners, original-time witnesses, feasible intervals, and exact peaks.
- `tests/test_checker.py`: 25 tests, including the documented fixtures, original-coordinate normalization checks, and 162 bounded speed-set comparisons at/below/above the maximum.
- `demo/index.html`: offline interactive demonstration of `(0,1,2)`, `(0,1,3)`, and `(0,1,4)`, with all reference runners, play/pause, time scrubbing, and exact-peak stepping. `demo/cases.json` contains the nine exact checker outputs. `scripts/build_demo.py` regenerates them and the display.
- `notes/CHECKER_VALIDATION.md`: commands, results, limits, and the starting comparison.

**Not built or run:** arbitrary-speed editing in the browser, distance-curve plots, an atlas, frontier computation, or a new mathematical result. No article has been submitted and no researcher has been contacted. The 162 cases are regression coverage, not the proposed research atlas.

Vance approved implementation in the current thread after the proposal to build the exact checker and a minimal demonstration. This does not authorize a large search or wider project expansion.

## Resume without asking Vance to reconstruct the context

1. Inspect live `main`, read AGENTS.md and this handoff, then RESEARCH_PLAN.md. Read the mathematical baseline before coding; consult Sources for current claims.
2. Check whether newer commits have changed the status below. Preserve existing work.
3. Briefly recover the purpose, show one concrete example, and follow Vance's present request.
4. The smallest checker and demonstration are built. Use their results and follow Vance's present direction; do not rebuild them or launch a large search by default.

If GitHub is unavailable, say what cannot be verified and continue from this file as a dated handoff; do not pretend to have read current repository state.

## First useful question

Take velocities `(0,1,2)` and focus on the runner at speed 0. At times `1/3` and `2/3`, its nearest neighbor is exactly `1/3` of the track away. Why are these moments enough, and why might a sampled animation miss them? Compare `(0,1,3)` at time `1/2`.

From there, ask: **Which runners take turns preventing the reference runner from becoming more isolated, and what changes when we alter one speed?** This is a starting question, not an asserted new mechanism.

## Opening message for the new thread

> We are continuing our Lonely Runner exploration for fun. Use the GitHub repository https://github.com/tradingartofwar/the-lonely-runner-conjecture. Read AGENTS.md and HANDOFF.md, then the validation note and mathematical baseline. Recover the live state without asking me to retell the history. We now have an exact checker and a three-case visual demonstration. Start from those examples; we will choose the next step together. Keep published results, our experiments, and proof claims distinct.

## Optional project instructions

> This project is Vance and AI exploring the Lonely Runner Conjecture. The repository owns the plan, code, evidence, and continuity. Read its current AGENTS.md and HANDOFF.md at re-entry. Keep the partnership curious and rigorous: use concrete examples, exact checks, and attempts to disprove our own ideas. Do not inflate observations into novelty or proof. Preserve meaningful progress without creating unnecessary systems or obligations. Follow my current direction before moving from a plan to implementation or expanding scope.

## Current stopping point

September 19, 2026: Stage 2 is implemented; a minimal Stage 3 demonstration is ready. See `notes/CHECKER_VALIDATION.md` for verification and reproduction commands. For stationary reference A, the three cases have exact maxima `1/3`, `1/2`, and `2/5`, respectively. The first attaining times are 20, 30, and 24 seconds when speeds are laps/minute. Every runner in all three cases passes its `1/3` requirement, sometimes at different times.

Unresolved exploration: what explains the change in which runner limits isolation when C's speed changes? Next action: explore the demo together, particularly `(0,1,4)` around 24 seconds, and formulate one small question from what Vance notices. No broader search or full visual lab is selected yet. Git history retains earlier stopping points.
