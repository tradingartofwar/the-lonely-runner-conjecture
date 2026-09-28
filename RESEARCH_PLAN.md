# Research plan and strategy

**Created:** September 19, 2026  
**Status:** Stage 2 implemented and checked September 19, 2026; a minimal Stage 3 demonstration exists. Broader stages remain proposals.

**Founding team:** Vance + AI. Public contributions are welcome through reviewable pull requests; no automatic agent team or background work.

## Purpose

Have fun working on a genuine mathematical question. Learn its structure well enough to ask a smaller question that matters. A useful explanation, a tested failed idea, or a reproducible computational observation is a worthwhile outcome; none automatically constitutes research novelty.

The project began from a search for an enjoyable open problem suited to intuition, multiple representations, exact mathematics, and computation. Any broader origin conversation is context only, not a mathematical connection or proposed physical mechanism.

## Current research queue — September28, 2026 UTC

The detailed stages below preserve the original strategy. The current state is in [HANDOFF.md](HANDOFF.md); these bounded priorities govern the next work:

| Priority | Task | State and constraint |
| --- | --- | --- |
| Completed | Fixed and adaptive time-pair studies | [Adaptive pair](notes/ADAPTIVE_REFLECTED_PAIR_2026_09_28.md) covers every admissible V and every runner11 phase in the fixed family; all8|V have duration at least1/(56V) as a supplied proof candidate. |
| Completed this round; Vance's small-gcd priority | Freeze a certificate input/cost budget and test selection before seeing overlaps | [One-pair policy](notes/ONE_PAIR_SELECTION_2026_09_28.md) uses supplied-core widest window, four singles, at most one overlap, and one endpoint. Six existing controls end in strict16 failure; no rule refinement. A cap test excludes all one-pair positivity in another window without querying overlaps. Exact records separate pair-stage failures and endpoint rescues. |
| Completed this round | Use pair-compatible full covers to specify one higher-order query | [Cover obligations](notes/COVER_OBLIGATION_SELECTION_2026_09_28.md): three frozen controls; strict16 uniquely forces triple6/11/16 mass1/896 under cover and its known geometric zero repairs the bound;112 exits on positive pair optimum;13 uses isolated endpoint. Explicit larger input/cost contract, exact certificates, separate verification; no new existence coverage. |
| Completed this round | Test collective obligations when no individual triple is compulsory | [Collective obligations](notes/COLLECTIVE_COVER_OBLIGATIONS_2026_09_28.md): symmetric abstract pair moments give four zero coordinate minima but force corrected aggregate `H=1/7` on every cover; any proper subset of triple types can vanish together. Same summaries admit opening `1/7`. Nineteen exact certificates and Möbius verification pass. Abstract only; `H=C-U` does not yet make geometry cheap. |
| Completed this round | Seek an existing runner-realizable collective-only window | [Collective-window audit](notes/COLLECTIVE_WINDOW_AUDIT_2026_09_28.md): among eighteen archived tree misses, eight are pair-positive, eight force some individual triple, and two reflected records realize the collective-only pattern. The physical windows have duration `1/600`; alternative covers remain abstract. Fifty-eight exact certificates and separate exact reconstruction agree. |
| Completed this round | Find a minimal joint exclusion on the physical counterpart | [Joint triple exclusions](notes/JOINT_TRIPLE_EXCLUSIONS_2026_09_28.md): exactly two pairs are inclusion-minimal within the four actual triple coordinates, with lower bounds `49/524400` and `13/22800`. Every singleton and other pair retains a simultaneous cover countermodel. All four bounds and supplied `H` recover `1/600`; the frozen lexicographic selector chooses the weaker pair. Fifty-two exact optimizations and separate verification pass. The dual forms are prior graph corrections, not new inequalities. |
| Completed this round | Compress the selected two-exclusion repair | [Shared pair containment](notes/SHARED_PAIR_CONTAINMENT_2026_09_28.md): `B_15 intersect B_38` is one component; two exact complement phase ranges verify both zero triples from one cached occurrence table, and the prior five-edge correction gives `49/524400`. This still carries two predicates and assumes the pair. Strict16/tight13/doubling112 separate geometry from duration and selection; exact independent reconstruction passes. |
| Completed this round | Select one shared-pair query from cheaper inputs | [One-query selector](notes/ONE_CONTAINMENT_SELECTION_2026_09_28.md): largest conditional slack selects `{61,100}` and fails the target; fewest positive components selects `{15,38}` and certifies `49/524400`. Strict16 succeeds, doubling112 exits pair-only with failed selector diagnostics, and tight13 has no eligible duration branch. Ten eligible pair geometries/29 components show the successful rule has a larger enumeration contract. No retuning, held-out-validation, runtime, or general-selector claim. |
| Completed this round | Replace component enumeration with arithmetic ordering | [Lap-band count](notes/LAP_BAND_COMPONENT_COUNT_2026_09_28.md): positive pair components equal integer lap pairs in one open determinant strip. Exact floor/ceiling rows match all 24 archived counts and reproduce the target/strict choices without interval lists or new containment queries. The active selector charges four pairs/seven rows; validation and diagnostics show the iteration remains speed-dependent. Elementary proof candidate plus independent 311-event/287-cell reconstruction; no held-out, runtime or general-selector claim. |
| Completed this round | Remove the lap-row scan with a floor sum | [Floor-sum count](notes/FLOOR_SUM_COMPONENT_COUNT_2026_09_28.md): two clipped rectangle half-plane counts and a Euclidean recurrence reproduce all24 pair counts and all archived branches without lap-row iteration. Strict boundaries pass. Cost is mixed/negative on the active small cases (12 recurrence rounds versus7 rows) and improves only on doubling diagnostics (28 versus39); unlike primitives imply no runtime order. Independent direct lattice/column/event checks cover 410 points,287 cells and173 fields. |
| Completed this round | Audit selector transfer on the archived tree misses | [Selector transfer audit](notes/SELECTOR_TRANSFER_AUDIT_2026_09_28.md): eight labels exit pair-only and minimum components certifies all ten active labels; largest slack certifies four transfer-active labels and fails four, plus both development labels. All six are oracle-classified ranking failures. Eight transfer reflection mechanisms, archival rather than held-out. A tied one-component success/failure proves the lexicographic tie-break matters and component count is not sufficient. Exact separate reconstruction checks 848 fields. |
| Immediate proposed continuation | Explain minimum-count ties without adding a query | On already archived eligible pairs, freeze one tie-only speed/window-arithmetic discriminator before reading containment answers. Use the squares125 one-component success/failure as development data and Fibonacci ties plus strict16 as controls; retain physical lexicographic fallback and every failure. Add no new speeds, windows, references, containment-query budget, broad scan, alternate-window campaign, or `+7/+9` work. |

