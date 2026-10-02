# Package, evidence, and positioning review

**Review baseline:** `ea482f54edae4775621bc69c1fb7359291f31ddd`, PR #3 branch `research/near-doubling-overlap-2026-09-24`. **Reviewed:** September 25, 2026. This is a fresh AI review of the package and evidence architecture, not external human review or formal verification. No repository files were changed by this reviewer.

## Assessment

The package is unusually explicit about scope, AI provenance, isolated equality times, and the difference between finite computation and an unbounded argument. I found no corruption in the checked source hashes or stored endpoint certificates, and no blocking software failure in the checks I ran. The main substantive status correction is that the reported finite-runner frontier advanced to **15 total runners in a September 24 revision**, whereas the repository currently records the earlier fourteen-runner version. The main reviewability problem is accumulated scope: many notes are successive refinements or applications of shared mechanisms, not independent candidate discoveries.

For an outside mathematician, the best first object remains **`notes/REVIEW_AFFINE_FAMILY.md`, Steps A–D**. It states one clean restricted theorem, contains its whole proposed proof, exposes its hypotheses, and has a directly checkable rational example. The strictness conclusion and elementary mechanism are the potential mathematical interest; merely proving the usual non-strict eight-runner conclusion would not move the existing finite-runner frontier. Novelty remains unresolved.

## Findings, ranked

### P2 — The current frontier statement needs its dated update

**Locations:** `notes/SOURCES.md` S7; `HANDOFF.md` “Research baseline and limits”; current remote `RESEARCH_PLAN.md`, “Strategic choice”.

The primary arXiv record for Allikvere is now *Fourteen and fifteen lonely runners*, `arXiv:2609.02604v2`, revised **September 24, 2026, 11:58:42 UTC**. Its abstract reports proofs for fourteen and fifteen total runners and publicly archived code/certificates. S7 accurately describes the pinned September 2 v1, but it is no longer the latest reported frontier. Independently, `RESEARCH_PLAN.md` still calls fourteen the next case beyond the cited thirteen-runner result; that sentence was already behind S7 v1.

**Action:** Preserve S7 v1 as reading history; append v2 and the exact reading limit. Update the live handoff and strategy sentence. Say “preprint reports fifteen” until the proof/computation has actually been audited. This corrects orientation; it neither strengthens nor weakens the repository's internal certificates.

**Source:** <https://arxiv.org/abs/2609.02604v2>. I read the abstract, comments, and submission history only. I did not audit the proof, archives, or certificates.

### P2 — The default test command validates the checker, not the research package

**Locations:** `tests/test_checker.py`; `notes/CHECKER_VALIDATION.md`; reproduction sections of newer notes; scripts' `main()` routines.

`python -m unittest discover -s tests -v` passes all **25 tests**. These are meaningful checker tests: exact fixtures, reference/normalization invariants, input/resource rejection, CLI behavior, and 162 bounded comparisons of different algorithms. However, discovery currently runs only `tests/test_checker.py`; it does not execute the unbounded-family reductions, finite remainders, phase geometry, or stored research certificates.

The research scripts have extensive internal assertions, but generally regenerate their JSON output when run. The notes disclose that those runs are finite diagnostics and that recent scripts did not rerun the wider suite. I found no false claim that the 25 tests certify the new mathematics. The practical risk is that a new reviewer sees “25 tests pass” and mistakes it for a package-wide check.

**Action:** Add one clearly named read-only certificate verification entrypoint and a small claim-to-command table. Keep the core checker suite as one layer. Provide separate commands for (a) verifying archived certificates, (b) regenerating a selected experiment in a clean checkout and comparing bytes, and (c) reviewing each analytic implication. A full rerun of all historical scripts is unnecessary for a focused external review.

As evidence that a small verifier is practical, this review's `audit_package.py` independently checks stored endpoint arithmetic without importing any project module. Its limitations are detailed below; it is not an unbounded proof checker.

### P3 — Four source manifests omit one transitive import

