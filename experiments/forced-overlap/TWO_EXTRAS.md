# All powers of two and two arbitrary integer speeds

November 24, 2026. **HYPOTHESIS with a complete proof candidate.** The argument is for a stationary reference, common starting point, unit circle, positive integer speeds, and a closed distance threshold. Independent specialist review and literature priority are open.

For every pair of positive integers $r,s$, there is a rational time $t$ for which every one of the speeds
$$
1,2,4,8,\ldots,\quad r,\quad s
$$
is at distance at least $1/6$ from the reference. This is the best guarantee over all pairs. A witness can always be chosen so that repeated doubling eventually follows the thirds or fifths cycle. In particular, the reduced denominator of the constructed time has odd part 3 or 5. Every finite subset of the dyadic core inherits the guarantee. For at least six total runners with relative speeds of this form, it implies the usual $1/n$ bound for that reference.

## The half-time construction

Write $\|y\|$ for distance to the nearest integer. Start with a pair having at least one odd speed. If both are odd, take $t=1/6$. Odd residues modulo 6 are 1, 3 and 5, and the dyadic phases from the first doubling onward alternate between thirds.

Otherwise write the pair as $a,2b$ with $a$ odd. The [one-extra construction](DYADIC_EXTENSION.md) gives a time $x\in[1/3,2/5]$ with
$$
\|bx\|\ge 1/5,\qquad \|2^j x\|\ge 1/5\quad(j\ge0).
$$
For completeness, if $3\nmid b$, choose $x=1/3$. If $3\mid b$, let $j$ be the least nonnegative integer with $b\le12\cdot4^j$ and take $x=1/3+1/(15\cdot4^j)$. Then $b/(15\cdot4^j)\in[1/5,4/5]$, and $b/3$ is an integer. Before doubling $2j$ times, the perturbation of a thirds phase is at most $1/30$. After $2j$ doublings the phase is $2/5$, and successive doublings visit the four nonzero fifths. This also proves the required location of $x$.

Consider the two times $x/2$ and $(x+1)/2$.

- Both are at least $1/6$ from an integer since $x\in[1/3,2/3]$. Every later dyadic phase is the same for the two choices and belongs to the already safe orbit of $x$.
- Speed $2b$ has phase $bx$ modulo one at either time.
- The two phases of $a$ differ by $a/2$, a half-integer. Of two antipodal points on the circle, at least one is at distance $1/4$ or more from zero. Choose its time.

Finally, for arbitrary $r,s$, write $(r,s)=2^m(r',s')$ with at least one of $r',s'$ odd. Construct $u$ for the reduced pair. Lift $u$ backwards through doubling $m$ times. At each step choose the preimage in $[1/4,3/4]$ (either works in a tie). This is possible since the preimages are half a lap apart. The new starting time $t$ has $2^mt=u\pmod1$, so the added runners land at $r'u$ and $s'u$. Each of the $m$ early dyadic phases is safe by construction. The rest follow the orbit of $u$. These finite backward steps preserve the eventual cycle. This covers all parity and common-factor cases.

**Example.** For extras 5 and 30, put $b=15$. Its one-extra time is $7/20$. The possible half-times are $7/40$ and $27/40$. At the first, speed 5 is only $1/8$ of a lap from zero. At the second it is $3/8$ away. Speed 30 stays $1/4$ away at both, and the powers of two are safe at $27/40$.

## Sharpness and a denominator prediction

With extras 3 and 5, the speeds include every integer from 1 through 5. Among the six points $0,t,\ldots,5t$, some cyclic gap is at most $1/6$. Its endpoints differ by a multiple $kt$ with $1\le k\le5$. At $t=1/6$ the entire speed set attains the bound. If all five distances are at least $1/6$, all six points are distinct and all six gaps equal $1/6$. Thus $t\bmod1$ has order six, so the only optimal times modulo one are $1/6$ and $5/6$.

More generally take extras $3d,5d$ with $d=2^m$. The subset $d,2d,3d,4d,5d$ forces $dt=\pm1/6\pmod1$ at any time meeting $1/6$. Consequently **every successful time in this family has reduced denominator exactly $6d$**. Its numerator before reduction is coprime to 6 and $d$ is a power of two. The construction supplies a successful time, so this is an exact prediction for every $m$. For $(48,80)$ it explains why the bounded test first succeeded at denominator 96.

## Exact checks

The [test protocol](TWO_EXTRAS_PROTOCOL.md) was frozen before the catalog was run, in commit [e2fa77e](https://github.com/tradingartofwar/the-lonely-runner-conjecture/commit/e2fa77e19c7c60af174720cbb3567bef49348e92). We tried every pair $1\le r<s\le128$, including speeds that duplicate core constraints, against all reduced rational times in $(0,1/2]$ of denominator at most 256 whose full doubling orbit stays safe. There were 68 catalog times. All 8,128 pairs received a witness, and each was rechecked using exact fractions. The largest first denominator was 96, attained only by $(48,80)$ with first witness $17/96$.

Separately, we implemented the parity construction itself and verified both extras and each full modular orbit on the same 8,128 pairs, on 162 ordered large-integer cases, and on five members of the sharp family. The repository maximum checker recovers both equality times for speeds 1 through 5 and all six equality times for speeds 1 through 6.

Run from the repository root with Python 3.11 or later. The optional CSV records the first catalog witness for each pair.

```sh
PYTHONPATH=. python experiments/forced-overlap/two_extras.py --rows /tmp/two_extras.csv
```

[Implementation](two_extras.py) · [Recorded results](two_extras_results.json)

## The next boundary

For three extras, $(3,5,6)$ together with the powers of two contains all speeds 1 through 6. The same gap argument caps the uniform target at $1/7$. Equality forces seven equally spaced points. All six nonzero sevenths work for this entire infinite set because doubling permutes the nonzero residues modulo seven. Thus any strategy for all triples at $1/7$ must accommodate times that reach neither the thirds cycle nor the fifths cycle. Whether every triple admits $1/7$ remains open in this work.

The shift by half a lap has a direct precedent in the common-divisor method. Allikvere's few-exception shift keeps divisible speeds fixed and counts which time shifts the other speeds forbid, adapting an argument of Rosenfeld. In our mixed-parity case, speed 1 and the odd extra are both exceptions to divisibility by 2. A plain count could lose both candidate times. The location of the one-extra witness guarantees that speed 1 accepts *both*, leaving the choice free for the odd extra. This is the extra information from the smaller solution that makes the extension work. [Allikvere, version 2, Lemma 4.6, September 24, 2026](https://arxiv.org/html/2609.02604v2)

The parity argument exploits the doubling symmetry of the core. Shifting the reference or replacing the core with arbitrary relative speeds can remove that symmetry. Earlier [work of Dubickas on lacunary speeds](https://web.mat.pmf.unizg.hr/glasnik/vol_46/no1_05.html) gives a different ratio hypothesis. A targeted literature check on November 24 did not settle priority for this statement. AI assisted with the construction, exposition and exact checks in response to Vance's direction to test generalization and seek counterexamples.
