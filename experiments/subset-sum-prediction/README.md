# Can four weights predict a shared lonely time?

The independent setter chose all 15 nonempty subset sums of four positive integer weights. The public conditions are $b>a$, $c>a+b$, $d>a+b+c$, $\gcd(a,b,c,d)=1$, and $16\mid S$ for $S=a+b+c+d$. The inequalities make all subset sums distinct. Include a runner at zero. The family has four varying weights and retains the pairing $u\leftrightarrow S-u$. Every time with denominator dividing 16 is blocked by speed $S$.

A separate solver team received the public family before the examples were opened. The setter made 60 draws, three in each of twenty scale/gap strata, using only primitivity and uniqueness filters. The [frozen rule and protocol](https://github.com/tradingartofwar/the-lonely-runner-conjecture/tree/de0a4c64511f6881df29514f8ad16ba9504d7f1d/experiments/subset-sum-prediction) include the panel, generator and seed commitments. The solver had access to the descriptions of the strata. Separation was procedural within the team.

## The sealed result

| Which gap varied | Cases | Four-weight prediction | First-lap formula | Earlier one-time predictor | Reduced denominators through 32 |
|---|---:|---:|---:|---:|---:|
| All close to the superincreasing boundary | 12 | 12 | 11 | 12 | 12 |
| Balanced gaps | 12 | 9 | 0 | 11 | 12 |
| Stretched first gap | 12 | 5 | 0 | 10 | 12 |
| Stretched middle gap | 12 | 1 | 0 | 11 | 12 |
| Stretched last gap | 12 | 12 | 3 | 12 | 12 |
| **Total** | **60** | **39** | **14** | **56** | **60** |

The frozen predictor returned a single rational time for 39 lineups. All 39 passed independent verification on all 15 physical opponents. It abstained on 21. Of its 39 successes, 14 used the first lap, 13 aligned the fastest weight, nine used parity, two fixed the three lower phases, and one used complements. No unverified fallback was counted. The earlier predictor and the four-weight predictor overlapped on 38 successes. The earlier predictor alone covered 18, the four-weight predictor alone covered one, and the direct grid covered the three both missed. The grid contained 162 candidate times up to reflection. It found a witness in every lineup, so no row required a full interval search.

The complement prediction was made on weights $(114,139,359,1100)$. It gave $20551/25680$, with verified minimum clearance exactly $1/15$. Both the earlier predictor and the denominator scan also succeed on this lineup at the requested $1/16$ threshold. On $(79,409,523,1037)$ only the new predictor of the two single-output methods succeeded. On $(3,5,28,60)$ the new method abstained and the older predictor missed. The exact time $2/23$ works.

## A theorem obtained before opening the examples

**Suppose $a,b,c$ share the same nonzero residue modulo five. The formulas below predict a single time with clearance exactly $1/15$ for the two extreme runners, zero and $S$.** All four weights may vary; $d>a+b+c$ is enough for the estimates. Only one of the sixty held-out lineups met this particular residue condition.

Put $C=a+b+c$ and $e=1/15$. Choose $h\in\{1,2,3,4\}$ with $ha\equiv1\pmod5$, and put $t_0=h/5$. The seven nonempty lower subset sums have phases in $\{1/5,2/5,3/5\}$ according to how many weights they contain. The other eight speeds are $S$ and the complements of these seven sums. This is why the total phase is the quantity to adjust.

- If $\{St_0\}=1/5$, move backward to $t=(\lfloor St_0\rfloor-e)/S$. The displacement is $4/(15S)$. Each lower sum moves by less than $2/15$, since $C<S/2$. Its new phase $z$ is in $[e,1-2e]$, and the complement has phase $1-e-z$ in the same interval.
- Otherwise move forward to $t=(\lceil St_0-e\rceil+e)/S$. The displacement is at most $2/(3S)$ because $\{St_0\}$ can only be $0,2/5,3/5,4/5$. A lower sum therefore moves by less than $1/3$. Its new phase $z$ lies in $[2e,1-e]$, and the complement has phase $1+e-z$ in that same interval.

All fourteen intermediate runners are at least $e$ from zero. The total phase is exactly $e$ or $-e$, so the minimum distance to zero is $e$. Reflection about the two extremes gives the identical minimum from speed $S$. The statement does not require all sixteen runners to become lonely simultaneously.

**Why a fixed list of times can miss this subfamily.** Fix the lower weights at $(1,6,11)$ and take $S=16k>36$, $d=S-18$. For any finite list of rational times choose $S$ divisible by all their denominators. Runner $S$ then collides with zero at every listed time, while the formula above still gives $1/15$. Even arbitrary fixed real times $\tau_1,\ldots,\tau_m$ can be defeated. Partition $[0,1)^m$ into boxes of side $1/17$. Infinitely many of the vectors $(\{16j\tau_i\})_i$ fall in the same box. Subtracting one fixed such index from arbitrarily large others gives arbitrarily large $k$ with every $\|16k\tau_i\|<1/17$. This compares against a fixed menu across unbounded parameters. It imposes no such restriction on another speed-dependent algorithm. The original project had already used simultaneous approximation in a different family. [Earlier fixed-clock study](../count-invariants/FIXED_CLOCKS.md).

## The other predeclared certificates

- **First lap.** At $1/(S+a)$ every speed lies between the phases of $a$ and $S$. The minimum is exactly $a/(S+a)$ and this reaches $1/16$ when $S\le15a$.
- **Parity.** The weights have two or four odd entries. The least positive even subset sum $E$ is the minimum of the even entries and the sum of the two smallest odd entries. The largest odd subset sum is $O=S-\min(\text{odd weights})$. At $1/2+1/(16E)$ the even speeds occupy $[1/16,15/16]$ if $S\le15E$. The odd speeds move forward from $1/2$ by at most $7/16$ if $O\le7E$.
- **Fixed lower phases.** At $1/(16a)$ the lower subset sums range from $1/16$ to $C/(16a)$ under the rule's size condition. Translating time by $j/g$, $g=\gcd(a,b,c)$, fixes them all. Since $\gcd(d,g)=1$, the phase of $d$ can be placed in any closed interval of length at least $1/g$. The interval $[1/16,(15a-C)/(16a)]$ has that length whenever $g(14a-C)\ge16a$. The ceiling and modular inverse in the predictor directly select the translate.
- **Fast wrap.** Put $k=\lceil(d-a)/(16a)\rceil$ and take $t=(16k+1)/(16d)$. This sets the fast phase to $1/16$ and has $at\ge1/16$. If $C(16k+1)\le14d$, the largest lower subset phase is at most $14/16$. Adding the fast generator is safe. Together the last two certificates handle the binary-prefix subfamily $(a,2a,4a,d)$. The public gcd and divisibility conditions force $a$ odd. If $a\ge3$, $7a^2\ge16a$ gives the fixed lower phase condition; if $a=1$, write $d=16m-7$ for $m\ge1$, so $k=m$ and $7(16m+1)\le14d$.
- **One interval for each prefix.** Within a fixed choice of generator lap indices $k_j$, each unwrapped phase is $w_jt-k_j$. Require each to be at least $1/16$. Their sum through step $i$ is constrained to be at most $1-(5-i)/16$. The program chooses the least nonnegative lap compatible with the running lower time bound, intersects the interval, and abstains from this branch on an empty intersection. It never backtracks. At step four the sum is at most $15/16$, so every nonempty subset has safe phase at the chosen midpoint.
- **Wide scale separation.** Start at $1/(16a)$. For each successive weight, round the time forward to put that phase at $1/16$. The adjustment for weight $w$ is less than $1/w$. The total increase of the earlier phases above their assigned values is less than $a/b+(a+b)/c+C/d$. If this is at most $11/16$, the final unwrapped sum is at most $15/16$, preventing any wrap and ensuring all nonempty subsets are safe.

## A control selected after the trial

An explanation based purely on the smallest and largest speeds cannot cover the following three subfamilies with a single predicted time. Fix the same multiple $S$ of 16, $S\ge112$. Choose one of three lower triples $(1,2,13),(1,3,8),(1,4,6)$ and put $d=S-a-b-c$. In every case the extrema are 1 and $S$. Together the three triples' lower subset sums include every integer from 1 to 16. For any time $t$, among the seventeen points $0,t,\ldots,16t$ two are within $1/17$. Their difference has speed in $\{1,\ldots,16\}$. At least one of the three lineups therefore misses $1/16$ at any time chosen only from the extrema.

A single rounding, using the lower triple's identity, gives a witness in each case. For $(1,2,13)$ take $t_*=1/12$; for the other two take $t_*=1/16$. Put $t=(\lceil dt_*-1/16\rceil+1/16)/d$. For the first triple, $d\ge96$ gives $1/12\le t<1/10$. The three lower phases are $t,2t,13t-1$, each at least $1/16$ and with sum at most $3/5$. For the other two triples $d\ge100$, $1/16\le t<1/16+1/d$, and the largest lower subset sum is at most $12t\le14/16$. Adding the fast phase $1/16$ keeps all subsets safe. This control demonstrates exactly which coarse description loses the prediction. It was found after scoring and is separate from the held-out evidence.

## Reproduce

Use Python 3.11 or later in this directory. The scorer regenerates the panel from its seed, checks the commitments, emits all frozen predictions before scoring, and checks against the original fifteen integer speeds. The ledger records per-lineup outcomes and a verifying time on the comparison grid.

    python score.py panel.json ledger.json
    python check_controls.py

The full independently chosen family remains open in this experiment. The 21 abstentions have verified witnesses. The wide middle-gap stratum (one certificate in twelve) records the main deficiency of the frozen rule. These arguments have received internal checks. Mathematical priority and independent review remain open.

