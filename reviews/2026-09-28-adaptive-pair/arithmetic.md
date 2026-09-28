# Independent arithmetic review of the adaptive reflected pair

September 28, 2026. Frozen scope: `protocol.json`, family
`{0,1,4,5,6,7,11,V}`, positive integer V outside `{1,4,5,6,7,11}`, selected
reference 0, n=8, threshold h=1/8. Only runner 11 may have an arbitrary
starting phase theta; all other runners retain phase zero. AI materially
performed the derivation and exact checks. The general implications remain
**HYPOTHESIS / proof candidates**; no novelty or global optimality is claimed.

**Review outcome:** no contradiction was found. The three candidate phase
separations are correct, including the third-branch minimum 61/224. The
unchanged minimum is exactly 1/8 in every branch, so the best minimum distance
achievable by the two prescribed times is identically 1/8 for every phase.
For both branches with 8 dividing V, the extra selected-runner margin and the
direction of the unchanged equality constraint give a strict one-sided
interval of length `1/(56V)` for every theta. These are different conclusions:
the two original points stay at equality, while neighboring times are strict.

The starting rule is already recorded in `notes/VARIABLE_SPEED_FAMILY.md`.
This review checks its reflected-pair consequence, using the circle argument
in `notes/TWO_TIME_CERTIFICATES_2026_09_27.md`. No new time-template search or
full allowed-set reconstruction was used.

## Shared notation and the exact pair envelope

Write `a=17/56`, `b=5/16`, and let t be the selected time. At the reflected
time `1−t`, every integer unchanged speed has the same circular distance as
at t. Let c be that common minimum and put `p={11t}`. The selected phases
are p and `1−p`. Thus the exact best-of-pair minimum is

\[
F_V(\theta)=\min\left(c,
 \max\{\|p+\theta\|,\|\theta-p\|\}\right).
\]

All branches below have `1/4<p<1/2`. Put `u=||theta||` in [0,1/2]. Direct
comparison of the two triangular distance functions gives

\[
\max\{\|p+\theta\|,\|\theta-p\|\}
=\begin{cases}
p+u,&0\le u\le1/2-p,\\
1-p-u,&1/2-p\le u\le1/2.
\end{cases}
\]

Its minimum is `1/2−p=d/2`, attained at theta=1/2, where
`d=||22t||=1−2p` is the pair's circular separation. Its maximum is 1/2.
This is an exact piecewise expression, not a phase-grid estimate. Since
every branch has c=1/8 and d/2>=1/8,

\[
\boxed{F_V(\theta)=1/8\quad\text{for every }\theta.}
\]

The cap is supplied by an unchanged runner at both times, so it is also an
upper bound on this pair's performance. It says nothing about the best
distance available at other times.

## Branch 1: 8 does not divide V

Take t=1/8. In speed order `(1,4,5,6,7)`, the unchanged phases and distances
are

\[
(1,4,5,6,7)/8,\qquad(1,4,3,2,1)/8.
\]

Writing `r=V mod8`, the remaining unchanged phase is r/8, with
`r in {1,...,7}`. Its distance is at least 1/8. Therefore c=1/8 exactly.
The selected phase is p=3/8, giving d=1/4 and d/2=1/8.

At t, speed 1 is a lower equality controller and speed 7 an upper equality
controller. V additionally joins the lower set when r=1 and the upper set
when r=7. At `1−t`, these orientations reverse. Hence whenever runner 11
allows one of these times, it is isolated: immediately to one side speed 1
fails, and immediately to the other speed 7 fails. A favorable phase of
runner 11 does not create a strict neighborhood around these particular times.
This preserves the V=13 common-start contact-only control without claiming
that other configurations or phases lack strict times elsewhere.

The finite reduction is exactly the seven nonzero residues modulo 8. The
excluded small values of V only remove inadmissible members; they do not
change the argument for any remaining integer.

## Branch 2: V=8m with 7 not dividing m

Take t=a=17/56. The five fixed unchanged phases are

\[
(17/56,\ 3/14,\ 29/56,\ 23/28,\ 1/8),
\]

and their distances are

\[
(17/56,\ 3/14,\ 27/56,\ 5/28,\ 1/8).
\]

For V, `Va=17m/7`, whose fractional part is `j/7` with
`j=3m mod7` in `{1,...,6}`. Its distance is at least 1/7, strictly above
1/8. Consequently c=1/8, with speed 7 the sole unchanged equality controller:
lower at t, upper at `1−t`.

For completeness, the entire residue calculation is

| m mod7 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| j=3m mod7 | 3 | 6 | 2 | 5 | 1 | 4 |
| Distance of V at t | 3/7 | 1/7 | 2/7 | 2/7 | 1/7 | 3/7 |

Runner 11 has p=19/56, so

\[
d=1-2p=9/28,\qquad d/2=9/56=1/8+1/28.
\]

Thus at every phase one pair member has selected-runner excess at least 1/28,
despite the unchanged cap keeping the pair's full value exactly 1/8.

## Branch 3: V=56m, m>=1

Put `epsilon=1/(8V)` and take `t=a+epsilon`. The integer quantifier gives
`0<epsilon<=1/448`, so t lies strictly inside `[a,b]`. The fixed unchanged
phases have the same laps as in branch 2 and are

