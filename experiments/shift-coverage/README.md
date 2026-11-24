# Which 16 shifts can the other runners actually block?

We count the stationary reference among the 16 runners and use its 15 positive absolute speed differences. These results are for that chosen reference. The two-endpoint and fixed-core arguments earlier in this project protected an interval of times. Here the protected object is a set of 16 times. The same question applies to both: if every time is blocked, where must two opponents duplicate a block?

## Exact-cover test at the equality boundary

Take the opponents whose speeds are divisible by 16. The known smaller-runner case supplies a time $t_0$ when these opponents clear $1/16$ whenever at least one speed is excluded. All of them stay safe at the sixteen times $t_0+j/16$. An excluded speed $v$ can block only the indices for which its phase lands in the open arc of radius $1/16$.

- If $v$ is odd, it blocks at most two indices. If it blocks two, their difference is $v^{-1}$ up to sign modulo 16. One index is even and one is odd.
- Otherwise $g=\gcd(v,16)$ is 2, 4 or 8. It blocks at most $g$ indices. If it blocks any, these indices constitute one complete residue class modulo $16/g$ and all have the same parity.

Suppose the sum of these individual maxima is exactly 16. To spoil all sixteen times the opponents must realize their maxima **and** their blocked sets must tile the indices without overlap. This gives a short proof for an infinite class: if the number of odd opponents is odd, they would block an odd number of the eight even indices. Every remaining opponent can contribute only an even number of even indices at saturation. The required total of eight is impossible.

The same parity proof works for $n=2^a\ge4$ using $n$ shifts at clearance $1/n$, conditional on a safe time for the speeds divisible by $n$. Even exceptions have capacity $g=\gcd(v,n)$, while odd ones have capacity two. This is a sufficient condition at equality, with a specified divisibility hypothesis.

A finer test uses the possible inverse steps of the odd exceptions. Group them by their residues up to sign modulo 16, group even exceptions by their gcd with 16, and ignore order. Among capacity-16 profiles with at least two odd exceptions, there are **845** profiles in this convention. For **542** no tiling exists. **457** of these also evade the strict capacity tests on all four dyadic divisors 2, 4, 8 and 16. These counts describe profiles, each abstracting arbitrarily large integer speeds. They do not measure the frequency of such profiles among the modular search's candidates.

For every one of the other **303** profiles, we constructed fifteen distinct positive speeds and checked that every shift from a common core-safe time is blocked. The program realizes the required maximal blocks at $t_0=1/31$, choosing each speed in its congruence class modulo 16 and adjusting its residue modulo 31. The fixed speeds are multiples of 16 with safe phases at that time. Another starting time may still give a witness.

## Two controls

**Where equality adds information.** Use speeds $1,2,3,4,5,12$ and $16,32,\ldots,144$. Every time on the grid of denominator 272 misses the target, with exact grid maximum $1/17$. The strict capacity counts at divisors 2, 4, 8 and 16 are respectively 3, 5, 13 and 16. The full tiling is impossible because the three odd speeds cover one index of each parity apiece at saturation. Starting at $1/160$ for the nine multiples of 16, shift by $2/16$ to reach $21/160$. Its verified clearance is $1/10$. Every tuple in this residue class modulo 272 has the same grid obstruction and divisibility profile, so the argument certifies the full class even though its exact witness may change.

**Why a larger grid can stall.** For prime 251 let $A=(3,13,16,17,23,38,42,54,55,74,77,93,120)$. The 15 speeds $16A,1,503$ have maximum clearance exactly $15/251$ on the 4,016-point grid, while at $6/25$ the clearance is $2/25$. More generally, for any $b\ge4$ choose a positive $M$ divisible by $2^b$ with $M\equiv16\pmod{25\cdot251}$. The speeds $MA,1,503$ then retain the same witness at $6/25$. On the grid of denominator $2^b\cdot251$, scaling its numerator by $M/2^b$ permutes the residues modulo 251, so its core can reach at most $15/251$. The examples at different depths are compatible modulo the preceding grids. The familiar four-shift test already settles this class, since the thirteen multiples of four stay fixed and each of the other two speeds can block at most one of four shifts. This is a control for the existing method, separate from the equality improvement.

## Using a discrete logarithm to describe an entire first grid

