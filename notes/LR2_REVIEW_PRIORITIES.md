# LR 2: what the next-step summary underemphasized

September 25, 2026. Baseline: `1955eb3ce66bd3574fb0b14fb5726c18dc8861a0`. This is the root's research-direction review, not another Ultra-team report or a full proof audit. AI materially supplied the analysis, exact controls, and writing. No candidate is promoted.

## 1. Require a useful selection rule

If a strict allowed interval already exists, a sufficiently small subinterval inside it has zero blocked duration and a positive certificate without overlap corrections. Cutting at every threshold crossing also reconstructs the exact checker. Thus saying that some arbitrarily selected subinterval works does not explain why an opening must exist.

Specify what information selects the core, window, graph, and arithmetic conditions. A useful theorem must force success under stated speed assumptions. Diagnostic reconstruction can check a proposed rule but should not secretly supply its successful window. An arbitrary-speed selection guarantee remains OPEN.

## 2. Retain a cycle and account for its triple overlap

Let B_i be extra runner i's strictly blocked times inside a core-safe interval J. Write D_i for its duration, O_ij for pair overlap, and U for clear duration. A graph G is fixed throughout J; S(t) is the set of active blockers.

An elementary sufficient condition for

`U >= |J| - sum_i D_i + sum_(ij in G) O_ij`

is that every induced active graph G[S(t)] be a forest almost everywhere. For nonempty S its edges number at most `|S|-1`; integrating gives the inequality. The global graph may have cycles if their vertices cannot all be active together. This is sufficient, not necessary for every valid bound.

For extras `{6,7,11,w}`, choose edges `{6,11}`, `{6,w}`, `{11,w}`, `{7,11}`: a triangle with an attached edge. Let T be the duration when 6,11,w all block. Counting its 16 possible active subsets gives the unconditional bound

`U >= |J| - sum_i D_i + O_6,11 + O_6,w + O_11,w + O_7,11 - T`.

The correction handles both the triangle-only and all-four states. At w=16 in the original window, the exact phase certificate gives T=0 and the bound is `1/896`. A small positive upper bound on T can also suffice. Requiring no triple overlap is stronger than necessary.

Established context: Dohmen's *Improved Inclusion-Exclusion Identities and Bonferroni Inequalities with Applications to Reliability Analysis of Coherent Systems*, Section 4.3, Theorem 4.3.1 and Corollary 4.3.3, gives chordal-graph inequalities and their tree specialization. This triangle-with-leaf formula is a direct specialization, independently checked here by counting. See [S18](SOURCES.md#s18--graph-sieves-beyond-trees). No new general inequality is claimed. The research task is to bound intersections from runner speeds and select a graph/window giving positive slack.

## 3. Nearby controls limit the proposal

Exactly five replacements were checked, with core `{1,4,5}`, extras `{6,7,11,w}`, reference 0, threshold 1/8, and J=`[9/32,3/8]`. The all-pair expression is `|J|-sum D_i+sum_all_pairs O_ij`; it is not always a lower bound.

| w | All-pair expression | Actual clear duration | Fixed triangle-with-leaf corrected bound |
| --- | ---: | ---: | ---: |
| 13 | 0 | 0 | -1/182 |
| 14 | 101/7392 | 1/112 | -1/616 |
| 15 | 1/112 | 1/112 | 1/112 |
| 16 | 1/896 | 1/896 | 1/896 |
| 17 | 5/462 | 1/112 | -11/1904 |

For w=14 and 17, adding all pairs overstates the opening because triple blocking occurs. The corrected fixed graph is valid but inconclusive. Other graphs were not searched here; there is no general graph-selection conclusion.

The two successful LR 1 intervals `[41/88,15/32]` and `[17/32,47/88]` are exact reflections under `t -> 1-t`. They certify this configuration but represent one symmetry type. Earlier notes disclosed reflection repeats; short summaries should preserve that distinction.

```bash
python -B reviews/2026-09-25-lr2/check_priority_findings.py --check
```

This standalone rational script checks all 16 logical states, reconstructs the five local schedules, reevaluates the w=16 phase bound, and verifies reflection. The [JSON](../reviews/2026-09-25-lr2/priority_findings.json) pins its script hash. Reconstruction is diagnostic, not a proposed efficient selection rule or an arbitrary-speed proof. Existing research code and evidence are unchanged.

## 4. Equality and quantifiers remain central

The w=13 control has zero clear duration but retains the singleton `t=3/8` in J. No positive-duration bound can certify that success. Our tight-case motivation needs an equality route alongside strict openings. Ultra sharpened the opposing-contact test to `8 | (a+b)/gcd(a,b)` for the pair alone; every other runner must still be checked. Carry that tool into selection work.

Fixed-coefficient eventual results do not imply uniform coverage of arbitrary speed sets. A cutoff can depend on the coefficients being varied. The missing bridge is a justified reduction, uniform estimate, or classification of unhandled configurations. This is a scope gap, not an error in the existing propositions.

## 5. Preserved deductions that need concrete follow-through

- **Growing residual:** [overlap.md](../reviews/2026-09-25-ultra/overlap.md) derives `q > 2M^2(29k+32r)` for a fixed positive core with maximum M and k positive-length safe components, extras `q,2q+r,u,v`, `u,v>=q`, and the original distinctness assumptions. It covers positive integer `r=o(q)` eventually. It does not allow arbitrary growth of all coefficients.
- **Affine simplification and wider references:** the moving-endpoint alternative proof, equal-winding all-reference corollary, and balanced-block extensions merit explicit scoped statements. Remaining mixed winding multiplicities were not settled by the review. See [affine.md](../reviews/2026-09-25-ultra/affine.md).
- **Claim inventory:** the package reviewer requested precise hypotheses, strongest conclusions, superseded versions, reproduction, and review scope. Our report-assignment map is not yet that mathematical inventory. This remains a consolidation task, not a prerequisite for each experiment.

A small packaging omission surfaced: the tiling report referenced `test_tilings_output.txt` beside itself, while the original console trace remained in the old workspace. It is now copied unchanged into the review directory. Its substantive counts/examples were already in the report and JSON. Historical reports and their manifest remain intact; the original 19 artifact hashes exclude this subsequently restored trace.

## Recommended next question

Within a stated speed family, can arithmetic select a core window and overlap graph, then bound the necessary triple intersections tightly enough to force positive slack, with a separate valid-contact certificate for equality-only cases?

Begin with the w=16 exclusion and w=14/17 failures. The graph inequality is available; speed-derived intersection control and guaranteed selection are unresolved. This proposes the next bounded investigation; the five controls do not establish a selection theorem.
