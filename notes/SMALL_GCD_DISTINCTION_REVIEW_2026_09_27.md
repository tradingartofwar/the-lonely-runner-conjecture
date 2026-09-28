# The 56/113 question: what is resolved and what remains

September 27, 2026, Pacific. Review baseline `c02b2161db2d0462a54af0192c888221230ef1a9`. Vance added this investigation to the research priorities after the phase-projection round. The coordinator and three AI collaborators traced the existing arguments, checked exact arithmetic, and reviewed counterexamples. This is a continuity and distinction audit, not a new speed search or a novelty claim.

**Finding:** the specific 56/113 explanatory gap was already closed in [OVERLAP_PLACEMENT.md](OVERLAP_PLACEMENT.md). The decisive repair keeps both actual local blocking concentration and overlap located by the relation `113−2·56=1`. Higher-order information yields stronger certificates but is not needed to prove an opening in this input. Existing proof candidates already extend beyond large gcd. The unresolved target is selecting and forcing useful structure under more general speed assumptions.

## The research brief preserved

Review [LOCAL_OVERLAP.md](LOCAL_OVERLAP.md), [SPEED_RATIOS.md](SPEED_RATIOS.md), and the exact 56/113 control. Treat the failed coarse bound as information. Ask which consequential distinctions it discards: overlap placement inside useful openings, phase alignment, distribution across subintervals, higher-order overlap with other runners, or another configuration-level constraint.

Seek the smallest useful higher-resolution representation, and test it against existing tight cases and controls. A proposed explanation should be formulated from the speeds and assumptions independently of the already-known final allowed set. Determine whether it gives a sharper local bound or a rigorous obstruction to complete blocking, particularly at small gcd.

Do not launch a broad speed search. Use exact arithmetic and existing cases first; preserve counterexamples and distinguish observations, proof candidates, known source results, and established proofs. The larger objective is to extend restricted infinite-family arguments toward a more general explanation of why collective blocking fails.

This review resolves where that request sits in the current record. The existing next task—residue classification of the two fixed time templates—is retained. The remaining small-gcd selection question is added as a related priority, without restarting completed calculations or automatically un-parking the +7/+9 extension.

## 1. The precise compression that fails

There are eight common-start runners, reference 0, and threshold 1/8. The fixed core `{1,4,5}` is safe throughout

\[
J=[9/32,3/8],\qquad L=3/32.
\]

The four remaining speeds are `{56,113,64,72}`. The old bound uses the selected pair's whole-cycle overlap fraction, its repetition period, and separate worst-case partial-period allowances. Its result is `−755/3072`, which is inconclusive.

It is important to identify the actual loss. A full reduced ratio and its gcd reconstruct both speeds, so that pair of arithmetic data does not itself discard their schedule. The bound subsequently replaces the detailed schedule by a few scalar features and phase-independent error allowances. That replacement forgets how J's endpoints meet each runner's blocking pattern and how the selected pair's phases are coupled inside J.

For speed w let D_w be its actual blocking duration in J. Put `T=sum D_w`, `E=T−L`, and let O be the selected pair's local overlap. Grouping that pair before the union bound gives

\[
U_J\ge L-T+O=O-E.
\]

For the input in question,

\[
(D_{56},D_{113},D_{64},D_{72})
=(11/448,11/452,3/128,13/576),\qquad
E=1045/911232.
\]

Each D comes from a cumulative blocking primitive at the two endpoints, rather than from the complete four-blocker intersection. With `m=floor(z)` and `r={z}`, one such primitive is

\[
C(z)=m/4+\min(r,1/8)+\max(0,r-7/8),\qquad
D_w=[C(3w/8)-C(9w/32)]/w.
\]

The pair overlap comes from the shared-clock identity. Near a q=56 meeting, write `x=56t−j`; then `113t−2j=2x+t`. On J the only relevant second lap label is 2j. Simultaneous blocking therefore occurs on the six intervals

\[
\left(\frac{j-1/8}{56},\frac{2j+1/8}{113}\right),
\qquad j=16,17,18,19,20,21.
\]

Their widths are `(41,33,25,17,9,1)/50624`, summing to `O=9/3616`. They are overlap intervals, not the final clear intervals. Thus

\[
U_J\ge\frac9{3616}-\frac{1045}{911232}
=\frac{1223}{911232}>0.
\]

The separately reconstructed actual duration is `6193/260352`. The inequality does not use that answer to derive the certificate.

