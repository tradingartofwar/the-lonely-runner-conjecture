# Independent challenge: four safe-set projections

September 28, 2026. Baseline supplied by coordinator:
`e76965fa484797c77d2b68411ef5aaa28ceb3e95`.

The reviewer independently derived the argument and the controls below before
reading the coordinator's implementation or results. This is a separate AI
mathematical challenge and implementation, not external proof certification.
No novelty or full Lonely Runner proof claim is made. The unbounded conclusion
remains a supplied proof candidate under the repository's governance.

## Statement and verdict

Let `0<a<=b`, let the phases be arbitrary real numbers, and let
`0<delta<1/2`. A runner of speed v is safe when
`||v*t+alpha_v||>=delta`. Let `P_v(t)` be its earliest safe time at or after t.
If

`2*delta/b <= (1-2*delta)/a`,

then `P_b(P_a(P_b(P_a(L))))` is the earliest simultaneous safe time at or
after any real L. In particular, the condition holds for every ordered pair
when `delta<=1/4`.

I found no defect in this claim. It applies to a supplied closed window
`[L,R]`: simultaneous safety occurs there if and only if the returned time is
at most R. It permits a singleton witness. Positive duration is a separate
question.

The arbitrary-phase statement is explicitly an auxiliary extension. The
original Lonely Runner setting retains a common start. Positive relative
speeds are assumed here; a negative relative speed can be converted to a
positive one only by also negating its phase. Zero relative speed requires a
separate constant-constraint check and is outside the statement above.

## Independent derivation

A speed-v safe occurrence is the closed interval

`[(m+delta-alpha_v)/v, (m+1-delta-alpha_v)/v]`.

The first occurrence whose right endpoint is at least t has index
`m=ceil(v*t+alpha_v-1+delta)`. Its first point at or after t is the larger
of t and its left endpoint. This proves the proposed ceiling formula even
for negative t, negative phase, and exact endpoint equality.

The projection is nondecreasing and never moves backward. More directly,
if u is simultaneously safe and u>=t, then `P_v(t)<=u`. Thus every projection
preserves every still-possible joint witness as an upper bound; no earlier
joint witness is skipped.

Put `t1=P_a(L)` and `t2=P_b(t1)`. If t2 is a-safe, it is already jointly
safe and the remaining projections fix it. Otherwise `t3=P_a(t2)>t2` is
exactly a lower endpoint of an a-safe interval. That interval has length
`(1-2*delta)/a`.

Every b-projection moves by less than `2*delta/b` when it moves at all:
the unsafe components are open intervals of that length, and both bordering
points are safe. Therefore the final b-projection remains within the same
closed a-safe interval under the stated inequality. Its output is jointly
safe. Since every potential earlier joint witness bounded all four iterates
from above, the output is the earliest one. No assumption that a common
witness already exists was used.

The sharper condition is `delta<=b/(2*(a+b))`. The uniform `1/4` bound is
sufficient, not claimed necessary for a particular phase/input. Arithmetic
operation count is at most four projections; exact integer/rational bit costs
still depend on the inputs. This is not a general constant-time claim in bit
complexity.

## Analytically chosen controls

These controls were proposed to the coordinator before new computation. They
are isolated scope checks, not an expanded speed or phase grid.

1. **A fourth projection can be necessary.** At threshold `1/8`, common
   start, speeds `(1,8)`, and `L=7/8`, the four outputs are
   `7/8,57/64,9/8,73/64`. The third output is unsafe for speed 8. The fourth
   is the earliest joint safe time. Setting R below or exactly at it checks
   the supplied-window decision and equality handling.
2. **The uniform endpoint is valid.** At threshold `1/4`, equal speeds 1
   and phases `0,1/2`, the common safe set is exactly the quarter points
   modulo one: `1/4,3/4`. From L=0 the output is `1/4`. This is an auxiliary
   phase control with isolated contacts, not a common-start LRC example.
3. **A threshold outside the guarantee can fail.** For the same speeds and
   phases but threshold `1/3`, the safe sets are disjoint. Four projections
   from zero give `1/3,5/6,4/3,11/6`; the first runner is unsafe at the final
   output. The four-step conclusion must not be asserted for all thresholds.
4. **Two sweeps do not extend automatically to three constraints.** At
   threshold `1/8`, common start, speeds `(1,7,8)`, and `L=7/8`, two sweeps
   in increasing speed order give
   `7/8,7/8,57/64,9/8,9/8,73/64`. At the final time speed 7 has phase
   `63/64`, which is blocked. The earliest triple-safe time is `65/56`.
   Here the middle runner was already safe at its second projection, near
   its right endpoint; the last projection destroys that safety. The proof
   for two constraints does not supply a fresh lower endpoint for every
   earlier constraint.

## Audit against the existing project record

`TWO_VARIABLE_SPEEDS.md` already gives a supplied family-existence argument
for all admissible integer x,y in `{0,1,4,5,6,7,x,y}`. The current projection
argument adds no existence coverage to that family.

