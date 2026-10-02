# A positive six-core window and a finite final-speed reduction

September 29, 2026. Research parent:
`da05361310a6e0d5607fdd7565ad226f637c8305`.

**HYPOTHESIS / proof candidates, internally reviewed.** The complete direct
argument below was developed with material AI assistance. General implications
await external mathematical review and novelty assessment. The frozen exact
records are **OBSERVED**. Established literature inputs are separately credited
in Section 7; none is silently used in the direct proof.

## 1. What this step closes

For every common-start six-constraint core with distinct positive integer speeds

`C={1,4,5,a,b,c}, a<b<c, a,b,c outside {1,4,5}`,

the proposed direct argument guarantees **positive safe duration at threshold
1/8**. It uses full safe laps, short blocking chains, and a small arithmetic
remainder. The final full family has eight total runners, reference0, and
speeds `{0,1,4,5,a,b,c,d}`, where d>c and all eight speeds are distinct.
Threshold equality is safe; all physical blocking intervals are open.

This closes the six-core positivity question within our framework. It does
not require positive duration after d is added: the final safe set can consist
of isolated equality witnesses.

The existence conclusion already follows from the established seven-runner
theorem. The direct route supplies an explicit fixed-core argument using
our window and arithmetic certificates, without importing that theorem.

A positive component has an explicit arithmetic width bound. With
`M=max(5,b)`, the direct route guarantees success whenever **d>=2Mc**.
Combined with the earlier sufficient tests, our remaining certificate cases
therefore lie in the finite region

**`a<=34, b<=47, c<=1565, d<=147109`.**

Separately, using credited six- and seven-total-runner results sharpens the
remaining region to

**`a<=34, b<=47, c<=281, d<=1268`.**

Neither region has been exhaustively checked. This is a finite reduction in a
fixed-core selected-reference family, not a full-conjecture proof or a new
eight-runner existence result. The repository already records a literature
proof of the eight-runner case whose computational component we have not
reproduced; our target is an explicit structural argument and the information
it exposes.

## 2. Strict safety from a supplied four-core window

Let W be a positive closed safe component for `{1,4,5,a}`, of width w.
The sufficient condition

`T2(b,c)=1/(4b)+1/(2c)<w`                                      (1)

forces positive six-core duration.

To retain strictness, temporarily cover using **closed** b and c blockers.
Their complement is strict safety. Put P=1/b and q=1/c, so q<P. An
increasing-right-endpoint chain of overlapping or touching blockers has at
most one P occurrence and two q occurrences. Indeed, consecutive equal
labels cannot meet, and a first P return would contain a P,q,P subchain
whose endpoint advance is at most `(P+q)/4<P`, impossible for two
occurrences separated by a period P. The chain span is at most P/4+q/2.

A finite closed cover of W would contain a connected chain spanning W.
Condition (1) excludes such a cover. The complement of these locally finite
closed blockers contains a nonempty relatively open part of W and therefore
a positive interval in its interior. All four original core constraints
are strictly safe inside their positive component. This proves the claim.

Equivalently, trim W slightly and increase the residual safety threshold
slightly; the strict inequality supplies the needed slack. Merely applying
a non-strict existence test would not justify positive duration.

## 3. An analytic reduction to 36 slow pairs

The inherited core-safe interval `J=[9/32,3/8]` has width3/32.
The clipping lemma supplies an a-safe subinterval of width at least

`min(3/(4a),3/64-1/(8a))`.

For every a>=19 this is a full safe lap of width3/(4a). Since b,c>a,
condition (1) holds. For a=11,13,14,16,17,18 there are also explicit full
safe laps inside the fixed-core safe set:

| a | Closed four-core window | Width |
| ---: | --- | --- |
| 11 | [25/88,31/88] | 3/44 |
| 13 | [33/104,3/8] | 3/52 |
| 14 | [33/112,39/112] | 3/56 |
| 16 | [41/128,47/128] | 3/64 |
| 17 | [1/8,23/136] | 3/68 |
| 18 | [41/144,47/144] | 1/24 |

These explicit intervals agree with the prior independently verified
31-core table. For a=8, its window width5/64 also exceeds
`T2(9,10)=7/90`, so every larger b,c succeeds.

Only the following eight values of a can remain. Monotonicity in b and c
reduces failure of (1) to these 36 pairs:

| a | Supplied w_a | Possible b | Largest possible c |
| ---: | --- | --- | ---: |
| 2 | 3/32 | 3,6,7 | 48 |
| 3 | 1/20 | 6 through14 | 60 |
| 6 | 7/160 | 7 through16 | 62 |
| 7 | 1/14 | 8,9 | 12 |
| 9 | 1/20 | 10 through14 | 20 |
| 10 | 1/16 | 11 | 12 |
| 12 | 1/24 | 13 through17 | 22 |
| 15 | 7/160 | 16 | 17 |

The corresponding windows are recorded in the
[previous note](CORE_WINDOW_REDUCTION_2026_09_29.md) and its exact table.
For each listed pair, the exact restriction is

