# Neighboring speeds explain the core exchange

September 27, 2026. Baseline `af6d0d6f83cfcf3c15e2573ccedd8d023040384a`. This completes the 44/46 follow-up proposed in [ALL_CORE_SELECTION_2026_09_27.md](ALL_CORE_SELECTION_2026_09_27.md). Material AI involvement includes the calculations, implementations, structural argument, and writing.

**Outcome:** the stronger pair inequality and the replacement core both survive the neighboring controls. More usefully, the replacement is explained by a fixed containment of blocking sets. Its chosen tree is exact for every admissible variable speed, and a short analytic bound certifies the same core/window for all integer speeds at least 29. This is a certificate refinement for an already-studied family, not a newly covered family or a proof of general Lonely Runner.

Finite results below are OBSERVED / independently REPRODUCED within their stated scope. The all-parameter argument remains a HYPOTHESIS / proof candidate under [CLAIM_STATUS.md](../CLAIM_STATUS.md). No novelty or external correctness certification is claimed.

## Scope and completed plan

Keep eight common-start runners `{0,1,4,5,6,7,11,y}`, reference 0, threshold 1/8, with y=44,45,46. Compare core `{1,5,6}` and its replacement `{1,4,6}` on **all eight complete components of each core**, giving 48 component calculations. Retain equality points. These are three fixed inputs and one reference; the earlier all-reference/all-core experiment was not expanded or repeated.

For each component, calculate the maximum tree bound, the optimal lower bound from all single/pair durations, and the actual allowed set. Verify the optimum using a rational primal and dual. Independently reconstruct moments, states, components, and tree optima. Finally, explain which fixed interval relations account for the observed repair.

The optimal pair bound is a relaxation over arbitrary nonnegative Boolean-state masses. An artificial mass table is not automatically a constant-speed runner realization. In particular, an optimum of zero certifies a limit of positive-duration inference from those statistics; it does not assert that the physical allowed set is empty.

## The main comparison

Let `B_v={t: ||v t||<1/8}`. For the old core use its complete component

`I=[9/40,5/16]`, with residual speeds `{4,7,11,y}`.

For the new core use its complete component

`J=[9/32,5/16]`, with residual speeds `{5,7,11,y}`.

| y | Old-core best tree on I | Old-core optimal pair lower bound | Actual clear duration on I and J | New-core best tree on J |
| ---: | ---: | ---: | ---: | ---: |
| 44 | 1/308 | 1/112 | 1/112 | 1/112 |
| 45 | -1/1260 | 1/1260 | 1/210 | 1/210 |
| 46 | -3/5152 | 3/8096 | 1/184 | 1/184 |

At 44, the original core already has successful tree windows. At 45 and 46, none of its eight components has a positive tree bound; the signed-cycle inequality succeeds on I and its reflection in both cases. The replacement core certifies J and its reflection in all three cases. It does not make every other component successful or exact.

The complete global allowed sets, direct strict witnesses, and all local components are in the [exact archive](../reviews/2026-09-27-lr2/neighbor_cores.json). Their full-period clear durations are `29/1232`, `1/105`, and `67/4048`, respectively. All three also retain the four isolated odd-eighth times. The witness times `69/224`, `257/840`, and `57/184` lie in the selected positive components and are checked against all seven moving constraints.

## Why the replacement core makes the tree exact

The fixed six runners leave, inside either I or J, the same interval

\[
S=[17/56,5/16],\qquad |S|=1/112.
\]

Inside J the residual fixed runners have a particularly simple relation:

\[
B_5\cap J=\varnothing,\qquad
B_{11}\cap J\subseteq B_7\cap J.
\]

For duration calculations their nonempty intervals have endpoints

\[
B_{11}\cap J:\ [9/32,25/88],\qquad
B_7\cap J:\ [9/32,17/56].
\]

The blocking sets themselves use strict inequalities; the displayed interval endpoints specify their closures and lengths. Direct phase checks preserve boundary safety. Both inclusions are valid for the strict sets as well.

