# Other-ray arithmetic review — September 29, 2026

**Verdict:** no arithmetic defect found in the assigned statement. The changed
orbit equation, all directed peak-edge losses, all 63 unbounded-domain upper
comparisons, and the physical witness/lap formulas survive this fresh exact
countercheck. The fixed-cell completeness and optimizer-face reductions remain
premises of this arithmetic review. This is an internal AI countercheck, not
external mathematical certification, formal verification, or a novelty claim.

Scope: eight common-start runners, stationary selected reference, moving speeds
`B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2)`, integer `q>=2`. No new family, reference
runner, physical optimum scan, or literature search was introduced.

**Provenance and dependency boundary.** The assigned frozen research head is
`12d08824ead7b772032ba240d0e858250fbd183c`. The supplied local tree has no `.git`,
so this reviewer cannot independently authenticate that commit using local Git.
The coordinator is responsible for reconciling it with the live repository.
The script records SHA-256 hashes of unchanged written mathematical, governance,
and review-protocol inputs.

Before authoring code, I read `AGENTS.md`, current README and HANDOFF entries,
`CLAIM_STATUS.md`, `CONTRIBUTING.md`, this review's `PROTOCOL.md`, and both target
mathematical notes. The current-entry documents at that reading had hashes:

- `README.md`: `bd8434e9d042acd76250121a72a7ef677a45845c78696baf9bac13d810012bfc`.
- `HANDOFF.md`: `48cbb661b4e5731b2111db8256b50994dda0b653989a82a409d41c7b99112f09`.

These two historical read hashes are deliberately absent from the script's
runtime hash dictionary: adding the coordinator's new current-state summaries
must not change the mathematical output.

I authored `arithmetic_check.py` before opening any original mathematical
implementation or saved JSON output. I have not opened any such original code
or output during this review. The script imports only Python's standard library
and no project helper. The written peak coordinates, directions, and edge
lengths are explicit input data, so their completeness is not independently
established by this file. Written lower witness formulas and the explanatory
seven-row loss table are comparison targets. The checker derives its global
winning directions from the full 21-direction list before comparing them with
the claimed winners.

Reproduce from the repository root:

```bash
python3 reviews/2026-09-29-cc-other-ray-review/arithmetic_check.py > reviews/2026-09-29-cc-other-ray-review/arithmetic_check.json
```

The saved output reports PASS. All computations use integer and rational
arithmetic. Polynomial identities are exact coefficient identities; rational
function identities use polynomial cross multiplication. An affine inequality
on `q>=q_min` is certified by its nonnegative slope and nonnegative value at
`q_min`, with strictly positive starting value when strictness is required.
There is no extrapolation from sampled `q` values.

**Orbit condition and reflection.** With `x={qt}`, `y={t}`, write
`qt=x+j`, `t=y+l` with integer laps. Then `x-qy=ql-j` is integral.
Conversely, `x-qy=h` and `0<x,y<1` give `qy=x-h`, hence `{qy}=x` at physical
time `t=y`. Consequently each `(a,b)` form has the physical fractional phase
of speed `aq+b`. Swapping the first two coefficient rows recovers the displayed
order of `B_q`.

At positive separation none of these fractional phases is zero. Reflection
therefore gives `(x,y)->(1-x,1-y)` and `H->1-q-H`, preserving integrality and
all distances. Folding **x** does not require `y<=1/2`. The residue-5 chart has
`y>1/2` and must be reflected to get the stated selected time. For residue 3,
both C and G lie on the folding boundary `x=1/2`; they already represent the
two reflected physical times. Counting them as two unrelated reflection pairs
would double-count.

Direct peak congruences give precisely:

| q mod 6 | Compatible peaks | Smallest q>=2 |
| --- | --- | --- |
| 0 | none | 6 |
| 1 | A | 7 |
| 2 | none | 2 |
| 3 | C, G | 3 |
| 4 | E | 4 |
| 5 | none | 5 |

In particular, the residue-1 domain starts at 7, not 1. The lower formulas use
`k>=1` there and in residue 0, and `k>=0` in the other four residues.

**Directed losses and strict comparisons.** On an outward peak edge,
`H=h0+d e`, with `h0=x0-qy0` and `d=alpha-q beta`. Every one of the 21
projections is nonzero and has constant sign for `q>=2`. In fact the supplied
directions make its sign `-sign(beta)` already for every `q>0`. For nonconstant
residues the peak fractional part `rho={h0}` is nonzero. The first directed
integer hit has loss `rho/(-d)` if `d<0`, and `(1-rho)/d` if `d>0`.
This directional distinction is necessary; replacing the numerator by the
nearest undirected integer distance would change some losses.

The independently derived complete table below gives **six times** the first
integer-hit loss. It refers to the ray extending each edge, whether or not
that first hit lies in the finite edge.

