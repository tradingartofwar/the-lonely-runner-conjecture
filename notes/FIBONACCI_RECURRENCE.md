# Explaining the Fibonacci plateaus

**September 20, 2026.** This continues [the bounded Fibonacci check](FIBONACCI_CHECK.md) using recurrence dynamics, continued fractions, and small interval certificates.

**Outcome:** the observed four-case plateau formula is an established result. Zhuravleva's [2011 paper, Theorem 1](https://arxiv.org/html/1112.6142v1#S3), matches it exactly. Pandey's [2013 paper, Theorem 5](https://cs.uwaterloo.ca/journals/JIS/VOL16/Pandey/pandey7.pdf), supplies the corresponding modular witness. Our earlier unsuccessful source search missed these papers; it was not evidence of novelty. Sources S11–S12 record the correspondence.

We now have exact local certificates through 21 total runners and a written reconstruction of the mechanism. The reconstruction below has not had independent review. Agreement between two computational methods checks the four specified stages, not an unbounded proof. This concerns the selected stationary reference in Fibonacci relative-speed prefixes, not every reference or arbitrary speeds.

Reproduce: `python -m scripts.analyze_fibonacci_recurrence`. [Script](../scripts/analyze_fibonacci_recurrence.py) · [Exact evidence](../experiments/fibonacci_recurrence.json).

## 1. The concrete result

Use `F_0=0,F_1=1` and `L_0=2,L_1=1`, both with the addition recurrence. With `n` total runners, the selected runner is at speed zero and the others have distinct relative speeds `F_2,...,F_n`. Thus `n` is also the largest Fibonacci index; the repeated initial 1 is not a second moving runner.

| Total runners | Largest speeds across the four prefixes | Best gap of the selected runner | All maximizing times in one cycle | Increasing / decreasing controlling speeds at the earlier peak |
| --- | --- | --- | --- | --- |
| 6–9 | 8, 13, 21, 34 | `2/11` | `3/11, 8/11` | 8 / 3 |
| 10–13 | 55, 89, 144, 233 | `5/29` | `8/29, 21/29` | 55 / 3 |
| 14–17 | 377, 610, 987, 1597 | `13/76` | `21/76, 55/76` | 377 / 3 |
| 18–21 | 2584, 4181, 6765, 10946 | `34/199` | `55/199, 144/199` | 2584 / 3 |

All four rows are now computationally certified. The previous experiment stopped at `n=14`. Each displayed gap exceeds the conjecture target `1/n`; these are not threshold-tight examples.

Only a few constraints are needed for each upper bound:

$$C_m=\{1,2,3,5,F_6,F_{10},\ldots,F_{4m-2}\},\qquad m\ge2.$$

For example, eight relative speeds `{1,2,3,5,8,55,377,2584}` give the upper bound for all four prefixes with 18–21 total runners. This subset has its own runner count, but we use its maximum as an upper bound on the original objective; we do not substitute its count into the original `1/n` target.

The script finds each subset maximum with the piecewise-linear method, separately intersects all its closed allowed intervals at that height, and evaluates every speed of the longest full prefix at the proposed peak. An upper bound plus a matching witness certifies the full-prefix maximum. No full-prefix time grid or large enumeration is involved.

## 2. Why a new runner moves the peak

Put

$$B_m=F_{4m-2},\quad c_m=F_{2m-1}F_{2m-2},\quad
t_m=\frac{F_{2m}}{L_{2m+1}},\quad
d_m=\frac{F_{2m-1}}{L_{2m+1}}=1-3t_m.$$

Near the earlier peak, speed 3 approaches its next meeting with the reference, while speed `B_m` has just passed a meeting. Their distances are

$$1-3t\quad\hbox{and}\quad B_mt-c_m.$$

Balancing them gives

$$t=\frac{c_m+1}{B_m+3}=t_m.$$

For the first three stages this reads `11t=3`, `58t=16`, `380t=105`, reducing to `3/11`, `8/29`, `21/76`. The reductions explain why the controlling sum need not equal the displayed denominator.

Also,

$$\frac{c_m}{B_m}=t_{m-1}\quad(m\ge3).$$

So the next critical runner collides with the reference exactly at the preceding best time. Speeds 55, 377, and 2584 destroy the old peaks in succession. The runners between these critical speeds preserve the new peak; the modular calculation below explains why.

**Local balance alone is insufficient.** It must be accompanied by a global upper bound and a witness satisfying every remaining speed. The next two sections supply a draft reconstruction of those arguments.

## 3. A small global upper-bound argument

Define

$$\varphi=\frac{1+\sqrt5}{2},\qquad
\alpha=\frac{1}{2+\varphi}=\frac{5-\sqrt5}{10},\qquad
d_\infty=1-3\alpha=\frac{3\sqrt5-5}{10}.$$

The proposed interval lemma is that, for `d_infinity <= delta <= d_m`, all times satisfying the constraints in `C_m` are exactly

$$J_m(\delta)\ \cup\ (1-J_m(\delta)),\qquad
J_m(\delta)=\left[\frac{c_m+\delta}{B_m},\frac{1-\delta}{3}\right].\tag{1}$$

Here `1-[a,b]=[1-b,1-a]`. Closed endpoints matter. At `delta=d_m`, each interval collapses to one point. A continuous finite minimum could not exceed `d_m` without leaving a nontrivial allowed interval at `d_m`, so (1) supplies the global upper bound and all its maximizing times.

For the base case `C_2={1,2,3,5,8}`, work in `[0,1/2]`. Throughout `d_infinity <= delta <= 2/11`, we have `1/6 < delta <= 2/11`. Speeds 1, 2, and 3 leave

$$[\delta,(1-\delta)/3]\ \cup\ [(1+\delta)/3,(1-\delta)/2].$$

Speed 5 removes the second interval and raises the first lower endpoint to `(1+delta)/5`. Speed 8 removes everything below `(2+delta)/8`. Its preceding safe interval ends too early because `delta>2/13`. This leaves exactly `J_2(delta)`.

For the induction, write `B=B_m`, `b=B_(m-1)`, `c=c_m`, and `e=c_(m-1)`. The meeting `c/B=t_(m-1)` lies inside the previous interval at the lower thresholds under consideration. The current blocking interval reaches strictly to the left of the previous allowed interval because

$$\frac{c-\delta}{B}<\frac{e+\delta}{b}
\quad\Longleftrightarrow\quad
\delta>\frac{bc-Be}{B+b}.$$

With `r=2m-2 >= 4`, recurrence identities give

$$bc-Be=F_{r-1}F_{r+1}=F_r^2+1,\qquad B+b=3F_{2r}=3F_rL_r.$$

The ratio is less than `1/6`: equivalently `2(F_r^2+1)<F_r L_r`, which follows from `L_r-2F_r=F_(r-3)` and `F_r F_(r-3)>=3`. Since `delta>=d_infinity>1/6`, the overlap condition holds.

The new right blocking endpoint becomes `(c+delta)/B`. It lies below `(1-delta)/3` precisely when `delta<=d_m`. No further blocking interval enters the remaining segment: the identities

$$5c_m=L_{4m-3}-1,\qquad
B_m\alpha=c_m+\frac{1+\varphi^{-(4m-2)}}5$$

put `B_m alpha-c_m` strictly between `1/5` and `2/5`, while `1-delta>=9/11`. The next block starts beyond `alpha`, and `(1-delta)/3<=alpha`. This establishes the induction step in the draft argument.

For completeness, the ranges used above follow from

$$\alpha-t_m=\frac{1}{\sqrt5\left(\varphi^{4m+2}-1\right)}>0.$$

Consequently `t_m` increases to `alpha` and `d_m` decreases to `d_infinity`, starting at `d_2=2/11`. The script checks the lemma at its peak and at one rational interior threshold for each of the four stages; those finite checks are not its general proof.

## 4. Why every intervening Fibonacci speed is clear

Here is our direct integer reconstruction of the witness. Set `s=2m+1`, `a=F_(s-1)`, `q=L_s`, so `t_m=a/q`. For `1<=r<=s`, the product identity

$$5aF_r=qL_{r-1}+(-1)^rL_{s-r}\tag{2}$$

follows from the Fibonacci and Lucas recurrences, or their two-root formulas. The Lucas residues modulo 5 repeat `2,1,3,4`. Equation (2) therefore places the phases near fifths of the track, with an explicitly controlled correction.

For odd `r`, the base residue is `2/5` or `3/5` and the correction is negative with magnitude less than `1/5`; the circular distance is greater than `1/5`. For `r=2 mod 4`, the base residue is `1/5` with a positive correction less than `1/5`, again giving distance greater than `1/5`.

The remaining case is `r=0 mod 4`. Its phase is `4/5+L_(s-r)/(5q)` and its distance is

$$\frac{q-L_{s-r}}{5q}\ge\frac{q-L_{s-4}}{5q}
=\frac{F_{s-2}}q=d_m.$$

The inequality uses increasing Lucas numbers at positive odd indices; equality occurs only at `r=4`, the speed 3. Since `d_m<=2/11<1/5`, all other cases are safely above the required height.

To extend beyond `r=s`, use

$$F_{2s}=qF_s,\qquad F_{2s-1}=qa+1,\qquad
F_{2s-r}\equiv(-1)^{r+1}F_r\pmod q.$$

The last congruence follows backward from the first two by the recurrence. Circular distance ignores the sign, so it reflects all indices through `2s-1=4m+1` into those already checked. The reflected equality index is `2s-4=4m-2`, precisely `B_m`. Thus only speeds 3 and `B_m` attain the minimum at this witness. Every prefix with `4m-2<=n<=4m+1` contains the upper-bound subset and has this matching witness.

The next speed is `F_(2s)`, a multiple of `q`, and therefore collides at both old maximizing times. This explains why the plateau ends after four runner counts.

## 5. What the recurrence and continued fractions reveal

The peak times are alternating convergents of

$$\alpha=[0;3,1,1,1,\ldots].$$

Our earlier matrix identities supplied candidates. The allowed-interval and remainder arguments explain their feasibility and optimality for this family.

There is also a particularly concrete picture at the limiting time. Put `psi=(1-sqrt(5))/2`, so `|psi|<1`. For every `r>=2`,

$$F_r\alpha=\frac{L_{r-1}}5+\frac{\psi^r}5.$$

As the **runner index** advances, phases approach the repeating cycle

$$\frac15,\ \frac35,\ \frac45,\ \frac25,\ \frac15,\ldots$$

with an alternating, shrinking error. This is a snapshot at one physical time, not an individual runner settling down while running. In the two-coordinate recurrence `(x,y)->(y,x+y mod 1)`, the error lies along the contracting eigenvalue `psi`. The other eigenvalue is `phi>1`; arbitrary phase pairs need not have this behavior.

For `r>=4`, the distance is at least `1/5-|psi|^r/5 >= d_infinity`, with equality at speed 3. Speeds 1 and 2 also exceed this bound directly. Thus this one irrational time keeps the selected reference at least `d_infinity`, approximately 0.170820 lap, from every Fibonacci-speed competitor, even in the infinite list. The finite upper bounds converge to the same value. This is a special-family statement; an infinite runner list is not an additional finite-runner case of the conjecture.

## 6. Counterchecks and one source anomaly

At the last prefix of a plateau, its largest speed is

$$w=F_{4m+1}=q a+1.$$

Replacing it by `w-1` makes it a multiple of `q`, destroying both old peaks by collision. The unchanged upper-bound subset allows equality only at those two times, so the modified finite schedule has a strictly smaller maximum. We do not calculate that new maximum here.

Replacing it by `w+1` gives phase `2a/q=2t_m` at the old peak, with distance `1-2t_m>d_m`. The unchanged subset and the surviving witness certify exactly the old maximum. These replacements are distinct from all other speeds.

| Last speed | Minus-one replacement | Plus-one replacement |
| --- | --- | --- |
| 34 | 33 destroys the `2/11` maximum | 35 preserves it |
| 233 | 232 destroys the `5/29` maximum | 234 preserves it |
| 1597 | 1596 destroys the `13/76` maximum | 1598 preserves it |
| 10946 | 10945 destroys the `34/199` maximum | 10947 preserves it |

All eight controls have exact certificates in the new script. This asymmetric response shows why closeness of speed values is not enough; their residues at the decisive times matter.

**Source detail:** the endpoint ordering in Pandey's abstract and Theorem 5 appears reversed when read as ordinary nonnegative residues. Already at `m=2` in our notation, `3*3=9 mod 11` is the upper endpoint and `8*3=2 mod 11` the lower. The interval bound and the unordered controlling pair agree with our checks; we use the actual residues for direction labels.

## What remains open in this project

The general Fibonacci plateau question is answered in the literature. Our interval reconstruction remains an unreviewed explanation, not an originality claim. Our new computation does not establish which reference runner is most constrained for `n>10`.

A useful next question is whether a small collection of blocking intervals can certify maxima for less structured speed sets, including our existing tight eight-runner examples. That would test whether the certificate idea transfers beyond Fibonacci recurrence. No new broad scan, graph implementation, or lattice computation was launched.
