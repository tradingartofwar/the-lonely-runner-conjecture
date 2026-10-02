# Two prescribed times give an exact all-phase certificate

September 28, 2026. Scope: the two velocity lists and two time pairs frozen in
`protocol.json`, reference 0, n=8, threshold 1/8. Only speed 11's starting phase
may vary. AI materially contributed the derivation, checking, and writing.
No additional velocity or test-time search was performed.

**Finite result (OBSERVED):** both prescribed pairs succeed. For V=16, at
least one of 7/15 and 8/15 has every runner at distance at least 2/15 for
every starting phase of speed 11. This gives the uniform strict margin
`2/15−1/8=1/120`. For V=13, at least one of 1/8 and 7/8 is safe for every
phase, with equality retained. The general circle argument making these
finite certificates sufficient is supplied below as a **HYPOTHESIS / proof
candidate**, under the repository's evidence rules.

The certificate does not require constructing the complete unchanged safe
set A or its projection. Its inputs are 24 directly checked unchanged
distances, two circular phase separations, and the original threshold.

## The two-time lemma

Suppose the unchanged runners have distance at least c at both times t1,t2.
Let the chosen runner's unshifted phases at those times be x1,x2, with
circular separation d. After an arbitrary common phase shift theta, the two
phase points still have separation d. The circle's triangle inequality gives

\[
d\le\|x_1+\theta\|+\|x_2+\theta\|.
\]

At least one chosen-runner distance is therefore at least d/2. At that time
every runner's distance is at least

\[
\gamma=\min\{c,d/2\}.
\]

Thus `gamma>=1/8` supplies an all-phase witness among the two times, and
`gamma>1/8` supplies a uniform strict margin. Endpoint equality is valid.
The phase-only criterion `d>=2gamma` is exact for obtaining a chosen-runner
distance of at least gamma from this pair for every phase: when `d<2gamma`,
centering the shorter connecting arc at zero puts both distances below gamma.
This statement concerns the fixed pair, not an optimal choice of times.

### Why some two-time certificate is complete at this threshold

There is a stronger supplied circle argument. For a nonempty compact phase
set P, let c(P) be its minimum covering-arc length. For `0<a<=1/3`,

\[
c(P)\ge a\quad\Longleftrightarrow\quad
\text{some }x,y\in P\text{ have }\|x-y\|\ge a.
\]

The reverse implication is immediate: an arc shorter than a cannot contain
such a pair. For the forward implication, argue contrapositively. Rotate a
point of P to zero. If every pair distance is less than a, all points have
unique lifts in `(-a,a)`. Compactness gives minimum and maximum lifts with
span `w<2a`. If `w>=a`, then `w<2a<=1−a` makes their circular distance
`min(w,1−w)` at least a, a contradiction. Thus P lies in an arc of length
`w<a`.

Let A be the unchanged safe set and `P={11t mod1:t in A}`. All-phase
nonemptiness means that no translated **open** blocking arc of length
`a=1/4` contains P. By compactness this is equivalent to `c(P)>=a`: fitting
inside an open arc leaves a positive endpoint margin and hence a shorter
closed covering arc. The equivalence above then supplies two phases at
separation at least a, and their safe-time preimages give a two-time
certificate. Therefore **existence of some two-time certificate is complete
for all-phase nonemptiness** in this setting. Success of an arbitrary
preselected pair is not guaranteed, and the result does not show that a
given runner configuration has the required covering span.

A strict version needs the unchanged margins. For `a<1/3`, the same argument
with weak pairwise inequalities shows that `c(B)>a` forces a pair in B with
separation strictly greater than a: otherwise lifts in `[-a,a]` have span
`w<=2a<1−a`, and pairwise distance at most a forces `w<=a`.
For the present finite nonzero-speed constraints, interiors of positive
unchanged-safe components are strict, and their phase images are dense in
the closed bulk support B. A pair separated by more than a can therefore be
approximated by phases of two strict unchanged-safe times while preserving
that separation. Those two times have positive unchanged margins, and the
two-time lemma gives a positive uniform strict margin. This explains the
additional assumptions needed for a completeness statement about strictness;
it does not change the zero margin of the prescribed 13 pair.