### Both parts of the repair matter

Exact fraction substitutions give the following ablation checks on this same existing input:

| Information used | Clear-duration lower bound |
| --- | ---: |
| Original coarse pair-period bound | −755/3072 |
| Exact singles, using only the trivial overlap bound O>=0 | −1045/911232 |
| Exact selected overlap, but worst-case single-runner excess `sum 3/(16w)` | −19567/2429952 |
| Exact singles and exact selected overlap together | **1223/911232** |

The third row uses excess allowance `25615/2429952`. Retaining the old pair-union allowance while inserting exact singles is also inconclusive; even replacing its negative inferred overlap by zero only reaches the second row. Thus “restore local overlap” is incomplete as an explanation if the overly large concentration allowance remains.

The smallest already-supported refinement in this overlap argument uses four local single durations and one selected pair duration; after summing, the decision needs only T and O. This is not a proof of absolute minimality among all representations. A direct witness verifies this one input with less conceptual machinery, but does not supply the desired family mechanism. Subinterval topology and higher-order moments are unnecessary for this particular positive conclusion.

## 2. What higher resolution adds—and what it does not

The archived certificate ladder is:

| Certificate for 56/113/64/72 on J | Lower bound |
| --- | ---: |
| Selected pair 56/113 with exact singles | 1223/911232 |
| Best single pair, using 72/113 | 1495/303744 |
| Best tree | 58073/3644928 |
| Optimal generic inequality using all local single/pair moments | 63239/3644928 |
| A justified four-cycle using Q=0 | 72311/3644928 |
| Best corrected five-edge graph | 11369/520704 |
| Actual duration, for comparison | 6193/260352 |

The pair-moment optimum is recorded in [the September 27 Ultra review](ULTRA_REVIEW_2026_09_27.md). The graph certificates and corrections are in [FOUR_BLOCKER_CYCLE_CORRECTIONS.md](FOUR_BLOCKER_CYCLE_CORRECTIONS.md).

On every 56/113 overlap interval, runner 64 is strictly safe. Therefore the triple `{56,64,113}` is empty, implying four-way duration Q=0. The other three triples have positive durations. Q=0 alone is sufficient for the displayed four-cycle improvement; the triple exclusion is a speed-derived way to establish it. The five-edge graph additionally uses a nonzero triple correction and still misses `1/512` of actual duration.

For the neighboring 56/112 control, Q=`1/896` and every triple has positive duration. A cycle can still improve the tree after paying this quantitative correction. This distinguishes a forbidden joint event from a permitted event of bounded duration. It does not imply every cyclic certificate needs separately measured higher moments: a valid upper bound derived from already-retained data can sometimes suffice.

## 3. Counterexamples that constrain the explanation

**Same residual relation, tight outcome.** The existing extras `{6,7,11,13}` satisfy `13−2·6=1`. On J the selected overlap is `1/208`, while `E=1445/96096`; its one-pair bound is `−983/96096`. Actual duration is zero, with the valid singleton `3/8`. Across the whole period all four odd eighths survive. A small residual relation alone cannot force positive duration, and no duration statistic certifies the equality point without checking its boundaries.

**Same selected local summary, different duration.** The ratio controls `(80,240,88,96)` and `(160,240,88,96)` have the same four individual durations, selected overlap `1/128`, selected pair-union duration `5/128`, whole-cycle selected overlap `1/12`, and selected-pair gcd 80. Both have `E=1/1408` and one-pair lower bound `5/704`. Their actual durations are `1153/42240` and `613/21120`. Other pair overlaps differ, so this comparison does not establish that higher-order information is necessary once every pair moment is available.

**All local pairs can still be insufficient for exact duration.** [RESIDUE_COLLISIONS_2026_09_27.md](RESIDUE_COLLISIONS_2026_09_27.md) supplies stronger physical controls in `{0,1,4,5,6,7,11,y}`. The y=45 and90 configurations match every local labeled single/pair duration yet differ in U by `1/720`; a triple correction distinguishes them. The y=266 and532 pair also matches every gcd among the four extra blockers but differs in U by `1/2128`. This does not match every core-to-blocker gcd or every reduced speed ratio. Both pairs remain locally feasible, so these are duration distinctions, not empty-versus-nonempty counterexamples.

**Available phase area is not actual occupancy.** The q=56 and57 controls with residuals r=1,2 reverse their ordering of actual overlap although their residual phase-width functions do not change. Endpoint discrepancy terms explain that reversal. A permissible region must still be reached by the actual shared-clock trajectory.