`TWO_SPEED_SPARSE_TRANSFER.md` already has a justified two-window selector
and finite reduction. Its local integer-lap strip checks common *blocking*
occurrences and contributes duration bounds. The new four-projection query
is earliest common *safety* on a supplied window. It neither computes full
safe duration nor replaces the proof that a useful core-safe window exists.

`FASTEST_CORE_CERTIFICATES_2026_09_27.md` conditions on a fastest runner's
safe window so every residual blocker is a single interval. Its duration
and endpoint mechanisms can then detect existing safety, but the global
choice among such windows remains separate. The current selector permits
arbitrary supplied windows with two residual runners; it does not resolve
the cross-window existence problem for an arbitrary full configuration.

The anchor-obstruction example showed that bounded *early-lap enumeration*
can miss arbitrarily distant useful fast laps. The projection directly
computes a lap index from the shared current time. Four such arithmetic
selections are compatible with that obstruction. This is a concrete repair
for the two-residual-runner query, not an algorithmic contradiction.

No public literature search or novelty audit was undertaken for this internal
review. No broad scan, external outreach, hourly automation, main merge,
paid compute, all-reference work, or parked `+7/+9` study was started.

## Independent exact computation

`verify.py` reads the frozen protocol, not the primary implementation or its
results. It enumerates every rational threshold event in each bounded closed
window, classifies every event and every open cell, and reconstructs the whole
closed allowed set. Its archive `verification.json` retains all components,
not just the first. Every supplied physical core window was independently
checked to be safe throughout by the same event construction.

The frozen domain has 16 bounded physical pair/window cases and four valid
auxiliary pair/window cases. Of these 20 windows, seven are empty, four have
an isolated first component, and nine have a positive first component. The
ratio-seven obstruction is an important countercontrol: its earliest
component is the singleton `2041/6720`, yet its same supplied window also has
later positive components. An isolated earliest point is not a verdict on
duration elsewhere.

The two negative scope controls confirm the disjoint threshold-one-third
safe sets and the failure of two simple three-runner sweeps. The huge
`B=10^12` case uses a symbolic lower-bound certificate and full lifted phase
containment for the earliest component; its events are never enumerated.
All tests use standard-library exact rational arithmetic. These calculations
check only the declared finite domain; the written argument supplies the
unbounded claim.

Read-only replay from the repository root:

```bash
python -S -B reviews/2026-09-28-lap-projection/verify.py
```

## Post-protocol analytical follow-on: three residual runners

This section was derived after the frozen protocol. The coordinator proposed
the waiting bound and nested composition; the reviewer independently checked
them and supplied the shorter one-moving-a-projection proof below. The only
new calculation applies the nested order to the already-frozen three-runner
countercontrol; no new input was added.

The pair selector has a useful waiting bound. In the sequence `a,b,a,b`,
at most one a-projection can move: if the first one moves, it lands on a
safe interval's left endpoint, and the subsequent b jump cannot leave that
interval under the pair hypothesis. Consequently the combined a moves are
less than `2*delta/a`, and the two b moves together are less than
`4*delta/b`. Thus the earliest pair-safe time is less than

`2*delta/a + 4*delta/b`

after the starting time. This is a conservative upper bound, not an exact
worst-case formula.

Now let `0<a<=b<=c`, and let `S_bc` be the proved four-projection selector
for b,c. Its waiting bound is

`D=2*delta/b+4*delta/c`.

Provided the b,c pair hypothesis holds and
`D<=(1-2*delta)/a`, the composition

`P_a, S_bc, P_a, S_bc`

returns the earliest common safe time for all three constraints. If the first
pair-safe result is a-safe, the process is finished. Otherwise the second
a-projection moves to an a-safe lap's left endpoint, and the final pair
selector cannot leave that lap by the displayed bound. Earliest-witness
preservation holds for `S_bc` because it is itself an earliest-safe projection
onto the intersection of two safe sets. This proves minimality as well as
feasibility.

At `delta=1/8`, ordering alone gives

`D=1/(4b)+1/(2c) <= 3/(4a)`,

exactly the a-safe lap length. Therefore ten scalar projections suffice for
three residual runners at the eight-runner threshold. The order is
`a,b,c,b,c,a,b,c,b,c`, not the failed naive order `a,b,c,a,b,c`.

The same supplied-window limitation remains. This reasoning does not select
or force a safe window for the other four moving runners, settle every
reference, establish positive duration, or solve general eight-runner Lonely
Runner. A separately marked `post_protocol_follow_on` record in the reviewer
archive applies the ten-projection order to the same `(1,7,8),L=7/8` control.
It returns `65/56`, matching the independently reconstructed earliest time.
The original six-step failure remains in the archive. This one diagnostic
checks the implementation; the general conclusion rests on the supplied
argument, not finite extrapolation.
