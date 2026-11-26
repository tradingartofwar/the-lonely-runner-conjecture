# Nineteen runners with two freely chosen speeds

**November 24, 2026 · HYPOTHESIS (computer-assisted proof candidate).** Let $Q=\{0,1,\ldots,14,105\}$ and $F=Q\cup\{420\}$. For **every** pair of distinct positive integer speeds $x<y$ outside $F$, every runner in $F\cup\{x,y\}$ has a time at distance at least $1/19$ from each of its eighteen opponents. Times may differ by runner. This removes the fixed speed 480 from the [one-addition result](NINETEEN_FIXED_CORE.md). A second argument below also frees 420 when all three additions are sufficiently large and separated.

## Two arbitrary speeds

Put $K=1680$ and $\delta=1/19$. The following cases partition all eligible pairs.

**1. Both additions are fast, $K\le x<y$.** For each $r\in F$, the verifier finds a rational interval $[a,b]$ safe against the other fixed speeds, of length $L$ with $15(K-r)L>4$. It obtains the interval by intersecting the individual closed safe arcs containing one rational time. On any time interval of length $L$, a runner of relative speed $v>0$ blocks at most $(2/19)(L+1/v)$ units of time. This follows by splitting the interval into full periods and one remainder. Thus the union of the two blocked sets has length less than $L$ whenever

$$15L>2\left(\frac1{x-r}+\frac1{y-r}\right).$$

Our interval condition implies this for every $K\le x<y$. For $r=x$ or $y$, apply the [diameter-420 argument](NEWCOMER_DIAMETER_420.md) with $M=420$. Its explicit times avoid every integer fixed speed in $[0,M]$ simultaneously. Its duration estimate likewise uses only that all fixed phases lie in $[0,1/2]$ during the chosen time window. The same proof therefore permits a seventeenth fixed speed and provides clearance $1/18$ for each newcomer, exceeding $1/19$.

**2. The smaller speed is below $K$ and $y\ge19m$, with $m=\max(420,x)$.** For each eligible $x<K$, the verifier supplies a $1/18$ time for every $r\in F\cup\{x\}$. Each relative distance changes at a rate bounded by $m$. Around such a time there is a closed $1/19$-safe interval of radius $(1/18-1/19)/m$. Since $y-r\ge18m$, the relative phase traverses at least $2/19$ of a lap on the interval. An open blocking pass cannot contain the whole interval, even at equality. The added runner $y$ can use $1/(2y)$, when the fixed speeds and $x$ have travelled at most $m/(2y)$ of a lap and $y$ is half a lap from the start.

**3. The finite remainder, $x<K$ and $x<y<19m$.** There are 1,663 eligible values of $x$ and 26,929,083 eligible pairs. The verifier certifies all nineteen references, accounting for 511,652,577 reference–pair combinations.

For an old reference or reference $x$, the program first keeps rational times that clear its known opponents. At a retained time $p/q$, the remaining speed $y$ clears reference $r$ exactly when

$$19\min(a,q-a)\ge q,\qquad a=(y-r)p\bmod q.$$

The allowed residues repeat with period $q$. The program packs one period into bits, repeats it across the finite range, and removes the certified speeds from the outstanding set. It requires the latter to become empty. For reference $y$, it reverses the roles and covers the possible $x$ with the same residue test. If $17y\ge19(K-1)$, then $1/(2y)$ suffices for this role since all other speeds are at most $K-1$. The finite search uses reduced denominators at most 64 for the residue tests. Equalities count throughout. The reported role count includes this analytic shortcut and the batched residue checks.

## A region where all three added speeds are free

Start with $Q$ alone, of diameter $105$. Let $u<v<w$ be integers with $u\ge1680$, $v-u\ge420$, and $w-v\ge420$. Under those conditions, the following argument covers all nineteen runners.

For each $r\in Q$, reuse the interval computed for $r$ in the larger set $F$. The verifier checks $13(1680-r)L>6$. Summing the three blocked-time upper bounds shows that some of this interval survives, since $13L>2\sum_{z\in\{u,v,w\}}1/(z-r)$.

For a newcomer $R$, let $d_1,d_2$ be its two absolute speed differences from the other newcomers. During $0\le t\le T=1/(2\cdot105)$, every fixed phase is in $[0,1/2]$. A phase of $R$ in $[1/2+1/19,1-1/19]$, an arc of length $15/38$, clears every fixed opponent. A speed $z$ occupies an arc of length $\beta$ for between $\beta(T-1/z)$ and $\beta(T+1/z)$ units of time. Subtract upper bounds for the two blocking arcs of length $2/19$ from the lower bound for the favorable arc. The surviving time is at least

$$\frac1{38}\left(7T-\frac{15}{R}-\frac4{d_1}-\frac4{d_2}\right)\ge \frac1{38}\left(\frac7{210}-\frac{15}{1680}-\frac8{420}\right)=\frac3{21280}>0.$$

This gives a testable next question for the three-free-speed problem. How can a new reference escape its two fellow newcomers when one or both relative gaps are too small for the duration estimate? Triples having a smaller first speed also need coverage. A solution for every triple over $Q$ would still retain sixteen prescribed speeds.

## How an induction could finish the conjecture

Suppose every runner in an arbitrary $n$-runner configuration already has a $1/n$ time, with $n\ge2$. Normalize its smallest speed to zero and write $D$ for the largest. The argument in case 2 works for every $n$: the safe interval around an old time has radius $1/[n(n+1)D]$. For an added speed $z\ge(n+1)D$, its relative speed against each old runner is at least $nD$, enough to traverse $2/(n+1)$ across the interval. At $1/(2z)$ the new runner clears the old runners by at least $n/[2(n+1)]\ge1/(n+1)$. This is the fast-runner principle used in the working paper.

A sufficient induction step would allow an arbitrary distinct added speed, or show that every potential counterexample has a runner whose removal and reinsertion a proved rule covers. The fast-speed bound alone leaves configurations in which no runner is far faster than the rest. The two-addition result above handles unrestricted speeds for one fixed group. Finding an argument for arbitrary base groups and runner counts is a separate open task.

## Reproduction and checks

Run from the repository root with Python 3.10 or later. The [standalone verifier](verify_nineteen_two_additions.py) uses the standard library and requires no certificate download.

```sh
python experiments/forced-overlap/verify_nineteen_two_additions.py
```

Expected output:

```text
1,663 single-speed tails, 26,929,083 finite pairs, 511,652,577 finite roles.
Checked 17 fixed-reference intervals for x >= 1680.
```

The program also finds witnesses directly for each reference in eight two-addition controls, including $(481,482)$, $(1679,31900)$, $(1679,31901)$ and $(1680,1681)$, and for the three-addition control $(1680,2100,2520)$ over $Q$. These scalar checks use each runner's actual speed and avoid the packed speed sets. At $(1679,31900)$ the smallest clearance among these particular witnesses is exactly $1/19$.

The question and controls follow the [19-runner single-addition investigation](NINETEEN_FIXED_CORE.md) and the [shared working paper](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/890b2aa82c12cb9f255bb3a292620a25df0e0827/experiments/forced-overlap/paper/runner-additions/Fast_Runner_Extensions.pdf). This is an exploratory follow-up. AI assistance contributed the argument and verifier. Independent review of the mathematics, implementation, and relation to prior work remains open.
