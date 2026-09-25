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

**Current direction — distinction audit:** Vance explicitly asked to change the angle of attack and audit what is hidden inside “collective coverage,” rather than force another proof extension. [DISTINCTION_AUDIT_2026_09_25.md](notes/DISTINCTION_AUDIT_2026_09_25.md) reviews the mathematical distinctions, identifies exact information loss, supplies physical matched-summary cases, and proposes three bounded next investigations. The +7/+9 family continuation is parked. Retain the principle: when an explanation fails, check for conflated distinctions; when a distinction appears, test whether it changes the chosen target.

The existing x<y<=80 domain outside {1,4,5,6,7} has 2775 inputs and 2771 labelled single/pair-duration signatures. Exactly four collision pairs occur: (2,23)/(2,69), (2,25)/(2,75), (8,25)/(8,75), and (21,25)/(21,75). The first three also preserve all joint duration moments. Their local component counts change 2 to 3 intervals, 3 intervals to 4 plus a singleton, and 2 to 3 intervals, respectively. In the 2/75 case the isolated t=3/8 has controllers 75 entering safety at phase 1/8 and core speed 5 leaving at 7/8. These are actual common-start speed configurations with the same core/J/threshold, not whole-speed scaling or abstract event arrangements. All four pairs have equal positive U; there is no physical same-signature/different-duration or different-existence example in this finite domain.

The matched quantities are duration moments, not the entire arithmetic description. Pair gcds differ in all four classes and already distinguish these examples; for example gcd(6,25)=1 versus gcd(6,75)=3. Do not present these as matches of every statistic the project has ever used, or infer that full chronology is necessarily the cheapest repair.

The 21/25 and 21/75 triples differ: T_(6,21,y),T_(7,21,y) are (0,3/800) versus (1/300,1/2400), but the sum is unchanged. B21=[9/32,7/24) union (55/168,19/56) lies inside B7 union B6, while B2 is empty. Thus replacing 2 by 21 preserves the entire allowed set for any common fourth blocker. Also B8=(23/64,3/8] is disjoint from B6 and B7. These implications explain why pair moments determine U for every y in each fixed-x class 2,8,21. The audit proves a scoped irrelevance statement instead of chasing a different-U collision in those already-excluded classes.

Exact R and E already determine U. For four blockers, U=-E+P2-P3+Q, so the scalar P3-Q is the missing duration correction when only singles/pairs are retained. Complete joint moments determine all state masses and U, but lose temporal arrangement and isolated contacts. The existing Ultra zero-clear alteration with unchanged pair data is still an abstract event model; it does not establish a physical matching pair. Ratio plus gcd reconstructs the full speed pair; the compression occurs when replacing the ratio by an overlap fraction or applying a coarse error estimate. Failure of a bound, actual empty J, and failure across all core windows remain separate.

Both requested stress cases are rechecked. Tight extras 6/7/11/13 have E=R=1445/96096, U=0, and only t=3/8. Extras 56/113/64/72 have E=1045/911232, R=5049/202496, U=6193/260352, and 11 positive components. Closed safe-lap labels (0,1,1,2,2,4,4) for speeds (1,4,5,6,7,11,13) give the singleton with lower controller 11 and upper controllers 5,13. Labels (0,1,1,20,41,23,26) for (1,4,5,56,113,64,72) give [329/904,335/904], width 3/452. This extends the already-constructed blocking lap lattice with explicit closed safe cells; the full general polyhedral/zonotope program remains unimplemented.

Reproduce with `python -B reviews/2026-09-25-lr2/check_distinction_audit.py --check`. The standalone archive pins its script and all-signature digest. It contains matched states/moments/components, stress and lattice cells, the ratio comparison, the dominated-constraint argument, and the reproduced abstract alternative. A separately structured periodic-integral signature calculation and phase-event reconstruction agree; the existing interval-intersection checker additionally agrees on all 14 actual-case component lists, including points. Older evidence and source scripts remain unchanged.

