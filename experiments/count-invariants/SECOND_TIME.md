# Choosing a second lonely time after the first one fails

Research note, November 24, 2026. Counts include the reference runner. Use positive relative speeds measured from that runner. A time is safe at clearance $\delta=1/n$ when $\|vt\|\ge\delta$ for every opponent. Equality is allowed. The argument below addresses arbitrary speed ratios and is a candidate for independent review.

## The answer to the question

There is no single replacement time of the form $c/M$ determined just by whether the first blocker was low or high, where $M$ is the largest relative speed. There is an adaptive rule using the actual speeds. It finds a time whenever one exists with all except the $k$ fastest opponents still in their first safe arc, provided $2^k\le n$. At 16 this includes four freely wrapping opponents. The remaining eleven must still be in their first safe arc.

For the negative statement, normalize $M=1$ and fix any proposed positive replacement coefficient $c$. A sufficiently small rational speed fails both $7/2$ and $c$; all the other nonfast speeds can be distinct and inside the original safe band. Even the high-only branch defeats any fixed $c$. Include speed $2/7$, which collides at $7/2$. At 16, if $c<7/2$ add a rational speed just above $1/56$ with $cu<1/16$. If $c\ge7/2$, the interval $c(1/56,1)$ contains an integer in its interior. Choose a rational $u$ inside that speed range close enough to the corresponding quotient that $\|cu\|<1/16$. Fill the remaining slots with distinct speeds above $1/56$. This gives no low blocker at $7/2$, at least one high blocker there, and a failed replacement time. Rational normalized speeds become integers on multiplying by a common denominator.

## Constructing the replacement

Sort the $m=n-1$ relative speeds $v_1\ge\cdots\ge v_m>0$. If all but the $k$ fastest opponents must remain in their first closed safe arc, the common time window is exactly

$$
I_k=\left[\frac{\delta}{v_m},\,\frac{1-\delta}{v_{k+1}}\right].
$$

An inverted interval is empty. For one speed $v$, let $E_v(s)$ be the first time at or after $s$ when that speed is safe. If it is already safe, keep $s$. Otherwise jump directly to the first boundary of its next safe arc. The wait is at most $2\delta/v$.

For the $k$ fastest, denote the corresponding joint first safe time by $E_k(s)$. Start with $E_1=E_{v_1}$. From $s$ take the following three steps.

1. Move to $x=E_{k-1}(s)$.
2. Move to $y=E_{v_k}(x)$. If $y=x$, all $k$ are safe.
3. Otherwise move to $z=E_{k-1}(y)$.

Put $D_1=2\delta/v_1$ and $D_k=2D_{k-1}+2\delta/v_k$. If step 2 moved, $y$ is the **start** of a closed safe interval of duration $(1-2\delta)/v_k$. Step 3 takes at most $D_{k-1}$. Since the speeds are ordered,

$$
D_{k-1}
=2\delta\sum_{j=1}^{k-1}\frac{2^{k-1-j}}{v_j}
\le \frac{2\delta(2^{k-1}-1)}{v_k}
\le \frac{1-2\delta}{v_k}
\quad\text{when }2^k\le n.
$$

Thus $v_k$ remains safe at $z$, including at equality. No earlier joint safe time was skipped. Before $x$ some earlier speed was unsafe, from $x$ to $y$ the new speed was unsafe, and from $y$ to $z$ the earlier speeds were never all safe. This proves the recurrence and the wait bound by induction. Reflection gives the last joint safe time at or before $s$ as $-E_k(-s)$. For a fixed lineup the speed-specific inequality can hold at larger $k$ too. The simple guarantee at $n=14,15,16$ is respectively $k=3,3,4$.

Clip the old time $7/(2M)$ into $I_k$. If the slowest runner had not reached the safe arc, look forward first. Otherwise look backward first. If that candidate is outside the window, try the opposite direction. Because these are the nearest joint safe points on each side, failure on both sides proves that **this window** contains no witness. Larger $k$ permits a nested larger set of feasible times.

## Controls at 16

- **Low blocker.** Take relative speeds $9,11,12,\ldots,22,150,560$. At $1/160$ only speed 9 fails. At $1/144$ it reaches $1/16$ but speed 150 is only $1/24$ away. At $17/2400$ speed 150 clears and speed 560 is only $1/30$ away. At **$13/1792$** every opponent clears and speed 560 is exactly $1/16$ away. The one-fast window is empty and the two-fast repair succeeds.
- **High blocker.** Take $12,13,\ldots,24,160,560$. At $1/160$ speed 160 collides. The backward repair reaches **$3/512$**, with clearance exactly $1/16$ against 160.
- **A missed witness.** Take $1,31,33,\ldots,55,101$. Only speed 1 fails the first time. Even after freeing the four fastest opponents, the remaining speeds range from 1 to 49. Their first safe arcs have no common time at clearance $1/16$. Every speed is odd, so **$1/2$** places every opponent half a lap away.

