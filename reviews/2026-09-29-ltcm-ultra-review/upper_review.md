# Exact spectrum: global upper-bound review

Date: 2026-09-29. Candidate frozen commit: `8a967b30fcd73abd814e4c8f7f53f216c4b3f61e`.

**Result: no counterexample or substantive gap found in the global upper-bound argument.** Conditional on completeness of the printed ten-cell vertex certificate and the slice-vertex lemma, the 21 peak-edge directions give the claimed upper bound for every integer `q>=2`. A fresh exact checker reconstructed all edge adjacencies from the printed vertices and defining inequalities and certified all 84 comparisons over their entire unbounded domains. This is an internal AI review, not independent human review, formal verification, or a novelty determination. The candidate's HYPOTHESIS/proof-candidate status is unchanged.

## Scope and independence

I read the repository instructions, current continuity, the candidate note, and this review's protocol. Before opening the original `audit.py`, I wrote and ran `upper_check.py` using only the printed coefficient rows, labels, vertex table, and proposed branch domains. It imports no project module and reads no archived JSON. It uses exact standard-library rational arithmetic.

The new checker independently reconstructs adjacency by the rank of common active facet normals. All nonsingleton cells have affine dimension three, and each printed vertex has three independent active normals. A pair of distinct vertices lies on an edge precisely when its common active normals have rank two. It finds 45 edge occurrences, including precisely 21 incident to the seven height-`1/6` peaks. Their directions and lengths match the note exactly. Every other printed vertex has height at most `1/7`.

This checks adjacency and the upper-bound consequences of the printed vertex list. It does **not** independently prove that the list contains every ambient vertex; the fixed-cell reviewer owns that premise. No physical-parameter scan or new family was computed here. Finite arithmetic evaluations concern the domain endpoints `q=3,5,6,10` and exceptional `q=4`, all within the authorized range; they are symbolic inequality and edge checks, not exhaustive physical optimum calculations.

Reproduction:

```bash
python3 reviews/2026-09-29-ltcm-ultra-review/upper_check.py
```

The output is `upper_check.json`, including all 21 reconstructed directions, sign checks, 84 inequalities, domain-endpoint ties, and the exceptional `q=4` ranges.

## Why the peak-edge reduction is sufficient

Choose a maximizing **vertex** of a nonempty physical slice of a cell. The slice-vertex lemma places it at an original vertex or on an original edge. If its height is strictly greater than `1/7`, an edge containing it must have an endpoint above `1/7`, because height is affine along the edge. The only such endpoints are the seven peaks at `1/6`. All 21 incident edges were reconstructed, including the shorter E edge ending at `(2/7,6/7,1/7)`.

Thus no other edge, nonpeak vertex, or constant-height lower face can create a missed maximum **above** `1/7`. This argument intentionally does not rule out lower faces at height exactly `1/7`; none can contradict a proposed upper bound at least `1/7`.

One wording improvement is advisable, without changing the proof: replace “Any slice maximum strictly above `1/7` must lie ...” by “If a slice maximum is strictly above `1/7`, a maximizing slice vertex can be chosen, and it lies ...”. The proof needs that existence statement, not an assertion about every point of a maximizing face.

## Integer arithmetic and projection signs

For peak P and an outward edge parameterized by

\[
(x,y,z)=(x_0+\alpha e,y_0+\beta e,1/6-e),\qquad e\ge0,
\]

the physical height is `H=h0+(q alpha-beta)e`, where `h0=q x0-y0`. If `rho={h0}` is nonzero, the first nonnegative loss that can reach an integer is

\[
d(q)=\begin{cases}
\rho/|q\alpha-\beta|,&q\alpha-\beta<0,\\
(1-\rho)/|q\alpha-\beta|,&q\alpha-\beta>0.
\end{cases}
\]

Every later integer requires at least this much loss. For **each of the 21 directions**, the denominator has a fixed nonzero sign for all real `q>=2`. The checker verifies that the signed affine denominator has nonnegative slope and a strictly positive value at `q=2`. No division-by-zero or sign-change case was suppressed.

Every peak has `6x0` integral, so the fractional part of `h0` depends only on `q mod 6`. The complete list of integral peaks by residue is: A in residue 1, B in residue 2, and none in residues 0, 3, 4, 5. Thus there is no missed height-`1/6` branch. The A/B peak witnesses and the ambient upper bound settle residues 1 and 2.

