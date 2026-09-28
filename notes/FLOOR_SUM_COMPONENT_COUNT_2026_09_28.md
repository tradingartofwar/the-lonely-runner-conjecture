# Euclidean floor sums count the open lap strip—but do not win the small active cost ledger

September 28, 2026 UTC. Baseline `1d3bdf05b930f5765db866e4614bb2733eaa219d`, draft PR #3. Material AI involvement: one coordinating agent, one exact-calculation agent, one separately structured verification agent, and one adversarial-review agent. This is internal AI work, not independent human mathematical validation.

**Question.** Can the positive components of `B_a intersect B_b` be counted by an exact Euclidean floor sum, eliminating the prior per-lap scan on the same 24 frozen pairs, while preserving strict boundaries and honestly comparing work with the row formula and cached interval enumeration?

**Outcome.** Yes as an exact representation, but not as a cost win on the active selector cases. All 24 counts and all four archived branch records agree. The primary contains no per-`m` or per-`n` loop and constructs no blocking intervals. Nevertheless, its Euclidean recurrence takes 12 rounds on the four active pairs, versus seven lap rows in the prior formula. Only the larger `doubling_112` diagnostic shows fewer recurrence rounds than lap rows, 28 versus 39. These are different-cost primitives and do not establish a runtime ordering.

**Status.** The 24 exact agreements and operation ledgers are **OBSERVED** on the frozen cases. The general half-plane/floor-sum derivation is an AI-assisted elementary proof candidate under the stated domain. It is a classical type of lattice-count transformation; no novelty search was performed and no novelty is claimed.

## 1. Frozen contract

The [protocol](../reviews/2026-09-28-floor-sum-component-count/protocol.json), SHA256 `a398539b747b9510259e5a134090f3eb6430370588d735bdec12f67260ec5724`, was frozen before calculation. A source-hash transcription error was corrected immediately after checking the pinned local file and before either implementation calculated results; the mathematical contract was unchanged.

The contract fixes:

- exactly the previous four windows and 24 physical pairs;
- inherited positive-slack eligibility and the minimum-component/physical-lexicographic selector;
- exact integers and `fractions.Fraction`, with no floating-point decision;
- no primary lap-coordinate scan or interval construction;
- no new containment query, fallback, speed, window, core, reference, alternate-window campaign, broad scan, or `+7/+9` work;
- a primitive-by-primitive cost ledger, with no synthetic score or wall-clock inference.

Before the archived answers are read, the primary projects each case to speeds, its window, inherited eligibility, and strict lap-rectangle bounds. All counts and branch records are fixed before postselection comparisons.

## 2. Exact transformation

Let `a<b` be positive integer speeds, `J=[L,R]`, and `delta=1/8`. Strict window participation gives the inclusive integer rectangle

`aL-1/8 < m < aR+1/8`,

`bL-1/8 < n < bR+1/8`.

The preceding lap-band lemma identifies positive pair components with rectangle points satisfying

`|b*m-a*n| < (a+b)/8`.

Set

`D=8*b*m-8*a*n` and `S=a+b`.

Because `D` is integral, the open strip is exactly

`-S+1 <= D <= S-1`.

For an integer `K`, let `H(K)` count rectangle points with `D<=K`. Then the required count is

`H(S-1)-H(-S)`.

For fixed `m`, `D<=K` is equivalent to

`n >= ceil((8*b*m-K)/(8*a))`.

If the rectangle's `n` range is `[n_min,n_max]` with `N_n=n_max-n_min+1`, define

`x_K(m)=floor((8*b*m-K+8*a-1)/(8*a))-n_min`.

The number of rectangle rows below the threshold is `clamp(x_K(m),0,N_n)`. This nondecreasing function splits at the exact first `m` with `x_K>=1` and first `m` with `x_K>=N_n`. For `x(m)=floor((A*m+B)/Q)`, those indices are obtained directly from

`first_ge(z)=ceil((Q*z-B)/A)`.

The unsaturated middle sum is a range sum of `floor((A*m+B)/Q)`. After exact signed-offset normalization, a quotient/remainder Euclidean recurrence evaluates it. Thus the primary loops only over recurrence rounds, not lap labels.

