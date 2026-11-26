# Transferring the eighteen-runner proof to a different core

November 24, 2026. Computer-assisted proof candidate. The [protocol](EIGHTEEN_TRANSFER_PROTOCOL.md) fixed the new core, the negative control and the pass conditions before execution. The old core was irregular and spanned 70 speed units. The new one consists of fifteen consecutive integers and a single outlier. The outlier was deliberately chosen by hand to challenge the previous clock.

## Result

Let $Q=\{0,1,\ldots,14,105\}$. For **every** pair of distinct positive integer speeds $x<y$ outside $Q$, each runner in $Q\cup\{x,y\}$ has a time with circular distance at least $1/18$ from each of its seventeen opponents. Runners start together and different runners may use different times. This is a second sixteen-speed core for which the [two-addition result](EIGHTEEN_RESULTS.md) holds.

| What was checked | First core | New core, frozen test |
| --- | ---: | ---: |
| Fixed speed diameter $M$ | 70 | 105 |
| Start of the region covered directly for both additions | 420 | 630 |
| Speed gap at which the duration bound takes over | 120 | 180 |
| Smaller admissible values of $x$ with an individually checked tail in $y$ | 404 | 614 |
| Remaining finite pairs | 16,566 | 30,386 |
| Exact reference–pair checks | 298,188 | 546,948 |

Every row in the certificate passed. Independent interval intersection also found times for all 18 roles at the control and at selected boundaries, including $(15,16)$, $(419,420)$, $(420,480)$, $(420,700)$, $(420,701)$, $(629,630)$, $(630,809)$ and $(630,810)$.

## A clock that actually failed

Take $x=420$, $y=480$ and use runner $R=420$ as reference. The speed gap is $d=60$. The first denominator among $2,\ldots,7$ that does not divide 60 is $q=7$. The previous core's clock gives
$$t_0=\frac1q+\frac{1}{2qR}=\frac{841}{5880}.$$
The nearest runner is the outlier at speed 105. Its distance is $3/56$, which falls short of $1/18$ by exactly $1/504$. This is a counterexample to reusing that clock with the first core's numerical cutoff. The frozen protocol covers the pair through the smaller-$x$ argument. An explicit alternative time for the very same reference is given below.

## What carried over without changing the argument

Write $\delta=1/18$. For a fixed runner $r$, let $I_r$ be a closed interval throughout which it clears the other fixed runners, and write $L_r$ for its length. On that interval a newcomer with relative speed $z$ can block at most $(L_r+1/z)/9$ of the time. This follows by counting whole periods and bounding the last partial period. Both newcomers therefore leave some time safe if $7(K-r)L_r>2$ and $y>x\ge K$. For the new core, the stored intervals already meet those sixteen inequalities at $K=140$. The old core's corresponding cutoff was 111. This part depends on the speeds inside the core.

For a new reference $R=x$ or $y$, all the fixed runners stay in $[0,1/2]$ on $0\le t\le1/(2M)$. When the phase of $R$ lies in $[1/2+\delta,1-\delta]$ it clears all of them. Relative speed $d=y-x$ blocks only part of that time. The duration left is at least
$$\frac1{18}\left(\frac{5}{2M}-\frac7R-\frac2d\right).$$
It is positive for $R\ge6M$ and $d\ge\lceil12M/7\rceil$. For smaller $d$ on this core, the old time $1/q+1/(2qR)$ works with the rescaled cutoff $R\ge630$. For $q\le7$ not dividing $d$, fixed opponents are clear by at least $(1-M/R)/(2q)$ and the other added runner by at least $\|d/q\|-d/(2qR)$. The checker verifies both inequalities for all $1\le d<180$. Here $\|z\|$ denotes distance to the nearest integer. The same two new-reference bounds apply to any integer core of diameter $M\le245$ when $R\ge6M$ and both additions are in that range. Then $d<\lceil12M/7\rceil$ implies $d\le419$, so a suitable $q$ exists. In this smaller-gap case the two margins are at least $5/84$ and $6/49$, respectively.

