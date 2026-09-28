# Six-agent transfer test: a structural explanation replaces the next search

September 27, 2026 (Pacific). Research baseline `910a26b044d6ea093a0d22aa678304a02e7e2642`. Vance authorized the plan and simultaneous team execution. Six workers handled exact calculation, independent verification, hostile review, lattice geometry, literature, and structural interpretation; the coordinating agent integrated the findings. Material AI involvement includes protocol design, code, mathematical arguments, review, and writing.

**The strongest outcome is a general simplification:** putting a fastest relative runner in the core makes the optimal tree bound exact on every complete core-safe window. A supplied argument explains why, and two separate implementations check all 8,800 such windows in the six fixed inputs. The argument also works with a one-runner core. See the self-contained [fastest-core proof candidate](FASTEST_CORE_CERTIFICATES_2026_09_27.md).

This resolves the proposed *conditional certificate-selection* question at the level of a supplied proof candidate: if strict lonely time exists, a fastest core detects it exactly. It does not establish strict lonely time or a valid equality contact in arbitrary configurations. The full Lonely Runner Conjecture remains unresolved by this work. Novelty is not asserted.

## Plan and execution

1. Freeze six inputs, reference 0, threshold 1/8, all 35 three-runner cores, and every complete closed core-safe component in `[0,1]`.
2. Apply the existing relationship reduction and quantitative selector Q. Preserve strict blocker endpoints, full allowed sets, isolated points, and the endpoint fallback.
3. Reconstruct all results with a separately structured implementation; challenge the hypothesis, build integer-lap certificates, and check related primary literature.
4. Preserve failures, explanations, scripts, hashes, and a bounded next question on the existing research branch.

All four steps were completed. No additional speed configurations or all-reference search were added. The adaptive stronger-pair investigation was reserved for an all-core strict failure; none occurred, so no new LP campaign was run. The later fastest-core and simple-witness diagnostics are explicitly retrospective additions, not alterations of the frozen inputs or Q rule.

## Frozen scope

[Protocol](../reviews/2026-09-27-team/protocol.json), SHA-256:

`578ad79f2d65ffe7309e3b1ae576de98e24ccaab1c23d3ea2600cedb5a9636a2`.

It was written and hashed before these new outcomes were calculated. This is an internal record, not external preregistration or a random sample. All runners start together. Each row has reference speed 0 and the seven other speeds listed below. Every row contains a multiple of eight, so `t=1/8` fails.

| Case | Other speeds | Complete core windows | Cores with a positive tree | Missed positive windows |
| --- | --- | ---: | ---: | ---: |
| Prime mix | 8,11,17,23,29,37,43 | 1,430 | 35/35 | 0 |
| Near pairs | 15,16,17,31,33,47,49 | 1,814 | 35/35 | 0 |
| Fibonacci | 8,13,21,34,55,89,144 | 3,130 | 35/35 | 8 |
| Squares | 8,9,25,49,81,121,169 | 3,828 | 35/35 | 4 |
| Prime powers | 16,25,27,49,64,81,125 | 3,324 | 35/35 | 2 |
| Perturbed chain | 7,8,15,23,38,61,100 | 2,170 | 35/35 | 4 |
| Total | Six selected references | **15,696** | **210/210** | **18** |

A missed positive window has actual duration greater than zero and tree bound at most zero. It does not imply its core or whole configuration fails. Core windows overlap, include reflection symmetry, and are not independent samples.

**Difficulty correction:** rejecting the eighth-time witness was insufficient to make these hard existence cases. Five rows (all except Fibonacci) have the simple strict witness `t=1/6`, since no listed speed in those rows is divisible by six. A separately frozen diagnostic testing `1/(2v_min)` and `1/(v_i+v_j)` finds strict witnesses in five rows, including Fibonacci, and fails on Squares. The half-slowest-lap candidate alone fails in all six. These diagnostic successes and failures are retained; no input was replaced after inspection. The study contributes representation and certificate evidence, not previously unknown existence coverage.

## What the fixed quantitative selector chose

Q maximizes the reduced optimal tree bound, then minimizes retained blocker count, maximizes width, and uses numerical core/left-endpoint tie breaks. It never uses actual duration or the allowed set in its selection key. Original runner count remains eight after reduction.

