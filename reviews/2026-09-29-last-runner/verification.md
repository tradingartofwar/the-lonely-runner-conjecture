# Independent last-runner verification

Date: 2026-09-29. Parent: f3c26e709fa1cd8945968dcd585bd012430c7243.

**OBSERVED:** every declared mathematical output from the frozen protocol
agrees between two separately structured exact implementations. There are
**3,162 numerical leaf fields**, 1,324 Boolean fields, three text fields,
and one null field, with **zero disagreements**. These are data-field
counts, not independent mathematical replications or proof certifications.

The general event-reduction argument remains a **HYPOTHESIS / proof
candidate** pending external review. Its finite calculations do not certify
unexamined cores or arbitrary phases.

## Freeze and independence

Root approved the immutable protocol with SHA-256

`660a3a7f27f6a1e7b2c0c68aeea22b42366c7a946d5612e967c6f355999d5aae`.

The verifier first wrote `verifier_plan.md`. The primary shared only output
schema, not source or mathematical results. The verifier then wrote and ran
its own source, froze its output, and recorded `INDEPENDENT_FREEZE.json`
before obtaining access to the primary output. The frozen hashes are:

- Source: `4c7993b518b5ca29abdf9a04fd7eb1e9f51d0c2588277c4406d148f2adb11d8c`.
- Output: `c949dc0e57b54927a85dff49e4ab386e5f10ebf6b0bd41904eb552dd291dec44`.

The comparison script verifies these hashes before comparing every field
under `records`, including all per-component and prefix bands. No primary
generator is imported or executed by the independent verifier.

## Method and exact finite scope

The core is reconstructed from rational threshold events, direct modular
predicates at every event, and predicates on every open time-cell midpoint.
All surviving cells and points are merged into maximal closed components.
This retains isolated core points.

For final phase theta in the declared set {0,1/2}, the speed events are all
values `(m+1/8-theta)/s` and `(m-1/8-theta)/s` in the bounded speed domain,
where s is a core endpoint or isolated point. The verifier reconstructs the
full seven-constraint safe time set directly at each contact and at one
rational midpoint of each intervening speed cell. Per-component and prefix
classifications then follow by intersecting these final safe sets with the
independently reconstructed core intervals.

The run evaluates 799 speed contacts and 799 open speed cells. It also
performs exactly the four old diagnostic reconstructions at d=13,16,112,113
with phase0. Across these 1,602 final time reconstructions it checks 203,603
time events and 202,001 open time cells. Core reconstruction separately
checks 542 events and 539 cells. No additional input core, physical final
speed diagnostic, phase, or reference is introduced.

## Outcomes

Here F means all closed components, including isolated points, are strictly
blocked. P ignores isolated core points but strictly blocks every positive
closed component. Z means zero positive final safe duration, allowing
closed-block endpoint contacts. All sets below are restricted to the frozen
domain `(max(core),1/(4w)]`, where w is the largest core component width.

| Core residual triple | Phase | F | P | Z |
| --- | --- | --- | --- | --- |
| (6,7,11) | 0 | empty | (220/17,196/15) | [220/17,196/15] |
| (6,7,11) | 1/2 | empty | empty | {18} |
| (3,7,24) | 0 | empty | empty | empty |
| (3,7,24) | 1/2 | empty | empty | empty |
| (56,64,72) | 0 or 1/2 | empty domain | empty domain | empty domain |

Every core also contains speeds1,4,5. The first speed domain is `(11,28]`;
the second is `(24,112/3]`. The third has width5/504 and cap126/5<72, so the
domain is empty by width before any final-speed event calculation.

The common-start integer P and Z sets for the tight core are both {13};
F is empty. For phase1/2, the only integer Z value is18. The narrow core
has no F, P, or Z integer member at either phase. For speeds greater than
the cap, positive final duration follows analytically from the strict
width comparison, for every phase; this is not an extra speed scan.

The designated old diagnostics reproduce:

- d=13: exactly the four isolated witnesses1/8,3/8,5/8,7/8; duration0.
- d=16: four positive components; total duration39/4928.
- d=112:54 positive components; total duration53/448.
- d=113:50 positive components; total duration214673/2278080.

The full component endpoints are retained in both result files. In
particular, the phase0 P interval shows exactly why omitting isolated core
points would change the existence conclusion around the old tight case.
The auxiliary phase1/2 singleton Z={18} separately exhibits zero duration
without strict coverage of all positive closed components.

## Reproduction

From the repository root:

```bash
python reviews/2026-09-29-last-runner/independent_last_runner.py
python reviews/2026-09-29-last-runner/compare_last_runner.py
```

The original freeze precedes primary access; rerunning after comparison
reproduces that deterministic calculation but is not a new independent
freeze. `comparison_last_runner.json` records the exact source and result
hashes, counts, and zero-disagreement result. No claim of novelty or general
Lonely Runner proof follows from this bounded verification.
