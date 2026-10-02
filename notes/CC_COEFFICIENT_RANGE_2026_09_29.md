# Compatibility Calculus: the exact range of the fixed geometry

September 29, 2026. Input head: `9e72fb318d83a4556f9063553da5a0b207aec72c`.
The mathematical input is the changed-row certificate saved at
`b2404d0d8ab43373a07c45d67bf4a432a2ddbc9d`.

**Result:** the fixed two-segment geometry supports two different exact
coefficient classifications. Requiring both whole segments gives **31 positive
integer rows**. Requiring the whole leading segment and only the fallback point
actually used gives **42 infinite residue classes**. Both suffice for the same
stationary-reference witness construction, with recomputed seventh laps and
the distinct-speed conditions below.

Status: **HYPOTHESIS / internally reviewed complete proof candidate**. The
derivation, programs and separately tasked reviews are materially AI-generated.
The exact finite outputs are reproduced. This is neither external human nor
formal certification, a new existence result, nor an originality claim. The
[prior literature comparison](CC_LITERATURE_COMPARISON_2026_09_29.md) and its
source attributions remain applicable; no further priority search was made.

## 1. The question was fixed before enumeration

The [protocol](../reviews/2026-09-29-cc-coefficient-range/PROTOCOL.md) fixes
the first six coefficient rows

\[
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),
\]

the closed threshold 1/8, and the geometry selected by the
[changed-row transfer](CC_CHANGED_COEFFICIENT_TRANSFER_2026_09_29.md):

| Role | Geometry | First-six torus laps |
| --- | --- | --- |
| Leader L | y=7/8−2x, 1/4≤x≤3/8 | (0,0,0,0,1,1) |
| Full fallback F | x=1/8, 3/16≤y≤1/4 | (0,0,0,0,0,0) |
| Used fallback C | (1/8,1/4), the upper endpoint of F | (0,0,0,0,0,0) |

The seventh row is (A,B), with A,B positive integers. Its old lap labels
are not retained. We classify two **geometric proof contracts**:

- W: every point of L and every point of F is seventh-safe.
- R: every point of L and the single point C are seventh-safe.

Every segment must lie in one common lap band. The first six phases are
already safe throughout L and F: their endpoint values, in eighths on L,
are (2,3,5,7,1,4) and (3,1,4,7,2,3); in sixteenths on F they are
(2,3,5,7,9,12) and (2,4,6,8,10,14). Affinity proves the assertion between
endpoints. Equality is included.

R is an exact classification of those stated geometric obligations. It is
**not asserted to be the largest coefficient set on which every actual
output of the deterministic selector is safe**. Nor does rejection exclude
a different menu or another lonely time. This step does not re-run clipping,
discovery, optimization or the conditional parent-interior diagnostic.

## 2. Necessary and sufficient coefficient predicates

Put

\[
u=2A+3B,\qquad v=3A+B,\qquad w=A+2B,\qquad \delta=A-2B.
\]

The real seventh-safe set is the disjoint union of the closed intervals
[m+1/8,m+7/8], m integer. An affine image of a connected segment is an
interval. It lies entirely in this safe set if and only if it lies in one
component; meeting two components forces it across an unsafe gap. Thus the
following are necessary and sufficient, including the shared lap:

\[
\begin{aligned}
L\text{ safe}&\iff \exists m\in\mathbb Z:\quad
8m+1\le\min(u,v)\le\max(u,v)\le8m+7,\\
F\text{ safe}&\iff \exists n\in\mathbb Z:\quad
16n+2\le u\le u+B\le16n+14,\\
C\text{ safe}&\iff w\not\equiv0\pmod8.
\end{aligned}
\]

Here L has endpoint values u/8,v/8, F has endpoint values u/16,(u+B)/16,
and C has value w/8. If safe, the unique laps are respectively
floor(min(u,v)/8), floor(u/16), and floor(w/8). Therefore W is the conjunction
of the first two tests, and R of the first and third.

### Complete finite classification of W

The L image has width |δ|/8, and a safe component has width 3/4. Hence
|δ|≤6. The F image has width B/16, so B≤12. Positivity gives B≥1 and
2B+δ>0. These proved bounds reduce W to the protocol's 12×13 rectangle;
discarding 5+3+1 nonpositive-A entries leaves exactly **147 cases**.
This is an exhaustive finite reduction, not evidence extrapolated from a box.

