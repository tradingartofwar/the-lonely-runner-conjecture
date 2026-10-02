# Four affine fast speeds above a fixed core: request for mathematical review

**Version 1 — September 24, 2026. Status: HYPOTHESIS / proof candidate.**

This note presents one restricted claim from an ongoing Lonely Runner investigation. It asks for scrutiny of the argument and its relation to existing literature. Independent review is pending; originality is unestablished. It makes no claim to solve the full conjecture.

Vance directed the investigation and its counterexample-driven questions. AI materially generated the argument, implementation, and this draft. The recorded checks are internal diagnostics, not independent proof certification.

**Review location:** [pull request #3](https://github.com/tradingartofwar/the-lonely-runner-conjecture/pull/3). Please identify this note's version and the step being reviewed. Its reproducible code and evidence baseline is [commit 25f8352](https://github.com/tradingartofwar/the-lonely-runner-conjecture/tree/25f8352944700a3060dab03dc42a75e23524a5c4).

## 1. Precise claim

Write ||y|| for the distance from a real number y to its nearest integer. There are eight runners on a unit circle, all starting together. Select the stationary runner of speed 0 as reference. The other speeds are

$$c_1,c_2,c_3,\quad b_1q+a_1,\ldots,b_4q+a_4.$$

Assume:

- The core speeds c_1,c_2,c_3 are distinct positive integers.
- Each b_i is a positive integer and each a_i is an integer.
- The four ordered pairs (b_i,a_i) are distinct.
- All these coefficients stay fixed as the positive integer q varies.

**Proposed proposition.** There is an integer Q such that, for every integer q>=Q, the eight speeds are distinct and the selected runner has a nonempty open interval of times on which its distance from every other runner is strictly greater than 1/8.

The threshold is determined by the total of eight runners; it remains 1/8 when considering subgroups. Equality counts in the original problem, but this proposition seeks strict separation. Q may depend on every fixed coefficient. The claim is about reference 0, not an all-reference conclusion.

## 2. Proposed proof

### Step A: the core leaves an open opportunity

In one unit time period, each positive integer core speed blocks a set

$$\{t:\|c_jt\|<1/8\}$$

of measure 1/4. The union of the three blocked sets therefore has measure at most 3/4. The core's allowed set has measure at least 1/4. It has finitely many boundary points, so removing all equality times leaves at least one nonempty open interval J inside (0,1) where every core distance is strictly above 1/8.

### Step B: a lowest-frequency coefficient prevents persistent tiling

Temporarily let x be a separate phase coordinate. At a fixed slow time t, define

$$B_i(t)=\{x\in\mathbb R/\mathbb Z:\|b_ix+a_it\|<1/8\},\qquad
M_t(x)=\sum_{i=1}^4{\bf1}_{B_i(t)}(x).$$

Each B_i has measure 1/4, because b_i is a positive integer. Thus the integral of M_t over the phase circle is exactly 1.

If the clear phase set {x:M_t(x)=0} has measure zero, then M_t>=1 almost everywhere. Its integral forces M_t=1 almost everywhere. In particular, all its nonzero Fourier coefficients must vanish. This assertion does not discard isolated equality points.

Use the convention

$$\widehat f(k)=\int_0^1 f(x)e^{-2\pi ikx}\,dx,\qquad b_*=\min_i b_i.$$

The indicator of B_i has period 1/b_i. Splitting the integral into b_i translates gives zero at frequency k unless b_i divides k. Consequently all terms with b_i>b_* vanish at frequency b_*.

For b_i=b_*, direct substitution gives

$$\widehat{{\bf1}_{B_i(t)}}(b_*)
=e^{2\pi ia_it}\int_{-1/8}^{1/8}e^{-2\pi iy}\,dy
=\frac{\sqrt2}{2\pi}e^{2\pi ia_it}.$$

Therefore

$$\widehat M_t(b_*)=\frac{\sqrt2}{2\pi}P(t),\qquad
P(t)=\sum_{i:b_i=b_*}e^{2\pi ia_it}. \tag{1}$$

P(0) is the positive number of terms in this sum. Multiplying P by an appropriate exponential makes it a nonzero polynomial in z=e^{2πit}: the exponents a_i are integers, including any negative ones. Hence P has only finitely many zeros for t in [0,1).

At every other t, equation (1) contradicts M_t=1 almost everywhere. There must be positive clear phase measure. A unique smallest b_i is a useful special case: |P(t)|=1 at every t.

### Step C: select a strict auxiliary point

Choose rational t0 in J outside the finite zero set of P. Each B_i(t0) has finitely many endpoints. Positive clear measure therefore contains an open phase interval after those endpoints are removed. Choose rational x0 in that interval, with 0<x0<1.

This gives positive margins

$$\mu_C=\min_j\|c_jt_0\|-1/8,\qquad
\mu_F=\min_i\|b_ix_0+a_it_0\|-1/8.$$

The actual runners do not have an independently adjustable x. Their common-start trajectory satisfies x=qt modulo 1. Step D must bridge that distinction.

### Step D: realize the point at a nearby actual time

Let M=max_j c_j, A=max_i|a_i|, and choose eta>0 such that (t0-eta,t0+eta) is contained in J. For each positive integer q set

$$m_q=\lfloor qt_0-x_0+1/2\rfloor,\qquad
t_q=(m_q+x_0)/q.$$

Then |t_q-t0|<=1/(2q). Since distance to the nearest integer is 1-Lipschitz,

$$\|c_jt_q\|\geq1/8+\mu_C-M/(2q).$$

For the fast speeds,

$$(b_iq+a_i)t_q=b_im_q+b_ix_0+a_it_q.$$

The term b_i*m_q is an integer. It disappears from the distance calculation, so

$$\|(b_iq+a_i)t_q\|\geq1/8+\mu_F-A/(2q). \tag{2}$$

In particular, the error in (2) depends on the fixed offsets, not the large winding term. Every integer q satisfying

$$q>\max\left(M+A,\;2A,\;\frac{M}{2\mu_C},\;
\frac{A}{2\mu_F},\;\frac1{2\eta}\right) \tag{3}$$

has t_q in J with all seven distances strictly above 1/8. The first bound puts the extra speeds above the core. The second separates extra speeds with different b_i; equal b_i have different a_i by assumption. Positivity follows as well.

Continuity gives an open interval around t_q. Taking Q to be one plus the floor of the right-hand side of (3) completes the proposed implication.

## 3. One exact witness and the finite evidence

For core (1,4,5) and coefficient pairs (1,0),(2,1),(3,5),(4,7), the recorded choices are

$$t_0=21/64,\quad x_0=875/1536,\quad
\mu_C=3/16,\quad\mu_F=115/512.$$

One may use eta=3/64 inside the core opening J=(9/32,3/8). The largest bound in (3) is 1792/115, giving the sufficient integer cutoff Q=16.

At q=16, the actual speeds are

$$0,1,4,5,16,33,53,71.$$

At t=8555/24576 their minimum distance from reference 0 is exactly 6377/24576>1/8. This witness can be checked without our repository code:

```python
from fractions import Fraction as F

t = F(8555, 24576)
speeds = (1, 4, 5, 16, 33, 53, 71)
phases = [(v * t) % 1 for v in speeds]
minimum = min(min(x, 1 - x) for x in phases)
assert minimum == F(6377, 24576) > F(1, 8)
print(minimum)
```

The archived diagnostics contain three prescribed families and four parameter values per family: one below the sufficient cutoff, the cutoff, one above it, and twice it. All twelve witnesses have exact interval certificates. Six auxiliary phase reconstructions and sixteen actual allowed-set boundary reconstructions agree by separately structured routines. The existing 25 software tests also pass.

These are finite internal checks. They do not prove Steps A–D for every permitted input. The computed profiles use nonnegative offsets; the written argument additionally allows negative offsets through A=max|a_i|.

## 4. Counterchecks that a review should retain

| Tempting inference | Recorded control |
| --- | --- |
| An auxiliary safe point is already an actual safe time. | In the old family q,q+1,q+5,q+7 with core (1,4,5), the rounding formula at q=6 gives a blocked time. The sufficient-range assumption matters. |
| Vanishing of the coefficient in (1) implies no phase opening. | At t=1/8, positions x,x+4t,2x+3t,2x+6t have P(t)=0 but clear phase length 1/8. Cancellation is necessary for tiling, not sufficient. |
| Zero clear measure means no valid phase. | Replace 2x+6t by 2x+5t at t=1/8. Clear phase measure is zero, but six isolated equality phases remain. |
| Increasing all speeds eventually gives strict room. | Speeds (0,q,2q,...,7q) remain exactly tight by time rescaling. The fixed-core hypothesis cannot simply be removed. |

The recorded controls and their full assumptions are in [the development note](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/25f8352944700a3060dab03dc42a75e23524a5c4/notes/FAST_CLUSTER.md), Sections 7–11.

## 5. Reproduce the pinned calculations

Python 3.10 or later; the exact calculation and tests use the standard library. Use a fresh checkout:

```bash
git clone https://github.com/tradingartofwar/the-lonely-runner-conjecture.git
cd the-lonely-runner-conjecture
git checkout --detach 25f8352944700a3060dab03dc42a75e23524a5c4
python -m scripts.analyze_affine_family
python -m unittest discover -s tests -v
```

The analysis regenerates [experiments/affine_family.json](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/25f8352944700a3060dab03dc42a75e23524a5c4/experiments/affine_family.json) from the [script](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/25f8352944700a3060dab03dc42a75e23524a5c4/scripts/analyze_affine_family.py). It records source hashes, exact witness intervals, complete zero-duration allowed sets, and compact hashes/summaries of the positive-duration unions compared in memory. Running it again is reproduction of this implementation, not by itself independent mathematical review.

## 6. Literature and review questions

Jain and Kravitz, *Relative Lonely Runner spectra*, [arXiv:2411.12684v2](https://arxiv.org/html/2411.12684v2), December 9, 2024, supplies a relevant two-dimensional-subtorus framework. Its Theorem 1.1 concerns relative spectra up to finitely many exceptions; Section 1.4 connects it to fast-runner limits. We inspected the statement and proof outline, not the full proof. We do not attribute the sufficient bound (3) or originality to that paper.

Our own coordinate mapping is

$$U=\{(c_1t,c_2t,c_3t,b_1x+a_1t,\ldots,b_4x+a_4t)\pmod1\}.$$

The actual trajectories have x=qt. Determining whether the proposed proposition or its mechanism is already known, or immediately follows from existing results, is part of the requested review. Further source-reading limits are in [SOURCES.md](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/25f8352944700a3060dab03dc42a75e23524a5c4/notes/SOURCES.md).

Useful review responses would address:

1. **Fourier calculation:** is the frequency selection and phase sign in Step B correct for all permitted coefficients?
2. **Existence of a strict point:** does finite polynomial cancellation justify Step C without losing equality cases or imposing an unstated genericity assumption?
3. **Actual-time transfer:** does Step D control every error, including negative offsets, distinctness, and the strict cutoff?
4. **Scope:** is a fixed hypothesis being used where a varying quantity was intended?
5. **Prior art:** what published result contains or implies this statement, or provides a simpler proof?

A response can identify a gap without finding a counterexample to the proposition. A finite example below the sufficient cutoff is not a counterexample. A counterexample to a claimed uniform sufficient range must satisfy the hypotheses and the bound; a counterexample to eventual strictness must defeat every sufficiently-large-q cutoff for one fixed set of coefficients.

Please distinguish mathematical correctness, reproducibility, and novelty in feedback. Comments on PR #3 can cite the step and exact parameters; corrections may also be submitted as pull requests under [CONTRIBUTING.md](../CONTRIBUTING.md). Review status should change only when the actual review and its scope are recorded.
