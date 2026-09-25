# LR 2 — resume after the Ultra review

September 25, 2026. This is the compact continuation entry point after LR 1 reached its conversation limit. It summarizes the verified research record; it is not a transcript or a new mathematical review. Material AI involvement in this recovery, verification, and writing is disclosed.

## Start here

The governing question remains: **What prevents the runners from collectively blocking every possible moment?** Work from the latest Ultra review and its follow-up, not an earlier proposed next step buried in the chronological handoff.

1. Read [the consolidated Ultra report](notes/ULTRA_REVIEW_2026_09_25.md), especially Section 7's correction.
2. For a focused proof candidate, read [the affine review note](notes/REVIEW_AFFINE_FAMILY.md), Steps A–D.
3. For exact reviewer scope and additional deductions, use the six reports below.
4. Use [HANDOFF.md](HANDOFF.md) for the deeper history and [CLAIM_STATUS.md](CLAIM_STATUS.md) for evidence labels.

All runners start together. `n` counts total runners; the selected reference leaves `n-1` relative constraints. Equality at `1/n` is valid. Selected-reference results do not silently become all-reference results.

## Where the material was made public

The repository is public. The research branch is `research/near-doubling-overlap-2026-09-24`, attached to [draft PR #3](https://github.com/tradingartofwar/the-lonely-runner-conjecture/pull/3). At recovery, the PR was open and draft, with no submitted reviews, conversation comments, or inline comments. `main` was protected and remained at `c8a287f52ef0066d2ba6247094bdeba023825081`; its tree did not contain the Ultra review package.

| Record | Permanent reference | Meaning |
| --- | --- | --- |
| Research assessed by Ultra | [`ea482f54`](https://github.com/tradingartofwar/the-lonely-runner-conjecture/commit/ea482f54edae4775621bc69c1fb7359291f31ddd) | Baseline for the six assignments |
| Ultra package posted | [`3061079d`](https://github.com/tradingartofwar/the-lonely-runner-conjecture/commit/3061079d3b0f7fccb36f60e8ba0b5fa234da139b) | Reports, verifiers, synthesis, and continuity/source updates |
| Final LR 1 mathematical follow-up | [`cc4328c6`](https://github.com/tradingartofwar/the-lonely-runner-conjecture/commit/cc4328c68671540284dd9796931103b43a845b1b) | All six core windows and exact triple-exclusion correction; LR 2 recovery baseline |
| Focused outside-review entry point | [Affine note, version 1](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/7093e1cf70ecfb4a06c72d98fe02871c42d17867/notes/REVIEW_AFFINE_FAMILY.md) | One self-contained candidate, with code/data baseline `25f8352944700a3060dab03dc42a75e23524a5c4` |

Thus the Ultra work was made available on GitHub for inspection. The repository had no GitHub releases at recovery. No journal/preprint publication of our results or outside referee acceptance was established by this audit. The existing record says no outside researcher was contacted. A literature preprint cited in the review is another author's work, not publication of this project's results.

## What was preserved and verified

The live tree at `cc4328c68671540284dd9796931103b43a845b1b` contains 139 files. LR 2 reconstructed and checked all 139 against their Git blob hashes. The old working directory matched 129 directly; the remaining ten were missing or stale governance, licensing, and overview files retrieved from the pinned remote revision. No research or Ultra artifact was missing from the remote tree.

At the initial recovery, the Ultra directory contained 20 files: six reports, eight Python verification/runner files, five JSON results, and the manifest. All 19 artifact SHA-256 entries in the manifest, plus its consolidated-report hash, matched. Comparing the original reviewer output directory with the public package found preserved mathematical reports and results, with portable path substitutions where needed. The root verifier/output additionally contains the documented post-review correction. Its earlier versions remain in Git history.

| Reviewer assignment | Preserved report | Main contribution |
| --- | --- | --- |
| Early families | [early.md](reviews/2026-09-25-ultra/early.md) | Finite reductions, modular witnesses, replacement classification, overlap/chains, and known Fibonacci status |
| Overlap | [overlap.md](reviews/2026-09-25-ultra/overlap.md) | Local tree failure, pair-total information loss, gcd contact refinement, and growing-residual deduction |
| Affine families | [affine.md](reviews/2026-09-25-ultra/affine.md) | Steps A–D, auxiliary-optimum approximation, alternative tiling argument, and scoped reference/block extensions |
| Perturbations | [perturbations.md](reviews/2026-09-25-ultra/perturbations.md) | Five perturbation families, strict witnesses, maxima, and equality distinctions |
| Tilings | [tilings.md](reviews/2026-09-25-ultra/tilings.md) | Positive/signed escape geometry and the proposed core-boundary extension |
| Package | [package.md](reviews/2026-09-25-ultra/package.md) | Evidence independence, source hashes, certificate scope, dependency metadata, and review positioning |

The complete read-only command was rerun successfully from the reconstructed snapshot:

```bash
python -B reviews/2026-09-25-ultra/verify.py
```

All seven groups passed: early, affine, overlap, tilings, perturbations, package, and root. The package group checked 165 recorded source hashes and 755 endpoint-certificate groups. These are bounded, overlapping checks, not 755 independent mathematical replications or a mechanical proof of every unbounded implication. No archived output was rewritten. The original 25 checker tests were reported passing in the Ultra package; LR 2 did not rerun them because no checker or research code changed.

No substantive Ultra output was found only in the old workspace. Available LR 1 retrieval corroborated the review discussion and final correction, but did not supply a complete verbatim transcript or a final answer to the last handoff request. This recovery therefore verifies the located artifacts and retrieved decisions; it does not claim that every sentence of LR 1 was recovered. Unrelated records returned by retrieval were excluded.

## Findings that must survive the thread change

**Status.** Six fresh-context Astra Ultra reviewers found no fatal mathematical defect within their stated scopes. Their scopes were divided; six reviewers did not each re-prove the entire project. The candidates remain HYPOTHESIS/proof candidates. External correctness review and originality remain unresolved. Organize the work by shared mechanisms and assumptions, not by counting notes as independent discoveries.

**The overlap obstruction and its correction.** For speeds `{0,1,4,5,6,7,11,16}`, core `{1,4,5}`, and window `[9/32,3/8]`, the actual opening has width `1/896`, but the best of all 16 tree bounds is `-23/29568`. An abstract event arrangement can preserve every single/pair duration while eliminating uncovered time. That arrangement is not another constant-speed runner configuration.

The subsequent all-window check is essential: two other windows for this same configuration have positive tree bounds `1/352`, certifying actual intervals `[41/88,15/32]` and `[17/32,47/88]`. Consequently the local failure does not defeat the method for this configuration. In the missed window, speed geometry excludes every triple overlap; adding that extra fact makes full pair inclusion-exclusion recover `1/896` exactly. This is information beyond pair totals alone. Section 7 and the root verifier preserve it.

**The affine mechanism.** Fixed coefficients and a fixed core yield the proposed estimate `L_U-K/(2q) <= L(q) <= L_U`. Strict auxiliary room eventually survives rounding to an actual time. Balanced-block and certain reference-change corollaries broaden its scope. They do not cover arbitrary speed sets with coefficients changing with `q`, nor does zero auxiliary margin imply strictness. The versioned Steps A–D note remains the clearest first outside-review object.

**Core boundaries.** The formerly proposed core-threshold question received a conditional one-sided extension in the Ultra review, preserving the sufficient positive/signed cutoffs `q>=8` and `q>=17`. A third active controller at a core boundary can turn an apparent interval start into an isolated valid instant. These are proposed corollaries, not newly established general theorems.

**Package limitations.** Four historical selected-source manifests omit the transitive `scripts/analyze_residual_overlap.py` dependency; the full pinned commit preserves it. This is a provenance-completeness issue, not a demonstrated wrong calculation. Preserve historical outputs. Future manifests should record the dependency closure or explicitly describe their selection. The dated literature update and reading limits are in [SOURCES.md](notes/SOURCES.md); LR 2 has not conducted another literature audit.

## Next useful work

**September 25 priority review:** [LR2_REVIEW_PRIORITIES.md](notes/LR2_REVIEW_PRIORITIES.md) sharpens the proposal: use established graph inequalities and speed-derived bounds on necessary triple intersections; require a useful selection rule; retain equality certificates. It includes five exact nearby controls and identifies underemphasized Ultra deductions. The two successful LR 1 windows are reflections. A referenced original tiling console trace was also restored; its substantive content was already preserved.

The current internal question is: **What small amount of additional runner geometry lets an overlap certificate detect a real opening?** Start from the exact triple-exclusion certificate already obtained for `{0,1,4,5,6,7,11,16}` and formulate a statement that could fail in a nearby case.

Keep three possible targets separate: recovering every positive-duration local opening; finding at least one useful core/window for a configuration; and handling isolated equality times. Success or failure for one target does not settle the others. A finer subdivision, a different core, and higher-intersection information are different possible refinements, not an established combined theorem.

The external-review track is separate: consolidate the affine proposition and ask correctness and prior-art questions about the pinned note. No outreach is authorized merely by recording that option. The LR 2 recovery itself adds continuity documentation only; it does not merge PR #3 or launch a new mathematical search.

Continue surfacing significant patterns, counterexamples, scope corrections, and literature connections promptly, as requested in LR 1. Preserve exact evidence and explain why each matters for the guiding question.
