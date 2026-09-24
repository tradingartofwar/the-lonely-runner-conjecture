# Speed ratios, repeated overlap, and useful openings

**Date:** September 24, 2026. **Status:** known pairwise overlap formula reproduced; restricted-family argument below is an unreviewed derivation, with no novelty claim. Exact finite checks support the arithmetic but do not replace review of the unbounded argument.

Vance asked us to retain the question, **what forces enough overlap when individual blocking durations could add up to complete coverage?** He approved extending the doubled-speed argument to other ratios and keeping a nearby countercheck. The useful distinction is between the amount of repeated overlap and its placement within the other runners' openings.

## 1. What is fixed

There are eight total runners, starting together. Select speed 0 as the reference and keep relative speeds `1,4,5`. Write the remaining four as `A,B,u,v`, all positive integers, with all seven relative speeds distinct. The target remains **1/8** throughout; studying a pair does not change the runner count.

A speed w blocks a time when `||wt||<1/8`. Each blocks 1/4 of a unit time cycle. Equality is allowed. The three fixed speeds leave the entire closed interval

$$J=[9/32,3/8],\qquad L=|J|=3/32$$

clear. Their fractional phases range respectively over `[9/32,3/8]`, `[1/8,1/2]`, and `[13/32,7/8]`. We seek clear duration inside J. Positive duration suffices; a zero duration conclusion would still require checking isolated equality times.

## 2. Ratio determines overlap; common factor determines a repetition period

Write `A=ga`, `B=gb`, where `g=gcd(A,B)`, `a<b`, and `gcd(a,b)=1`. The pair's joint blocking pattern has period `1/g`. Its full-cycle simultaneous-blocking fraction, denoted rho, depends only on a,b. Multiplying both speeds by g repeats and compresses the same pattern without changing that fraction.

Put `f(x)=x(1-x)` and let `{x}` mean fractional part. At our fixed threshold,

$$\rho(a,b)=\frac1{16}+\frac{f(\{(a+b)/8\})-f(\{(b-a)/8\})}{ab}. \tag{1}$$

This is a specialization of known pairwise-intersection mathematics. Perarnau and Serra's Proposition 8 gives an equivalent geometric formula; Jensen's Lemma 4.1 and following remark give the equivalent Bernoulli-polynomial expression, including unequal thresholds. We inspected both sources, matched the formulas algebraically, and checked prescribed inputs exactly. See [Sources S13–S14](SOURCES.md). We are reproducing this result, not discovering it.

For the algebraic match, put `x={a/8}`, `y={b/8}`. Splitting at `x=y` and `x+y=1` gives `f({x+y})-f({y-x})=2[min(x,y)+max(x+y-1,0)-2xy]`, the correction in Perarnau–Serra. Jensen's match follows from `B2(x)=1/6-f(x)`.

An elementary reconstruction of (1) makes the arithmetic visible. Scale time by ab. The meeting centers for a and b become `bj` and `ak`, on a circle of length ab, with blocking half-widths `b/8` and `a/8`. Coprimality makes `bj-ak`, for `0<=j<a`, `0<=k<b`, run once through all residues modulo ab. Put

$$s=(a+b)/8,\quad c=(b-a)/8,\quad H(x)=\sum_{d\in\mathbb Z}(x-|d|)_+.$$

Two intervals with center difference d have intersection length `(s-|d|)_+-(c-|d|)_+`. Summing over integer lifts of the center differences, and dividing by ab, gives

$$\rho=\frac{H(s)-H(c)}{ab},\qquad
H(x)=x(2\lfloor x\rfloor+1)-\lfloor x\rfloor(\lfloor x\rfloor+1)
=x^2+\{x\}(1-\{x\}).$$

Each speed's own blocking intervals are disjoint, so this sums intersections without duplicating simultaneous-blocking time. Since `s^2-c^2=ab/16`, (1) follows. Endpoint inclusion does not affect these measures.

The pair's union fraction is `p=1/2-rho`: we subtract the simultaneous blocking that was counted twice.

| Pair of speeds | Reduced ratio, faster:slower | Simultaneous blocking rho | Union fraction p |
| --- | --- | --- | --- |
| g, 2g | 2:1 | 1/8 | 3/8 |
| g, 3g | 3:1 | 1/12 | 5/12 |
| 2g, 3g | 3:2 | 1/12 | 5/12 |
| g, 7g | 7:1 | 1/28 | 13/28 |
| g, 8g | 8:1 | 1/16 | 7/16 |
| g, 9g | 9:1 | 1/12 | 5/12 |

Three patterns survive counterchecks:

- Different ratios can have the same overlap fraction: 3:1 and 3:2 do. Their schedules need not be the same.
- Overlap does not decrease monotonically with speed ratio. It falls through 7:1 in this list, then rises at 8:1 and 9:1.
- The fractional-part correction is controlled by residues modulo 8 and divided by ab. If either reduced speed is divisible by 4, the correction vanishes and rho is exactly 1/16. In general, `|rho-1/16|<=1/(4ab)`.

That last baseline equals `(1/4)^2`, but matching an independent-probability value does not establish independence of the full time schedules.

## 3. A uniform pair-overlap floor at this threshold

Because `0<=f(x)<=1/4` on `[0,1]`, (1) implies

$$\rho(a,b)\geq\frac1{16}-\frac1{4ab}.$$

For `ab>=10`, this is at least `3/80>1/28`. For `ab<10`, the complete list of distinct coprime positive pairs is `(1,2),...,(1,9),(2,3)`. Their fractions are, in that order,

$$1/8,\ 1/12,\ 1/16,\ 1/20,\ 1/24,\ 1/28,\ 1/16,\ 1/12,\ 1/12.$$

