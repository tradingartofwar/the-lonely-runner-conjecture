# Changing the fixed core and preserving isolated valid times

**Date:** September 24, 2026. **Status:** OBSERVED for the listed exact diagnostics; HYPOTHESIS/proof candidate for the transfer and boundary arguments below; OPEN for arbitrary seven relative speeds. The derivation and code are materially AI-generated and await independent review. No novelty claim.

Vance asked whether our progress helped the overall goal and approved testing the mechanism beyond the core {1,4,5}, including configurations with isolated threshold touches. Further polishing of the two unspecified runners' duration allowance is parked.

## 1. What transfers

Keep eight common-start runners, reference speed 0, and threshold delta=1/8. Let C be **any fixed triple of distinct positive integer relative speeds**, and let A be its complete closed allowed set in [0,1], retaining isolated points. Add four distinct speeds q,2q+r,u,v, disjoint from C, with u,v>=q. The positive integer r is fixed while q grows.

The same local arithmetic works on every component of A:

$$U_A\geq O_A-E_A,\qquad
E_A=D_q+D_{2q+r}+D_u+D_v-|A|.$$

Here D counts individual blocking duration inside A, O is the selected pair's shared blocking duration there, and U is the full seven-speed clear duration. Because A is the core's complete allowed set, U is also the full clear duration over [0,1].

For the signed q-phase x, define

$$K_r(t)=\operatorname{length}\{x\in(-1/8,1/8):\|2x+rt\|<1/8\}
=\min\left(1/8,\max(0,(3/8-\|rt\|)/2)\right).$$

Its area over the core's allowed times is

$$I_{C,r}=\int_A K_r(t)\,dt.$$

The important transfer is that this area is positive for **every such core and every fixed positive integer r**. The following is a complete candidate argument, separate from the finite diagnostics.

### Why a core cannot exclude all the eligible phase region

Each core runner blocks exactly 1/4 of [0,1]. Put M=max(C). All three block simultaneously on

$$(0,1/(8M))\quad\text{and}\quad(1-1/(8M),1).$$

These intervals have total length 1/(4M). Summing three blocking indicators overcounts their union by two there. Consequently

$$|A|\geq 1-\left(3/4-1/(2M)\right)
=1/4+1/(2M)>1/4. \tag{1}$$

Meanwhile K_r is positive precisely where $\|rt\|<3/8$. Since r is a positive integer, this region occupies 3/4 of [0,1]. Its complement occupies only 1/4. The core's allowed set, whose measure is strictly larger than 1/4, cannot fit entirely into that complement. Hence I is positive.

A quantitative version avoids relying only on strict positivity. For $0<\epsilon\leq1/8$, the set where $K_r\geq\epsilon$ has measure $3/4-4\epsilon$. Choose $\epsilon=1/(16M)$. From (1),

$$|A\cap\{K_r\geq\epsilon\}|
\geq1/(2M)-4\epsilon=1/(4M),$$

so

$$I_{C,r}\geq1/(64M^2)>0. \tag{2}$$

This explains a role for the common starting point: overlap among the core runners forces their total free-time measure above 1/4. The simultaneous blocking near the start is not itself a valid time; the measure comparison forces some eligible phase region elsewhere.

### From eligible phases to actual overlap

Split the positive-length components of A at the finitely many times

$$rt=m\pm1/8,\qquad rt=m\pm3/8,\qquad m\in\mathbb Z.$$

On each piece where K is positive, the permissible signed q-phase is a single interval $(a(t),b(t))$. Its endpoints are selected from

$$a(t)=\max\left(-1/8,(m-1/8-rt)/2\right),\quad
b(t)=\min\left(1/8,(m+1/8-rt)/2\right).$$

Each endpoint has slope 0 or -r/2. The floor-function identity and periodic primitive P from [OVERLAP_PLACEMENT.md, Section 7](OVERLAP_PLACEMENT.md) therefore apply without fixing the core.

Let k count the positive-length components of A, and let m count their positive affine phase pieces after splitting. Isolated core points contribute to neither duration nor these counts. On each piece the absolute endpoint correction is at most 1/(4q), since both endpoint frequencies are at least q. Thus

$$|O_A-I_{C,r}|\leq m/(4q).$$

The earlier single-runner interval bound, summed over k components, gives

$$E_A\leq\frac{3k}{16}\left(\frac1q+\frac1{2q+r}+\frac1u+\frac1v\right)
\leq\frac{21k}{32q}.$$

Combining them,

$$U_A\geq I_{C,r}-\frac{8m+21k}{32q}. \tag{3}$$

In particular, q greater than $(8m+21k)/(32I_{C,r})$ suffices for positive clear duration. Equation (2) also supplies the more conservative explicit condition $q>2M^2(8m+21k)$. These are proof-candidate implications, not sharp cutoffs.

