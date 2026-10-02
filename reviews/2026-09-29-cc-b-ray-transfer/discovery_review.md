# B-ray discovery: separate arithmetic reconstruction

September 29, 2026. **Proof candidate with exact internal reproduction.** This
review was separately authored by an AI reviewer within the same model/context.
It is not independent human review, formal verification, or a novelty claim.

## Read order and separation

Read AGENTS.md, the frozen B-ray transfer PROTOCOL.md, the parent-only
PARENT_INPUT.json, CLAIM_STATUS.md, and CONTRIBUTING.md. To preserve the task's
source isolation, current handoffs and discovery notes were not used for this
reconstruction. No A discovery code/output, B coordinator adapter/result, or B
spectrum was read to choose geometry, ranking, exceptions, or times. Prior work
was present in shared conversational context; the calculations here were freshly
implemented from parent vertices, original edge IDs, labels, and constraints.

The script imports only Python standard-library modules. Its initial output was
frozen before comparison as discovery_review.json, SHA256
`4519659164950de54f411e7bccf7d1e76e1d6e203727230c8080e4e65bf4ec23`.
The JSON records the exact parent-input hash and every candidate and interval.

Reproduce from repository root:

```sh
python reviews/2026-09-29-cc-b-ray-transfer/discovery_review.py
```

## Reconstruction and selection

Work in the native parent coordinates (x,y), with physical clock t=y and
integer orbit h=qy-x. Orient clipped endpoints by (y,x). Retain the fold
x<=1/2; no fold on time is assumed. Read only edges with both endpoint heights
z=1/8. Intersect their added phase 5x+2y with every closed band
[k+1/8,k+7/8], retaining singleton and horizontal-clock candidates.

The resulting inventory is 24 original floor edges and 27 clipped candidates.
For oriented displacement (dx,dy) with dy>0, assign

\[
Q=\max\left(2,\left\lceil\frac{1+dx}{dy}\right\rceil\right).
\]

Candidates with dy=0 receive no sufficient tail cutoff, but remain eligible
for finite prefix coverage. The minimum cutoff is Q=4; two candidates tie.
The frozen provenance tie-break selects parent P1, edge (1,3), added lap k=1.
Its prefix is q=2,3. It covers q=3 and misses q=2. The greedy largest-gain
rule, with the same provenance tie-break, selects parent P3, edge (0,1),
added lap k=2 to cover the remaining q=2. The Q>26 guard is not triggered.
The JSON carries every tail cutoff, prefix interval, and integer test.

No candidate or ranking adjustment was needed after the protocol.

## Tail and prefix proof

The first selected segment has endpoints

\[
A=(5/24,1/4,1/8),\qquad B=(1/8,1/2,1/8),
\]

parent labels (0,0,0,0,0,1), and added lap 1. Its orbit image is

\[
[q/4-5/24,\;q/2-1/8]
=\left[\frac{6q-5}{24},\frac{4q-1}{8}\right],
\]

of width (3q+1)/12. For every integer q>=4 the width is at least 13/12,
so the closed interval contains an integer. At q=3 the interval is
[13/24,11/8], containing 1. At q=2 it is [7/24,7/8], containing none.
Thus the first candidate fails exactly q=2 over the declared domain q>=2.
For q>=3 the least integer is

\[
h=\left\lceil\frac{6q-5}{24}\right\rceil
=\left\lfloor\frac{q+3}{4}\right\rfloor,
\qquad
 t=\frac{24h+7}{8(3q+1)}.
\]

The rounding equality follows from division into the four integer residues of
q modulo 4. The time formula follows by solving 3x+y=7/8 and qy-x=h.

The second selected segment has endpoints

\[
C=(1/2,1/8,1/8),\qquad D=(3/8,3/8,1/8),
\]

parent labels (0,0,0,1,1,1), and added lap 2. Its orbit image is
[(q-4)/8,3(q-1)/8]. At the only required fallback q=2, the interval is
[-1/4,3/8], containing 0. Solving 2x+y=9/8 and 2y-x=0 gives
(x,y)=(9/20,9/40), hence **t=9/40**.

The implementation checks the two segment intervals in order; it does not
encode q=2 as an unexplained exception. Selection uses at most two integer
roundings and interval comparisons, then one affine interpolation. This is a
bound on the count of arithmetic operations, not a constant bit-time claim.
Numerators, denominators, and their arithmetic cost grow with q.

## Endpoint safety, equality, and physical recovery