## Frozen comparison

Each row has 256 inputs. The first numeric column counts failures of the original physical time. Each subsequent column counts how many of those failures the replacement recovers, cumulatively. These are deterministic sample results. The planted panels deliberately select where the first blocker lies. [Sampling rule and checks](SECOND_TIME_PROTOCOL.md).

| Runners | Panel | Initial misses | One free | Two free | Three free | Four free |
|---:|---|---:|---:|---:|---:|---:|
| 14 | Neutral | 211 | 95 | 98 | 101 | — |
| 14 | Low | 256 | 81 | 85 | 94 | — |
| 14 | High | 256 | 256 | 256 | 256 | — |
| 14 | Mixed | 256 | 0 | 67 | 74 | — |
| 15 | Neutral | 217 | 84 | 86 | 89 | — |
| 15 | Low | 256 | 75 | 80 | 86 | — |
| 15 | High | 256 | 256 | 256 | 256 | — |
| 15 | Mixed | 256 | 0 | 77 | 80 | — |
| 16 | Neutral | 220 | 71 | 76 | 76 | 85 |
| 16 | Low | 256 | 77 | 83 | 92 | 97 |
| 16 | High | 256 | 256 | 256 | 256 | 256 |
| 16 | Mixed | 256 | 0 | 88 | 91 | 95 |

An independent endpoint-enumeration procedure checked each tested window and each returned physical time. Another 1,470 exact comparisons checked the earliest-time recursion itself, including negative start times and equality at a boundary. Both procedures were written for this project.

## Consequence for the geometric estimate

Normalize $v_1=1$ and write $a=v_m$. A true failure implies $a<1/(n-1)$, since at or above that ratio the time $(1-\delta)/v_1$ works. Also each $I_k$ must fail. From its left endpoint the $k$ fastest become simultaneously safe within $D_k$. Thus failure implies

$$
v_{k+1}>\frac{n-1}{1/a+2\sum_{j=1}^{k}2^{k-j}/v_j}.
$$

These necessary inequalities keep the identities of different ranked speeds. Using them successively bounds $v_2,\ldots,v_{k+1}$ below as functions of $a$. A too-slow runner can force several distinct fast opponents away from the relaxed worst shape. This is where the physical timing information enters the product estimate.

We used the scalar function $h_m$, the shape factor $H$, and the unmodified lattice factor $K$ from the [preceding note](README.md). Partition $[0,1/(n-1)]$ into 512 equal bins. In each bin, evaluate the increasing speed lower bounds at the left endpoint and the decreasing $h_m(a)$ at the right. At a left endpoint of zero use zero lower bounds for all nonfast speeds. Charge each distinct fast slot at least its scalar minimum on the allowed interval, and charge all unused slots at least the global scalar minimum. The slowest and the charged fast slots are distinct indices in all rows. The product of these $m-1$ factors bounds $H^{m-1}$ below. Integer floors of rational lower bounds on $h_m^m$ keep the calculation conservative. Using $\prod v_i\le (KH)^{-m/2}$ bounds the natural logarithm of a hypothetical primitive counterexample's speed product, assuming the lower runner results. [Allikvere, Theorem 3.8 and its proof](https://arxiv.org/html/2609.02604v2#S3.SS6).

| Runners | Previous clock | One free | Two free | Three free | Four free |
|---:|---:|---:|---:|---:|---:|
| 14 | 340.377 | 339.819 | 339.716 | 339.714 | — |
| 15 | 414.027 | 413.388 | 413.282 | 413.279 | — |
| 16 | 496.044 | 495.330 | 495.222 | 495.218 | 495.218 |

All ceilings are rounded upward. Freeing a fourth runner recovered more 16-runner sample inputs but gave no further improvement in this 512-bin product estimate. Independent review remains open. The necessary prime-divisibility checks for a proof at 16 remain to be done.

## Reproduce

Run from this directory using Python 3.11 or later.

    python test_second_time.py
    python second_time_bound.py

The latter imports the existing scalar shape certificate. The protocol file was recorded before the panel was run. Its SHA-256 is aecfcba92cff62e546eb608840008268b728d1c0939bbeaeec6a6e93e1b40d58.
