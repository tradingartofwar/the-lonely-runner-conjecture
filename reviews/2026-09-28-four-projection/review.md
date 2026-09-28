# Independent review: conditional selection for four residual runners

September 28, 2026. Baseline
`b5fbc19457794d3884d758de0833a38b236d3246`.

This reviewer independently checked the supplied argument and implemented the
bounded event oracle and fixed projection trace before reading the primary
implementation or results. This is internal AI challenge, not external proof
certification. The general result remains a supplied proof candidate; no novelty
or full Lonely Runner proof is asserted.

## Mathematical verdict

The proposed sufficient condition is valid at threshold `delta=1/8` for four
ordered positive speeds `a<=b<=c<=d`, with arbitrary phases allowed only as an
explicit auxiliary formulation. The condition is

`1/(4b)+1/(2c)+1/d <= 3/(4a)`.

Under that condition, applying

`P_a, S_bcd, P_a, S_bcd`

returns the earliest simultaneous safe time at or after L. Here `P_v` is the
earliest v-safe projection, and `S_bcd` is the previously supplied ten-step
earliest-safe selector for the other three runners. Expanding this composition
uses 22 scalar projections. Equality in the condition is permitted.

The argument concerns a supplied closed core-safe window `[L,R]`. Its outcome
does not choose the window or force some window to succeed in an arbitrary
full configuration. The fixed threshold remains `1/8` when constraints are
temporarily omitted. All eight physical controls have eight common-start
runners and selected reference zero. Two constructed auxiliary four-constraint
fixtures are not additional eight-runner configurations.

## Derivation and endpoint audit

For positive speed v, an unsafe component is an open interval of length
`2*delta/v`. Therefore `P_v(t)-t` is nonnegative and strictly less than that
length. Whenever it is positive, the output is a safe lap's left endpoint.
For any joint witness u>=t, `P_v(t)<=u`. These facts establish both direction
and preservation of the earliest possible common witness.

At `delta=1/8`, the earlier pair result applies to every ordered positive
pair. Its waiting bound for c,d is

`D2=2*delta/c+4*delta/d`.

Ordering gives `D2 <= (1-2*delta)/b`, so the ten-step selector
`S_bcd = P_b,S_cd,P_b,S_cd` is valid. Moreover, at most one of its two
b-projections moves: if the first moves, it starts a fresh b-safe lap and the
following pair selector cannot leave that lap. Thus both b-projections
together advance less than `2*delta/b`, and both pair calls together advance
less than `2*D2`. The triple waiting bound is consequently

`D3=2*delta/b+4*delta/c+8*delta/d`.

If the first `S_bcd` result is a-safe, the remaining operations fix it.
Otherwise the second a-projection starts a fresh a-safe interval of width
`(1-2*delta)/a`. The final triple selector advances less than D3, so the
displayed sufficient condition keeps it within that safe interval. It is
then safe for all four runners. Every still-possible earlier witness has
bounded all iterates from above, so feasibility proves earliestness.

There is no endpoint loss: the blockers are open, safe bands are closed, and
the displacement bounds are strict. The equality fixture tests both equality
in the waiting condition and a witness at the supplied window's right edge.

The generalized symbolic expression in delta requires the inner pair and
triple hypotheses as well as the outer condition. The automatic inner
guarantees used here are specifically supplied by the `delta=1/8` threshold
and speed ordering; no arbitrary-threshold extension is asserted.

## Three distinct meanings of failure

1. A negative condition margin only means this sufficient waiting bound
   does not certify the 22-step termination guarantee.
2. A final iterate safe for all four runners is their earliest safe time at
   or after L, even if the condition failed. This follows from witness
   preservation and needs no unconditional termination theorem.
3. A final iterate beyond R proves the supplied window empty, whether or
   not that iterate is jointly safe. Every joint witness must be at least
   every iterate. A final iterate at or before R that is still unsafe is
   inconclusive; the window could be empty or could contain a later witness.

Since iterates never decrease, testing the final iterate against R captures
any earlier crossing of R. Right-endpoint equality is not an empty-window
certificate.

## Independent exact outcomes

`verify.py` reads only the frozen protocol. It reconstructs all threshold
events, all open cells between them, all safe endpoints, and every closed
allowed component in each window. It separately certifies the entire physical
core window for speeds `{1,4,5}`. Its independent projection implementation
uses fractional-phase cases rather than the primary ceiling formula.

The eight physical inputs are exactly the old four-blocker-cycle controls.
Every one fails the sufficient waiting condition, but every fixed 22-step
run still finds the earliest actual witness. This supplies finite successes
beyond the condition; it neither proves unconditional 22-step completeness
nor makes the sufficient condition necessary.

