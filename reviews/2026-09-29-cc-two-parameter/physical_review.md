# Two-parameter direct physical review — September 29, 2026

**Status:** OBSERVED exact controls and separate AI review of the physical map.
The infinite family claim remains an internally reviewed proof candidate. This
is neither a human review nor a formal or externally independent certificate.

**Inputs:** `PROTOCOL.md`, the two stated segments and lap labels, and exactly
the 18 declared pairs. No optimizer, broad parameter scan, additional reference
runner, or existing checker was used. The separately written
[`physical_checks.py`](physical_checks.py) computes products of the seven
explicit integer speeds with the recovered rational time, then takes exact
floors and fractional parts. Its complete output is
[`physical_checks.json`](physical_checks.json).

## Physical identities reviewed

Write `d=gcd(p,q)`, `P=p/d`, `Q=q/d`; choose `rP+sQ=1`. For an actual primitive
orbit point, `h=Qx-Py` is an integer. With

\[
T=rx+sy,\qquad N=\lfloor T\rfloor,\qquad
\tau=T-N,\qquad t=\tau/d,
\]

direct expansion gives

\[
P\tau=x-sh-PN,\qquad Q\tau=y+rh-QN.
\]

Consequently, for row `(a,b)` and its geometric lap `m`, the original physical
speed is `d(aP+bQ)` and its physical lap is

\[
\ell=m+(-as+br)h-(aP+bQ)N.
\]

Subtracting this integer from `d(aP+bQ)t` returns the geometric phase
`ax+by-m`. The original speed, primitive speed and factor `d` must not be
silently interchanged in this formula. For the selected segments the phase is
strictly between zero and one, so the displayed integer really is the physical
floor, not merely an unspecified integer offset.

The alternative pair `r'=r+kQ`, `s'=s-kP` changes `T` by the integer `kh`.
Thus `N'=N+kh`, the recovered time is unchanged, and the lap formula is
unchanged. The checker uses both `k=-3` and `k=2` on every declared pair.

For a separately structured time check, let `n=floor(P tau)`. Then
`Qn=-h (mod P)`. For `P>1`, take the least nonnegative residue
`n=-h Q^{-1} (mod P)` and recover `tau=(x+n)/P`; for `P=1`, take `n=0`.
This agrees with the Bezout recovery on every control without using its
coefficients `r,s`. Modular inversion is arithmetic recovery work, not a
constant-cost consequence of retaining only two geometric segments.

All original speeds are integers. Since each safe phase is nonzero, reflection
`t'=1-t` has phase `1-phase` and lap `speed-1-lap`. This remains correct for the
scaled controls, even though the chosen initial time lies in `[0,1/d)` and its
reflection need not.

## Fixed exact controls

| `(p,q)` | Segment | Recovered physical time |
| --- | --- | --- |
| `(1,1)` — repeated-speed auxiliary | P3 | `3/8` |
| `(1,2)` | P1 | `7/40` |
| `(1,3)` | P3 | `17/40` |
| `(1,4)` | P1 | `1/8` |
| `(1,5)` | P3 | `25/56` |
| `(2,1)` | P3 | `9/40` |
| `(2,3)` | P3 | `41/56` |
| `(3,1)` | P3 | `9/56` |
| `(1,6)` | P3 | `25/64` |
| `(2,5)` | P3 | `17/72` |
| `(3,2)` | P3 | `9/64` |
| `(3,4)` | P3 | `13/16` |
| `(4,3)` | P3 | `9/88` |
| `(5,2)` | P3 | `65/96` |
| `(5,7)` | P3 | `65/136` |
| `(3,5)` | P3 | `41/88` |
| `(4,6)` | P3 | `41/112` |
| `(6,10)` | P3 | `41/176` |

All 126 selected and 126 reflected exact distances are at least `1/8`.
Every selected minimum equals `1/8`. The corresponding 126 selected lap
identities and 126 reflected lap identities hold. All 18 coordinate-congruence
recoveries and 36 alternative Bezout recoveries agree; the latter additionally
check 252 phase identities and 252 lap identities. These alternative recoveries
repeat the same physical times and are invariance checks, not new configurations.

There are 17 distinct-speed configurations. The `(1,1)` record is an algebraic
auxiliary with repeated speed, and is not counted as an eight-distinct-runner
case. P3 is selected in 16 controls and P1 in exactly `(1,2),(1,4)`.

## Failure tests and information retained

**The original negative fixture did not meet its intended premise.** For
`p=2,q=4`, the protocol's ambient-safe P3 point `(7/16,1/4)` gives
`qx-py=5/4`, not an integer. It cannot refute the naive integrality criterion.
The failed attempt is retained in the JSON rather than silently replaced.

The analytically derived replacement `(x,y)=(13/32,5/16)` is also safe on P3,
but `qx-py=1` while `Qx-Py=1/2`. It passes naive integrality and fails true
orbit compatibility. Independently, any time satisfying `{2t}=13/32` forces
`{4t}=13/16`, contradicting the required `5/16`. The lost divisibility datum
changes existence, not just a lap label.

**Neither coordinate is the general physical clock.** Across the 18 controls,
using `t=x` violates safety in 10 cases and using `t=y` violates safety in 15;
the checker evaluates all 252 resulting distances. At `(p,q)=(2,5)`, the
recovered time is `17/72`, with `(x,y)=(17/36,13/72)`. Setting `t=x` gives speed
2 distance `1/18`; setting `t=y` gives speed 11 distance `1/72`.

Passing a wrong-clock safety test does not validate recovery. For example,
at `(4,3)` the selected time `9/88` has minimum `1/8`, while the different time
`x=9/22` happens to be safe with minimum `3/22`. This also directly shows that
the selected witness need not optimize separation.

**The retained torus fold does not bound physical time by one half.** At
`(3,4)`, the selected torus point is `(7/16,1/4)` but the recovered physical
time is `13/16`. Omitting this distinction loses a valid recovered witness.

**Closed endpoints matter.** At primitive `(1,4)`, the P1 orbit interval is
`[0,7/12]`; its only integer is zero, attained at `(x,y)=(1/8,1/2)`. Opening
both endpoints removes that fallback. The checker does not infer anything
about a full safe set from this segment-specific test.

## Reproduction and limits

From the repository root:

```bash
python reviews/2026-09-29-cc-two-parameter/physical_checks.py
```

The script writes `physical_checks.json` and prints counts. It uses only Python
standard-library exact fractions. No assertion failed. These finite checks
support the physical implementation on their listed inputs; the general
coverage proof must come from the separately reviewed infinite argument.
Optimal values, all safe times, other selected reference runners, and novelty
are outside this review. The smallest adequate representation here retains
the segment, primitive divisibility, Bezout or congruence recovery, physical
laps, scaling and equality. Geometry with an unlabeled clock is insufficient.
