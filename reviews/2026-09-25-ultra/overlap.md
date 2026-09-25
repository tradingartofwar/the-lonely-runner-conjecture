# Overlap, residue, and core-transfer review

Reviewed September 25, 2026, for Vance's Ultra review. Intended live revision: `ea482f54edae4775621bc69c1fb7359291f31ddd`. The local synthetic checkout reports an earlier HEAD; the parent reviewer independently matched the research files to the intended live revision by Git blob hashes. No repository files were edited or published.

## Verdict

I found **no fatal mathematical gap in the stated unbounded implications in this assignment**. The local period estimate, all stated overlap cutoffs, endpoint correction, residue reduction, core-transfer positivity argument, and Hunter-tree accounting survive this review. This is a fresh AI review, not external mathematical validation or a novelty finding.

The strongest new finding is a small exact counterexample to extending the successful finite tree diagnostic to every positive-duration core component. A second deduction shows that the obstruction goes beyond the particular tree inequality: for the counterexample, the individual and pair durations alone are compatible with complete coverage by abstract events. These observations narrow the next research question materially.

## Severity-ranked findings

### Medium — the 38/38 tree success does not extend even to a nearby single-speed change

**Location:** `notes/CORE_TRANSFER.md`, Sections 6–8, especially the table of 38 positive-duration components, the tree-gap identity (7), and the proposed question at the end. The existing text carefully calls its success finite and does not assert the false extension; this is a limitation discovered by review, not a contradiction of its stated theorem.

Use common-start velocities

\[
\{0,1,4,5,6,7,11,16\},\qquad C=\{1,4,5\},\qquad J=[9/32,3/8].
\]

This changes only 13 to 16 in the familiar tight control. The complete allowed set inside this core component is

\[
[17/56,39/128],\qquad U_J=1/896>0.
\]

Every fixed spanning-tree certificate on the four extras fails to prove positive duration in this component. The exact certificate is:

| Extra speed | Individual blocking duration in J |
|---|---:|
| 6 | 1/24 |
| 7 | 5/224 |
| 11 | 9/352 |
| 16 | 3/128 |

Thus `E=569/29568`.

| Pair | Overlap in J |
|---|---:|
| 6,7 | 0 |
| 6,11 | 1/528 |
| 6,16 | 1/128 |
| 7,11 | 1/352 |
| 7,16 | 0 |
| 11,16 | 1/128 |

The unique maximum tree uses `{6,16}`, `{7,11}`, `{11,16}`. Its weight is `13/704`; subtracting E gives `-23/29568`. The tree loses exactly `1/528`, the pair-only `{6,11}` duration. This loss exceeds the actual clear duration. The reflection component `[5/8,23/32]` has the same failure.

The graph of positive pair overlaps contains a triangle on 6,11,16, but no triple intersection occurs. A tree has to omit an edge although all three pair-only overlaps are genuine redundancy. This makes the mechanism particularly transparent.

**Reproduction and independence:** `overlap_check.py` beside this report has no project imports. It uses exact rational threshold boundaries, checks every open cell and boundary, and enumerates all 16 trees by Prüfer codes. Its output is `overlap_check.json`. The project interval checker separately returned the same local interval, and its selection implementation returned the same edge table and optimum. The only new speed controls tried were replacements 12,14,15,16 for the original 13; no broad scan was performed. The first three did not produce a missed positive component.

**What this does not show:** it does not show that trees fail on every core opening of this configuration, that a different core cannot work, that a tree on a finer interval cannot work, or that the Lonely Runner Conjecture fails. It disproves the component-level extension “a positive-duration core component always has a positive fixed-tree bound.”

### Medium — complete first- and second-order overlap data can still be insufficient

**Location:** the same proposed tree-selection research direction, `CORE_TRANSFER.md` Section 8. Again, this is an obstruction to an extension, not an error in the note.

In the preceding example, let `theta=1/896`, its uncovered measure. Modify the exact active-set duration distribution as follows:

1. Subtract theta from the empty state and from each pair-only state `{6,11}`, `{6,16}`, `{11,16}`.
2. Add theta to `{6,11,16}` and to each singleton `{6}`, `{11}`, `{16}`.

