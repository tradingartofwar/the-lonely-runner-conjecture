# Adversarial review: seven-runner margin bridge

Date: September 29, 2026. Research parent: `da05361310a6e0d5607fdd7565ad226f637c8305`.

This is a materially AI-assisted internal audit. The local deductions remain
**HYPOTHESIS / proof candidates** pending external review. The lower-runner
input is credited literature; this audit does not independently reproduce its
published proof. No new mathematical executable domain was evaluated.

## 1. Claim checked

For the common-start integer family

`{0,1,4,5,a,b,c,d}`, with `a<b<c<d` distinct and outside `{1,4,5}`,

the proposed bridge imports the known seven-total-runner theorem for the
six-constraint core `{1,4,5,a,b,c}`, obtains a positive closed safe window
at threshold 1/8, and proves that `d>=7c` suffices for the selected reference 0.

The literature collaborator identified Barajas and Serra, *The Lonely Runner
with Seven Runners*, arXiv:0710.4495v1 (October 24, 2007), published in
*Electronic Journal of Combinatorics* 15(1), R48 (March 20, 2008),
DOI `10.37236/772`. Its convention is `k+1` total runners, `k` positive
integer speeds, and separation `1/(k+1)`. Therefore six positive speeds
give threshold 1/7. Its gcd-one normalization holds here because speed 1 is
present. The source inspection and its extent belong in the literature review.

## 2. Line-by-line bridge audit

**Maximum-speed premise.** There are only two admissible positive residual
speeds below 6, namely 2 and 3. Since a, b, c are three distinct sorted
residuals, `c>=6`. Thus c is indeed the maximum of the six core speeds,
including fixed speeds 4 and 5. This premise should be stated; merely writing
`a<b<c` would not establish it for an arbitrary fixed core.

**Margin.** The seven-total-runner theorem supplies a time t0 such that

`||v t0|| >= 1/7` for every `v in {1,4,5,a,b,c}`.

Distance to the nearest integer is 1-Lipschitz on the real line. For every
such v and every `|h|<=r=1/(56c)`, therefore,

`||v(t0+h)|| >= ||v t0|| - v|h| >= 1/7-c/(56c)=1/8`.

The closed interval `W=[t0-r,t0+r]` is six-core safe and has width
`2r=1/(28c)`. A one-sided radius would lose a factor of two; the claimed
constant correctly uses both sides.

**Period and wrap.** All speeds are integers, so t0 may be reduced modulo 1.
The speed-1 constraint gives `t0 in [1/7,6/7]`. Since `r=1/(56c)<1/7`,
the whole interval W lies inside [0,1]. No circular clipping or window split
is necessary. Alternatively the argument works on the real time line.

**Final blocker.** The d-blocked set is the disjoint union of the open intervals

`((j-1/8)/d,(j+1/8)/d)`, for integer j,

each of width `1/(4d)`. If a connected closed interval were entirely blocked,
it would have to lie inside a single one of these open components, and its
width would consequently be strictly smaller than `1/(4d)`. Thus every
closed interval of width at least `1/(4d)` contains a d-safe point.

For `d>=7c`,

`1/(4d) <= 1/(28c) = width(W)`.

This establishes the desired simultaneous safety. The equality case
`d=7c` is valid: an open blocker cannot cover both endpoints of a closed
interval of the same width. Threshold equality must remain safe.

**Phases and scaling.** No shifted lower-runner theorem is invoked. The six
core speeds start together. The last-blocker argument itself tolerates any
phase of d, but that auxiliary strengthening does not justify arbitrary
phases for the six core runners. Integer periodicity is used for the [0,1]
normalization; the ratio calculation by itself does not extend the entire
fixed-core family to arbitrary real speeds or other selected references.

**Verdict:** no flaw was found in this bridge under the explicitly sourced
seven-total-runner input. It is an elementary consequence of a known margin,
not a novelty claim or a replacement proof of that input.

## 3. What the finite reduction does and does not say

Combining the bridge with the prior proof-candidate cutoffs leaves only

`a<=34`, `b<=47`, `c<=1565`, and `d<7c`.

