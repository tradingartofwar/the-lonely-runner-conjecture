# Ultra review: findings, limits, and the next useful question

September 25, 2026. Reviewed research revision: `ea482f54edae4775621bc69c1fb7359291f31ddd`, on draft PR #3. Vance requested review of the proof candidates, package, and any other useful evidence.

Six separate GPT-6 Astra reviewers ran with **Ultra reasoning** and fresh task contexts, divided by proof family and package quality. The root checked consequential findings and consolidated this report. They were separate AI reviewers, not external mathematical referees. No candidate is promoted to an established or novel result by this review. No researcher was contacted and no main-branch merge occurred.

## Overall assessment

**The reviewers found no fatal mathematical gap in the candidate implications they audited.** Their reports explain the algebra and quantifiers checked, and their coverage limits. This means the arguments survived a substantial adversarial AI review; it is not a guarantee that every historical claim is correct.

The most useful returns were more specific than agreement:

1. A small exact example breaks a tempting extension of the successful tree-overlap diagnostic. Individual and pairwise duration totals can be insufficient even for any generic event inequality using only those totals.
2. The affine argument supports a quantitative approximation bound and balanced-block extensions beyond eight runners. Several reference changes also work. These are proposed corollaries, with fixed-coefficient and asymptotic restrictions.
3. The proposed core-threshold question has a short one-sided existence extension with the same cutoffs. Contact classification needs a third controller there.
4. The written work should be organized around a few shared mechanisms. Counting notes, certificates, or successive cutoff improvements is not counting independent discoveries.
5. The reported finite-runner literature advanced in a September 24 revision. The current source record and strategy paragraph have been updated, preserving the earlier version history.

## 1. An exact limit of the overlap method

Use eight common-start speeds

\[
\{0,1,4,5,6,7,11,16\},
\quad C=\{1,4,5\},\quad J=[9/32,3/8].
\]

Only 13 was changed to 16 in the familiar comparison family. The reference runner has precisely the following allowed component inside J:

\[
[17/56,39/128],\qquad\text{length }1/896>0.
\]

Yet the strongest of all sixteen spanning trees on the four extra runners has clear-duration lower bound

\[
-23/29568<0.
\]

The positive-overlap graph contains a triangle on speeds 6,11,16 with no triple overlap. Every tree must omit an edge, thereby discarding useful pair-only overlap. This does not contradict the earlier explicitly finite 38/38 success; it disproves its proposed universal component-level extension. It does not establish failure for every core choice or every subdivision of this example.

The stronger information limit is exact. Let theta=1/896. From the distribution of blocking states, remove theta from the empty state and from each pair-only state {6,11}, {6,16}, {11,16}; add theta to each singleton {6}, {11}, {16} and to the triple {6,11,16}. Every mass stays nonnegative. All four individual durations, all six pairwise overlaps, and total duration stay unchanged, but uncovered duration becomes zero.

That alternative is an **abstract arrangement of events**, not a second runner configuration. It proves that these pairwise totals alone cannot force a positive opening through a universal event inequality. A successful refinement must use additional runner geometry, higher-order intersection information, or where overlaps occur within the interval.

The overlap reviewer and root independently reconstructed this example using separate standard-library rational code with no project imports. Full durations, best edges, and both blocking-state distributions are saved in [overlap_check.json](../reviews/2026-09-25-ultra/overlap_check.json) and [root_checks.json](../reviews/2026-09-25-ultra/root_checks.json).

## 2. The affine argument contains a broader transfer principle

For fixed core c_j and fixed integer pairs (b_i,a_i), define the best separation in the auxiliary two-coordinate system by

\[
L_U=\max_{t,x}\min\bigl(\|c_jt\|,\|b_ix+a_it\|\bigr),
\qquad K=\max\bigl(\max_j|c_j|,\max_i|a_i|\bigr).
\]

Let L(q) be the actual best separation for speeds c_j and b_i q+a_i, with the stationary reference retained. The actual trajectory x=qt lies inside the auxiliary system, giving the upper bound. Rounding an auxiliary maximizer exactly as in the original proof gives the lower bound:

\[
\boxed{L_U-\frac{K}{2q}\le L(q)\le L_U.}
\]

This explains the link between room in the auxiliary model and room reached by actual motion. A strictly positive auxiliary margin eventually survives the bounded rounding loss. A zero margin does not gain strictness from this inequality. The root independently checked this derivation; it is recorded here as a proposed corollary awaiting external correctness/prior-art review.

