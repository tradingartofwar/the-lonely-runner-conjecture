# Lonely Runner — new-thread handoff

**Prepared:** September 24, 2026

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
- `notes/BLOCKING_OVERLAPS.md`, `scripts/analyze_blocking_overlaps.py`, and `experiments/blocking_overlaps.json`: exact overlap/touch/gap arithmetic, complete blocking schedules for the seven existing configurations, 147 pair-duration crosschecks, and a blocking-count identity.
- `notes/FIBONACCI_CHECK.md`, `scripts/check_fibonacci_patterns.py`, and `experiments/fibonacci_patterns.json`: prescribed Fibonacci prefixes, nearby controls, an additive collision constraint, and a finite Fibonacci/Lucas pattern in maxima and peak times.
- `notes/FIBONACCI_RECURRENCE.md`, `scripts/analyze_fibonacci_recurrence.py`, and `experiments/fibonacci_recurrence.json`: small upper-bound subsets, full-prefix witnesses through 21 total runners, eight speed controls, and an unreviewed explanatory reconstruction of the now-located known formula (Sources S11–S12).
- `notes/BLOCKING_CHAINS.md`, `scripts/analyze_blocking_chains.py`, and `experiments/blocking_chains.json`: minimum open-window chains for eight prescribed configurations, 46 graph/greedy comparisons, 21 sole-blocker witnesses, and a 13-to-8 control that blocks all denominators up to 8 while allowing time 4/13.
- `notes/VARIABLE_SPEED_FAMILY.md`, `scripts/analyze_variable_speed_family.py`, and `experiments/variable_speed_family.json`: an elementary argument for every positive integer seventh speed added to `{1,4,5,6,7,11}`, an explicit witness formula, exact certificates, and endpoint counterchecks. Selected reference only; independent proof review remains outstanding.
- `notes/TWO_VARIABLE_SPEEDS.md`, `scripts/analyze_two_variable_speeds.py`, and `experiments/two_variable_speeds.json`: an exact finite reduction for every distinct positive integer pair added to `{1,4,5,6,7}`. A local duration bound, 28 certified intervals, and eight residual witnesses cover the selected reference; independent proof review remains outstanding.
- `notes/LOCAL_OVERLAP.md`, `scripts/analyze_local_overlap.py`, and `experiments/local_overlap.json`: local redundancy versus blocking concentration in eight prescribed cases, 64 region measurements, 384 pair-duration crosschecks, and an unreviewed positive-duration argument for the structured family `{0,1,4,5,q,2q,u,v}` with q>=53 and u,v>=q, all distinct.

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

Overlap continuation completed: for meeting centers `p/a < q/b`, put `D=aq-bp`. At target `1/n`, the facing blocking endpoints have signed gap `[nD-(a+b)]/(nab)`. Its sign determines overlap, exact contact, or a gap. The same speeds 11 and 13 give all three in the same tight configuration: determinants 1, 3, and 5 yield overlap 2/143, contact at 3/8, and gap 2/143. Speed 7 covers that last gap entirely. Exact contact is useful only when every other runner is clear too.

This strengthens the earlier conditional speed-sum observation: for integer relative speeds and n>=3, any tight maximum has active increasing and decreasing curves, whose touching blocking endpoints force `n | (a+b)`. No denominator assumption on the touch time is needed. It is a necessary condition for equality, not a proof of the conjectured lower bound or a sufficiency test.

Blocking-count accounting also gives `R=(n-2)/n+U`, where U is completely clear duration and R counts blocking beyond the first blocker. For eight runners, R=3/4+U. All three tight schedules have R=3/4, but their summed pair overlaps differ; a non-tight control lies between two tight cases in that latter statistic. Zero duration still cannot distinguish isolated valid times from no valid times. The seven schedules and 147 pair durations were crosschecked exactly; no new speed-set search was run. See `notes/BLOCKING_OVERLAPS.md`.

