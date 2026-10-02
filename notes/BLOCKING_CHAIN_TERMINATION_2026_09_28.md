# What a continuing blocking chain consumes

September 28, 2026. Baseline: `dd5b3bce9a7a3fb22474a724161438f24e35fb41`.

**Result:** a supplied proof candidate bounds the number of advancing next-safe
projections for four common-start integer-speed constraints at threshold
`delta=1/8`. Repeating the existing selector therefore has a justified,
speed-dependent stopping bound. The bound can be extremely loose. Whether a
speed-independent bound exists remains **OPEN**.

**Evidence:** the general argument is **HYPOTHESIS / proof candidate**, with
material AI derivation and internal mathematical challenge, pending external
review. Exact replays are **OBSERVED** only on the twelve frozen window cases.
No novelty, full Lonely Runner proof, new family existence coverage, or
all-reference result is claimed. The prior unconditional 22-call guarantee
remains **DISPROVEN**; seven advances in its counterexample do not establish a
universal seven-advance or 23-call repair.

## 1. Question and prior work

The [fourth-runner study](FOUR_RUNNER_PROJECTION_LIMIT_2026_09_28.md) found a
common-start integer example where two eleven-call rounds end unsafe. A chain
of seven open blocking occurrences explains why, and its last endpoint is the
actual first witness. The next question was what controls continued chains.

Two existing ingredients must be credited precisely:

- [Blocking chains](BLOCKING_CHAINS.md) already represent occurrences with
  strict overlaps and increasing right endpoints. Mere touching preserves a
  possible equality witness.
- [Overlap placement, Section 8](OVERLAP_PLACEMENT.md) already defines the
  centered blocking primitive with range `[-3/32,3/32]`, and earlier sections
  use the per-runner discrepancy allowance `3/(16v)`.

The proposed additional implication here charges successive selected
occurrences against that existing discrepancy allowance, using an arithmetic
lower bound on every positive overlap. This is not a newly discovered
primitive. Existing exact interval methods already decide bounded windows;
finite decidability itself is not a new existence result.

## 2. Four blockers give an exact excess-coverage potential

Let the four residual speeds be positive and let their phases be `alpha_i`.
An occurrence is the **open** interval

\[
I_{i,m}=\left(\frac{m-1/8-\alpha_i}{v_i},
                 \frac{m+1/8-\alpha_i}{v_i}\right).
\]

Write `M(t)` for the number of residual constraints blocking time t. Each
runner has blocking duty `1/4`. For `0<=x<=1`, define

\[
h(x)=\min(x,1/8)+\max(0,x-7/8)-x/4,
\qquad
H(t)=\sum_{i=1}^{4}\frac{h(\{v_it+\alpha_i\})}{v_i}.
\]

The function h is continuous and periodic, with minimum `-3/32` and maximum
`3/32`. Away from thresholds,

\[
H'(t)=M(t)-1.
\]

On any continuously blocked segment `[A,B]`, integration gives

\[
\int_A^B(M(t)-1)\,dt=H(B)-H(A)
\leq \mathcal B:=\frac3{16}\sum_i\frac1{v_i}. \tag{1}
\]

The integral counts **excess coverage**: double coverage contributes once,
triple coverage twice, and quadruple coverage three times. A sum of pairwise
overlaps would instead count triple coverage three times and is not the same
quantity. Threshold points have measure zero in this identity; their exact
safety is preserved separately in the algorithm.

Thus a connected blocked chain has a finite allowance for overlap. The
identity alone does not bound the chain's elapsed duration: a segment covered
exactly once consumes no excess allowance.

## 3. Charging each advancing move

The next-safe projection is

\[
m=\lceil vt+\alpha-7/8\rceil,
\qquad P_{v,\alpha}(t)=\max\left(t,\frac{m+1/8-\alpha}{v}\right).
\]

A nonzero move starts strictly inside one blocked occurrence and ends at its
right endpoint. The next nonzero move starts at that endpoint, strictly inside
another occurrence. Consecutive selected intervals therefore overlap by
positive length and their right endpoints strictly increase. No occurrence
can be selected twice.

