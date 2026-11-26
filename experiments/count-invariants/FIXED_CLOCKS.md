# How many observation times do 16 runners need?

November 25, 2026. Research note for independent review. The unit circle has length one. All runners start at zero. A time is safe for a selected runner if every other runner is at circular distance at least $1/16$ from it. Different runners can use different times. A fixed schedule is a list of physical times selected before the speeds are known. A schedule may depend on a stated speed bound $H$. Times have the same units in every instance.

## A sufficient condition for all sixteen runners

Put one runner at speed zero. Take eleven positive odd speeds and four positive even speeds. Let $M$ be the smallest of the four even speeds. Assume the following.

- The eleven odds are distinct modulo 26 and each is at most $7M/8$.
- The four evens are distinct modulo 8 and each is at most $15M/8$.

**Every runner in every such lineup has a lonely time.** Both groups may vary. The odd degrees of freedom include independent additions of multiples of 26 within the size limit. The even speeds need only satisfy the stated size and residue conditions.

**Speed zero.** Take $t=1/2+1/(2M)$. The phase of each odd speed $s$ lies between $1/2$ and $1/2+7/16$. For an even speed $R$, the fractional part at this time is $R/(2M)$, between $1/2$ and $15/16$. Both intervals are safe.

**An odd speed $r$.** Try the six times $h/26$ with $h=1,3,5,7,9,11$. These are the units modulo 26 up to sign. Every other odd speed has a nonzero even difference from $r$ modulo 26. Its clearance at every one of these times is at least $2/26>1/16$. There are five even opponents, counting zero. Each has an odd difference $d$ from $r$. A failure at a candidate time requires $dh\equiv\pm1\pmod{26}$. An invertible $d$ spoils exactly one candidate, and a multiple of 13 spoils none. At most five of the six candidates can fail.

**An even speed $R>0$.** At $1/8$ each odd opponent is at least $1/8$ away, and each of the other three fast opponents is at least $1/4$ away. If $8\nmid R$, the zero runner is also clear. If $8\mid R$, move the time forward by $1/(16R)$. The distance to zero becomes exactly $1/16$. Every relative speed has magnitude at most $R$, since all speeds lie in $[0,15M/8]\subset[0,2R]$. During the adjustment each circular distance can fall by at most $1/16$. All fifteen opponents therefore clear.

This elementary sufficient condition uses the designated runner's relative residues, the relative speed during a short adjustment, and equality at the threshold. It proves the all-runner statement for this class without a smaller-runner theorem or a finite exhaustive search. Arbitrary 16-runner lineups can violate its hypotheses. For instance, $0,1,\ldots,15$ has a different parity split.

## When two runners collide, one adjustment can protect them both

The previous sufficient condition can be widened. Translate all speeds by the same integer so the colliding pair has speeds $0,F$, with $F>0$ divisible by 8. Suppose eleven odd speeds lie in $[0,F]$ and are distinct modulo 26. The three remaining even speeds lie in $[-2F,3F]$ with residues 2, 4 and 6 modulo 8, one of each. Allowing signed speeds here is equivalent to translating the lineup again until every speed is nonnegative.

At $1/8$ the three remaining even runners are each lonely. Runners $0$ and $F$ collide with each other. For both use the same time $1/8+1/(16F)$. Their mutual clearance becomes exactly $1/16$. From either member of the pair every odd opponent starts at least $1/8$ away and has relative speed at most $F$ in magnitude, losing at most $1/16$. Every remaining even opponent starts at least $1/4$ away and has relative speed at most $3F$ in magnitude, losing at most $3/16$. Thus both runners clear everyone. The six candidate times with denominator 26 still protect every odd runner. This proof allows every speed to vary and lets the speed ranges overlap.

The checker exercised all roles in 2,059 independently varied lineups of the first class, two explicit threshold-equality controls and 880 lineups of the wider class. In the last panel it directly verified that both members of the colliding pair achieve exactly $1/16$ at their shared adjusted time.

## An exact cost for a preselected schedule

