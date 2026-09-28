# The fourth runner: a valid condition and a failed universal step bound

**September 28, 2026.** Baseline
`b5fbc19457794d3884d758de0833a38b236d3246`, existing research branch.
Material AI involvement: a coordinator, a separate proof/threshold-verification
agent, and a structural challenger. The structural challenger constructed the
blocking chain; the coordinator converted it into an integer common-start case.
Exact implementations and review provenance are preserved below.

**Outcome:** the waiting-time argument gives a correct **conditional**
22-projection selector for four residual runners at threshold `1/8`. Its
conservative speed condition fails on all eight archived controls, although
the unchanged 22-step diagnostic succeeds on every one. A subsequently
constructed counterexample then shows that **this fixed 22-step order is not
complete in general**, including for eight distinct integer-speed runners starting together.

The conditional implication remains a HYPOTHESIS / supplied proof candidate
awaiting external review. The unconditional 22-step claim is **DISPROVEN** by
an exact counterexample. No novelty or new Lonely Runner family coverage is
asserted. The example has a valid lonely time immediately after one additional
projection; the conjecture is not contradicted.

## 1. The question and prior-work audit

The [previous selector](DIRECT_LAP_PROJECTION_2026_09_28.md) computes the earliest
joint safe time for two or three residual constraints using four or ten
projections, respectively, at threshold `delta=1/8`. It assumes a supplied
closed window on which the other runners are already safe. The next question
was whether the same argument extends to four residual runners.

We first audited the [four-blocker cycle study](FOUR_BLOCKER_CYCLE_CORRECTIONS.md)
and the [fastest-core argument](FASTEST_CORE_CERTIFICATES_2026_09_27.md).
The former already explains local duration and higher-order corrections on
the eight configurations used here. The latter makes local tree bounds exact
when conditioning on a fastest runner. Neither establishes the proposed
fixed 22-step bound. All eight archival inputs already had valid times.

The frozen physical setup retains eight common-start runners, reference zero,
core speeds `{1,4,5}`, and the old core-safe window

`J=[9/32,3/8]`.

The [protocol](../reviews/2026-09-28-four-projection/protocol.json) fixes exactly
the previous eight four-blocker configurations and two explicitly constructed
auxiliary condition fixtures. It also fixes the projection order and the
distinction between a condition-gated policy and an ungated diagnostic.
There was no speed, phase, core, or window scan.

## 2. The conditional 22-step statement

For a positive speed v and phase alpha, define the next-safe-time projection

`P_v(t)=max(t,(m+delta-alpha)/v)`,

where `m=ceil(v*t+alpha-1+delta)`.

Every projection preserves all possible earlier joint witnesses as upper
bounds on its output. Its advance is strictly less than `2*delta/v`; if it
moves, it lands on a safe lap's left endpoint. Safety includes equality.

Order four residual speeds `0<a<=b<=c<=d`. At `delta=1/8`, the previously derived
triple selector `S_bcd` has order

`b,c,d,c,d,b,c,d,c,d`.

In its two b projections, at most one moves: a moving first b projection
begins a fresh safe lap, which the following pair operation cannot leave.
Combining that fact with the pair waiting bound gives

`S_bcd(t)-t < D3 = 1/(4b)+1/(2c)+1/d`.

If

`D3 <= 3/(4a)`,                                                (1)

then the order

`P_a, S_bcd, P_a, S_bcd`

returns the earliest time safe for all four. It uses at most 22 scalar
projections. If the first triple output is a-safe, it is already a joint
witness. Otherwise the second a projection begins a fresh safe lap of width
`3/(4a)`, and the final triple operation cannot leave it by (1). The earlier-
witness preservation property proves minimality, not just feasibility.

Equality in (1) is allowed: the actual triple advance is strictly below D3.
The formula uses arbitrary phases as an auxiliary mathematical extension;
the physical controls retain a common start. At a general threshold one must
also retain the inner pair/triple hypotheses; this note does not silently
extend the argument to every delta.

## 3. Three verdicts must stay separate

The frozen diagnostic runs the same 22 projections even when (1) fails.
Let T be the final iterate and W the supplied closed window `[L,R]`.

| Diagnostic outcome | What follows without assuming (1) |
| --- | --- |
| T>R | W is empty: every possible joint witness had to be at least T |
| T<=R and every residual runner is safe at T | T is the earliest witness in W |
| T<=R but some residual runner is unsafe | The diagnostic is inconclusive |

Failure of (1) alone establishes none of those three outcomes. It only removes
this particular uniform waiting-time guarantee. Checking `T<=R` without also
checking final safety would be an invalid extension of the theorem.

