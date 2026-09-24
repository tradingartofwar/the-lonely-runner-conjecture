# One variable speed cannot block every opportunity

**September 24, 2026.** Vance approved the proposed next step: fix six relative speeds and let the seventh range over all distinct positive integers. The question continues his broader direction, "What prevents the runners from collectively blocking every possible moment?" Fibonacci is not an assumption.

**Outcome:** an elementary argument supplies an explicit valid time for every member of this one-parameter family. The original interval-width reduction leaves three finite checks; a further modular observation removes even those exceptions from the main argument. Exact arithmetic certificates support the calculation. The written argument has not received independent proof review, and no novelty is claimed.

[Reproduction script](../scripts/analyze_variable_speed_family.py) · [Exact certificates](../experiments/variable_speed_family.json). Run `python -m scripts.analyze_variable_speed_family`.

## The precise claim and its scope

There are eight runners with velocities

$$\{0,1,4,5,6,7,11,w\},\qquad
w\in\mathbb Z_{>0}\setminus\{1,4,5,6,7,11\}.$$

All start together. Select the speed-zero runner, stationary in these relative coordinates. Write `||x||` for distance to the nearest integer. We want a time t with

$$\min_{v\in\{1,4,5,6,7,11,w\}}\|vt\|\ge\frac18.$$

Only this selected reference is treated. The argument does not assert simultaneous loneliness, calculate the best separation for each w, classify tight configurations, handle arbitrary real w, or prove the general conjecture. Adding the same velocity to all eight makes every runner move while preserving these separations.

## A whole interval is clear for the fixed six

Put

$$a=\frac{17}{56},\qquad b=\frac5{16},\qquad
I=[a,b],\qquad b-a=\frac1{112}.$$

Every fixed runner is at least 1/8 away throughout I. Here is a direct certificate, independent of the interval-intersection implementation:

| Speed v | Integer part of vt throughout I | Phase at a | Phase at b |
| --- | ---: | --- | --- |
| 1 | 0 | 17/56 | 5/16 |
| 4 | 1 | 3/14 | 1/4 |
| 5 | 1 | 29/56 | 9/16 |
| 6 | 1 | 23/28 | 7/8 |
| 7 | 2 | 1/8 | 3/16 |
| 11 | 3 | 19/56 | 7/16 |

Each phase increases linearly between the listed endpoints without crossing an integer. Both endpoints lie in `[1/8,7/8]`, so every intermediate phase does too. The inequalities are strict in the interior of I. The existing exact interval checker separately confirms that I is a full allowed component for the core, at the unchanged eight-runner target.

## The promised finite reduction

At `t=1/8`, the fixed six are clear. If `8` does not divide w, then `w/8` has a nonzero eighth residue, so its distance to an integer is at least 1/8. Thus **only a multiple of 8 could block every opportunity**.

The times when the extra runner is strictly too close form disjoint open intervals

$$\left(\frac{j-1/8}{w},\frac{j+1/8}{w}\right),\qquad j\in\mathbb Z.$$

Each has width `1/(4w)`. To cover the connected closed interval I, one of these open intervals must contain all of I: moving between two of its disjoint components would cross a clear gap. Strict containment requires

$$\frac1{4w}>\frac1{112},\qquad w<28.$$

The inequality is strict because equality with the threshold is allowed. An open interval of the same length cannot contain both endpoints of I.

Combining divisibility and width leaves exactly **w=8,16,24**. All three are clear at the same time, `t=a=17/56`:

| Extra speed w | Extra runner's distance at a | Minimum over all seven competitors |
| --- | --- | --- |
| 8 | 3/7 | 1/8 |
| 16 | 1/7 | 1/8 |
| 24 | 2/7 | 1/8 |

This completes the finite reduction argument. The infinitely many speeds outside this list are handled by the inequalities, not by extrapolating a scan. This reuses the divisibility-plus-width method already used in our [6-to-12 replacement explanation](TIGHT_CASES_4_8_12.md), with a different fixed core and question.

## A sharper pattern: blocking two times forces speed 56 or more

