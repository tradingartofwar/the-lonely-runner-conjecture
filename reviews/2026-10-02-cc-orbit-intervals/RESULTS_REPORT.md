# Orbit intervals: complete finite recovery and a two-source family candidate

Completed October 2, 2026 UTC. AI-assisted derivation, implementation and verification. **OBSERVED** finite coverage and exact reproduction; **HYPOTHESIS / proof candidate** for the parameterized arguments; novelty and independent proof review remain **OPEN**.

The complete interval-and-point representation covered all 1,197 fresh cases and recovered exactly the full physical safe-time set in each case. The strongest analytic result is a two-source construction for every admissible integer r in the fixed (p,q)=(1,2) family. Severe compression remains incomplete: the widest-source policy missed 216 fresh cases. Dropping isolated points lost the fresh case (1,4,13).

## Freeze and scope

The protocol, derivation, development ledger, input list and executable rules were published at **1b4c636a68363047566d5f816c4bda661b0e1c9f**. That commit was fetched and its tree matched the clean local checkout before target execution. No frozen code or policy changed after fresh outcomes.

The ten common-start speeds are

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r).
\]

All parameters are positive integers and all speeds are distinct. The selected stationary reference has target distance at least 1/8, stronger than its required 1/10. This is not an all-reference result or arbitrary mixed-r family.

Fresh inputs are all primitive triples in [1,15]^3 outside [1,12]^3 meeting distinctness, except (1,2,13), (1,2,14), (1,2,15). Those three were already used in the finite family derivation and were excluded before fresh execution. The resulting 1,197 cases include 528 with previously exposed primitive pairs and 669 with new pairs. The deterministic outer box is not a random sample or a uniform finite reduction over p,q,r.

## Frozen comparison

Every core was built from its primitive pair P,Q before any r query. All policies used exact rational contact, closed boundaries and all normalized clock lifts. Selection order was descending width, then earliest starting point; it was fixed without r.

| Retained sources | Development, already exposed | Fresh cases |
| --- | ---: | ---: |
| One widest component | 849/1,050 | 981/1,197 |
| Every component, including isolated points | 1,050/1,050 | 1,197/1,197 |
| Every positive-width component | 1,048/1,050 | 1,196/1,197 |

| Fresh stratum | Cases | Widest | All components | Positive only |
| --- | ---: | ---: | ---: | ---: |
| Previously seen primitive pair | 528 | 484 | 528 | 527 |
| New primitive pair | 669 | 497 | 669 | 669 |
| One normalized clock lift | 887 | 671 | 887 | 886 |
| Multiple normalized clock lifts | 310 | 310 | 310 | 310 |

The two sets of strata partition the same cases in different ways. All 216 widest misses and their complete physical safe-time unions remain in the raw records. Recovery by another component does not count as a widest success.

### A fresh isolated-point counterexample

At (p,q,r)=(1,4,13), the moving speeds are (1,4,5,6,7,11,14,35,13). The complete 1/8-safe set in [0,1] is exactly

\[
\{1/8,3/8,5/8,7/8\}.
\]

The widest core interval [17/56,87/280] has width 1/140 and fails the added constraint. Every other positive-width core component also fails. The retained singleton t=1/8 gives phases

\[
(1/8,1/2,5/8,3/4,7/8,3/8,3/4,3/8,5/8).
\]

Thus isolated points are necessary for this representation to preserve even one witness at the declared 1/8 threshold. This says nothing about isolated-point necessity at the weaker 1/10 threshold. The core itself is mixed; the final safe set is isolated-only.

A different loss appears at (1,6,13): the widest interval [17/56,127/408] fails, while the shorter interval [3/16,23/120] survives and supplies t=3/16. Width alone does not preserve the phase placement needed for a later constraint.

## The analytic value: a complete fixed-pair construction

For (p,q)=(1,2), the first eight moving speeds are (1,2,3,4,5,7,10,19). They are simultaneously 1/8-safe throughout

\[
I=[25/152,7/40],\qquad |I|=1/95,
\]

and at the isolated core time t0=1/8. Every unsafe gap for the added integer speed r has length 1/(4r). Consequently I must contain a safe time whenever r>=24. The fifteen admissible smaller r were all checked exactly; only 6 and 12 fail on I, and t0 handles both. The resulting candidate formula is