These are general proof candidates derived without additional velocity or
time examples, not finite-output extrapolations or established novelty claims.

## Exact arithmetic of the prescribed pairs

The unchanged speed order is `(1,4,5,6,7,V)`. Reflection makes their distance
vectors identical at the two times in each row.

| V | Prescribed times | Unchanged distance vector | Speed 11 phases | Separation d | Guaranteed gamma |
| ---: | --- | --- | --- | --- | --- |
| 13 | 1/8, 7/8 | (1,4,3,2,1,3)/8 | 3/8, 5/8 | 1/4 | 1/8 |
| 16 | 7/15, 8/15 | (7,2,5,3,4,7)/15 | 2/15, 13/15 | 4/15 | 2/15 |

For V=16, unchanged speed 4 has distance exactly 2/15 at both times. For
V=13, unchanged speeds 1 and 7 have distance exactly 1/8 at both. Consequently
the better of the two minimum distances is **exactly gamma for every phase**,
not merely bounded below by gamma: the unchanged constraints supply the upper
bound at each time. This identifies the exact performance of each prescribed
pair. It makes no claim that either pair attains the best possible time in
the full schedule.

A simple selection rule is to choose the first time whenever speed 11's
shifted distance there is at least gamma, and the second otherwise. In the
V=16 case the first time fails that test only for
`theta in (11/15,1)` modulo one. In the V=13 case it fails only for
`theta in (1/2,3/4)`. The open endpoints are important: equality passes.

### A finite integer certificate

For a test time `t=a/b` and target `gamma=p/q`, let `r_v=va mod b`. An
unchanged speed meets the target exactly when both integers

\[
q r_v-pb,\qquad q(b-r_v)-pb
\]

are nonnegative. Put both chosen phases over common denominator L, and let
s1,s2 be their residue numerators. With
`Delta=min(|s1−s2|,L−|s1−s2|)`, the separation condition is the integer
inequality

\[
q\Delta-2pL\ge0.
\]

The archive records all 48 unchanged endpoint slacks and the two separation
slacks. For 13, `(p,q,L,Delta)=(1,8,8,2)`; for 16 they are `(2,15,15,4)`.
Both separation slacks are zero. These nonnegative integer inequalities plus
the supplied circle lemma are a compact sufficient certificate for every
initial phase, with no reconstruction of A.

## A strict interval can be extracted from the 16 certificate

Circular distance changes by at most `v|Delta t|` for speed v. At either
prescribed time, the unchanged runners' individual margins above 1/8,
divided by speed, are

\[
(41/120,\ 1/480,\ 1/24,\ 1/80,\ 17/840,\ 41/1920).
\]

They therefore remain safe throughout a symmetric radius `R=1/480`.
Whenever the selected center has shifted speed 11 distance at least 2/15,
that runner remains safe throughout radius
`rho=(1/120)/11=1/1320`. Hence at every phase at least one of the two fixed
menu intervals is entirely safe:

\[
[41/88,617/1320],\qquad[703/1320,47/88].
\]

Each has width 1/660 and a strict interior. The checker directly certifies
unchanged-runner safety on both by single-lap endpoint inequalities; the
phase-dependent runner uses the center margin. These intervals are derived
from the prescribed times, rather than found by a further time search.

One-sided geometry gives a larger sufficient width without changing the
test times. At a selected center let l,r be speed 11's distances in time to
its two safe-lap endpoints. They obey `l,r>=rho` and `l+r=3/44>2R`. At least
one side reaches the full unchanged-safe radius R. The common interval has
width

\[
\min(l,R)+\min(r,R)\ge R+\rho
=1/480+1/1320=1/352.
\]

