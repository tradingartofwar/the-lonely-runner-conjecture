# Arithmetic jumps select compatible safe laps

**September 28, 2026.** Baseline
`e76965fa484797c77d2b68411ef5aaa28ceb3e95`, on the existing research branch.
Material AI involvement: coordinator derivation and implementation, one
separately tasked mathematical reviewer with an independent threshold-event
implementation, and a shared follow-on deduction whose provenance is below.

**Outcome:** at threshold `1/8`, on a supplied closed window, the earliest
simultaneous safe time for two residual runners can be selected by at most
**four direct arithmetic projections**. A post-protocol deduction extends this to
three residual runners with at most **ten nested projections**. Useful lap
indices are computed from the shared time, however large those indices are.
No intervening laps need to be enumerated.

**Status:** bounded exact calculations are OBSERVED / internally REPRODUCED.
The general statements are HYPOTHESIS / supplied proof candidates under
repository governance, with separate AI challenge and external review still
outstanding. No literature novelty is asserted. These select a witness in a
given window; they do not prove that an arbitrary full runner configuration
must supply a successful window, or solve Lonely Runner.

## 1. Scope and what was already available

In the principal application there are eight common-start runners, selected
reference zero, and threshold `delta=1/8`. Suppose the other constraints are
already certified safe on a closed window `W=[L,R]`. There are either two or
three residual moving runners to handle. The selector answers whether W
contains a time safe for those remaining constraints, and returns its earliest
such time if it does. The total-runner threshold never changes when constraints
are temporarily omitted.

The auxiliary mathematical formulation allows arbitrary phases, positive real
speeds, and arbitrary real L. Our executable arithmetic uses exact rational
inputs. Phase-shifted and equal-speed diagnostics below are explicitly auxiliary,
not new common-start Lonely Runner configurations. A negative speed can be
replaced by its absolute value while also negating its phase; zero speed needs
a separate constant-constraint check and is outside the selector theorem.

The prior-work audit matters:

| Existing result | What it already answers | Remaining distinction here |
| --- | --- | --- |
| [Two-variable family](TWO_VARIABLE_SPEEDS.md) and [sparse transfer](TWO_SPEED_SPARSE_TRANSFER.md) | Selected-reference existence and a justified window dispatch in the fixed family | No additional family existence is claimed here |
| [Lap-band](LAP_BAND_COMPONENT_COUNT_2026_09_28.md) and [floor-sum](FLOOR_SUM_COMPONENT_COUNT_2026_09_28.md) counts | Count common blocking occurrences without enumerating every fast lap | The present query is earliest joint safety, not a component count or full duration |
| [Adaptive pair](ADAPTIVE_REFLECTED_PAIR_2026_09_28.md) | A speed-dependent witness formula in a special family | The selector below accepts arbitrary two-residual-runner inputs and a supplied window |
| [Fastest-core argument](FASTEST_CORE_CERTIFICATES_2026_09_27.md) | Exact local duration representation when residual blockers become intervals | It does not remove global core/window selection; neither does this selector |

The [preceding obstruction](FINITE_ANCHOR_OBSTRUCTION_2026_09_28.md) rules out
fixed menus with a fixed allowance of early laps. It leaves arithmetic selection
of distant lap labels open. This work addresses that precise opening.

## 2. A direct next-safe-time operation

For speed `v>0`, phase alpha, and `0<delta<1/2`, the safe lap labelled m is

`[(m+delta-alpha)/v, (m+1-delta-alpha)/v]`.

Define `P_v(t)` as the earliest safe time at or after t. The first lap whose
right endpoint is at least t has label

`m=ceil(v*t+alpha-1+delta)`.

Consequently

`P_v(t)=max(t,(m+delta-alpha)/v)`.

This is one ceiling calculation, not a search over lap labels. It includes
both safe endpoints. Two elementary facts drive the proof:

1. If u is a joint safe time and `u>=t`, then `u>=P_v(t)`. Applying a projection
   cannot skip a possible earlier joint witness.
2. `0<=P_v(t)-t<2*delta/v`. If the projection moves, it lands exactly at the
   left endpoint of a safe lap. The strict upper bound follows because unsafe
   intervals are open and have length `2*delta/v`.

The ceiling formula remains valid at negative times and phases, but no added
negative-time or phase grid was used to claim finite coverage.

## 3. Four projections are complete for two constraints

Let `0<a<=b`. Assume