The three checks suggest looking at a directly. After the first step, write `w=8m`. Then

$$wa=8m\frac{17}{56}=\frac{17m}{7}.$$

Unless `7` divides m, this is a nonzero seventh residue. Its distance to an integer is at least `1/7`, which is **greater** than the required `1/8`. Therefore a speed blocking both `1/8` and a must be divisible by **56**.

Write `w=56m`, with `m>=1`. This runner collides exactly at a because `wa=17m`. Wait just long enough for it to travel 1/8 lap:

$$t=a+\frac1{8w}.$$

At that time `wt=17m+1/8`, so the extra runner is exactly 1/8 away. The wait satisfies

$$0<t-a=\frac1{448m}\le\frac1{448}<\frac1{112}=b-a.$$

Thus t remains inside I, where all six fixed runners are strictly farther than 1/8. This supplies the explicit witness rule

$$t(w)=\begin{cases}
1/8,&8\nmid w,\\
17/56,&8\mid w\text{ and }56\nmid w,\\
17/56+1/(8w),&56\mid w.
\end{cases}$$

The three cases exhaust every admissible positive integer w. For example, `w=56` gives `t=137/448`, while `w=112` gives `t=39/128`. The formula also supplies a directly checked witness for `w=56*10^12` without enumerating its meetings. The number of arithmetic operations is bounded; operations on larger integers still have larger bit costs.

The mechanism is concrete: **blocking both selected moments forces an arithmetic multiple large enough that the runner exits its blocking zone before the six-runner opening closes.** The escape delay scales as `1/w`, while the core's opening remains fixed.

## Counterchecks and limitations of the pattern

- **A slow enough runner really can cover I.** Speed 13 has the blocking interval `(31/104,33/104)`, which strictly contains I. But it leaves `t=1/8` valid. Width alone cannot finish the argument; the modular restriction matters.
- **Blocking both endpoints does not block the interior.** Speed 112 collides at both a and b, yet `t=39/128` is valid inside. Endpoint evaluations alone are not a coverage certificate.
- **A fixed finite list of rational times cannot work for every w.** A common multiple of their reduced denominators collides at every listed time. For our four times `{1/8,17/56,5/16,4/13}`, speed 1456 does exactly this; the adaptive formula still supplies a witness. In general choose a sufficiently large multiple to keep w distinct from the core.
- **This is existence, not a best-gap formula.** The displayed witnesses reach exactly 1/8 even when the configuration can do better. The earlier `w=8` case, for example, has its separately certified maximum 2/13.

These observations are exact consequences or deliberate nearby counterchecks, not patterns inferred from a large sample. They do not imply that a comparable positive-width opening exists for every choice of fixed speeds.

## Evidence and context

The script checks the core interval in two ways: exact interval intersection and the affine phase table above. It crosschecks the three reduced candidate witnesses against interval feasibility, verifies the finite residue classes modulo 8 and 7, and records nine prescribed diagnostic inputs. The unbounded conclusion rests on the written divisibility and interval arguments, not on those nine examples. No all-reference computation or broad speed search was run; independent proof review remains outstanding.

The interval-covering formulation is established mathematics. [Tao's 2017 exposition, S4](https://terrytao.wordpress.com/2017/01/10/some-remarks-on-the-lonely-runner-conjecture/), re-opened September 24, explicitly gives the constituent intervals. His radius formulation uses closed Bohr sets and counts moving speeds; ours uses open strictly-too-close sets at a fixed target and counts eight total runners. Its historical frontier is not used as current status. S8's previously recorded source notes concern related single-speed modifications; its HTML could not be retrieved again today, and no newly inspected claim from it is asserted.

Vance's contribution was to keep the inquiry centered on collective blocking beyond Fibonacci and authorize this infinite-family question. The AI contribution was the finite reduction, its modular sharpening, exact certificates, and counterchecks. This records the work performed here, not independent corroboration or a novelty claim.

One useful next question is what changes when **two** variable runners can share the blocking duty. The single-runner connected-interval argument then no longer suffices: different runners' windows may overlap and cover one another's gaps. That is a proposed next investigation, not work completed here.