The same existence mechanism is not inherently limited to eight runners:

| Total runners | Fixed nonzero core speeds | Affine fast speeds | Why an auxiliary gap exists |
| --- | --- | --- | --- |
| n=2m, m>=2 | m-1 | m | At target 1/n, fast blocking measures sum to one. The same nonzero lowest-frequency coefficient excludes persistent exact tiling. |
| n=2m+1, m>=1 | m | m | Both groups have total blocking measure 2m/(2m+1)<1, so the phase gap needs no Fourier argument. |

In both rows the coefficients stay fixed as q grows; the conclusion is eventual strict loneliness for the selected reference. It does not cover arbitrary speed sets by freely choosing q after the fact. Exclude n=2 from the even strict statement: two runners cannot exceed a half-lap distance.

Reference changes give more scope in specific cases. Every runner in the fixed slow block has eventual strictness. For two equal-winding blocks of m runners each, all 2m references have eventual strictness, generally at different times. For the eight-runner affine family, a fast runner whose winding rate is unique also has eventual strictness; pairwise-distinct fast winding rates therefore give another all-reference special case. The remaining mixed multiplicities are not automatically covered. Repeated absolute relative speeds must be deduplicated without changing the original threshold.

As one exact diagnostic beyond eight runners, root checked

\[
\{0,1,2,3,4,50,101,153,207,261\}
\quad\text{at }t=41/200,
\]

whose minimum distance from reference 0 is 9/50>1/10. This illustrates the proposed general mechanism; it does not prove the unbounded corollary.

The affine reviewer also supplies an elementary alternative to the Fourier step: a perfect tiling must contain a contact between different boundary velocities, unless all blockers share a center and overlap. Such a contact fixes one rational slow time, and only finitely many endpoint pairings are possible. Both this argument and the quantitative Fourier route merit consolidation before a novelty inquiry.

## 3. The core-boundary question becomes a corollary, with a new caveat

The complete closed safe set for the normalized core {x,2x,3x} is

\[
[1/8,7/24]\cup[3/8,7/16]\cup[9/16,5/8]\cup[17/24,7/8].
\]

Each endpoint has exactly one active core constraint, and the shortest component has length 1/16. An arc with extreme absolute ratio M has an outward opening in each x-direction, one at each endpoint of that arc. Choose the direction entering the strict core. The earlier neighborhoods H=1/(8M) for positive coefficients and H=1/(16M+1) for signed coefficients are both shorter than 1/16. Their same entry estimates therefore give strict escape at a core boundary for q>=8 and q>=17 respectively.

This is a proposed extension of existence to **closed-core-safe** tilings under the remaining original assumptions. At an actual contact there are now three active runners. All three phases 1/8 start a strict interval; all three phases 7/8 end one; mixed phases isolate the contact.

For example, speeds {0,35,70,105,141,1119,807,1923} at t=5/24 have exceptional phases 1/8 for 1119 and 807, but core speed 105 has phase 7/8. The two exceptions alone suggest an interval beginning; the core closes it, leaving an isolated actual time. This is exactly the obstruction anticipated in the preceding conversation, but it does not defeat the safe-direction existence construction elsewhere nearby.

The reviewer checked sixteen prescribed endpoint profiles and seventy-two reachable contact cases. Root separately reconstructed the core intervals and checked the named three-controller examples. [The tiling review](../reviews/2026-09-25-ultra/tilings.md) contains the complete derivation and exact components.

## 4. Review coverage and how the candidates relate

This is a scope map, not a count of independent theorems. The earlier informal package count grouped research notes and refinements. It should not be used as a measure of progress toward the full conjecture.