**Locations:** `experiments/affine_family.json`, `experiments/core_transfer.json`, `experiments/fast_cluster.json`, `experiments/pair_selection.json`, and their generating scripts' source-path lists.

All recorded hashes tested match the current verified source/evidence bytes. Nevertheless, these four manifests omit `scripts/analyze_residual_overlap.py`, which is imported through `scripts/analyze_phase_discrepancy.py`. A static import-closure traversal reproduces this omission. The current values are not thereby shown wrong: this is an import/provenance completeness defect, and no altered numerical dependency was demonstrated. The pinned full Git commit still identifies the omitted file.

Earlier evidence uses narrower provenance records, sometimes only a checker hash. `reference_patterns.json`, for example, records a base commit but no hashes of its two input JSON files. This is acceptable as historical evidence at a pinned repository revision, but should not be described as uniformly complete source manifests.

**Action:** For future evidence generations, derive the import/input manifest automatically or explicitly distinguish “selected source hashes” from “all dependencies”. Do not rewrite historical evidence solely to replace its historical pin. A new verification manifest can attest to the intact archived output.

### P3 — Consolidate the claim inventory before widening the public review request

**Locations:** `HANDOFF.md` “What exists now” and continuations; `notes/FAST_CLUSTER.md`; overlap and perturbation/tiling note sequences; `CLAIM_STATUS.md`.

The scope labels themselves are generally careful. In particular, `signed_tilings.json` says repeated geometry is not independent evidence; `SIGNED_TILING_RULE.md` says forty certificates include repeated intervals; the core-transfer/pair-selection evidence distinguishes eleven decompositions from ten speed sets. I found no explicit inflated global candidate count to correct.

However, the many historical cutoffs, continuation sections, and large verification counts are hard to interpret as a current mathematical inventory. `CLAIM_STATUS.md` defines a vocabulary, not a ledger of actual claims. There are 30 experiment JSON files, but they are not 30 independent theorem candidates.

**Action:** Add a compact claim table with hypotheses, strongest current conclusion, superseded statements, evidence command, and review status. Group the work into: known reconstructions; exact checker/case evidence; local coverage and discrepancy estimates; the fixed-core affine theorem; perturbation/tiling geometry and actual-time transfer. Preserve historical notes but give the reader one current statement per thread. Keep changes to claim status tied to the precise scope of completed review.

## Evidence actually checked

The parent reviewer verified the local mathematical sources, scripts, evidence, checker, tests, and handoff against the remote tree. I fetched the current `README.md`, `CLAIM_STATUS.md`, and `CONTRIBUTING.md` directly at the pinned commit, and read the parent's verified current `AGENTS.md` and `RESEARCH_PLAN.md` snapshots. Stale local copies of governance files were not treated as remote defects.

Executed, without rewriting experiment outputs:

```bash
python -m unittest discover -s tests -v
python -m scripts.build_demo --check
python reviews/2026-09-25-ultra/audit_package.py \
  .
```

Results:

| Check | Result | What it establishes |
| --- | --- | --- |
| Core checker tests | 25 passed, approximately 0.5 seconds | Bounded software regression evidence described above |
| Demo regeneration check | Matched | Committed demo agrees with checker/templates |
| JSON parsing | All 30 experiment files read | Files are parseable, not that every value was validated |
| Recorded hashes | 165 checked, all matched | 151 mapped hashes plus 14 legacy checker/script/input hashes agree with the reviewed bytes |
| Endpoint-certificate arithmetic | 755 groups passed | Each recovered interval is common to all rows, has positive width, and stays within the displayed safe phase strips |
| Seven-speed certificate subset | 723 occurrences, 683 distinct speed-set/interval pairs, 536 distinct speed sets | Rational intervals exist for these represented configurations; duplicate occurrences are not additional configurations |
| Pinned affine reproduction baseline | Script and JSON blobs identical at `25f8352` and current reviewed bytes | The review note's older pin has not silently drifted from those two current artifacts |

