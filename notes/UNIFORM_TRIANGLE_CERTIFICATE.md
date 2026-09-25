# A triangle exclusion that survives unbounded speeds

September 25, 2026. Baseline: `59c00ff4e3dea25c0bfd4c47b8ea284dce753034`. **HYPOTHESIS/proof candidate:** the complete argument below awaits independent review. **OBSERVED:** the stated finite checks and controls. AI materially supplied the derivation, implementation, and writing. No novelty or general Lonely Runner result is claimed.

The previous [four-blocker comparison](FOUR_BLOCKER_CYCLE_CORRECTIONS.md) asked for a speed-derived bound on one cycle intersection without reconstructing the full schedule. For a structured part of the existing near-doubling family, that upper bound is exactly zero. The specific 56/64/113 exclusion extends to `q, q+8, 2q+1` for every admissible q. Six fixed affine strips then provide an exact, constant-size duration certificate.

## 1. Statement and scope

Consider eight common-start runners with distinct integer speeds

$$\{0,1,4,5,q,q+8,2q+1,v\},\qquad q\ge28,\quad v\ge q,$$

where v differs from q, q+8, and 2q+1. Select reference 0 and threshold `delta=1/8`, with equality valid. The proposed conclusion is **positive clear duration** in the prescribed core-safe window

$$J=[9/32,3/8],\qquad L=3/32.$$

There is no upper bound on v or requirement that `v-q` stay fixed. The certificate uses a fixed number of rational endpoint operations, independent of q and v. The integer bit complexity still grows with their sizes.

The earlier near-doubling argument covers arbitrary distinct u,v>=q for q>=242 using its refined one-pair bound; see [OVERLAP_PLACEMENT.md, Section 8](OVERLAP_PLACEMENT.md). Here we impose the additional relation u=q+8 and obtain a stronger local certificate starting at q=28. The broader q>=242 result is unchanged. This is a restricted certificate refinement, not a new general mechanism or an all-reference conclusion.

## 2. Why the triple is impossible

Put `A=q+8` and `B=2q+1`. If q blocks at time t, there is an integer j such that

$$x=qt-j,\qquad -1/8<x<1/8.$$

On J, `1/32<2x+t<5/8`. Thus if B also blocks, its nearby integer must be 2j and

$$-1/8<x<1/16-t/2.$$

Now the A phase relative to j is `x+8t`. The two inequalities imply

$$8t-1/8<x+8t<(15/2)t+1/16.$$

Across the whole window, the lower endpoint is at least 17/8 and the upper endpoint is at most 23/8. Hence

$$1/8<At-(j+2)<7/8.$$

Runner A is strictly safe. Therefore the triple intersection of q,A,B is empty, as is any four-way intersection containing that triple. The implication includes the window endpoints whenever the premise holds.

This depends on the particular offset. At q=56, replacing +8 by +7 gives triple duration `37/25312`; replacing it by +9 gives `13/25312`. Those controls disprove transferring this exclusion unchanged to neighboring offsets. They do not say +8 is the only offset with an exclusion.

## 3. Keep the triangle, leave the fourth runner separate

Let D_w be individual blocked duration in J and O_ab pair overlap duration. Since the triple q,A,B is empty, their exact union duration is

$$D_q+D_A+D_B-O_{qB}-O_{qA}-O_{AB}.$$

Adding the fourth blocker by the union bound gives

$$U_J\ge L-D_q-D_A-D_B-D_v+O_{qB}+O_{qA}+O_{AB}.\tag{1}$$

The graph is the triangle q,A,B with v isolated. It is globally cyclic but every active induced graph is a forest. No pair involving v needs to be computed. This is the earlier graph-count principle applied to a speed-proved exclusion.

For any positive w, the periodic primitive

$$C(z)=\frac{\lfloor z+1/8\rfloor}{4}
 +\min\bigl(\{z+1/8\},1/4\bigr)$$

gives `D_w=(C(3w/8)-C(9w/32))/w`. Its deviation from z/4 has range of width 3/16, yielding