The strictness shifts are essential. With `a=3`, `b=5`, `S=8`, lap pairs `(1,2)` and `(2,3)` give `D=-S` and `D=+S`, at contacts `3/8` and `5/8`. Both are excluded and contribute no positive pair component.

## 3. Exact finite results

The floor-sum count vectors, in physical-speed lexicographic pair order, are unchanged:

| Case | Six pair counts | Frozen branch record |
| --- | --- | --- |
| target `{15,38,61,100}` | `1,1,1,2,2,3` | select `{15,38}`; prior `49/524400` certificate |
| `strict_16` `{6,7,11,16}` | `0,1,1,1,0,1` | eligible 1–1 tie; select `{6,11}` |
| `doubling_112` `{56,64,72,112}` | `2,3,6,3,5,4` | diagnostic `{56,64}` after pair-only exit |
| `tight_13` `{6,7,11,13}` | `0,1,1,1,1,0` | no eligible pair; isolated `3/8` remains separate |

All 41 positive lap points match the prior row archive. This is exact representation recovery on known development and control cases, not held-out evidence that the selector generalizes.

## 4. Honest cost comparison

The frozen ledgers count unlike primitives separately:

| Scope | Floor-sum half-planes | Range sums | Euclidean rounds | Quotient/remainder pairs | Prior lap rows | Cached interval work |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| four active pairs | 8 | 5 | 12 | 20 | 7 | 38 lap candidates, 17 pieces, 13 joins |
| six doubling diagnostics | 12 | 12 | 28 | 49 | 39 | 126 lap candidates, 93 pieces, 87 joins |
| all 24 validation pairs | 48 | 29 | 65 | 107 | 63 | not archived for all ineligible pairs |

The floor-sum ledger also charges 16, 24, and 96 threshold ceiling divisions in those three scopes. The row ledger charges two band bounds, two max/min operations, and two floor/ceiling operations per row. The cached interval ledger includes additional named state, clipping, phase-fold, and join comparisons in the result artifact.

The structural improvement is real: the floor-sum count does not scan a speed-dependent list of lap rows. The finite cost result is mixed and mostly negative: recurrence rounds exceed lap rows on the active selector (`12>7`) and over all validation pairs (`65>63`), while the larger doubling diagnostic reverses this comparison (`28<39`). Recurrence rounds and rows are not equal-cost operations; integer operand sizes, implementation overhead, caching, and wall-clock time were not converted into a common score.

The comparison also exposed and corrected one old prose transcription: the four active pairs contain six compatible lap pairs, not four. The pinned earlier `results.json` already recorded the correct six (`1+3+1+1`), so no count or selector result changed.

This floor-sum method remains arithmetic overlap geometry. It compresses iteration but does not explain why the minimum-component pair should satisfy the needed complement containment. The sparse triple-exclusion and alternate-window mechanisms already in the repository remain distinct prior selection work.

## 5. Verification and controls

Artifacts are under [reviews/2026-09-28-floor-sum-component-count/](../reviews/2026-09-28-floor-sum-component-count/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-floor-sum-component-count/primary.py --check
python -S -B reviews/2026-09-28-floor-sum-component-count/verify.py --check
```

The independent verifier imports no primary code. It directly scans 410 exact points in the 24 lap rectangles, reconstructs 311 threshold events and 287 open cells, checks all 41 positive lap points and archived component counts, and independently recomputes both half-plane totals column-wise. It matches 173 primary critical fields and both strict-boundary controls. All 25 repository tests pass.

Three complementary AI agents performed the primary calculation, separate verification, and adversarial proof/cost review. Their agreement is internal error control, not independent human mathematical validation.

## 6. Remaining uncertainty and next bounded step

The floor sum answers how to count without a lap-row scan; it does not make the development-case selector predictive. The active finite cases give no operation-count reason to prefer this implementation, and no bit-complexity or runtime advantage was established.

The next more consequential question is therefore selector transfer rather than another representation rewrite. Freeze the unchanged positive-slack/minimum-floor-sum rule, one compound containment query, physical lexicographic ties, and no fallback on the **already archived eighteen tree-missed positive windows**. Mark the present target and its reflection as development cases; treat the rest as an archival transfer audit, not prospective held-out data. Compare against largest potential slack and the already known sparse/alternate-window certificates without presenting those as new. Preserve every failed selection and exact violation. Generate no new speeds, windows, references, broad scan, or `+7/+9` work.
