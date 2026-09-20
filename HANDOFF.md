# Lonely Runner — new-thread handoff

**Prepared:** September 20, 2026

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

Standing direction from Vance: during the entire active investigation, watch for striking patterns, anomalies, and exceptions. Preserve them with exact evidence, test nearby counterexamples, and explain what the pattern does and does not establish. His observation about consistent touch-time spacing led to the latest continuation below.

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
- `scripts/analyze_eight_runner_replacement.py` and `experiments/eight_runner_replacement.json`: exact interval explanation of the 6-to-12 replacement, controls 11/13/18, touch-time spacing, and a fixed-case argument excluding all other faster integer replacements for the deleted speed 6. The explanation and pattern/exception record extend the same research note.
- `scripts/compare_reference_runners.py` and `experiments/reference_runner_roles.json`: all 96 reference runners in 13 explicit configurations, with exact maxima and symmetry checks. The same research note now distinguishes a most-constrained runner from an exactly tight runner.
- `notes/DOMAIN_CONNECTIONS.md`: September 20 map of algebra, number theory, geometry, dynamics, waves, quantum phase notation, and log coordinates. `scripts/check_phase_space_examples.py` and `experiments/phase_space_examples.json` certify three small geometric comparisons. S9–S10 record the newly inspected relation and polyhedron papers.
- `scripts/analyze_cooperative_blocking.py` and `experiments/cooperative_blocking.json`: seven eight-runner configurations, all 56 references, three constraint deletions, complete cooperative coverage, and equal-snapshot controls. The explanation extends `notes/TIGHT_CASES_4_8_12.md`.
- `scripts/analyze_reference_patterns.py` and `experiments/reference_patterns.json`: grouping of seven tight references from ten existing eight-runner configurations into three normalized sets, fixed individual blocking fractions, and certified near-peak timing widths. The same research note records these further patterns.

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

Continuation completed: omitting relative speed 6 leaves exactly two open opportunities for exceeding 1/8, `(9/56,7/40)` and its reflection, besides four isolated equality times. Speed 12 stays too close throughout both openings while preserving the four equality times. Any tight integer replacement `w>7` must be divisible by 6 (check time 1/6) and at most 15 (coverage width), so only 12 works for this fixed deletion. This elementary explanation reproduces known structure; it is not a new general theorem. Replacements 11 and 13 reach 1/6; 18 reaches 3/23 despite meeting the reference at the same critical instants. All retain the old equality times, showing why that pattern alone is insufficient.

Vance's spacing observation: consecutive-speed cases have global touch times `q/n` with `gcd(q,n)=1`. Four and eight runners have equal cyclic gaps; twelve alternates 1/3 and 1/6. Sixteen provides another power-of-two check with equal 1/8 gaps. Reflection symmetry is shared by every integer-speed case, including non-tight ones. A directly relevant August preprint was found and logged as S8; its broader claims were not audited.

Latest follow-up: Vance suggested the particularly constrained runner might occupy a different speed rank. The exact comparison confirms this. Actual speeds `{1,2,3,4,8,9,11,16}` have only speed 4 tight at 1/8. Reflecting the original uneven case via `v -> 14-v` makes only the fastest runner tight. Consecutive examples have both extremes tight. The control `{1,2,4,8,16,32,64,128}` has no tight runner; its most-constrained runner (speed 2) still achieves 32/127 > 1/8. Record the distinction: minimize each runner's best full-cycle separation to identify the most constrained; equality with 1/n is a separate property. Independent relative sign changes preserve the selected runner's distances, so its speed rank is not intrinsic. Other references must be rechecked after such changes.

September 20 direction: Vance asked to explore other domains for clues, then more dimensions. The completed first map identifies integer relations among relative speeds as a common object in number theory, geometry, and wave notation. The state is one point in an `(n-1)`-coordinate torus, and loneliness means meeting a closed central box. Ambient dimension and orbit-closure dimension differ: integer examples still follow closed one-dimensional paths. Exact three-runner comparisons demonstrate touching the box, entering it, and missing an artificially strengthened target. Zero allowed duration can still contain valid equality times.

S9 reports a short odd-sum integer relation as a necessary condition for tightness or a counterexample; it is not sufficient. The tight 6-to-12 replacement and non-tight 6-to-11 control already share a short relation, providing a countercheck. The earlier Class C paper explicitly calls its broad universality statements conjectures. Quantum phase equations share a formal representation, but no quantum theorem or physical mechanism was transferred. No universal law or new LRC theorem is claimed.

Continuation completed September 20: deleting relative speeds 2 and 3 leaves six strict openings at the original 1/8 target. Relative speeds 11 and 13 cover them, with genuine overlap needed in two reflected openings. The complete configuration has the same four tight times as before. At 3/8, speeds 5, 11, and 13 tie; 11 controls just before and 13 just after, so the controlling sum is 24 rather than 8. The earlier sum-equals-n observation does not generalize. Conditional on a reduced time q/n and opposite threshold phases, divisibility by n of the speed sum does follow.

Changing relative 11 to 19, or 13 to 21, preserves the entire labeled phase vector at all four old touch times, yet raises the selected maximum to 4/25 or 2/13; every runner in these two controls exceeds 1/8. Counting short additive relations also fails to explain tightness monotonically.

A separate one-speed control directly supports Vance's earlier role intuition: actual speeds `{1,2,5,6,7,8,12,14}` have only speed 1 tight, while slowing 14 to 13 makes only speed 8 tight. The latter runner's absolute relative speeds are exactly `{1,...,7}`, explaining its whole distance curve by the consecutive case. This control is non-tight only for the initial reference, not for the full configuration. All 56 references and three fixed-target deletions were exactly crosschecked; the current work makes no novelty or general proof claim.

Further pattern check completed: ten existing eight-runner configurations contain seven tight references, which reduce to three normalized absolute-relative-speed sets. This grouping is within our data, not a classification. Every individual competitor blocks exactly 1/4 of a common integer-speed cycle at the 1/8 target; speed changes the number and duration of visits, not their total fraction. This elementary invariant follows from uniform circular motion, but overlapping totals cannot prove that a valid time exists.

The consecutive and single-replacement cases have identical full distance envelopes near all four peaks, yet differ at 1/12. The double-replacement case has steeper middle peaks. After a diagnostic 1% relaxation of the threshold, its middle openings are only 45/143 (about 31.5%) as wide as the first two cases; outer openings match. Complete piecewise-linear checks certify the local formulas throughout the small threshold-relaxation range. The actual conjecture threshold is unchanged.

Next useful action: investigate which overlaps among the equal-total-duration blocking schedules are forced by the speed relations. Keep the distinction between positive-duration gaps and isolated valid contacts, and retain original runner counts and all-reference profiles. Follow Vance's next direction; no broad scan is authorized. Git history retains earlier stopping points.