Three prioritized follow-ups are concrete: (1) classify physical moment collisions by endpoint residues, using x=11 as a nontrivial duration anchor and x=3 to ask whether complete-moment collisions cross the y mod 8 empty/contact distinction; (2) use the actual matched pairs to test the minimum contact/ordering record, challenged by earlier frozen-snapshot and third-controller controls; (3) minimize uncovered mass in a 16-state moment relaxation and add only speed-certified support/implication constraints, measuring their actual benefit. No new scan domain, solver campaign, outside outreach, or next family extension was launched in the audit.

**Earlier continuation — an unbounded triangle exclusion:** [UNIFORM_TRIANGLE_CERTIFICATE.md](notes/UNIFORM_TRIANGLE_CERTIFICATE.md) supplies a complete proposed certificate for `{0,1,4,5,q,q+8,2q+1,v}`, integer q>=28, arbitrary v>=q, distinct speeds, reference 0, threshold 1/8, and the same J. If x=qt-j and q,2q+1 block, then `-1/8<x<1/16-t/2`. Consequently `17/8<x+8t<23/8`, so q+8 is strictly safe. The triple is impossible for every admissible q; all four cannot block together either.

Keeping the triangle and leaving v isolated gives `U>=L-D_q-D_(q+8)-D_(2q+1)-D_v+O_qB+O_qA+O_AB`, A=q+8,B=2q+1. Six fixed affine strips evaluate the three pairs exactly using a periodic quadratic primitive; their areas total 41/3840. No q- or v-dependent lap list is needed by the certificate. For all v>=q, the exact uniform expression H(q) is at least `41/3840-5/(8q)-11/(16(q+8))-19/(16(2q+1)) >= 41/3840-61/(32q)>0` from q=179. The 151 q values 28..178 all have H(q)>0. Additional lower diagnostics give nonpositive H only at 6,8,9,11,12,13,14,15,17,20,24,27; q=7 is excluded because A=B. These are certificate failures, not actual counterexamples.

At q=28, H=587/153216, while the same-budget near-pair bound is -11/2432 and the best of the three fixed-pair bounds is -163/51072. At q=27,v=43 the best of all six exact one-pair bounds is -1777/893970, but the triangle gives 2923/595980 versus actual 31309/1787940. At q=6,v=30 the triangle still fails despite positive duration 3/560. Changing offset +8 to +7 or +9 at q=56 gives positive triple durations 37/25312 and 13/25312, respectively. Do not transfer the exclusion to arbitrary offsets.

Reproduce with `python -B reviews/2026-09-25-lr2/check_uniform_triangle.py --check`. The six bands are reconstructed from residual integer labels. Direct phase partitions crosscheck three singles, three pairs, and zero triple for 172 finite q values, including the 151 proof remainder values. Eight full four-blocker controls, two offset countercontrols, and three large formula-only controls also pass; the largest v is 10^40. A separate session check with the existing safe-interval checker agrees on all eight full durations. Counts overlap and are not independent proof replications. The analytic tail and finite remainder, not the large examples, establish the proposed unbounded implication. The archive pins its standalone script. All source scripts and historical outputs remain unchanged.

This narrows the existing near-doubling family by imposing A=q+8, while strengthening its certificate below the prior broader q>=242 cutoff. It is not a general-conjecture result, an all-reference result, or an externally reviewed proof. Its proposed next +7/+9 test is parked under the newer distinction-audit direction above; do not resume it merely because it was the earlier next step.

**Earlier continuation — four blockers and cycle corrections:** [FOUR_BLOCKER_CYCLE_CORRECTIONS.md](notes/FOUR_BLOCKER_CYCLE_CORRECTIONS.md) compares the seven existing overlap-placement cases and the original 6/7/11/16 tree failure, keeping core 1/4/5 and J=`[9/32,3/8]`. All six pair overlaps are positive in each of the five fast cases. Compatibility exclusions improve the best tree in five of eight inputs. Four-way blocking of positive duration in 56/64/72/112 and 309/320/328/619 forces every graph satisfying the active-forest condition to be a global forest. This limits that certificate class, not all possible pair-data inequalities.