The main algorithm uses exact ceilings and direct phase checks. It does not
build threshold lists or scan lap labels. The independent verifier deliberately
reconstructs the full safe sets in the small supplied windows.

## 4. All eight archived controls pass the diagnostic, despite failing (1)

Every physical condition margin `D3-3/(4a)` is strictly positive. Nevertheless,
the 22-step output is feasible and equals the independently reconstructed
earliest witness in each supplied J:

| Four residual speeds | Earliest T | First clipped safe component |
| --- | --- | --- |
| 56,64,72,112 | 145/512 | [145/512,127/448] |
| 56,64,72,113 | 129/448 | [129/448,167/576] |
| 6,7,11,13 | 3/8 | singleton 3/8 |
| 6,7,8,11 | 17/56 | [17/56,5/16] |
| 309,320,328,619 | 697/2472 | [697/2472,1399/4952] |
| 310,320,328,621 | 467/1656 | [467/1656,743/2624] |
| 320,328,336,641 | 721/2560 | [721/2560,1447/5128] |
| 6,7,11,16 | 17/56 | [17/56,39/128] |

The two auxiliary fixtures check that the condition can pass. Speeds
`(1,2,4,8)` on `[7/8,6/5]` have strict condition slack and return `73/64`.
Speeds `(15,20,30,48)` have exact equality in (1); on `[0,1/120]` their answer
is the included right endpoint `1/120`. These four-constraint fixtures are not
additional full eight-runner configurations.

Separate implementations agree on all ten cases, all 220 scalar projection
outputs, every condition value, earliest time, and first clipped component.
The frozen domain has no raw empty or inconclusive outcomes. Its success
therefore cannot establish that 22 steps suffice outside those cases.

## 5. Post-protocol counterexample: a repeated blocking occurrence matters

The structural challenger attacked both the unconditional rule and a tempting
repair: perhaps every triple has waiting time at most `3/(4b)`, which would
fit any slower a-safe lap. The following single interval chain defeats that
stronger bound and, with a fourth runner, the actual 22-step composition.

This is analytical follow-on work, separately
[declared](../reviews/2026-09-28-four-projection/follow_on_protocol.json).
It does not replace the frozen condition or its successful controls.

Start with auxiliary speeds and phases

`(a,b,c,d)=(1,1,6/5,33/20)`,

`(alpha_a,alpha_b,alpha_c,alpha_d)=(97/352,925/1056,127/220,1/8)`.

The following table writes times in units of `1/1056`. All listed intervals
are **open blocked intervals**:

| Runner and meeting occurrence | Left | Right |
| --- | ---: | ---: |
| c, preceding | -618 | -398 |
| a, preceding | -423 | -159 |
| d, first | -160 | 0 |
| b | -1 | 263 |
| c | 262 | 482 |
| d, next | 480 | 640 |
| a, next | 633 | 897 |

Every consecutive pair overlaps strictly. This chain covers the full closed
window `[-423/1056,640/1056]`, including both of its endpoints. In particular,
the middle four intervals d,b,c,d cover a continuous span of length `25/33`,
greater than `3/4`. The fast runner contributes **two different occurrences**,
connected through the other two runners.

The four outer operations give

`-423/1056 -> -398/1056 -> -159/1056 -> 640/1056`.

The first a-safe endpoint stays fixed; the first triple call leaves a blocked;
the second a projection begins a fresh safe lap ending at `633/1056`;
and the second triple call jumps past that endpoint. At the final output,
runner a's phase is `931/1056>7/8`. The fixed 22-step result is unsafe.

One further a projection returns `897/1056=299/352`, safe for all four.
The open cover and exact endpoint check prove it is the earliest such time
after L. This exhibits a real failure of the unconditional 22-step claim,
while the correctly guarded diagnostic remains inconclusive rather than
issuing a false witness.

To remove equal speeds, replace a by `127/128`, set its phase to
`12363/45056`, and start at `L=-17995/44704`. The other three speeds and phases
stay fixed. Both triple outputs are unchanged; the final a-phase exceeds
`7/8` by `97/135168`. Its next a projection gives the earliest witness
`38325/44704`. This still uses arbitrary phases; it is not yet a common-start
Lonely Runner input.

## 6. A common-start, integer-speed version

The coordinator then converted the distinct auxiliary construction into one
directly constructed physical example. This is a **new post-protocol input**,
not one of the archived controls, a held-out test, or a broad search.

Let v_i and alpha_i be the four distinct auxiliary speeds and phases above.
Set

`M=675840`, `P=225281`, `tau=P/M`, `N=640*M*10^6=432537600000000`.