$$\left|D_w-L/4\right|\le\frac3{16w}.$$

For every v>=q, (1) is consequently at least

$$H(q)=\frac{3L}{4}-D_q-D_A-D_B
 +O_{qB}+O_{qA}+O_{AB}-\frac3{16q}.\tag{2}$$

The finite and tail arguments below show H(q)>0 for every q>=28. When v is specified, using its exact D_v in (1) can improve the bound further.

## 4. Exact pair durations from six affine strips

For a pair w and `bw+r`, use `x=wt-j` in `(-1/8,1/8)`. The second blocker requires `bx+rt` to lie within 1/8 of an integer. The resulting vertical strips have affine lower and upper boundaries `ell(t),h(t)`.

| Pair | Anchor w | Time interval | Lower x boundary | Upper x boundary |
| --- | --- | --- | --- | --- |
| q,B | q | 9/32 to 3/8 | -1/8 | 1/16-t/2 |
| q,A | q | 11/32 to 3/8 | 23/8-8t | 1/8 |
| A,B | A | 9/32 to 7/24 | 15t/2-33/16 | 1/8 |
| A,B | A | 37/120 to 13/40 | -1/8 | 15t/2-39/16 |
| A,B | A | 13/40 to 41/120 | 15t/2-41/16 | 15t/2-39/16 |
| A,B | A | 41/120 to 43/120 | 15t/2-41/16 | 1/8 |

The last four rows use `B=2A-15`. Outside the listed intervals the corresponding pair has no blocking strip. The script independently reconstructs these six rows from the possible integer labels and line intersections; no q-dependent lap list supplies them.

Let

$$\Phi(z)=\frac{\{z\}(\{z\}-1)}2,\qquad -1/8\le\Phi(z)\le0.$$

For the affine line `f(t)=st+c`, define the endpoint term

$$E_w(f;[a,b])=
\frac{\Phi((w-s)b-c)-\Phi((w-s)a-c)}{w-s}.$$

The frequency w-s is positive for every row in the stated domain. The **exact actual-time** overlap on one strip is

$$\int_a^b(h(t)-\ell(t))\,dt
 +E_w(h;[a,b])-E_w(\ell;[a,b]).\tag{3}$$

To see this, the number of integers j with `ell(t)<wt-j<h(t)` equals `floor(wt-ell(t))-floor(wt-h(t))` away from boundaries. Expanding the floors gives the width plus a difference of fractional parts. The derivative of Phi is `{z}-1/2` away from integers, so integration gives (3). The strips have width less than one; their boundary exceptions have zero duration. Endpoint validity remains a separate matter.

The strip areas, before their exact endpoint corrections, are

$$I_{qB}=9/4096,\qquad I_{qA}=1/256,
\qquad I_{AB}=281/61440,$$

with total

$$I_{qB}+I_{qA}+I_{AB}=41/3840.$$

These areas alone are not actual overlap durations. Equation (3) accounts exactly for the actual shared-clock trajectory. It extends the endpoint technique already used for near-doubling pairs; no probabilistic independence or limiting equidistribution is assumed.

## 5. The unbounded tail and finite remainder

The range of Phi gives one endpoint-difference error at most `1/[8(w-s)]`. For the first two pairs,

$$|O_{qB}-I_{qB}|\le\frac1{8q}+\frac1{4B},\qquad
|O_{qA}-I_{qA}|\le\frac1{8q}+\frac1{8A}.$$

For A,B, merge adjacent contributions with the same affine boundary. The upper line `15t/2-39/16` extends from 37/120 to 41/120, and the lower line `15t/2-41/16` extends from 13/40 to 43/120. Together with the first A,B band this leaves three endpoint differences of frequency A and three of frequency B/2. Therefore

$$|O_{AB}-I_{AB}|\le\frac3{8A}+\frac3{4B}.$$

Combining the pair errors and the individual-duration allowances in (2) yields

$$H(q)\ge\frac{41}{3840}-\frac5{8q}
-\frac{11}{16(q+8)}-\frac{19}{16(2q+1)}
\ge\frac{41}{3840}-\frac{61}{32q}.\tag{4}$$