| B | All A for W |
| --- | --- |
| 1 | 1, 2, 3, 4 |
| 2 | 3, 6, 7 |
| 3 | 5, 6, 8, 9 |
| 4 | 5, 7, 11 |
| 5 | 4, 10, 11, 13 |
| 6 | 9, 10, 16 |
| 7 | 9, 15, 16 |
| 8 | 14, 15, 21 |
| 9 | 20 |
| 10 | 19 |
| 11 | 25 |
| 12 | 23 |

There are 31 rows. The absolute δ bound is attained by (4,5), whose L image
is [17/8,23/8]. The B bound is attained by (23,12), whose F image is
[41/8,47/8]. Both use closed safe-band equality. W does not attain δ=+6:
its leader condition forces B≡3 mod8, and the two possibilities B=3,11
under the bound fail F safety. The necessary width bounds alone are not sufficient.

### Complete residue classification of R

Since

\[
u=7B+2\delta,\quad v=7B+3\delta,\quad w=4B+\delta,
\]

the change (A,B)↦(A+16,B+8) adds 56 to u,v and 32 to w. It preserves
the predicates, while increasing the L lap by 7 and C lap by 4.
Together with |δ|≤6, this proves reduction to **104 residue cells**.
The complete accepted table contains **42 classes**:

| δ=A−2B | All B modulo 8 for R |
| --- | --- |
| −6 | 5 |
| −5 | 0, 7 |
| −4 | 2 |
| −3 | 3, 4, 5, 6 |
| −2 | 0, 1, 5, 6, 7 |
| −1 | 0, 1, 2, 3, 4, 7 |
| 0 | 1, 3, 5, 7 |
| 1 | 0, 1, 4, 5, 6, 7 |
| 2 | 0, 1, 2, 3, 7 |
| 3 | 2, 3, 4, 5 |
| 4 | 6 |
| 5 | 0, 1 |
| 6 | 3 |

In every row retain **B≥1 and A=2B+δ≥1**. For example δ=−4,B=2 gives
A=0 and is excluded despite its residue. Each accepted cell contains
infinitely many positive rows. Periodicity is an algebraic identity, not
an inference from testing successive rows. The checker uses representatives
B=b+8, b=0,...,7, for which A is positive at every δ.

W⊂R because C belongs to F. Inclusion is proper, as (22,10) demonstrates below.

## 3. Why R supplies a physical witness

Let p,q be positive integers, d=gcd(p,q), and P=p/d,Q=q/d. Physical torus
points have Qx−Py in Z. The leader projects to

\[
I(P,Q)=\left[\frac{2Q-3P}{8},\frac{3Q-P}{8}\right],
\qquad |I|=\frac{Q+2P}{8}.
\]

Take h=ceil((2Q−3P)/8). If h≤(3Q−P)/8, use

\[
x=\frac{8h+7P}{8(Q+2P)},\qquad y=7/8-2x.
\]

Every interval of length at least one contains this first integer. The
complete primitive complement Q+2P<8 consists of eight pairs:

| (P,Q) | I(P,Q) | h | Leader hit |
| --- | --- | --- | --- |
| (1,1), repeated-speed auxiliary | [−1/8,1/4] | 0 | yes |
| (1,2) | [1/8,5/8] | 1 | no |
| (1,3) | [3/8,1] | 1 | yes |
| (1,4) | [5/8,11/8] | 1 | yes |
| (1,5) | [7/8,7/4] | 1 | yes |
| (2,1) | [−1/2,1/8] | 0 | yes |
| (2,3) | [0,7/8] | 0 | yes |
| (3,1) | [−7/8,0] | 0 | yes |

Only (1,2) uses C, where Qx−Py=0. This gives primitive time 1/8 and
physical time 1/(8d). Thus safety of unused F points is unnecessary for
this construction. Coverage uses the width proof and complete complement,
not the 54 physical implementation controls.

For any selected point and its integer h, choose rP+sQ=1 and set

\[
T=rx+sy,\quad N=\lfloor T\rfloor,\quad
\tau=T-N,\quad t=\tau/d.
\]

For coefficient row (a,b) with torus lap m, let

\[
\ell=m+(-as+br)h-(aP+bQ)N.
\]

Then (ap+bq)t=ℓ+(ax+by−m). Indeed PT=x−sh and QT=y+rh, giving this
identity directly. The selected coordinates are strictly between zero and
one, so 0<τ<1. An alternative Bezout choice changes T by an integer and
leaves τ unchanged. R supplies the correct seventh m; all seven fractional
phases are in [1/8,7/8]. The fourth leader phase is 7/8 and the first C
phase is 1/8, so the selected minimum distance is **exactly 1/8**.

