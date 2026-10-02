# Exact value of retained moments and support restrictions

September 27, 2026. Reviewer: AI optimization review requested as part of the six-reviewer audit. Baseline: `e94a87f650264826569cae63412c43a5175f5ae4`. Material AI involvement: formulation, calculation, certificate generation, and writing.

**Status:** the ten prescribed examples and their rational optimization certificates are **OBSERVED** bounded results. The elementary reductions below are explicit general arguments about event measures, offered for independent review; they do not establish a new runner family or the full conjecture. No novelty claim or literature priority claim is made.

The principal finding is that **logical support information sometimes closes the entire duration gap and sometimes has no value at all**. The 16 example needs only one excluded triple. The 266/532 examples have identical full positive support, and every physically justified nonempty-state zero leaves the pair relaxation unchanged. Their missing information is quantitative. Separately, optimal pair inequalities can already outperform the best positive-edge tree certificate: this occurs at 56/64/72/113.

## 1. The precise optimization and its certificate

Use eight total runners, common starts, reference 0, threshold 1/8, core 1/4/5, and `J=[9/32,3/8]`, of length `L=3/32`. The four extras are listed in the order recorded in the archive. For each subset `S` of the four extras, let `x_S` be the duration on which exactly that subset strictly blocks. The sixteen variables satisfy

\[
x_S\ge0,\qquad \sum_Sx_S=L,\qquad
\sum_{S\ni i}x_S=D_i,\qquad
\sum_{S\supseteq\{i,j\}}x_S=O_{ij}.
\]

Minimize `x_empty`; also maximize it to expose the complete uncertainty interval. This is an **abstract event-measure relaxation**, not optimization over physical integer speeds. A feasible artificial distribution need not have a common-start runner realization. It bounds what follows from only the retained equalities and support exclusions.

A zero triple forbids every state containing its three labels. A Boolean implication `A => B` forbids the states violating it, so this formulation directly accommodates implications without another class of variables. The strongest tested support model sets `x_S=0` for every physically absent **nonempty** exact state. It deliberately never inserts `x_empty=0` from the answer being sought. All exclusions are proved for these inputs by exact phase intervals; none is inferred from floating point samples.

For a minimization with allowed columns A, the archived rational vectors satisfy

\[
Ax=b,\quad x\ge0,\quad A^Ty\le c,\quad b^Ty=c^Tx.
\]

These equalities and inequalities prove optimality directly by multiplication and summation. Maximization uses `c=-e_empty`. The verifier checks every entry with `Fraction`; it does not invoke an optimizer. SciPy is used only by `--write` to find candidate bases and dual coefficients. Rational row reduction recovers primals, and exact inequalities reject any faulty rationalized dual. Every reported endpoint has both certificates, including the zero endpoints.

## 2. Exact results

“Support minimum” retains all pair moments and every actual nonempty-state zero. “Triple-sum minimum” instead retains pair moments and the single number `sum T_ijk`. Complete moments recover the actual duration in every row.

| Extra speeds | Pair-only feasible U interval | Support minimum | Triple-sum minimum | Actual U |
| --- | --- | --- | --- | --- |
| 6,7,11,16 | [0, 1/896] | 1/896 | 1/896 | 1/896 |
| 6,7,11,13 | [0, 0] | 0 | 0 | 0 |
| 6,7,11,45 | [157/110880, 31/5040] | 59/13860 | 1/210 | 1/210 |
| 6,7,11,90 | [157/110880, 31/5040] | 31/5040 | 31/5040 | 31/5040 |
| 6,7,11,266 | [457/140448, 17/2128] | 457/140448 | 13/2128 | 13/2128 |
| 6,7,11,532 | [457/140448, 17/2128] | 457/140448 | 1/152 | 1/152 |
| 56,64,72,113 | [63239/3644928, 95621/3644928] | 72311/3644928 | 6193/260352 | 6193/260352 |
| 56,64,72,112 | [761/32256, 1165/32256] | 761/32256 | 51/1792 | 53/1792 |
| 3,10,28,1680 | [0, 0] | 0 | 0 | 0 |
| 3,10,28,3360 | [0, 0] | 0 | 0 | 0 |

