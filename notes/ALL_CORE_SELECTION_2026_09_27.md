# All-core certificate selection — plan and exact experiment

September 27, 2026. Baseline `5c6e7dee3fd096101e5ce759b4a0c84838d0a932`. This follows the [Ultra review](ULTRA_REVIEW_2026_09_27.md) and its [team summary](ULTRA_REVIEW_SUMMARY_2026_09_27.md). Material AI involvement includes the experimental design, implementation, analysis, and writing. The general selection statement is a HYPOTHESIS; finite results have their explicitly stated scope.

## Question fixed before computation

For eight common-start runners and a selected reference having a **strict** lonely time at threshold 1/8, does some three-constraint core and one of its complete positive-length safe components admit a positive maximum-spanning-tree lower bound on the remaining four labelled constraints?

For a closed complete core component I, set

`B(I)=|I|-sum_i |B_i intersect I|+max_T sum_(i,j in T) |B_i intersect B_j intersect I|`.

The maximum is over all 16 trees on the four remaining runner labels. Strict blocking uses distance <1/8; equality is safe. A positive B certifies positive allowed duration. The sign of the maximum over every core/component is the tested outcome. This is a test of certificate content and placement, not a proposed fast selector.

## Plan

1. Use eleven existing controls: extras 6/7/11 with y=16,13,45,90,266,532; extras 56/64/72 with y=112,113; the local-contact family with y=1680,3360; and consecutive speeds 0 through 7. The first two groups retain core 1/4/5 only as their historical naming convention, not as a restriction of the new search.
2. For every configuration, examine all eight references and all 35 choices of three **labelled** nonreference runners. Use absolute relative speeds for the distance constraints while preserving duplicate labels and the original threshold. Do not treat deduplication as a smaller runner count.
3. Construct every closed core-safe component in [0,1], including singleton components. Evaluate the best tree bound and actual clear duration on each. Archive per-core counts, extrema, a maximizing component, and a digest of all component calculations; retain full details of each reference's strongest certificate and a direct global witness.
4. Reconstruct the complete enumeration by a separately structured threshold-event sweep, accumulating all 16 residual blocking-state masses. Compare every component digest, count, and extremum. Check the best certificates and all global witnesses directly against the original velocities.
5. If a strict reference defeats every tree certificate, use the exact pair-moment relaxation on that failed case to distinguish tree insufficiency from pair-information insufficiency. Equality-only references are controls, not counterexamples to the strict hypothesis.
6. State the bounded outcome and choose the next structural question. Passing this list cannot establish the universal hypothesis. An exact strict failure disproves it within its stated scope.

The computation is limited to these eleven configurations; no new speed-box scan or arbitrary parameter expansion is authorized by this plan. The +7/+9 extension remains parked.

## Implementation and reproduction

The primary script is [check_core_selection.py](../reviews/2026-09-27-lr2/check_core_selection.py). It uses integer ticks on the exact common grid `1/(8*lcm(relative speeds))`, closed interval intersections for core openings, and prefix integrals of individual and pair blocking intervals. It imports no project analysis code. All prescribed relative vectors have gcd 1, checked explicitly; time remains the original [0,1] period.

```bash
python -B reviews/2026-09-27-lr2/check_core_selection.py --write
python -B reviews/2026-09-27-lr2/check_core_selection.py --check
```

The independent script [crosscheck_core_selection.py](../reviews/2026-09-27-lr2/crosscheck_core_selection.py) imports neither the first script nor the project checker. It sweeps exact threshold events on a different product-denominator grid, accumulates the 16 residual-state masses in each core component, and uses Kruskal's algorithm instead of enumerating all 16 trees. It reconstructs every component and all full allowed sets, including equality points. Direct signed-velocity substitution checks every supplied witness. Its [comparison record](../reviews/2026-09-27-lr2/core_selection_crosscheck.json) pins the eleven input archives.

```bash
python -B reviews/2026-09-27-lr2/crosscheck_core_selection.py --check
python -B reviews/2026-09-27-lr2/check_core_selection_repair.py --check
```

## Completed outcome

