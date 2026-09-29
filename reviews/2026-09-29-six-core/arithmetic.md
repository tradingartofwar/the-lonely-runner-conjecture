# Arithmetic closure of the six-core remainder

September 29, 2026. Research parent `da05361310a6e0d5607fdd7565ad226f637c8305`.

**HYPOTHESIS / proof candidate.** These are symbolic deductions and hand
calculations, materially AI-assisted. No mathematical executable evaluation
was run by this reviewer. Internal agreement is not external certification.
The coordinator's frozen numerical protocol is separate and unchanged.

## Scope and dependencies

Take six distinct common-start positive integer speeds
`{1,4,5,a,b,c}`, with `a<b<c`, residuals outside `{1,4,5}`. Safety means
distance at least 1/8; equality is safe and blocking intervals are open.
Necessarily c>=6, so c is the largest of all six speeds.

The structure review reduces positive six-core safety to 36 specified
`(a,b)` pairs, `b<c<=62`, satisfying

`1/(4b)+1/(2c)>=w_a`.

Its table is an input to this arithmetic review; the proof reducing to that
table must also be checked. The only surviving a values and pair lists are

| a | b values | w_a |
| ---: | --- | --- |
| 2 | 3,6,7 | 3/32 |
| 3 | 6,...,14 | 1/20 |
| 6 | 7,...,16 | 7/160 |
| 7 | 8,9 | 1/14 |
| 9 | 10,...,14 | 1/20 |
| 10 | 11 | 1/16 |
| 12 | 13,...,17 | 1/24 |
| 15 | 16 | 7/160 |

These are proof-derived bounds, not an authorization for broader searches.

## 1. Strict rational anchors

If none of a,b,c is divisible by 6, all six distances at t=1/6 are at least
1/6. Since every speed is at most c, the closed interval centered there
with radius `1/(24c)` is safe. Its width is `1/(12c)`.

If none is divisible by 7, the analogous interval at t=1/7 has radius
`1/(56c)` and width `1/(28c)`.

If no residual is 0 or 7 modulo 8, the interval

`[1/8,1/8+1/(8c)]`

is safe. At its left endpoint a speed in residue class 1 enters the safe
band as time increases, and every other allowed residue starts at least
1/8 from the opposite safe boundary. The core speeds have classes 1,4,5.

If no residual is 0 or 3 modulo 8, instead use

`[3/8-1/(8c),3/8]`.

Here decreasing time moves residue 7 of the phase into its safe band;
the dangerous phase residue 1 corresponds to speed residue 3 modulo 8.
The core phases are 3,4,7 modulo 8. Both displayed windows have positive
width. Therefore, if no residual is 8-divisible, failure of these two
certificates requires both speed classes 3 and 7 modulo 8 to occur.

## 2. Rescue when c is the unique multiple of 7

Suppose `7|c`, `7` does not divide a, and `7` does not divide b. Among
`j=1,2,3`, choose one for which

`ja != 6 (mod 7)` and `jb != 6 (mod 7)`.

Each of a,b excludes at most one j: multiplication by a nonzero residue
modulo 7 is injective. Thus some j survives. At these three j values none
of the core speeds 1,4,5 has phase residue 6 either:

| j | residues of j,4j,5j modulo 7 |
| ---: | --- |
| 1 | 1,4,5 |
| 2 | 2,1,3 |
| 3 | 3,5,1 |

Consequently every speed v other than c starts at some phase `k/7`,
`1<=k<=5`, at t=j/7. For

`1/(8c)<=u<=9/(56c)`,

its phase after adding u remains between `1/7` and
`5/7+9/56=7/8`. There is no wrap. Runner c, whose anchor phase is zero,
has new phase in `[1/8,9/56]`. Hence

**`[j/7+1/(8c),j/7+9/(56c)]` is six-core-safe, with width `1/(28c)`.**

This is a proved selector with a speed-dependent displacement. It is not
a claim that a fixed finite rational anchor menu is complete. The prior
finite-anchor/early-lap obstruction remains intact.

## 3. Hand pruning to nine pairs

Any case not settled by Section 1 or 2 must have a or b divisible by 7.
Indeed, if neither is divisible by 7, either no residual is divisible by
7, or c is the unique such residual. Inspecting the declared pair table
leaves exactly the following nine pairs. The cap is the integer part of
`2b/(4b w_a-1)`; all displayed denominators are positive.