`b<c<=floor(2b/(4b*w_a-1))`.

All denominators are positive. The maximum bound is
`floor(560/9)=62`, attained in this calculation at a=6,b=7.
This proves that c>=63 already gives positive six-core duration, irrespective
of the larger final speed d. It does not by itself prove final eight-runner
safety for c>=63.

## 4. Arithmetic closes the remainder

The complete [arithmetic proof](../reviews/2026-09-29-six-core/arithmetic.md)
and [structural proof](../reviews/2026-09-29-six-core/structure.md) provide
the following explicit certificates.

**Strict anchors.** If no residual a,b,c is divisible by6, time1/6 is strictly
safe. If none is divisible by7, time1/7 is strictly safe. If no residual
is0 or7 modulo8, use `[1/8,1/8+1/(8c)]`. If none is0 or3 modulo8,
use `[3/8-1/(8c),3/8]`. These closed intervals have strictly safe interiors.
Thus a remaining triple must contain multiples
of6 and7, and must either contain a multiple of8 or contain both residue
classes3 and7 modulo8.

**A three-direction seventh-anchor selector.** Suppose c is the unique
7-divisible residual. Choose j in {1,2,3} with ja and jb both different
from6 modulo7. Each nonzero residue excludes at most one j, and the core
speeds1,4,5 exclude none. Then

`[j/7+1/(8c),j/7+9/(56c)]`                                  (2)

is safe, of width1/(28c). Every other speed starts at a phase k/7 with
1<=k<=5 and moves forward by at most9/56; c moves from1/8 to9/56.
This preserves all six constraints on the same time interval.

Consequently an unresolved pair must have7 dividing a or b. Inspecting
the 36-pair table leaves only nine pairs:
`(2,7),(3,7),(3,14),(6,7),(6,14),(7,8),(7,9),(9,14),(12,14)`.
The divisibility and residue filters, together with the next family
certificate, reduce these to seven explicit triples:

`(3,7,12),(3,7,18),(3,7,24),(3,7,30),`
`(6,14,16),(7,8,12),(12,14,16)`.

**A shared window.** The interval `W*=[25/56,15/32]`, width5/224,
is safe for the core1,4,5 and each speed in {3,6,7,8,10,12}.
It handles (7,8,12) directly. For the families (3,7,c) and (6,7,c),
every c>=12 has blocker width `1/(4c)<5/224`, so it cannot cover
W* and a positive safe interval survives. For (6,7,c) with c=8,9,10,11,
use respectively W*, `[11/24,15/32]`, W*, and `[17/56,5/16]`.
The two c=16 triples are both safe on
`[17/128,15/112]`, width1/896.

Every displayed containment has exact lap ranges in the two supporting
reports. This closes the direct six-core argument by hand. The separate
frozen computation below deliberately retains a larger, simpler domain,
so its result does not depend on this extra pruning.

## 5. A frozen exact check, not a broad triple search

Before any six-core evaluation, the coordinator froze
[PROTOCOL.json](../reviews/2026-09-29-six-core/PROTOCOL.json), SHA-256

`25c818133f6e78054d14e82bf4b0f0c6b63c9dd7d1ca9a12071d83f878b891a2`.

Its domain is determined solely by the 36 pairs, c<=62, failure of (1),
and the strict sixth/seventh/eighth anchor filters. It does not use the
additional seventh-anchor selector or shared-window family pruning.
The formula generates exactly **27 triples**.

One implementation intersects exact closed safe bands. A separately
structured implementation generates the domain independently, evaluates
modular safety at all rational thresholds and open-cell midpoints, and
reconstructs maximal components. It froze its results before reading the
primary code or output.

The two implementations agree across **2495 numerical leaf fields** and
the complete 27-triple domain, with zero disagreements. A separate check
of the inherited widths verifies the36 branches and c<=62 using45 scalar
inequalities; it evaluates no additional six-core tuple.

All27 cores have positive safe duration. The records retain **190 positive
components and50 isolated points**. The smallest widest-component width is
3/448 at (3,7,24); the largest one-additional-runner cutoff
`ceil(1/(4w))` is38. The independent calculation checks2730 endpoints
and2703 open cells. No final d values, phases, or all-reference cases
were evaluated.

See [PRIMARY_TABLE.md](../reviews/2026-09-29-six-core/PRIMARY_TABLE.md),
the comparison record, and source/output hashes in
[MANIFEST.json](../reviews/2026-09-29-six-core/MANIFEST.json).
These exact results support only the frozen domain; the universal
conclusion also requires the analytic reduction above.

Reproduce from the repository root (exact fractions throughout):

```bash
python reviews/2026-09-29-six-core/primary_six_core.py
python reviews/2026-09-29-six-core/independent_six_core.py
python reviews/2026-09-29-six-core/compare_six_core.py
python reviews/2026-09-29-six-core/audit_branch_reduction.py
```

## 6. The direct fourth-speed bound

