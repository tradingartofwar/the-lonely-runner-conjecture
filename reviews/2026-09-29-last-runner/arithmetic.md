# Integer lap obligations across the inherited core windows

September 29, 2026. Parent `f3c26e709fa1cd8945968dcd585bd012430c7243`.

**HYPOTHESIS / analytic proof candidates.** This report was developed by an
AI collaborator and has not received external mathematical review. The
component endpoints below are inherited **OBSERVED** exact records, except
for the explicitly derived small-gcd window. No new executable evaluation,
speed scan, tuple scan, or phase scan was performed for this report.

Scope: common-start integer speeds, selected reference0, total runners8,
threshold1/8, open blockers and safe equality. The last speed d is larger
than the three residual speeds in the supplied six-constraint core.
All cases discussed are diagnostics or restricted certificate extensions;
no novelty or new Lonely Runner existence theorem is claimed.

## 1. A lap strip has an integer-speed obstruction, not just a width cap

If one open d-blocker centered at m/d contains a closed interval [l,r],
then

`dr-1/8 < m < dl+1/8`.

For l>0 this is equivalently the open speed band

`(m-1/8)/l < d < (m+1/8)/r`.

A connected interval covered by the full d-blocking schedule must lie in
one such occurrence: separate occurrences have positive intervening gaps.
Width gives d<1/[4(r-l)], but that necessary real inequality does not
ensure that the speed bands contain any admissible integer. Their endpoints
couple the same integer lap m to both controlling core endpoints.

This is a specialization of the existing interval/lap representation,
not a claim that generic interval intersection is a new method.

### General two-window protection lemma

Let I=[l1,r1] and K=[l2,r2] be positive closed core-safe intervals with
r1<=l2. Put

`D=r2-l1`, `G=l2-r1`, `w=max(r1-l1,r2-l2)`.

Allow any real d>0 and any final-runner phase alpha. These are auxiliary
parameters; the physical application retains integer d and alpha=0.
If its open blockers cover I union K, each interval belongs to one lap.
If the labels coincide, the whole hull lies in that lap and

`d*D<1/4`.

If the labels differ, ordering gives m_K-m_I>=1. Subtracting the endpoint
inequalities gives

`d*G>(m_K-m_I)-1/4>=3/4`.

Thus one of these two strict inequalities is necessary. Consequently
I union K contains a final-runner-safe point for every phase whenever

`1/(4D)<=d<=3/(4G)`.

For G=0 the upper endpoint means infinity: touching windows cannot be
contained in different blocking laps. Independently, the widest interval
protects a point whenever d>=1/(4w). If G<=3w, these two ranges overlap,
and their union gives protection for **every d>=1/(4D)**, at every phase.

There is a useful strict version. If G<3w, then **every d>1/(4D)** leaves
positive final-safe duration within I union K, at every phase. To prove
it, attempt coverage by closed blockers instead. Same-lap coverage now
requires dD<=1/4, while different-lap coverage requires dG>=3/4.
Closed containment of the widest interval also requires dw<=1/4.
If d>1/(4w), that individual interval cannot be closed-covered. If
d<=1/(4w), then dG<=G/(4w)<3/4 and dD>1/4 exclude both lap alternatives.
In either case the closed cover fails. Its complement is relatively open
in at least one positive interval, hence contains positive duration.
The original core constraints are safe throughout that interval, so the
full configuration has positive safe duration there.

Equality at d=1/(4D) is deliberately not promoted to positive duration:
one closed blocker can exactly span the hull and leave only its two outer
endpoints safe within this pair. Likewise G=3w gives weak protection but
does not supply the strict overlap of ranges used in the positive proof.

The sufficient G<=3w relation describes the placement of two supplied
openings. It does not assert that every six-core safe set has such a pair.
It is a concise application of the existing all-phase interval geometry,
with an explicit same-lap/different-lap obstruction and speed ray.

## 2. The tight/strict diagnostic has one exceptional interval-covering speed

For C={1,4,5,6,7,11}, the inherited complete safe set consists of

- I=[17/56,5/16] and its reflection;
- K=[41/88,15/32] and its reflection;
- isolated points1/8,3/8,5/8,7/8.

