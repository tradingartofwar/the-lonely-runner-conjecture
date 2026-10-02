# Sheet coverage: exact criterion, partial transfer, and a source-class obstruction

October 2, 2026 UTC. Completed after published freeze `afc11e6aae4dad703aac7a587311790572268752`. **OBSERVED / REPRODUCED** for the exact finite checks. General derivations remain AI-generated proof candidates awaiting independent review. No novelty or general Lonely Runner result is claimed.

The revised seven-sheet menu covers **641/643 fresh cases**, leaving two misses. The original four cover 639/643, the revised four-sheet prefix 640/643, and all 36 supplied sheets 643/643. Every fresh contact bit agrees with a separately structured physical-time checker. The complete-development menu therefore **does not achieve complete fresh coverage**. We preserved the failures without repairing the frozen rule.

The more consequential finding is a limit of the source class itself: **all 36 sheets fail at (p,q,r)=(1,2,40), while t=25/152 is physically 1/8-safe.** A denominator-resonance argument extends that obstruction to (1,2,40k), with an explicit safe-time recovery from a continuous core interval. The concrete failure is exactly checked; the family argument remains a proof candidate. Reselecting a menu from these 36 cannot fix this family.

## What the exact criterion adds

The [derivation](DERIVATION.md) retains the prior saturated joint orbit conditions and Bezout clock. Normalize (p,q,r)=g(A,B,C), let d=gcd(A,B), P=A/d, Q=B/d, and choose aP+bQ=1. On a sheet S(s) times [1/8,7/8], the first integer condition is h=Qx-Py. Each nonconstant integer h slice has second range

\[
[C(ax+by)-7d/8,\ C(ax+by)-d/8].
\]

For d>=2, its width is at least 3/2, so any first integer contact guarantees a second. For d=1, the exact additional condition is {C(ax+by)} in [1/8,7/8]. The resulting rational arithmetic progression is tested by inclusive modular counting using standard Euclidean floor sums; prefix counts recover the first admissible contact without scanning all integer h values. Constant first projection uses its full second-coordinate interval, including point bases and equality.

This is an exact decision and witness-recovery criterion for a **supplied** sheet. It is extensionally equivalent to the older enumerating solver, not a new source of safe points or a uniform sheet-existence theorem. Existing polyhedral/segment context remains credited through the earlier [literature comparison](../../notes/CC_LITERATURE_COMPARISON_2026_09_29.md); [FLOOR_SUM_SOURCE.json](FLOOR_SUM_SOURCE.json) records the official primitive documentation inspected and the implementation changes. No general novelty review was performed.

Development checks pass for 35,721 signed floor sums, 8,019 inclusive residue counts/first hits, 14,652 archived sheet bits and all 4,582 successful development witness reconstructions. Six auxiliary contact fixtures include points, constant h, rejection and equality. They are kernel checks, with some repeated speeds, and are excluded from physical-case counts.

## Old failures and revised selection

All eight archived menu misses have normalized d=1. The first integer slices that remain in the selected sheets yield only unsafe third-runner phases; every other selected sheet lacks a first integer contact. DEVELOPMENT.json and DERIVATION.md retain the complete per-sheet diagnosis and all archived fallback witnesses.

All 407 previously exposed primitive cases in [1,9]^3 became development data. A single maximum-gain greedy selection with numeric-provenance tie breaks and the inherited cap of eight selects seven sources [27,21,12,6,8,4,10]. Its first four are separately evaluated to show the equal-size comparison. We did not describe reused holdout successes as validation.

| Fixed representation | Sheets | Exposed development | Fresh validation |
| --- | ---: | ---: | ---: |
| Original menu | 4 | 399/407 | 639/643 |
| Revised greedy prefix | 4 | 401/407 | 640/643 |
| Revised complete-development menu | 7 | 407/407 | 641/643 |
| Entire supplied class | 36 | 407/407 | 643/643 |

The fresh domain is **every** positive primitive, ten-distinct-speed triple in [1,12]^3 outside [1,9]^3, listed in the published freeze before any fresh outcomes. It is a deterministic outer-box transfer, not a random sample or a proved finite reduction. The constructed r=40 failure lies outside it and is explicitly development evidence. The new seven-sheet menu uses three more objects than the original four, so its aggregate gain cannot be attributed to better equal-size selection alone.

## Complete fresh misses and paired changes

| Menu | All fresh misses |
| --- | --- |
| Original four | (1,3,11), (1,6,10), (3,2,12), (3,8,10) |
| Revised four | (1,3,11), (1,6,10), (4,1,11) |
| Revised seven | (1,6,10), (4,1,11) |
| Full 36 | None |

At equal size, the revised four repair (3,2,12) and (3,8,10) but lose (4,1,11), which the original menu covered. The seven-sheet menu additionally repairs (1,3,11), but keeps the new loss. These are case-specific changes, not a monotone improvement or a significance claim.

The two seven-sheet misses both retain an exact fallback in the unchanged source class:

| Miss | Full-class source | Physical time | (x,y,z) |
| --- | --- | --- | --- |
| (1,6,10) | P0:E0-3:K1:L1, index 2 | 3/16 | (3/16,1/8,7/8) |
| (4,1,11) | P2:E0-1:K2:L3, index 13 | 33/104 | (7/26,33/104,51/104) |