Consequently **rho>=1/28 for every pair of distinct positive integer speeds**, with equality exactly for reduced ratio 7:1. The finite list is exhaustive because of the preceding product bound; this is not an inference from scanning examples. It is a threshold-specific deduction from a known formula, with no originality claim.

This floor concerns a whole cycle. It does not say where in the cycle the overlap occurs.

## 4. Turning repeated overlap into a local guarantee

Recall the elementary bound in [LOCAL_OVERLAP.md](LOCAL_OVERLAP.md). A periodic occupied set with period `1/h` and fraction p occupies at most

$$pL+\frac{p(1-p)}h$$

of any interval of length L. To verify it, split the interval into full periods and a remainder r. The remainder occupies at most `min(r,p/h)`, whose excess over pr is at most `p(1-p)/h`. No assumption about the set's shape or its starting phase is required.

Apply this to the pair union with `p=1/2-rho`, `h=g`, then to u and v separately with fraction 1/4. Subtracting these upper bounds from L yields

$$U_J\geq\rho L-\frac{1/4-\rho^2}{g}-\frac3{16u}-\frac3{16v}. \tag{2}$$

The first term is the benefit of duplication. The remaining terms bound how much concentration in the partial periods can consume that benefit. This is a lower bound obtained from the speeds before calculating the final allowed set.

If `u,v>=g`, then

$$U_J\geq\rho L-\frac{5/8-\rho^2}{g}>0
\quad\hbox{whenever}\quad g>\frac{5/8-\rho^2}{\rho L}. \tag{3}$$

| Pair | Sufficient g, assuming u,v>=g |
| --- | --- |
| g,2g | g>=53 |
| g,3g | g>=80 |
| 2g,3g | g>=80 |
| g,7g | g>=187 |

These are conservative sufficient bounds, not sharp boundaries between success and failure. They apply to the selected reference with fixed core `1,4,5`, not automatically to the other reference runners.

There is also a ratio-free sufficient family. If **`gcd(A,B)>=187` and `u,v>=187`**, use `rho>=1/28` directly in (2):

$$U_J\geq\frac3{896}-\frac{489}{784\cdot187}
=\frac{15}{1172864}>0. \tag{4}$$

Here replacing the three denominators by 187 is only a worst-case estimate; it does not require any actual speeds to coincide. The ratio A:B is unrestricted. All seven relative speeds must still be distinct. Thus exact doubling was a useful starting point, but it is not essential to this particular mechanism.

The unbounded family argument is a proof candidate awaiting independent review. It does not cover arbitrary four added speeds, or settle the general conjecture.

## 5. Exact checks and the nearby counterexample to an overstrong interpretation

Each row below has the same fixed core `1,4,5`, target 1/8, and window J. The lower bound uses the actual u,v in (2).

| Pair A,B | Other u,v | g | Guaranteed lower bound for U_J | Exact U_J |
| --- | --- | --- | --- | --- |
| 56,112 | 64,72 | 56 | 43/21504 | 53/1792 |
| 80,240 | 88,96 | 80 | 35/50688 | 1153/42240 |
| 160,240 | 88,96 | 80 | 35/50688 | 613/21120 |
| 192,1344 | 200,208 | 192 | 3487/16307200 | 86543/3494400 |
| 56,113 | 64,72 | 1 | -755/3072, inconclusive | 6193/260352 |

The 3:1 and 3:2 rows even have the same pair overlap inside J, namely 1/128, but different total clear duration after u,v are included. Placement and higher-order overlaps matter beyond that scalar statistic.

Changing 112 to 113 gives a particularly useful control:

| Quantity | Pair 56,112 | Pair 56,113 |
| --- | --- | --- |
| Reduced speeds | 1,2 | 56,113 |
| Joint pattern period 1/g | 1/56 | 1 |
| Whole-cycle overlap | 1/8 | 1/16 |
| Pair overlap inside J | 11/896 | 9/3616 |
| Minimum distance at old witness 6/17, all seven speeds | 4/17 | 2/17, below threshold |

The changed configuration still has clear intervals. Its negative bound means the estimate is too weak, not that coverage is complete. For example, `t=83/226` has minimum distance `37/226>1/8`. Large absolute speeds do not imply a large pair gcd, and a ratio numerically close to 2 need not retain doubling's short repeated pattern.

## 6. Reproduction and remaining question

Run `python -m scripts.analyze_speed_ratios` from the repository root. [The script](../scripts/analyze_speed_ratios.py) writes [exact certificates](../experiments/speed_ratios.json), including dependency hashes and the base commit.

Completed checks: 11 prescribed reduced ratios agree among the fractional-part formula, geometric sum, Perarnau–Serra formula, and direct interval intersections. The nine-pair remainder in the overlap-floor argument is complete. Five full configurations verify scale invariance, the pair's period, local duration bounds, and exact allowed intervals. Six affine interval certificates (the core plus one interval in each configuration) check their endpoint phases directly, independently of interval selection. No broad search, new maximum calculation, all-reference campaign, or independent proof review was run.

The retained question now has a restricted answer: **arithmetic relationships force overlap, and sufficiently short repetition periods make its coverage savings survive inside a useful opening.** This is still only one sufficient mechanism. Pairs with small gcd, including the 56:113 control, can leave room that this coarse bound does not explain.

Next useful step: derive a sharper local bound for small-gcd pairs from where their overlap intervals actually fall in J, and test it against the 56:113 control and the tight `6,7,11,13` case. Retain isolated equality times; any claim that all cases leave positive duration would already contradict the tight example. Vance's question directs the investigation; the AI supplied the derivation, literature match, implementation, and counterchecks recorded here.
