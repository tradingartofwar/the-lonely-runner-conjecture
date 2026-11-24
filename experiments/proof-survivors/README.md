# Why particular residue classes survive the Lonely Runner search

Counts below include the stationary runner. A witness is a time at which it clears every opponent by at least $1/n$ on a unit track. This note compares the mechanisms in the existing proofs with two small exact computations.

## What closed the earlier proofs

The computer-assisted proofs for 8 through 15 bound the product of the positive relative speeds of a possible primitive counterexample. A successful check at a prime $p$ forces at least one speed of that counterexample to be divisible by $p$. Once the product of the verified primes exceeds the upper bound, the counterexample is impossible. This explains why finitely many computations can establish a result for every lineup. Sieve construction and the last step for the surviving residue classes differ by runner count. Earlier proofs for smaller counts used several methods. [Rosenfeld](https://doi.org/10.1090/mcom/4243), [Trakulthongchai](https://doi.org/10.37236/14972), [Sungkawichai and Trakulthongchai, v2](https://arxiv.org/html/2604.23906v2), [Allikvere, v2, Sections 2–5](https://arxiv.org/html/2609.02604v2).

- **13 runners.** We independently read the authors' residual seed lists for the 91 primes used in Table 1. We found 12 distinct listed tuples per prime, 1,092 in total. Each is a reordering of the residues of a single nonzero multiple of $(1,\ldots,12)$, with signs identified. The large-prime polynomial result applies to this entire class. The audit checks the logged residuals. Their exhaustive generation is a separate part of the authors' proof. [Original log snapshot](https://github.com/vzsky/lonely-runners/tree/bd4fb465b874db1fe29b73ee3e7b3811674c00a5/results/raw_log_13).
- **14 runners.** Allikvere reports that at all 111 archived primes precisely two classes persisted through binary refinement. The representatives are $(1,\ldots,13)$ and $(1,\ldots,11,13,24)$. At the final level 14, every lift without a grid witness had all coordinates divisible by 7. A primitive counterexample has greatest common divisor 1. [Sections 4.2–4.3](https://arxiv.org/html/2609.02604v2).
- **15 runners.** The same paper reports just the consecutive class at 52 of the verified primes and additional classes in the other 19 searches. The final step factors 15 as $3\cdot5$. When enough speeds share a divisor, shifting the time by fractions with that denominator keeps those runners safe and lets the exceptional runners move. [Sections 4.4–5](https://arxiv.org/html/2609.02604v2).

## Why a finer grid can keep missing a real witness

For the literal consecutive tuple, the witness times have reduced denominator exactly $n$. Indeed, if all relative speeds $1,\ldots,n-1$ clear $1/n$ at $t$, every pair among the $n$ points $0,t,\ldots,(n-1)t$ is separated by at least $1/n$. Their $n$ gaps sum to 1, so all gaps equal $1/n$. The possible times are exactly $a/n$ with $\gcd(a,n)=1$. A grid of denominator $D$ hits a witness exactly when $n$ divides $D$.

We checked a stronger, finite question by enumerating **all binary lifts** of each indicated residue tuple at primes 199 and 251. Each stage keeps lifts lacking a grid witness and passing the common-divisor condition for a possible primitive counterexample. Levels 1, 2, 4, 8, 16 and 32 use time denominators equal to the level times the prime.

| Seed | Retained at successive levels, $p=199$ | Retained at successive levels, $p=251$ |
| --- | --- | --- |
| 13, consecutive | 1, 1, 2, 4, 8, 16 | 1, 1, 2, 4, 8, 16 |
| 14, consecutive | 1, 3, 2, 4, 8, 16 | 1, 1, 2, 4, 8, 16 |
| 14, speed 12 replaced by 24 | 1, 1, 2, 4, 8, 16 | 1, 1, 2, 4, 8, 16 |
| 15, consecutive | 1, 1, 2, 4, 8, 16 | 1, 1, 2, 4, 8, 16 |
| 16, consecutive | 1, 1, 2, 4, 0, 0 | 1, 1, 2, 4, 0, 0 |

At both primes the whole consecutive residue class clears by level 16 for 16 runners. The denominator argument alone explains the literal tuple. Exhausting the lifts establishes the stronger statement for these two primes. Other initial classes require separate checks.

## An exact rule for the first doubling when $p=2n-1$ is prime

Fix $n\ge4$, $p=2n-1$ prime. Work with speeds nonzero modulo $p$, identifying a residue with its negative. There are $n-1$ such classes. Each speed blocks exactly one unsigned nonzero time on the $p$-grid, since the only nonzero forbidden distances are $1/p$. To cover all times, the $n-1$ speeds must therefore occupy every class once. Up to signs and order, the only starting tuple is $(1,\ldots,n-1)$.

At level 2 each class $j$ has an even lift and an odd lift. Let $E$ be the classes given the even lift. A lift survives the grid and gcd tests exactly when:

1. $E$ is nonempty and at least two classes lie outside $E$.
2. For every unsigned class $j$, if $j$ and $3j$ lie in $E$, then $2j$ lies in $E$ (multiplication is modulo $p$, up to sign).

To see this, even time numerators reproduce the blocked $p$-grid. At the half-lap time some speed must be even to block it. The gcd test eliminates assignments with at most one odd speed. For any remaining odd numerator $h$ coprime to $p$, a speed can block only at absolute residues 1, 2 or 3 modulo $2p$, since $3<2p/n<4$. Set $j=h^{-1}$ modulo $p$, up to sign. A block requires an odd lift at $j$, an even lift at $2j$, or an odd lift at $3j$. This gives condition 2 in both directions.

We compared the rule's complete set of predicted assignments with direct integer grid enumeration. The sets agreed for all six rows.

| Total runners | Prime | Retained parity assignments |
| ---: | ---: | ---: |
| 7 | 13 | 24 |
| 9 | 17 | 78 |
| 10 | 19 | 132 |
| 12 | 23 | 330 |
| 15 | 29 | 2,018 |
| 16 | 31 | 2,746 |

The 10- and 12-runner counts also appear in the authors' logs. For those individual primes, the 10-runner log reaches zero after lifting by 5 to level 10, and the 12-runner log reaches zero at level 36. The first-doubling rule explains one reproducible stage. Subsequent levels and other primes are separate problems. [10-runner log](https://github.com/vzsky/lonely-runners/blob/ffd4a6b9b8ecf284b83203fc8057dd5d0e9cb7b9/results/result_10), [12-runner log](https://github.com/vzsky/lonely-runners/blob/bd4fb465b874db1fe29b73ee3e7b3811674c00a5/results/result_12).

## Reproduction

Run `python binary_lifts.py` in this directory using Python 3.11 or later. To repeat the separate log audit, download the linked raw_log_13 directory at its pinned revision and run `python audit_seeds.py /path/to/raw_log_13`. Both programs use the standard library.
