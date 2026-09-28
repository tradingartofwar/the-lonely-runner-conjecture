# Occurrence combinatorics: periodic limits and a finite obstruction

Date: 2026-09-28. Pinned baseline: `5871f2b6c57552b5bd55fd4caa82d0c61307b10e`.

**Status:** HYPOTHESIS / proof candidates, with material AI derivation and internal mathematical challenge. No scan, extra physical configuration, literature novelty claim, or external review is supplied here. This note addresses four auxiliary positive speeds with arbitrary phases. Any resulting upper bound therefore also applies to common-start positive integer speeds. It does not assert that arbitrary auxiliary phases are themselves physical common-start inputs.

Write a label's period as `p_i=1/v_i` and its open occurrences as

`I_(i,k)=(s_i+k p_i, s_i+k p_i+p_i/4)`.

All four labels have blocking duty 1/4. Equality at a left/right endpoint is safe for that label.

## 1. Pairwise disjoint trains have very restricted period ratios

**Lemma candidate.** If two such trains with periods p and q have disjoint interiors everywhere, their ratio is rational. Write `p=r g`, `q=s g`, where r and s are coprime positive integers. Then

`r+s <= 4`.

Consequently the only possible ratios are 1, 2, 3 and their reciprocals.

**Proof.** Let the trains start at x and y. Two occurrences overlap precisely when

`(y-x)+l q-k p` belongs to the open interval `(-q/4,p/4)`.

If p/q is irrational, the additive group `{l q-k p : k,l integers}` is dense, so such an overlap is unavoidable. If p/q is rational, Bezout's identity gives that group exactly `g Z`. An open interval of length greater than g contains a member of every translate of `g Z`. Avoiding overlap therefore requires `(p+q)/4 <= g`, which is the stated inequality. The weak inequality is essential: an open interval of length exactly g can avoid the lattice by having lattice points at its two endpoints.

The same conclusion holds if interiors are disjoint only on a half-line. In the rational case every strict overlap repeats with a common period. In the irrational case positive-time irrational rotation returns yield strict overlaps arbitrarily far to the right. Alternatively, simultaneous approximate recurrence of both phase coordinates transfers any strict overlap into the half-line.

**Corollary candidate.** A four-label exact tiling, meaning multiplicity one almost everywhere, has a common period P. Indeed every pair has rational period ratio, so a common multiple of their periods exists. The largest/smallest period ratio is at most 3. A simultaneous ratio-2 and ratio-3 class is impossible, because their mutual ratio 2/3 violates `r+s<=4`.

For compactness purposes only commensurability is needed; the complete tiling classification need not be asserted.

## 2. Exact tilings have two occurrences at each boundary

In an exact tiling by these positive-length open intervals, every boundary has exactly one interval ending and exactly one interval starting. There can be no third occurrence at that boundary: a third positive-length interval would extend to one side or the other, creating an interior overlap there. Intervals also cannot leave a positive gap, since that would violate the tiling property.

The open union itself omits each touching boundary. Thus an exact tiling is a limit of possible blocking patterns, not an example of an everywhere strictly blocked line.

There are finitely many boundaries in a period. Their spacings are positive because every tiling interval has positive length.

## 3. A neighboring strict cover is impossible over sufficiently many periods

This is an independent check of the max-period cycle argument supplied by the geometry agent.

Fix an exact tiling with common period P and define the positive integers

`q_i=P/p_i`.

There are `q_i` occurrences of label i in one period and `m=sum_i q_i` occurrences altogether. Perturb the periods to `p'_i` and starts to `s'_i`, while retaining the occurrence labels of a finite portion of the tiling. Define

`sigma_i=q_i p'_i`.

Choose a label r maximizing sigma. Start at an occurrence of r and follow the original tiling order for m consecutive transitions, finishing at its q_r-th successor. This cycle includes exactly q_i next intervals of label i; the initial occurrence is excluded from those counts and the final r occurrence is included.

If every consecutive pair strictly overlaps, writing R_j for right endpoints gives

`overlap_j=R_(j-1)-(R_j-p'_(label j)/4)>0`.

Summing over the cycle telescopes:

`sum_j overlap_j = (1/4) sum_i q_i p'_i - q_r p'_r`

`                     = mean_i(sigma_i)-max_i(sigma_i) <= 0`.

This contradicts strict positivity. No assumption about a greedy projection order is used. The argument also permits equal perturbed periods. It is the four duties of 1/4 that make the final expression an arithmetic mean.

**Local stability bridge.** Take a finite window containing two entire periods of the exact tiling, with a small margin at each end, and choose one occurrence of each label in its first period. All four full cycles described above lie in this window. At each of its finitely many relevant boundaries choose a small neighborhood containing only the two incident occurrences. Such neighborhoods exist by Section 2 and local finiteness. For all sufficiently small perturbations of periods and starts:

- the same occurrence indices remain the only intervals meeting a smaller neighborhood of each relevant boundary;
- their two relevant endpoints stay inside that neighborhood;
- no other label's occurrence can fill a gap between those endpoints.

