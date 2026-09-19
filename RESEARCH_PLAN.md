# Research plan and strategy

**Created:** September 19, 2026  
**Status:** Stage 2 implemented and checked September 19, 2026; a minimal Stage 3 demonstration exists. Broader stages remain proposals.

**Team:** Vance + AI, with no automatic agent team or background work

## Purpose

Have fun working on a genuine mathematical question. Learn its structure well enough to ask a smaller question that matters. A useful explanation, a tested failed idea, or a reproducible computational observation is a worthwhile outcome; none automatically constitutes research novelty.

The quantum-observation conversation prompted the search for an enjoyable open problem. It is origin context, not a mathematical connection or a proposed quantum mechanism. The fit we want to explore is Vance's interest in rhythm, phase, and structure combined with AI's ability to formulate and test precise questions.

## Strategic choice

Begin with **tight configurations and the way different runners limit the available separation over time**. The survey identifies tight-instance classification as a research direction [S1 in Sources](notes/SOURCES.md). This gives us something concrete to see and test at small scale.

Use three complementary representations of exactly the same input:

1. A circular track: what happens to the runners?
2. Distance-versus-time curves: which runner is closest to the reference, and when does that identity change?
3. Exact allowed-time intervals: when do all required inequalities hold together?

Moving between these representations may reveal a useful pattern. That is a proposed method, not a claim that our perspective is unique.

Do not make the first assignment an exhaustive 14-runner search. According to the frontier source inspected, that is the next case beyond its reported result, not a tractability guarantee. Before committing to it, audit the reduction, code, certificates, memory needs, and runtime [S3](notes/SOURCES.md).

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

Notice something -> state a testable proposition -> try hard to break it -> compare with known work -> explain what survives. Vance and AI can each introduce and challenge ideas. Maintain room for detours and enjoyment.

A useful experiment note needs only: question, exact assumptions, source/code revision, bounds or seed, command, result, counterchecks, and what changes next. Create `experiments/` and code folders only when they have actual content; do not prebuild a workflow platform.

## Verification and resource limits

- A witness proves that one input passes. A claimed maximum needs a complete upper-bound argument or exhaustive exact evaluation over all relevant segments.
- A search failure may be a bug, normalization mistake, endpoint error, or missed time. Check these before treating it as mathematical evidence.
- No 14-runner campaign, paid compute, long unattended run, scheduled job, or external publication is selected by this plan. Agree a bounded budget before any expensive experiment.
- Keep low-level reproduction claims separate from checking an entire published proof.
- If the work stops being interesting, pause with a short handoff. There is no deadline or success quota.

## First next-thread session

Recover the handoff, briefly explain `(0,1,2)` and the exact-equality issue, then follow Vance's current direction. If he asks to begin building, implement Stage 2 with the fixture set and a minimal output view; defer a broad search and a polished interface.
