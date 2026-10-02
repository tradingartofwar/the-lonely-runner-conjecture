# Fresh review: five perturbation families

Reviewed 25 September 2026. Target: PR 3, live commit `ea482f54edae4775621bc69c1fb7359291f31ddd`. The coordinating reviewer verified the supplied research-file bytes against that commit; the workspace's synthetic Git HEAD/index is not used as research provenance. Repository files were not edited or regenerated.

## Findings by severity

**No critical, high, or medium mathematical defect found in the audited claims.** In particular, I found no missing sign case, omitted finite remainder, unsupported passage from finitely many scales to all scales, or confusion between a witness and a maximum in these five notes. The all-scale conclusions are restricted to their stated selected reference and parameter families. They do not prove the general conjecture, every reference runner, or novelty.

No low-severity mathematical correction is requested. The following are review observations and simplifications, not proof-blocking findings:

1. **The larger evidence package contains substantial intentional redundancy.** For the strictness conclusions in FOUR_PERTURBATIONS §5, UNEQUAL_PERTURBATIONS §4, and TWO_DOUBLED_OFFSETS §4, full actual allowed-set reconstructions and exact maxima are unnecessary once the rational remainder witnesses are directly certified. A minimal proof certificate needs the all-scale rounding argument, exact auxiliary interval endpoints where used, the exhaustive remainder index set, and one strict rational point per remainder. The existing extra checks provide useful diagnostics but should not be counted as independent mathematical results.
2. **The tiling results and reachability results are logically distinct.** The geometric lemma in UNEQUAL_PERTURBATIONS §3 and the criterion/parity argument in TWO_DOUBLED_OFFSETS §§2–3 explain why openings exist. The actual uniform cutoffs in their §4 arguments are supplied by explicitly certified widths and rounding. Even without using the geometric lemmas, those positive-width certificates plus the remainder certificates suffice for the stated all-q results. Conversely, the geometric lemmas alone do not establish those cutoffs or reachability. The notes keep this distinction correctly.
3. **Symmetry does not justify discarding all sign cases in the actual-time proof.** Reversing all offsets reflects auxiliary phase geometry and preserves its interval widths, but the fixed-x actual grid must still be checked or transformed with its core phase. The complete sign enumeration in the evidence is appropriate. The notes explicitly acknowledge geometric repeats and do not present raw counts as independent samples.

## Proof logic audited

| Note and sections | Review conclusion |
| --- | --- |
| SCALED_PERTURBATION §§2–3 | The circle-spacing upper bound and equality classification are valid. At a core-optimal time the exceptional distance is exactly `||t||`, giving both the value `1/7` and the complete peak set, including the `7 divides q` earliest-time exception. The broader coprime-exception pre-jump argument is also valid for its stated `q>=2`. |
| SCALED_PERTURBATION §§4–5, 7 | Old-touch survival/direction classification, opposing-endpoint completeness argument for new isolated contacts, and six signed congruence classes withstand review. The normalized-clock waiting-time explanation and fixed-horizon Lipschitz bound distinguish the two limits correctly. |
| TWO_PERTURBATIONS §§3–4 | The strict-open-arc count is `ceil(2dq)`, including integer-boundary cases. The `q=4` exception at target `1/6` is real and handled by the separate unit-offset phase calculation. Its half-interval construction, all four signed choices, complete peak table, and earliest-time formula are sound. |
| FOUR_PERTURBATIONS §§3–5 | Quarter tiling and the actual `q=2 mod 4` equality survivors are correctly separated. At `x=1/5`, four centers among five grid positions force a gap of at least `2/5`, even with repeated centers. Nearest-grid rounding has error at most `1/(2q)` and yields strictness for `q>=7`; all 64 remainder inputs are present. |
| FOUR_PERTURBATIONS §§6–8 | The positive-gap/missed-grid control and frozen-singleton/actual-interval control are genuine. The `1/4` maximum criterion has a valid upper bound and a complete equality-time reduction. Its signs and q residues agree with the independent maxima. No universal maximum staircase is claimed. |
| UNEQUAL_PERTURBATIONS §§2–4 | For three unit arcs and one rate-m blocker, zero uncovered measure forces each complementary gap of length `3/(4m)` to contain an integer number of quarter arcs; hence `m` divides 3. The argument handles open endpoints correctly. For `m=2`, all 64 vectors have certified positive intervals. Signed slopes, doubled-rate widths, the strict inequality `q>1/w`, and the exact 44-case remainder are correct. |
| UNEQUAL_PERTURBATIONS §5 | The doubled offset repeats grid phases when `gcd(2,q)>1`; the corrected multiplicity bound is valid. All eight missed-strictness controls are included. Their maxima are independently corroborated rather than inferred from the chosen witnesses. |
| TWO_DOUBLED_OFFSETS §§2–4 | The first Fourier coefficient forces the two unit centers to be antipodal. Filling the two remaining quarter gaps then forces exactly the stated `3/8,5/8` doubled-phase shifts; this establishes both necessity and sufficiency. Eliminating x forces `4 | d`, leaving signed unit indices 5 and 7 and then the even/odd contradiction. This works at every real x and for all 96 vectors. All 48 remainder inputs are present and have strict witnesses on the prescribed quarter/fifth grids. |
| TWO_DOUBLED_OFFSETS §5 | The changed-coefficient control satisfies the criterion. All auxiliary safe phases have denominator dividing 8, so no integer q can realize core phase `3/16` there. This obstructs only that schedule. The separate actual `q=5` maximum of `1/4` has the stated complete two-point peak set. |