`2*delta/b <= (1-2*delta)/a`.                                      (1)

Starting from L, apply the order

`a, b, a, b`.

After the first two projections, runner b is safe. If runner a is also safe,
the last two projections leave that time unchanged. Otherwise the second a
projection moves to the beginning of a fresh a-safe lap, whose length is
`(1-2*delta)/a`. The final b projection moves less than `2*delta/b`, so by (1)
it remains inside that same a-safe lap. Its output T is safe for both runners.

Every possible joint witness at or after L remained an upper bound on every
iterate. Since T is itself feasible, it is the **earliest** joint safe time.
No prior assumption that a witness exists was needed. Therefore the supplied
closed window is feasible exactly when `T<=R`.

Condition (1) is equivalently `delta<=b/[2(a+b)]`. The simpler uniform condition
`delta<=1/4` guarantees it for every ordered pair, including our threshold
`1/8`. This is a sufficient condition, not a necessary classification for each
individual phase arrangement.

A fourth projection can be necessary. At `delta=1/8`, common phases zero,
speeds `(1,8)`, and `L=7/8`, the outputs are

`7/8 -> 57/64 -> 9/8 -> 73/64`.

Speed eight is still blocked at the third output. The fourth is the earliest
joint safe time. Choosing a right endpoint below, equal to, or above `73/64`
checks empty-window, endpoint-only, and positive-component behavior.

## 4. What the exact controls show

The [frozen protocol](../reviews/2026-09-28-lap-projection/protocol.json)
contains 16 bounded physical pair/window cases, four valid auxiliary cases,
two negative scope controls, and one huge-speed formula-only case. Analytic
controls were constructed with expected outcomes; this is not held-out data
or a broad speed scan.

For the fixed core `{1,4,5,6,7}`, retain the existing windows

`I=[17/56,5/16]`, `K=[17/48,3/8]`, `H=[25/56,15/32]`.

The following table reports the first clipped component, not total duration:

| Residual speeds | I | K | H |
| --- | --- | --- | --- |
| 11,13 | empty | singleton 3/8 | empty |
| 11,16 | [17/56,39/128] | empty | [41/88,15/32] |
| 16,23 | empty | [17/48,47/128] | [25/56,15/32] |
| 3,8 | empty | empty | [25/56,15/32] |

These preserve the old tight, strict, cooperative-blocking, and empty-window
examples. They are not new existence coverage.

For the small-gcd controls, the supplied five-runner core is `{1,4,5,64,72}`
on `[65/512,79/576]`, obtained from the already used `1/8` anchor. The remaining
pair `(56,113)` yields `[57/448,119/904]`; `(56,112)` yields
`[57/448,17/128]`. Both recover previous certificates from direct lap selection.

The obstruction pair `(840,6720)` on I returns exactly
`[5443/17920,1089/3584]`. Replacing the fast speed by `8*10^12*840` still needs
only four projections and recovers the previously supplied later interval of
width `1/8960000000000000`. The fast lap is chosen by arithmetic at the slow
runner's safe entry; the skipped laps are never traversed.

The ratio-seven control `(840,5880)` has earliest component `{2041/6720}`.
The independent full-window reconstruction also finds positive components
later in that same I. Thus **an isolated first component does not imply zero
duration in the window**. The algorithm decides existence and the earliest
time. It does not compute the whole allowed set or classify all later components.

Across the 20 bounded pair cases, the separate threshold-event reconstruction
and primary selector agree on every earliest time, empty-window verdict, and
first clipped component: seven empty, four singleton-first, nine positive-first.
The huge formula-only case supplies one additional positive component; it is
excluded from the event-enumeration counts.

The auxiliary quarter-threshold control uses equal speeds one and phases
`0,1/2`: its first safe point is `1/4`, isolated. At threshold `1/3`, outside
the hypothesis, those two safe sets are disjoint. Four projections end at
`11/6`, which is unsafe for the first runner. This preserves the threshold
restriction rather than extrapolating beyond it.

## 5. Post-protocol deduction: ten projections for three runners

The frozen negative control already showed that simply making two increasing-
speed sweeps through three runners can fail. For `(1,7,8)`, phases zero,
`delta=1/8`, and `L=7/8`, the order `1,7,8,1,7,8` ends at `73/64`.
Runner seven's phase is `63/64`, so it is blocked.