The [56/113 audit](notes/SMALL_GCD_DISTINCTION_REVIEW_2026_09_27.md) already closes the original coarse-bound gap and records restricted infinite-family candidates beyond large gcd. Current work targets the unresolved selection/general-scope bridge. Individual concentration supplies an overlap upper cap, not a guarantee of useful overlap; a small verifiable certificate is not automatically discoverable cheaply or forced to exist. Preserve counterexamples, exact endpoint contacts, and the distinction between local certificate failure and failed loneliness. No broad speed search, cutoff polishing, or +7/+9 extension is scheduled.

## Strategic choice

Begin with **tight configurations and the way different runners limit the available separation over time**. The survey identifies tight-instance classification as a research direction [S1 in Sources](notes/SOURCES.md). This gives us something concrete to see and test at small scale.

Use three complementary representations of exactly the same input:

1. A circular track: what happens to the runners?
2. Distance-versus-time curves: which runner is closest to the reference, and when does that identity change?
3. Exact allowed-time intervals: when do all required inequalities hold together?

Moving between these representations may reveal a useful pattern. That is a proposed method, not a claim that our perspective is unique.

Frontier computation is not the current assignment. The September 25 source check found a September 24 preprint revision reporting fourteen and fifteen total runners [S7](notes/SOURCES.md); its proof and computation have not been audited here. Before choosing any frontier-scale reproduction or search, refresh the literature and audit the reduction, code, certificates, memory needs, and runtime. A reported runner-count frontier is not a tractability guarantee.

## Proposed stages

Implementation evidence: [checker validation](notes/CHECKER_VALIDATION.md), [exact checker](lonely_runner/checker.py), and [three-case demonstration](demo/index.html). The stage descriptions below remain the design; the demo currently has three presets and no distance-curve plot or arbitrary-speed editor.

### 1. See and understand one example

Start with total velocities `(0,1,2)` and select the stationary runner. Explain why the threshold is `1/3`, find valid times, and show why equality counts. Then switch the reference runner: each runner has its own question and may have a different best time.