The denominator multiple M makes every `M*alpha_i` an integer. Since P is
invertible modulo M, choose

`r_i=(M*alpha_i)*P^(-1) mod M`, `U_i=N*v_i+r_i`.

The residues are `(185445,141440,390144,84480)`. Each `N*v_i` is an integer
multiple of M, so at the common-start anchor tau the four phases are exactly
the desired alpha_i. The full eight-runner configuration is

`{0,1,4,5,429158400185445,432537600141440,`

`519045120390144,713687040084480}`.

All speeds are distinct integers; the overall gcd is one. The magnitude N was
selected once, without a search. Exact interval inequalities, rather than an
unquantified closeness argument, verify the resulting example.

Use the supplied window

`L=tau+(-1/8-alpha_a)/U_a`

` =1144427480494519/3433267201483560`,

`R=tau+(9/8-alpha_d)/U_d`

` =1903173888225289/5709496320675840`.

This is a tiny clipped window **inside the old J**, not a claim that the
entire old J is empty. Core speeds 1,4,5 remain strictly safe throughout it
and through the later witness below.

The 22-step output is exactly R, where the first residual runner's phase is

`47618157730181/54376155435008`.

It exceeds `7/8` by `39021724549/54376155435008>0`, so the output is unsafe.
The same seven-interval open covering pattern proves the supplied window is
empty. The next first-runner projection returns

`T*=163489640070647/490466743069080`,

which is the earliest full-configuration lonely time at or after L. The
cover excludes every earlier time and all seven moving runners pass the exact
distance check at T*. Thus the obstruction concerns the selector, not
Lonely Runner existence.

If the supplied right endpoint is extended to T*, the same 22-step output is
still unsafe even though the window now contains a valid witness. The separate
event reconstruction checks this same-input extension: its allowed set on
`[L,T*]` is exactly the included right endpoint. Thus the example also supplies
an actual missed-witness window, not only an inconclusive run on an empty one.

The enormous speed magnitudes do not require a whole-period computation.
Only direct arithmetic and the few threshold events in this tiny local
interval are checked. All computations use rational arithmetic, with no float
rounding or sampled-time certification.

## 7. What the fourth runner exposed

The proof failed at a specific relational fact: a triple can carry a blocked
chain across more than one occurrence of a fast runner, and that chain can
last longer than the fresh safe lap of the fourth runner. The same runner
can therefore become a constraint again after other runners connected its
separated blocking intervals.

The findings must remain distinct:

- The conservative sufficient condition fails on all eight old inputs, yet
  their actual 22-step runs succeed.
- The unconditional 22-step rule really fails on the constructed input,
  including a common-start integer-speed version.
- The conditional theorem remains valid.
- One extra step happens to repair these counterexamples; no universal
  23-step guarantee follows.
- A supplied empty window does not imply failed loneliness elsewhere.

The result neither excludes a different projection order nor proves that
every fixed step bound must fail. Arithmetic operation counts remain distinct
from integer bit complexity. No new invariant, all-reference guarantee,
family existence result, or novelty claim is made.

**Next bounded question:** what controls the number and arrangement of
connected blocking occurrences encountered by the repeated map
`P_a,S_bcd`? Seek a termination bound or a parameterized counterexample to a
uniform bound, preserving common-start constraints and endpoint equality.
Do not merely replace 22 by 23 on the evidence of this example. The separate
problem of forcing a successful core-safe window for arbitrary configurations
remains open.

## Reproduction and review

From the checkout root, with the Python standard library:

```bash
python -B reviews/2026-09-28-four-projection/primary.py --check
python -S -B reviews/2026-09-28-four-projection/verify.py
python -B reviews/2026-09-28-four-projection/follow_on.py --check
python -S -B reviews/2026-09-28-four-projection/follow_on_verify.py
python -B reviews/2026-09-28-four-projection/compare.py
```

The [frozen-method review](../reviews/2026-09-28-four-projection/review.md)
and [structural challenge](../reviews/2026-09-28-four-projection/structural.md)
preserve the independently derived arguments, negative results, and provenance.
The threshold verifier imports no primary code or saved primary answers.
It reconstructs all ten frozen windows, then separately checks the three fixed
follow-on constructions locally, including their earliest later witness.
The primary follow-on instead uses a strict open-interval covering certificate.
The comparison checks actual saved traces, bounds, components, and endpoints.
Manifest hashes preserve both protocols and all results.

This is internal AI error control, not external proof certification. Hourly
research remains paused. There was no broad scan, all-reference campaign,
outside outreach, paid compute, main merge, or parked `+7/+9` continuation.
