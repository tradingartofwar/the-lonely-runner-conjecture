# Blocking chains beyond Fibonacci

**September 23, 2026.** Vance clarified that Fibonacci should not constrain the investigation and selected the broader question: **What prevents the runners from collectively blocking every possible moment?** The Fibonacci detour is complete for present purposes. This note tests interval-cover certificates on existing non-Fibonacci examples and one nearby change.

**Result:** the three tight cases admit short, exact chains of blocking windows. Their shared lonely times also have an elementary modular explanation, which limits what those examples can teach us about the general existence question. A change from relative speed 13 to 8 removes that modular shortcut and blocks every old lonely time, but exposes different valid times. The calculations explain this fixed example; they do not prove that every attempted complete blocking schedule must fail.

[Reproduction script](../scripts/analyze_blocking_chains.py) · [Exact certificates](../experiments/blocking_chains.json). Run `python -m scripts.analyze_blocking_chains`.

## Scope and conventions

All configurations have eight total runners. The selected reference is stationary after subtracting its speed; the other seven relative speeds are positive integers. All start together, time is measured over a common period, and the target stays `delta=1/8`.

The computation reuses the seven configurations in `cooperative_blocking.json` and adds exactly one input, `{1,4,5,6,7,8,11}`, obtained from `{1,4,5,6,7,11,13}` by replacing 13 with 8. Only the selected reference is examined here; no new all-reference claim or speed-set search is made.