| Case | First exact component on the supplied window |
| --- | --- |
| 56,64,72,112 | [145/512,127/448] |
| 56,64,72,113 | [129/448,167/576] |
| 6,7,11,13 | {3/8} |
| 6,7,8,11 | [17/56,5/16] |
| 309,320,328,619 | [697/2472,1399/4952] |
| 310,320,328,621 | [467/1656,743/2624] |
| 320,328,336,641 | [721/2560,1447/5128] |
| 6,7,11,16 | [17/56,39/128] |

The two constructed auxiliary fixtures pass the condition. For `(1,2,4,8)`
on `[7/8,6/5]`, the first component is `[73/64,6/5]`. For `(15,20,30,48)`
on `[0,1/120]`, the waiting-condition margin is exactly zero and the only
window witness is its right endpoint `1/120`. This latter clipped singleton
does not claim isolation in the full time line.

The archive retains every full component, exact duration, condition margin,
22-step trace, raw verdict, and first-component status. All ten raw runs have
an earliest-witness verdict; none is empty or inconclusive in this frozen
domain. This domain therefore tests no numerical instance of the latter two
raw classifications; their validity follows from the written lower-bound
argument. The fixed condition itself is not retuned after these outcomes.

Read-only replay from the repository root:

```bash
python -S -B reviews/2026-09-28-four-projection/verify.py
```

No primary implementation or output was read before these independent results
were completed. No extra input, speed scan, phase grid, all-reference campaign,
paid compute, external outreach, main merge, hourly restart, or parked `+7/+9`
work was performed. The separate structural challenger handles possible
counterexamples or improved bounds; those must remain distinct from this
frozen method and its observed outcomes.

## Separate post-protocol counterexample verification

After completion of the frozen ten-case archive, the structural challenger
constructed an auxiliary shifted-phase counterexample and a distinct-speed
version. The coordinator then supplied one explicit common-start integer-speed
lift. These are the three fixed constructions in `follow_on_protocol.json`;
they are not additional archival controls or held-out tests. The original
condition and ten-case results remain unchanged.

The separate `follow_on_verify.py` imports only this reviewer's independent
threshold/phase routines. It derives all three inputs from that protocol,
then reconstructs events only on the small interval from the supplied L to
the next a-projection after step 22. Each reconstruction has exactly 13
threshold events, even for the huge integer speeds. No full period, range of
speeds, choices of phase, scales, or candidate windows was searched.

All three cases have the same qualitative result:

- The 22nd output equals the supplied right endpoint R, but runner a is
  unsafe there; the other three residual runners are safe.
- The original closed window `[L,R]` is empty. A strict open-blocking cover
  confirms this independently of the threshold reconstruction.
- One additional a-projection yields the earliest common safe time after L,
  beyond R. On `[L,T23]`, the full allowed set is the clipped singleton
  `{T23}`. This does not claim global isolation of that time.

The cover consists of the seven open bad intervals with local labels
`(c,0),(a,0),(d,0),(b,1),(c,1),(d,1),(a,1)`.
Successive intervals overlap strictly, L lies strictly inside the first, and
R lies strictly inside the last. The last interval ends at T23. The archive
retains every exact endpoint and all 22 iterates. Thus an unsafe final iterate
at R remains inconclusive under the frozen policy; the separate cover proves
emptiness. On the already reconstructed larger window `[L,T23]`, the same
22-step run misses a witness that does exist, so the failure is also a genuine
limitation of unconditional witness selection.

For the equal-speed auxiliary construction, T23 is `299/352`; for the
distinct-speed auxiliary construction it is `38325/44704`. Neither
auxiliary example is itself a common-start LRC configuration.

The third construction is a common-start eight-runner input with speeds

`{0,1,4,5,429158400185445,432537600141440,519045120390144,713687040084480}`.

The coordinator's residue construction uses `M=675840`, `P=225281`,
`N=640*M*10^6`, and anchor `tau=P/M`. The reviewer independently recomputed
the modular inverse and residues `185445,141440,390144,84480`, recovered the
prescribed auxiliary phases at tau, and checked that all eight original
speeds are distinct. The fixed core `{1,4,5}` is safe throughout the tiny
extended interval. The earliest full eight-runner witness after L is exactly

`163489640070647/490466743069080`.

This explicitly disproves unconditional completeness of the stated 22-step
order in the common-start setting. It does not contradict the sufficient
speed condition, which fails here, or disprove another projection count,
adaptive iteration, arithmetic method, or Lonely Runner itself. The
counterexample is algebraically constructed after the initial freeze; its
large speed sizes are not evidence of a search or a minimality claim.

Separate read-only replay:

```bash
python -S -B reviews/2026-09-28-four-projection/follow_on_verify.py
```