All masses remain nonnegative, since the smallest pair mass removed is `1/528>theta`. Total measure, every individual blocking duration, and all six pair overlaps remain identical, but uncovered measure becomes zero. The standalone diagnostic checks these identities exactly.

This alternative distribution is an abstract event arrangement, **not a second common-start speed configuration**. It proves a precise information limitation: no universal event inequality depending only on these individual/pair durations can force positive clear duration for these margins. A stronger explanation must use additional speed geometry, higher-order intersections, or the distribution of overlaps across finer time intervals. Replacing Hunter by another generic pair-data inequality cannot by itself solve this example.

### Low — opposing-contact divisibility can be sharpened substantially

**Location:** `notes/CORE_TRANSFER.md` Section 3, equation (5), lines 121–129 in the reviewed file.

The stated necessary condition `8 | (a+b)` is correct but loses the gcd constraint. Put `g=gcd(a,b)`. The exact necessary and sufficient condition for the pair alone to have an oriented contact

\[
\{at\}=1/8,\qquad\{bt\}=7/8
\]

is

\[
8\mid(a+b)/g.
\]

Indeed the displayed Diophantine equation in the note is soluble exactly when `g | (a+b)/8`. Dividing by g gives a coprime pair, and Bézout gives the converse. When it holds there are g such oriented contacts modulo one; every other speed still needs checking. For example, a=2,b=6 passes `8|(a+b)` but fails the stronger test and has no such contact. This is a useful refinement for endpoint enumeration, not a repair needed for the existing argument.

## Positive findings and algebra audited

| Item | Review result |
|---|---|
| `LOCAL_OVERLAP.md` lines 91–118 | The arbitrary-phase period tail `D<=pL+p(1-p)/h` is valid for any measurable periodic set, including a union of windows. Splitting an interval into complete periods from its own left endpoint is legitimate. Grouping the doubled pair gives exactly the stated q>=53 condition. |
| `SPEED_RATIOS.md` Sections 2–4 | The geometric interval sum, fractional-part expression, ratio/gcd distinction, exhaustive `ab<10` remainder, unique overlap minimum 1/28, and uniform gcd/other-speed cutoff 187 are consistent. The ratio-free lower bound increases with rho; using its minimum and replacing all denominators by 187 has the correct direction. |
| `OVERLAP_PLACEMENT.md` Section 4 | The retained full windows lie in J. Their arithmetic-sum lower bound is valid even when qL<1 (then it is merely weak). The quadratic numerator and strict positivity for integer q>=310 are correct. |
| Same note Sections 6–7 | The phase width K, distinct treatment of phase availability and actual occupancy, floor identity away from finitely many boundary times, periodic primitive, and r=3 slope-change cancellation are correct. The discrepancy cutoff values are implications of a monotone bound, not finite extrapolation. |
| Same note Section 8 | Periods 32,16,96 for overlap coefficients and 32,32,96 for the full pair budget are valid. Each frozen class has a positive-leading quadratic with negative constant, hence exactly one positive root. The recorded brackets genuinely certify all larger members of each class, giving 242,263,36. |
| `CORE_TRANSFER.md` Section 1 | Common-start overlap of the three core blockers yields `|A|>=1/4+1/(2M)`. The phase-area lower bound `1/(64M^2)` is correct. The finite affine partition and uniform frequency lower bound q yield the stated `m/(4q)` discrepancy and clear-duration condition. |
| Same note Section 3 | The isolated-contact iff criterion is valid under the stated positive-speed assumptions. The complete boundary reconstruction keeps singleton successes separate from zero measure and empty sets. |
| Same note Section 7 | Hunter's tree bound and the induced-component gap identity are correct. One tree is fixed over a whole core component; it is not illicitly selected separately at each time. |

Positive-duration conclusions imply a genuinely strict witness in these finite integer-speed systems: only finitely many threshold boundary times occur in a unit period, so a positive-measure allowed set contains an interval avoiding them. Zero or negative lower bounds remain inconclusive, as the notes consistently state.

## Useful strengthening already implicit in the core-transfer proof