Subtracting the active cycle rank gives a general count identity; for a connected graph with one cycle it costs just the intersection duration of that cycle's vertices. The best of 12 triangle-with-leaf graphs and three four-cycles improves the tree in seven of eight cases; the remaining tree is already exact. The four-cycle selector omits the cheapest of three perfect matchings and subtracts Q. Triangle-with-leaf remains necessary in the old 6/7/11/16 control, where the best four-cycle still has negative bound.

For 56/64/72/113, six 56/113 overlap intervals keep speed 64's phase strictly inside (1/8,7/8). This excludes triple 56/64/113 and therefore Q. The best tree is 58073/3644928, the best compatibility/four-cycle bound is 72311/3644928, and the best five-edge bound is 11369/520704 versus actual 6193/260352. Its two triangle corrections are zero and 25/50624; the residual gap is exactly 1/512. For 56/64/72/112, Q=1/896 on (335/896,3/8]. The tree, one-cycle, and five-edge bounds are 761,851,911 over 32256, versus actual 954/32256. The gap for a five-edge graph missing ij is exactly the duration when only i and j block; all six such masses are positive in all five fast inputs.

Reproduce with `python -B reviews/2026-09-25-lr2/check_four_blocker_cycles.py --check`. All 120 nonempty moments agree between lap-interval joins and a separate phase partition. All 64 graphs in each case satisfy the corrected gap identity, and each graph's 16 logical states are checked. These overlapping counts are not independent proof replications. An additional session check with the existing safe-interval checker confirms all eight local durations and the equality-only 6/7/11/13 case at t=3/8. The archive pins its standalone script and preserves all higher-intersection lap witnesses and graph options. Older evidence remains unchanged.

This was bounded analysis of existing examples, not a uniform algorithm: computing those moments enumerates speed-dependent interval lists. The proposed speed-derived cycle bound has now been supplied for a structured subfamily in the latest entry above. Keep equality and useful window selection separate. General selection and independent review remain open.

**Earlier continuation — two variable speeds:** [TWO_SPEED_SPARSE_TRANSFER.md](notes/TWO_SPEED_SPARSE_TRANSFER.md) transfers the sparse graph to `{0,1,4,5,6,7,x,y}`, x<y. Two triple types still suffice because blockers 6 and 7 are disjoint on J=`[9/32,3/8]`. Their feasibility is an explicit integer lap-lattice test, `|ym-xn|<(x+y)/8`, with local lap bounds. The known 16/23 pair closes the old small I but leaves `[17/48,47/128]` of length 5/384 in J. The genuine empty-J family is `(3,8m)`.

The window rule chooses H=`[25/56,15/32]` when x=3 or x>=34, and J otherwise. The existing fast bound handles x>=34; x=3 leaves one blocker, with a tail from y>=12 and four small controls. For the other 27 x<34, fixed conservative graphs give `L_x-C_x/y>0` above tabulated cutoffs. The 819 remaining pairs have 815 positive sparse bounds; `(2,3),(10,11),(11,13),(11,26)` retain t=3/8. Only up to four smaller-speed occurrences in J are needed by the certificate generator; y's laps are never enumerated. A separate 2775-pair diagnostic box found no missed positive J openings and exactly ten empty cases `(3,8m)`, m=1..10. The diagnostic box overlaps the proof checks and is not an unbounded proof. Reproduce with `python -B reviews/2026-09-25-lr2/check_two_speed_transfer.py --check`.

This is a certificate/window-selection refinement for the already-covered two-variable family, with the written synthesis still awaiting independent review. The local lap-lattice LTCM has now been applied; the full general polyhedral model has not. The proposed comparison with existing four-blocker inputs is completed above; do not restart the earlier one-/two-variable existence results as new findings.

