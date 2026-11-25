# What relationships have taught us about Lonely Runner

November 24, 2026. Team review of the September–November project results, with three reproducible checks. The runner count includes the chosen reference. At time $t$, join two physical runners $i,j$ when their circular distance $\|(v_i-v_j)t\|$ is strictly less than $1/n$. A runner is lonely exactly when no edge touches it. Each runner may have its own time. An equality contact is safe.

## An experiment that distinguishes two meanings of “relationships”

Take $X=\{0,1,4,7\}$ and $Y=\{0,9,18,28\}$. Form two 16-speed lineups, $A=\{x+y\}$ and $B=\{x+28-y\}$, over all $x\in X,y\in Y$. Each list has 16 distinct nonnegative speeds, including 0. The **multiset of all 120 pair distances is identical for every real time**. To see why, count ordered speed differences. They have the form $(x-x')+(y-y')$ in the first lineup and $(x-x')-(y-y')$ in the second. Interchanging $y$ and $y'$ preserves multiplicity. Taking absolute gaps, then applying $d\mapsto\|dt\|$, gives the claim. Direct-sum constructions of sets with identical differences are established in the homometry literature. [Averkov and Langfeld](https://arxiv.org/abs/1412.7676).

| At time $1/3$ | Runners at the start | At $1/3$ lap | At $2/3$ lap | Lonely runners |
|---|---:|---:|---:|---|
| Lineup A | 3 | 10 | 3 | None |
| Lineup B | 1 | 6 | 9 | Runner 0 |

Both have exactly 51 colliding pairs and 69 pairs one-third of a lap apart. In the second lineup the 51 collisions all miss runner 0. The multiset forgets **which edges meet at which runner**. At any reduced time $a/q$ with $2\le q\le n$, the analogous exact rule is simple: each speed alone in its residue class modulo $q$ is lonely, and only those speeds are. Distinct occupied positions are at least $1/q$ apart. This rule preserves the labels of the isolated runners.

A second constructed pair in the checker has different maximum clearances even after optimizing each reference over **all** times. The worst runner in one has maximum $2/17$; in the other it is $1/9$. Both exceed $1/16$. These examples concern the information needed to identify lonely times or measure clearance. They do not contradict the conjecture. [Matched-lineup checker](relationship_pairs.py).

## What the project had already established

| Study | Result for the physical runners | Information needed |
|---|---|---|
| September, overlapping blockers | In $[9/32,3/8]$, speeds 6 and 16 block together on 16's fifth lap. Speeds 11 and 16 block together on its sixth. The two pair events cannot combine into that triple. | Identity of the shared runner **and its lap**. [Original study](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/52c4912a89e4c314201e66e7fa94da7fa3366964/notes/LAP_LABELLED_CONSTRAINTS.md) |
| September, equality contacts | Replacing speed 1680 by 3360 in an eight-runner lineup preserved all 128 labelled subset blocking durations and all 21 pair gcds among moving speeds on the specified comparison. One lineup retained the isolated witness $9/32$ in the test interval and the other had none there. Both had witnesses elsewhere. | Exact endpoints. A singleton has duration zero. [Contact study](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/52c4912a89e4c314201e66e7fa94da7fa3366964/notes/CONTACT_MOMENTS_2026_09_27.md) |
| September, Compatibility Calculus | With primitive parameter speeds $P,Q$, phases $x,y$ arise at one physical time iff $Qx-Py$ is an integer. Bézout recovery gave a constructive argument for a structured family. After adding an independent parameter, four selected sheets succeeded on 89/89 training examples and 310/318 holdout examples. | A verified route from abstract phases back to the same time. [Two parameters](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/52c4912a89e4c314201e66e7fa94da7fa3366964/notes/CC_TWO_PARAMETER_WITNESS_2026_09_29.md) · [Third parameter](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/52c4912a89e4c314201e66e7fa94da7fa3366964/notes/CC_THREE_PARAMETER_TEST_2026_09_30.md) |
| October, adding an opponent | Every one of 1,199 tested components across twelve challenge cores had an added speed that blocked that component. The blocker could differ between components. | Which speed blocks which interval. This failed to establish that any one speed blocks them all. [Center-selection handoff](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/35e426bb200f49fa742165b9e279b13d7524e0b6/notes/MISSION_CONTROL_HANDOFF_2026_10_17_CENTER_SELECTION.md) |
| November, endpoint and prime-grid tests | A fast opponent has to block both endpoints of a closed interval in the same open pass. On two prime grids, reversing the assignment of one list of residues to physical runners turns a pair of individually blocked grids into a class with an explicit near-half-lap witness. Independently reassigning labels can also make a short equation appear on every grid without settling any case. | Shared runner labels, phase, and open or closed endpoints. [Endpoint study](../forced-overlap/ENDPOINT_RESULTS.md) · [Cross-prime controls](../cross-prime-relations/README.md) |

One bit can matter. At $7/22$ and $9/11$ the positions of speeds 6 and 16 are identical, respectively $10/11$ and $1/11$. Speed 11 is half a lap away at the first time and at the reference at the second. Because $6+16=2\cdot11$, halving the sum of the two lifted phases requires the parity of the sum of their lap numbers. Likewise, the archived shift from $3/16$ to $11/16$ fixes eight even-speed phases and moves speed 5 from phase $15/16$ to $7/16$. Both calculations were replayed.