| Case | Selected core speeds | Selected window | Q | Actual local duration | Retained speeds |
| --- | --- | --- | ---: | ---: | --- |
| Prime mix | 8,11,29 | [33/232,39/232] | 865/46139 | same | 37,43 |
| Near pairs | 15,16,17 | [1/120,7/136] | 1357451/66752455 | same | 31,33,47,49 |
| Fibonacci | 8,13,21 | [41/104,71/168] | 306451/67104576 | 381295/67104576 | 34,55,89,144 |
| Squares | 8,9,25 | [33/200,39/200] | 2053/200772 | 95731/6625476 | 49,81,121,169 |
| Prime powers | 16,25,27 | [97/216,19/40] | 35029/4704000 | 13/1536 | 49,64,81,125 |
| Perturbed chain | 7,23,38 | [41/184,71/304] | 2827/426512 | same | 61 |

All six have directly checked strict witnesses. The full-period allowed set is stored exactly; the Near-pairs row also has four isolated valid points alongside its positive-duration components. Zero-dimensional information was not dropped.

None of these six selected cores contains the fastest runner. Each chosen window is wider than a fastest safe lap and gives a larger Q than any fastest-containing three-core in its row. This is consistent with fastest-core exactness: an exact small window need not maximize the amount of certified duration. Selecting the largest lower bound and selecting a guaranteed exact representation are different tasks.

Containment is not necessary for success or exactness. The Near-pairs winner retains all four residual blockers, has no nonempty containment, and nevertheless has Q equal to actual duration. The Fibonacci, Squares, and Prime-powers winners also retain all four and succeed with nonzero slack. Prime mix loses two vanished blockers. Perturbed chain has vanished speeds 8 and 15 and the containment `B100 subset B61`, leaving only 61.

## The structural finding

At threshold delta, a fastest safe lap has length `(1-2delta)/V`. Every slower runner's consecutive blocking intervals are separated by a safe gap of length `(1-2delta)/v`, at least as long. A core-safe component containing a fastest constraint therefore meets at most one blocking interval per residual runner.

For intervals, order by left endpoint and connect each new interval to an earlier one with greatest right endpoint. Its overlap with the entire preceding union equals its overlap with that one interval, in duration. The resulting tree accounts for the union exactly. The [proof note](FASTEST_CORE_CERTIFICATES_2026_09_27.md) handles endpoints, equal absolute speeds, empty blockers, the arbitrary-core extension, and equality-only limitations.

| Case | Fastest-containing cores | Their complete windows | Windows with exact tree |
| --- | ---: | ---: | ---: |
| Prime mix | 15 | 716 | 716 |
| Near pairs | 15 | 880 | 880 |
| Fibonacci | 15 | 1,848 | 1,848 |
| Squares | 15 | 2,222 | 2,222 |
| Prime powers | 15 | 1,856 | 1,856 |
| Perturbed chain | 15 | 1,278 | 1,278 |
| Total | **90** | **8,800** | **8,800** |

The finite equality is OBSERVED / independently REPRODUCED. The general argument remains a proof candidate under repository rules. It was derived during review, not inferred by fitting these numbers. A simple safe-gap arithmetic error in the first informal formulation was caught and corrected to `3/(4v)` at threshold 1/8 before the written proof.

All 210 cores succeeding is still only a bounded fact. The earlier speed-45 example already disproves universal success for *every* core. The proposed general statement guarantees the cores containing a fastest runner.

## What the tree loses on other windows

For a fixed tree T and active residual blocker set S, let `c_T(S)` be the number of connected components of the induced forest. With `c_T(empty)=0`,

\[
U-Q_T=\sum_{S\ne\varnothing}m_S\bigl(c_T(S)-1\bigr),
\]

where `m_S` is the duration of exactly that active set. The tree loses duration when simultaneous blockers form disconnected pieces in its chosen graph. Maximum-tree selection minimizes that integrated loss.

This identity was checked on every component. The Fibonacci winner's entire slack `27/24208` comes from the disconnected active pair `{34,89}`. The Squares winner has four contributing active patterns; the Prime-powers winner has two. The full tree is exact on 15,350 of 15,696 components, with positive slack on 346. There are 7,971 positive-duration windows and 7,953 positive tree bounds.

