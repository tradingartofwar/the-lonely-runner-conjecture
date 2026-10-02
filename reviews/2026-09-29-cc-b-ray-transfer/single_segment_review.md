# Post-protocol review: one segment suffices for B

September 29, 2026. Author: the separate internal AI physical reviewer
`b_physical_review`. Status: **PASS / internally checked proof candidate**.

This follow-on was explicitly requested after the frozen two-segment transfer
and its review. `POST_PROTOCOL_SIMPLIFICATION.md` was read before executing the
additional physical checks. It records that the discovery reviewer noticed
P3:E0-1:K2 already covers both q=2 and q=3 in the frozen matrix and has tail
cutoff Q=4. This is a simplification extracted after the result. The original
rule, tie-break, two-segment answer and review files remain unchanged.

## Formula recovered from the segment

The P3 segment in original coordinates is

    3/8 <= x <= 1/2,  y=9/8-2x.

Its original local labels are (0,0,0,1,1,1,2). In canonical coordinates u=y,
v=x, its endpoints are (1/8,1/2) and (3/8,3/8), and its line is
v=9/16-u/2. The actual B-ray orbit integer is g=qu-v. Solving this equation
gives the single-segment selector

    g=floor((q+3)/8),
    t=u=(16g+9)/(8(2q+1)).

The formula therefore uses one integer rounding and one rational clock
recovery, independently of the magnitude of q. Arithmetic bit cost may grow
with q.

## All-q coverage and physical safety

The projected closed interval is

    [(q-4)/8, 3(q-1)/8].

Its width (2q+1)/8 is at least 1 for q>=4. The chosen integer is precisely the
ceiling of the lower endpoint. To verify the floor/ceiling conversion without
a finite q scan, write q=8a+r: for each of the eight possible r, the checker
certifies 0<=8g-q+4<8. Width then guarantees this integer lies below the upper
endpoint. For q=2, the interval is [-1/4,3/8]; for q=3 it is [-1/8,3/4]. Both
contain the chosen g=0. These cases and the width argument exhaust all q>=2.

The seven display-ordered phases on the segment, at its two canonical
endpoints, are:

| Physical speed | Phase at (u,v)=(1/8,1/2) | Phase at (u,v)=(3/8,3/8) |
| --- | --- | --- |
| 1 | 1/8 | 3/8 |
| q | 1/2 | 3/8 |
| q+1 | 5/8 | 3/4 |
| 2q+1 | 1/8 | 1/8 |
| 3q+1 | 5/8 | 1/2 |
| 3q+2 | 3/4 | 7/8 |
| 5q+2 | 3/4 | 5/8 |

These entries describe the affine torus phases; an endpoint itself need not
be on a given q's physical orbit. Every affine interpolation remains in the
closed band [1/8,7/8]. At the integer hit, the identity

    (aq+b)t = (ax+by-m) + (m+a*g)

proves those are the actual physical phases, with physical laps m+a*g.
The phase for speed 2q+1 is identically 1/8, so every selected separation is
exactly 1/8. Reflection gives the same distances, phases 1-phi, and laps
speed-1-lap. The integer hit, rather than an arbitrary endpoint, supplies
the physical witness.

## Exact checks and provenance

`single_segment.py` is a separate standard-library checker. It reads the
frozen P3 endpoints and labels from `transfer.json` as claims under test and
imports neither discovery/adapter code nor the earlier physical checker.
It independently recovers the line, clock formula and projected interval.

Only the already declared q=2,...,25 receive direct physical evaluation. There
are 24 additional selected/reflected pairs: 48 time records and 336 exact
distances. Every selected and reflected phase and lap passes the direct
speed-times-time floor check. The universal certificate separately retains
28 endpoint inequalities, the eight rounding residue identities, the width
bound and the two small prefix cases. No optimizer or new physical q value
was used. The q=2 result is t=9/40; the q=3 result is t=9/56; the equality
endpoint at q=4 is t=1/8.

The script records SHA-256 hashes of the protocol, input, checker and four
original output/review files, and verifies those original files did not
change. Reproduction from repository root:

    python reviews/2026-09-29-cc-b-ray-transfer/single_segment.py

Output: `single_segment.json`.

The useful distinction is between finding a sufficient cover and minimizing
its size. The frozen minimum-cutoff/provenance rule succeeds at the first
task, but its output is not minimal here. This case supports simplifying its
output; it does not establish that a greedy pruning procedure would always
find a minimum cover elsewhere. The physical clock, lap map, closed endpoints
and richer discovery provenance must remain attached to the one-segment
record.

This is internal AI review, not independent human certification or a blind
test. It asserts one safe physical time in the B-ray family only, not optimal
values, all witnesses, transfer to another family, novelty or formal proof.