Compare with `(0,1,3)`, whose stationary runner can achieve separation `1/2`.

**Exit:** Vance can point to what the conjecture asks; the AI can derive the example exactly. No requirement for Vance to learn a formal syllabus.

### 2. Build the smallest trustworthy numerical foundation

If Vance proceeds to implementation, write a small exact-arithmetic reference checker and tests before adding search scale. The [baseline](notes/MATHEMATICAL_BASELINE.md) specifies two different checking methods.

Recommended first implementation: Python standard-library rational arithmetic for correctness and inspectable output. This is a design preference, not an installed dependency claim. Optimize only after measuring a real bottleneck.

Required outputs: input and reference runner, original `n`, normalization map, threshold, exact feasible intervals including singleton points, a witness when available, and exact maximum separation when requested.

**Exit:** known fixtures, invalid inputs, normalization invariance, and independent-method comparisons pass. A sampled plot agrees with exact results visually, but never overrides them.

### 3. Add a small visual laboratory

After the checker is reliable, present a track with play/pause, speed editing, reference-runner selection, threshold shading, exact witness stepping, and the lower envelope of distance curves. Selecting a point should reveal which runners constrain it.

Keep display rounding separate from certification. Free movement in the display is not an exact search. The standard mode has common initial position and constant speeds; any variants must be visibly labeled.

**Exit:** Vance can suggest a change, see its consequence, and ask the checker for the exact answer. A standalone local prototype is sufficient; website hosting is not assumed.

### 4. Make a bounded atlas and test one idea

Initial proposed search domain: stationary reference, `1 <= v1 < ... < vk <= 12`, `k=2,3,4`, with gcd 1. These are study cases, not a frontier search. Validate the checker first and estimate cost before enlarging the domain.

For each case record maximum separation `L`, excess `L-1/n`, the maximizing times, and which distance curves attain the minimum there. Label tight cases (`L=1/n`) separately from non-tight cases and never rank by a rounded decimal alone.

Compare consecutive speeds, known nonconsecutive tight examples, one-speed changes, and bounded random controls. Test whether an apparent signature survives held-out cases. Random sampling is a comparison tool, not an exhaustive search.

**Exit:** a reproducible, bounded result and one specific question worth discussing. Do not expand computation merely because it is available.

### 5. Choose a research direction from evidence

| Candidate direction | Small first question | What would count as progress |
| --- | --- | --- |
| Constraint handoffs | Which runners determine the peaks of the lower envelope in known tight examples? | A precise signature, a counterexample to it, or a proved restricted statement |
| Perturbations | When one integer speed changes, what destroys or preserves tightness? | A checked family and an explanation of its scope |
| Certificate efficiency | Can repeated interval constraints be removed without changing the exact result? | Same verified answers with smaller certificates or measured speed improvement |
| Literature reproduction | Can we reproduce a small case of an existing modular sieve? | An independent match with pinned code, parameters, and logs |
| Frontier assessment | Which bottleneck blocks the next runner count in the published method? | A realistic cost estimate or a justified reduction, not an assumed extension |

The first three are exploratory proposals and may rediscover known work. Search for prior results before selecting an originality claim. The fresh spectrum-paper lead in Sources makes that check especially important.

## Working loop

Notice something -> state a testable proposition -> try hard to break it -> compare with known work -> explain what survives. Human and AI collaborators may each introduce and challenge ideas. Maintain room for detours and enjoyment.

A useful experiment note needs only: question, exact assumptions, source/code revision, bounds or seed, command, result, counterchecks, and what changes next. Create `experiments/` and code folders only when they have actual content; do not prebuild a workflow platform.

## Verification and resource limits

- A witness proves that one input passes. A claimed maximum needs a complete upper-bound argument or exhaustive exact evaluation over all relevant segments.
- A search failure may be a bug, normalization mistake, endpoint error, or missed time. Check these before treating it as mathematical evidence.
- No 14-runner campaign, paid compute, long unattended run, scheduled job, or external publication is selected by this plan. Agree a bounded budget before any expensive experiment.
- Keep low-level reproduction claims separate from checking an entire published proof.
- If the work stops being interesting, pause with a short handoff. There is no deadline or success quota.

## First next-thread session

Recover the handoff, briefly explain `(0,1,2)` and the exact-equality issue, then follow Vance's current direction. If he asks to begin building, implement Stage 2 with the fixture set and a minimal output view; defer a broad search and a polished interface.
