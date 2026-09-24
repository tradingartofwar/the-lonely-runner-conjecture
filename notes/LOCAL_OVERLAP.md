# Where duplicated blocking creates room

**September 24, 2026.** Vance suggested that an unknown variable might be creating room, then approved examining duplicated blocking inside the openings left by other runners. We make that omitted information explicit and test what it can establish.

**Outcome:** overlap inside those openings matters together with the concentration of individual blocking there. More overlap alone does not predict more clear time. An exact doubled-speed relationship supplies a separately derived overlap constraint, leading to a positive-duration guarantee for one structured family with four remaining competitors. This is a proof candidate with exact supporting certificates and no novelty claim; independent proof review remains outstanding.

[Reproduction script](../scripts/analyze_local_overlap.py) · [Exact certificates](../experiments/local_overlap.json). Run `python -m scripts.analyze_local_overlap`.

## Fix the location before counting overlap

There are still **eight total runners**, all starting together, with selected reference speed 0 and threshold `delta=1/8`. We fix three relative speeds

$$F=\{1,4,5\}$$

and examine four other speeds, collectively B. This changes the fixed/variable split; it does not add more runners to the previous eight-runner problem.

The times A during which the fixed three are all clear are exactly

$$[1/8,7/40]\cup[9/32,3/8]\cup[17/40,15/32]
\cup[17/32,23/40]\cup[5/8,23/32]\cup[33/40,7/8].$$

Their total duration is `|A|=3/8` of the common integer-speed cycle. A lonely moment for all seven competitors must lie in A. Overlap elsewhere cannot by itself identify such a moment.

Let M(t) count how many of the four competitors in B are strictly too close. On A define

$$T_A=\int_A M(t)\,dt,\qquad
R_A=\int_A\max(M(t)-1,0)\,dt,\qquad
U_A=\int_A\mathbf1_{M(t)=0}\,dt.$$

T adds their individual blocking times. R counts the duplicated part: if three runners block simultaneously, the redundancy count is two, not three pair overlaps. U is clear duration for all seven competitors.

The exact identity is

$$U_A=|A|-T_A+R_A.$$

Each of the four individually blocks one-quarter of a complete cycle. Their summed baseline over a region of length `|A|` is therefore `|A|`, although their actual local total need not equal this. Define the excess concentration

$$E_A=T_A-|A|.$$

Then

$$\boxed{U_A=R_A-E_A.}$$

Positive E means the four concentrate more blocking inside A than their full-cycle fractions would suggest; negative E means less. Clear duration appears when duplicated blocking exceeds that concentration. This is a local version of our earlier [global accounting identity](BLOCKING_OVERLAPS.md), not a new independent physical variable.

An identity alone does not prove a lower bound: computing R from already-known clear time would be circular. The useful next step is to constrain overlap from the speed relationships themselves.

## The common-start clue has a location problem

For the four competitors B considered alone over the entire cycle, their total individual blocking duration is 1, so

$$U_B=R_B.$$

If their largest speed is V, all four block whenever `||t||<1/(8V)` near the common start and end of the cycle. This supplies redundant blocking at least `3/(4V)>0`, hence some positive clear duration for these four elsewhere.

But this particular guaranteed overlap lies wholly where **fixed speed 1 is also too close**. It is outside A. The argument guarantees an opening for the four competitors considered alone and leaves unresolved whether the other three are clear there. Common start is useful structure; its initial overlap is not enough to settle placement.

## Countercheck: more overlap inside A can accompany less clear time

The following exact measurements use the same fixed set F and the same region A throughout:

| Remaining four speeds B | Redundancy R_A | Excess concentration E_A | All-seven clear duration U_A |
| --- | --- | --- | --- |
| 6,7,11,13 | 34079/240240 | 34079/240240 | 0 |
| 6,7,8,11 | 271/2310 | 1733/18480 | 29/1232 |
| 6,7,16,23 | 1277/6720 | 401/3360 | 95/1344 |
| 40,48,56,64 | 211/2240 | -1/560 | 43/448 |

The first case has **more redundancy inside A** than the second, yet zero clear duration. Its local concentration is also greater and cancels the redundancy exactly. It still has the four valid isolated odd-eighth times; zero duration does not mean no lonely moments.

The fourth case illustrates the other sign: its blocking is slightly underrepresented in A, so E is negative. Both the underrepresentation and the overlap contribute to clear duration. The exact per-opening records and full closed allowed sets are retained in the JSON.

Thus the user hypothesis leads to a more precise quantity to track: overlap **relative to the blocking concentrated in the same opening**. Merely increasing a global overlap total, or even the local total R by itself, is not sufficient reasoning.

## A speed relationship that forces repeated overlap

Take two of the four speeds to be q and 2q. At the fixed threshold `1/8`, they are simultaneously too close exactly when

$$\|qt\|<\frac1{16}.$$

To see this, write the phase of qt as a signed value s with `|s|<1/8`. Then `2s` lies in `(-1/4,1/4)`, so doubling is also too close precisely when `|2s|<1/8`, or `|s|<1/16`.

Their overlap occupies **1/8 of each period `1/q`**. Consequently their union occupies

$$\frac14+\frac14-\frac18=\frac38$$

