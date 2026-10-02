# Arithmetic and translated-core alternatives

September 29, 2026. Internal arithmetic/window-selection review, under the
root's pinned research state `db2867ed65c4df3668f5275878f21ba400faff2b`.

**Status: HYPOTHESIS / analytic proof candidates; external mathematical and
novelty review pending.** No executable check, speed-tuple scan, new physical
fixture, phase scan, or literature novelty assessment was performed. This
report was generated with material AI assistance. It concerns only reference
0 in the common-start integer configuration
`{0,1,4,5,a,b,c,d}`, at threshold `1/8`, with four distinct positive residual
speeds `a<b<c<d` outside the fixed core.

## Result for a large residual gcd

Let `g=gcd(a,b,c,d)`. The proposed sufficient statement is

> If `g>=7`, the full common-safe set in `[0,1]` has positive measure at least
> `3/(4d)`, independently of the residual ratios and of the fixed-window
> sufficient inequality `H<=3/32`.

This uses all core-safe components, not just `J=[9/32,3/8]`. It does not
classify the remaining configurations or assert that the condition is
necessary. In particular, `g<=6` does not imply a failure of loneliness.

### 1. An exact grid-hitting property of the core

Write

`F={t mod 1 : ||t||, ||4t||, ||5t|| >= 1/8}`.

For an integer `g>=1`, consider the property

`F intersects {u+j/g mod 1 : j=0,...,g-1} for every real u`.       (G)

**Claim: (G) holds exactly when `g>=7`.** The implication needed for the
residual argument is the positive half, proved case by case below without a
search.

For an equally spaced grid with `m` points, any open circular arc of length
`1/4` contains at most `ceil(m/4)` points. When `m/4` is an integer the open
endpoints still give the same bound. A speed coprime to `m` permutes that
grid.

* `g>=11`: the closed core-safe interval `J` has length `3/32>=1/g`, so it
  meets every grid coset. This also gives an independent simple argument for
  all sufficiently large `g`.
* `g=7`: each of speeds `1,4,5` blocks at most two of the seven grid points.
  Their union blocks at most six, leaving a core-safe point.
* `g=8`: split the grid into its two parity classes. Speed 4 has constant
  phase in each class, and the two phases differ by `1/2`. Choose a class
  where its distance is at least `1/4`. The chosen class consists of four
  points spaced by `1/4`; speeds 1 and 5 each block at most one of them.
  At least two points remain safe for all three core speeds.
* `g=10`: split into parity classes and select one where speed 5 has
  distance at least `1/4`. Its five time points are spaced by `1/5`.
  Speeds 1 and 4 each block at most two points, leaving at least one.
* `g=9`: each core speed blocks at most three points, since all are coprime
  to 9. If speed 1 blocks at most two, the union has size at most eight.
  Otherwise, its three blocked points are consecutive in the arc
  `(-1/8,1/8)`. Write their middle point as `x mod 1`, with its nearest
  integer chosen so that the other two are `x-1/9` and `x+1/9`. Strict
  blocking of both outside points gives `|x|<1/8-1/9=1/72`.
  Consequently `||4x||<4/72<1/8` and `||5x||<5/72<1/8`: all three core
  blockers share this grid point. The sum of their cardinalities is at
  most nine, and this triple overlap reduces the union bound by at least
  two, leaving at least two safe points.

All blockers are open. Equality at `1/8` is retained throughout, including
the four-point parity argument where a closed bad arc would give a different
count. The chosen parity's controlling speed has a strict `1/4` margin.

For completeness, the negative half of (G) has explicit cosets:

| g | A coset avoiding F | Blocking reason |
| ---: | --- | --- |
| 1, 2, 4 | `{j/g}` | Speed 4 is integral at every point. |
| 5 | `{j/5}` | Speed 5 is integral at every point. |
| 3 | `{1/12,5/12,9/12}` | Blocked respectively by speeds 1, 5, 4. |
| 6 | The six odd twelfths | Speeds 1 block `1/12,11/12`; 4 blocks `3/12,9/12`; 5 blocks `5/12,7/12`. |

These are auxiliary grid cosets, not proposed physical residual
configurations. Their failure does not show that the actual residual-safe
set can be confined to such a coset. They locate the exact limit of the
universal translated-core statement.

### 2. Common start supplies positive residual-safe measure

Let `R` be the set safe for the four residual speeds, and let `M` be their
blocked multiplicity. All four are periodic with common period `T=1/g`.
On one such period each blocker has measure `T/4`; hence

`integral_0^T M(t) dt = T`.

At both ends of this period all four runners collide. They are all blocked
on `(0,1/(8d))` and `(T-1/(8d),T)`, total length `1/(4d)`. The intervals
are disjoint. Therefore