For each, five of the seven selected sources have no integer h; sources 27 and 21 have a first contact but fail the residue condition. Their third-runner phases are respectively (1/28,1/12) and (3/40,3/112), all below 1/8. The exact rejection records, inverse clocks, phase lists and physical/torus laps are saved in run/RESULTS.json. Fallback witnesses are not counted as compact-menu successes.

All menu misses occur in the 481 d=1 cases. The old four, new four, new seven and full class cover 477, 478, 479 and 481 there. All four representations cover all 162 d>=2 cases. The latter observation does not prove that their first projection contains an integer for every possible pair; the width theorem guarantees only the second condition once a first contact exists.

## Why the full source class still has a structural limit

For p=1,q=2, exhaustive exact intersection with all 36 xy source records gives only the times

\[
1/8,\quad7/40,\quad3/8
\]

modulo one. Multiplying any of these by r=40k produces an integer, placing the added runner at phase zero. Reflections fail too. The source-class loss therefore persists even if every original sheet is kept or reordered.

For r=40 specifically, the independent physical-time path also finds zero sheet contacts. Direct speed multiplication certifies t=25/152 with phases

\[
(25/152,25/76,75/152,25/38,125/152,23/152,49/76,1/8,11/19).
\]

The complete physical 1/8-safe union is [25/152,11/64] union [53/64,127/152]. This is not a counterexample to loneliness or to the 1/8 target; it is an exact counterexample to uniform coverage by the specified source class.

The first eight moving speeds are safe throughout I=[25/152,7/40], width 1/95. Fixed lap labels [0,0,0,0,0,1,1,3] and endpoint checks certify the interval. For r=40k the added runner's largest connected unsafe time gap is 1/(160k), shorter than I. The derived formula in DERIVATION.md selects a point in I and an r-safe band for every positive k. This analytic family argument is separate from the 643-case validation and awaits independent review.

A sheet whose base follows {(t,2t):t in I} would retain an interval of compatible pair times and avoid this particular loss. Such a source is different from the 36 inherited records. It was not added to the frozen comparison, and nothing here establishes that every pair admits a suitable interval. Full three-dimensional cells have not been shown necessary: a differently oriented sheet suffices for the constructed family.

## Freeze, checks, costs and scope

All 16 manifest-pinned source, executable, derivation, development and validation-input files were published in freeze `afc11e6aae4dad703aac7a587311790572268752`. Remote fetch confirmed the identical local/remote tree before execution. No frozen file was changed after observing fresh outcomes. Both the new runner and the physical checker passed their first fresh execution; no repair, rerun for better outcomes, domain extension or budget extension occurred.

Fresh evaluation started at 03:25:23.332523 UTC, October 2, and ended at 03:25:24.447518, taking 1.115 seconds. Physical verification followed and ended at 03:25:30.752847, taking 6.305 seconds. Each was within its frozen 600-second limit. These are recorded orchestration wall times, not a comparative runtime benchmark. Preparation, source lookup, development, publication and later reproduction are outside them.

The new kernel performs 23,148 sheet calls, 11,143 residue-count calls, 22,286 floor-sum calls and 41,618 Euclidean iterations. The physical checker agrees on **all 23,148 sheet bits**, verifies **1,301 stored witnesses** and **576 source endpoint bands**, and recomputes selection/order/totals. Its inherited routine also computes unused edge bits; the stated bit count includes only compared sheet bits. Both code paths are by the same AI author, with different coordinates and algorithms; this is not separate-agent, independent human or formal proof review.

All 643 cases have full-class witnesses, so the fresh full-class-loss and empty-safe-set branches were not reached. The r=40 class failure was checked separately during development. Do not count unexecuted negative-event or 1/10-fallback branches as validated. Reproduction reruns the pinned executables in a temporary output directory and matches RESULTS.json, SUMMARY.json and VERIFICATION.json byte for byte; it uses the same checked source checkout, not a new clone or new mathematical cases.

The package's result commit contains RESULTS_REPORT.md, EXECUTION_RECORD.json, REPRODUCTION.json, the full case records and RESULT_MANIFEST.json. Resolve its exact SHA with `git log -1 --format=%H -- reviews/2026-10-02-cc-sheet-coverage/RESULTS_REPORT.md`. The research branch remains separate from main.

## Representation checkpoint and next question

We now distinguish three failures with exact records: no first integer contact, failure of the third phase at every available first contact, and absence of the needed times from the entire supplied source class. The gcd/residue criterion preserves simultaneous contact, saturated relations, closed equality, labels and physical recovery. It supports exact decisions about the supplied sheets; it does not preserve the full safe set or prove a compact universal certificate exists.

The recommended next task is **source construction that follows an interval of the actual pair orbit**, beginning with I and the r=40k obstruction. Define a parameter-dependent sheet/recovery contract, distinguish pairs with positive safe duration from isolated-only cases, and test that construction under a new freeze against full physical-time recovery. The present two fresh menu misses become development cases at that point. Another reranking of these 643 cases is not fresh validation, and merely increasing the old menu cannot address the known all-36 failure. No next-stage implementation or sweep was launched here.

## Reproduction

From the repository root:

```bash
python reviews/2026-10-02-cc-sheet-coverage/reproduce.py
```

This checks frozen pins and reproduces the three deterministic outputs. The first-execution commands and timestamps are preserved in EXECUTION_RECORD.json. The runner refuses to overwrite an existing run result. For direct inspection use DERIVATION.md, DEVELOPMENT.json, VALIDATION_INPUTS.json and run/RESULTS.json together. The result manifest hashes every named path; its scope is stated in that file.