For these ten controls, adding every absent nonempty state gives exactly the same minimum as adding only all absent triples. This is a bounded observation, not a general redundancy theorem. All individual triple/quadruple retention experiments and individual zero-triple experiments are also archived; no speed scan was performed.

## 3. Why two numbers describe the 6/7 cases

Here `B6` and `B7` are disjoint, already visible in `O6,7=0`. Write the labels as `a=6,b=7,c=11,d=y` and

\[
C=L-\sum_iD_i+\sum_{i<j}O_{ij},\qquad
\alpha=T_{acd},\quad\beta=T_{bcd}.
\]

Every possible state mass follows from the pairs and these two numbers:

| Exact state | Mass |
| --- | --- |
| empty | C-alpha-beta |
| a / b | D_a-O_ac-O_ad+alpha / D_b-O_bc-O_bd+beta |
| c | D_c-O_ac-O_bc-O_cd+alpha+beta |
| d | D_d-O_ad-O_bd-O_cd+alpha+beta |
| ac / ad | O_ac-alpha / O_ad-alpha |
| bc / bd | O_bc-beta / O_bd-beta |
| cd | O_cd-alpha-beta |
| acd / bcd | alpha / beta |
| any state containing a and b | 0 |

Consequently define

\[
\ell_a=\max(0,O_{ac}+O_{ad}-D_a),\quad u_a=\min(O_{ac},O_{ad}),
\]
\[
\ell_b=\max(0,O_{bc}+O_{bd}-D_b),\quad u_b=\min(O_{bc},O_{bd}),
\]
\[
\ell_H=\max(\ell_a+\ell_b,
 O_{ac}+O_{bc}+O_{cd}-D_c,
 O_{ad}+O_{bd}+O_{cd}-D_d),
\]
\[
u_H=\min(u_a+u_b,O_{cd},C).
\]

For feasible data, all sums `H=alpha+beta` between `ell_H` and `u_H` occur in this abstract model: sums of the two feasible coordinate intervals fill an interval, and the remaining restrictions concern only H. Thus the exact pair-only range is

\[
\boxed{C-u_H\ \le U\le\ C-\ell_H.}
\]

The verifier independently evaluates this formula on all six applicable rows and checks both LP endpoints. It also explains why the single retained scalar H completely recovers U, whereas retaining either triple separately need not do so. This is the precise value of the aggregate correction already proposed in the residue-collision note; it is not a new physical statistic.

### The old 16 control

Here `C=1/896`, and `O7,16=0` already forces beta=0. The abstract pair model allows alpha=C and U=0. A particularly transparent primal is obtained from the actual distribution by putting `d=1/896` into state `{6,11,16}`, adding d to each corresponding singleton, subtracting d from each corresponding pair-only state, and subtracting d from the empty state. All masses remain nonnegative; every singleton and pair moment is unchanged. The archived minimizer records this exact alternative.

The speed-derived exclusion `T6,11,16=0` alone removes that freedom, forcing U=C. The other three zero-triple constraints individually do not improve the lower bound. Therefore the full value of the missing support information in this case is exactly **1/896**, supplied by one particular exclusion. The zero-clear distribution remains abstract and is not presented as another physical speed configuration.

### The physical matching pairs

For 45/90, pair moments already imply positive U in both inputs; their failure is exact duration recovery. At y=45, only `T7,11,45=0` adds useful support information. It raises the lower endpoint by **1/352**, from 157/110880 to 59/13860, but a gap of **1/1980** remains below actual U=1/210. Measuring `T6,11,45=1/720` in addition to that exclusion removes the gap. At y=90 both relevant triples vanish, so the same style of support information determines U exactly.

For 266 and 532, every one of the twelve states avoiding the pair `{6,7}` has positive duration. Their actual positive supports are identical, and their support zeros are already forced by the pair data. No further true Boolean implication on these four instantaneous blocking indicators can exclude any positive-duration state. Thus all such implications together have **zero additional value** for the lower bound. The actual values differ, so even preserving the full support together with the pair moments cannot determine U within these physical controls. The scalar H takes values 1/532 and 3/2128, respectively, and recovers their different U values.