| Peak | Direction (alpha,beta) | q=0 mod 6 | q=2 mod 6 | q=5 mod 6 |
| --- | --- | --- | --- | --- |
| A | (-1,2) | 1/(2q+1) | 5/(2q+1) | 2/(2q+1) |
| A | (1/5,-1) | 25/(5q+1) | 5/(5q+1) | 20/(5q+1) |
| A | (1,-1) | 5/(q+1) | 1/(q+1) | 4/(q+1) |
| B | (-1,1) | 1/(q+1) | 3/(q+1) | 3/(q+1) |
| B | (-1,4) | 1/(4q+1) | 3/(4q+1) | 3/(4q+1) |
| B | (1,-2) | 5/(2q+1) | 3/(2q+1) | 3/(2q+1) |
| C | (-3,5) | 3/(5q+3) | 1/(5q+3) | 4/(5q+3) |
| C | (0,-1) | 3/q | 5/q | 2/q |
| C | (0,1/2) | 6/q | 2/q | 8/q |
| D | (-1,2) | 3/(2q+1) | 5/(2q+1) | 5/(2q+1) |
| D | (0,-1/2) | 6/q | 2/q | 2/q |
| D | (0,1) | 3/q | 5/q | 5/q |
| E | (-2,1) | 2/(q+2) | 4/(q+2) | 1/(q+2) |
| E | (0,1) | 2/q | 4/q | 1/q |
| E | (1,-2) | 4/(2q+1) | 2/(2q+1) | 5/(2q+1) |
| F | (-1,2) | 3/(2q+1) | 1/(2q+1) | 1/(2q+1) |
| F | (0,-1) | 3/q | 5/q | 5/q |
| F | (0,1/2) | 6/q | 2/q | 2/q |
| G | (-3/5,1) | 15/(5q+3) | 25/(5q+3) | 10/(5q+3) |
| G | (0,-1/2) | 6/q | 2/q | 8/q |
| G | (0,1) | 3/q | 5/q | 2/q |

For two such losses, positive denominators reduce comparison to an affine
cross product. The checker records all 63 cross products against the derived
winner. Three are the winner's self-comparison, identically zero. All other
60 have a strictly positive starting value and nonnegative slope on their
whole domains. The unique winners are B's `(-1,4)` direction in residue 0,
C's `(-3,5)` in residue 2, and F's `(-1,2)` in residue 5.

All 63 additional comparisons against the note's within-peak minima also
pass. The nontrivial within-peak tie at `q=2` is D's `(-1,2)` versus
`(0,-1/2)`: the cross product is `q-2`. This is far above the global winning
loss, so it does not weaken global strictness.

**Finite edges and endpoints.** The checker derives ambient lap labels at each
peak, then checks the bands, `z>=1/8`, and `x<=1/2` at both ends of every
supplied edge. Linearity gives feasibility along each whole segment. Both
endpoints have active-normal rank three; their common active normals have
rank two. Thus all 21 supplied directions and lengths really describe edges
of their associated cells. This verifies the listed local data but does not
exclude additional cells or edges omitted from the input table.

An extended-ray first hit beyond an edge's endpoint is harmless for the upper
bound: it only gives an unattainable lower bound on the loss, making that edge
less competitive. For example, B's residue-2 `(-1,4)` first hit at `q=2`
has loss `1/18>1/24`, and E's residue-0 `(-2,1)` first hit at `q=6` has loss
`1/24>1/42`. The checker derives, algebraically and without a parameter scan,
the first admissible q in each residue when every extended-ray first hit
enters its edge. The three actual winners are feasible from their first
allowed q onward: their largest losses are `1/150`, `1/78`, and `1/66`,
respectively. Each is strictly smaller than `1/42` and hence `1/24`.

**Witness and physical-lap transfer.** Substituting the derived winning losses
recovers the claimed values and times. At `q=6k+r`, the selected folded charts
and their integer `H` values are:

| r | Folded chart | H | Reflect to selected t? |
| --- | --- | --- | --- |
| 0 | B + e(-1,4) | -2k | no |
| 1 | A | -k | no |
| 2 | C + e(-3,5) | -k | no |
| 3 | C | -k | no |
| 4 | E | -5k-3 | yes |
| 5 | F + e(-1,2) | -4k-3 | yes |

The ambient labels are derived by taking floors at the peaks. Along these
safe segments the labels stay fixed. The identity
`(aq+b)y = ax+by-aH` proves the unreflected physical lap formula
`ell=m-aH`. Reflection changes it to `(aq+b)-1-ell` and complements the
fractional phase. After the first-two-coordinate permutation, every derived
lap equals the corresponding written lower-witness lap polynomial.

The checker verifies all 42 polynomial phase identities and all 84 band
inequalities in the recovery note over their full k domains. It separately
checks 42 ambient-to-physical transfer identities and 42 reflected phase/lap
identities. Positive A and D, with `A<=R<=D-A`, certify the actual floors as
well as circular safety. The stated opposing contacts occur in all three
nonconstant branches. It also proves `7A>D` and `0<2N<D`, so every witness
has value strictly above `1/7` and yields two distinct reflected times.

**What this establishes conditionally.** Assuming the complete fixed-cell
height/edge classification and the slice-vertex reduction, the strict loss
comparisons force every maximizing slice vertex in the nonconstant branches
to be the single first contact on the stated winning edge. The objective
decreases strictly along each such edge; a later integer hit cannot tie. An
optimal slice face whose vertices all equal this one point is that point,
so there is no hidden optimal segment. The winner has `x<1/2`; undoing the
fold produces precisely the two distinct reflected times. In constant
branches, the peak congruences leave only A, C/G, or E and hence the same two
physical times `1/6,5/6`. Arithmetic alone does not prove that the supplied
list exhausts every possible optimal slice vertex.

**Simplification and information retained.** The modular numerator can be
computed without nested fractional parts: let `c=6x0-q(6y0)` modulo 6. For
`c` in `{1,...,5}`, the sixfold directed loss is `c/|d|` when `d<0` and
`(6-c)/|d|` when `d>0`. The proof then consists of seven fixed peak records,
the sign of 21 affine projections, three residue comparisons, and one lap
transport identity. The 63 comparisons are finite arithmetic certificates,
not 63 independent experiments.

The seven-row minimum table is an adequate summary for determining the
winning *value*, once its reduction is checked. It alone would lose the
direction identity, global strictness, and finite-edge membership needed for
the claimed witness and uniqueness. Likewise, folding without the physical
time/lap map would lose the residue-5 time and the boundary double-counting
distinction in residue 3. The present code retains those data explicitly.
No additional geometry, universal transfer rule, arbitrary-speed result, or
promotion from proof candidate is justified by this arithmetic success.
