# What persists as the runner count changes?

November 24, 2026. Research note for independent review, following Vance Williams's question about invariants across the solved counts. Let $n$ include the reference runner. The $m=n-1$ speeds below are positive integer distances in speed from that reference. Either sign of a relative speed gives the same distance on the circle. Equality at clearance $1/n$ counts.

## What the existing proofs used

Two and three total runners have elementary proofs. At four there are Diophantine approximation proofs, at five a computer-assisted proof using exponential sums, at six separate direct proofs, and at seven a prime-filtering argument. Starting at eight, a bound on a possible counterexample and exhaustive modular checks gave a method that transferred between counts. The nine- and ten-runner proofs refined the sieve. At eleven and thirteen a polynomial argument treated a persistent consecutive residue pattern. At twelve intermediate sieves and symmetry sufficed. At fourteen the final step used direct enumeration. At fifteen it used $15=3\cdot5$ and time shifts. Allikvere used the smaller cases simultaneously, imposing an inequality at each dimension of the lattice calculation. [Earlier cases](https://arxiv.org/html/2604.23906v2#S1) · [Seven](https://doi.org/10.37236/772) · [Eight](https://doi.org/10.1090/mcom/4243) · [Nine and ten](https://doi.org/10.37236/14972) · [Fourteen and fifteen](https://arxiv.org/html/2609.02604v2).

## An invariant in the geometric bound

Allikvere's Lemma 3.7 analyzes a factor that converts a lattice estimate into a bound on the product of the speeds of a hypothetical primitive counterexample. Normalize $u_i=v_i/M$, where $M$ is the maximum relative speed, and choose $u_1=1$. For $0<s\le1$ write $q(s)=1+2s-s^2$, $a(s)=q(s)/s^{2/m}$ and $w(s)=s^2/q(s)$. The paper's shape factor satisfies $R_m^2=m^2/H$, where $H=(\sum w(u_i))\prod a(u_i)$. [Definitions and shape bound](https://arxiv.org/html/2609.02604v2#S3.SS5).

Because $w(1)=1/2$ and $a(1)=2$, the arithmetic–geometric mean inequality reduces this problem to one variable at every $m\ge2$. Set

$$
h_m(s)=[1+2(m-1)w(s)]a(s)^{m-1}
=\frac{[1+2s+(2m-3)s^2]q(s)^{m-2}}{s^{2(m-1)/m}}.
$$

The arithmetic mean of the $m-1$ numbers $1+2(m-1)w(u_i)$ for $i\ge2$ is $1+2\sum_{i=2}^m w(u_i)$. Bound this mean below by their geometric mean and multiply by $\prod_{i=2}^m a(u_i)$ to obtain

$$
H\ \ge\ \left(\prod_{i=2}^m h_m(u_i)\right)^{1/(m-1)}
\ \ge\ \min_{0<s\le1}h_m(s).
$$

The last bound is attained in the relaxed continuous problem by taking every coordinate after the first equal to a minimizer. Actual runner speeds may be distinct. For $m\ge5$, the logarithmic derivative on $0<s<1$ has the sign of the cubic

$$
(m-1)(2m-3)s^3+(2m-5)s^2+(m-5)s-1.
$$

Differentiation gives this cubic times $2(m-1)(1-s)/(ms[1+2s+(2m-3)s^2]q(s))$. The cubic increases strictly from a negative value to a positive one. Its unique root minimizes $h_m$. This recovers the cubics in the author's 14- and 15-runner calculations and gives the 16-runner one.

## A physical time excludes the worst shape

Put $t=7/(2M)$. The fastest opponent is half a lap from the reference. Any other opponent whose relative speed satisfies

$$
\frac{2}{7n}\le\frac{v}{M}\le\frac{2(n-1)}{7n}
$$

has phase between $1/n$ and $1-1/n$. If all remaining speeds are in the interval, this time works. The half-integer $7/2$ was selected while exploring several possible times.

In a failing lineup at least one of the remaining ratios must therefore lie outside that closed interval. Write $a,b$ for its endpoints and $h_*$ for the minimum of $h_m$. At each count below the minimizer lies strictly between $a$ and $b$. Monotonicity and the geometric-mean bound give

$$
H\ge [h_*^{m-2}\min(h_m(a),h_m(b))]^{1/(m-1)}.
$$

At 16, for instance, the interval is $[1/56,15/56]$. With relative speeds $10,11,\ldots,22,150,560$, the time is $1/160$. Runners 10 and 150 attain the two allowed endpoints. Replacing 10 by 9 breaks this particular time.

Write $B_r=4r^2/[n^2(n-r)^2]$ and $K=\prod_{r=1}^{m-1}(B_r-B_{r-1})$. Assuming the lower cases, Allikvere's Theorem 3.8 and its proof yield $\prod v_i\le(KH)^{-m/2}$ pointwise for a primitive counterexample whenever each successive ratio of increments of $B_r$ exceeds $4/3$. The checker verifies this condition at each count. At 16 its minimum is $3751/2349$. The paper denotes our $m$ by $n$. [Theorem and pointwise product identity](https://arxiv.org/html/2609.02604v2#S3.SS6).

Ratios below are rounded to nearest. The natural-log ceilings are rounded upward. The 14- and 15-runner rows are retrospective comparisons inside a proof by contradiction.

| Total runners | Common slower/fastest ratio in the unrestricted worst shape | Log product ceiling from unrestricted scalar estimate | Log ceiling after excluding the known lonely time |
|---:|---:|---:|---:|
| 14 | 0.084930269 | 341.011 | 340.377 |
| 15 | 0.078207040 | 414.653 | 414.027 |
| 16 | 0.072476828 | 496.665 | 496.044 |

Allikvere's bounds rounded upward were 341.032 and 414.780 at 14 and 15. At 16 the forced divisor $\operatorname{lcm}(2,\ldots,16)=720720$ reduces the sufficient log-sum of additional distinct primes greater than 16 to 482.556, using the unrounded calculation. Each such prime must be proved to divide the speed product for **every** primitive counterexample. This note certifies no such prime.

Munim Technologies independently reports a multiplier $12150/9163$ on $K$ at 16 and a prime target of 481.123. Their article also identifies the shape with one fast speed as relevant. Conditional on their multiplier, the physical-time estimate gives a sufficient target of **480.440**. We checked the substitution. Their proof of the multiplier is a separate input awaiting independent review. A reduction of 0.683 is smaller than the log of one prime near 800 (about 6.68). [Munim's result and limitations](https://www.munimtech.com/research/dual-cap-lonely-runner-flag-bound).

**Question for a follow-up.** If a lineup escapes the clock, record which relative speed escapes and on which side. Can a second clock certify that runner together with the others? To improve the bound uniformly one needs a lower bound on $H$ over the shapes escaping both clocks. The displayed product of individual scalar penalties makes such a comparison possible.

## A separate change on the grid of 2n times

Consider every time $h/D$ with $D=2n$. A speed blocks a time precisely when the residue of its product with $h$ is $0,1$, or $-1$ modulo $D$. A single speed divisible by $D$ blocks the entire grid. In the absence of such a speed, full blockage is equivalent to both requirements below.

1. Every unit residue modulo $D$, up to sign, occurs among the speeds. A numerator $h$ coprime to $D$ is blocked exactly by speeds congruent to $\pm h^{-1}$.
2. For each distinct prime $p\mid D$, some individual speed is divisible by $D/p$. The numerator $h=p$ can only be blocked at residue zero. Every nonzero nonunit numerator is a multiple of such a $p$, so these speeds suffice for all other numerators.

A speed doing two different divisor jobs would have to be divisible by $D$. Thus the minimum number of speeds needed to block this grid with no multiple of $D$ is exactly $\varphi(D)/2+\omega(D)$, where $\omega$ counts distinct prime factors. Take one representative per unit sign pair and each integer $D/p$ to attain it. Moody states the unit-class obstruction in a public preprint. [Moody](https://rxiverse.org/abs/2509.0023).

| Total runners | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Minimum blocking speeds without a multiple of $2n$ | 2 | 3 | 3 | 4 | 4 | 5 | 5 | 5 | 6 | 7 | 6 | 8 | 8 | 7 | 9 |

For 4, 8 and 16 runners, one speed must be $n\bmod 2n$ and all $n/2$ odd sign pairs must occur. At 4 this uses all three opponents. At 8 it leaves two opponents free. At 16 it leaves six free. With one total runner there are no opponents.

**Comparison with the earlier prime test.** At $p=2n-1$ prime, take the normalized consecutive seed and all lifts to modulus $2p$ with no witness there and at least two odd speeds, as in the [previous experiment](../proof-survivors/README.md). The new grid and $2p$ share exactly the factor 2. With no speed divisible by $2n$, a parity assignment is compatible with blocking both grids exactly when it has enough odd and even slots for the required classes. Necessity follows from the distinct roles. For sufficiency assign one slot per role, fill the others with nonzero residues of matching parity, and lift each slot by the Chinese remainder theorem. This establishes compatibility on those two grids.

| Total runners | 4 | 6 | 7 | 9 | 10 | 12 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Earlier parity assignments | 3 | 10 | 24 | 78 | 132 | 330 | 2,018 | 2,746 |
| Can block both grids without a multiple of $2n$ | 3 | 5 | 15 | 70 | 120 | 319 | 2,004 | 2,623 |
| Would require a multiple of $2n$ to block both | 0 | 5 | 9 | 8 | 12 | 11 | 14 | 123 |

As a control, speeds $1,\ldots,16$ with 15 omitted admit $15/32$ with clearance $1/16$. Swap 8 for 15. Every time on the 32-point grid now fails, yet $3/25$ works with clearance $2/25$. More generally a single speed divisible by every denominator in any finite list blocks that entire list.

## Reproduction and scope

Run the following with Python 3.11 or later in this directory, alongside the existing proof-survivors directory.

    python check_shape.py
    python check.py

The first checker brackets the cubic root by rational bisection, bounds integer powers of the shape factor and speed product with fractions, and encloses logarithms for display. It checks the proposed time at both boundary speeds. The second checker enumerates 1,016 small-grid subsets, checks minimal blocking sets at every count from 2 to 16, and constructs and checks integer lifts for every compatible parity assignment in the table. The symbolic inequality supplies the general quantifier. Independent mathematical and priority review remain open.

[Second-time follow-up](SECOND_TIME.md). The adaptive repair handles up to four freely wrapping opponents at 16 and tightens the conditional log-product ceiling to 495.218.

[Team review of runner relationships](RELATIONSHIPS.md). Matched 16-runner lineups, lap and equality controls, and a comparison of shared safe windows on different laps.

[Two independent short relations](TWO_RELATIONS.md). A Fourier argument for the first open count and exact controls on how much two relations can distinguish.

[Fixed observation times and a shared adjustment](FIXED_CLOCKS.md). An exact four-time lower and upper bound for a selected runner, and a proof for all sixteen roles in varying parity classes.