All seven labeled phases are affine on each segment. Their endpoint vectors
in the original row order are:

| Endpoint | Seven labeled phases |
| --- | --- |
| A | (5/24, 1/4, 11/24, 2/3, 7/8, 1/8, 13/24) |
| B | (1/8, 1/2, 5/8, 3/4, 7/8, 3/8, 5/8) |
| C | (1/2, 1/8, 5/8, 1/8, 5/8, 3/4, 3/4) |
| D | (3/8, 3/8, 3/4, 1/8, 1/2, 7/8, 5/8) |

Every entry lies in the closed interval [1/8,7/8]. Convexity gives safety
at every selected point, including all equalities. On the primary segment
the fifth phase is constantly 7/8; on the fallback the fourth is constantly
1/8. The selected points therefore have minimum separation exactly 1/8,
which does not claim these times are optimal.

For an original row (a,b), speed aq+b, and ambient lap m, the same selected
point satisfies x=qy-h. Therefore

\[
(aq+b)t = ax+by+ah,\qquad
\ell=m+ah,\qquad
(aq+b)t-\ell=ax+by-m.
\]

The final quantity is the safe phase proved above. Thus the orbit integer,
clock, laps, and all seven phases belong to one point. Displaying B_q with
speed 1 first requires the same first-two permutation of speeds, labels,
phases, and laps. The script's JSON deliberately retains original row order.
Reflection t -> 1-t has lap speed-1-ell and phase 1-phase, preserving safety.
No premise requires the selected physical time to be <=1/2.

## Scope and limits

The proof uses a sufficient two-segment cover for one safe time in the declared
B family, selected reference, and common-start setting. It does not establish
optimal values, all maximizers, the full safe set, other references, or a
procedure guaranteed to succeed on every parent model. Parent completeness
and the correctness of supplied parent incidence are frozen dependencies,
not independently reconstructed here. The two-segment safety argument itself
needs only the displayed endpoints and labels, not completeness of the atlas.

The retained data support the requested selection operation: endpoint values,
closed bands, orbit sign, parent provenance, labels, and physical recovery.
The remaining candidate geometry and full parent input remain available to
recover omitted information before a broader operation. No physical control
beyond the archived q=2,...,25 was generated; those JSON point records are
recovery certificates, not an optimum search. Universal coverage comes from
the interval-width proof and explicit finite prefix, not sample agreement.

## Comparison status

Initial reconstruction and report were frozen before reading coordinator results.
The pre-comparison report SHA256 was
`0aac58a7c9c8d31be3fe667d5dc997ed9263e35ea7b7ccf4515d38e034b203fd`.
After notification, the separate `--compare` mode read transfer.json. It matched
all 27 candidates' original provenance, native endpoints, labels, displacements,
source-edge clipping parameters, and tail cutoffs; all 54 finite-prefix Boolean
entries; the chosen order; and all 24 archived-scope recovered points, clocks,
orbit integers, and physical laps. No defect was found in this arithmetic scope.

Compared coordinator output SHA256:
`9ee2a034051b60b376bd3ec84de092ec5a2509c8871d5e3ddda881228feb7095`.
The frozen reviewer JSON was not changed by this comparison.

```sh
python reviews/2026-09-29-cc-b-ray-transfer/discovery_review.py --compare
```

## Post-freeze redundancy observation

The frozen coverage matrix contains a useful extra deduction: the fallback
P3:E0-1:K2 has Q=4 and covers both q=2 and q=3. Consequently, **that single
segment alone covers every integer q>=2**. For q>=4 its orbit width
(2q+1)/8 is at least 9/8; its intervals at q=2 and q=3 contain 0.
Its all-q rounding formula would be

\[
h=\left\lceil\frac{q-4}{8}\right\rceil
 =\left\lfloor\frac{q+3}{8}\right\rfloor,
\qquad t=\frac{16h+9}{8(2q+1)}.
\]

This is an exact consequence of the already frozen candidate matrix and
endpoint certificate, not another physical scan. It was recognized after the
frozen reconstruction and comparison; it is not a change to the tested rule.
The frozen rule still returns two candidates because its initial tie-break
uses provenance rather than finite-prefix coverage. It is correct for bounded
selection but does not minimize selected count. A later deletion check could
remove a redundant selected candidate, or a revised tie-break could be tested;
either would need its own declared protocol. No such algorithm revision was
made here. The observation distinguishes successful transfer from optimal
compression of the transferred result.