Deleting empty/contained blockers preserves both the full allowed set and the optimal tree bound throughout the batch. There are 198 positive windows in which the map removes no blocker at all. In the archive this count is named `positive_bound_without_reduction`; it does **not** mean only 198 unreduced bounds are positive. All 7,953 positive bounds also hold before reduction because full and reduced optima agree.

A further supplied diagnostic is that a positive window missed by every tree must have at least one retained blocker with multiple interval pieces. Otherwise the interval construction would be exact. Such a residual speed exceeds every core speed. This points directly toward moving a faster constraint into the core, while leaving the global existence question intact.

## Lattice certificates and literature

For each selected surviving interval, the geometry worker records a common vector of integer lap numbers. The interval is exactly the intersection of the seven safe-lap intervals, obtained by taking the greatest left endpoint and least right endpoint. Each strict witness additionally satisfies fourteen strict integer inequalities after clearing denominators. This recovers lap alignment explicitly; it is an equivalent exact certificate, not an independent global-existence theorem. See [geometry review](../reviews/2026-09-27-team/geometry.md).

All 20 selected surviving intervals and all 12 selected/global witnesses pass these checks. For a fixed shared lap vector m, eliminating time gives the pair-indexed inequalities `v_j(8m_i+1)<=v_i(8m_j+7)` for every i,j. Strict inequalities give a positive common lap interval. These pairwise alignment constraints determine feasibility for the shared vector; pairwise overlap totals generally do not. Thus the word *pairwise* alone does not specify how much information a representation preserves. Finding a feasible shared integer vector is still the existence problem.

The [targeted literature review](../reviews/2026-09-27-team/literature.md) identifies the tree framework as Hunter's existing probability-union bound. It also pins the earlier signed four-cycle with a negative diagonal to Prékopa–Vizvári–Regős–Gao, RUTCOR 4-2001, Lemma 7.3, printed p.30; the form is KNOWN. The review did not establish novelty for the fastest-runner application or audit the full current Lonely Runner frontier. Historical notes are retained and linked to this later attribution.

## Reproduction and review limits

Run from the repository root:

```bash
python -B reviews/2026-09-27-team/calculate.py --check
python -B reviews/2026-09-27-team/verify_independent.py --check
python -B reviews/2026-09-27-team/challenge_check.py --check
python -B reviews/2026-09-27-team/lattice_check.py --check
python -B reviews/2026-09-27-team/structure_check.py --check
```

The primary method uses integer interval intersections, prefix integration, strict endpoint sets, and exhaustive trees. The independent method uses a threshold-event state sweep on a product-denominator grid and Kruskal trees. It does not read or import the primary calculation code. They agree on all 210 per-core component digests, every component's maps/bounds/durations, selected moments/strict sets/tree ties, all full allowed sets, and all witnesses. Additional geometry/structure/challenge scripts check their own bounded claims. Exact source and artifact hashes are in the [manifest](../reviews/2026-09-27-team/manifest.json).

These implementations are independently structured AI-produced checks, not outside human review or a formal proof-assistant verification. No previous checker/evidence archive was changed, no broad regression suite was repeated, and no external contact, paid compute, main merge, or publication outside the existing research branch occurred.

## Next investigation

Stop treating a larger all-core success count as the central missing evidence. The fastest-core argument explains that conditional success.

The next bounded task is to use **only the fastest runner as the core** in two already studied inputs, `{0,1,4,5,6,7,11,13}` and `{0,1,4,5,6,7,11,16}`. Record the interval-cover chains, exact gap/contact endpoints, and integer lap relations on all 13 and 16 fastest safe laps. The first has only isolated lonely contacts; the second has positive openings. Ask which arithmetic restrictions link the chains across laps, and which distinguish complete coverage, a boundary contact, and a positive gap.

This next task is proposed, not run in this package. A useful outcome would be a constraint on simultaneous coverage across different laps, or an exact demonstration that a proposed cross-lap summary loses that information. The remaining obstacle is global existence, with equality preserved. The +7/+9 extension remains parked.
