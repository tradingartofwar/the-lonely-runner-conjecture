# Independent exact verification

Status: OBSERVED/REPRODUCED for the frozen physical cases. This separate
AI-authored implementation is not independent human mathematical validation.

`verify.py` imports neither the primary implementation nor its LP helper. It
uses standard-library exact fractions, a threshold-event cell reconstruction,
and the verifier author's separately implemented two-phase Bland-rule simplex
from the preceding study. Inequality bounds become equality rows with
nonnegative slack variables. The simplex constructs its own exact primal and
dual vectors; feasibility and equality of their objectives are checked before
comparison with primary results. No floating optimizer is used.

## Scope and exact comparison

The reconstruction covers the target17 cells, its reflected17 cells,
strict16's9 cells, doubling112's57 cells, and tight13's8 cells:108 total. Core
safety is separately verified on the entire closed window. Threshold-point
distances are retained separately from positive-duration states.

The verifier solves exactly52 problems:16 target coordinate subsets,
16 strict16 subsets,16 tight13 subsets, one doubling112 baseline, and three
collective-H bounds. All52 optima agree with the primary and have independently
produced primal/dual certificates. This implementation performs883 exact
simplex pivots. All33 zero-optimum coordinate cases retain compatible abstract
complete-cover distributions; the primary's alternative countermodels are
also checked for all required moments, inequalities, nonnegativity, and U=0.

Subset ranking is explicitly checked using cardinality followed by the
lexicographic list of physical speed triples. Numeric mask order happens to
agree here because all residual speed lists are increasing; the physical
ranking is asserted rather than assumed.

## Target result

Let A=15, B=38, C=61, D=100 label the four residual blockers. The target is the
archived core{7,8,23} window[33/184,39/184]. Every single physical triple bound
still permits an abstract cover. Exactly two pairs are inclusion-minimal
successful subsets:

| Simultaneous physical bounds | Exact minimum U |
| --- | --- |
| T_ABC=0 and T_ABD=0 | 49/524400 |
| T_ACD<=1/48800 and T_BCD<=119/231800 | 13/22800 |

The first pair wins the frozen cardinality/lexicographic rule even though the
second yields a larger duration lower bound. All other pairs have minimum0.
The four three-coordinate subsets inherit the respective minimal-pair bounds.
All four coordinate bounds together give1/600, matching physical duration.
No coordinate subset's bound exceeds the physical value.

Write the pair-moment constant as K=L−sum D_i+sum P_ij. The two minimal-pair
dual certificates simplify to

- U >= K−P_CD−T_ABC−T_ABD;
- U >= K−P_AB−T_ACD−T_BCD.

These follow from U+H=K and the elementary containments
T_ACD+T_BCD−Q <= P_CD and T_ABC+T_ABD−Q <= P_AB. The respective left sides
measure the unions of two triple intersections sharing the indicated pair.
This also shows why simultaneous information is consequential: the required
overlap cannot be reassigned freely once both coordinate bounds apply.
The complete subset lattice and exact countermodels, rather than this
explanation alone, certify inclusion-minimality in the frozen four-bound set.

## Collective comparison, reflection, and controls

The identity U+H=K is checked on all16 logical states. For the target,
K=6121/2781600 and physical H=99/185440. The single supplied bound on H therefore
gives the exact1/600. It is one optimization input, but its present geometric
derivation uses all four triple durations and the four-way duration. This
verification does not supply a cheaper way to derive H or treat it as free.

The reflected interval[145/184,151/184] has the exact reversed reflected cell
sequence, identical state masses, and identical all-order moments. It receives
no duplicate LP search and is not a second independent configuration.

Strict16 recovers the already-known one-coordinate repair: its {6,11,16}
zero bound gives1/896. Doubling112 stops at the empty subset with positive
pair-only minimum761/32256. Every tight13 coordinate subset and its collective
bound has minimum0. Its endpoint3/8 is valid and isolated: exact distances are
safe, runner11 blocks immediately left, and runners5 and13 block immediately
right. No measure-based certificate converts that isolated equality into
positive duration.

The four canonical covers from the pinned prior symmetric abstract model
are checked read-only. Together they witness compatibility of every one of
its15 proper zero-triple subsets with a cover. This is an archived comparison,
not a fourth physical control or a new result. The physical target's two-bound
repair is therefore stronger than that abstract example's proper-subset
behavior; zero individual minima alone do not determine the needed joint
information.

## Reproduction and limits

```bash
python -B reviews/2026-09-28-joint-triple-exclusions/verify.py --check
```

The read-only replay checks source/protocol hashes, the primary source hash,
all independent optimization values, countermodels, reflection, and endpoint
semantics. Models with U=0 cover almost everywhere; they do not decide isolated
safe points. Countermodels are measurable-event distributions, not assertions
of another common-start runner realization. “Minimal” concerns only these four
fixed triple coordinates and physical bounds. No new speeds, windows, reference
choices, general selection guarantee, discovery-cost improvement, or novelty
claim is checked.
