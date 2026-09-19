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

The original frontier source in notes/SOURCES.md reports a computer-assisted result through 13 total runners. A later source check found a September 2 preprint reporting 14 total runners (S7). We have not independently audited either proof or run their code. Frontier computation is not the current assignment.

Start all runners together: shifted-start variants are different. Use exact rational arithmetic for certification. A plot, time grid, or large batch of passing examples cannot prove the general conjecture. A valid equality time can be an isolated point, invisible to a coarse animation.

## What exists now

- Repository overview, working instructions, research plan, and versioned source pointers.
- `lonely_runner/checker.py`: exact rational normalization, Method A closed-interval feasibility, and Method B piecewise-linear maximum with an interval crosscheck.
- `python -m lonely_runner`: readable or JSON output for one or all reference runners, original-time witnesses, feasible intervals, and exact peaks.
- `tests/test_checker.py`: 25 tests, including the documented fixtures, original-coordinate normalization checks, and 162 bounded speed-set comparisons at/below/above the maximum.
- `demo/index.html`: offline interactive demonstration of `(0,1,2)`, `(0,1,3)`, and `(0,1,4)`, with all reference runners, play/pause, time scrubbing, and exact-peak stepping. `demo/cases.json` contains the nine exact checker outputs. `scripts/build_demo.py` regenerates them and the display.
- `notes/CHECKER_VALIDATION.md`: commands, results, limits, and the starting comparison.

- `scripts/compare_tight_cases.py`, `experiments/tight_cases_4_8_12.json`, and `notes/TIGHT_CASES_4_8_12.md`: exact comparison of 4, 8, and 12 runners, including 179 specified single-speed changes. Four selected-reference tight cases were crosschecked with the independent maximum method. Inline conversation plots also show distance curves; the original offline demo is unchanged.

**Not built or run:** arbitrary-speed editing in the browser, an exhaustive atlas, frontier computation, or a new mathematical result. No article has been submitted and no researcher has been contacted. The 162 regression inputs and the new 182-input research comparison are separate bounded checks.

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

September 19, 2026: Vance asked to record threshold-touching cases and double/triple the four-runner example. We compared 4, 8, and 12 total runners with the slowest runner (speed 1) selected. Consecutive actual speeds `1,...,n` give exact maxima `1/n`. Of 179 bounded single-relative-speed replacements, one remains tight: eight-runner relative speeds `{1,2,3,4,5,7,12}` (actual speeds `{1,2,3,4,5,6,8,13}`). This is a known example reproduced here, not a discovery. See `notes/TIGHT_CASES_4_8_12.md` and its script/data links for exact times, the search domain, controls, and all-reference checks.

Shared observation: at every recorded tight peak, one runner's distance is increasing while another's is decreasing; the two limiting relative speeds sum to `n`. The uneven eight-runner example has the same peak times and limiting pairs as the consecutive case, so equal speed spacing is not necessary. A handoff also occurs at non-tight peaks, so it is not sufficient to characterize tightness.

Next useful action: compare the exact allowed-time intervals for relative speed 6 versus 12 in the eight-runner case, and connect the preservation of tightness to the known acceleration criterion. Do not expand the search or claim a general classification from this bounded result. Git history retains earlier stopping points.