Requiring positive mass, without a numerical lower bound, on each physically possible state also cannot improve the infimum: mix any support-feasible optimizer with an arbitrarily small positive amount of the actual distribution. All required states become positive while the objective approaches the same bound. Quantified support mass would be additional information.

## 4. A limitation of the tree comparison itself

The 56/64/72/113 control has an exact pair-only optimum

\[
63239/3644928,
\]

which exceeds the earlier best tree `58073/3644928` by `5166/3644928`. Its dual is the valid signed-pair inequality

\[
U\ge L-\sum D_i
+O_{56,64}+O_{56,72}+O_{64,113}+O_{72,113}
-O_{56,113}.
\]

One elementary derivation starts with the four-cycle correction `U >= L-sum D+sum_cycle O-Q` and uses `Q<=O56,113`. The archived dual independently checks the associated pointwise inequality on all sixteen states. This demonstrates that failure of the best tree is not automatically failure of every pair-only inequality. The negative diagonal coefficient matters; the tree comparison searches a narrower certificate class.

The independently justified exclusion `T56,64,113=0` makes Q zero and eliminates the diagonal penalty. The lower bound becomes `72311/3644928`, exactly the earlier compatibility/four-cycle result. Retaining only `Q=0` produces the same optimum here. All additional actual support zeros provide no further gain.

The aggregate triple duration alone supplies an exact **lower certificate** in the 113 case, because inclusion-exclusion gives `U=C-sum T+Q` and Q is nonnegative. It does not determine U: the resulting maximum is `355727/14579712`, above actual U. In the 112 control, actual `Q=1/896`, so the same triple-sum lower bound misses actual U by exactly 1/896. Retaining Q as well closes this gap. These controls distinguish obtaining a sufficient lower bound from recovering the complete target value.

## 5. Zero duration is already settled before higher moments

For tight 6/7/11/13, pair data already force U=0. Additional triple information cannot improve that duration conclusion; the actual contact `{3/8}` requires the separate pointwise check.

For the new 3/10/28/1680 and 3/10/28/3360 controls, even the fixed first three runners have the second-order upper bound

\[
U\le L-D_3-D_{10}-D_{28}+O_{3,10}+O_{3,28}+O_{10,28}=0.
\]

Together with nonnegativity this forces zero duration using only fixed-runner pair data. The independent phase-event check gives `{9/32}` for 1680 and the empty set for 3360, while all sixteen moment values and exact-state durations match. Consequently **optimizing higher duration moments is already exhausted for this distinction**. A contact supplement must provide pointwise information, directly or through an arithmetic rule known to determine it. The LP has neither established nor contradicted existence at its zero optimum.

## 6. Reproduction, limits, and useful next step

Run the standard-library certificate replay:

```bash
python -B reviews/2026-09-27-ultra/optimization_check.py --check
```

It verifies **244 rational primal/dual certificates** over ten prescribed physical inputs; recomputes every physical moment by an exact threshold partition and a separately structured blocking-interval intersection; checks the analytic disjoint-pair formula; checks the physical matching summaries; and checks the zero-duration contact sets. The JSON pins the script SHA-256. Regeneration with `--write` uses SciPy, but solver status or floating objective values are never the certificate. No preexisting files were changed.

This investigation does not optimize over physical realizations, prove a speed-independent cost bound, select windows, or find contacts efficiently. Enumerating actual support here costs work proportional to the finite speed schedules; it is diagnostic evidence, not a uniformly bounded support oracle. The concrete zero-triple exclusions already have short speed-based derivations in the earlier notes; the complete support check adds no claim of a short general derivation.

A focused next representation test would compare a proposed cheap constraint generator against this exact 16-state benchmark, measuring the gain from each genuinely derived restriction. Pair-only signed inequalities should be included in the baseline before attributing a gap to missing geometry. The 16, 45/90, 266/532, and 1680/3360 controls distinguish four tasks: one forbidden overlap, quantitative overlap allocation, zero-duration contact recovery, and information that is already sufficient for the requested duration bound. None calls for another broad speed scan.