Fibonacci check completed after Vance noticed `3+5=8`: the general speed-sum condition is not Fibonacci-specific, but a complete Fibonacci speed family has real structure. If relative speeds a, b, and a+b are present, the first two cannot control a positive lonely peak through opposite phases: the third then coincides with the reference. At t=3/8, speeds 3 and 5 are 1/8 away while speed 8 is at distance zero. This applies to all additive triples, not only Fibonacci triples.

Distinct Fibonacci prefixes starting `{1,2,3,5,...}` give selected-reference maxima 2/11 for n=6..9, 5/29 for n=10..13, and 13/76 for n=14. Peak times are respectively `{3/11,8/11}`, `{8/29,21/29}`, and `{21/76,55/76}`. These match alternating Fibonacci numerators and Lucas denominators. Two full plateaus and one case of the third are verified; no general formula or infinite-prefix limit is proved. Adding 55 or 377 creates collisions at the preceding plateau's maximizing times.

All references were checked for the eight prefixes n=3..10 and four nearby eight-runner controls; selected references only for n=11..14 and seven pair comparisons. The script has 95 reference evaluations, all independently crosschecked with interval feasibility. No prefix with n=5..10 has a tight runner. Changing 21 to non-Fibonacci 20 preserves the eight-runner selected maximum 2/11; changing it to 22 gives 1/6. Thus this single plateau is not unique to Fibonacci inputs. The source search found the broader lacunary-sequence context but no verified Fibonacci-prefix formula; absence from the search is not a novelty claim.

Modeling-language follow-up: Vance asked which representations remain untested. The prioritized shortlist is discrete recurrence dynamics, continued fractions, interval-coverage graphs, and integer-lattice geometry. The last two have established related literature, but our examples have not yet been treated through graph or lattice certificates. See the appended section of `notes/DOMAIN_CONNECTIONS.md`.

A small exact preview confirms that the Fibonacci matrix A=((0,1),(1,1)) has diagonal sums 11,29,76 at powers 5,7,9, while the diagonal entries give the observed peak-time numerators. Also, 3/11,8/29,21/76 are alternating continued-fraction convergents of alpha=(5-sqrt(5))/10. These identities re-express the finite observed pattern; they do not prove further maxima or convergence of maximizing times. The phase map (x,y)->(y,x+y mod 1) advances through Fibonacci runner indices at a fixed physical time, starting on (t,2t mod 1); it is not a new physical-time evolution or an arbitrary torus initial state.

Recurrence continuation completed: four sparse subsets have maxima independently crosschecked by piecewise-linear and interval methods. Full-prefix witnesses certify the selected reference for every n=6..21, extending the third plateau through n=17 and adding n=18..21 at 34/199, times 55/199 and 144/199. Critical speeds 8,55,377,2584 successively block the old peaks; speed 3 supplies the decreasing curve at each new peak. An integer Fibonacci/Lucas identity explains why intervening speeds preserve it. This is not a new all-reference check.

The renewed source search found a direct match: Zhuravleva (2011), Theorem 1, already establishes the general plateau formula and its limit; Pandey (2013), Theorem 5, provides the modular witness. Sources S11–S12 supersede the earlier unsuccessful search. Our written interval argument remains an unreviewed reconstruction, with no novelty claim. The limit time alpha=(5-sqrt(5))/10 gives a four-phase cycle approached as the runner index increases; the best infinite-prefix gap is (3*sqrt(5)-5)/10. This is not physical motion settling into a cycle.

Eight exact nearby controls show that at each plateau's final prefix, lowering its largest speed by 1 destroys the old maximum, while raising it by 1 preserves the value and both peak times. The new smaller maxima were not computed. A reversed endpoint ordering in S12 was also noticed and checked on residues modulo 11; it does not affect the interval bound. See `notes/FIBONACCI_RECURRENCE.md` for scope, calculations, and the draft reconstruction.

