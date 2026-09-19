# Mathematical baseline and checker specification

**Status:** Standard formulation plus proposed exact-checking design. No production checker or research dataset has been implemented in this repository.

## Fix the notation

Let `n >= 2` be the total number of runners, with distinct constant velocities `s0,...,s(n-1)` and a common starting point on a track of circumference 1. For a selected reference runner `r`, write the `k=n-1` nonzero relative velocities as `ui=si-sr`.

Use circular arc distance, not chord length:

$$\|x\|=\min_{m\in\mathbb Z}|x-m|.$$

The reference runner's nearest-neighbor distance is

$$f_r(t)=\min_{i\ne r}\|(s_i-s_r)t\|.$$

The conjecture is `for every velocity configuration, for every r, there exists t>0 with f_r(t)>=1/n`. The time may depend on `r`. It does not ask for all runners to be lonely simultaneously. Negative velocities are allowed; equal original velocities are excluded.

The standard reduction permits work with positive integer speeds relative to a stationary runner [S1, S4](SOURCES.md). Do not approximate arbitrary irrational inputs by decimals and call that reduction proved. The initial implementation accepts integers or exact rationals; rational denominators can be cleared by rescaling time.

## Exact objective and normalization

For positive integer relative speeds `V`, set

$$L(V)=\max_{0\le t\le1}\min_{v\in V}\|vt\|.$$

The period 1 suffices in these normalized units. The target is `L(V)>=1/n`. A tight input reaches equality; a numerically close value is not necessarily tight.

- Permuting constraints or changing their signs does not change the minimum distance function.
- Dividing all integer relative speeds by their gcd preserves `L` and rescales witness time: if `u=g*v`, normalized time `tau` maps to original time `tau/g`.
- Keep the full time-scaling map if rational denominators were also cleared.
- Opposite relative velocities can become duplicate absolute speeds. A checker may deduplicate identical constraints, but must retain the original `n` and its target `1/n`. The number of stored constraints is not a new runner count.
- Adding a constant to **all original velocities** preserves relative motion. Adding it only to the relative speeds while keeping the reference stationary generally does not preserve `L`.
- Gcd 1 does not imply that the smallest speed is 1. Do not silently restrict searches to tuples beginning with 1.

## Method A: exact feasibility at a chosen threshold

For an integer `v>0` and rational threshold `0<delta<=1/2`, all allowed times in `[0,1]` are

$$A_v(\delta)=\bigcup_{j=0}^{v-1}\left[\frac{j+\delta}{v},\frac{j+1-\delta}{v}\right].$$

This follows directly by writing the fractional part of `vt` and requiring it to lie in `[delta,1-delta]`. Intersect the finite unions across speeds using exact rationals. Preserve closed endpoints and zero-width intervals. A nonempty intersection supplies a witness; an empty intersection certifies infeasibility for this input and threshold, assuming the implementation is correct.

For example, `V=(1,2)` at `delta=1/3` leaves precisely `t=1/3` and `t=2/3`. Their total interval length is zero, but both are valid. Therefore neither zero measure nor a grid that misses equality is evidence of a counterexample.

## Method B: exact maximum via piecewise-linear segments

Independently compute `L(V)` for small inputs:

1. Partition `[0,1]` at every `m/(2v)`, for each `v` and `m=0,...,2v`. These are the corners of the triangular distance curves.
2. On each resulting interval, express every distance curve as an affine function with exact coefficients.
3. Include the interval endpoints and all pairwise affine intersections inside it. Parallel or coincident pieces need no additional crossing point.
4. Evaluate the minimum over **all** speeds at every candidate time; take the largest value.

Why this is complete: between corners and pairwise crossings, the ordering of all affine pieces is fixed, so their minimum is affine and reaches its maximum at an endpoint (or is constant). All candidate coordinates and values are rational. This is an elementary derivation for our checker design, not a claimed new theorem.

The naive method grows with the sum of speeds and the number of constraints. It is a correctness oracle for small cases, not an assumed frontier-scale algorithm. Agreement with Method A at, below, and above its computed maximum is a required crosscheck.

## Planned regression fixtures

Here `V` contains the relative speeds; `n` is stated independently.

| Input | Expected result | Purpose |
| --- | --- | --- |
| `V=(1)`, `n=2` | `L=1/2`, witness `t=1/2` | Simplest case |
| `V=(1,2)`, `n=3` | `L=1/3`; equality times `1/3,2/3` | Singleton intervals |
| `V=(1,3)`, `n=3` | `L=1/2`, witness `t=1/2` | Non-tight comparison |
| `V=(1,2,3)`, `n=4` | `L=1/4` | Consecutive-speed fixture |
| `V=(1,3,4,7)`, `n=5` | `L=1/5` | Known nonconsecutive tight fixture, S1 |
| `V=(2,4)`, `n=3` | `L=1/3`, witness `t=1/6` | Time rescaling |
| Original `(0,1,2)`, reference speed `1` | Relative `(-1,1)`, `L=1/2`, target still `1/3` | Reference change and duplicate constraints |
| `V=(1,2)`, artificial `delta=2/5` | Empty feasible set | Negative test, not a conjecture counterexample |

Also test input rejection, permutations, sign changes, rational scaling, all reference runners, and exact-threshold neighbors. During document QA on September 19, temporary exact-rational calculations checked the listed maxima, the two singleton equality times, and the artificial infeasible threshold. The repository's production checker and regression suite have not been built; this spot check is not a research search.

## What an output would establish

A passing witness certifies one reference runner in one case. To certify an entire configuration, check every reference runner. To prove a fixed-runner theorem by computation, one needs a valid finite reduction, every required case, and independently checkable computation. A bounded atlas has none of that broader force by itself.