At a prime $p>16$ assume no speed is divisible by $p$. A time numerator $h$ is blocked by speed $v$ exactly when the unsigned residue of $hv$ belongs to $1,\ldots,\lfloor(p-1)/16\rfloor$. In the cyclic multiplicative group modulo sign, taking discrete logarithms turns each speed's forbidden set into a translate of one fixed set of positions. At $p=37,41,43,47$ only residues 1 and 2 are forbidden. Every time is blocked exactly when no doubling cycle contains adjacent missing speed classes. At $p=53,59,61$ the rule requires three positions. The checker enumerates every support of up to 15 speed classes and independently checks the counts in the original modular arithmetic. This is an exact reformulation with manageable widths at these primes. Scaling it to the large primes is open.

## When the two tests can help each other

Define $\tau(p)$ as the fewest unsigned nonzero speed classes that together block the entire $p$-grid. Restrict to the modular search where no speed is divisible by $p$. Suppose the 16-shift equality test succeeds for a profile that escaped the strict dyadic counts, but the full grid of denominator $16p$ still has no witness. Then **$\tau(p)\le9$**.

Here is the counting argument. Write $e_0,e_1,e_2,e_3$ for the numbers of exceptions with gcd 1, 2, 4, 8 respectively, with $e_0\ge2$ as throughout the 845-profile panel. At equality, $2e_0+2e_1+4e_2+8e_3=16$. If $e_3>0$, the capacity at divisor 8 is $e_0+2e_1+4e_2=16-e_0-8e_3<8$, so the strict test already settles the case. Thus $e_3=0$. The even integer $e_0+e_1$ must be at least 4: if it were 2, both speeds would be odd and the strict divisor-4 cost would be only 2. The number of exceptions is therefore $4+(e_0+e_1)/2\ge6$, leaving at most nine core speeds. If that core did not block the whole $p$-grid, some $h/p$ would be core-safe. Our shift rule would then give a witness among $h/p+j/16$, points already on the full grid. This proves the bound. It limits additional eliminations **after** examining the full grid. A shift test might still save computation if applied earlier.

The two implementations in `check_log_grids.py` gave these covering numbers:

| Prime | 37 | 41 | 43 | 47 | 53 | 59 | 61 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Minimum covering classes | 9 | 10 | 12 | 12 | 11 | 12 | 12 |

Only 37 remains possible in this panel, and we can attain the bound there. Its nine classes $A=(1,3,4,7,9,10,11,12,16)$ are the powers of 4 modulo 37 up to sign. They alternate on the doubling cycle. Take $16A$ and the six exceptional speeds $1,2,3,4,5,12$. The strict dyadic tests all miss. The maximum on the 592-point grid is $2/37<1/16$, yet $t=1/13$ attains $1/13$. By the equality argument every lineup in this residue class modulo 592 has a lonely time, even though the witness $1/13$ is specific to this example.

We also measured the incremental effect on the consecutive seed at four selected primes. At primes 83, 89, 97 and 101 its fourth binary level retained 2,112, 128, 64 and 64 lifts, respectively. Strict divisor tests already cleared all 2,368. The equality test added zero on that panel. Prime 103 had no binary survivors to begin with.

## Reproduce and compare

Run `python check_shifts.py`, `python check_log_grids.py` and `python check_panel.py` with standard Python 3.11 or later. The first script verifies the exact classification, physical negative controls, reference witnesses and grid maxima. The second compares support-size histograms for seven primes. The third reuses the binary lift checker in the adjacent proof-survivors directory.

The strict few-exception shift is established prior work, and other 16-runner projects already test divisor shifts. Sungkawichai and Trakulthongchai and Allikvere give the modular framework. Munim reports a uniform result for two familiar 16-runner patterns, subject to its stated computational assumptions and review status. We make no priority claim. [Allikvere, Section 4.4](https://arxiv.org/html/2609.02604v2) · [Sungkawichai and Trakulthongchai, v2](https://arxiv.org/html/2604.23906v2) · [Munim's public research](https://github.com/munimtechnologies/lonely-runner-16).

For a route toward arbitrary lineups, Beck and Everett prove that absence of strict clearance forces a short integer relation among the speeds whose coefficients sum to an odd number. A proposed experiment is to retain such a relation when matching modular survivors across primes. Allow permutations and sign changes when aligning the speeds at each prime. Its value would be whether it rules out classes that pass the individual prime checks. A positive control for false alarms is the 37-prime example above: its speeds satisfy $1+2-3=0$, an odd-sum relation, and it still has a verified witness. [Beck and Everett, *Lonely Runner Relations*](https://arxiv.org/abs/2609.06259).