**Earlier continuation — sparse graph selection:** [SPARSE_OVERLAP_SELECTION.md](notes/SPARSE_OVERLAP_SELECTION.md) carries the occurrence insight back to a small runner graph. For `{0,1,4,5,6,7,11,w}` on J=`[9/32,3/8]`, 6 and 7 never block together, leaving just two possible triple types. Two integer-existence tests determine which cycles may be retained; at most 32 edge masks select the largest valid pair weight. Five periodic interval evaluations supply the needed durations without enumerating w's laps.

The fixed family now has a compact overlap certificate: an ordinary star gives `U_J >= 31/9856-15/(16w)>0` for all integer w>=299. All 292 admissible smaller w were checked exactly; 288 give positive lower bounds, while w=3,10,13,26 have zero duration and valid t=3/8 (w=10,26 also t=5/16). Only 79 finite bounds equal the full duration, so do not overstate exact recovery. Reproduce with `python -B reviews/2026-09-25-lr2/check_sparse_overlap.py --check`. The unbounded synthesis is a proof candidate pending independent review. Existence for this family was already covered more simply in VARIABLE_SPEED_FAMILY.md; this does not add a new family or an all-reference result.

That proposed second-variable test is completed in the latest entry above. TWO_VARIABLE_SPEEDS.md already covered existence for the family; this continuation concerns sparse compatibility information and window choice. Arbitrary-speed core/window selection is still open.

**September 25 LTCM continuation:** Vance named **LTCM — Languages That Carry Models**, asked about unused representations, dimensions, relational information, and runner thought experiments. [DOMAIN_CONNECTIONS.md](notes/DOMAIN_CONNECTIONS.md#september-25-ltcms-and-runner-thought-experiments) records the framing and limits. The shared-clock experiment is now carried out in [LAP_LABELLED_CONSTRAINTS.md](notes/LAP_LABELLED_CONSTRAINTS.md).

The useful distinction is the **lap occurrence** behind an overlap. In the original w=16 window, speed 16 overlaps runner 6 only around lap 5 and runner 11 only around lap 6. The abstract triple has no consistent occurrence assignment. Keeping individual blocking intervals as graph vertices gives exact maximum-forest duration certificates in all five controls w=13..17, including the w=14/17 cases where the earlier fixed runner graph was inconclusive. A self-contained interval-union argument explains this; no novelty or general successful-window theorem is claimed. All five certificates agree with direct phase partitions. The w=13 equality point survives at t=3/8. Reproduce with `python -B reviews/2026-09-25-lr2/check_lap_constraints.py --check`.

That continuation proposed asking whether speed arithmetic can select a small collection of occurrence incompatibilities **without reconstructing every interval**; the latest sparse result above answers this for one already-covered fixed family. The complete occurrence-forest construction itself explains existing schedules and does not force positive slack. Earlier graph-level pair-data limitations remain valid because the refined representations contain additional occurrence information.

**September 25 priority review:** [LR2_REVIEW_PRIORITIES.md](notes/LR2_REVIEW_PRIORITIES.md) sharpens the proposal: use established graph inequalities and speed-derived bounds on necessary triple intersections; require a useful selection rule; retain equality certificates. It includes five exact nearby controls and identifies underemphasized Ultra deductions. The two successful LR 1 windows are reflections. A referenced original tiling console trace was also restored; its substantive content was already preserved.

The current internal question is: **What small amount of additional runner geometry lets an overlap certificate detect a real opening?** Start from the exact triple-exclusion certificate already obtained for `{0,1,4,5,6,7,11,16}` and formulate a statement that could fail in a nearby case.

Keep three possible targets separate: recovering every positive-duration local opening; finding at least one useful core/window for a configuration; and handling isolated equality times. Success or failure for one target does not settle the others. A finer subdivision, a different core, and higher-intersection information are different possible refinements, not an established combined theorem.

The external-review track is separate: consolidate the affine proposition and ask correctness and prior-art questions about the pinned note. No outreach is authorized merely by recording that option. The LR 2 recovery itself adds continuity documentation only; it does not merge PR #3 or launch a new mathematical search.

Continue surfacing significant patterns, counterexamples, scope corrections, and literature connections promptly, as requested in LR 1. Preserve exact evidence and explain why each matters for the guiding question.