The fixed-residual hypothesis is enough, but the audited inequalities give a modest uniform extension without a new search. There are exactly `4r` possible split points `rt=m±1/8,m±3/8` in `(0,1)`. For k positive-length core components, their positive affine piece count satisfies

\[
m\le k+4r.
\]

Consequently the existing proof gives

\[
U_A\ge {1\over64M^2}-{29k+32r\over32q}.
\]

Thus the explicit sufficient condition

\[
q>2M^2(29k+32r)
\]

allows r to vary with q. In particular, for a fixed core, any positive integer residual `r=o(q)` is eventually covered (with the same distinctness and u,v>=q assumptions). This is a deduction from the reviewed proof, not a literature novelty claim or a general-speed result. It also explains exactly why arbitrary growth of r or the core is not justified by the original limiting argument.

## Dependency and research-value assessment

The assigned notes describe a progression of the same two main mechanisms, not four independent proof strategies:

1. **Pair grouping plus periodic tail bounds.** Exact doubling is a special case of the ratio formula. The q>=53 and gcd>=187 implications are different sufficient applications of this mechanism.
2. **Affine phase relation plus endpoint discrepancy.** The q>=310 construction, residual profiles, discrepancy bounds, residue refinements, and arbitrary fixed-core transfer all build on this mechanism. The improved residue cutoffs replace weaker constants within the same three families; they do not expand to arbitrary four added speeds.

The local redundancy identity is bookkeeping, not an independent existence proof. Hunter is an established way to combine pair data; the exact gap formula is useful diagnostic accounting. Common-start positivity of the core phase area is the most structurally transferable argument in this group because it prevents the entire useful phase region from being excluded by an arbitrary fixed triple. None of these arguments establishes a frontier runner-count result, arbitrary-speed coverage, or an all-reference result.

The new tree counterexample suggests a more discriminating next task than improving cutoffs: identify a speed-based or higher-intersection condition that controls the cyclic overlap lost by every tree, or prove that some other core opening or regrouping must admit a certificate. Those are separate questions. Merely collecting more successes of fixed trees would not address the demonstrated information obstruction.

## Evidence reproduced

I reran all eight assigned script entrypoints while intercepting `Path.write_text` in memory. Every script assertion passed; each complete regenerated JSON object was identical to its existing corresponding evidence file. No evidence file was overwritten:

- `analyze_local_overlap`: 64 regions and 384 pair comparisons.
- `analyze_speed_ratios`: 11 prescribed ratio checks, complete 9-pair reduced remainder, 5 configurations.
- `analyze_overlap_placement`: 7 configurations.
- `analyze_residual_overlap`: 9 configurations.
- `analyze_phase_discrepancy`: 15 configurations.
- `analyze_phase_residues`: all 144 overlap and 160 combined classes, 320 pair checks, 17 full configurations.
- `analyze_core_transfer`: 20 profiles and 11 decompositions.
- `analyze_pair_selection`: 72 components, 432 pair durations, 1152 tree checks, 72 exhaustive/greedy comparisons, and 11 boundary reconstructions.

These are reproduction of the supplied exact diagnostics, not independent implementations of every certificate. The newly supplied `overlap_check.py` is separately implemented and covers the new counterexample only.

## Literature checked and scope limits

Reopened the primary source Perarnau–Serra, *Correlation among runners and some results on the Lonely Runner Conjecture*, arXiv:1407.3381v3: [versioned PDF](https://arxiv.org/pdf/1407.3381v3). Read Propositions 7–8 (printed pp. 5–7) and Lemma 13, equation (12), with its following maximum-tree sentence (printed p. 12). These support the existing attribution of the pair formula and Hunter method. No novelty is asserted for the local specialization or the new diagnostic.

Reviewed: the four full assigned notes; the eight named analysis scripts; their directly used interval, phase-certificate, and boundary helpers; the corresponding exact JSON through regeneration; AGENTS/HANDOFF, research plan, baseline, and relevant source entries.

Not reviewed: a general checker proof or complete checker regression audit; the entire cited papers; novelty across all literature; higher-runner frontier results; other research families outside this assignment; every reference runner; any broad speed scan. This review supplies mathematical reasoning and exact finite evidence, not formal verification or human peer review.