The core, r, k, and m stay fixed in this argument. If r or the core speeds grow with q, the error constant may grow too; no all-fast-speeds conclusion is justified by this limit. The runner count remains eight. The proof uses the matching fractions 1/4 and 3/4 specific to this setup and does not establish a result for arbitrary runner counts.

## 2. Exact changes of core

Four prescribed cores were checked with the same fast extras {56,113,64,72}, and then with the same small extras {6,7,11,13}. All speeds remain distinct. We use each core's **whole** allowed set, so these durations are not directly comparable to earlier measurements restricted to J=[9/32,3/8].

| Core | Core allowed duration | Phase area I for r=1 | Full clear duration with small extras | Isolated valid times with small extras |
| --- | --- | --- | --- | --- |
| {1,4,5} | 3/8 | 801/51200 | 0 | 1/8,3/8,5/8,7/8 |
| {1,3,5} | 23/60 | 137/7200 | 199/3432 | 1/8,3/8,5/8,7/8 |
| {1,4,8} | 15/32 | 5/256 | 1347/16016 | none |
| {2,3,5} | 23/60 | 499/14400 | 111/1144 | 3/8,5/8 |

All four fast cases have positive exact one-pair lower bounds and positive clear duration. Among the small cases, that selected-pair bound is positive only for core {2,3,5}; the exact allowed sets certify the other outcomes.

Two patterns stand out:

- Cores {1,3,5} and {2,3,5} have equal total allowed duration but different phase areas. The location of their allowed time matters.
- A configuration can have both intervals and isolated valid instants. Changing core speed 4 to 3 opens intervals while preserving all four old isolated times. Changing 5 to 8 instead blocks the old odd-eighth instants and creates intervals elsewhere.

The positive-area argument does not imply that every individual opening contains useful overlap. For core {1,3,5}, the component [17/40,23/40] has K_1 identically zero. Every r=1 pair q,2q+1 has zero simultaneous-blocking duration there, including 56,113. Nevertheless the tested four extras leave clear duration 1923/50624 inside this component. Here E=1271/1822464>0, so overlap is needed for the duration accounting, but other pairs provide it. For example, pair 56,72 overlaps for 23/2016, which exceeds E. The chosen pair need not explain every opening.

## 3. What detects an isolated success

Duration accounting alone cannot distinguish no valid time from one isolated valid time. In the original tight configuration {1,4,5,6,7,11,13}:

- [9/32,1/3] contains no valid time;
- [9/32,3/8] contains the valid singleton {3/8}.

Both regions have U=0 and R=E. The exact outputs preserve this difference.

There is a simple local characterization at threshold 1/8. Suppose t is valid for all seven speeds. It is isolated if and only if both sets below are nonempty:

$$L(t)=\{a:\{at\}=1/8\},\qquad
R(t)=\{b:\{bt\}=7/8\}. \tag{4}$$

A speed in L stops blocking at t: it blocks immediately before t. A speed in R starts blocking at t: it blocks immediately after t. Both sets together eliminate the left and right neighborhoods, while equality keeps t valid.

Conversely, if either set is empty, there is a sufficiently small valid interval on at least one side. Every strictly separated runner has positive margin, and the remaining threshold contacts move in the allowed direction on that side. There are finitely many runners, so the neighborhood can be chosen for all of them. This proves the proposed local characterization; it does not prove that arbitrary configurations must possess a valid t.

For any chosen a in L and b in R, integer phases j,k satisfy

$$at=j+1/8,\qquad bt=k-1/8,$$

hence

$$ak-bj=(a+b)/8. \tag{5}$$

Therefore a+b must be divisible by 8. This recovers our earlier contact constraint. The other runners must still be checked. In the {1,4,8} small case, speeds 11 and 13 still make such an opposing contact at 3/8, but speed 8 is at an integer and blocks it. Divisibility and a pair contact alone do not certify loneliness.

The implementation partitions at every blocking boundary. It checks the predicate on each open cell and separately at every boundary, then merges the valid pieces. This independently reconstructs the complete allowed sets, including all isolated points. The same finite representation handles intervals and equality instants.

## 4. Regrouping and further controls

The original tight seven-speed set was regrouped with core {1,6,7} and extras {4,5,11,13}, using pair 4,11 (r=3). The physical configuration and its four isolated valid times are identical.

The accounting changes: the original core has R=E=34079/240240, whereas the regrouped core has R=E=1467/10010. R and E depend on the chosen core's allowed region. They are not configuration-wide invariants under regrouping. The full allowed set remains unchanged.

