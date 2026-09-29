# Core windows bound three residual speeds

September 29, 2026. Research parent: `db2867ed65c4df3668f5275878f21ba400faff2b`.

**HYPOTHESIS / proof candidates.** Six AI collaborators and the coordinator
derived and challenged the arguments below. Exact finite results have status
**OBSERVED**. Internal agreement is not an external proof certificate; external
mathematical review and literature/novelty assessment remain pending. Material
AI involvement covers the reasoning, code, checking, and writing.

## 1. Result and scope

Take eight common-start runners, select reference 0, and fix the distinct
positive integer speeds

`{1,4,5,a,b,c,d}, a<b<c<d, a,b,c,d outside {1,4,5}`.

Safety means distance at least 1/8; threshold equality is safe and all blocking
intervals are open. The proposed sufficient conditions now imply that any
configuration not certified by these arguments satisfies

**`a<=34, b<=47, c<=1565`.**

The last residual d remains unbounded. These are bounds on the cases left by
our sufficient certificates in this fixed-core, selected-reference family.
They do not settle every configuration in the displayed range, all references,
other fixed cores, or the full Lonely Runner Conjecture.

The central additional statement is that the five-constraint core
`{1,4,5,a,b}` always has safe measure at least **1/24**. This forces a
positive closed safe window before the last two residuals are added. The
proof uses how each blocking schedule intersects the complete fixed-core
safe set, rather than its global blocking fraction alone.

## 2. Inherited window guarantee and shorter residual chains

The [short-kernel candidate](SHORT_KERNEL_BOUND_2026_09_28.md) supplies a
common-safe point for four arbitrary-phase quarter-duty trains inside every
closed interval of length

`H=1/a+(3/4)(1/b+1/c+1/d)`.

For the core `{1,4,5}`, the closed window `J=[9/32,3/8]` has width 3/32.
Thus `a>=35` already suffices, since `H<=13/(4a)<=3/32`.

Two and three remaining trains have the respective span budgets

`T2=1/(4c)+1/(2d)`,
`T3=1/(4b)+1/(2c)+1/d`.

For clarity, their elementary proof does not require numerical experiments.
Order periods `P>=q>=r`. In a strict increasing-right-endpoint chain, each
transition into a period-p blocker advances by less than p/4. Consecutive
occurrences of the same label cannot overlap. A q label in a two-label chain
cannot repeat: the intervening r occurrence and return advance by less than
`(q+r)/4<q`. Hence the counts are at most one q and two r. A P label in a
three-label chain cannot repeat, since the intervening two-label piece and
return advance by less than `(P+q+2r)/4<=P`. The counts are at most one P,
two q, and four r.

The open connected chain spans strictly less than T2 or T3. A cover of a
closed interval of that width would yield a finite strict chain extending
beyond both ends, a contradiction. Positive periods give local finiteness.
This justifies the non-strict window-width tests, including isolated equality
witnesses. The remaining trains may have arbitrary phases in these auxiliary
chain lemmas; the fixed-core arithmetic below uses common-start integers.

## 3. Absorb a: b>=48 suffices

For a periodic train with open blocked width B and safe-gap width S, any
closed interval of length L>B contains a closed safe subinterval of width
at least `min(S,(L-B)/2)`. If it contains a full safe gap, use that gap.
Otherwise it meets at most one blocked occurrence, leaving at most two safe
pieces and at least L-B total safe length.

For a>=3, applying this to runner a on J gives

`w_a >= min(3/(4a),3/64-1/(8a))`.

Suppose b>=48. Distinctness gives c>=49 and d>=50, hence

`T3<=1/192+1/98+1/50=8329/235200<25/704`.

Three analytic cases finish:

- If a>=22, the original test already works:
  `H<=1/22+9/192=65/704<3/32`.
- If 11<=a<=21, the clipping bound gives
  `w_a>=min(1/28,25/704)=25/704`.
- For the seven smaller admissible a, the following explicit four-core
  windows all have width at least 7/160, which exceeds 25/704.

