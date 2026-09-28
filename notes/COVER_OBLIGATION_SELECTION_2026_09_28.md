# Let hypothetical full covers specify the next overlap question

September 28, 2026 UTC. Baseline `c1e88837c8d48954b0de217d857d0bd6ac9cbccf`, draft PR #3. Material AI involvement: a coordinating agent and three complementary agents supplied calculation, separate verification, and adversarial/prior-coverage review. This is internal AI work, not independent human mathematical validation.

**Question.** Given all local single and pair durations, can a frozen rule choose which additional geometric fact to request by asking what *every compatible full cover would require*?

**Status.** Three prescribed diagnostics are OBSERVED/REPRODUCED within the recorded scope. General implications remain HYPOTHESIS/proof candidates under repository convention. No new family coverage, arbitrary-speed guarantee, novelty claim, or proof-status promotion. The controls are familiar design cases, not held-out tests.

## Increment and prior work

The [one-pair policy](ONE_PAIR_SELECTION_2026_09_28.md) failed locally on strict_16. The next queue requested an explicitly larger information contract that excludes every compatible covering arrangement, rather than just one displayed countermodel.

The relevant mathematics and repairs were already in the repository. [The quantitative review](../reviews/2026-09-27-ultra/optimization.md), especially Sections 2–3, gives the complete disjoint-pair polytope and the exact value of the strict_16 triple exclusion. [Sparse selection](SPARSE_OVERLAP_SELECTION.md) already selects using two geometric compatibility tests in its special family; [two-window dispatch](TWO_SPEED_SPARSE_TRANSFER.md) already supplies its alternate-window route. [Cycle corrections](FOUR_BLOCKER_CYCLE_CORRECTIONS.md) already preserves nonzero higher intersections for 112.

This round adds a **frozen prequery decision rule and exact decision trace**: use the pair relaxation to specify a compulsory overlap amount before querying triple geometry. It does not discover the strict_16 exclusion again or improve the old duration bounds. Its enlarged input and optimization costs are explicit.

## Frozen information and computation contract

[Protocol](../reviews/2026-09-28-cover-obligations/protocol.json), SHA256 `8619a3b5594c9c8219dfd39e69a796e82dfc5204d9ed3b9b5faf17fde79a5de7`, was written before the new calculations. All three inputs use eight common-start runners, reference 0, threshold 1/8, supplied core {1,4,5}, and supplied window J=[9/32,3/8]. Equality is valid. Extra speeds, in frozen order, are {6,7,11,16}, {56,64,72,112}, and {6,7,11,13}.

The input includes L=|J|, four individual durations and all six pair durations. Evaluation of those data is separately charged; they are not free discoveries or inherited from the old one-query budget. No new core/window selection is attempted.

1. Minimize empty-state duration in the 16-state nonnegative pair-moment model. Positive optimum is a sufficient pair-only certificate; stop that input without requesting triple geometry.
2. Otherwise restrict the model to zero empty-state mass. For each of the four inclusive triples, minimize its duration over **all** compatible covering distributions.
3. Select the largest strictly positive minimum, breaking ties by physical speed labels. If every minimum is zero, make no triple query. No ranking changes after seeing geometry.
4. Evaluate only the selected triple's actual duration by intersecting its three blocking schedules. This exact duration also supplies an upper bound. If it lies below the mandatory covering minimum, complete coverage is impossible; reoptimize with this one upper bound to report a duration certificate.
5. For an unrepaired input, check only the right endpoint 3/8, retaining an isolated point separately from a positive interval. No second triple, alternate window, or full allowed-set search by the selector.

Floating optimization may propose a basis, but every accepted optimum requires nonnegative rational primal masses, exact moment equalities, rational dual inequalities on every allowed logical state, and equality of objectives. The independent checker may reconstruct all four-blocker states on these three windows **after selection**, solely to validate the record.

## Why the test concerns every compatible cover

Let x_S denote the nonnegative duration with exactly the blocker set S active. The total, singles and pairs are linear sums of these sixteen masses. Put

\[
\mathcal C=\{x\ge0:Ax=b,\ x_\varnothing=0\},
\qquad
\tau_K=\min_{x\in\mathcal C}\sum_{S\supseteq K}x_S.
\]

For a triple K, any complete cover consistent with the supplied moments has T_K>=tau_K by definition. Thus a speed-derived bound T_K<=u_K<tau_K excludes **the entire set** C. One incompatible displayed countermodel would not establish this implication. Both primal attainability and dual lower inequalities are retained, so a numerical solver's output is not the justification.

Conversely, u_K>=tau_K does not by itself prove a cover exists under every additional physical constraint, and minima for different triples can occur at different abstract arrangements. Zero individual minima do not generally imply that all triples can vanish simultaneously. The frozen policy does not solve that collective selection question.

“Complete cover” here means full coverage **in measure**. Nonempty equality-point sets can have zero measure and are invisible to this model. Abstract feasible distributions are not asserted to be realizable by another common-start runner configuration.

## Exact control decisions

| Control | Pair-only minimum U | Triple information requested | Frozen outcome |
| --- | ---: | --- | --- |
| strict_16: 6,7,11,16 | 0 | T(6,11,16) must be at least 1/896 under every complete cover | Actual T=0; repaired minimum U=1/896 |
| doubling_112: 56,64,72,112 | 761/32256 | None: pair data already suffice | Positive duration certified before escalation |
| tight_13: 6,7,11,13 | 0 | None: all four mandatory minima are zero | Right endpoint 3/8 is valid and isolated |