Let [l,r] be any positive maximal six-core safe component. Its endpoints
are threshold events with denominators8v and8w for core speeds v,w.
Let c be the largest core speed and M=max(5,b) the second largest.
Necessarily c>=6.

If v and w are distinct, their positive separation is an integer multiple
of `1/(8*lcm(v,w))`, so

`r-l>=1/(8Mc)`.

If both endpoints come from the same speed, the separation is at least
1/(4v), since the threshold numerators are odd and distinct; this also
exceeds1/(8Mc). Alternatively, when they bound one maximal safe component
of that speed they delimit its full safe lap. The fixed speed1 keeps the
six-core safe set away from0 and1, so no artificial domain endpoint is
needed.

A d-blocker has open width1/(4d). Therefore d>=2Mc makes its width no
larger than r-l, and it cannot cover that closed component. A connected
interval covered by the union of d-blockers would have to lie in one
blocker, since successive occurrences are separated by positive safe gaps.
Equality can leave only an endpoint, which is valid.

Combining this with the inherited a>=35, b>=48 and c>=1566 sufficient
conditions gives the direct finite region in Section1. The large constant
is conservative. It establishes finiteness in this framework, not a
feasible exhaustive computation or a claim that all remaining cases pass.

## 7. What established results already provide

These inputs are **KNOWN**, with targeted source inspection rather than
independent reproduction of their entire proofs:

- Bohman, Holzman and Kleitman, *Six Lonely Runners* (2001), Theorem2,
  gives five positive frequencies a witness at distance at least1/6.
  [Author-hosted published paper](https://holzman.technion.ac.il/files/2012/09/runners.pdf).
- Barajas and Serra, *The lonely runner with seven runners* (2008),
  establishes distance at least1/7 for six positive integer frequencies.
  [Published paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v15i1r48/pdf).
- Kravitz, *Barely lonely runners and very lonely runners* (2021),
  Proposition6.1, gives the fast-runner time-perturbation principle used
  here. [Published paper](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf).

The seven-runner theorem supplies a six-core time t0 with margin1/56 above
our threshold. Since every core speed is at most c,

`[t0-1/(56c),t0+1/(56c)]`

is 1/8-safe, of width1/(28c). Hence **d>=7c** succeeds, including
equality. This is exactly the indicated specialization of Kravitz's
proposition, not a new perturbation theorem.

The six-runner theorem similarly gives the five-core a closed window of
width1/(12M). A useful elementary quarter-duty refinement is that every
two-train blocked component for speeds c<d has span **<1/(2c)**.
With at most one fast occurrence, its span is less than
`1/(4c)+1/(4d)<1/(2c)`. With two fast occurrences, the intervening
safe gap3/(4d) must lie strictly inside the slow blocker1/(4c), forcing
d>3c. The earlier three-occurrence budget then gives span
`<1/(4c)+1/(2d)<5/(12c)<1/(2c)`.
This is a quarter-duty adaptation of the two-block reasoning in the
six-runner paper's Lemma4. Therefore **c>=6M** suffices.

For a bound on d independent of c, **d>=27M** suffices:
if c<=27M/7, use d>=7c; otherwise

`1/(4c)+1/(2d)<=7/(108M)+2/(108M)=1/(12M)`,

so the five-core window and the two-train budget apply. With b<=47,
M<=47, yielding c<=281 and d<=1268 among still-uncertified cases.

This smaller region uses established lower-runner results as inputs.
Neither its existence conclusion nor the margin principle is presented
as new. The [literature audit](../reviews/2026-09-29-six-core/literature.md)
records versions, conventions, exact sections read, and limitations.
Text extraction misread the non-strict signs in Kravitz's proposition;
the published page image was checked to retain equality correctly.

## 8. Relational information and the next bounded question

The exact singleton masses Q(6),Q(7),Q(11) on the complete core1,4,5 safe
set give

`3/8-Q(6)-Q(7)-Q(11)=-289/9240<0`.

Yet the corresponding six-core contains `[17/56,5/16]`, width1/112.
Thus exact marginal blocked masses restricted to the core still fail to
capture the opening's placement and joint compatibility. The shared W*
and the three-direction selector restore concrete timing relationships.

Total duration and useful contiguous width also differ: among the frozen
cases, (6,7,11) has total safe measure29/1232 and largest width1/112;
(3,7,24) has larger measure53/1680 but smaller largest width3/448.
Both are exact bounded comparisons, not invariant or novelty claims.

The next step is **last-runner coverage of the complete six-core safe
set**. A complete cover requires one d-blocking schedule to contain every
closed component, with compatible integer lap labels on the shared clock.
Derive an explicit arithmetic condition or obstruction for those simultaneous
containments, keeping endpoint-only final witnesses. A finite region is now
available for orientation, but it does not authorize a broad quadruple scan.

The old tight example, the small-gcd56/113 record and strict16 truncation
obstruction remain unchanged. Hourly research stays paused; no outreach,
paid compute, all-reference scan, main merge or parked +7/+9 restart.