\[
t(r)=\begin{cases}
1/8,&r\in\{6,12\},\\
\max\{25/152,(\lceil25r/152-7/8\rceil+1/8)/r\},&\text{otherwise}.
\end{cases}
\]

Its domain is every positive integer r distinct from the eight core speeds. It includes all r=40k, repairing the prior source-class obstruction, and gives t=25/152 for r=40. Positive integer common scaling rescales time inversely. This finite-remainder argument, not the fresh box, supports the infinite-family candidate.

The more general derivation gives an exact first-band contact formula, a sufficient interval-width criterion, and a multiple-lift criterion. For a fixed original pair p,q with a positive primitive-core interval, these reduce the unresolved r to finitely many small multiples of gcd(p,q). They do not supply a uniform bound or prove that every parameter pair has such an interval. The full argument and assumptions are in [DERIVATION.md](DERIVATION.md).

## Verification, cost and unreached branches

The event-based compiler produced 140 primitive-pair cores: 61 mixed and 79 positive-only. It retained 3,938 components, including 258 isolated points; the maximum was 54 components for a pair. No complete core was empty or isolated-only. Development includes supplied-singleton controls, including a rejection, but those are not evidence of an actual isolated-only core.

The alternate checker imports none of the new construction code. It uses the pinned older physical-band intersection implementation and agrees on:

- all 3,938 core components and 63,008 endpoint-band checks;
- all 34,364 component contact bits and 1,197 saved witnesses;
- the complete recovered physical safe-time union in every one of the 1,197 cases.

No full 1/8 failure occurred, so the conditional 1/10 computation and negative-event checks were not reached. No new evidence is claimed for those branches. The full-set correspondence is expected from the representation's exact construction; agreement validates implementation, not universal existence.

Construction charged 140 core builds, 75,348 distinct core events, 150,556 exact phase predicates, 34,364 component queries and 35,394 lift queries. It took 5.778 seconds; alternate verification took 5.642 seconds. These are execution records, not comparative performance evidence. The complete source construction is substantially richer than a fixed compact menu and is not free preprocessing. The evaluation visits every component to retain the full comparison matrix; it is not an optimized dispatcher benchmark.

Reproduction in a temporary output directory matched RESULTS.json, SUMMARY.json and VERIFICATION.json byte for byte. This was the same pinned checkout, not a fresh clone or another domain. The algorithms and review are same-author AI work, not independent human or formal certification. No external literature/novelty search was performed for this stage; no novelty claim is made.

## What to do next

Review the explicit two-source (1,2,r) argument and its endpoint/scaling assumptions before promoting its status. For a subsequent construction study, formulate a small-source sufficiency criterion that preserves phase alternatives, with core-construction cost visible. The 216 widest failures are development evidence for that work, not fresh validation for a revised selector. Freeze a new validation only after the new criterion is concrete. Do not run another larger box merely to accumulate successes.

## Reproduction and records

From the repository root, using a new output directory:

```bash
python reviews/2026-10-02-cc-orbit-intervals/run.py --freeze 1b4c636a68363047566d5f816c4bda661b0e1c9f --out /tmp/lr-orbit-check
python reviews/2026-10-02-cc-orbit-intervals/verify.py --out /tmp/lr-orbit-check
python reviews/2026-10-02-cc-orbit-intervals/reproduce.py
```

[PROTOCOL.md](PROTOCOL.md), [MANIFEST.json](MANIFEST.json) and [VALIDATION_INPUTS.json](VALIDATION_INPUTS.json) identify the frozen study. [DEVELOPMENT.json](DEVELOPMENT.json) preserves the exposed cases and finite family checks. [run/RESULTS.json](run/RESULTS.json), [run/SUMMARY.json](run/SUMMARY.json) and [run/VERIFICATION.json](run/VERIFICATION.json) retain all outcomes, geometry and failure unions. [EXECUTION_RECORD.json](EXECUTION_RECORD.json) records commands, times, statuses and raw diagnostics; [REPRODUCTION.json](REPRODUCTION.json) records exact output hashes. RESULT_MANIFEST.json pins the completed package and research note. Earlier packages remain unchanged.
