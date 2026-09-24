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

The useful next question is **how to select useful blocking relationships from the configuration itself**. The zero-phase-area opening shows why selecting one pair in advance can miss the explanation. A bounded next step could compare which pair certifies each existing core opening, retaining endpoint contacts where no positive-duration certificate is possible. No such systematic selection study has been run. Arbitrary seven-speed coverage and independent mathematical review remain OPEN.