Consequently speed 5 adds no blocking on J, and speed 11 adds no blocking beyond speed 7. The four residual constraints reduce, for coverage on this window, to blockers 7 and y. Choose the fixed tree with edges `(5,7)`, `(7,11)`, `(7,y)`. If `D_v=|B_v intersect J|` and `O_uv=|B_u intersect B_v intersect J|`, its bound is

\[
\begin{aligned}
T_J(y)
&=|J|-D_5-D_7-D_{11}-D_y+O_{5,7}+O_{7,11}+O_{7,y}\\
&=|J|-D_7-D_y+O_{7,y}\\
&=U_J(y)=\frac1{112}-|B_y\cap S|.
\end{aligned}
\]

This is exact two-event inclusion-exclusion, not an approximation. No other tree can have a larger valid lower bound than the actual duration, so this fixed tree is a maximum tree for every admissible y. The optimal generic pair-data lower bound is also exact here: the tree attains the physical value, while the physical state masses are feasible for the relaxation.

The argument applies to every positive integer y distinct from the six fixed speeds. It does **not** claim U is positive for every such y. It explains the certificate and its precise scope. The three tested speeds produce the following actual portions of S:

| y | Variable blocking within S | Surviving part of S |
| ---: | --- | --- |
| 44 | Empty | [17/56,5/16] |
| 45 | From 37/120 to 5/16, with the threshold endpoint safe | [17/56,37/120] |
| 46 | From 17/56 to 113/368, with the threshold endpoint safe | [113/368,5/16] |

The movement of the surviving interval matters even when the same core and the same tree remain valid.

### A fixed successful certificate for the whole tail

For the 1/8 blocking threshold, use the continuous primitive

\[
A(z)=\frac{\lfloor z\rfloor}{4}
 +\min(\{z\},1/8)+\max(0,\{z\}-7/8).
\]

Its periodic correction `A(z)-z/4` is affine between fractional parts `0,1/8,7/8,1`, where its values are `0,3/32,-3/32,0`. Its range therefore has width `3/16`. Integrating on S gives

\[
|B_y\cap S|\le\frac{|S|}{4}+\frac{3}{16y},
\qquad
U_J(y)\ge\frac3{448}-\frac3{16y}>0\quad(y>28).
\]

Thus the same core `{1,4,6}`, the same complete opening J, and the same three tree edges certify a positive-duration opening for every integer y>=29. This is a supplied analytic argument, not an extrapolation from 44,45,46. The cutoff is sufficient and is not asserted sharp. It is a special-case selection rule, not a rule for arbitrary speed configurations or other references.

The earlier one- and two-variable work already treated this underlying family, including small equality controls. The gain here is an exact tree representation, a reason to select this component, and an elementary uniform tail bound. It does not create additional evidence of novelty or new Lonely Runner coverage.

## Why the old signed cycle loses different amounts

On I, write `A=B_4`, `B=B_7`, `C=B_11`, `D=B_y`, all restricted to I. Up to endpoints, the fixed intervals are

\[
A=[9/40,9/32],\quad
B=[15/56,17/56],\quad
C=[23/88,25/88].
\]

They obey

\[
A\cap B\subseteq C\subseteq A\cup B.
\]

The signed-cycle bound used in the preceding experiment is

\[
Q_I(y)=|I|-D_4-D_7-D_{11}-D_y
 +O_{4,11}+O_{7,11}+O_{4,y}+O_{7,y}-O_{11,y}.
\]

Its pointwise slack, compared with the true uncovered indicator, is nonzero only in four Boolean states. Two are impossible under the displayed fixed containments. The remaining slack is exactly the time when y and 11 block, while only one of 4 and 7 blocks. Define the two fixed intervals

\[
W=[23/88,15/56]\ \cup\ [9/32,25/88].
\]

Then, for every admissible y,

\[
U_I(y)-Q_I(y)=|B_y\cap W|,
\qquad
Q_I(y)=\frac1{112}-|B_y\cap S|-|B_y\cap W|.
\]

The exact endpoint conventions in W do not affect these duration identities. This identifies the location of the lost contribution rather than merely its total order of intersection.

