# Separate coverage review — September 29, 2026

**Status:** HYPOTHESIS / internally reviewed proof candidate. This separately
tasked AI review found no defect in the proposed two-segment coverage argument.
It is not independent human review, formal verification, or a novelty finding.

**Question:** Do the two already retained segments contain an actual-orbit
point for every positive primitive pair (P,Q), at closed threshold 1/8, for
the seven rows (1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2)? The selected
reference is stationary and all runners have a common start. A separate orbit
review must justify conversion of an integral H=Qx-Py into physical time.

The protocol pins the source branch at
`1696035e73bb53764f431237794cfca342dad002` and the preceding mathematical
package at `e37858ffd238a668682289280ee26c6c5e8a0646`. The two segments and
labels are those in `notes/CC_BOUNDED_SELECTOR_2026_09_29.md`, with provenance
P1:E1-3:K1 and P3:E0-1:K2 retained in the later discovery/transfer package.
The present proof needs their explicit affine geometry and labels; it does not
assume that the atlas is complete or that its discovery rule is optimal.

## 1. Joint safety on the entire segments

P1 has x in [1/8,5/24], y=7/8-3x and labels (0,0,0,0,0,1,1).
Its seven labelled phases are

\[
x,\quad 7/8-3x,\quad 7/8-2x,\quad 7/8-x,\quad
7/8,\quad 3/4-3x,\quad 3/4-x.
\]

P3 has x in [3/8,1/2], y=9/8-2x and labels (0,0,0,1,1,1,2).
Its phases are

\[
x,\quad 9/8-2x,\quad 9/8-x,\quad 1/8,\quad
1/8+x,\quad 5/4-x,\quad 1/4+x.
\]

The endpoint values are as follows, in native row order.

| Segment endpoint (x,y) | Seven phases |
| --- | --- |
| P1: (1/8,1/2) | 1/8, 1/2, 5/8, 3/4, 7/8, 3/8, 5/8 |
| P1: (5/24,1/4) | 5/24, 1/4, 11/24, 2/3, 7/8, 1/8, 13/24 |
| P3: (3/8,3/8) | 3/8, 3/8, 3/4, 1/8, 1/2, 7/8, 5/8 |
| P3: (1/2,1/8) | 1/2, 1/8, 5/8, 1/8, 5/8, 3/4, 3/4 |

Each phase is affine, so the two endpoint bounds imply the closed band
[1/8,7/8] throughout the segment. These are joint phases at one point,
not independently realizable marginal ranges. The fifth phase on P1 and
fourth phase on P3 have distance exactly 1/8 everywhere. Once time recovery
is justified, every selected witness therefore has minimum distance exactly
1/8. That fact does not make it an optimal witness.

## 2. Projection and the infinite tail

On P3,

\[
H=(Q+2P)x-9P/8,
\quad I_3(P,Q)=\left[\frac{3(Q-P)}8,\frac{4Q-P}8\right],
\quad |I_3|=\frac{Q+2P}{8}.
\]

The derivative Q+2P is positive, so this is the exact image of the entire
closed segment. If Q+2P>=8, the interval has width at least one. For every
real L, the integer ceil(L) satisfies L<=ceil(L)<L+1; hence it lies in every
closed interval [L,U] of width at least one. Put

\[
h=\left\lceil\frac{3(Q-P)}8\right\rceil,
\qquad x=\frac{8h+9P}{8(Q+2P)},\qquad y=9/8-2x.
\]

Whenever h is at most the upper endpoint, this inverse formula gives the
unique point of P3 with H=h. The width argument proves success on the entire
unbounded domain Q+2P>=8; no finite scan is used to extrapolate this claim.

## 3. Complete finite complement

Positive P,Q with Q+2P<8 have P<=3: P>=4 would give Q+2P>=9.
The possibilities are P=1 with Q=1,...,5; P=2 with Q=1,...,3; and
P=3 with Q=1. Removing the sole nonprimitive pair (2,2) leaves exactly
eight primitive pairs. Their exact P3 intervals and first integers are:

| (P,Q) | P3 interval | ceil(lower) | Covered by P3? |
| --- | --- | --- | --- |
| (1,1) | [0,3/8] | 0 | yes; repeated-speed auxiliary |
| (1,2) | [3/8,7/8] | 1 | no |
| (1,3) | [3/4,11/8] | 1 | yes |
| (1,4) | [9/8,15/8] | 2 | no |
| (1,5) | [3/2,19/8] | 2 | yes |
| (2,1) | [-3/8,1/4] | 0 | yes |
| (2,3) | [3/8,5/4] | 1 | yes |
| (3,1) | [-3/4,1/8] | 0 | yes |