Dropping an edge's finite length is valid for the upper bound: it replaces the actual permitted interval by a larger ray, so its first possible integer hit provides a necessary lower bound on loss. A predicted hit beyond the finite edge creates a spurious competitor, which can only weaken the upper bound. It cannot eliminate a genuine competing maximum. For the **winning** directions, the checker separately verifies that the selected first hit is within the real edge throughout the applicable domain.

## Unbounded inequalities, including ties

For each direction the checker writes its loss as `n/(a q+b)` with a positive denominator on `q>=2`. If the proposed winning loss is `nw/(aw q+bw)`, the desired comparison is exactly

\[
[n a_w-n_w a]q+[n b_w-n_w b]\ge0.
\]

The checker verifies a nonnegative slope and a nonnegative value at the smallest allowed `q`. This proves each inequality throughout the entire real half-line from that endpoint, hence throughout the required infinite residue subsequence. It is not inference from several sample values.

| Residue | Domain start | Winning peak and direction | Winning loss | Upper bound |
|---|---:|---|---|---|
| 0 | 6 | E, `(-2,1)` | `1/[6(2q+1)]` | `q/[3(2q+1)]` |
| 3 | 3 | E, `(-2,1)` | `1/[6(2q+1)]` | `q/[3(2q+1)]` |
| 4 | 10 | E, `(-2,1)` | `1/[2(2q+1)]` | `(q-1)/[3(2q+1)]` |
| 5 | 5 | C, `(-3,5)` | `1/[3(3q+5)]` | `(q+1)/[2(3q+5)]` |

All 84 comparisons pass. The reduced A/B/C/E table in the note also agrees with the individual directions; checking all 21 directions makes any informal elimination of D, F, or G unnecessary to the proof. In particular, “C dominates G” is non-strict for the even residues: their relevant losses are identical. This is harmless and should not be interpreted as uniqueness of the winning edge.

The winning loss decreases with `q`. At each domain's smallest parameter it is at most the actual winning edge length and at most `1/42`. Therefore every displayed proposed upper bound is at least `1/7`, including the two boundary equalities. This closes the contradiction correctly: a hypothetical actual maximum greater than the proposed value would be strictly greater than `1/7`, where the peak-edge reduction applies. No strict inequality is incorrectly substituted at `q=3` or `q=10`.

The exact endpoint ties recovered from all directions are:

| q | Peak edges tied for the best loss | Half-period times from those edges |
|---:|---|---|
| 3 | B `(-1,4)`, C `(-3,5)`, E `(-2,1)` | `1/7`, `3/7`, `2/7` |
| 10 | B `(-1,4)`, C `(-3,5)`, E `(-2,1)`, G `(-3/5,1)` | `1/7`, `3/7`, `2/7`, `17/35` |

All have loss `1/42` and lie on their actual finite edges. The E hit is exactly its endpoint; the other listed hits are interior to their edges. The `q=10` G tie is useful to preserve even though the note only promises one attaining time. These are all ties among the peak-edge bounds at the two endpoints, not a separate assertion here that all possible height-`1/7` maximizers were enumerated.

## The exception q=4

The peak-edge argument alone controls maxima strictly above `1/7`, so it must not be used to infer a bound below that threshold. The note correctly supplies a separate full-cell calculation for `q=4`.

I reconstructed the range of `4x-y` on every printed cell by taking its extrema on all vertices. The ten ranges exactly match the note. Only cell 2 reaches integer level 0 and cell 5 reaches integer level 1. In each case the integer is an extreme value of the linear functional, attained at exactly one vertex. Hence its entire intersection with that integer plane is the singleton, not an overlooked face or segment. The two points are `(1/8,1/2,1/8)` and `(3/8,1/2,1/8)`. Reflection gives precisely the four threshold times stated in the candidate.

## Original audit implementation

After the fresh checker had passed, I inspected `audit.py`. Its 84 comparisons use algebraically equivalent rescaled denominators and correctly prove the same affine inequalities on the infinite domains. Its projection-sign checks are sufficient on each domain, and its `q=4` range argument matches the reconstruction. I found no mismatch between the written universal upper bound and that implementation.

The upper-bound result therefore survives the assigned adversarial review. Its remaining dependencies are the finite-cell completeness certificate and slice-vertex theorem, reviewed separately; this report does not elevate shared AI agreement into an external proof certificate.
