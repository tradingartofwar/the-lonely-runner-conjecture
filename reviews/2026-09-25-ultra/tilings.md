# Review of the tiling escape packages

Reviewed September 25, 2026. Target commit: `ea482f54edae4775621bc69c1fb7359291f31ddd`, PR #3 branch `research/near-doubling-overlap-2026-09-24`. The root reviewer verified the working copies of the mathematical notes, scripts, and evidence against that live commit's blob hashes; the local Git HEAD/index are a stale synthetic snapshot and are not the provenance claim. Authoritative governance files were read from `ultra-review/snapshot`.

This is a fresh AI mathematical/code review with a separately implemented exact verifier. It is not independent human review, external certification, a formal proof-assistant verification, or a novelty determination. No repository file was modified and no publication action was taken.

## Verdict and findings

I found no fatal mathematical gap or counterexample in the stated fixed-family all-q>=5 result, the positive conditional q>=8 result, or the signed conditional q>=17 result. The essential unbounded arguments are actual derivations, rather than extrapolations from the four tested coefficient profiles. In particular, the denominator bound really does compensate for a small core margin, and the signed extreme-boundary argument really does produce an actual common-start time.

The most useful new observation is that the proposed next question about **core threshold tilings** is already answered affirmatively for existence by a short one-sided extension of the same argument. The same q cutoffs suffice when the core is merely safe (>=1/8) at the tiling. The threshold case does add a third active constraint to the local contact classification; that is a real change and gives an instructive counterexample to naively extending the two-exception classification.

| Severity / type | Location | Finding |
| --- | --- | --- |
| No blocking defect found | `LOCAL_TILING_RULE.md` 76–145; `SIGNED_TILING_RULE.md` 73–146 | Denominator, core safety, collision, and actual entry estimates are valid under their explicit hypotheses. |
| Medium, research-direction correction | `SIGNED_TILING_RULE.md` 233; final signed continuation in `HANDOFF.md` | Strict core safety is unnecessary for existence with this specific `{q,2q,3q}` core. The proposed boundary question is a short corollary, not a substantial new obstruction. Derivation below. |
| Medium, extension warning (not an error in current scope) | `SIGNED_TILING_RULE.md` 150–160 | The current two-controller classification is correct only with a strict core. At a core threshold, a third controller can turn an auxiliary interval endpoint into an isolated actual time. Explicit exact example below. |
| Low, exposition improvement | `TWO_DOUBLED_OFFSETS.md` 42–51 | The tiling criterion has an elementary half-periodicity proof; Fourier analysis is optional. |
| Low, exposition improvement | `LOCAL_TILING_RULE.md` 151–159 | The contact period also obeys `P | d`, because the six contacts are translates by eighth-grid values of `-A0*x0`. This makes the arithmetic reduction more transparent. |

No severity labels here should be read as an automatic promotion of proof-candidate status. The repository's current cautious status labels remain appropriate.

## What was checked