**Every strict reference in the prescribed domain has a positive tree certificate somewhere.** There is no counterexample to the proposed existence-of-a-core hypothesis in this experiment.

The exact enumeration covers eleven configurations, 88 reference cases, 3,080 labelled core choices, and 778,145 complete core components. The second implementation matches every component digest, count, and extremum. These counts overlap heavily and include reflection symmetries and duplicate absolute constraints; they are not independent samples or discoveries.

- 85 reference cases have positive lonely duration. Of these, 50 have seven distinct absolute relative speeds; 35 have repeated absolute constraints. All 85 have strict witnesses and successful cores.
- Among their 2,975 labelled cores, **2,974** have a positive tree certificate in some complete opening. The one failure is core `{1,5,6}`, reference 0, in `{0,1,4,5,6,7,11,45}`.
- Three reference cases have only isolated equality points: reference 0 in `{0,1,4,5,6,7,11,13}`, and references 0 and 7 in `{0,1,2,3,4,5,6,7}`. Each has allowed set `{1/8,3/8,5/8,7/8}`. Their 105 core choices have no positive tree bound, as required by zero true duration. They are not failures of the strict hypothesis.
- Across all cases, 380,463 core components have positive tree bounds. The full enumeration is an exact benchmark, not a bounded-complexity selection algorithm independent of speeds.

| Original configuration, beyond reference 0 | Strict references out of 8 | Successful core choices among strict references | Best core at reference 0 | Best bound at reference 0 |
| --- | ---: | ---: | --- | --- |
| 1,4,5,6,7,11,16 | 8 | 280/280 | 1,5,7 | 1/176 |
| 1,4,5,6,7,11,13 | 7 | 245/245 | 1,4,5 | 0; equality-only reference |
| 1,4,5,6,7,11,45 | 8 | 279/280 | 1,4,6 | 1/210 |
| 1,4,5,6,7,11,90 | 8 | 280/280 | 1,4,6 | 31/5040 |
| 1,4,5,6,7,11,266 | 8 | 280/280 | 1,4,6 | 13/2128 |
| 1,4,5,6,7,11,532 | 8 | 280/280 | 1,4,6 | 1/152 |
| 1,4,5,56,64,72,112 | 8 | 280/280 | 1,4,5 | 761/32256 |
| 1,4,5,56,64,72,113 | 8 | 280/280 | 1,4,5 | 58073/3644928 |
| 1,3,4,5,10,28,1680 | 8 | 280/280 | 1,3,5 | 15/448 |
| 1,3,4,5,10,28,3360 | 8 | 280/280 | 1,3,5 | 15/448 |
| 1,2,3,4,5,6,7 | 6 | 210/210 | 1,2,3 | 0; equality-only reference |

Every row is one named configuration, not an unbounded family. The displayed bounds maximize unnormalized duration over individual complete components. A larger bound does not necessarily imply a faster selector, a larger separation margin, or recovery of the full allowed duration.

## The one failed core isolates two different repairs

For `{0,1,4,5,6,7,11,45}` at reference 0, select core `{1,5,6}`. The residual blockers are `{4,7,11,45}`. All eight complete core openings are listed below. No tree bound is positive, although two openings contain strict lonely time.

| Complete core component | Best tree bound | Actual clear duration |
| --- | ---: | ---: |
| [1/8,7/48] | 0 | 0 |
| [9/40,5/16] | -1/1260 | 1/210 |
| [17/48,3/8] | 0 | 0 |
| [17/40,23/48] | 0 | 0 |
| [25/48,23/40] | 0 | 0 |
| [5/8,31/48] | 0 | 0 |
| [11/16,31/40] | -1/1260 | 1/210 |
| [41/48,7/8] | 0 | 0 |

This is an exact counterexample to the stronger statement **every core has a successful tree window whenever strict loneliness exists**. It does not refute the tested statement that *some* core succeeds.

### Repair 1: change one core runner

Replace core speed 5 by 4. The complete core component `[9/32,5/16]` now has residual speeds `{5,7,11,45}`. Speed 5 is safe throughout this component. The best tree lower bound is exactly `1/210`, equal to the actual duration there. One strict witness is `257/840`; direct substitution checks all seven constraints.