| y | Blocking within the first part of W | Blocking within the second part of W | Total cycle slack |
| ---: | --- | --- | ---: |
| 44 | Empty | Empty | 0 |
| 45 | [19/72,15/56] in duration | Empty | 1/252 |
| 46 | [23/88,97/368] in duration | Entire interval [9/32,25/88] in duration | 41/8096 |

At 44 the cycle is exact. At 45 and 46 it remains positive but loses precisely the listed mass. It is nevertheless the optimal generic pair-data lower bound on I for all three tested inputs, as witnessed by the archived rational primal/dual certificates. Optimality is not asserted for all y; the duration identity and inequality validity have the general argument above.

This explains why the core exchange helps: it removes the residual role of speed 4, makes speed 5 harmless on the selected window, and replaces a three-set overlap relation by a direct containment `B_11 subset B_7`. The gap between the cycle lower bound and actual U disappears from this tree calculation.

## Pair information still fails on other openings

The repair is deliberately local. At y=44 and y=46, the original core's central components `[17/40,23/48]` and its reflection each contain actual clear duration `1/352`, but their optimal pair-only lower bound is zero. The replacement core's central components `[17/48,15/32]` and its reflection have the same issue. These give eight component-level positive-duration failures of generic pair inference across the two inputs and two cores.

For each such component, the archive contains an exact nonnegative state-mass table with the same single/pair moments and zero uncovered mass. This proves that strengthening the inequality alone, while keeping only those moments on that component, cannot certify positive duration. It does not produce a second physical runner configuration, rule out isolated equality in an abstract realization, or obstruct a successful certificate on another opening.

The neighboring controls therefore preserve all three distinct phenomena: tree inequalities can be too weak; pair data can be sufficient but leave a quantitative gap; and pair data can genuinely fail to certify positive duration in a particular region. The replacement succeeds by selecting a region with a simpler implication among blockers.

## Verification and preserved artifacts

The primary script partitions exact threshold events and computes all 16 state masses on each of 48 components. It enumerates all 16 residual trees and stores an exact rational primal/dual certificate for every pair optimum. Numerical optimization is used only to discover candidate certificates in `--write` mode. Read-only replay uses standard-library rational arithmetic.

The separate verifier imports neither the primary script nor the LP helper. It computes moments by intersections of blocking intervals, obtains states by Boolean inversion, reconstructs closed feasible sets from event vertices and cells, and obtains tree weights by Kruskal's algorithm. It checks all certificates, all direct witnesses, the conditional Boolean identities, and the primitive's affine-vertex range.

```bash
python -B reviews/2026-09-27-lr2/check_neighbor_cores.py --check
python -B reviews/2026-09-27-lr2/crosscheck_neighbor_cores.py --check
```

- [Primary script](../reviews/2026-09-27-lr2/check_neighbor_cores.py)
- [Exact calculations and 48 LP certificates](../reviews/2026-09-27-lr2/neighbor_cores.json)
- [Independent verifier](../reviews/2026-09-27-lr2/crosscheck_neighbor_cores.py)
- [Independent comparison record](../reviews/2026-09-27-lr2/neighbor_cores_crosscheck.json)

No existing checker or earlier experiment output was changed. The broader regression suite, earlier all-core enumeration, and full Ultra review were not rerun. This was a focused mathematical follow-up, with no new literature/frontier or novelty claim, outside contact, or main merge.

## Next question

Can the containment give an explicit selection criterion when fixed speed 11 is replaced by x? Keep core `{1,4,6}`, residual fixed speeds 5 and 7, and the same J. The needed condition is that x remains safe throughout S. For a single integer lap m this is

\[
m+1/8\le 17x/56,\qquad 5x/16\le m+7/8,
\]

equivalently

\[
\left\lceil5x/16-7/8\right\rceil
\le
\left\lfloor17x/56-1/8\right\rfloor.
\]

The width condition requires x<=84. The next proposed step is to verify this finite reduction and classify the admissible positive integer x, excluding repeated original speeds, then determine the resulting scope of the same fixed tree/window certificate. That classification has not been performed here. It would refine certificate selection for the earlier two-variable family, rather than silently claiming new family coverage. The +7/+9 extension remains parked.