September 23 direction: Vance does not want Fibonacci to limit the investigation and favors the question, "What prevents the runners from collectively blocking every possible moment?" The Fibonacci detour is complete for current purposes. We applied the small-certificate idea to seven existing non-Fibonacci eight-runner cases and one new nearby control, with the selected reference only.

The three tight schedules require minimum covers of 18,18,26 blocking windows, down from 28,34,47 total visits. Greedy chains agree with graph shortest paths across all 46 blocked components in the eight inputs. Exact witnesses show every one of the seven competitors is individually necessary in each tight case, at the fixed original target 1/8; the compression removes visits, not whole runners. Non-tight cases can have the same minimum window count as tight ones, so this statistic is not a classification.

The comparison exposed a shared shortcut: none of the old seven inputs has a relative speed divisible by 8, so odd-eighth times are immediately valid by modular arithmetic. To remove that shortcut, change `{1,4,5,6,7,11,13}` to `{1,4,5,6,7,8,11}`. Speed 8 collides at all four old lonely times. In fact every reduced denominator at most 8 is blocked by a divisible speed. Yet the new maximum is exactly 2/13 at 4/13 and 9/13, independently crosschecked by the two existing methods.

The first new allowed window is `[17/56,5/16]`, width 1/112, between the blocking periods of speeds 7 and 6. Speed 13 used to cover it; speed 8 stays clear. Removing `13=6+7` frees the new handoff while adding `8=1+7` blocks the old one. This uses the general additive collision rule without requiring Fibonacci speeds. The new case's four allowed intervals equal the positive-length intervals of the old 13-to-12 control, with the four old singleton witnesses now absent. The full calculation and scope are in `notes/BLOCKING_CHAINS.md`. No general noncoverage theorem or novelty is claimed.

September 24 continuation: Vance approved fixing the six relative speeds `{1,4,5,6,7,11}` and allowing a seventh distinct positive integer speed w with no upper bound. The AI developed the proposed finite reduction and found a sharper modular explanation. To block `t=1/8`, w must be divisible by 8. The six fixed runners are clear throughout `I=[17/56,5/16]`, width 1/112. Covering this connected closed interval with one runner's disjoint open blocking windows requires `1/(4w)>1/112`, so w<28. Only 8,16,24 remain, and all allow `t=17/56`. Exact interval and affine-phase certificates support the argument; no scan over an unbounded range was used.

The sharper pattern removes even those exceptions: with w=8m, the phase at `17/56` is `17m/7`, so blocking both selected times requires `56|w`. Then `t=17/56+1/(8w)` is still inside I and the added runner is exactly 1/8 away. Together with `t=1/8` when `8` does not divide w and `t=17/56` when `8|w` but `56` does not divide w, this gives an explicit witness for every admissible w. The argument is for the selected reference only, has not received independent proof review, and carries no novelty claim. See `notes/VARIABLE_SPEED_FAMILY.md` for the full derivation and exact certificates.

Counterchecks: speed 13 covers the whole interval but cannot block the old eighth time; speed 112 blocks both interval endpoints but leaves the interior witness `39/128`. No fixed finite list of rational times can work for all integer w: a sufficiently large common denominator multiple collides at them all. The formula therefore adapts the witness to w. Nine prescribed inputs include a very large speed to demonstrate direct arithmetic, not to establish the infinite statement. The previous divisibility-plus-width method from the 6-to-12 explanation was reused, then simplified; Fibonacci is not assumed.

Two-variable continuation, September 24: Vance approved the next step. Fix `{1,4,5,6,7}` and add any distinct positive integers x<y outside that core, still eight total runners. The AI found that speeds 16 and 23 cooperatively cover all of the previous interval `[17/56,5/16]`, although neither can do so alone; their blocking windows overlap by 15/2944. But `t=5/11` gives minimum distance 2/11, and a different interval `J=[25/56,15/32]` remains clear. This is a countercheck against extending the one-runner argument unchanged.