The width of I is1/112. Thus full containment of I requires d<28.
For an integer d>11 the possible laps are m=4,5,6,7,8, and their speed
bands are

| m | Open speed band | Integer d>11 in the band |
| ---: | --- | --- |
| 4 | (217/17,66/5) | 13 |
| 5 | (273/17,82/5) | none |
| 6 | (329/17,98/5) | none |
| 7 | (385/17,114/5) | none |
| 8 | (441/17,26) | none |

The excluded endpoint26 is consequential: equality is safe. These five
lap bands follow directly from ((56m-7)/17,(16m+2)/5), and do not require
testing each integer speed separately.

At d=13, I has phase interval [4-3/56,4+1/16] and K has phase interval
[6+5/88,6+3/32]. Both lie strictly within a single blocker. Their
reflections are also blocked. The four isolated points survive; their
distances from13Z-time collisions are respectively3/8,1/8,1/8,3/8.
Thus this same core exhibits complete blocking of its positive components
without complete blocking of its closed safe set.

There is an even shorter simultaneous-obligation contradiction. Covering
the isolated1/8 forces8|d. The width cap and d>11 then leave only16 and24.
But their distances at17/56 are1/7 and2/7, respectively, so both fail.
This is an endpoint congruence coupled to a core-dependent opening.

This entire variable-speed family was already covered in
`ADAPTIVE_REFLECTED_PAIR_2026_09_28.md`, even with the stronger auxiliary
quantifier over runner11's phase. The present calculation explains its
integer lap obstruction and the tight13/strict16 contrast; it adds no
family existence coverage.

## 3. The smallest inherited widest window excludes every admissible integer

For C={1,4,5,3,7,24}, take the inherited component

`I=[25/56,29/64]`, width3/448.

Its width cap permits integer25<=d<=37. A covering lap must satisfy

`(56m-7)/25 < d < (64m+8)/29`.

The strict lap inequalities and25<=d<=37 force12<=m<=16. Exact band
placement gives:

| m | Open band | Reason it has no admissible integer |
| ---: | --- | --- |
| 12 | (665/25,776/29) | lies strictly inside(26,27) |
| 13 | (721/25,840/29) | lies strictly inside(28,29) |
| 14 | (777/25,904/29) | lies strictly inside(31,32) |
| 15 | (833/25,968/29) | lies strictly inside(33,34) |
| 16 | (889/25,1032/29) | lies strictly inside(35,36) |

Consequently this single interval cannot be completely blocked by any
integer d>24. The scalar width test only certified d>=38; the lap strip
integrality eliminates the entire remaining speed range without a full
eight-runner reconstruction. This is a certificate for this supplied
core, not an assertion that every positive core component has this property.

### A stronger two-opening contradiction

The inherited next component K=[89/192,15/32] sharpens this example.
The gap from I to K is1/96, and the span of their joint hull is5/224.
If both intervals are strictly covered by a single d-schedule, their
occurrence labels m_I,m_K must satisfy exactly one of these alternatives:

- Same label: the hull lies in one blocker, requiring d<56/5.
- Different labels: m_K-m_I>=1, and the gap between the two contained
  intervals is strictly greater than3/(4d), requiring d>72.

The second inequality follows by subtracting the two strict endpoint
conditions: d*(l_K-r_I)>(m_K-m_I)-1/4>=3/4.
Therefore simultaneous containment is impossible for56/5<=d<=72.
For d>=112/3, the width of I already prevents its containment. These
ranges overlap, so in fact every real d>=56/5 succeeds on this supplied
core safe set, even with an arbitrary phase for the final runner.
Here G=1/96<3w=9/448, so the general strict version also guarantees
**positive safe duration for every real d>56/5**, at every final phase.

Only the common-start integer d>24 specialization is physical here.
The real-speed/phase conclusion is explicitly auxiliary. It concerns
witness existence in the supplied core period[0,1], not periodicity of
a noninteger d schedule. This is a concrete application of linked lap
labels and the already studied two-time/all-phase geometry, not a new
general phase-robustness theorem. It is stronger than the integer band
calculation, which remains a useful transparent arithmetic diagnostic.