These examples ask different questions. The small one-pair certificate suffices to prove positivity in 56/113. It does not recover every duration, identify every contact, or become a universal selection rule.

## 4. Small-gcd extensions already in the record

The request to move beyond large gcd has already produced several supplied arguments. They remain proof candidates rather than newly established results of this review.

| Existing scope | Supplied conclusion | Source |
| --- | --- | --- |
| `{0,1,4,5,q,2q+r,u,v}`, distinct speeds, u,v>=q, r=1,2,3 | Positive duration in J for q>=242,263,36 respectively; these supersede older sufficient cutoffs | [Overlap placement, §8](OVERLAP_PLACEMENT.md) |
| `{0,1,4,5,q,q+8,2q+1,v}`, q>=28, v>=q, distinct speeds | Positive duration from a triple exclusion and six fixed affine strips | [Uniform triangle certificate](UNIFORM_TRIANGLE_CERTIFICATE.md) |
| Any fixed positive integer core triple C, extras q,2q+r,u,v, u,v>=q, positive integer r, all speeds distinct | If M=max C and k counts positive core components, `U_A>=1/(64M²)−(29k+32r)/(32q)`; hence `q>2M²(29k+32r)` suffices | [Core transfer](CORE_TRANSFER.md), [September 25 overlap review](../reviews/2026-09-25-ultra/overlap.md) |
| Any fixed positive integer core triple and four distinct fixed affine coefficient pairs `(b_i,a_i)`, b_i>0 | Eventual strictness for speeds `b_i q+a_i`, with a cutoff depending on the fixed coefficients | [Affine family review](REVIEW_AFFINE_FAMILY.md) |

For r=1 the pair gcd is always 1. More generally `gcd(q,2q+r)=gcd(q,r)`. The explicit core-transfer condition already covers positive integer residuals r=o(q) for a fixed core, and should be used in its stated inequality form rather than treated as merely a fixed-r limit. It provides no unrestricted guarantee when the core and residual relations vary arbitrarily. Likewise the affine-family cutoff is not uniform over all coefficient choices.

The recurring mechanism is a controlled local phase relation plus exact or bounded endpoint discrepancy. It replaces dependence on a short full repetition period with dependence on structure along the portion of the trajectory that matters.

## 5. The remaining priority

The missing statement is no longer “why does 56/113 leave an opening?” It is:

> Under which speed assumptions can we select a useful opening and a small set of local quantities, then bound them from arithmetic strongly enough to force a witness, without first reconstructing the full allowed set?

A useful follow-up must improve at least one of selection, uniform scope, or the cost of evaluating a certificate. Reporting more successful exact reconstructions would not answer this question. A fixed number of reported moments does not imply a fixed cost for computing them.

After the queued two-time-template classification, use the existing cases above as diagnostic requirements for any proposed selection rule. Specify the rule and the information it may inspect before using final allowed sets to evaluate it. Existing known examples are not blinded validation. Include a countercheck where the proposed representation provably loses the target quantity, and preserve negative sufficient bounds as failures of the certificate rather than of loneliness. A separate endpoint route must retain tight cases.

The +7/+9 triple-correction direction and further cutoff polishing remain parked. This addition does not authorize a broad speed search or reopen those tasks automatically. No general Lonely Runner proof follows from the present review.

## Verification and status

The three audit assignments independently traced family scope, challenged information-sufficiency claims, and checked the certificate arithmetic against existing archives. Exact fraction identities, graph corrections, and interval durations were rechecked read-only. Two existing replay commands passed:

```bash
python -B reviews/2026-09-25-lr2/check_four_blocker_cycles.py --check
python -B reviews/2026-09-25-lr2/check_uniform_triangle.py --check
```

The first covers eight archived cases, 120 moment comparisons, graph identities, and equality handling. The second covers the six affine bands, 172 finite q values, eight four-blocker controls, two offset countercontrols, and three large formula controls. These are replays of declared old domains, not new searches. Neither is a formal proof of every unbounded implication.

Known source-attributed machinery retains its previous status and citations; no fresh literature or novelty audit was performed. Finite archived calculations remain OBSERVED/REPRODUCED within their scope. General family, discrepancy, and certificate arguments remain HYPOTHESIS/proof candidates under [CLAIM_STATUS.md](../CLAIM_STATUS.md). Open selection and uniformity claims remain OPEN. This review promotes no claim to an established proof.