This demonstrates the practical effect of core selection without introducing higher moments. The component is narrower, and the useful pair intersections are represented by a tree. The archive retains all durations, chosen edges, and witness distances.

### Repair 2: retain the core and use more of the same pair data

The planned all-core failure did not occur, so a global LP failure investigation was unnecessary. The sole core failure did leave a concrete question: were its pair statistics insufficient, or was the tree inequality insufficient? A targeted exact LP calculation resolves it.

On `I=[9/40,5/16]`, write `D_v=|B_v intersect I|` and `O_uv=|B_u intersect B_v intersect I|`. The inequality

\[
\begin{aligned}
U_I\ge{}&|I|-D_4-D_7-D_{11}-D_{45}\\
&+O_{4,11}+O_{7,11}+O_{4,45}+O_{7,45}-O_{11,45}
=\frac1{1260}>0
\end{aligned}
\]

uses exactly the same singles and pairs available to the trees. Its four positive pair terms form a cycle, with one subtracted diagonal term. The same calculation holds on the reflected component `[11/16,31/40]`.

The new standalone [repair verifier](../reviews/2026-09-27-lr2/check_core_selection_repair.py) checks the pointwise inequality on all 16 Boolean blocking states. It then evaluates the physical moments exactly. A nonnegative rational 16-state mass table matches every retained moment and attains `1/1260`, certifying that this is the **optimal generic pair-data lower bound** on this component. The artificial optimum is not asserted to be another runner realization. The physical clear duration is larger, `1/210`.

The optimum was first found using the existing Ultra LP helper with the new window; the preserved replay uses only standard-library rational arithmetic and the explicit primal/dual certificates. It does not require SciPy or trust a numerical answer. [The repair archive](../reviews/2026-09-27-lr2/core_selection_repair.json) includes all eight windows, full actual state masses, the two primal/dual checks, and the changed-core certificate.

Consequently, **every one of the 2,975 strict-case core choices has some complete component with a positive certificate using only single and pair durations**: 2,974 are certified by trees, and the remaining one by the signed cycle inequality. This is a stronger bounded observation, not a universal every-core theorem.

## The distinction this experiment adds

Three failures must now be kept separate:

1. **Placement:** the chosen component can be unhelpful even when another component works.
2. **Inequality strength:** the available statistics can already certify success, while a selected family of inequalities fails to extract it.
3. **Information loss:** even the optimal consequence of the retained statistics may fail to determine or certify the target, requiring additional information or a different region.

The failed `{1,5,6}` core demonstrates the second failure. The earlier `{1,4,5}` / `{6,7,11,16}` fixed-window example demonstrates a genuine pair-data limitation in that particular window. Neither local failure implies that all cores or all windows fail for the full configuration.

This also sharpens the distinction between **certifying positive duration** and **recovering its exact value**. The repaired lower bound is only one sixth of the actual duration and is sufficient for the existential task. We do not need a full reconstruction to certify a witness exists.

## Next decision

The original some-core tree hypothesis survives these controls. The stronger every-core tree hypothesis is disproven by the explicit speed-45 core. The stronger every-core pair-certificate hypothesis survives this finite domain after the repair. None is established universally.

The next proposed investigation is a focused stability and structural test around this exception: change the exceptional speed from 45 to 44 and 46, keep reference 0 and threshold 1/8, and compare the failed core, its one-runner replacement, and the optimal pair bound. These two neighboring configurations have **not** been checked here. The purpose is to determine which geometric relation makes the repair work and whether it persists, before considering a wider search or an unbounded statement. If a chosen core defeats all pair certificates, check the other cores before interpreting it as a global obstruction.

The experiment has not produced a general rule forcing a useful certificate for arbitrary speeds. The controls were selected from our existing research, not sampled representatively. Their success is reason to investigate a structural selection or inequality argument, not evidence that the missing universal step is small.

No existing checker or research analysis implementation was changed. The broader regression suite and the whole Ultra package were not rerun. There was no new literature/novelty claim, outside contact, or main-branch merge. The original dated Ultra reports and their evidence remain intact.
