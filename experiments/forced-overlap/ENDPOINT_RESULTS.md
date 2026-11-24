# Endpoint congruences for the Two-Endpoint Fast-Runner Lemma

November 24, 2026. **Proof candidate.** Fourteen distinct positive integer speeds form the retained core. The stationary reference starts with every runner. Given a fifteenth moving speed $V$ greater than all fourteen, the goal is a common distance of at least $1/16$. The [original lemma](../../notes/Lonely_Runner_Forced_Overlap_Handoff_2026-11-24.md#two-endpoint-fast-runner-lemma) uses the $1/15$ guarantee for the retained core from [Allikvere, version 2](https://arxiv.org/abs/2609.02604v2). The code below assumes that mathematical input for its prediction. An explicit witness can separately be checked directly on all fifteen speeds.

## Which widths can the endpoints actually have?

Take a closed safe component $[a,b]$ at threshold $1/16$ containing a time $t_0$ at which the retained speeds have clearance $1/15$. If the same runner sets both ends, the component has width $7/(8u)$, already greater than the blocking width $1/(8V)$. Otherwise let $u$ set the left end and $w$ the right. A positive speed enters its safe arc just as its phase crosses $1/16$, and exits as its phase crosses $15/16$. For integers $i,j$ this gives
$$
a=(16i+1)/(16u),\qquad b=(16j-1)/(16w).
$$
The component contains $t_0$ with positive slack, so endpoint ties cause no ambiguity in these signs. Put $S=u+w$, $g=\gcd(u,w)$ and $D=16uw(b-a)$. Then
$$
D=16(uj-wi)-S,\qquad D+S\equiv0\pmod{16g}.
$$
The earlier endpoint argument gives $b-a\ge(1/u+1/w)/240$, or $D\ge S/15$. The smallest value consistent with both restrictions is
$$
D_{u,w}=16g\left\lceil\frac{S}{15g}\right\rceil-S.
$$
It may exceed the earlier width estimate. The formula is symmetric in $u,w$, so the implementation needs only 91 unordered pairs. A sufficient cutoff for every strong-witness component to contain a full witness is
$$
V\ \ge\ \max_{u<w}\frac{2uw}{D_{u,w}}.
$$
Indeed, each such component is then at least as wide as an open blocking interval of $V$. Equality counts. Below the cutoff the code returns the pairs whose width bound still permits a trap. Actual trapping also requires the rest of the core to remain safe and $V$ to block the entire interval at that position.

**Exactly when the cutoff improves.** Write $L<M$ for the two largest core speeds. The refined *rational cutoff* is strictly smaller than $30LM/(L+M)$ exactly when $(L+M)/\gcd(L,M)$ is not a multiple of 15. For a pair $u,w$, rounding gives equality in the old estimate precisely when $15g$ divides $u+w$. And $30uw/(u+w)$ strictly increases with either positive argument, giving a unique maximizing pair $L,M$ for the original estimate. If that pair rounds upward in width, every refined pair cutoff lies strictly below the old maximum. A smaller rational cutoff can still have the same integer ceiling.

## Controls that distinguish the mechanisms

- **A successful improvement.** For $1,\ldots,13,26$, the old cutoff is 260. The refined cutoff is 112, set by speeds 7 and 8. For example, add $V=240$. Both $1/15$ and $1/16$ put 240 at the reference. The tool returns $241/3840$, where speed 240 reaches exactly $1/16$. All fourteen core speeds also pass a direct distance check.
- **An unchanged cutoff.** Replacing 26 with 17 gives 221 under both rules. The top pair $13,17$ has normalized sum 30.
- **A real trap.** With core $1,\ldots,14$, the component through $13/15$ runs from $97/112$ to $111/128$, with endpoint runners 7 and 8. Its width is exactly $1/896$, attaining the rounded pair bound. Speed 90 blocks this entire interval, yet $1/16$ is a full witness elsewhere. The same core's component through $1/15$ reproduces the handoff controls for added speeds 15 and 210.

## Frozen comparison

The [protocol](ENDPOINT_PROTOCOL.md) was committed [before running the study](https://github.com/tradingartofwar/the-lonely-runner-conjecture/commit/abb64f4263489381c805fc2af4fc705ae27623e0). The inputs use every integer fastest speed $M<V\le15M$ for each specified core.

| Panel | Cores | Tuples | Original lemma certifies | Refined rule certifies | Additional |
|---|---:|---:|---:|---:|---:|
| All 14-speed subsets of 1 through 16 | 120 | 26,656 | 1,103 | 4,333 | 3,230 |
| Three prescribed controls | 3 | 980 | 182 | 478 | 296 |
| Eight deterministic sparse cores | 8 | 9,128 | 362 | 2,841 | 2,479 |
| **Total** | **131** | **36,764** | **1,647** | **7,652** | **6,005** |

**OBSERVED.** Fourteen of the 131 cores gained no additional integer speeds in their panel. The rule left 29,112 tuples unresolved. These are coverage counts for two sufficient tests on the specified inputs.

The study computed each core's exact safe components containing a stronger witness. It checked 1,147,146 component–speed combinations. For every arithmetic certification it recovered a valid physical time in every such component and checked all fifteen distances. At five specified speeds per core it independently compared component survival with the full tuple's exact closed intervals. Separately, direct enumeration of boundary differences for all 276 pairs with $1\le u<w\le24$ agreed with the formula.

## Reproduction and next question

From the repository root, using Python 3.11 or later, run

```sh
PYTHONPATH=. python experiments/forced-overlap/endpoint_pairs.py 1 2 3 4 5 6 7 8 9 10 11 12 13 26 --fastest 240 --witness
PYTHONPATH=. python experiments/forced-overlap/endpoint_study.py
```

The prediction uses integer arithmetic and compares exact rational cutoffs. The optional witness search uses the repository's bounded interval solver for the retained core. The study prints a reproducible JSON ledger by panel and core. [Pair tool](endpoint_pairs.py) · [Study](endpoint_study.py)

**Open question.** For a pair that survives the width test, can the two endpoints actually lie inside the *same* blocking interval of $V$? Combining that phase condition with the width congruence could eliminate more pairs before constructing the core's full time intervals. The speed-90 example gives a positive trapping control for such a test. Vance proposed using the lemma as the basis for a research tool. AI assisted with the derivation and implementation. Independent review and literature priority remain open.