\[
17/56+\epsilon,\quad3/14+4\epsilon,\quad29/56+5\epsilon,
\quad23/28+6\epsilon,\quad1/8+7\epsilon.
\]

They are all strictly inside `[1/8,7/8]`. Their exact distance excesses above
1/8 are respectively

\[
5/28+\epsilon,\quad5/56+4\epsilon,\quad5/14-5\epsilon,
\quad3/56-6\epsilon,\quad7\epsilon.
\]

Every expression is positive on the specified epsilon range. Meanwhile
`Vt=17m+1/8`, so V alone is an unchanged equality controller, lower at t
and upper at `1−t`. Again c=1/8 exactly.

The selected phase is

\[
p=19/56+11/(8V),\qquad
19/56<p\le163/448<1/2.
\]

It follows that

\[
d=1-2p=9/28-11/(4V).
\]

This increases with V on the allowed range V>=56. Its minimum is

\[
d(56)=61/224=1/4+5/224>1/4.
\]

The selected-runner excess supplied by the pair is exactly bounded below by

\[
d/2-1/8=1/28-11/(8V)\ge5/448>0.
\]

No residue scan is needed in this branch: integer m>=1 provides the lower
bound V>=56, and the phase inequalities are affine in epsilon on one common
lap. This includes the prescribed very large diagnostic without enumerating
meetings or intervening speeds.

## Equality directions and a uniform strict interval when 8 divides V

For branches 2 and 3, choose the pair member whose runner-11 distance is at
least d/2. The circle inequality ensures one exists. It is essential to use
this stronger selection test: a member that merely passes 1/8 can have an
opposing runner-11 equality and be isolated.

At the first time t the sole unchanged equality controller is lower, so
move forward. At the reflected time the sole unchanged equality controller
is upper, so move backward. Set

\[
R=1/(56V).
\]

In branch 2, the fixed five remain strict inside `[a,a+R]`, since
`R<=1/448<1/112=b−a`. The variable runner's phase is
`j/7+Vs`; for `0<=s<=R` it remains between 1/7 and
`6/7+1/56=7/8`. It is strict in the interior. Runner 11 loses at most 11R
in distance and retains excess at least

\[
1/28-11/(56V)=(2V-11)/(56V)>0\qquad(V\ge8).
\]

In branch 3,

\[
t+R=a+1/(7V)<b,
\]

so the fixed five remain strictly safe throughout this short interval. The
variable runner's phase rises from 1/8 to `1/8+1/56=1/7`, becoming strict
immediately after t. Runner 11 retains excess at least

\[
1/28-11/(8V)-11/(56V)=(V-44)/(28V)>0
\qquad(V\ge56).
\]

Reflection supplies the unchanged-runner inequalities on `[1−t−R,1−t]`.
The selected runner uses the same Lipschitz bound in either time direction,
even though its arbitrary starting phase does not preserve reflection of
the entire configuration. Therefore at every theta at least one of these
two directed intervals is safe with strict interior, giving the sufficient
bound

\[
D_V(\theta)\ge1/(56V)>0\qquad(8\mid V).
\]

This is an interval construction beside an equality witness. It is not a
claim that the original pair has positive margin, nor an optimal-duration
calculation. A stronger branch-3 radius `5/(88V)` also follows from the same
inequalities, but it is unnecessary for the uniform statement and was not
obtained by an optimization or additional search.

## Where runner 11 joins an equality controller

For the selected first phase p in any branch, runner 11 reaches a threshold
at the following phases, all represented in [0,1):

| Time | Lower threshold of 11 | Upper threshold of 11 |
| --- | --- | --- |
| t | 1+1/8−p | 7/8−p |
| 1−t | 1/8+p | p−1/8 |

In branches 2 and 3, the first time becomes an opposing contact when
`theta=7/8−p`; the reflected time does so when `theta=1/8+p`. These phases
are distinct because their difference is `3/4−2p=d−1/4>0`. At either one,
the other time has selected distance `d−1/8>1/8` and supports a strict
neighborhood. Thus isolated pair members at special phases do not defeat
the all-phase strict-interval conclusion. In branch 1 the two displayed
opposing phases coincide at theta=1/2, and the unchanged constraints already
oppose at both times for every phase.

## Bounded checks and remaining limits

Read-only exact substitutions at precisely the eight protocol values
`13,16,32,56,88,112,120,56000000000000` confirm the derived c and d,
the unchanged equality controllers, and the directed endpoint inequalities.
For the nonconstant branch, V=56 gives `t=137/448`, `p=163/448`,
`d=61/224`; V=112 gives `t=39/128`, `p=45/128`, `d=19/64`.
The large value uses the formula directly and no meeting enumeration.
These checks support arithmetic execution; the residue and inequality
arguments above carry the unbounded integer quantifiers.

The earlier fixed-menu failures V=32,88,120 all fall in branch 2 and are
covered by the already specified adaptive time. This is a change from a
fixed finite menu to an existing V-dependent rule, with its reflection;
it does not reinterpret those fixed-menu failures as actual infeasibility.
No statement is made about other references, two independently shifted
runners, arbitrary changing velocity families, or a small-gcd selection rule.
The V=13 contact-only common-start control is retained. General conclusions
remain proof candidates with internal review, and originality is unestablished.