| a | Closed four-core window | Width |
| ---: | --- | --- |
| 2 | [9/32,3/8] | 3/32 |
| 3 | [1/8,7/40] | 1/20 |
| 6 | [17/40,15/32] | 7/160 |
| 7 | [17/56,3/8] | 1/14 |
| 8 | [9/32,23/64] | 5/64 |
| 9 | [1/8,7/40] | 1/20 |
| 10 | [5/16,3/8] | 1/16 |

Each listed interval lies in one closed safe lap of a and in the core-safe
set. See the full [peeling derivation](../reviews/2026-09-29-core-windows/peeling.md)
for the lap ranges.

The analytically specified tuple `(a,b,c,d)=(21,47,48,49)` shows that 48
is optimal for combining these two particular sufficient tests:
`H-3/32=335/442176>0`, while every a-safe window is at most 1/28 wide
and `T3-1/28=95/221088>0`. This is a method limitation, not failed
loneliness. No full-configuration oracle or tuple search was run on it.

## 4. Absorb b: the core retains at least 1/24 of a period

Let S be the complete safe set for `{1,4,5}`. It consists of the following
three first-half intervals and their reflections about 1/2:

`A=[1/8,7/40], B=[9/32,3/8], C=[17/40,15/32]`.

Their widths are 1/20, 3/32, and 7/160, so `measure(S)=3/8`.
Define the placed blocking mass

`Q(v)=measure(S intersect {t: ||vt||<1/8})`.

A periodic primitive of the speed-v blocker indicator minus 1/4 has range
3/(16v): it rises at slope 3/4 over one blocker of width 1/(4v), then
falls at slope -1/4. On any interval I, the blocked mass is therefore at
most `width(I)/4+3/(16v)`. Summing over the six intervals gives

`Q(v)<=3/32+9/(8v)`.

For v>=16 this is at most `21/128<1/6`. The remaining admissible
integers have these exact intersections:

| v | Q(v) | v | Q(v) |
| ---: | --- | ---: | --- |
| 2 | 1/16 | 9 | 1/9 |
| 3 | 1/6 | 10 | 1/20 |
| 6 | 17/120 | 11 | 93/880 |
| 7 | 89/560 | 12 | 1/12 |
| 8 | 1/16 | 13 | 23/208 |
| 14 | 69/560 | 15 | 7/80 |

The [scope derivation](../reviews/2026-09-29-core-windows/scope.md)
displays all three scaled interval intersections for each row. These twelve
values were derived by hand and then checked using the measures from both
already-declared exact 31-core reconstructions. No additional speed domain
was evaluated. Thus the proposed universal inequality is

**`Q(v)<=1/6 for every positive integer v outside {1,4,5}`.**

Deleting the two residual blocked sets from S now yields

**`measure(safe{1,4,5,a,b}) >=3/8-Q(a)-Q(b)>=1/24`.**

No independence assumption is used. The overlap of the two added blockers
can only improve this lower bound. Likewise the four-core safe measure is
at least 5/24.

The five-core safe set has at most `K=a+b+6` positive components: start
with the six components of S, and each added speed v introduces at most v
splits. This is deliberately conservative. Isolated safe points have zero
measure and do not affect the argument. Some closed safe component therefore
has width at least

`w5>=1/(24K)`.

## 5. The third-speed cutoff

The last two residuals cannot cover that closed window if

`1/(4c)+1/(2d)<=1/(24K)`.

Since d>c, a sufficient condition is **`c>=18K=18(a+b+6)`**.
The cases not already certified have a<=34 and b<=47, so K<=87. Therefore
c>=1566 suffices and the remaining cases have c<=1565.

The constants are not optimized. Supplementary reviews record ways to
tighten the component count and exploit distinctness; the headline uses
the simpler 1/24 and K<=87 estimates. No pairs or triples of residual
speeds were enumerated to obtain the cutoff.

## 6. Additional arithmetic certificate

The [arithmetic review](../reviews/2026-09-29-core-windows/arithmetic.md)
gives a separate proof candidate. The full core-safe set S meets every
translate of the g-point uniform grid exactly when the integer g>=7.
For g>=11, J alone is long enough. The cases 7,8,9,10 follow respectively
from a union count, a parity class safe for speed 4, a forced shared blocked
point, and a parity class safe for speed 5. Explicit avoiding cosets for
g<=6 show the limit of this translated-grid statement.