The covering viewpoint is established mathematics: see [Tao's exposition, S4](https://terrytao.wordpress.com/2017/01/10/some-remarks-on-the-lonely-runner-conjecture/), re-opened September 23. His `n` counts moving speeds, our `n-1`, and his extremal-radius formulation uses closed Bohr sets. At our fixed allowed threshold, the strictly-too-close sets are **open**; endpoints at exactly `1/8` must remain valid. His historical frontier is not used as current status.

## First finding: our original examples share an easy witness

The three tight relative-speed sets are

$$A=\{1,2,3,4,5,6,7\},\quad
B=\{1,2,3,4,5,7,12\},\quad
C=\{1,4,5,6,7,11,13\}.$$

None contains a multiple of 8. Consequently every odd-eighth time `t=q/8` is a valid witness. For odd `q`, multiplication by `q` cannot turn a nonzero residue modulo 8 into zero. Every phase is therefore one of `1/8,...,7/8`, and every circular distance is at least `1/8`.

More generally, if none of the integer relative speeds is divisible by the original total `n`, then `t=1/n` is a witness. Numerators coprime to `n` work too. This is sufficient, not necessary, and does not establish that the maximum is exactly `1/n`.

All seven previously studied inputs share the modulo-8 witness, even the non-tight controls. Their blocking chains explain their different **upper bounds**; the existence of the shared equality times needs no complicated chain argument. This is a limitation of our chosen examples, not a reason to assume the same denominator works in general.

## A change that closes every old lonely moment

Replace speed 13 in C by 8:

$$C'=\{1,4,5,6,7,8,11\}.$$

The new speed collides with the reference at all four old times `1/8,3/8,5/8,7/8`. Indeed it blocks **every** rational time whose reduced denominator is at most 8: for each denominator `q=1,...,8`, some speed in C' is a multiple of q. For q=3 that speed is 6; all other needed divisibilities are immediate. Such a speed has integer position at every `p/q`.

Nevertheless, the new exact maximum is

$$L(C')=\frac{2}{13}>\frac18,$$

attained at `t=4/13` and `9/13`. The two checker methods agree. These times have a denominator outside the entire blocked range just described.

Here are the distances at the earlier maximum:

| Relative speed | Shorter-arc distance at `t=4/13` |
| --- | --- |
| 1 | `4/13` |
| 4 | `3/13` |
| 5 | `6/13` |
| 6 | `2/13` |
| 7 | `2/13` |
| 8 | `6/13` |
| 11 | `5/13` |

On a 400-meter track, the minimum separation is about 61.54 meters, above the required 50 meters. This statement concerns the selected runner at that instant.

### Exactly which handoff breaks

Speed 7's blocking window around its second meeting ends at `17/56`. Speed 6's window around its second meeting starts at `5/16`. Between them lies

$$\left[\frac{17}{56},\frac5{16}\right],\qquad
\frac5{16}-\frac{17}{56}=\frac1{112}.$$

Originally, speed 13 blocked this entire interval through its window

$$\left(\frac{31}{104},\frac{33}{104}\right).$$

Speed 8 cannot replace that bridge. Across the interval its phase goes from `3/7` to `1/2`, staying far from the reference. Every other speed also meets the target throughout; the complete interval checker confirms both endpoints and the interior.

The new local peak balances the distances of speeds 7 and 6:

$$7t-2=2-6t,\qquad t=\frac4{13},\qquad \text{gap}=\frac2{13}.$$

The old speed 13 would meet the reference exactly there: `13*(4/13)=4`.

This also connects to our earlier **general additive relation**, without requiring a Fibonacci sequence. Speeds `a,b,a+b` cannot all be clear when the first two have opposite equal phases: their sum then collides. Here, removing `13=6+7` frees the 6/7 handoff, while adding `8=1+7` blocks the old 1/7 handoff at `1/8`. This explains the two concrete competing opportunities. It does not establish that every speed replacement necessarily creates another one.

The complete new allowed set is

$$[17/56,5/16]\ \cup\ [41/88,15/32]\ \cup\
[17/32,47/88]\ \cup\ [11/16,39/56].$$

A further coincidence worth recording: these are exactly the positive-length intervals of the earlier 13-to-12 control. That control additionally retains the four isolated odd-eighth times; the new speed 8 removes those isolated points. The script checks this equality of interval sets.

## Compressing the blocking schedules

Each meeting at `j/v` contributes the open window

$$I_{v,j}=\left(\frac{j-1/8}{v},\frac{j+1/8}{v}\right).$$

A chain covers an open time segment when its first interval starts at the segment's left endpoint, each subsequent interval **strictly overlaps** the covered portion and extends its right endpoint, and the last interval ends at the segment's right endpoint. Mere touching leaves a valid point unless another window covers it.

For the three tight cases, four chains cover everything between their four isolated witnesses. The final component wraps around the common cycle boundary, from `7/8` to `9/8`.

| Case | Individual windows per cycle | Minimum windows needed to cover all blocked times | Chain lengths between successive witnesses |
| --- | ---: | ---: | --- |
| A: consecutive | 28 | 18 | `6,5,6,1` |
| B: replace 6 by 12 | 34 | 18 | `6,5,6,1` |
| C: replace 2,3 by 11,13 | 47 | 26 | `8,9,8,1` |

For the first component `(1/8,3/8)`, the speed sequences of the minimum chains are:

- A: `7,6,5,4,7,3`.
- B: `7,12,5,4,7,3`.
- C: `7,6,5,4,7,13,6,11`.

Repeated speed labels denote different meetings. The exact meeting indices, intervals, and overlap margins are in the JSON certificates.

For example, the bridge supplied by speed 6 in A is `(7/48,3/16)`. Speed 12 replaces it in B with the narrower `(5/32,17/96)`, which still overlaps both neighbors. Its overlaps with speed 7 on the left and speed 5 on the right are respectively `1/224` and `1/480`. This preserves the chain despite changing the speeds and widths.

The certificate compresses **visits**, not necessarily runners. For each of the seven speeds in each tight case, we found an exact time when it alone is too close and all six others are strictly farther than `1/8`. Those 21 witnesses show that removing any whole constraint raises the attainable gap above the fixed original target. These diagnostic deletions do not redefine the original runner count.

Minimum chain length also fails as a tightness test: the new non-tight case C' needs 26 windows, just like tight case C. Thus neither the total number of visits nor the compressed count alone distinguishes the outcomes.

## Verification and the graph model

For each blocked component, a graph vertex represents an entire blocking window. There is a directed edge from I to J when J overlaps I strictly and extends its right endpoint. Edges advance the right endpoint, so the graph is acyclic. Initial vertices start at the left boundary; terminal vertices reach the right boundary. A shortest path gives a minimum interval chain.

The script independently compares two constructions: the greedy rule that always reaches farthest, and dynamic programming over all graph edges. Greedy is optimal by the usual exchange argument: replacing the first interval of any cover by an eligible interval reaching farther cannot hinder subsequent coverage. Repeat at each reached endpoint. Coordinates and strict inequalities are retained; an unlabeled overlap graph would lose the endpoint distinctions we need.

All **46 blocked components across eight configurations** agree between the constructions. Selected chains are then checked on every interval-boundary point and every open cell cut out by their endpoints. These finite partitions are complete for their predicates; they are not a time grid. Maxima for all eight selected references agree between the existing piecewise-linear and closed-interval methods.

Each internal overlap also satisfies the integer identity from [the overlap note](BLOCKING_OVERLAPS.md): for ordered meetings `p/a<q/b`, the facing gap is

$$\frac{8(aq-bp)-(a+b)}{8ab}.$$

It is negative inside every constructed chain. Between chains it is zero for an isolated witness, or positive for an allowed interval. This explains the certificates for the specified inputs; it does not prohibit a hypothetical completely overlapping cycle for arbitrary speeds.

## What this changes in our research direction

We can now explain a particular blocking schedule with a short certificate and identify the exact bridge lost in a speed change. We also corrected a selection bias: every old case had an immediate modulo-8 witness. The new control requires leaving that denominator range.

The common-start rule ties together each runner's meeting locations, spacing, and window width. Changing a speed moves all its windows at once; they cannot be positioned independently. These constraints are the material a general argument would need to use. Their mere existence is not a proof of noncoverage.

The next useful question is: **when every reduced denominator up to n is blocked, what forces a different valid fraction or time to remain?** Our C' example provides one exact object to study. We should investigate that arithmetic constraint before expanding any search. Fibonacci is not an assumption of this direction, and no universal law, new theorem, or solution of the general conjecture is claimed.
