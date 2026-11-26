# Eighteen runners with two independently variable speeds

November 24, 2026. Computer-assisted proof candidate for independent review. The [protocol](EIGHTEEN_PROTOCOL.md) fixed the sixteen speeds, the two-variable domain, the controls, and the failure criteria before execution.

## Claim

Take the fixed physical speeds

$$P=\{0,11,13,16,17,20,28,38,39,42,43,52,56,60,63,70\}.$$

For every pair of distinct positive integers $x<y$ outside $P$, each of the eighteen runners with speeds in $P\cup\{x,y\}$ has a time at which it is at least $1/18$ of a lap from each of the other seventeen. Runners start together on a unit circle. Different reference runners can use different times. Either added speed can fall between fixed speeds, and both are unbounded. The [seventeen-runner result](SEVENTEEN_RESULTS.md) treated just one arbitrary added speed.

Write $\delta=1/18$ and $\|z\|$ for distance to the nearest integer. The target for reference $r$ is $\|(s-r)t\|\ge\delta$ for all opponents $s$. The certificate and verifier use exact arithmetic throughout. The particular set $P$ is a hypothesis of the claim.

## Both additions at least 420

**A fixed runner as reference.** For each $r\in P$ the certificate supplies a closed interval $I_r$ of length $L_r$ on which all fixed opponents are clear. For each $s\ne r$ the checker verifies that the image $|s-r|I_r$ lies in a single interval $[k+\delta,k+1-\delta]$. It also checks $7L_r(420-r)>2$.

On a time interval of length $L$, the duration spent in a phase band of fractional length $\beta$ by speed $z>0$ lies between $\beta(L-1/z)$ and $\beta(L+1/z)$. Split the interval into whole periods of length $1/z$ and one remaining piece. That piece can contribute at most the band's duration in one period. The same estimate applies if the band crosses phase zero. Each new opponent therefore blocks at most $(L_r+1/|s-r|)/9$ on $I_r$. The time left clear by both has length at least
$$\frac{7L_r-1/(x-r)-1/(y-r)}9>0.$$

**An added runner as reference, gap $d=y-x\ge120$.** Write $R=x$ or $y$. During $0\le t\le1/140$, every fixed speed has phase in $[0,1/2]$. If the phase of $R$ is in $[1/2+\delta,1-\delta]$, it clears the whole fixed group. That band has length $7/18$. The other new runner blocks for a fraction $2/18$ of each relative period. On the time interval of length $L=1/140$, the preceding estimates leave at least
$$\frac{5L-7/R-2/d}{18}\ \ge\ \frac{1}{7560}>0.$$
In particular, the boundary values $R=420$ and $d=120$ are covered.

**An added runner as reference, gap $1\le d\le119$.** Choose $q\in\{2,3,4,5,6,7\}$ that does not divide $d$. Such a choice exists since their least common multiple is 420. Put
$$t=\frac1q+\frac{1}{2qR}.$$
At that time $R$ is halfway between consecutive multiples of $1/q$. A fixed speed $p$ has moved by at most $70/(2qR)$ from the grid point $p/q$. The circular distance from $R$ to each fixed runner is at least $(1-70/R)/(2q)\ge5/84>1/18$. Its distance to the other added runner is at least
$$\|d/q\|-\frac{d}{2qR}\ \ge\ \frac{1-119/840}{7}>\frac1{18}.$$
For example, the pair $420,421$ can use $q=2$. Their respective times are $841/1680$ and $843/1684$, at which their exact nearest-opponent distances are $5/24$ and $179/842$.

## The smaller addition below 420