Return to the [previously studied family](RELATIONSHIPS.md) with odd speeds $1,3,\ldots,21$ and even speeds $M,M+2,M+4,M+6$ for even $M\ge60$. All the hypotheses above hold. The following exact scheduling result concerns the stationary runner. Let $K(H)$ be the minimum size of a fixed schedule that supplies at least one safe time for it in every such lineup with $M+6\le H$.

**Any three times can fail below one million.** More generally, take any $s$ real times $t_1,\ldots,t_s$. For $j=0,\ldots,16^s$, put the point with coordinates $\{60jt_i\}$ in the unit cube. Partition the cube into $16^s$ half-open boxes of side $1/16$. Two points lie in the same box. Let $M$ be 60 times the positive difference of their indices. Then $60\le M\le60\cdot16^s$, and $\|Mt_i\|<1/16$ for every proposed time. Runner $M$ blocks the stationary reference at all of them. In particular, three times fail for some lineup of maximum speed at most 245,766. This is simultaneous pigeonhole approximation and applies even to irrational times.

**Four times suffice up to one million.** At $t_L=1/2+1/(16L)$ the odd speeds are within $21/(16L)$ of the opposite point. If $L\le M\le15L-6$, each of the four even speeds has phase in $[1/16,15/16]$. Start at $L=60$ and take the next $L$ to be $15L-4$, the first even $M$ beyond the current interval. The first four values are 60, 896, 13,436, and 201,536. Together they cover every even $M$ from 60 through 3,023,034. This proves $K(1{,}000{,}000)=4$. The checker separately tests the designated time against all fifteen opponents for each of the 499,968 eligible lineups under the million-speed cap.

For growing $H$, the pigeonhole lower bound and geometric upper bound give $K(H)=\Theta(\log H)$. The logarithm counts how many times a preselected schedule needs as the speed range grows. If the speed $M$ is known before the time is selected, the single formula $1/2+1/(2M)$ gives the stationary runner clearance exactly $1/2-21/(2M)$. The runner count stays fixed at 16 throughout.

### The growth rate for a schedule shared by all roles

For the consecutive-odd, four-even family above, one fixed schedule can supply a time for each role, with $O(\log H)$ times in all. Include the stationary-runner schedule and the six odd-runner candidates. For the fast roles take scales $L=32(3/2)^j$, $j=0,1,\ldots$, and use $1/5+1/(16L)$ for fast speeds $L+21\le R\le11L/5$. These intervals overlap because $3L/2+21\le11L/5$ for $L\ge32$, and the first interval starts at 53. Stop once the intervals cover $H$.

For a slow opponent $s\in\{0,1,3,\ldots,21\}$, the starting relative phase at $1/5$ is a multiple of $1/5$. The added displacement $(R-s)/(16L)$ is between $1/16$ and $1/5-1/16$, a safe range after any such multiple. The other fast gaps have magnitude 2, 4, or 6. They are at least $1/5$ from zero at the starting time, and move by at most $6/(16L)$. The lower bound for the stationary runner applies to any schedule covering all roles, so the all-role cost also grows as $\Theta(\log H)$. Its exact value at one million is open in this note.

## What motivated the test

OpenAI's November matrix multiplication paper matched an achievable exponent to a lower bound. That suggested asking for both a working schedule and a proof of how a shorter one can be defeated. The argument here uses elementary properties of the circle and simultaneous approximation. Hu and Jing's October Lonely Runner preprint from the earlier handoff gives a more direct connection to the general conjecture. Their uniform improvement combines arithmetic relations among speeds with overlaps among the intervals they block. The consecutive lineup supplies a control for any attempt to strengthen such an overlap argument at 16 runners. For reference zero its only witnesses are the eight odd sixteenths. An argument requiring a safe interval of positive length would miss all eight. [Matrix multiplication and formalization scope](https://github.com/openai/math/blob/main/lean/docs/379.md) · [Hu and Jing](https://arxiv.org/abs/2610.23790) · [Earlier relationship review and equality control](RELATIONSHIPS.md).

Run both checkers with standard Python 3.11 or later. The proofs above give the infinite conclusions. The scripts check examples, arithmetic boundaries and finite enumerations.

    python fixed_clock_bounds.py
    python all_role_scales.py