Because d and c are integers, the last condition is

`d<=7c-1<=7*1565-1=10954`.

These bounds give a finite set of configurations still uncertified by the
sufficient tests, conditional on the prior core-window arguments. The tighter
coupled inequality `d<=7c-1` should be retained when stating that set.
They do not establish that any point in this set is a counterexample, nor
that every point has already been checked. No exhaustive tuple calculation
was performed in this audit.

The theorem supplies existence of t0. Once a concrete t0 is available, the
last step is constructive: use W's left endpoint if it is d-safe; otherwise
move to the right boundary of the unique d-blocker containing it. That move
is at most one blocker width and stays inside W. This does not make the
literature existence input itself a newly implemented fast witness algorithm.

The argument concerns one fixed-core family and selected reference 0. It
does not establish the full eight-runner conjecture, any all-reference
statement for arbitrary inputs, or a new runner-count frontier. Current
literature claims beyond seven runners require separate source/proof status;
they cannot be conflated with what this local audit checked.

## 4. Exact singleton placed masses still lose decisive information

Let S be the safe set for `{1,4,5}`, of measure 3/8, and let
`Q(v)=measure(S intersect B_v)`. The already independently verified 31-case
records give

`Q(6)=17/120`, `Q(7)=89/560`, `Q(11)=93/880`.

Using even these exact placed masses in a three-deletion union bound yields

`3/8-Q(6)-Q(7)-Q(11) = -289/9240 < 0`.

This is a failure of that lower-bound certificate, not evidence of failed
core safety. In fact the same archived four-core component lists contain

- for speed 6: `[9/32,5/16]`;
- for speed 7: `[17/56,3/8]`;
- for speed 11: `[25/88,31/88]`.

Their intersection is the closed interval `[17/56,5/16]`, of width 1/112.
It is safe for `{1,4,5,6,7,11}`. This recombines already verified records;
it adds no executable tuple or phase domain. It may also be checked directly:
the fractional lap ranges on that interval are

| v | Fractional lap range |
| ---: | --- |
| 1 | `[17/56,5/16]` |
| 4 | `[3/14,1/4]` |
| 5 | `[29/56,9/16]` |
| 6 | `[23/28,7/8]` |
| 7 | `[1/8,3/16]` |
| 11 | `[19/56,7/16]` |

Every range lies in `[1/8,7/8]`.

The exact six-core measure formula contains the correction

`Q67+Q6,11+Q7,11-Q6,7,11`.

The singleton data erase this joint information. The positive explicit
interval proves that the negative singleton bound can coexist with usable
clear time. This supports examining the joint correction directly; it does
not prove that an arbitrary pairwise summary will suffice or that a new
configuration invariant has been identified.

## 5. Preservation requirements

- Keep the known lower-runner theorem separate from the local proof candidate.
- Keep the exact `[17/56,5/16]` witness separate from the unsuccessful marginal
  lower bound; neither is a fresh full-configuration search result.
- Keep equality safe and final blockers open throughout.
- Keep finite reduction distinct from finite exhaustion.
- Positive width is guaranteed for the six-core stage. Positive duration is
  not imposed on the final seven constraints, where tight equality-only
  configurations must remain valid.
- No external review, novelty assessment, broad scan, outreach, paid compute,
  automation restart, or main-branch merge occurred in this audit.

## 6. Additional audit: direct six-core reduction

The coordinator subsequently prioritized the direct route in `structure.md`.
The frozen protocol is `PROTOCOL.json`, SHA-256
`25c818133f6e78054d14e82bf4b0f0c6b63c9dd7d1ca9a12071d83f878b891a2`.
The following audit is symbolic: this investigator did not execute its domain.

### Strict pair-window test

The implication from `T2(b,c)<w_a` to positive six-core duration is valid,
but it requires more than the previous non-strict point-existence result.
The closed-blocker proof in the structure report supplies that missing step:
with lengths P/4 and q/4, a chain of overlapping or touching closed blockers
has at most one P occurrence and two q occurrences. Indeed, a repeated P
would contain a consecutive P,q,P segment whose right-endpoint advance is
at most `(P+q)/4<P`, contradicting the period P. Thus a connected component
of the closed blocked union spans at most `P/4+q/2=T2`.