If `g=gcd(a,b,c,d)>=7`, residual safety has period 1/g. Its measure
on one such period is at least 3/(4d): total blocked multiplicity has mean
one, while the common collision at the period endpoints gives excess
multiplicity at least three over total length 1/(4d). Integrating over the
g translates and using the grid-hitting property yields full safe measure
at least **3/(4d)>0**. This deduction does not use the 23-move candidate.

The anchors 1/6,1/7,1/8 additionally show that a case not certified by
these elementary checks must have residual multiples of each of 6,7,8,
possibly the same residual for more than one requirement, and gcd<=6.
These are further restrictions on unresolved certificate cases, not a
classification of counterexamples.

## 7. Exact verification and provenance

The frozen [protocol](../reviews/2026-09-29-core-windows/PRIMARY_PROTOCOL.md)
covers precisely the 31 values `a=2,3,6,...,34`, with all four-core safe
components over [0,1]. Its SHA-256 is
`d5ff2d4e06c1d8c7629c6c115fb9faa23a0a1510791cb9b983903277726e65d0`.
Approval was recorded separately before execution; the protocol is unchanged.

The primary algorithm intersects closed safe bands using exact fractions.
A separately structured implementation partitions at every threshold,
evaluates modular predicates at endpoints and open-cell midpoints, and
reconstructs connected components. It completed its independent output
before reading the primary code or output. Both preserve singleton components.

The two implementations agree on 1932 numerical fields across all 31 cores.
The records contain 348 positive components and 20 isolated points.
The independent evaluation checks 1814 endpoints and 1783 open cells.
The widest-component table has minimum width 3/136 at a=34; its deliberately
coarse standalone b cutoff reaches 80. The stronger analytic cutoff 48
combines information from the inherited H test and the clipping argument;
it is not a retuned version of the table's frozen cutoff rule.

See [PRIMARY_TABLE.md](../reviews/2026-09-29-core-windows/PRIMARY_TABLE.md),
the comparison report and source/output hashes in
[MANIFEST.json](../reviews/2026-09-29-core-windows/MANIFEST.json), and the
[adversarial review](../reviews/2026-09-29-core-windows/challenge.md).
The bounded exact records are OBSERVED; general implications remain proof
candidates. No all-reference search, phase scan, broad tuple scan, paid
compute, outreach, or main-branch merge occurred. Hourly research stays paused.

Reproduce from the repository root:

```bash
python reviews/2026-09-29-core-windows/primary_core_windows.py
python reviews/2026-09-29-core-windows/independent_core_windows.py --protocol-hash d5ff2d4e06c1d8c7629c6c115fb9faa23a0a1510791cb9b983903277726e65d0
python reviews/2026-09-29-core-windows/compare_independent.py
```

## 8. What relational information was added, and what remains

Q(v) is not merely a runner's quarter-period blocked fraction. It measures
that schedule relative to the exact openings left by three other runners.
The safe-window argument then converts collective surviving measure into
contiguous space that the remaining blocking chains cannot fill. The gcd
argument uses the complete union of core windows and a shared residual
translation orbit. No claim of a newly discovered invariant is made.

A concrete next target is the six-constraint core `{1,4,5,a,b,c}`.
Writing `Qij=measure(S intersect Bi intersect Bj)` and similarly Qabc,
its safe measure is exactly

`3/8-Q(a)-Q(b)-Q(c)+Qab+Qac+Qbc-Qabc`.

The signed joint terms give a direct target for the user's relational
question. With K=a+b+6, discrepancy already guarantees positive six-core
measure when c>6K, and a further sufficient condition is

`d>=8c(K+c)/(c-6K)`.

The derivation is in the scope review. For c<=6K, this particular estimate
is inconclusive. The next bounded milestone is a direct six-core positivity
argument, or a precisely stated obstruction to that route. Any use of an
existing lower-runner theorem must be separately sourced and credited.
No such theorem is imported here, and there is no claim that this
framework's unresolved step is a new open problem in the literature.

Positive measure must not be imposed on the final seven constraints:
the archived tight example has only equality witnesses. The strict16
truncation obstruction and the small-gcd 56/113 record remain unchanged.
The latter was already certified by the inherited width bound; this work
does not rebrand it as new coverage.
