# LTCM continuation recovery: distinguish the two parameter rays

September 29, 2026. Preservation base: `908a089ac39f9af796d6261d22f8b37009b1eb53`,
branch `research/near-doubling-overlap-2026-09-24`.

**Status:** the recent four-row spectrum formula is **HYPOTHESIS**. Its exact
maxima are **OBSERVED** for every integer q=2,...,150 in the reproduction below.
Explicit symbolic witnesses establish the lower-bound half, subject to the
repository's review standard for AI-generated derivations. A matching universal
upper bound for this ray remains **OPEN**. No novelty claim or independent
review is asserted. AI materially supplied the recovery, derivation, code,
checks, and writing.

## 1. The correction that must survive the handoff

The two-parameter family under discussion was

\[
V(p,q)=(p,q,p+q,2p+q,3p+q,3p+2q,5p+2q).
\]

The original, already committed LR-2 candidate fixes p=1:

\[
A_q=V(1,q)=(1,q,q+1,q+2,q+3,2q+3,2q+5).
\]

Its [five-branch spectrum candidate](LTCM_EXACT_SPECTRUM_2026_09_29.md) contains
both witnesses and a matching upper-bound argument using ten ambient cells.
The [Ultra review](LTCM_ULTRA_REVIEW_2026_09_29.md) applies to that statement.
It was saved in commits `8a967b30fcd73abd814e4c8f7f53f216c4b3f61e` and
`908a089ac39f9af796d6261d22f8b37009b1eb53`, respectively.

The unsaved continuation instead displayed

\[
B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2).
\]

This is **V(q,1), with its first two coordinates permuted**, not V(1,q).
Accordingly, the recent objective should be called M_B(q), or M(q,1) in the
original two-parameter notation, not M(1,q). Both have seven moving relative
speeds and a stationary reference: n=8 total common-start runners.

The distinction changes the answer even at small parameters:

| q | M_A(q), original ray | M_B(q), recent ray |
| --- | --- | --- |
| 2 | 1/6 | 2/13 |
| 4 | 1/8 | 1/6 |

These two controls were recomputed exactly during preservation. The families
cannot be identified by permutation or a common speed scaling, since either
operation preserves the optimum. The original tight13 example belongs to A_4.

The initial continuation also incorrectly described the original ray's upper
bound as unfinished. Its full candidate argument was already in the repository.
The upper bound left open here is for B_q. Ultra's earlier verdict does not
automatically review this changed statement.

## 2. Preserve the recent formulas with their correct scope

For integer q>=2 define

\[
M_B(q)=\max_{0\le t\le1}\min_{v\in B_q}\|vt\|.
\]

The proposed value F_B and an explicit attaining witness for that value are:

| q mod 6 | F_B(q) | Selected t(q) | Limiting contact at the selected time |
| --- | --- | --- | --- |
| 0 | \(2q/[3(4q+1)]\) | \((4q/3+1)/(4q+1)\) | q and 3q+1 |
| 2 | \((5q+2)/[6(5q+3)]\) | \((5q+8)/[6(5q+3)]\) | 2q+1 and 3q+2 |
| 5 | \(q/[3(2q+1)]\) | \(2q/[3(2q+1)]\) | 3q+1 and 3q+2 |
| 1, 3, 4 | \(1/6\) | \(1/6\) | Residue-dependent contacts |

This is a four-row rule with six residue states, distinct from the original
five-branch rule for A_q. For B_q the proposed formula agrees with the exact
optimum in all 149 reproduced cases q=2,...,150. The universal equality
M_B=F_B is still a hypothesis; the certificates below prove M_B>=F_B.

## 3. Symbolic physical phases and lap vectors

Write q=6k+r. In each branch set t=N/D and F_B=A/D. Let ell be the physical
lap vector in the displayed order of B_q. The following identities hold
coordinate by coordinate:

\[
v_iN=\ell_iD+R_i,\qquad A\le R_i\le D-A.
\]

Thus R_i/D is the actual fractional phase, every circular distance is at
least F_B, and a coordinate with R_i=A or D-A attains it. Since A>0 and D>0
on the stated domain, these inequalities also certify 0<R_i<D and therefore
the claimed floor/lap labels. No search over laps is required.

### Residue 0: q=6k, k>=1

\[
N=8k+1,\quad D=24k+1,\quad A=4k,
\]
\[
\ell=(0,2k,2k,4k,6k,6k+1,10k+1),
\]
\[
R=(8k+1,4k,12k+1,16k+1,20k+1,4k+1,12k+1).
\]

The allowed numerator band is [4k,20k+1]. The q coordinate meets its lower
boundary; 3q+1 meets its upper boundary. Hence they supply opposing contacts.

### Residue 2: q=6k+2, k>=0

\[
N=5k+3,\quad D=30k+13,\quad A=5k+2,
\]
\[
\ell=(0,k,k,2k+1,3k+1,3k+1,5k+2),
\]
\[
R=(5k+3,15k+6,20k+9,5k+2,20k+8,25k+11,25k+10).
\]

The band is [5k+2,25k+11]. The contacts are the lower phase of 2q+1 and the
upper phase of 3q+2. The endpoint k=0, q=2 is included.

### Residue 5: q=6k+5, k>=0

\[
N=12k+10,\quad D=36k+33,\quad A=6k+5,
\]
\[
\ell=(0,2k+1,2k+1,4k+3,6k+4,6k+5,10k+8),
\]
\[
R=(12k+10,18k+17,30k+27,12k+11,30k+28,6k+5,6k+6).
\]

The band is [6k+5,30k+28]. The upper contact is 3q+1 and the lower contact
is 3q+2. N/D need not be in lowest terms for these identities to hold.

### Residues 1, 3, and 4