The physical speeds, including stationary reference 0, are distinct exactly
when

\[
p\ne q,\qquad (A-a)p+(B-b)q\ne0
\quad\text{for }(a,b)\in\{(1,1),(2,1),(3,1),(3,2)\}.
\]

Positivity makes Ap+Bq exceed p,q; the four other core speeds strictly
increase and exceed both. The accepted rows (1,1),(2,1),(3,1),(3,2)
duplicate core rows identically, so their eight-distinct-speed domains are
empty. Labelled geometric safety still holds. Do not compress this into
31 nonempty eight-runner families.

## 4. An infinite family with exactly the same selected phases

For every integer k≥0, set

\[
(A,B)=(6+16k,2+8k).
\]

On L, 16x+8y=7; at C it equals 4. Hence the new seventh phase equals the
old (6,2) phase, but its torus lap is **2+7k on L** and **1+4k at C**.
All six other rows are unchanged. The selector depends only on p,q, so
the selected point, time and entire fractional phase vector remain the
same for every k. This is a uniform identity. The seventh speed exceeds
3p+2q, making p≠q the only distinctness restriction for this progression.

At k=1, row (22,10) belongs to R but not W. F's endpoint seventh values
are 37/8=4+5/8 and 21/4=5+1/4. Both residues are safe, but at the interior
point (1/8,9/40) the value is exactly 5: a collision. This ambient control
refutes whole-F safety and the shortcut of checking endpoint residues
without a shared lap. It does not exhibit a failed physical selector.

The protocol also fixes two distinct-speed physical failures of this geometry:

| Row (A,B) | (p,q) | Fixed-selector output | Seventh phase | Meaning |
| --- | --- | --- | --- | --- |
| (4,2) | (1,2) | C, t=1/8 | 0 | Whole-L safety alone omits the needed fallback |
| (5,2) | (2,3) | Left endpoint of L, t=1/8 | 0 | This leader fails for the old row |

The earlier successful (5,2) construction used different geometry and is
preserved. Neither failure means the configuration has no lonely time.

## 5. Exact checks, review and information retained

The [review package](../reviews/2026-09-29-cc-coefficient-range/README.md)
contains the frozen protocol, full positive finite table, complete residue
table including rejections, physical records and separate reviews. Run:

```sh
python3 reviews/2026-09-29-cc-coefficient-range/reproduce.py
```

The coordinator tests scaled integer band containment and recovers time
with Bezout coefficients. The algebra reviewer instead intersects affine
images with open forbidden bands. The physical reviewer uses coordinate
congruences: Qi≡−h modP, 0≤i<P, j=(Qi+h)/P, τ=(x+i)/P and physical lap
m+ai+bj. Neither reviewer imports the coordinator code. Their initial
outputs preceded the coordinator implementation; the coordinator then read
the review outputs/code. These are separately structured, parallel reviews,
not a claim of blind replication.

Both classifications agree throughout their complete reduced domains. The
54 progression controls use only k=0,1,2 and the prior 18 p,q pairs: 51
distinct-speed configurations and three repeated-speed auxiliaries. All
selected/reflected phases and laps agree, and all 18 k=0 records reproduce
the archive. All 36 k>0 controls expose wrong phase reconstruction from
stale seventh labels. The two negative physical controls fail as predicted.
The algebra reviewer corrected a mistaken expected case count (144→147)
before producing JSON; its predicates and trial domain were unchanged.

The CC checkpoint identifies four consequential distinctions:

- Whole-segment safety and safety at the point used for an exceptional
  direction are different obligations. The conditional role of C is needed.
- Safe endpoint residues do not preserve connected safety without the
  common lap. Row (22,10) is an explicit failure test.
- Equal fractional phases do not preserve integer laps. New coefficients
  must pass through physical recovery even when the selected time is unchanged.
- Exactness of W/R, sufficiency for this selector, and existence of some
  other witness are different claims. Coefficient positivity and physical
  distinctness also remain separate.

The smaller R representation retains L, C, their coverage roles, shared
lap conditions, primitive normalization and recovery. It can omit F away
from C for this one-witness operation; the pinned old certificate recovers
the fuller geometry when a new operation needs it. No replacement ambient
model is required for the present question.

**Next proposed:** determine the closure of the points actually selected on
L as primitive P,Q vary, then ask whether requiring all of L is necessary
for uniform success of this exact deterministic selector. This is a distinct
necessity question; no such classification, new scan, or extra physical
trial has been performed here. External mathematical review remains open.