At q=179 the last expression is `19/687360>0`, and it increases with q. Thus all q>=179 are handled analytically, uniformly over the infinitely many admissible v>=q.

Exactly 151 remaining values q=28,...,178 have H(q)>0, using the six-band formula. The verification also evaluates the lower range q=6,...,27, omitting q=7 because A=B there. Across the resulting 172 q values, the only nonpositive H values occur at

`6, 8, 9, 11, 12, 13, 14, 15, 17, 20, 24, 27`.

At q=28,

$$H(28)=587/153216>0.$$

For comparison under the **same** individual-duration budget, retaining only O_qB gives `-11/2432`, and retaining the largest of the three fixed-pair overlaps gives `-163/51072`. The triangle therefore contributes more than simply fixing one formerly arbitrary speed.

The sufficient cutoff 28 belongs to this uniform certificate. A nonpositive H at q=27 or below is not a counterexample or a claim that every v fails. No claim is made that 28 is the smallest cutoff for actual local existence.

## 6. A control where every one-pair bound fails

Take q=27, v=43, giving extra speeds `{27,35,55,43}`. Using the exact fourth-runner duration gives:

| Quantity | Value |
| --- | ---: |
| Best of all six exact one-pair lower bounds | -1777/893970 |
| Excluded-triangle lower bound (1) | 2923/595980 |
| Actual clear duration in J | 31309/1787940 |

This demonstrates an actual certificate improvement even though the coarser uniform H(27) is negative. It does not establish failure of every tree certificate or of a different window.

For the original q=56, v=72 input, (1) gives `38471/3644928`, while its best exact one-pair bound is `1495/303744`. The previously studied best tree is stronger still. The value of (1) here is the compact unbounded construction, not optimality on this one input.

A failure control is retained: q=6, v=30 has negative triangle bound `-23/1820` but positive actual duration `3/560`. The excluded triangle alone does not force success at every parameter.

## 7. Evidence and next question

```bash
python -B reviews/2026-09-25-lr2/check_uniform_triangle.py --check
```

[Standalone verifier](../reviews/2026-09-25-lr2/check_uniform_triangle.py) and [exact archive](../reviews/2026-09-25-lr2/uniform_triangle.json). The script pins its own SHA-256 and imports no project modules.

- Six affine strips are reconstructed from residual integer labels and line intersections.
- For all 172 finite q values, a separately structured exact phase partition checks the three single durations, three pair durations, zero triple, and resulting three-runner union. These include the 151 q values used in the proof's finite remainder.
- Eight four-blocker controls check the triangle bound against actual duration: `(q,v)=(6,30),(27,43),(28,44),(28,29),(28,1000),(56,72),(178,194),(179,195)`.
- Two neighboring-offset controls retain positive triples. Three large formula examples, including v=`10^40`, exercise the certificate without a time partition.

The finite ranges and controls overlap and are not independent proof replications. The six-strip formula and the analytic tail justify the infinite parameter range; large examples do not. An additional session check with the existing `feasible_intervals` checker confirms all eight four-blocker durations. Its source SHA-256 is `ba240664c273d254d0ab8d2da053dc1248dd0b0a88cd5f1c4ed35a3f6c579971`. That additional check is separate from the standalone archived command. Existing research helpers and historical evidence were unchanged.

The method now has a concrete information-to-computation bridge: a shared-clock restriction keeps a useful cycle, and fixed residuals allow its pair weights to be evaluated without speed-dependent occurrence lists. The full general polyhedral model and an arbitrary-speed successful-window theorem remain unimplemented/open.

**Next useful question:** replace the special offset +8 by the adjacent +7 or +9 controls and retain their nonzero triple correction. Can the same finite affine-strip representation bound that correction and preserve useful slack for arbitrary v>=q? Compare with existing one-pair and tree bounds, and preserve genuine failures. This tests the quantitative mechanism beyond an exact exclusion instead of optimizing the present cutoff further.
