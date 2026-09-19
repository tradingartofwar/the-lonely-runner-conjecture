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

- Repository overview and AI working instructions.
- Proposed research stages and success criteria.
- Mathematical notation, normalization rules, two exact-checking designs, and expected test fixtures.
- Versioned source pointers with explicit verification limits.
- This new-thread handoff.

**Not built or run:** the research checker, visual laboratory, atlas, frontier computation, or any new mathematical result. No article has been submitted and no researcher has been contacted. Plan text is not implementation evidence.

Document QA checked relative links and spot-checked the baseline's small examples using temporary exact-rational calculations. This is not a completed research implementation or a new result.

## Resume without asking Vance to reconstruct the context

1. Inspect live `main`, read AGENTS.md and this handoff, then RESEARCH_PLAN.md. Read the mathematical baseline before coding; consult Sources for current claims.
2. Check whether newer commits have changed the status below. Preserve existing work.
3. Briefly recover the purpose, show one concrete example, and follow Vance's present request.
4. If he chooses implementation, build the smallest exact checker and fixture tests first. Do not launch a large search or polished website by default.

If GitHub is unavailable, say what cannot be verified and continue from this file as a dated handoff; do not pretend to have read current repository state.

## First useful question

Take velocities `(0,1,2)` and focus on the runner at speed 0. At times `1/3` and `2/3`, its nearest neighbor is exactly `1/3` of the track away. Why are these moments enough, and why might a sampled animation miss them? Compare `(0,1,3)` at time `1/2`.

From there, ask: **Which runners take turns preventing the reference runner from becoming more isolated, and what changes when we alter one speed?** This is a starting question, not an asserted new mechanism.

## Opening message for the new thread

> We are continuing our Lonely Runner exploration for fun. Use the GitHub repository https://github.com/tradingartofwar/the-lonely-runner-conjecture. Read AGENTS.md and HANDOFF.md, then RESEARCH_PLAN.md and the mathematical baseline. Recover the live state without asking me to retell the history. Start by making the first small example understandable; we will choose the next step together. Keep published results, our experiments, and proof claims distinct.

## Optional project instructions

> This project is Vance and AI exploring the Lonely Runner Conjecture. The repository owns the plan, code, evidence, and continuity. Read its current AGENTS.md and HANDOFF.md at re-entry. Keep the partnership curious and rigorous: use concrete examples, exact checks, and attempts to disprove our own ideas. Do not inflate observations into novelty or proof. Preserve meaningful progress without creating unnecessary systems or obligations. Follow my current direction before moving from a plan to implementation or expanding scope.

## Current stopping point

Foundation documents prepared; exploration remains at Stage 1. Next action is to open this handoff in the new thread and examine the small example. At future meaningful pauses, replace this section with completed work, evidence pointers, unresolved questions, and one next action. Git history retains earlier versions.