`integral_0^T (M-1)_+ dt >= 3/(4d)`.

Since `M` is integer-valued and `integral(M-1)=0`, its negative part is
exactly the indicator of the residual-safe set up to measure-zero
thresholds. Thus

`measure(R intersect [0,T]) = integral_0^T (M-1)_+ dt >= 3/(4d)`. (1)

This is an elementary common-start excess calculation. It does not invoke
the 23-move candidate, nor assume a residual-safe point has positive
duration merely because some point exists. The common overlap establishes
the positive measure directly.

### 3. Transfer across all core windows

Residual safety is invariant under translation by `j/g`. Partitioning the
unit period into its `g` subperiods gives

`measure(F intersect R) = integral_0^(1/g) 1_R(u) sum_(j=0)^(g-1) 1_F(u+j/g) du`.

For `g>=7`, (G) makes the sum at least one for every `u`. Equation (1)
then yields

`measure(F intersect R) >= measure(R intersect [0,1/g]) >= 3/(4d)>0`.

Since the speeds are finite integers, these sets have finitely many
thresholds in one period. Positive measure therefore includes a
positive-length interval, not only isolated equality points.

For `g<=10`, the width of `J` is strictly smaller than the grid spacing
`1/g`; hence J alone cannot hit every grid coset. The small-gcd part of the
argument genuinely uses the union of available core windows. It preserves
the phase relation between the three core speeds while translating the
same residual-safe occurrence.

## Elementary residue filters for the remaining work

At a rational anchor `1/q` with `q<=8`, every positive integer speed not
divisible by q is at distance at least `1/q>=1/8`. The core speeds are all
nonzero modulo `q=6,7,8`. Therefore:

* if no residual is divisible by 6, `t=1/6` is a witness;
* if no residual is divisible by 7, `t=1/7` is a witness;
* if no residual is divisible by 8, `t=1/8` is a witness (indeed every odd
  eighth is a witness).

Consequently a configuration not already certified by these elementary
anchors and the gcd argument must have `g<=6` and must contain at least
one residual divisible by each of `6,7,8`. One residual may meet several
of these requirements. Combined with the inherited H-width test, any
remaining failure of these sufficient certificates has `a<=34` as well.
These are restrictions on unresolved certificate cases, not necessary
conditions for a mathematical counterexample.

The sixth-anchor condition strengthens the initially suggested third-anchor
filter: absence of a multiple of 3 also makes `1/3` safe, but absence of a
multiple of 6 is sufficient at `1/6` even if an odd multiple of 3 occurs.
At `1/6` the core distances are `1/6,1/3,1/6`, all strictly above threshold.
The required multiples of 6, 7, and 8 may occur anywhere among `a,b,c,d`;
none is asserted to be the smallest residual.

The eighth-grid displacement rule is not complete. At `1/8` the core only
permits an inward forward displacement, and a residual congruent to 7
modulo 8 immediately vetoes that direction. At `3/8` the inward direction
is backward, vetoed by a residual congruent to 3 modulo 8. The reflections
give the same two conditions. The inherited strict16 control has both
vetoes, through residuals 7 and 11, and a collider 16. Its known interval
elsewhere survives; this adds no new counterexample.

## Prior-work boundary and concrete next distinction

The adaptive reflected-pair note already handles the one-variable family
`{0,1,4,5,6,7,11,V}`, including speed-dependent witnesses when fixed menus
fail. The finite-anchor note already proves that every fixed rational menu
with every fixed finite early-lap budget can fail simultaneously. Neither
is contradicted here: the residual-safe occurrence in the gcd proof is
not restricted to a fixed anchor or an early lap, while its `g` translates
are forced to hit the complete core-safe set.

Sources read locally for this review:

* `notes/SHORT_KERNEL_BOUND_2026_09_28.md` in the prior short-kernel workspace;
* `notes/ADAPTIVE_REFLECTED_PAIR_2026_09_28.md` in the prior repository;
* `notes/FINITE_ANCHOR_OBSTRUCTION_2026_09_28.md` in the anchor-obstruction workspace;
* `notes/COMMON_DISPLACEMENT_CERTIFICATES_2026_09_28.md` in the relational-continuation workspace.

The remaining concrete distinction is between a residual gcd that supplies
a universal core-hitting translation orbit and smaller gcds whose orbits
can miss the core. For `g<=6`, one would need a relation between the actual
residual-safe phase set and the exceptional non-hitting cosets. Merely
knowing its positive measure or one arbitrary safe point does not supply
that relation. No claim that such a relation always exists is made here.