## Independent exact verification

A new review script, `check_perturbations.py`, imports no repository code and does not write into the repository. Its rational distance evaluation, boundary reconstruction, certificate checks, and maximum oracle were implemented separately from the project's helpers.

The maximum oracle uses the following completeness argument: a positive local maximum of the minimum of finitely many triangular distance curves must involve a downward cusp or active slopes of opposite signs. Its time therefore has the form `n/(v+w)`, allowing `v=w`. Enumerating these rational candidates and evaluating every constraint gives an exact upper bound and complete maximizing set. This differs from the repository's corner partition and within-cell pair-crossing implementation.

The boundary reconstruction builds all signed affine threshold-crossing times, tests every intervening rational cell and every boundary, and merges the allowed components. Its mathematical organization resembles one of the repository's crosschecks, but shares no implementation or distance primitive. Full boundary reconstruction is supporting evidence, not a substitute for the written unbounded reductions.

Run:

```sh
python reviews/2026-09-25-ultra/check_perturbations.py
```

Result: **PASS**, recorded in `check_perturbations_results.json`.

| Independent check | Coverage |
| --- | ---: |
| Complete maximum/peak records | 164 records, 162 distinct speed tuples |
| Reconstructed actual allowed sets | 248 records, 246 distinct speed tuples |
| Old-touch classifications | 1,392 |
| Strict rational point and interval certificates | 397 |
| Stored actual-grid profiles | 820, containing 4,416 choices |
| Four-unit complete remainder | All 64 `(q, signs)` pairs for q=3,4,5,6 |
| One-double complete remainder | Exactly all 44 vector-specific residual inputs |
| Two-double complete remainder | Exactly all 48 vector-specific residual inputs |
| Complete prescribed auxiliary profiles | 387 |
| Signed chosen phase intervals and sufficient cutoffs | 320 profiles: 128 one-double and 192 two-double |
| Necessary tiling-candidate phase records | All 608; each has positive clear length |

For stored actual-set summaries, the verifier compared exact endpoint hashes, durations, and component counts where supplied. The two baseline/control entries without such a summary were reconstructed separately; the four-unit baseline was matched to its explicit allowed set, and the changed-coefficient control's strict witness was checked against its reconstructed set. The strict interval checks recompute each runner's affine endpoint phases with a common integer part and establish **strict** separation throughout the interval. No stored endpoint-certificate assertion is trusted without recomputation.

The finite-remainder coverage checks construct the expected sets independently from all placements, all signs, the stated lower q bound, and each certified cutoff. They compare those sets to the JSON, checking both omissions and duplicates. The cutoff histograms match the notes exactly:

- One double: `{3:8, 4:32, 5:12, 6:8, 7:2, 9:2}`.
- Two doubles: `{4:28, 5:32, 6:32, 9:4}`.

## Scope and remaining limits

Read AGENTS, HANDOFF research status, RESEARCH_PLAN, MATHEMATICAL_BASELINE, SOURCES, the five notes, their five analysis scripts, and the pertinent affine-profile, boundary-certificate, and endpoint-certificate helper implementations. The coordinating reviewer separately checked commit provenance.

No broad speed search, extra unbounded scan, repository mutation, figure regeneration, or source-evidence overwrite was performed. The original five generating scripts were inspected but not rerun; the checked-in exact data were verified by the separate implementation instead. Figures, CLI behavior, the checker as a general software package, and other proof families are outside this subreview. No new literature search or novelty audit was performed. Existing literature descriptions are context, not independently authenticated source results in this review.

The unbounded family arguments pass this adversarial mathematical reading and their required finite certificates pass a separate exact implementation. This is an AI-assisted review, not a formal proof assistant certificate, human peer review, or a guarantee that no error remains. The key reusable mathematical content is the modular separation of core phase, auxiliary opening, and actual-grid reachability, together with the two tiling obstructions; the restricted family theorems should retain their precise scope.