| Research thread | Current content and review conclusion | Detailed report |
| --- | --- | --- |
| Fixed replacement and one-/two-variable families | Modular witnesses, local width/measure bounds, and exhaustive finite remainders survived review. Two minor exposition/consolidation suggestions. | [Early](../reviews/2026-09-25-ultra/early.md) |
| Foundational overlap/chains; Fibonacci | Scoped identities and chain certificates checked. Fibonacci formulas correctly identified as known; no full published-proof audit. | [Early](../reviews/2026-09-25-ultra/early.md) |
| Local overlap and speed ratios | Applications of pair grouping and periodic tail bounds; no fatal gap found in the stated cutoffs. | [Overlap](../reviews/2026-09-25-ultra/overlap.md) |
| Placement, discrepancy, residue improvements, core transfer | Successive versions of affine phase analysis plus endpoint correction. Improved constants are not new independent strategies. New fixed-tree limitation above. | [Overlap](../reviews/2026-09-25-ultra/overlap.md) |
| Fast cluster / affine family | One general fixed-core transfer mechanism, with equal-winding specialization. Steps A–D survived review; strongest first external-review object. | [Affine](../reviews/2026-09-25-ultra/affine.md) |
| One, two, four, unequal and doubled perturbations | Specialized pre-jump/tiling arguments plus exact remainder coverage. Review distinguishes maximum claims, strict witnesses and equality contacts. | [Perturbations](../reviews/2026-09-25-ultra/perturbations.md) |
| Fixed tiling escape, positive local rule, signed local rule | Exact gap geometry plus actual reachability; same mechanism with broader hypotheses and coefficient-uniform cutoffs. No fatal gap found; boundary extension above. | [Tilings](../reviews/2026-09-25-ultra/tilings.md) |
| Checker, provenance and package | Intact checked evidence, but the default 25 tests only cover the checker. Four selected-source manifests omit one transitive import. | [Package](../reviews/2026-09-25-ultra/package.md) |

The overlap report also derives a growing-residual extension of its fixed-core estimate, and a sharper pair-contact condition using gcd. These remain review deductions with their exact assumptions, not silently expanded historical claims.

## 5. Evidence and package corrections

The root matched 107 working files to the reviewed live Git tree, including all mathematical notes, scripts, experiments, checker/tests and HANDOFF. Older local governance copies were excluded from that claim; the authoritative instructions and package files were retrieved at the pinned revision. Reviewers made no edits to the original research code or evidence.

The package audit found all **165 recorded hashes** intact and independently checked **755 endpoint-certificate groups** without importing the project checker. Of these, 723 seven-speed occurrences reduce to 683 unique speed-set/interval certificates across 536 distinct speed sets. Counts overlap with family audits and do not measure independent replications. All 25 checker tests and the demo consistency check passed.

Four manifests—affine_family, core_transfer, fast_cluster and pair_selection—omit the transitive dependency `scripts/analyze_residual_overlap.py`. The full pinned commit still identifies it; no incorrect output followed from the omission. Historical evidence has been preserved. Future manifests should identify the full dependency closure or call themselves selected-source records.

The source update is recorded in [SOURCES.md, S7](SOURCES.md): Allikvere's [September 24 v2](https://arxiv.org/abs/2609.02604v2) reports fourteen and fifteen total runners. Only abstract/comments/history were inspected. Neither proof nor computational archive was audited. The live handoff and strategy paragraph now reflect this dated report; no claim of a latest proved frontier beyond that source check is made.

### One portable, read-only verification command

From the repository root containing this review package:

```bash
python reviews/2026-09-25-ultra/verify.py
```

The seven selected checks all passed after packaging. The runner imports no project mathematical helper into the standalone reviewers. It captures attempted review-JSON writes in memory, compares them with the archived review results, and leaves the original experiment files unchanged. Selected groups can also run, for example:

```bash
python reviews/2026-09-25-ultra/verify.py package overlap root
python -m unittest discover -s tests -v
```

The full reports state what each verifier covers. These commands verify bounded arithmetic, geometry and recorded reductions; they do not mechanically prove every symbolic or unbounded implication. Some family scripts were also reproduced by their reviewers with output writes intercepted; that reproduces an implementation rather than creating a second independent algorithm.

The root only normalized execution paths in the archived reviewer reports/scripts and added the read-only runner and root checks. Their mathematical reports are otherwise preserved. [review_manifest.json](../reviews/2026-09-25-ultra/review_manifest.json) records the pinned research tree and review artifact hashes. Original proof notes retain their prior status and scope; the proposed extensions are collected here for explicit future review.

## 6. Recommended next action

The most focused external correctness/prior-art request remains the pinned [affine review note](REVIEW_AFFINE_FAMILY.md), Steps A–D, with this audit as optional supporting material. A specialist can assess one clean proposition without reading the whole research history. No outreach has been performed.

For the next internal mathematical question, the tree counterexample is more discriminating than further cutoff polishing: **which information about overlap placement or higher intersections rules out the abstract complete-cover arrangement while respecting actual runner speeds?** An alternative is to ask whether a different core or a finer time subdivision must yield a certificate. Those are distinct conjectures, and the present review proves neither.

The useful progress is a more precise map of what survives scrutiny, what can be generalized, and what information our current methods lose. Independent external correctness and novelty review remain open.
