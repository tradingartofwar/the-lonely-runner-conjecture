# When a Fast Runner Can Block Both Endpoints

*Lonely Runner Project · Working paper for independent review · November 24, 2026*

**Abstract.** Fix a stationary runner and fourteen distinct positive integer speeds. At the target clearance of one sixteenth of a lap, consider an interval containing a time at which all fourteen have clearance one fifteenth. We give an integer test for whether two specified endpoint runners can bound such an interval inside a single blocking pass of a faster runner. If every pair fails the test, each such interval contains a time safe for all fifteen moving runners. On a pre-specified holdout, the test certified 5,397 of 7,602 configurations. A direct search of small denominators found witnesses in 7,474, missing 80 that the endpoint test certified. The proof and its relation to prior work are offered for review.

## 1. From clearance to endpoint widths

All runners start together on a unit circle. Write $\|x\|$ for distance to the nearest integer. Let $C$ be the fourteen moving speeds, $V>\max C$ an integer, $\delta=1/16$ and $\sigma=1/15$. A **strong component** is a closed component of the set of times safe for $C$ at $\delta$ that contains a time $t_0$ safe for $C$ at $\sigma$. Work on the real time axis and identify times differing by one. Allikvere's fifteen-runner result supplies such a time [[1]](#references).

The initial bound $V\ge15\max C$ is a direct specialization of Kravitz, Proposition 6.1, using $L=\sigma$ and $\varepsilon=\sigma-\delta=1/240$. Kravitz also tracks active left and right speeds and fastest-runner residues near equality times in Lemmas 6.4 and 6.9 [[2]](#references). Here the local question concerns both endpoints of a component at a fixed threshold. Priority for the following formulation is open.

**Two-Endpoint Fast-Runner Lemma (proof candidate).** Let $L<M$ be the two largest speeds in $C$. Every strong component contains a time safe for $C\cup\{V\}$ whenever $V\ge30LM/(L+M)$.

*Proof.* Let $[a,b]$ be such a component. A runner of speed $u$ needs at least $1/(240u)$ time to spend the clearance available at $t_0$. If distinct speeds $u,w$ determine the left and right endpoints, then
$$b-a\ge \frac{1}{240}\left(\frac1u+\frac1w\right)\ge\frac{1}{240}\left(\frac1L+\frac1M\right).$$
If the same speed $u$ determines both ends, this component has width $7/(8u)$. In either case the stated cutoff makes the component at least as wide as the open blocking interval of $V$, of width $1/(8V)$. A closed interval of equal length already contains a safe endpoint. $\square$

**Integer widths.** For different endpoint speeds, their phases enter and leave the safe arc at $1/16$ and $15/16$. Hence $a=(16i+1)/(16u)$ and $b=(16j-1)/(16w)$. Put $S=u+w$, $g=\gcd(u,w)$ and $D=16uw(b-a)$. The endpoint equations give $D+S=16(uj-wi)$ and the clearance bound gives $D\ge S/15$. The least compatible width in these units is
$$D_0=16g\left\lceil\frac{S}{15g}\right\rceil-S.$$
Thus $V\ge\max_{u<w}2uw/D_0$ suffices. The maximum is over the 91 pairs in $C$, with $D_0$ computed separately for each pair.

## 2. Can one pass cover both ends?

An interval can be narrow enough to fit a blocking pass, yet sit in the wrong place on the track clock. The test below accounts for every placement consistent with the two endpoint speeds.

**Proposition (proof candidate).** Fix $u<w<V$. Consider each $D=D_0+16g\ell$ with $\ell$ a nonnegative integer and $VD<2uw$. Choose one integer solution of
$$uj-wi=(D+S)/16,$$
and form $a=(16i+1)/(16u)$ and $b=(16j-1)/(16w)$. Write $q=g/\gcd(g,V)$. A strong component for the pair $u,w$ can be wholly blocked by $V$ if and only if, for at least one of these widths, the following open interval contains an integer:
$$q(Vb-1/16)<k<q(Va+1/16).$$

*Proof.* If $V$ blocks the component, its endpoints must be set by different speeds, by the same-speed argument on page 1. Reflection $t\mapsto1-t$ exchanges their roles, so it suffices to have $u$ on the left. Its width $b-a$ must be strictly less than $1/(8V)$, which gives the upper bound on $D$. Integer solutions exist for each listed width because $16g$ divides $D+S$. They give all endpoint placements by translating $a$ and $b$ together by $h/g$ for integers $h$.

After multiplication by $V$, these translations give the subgroup of multiples of $1/q$ modulo one. To trap a placement there must be one integer pass center strictly between its right endpoint phase minus $1/16$ and its left endpoint phase plus $1/16$. As the placements vary, the possible centers relative to the original placement are precisely the multiples of $1/q$. Multiplying the inequalities by $q$ gives the test. If an endpoint meets the boundary of a pass, that endpoint survives.

Conversely, a listed width satisfying the test gives such a common pass. Since $b-a<1/(8V)$, neither endpoint runner reaches the opposite end of its own safe arc on $[a,b]$. A time in
$$[a+1/(240u),\ b-1/(240w)]$$
meets the stronger threshold for both runners. This interval is nonempty by $D\ge S/15$. Outside $a$ on the left, speed $u$ blocks immediately, and outside $b$ on the right, speed $w$ blocks immediately. Thus $[a,b]$ is an actual strong component of the two-speed system. $\square$

**Consequence for fourteen speeds.** A trapped full-core strong component would also be a trapped component for its two endpoint runners alone. Rejecting all 91 pairs therefore certifies every strong component. An accepted pair may occur at times when another retained runner blocks. A surviving pair alone cannot decide the full configuration.

**A trap and a successful prediction.** For $u=7$, $w=8$, the interval $[97/112,111/128]$ contains $13/15$. Speed 90 traps it in the pass about lap 78, while speed 112 has blocking width exactly equal to the interval length and cannot trap it. With the full core $1,\ldots,14$ and speed 90 a different time, $1/16$, works. For a positive example missed by the width rule, take $C=\{1,\ldots,11,13,14,15\}$ and $V=48$. The pass test rejects every pair. The time $15/176$ works, and every denominator at most 16 fails.

## 3. Evidence and limits

The rule, panels, comparison and failure conditions were fixed in the [experiment protocol](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/1650a626e59cbb0dd3844b5ad43a6a8c28778610/experiments/forced-overlap/SAME_PASS_PROTOCOL.md). Each core was tested on all integer $V$ from $M+1$ through $15M$. The first three panels reuse the prior width study. Eight newly specified cores form the holdout. As a separate existence test, the short-clock benchmark checks every reduced rational time of denominator at most 16 up to reflection.

| Panel | Configurations | Width | Same pass | Short clocks | Same pass only* |
|:---|---:|---:|---:|---:|---:|
| Dense | 26,656 | 4,333 | 22,437 | 19,131 | 6,001 |
| Previously fixed controls | 980 | 478 | 880 | 980 | 0 |
| Previous sparse cores | 9,128 | 2,841 | 6,332 | 8,818 | 190 |
| Fresh holdout | 7,602 | 1,941 | 5,397 | 7,474 | 80 |
| **Total** | **44,366** | **9,593** | **35,046** | **36,403** | **6,271** |

\* Certified by the same-pass rule and missed by the short-clock benchmark. The width and same-pass rules certify every strong component. A short clock supplies one time for the full tuple. The panels measure coverage under these particular input choices.

The pair test agreed with a separate exact interval solver on all 3,276 integer triples $1\le u<w<V\le28$. For every same-pass certification we recovered an exact time in every full-core strong component and checked it on all fifteen moving speeds, giving 1,237,973 component checks. On the fresh holdout, the phase test added 3,456 certifications over width alone. Of the 80 holdout configurations that same-pass certified and short clocks missed, 46 were also missed by width alone. Both the pass test and the short-clock benchmark left 48 holdout configurations undecided.

**Scope and review priorities.** The 16-runner conjecture for arbitrary speeds remains open in this work. The certificate is a sufficient test for the full core and an exact trap test for two specified endpoint speeds. Review should first check the converse of the proposition, the treatment of equality and reflection, and whether the endpoint-width rounding or pass criterion follows from an existing fast-runner result. Those questions now carry more weight than increasing the sample size.

### References

[1] Jaan Allikvere, [*Fourteen and fifteen lonely runners*](https://arxiv.org/abs/2609.02604v2), arXiv:2609.02604, version 2, September 2026.

[2] Noah Kravitz, [*Barely lonely runners and very lonely runners: a refined approach to the Lonely Runner Problem*](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf), *Combinatorial Theory* 1 (2021), paper 17, §6.

**Reproduction.** From the repository root run
~~~sh
PYTHONPATH=. python experiments/forced-overlap/same_pass_study.py
~~~
The archived numerical output accompanies the program. The repository identifies the earlier width experiment and its frozen inputs. Vance directed this investigation into common blocking times and the use of the lemma as a research tool. The AI collaborator assisted with derivation, code and drafting. Independent mathematical review and publication priority remain open.