This interval can depend on the phase; the earlier two intervals are a fixed
menu. Both bounds are weaker than the previous phase-union bound 1/176.
Their purpose is a small, independently checkable existence and margin
certificate, not an optimal duration estimate.

For V=13, the prescribed times cannot yield strict neighborhoods. At 1/8,
speed 1 is at a lower threshold and speed 7 at an upper threshold; moving
left immediately violates speed 1 and moving right violates speed 7. At
7/8 the roles reverse. Thus these are isolated points of the unchanged safe
set, regardless of speed 11's phase. The pair proves an equality witness for
every phase, while the prior phase-union argument supplies strict intervals
elsewhere whenever the phase is nonzero.

## Comparison with the previously certified phase subsets

The checker revalidates two known safe intervals in each case by their endpoint
inequalities only; it does not enumerate the rest of A.

| V | Unchanged-safe intervals | Centered speed 11 image union | Width | Consequence |
| ---: | --- | --- | ---: | --- |
| 13 | [17/48,3/8] and its reflection | [−1/8,1/8] | 1/4 | D13(theta) >= min(||theta||,1/4)/11 |
| 16 | [25/56,15/32] and its reflection | [−5/32,5/32] | 5/16 | D16(theta) >= 1/176 for every phase |

For 13, the image union exactly matches the blocking-arc width. Any nonzero
translation leaves positive phase length uncovered, but theta=0 can cover
its entire interior. For 16, the phase union exceeds the blocking-arc width
by 1/16, so every translation leaves at least that much phase length; pulling
back by speed 11 gives 1/176. These are sufficient subset arguments. They do
not identify full multiplicity, exact duration profiles, or optimal phases.

The compact pair and these interval subsets answer different questions. The
13 pair protects existence even when the bulk phase arc is exactly covered,
using isolated unchanged-safe times. The 16 pair certifies an explicit
uniform distance margin from two times; the interval subset gives a better
duration bound. No extra phase profile or test-time search is needed for
either conclusion.

The full projection archive now supplies a precise comparison. For 13, the
known interval subset already spans the entire bulk support B. The two extra
isolated projection points are exactly `3/8,5/8`, the phases of the prescribed
time pair. Thus the compact pair uses the part of P that bulk duration
calculations discard. The true minimum duration is zero only at phase zero,
while the true maximum is 115/2184; the pair itself continues to return
threshold witnesses at every phase.

For 16, the full bulk adds the arcs `[19/56,45/128]` and
`[83/128,37/56]` to the previously certified phase union. Each extra arc has
length 11/896. The full bulk measure is therefore
`5/16+11/448=151/448`. Since a blocking arc removes at most 1/4 of this
measure, the complete support gives the uniform bound

\[
D_{16}(\theta)\ge\frac{151/448-1/4}{11}=39/4928.
\]

The exact profile attains this value, so this support-measure bound is sharp
for the fixed configuration. Its improvement over 1/176 is precisely 1/448,
the common-start duration of the two outer allowed intervals. The profile's
minimum occurs on `[0,1/48]` and `[47/48,1)` modulo one, and its maximum is
7/96. These exact profile values come from the separately computed complete
archive; they were not used to choose the candidate times or derive their
certificates. The standalone comparison checks subset containment and the
measure arithmetic and pins that archive's hash.

## Reproduction and limits

```bash
python -B reviews/2026-09-27-phase-projection/arithmetic_check.py --check
```

The standalone checker uses the Python standard library and imports no project
implementation. Its compact certificates read only the frozen protocol; a
separate comparison reads the primary full profile archive. It checks the four prescribed
times, 24 unchanged distances, two phase separations, four previously certified
safe intervals, and two derived fixed menu intervals, using exact rational and
integer arithmetic. `arithmetic.json` pins the protocol and script hashes.
The all-phase implications and the interval deductions are supplied arguments,
not numerical phase-grid evidence or a formal machine proof. No general
Lonely Runner or global-optimality claim is made.