The endpoint verifier recognizes lists of rows with `speed`, `integer_part`, `phase_left`, and `phase_right`. For each row it reconstructs the interval endpoints as `(integer_part + phase)/speed`, requires the same endpoints across rows, and checks integer positive distinct speeds and `1/8 <= phase_left < phase_right <= 7/8`. The midpoint is strictly safe, and affineness with a fixed integer part certifies the whole closed interval. It imports only standard-library modules. Of the 755 groups, 32 are partial-core certificates rather than seven-speed configurations.

This checks the displayed certificate arithmetic independently of the project's interval routines. It does **not** validate every surrounding label, the derivation of a claimed family cutoff, completeness of finite remainder selection, all stored full-union hashes, isolated-only cases, or every maximum. Those need the specific proof/evidence reviews. It also does not turn AI review into external independence.

The two pinned affine blobs were fetched through the GitHub API and compared with local Git blob hashes:

- `scripts/analyze_affine_family.py`: `4d59908bdcdd3698104517a561c474ba86778b50`
- `experiments/affine_family.json`: `f1ecd3c385014911a27c0bfa65e79566c731dbb5`

## What “independent” currently means

The checker genuinely has different search algorithms: Method A intersects closed rational safe intervals; Method B enumerates triangle-wave corners and affine crossings and directly evaluates candidate distances. They share parsing, normalization, `Fraction`, and distance evaluation. This is useful algorithmic crosschecking, not wholly independent software or formal verification.

The boundary-cell reconstructions in `analyze_core_transfer.py` and frozen-phase reconstruction in `analyze_affine_family.py` also supply a real second computational route. Their shared helpers create correlated failure possibilities. Dozens of scripts that import the same `phase_certificate`, `feasible_intervals`, `boundary_certificate`, and phase geometry routines do not multiply independence. Direct endpoint certificates are therefore an especially useful part of the package: a reviewer can verify their rational arithmetic without adopting the whole implementation.

The project's disclosure in `REVIEW_AFFINE_FAMILY.md` is accurate: generation, internal reproduction, and agreement among AI reviewers do not themselves constitute independent external mathematical certification.

## Literature and best external review object

I reread Jain–Kravitz, *Relative Lonely Runner spectra*, `arXiv:2411.12684v2`, definitions and Sections 1.2–1.4, Theorem 1.1, and the opening of the Section 2.1 outline. Its two-dimensional relative-spectrum framework and fast-runner discussion are a genuine match to the affine family's auxiliary torus. The paper gives much richer spectral structure, but the repository's strict threshold for its particular torus still needs justification; merely naming Theorem 1.1 does not establish that threshold. The finite-frequency obstruction plus elementary rounding is the most focused object for correctness and prior-art comparison. I did not audit the full paper, and this reading does not establish novelty or priority.

Recommend sending an external reviewer only the versioned affine note, its standalone rational witness, and an optional concise certificate appendix first. Ask them separately whether the proof is correct and whether its proposition/mechanism is an existing corollary. The latest signed local-tiling rule is a second object after that: its coefficient-uniform cutoff is structurally different, but the larger hypothesis/case apparatus makes it a less efficient initial review request. This recommendation does not rank their eventual research value.

Additional primary-source reading during this audit:

- <https://arxiv.org/abs/2604.23906>: abstract/history confirm the September 1 v2 reporting thirteen total runners; no proof or code audited.
- <https://arxiv.org/abs/2609.02604v2>: abstract/comments/history, as above.
- <https://arxiv.org/html/2411.12684v2>: the relative-spectrum material stated above.
- <https://arxiv.org/html/2609.23952v1>, Poliakova, *More (shifted) runners, less loneliness*: abstract/introduction, definitions and theorem statements, plus the displayed uniform-rule construction inspected as a fresh literature lead. It concerns arbitrary shifts, not this common-start theorem, and supplies no certification of the repository's claims. No independent audit of its proof.
- Direct retrieval of <https://arxiv.org/abs/2509.14111v2> failed; no extra claim about that source was adopted from the failed request.

No broad literature/novelty search, code-archive audit, all-script regeneration, full proof-family review, or outward communication was performed by this reviewer.