There is a separate theoretical reason to examine integer relations. Beck and Everett's Theorem 2.1 requires a short integer relation with odd coefficient sum in tight instances or counterexamples. For 15 different positive relative speeds the coefficient absolute values total at most 33. Having such a relation alone does not identify a witness. Allikvere's fifteen-runner preprint gives another constructive use: time shifts can preserve one group while allowing a few exceptions to move. [Beck and Everett](https://arxiv.org/html/2609.06259v2) · [Allikvere, §4.4](https://arxiv.org/html/2609.02604v2#S4.SS4).

## How much synchronization is actually necessary?

On the 135 residual lineups from the earlier neutral 16-runner panel, we exhaustively tested whether at a full witness some of the eleven slowest opponents could occupy one nonzero position. For each pair all possible reduced denominators divide its speed difference. For equality of distances, opposite phases are possible too, so its speed sum also contributes denominators. The counts below include only times checked against **all fifteen** opponents.

| Required group size among eleven | Same position | Same distance from reference, allowing reflection |
|---:|---:|---:|
| 11 | 0 | 2 |
| 7 | 1 | 15 |
| 5 | 19 | 67 |
| 3 | 134 | 135 |

All 135 lineups already have a witness of denominator at most 32. For an external control, the consecutive speeds $0,\ldots,15$ have only the odd sixteenths as witnesses for runner 0. At each one all positions are distinct and at most two opponents share any given distance. The equal-spacing proof follows by taking all pair differences, which are among $1,\ldots,15$: the sixteen cyclic gaps must sum to 1 and each must be at least $1/16$. Exact synchronization is therefore one sufficient mechanism and fails as a necessary one. These coincidence counts used positive physical speeds against stationary 0. With a different reference, retain signed relative speeds for statements about physical positions. [Alignment audit](relationship_alignment.py).

## What can be predicted before finding the time?

Suppose a group of **positive** relative speeds occupies the same safe phase $p\in[\delta,1-\delta]$ at $t_0$, where $\delta=1/n$. Let $V$ be the largest speed in this group. In either direction it reaches the boundary of the safe arc at least as soon as every other member. The common safe interval through $t_0$ is therefore exactly

$$
\left[t_0-\frac{p-\delta}{V},\ t_0+\frac{1-\delta-p}{V}\right].
$$

Its width is $(1-2\delta)/V$ regardless of how many different laps the group has completed. More generally, if the phases at $t_0$ lie in $[p_-,p_+]\subseteq[\delta,1-\delta]$, the width is at least $(1-2\delta-(p_+-p_-))/V$. One can compute the exact common endpoints from the individual lap numbers. A zero-width intersection must still be tested directly. Positive speeds here may also represent folded absolute velocities when the conclusion concerns clearance only.

The [previous adjustment rule](SECOND_TIME.md) bounds the wait for $k$ faster exceptions by $D_k=2\delta\sum_{j=1}^k 2^{k-j}/w_j$, for $w_1\ge\cdots\ge w_k$ and $2^k\le n$. A window at least this wide contains a full witness. For $n=16$ a common-phase group can accommodate three exceptions at least as fast as $V$, or four if the slowest exception is at least $15V/7$. Individual speed values can give a better bound.

A simple two-group construction makes the adjustment explicit. Take eleven odd relative speeds $1,3,\ldots,21$ and four even speeds $M,M+2,M+4,M+6$ for even $M\ge60$. At $1/2$ all eleven odds are opposite the reference and all four evens collide with it. At $1/2+1/(2M)$ the odds are displaced from half a lap by at most $21/(2M)$; the evens are displaced from half a lap by at most $3/M$. The minimum clearance is **exactly** $1/2-21/(2M)>1/16$. Taking $M$ divisible by every denominator in any proposed finite list defeats every direct time in that list, while the formula still works. The earlier four-fast first-lap window is empty since $21>15$. This illustrates how one relationship can choose a new time before a scan.

For a broader test we used safe intervals around reduced times of denominator through 7, permitting the eleven slower opponents to occupy different safe phases on different laps. On 1,024 fresh draws with four predeclared maximum speeds, 428 lineups defeated both the earlier repair/original time and all direct anchors. Shifting inside the shared windows recovered 132 of those 428. A post-hoc direct scan through denominator 32 recovered **all 132** too. The constructive example above establishes a distinction from any fixed finite list of times. The fresh sample shows no extra coverage over the larger direct scan among those 132. [Protocol, controls, and fresh replay](relationship_windows.py).

## Open proof question

At an instant, knowing the cyclic order and the two adjacent gaps of a labelled runner is sufficient to decide its loneliness, including ties. Inserting a new runner splits one gap, so only its two neighbors in the old order can acquire a closer neighbor at that instant. The open problem is to predict an instant when **both** adjacent gaps for a specified runner reach $1/n$. A candidate rule should accept the isolated equality witnesses of the consecutive lineup and distinguish the two matched 16-runner lineups at $1/3$. Finding a time after sorting every event is an exact verification procedure. Predicting it from a smaller set of labelled relationships is the research target. All new examples and the audit are internal checks, awaiting independent review.