A second tight family uses core {1,2,4} and extras {3,5,6,7}, giving the consecutive relative speeds 1 through 7. Its only valid times are again the four odd eighths. Replacing speed 7 with 8 gives six intervals of total duration 9/160 and no isolated points. This supplies a distinct tight-to-interval control.

## 5. Reproduction and limits

Run **python -m scripts.analyze_core_transfer**. The [script](../scripts/analyze_core_transfer.py) and [exact JSON](../experiments/core_transfer.json) record:

- Six cores crossed with residuals 1,2,3, plus core {2,3,5} at residuals 5 and 8: twenty exact profiles and pair-only checks at q=56.
- Eleven prescribed full decompositions, comprising ten distinct full speed sets: the eight table cases, the consecutive tight and 7-to-8 cases, and the regrouped original tight case.
- Eleven complete allowed-set reconstructions, 44 individual endpoint-duration comparisons, and 66 pair-duration comparisons from independent interval operations.
- Eight positive-interval affine certificates and eighteen isolated-contact certificates, counting the intentionally repeated tight configuration under its two groupings.
- One zero-phase-area local control and two zero-duration endpoint controls.

All checks passed. Their finite scope does not replace the written unbounded argument or independent review.

S13, Perarnau–Serra's pair-correlation setup and geometric intersection argument, was re-opened. The proof uses established interval counting, fractional parts, and endpoint primitives; no originality is asserted. Equation (5) was already recorded in our [blocking-overlap note](BLOCKING_OVERLAPS.md). The newly documented contribution is the scoped synthesis and its explicit counterchecks, not an established new result on the general conjecture.

The resulting next question was **how to select useful blocking relationships from the configuration itself**. The zero-phase-area opening shows why selecting one pair in advance can miss the explanation. Sections 6–8 carry out the subsequently authorized bounded study, retaining endpoint contacts where no positive-duration certificate is possible. Arbitrary seven-speed coverage and independent mathematical review remain OPEN.

## 6. Selecting pairs from the configuration

**Continuation, September 24:** Vance approved the proposed selection study. We reused the eleven decompositions above (ten distinct full speed sets), without adding any speeds or scanning new configurations. Every closed core component was retained, including singleton components. The [selection script](../scripts/analyze_pair_selection.py) and [exact output](../experiments/pair_selection.json) record the six pair overlaps on each component.

For a component J, choose a pair maximizing its overlap O inside J. Since the excess E is the same for all six choices, this also maximizes O-E. Selection uses the local individual and pair durations; the full allowed set is computed separately to check the result.

The 72 core components consist of 62 positive-width intervals and ten singletons. Their outcomes are:

| Outcome or certificate | Number of components |
| --- | ---: |
| Actual positive clear duration | 38 |
| Certified by individual durations alone, -E>0 | 16 |
| Certified by the previously preferred pair | 22 |
| Certified by the best of all six pairs | 32 |
| Certified by the best tree of pair overlaps | 38 |
| Only isolated valid times | 18 |
| No valid time | 16 |

The certificate rows are nested, not disjoint categories. Counts include reflection partners and the deliberately regrouped tight configuration; they are not counts of independent random examples. The last two outcome rows together with the first partition all 72 components. Each of the eighteen isolated-only components happens to contain one valid time in these cases.

The useful pair changes with the opening. For the same extras {56,64,72,113} and core {1,4,5}, the unique largest-overlap pairs are:

| Core component in the first half-period | Best pair |
| --- | --- |
| [1/8,7/40] | 56,113 |
| [9/32,3/8] | 72,113 |
| [17/40,15/32] | 56,72 |

The reflected components have exactly the same overlaps, as expected from integer-speed symmetry under t -> 1-t. This explains the repeated pattern; it is not a separate empirical coincidence.

Choosing the best single pair still misses six positive-duration components. They are three reflection pairs: the outer components for core {1,4,8} with small extras, the outer components for core {2,3,5} with small extras, and the inner components of the consecutive 7-to-8 control. A single exceptional pair is therefore not a sufficient explanation even for our existing examples.

## 7. Several pairs can supply the certificate together

A known inequality provides a disciplined way to combine overlaps. Put the four extra speeds at the vertices of a graph, and choose a spanning tree T: three connections joining all four vertices without a cycle. Give each edge ij weight O_ij, its pair overlap duration inside J. Then

$$U_J\geq \sum_{ij\in T}O_{ij}-E_J. \tag{6}$$

This is **Hunter's tree inequality**, stated and used for Lonely Runner in S13, Perarnau–Serra, Lemma 13, equation (12). Their next sentence explicitly proposes maximizing the tree's total pair weight. For positive-length J, apply that known inequality to the uniform probability measure on J and multiply by |J|. No new inequality or literature novelty is claimed.