The independent verifier is `test_tilings.py`, with exact output in `test_tilings_results.json` and console output in `test_tilings_output.txt`, beside this report. It uses only the standard library, imports no repository code, and writes only beside itself. It reconstructs threshold partitions directly from the original rational inequalities, including singleton contacts and endpoints.

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python reviews/2026-09-25-ultra/test_tilings.py
```

Checks passed:

- 39 recorded source hashes, including repeated dependencies across packages;
- 54 complete frozen phase sets, including zero, half-radius, full-radius, both signs, and wraparound;
- all 64 recorded complete local actual schedules: 16 fixed-family, 24 positive, 24 signed;
- 173 stored positive-length interval certificates, by direct affine phase-strip inequalities;
- all 6 recorded signed reachable-contact types;
- 864 affine runner/cell certificates, recomputing 3,456 vertex phases rather than trusting the stored values;
- all 40 fixed-family symbolic winner comparisons, with nonnegative q coefficient and strictly positive value at q=5;
- 16 constructed core-endpoint profiles, one positive and one mixed-sign profile at each of the eight endpoints, with an extreme-boundary strict witness at q=8 and q=17 respectively;
- 72 reachable contact cases in those prescribed endpoint profiles, covering all their contact residues with representatives at least 17;
- 4 complete actual-time schedules for the new named endpoint examples below.

These counts contain repeated/symmetric structure. They are not counts of independent mathematical replications. The extra positive compatibility case stored under `signed_tilings.json` was not separately repeated because its positive profile is already covered. I did not regenerate or overwrite any tracked JSON or figure, run a coefficient-box search, or enumerate any million-point time grid.

## Tiling criterion and exact local geometry

### The rates-1,1,2,2 criterion is valid

In `TWO_DOUBLED_OFFSETS.md` 30–53, the total blocked length, with multiplicity, is exactly 1. Zero clear measure therefore forces blocker multiplicity 1 almost everywhere. The two doubled blockers are invariant under translation by 1/2. Consequently the sum of the two unit-blocker indicators must also be invariant under that translation. Their disjoint union consists of two quarter arcs. The half-turn swaps these connected components, so their centers differ by 1/2.

After rotating the unit centers to 0 and 1/2, the remaining two quarter gaps must each be partitioned by two eighth arcs. Their centers are forced to be 3/16,5/16,11/16,13/16. Pairing centers half a cycle apart yields the doubled phase residues 3/8 and 5/8, one of each. This proves both necessity and sufficiency without Fourier coefficients. The Fourier computation in the note is also correct.

Because blocking arcs are open, all six tiling contacts are allowed. The scripts correctly preserve the endpoint copy 1 of contact 0 when working on `[0,1]`; it is not a seventh point of the phase circle. Equal normalized ratios would force positive overlap (or identical blockers), so the four ratios are distinct. At each contact exactly two exceptional constraints are active, under the strict-core hypothesis.

### Cyclic growth is an exact local identity

For the arc ending at c and the arc beginning at c, the gap length is `(r_L-r_R)*epsilon`, when positive. The cyclic differences telescope. Thus the sums of positive and negative differences have equal magnitude, and both one-sided clear-length slopes are

`K = (1/2) sum_contacts |r_L-r_R| > 0`.

This is valid for either sign of the coefficients. It is exact because the boundary motions are affine. It remains valid only while different contact clusters retain their cyclic order. The stated collision estimates ensure this. An overlap at one former contact cannot conceal a gap at another before such a collision occurs.

For `TILING_ESCAPE.md` 43–69, the six stated gap branches and the `14|epsilon|` total agree with the independently reconstructed exact phase sets. The affine vertex checks certify the intervening continuum; checking the endpoints separately avoids losing collapsed cells or singleton contacts at h=0 and h=1/56. The control at epsilon=1/55 appropriately limits the formula's range.

## Denominators, safety, and collision estimates

For either signed or positive coefficients, write `x0=p/d` in lowest terms. The unit congruence forces `A1-A0 != 0`, rational x0, and `d | 2(A1-A0)`. The doubled congruence at residue 3/8 implies `8 | d`. This is not a numerical pattern.

For positive coefficients, `d <= 2|a1-a0| < 2M`. Since every core phase and 1/8 are multiples of 1/d, strict safety gives a margin of at least 1/d. Dividing by core speeds 1,2,3 gives `R_core >= 1/(3d) > 1/(6M)`. Neighboring tiling contacts have spacings 1/8 or 1/4. Every difference between positive boundary ratios is strictly below M. Hence `H=1/(8M)` is strictly below every relevant collision radius and the core-safety radius. No positivity bound is accidentally applied to signed data.

For signed coefficients, `d <= 2|A1-A0| <= 4M`, hence `R_core >= 1/(12M)`. Boundary differences are at most 2M. The choice `H=1/(16M+1)` is strictly below `1/(16M)` and `R_core`. The extra `+1` makes the closed-neighborhood strictness immediate. M>=4 holds because the two unit coefficients have absolute value at least 4, even though doubled ratios can have magnitude 2.

The distinct-speed arguments are also valid: at q>=3 in the positive class an offset difference of at most 1 cannot cancel distinct integer coefficient multiples of q; at q>=5 in the signed class the maximum offset difference is 4. Equal physical coefficients with identical signed offsets would contradict tiling through identical blockers. Every exceptional physical speed exceeds 3q in the claimed scope.

## Actual-time reachability, signs, and endpoint conventions

### Positive class and fixed example

On the approaching side of a contact, the strictly chosen nearest integer branch gives `0<rho<=1`. Substituting the actual slope `s/q` into the moving gap yields

`h_enter=rho/(Aq+1)`, `h_exit=rho/(Bq+1)`, with `A>B>0`.

The formulas have the correct `+1` for either direction of core-phase motion. Reducing j modulo q simply chooses an equivalent lift of the phase circle. A zero mismatch must be retained as an equality contact and then replaced by rho=1 to locate the next approaching branch. The scripts do this in `analyze_local_tilings.py` 171–181.

Some gap uses the largest ratio M as its faster edge, so q>=8 gives `h_enter<=1/(Mq+1)<H`. Its other boundary is strictly separated at entry, which leaves a nonempty strict interval. This is a complete coefficient-unbounded argument. It does not depend on the four profile calculations.

The fixed-family eight-residue winners in `TILING_ESCAPE.md` 118–148 survive independently recomputed symbolic cross-products. All winning exits are before H. Thus minimizing these entries really does give the nearest feasible core-phase displacement globally: any closer displacement would already lie in the completely described local neighborhood. The nearest displacement, time displacement from the chosen branch, and waiting time from the common start are correctly distinguished.

### Signed class

At `epsilon=s*h`, subtracting the actual branch motion from the two boundaries gives exactly

`ell*h <= d_j <= u*h`, where `ell=-s(r_L+1/q)` and `u=-s(r_R+1/q)`.

The three sign cases in `SIGNED_TILING_RULE.md` 116–122 and `solve_wedge` in the script are correct. In the straddling case, a reachable zero-displacement contact enters a strict interval immediately. No denominator can vanish: `|r_i|>=2` and `1/q<=1/5`. Nearest branches above, below, and at the contact are sufficient, since for each fixed side the entry displacement is monotone in branch distance.

For an arc with |r|=M, either adjacent contact has that edge at an outward extreme in its opening direction. If r=M it is globally largest; if r=-M it is globally smallest. Adding 1/q preserves that extremum and its sign. A strictly outward nearest branch lies at distance at most 1/q, and its entry is at most `1/(qM-1)`. For q>=17 and M>=4 this is strictly below H. At the entry the other edge is separated by `(u-ell)*h_entry>0`. This supplies an actual open time interval where every exception and the core are strict.

The contact classification at strict core phases is correct. The left-ending normalized blocker has phase +1/8; the right-starting blocker has phase -1/8. Multiplying by the coefficient signs gives either opposing physical threshold phases (isolated time), both 1/8 (interval begins), or both 7/8 (interval ends). All physical speeds are positive. The associated sum/difference integrality relations are necessary phase identities, not sufficient loneliness tests; the note correctly says so.

## The core-threshold extension follows with the same cutoffs

This is an additional proof candidate derived during review, not an edit to the repository or a novelty claim.

The complete closed safe set of the fixed core is

`C = [1/8,7/24] ∪ [3/8,7/16] ∪ [9/16,5/8] ∪ [17/24,7/8]`.

Every boundary point has exactly one active core constraint. The component lengths are `1/6,1/16,1/16,1/6`, so the minimum is 1/16. At the left endpoint, moving x positively enters the strict core; at the right endpoint, moving negatively enters it.

Take any arc whose |r| equals M. **It has an outward-extreme opening in each core-phase direction, at its two contacts.** Explicitly:

- If r=M, its ending contact has `Delta=M-r_neighbor>0`, and its starting contact has `Delta=r_neighbor-M<0`.
- If r=-M, its ending contact has negative Delta, and its starting contact has positive Delta.

The chosen arc's edge is an outward extreme of the corresponding relative wedge in each case. Thus select the contact whose opening direction points into C, and apply the same nearest outward branch construction.

In the positive class, `H=1/(8M)<=1/32<1/16`. In the signed class, `H=1/(16M+1)<=1/65<1/16`. Therefore moving from a core endpoint in the chosen direction stays strictly inside that core component for every `0<h<=H`. The collision bounds do not need strict core safety. The existing entry bounds then produce strict witnesses for q>=8 positive, q>=17 signed.

This extends the existence conclusion from strict-core tilings to all tilings with `||kx0||>=1/8` for k=1,2,3, with the same hypotheses on coefficients and q. Interior x0 is already handled by the existing proof; the argument above handles all boundary points. The denominator-based core margin is replaced only at those finitely described endpoints by one-sided core geometry.

A concrete positive endpoint example is `A=(4,8,11,13)`, x0=1/8, q=8. Here H=1/64; the safe-direction extreme opening is reached at h=7/520, before H. The independently checked time `t=1161/66560` has minimum distance `137/1024>1/8`. This is one bounded certificate illustrating the general derivation.

### Contact behavior does change at a core boundary

At an actual tiling contact, there are now three active constraints: two exceptional runners and one core runner. A strict interval begins exactly when all three physical phases are 1/8; it ends exactly when all three are 7/8; mixed phases give an isolated time. Other constraints are strict locally.

The following complete actual components were reconstructed from all threshold boundaries with fresh exact code. A=(A0,A1,A2,A3) is ordered against b=(1,1,2,2), and physical exception speeds are `|Ai|q+sign(Ai)bi`.

| A | x0 | q | Actual contact t | Complete component containing t |
| --- | --- | ---: | --- | --- |
| (4,-8,11,-11) | 1/8 | 21 | 5/8 | [5/8,1167/1864] |
| (5,-19,20,-32) | 7/16 | 23 | 1/16 | [217/3488,1/16] |
| (4,8,11,13) | 1/8 | 17 | 1/8 | {1/8} |
| (4,-32,23,-55) | 7/24 | 35 | 5/24 | {5/24} |

In the last row the physical speeds are `{0,35,70,105,141,1119,807,1923}`. At t=5/24, the two active exceptions 1119 and 807 both have phase 1/8, so their auxiliary contact would begin a strict interval. The active core runner 105 has phase 7/8 and blocks the right side, while the exceptions block the left side. The actual contact is isolated. This precisely demonstrates why the old two-controller classification cannot simply be copied into the relaxed-core statement, even though strict escape elsewhere in the local safe direction still follows.

The most useful boundary follow-up is therefore a short corollary plus this three-controller clarification. It does not require a new broad experiment or a new unbounded mechanism. A more substantial subsequent scope would change the core so that its closed safe set may have isolated components, or remove the tiling assumption; neither follows from this review.

## Literature and limits

I read the repository's relevant source notes and reopened the published Kravitz paper, *Barely lonely runners and very lonely runners: a refined approach to the Lonely Runner Problem*, Combinatorial Theory 1 (2021), #17, DOI 10.5070/C61055383, Section 2, printed pp. 4–5. The opposing-half local-maximum discussion and the pre-jump paragraph support the limited methodological context attributed in these notes. They do not supply an external certification of the new tiling cutoffs. The technical n there counts moving speeds; our eight-runner system has seven such speeds.

Published source: https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf . No wider prior-art audit was performed in this subreview.

This review does not establish novelty, sharp cutoffs, a theorem for arbitrary speed sets, any global maximum formula, or loneliness for every reference runner in these configurations. It also does not audit the entirety of `TWO_DOUBLED_OFFSETS.md`'s 96-vector finite remainder; only its tiling criterion and the changed-coefficient control are dependencies here. All unbounded conclusions remain proposed mathematical derivations with AI review, while the listed rational test results are bounded reproduced computations.
