# Two fast newcomers for cores of diameter at most 420

**November 24, 2026 · HYPOTHESIS (proof candidate).** This research note revisits Proposition 2 in the [November 24 working paper, pp. 3–4](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/890b2aa82c12cb9f255bb3a292620a25df0e0827/experiments/forced-overlap/paper/runner-additions/Fast_Runner_Extensions.pdf). In its proof, 157 ensures that every gap outside the duration argument is at most 419. A separate treatment of intermediate gaps gives the following candidate.

## Statement

Let $F$ consist of sixteen distinct integer speeds, with $\min F=0$ and $\max F=M\le420$. Let $x,y$ be integers satisfying $y>x\ge4M$. All eighteen runners start together on the unit circle. For each $R\in\{x,y\}$ there is a time $t_R$ such that $\|(R-s)t_R\|\ge1/18$ for every speed $s\in(F\cup\{x,y\})\setminus\{R\}$. Here $\|u\|$ is distance to the nearest integer. The two times may differ. The sixteen fixed reference roles are a separate question.

## Argument

Write $d=y-x$ and fix either newcomer $R$. There are three ranges.

**1. Small gap, $d<M$.** Since $1\le d\le419$ and $\operatorname{lcm}(2,3,4,5,6,7)=420$, choose $q\in\{2,\ldots,7\}$ that does not divide $d$. Use the paper's balanced time

$$t=\frac1q+\frac{1}{q(2R-M)}.$$

At time $1/q$ the phase against every fixed speed is on the $1/q$ grid. The added displacement against fixed speed $s$ lies between $(R-M)/[q(2R-M)]$ and $R/[q(2R-M)]$. These two endpoints are equally far from opposite ends of the grid cell. Thus the distance from every integer is at least $(R-M)/[q(2R-M)]\ge3/49$, using $R\ge4M$. The other newcomer is at distance at least

$$\left\|\frac d q\right\|-\frac{d}{q(2R-M)}\ \ge\ \frac{1}{q}\left(1-\frac{d}{2R-M}\right)\ >\ \frac{6}{49}.$$

Both margins exceed $1/18$.

**2. Large gap, $d>8M/3$.** Equation (3) on page 3 of the working paper bounds the duration of safe times for $R$ from below by

$$\frac{1}{18}\left(\frac{5}{2M}-\frac7R-\frac2d\right).$$

To see the estimate, take $0\le t\le1/(2M)$. All fixed phases lie in $[0,1/2]$. The phase of $R$ clears them all throughout the arc $[1/2+1/18,1-1/18]$ of length $7/18$. A speed $z>0$ spends between $\beta(T-1/z)$ and $\beta(T+1/z)$ in an arc of length $\beta$ during an interval of length $T$, by splitting into full periods and one remainder. Apply the lower bound to the $7/18$ arc at speed $R$ and subtract the upper bound for the other newcomer's blocking arc of length $2/18$ at relative speed $d$. This gives the displayed estimate. Since $7/R\le7/(4M)$ and $2/d<3/(4M)$, the duration is positive.

**3. Intermediate gap, $M\le d\le8M/3$.** If $R>14d$, then $7/R+2/d<5/(2d)\le5/(2M)$, so the same duration estimate is positive. If $R\le14d$, use

$$t=\frac5{6R}.$$

For all fixed speeds $s$, the relative phase $(R-s)t$ lies in $[5/8,5/6]$, since $0\le s\le M\le R/4$. The phase $dt$ lies in $[5/84,5/9]$, since $R\le14d$ and $d/R\le2/3$. Both intervals lie inside $[1/18,17/18]$. The distance test is the same for either sign of the relative speed $d$. This case includes $d=M$, $d=8M/3$, and the explicit time covers $R=14d$.

These three ranges cover every positive integer gap. Only the small-gap step uses the upper bound of 420 for the diameter.

## Exact controls

Each minimum below includes the other newcomer and **every** integer speed from 0 through $M$. It consequently gives a lower bound for every admissible choice of sixteen fixed speeds. The last two rows exercise equality in a split where the duration estimate for $R=x$ gives zero.

| $M$ | $(x,y)$ | Times for $(x,y)$ | Minimum clearances for $(x,y)$ |
| ---: | --- | --- | --- |
| 158 | $(632,1052)$ | $(1/1680,1/1680)$ | $(1/4,1/4)$ |
| 420 | $(1680,2100)$ | $(1/2016,1/2520)$ | $(1/6,1/6)$ |
| 420 | $(1680,2800)$ | $(1/2016,1/3360)$ | $(1/6,1/6)$ |
| 420 | $(5880,6300)$ | $(1/7056,1/7560)$ | $(5/84,1/18)$ |

For the first row, the two newcomers are separated by $420/1680=1/4$. Against the fixed speeds their relative phases have numerators in $[474,632]$ and $[894,1052]$ over 1680. Both ranges lie inside $[1/4,3/4]$ after division. In the final row the explicit time for $y$ is an additional equality control. The proof can also use positive duration for that role.

The table can be checked with Python's standard library.

```python
from fractions import Fraction as F

def clearance(M, R, other, t):
    opponents = [*range(M + 1), other]
    phases = [((R - s) * t) % 1 for s in opponents]
    return min(min(p, 1 - p) for p in phases)

controls = [
    (158, 632, 1052, F(1, 1680), F(1, 1680), F(1, 4), F(1, 4)),
    (420, 1680, 2100, F(1, 2016), F(1, 2520), F(1, 6), F(1, 6)),
    (420, 1680, 2800, F(1, 2016), F(1, 3360), F(1, 6), F(1, 6)),
    (420, 5880, 6300, F(1, 7056), F(1, 7560), F(5, 84), F(1, 18)),
]
for M, x, y, tx, ty, expected_x, expected_y in controls:
    assert clearance(M, x, y, tx) == expected_x
    assert clearance(M, y, x, ty) == expected_y
print("All eight exact clearances agree.")
```

## Review status

The candidate covers the two newcomer reference roles for $x\ge4M$. Extending it to all eighteen roles requires a separate argument for each fixed reference. The sharp diameter and the relation to earlier results remain open. A useful review would check the period estimate, the grid-cell margins, and the two equality boundaries in the intermediate-gap argument. The derivation and exact controls were prepared with AI assistance and await independent mathematical review.