The counting reason is short. At a time when m blockers are active, their induced subgraph in a tree is a forest, with at most m-1 edges if m>0. Those edges therefore count no more than the m-1 redundant copies of blocking. Integrating gives the tree's total weight at most R; using U=R-E gives (6). Adding all six pairs would be unsafe: four simultaneous blockers give six pair overlaps but only three redundant copies.

There are sixteen labeled spanning trees on four vertices. The script checks all sixteen and independently compares their maximum weight with Kruskal's greedy maximum-tree algorithm. One tree is fixed over each entire core component; it is not chosen afresh on every interval of constant blocking status.

### An exact example where every single pair fails

Take core {1,2,4}, extras {3,5,6,8}, and

$$J=[9/32,7/16],\qquad E=1/20.$$

The largest individual overlap is O_3,6=1/24, so even the best pair bound is

$$1/24-1/20=-1/120.$$

The following three overlaps connect all four blockers in a tree:

| Tree edge | Overlap inside J |
| --- | --- |
| 3,6 | 1/24 |
| 3,8 | 1/64 |
| 5,8 | 1/64 |
| Sum | 7/96 |

Together they give

$$U_J\geq 7/96-1/20=11/480>0.$$

Here the lower bound is exact. The complete valid set in J is

$$[9/32,7/24]\ \cup\ [17/40,7/16],$$

whose total length is 11/480. Enough duplicate blocking is distributed across several relationships, even though no individual relationship supplies enough.

### Exactly what the tree leaves uncounted

Let S(t) be the active blockers and let c_T(S) count connected components of the induced graph T[S], including its isolated active vertices. For S nonempty, a forest has |S|-c_T(S) edges. Thus

$$R_J-\sum_{ij\in T}O_{ij}
=\int_{J:\,S(t)\ne\varnothing}\bigl(c_T(S(t))-1\bigr)\,dt. \tag{7}$$

This is our elementary local accounting derivation, marked **HYPOTHESIS/proof candidate pending independent review**, not a claim of originality. It identifies precisely the loss in the tree certificate. The bound is exact if, apart from zero-duration boundary instants, the active blockers always form a connected induced subtree whenever any are active.

The best tree gives the exact clear duration in seventeen of the 38 positive-duration components. The other 21 have positive uncounted overlap, so “the tree always captures all redundancy” is false even here.

For a concrete countercheck, use core {2,3,5}, small extras {6,7,11,13}, and J=[1/16,7/40]. The maximizing tree has edges {6,13},{7,13},{11,13}. Its bound is 263/11440; the actual duration is 63/2288. Their difference is exactly 1/220, the duration for which just blockers 6 and 11 are active. Their tree connection goes through inactive vertex 13, so the induced active graph is disconnected. This explains the missing amount without introducing a new physical variable.

## 8. Boundary contacts and the unresolved step

Trees combine duration information. They cannot establish a singleton. For example, with core {1,4,5} and small extras, the best-tree bound is zero both on [1/8,7/40], which retains {1/8}, and on [17/40,15/32], which retains nothing. Both bounds even equal the actual duration zero.

We therefore kept the complete boundary reconstruction and the opposing-contact certificates from Section 3. All eighteen valid isolated contacts survive the selection study. Some contacts involve core runners, so restricting the boundary test to the four extras would be incorrect.

**Verification:** all 432 component pair durations agree with direct interval intersections; all 1,152 tree weights have the exact status-partition gap in (7); 72 exhaustive/greedy maximum-tree comparisons agree. Eleven full boundary reconstructions match the prior complete allowed sets. Each of the 38 components with positive duration has a separate affine interval certificate. Component sums reproduce the earlier E,R,U values, and every reflection partner matches exactly. Run **python -m scripts.analyze_pair_selection** to regenerate the JSON.

This is a finite diagnostic result, not a universal tree-selection theorem. Exact overlap weights still require arithmetic work, and we have not derived speed-only conditions forcing their maximum tree weight above E in some opening. Nor have we shown that a valid opposing boundary contact must exist when no such strict bound is positive. A negative or zero lower bound by itself is inconclusive.

The resulting question was: **what arithmetic condition forces a sufficiently heavy overlap tree in at least one core opening, or a valid boundary contact when only equality is possible?** The observed success of trees suggests a specific candidate mechanism to study; it does not show that this mechanism handles arbitrary configurations. The subsequently authorized [fast-cluster continuation](FAST_CLUSTER.md) tests nearby additive patterns and gives a different constructive route for three fixed core speeds plus four speeds q+a_i with fixed offsets. It preserves the distinction between an auxiliary phase gap and an actual common-start time. A universal tree-selection guarantee remains unresolved. Further cutoff polishing is parked; independent mathematical review remains outstanding.