Suppose every positive overlap has length at least `eta>0`. For N selected
occurrences their union U is one open interval. Each interval after the first
overlaps the previous union by at least eta, even if it extends its left end.
The union-length identity yields

\[
(N-1)\eta\leq\sum_{j=1}^N|I_j|-|U|
\leq\int_U(M(t)-1)\,dt\leq\mathcal B. \tag{2}
\]

The middle comparison holds because the actual multiplicity includes every
selected occurrence, plus any unselected ones. This proves a bound on every
finite prefix without assuming that a later witness already exists.

For **positive integer speeds with common phases zero**, put

\[
Q=\max_{i<j}\operatorname{lcm}(v_i,v_j),\qquad \eta=\frac1{8Q}.
\]

Endpoints of two runners lie on the pair's lattice of spacing
`1/(8 lcm(v_i,v_j))`. A positive overlap is therefore at least eta. Containment
also satisfies this bound: a whole blocked occurrence has width `1/(4v_i)`.
Occurrences of one runner are disjoint. Consequently

\[
\boxed{N\leq K_{\rm global}:=
\left\lfloor1+\frac{3Q}{2}\sum_i\frac1{v_i}\right\rfloor.} \tag{3}
\]

This counts **nonzero scalar advances**, not every projection call, number of
laps skipped, elapsed time, or arithmetic bit operations. The formula is
unchanged if all integer speeds are multiplied by the same positive integer.
It does not silently extend to arbitrary real speeds or shifted phases;
those settings need their own positive overlap quantum.

## 4. Keeping the actual starting phases

Let L be the starting time, `m_L=M(L)` with equality counted safe, and

\[
H_{\max}=\frac3{32}\sum_i\frac1{v_i}.
\]

At most `m_L` selected occurrences can contain L. Every other selected
occurrence begins at or after L and contributes at least eta of incremental
overlap inside `[L,T]`, where T is the last selected right endpoint. An
occurrence beginning exactly at L is included in this latter group; its
positive overlap lies to the right of L. Therefore

\[
(N-m_L)\eta\leq H(T)-H(L)\leq H_{\max}-H(L),
\]

and

\[
\boxed{N\leq K_{\rm phase}:=m_L+
\left\lfloor\frac{H_{\max}-H(L)}{\eta}\right\rfloor.} \tag{4}
\]

The envelope `H_max` need not be simultaneously attainable by all runners.
Use `K=min(K_global,K_phase)`. If L is already safe for all four, return L
immediately regardless of the numerical bound.

This addresses the relational-information inquiry in a concrete way. The
single-runner primitives are familiar, but the useful constraint combines
their phases on one clock with the order and strict overlaps of selected
occurrences. The sum's endpoint change describes what the entire blocked
chain can afford. It does not assign a decisive invariant to one runner or
claim that one scalar classifies all full configurations.

## 5. Termination and the supplied-window distinction

Retain the ordered speeds `a<=b<=c<=d` and repeat the prior eleven-call round

`a,b,c,d,c,d,b,c,d,c,d`.

A round beginning unsafe makes at least one nonzero move: if all calls were
stationary, every constraint visited in the round would already be safe.
Testing safety after each round therefore stops within K rounds, at most
`11K` scalar calls. The argument needs only that each round visits all four
constraints; it does **not** depend on assuming the preceding triple-selector
theorem. An arbitrary fair order without bounded delays has the same bound on
advances, but no resulting bound on all calls.

Each next-safe projection preserves every possible later joint witness as an
upper bound on its output. The verified safe terminal time is consequently
the earliest residual-safe time at or after L. On a supplied closed core-safe
window `[L,R]`, there are two valid exits:

1. A verified jointly safe time `T<=R` is the earliest full witness in the
   window.
2. Any iterate `T>R` certifies that this window is empty. It need not be a
   full witness, and the core need not stay safe beyond R.

The primary replay checks `T>R` after every scalar call and safety at complete
round boundaries. It therefore may execute stationary calls after reaching
its eventual witness. That distinction is visible in the recorded costs.

