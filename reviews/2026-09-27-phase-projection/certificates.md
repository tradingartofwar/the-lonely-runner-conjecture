# Two fixed times certify every phase

Scope: only the two time pairs frozen in `protocol.json`, SHA256
`8eba9a06595a2014095f84cc22c6b91d65d6f9fd71771912e0af368293bdff17`.
Eight runners, reference 0, threshold 1/8; only speed 11 may have initial
phase theta. The unchanged speeds are 1,4,5,6,7,V with V=13 or V=16.
This is a materially AI-generated exact calculation and supplied geometric
certificate. Its general mathematical interpretation remains subject to
the repository's proof-review rules; no novelty or global optimality claim
is made. No additional time candidates are tested.

**OBSERVED:** on these two fixed pairs, the exact full two-time margin is
constant over the entire phase circle, respectively 1/8 and 2/15.

Define the two-time separation margin

`M(theta)=max over declared times t of min(||11t+theta||, min unchanged v ||vt||)`.

This is a distance, not an allowed duration. The primary profile D(theta)
instead measures the set of all safe times during [0,1]. A two-time witness
can certify existence without calculating D or the full allowed time set.

## Exact constants and proof

For two phase points x,y at circular separation d, every rotation theta
obeys `max(||x+theta||,||y+theta||)>=d/2`. Otherwise their circle distances
to zero would sum to less than d, contradicting the triangle inequality.
Equality is attained by rotating the midpoint of their shorter arc to zero.
Thus this raw speed-11 best-of-two worst-case margin is exactly d/2.

If all unchanged runners have distance at least c at both declared times,
one of those times has full separation at least `min(c,d/2)` for every theta.
Here each time has an unchanged runner attaining c, and c=d/2 in both cases.
Consequently the full two-time margin is identically c over the entire phase
circle: the upper cap and the geometric lower bound agree pointwise.

Endpoint equality is essential for the V=13 certificate. At theta=1/2,
speed 11 has distance exactly 1/8 at both declared times. Both remain valid
under the original weak inequality; an argument that replaced the strict
blocking arc by a closed one would incorrectly discard them.

| V | Declared times | Unchanged distances at either time, speed order 1,4,5,6,7,V | Speed-11 phases at the two times | Circular separation d | Exact M(theta), every theta |
| ---: | --- | --- | --- | --- | --- |
| 13 | 1/8,7/8 | 1/8,1/2,3/8,1/4,1/8,3/8 | 3/8,5/8 | 1/4 | 1/8 |
| 16 | 7/15,8/15 | 7/15,2/15,1/3,1/5,4/15,7/15 | 2/15,13/15 | 4/15 | 2/15 |

The distances agree at complementary times because all unchanged speeds are
integers. For V=13 the unchanged bottlenecks are speeds 1 and 7. For V=16
the unchanged bottleneck is speed 4. The V=16 separation exceeds the required
threshold by exactly `2/15-1/8=1/120`, uniformly over theta.

The raw speed-11 maximum is minimized only at theta=1/2 for V=13 and theta=0
for V=16, with respective minima 1/8 and 2/15. These are **not** the argmin
sets of full M: since M is constant, its argmin is the entire phase circle.
The finite affine archive records both objects separately.

## Consequences and limitations

For V=13, at least one declared time is valid for every initial phase of
speed 11. These two times never establish strictness: unchanged runners
remain exactly at threshold at both times, independently of theta. That
limitation says nothing about whether other times are strict.

For V=16, one declared time is strictly safe for every initial phase, with
uniform excess at least 1/120. Continuity then gives positive allowed duration
for every theta. The value 2/15 is the exact robust margin for **this pair**;
it is not asserted to be the best achievable margin over all times or all
candidate pairs, nor is it the value or minimum of D(theta).

Thus both all-phase existence statements bypass enumerating A, its phase
projection, its multiplicity, and the duration profile. Those richer objects
answer different questions: where other witnesses lie and how much time is
available. A fixed finite witness certificate need not reproduce them.

## Comparison with the independently calculated duration profile

Only after completing the certificate calculation, compare the primary
`results.json` profile. Its exact duration ranges are

| V | Full two-time distance margin M(theta) | Minimum D(theta) | Maximum D(theta) |
| ---: | ---: | ---: | ---: |
| 13 | Constant 1/8 | 0, only at theta=0 | 115/2184, throughout [1/4,3/4] |
| 16 | Constant 2/15 | 39/4928, for theta in [-1/48,1/48] modulo 1 | 7/96, throughout [61/128,67/128] |

For V=13, D is positive at every nonzero phase, although the two declared
times are never strictly safe. More sharply, theta=1/2 minimizes the raw
speed-11 best-of-two distance while it **maximizes** D. There is no
contradiction: fixed-time distance and total safe-time measure answer
different questions, and the strict witnesses at theta=1/2 occur elsewhere.

For V=16, the certificate already proves strictness everywhere without
computing D. A crude explicit duration consequence is also available: every
distance function is at most 16-Lipschitz in time, so an excess of 1/120 at
the chosen time gives a closed allowed interval of radius 1/1920 and strict
interior. Both declared times are far enough from 0 and 1 to retain the
whole interval. Thus `D(theta)>=1/960` follows directly from the compact
certificate. The primary exact minimum `39/4928` is larger; `1/960` is a
derived sufficient lower bound, not an estimate claimed to be sharp.

## Exact continuum verification

`python -B reviews/2026-09-27-phase-projection/certificates.py --check`
rebuilds `certificates.json` read-only. `--write` writes that owned archive.
The script uses only protocol inputs and standard-library rational arithmetic;
it neither imports project helpers nor reads the primary D profile.

Breakpoint completeness is explicit. A circular distance changes affine
formula only when its phase reaches 0 or 1/2. Clipping at an unchanged cap c
adds only crossings of raw distance with c. On the resulting cells, taking
the maximum of two affine functions adds only their exact equality point.
All these points are generated algebraically. Therefore the recorded affine
formulas and endpoint evaluations cover every phase, rather than merely a
finite sampled grid. Phase 1 is identified with 0 and is not duplicated in
the event-point list. The full-margin argmin is serialized as `full_circle`.

Only the two frozen pairs are evaluated. No extra times, configurations,
references, phase grid, external publication, or novelty claim are added.