For each of the 614 smaller $x$, the generator found a positive-width safe interval for every runner in $Q\cup\{x\}$ at $1/18$. This core needed no prior seventeen-runner witness ledger. Let the resulting threshold be $B_x$ and $m=\max(105,x)$. The checker verifies $B_x>m$, $16B_x\ge17m$, and $(B_x-r)L_{x,r}\ge1/9$ for each role. For every $y\ge B_x$, one open blocking pass of $y-r$ is too short to cover the closed interval. Runner $y$ itself can use $1/(2y-m)$. The $B_x$ range from 119 to 709. For every remaining $x<y<B_x$ outside $Q$, the verifier recovers an exact rational time for each reference and checks all seventeen signed distances. This completes the case split.

## A stronger clock obtained from the failure

At $t=1/q$, the phase difference between $R$ and any integer fixed speed $p$ is a multiple of $1/q$. Move forward in time by $\varepsilon$. The relative displacement is $(R-p)\varepsilon$, so it lies between $(R-M)\varepsilon$ and $R\varepsilon$. To stay clear of every grid point, balance the two margins
$$ (R-M)\varepsilon=\frac1q-R\varepsilon,\qquad
\varepsilon=\frac{1}{q(2R-M)}.$$
At $t=1/q+\varepsilon$, every fixed opponent is at distance at least $(R-M)/[q(2R-M)]$. The other added runner is at distance at least $\|d/q\|-d/[q(2R-M)]$. For the failed control this gives $t=736/5145$, with exact minimum distance **$3/49>1/18$**. This refinement was derived after the primary protocol was fixed. The primary result in the table used the original clock and the scaled constants.

**Transferable bound.** For any sixteen integer fixed speeds in $[0,M]$ containing $0,M$, with $M\le157$, the following argument covers **both new reference roles** whenever $y>x\ge4M$. For $d>\lfloor8M/3\rfloor$, the duration estimate is positive since $5/(2M)-7/(4M)=3/(4M)$. Otherwise $d\le419$ and some $q\in\{2,\ldots,7\}$ does not divide $d$, because their least common multiple is 420. For the balanced time, the fixed-opponent margin is at least $3/49$, and the margin against the other newcomer is at least $(1-8/21)/7=13/147$. Both exceed $1/18$. The original sixteen reference roles also follow whenever supplied intervals meet $7(4M-r)L_r>2$. Extending to every smaller $x$ still requires the seventeen intervals and finite checks in the preceding section.

For this new core the checker verifies those interval inequalities and both balanced-clock bounds with **$K=420$ and gap boundary 281**. Thus only 404 smaller $x$ and 16,501 finite pairs are necessary with the refinement. The archived run checks all 30,386 pairs prescribed by the primary protocol.

The boundary of this particular uniform bound is concrete. At $M=158$, $R=4M=632$, $d=420$, all six denominators divide the gap, and the quantity in parentheses in the duration estimate is $-1/66360$. This exposes a gap in the $4M$ argument. The larger $6M$ cutoff above still applies to diameter 158 once both added speeds reach it. The unrestricted eighteen-runner problem and independent mathematical review of these proof candidates remain open.

## Reproduction

From the repository root with Python 3.11 or later, leave assertions enabled. The [verifier](verify_eighteen_family.py) reads the [compressed certificate](eighteen_transfer.json.xz) using only the standard library. Its interval and modular-distance checks are independent of the generator.

~~~sh
python experiments/forced-overlap/verify_eighteen_family.py --transfer
python experiments/forced-overlap/verify_eighteen_family.py
PYTHONPATH=. python experiments/forced-overlap/eighteen_family.py --transfer --out /tmp/eighteen_transfer.json.xz
cmp /tmp/eighteen_transfer.json.xz experiments/forced-overlap/eighteen_transfer.json.xz
~~~

The first core's certificate still regenerates byte-for-byte. Its 298,188 finite checks and the repository's 25 unit tests passed again.