There are seven moving constraints in the full eight-runner problem. Applying
the same potential to all seven at threshold 1/8 gives `H'=M-7/4`, which can
be negative even while a time is blocked. The nonnegative excess-coverage
argument (2) then fails. The four-residual result does not force its terminal
time into a core-safe window, so it does not close the general conjecture.

## 6. Frozen exact checks and cost limits

The [protocol](../reviews/2026-09-28-chain-termination/protocol.json) reuses the
eight old physical controls, the two preceding common-phase auxiliary
fixtures, and both the clipped and extended windows of the one existing
common-start lift. This is twelve window records, nine distinct full physical
configurations and two auxiliary four-constraint inputs. No new speed scan or
physical configuration was added; these cases are not held-out validation.

| Reused case | Advancing moves | Scalar calls | Phase bound on moves | Result |
| --- | ---: | ---: | ---: | --- |
| doubling 112 | 1 | 11 | 45 | first witness `145/512` |
| small-gcd 113 | 3 | 22 | 400 | first witness `129/448` |
| tight 13 | 4 | 22 | 62 | equality witness `3/8` |
| control 8/11 | 1 | 11 | 34 | first witness `17/56` |
| affine 309 | 1 | 11 | 1557 | first witness `697/2472` |
| affine 310 | 2 | 11 | 1064 | first witness `467/1656` |
| affine 320 | 1 | 11 | 1255 | first witness `721/2560` |
| strict 16 | 1 | 11 | 69 | first witness `17/56` |
| auxiliary strict | 3 | 22 | 20 | first witness `73/64` |
| auxiliary equality | 1 | 11 | 34 | right endpoint `1/120` |
| lifted clipped window | 7 | 23 | 475427840573787 | empty window |
| same lift, extended window | 7 | 33 | 475427840573787 | right endpoint `163489640070647/490466743069080` |

The primary records 32 advancing moves and 199 calls in total. For the extended
lift, the witness is reached at call 23; the remaining ten calls are stationary
before the prescribed round-end safety test. The clipped case exits empty at
call 23 because that same time exceeds its R. This certifies the two specified
windows, not emptiness of the entire old core window J.

In the large lift the global bound is `887654400674673`, while the phase bound
is `475427840573787`. Both dwarf the seven actual moves. The useful result is
termination and an exact accounting relation, not a practical worst-case
performance guarantee or evidence that long chains of those lengths exist.

Reproduce from the repository root:

```bash
python reviews/2026-09-28-chain-termination/primary.py
python reviews/2026-09-28-chain-termination/verify.py
python reviews/2026-09-28-chain-termination/compare.py
```

The independently structured verifier receives the protocol inputs, without
reading primary code or outputs. It reconstructs threshold-event safe sets,
uses direct phase cases for projection traces, and integrates multiplicity by
clipping explicit occurrences. The comparison checks traces, earliestness,
empty-window decisions, strict chains, potential differences and both bounds.
See the [review record](../reviews/2026-09-28-chain-termination/review.md) for
final counts and the limitations of internal AI review.

## 7. What remains unresolved

The structural challenger did not construct a family requiring arbitrarily
many rounds. A naive repeated four-interval construction fails: one occurrence
from each ordered runner has total width at most the slow runner's period,
and strict overlaps consume part of that width. Connecting successive slow
occurrences therefore needs additional fast occurrences.

The [structural note](../reviews/2026-09-28-chain-termination/structural.md)
also supplies a general finite-certificate lift. Any suitable rational
auxiliary chain with strict endpoint comparisons can be realized, after a
sufficiently large explicit scaling, by common-start integer speeds inside
the `{1,4,5}` core window. It does not preserve arbitrary cross-runner equality
ties and does not supply a long chain by itself. This ancillary argument is
also a proof candidate, with no new computed physical input.

**Next structural question:** does the required occurrence order impose a
speed-independent bound, or can one write a parameterized, strictly compatible
chain that forces arbitrarily many advances or rounds? These are distinct cost
questions; a long arbitrary covering chain need not be the selector's actual
itinerary. Any construction must specify that itinerary and its necessary
endpoint comparisons, then address common-start realization. Do not infer
unbounded behavior merely from a growing upper bound or tiny possible
overlaps. The separate global question of a successful core window remains
open. Hourly research stays paused.