For P1, the corresponding exact image and inverse formula are

\[
I_1(P,Q)=\left[\frac{Q-4P}8,\frac{5Q-6P}{24}\right],
\quad |I_1|=\frac{Q+3P}{12},
\quad x=\frac{8h+7P}{8(Q+3P)},\quad y=7/8-3x.
\]

At (1,2), I1=[-1/4,1/6] contains h=0 and gives (x,y)=(7/40,7/20).
At (1,4), I1=[0,7/12] contains only h=0 and gives (x,y)=(1/8,1/2).
These cover the only two P3 misses. This proves the required geometric
coverage for all positive primitive pairs, including the separately labelled
auxiliary (1,1).

The second fallback is an essential closed endpoint. Replacing P1 by its
relative interior makes its image (0,7/12), which contains no integer; P3
already misses (1,4). Thus deleting the endpoints breaks this two-segment
certificate. It does not establish a claim about the absence of safe points
elsewhere in the full atlas.

## 4. Domain, recovery and cost boundary

For raw positive p,q, first set d=gcd(p,q), P=p/d and Q=q/d. The integral
orbit test needed here is Qx-Py in Z, equivalently qx-py in dZ. The proof
above addresses that primitive test. Physical recovery requires the separate
Bezout construction, followed by division of primitive time by d. Merely
checking qx-py in Z is insufficient when d>1.

All seven speeds p,q,p+q,2p+q,3p+q,3p+2q,5p+2q are positive. The last
five strictly increase and exceed both p and q. Consequently all eight
speeds, including the stationary reference, are distinct precisely when
p!=q. In the primitive domain P=Q implies (P,Q)=(1,1); that case remains
an explicitly repeated-speed auxiliary, not an eight-distinct-runner example.

The selector uses at most two integer roundings and interval tests after gcd
reduction. This is not a constant bound for the complete algorithm: computing
gcd and Bezout coefficients by extended Euclid has an input-dependent iteration
count, and integer bit lengths also grow. No constant bit-cost claim follows.

The result selects one safe time for the stationary reference. It neither
optimizes the separation nor lists every maximizing or safe time. It does not
settle all reference runners or arbitrary seven-speed configurations. It is a
new analytic coverage argument for two existing segments, not a retuning or
rerun of the archived frozen discovery procedure. No external result is
imported and novelty remains OPEN.

## 5. Reproduction and representation checkpoint

Run from the repository root:

```sh
python reviews/2026-09-29-cc-two-parameter/coverage_checks.py
```

The script writes `coverage_checks.json`. It computes the 28 endpoint phases
and their 56 band inequalities, checks projection coefficients as exact affine
functions of P,Q, enumerates only the proved finite complement, reconstructs
all its selected points and verifies the endpoint-removal failure. Fractions
are exact. The infinite assertion rests on sections 2–3, not on the finite
output or agreement between AI systems.

The two-edge record retains joint phase bands, labels, primitive orbit
compatibility, equality and the recovery interface. It deliberately omits
most safe points, optimum values and other references. Those omissions do
not obstruct the selected-witness question but do obstruct stronger uses;
the pinned full atlas remains the recovery source. The change from one ray
to two parameters needs the added gcd/Bezout layer and revised cost claim.
Ordinary affine geometry and integer interval arithmetic suffice for this
coverage step; no richer geometric model is presently needed for this exact
output. Any changed row, threshold, reference or requested output requires
a fresh adequacy check.

The protocol's original proposed gcd-negative fixture was not used as
coverage evidence. Its corrected arithmetic and replacement are preserved
by the coordinator/orbit review; the finite cover above is unaffected.

## 6. Coordinator note cross-check

After completing this review, I read the main claim and sections 2–4 of
`notes/CC_TWO_PARAMETER_WITNESS_2026_09_29.md` against the derivation above.
The segment domains, row order, lap labels, seven affine phase lists,
projected endpoints and widths, finite-complement table, inverse formulas,
fallback times and closed-endpoint requirement are transcribed correctly.
The note excludes p=q from its main distinct-speed assertion and limits its
output to one stationary-reference witness. No transcription or quantifier
correction is required in those sections. This cross-check adds no computation
or broader claim.