If a closed four-core component W has width greater than T2, it contains
a point outside that closed union. The complement is relatively open in W,
so it contains a positive interval meeting W's interior. Every point in
the interior of a positive four-core safe component is strictly safe for
the four original speeds: a threshold crossing would have a blocked side
and could not lie in that interior. This proves positive six-core duration.

An independent way to check the endpoint issue is to trim W to an interior
closed interval still wider than T2, then choose `delta>1/8` sufficiently
close to 1/8 with `delta<1/4` and
`2*delta*(1/b+2/c)<width(trimmed W)`. The same chain counts hold since
`2*delta*(P+q)<P`. The resulting delta-safe residual point has strict
1/8 margin for all six speeds. Both derivations preserve the need for a
strict inequality in the positive-duration test.

### All a values and all 36 pair branches

For a>=19, the fixed-core window J contains a full a-safe gap: its width
3/32 is at least `P+S=7/(4a)`, where P=1/a and S=3/(4a). Any interval
at least P+S long contains one complete periodic safe gap. The inherited
clipping inequality gives the same conclusion. Since b,c>a, their pair
budget is strictly below `3/(4a)`.

For a=11,13,14,16,17,18, the inherited exact widest widths equal
`3/(4a)` and give the identical implication. For a=8,
`T2(9,10)=7/90<5/64`, with difference 1/2880. This leaves exactly
the eight a rows listed in the frozen protocol.

For each row, `F(b)=1/(4b)+1/(2(b+1))` strictly decreases with b.
Checking the last potentially valid b and its successor gives precisely
the branch ranges below. The omitted b=4,5 are inadmissible. For a=2,b=3,
the first admissible c is 6; it still satisfies the failure inequality,
so no branch is spuriously introduced by using b+1 to bound the others.

| a | Included b | Last b | Largest possible c |
| ---: | --- | ---: | ---: |
| 2 | 3,6,7 | 7 | 48 |
| 3 | 6 through 14 | 14 | 60 |
| 6 | 7 through 16 | 16 | 62 |
| 7 | 8,9 | 9 | 12 |
| 9 | 10 through 14 | 14 | 20 |
| 10 | 11 | 11 | 12 |
| 12 | 13 through 17 | 17 | 22 |
| 15 | 16 | 16 | 17 |

The row counts sum to `3+9+10+2+5+1+5+1=36`.
In all rows `w_a-1/(4b)>0`; solving the failure inequality gives

`c<=floor(1/(2*(w_a-1/(4b))))`.

This bound decreases as b increases. Substituting each row's least b gives,
before flooring, respectively

`48,60,560/9,112/9,20,88/7,156/7,160/9`.

Hence the global cutoff c<=62 is correct. These are hand algebra checks,
not an additional executed domain or an empirical cutoff fit.

### Strict anchor filters

At t=1/6 all three fixed core speeds are strictly safe; any integer
residual not divisible by 6 has distance at least 1/6. Thus absence of
a multiple of 6 in a,b,c certifies positive six-core duration.
The same argument at t=1/7 gives a strict certificate unless one of a,b,c
is divisible by 7.

If none of a,b,c is divisible by 8, t=1/8 is safe. Its only runners
that become unsafe immediately to the right have residue 7 modulo 8.
The fixed-core speed 1 instead improves to the right. Thus absence of
residue 7 certifies a strict interval to the right of 1/8.
At t=3/8, moving left improves the fixed speed-5 threshold contact.
The obstructing residual residue is 3 modulo 8, since `3*v=1 mod8`
puts that runner at a threshold that worsens when time decreases.
Therefore absence of residue 3 certifies a strict left neighborhood.

The complete necessary condition for surviving these two eighth-anchor
tests is exactly the protocol's condition: either one of a,b,c is
divisible by 8, or their residues include both 3 and 7 modulo 8.
No condition on final speed d is needed or intended at this six-core stage.

