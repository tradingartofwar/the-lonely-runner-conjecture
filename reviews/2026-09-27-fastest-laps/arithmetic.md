# Shared laps distinguish a contact from a surviving interval

September 28, 2026. This arithmetic calculation uses only the common-start
speed lists `{0,1,4,5,6,7,11,13}` and `{0,1,4,5,6,7,11,16}`, reference 0,
n=8, and threshold 1/8, as fixed in `protocol.json`. AI materially contributed
the derivations, code, and checking. The exact finite calculations are
**OBSERVED** and independently reconstruct the residual allowed set. No
novelty, general Lonely Runner existence result, or additional speed case is
claimed.

The useful finite distinction is precise: speed 13 covers every positive
interval left by the six residuals and preserves four isolated contacts.
Speed 16 removes those contacts, but leaves four positive intervals. Each
positive interval for 16 has an endpoint determinant exactly 1. These facts
retain the shared integer laps rather than just individual pattern inventories.

The final section supplies additional continuous-phase arguments requested
after the frozen finite protocol. They use the same speed lists, with only
speed 11's starting phase variable, and remain **HYPOTHESIS / proof
candidates**. No additional numerical phase scan was performed here.

## The six fixed constraints give a small exact certificate

Let A be the complete allowed set for speeds `1,4,5,6,7,11`, still at the
eight-runner threshold 1/8. Intersecting their closed safe laps gives

\[
A=\{1/8,3/8,5/8,7/8\}
\cup[17/56,5/16]\cup[41/88,15/32]
\cup[17/32,47/88]\cup[11/16,39/56].
\]

Its positive duration is `2(1/112+1/352)=29/1232`. The intervals and their
reflections are separate from the four isolated points. `arithmetic.json`
records a single common lap for every runner on every component and checks
that maximum lower bound and minimum upper bound recover its endpoints.

Only two non-reflected intervals need to be displayed to explain the fastest
runner's effect; the archive checks all four directly.

| Part of A | Image under speed 13 | Effect of 13 | Effect of 16 |
| --- | --- | --- | --- |
| [17/56,5/16] | [221/56,65/16] inside (4−1/8,4+1/8) | Entire interval strictly blocked | Leaves [17/56,39/128] |
| [41/88,15/32] | [533/88,195/32] inside (6−1/8,6+1/8) | Entire interval strictly blocked | Whole interval safe |

The strict-cover phase margins for 13 are `(1/14,1/16)` in the first row and
`(2/11,1/32)` in the second, respectively at the lower and upper collision
boundaries. Therefore this is strict coverage of the closed intervals,
including their endpoints. On the central interval, speed 16 has phase
`16t−7` in `[5/11,1/2]`, wholly inside `[1/8,7/8]`. On the outer interval,
its lifted phase runs from `4+6/7` to 5 and first enters strict blocking just
after `t=39/128`.

At `t=q/8` for q=1,3,5,7, speed 13 has phases `(5,7,1,3)/8`, all safe;
speed 16 collides exactly. Hence the complete results are

\[
A\cap S_{13}=\{1/8,3/8,5/8,7/8\},
\]

\[
A\cap S_{16}=[17/56,39/128]\cup[41/88,15/32]
\cup[17/32,47/88]\cup[89/128,39/56],
\]

with total duration `2/896+2/352=39/4928` in the latter case. This finite
decomposition proves the contrast without inference from qualitative lap
ordering or moment totals.

## One lap coordinate determines all six residues

On fastest safe lap m, write `t=(m+u)/V`, where `1/8<=u<=7/8`. For each fixed
residual speed v, let

\[
vm=Vq_v(m)+r_v(m),\qquad 0\le r_v(m)<V.
\]

Then

\[
vt=q_v(m)+\frac{r_v(m)+vu}{V},\qquad
r_v(m+1)=(r_v(m)+v)\bmod V.
\]

All six residues use the **same integer m**. Here speed 1 makes that coupling
especially explicit: `r_1(m)=m`, so `r_v(m)=v r_1(m) mod V`. The six residues
cannot be chosen independently. Their pair determinants obey

\[
v_i r_j-v_j r_i
=V(v_j q_i-v_i q_j).
\]

The archive checks all 29 lap vectors, all 435 pair determinants, and every
successor recurrence including the wrap to m=0. For V=13 every individual
residue has period 13. For V=16 the periods in speed order are
`(16,4,16,8,16,16)`. Periods alone do not specify their shared alignment.

