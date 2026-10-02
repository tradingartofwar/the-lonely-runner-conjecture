# Primary result and exact comparison

**OBSERVED** finite arithmetic, with a **HYPOTHESIS / proof candidate**
implication through the supplied three-train span theorem.

The approved 31-core calculation completed once under the frozen protocol.
All exact arithmetic assertions passed. The complete safe sets contain 348
positive components and 20 isolated safe points. The earliest widest component
is selected without discarding other widest ties or isolated points.

The smallest selected width is `3/136`, attained at `a=34`, whose selected
window is `[41/272,47/272]`. The largest coarse sufficient second-residual
threshold is `B_a=80`. Thus, for every declared `a`, `b>=80` implies

`1/(4b)+1/(2c)+1/d <= 7/(4b) <= w_a`

whenever `a<b<c<d`. The per-`a` thresholds in `PRIMARY_TABLE.md` are often
smaller. This implication is conditional on the reviewed span theorem; the
table does not by itself establish it.

The separately structured threshold-event verifier reported agreement on all
31 records and 1,932 numerical fields, with zero disagreements. It compared
the complete components and isolated points, widest ties, counts, measures,
selected certificates, widths, and coarse thresholds. That implementation was
frozen and executed before its author read the primary output or code. This is
internal AI-assisted arithmetic verification, not independent human proof
review. Its artifacts are `independent_core_windows.json`,
`independent_comparison.json`, and `compare_independent.py` in this directory.
It additionally reported agreement with the scope reviewer's twelve hand
calculations of `3/8-mu(Safe{1,4,5,a})`, using only the approved domain.

## Analytic compression of the final table

For each `a=16,...,34`, the table gives `w_a=3/(4a)`, the maximum width
permitted by speed `a` alone; hence the coarse threshold is `ceil(7a/3)`.

The continuation for all integers `a>=19` needs no further enumeration.
The left endpoints of `a`'s safe laps are spaced by `1/a`, and each lap has
width `3/(4a)`. Any closed interval of width at least `7/(4a)` therefore
contains a complete safe lap: choose the first safe-lap left endpoint at or
after the interval's left endpoint. Its displacement is strictly less than
`1/a`, and adding the lap width stays within the interval. Since the fixed
core-safe window `[9/32,3/8]` has width `3/32`, it satisfies this condition
for `a>=19`. Its contained complete lap is safe for all four core speeds,
and no four-core safe component can exceed the width of one `a`-safe lap.
The exact finite rows at `a=16,17,18` extend this conclusion to `a>=16`.
This paragraph is a post-calculation analytic deduction, not an expanded
executed domain or a separately reviewed theorem.

## Reproduction and hashes

Command from repository root:

`python reviews/2026-09-29-core-windows/primary_core_windows.py`

| Item | SHA-256 |
| --- | --- |
| Frozen protocol | `d5ff2d4e06c1d8c7629c6c115fb9faa23a0a1510791cb9b983903277726e65d0` |
| Primary source | `fd0ce8cc050d534ea56d0dbb1560a228649f28ec2ab96d4784947557e7461ab9` |
| Primary JSON | `4bbf907e6dc9b85d868a4d739e7f75a88969dead514ae2aca4a9879ca7fa997a` |
| Primary table | `0c6a4f14b5f87297d70ad1ed663712ff4f7a171bfd661d08d15ec806deb714b0` |

No `b,c,d` tuples, phases, words, all-reference cases, or expanded finite
`a` domain were evaluated. The stronger integer-separation threshold was not
computed. There is no claim that `B_a` is sharp, that the cases below it fail,
that all remaining configurations are now finite, or that the full conjecture
has been proved. Material AI involvement is disclosed; external proof and
novelty review remain pending.