### Supplemental unique seventh-divisor certificate

The separate arithmetic argument also checks cleanly. If c is the unique
residual divisible by 7, select j in {1,2,3} avoiding `j*a=6 mod7` and
`j*b=6 mod7`. Each of a,b excludes at most one j, so a choice remains.
The fixed speeds 1,4,5 never have residue 6 at any of these j. Every slower
core speed therefore has phase k/7 with 1<=k<=5. For

`t=j/7+u`, `1/(8c)<=u<=9/(56c)`,

each slower phase lies strictly between 1/8 and 7/8, because its upper
bound is strictly below `5/7+9/56=7/8`. The c phase is in
`[1/8,9/56]`. This gives a closed safe interval of width 1/(28c).
The frozen computational protocol intentionally does not use this
additional pruning, and should remain unchanged.

### Endpoint quantum and direct final-speed cutoff

Assume a positive six-core component has been established by the direct
route. Its endpoints are threshold events of the form `(8j+/-1)/(8v)`.
For endpoints associated with speeds v,w, any positive difference is an
integer multiple of `1/(8*lcm(v,w))` and is therefore at least that much.

Let `M=max(5,b)`. Since c>=6, the two largest distinct six-core speeds
are c and M. For distinct v,w, `lcm(v,w)<=v*w<=M*c`. For v=w,
`lcm(v,w)=v<=c<=M*c`. Thus every positive component has width at least

`1/(8*M*c)`.

The final open d-blocker cannot cover a closed window of this width when
`d>=2*M*c`. Combining with the prior candidate bounds b<=47 and c<=1565
leaves only

`d<=2*47*1565-1=147109`.

This is a valid conservative direct cutoff, conditional on closure and
verification of the six-core remainder plus the prior cutoff arguments.
It is weaker than the literature-assisted d<=10954 cutoff and should be
identified separately. Neither bound is an exhaustive verification of the
remaining four-residual configurations.

## 7. Supplemental literature-assisted cutoffs

These sharper constants are separate from the direct six-core construction.
They additionally require the known six-total-runner theorem, which supplies
threshold 1/6 for five positive integer constraints. The seven-total-runner
threshold 1/7 alone is not enough for the following five-core window width.
The literature review must identify the six-total-runner source separately.

For the five-constraint core `{1,4,5,a,b}`, put `M=max(5,b)`. The known
1/6 witness, combined with Lipschitz margin `1/6-1/8=1/24`, gives a
closed 1/8-safe window of width `1/(12M)`.

A sharper two-residual chain estimate is valid: every strict connected
blocking chain for c<d spans less than `1/(2c)`. The earlier chain counts
allow one slow c occurrence and at most two fast d occurrences. With at
most one fast occurrence, total span is less than
`1/(4c)+1/(4d)<1/(2c)`. With two fast occurrences, the chain must have
form fast-slow-fast. The slow blocker strictly bridges the fast safe gap
of width `3/(4d)`, so `1/(4c)>3/(4d)` and hence `d>3c`. Its span is
then less than

`T2=1/(4c)+1/(2d)<1/(4c)+1/(6c)=5/(12c)<1/(2c)`.

This covers all possible chain shapes. Thus `c>=6M` suffices in the
literature-supplied five-core window, regardless of the distinct larger d.
The uncertified integer c values satisfy `c<=6M-1<=281` when M<=47.

There is also a valid d-only cutoff at `d>=27M`. If `c<=d/7`, the
seven-total-runner bridge gives success immediately. Otherwise `c>d/7`,
and the original pair budget obeys

`T2<7/(4d)+1/(2d)=9/(4d)<=1/(12M)`.

Thus the five-core window succeeds in the second case as well. The split
includes the equality case c=d/7 in the first branch. Consequently the
uncertified integer d values satisfy `d<=27M-1<=1268` when M<=47.

These arguments support the separately credited literature-assisted bounds
`c<=281,d<=1268`; they do not improve the constants of the self-contained
route without importing those known lower-runner margins. This audit has
not undertaken further optimization or evaluated additional cases.