The frozen shift of only speed 11 makes the lost relationship explicit.
Its residue becomes `r'_11(m)=11(m+s) mod V`, while `r_1(m)=m` stays fixed.
Their determinant therefore satisfies

\[
r'_{11}(m)-11r_1(m)\equiv11s\pmod V.
\]

Because 11 is coprime to both 13 and 16, every nonzero allowed offset breaks
this common-start pair relation, although it merely permutes speed 11's
individual inventory across laps. Shifting all runners together restores
`r'_1(m)=m+s mod V` and determinant zero. The archive checks this arithmetic
for all 29 prescribed offsets, without duplicating the phase outcome scan.
Breaking this relation does not by itself imply more or less lonely duration;
the exact phase-image arguments below determine the consequence in these
two fixed families.

The nonempty allowed laps illustrate that alignment directly:

| V | Fastest lap m | Surviving normalized u |
| ---: | ---: | --- |
| 13 | 1,4,8,11 respectively | {5/8}, {7/8}, {1/8}, {3/8} |
| 16 | 4 | [6/7,7/8] |
| 16 | 7 | [5/11,1/2] |
| 16 | 8 | [1/2,6/11] |
| 16 | 11 | [1/8,1/7] |

These identities are exact encodings, not alone an existence mechanism. The
substantive positive conclusion comes from checking that the same intervals
also lie in A; residue compatibility without safety would be insufficient.

## Contact congruences and unit gaps

At a lower threshold of speed a and an upper threshold of speed b, a common
time must satisfy

\[
t=\frac{8p+1}{8a}=\frac{8q+7}{8b},\qquad
8(bp-aq)=7a-b.
\]

For positive integer a,b and `g=gcd(a,b)`, this integer equation is solvable
exactly when `8g` divides `7a−b`, equivalently when `(a+b)/g` is divisible
by 8. Integer solutions can be shifted by the common period 1/g into [0,1].
For two equally oriented thresholds, the corresponding criterion is that
`|a−b|/g` is divisible by 8. For lower/lower contacts this follows from
`8(bp−aq)=a−b`; upper/upper has `7(a−b)` on the right, and 7 is coprime to 8.
These general equivalences are supplied elementary proof candidates; the
checker directly verifies their predictions on all 42 pairs in the two fixed
inputs.

For the four contacts in A, speeds 1 and 7 supply opposing thresholds at
1/8 and 7/8, and speeds 5 and 11 supply them at 3/8 and 5/8. Their normalized
sums are 8 and 16. Speed 13 shares speed 5's orientation at 3/8 and 5/8
because `13−5=8`; it also has an opposite contact with speed 11 because
`13+11=24`. At 3/8 the lower controller is 11 and the upper controllers are
5 and 13; at 5/8 the orientations reverse. Opposing safe directions explain
why these are isolated points rather than intervals.

Pair divisibility does **not** guarantee a surviving contact. The very same
1/7 and 5/11 pair contacts exist arithmetically in the V=16 configuration,
where speed 16 blocks all four. This counterpressure uses only the fixed
inputs and preserves the quantifier: the criterion decides existence of a
pair contact, not simultaneous safety of seven constraints.

For an interval whose left controller is speed a at lower lap p and whose
right controller is speed b at upper lap q, the width is

\[
\Delta t=\frac{a(8q+7)-b(8p+1)}{8ab}.
\]

The numerator is an integer. For the two non-reflected V=16 openings,

\[
7\cdot39-16\cdot17=1,
\qquad
11\cdot15-4\cdot41=1.
\]

Their widths are consequently `1/(8·7·16)=1/896` and
`1/(8·11·4)=1/352`; the reflected openings also have numerator 1. Thus these
are the smallest positive endpoint separations for these fixed controlling
speed pairs. The integer gap certifies a positive interval **after** all
other constraints have been checked through A. A positive determinant alone
does not make the interval globally safe.

## Additional continuous-phase arguments

Let `D_V(theta)` be the total allowed duration after shifting only speed 11
by starting phase theta modulo one. The unchanged runners retain common
start. The protocol's shifts correspond to `theta=11s/V mod 1`; the statements
below address all phases analytically, without another phase scan. This is a
shifted-start comparison, not a change to the common-start conjecture.

### V=13: a nonzero phase necessarily opens a gap