The complete fixed-family reduction uses the duration bound `D_v(J)<=L/4+3/(16v)`, derived by splitting J into full periods and a remainder. Here L=5/224. If both variable speeds are at least 34, the pair leaves at least 1/7616 of J clear. Otherwise the smaller speed belongs to 28 possibilities. For each, an exact positive-width clear interval bounds the larger speed by `y<1/(4*width)`. Together with the necessary condition `8|x` or `8|y` for blocking the old eighth time, only eight pairs remain: `(2,8),(3,8),(8,9),(8,10),(8,11),(11,16),(11,24),(22,24)`. All have exact witnesses at 4/13, 5/11, 6/13, or 7/15, with minimum distances strictly above 1/8.

The 28 affine phase certificates independently validate the intervals chosen by the intersection checker, and all eight point witnesses are directly verified. Controls also check the fast pair `(40,48)` and the old tight pair `(11,13)`, which retains only four isolated odd-eighth times. Thus the family contains both slack and exact touches. The unbounded conclusion rests on the written reduction, not a scan. Selected reference only, positive integer parameters, no novelty claim, and independent proof review outstanding. See `notes/TWO_VARIABLE_SPEEDS.md` and its exact JSON certificates.

Local-overlap continuation, September 24: Vance suggested an unknown variable might be creating room and approved tracking overlap inside the fixed runners' openings. We now fix relative speeds `{1,4,5}` and examine four other competitors, retaining eight total runners. Their fixed-runner allowed region A is six intervals of total length 3/8. On A, let T add the four individual blocking durations, R count blocking beyond the first blocker, and E=T-|A| measure excess local concentration. Exact accounting gives U=R-E. More local overlap alone does not guarantee more clear duration: the tight `(6,7,11,13)` case has R=E=34079/240240, while `(6,7,8,11)` has smaller R=271/2310 but U=29/1232>0. The tight case still retains its four equality times.

The common-start overlap of the four competitors lies where fixed speed 1 also blocks, so that initial overlap alone does not locate a valid all-seven opening. An arithmetic relationship supplies repeated overlap: the bad sets for q and 2q intersect exactly where `||qt||<1/16`, giving overlap fraction 1/8 and union fraction 3/8 per period 1/q. For a periodic set of occupied fraction p and frequency h, the interval-duration upper bound is `pL+p(1-p)/h`. Grouping the doubled pair before adding the other two runners uses this forced duplication without calculating the final clear set first.

On the fixed-runner interval `J=[9/32,3/8]`, length 3/32, the resulting bound is `U_J>=3/256-15/(64q)-3/(16u)-3/(16v)`. Thus all distinct integer velocities `{0,1,4,5,q,2q,u,v}` with q>=53 and u,v>=q leave at least `(3q-156)/(256q)>0` clear duration for the selected reference in J. This is an elementary structured-family proof candidate with independent review outstanding, no novelty claim, and no arbitrary-four-speed conclusion. The constant 53 is a sufficient coarse bound, not a sharp cutoff.

Eight prescribed cases, 64 regions, and 384 pair durations were checked exactly with independent interval operations; no speed-set scan was run. Diagnostics include q=52 (uniform bound zero but actual openings), q=53, and q=56. In `{0,1,4,5,56,112,64,72}`, time 6/17 gives minimum 4/17. Changing 112 to 113 reduces the pair's overlap inside J from 11/896 to 9/3616 and blocks that witness at distance 2/17; other openings remain. See `notes/LOCAL_OVERLAP.md` for the full derivation, concentration countercheck, and scope. This records Vance's hypothesis and how the measurements sharpened it; it is not evidence of a new physical variable or universal multiplicative law.

Next useful question: which relationships beyond exact doubling force enough repeated local overlap to guarantee an opening? The challenge is a lower bound derived from the speeds, not merely measuring overlap after solving a case. Retain local concentration and exact equality points. Follow Vance's direction before expanding scope; no broad scan or independent reviewer contact is authorized. Interval-graph certificates are implemented; lattice certificates are not. Git history retains earlier stopping points.