## 4. The small-gcd control is already excluded by a larger core window

For C={1,4,5,56,64,72}, consider

`I=[67/192,159/448]`, width1/168.

It lies inside J=[9/32,3/8], so speeds1,4,5 are safe. The other lifted
phase ranges are

| Speed | Phase range on I |
| ---: | --- |
| 56 | [19+13/24,19+7/8] |
| 64 | [22+1/3,22+5/7] |
| 72 | [25+1/8,25+31/56] |

These intervals are safe, including both equality endpoints. A blocker
for any d>=42 has width at most1/168 and cannot contain I strictly.
Every admissible d>72 therefore succeeds, in particular the existing
112 and113 controls. This core is not an unresolved test of simultaneous
containment. Its old gcd/ratio distinctions remain useful for comparing
other summaries and local windows, not for claiming a new existence gap.

## 5. The inherited 27-core table has no unresolved final integer speed

This is a hand consequence of the archived table and the preceding
certificates, not an exhaustive check of the much larger finite reduction.
For every archived row except four, the published sufficient cutoff
ceil(1/(4w)) is at most c+1. Therefore its existing widest-window bound
already handles every integer d>c. The four exceptions are

`(3,6,7), (3,7,24), (6,7,8), (6,7,11)`.

Sections2-3 handle the second and fourth. The other two both have the
archived window W*=[25/56,15/32], width5/224, so d>=12 succeeds.
For (3,6,7), the remaining d=9,10,11 are safe at1/8; d=8 is safe on W*.
For (6,7,8), the remaining cases have these supplied safe intervals:

| d | Closed interval safe for all seven constraints |
| ---: | --- |
| 9 | [11/24,15/32] |
| 10 | [25/56,15/32] |
| 11 | [17/56,5/16] |

The first interval was already an explicit six-core certificate for
(6,7,9), and speed8 has phases[3+2/3,3+3/4] on it. On W*, speed10 has
phases[4+13/28,4+11/16], while speed8 is already part of the core.
The final interval was already safe for1,4,5,6,7,11; speed8 has phases
[2+3/7,2+1/2] on it. These verify the additional constraint directly.

This closes the final-speed question for these27 inherited six-core
templates, with no new tuple domain and no speed sweep. It does not
close every six-core template in the global finite region. Many of these
templates and their completions belong to already covered families.

## 6. An exact general relation to retain

Suppose selected core-safe points t_i satisfy an integer relation

`sum_i h_i*t_i=q`, with h_i,q integers.

If integer speed d strictly blocks every t_i, let m_i be its unique
blocking lap there and e_i=d*t_i-m_i, so |e_i|<1/8. Then

`d*q-sum_i h_i*m_i=sum_i h_i*e_i`.

The left side is an integer. If sum_i|h_i|<=8, strictness forces it to
vanish. Thus the lap labels must obey exactly the same short integer
relation as the points, scaled by d. In particular, two core-safe points
separated by a reduced p/q with q<=4 force q|d under simultaneous
blocking: their phase difference has distance<1/4, whereas a nonzero
q-residue has distance>=1/q>=1/4.

For coverage by **closed** blockers, |e_i|<=1/8. A relation with
sum_i|h_i|<8 still forces the integer error to vanish. At exactly8 the
error can instead be+1 or-1, but only if every participating point is
an aligned boundary contact: for one common sign sigma in{+1,-1},

`e_i=sigma*sign(h_i)/8` for every h_i!=0.

This follows from equality in both the triangle inequality and the sum
of the individual1/8 bounds. Such nonzero weak-boundary errors therefore
identify threshold-equality witnesses at every participating core-safe
point; they cannot be silently included in a strict blocking argument.
This relation uses common start. With phase theta, the left side acquires
theta*sum_i h_i; arbitrary phase cancels automatically only when
sum_i h_i=0. No unqualified phase extension is asserted.

These constraints are necessary, not sufficient, and do not guarantee
that a useful short relation exists in every six-core safe set. Fixed
rational point menus remain incomplete by the existing finite-anchor
obstruction. The useful next target would be a core-dependent short
relation combined with incompatible interval endpoint inequalities, not
another universally fixed anchor menu.