There are 404 choices of $1\le x<420$ outside $P$. For each $x$ the certificate supplies a threshold $B_x$ and, for each $r\in P\cup\{x\}$, a closed interval safe for its sixteen opponents in that group. The generator uses [last round's witnesses](seventeen_family_witnesses.csv) to locate positive-width intervals. The standalone verifier checks the intervals directly against the physical speeds.

* **Every $y\ge B_x$.** Write $m=\max(70,x)$. The checker verifies $B_x>m$, $16B_x\ge17m$, and $(B_x-r)L_{x,r}\ge1/9$ for the first stored interval of each old reference. A single open blocking pass of relative speed $y-r$ has length $1/[9(y-r)]$, so it cannot contain the entire closed interval. Equality suffices. For reference $y$, take $t=1/(2y-m)$. Its relative phases against the other seventeen run from $(y-m)/(2y-m)$ to $y/(2y-m)$, placing them in $[\delta,1-\delta]$.
* **Every $x<y<B_x$ outside $P$.** There are 16,566 pairs in total. For each old reference the checker finds the intersection of one stored interval with a closed safe band of $|y-r|$. For the new reference it uses the same explicit time when applicable, or an individually recorded rational time. In all eighteen roles it checks the signed modular distance to all seventeen opponents directly. This gives 298,188 exact role checks. The thresholds range from 86 to 511.

The large region, these 404 unbounded ranges in $y$, and the 16,566 finite pairs exhaust the claim. The verifier needs only Python's standard library and the [compressed JSON certificate](eighteen_family.json.xz). It does not need the generator or the seventeen-runner data.

## How often did the two-endpoint test itself succeed?

The family proof above combines several arguments. To measure the endpoint test separately, we used sixteen fresh cores with a **specified stationary reference** and sixteen fixed relative speeds. For each core, a rational $1/17$ witness was found and checked before testing every integer added speed $M<V\le17M$, with $M$ the core maximum. The width test asks whether one blocking pass is too short to swallow the interval. The same-pass test also uses the positions of both endpoints. A short clock is a reduced rational time with denominator at most 18.

| Fresh panel | Configurations | Width test | Same-pass test, including width | Short clock | Verified lonely time |
| --- | ---: | ---: | ---: | ---: | ---: |
| Eight sparse cores | 10,016 | 2,045 | 6,933 | 9,713 | 10,016 |
| Eight cores designed to block short clocks | 11,744 | 2,187 | 7,056 | 0 | 11,744 |
| Total | 21,760 | 4,232 | 13,989 | 9,713 | 21,760 |

The endpoint positions added 9,757 certificates beyond width alone. There were 4,810 configurations where neither the same-pass test nor a short clock supplied the witness. Searching verified core intervals found a time in every such case. For one challenge core with $M=90$, the same-pass test was inconclusive at $V=91$ and succeeded at $V=260$. The time $19/1080$ works for both. All 16 cores had the stronger time needed to apply the lemma, but chaining two successive same-pass deductions certified none of these panel configurations. These finite panel counts concern a single specified reference.

The pair test agreed with exact interval intersection on all 4,060 triples $1\le u<w<V\le30$. On the tight control with relative speeds $1,\ldots,17$, the complete safe set consists of the six isolated times $a/18$ for $a=1,5,7,11,13,17$. This tests exact equality at the conjectured distance.

## Review and reproduction

From the repository root with Python 3.11 or later, run the following commands with assertions enabled.

~~~sh
python experiments/forced-overlap/verify_eighteen_family.py
PYTHONPATH=. python experiments/forced-overlap/eighteen_study.py > /tmp/eighteen_results.json
cmp /tmp/eighteen_results.json experiments/forced-overlap/eighteen_results.json
PYTHONPATH=. python experiments/forced-overlap/eighteen_family.py --out /tmp/eighteen_family.json.xz
cmp /tmp/eighteen_family.json.xz experiments/forced-overlap/eighteen_family.json.xz
~~~

The [standalone verifier](verify_eighteen_family.py) validates every finite witness, each stored interval, and the inequalities in both infinite regions. The [panel output](eighteen_results.json) records the exact cores, counts, and examples. Independent mathematical review and literature priority are open. A transfer test would replace the fixed sixteen speeds with a different group chosen before the run and determine which interval widths and gap bounds still suffice.