of that period. Adding two more competitors gives a nominal union bound `3/8+1/4+1/4=7/8`, below a whole cycle. The overlap repeats frequently when q is large, giving us a way to locate some of its effect inside a fixed opening. Counting the doubled pair together avoids the duplication discarded by the previous four-term duration estimate.

This uses exact doubling and common starts. Nearby speeds do not automatically share the same identity.

## A local bound that does not use the answer in advance

For any periodic blocking set with period `1/h` and fraction p occupied in each period, its duration D in an interval of length L obeys

$$D\le pL+\frac{p(1-p)}h.$$

Write `hL=m+r`, where m is a nonnegative integer and `0<=r<1`. The full periods contribute `mp/h`; the remainder contributes at most `min(r,p)/h`. Since `min(r,p)-pr<=p(1-p)`, the displayed bound follows, independently of the interval's starting phase. The estimate applies to a union of windows within a period as well as to one window.

Use the fixed-runner opening

$$J=[9/32,3/8],\qquad L=3/32.$$

The fixed speeds are clear throughout: their phases run respectively from `9/32` to `3/8`, from `1/8` to `1/2`, and from `13/32` to `7/8`, each with a constant integer part.

For the doubled pair, set `p=3/8` and `h=q`. For two additional speeds u,v, use `p=1/4` and frequencies u,v. Summing these **three group bounds** gives a local clear-duration guarantee

$$U_J\ge\frac L8-\frac{15}{64q}-\frac3{16u}-\frac3{16v}.$$

If `u,v>=q`, then

$$U_J\ge\frac3{256}-\frac{39}{64q}
=\frac{3q-156}{256q}>0\qquad\text{for integer }q\ge53.$$

We have therefore obtained the following restricted argument:

> For all distinct integer velocities `{0,1,4,5,q,2q,u,v}` with `q>=53` and `u,v>=q`, the selected speed-zero runner has positive lonely duration inside `[9/32,3/8]` at the eight-runner threshold `1/8`.

The other two speeds have no upper bound. The conclusion rests on the periodic overlap identity and the local boundary allowance; it does not infer an infinite statement from numerical examples. The argument remains unreviewed, and this elementary restricted statement is not claimed as a new result.

The constant 53 is sufficient for this deliberately coarse uniform bound. It is not claimed to be optimal, necessary, or a classification of smaller speeds. When `q=52`, this uniform lower bound is zero, while the exact control `(q,u,v)=(52,56,64)` still has positive clear duration `1315/46592` in J; even the less-coarse displayed bound is positive there.

For the diagnostic `(q,u,v)=(56,64,72)`, all four added speeds are multiples of 8, so they block the old eighth times. Nevertheless, `t=6/17` gives minimum distance `4/17>1/8` from all seven competitors. The exact clear duration in J is `53/1792`, above the uniform guarantee `3/3584`. These witness values are not claimed maxima.

## A nearby change breaks the chosen witness

Change 112 to 113 while retaining `(56,64,72)` and the fixed set F. In J, the overlap of the altered pair falls from

$$|B_{56}\cap B_{112}\cap J|=11/896
\quad\text{to}\quad
|B_{56}\cap B_{113}\cap J|=9/3616.$$

The old witness `t=6/17` now fails: speed 113 is only `2/17<1/8` away. Other valid times remain; exact clear duration in J is `6193/260352>0`. Thus exact doubling creates useful structure, but the new existence bound does not automatically extend to a near-doubled pair. This control does not disprove a broader extension; it shows which identity and witness cease to apply.

## Verification, source context, and next question

Eight prescribed configurations are analyzed on the whole cycle, the union A, and its six constituent intervals: **64 measured regions**. Complete rational partitions cut at every blocking-status boundary; midpoints represent entire constant-status cells, not sampled-time estimates. Every region's clear duration is crosschecked against the existing closed-interval checker. The full seven-speed allowed sets agree with intersecting the four-speed allowed sets with A. Individual durations and **384 pair durations** are separately checked by direct interval intersections. The doubled-pair predicate identity is checked on all cells and boundary points of its unit-phase partition. Three exact family diagnostics include q=52,53,56; none replaces the unbounded argument.

The covering formulation, equal individual fractions, and the role of overlap are established mathematics. [Tao's exposition, S4](https://terrytao.wordpress.com/2017/01/10/some-remarks-on-the-lonely-runner-conjecture/), re-opened September 24, discusses the common-start overlap, the limitations of the union bound, and arithmetic structure that can enforce additional overlap. His n counts moving speeds; ours counts total runners. His historical frontier is not used as current status. No novelty search or independent proof review of this restricted argument is claimed.

Vance supplied the suggestion to look for an omitted quantity creating room and authorized the local overlap investigation. The AI supplied the local accounting, counterchecks, and doubled-speed bound. The result identifies useful information missing from our coarse estimate, not an undiscovered physical property or universal multiplicative law.

The next useful question is which speed relationships, beyond exact doubling, force enough **repeated local overlap** to give an independent lower bound inside fixed-runner openings. Arbitrary four-speed inputs remain outside the family proved here. Any extension should retain the concentration term and exact equality points, rather than treating a measured overlap total as a proof by itself.
