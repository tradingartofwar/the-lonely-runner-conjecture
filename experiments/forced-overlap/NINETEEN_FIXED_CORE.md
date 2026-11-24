# Nineteen runners with one freely chosen speed

**November 24, 2026 · HYPOTHESIS (computer-assisted proof candidate).** Fix the eighteen speeds $B=\{0,1,\ldots,14,105,420,480\}$. For every positive integer $z\notin B$, every runner in $B\cup\{z\}$ has a time at distance at least $1/19$ from all eighteen opponents. Times may differ by runner. The choices 420 and 480 come from the [second core's clock-failure control](EIGHTEEN_TRANSFER.md). They are fixed throughout this argument.

## All speeds from 9,120 onward

Write $D=480$. For each runner $r\in B$, there is a time $t_r=1/q_r$ giving clearance at least $1/18$ from the other seventeen. In increasing speed order the denominators are

$$17,14,13,12,11,11,10,8,9,10,11,12,14,14,15,18,25,21.$$

Each of these certificates is checked directly. Put $h=1/18-1/19=1/342$. For $|t-t_r|\le h/D$, the change in each old relative distance is at most $D|t-t_r|$. Thus this whole closed interval is safe for $r$ against $B$ at clearance $1/19$.

If $z\ge19D=9120$, the speed relative to $r$ is at least $18D$. It traverses at least $(18D)(2h/D)=2/19$ of a lap during the interval. A single open blocking arc has length $2/19$, so it cannot cover the entire closed interval, including at equality. One time in that interval clears all opponents. The added runner itself uses $t=1/(2z)$, when every old runner is at most $D/(2z)$ of a lap from the start and the added runner is at half a lap. This finishes the unbounded range. The interval argument is the fast-runner principle of Kravitz, Proposition 6.1 ([2021 paper](https://doi.org/10.5070/C61055383)).

## Exact checks below 9,120

There are 9,119 positive speeds below the cutoff, of which 17 already belong to $B$. For each of the remaining 9,102 speeds the checker finds a rational time for each of the nineteen runners. It rechecks the time against every opponent. At time $p/q$ with relative speed $v$, put $a=p|v|\bmod q$. The check $19\min(a,q-a)\ge q$ includes equality. All **172,938 runner checks** passed.

For old references the checker searches reduced fractions up to denominator 40. For the added runner it uses the same search or the explicit time $1/(2z)$ when $17z\ge19D$. Every required time was found. This finite search was designed specifically for this fixed core.

From the repository root, run with Python 3.10 or later:

```sh
python experiments/forced-overlap/verify_nineteen_fixed_core.py
```

A simple control shows why new times can be necessary. With $z=17$, runner zero's original time $1/17$ gives a collision. At $1/19$ it clears every opponent because none of their speeds is divisible by 19.

## What remains open

This fixes eighteen speeds and frees one. The stronger question prompted by the working paper is whether, starting with a specified sixteen-speed core $P$ or $Q$, all nineteen runners have a lonely time for **every triple** of distinct positive added integer speeds outside that core. Here only the slice $Q\cup\{420,480,z\}$ is exhausted. The general conjecture also allows the sixteen-speed core itself to vary.

The argument and finite verifier were developed with AI assistance. Independent mathematical review and comparison with prior results remain open.
