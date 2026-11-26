# Testing the Two-Endpoint Fast-Runner Lemma on 17 runners

November 24, 2026. All runners start together on the unit circle. With one reference and sixteen other runners, the target distance is $1/17$. The [16-runner working paper](paper/Two_Endpoint_Fast_Runner.md) supplies the method. This supplement records a conditional transfer argument, a frozen experiment, and a computer-assisted proof candidate for an infinite family **with every runner taken as reference**. Independent review and literature priority remain open.

## Which part transfers?

Fix a reference and fifteen distinct positive relative speeds $C$. Let $V>\max C$ be the added speed. The method begins with a time at which $C$ is clear by at least $1/16$. The [fifteen-runner preprint](https://arxiv.org/abs/2609.02604v2) gives $1/15$ for fourteen moving speeds and a reference. It does not supply the extra runner in this premise. We record an explicit $1/16$ time for every tested core. Separately we record when the earlier 16-runner rule can establish that premise by deleting the largest core speed, using the preprint as its starting point.

For a closed $1/17$-safe component containing a $1/16$ witness, the clearance margin is $1/272$. If one speed $u$ bounds both ends, the width is $15/(17u)$, greater than the open blocking width $2/(17V)$. For distinct endpoint speeds $u,w$, the left and right times have the forms $a=(17i+1)/(17u)$ and $b=(17j-1)/(17w)$. Put $S=u+w$, $g=\gcd(u,w)$ and $D=17uw(b-a)$. The margin forces $D\ge S/16$ and the endpoint equations force $D+S\equiv0\bmod 17g$. The least compatible value is
$$D_0=17g\left\lceil\frac{S}{16g}\right\rceil-S.$$
Thus $V\ge\max_{u<w}2uw/D_0$ suffices. Before rounding, the corresponding cutoff is $32LM/(L+M)$ for the two largest core speeds $L,M$.

For each remaining $D=D_0+17g\ell$ with $\ell\ge0$ and $VD<2uw$, solve $uj-wi=(D+S)/17$ once. All placements of these endpoints differ by multiples of $1/g$. Under multiplication by $V$, their relative phases give multiples of $1/q$ modulo one, with $q=g/\gcd(g,V)$. Both ends fit in one open blocking pass precisely when an integer $k$ satisfies
$$q(Vb-1/17)<k<q(Va+1/17).$$
The converse for the two specified endpoint speeds uses $[a+1/(272u),b-1/(272w)]$, nonempty by the margin bound. Throughout this narrow interval both speeds remain in their original safe arcs. Reflection exchanges which speed bounds the left end. If no pair can trap a component, every component through a stronger witness yields a full time. A surviving pair leaves the full-core prediction undecided.

**Control.** On speeds $1,\ldots,15$, the component through $7/16$ is $[52/119,67/153]$. Speeds 7 and 9 set its endpoints. Speed 96 blocks this entire interval. At speed 126 the blocking width equals the component width and a safe endpoint survives. Adding 16 gives speeds $1,\ldots,16$ and exactly the sixteen nonzero seventeenths as full witness times. The pair test also agreed with a separate three-speed exact interval solver on **all 4,060 triples** $1\le u<w<V\le30$.

## Frozen comparison

The [protocol](SEVENTEEN_PROTOCOL.md) was committed [before execution](https://github.com/tradingartofwar/the-lonely-runner-conjecture/commit/76c4a3a52005798dd62d43b3de2724cea94d0e04). It tests all $M<V\le16M$ for each core. A short clock supplies a time of reduced denominator at most 17. The width and same-pass predictions certify every component through a stronger witness, assuming that witness exists. A direct short clock establishes existence at one time.

| Panel | Cores | Configurations | Width | Same pass | Short clock | Same pass, short clock missed |
|---|---:|---:|---:|---:|---:|---:|
| Dense | 136 | 34,425 | 5,237 | 29,328 | 25,734 | 7,135 |
| Sparse | 8 | 8,685 | 1,828 | 6,111 | 8,529 | 100 |
| Short-clock challenge | 8 | 8,580 | 2,819 | 6,638 | 0 | 6,638 |
| Controls | 2 | 2,115 | 1,609 | 2,015 | 2,108 | 7 |
| **Total** | **154** | **53,805** | **11,493** | **44,092** | **36,371** | **13,880** |

**OBSERVED.** All 154 cores had verified $1/16$ times. Forty-five also received a core certificate by applying the previous 16-runner same-pass rule, giving **11,141** two-step certifications among the 44,092. For every same-pass prediction we recovered and checked a witness in every stronger-witness component, giving 1,440,025 component checks. Direct computations recovered a witness for the selected reference in all 53,805 configurations, including all 3,554 missed by both the same-pass and short-clock tests. The archived 16-runner study replayed byte-for-byte after parameterizing the code.

The challenge cores contain speeds 11, 13, 16, 17, 60, 63, and 70. Every denominator through 17 divides one of these speeds, so the corresponding runner returns to the reference at every time on that clock. For seed zero with added speed 84, the same-pass test succeeds where width and short clocks fail. An exact witness is $1/187$; speed 11 is exactly $1/17$ from the reference.

**Changing the reference changes the experiment.** On the eight sparse and eight challenge cores, we also tested $V=M+1$ and $V=2M$, taking every physical runner as reference in turn. Signs and duplicate absolute differences were folded for the predictor. Witnesses were checked on the original signed differences at $1/17$. The same-pass test certified **47 of 544** roles, with no group certified in all 17 roles by this rule alone. The exact solver supplied the rest, so **32 of 32 groups** were verified for all runners. On these same 32 groups the zero reference alone was predicted in 5 cases. These groups emphasize moderately sized added speeds; their coverage is not directly comparable with the full $M<V\le16M$ panel.

## A fixed core with any added positive integer speed

**Computer-assisted proof candidate.** Take these sixteen fixed physical speeds,
$$P=\{0,11,13,16,17,20,28,38,39,42,43,52,56,60,63,70\}.$$
For **every** positive integer $V\notin P$, every runner in $P\cup\{V\}$ has a time at which its distance from every other runner is at least $1/17$. Different runners may use different times. This is the seed-zero challenge core. We [fixed the family and verification rules](SEVENTEEN_FAMILY_PROTOCOL.md) after the panel comparison and [before checking this all-reference extension](https://github.com/tradingartofwar/the-lonely-runner-conjecture/commit/1bbfada804fc85f5e0bccd7662fcf1616d6711d9).

1. **Each old runner.** For each $r\in P$, the [certificate](seventeen_family_results.json) gives an exact $1/16$ time for the fifteen fixed opponents and a closed interval $[a_r,b_r]$ about this time throughout which they remain $1/17$ clear. One can verify the whole interval using only its endpoints: for each $u=|s-r|>0$, check that $[ua_r,ub_r]$ is contained in one interval $[k+1/17,k+16/17]$. The endpoint-width cutoff, maximized over the reference roles and including the requirement that $V-r$ be fastest, gives $V\ge964$. There is also a shorter independent tail check using the recorded interval widths directly. For each $r$ it suffices that $(V-r)(b_r-a_r)\ge2/17$ and $V>70$. The maximum of the resulting integer cutoffs is **391**. The added speed's open blocking pass cannot cover the certified closed interval.
2. **The new runner.** For $V>70$ take $t=1/(2V-70)$. Its relative phases against the fixed runners range from $(V-70)/(2V-70)$ through $V/(2V-70)$, symmetrically about $1/2$. All distances are at least $1/17$ whenever $15V\ge16\cdot70$, in particular for the whole tail above.
3. **Finite remainder and overlap.** Following the frozen cutoff, the [CSV](seventeen_family_witnesses.csv) records one exact time per reference for each of the **948** admissible integers $1\le V<964$, giving **16,116** verified role–speed pairs. This includes speeds inserted among the fixed runners. With the direct tail check, only the 375 admissible additions below 391 are needed. Positive integers coinciding with a fixed speed are excluded.

The [standalone checker](verify_seventeen_family.py) uses only Python's standard library and the JSON and CSV certificates. It checks all finite witnesses, each old runner's safe interval, and the sufficient infinite-tail cutoff. Thus this particular family's certificate can be reviewed without relying on an unrestricted 16-runner theorem, the same-pass implementation, or the code that generated the certificate. The finite panels and this fixed-core infinite family leave arbitrary 17-runner configurations open.

## Reproduction

Run these commands from the repository root with Python 3.11 or later. The family checker must run with Python assertions enabled.

~~~sh
python experiments/forced-overlap/verify_seventeen_family.py
PYTHONPATH=. python experiments/forced-overlap/seventeen_family.py --speed 84
PYTHONPATH=. python experiments/forced-overlap/seventeen_study.py
PYTHONPATH=. python experiments/forced-overlap/endpoint_pairs.py 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 --runners 17 --fastest 126 --core-time 7/16 --same-pass --witness
~~~

[Panel ledger, stronger core times and all-reference witnesses](seventeen_results.json) · [Study implementation](seventeen_study.py) · [Family construction](seventeen_family.py)

Vance asked whether the 16-runner result transfers. AI assisted with the conditional derivation, implementation and certificate checking. The short-clock challenge is deliberately selected to test complementary coverage. Its success rate is not a population estimate.