Hence an open cover of the window forces the former left interval's right endpoint to lie **strictly** beyond the former right interval's left endpoint at every boundary. Equality is insufficient because both intervals are open. These forced inequalities include the full cycle for every possible maximizing label r, contradicting the telescoping calculation.

This proves a local statement: each exact tiling has a neighborhood in parameter space and a finite time window which no member of that neighborhood can openly cover. The window can be chosen before knowing which label maximizes `q_i p'_i` because it contains an appropriate cycle anchored at every label.

Continuous phase coordinates may be chosen locally by lifting phase values modulo one. Any wrap changes an occurrence index once; it does not affect the finite comparison argument.

## 4. Role in a qualitative uniform-bound argument

Sections 1–3 supply the previously missing obstruction at the compactness limit. They do not by themselves bound the number of arbitrary occurrences in a component.

The proposed synthesis additionally needs the following independently justified reductions:

1. An unbounded period ratio is excluded by a quantitative overlap charge. The geometry agent supplies `d>=4a` implies at most 175 selected occurrences, explicitly for the actual increasing-right-endpoint chain, not just a minimal subchain.
2. In the remaining regime normalize a=1, so all speeds lie in [1,4]. Selected occurrences are distinct and each label's right endpoints have spacing at least 1/4. Thus unbounded selected-occurrence counts force arbitrarily long openly covered time intervals directly; no minimal-cover reduction is needed in this regime.
3. Compact normalized parameters admit a subsequence whose arbitrarily long covered intervals limit to a half-line weak cover.
4. Such a critical-density half-line weak cover is an exact tiling almost everywhere. One route is that the continuous potential H is nondecreasing on the covered half-line, while simultaneous recurrence of its finite phase vector brings H arbitrarily close to its initial value at arbitrarily late times. Hence H is constant and `M=1` almost everywhere.
5. Sections 1–3 then contradict the original sequence's long open covers, because sufficiently late parameters lie in the limiting tiling's excluded neighborhood.

If all five reductions are checked, this yields a qualitative speed-independent bound. It does not supply an explicit numerical constant for the compact speed-ratio regime. A local neighborhood exclusion plus compactness must not be advertised as an effective formula without additional quantitative work.

## 5. Actual selector order and irredundancy

An actual advancing projection trace is an increasing-right-endpoint strict-overlap chain, but it need not be a minimal cover: a later large interval may contain earlier selected intervals. Therefore any result stated only for minimal covers would need a separate reduction before it bounds actual advances or rounds. The geometry agent confirms that its large-ratio bound concerns the actual selected chain, and the bounded-ratio occurrence count in Section 4 also directly concerns that chain. This avoids needing that reduction in the proposed synthesis.

Sections 2–3 concern the union's open coverage, not the sequence in which the algorithm selected intervals. They therefore remain valid after pruning selected occurrences and do not assume that the selector follows the tiling word. The finite tiling word is used only to identify the unavoidable local adjacency inequalities in a hypothetical long open cover.

No unbounded family of actual selector itineraries was constructed here. A final assertion about scalar moves, eleven-call rounds, or total arithmetic work must name the corresponding conversion separately.

## 6. Universal square-free rule for the actual moving label word

**Lemma candidate.** The label word of any increasing-right-endpoint strict-overlap chain using at most four of these trains is square-free: it cannot contain `W W` for a nonempty finite word W.

Let m be the length of W and q_i the number of occurrences of label i in W, allowing q_i=0 for labels absent from W. Select r maximizing `q_i p_i`, and choose an r occurrence in the first copy. The matching r occurrence m positions later is in the second copy. The intervening m next intervals are a cyclic rotation of W and therefore contain exactly q_i occurrences of each label i.

Among those next intervals are q_r selected occurrences of r. Since right endpoints increase strictly, successive selected occurrences of that label differ by at least one period. The right-endpoint displacement between the matched r occurrences is therefore at least `q_r p_r`; skipped laps only increase it. On the other hand, summing strict adjacent overlaps gives

`0 < sum overlaps = (1/4) sum_i q_i p_i - displacement`

`                  <= (1/4) sum_i q_i p_i - max_i(q_i p_i) <= 0`.

This is a contradiction. It does not require irredundancy, commensurate periods, integrality, specified phases, or the eleven-call selector. It applies directly to the actual moving label word after stationary calls have been removed, because advancing projections satisfy the required strict overlaps and increasing right endpoints.

This is a forbidden-pattern **schema**, not a finite list of all forbidden words. It alone gives no length bound: abstract square-free words over four letters can be arbitrarily long. It is nevertheless stronger than excluding repetition of just the archived seven-interval example or just one exact tiling word. Additional periodic-occurrence geometry is still needed for uniform boundedness.

## 7. Counterpressure retained

The critical tiling need not use four equal periods. Examples, in abstract time units, are:

- periods `(8,8,4,4)`, widths `(2,2,1,1)`, tiling word `A C D B C D`;
- periods `(12,12,12,4)`, widths `(3,3,3,1)`, tiling word `A D B D C D`.

They are auxiliary exact tilings with touching endpoints. They are not strict covers, nor physical common-start counterexamples. They demonstrate why an argument considering only four equal-period quarter intervals would miss valid compactness limits.