After that protocol was frozen, the coordinator proposed a waiting-time bound
and nested repair. The reviewer supplied a shorter proof of the bound and
independently checked the deduction. The original failed sweep is retained;
this section and its [separate protocol](../reviews/2026-09-28-lap-projection/follow_on_protocol.json)
are explicitly follow-on work.

For a pair satisfying (1), **at most one of the two a projections moves**.
If the first moves, it begins a fresh a-safe lap; the following b projection
cannot leave it, and the second a projection is stationary. If the first is
stationary, only the second could move. Their combined advance is therefore
less than `2*delta/a`. The two b advances together are less than `4*delta/b`.
The pair's earliest shared safe time is thus less than

`2*delta/a + 4*delta/b`

after its starting time. This conservative bound is not an exact worst-case
formula.

Now order three speeds `0<a<=b<=c`, and let `S_bc` be the earliest-safe selector
for the pair b,c. Its advance is less than

`D=2*delta/b+4*delta/c`.

Assume that the b,c pair satisfies (1) and `D<=(1-2*delta)/a`. Apply

`P_a, S_bc, P_a, S_bc`.

If the first pair result is a-safe, it is already a triple witness. Otherwise
the second a projection starts a fresh a-safe lap; the last pair operation
cannot leave it because its advance is less than D. The final time is feasible
for all three. The same witness-preservation argument proves it is earliest.

At our threshold `delta=1/8`, speed ordering guarantees both conditions:

`D=1/(4b)+1/(2c) <= 3/(4a)`.

The right side is exactly the a-safe lap width. Expanding the two pair calls
gives at most ten scalar projections, in order

`a, b, c, b, c, a, b, c, b, c`.

On the same frozen `(1,7,8)` countercontrol, this nested order returns `65/56`,
the earliest time independently found by threshold reconstruction. The clipped
first component on `[7/8,6/5]` is `[65/56,6/5]`. There are no new input cases
in this follow-on calculation. Its one exact diagnostic checks the implementation;
the unbounded conclusion rests on the argument above.

## 6. What has been gained, and what remains open

This supplies a complete arithmetic witness selector for **two or three
residual constraints at threshold 1/8 on a supplied core-safe window**. The
core need not be the particular fixed speeds used in our physical controls:
only its certified safety throughout the window is used. A failed test now
means the supplied closed window is actually empty, rather than merely that
an early-lap itinerary failed. It still says nothing against loneliness in
another window.

The relational structure exposed here is a shared lower bound on time, updated
by each constraint, together with a bound on how far the remaining constraints
can push that time. A fresh safe lap gives enough room for the next operation.
For three runners, grouping two as an earliest-joint-safe operation preserves
that guarantee; a naive sweep does not. This is not a new invariant or a claim
that speeds alone lack the required information.

Four or ten counts **arithmetic projections**, not bit operations or runtime.
Large rational multiplication, ceiling, and comparison still depend on input
bit length. The selector does not calculate total safe duration, enumerate all
components, pick the other runners' core-safe windows, certify all references,
or establish a new family of Lonely Runner existence results. No originality
assessment or general conjecture solution is claimed.

**Next bounded question:** where does the waiting-room argument break with a
fourth residual runner at threshold 1/8? Test the composition's sufficient
speed condition before assuming another bounded number of sweeps works. Use
the existing four-blocker controls and preserve a failed condition separately
from an empty window. Audit earlier four-blocker and fastest-core results
before introducing another selector. Arbitrary-configuration certificate
existence remains the larger open problem.

## Reproduction

From the checkout root, with the Python standard library:

```bash
python -B reviews/2026-09-28-lap-projection/primary.py --check
python -S -B reviews/2026-09-28-lap-projection/verify.py
python -B reviews/2026-09-28-lap-projection/follow_on.py --check
python -B reviews/2026-09-28-lap-projection/compare.py
```

The [review](../reviews/2026-09-28-lap-projection/review.md) and
[independent verifier](../reviews/2026-09-28-lap-projection/verify.py) were
derived without importing primary code or results. They reconstruct every
bounded threshold cell and endpoint, independently check the supplied core
windows, and use lifted inequalities for the huge input. The comparison checks
the actual saved records, including all seven huge-input lifted bands and the
post-protocol ten-step trace. Manifest hashes preserve the artifacts.

Hourly research remains paused. No broad speed or phase scan, all-reference
campaign, outside outreach, paid compute, main merge, or parked `+7/+9` work
was started.