### strict_16: obligation first, geometric contradiction second

The pair zeros O(6,7)=O(7,16)=0 forbid every state containing either pair. All triple intersections except T(6,11,16), and the four-way intersection, therefore vanish in every compatible abstract model. Define

\[
C=L-\sum_iD_i+\sum_{i<j}O_{ij}=1/896.
\]

Inclusion-exclusion reduces to the exact identity

\[
U+T(6,11,16)=C.
\]

Consequently **every full-cover distribution must allocate exactly 1/896 to this triple**. The four triple minima in physical label order are 0,0,1/896,0, so the query is uniquely selected before its geometry is inspected. The baseline primal retains a nonnegative abstract full-cover arrangement, showing why the pair data cannot already prove U>0.

The overlap of 6 and 11 lies between 31/88 and 17/48. Across its closure, speed 16's fractional phase lies in [7/11,2/3], wholly inside (1/8,7/8). Hence the selected triple has duration zero. This is the **previously known** short geometric exclusion, now requested by the obligation rule. The resulting bound U=1/896 agrees with the existing actual interval [17/56,39/128].

The exact identity makes the useful information quantitative: any certified upper bound T(6,11,16)<1/896 would suffice. A perfect zero test is stronger than necessary. Neither this implication nor its special-family repair is claimed as a new theorem.

### doubling_112: a positive pair baseline prevents an unnecessary query

The pair relaxation's minimum 761/32256 is already positive. The rule requests no triple and asserts no exclusion. Independent diagnostic reconstruction retains all four positive triple durations and four-way duration 1/896; actual U=53/1792. These higher moments are diagnostics, not inputs to this decision. In particular, this control does not test the triple-selection branch or show that selected positive triple durations can be bounded usefully.

### tight_13: the duration model is exhausted

Here O(6,7)=O(11,13)=0, so every triple and the four-way intersection are already forced to vanish. The same C is zero, forcing U=0. Higher duration information cannot create a positive-duration conclusion. At t=3/8 all seven constraints hold; speed 1 is safely separated, while opposing threshold boundaries are supplied by speed 11 at phase 1/8 and speeds 5 and 13 at phase 7/8. Intersecting their closed safe laps with the other constraints leaves the singleton {3/8}. The zero-duration full-cover model and this valid isolated instant are consistent.

## What this does and does not establish

The finite trace separates three requests: no new geometry when pair data already certify duration; one targeted triple when every cover must use it; and pointwise endpoint information when duration cannot help. The speed-16 selection excludes all compatible covers with one extra fact, rather than rejecting an arbitrarily chosen alternative arrangement.

But these controls do not exercise competing positive triple obligations, a nonzero selected triple upper bound, or a strict physical opening whose covering relaxation has no individually compulsory triple. There is no evidence here that “largest forced minimum” is generally the best ranking, that the required geometric upper bound is cheaply discoverable, or that the rule must succeed on arbitrary speeds. Moment-query count is not runtime. The LP has fixed size for four blockers, while generating physical interval lists still grows with speed and rational bit sizes.

## Reproduction and verification

The evidence directory is [reviews/2026-09-28-cover-obligations/](../reviews/2026-09-28-cover-obligations/). Its manifest records exact commands, hashes, verification counts and dependency limits. The primary uses individual blocking intervals and selected intersections; the independent verifier uses a complete rational threshold-cell partition on only the three frozen windows and separately derived cover algebra. No broader checker regression or speed-domain expansion is needed for these standalone additions; existing checker code is unchanged.

Both read-only commands pass:

```bash
python -B reviews/2026-09-28-cover-obligations/primary.py --check
python -B reviews/2026-09-28-cover-obligations/verify.py --check
```

The 12 exact optimum certificates comprise three pair baselines, eight cover-constrained triple minima and one repaired minimum. Independent reconstruction covers 74 threshold cells (9 strict16,57 doubling112,8 tight13), compares all33 supplied total/single/pair quantities, and retains all higher moments for diagnostics. Separate algebra reconstructs the unique abstract full-cover distribution in strict16 and tight13. [Adversarial review](../reviews/2026-09-28-cover-obligations/challenge.md) checked the scripts, arithmetic, scope and prior coverage; [verification report](../reviews/2026-09-28-cover-obligations/verification.md) details the independent implementation.

For **one policy evaluation**, the recorded work is12 LP solves on16 logical states,18 pair queries,75 candidate laps producing42 individual blocking pieces,107 pair-list comparisons,one selected triple query with two further comparisons,and one endpoint check. These are algorithm counters, not wall-time measurements or totals across repeated checks. Only the independent diagnostic verifier reconstructs full four-blocker states. The standalone replay commands require only Python's standard library; regenerating primary optimization certificates with `--write` uses NumPy/SciPy solely to propose candidates for exact acceptance.

## Next bounded question

Freeze a purely abstract four-event moment-model study: can complete coverage require a positive **combined** higher-order mass while every individual triple has zero minimum over compatible covers? Test a selected collective obligation and its dual certificate before proposing another physical speed test. Keep abstract countermodels explicitly separate from runner realizability. This targets the unexercised limitation of the present query rule; it does not authorize a broad speed search, all-reference scan, alternate-window campaign, or the parked +7/+9 work.
