# Independent exact verification

Status: REPRODUCED/OBSERVED on the three frozen windows; internally generated
algebraic implications remain proof candidates. This is a separate AI-authored
implementation, not independent human mathematical certification.

`verify.py` imports no primary functions and uses no optimizer. It partitions
J=[9/32,3/8] at all four residual speeds' exact 1/8-distance threshold times,
classifies each open cell at a rational midpoint, and accumulates all 16 exact
state masses. It verifies core {1,4,5} safety throughout J by containing safe
laps. The diagnostic reconstructs only these three selected-reference windows:
9 cells for strict_16, 57 for doubling_112, and 8 for tight_13, totaling 74.
Threshold boundaries have zero measure and are handled separately when the
frozen policy requests the endpoint.

It reconstructs and checks all 12 individual lists, all 18 pair lists, their lap
labels and moment totals, the one selected triple list and third-runner phase
range, and the requested endpoint. For each of the 12 LP certificates it checks
the exact problem rows and objective against its own moment construction,
nonnegative primal feasibility, exact equality and inequality constraints,
dual sign and reduced-cost conditions, and equality of rational primal and
dual objective values. It also verifies protocol and primary-source hashes.
No floating result is accepted as a certificate. Operational intersection
comparison counters are not independently re-executed by this different
algorithm; its independent geometric cost is the 74-cell reconstruction.

## Cover obligations without optimizing

Let x_S denote the nonnegative mass of exact blocker state S. A zero pair
moment forces every x_S containing that pair to zero. Put

K = L − sum(single moments) + sum(pair moments).

For strict_16 the zero pairs are (6,7) and (7,16). They exclude all states of
size at least three except {6,11,16}; they also exclude the four-way state.
Writing t=x_{6,11,16}, inclusion-exclusion gives x_empty=K−t, with
K=1/896. Every exact pair and single state is then determined affinely by t.
Both endpoints t=0 and t=K give nonnegative states; hence the entire pair-moment
feasible region is t in [0,K]. Complete cover forces t=K, uniquely determining
the state masses. These masses are archived in `verification.json`; they
describe abstract measurable-event arrangements, not another runner example.

Thus every abstract complete-cover arrangement matching these moments must
spend exactly 1/896 in the triple {6,11,16}. The physical (6,11) overlap lies
in [31/88,17/48]. On it, 16t lies in [62/11,17/3], wholly away from an integer
by more than 1/8. The triple therefore has duration zero. The single geometric
fact excludes every compatible complete-cover distribution and yields the
exact physical empty mass 1/896. It is the known sparse exclusion, now selected
as an obligation of complete cover; its geometric content is not new.

For tight_13 the zero pairs (6,7) and (11,13) exclude every triple and the
four-way state. Here K=0. The pair moments already fix all exact-state masses
uniquely and match the physical reconstruction. All four complete-cover triple
minima are therefore zero, so the frozen rule requests no triple. The endpoint
3/8 is valid. Its containing safe-lap intersection is [3/8,3/8]: runner11
blocks an immediate left neighborhood, while runners5 and13 block an immediate
right neighborhood. This certifies an isolated equality point, not positive
duration. A measure-based complete-cover model says nothing about such
zero-measure valid points; here cover means almost-everywhere cover.

## Positive pair-only control and retained higher intersections

For doubling_112 the exact pair-moment optimum is 761/32256>0. One checked
dual lower bound is

L − sum(D_i) − P_(56,64) + P_(56,72) + P_(64,72)
  + P_(56,112) + P_(64,112).

The checker evaluates this dual inequality on all 16 logical states and
matches it with an exact feasible abstract distribution. The actual physical
empty mass is 53/1792, larger by 193/32256. Pair information is sufficient for
positivity but does not determine its exact duration. The frozen rule stops
before any higher-order query in this case. Its all-state reconstruction is a
post-selection diagnostic only.

The four physical inclusive triple moments, in masks 7,11,13,14 order, are
1/576, 1/512, 23/8064, 1/896, and the four-way moment is 1/896. In particular,
the strict16 zero-triple exclusion cannot be transplanted into this control.

## Reproduction and limits

```bash
python -B reviews/2026-09-28-cover-obligations/verify.py --check
```

This read-only command passes. The state and certificate records are in
`verification.json`; the primary script and result are separately authored.
This checks no new speeds, other windows, other references, broad families,
full-period loneliness, discovery complexity guarantee, or novelty claim.
All three controls were known before freezing this test. General selection
efficiency, usefulness when zero pair moments do not simplify the cover
polytope, and the need for joint rather than individual higher-order bounds
remain open.
