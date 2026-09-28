# Targeted literature review: trees, pair moments, and the fastest core

Review performed September 28, 2026, for the September 27 six-case protocol. Scope: five primary sources, the repository's relationship-selector and all-core notes, and the team's supplied fastest-core argument. Materially AI-assisted. Only this review file was edited. This is neither a frontier audit nor an independent audit of any entire paper.

**Main finding:** the maximum-tree certificate is the established Hunter union bound, applied to the complement on a time window. The repository's earlier signed four-cycle repair also has an exact published predecessor. During this review the team supplied a much more decisive structural argument for its some-three-core hypothesis: a core containing a fastest relative runner confines every remaining blocker to a single interval, and an interval family admits an exact tree. That argument should be assessed as a supplied proof candidate, not as an inference from the six finite tests. The targeted searches did not locate a pinpoint published statement of that particular LR consequence; they do not establish novelty.

## 1. What is already in the probability literature

Let W have length L>0, with m residual blocking events, durations D_i, pair overlaps O_ij, and uncovered duration U. Normalize Lebesgue measure on W to a probability measure. Hunter [S1] studies union bounds using single and pair probabilities, optimizing his tree family by a spanning-tree algorithm. The explicit heaviest-tree formula is also recorded in [S2], opening discussion and Section 7:

\[
Q_T=L-\sum_iD_i+\sum_{ij\in T}O_{ij}\le U,
\qquad Q_* = \max_T Q_T.
\]

[S2], Lemma 7.1, gives the more general criterion
`sum_{i<j, i,j in A} w_ij <= |A|-1` for every nonempty active subset A (singletons are automatic). Printed p.29 derives the tree case from the fact that an induced subgraph of a tree is a forest.

Here is the elementary refinement used by this experiment, reconstructed directly rather than attributed verbatim to Hunter. For A(t) nonempty, let c_T(A(t)) count components in its induced forest. Its edge count is `|A|-c_T(A)`, so

\[
U-Q_T=\int_{\{t:A(t)\ne\varnothing\}}
        \bigl(c_T(A(t))-1\bigr)\,dt.
\]

Thus a fixed tree is exact in duration precisely when its nonempty active sets induce connected subgraphs almost everywhere. For the optimum, `U-Q_*` is the minimum of these integrated defects over trees. This distinguishes a positive certificate from an exact certificate. Isolated vertices in time have zero measure; this identity alone cannot settle equality-only loneliness or justify dropping strict-set endpoint checks.

### An exact precedent for the earlier signed-cycle repair

[S2], Lemma 7.3, printed p.30, permits a graph with a unique cycle of length at least four, assigning +1 to its edges and -1 to one nonadjacent chord. Complementing the source's union inequality gives the repository's four-blocker pattern

\[
U\ge L-\sum_i D_i+O_{AC}+O_{BC}+O_{AD}+O_{BD}-O_{CD}.
\]

For the earlier core failure, `(A,B,C,D)=(4,7,11,45)`. The same four-event instance is also contained in Lemma 7.2 with its distinguished pair `(C,D)`. **The form of this repair is KNOWN.** Its exact application, physical durations, and LP-optimality certificate in the repository remain separately scoped computations. This review does not claim the 2001 report is the earliest source.

## 2. What a full pair LP certifies

Boros–Lee [S3], Section 2, equations (1)–(2), states the atom formulation and explains its attainability over arbitrary probability spaces. In the present unnormalized notation it is

\[
\min x_{\varnothing}\quad\text{subject to}\quad
x_A\ge0,\quad \sum_A x_A=L,\quad
\sum_{A\ni i}x_A=D_i,\quad
\sum_{A\supseteq\{i,j\}}x_A=O_{ij}.
\]

For four residual blockers this has 16 state-mass variables. Every tree is a feasible pointwise inequality, so the optimal pair lower bound is at least `max(0,Q_*)`. It can improve a failed tree, as the earlier signed-cycle example demonstrates. A feasible zero-uncovered atom table shows that these moments alone do not force a positive duration among arbitrary event systems. It does **not** exhibit another physical runner configuration or refute loneliness for the given physical input. Conversely, when an interval family makes the tree exact, the pair LP must be exact as well: its optimum lies between that tree value and the actual feasible atom table.

The source's aggregation hierarchy is not needed for the four-blocker task and was not audited. No new LP computation was run in this review.

## 3. The fastest-core argument changes the interpretation

The following is the team's supplied argument, reproduced here to identify precisely what the literature does and does not settle. Its review status remains **proof candidate / HYPOTHESIS** under `CLAIM_STATUS.md`; AI agreement is not promotion to an established result.

Put `a_i=|v_i-v_ref|`, `V=max_i a_i`, and `delta=1/8`. If a core includes a runner with relative magnitude V, every complete core-safe component W lies inside one safe lap of that runner. Therefore

\[
|W|\le\frac{1-2\delta}{V}=\frac{3}{4V}.
\]

The gap between consecutive strict blocking intervals of any residual runner i is `(1-2*delta)/a_i >= 3/(4V)`. Two points in different strict blocking intervals are separated by **more** than that gap. Hence a positive-length W cannot meet two such intervals: every residual blocker restricted to W is empty or an interval. The constant is `3/(4V)`, not `7/(8V)`.

For finitely many intervals, order by left endpoint. Attach each interval after the first to an earlier interval whose right endpoint is largest. Its intersection with the union of all earlier intervals agrees, up to endpoints, with its intersection with that chosen predecessor. Telescoping the union measure gives an exact tree formula. Disconnected groups are connected by zero-overlap edges. This is also a constructive way to make the induced-active-set defect vanish almost everywhere.