Here N=1, D=6, A=1:

| r | k domain | Physical laps ell | Phase numerators R |
| --- | --- | --- | --- |
| 1 | k>=1 | (0,k,k,2k,3k,3k,5k+1) | (1,1,2,3,4,5,1) |
| 3 | k>=0 | (0,k,k,2k+1,3k+1,3k+1,5k+2) | (1,3,4,1,4,5,5) |
| 4 | k>=0 | (0,k,k,2k+1,3k+2,3k+2,5k+3) | (1,4,5,3,1,2,4) |

Every entry is in [1,5], and the speed-1 coordinate has distance 1/6.

The reproduction script checks all 42 polynomial phase identities. It checks
84 affine inequalities R_i-A>=0 and D-A-R_i>=0 by recording each slope and its
value at the smallest admissible k. Nonnegative slopes and starting values
certify the inequalities on the whole unbounded domain, not a finite sample.
These are new certificates for B_q; they are not the 84 upper-bound
comparisons in the original A_q proof package.

For a fixed lap vector, the old exact certificate remains

\[
L_\ell=\max_i\frac{\ell_i+\delta}{v_i},\qquad
R_\ell=\min_i\frac{\ell_i+1-\delta}{v_i}.
\]

A common safe time exists in that cell exactly when L_ell<=R_ell. The formulas
above supply ell and a time in that interval directly at delta=F_B(q).

## 4. Exact bounded optimum reproduction

The preserved [verification script](../reviews/2026-09-29-ltcm-other-ray/verify.py)
uses only standard-library integer and rational arithmetic. It does not use
the proposed formula to generate or prune optimizer candidates.

For each B_q it enumerates:

- both endpoints of [0,1/2];
- every time m/(v+w) in that interval for distinct speeds v,w;
- every individual tent peak (2j+1)/(2v) in that interval.

Why this is complete for a fixed positive integer input: a positive local
maximum of the lower envelope either occurs at an individual tent peak or
has an active rising tent and an active falling tent. In the latter case the
phases sum to one, so (v+w)t is integral. A zero of any tent has objective zero
and cannot beat the positive witnesses already supplied. Away from these
events the envelope has nonzero slope and cannot maximize. Reflection
t -> 1-t gives the other half of the period. Including extra non-opposing
m/(v+w) times is harmless because all seven distances are evaluated there.

The run produced:

- 149 exact maximum matches, q=2,...,150; zero exceptions;
- 384,107 distinct candidate times summed across the half-period calculations;
- every proposed witness among the corresponding exact maximizing times;
- actual physical lap, phase, distance, and active-speed records for every case;
- all 42 symbolic identities and 84 unbounded-domain safe-band inequalities;
- the two family-distinction controls in Section 1.

Candidate counts are processing counts, not independent experiments. This
finite optimum check is not the missing infinite upper-bound proof.

Reproduce from the repository root:

```bash
python3 reviews/2026-09-29-ltcm-other-ray/verify.py > /tmp/ltcm-other-ray-verification.json
```

The complete [saved output](../reviews/2026-09-29-ltcm-other-ray/verification.json),
[protocol](../reviews/2026-09-29-ltcm-other-ray/PROTOCOL.md), and
[manifest](../reviews/2026-09-29-ltcm-other-ray/MANIFEST.json) preserve the inputs,
results, scope, and file hashes. This run supplies a reproducible record for
the earlier conversational claim; no earlier execution log was recovered.
The archived Ultra opposing-contact method was inspected before implementing
this run, so it is a reproduction, not an independently authored review.

## 5. What this preserves about LTCM

The useful conceptual proposal from the continuation is:

> Propagate a rule for generating compatible contact configurations, rather
> than requiring every new witness to be inherited from an old safe cell.

For this family, q selects a residue state, that state selects a contact pair
and a rational time, and the formulas recover the physical laps and an exact
safety certificate. This is a concrete arithmetic selector of witnesses.

The selector performs a fixed number of residue tests and rational operations;
integer bit lengths still grow with q. The exhaustive reproduction algorithm
does grow with q. Keep the witness selector and its bounded testing procedure
distinct. Until the matching upper bound is established, its selected contact
is analytically certified at the claimed value and observed to be globally
optimal only in the stated finite range.

The earlier tight13 lesson remains: an inheritance-only rule using only cells
feasible at the smaller system's stronger threshold can miss valid witnesses.
The original spectrum note gives the precise counterexample. That motivates
generating new compatible labels, but does not prove a universal induction or
show that arbitrary configurations have a comparably small arithmetic state.

Fixed-torus geometry, integer-orbit compatibility, polyhedral certificates,
and residue selection have existing precedents already discussed in the
original candidate and review. No new prior-art assessment was performed for
B_q in this preservation task, and novelty remains OPEN.

## 6. Resume from the correct state

1. Keep A_q's completed, internally reviewed proof candidate intact. Its saved
   next question compares the six-coordinate model with the appended seventh
   constraint, seeking a transferable rule.
2. Keep B_q's newly preserved selector and symbolic lower bound separate. To
   continue this ray, derive and challenge its matching upper bound. A possible
   route is the same fixed two-coordinate ambient model, but the physical
   compatibility condition changes: A_q uses qx-y in Z, whereas B_q uses
   x-qy in Z, with x and y retaining their original meanings. Any folded-domain
   or reflection convention must be carried through that transfer explicitly.
3. Do not describe either ray as a solution for arbitrary speeds, every reference
   runner, or the full Lonely Runner Conjecture. Do not transfer an Ultra verdict
   from one parameterization to the other without checking the argument.

This save task performs no new upper-bound derivation, team review, main-branch
merge, literature search, external contact, recurring work, or broader scan.
The scientific content is preserved as a research note, not a private-chat
transcript.
