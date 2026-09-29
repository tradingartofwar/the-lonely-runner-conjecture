# Direct six-core window structure

September 29, 2026. Research parent `da05361310a6e0d5607fdd7565ad226f637c8305`.

**HYPOTHESIS / proof candidate.** This is a symbolic derivation, materially
AI-assisted. No mathematical executable evaluation or scan was performed by
this investigator. The 31 four-core windows cited below are the previously
declared, independently reconstructed records, not new observations. General
claims require the repository's further review. No lower-runner literature
theorem is used in this argument.

Scope: common-start distinct positive integer speeds
`{1,4,5,a,b,c}`, with `a<b<c` outside `{1,4,5}`, all at threshold `1/8`.
The goal here is positive six-constraint safe duration. This requirement is
not imposed on the final seven constraints, where equality-only witnesses
can occur.

## 1. A strict two-train window test

Let `W=[l,r]` be a positive closed four-core safe component for
`{1,4,5,a}`, of width `w`. If

`1/(4b)+1/(2c) < w`,

then the six-core safe set has positive measure.

For a direct endpoint check, temporarily use **closed** blockers for b and c;
their complement is strict safety. Put `P=1/b`, `q=1/c`, so `q<P`.
In an increasing-right-endpoint chain of overlapping or touching closed
blockers, consecutive blockers cannot have the same label, because a
period-p train has blocker length p/4 and positive intervening gap.
Two occurrences of the P label would therefore include a consecutive
subchain P,q,P. Its right endpoints advance by at most `(P+q)/4<P`,
but distinct P occurrences differ by at least P. This is impossible.
Hence a chain contains at most one P blocker and two q blockers, with
total span at most `P/4+q/2`.

A finite closed cover of W by the two trains would contain an overlapping
or touching chain spanning W. Local finiteness holds because the periods
are positive. The strict displayed inequality rules this out. The
complement of the closed blocker union is relatively open and nonempty
in W, hence contains a positive interval within the interior of W. In
that interior all four original core constraints are strictly safe.
This proves positive six-core duration. The strict inequality is deliberate:
the inherited non-strict test only promises a safe point.

## 2. All but eight values of a disappear analytically

The fixed-core interval is `J=[9/32,3/8]`, of width `3/32`.
The previous clipping lemma gives an a-safe subinterval of width at least

`min(3/(4a),3/64-1/(8a))`.

For every `a>=19`, the second expression is at least the first. Thus J
contains a full a-safe gap of width `3/(4a)`, and

`1/(4b)+1/(2c) < 3/(4b) < 3/(4a)`.

The strict two-train test proves positive six-core duration for every
`a>=19`, independently of b and c. Alternatively, discrepancy on that gap
gives the explicit positive measure lower bound

`(3/16)(2/a-1/b-1/c)`.

For `a=11,13,14,16,17,18`, the inherited widest four-core windows also
have width exactly `3/(4a)`, so the same strict test applies. Their
respective left endpoints are `25/88,33/104,33/112,41/128,1/8,41/144`.
For `a=8`, the inherited window has width `5/64`, while even the largest
remaining two-train budget is

`1/(4*9)+1/(2*10)=7/90 < 5/64`.

Consequently only `a in {2,3,6,7,9,10,12,15}` remains for this test.

## 3. A precisely bounded remainder before arithmetic pruning

Use the following inherited four-core widths. Since the budget decreases
in both b and c, testing the smallest possible c=b+1 gives exactly the
listed possible b values whenever the strict test fails.

| a | w_a | Remaining b values | Largest possible c |
| ---: | --- | --- | ---: |
| 2 | 3/32 | 3,6,7 | 48 |
| 3 | 1/20 | 6 through 14 | 60 |
| 6 | 7/160 | 7 through 16 | 62 |
| 7 | 1/14 | 8,9 | 12 |
| 9 | 1/20 | 10 through 14 | 20 |
| 10 | 1/16 | 11 | 12 |
| 12 | 1/24 | 13 through 17 | 22 |
| 15 | 7/160 | 16 | 17 |

There are 36 listed (a,b) pairs. In each row and for each listed b,
`4*b*w_a-1>0`, and the exact c restriction is

`b<c<=floor(2*b/(4*b*w_a-1))`.

The maximum is attained in this bound at a=6,b=7 and equals
`floor(560/9)=62`. Thus **c>=63 already guarantees positive six-core
duration by this direct structural argument**. The table is a symbolic
reduction, not a performed triple scan.

## 4. A shared five-core window

The interval

`W*=[25/56,15/32]`, width `5/224`,

lies in the fixed-core component `[17/40,15/32]`. It is safe for runner7
and for each runner in `{3,6,8,10,12}`. These are the exact scaled ranges:

| v | v W* | Containing closed safe lap |
| ---: | --- | --- |
| 3 | [75/56,45/32] | [9/8,15/8] |
| 6 | [75/28,45/16] | [17/8,23/8] |
| 7 | [25/8,105/32] | [25/8,31/8] |
| 8 | [25/7,15/4] | [25/8,31/8] |
| 10 | [125/28,75/16] | [33/8,39/8] |
| 12 | [75/14,45/8] | [41/8,47/8] |

A single speed-c closed blocker has length `1/(4c)`. Its distinct
occurrences have positive gaps, so they cannot cover an interval longer
than that length. Since

`1/(4c)<5/224` for every integer `c>=12`,

both six-core families `(a,b,c)=(3,7,c)` and `(6,7,c)` have positive
duration for every c>=12. This is valid for any phase of the last c
train; the construction of W* uses common-start integer phases.

For the remaining c values in the `(6,7,c)` family, explicit positive
safe windows are:

| c | Window |
| ---: | --- |
| 8 | W* |
| 9 | [11/24,15/32] |
| 10 | W* |
| 11 | [17/56,5/16] |

All are checked by direct closed safe-lap containment. This removes the
whole pair `(a,b)=(6,7)` from the finite remainder. The same W* itself
is safe for the triple `(7,8,12)`.

## 5. Integration with the separate arithmetic argument

The arithmetic investigator supplies these independently proved candidate
certificates; their detailed derivation belongs in `arithmetic.md`:

1. Strict anchors 1/6 and 1/7 succeed unless the residual triple contains
   a multiple of 6 and a multiple of 7, respectively.
2. If no residual is divisible by 8, the one-sided eighth anchors give
   positive duration unless residues 3 and 7 modulo 8 both occur.
3. If c is the unique residual divisible by 7, a shifted seventh anchor
   always supplies positive duration.

Applying these criteria to the exact 36-pair domain is short hand
casework. Criterion 3 means any survivor must have 7 dividing a or b.
Consequently only a=7, b=7, or b=14 need remain from the table. Removing
the whole `(6,7)` family by Section 4, criteria 1 and 2 leave exactly

`(3,7,12),(3,7,18),(3,7,24),(3,7,30),`
`(6,14,16),(7,8,12),(12,14,16)`.

The arithmetic and structural investigators independently reached that same
seven-triple list by hand before mathematical execution. The four
`(3,7,c)` triples are covered by W* plus its single-train width argument.
The `(7,8,12)` triple has all of W* safe. The two c=16 triples are
covered by a common interval

`[17/128,15/112] = 1/8 + [1/128,1/112]`, width `1/896`,

from the separate shifted-eighth argument. Thus these symbolic
certificates close the precisely reduced remainder, subject to the
coordinator's independent domain and endpoint review.

The configuration-level information here is the availability of the same
actual safe window for several different slow-runner cores, together with
which residual must be responsible for each failed rational anchor. Scalar
blocked fractions alone would not express those obligations.

## 6. A direct endpoint quantum and final-speed bound

Given the positive six-core conclusion, choose a maximal positive closed
component and write `M=max(5,b)`, the second-largest speed among its six
constraints. Its endpoints are threshold events: fixed speed1 keeps
the safe set away from times0 and1. If the two endpoint-controlling
speeds v and w differ, subtracting their threshold forms
`(8j+/-1)/(8v)` and `(8l+/-1)/(8w)` gives a positive integer divided
by `8vw`. Since `vw<=Mc`, the component width is at least `1/(8Mc)`.
If both endpoints are controlled by the same speed v, they delimit one
full v-safe lap, of width `3/(4v)`, which satisfies the same lower bound.

The final speed-d open blocker has length `1/(4d)`. Thus

`d>=2Mc`

guarantees a final safe point in this component. Equality is sufficient:
an open blocker cannot cover a closed interval of at least its own width,
and distinct d-blockers have gaps. No positive final duration is asserted
at equality.

Combining the inherited uncertified restrictions `a<=34,b<=47,c<=1565`
with this direct six-core candidate leaves

`d<=2*47*1565-1=147109`.

This is a finite conditional reduction for the specified fixed-core,
selected-reference family. It does not evaluate that finite domain or
authorize a broad scan of it. A sharper separately credited literature
bridge may give smaller bounds; none is needed for this endpoint argument.

## 7. Status and verification boundary

This report proposes a direct positive six-core guarantee for the stated
fixed-core integer family. It does not prove the full Lonely Runner
Conjecture, does not require positive final seven-core duration, and does
not claim novelty. The seven finite remainder triples and explicit
windows are contained in the coordinator's separately frozen, conservative
27-triple protocol. This report itself performed no executable
certificate reconstruction. No broad speed, phase, or all-reference scan
has been run here, and the hourly task stays paused.