The unchanged speeds `{1,4,5,6,7,13}` are safe throughout
`J13=[17/48,3/8]` and its reflection `[5/8,31/48]`, each of width 1/48.
Common-lap endpoint inequalities for both intervals are in the archive.

Their speed 11 images, after subtracting the nearby integers, are

\[
11J13-4=[-5/48,1/8],\qquad
11(1-J13)-7=[-1/8,5/48].
\]

Their union is exactly `[-1/8,1/8]`, a circular arc of length 1/4. At theta=0
the strict blocking arc has the same interior, so only the two outer phase
endpoints survive on these two time intervals. They give t=3/8 and t=5/8.

For a shift theta, put `d=||theta||=min(theta,1−theta)` in [0,1/2]. Two arcs
of length 1/4 with center separation d overlap in length `1/4−d` when
`d<=1/4`, and have zero overlap when `d>=1/4`. Thus the fixed phase union
has uncovered length `min(d,1/4)`. Each uncovered phase has at least one
preimage in the two unchanged-safe time intervals, with scale factor 1/11.
This gives the candidate

\[
D_{13}(\theta)\ge\frac{\min\{\|\theta\|,1/4\}}{11}>0
\quad(\theta\not\equiv0\pmod1).
\]

There is also a direct interval check behind positivity. For `0<theta<=1/2`,
the interval ending at 3/8 of width `min(1/48,theta/11)` is safe, since speed
11's phase is `1/8+theta−11(3/8−t)`. For `1/2<=theta<1`, the interval beginning
at 5/8 of width `min(1/48,(1−theta)/11)` is safe, since its phase is
`theta−1/8+11(t−5/8)`. This gives a weaker bound and checks the one-sided
contact geometry directly. The phase-union bound has the stronger plateau
1/44 instead of 1/48.

The already reconstructed theta=0 case has zero duration and four contacts.
Thus zero is the unique tight starting phase modulo one in this restricted
one-runner phase family, if the supplied argument is accepted. Every nonzero
protocol offset has `min(theta,1−theta)>=1/13`, giving the sufficient lower
bound 1/143. This is a consequence of the argument, not a sampled phase
minimum or an asserted sharp bound.

### V=16: positive duration survives every phase

The unchanged speeds `{1,4,5,6,7,16}` are safe throughout
`J=[25/56,15/32]` and `1−J=[17/32,31/56]`. Each interval is checked by common
laps in the archive. Under speed 11, subtracting the nearby integer gives
the phase images

\[
11J-5=[-5/56,5/32],\qquad
11(1-J)-6=[-5/32,5/56].
\]

They overlap, and their union is `[-5/32,5/32]`, of circular length 5/16.
For any starting phase, speed 11 blocks an open circular arc of length 1/4.
At least `5/16−1/4=1/16` of that phase union remains safe. Each phase in the
union has at least one preimage in the two time intervals, with scale factor
1/11; overlapping phase images can only add time. Hence the supplied argument
gives

\[
D_{16}(\theta)\ge1/176>0\qquad\text{for every starting phase }\theta.
\]

The bound is sharp for the restricted union `J union (1−J)`: at theta=0 its
survivors are exactly `[41/88,15/32]` and its reflection, with total 1/176.
It is not asserted sharp for the full time interval; the original full
schedule has duration 39/4928.

These two supplied arguments use the same comparison. For 13 the unchanged
safe intervals span exactly one blocking arc's width, and coverage requires
exact phase alignment. For 16 their phase union is wider than a blocking arc,
so every alignment leaves positive duration. They do not extrapolate to other velocities or arbitrary runner
configurations. The code verifies all rational constants and interval
inclusions; the universal phase implications remain the written proof
candidates, not a claim of formal machine verification.

## Reproduction

`arithmetic_check.py` uses only the Python standard library and imports no
project code. It reads the frozen protocol, independently intersects closed
safe laps, preserves isolated points, verifies shared residue recurrence and
determinants, checks pair contact criteria by direct enumeration, and records
direct witnesses and exact fastest-cover margins. `arithmetic.json` pins both
the protocol and checker hashes. The continuous-phase section records exact
constants separately from the finite results.

```bash
python -B reviews/2026-09-27-fastest-laps/arithmetic_check.py --check
```

Finite totals: two cases, 29 shared lap records, 435 pair determinant checks,
42 pair contact checks, eight residual components, and eight final components
(four points for 13 and four intervals for 16). No claim that these checks are
independent samples, a literature review, or an unbounded existence proof is
made.