Consequently the supplied argument yields `Q_*(W)=U(W)` on **every** component of a core containing a fastest relative runner. If a strict lonely time exists, its core component contains a positive neighborhood of that time, so its tree certificate is positive. For eight runners, any three-runner core containing that fastest runner suffices; the mechanism does not depend specifically on a core of size three. Duplicate absolute relative magnitudes do not affect the comparison.

This explains why finite success across all 35 cores would be much weaker evidence than the structural argument. It does not show that a strict lonely time exists, handle equality-only existence by duration, or solve LRC. It also does not guarantee success for a core omitting every fastest runner; the repository already preserves a counterexample to that stronger every-core assertion.

Targeted searches used the phrases Hunter/interval events, interval union/maximum spanning tree, induced-subgraph equality, and running intersection. They found the induced-forest and weighted-graph framework in [S2], but no inspected source explicitly naming the above interval-family lemma or fastest-core LR consequence. The elementary derivation should accompany any use; absence from these targeted results is not evidence of novelty.

## 4. What the lattice formulations retain

Beck–Hoşten–Schymura [S4], Section 2, equation (5) and Proposition 1, makes common-start loneliness equivalent to an integer point in
`R*a - [delta,1-delta]^k`, where their k matches this repository's k=n-1. Restricting the time coefficient to W gives the direct local adaptation

\[
P_W=\{ta-s:t\in W,\ s\in[\delta,1-\delta]^k\}.
\]

A lattice point in this bounded zonotope is exactly a locally feasible lap vector. The closed cube retains equality contacts; strict loneliness corresponds to a time whose coordinates lie in the cube interior. The local restriction is our adaptation of the inspected equivalence, not a separate theorem quoted from that paper.

Malikiosis–Santos–Schymura [S5], Proposition 1.5 and its proof sketch, projects the global line-and-cube problem to a zonotope/lattice intersection. Their n counts relative velocities, thus equals our k. Proposition 1.8 and the following comparison distinguish common-start lattice contact from the stronger all-starting-phase covering-radius requirement. These encodings retain arithmetic and geometry beyond the pair moments, but the inspected statements do not select a core-safe window or imply a positive tree bound. They provide no substitute for checking the interval argument. The paper's finite-reduction proofs were not audited here.

## Sources, versions, and actual reading depth

| ID | Primary source and dated version | Inspected scope |
| --- | --- | --- |
| S1 | David Hunter, *An upper bound for the probability of a union*, Journal of Applied Probability 13(3), September 1976, pp.597–603, DOI [10.2307/3212481](https://doi.org/10.2307/3212481). [Publisher record](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/an-upper-bound-for-the-probability-of-a-union/092D711504BA968EF0D1D903A2685D60). | Publisher abstract and bibliographic metadata only; original proof not accessed. Cambridge's July 14, 2016 date is online publication, not the result's original date. Explicit formula checked in S2. |
| S2 | András Prékopa, Béla Vizvári, Gábor Regős, Linchun Gao, *Bounding the Probability of the Union of Events by the Use of Aggregation and Disaggregation in Linear Programs*, RUTCOR Research Report **4-2001, January 2001**. [Author/institution PDF](https://rutcor.rutgers.edu/~prekopa/04.pdf); [institutional report listing](https://rutcor.rutgers.edu/2001.html). | Opening Hunter formula; Section 7, printed pp.28–30, Lemmas 7.1–7.3 and their local graph arguments. Downloaded text inspected; printed pp.29–30 visually checked. Remaining LP/aggregation results not audited. Cite this report version, not the shorter 2005 publication as though identical. |
| S3 | Endre Boros, Joonhee Lee, *Boole's probability bounding problem, linear programming aggregations, and nonnegative quadratic pseudo-Boolean functions*, [arXiv:2110.10672v4](https://arxiv.org/abs/2110.10672v4), January 24, 2025, 18:46:59 UTC; [versioned HTML](https://arxiv.org/html/2110.10672v4). | Sections 1–2, atom definition, equations (1)–(3), attainability explanation and normalization distinction. Did not audit later aggregation proofs or claim a current computational-complexity frontier. |
| S4 | Matthias Beck, Serkan Hoşten, Matthias Schymura, *Lonely Runner Polyhedra*, Integers 19 (2019), A29, published June 3, 2019. [Journal PDF](https://math.colgate.edu/~integers/t29/t29.pdf). | Section 2, printed pp.2–4, closed-cube derivation, equation (5), Proposition 1. Rechecked elementary translation; remaining results not audited. |
| S5 | Romanos Diogenes Malikiosis, Francisco Santos, Matthias Schymura, *Linearly exponential checking is enough for the lonely runner conjecture and some of its variants*, Forum of Mathematics, Sigma 13 (2025), e164, published October 1, 2025. [Publisher/DOI](https://doi.org/10.1017/fms.2025.10107). | Section 1.2, Proposition 1.5 with proof sketch, Proposition 1.8 and comparison of common-start versus shifted conditions; Corollary 2.3 formula inspected but not used above. No full finite-reduction proof audit. |

Primary-source searches and this reading support attribution of the bounds and their scope. They neither certify novelty nor turn the six-case experiment into a theorem. The most useful next review target is the supplied fastest-core proof itself, including strict blockers, maximum **absolute relative** speed, complete components, and the separation of positive duration from equality-only witnesses.