| (a,b) | cap on c | after the 6-divisibility condition |
| --- | ---: | --- |
| (2,7) | floor(112/13)=8 | none |
| (3,7) | 35 | 12,18,24,30 |
| (3,14) | floor(140/9)=15 | none |
| (6,7) | floor(560/9)=62 | handled as a family below |
| (6,14) | floor(560/29)=19 | 15,...,19 |
| (7,8) | floor(112/9)=12 | 12 |
| (7,9) | floor(126/11)=11 | none |
| (9,14) | floor(140/9)=15 | none |
| (12,14) | 21 | 15,...,21 |

For (6,14) and (12,14), the two fixed residues modulo 8 are respectively
`(6,6)` and `(4,6)`. A single further nonzero residue cannot supply both
3 and 7. Thus Section 1 removes all of their remaining c values except
the 8-divisible c=16.

## 4. The two c=16 cases

Both six-cores `(a,b,c)=(6,14,16)` and `(12,14,16)` are safe on

`[1/8+1/128,1/8+1/112]=[17/128,15/112]`,

whose width is `1/896`. This can be checked without any enumeration:

| speed | phase range on the interval | containing closed safe band |
| ---: | --- | --- |
| 1 | [17/128,15/112] | [1/8,7/8] |
| 4 | [17/32,15/28] | [1/8,7/8] |
| 5 | [85/128,75/112] | [1/8,7/8] |
| 6 | [51/64,45/56] | [1/8,7/8] |
| 12 | [51/32,45/28] | [9/8,15/8] |
| 14 | [119/64,15/8] | [9/8,15/8] |
| 16 | [17/8,15/7] | [17/8,23/8] |

Only one of speeds 6 and 12 is required in each case.

## 5. One common window closes the remaining families

Put `W=[25/56,15/32]`, of width `5/224`. The following exact ranges
show that W is safe for each speed in `{1,3,4,5,6,7,8,10,12}`:

| speed | phase range on W | containing closed safe band |
| ---: | --- | --- |
| 1 | [25/56,15/32] | [1/8,7/8] |
| 3 | [75/56,45/32] | [9/8,15/8] |
| 4 | [25/14,15/8] | [9/8,15/8] |
| 5 | [125/56,75/32] | [17/8,23/8] |
| 6 | [75/28,45/16] | [17/8,23/8] |
| 7 | [25/8,105/32] | [25/8,31/8] |
| 8 | [25/7,15/4] | [25/8,31/8] |
| 10 | [125/28,75/16] | [33/8,39/8] |
| 12 | [75/14,45/8] | [41/8,47/8] |

This directly settles `(7,8,12)`. It also provides a five-core window for
every `(3,7,c)` or `(6,7,c)`. If c>=12, a speed-c open blocking occurrence
has width `1/(4c)<=1/48<5/224`. A closed interval longer than that blocked
width must contain a positive safe subinterval: either a whole safe gap
lies inside, or at most one blocked occurrence separates two end pieces.
More quantitatively, the already stated clipping lemma gives width at least

`min(3/(4c),(5/224-1/(4c))/2)>0`.

For the remaining `(6,7,c)` cases, c=8 is safe on W; c=9,10 use the
leftward eighth-anchor rule since the residuals avoid classes 0 and 3;
and c=11 has the explicit safe interval `[17/56,5/16]`, width `1/112`.
Its speed phases are contained respectively in the safe bands
`[1/8,7/8]`, `[9/8,15/8]`, `[9/8,15/8]`, `[9/8,15/8]`,
`[17/8,23/8]`, `[25/8,31/8]` for speeds 1,4,5,6,7,11.

For optional hand verification of the four `(3,7,c)` remainders,
the following direct windows suffice:

| c | safe window | width |
| ---: | --- | --- |
| 12 | [25/56,15/32] | 5/224 |
| 18 | [65/144,15/32] | 5/288 |
| 24 | [25/56,29/64] | 3/448 |
| 30 | [25/56,37/80] | 9/560 |

## Conclusion and limits

Given the structure review's analytic reduction to the displayed 36 pairs,
these symbolic certificates leave no exceptional triple in that remainder.
They therefore complete that route to positive six-core safety. Every
step concerns the selected reference and fixed core `{1,4,5}`; it does not
assert positive final seven-constraint measure or settle the full conjecture.
The standard known result for seven total runners supplies a different
existence route, which must retain its own source attribution.

The useful relational fact in the modulo-7 selector is that the three fixed
core speeds jointly leave all three forward directions available; each of
the two other noncolliding speeds can veto at most one direction. The
surviving direction exists because of this joint compatibility, not because
of an individual runner's blocked fraction.
