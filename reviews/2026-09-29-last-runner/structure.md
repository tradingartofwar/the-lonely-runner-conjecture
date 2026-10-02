# Exact last-runner containment and integer endpoint slack

September 29, 2026. Parent `f3c26e709fa1cd8945968dcd585bd012430c7243`.

**HYPOTHESIS / proof candidates.** These elementary derivations have material
AI involvement and await external review. No executable mathematical
evaluation was performed for this report. The generic interval identities
are a reformulation of the repository's existing exact interval work; no
novelty or new Lonely Runner existence result is claimed.

Let `C={1,4,5,a,b,c}` be the common-start integer six-constraint core,
and let `S_C={t in [0,1]: ||vt||>=1/8 for all v in C}`. Write its maximal
positive closed components and isolated points as `[l_j,r_j]`, allowing
`l_j=r_j` for a point. Since speed 1 belongs to C, all these endpoints
lie in `[1/8,7/8]`. The preceding six-core result supplies at least one
positive component. Put `delta=1/8` throughout.

## 1. Exact strict containment, with equality retained as safety

For real `x` and `rho>=0`, the maximum of distance to the integers on the
closed interval `[x-rho,x+rho]` is

`min(||x||+rho,1/2)`.

The upper bound follows from the Lipschitz inequality and the universal
bound 1/2. Moving from x toward a nearest half-integer attains the smaller
of these bounds. Therefore, for any positive real d and closed component
I with midpoint x and halfwidth h,

`I is contained in {t:||dt||<delta}`

if and only if

`||d*x||+d*h<delta`.                                           (1)

The capped maximum is essential when stating its value, but the cap
disappears from the strict comparison because `delta<1/2`.

Equivalently, the connected interval dI must fit into a single open
blocking lap. Thus there must be an integer m satisfying

`d*r-delta < m < d*l+delta`.                                   (2)

The possible m is unique, since this open interval has length at most
`2*delta=1/4`. The exact integer test is

`floor(d*r-delta)+1 <= ceil(d*l+delta)-1`.                       (3)

The two strict signs cannot be replaced by weak signs: failure at an
endpoint gives a valid final lonely moment. Equations (1)--(3) also
apply to isolated points by setting h=0. A complete absence of final
safe time is equivalent to (2) on **every** component and isolated point.
Coverage of positive components alone does not settle the question.

## 2. A complete real-d band description on one core period

For fixed component j and integer lap m, (2) gives the open d-band

`((m-delta)/l_j, (m+delta)/r_j) intersect (0,infinity)`.

The complete blocker set for the supplied core period is therefore

`D_C = intersection_j union_(m in Z)
       ((m-delta)/l_j,(m+delta)/r_j) intersect (0,infinity)`.     (4)

If a positive component has width w, every d in D_C satisfies
`d<1/(4w)`. Consequently the bands and relevant lap labels are finite
after imposing `d>c` and the widest-component upper bound.

Equation (4) is exact for arbitrary real d **on the fixed domain [0,1]**.
For an integer d, all runners have period 1 and the test is complete for
all time. For noninteger d, a statement about one core period is not
automatically a statement about all time.

For integer d, reflection sends `[l,r]` to `[1-r,1-l]` and the unique
covering label m to `d-m`. Reflected requirements are redundant. This
identity is not available unchanged for arbitrary real d or a shifted
final-runner phase.

## 3. Exact endpoint residues plus one width cap suffice

Every genuine core threshold endpoint has a reduced form p/q with
`gcd(p,q)=1` and `8|q`: before reduction its numerator is odd and its
denominator is 8v. Strict blocking by integer d is exactly

`d*p mod q belongs to {-(q/8-1),...,q/8-1} mod q`.              (5)

Thus the permissible residues of d modulo q are obtained by multiplying
this centered integer interval by the inverse of p modulo q.

For a positive component I, suppose both endpoints satisfy (5), and
`d*width(I)<1/4`. Their containing blocking laps must be the same:
distinct laps are separated by a safe phase gap of length 3/4, larger
than the phase distance between the endpoints. Hence the whole interval
is covered. Conversely, complete strict coverage implies both endpoint
conditions and the width cap.

It follows that complete coverage can also be represented as the
intersection of the endpoint residue conditions (including isolated
points), together with `d<1/(4*w_max)`. This is a congruence problem
with a size constraint. The endpoint congruences alone are insufficient:
a multiple of all endpoint denominators sends every endpoint to phase
zero, but such a large d can fail to cover every interval interior.

The shared residues can be combined by the generalized Chinese
remainder condition: selected local residues at denominators q and u
must agree modulo `gcd(q,u)`. This gives an exact arithmetic interface,
not an automatic contradiction for every core.

## 4. Integer slack strengthens the raw width obstruction

Suppose a component `[l,r]` with reduced endpoints `l=p/q`, `r=s/u`
is strictly contained in the lap centered at integer m. Because 8
divides both denominators, its inward endpoint slacks obey

`d*l-(m-1/8) >= 1/q`,

`(m+1/8)-d*r >= 1/u`.

Adding the two inequalities gives the necessary condition

`d*(r-l) <= 1/4 - 1/q - 1/u`.                                 (6)

This is stronger than `d*(r-l)<1/4`. It is a lattice consequence of
integer d and the actual endpoint denominators; it is not valid for
arbitrary real d. In exact integer form the covering label must satisfy

`d*s-u/8+1 <= u*m`,

`q*m <= d*p+q/8-1`.                                            (7)

Equality in (6) is possible and must not be discarded. An isolated
point is governed directly by (5), not by a positive-width conclusion.

## 5. Controlling runner residues provide additional slack constraints

A left endpoint of a positive maximal component is an entering safety
threshold for at least one core speed v; a right endpoint is an exiting
threshold for at least one speed w. Write these as

`l=(8k+1)/(8v)`, `r=(8h-1)/(8w)`.

If a threshold with the opposite orientation were active at the left
endpoint, it would block the immediate interior, contradicting the
positive component; the analogous statement holds at the right.
When several speeds control a boundary, every resulting necessary
inequality applies.

For a positive integer z, or any integer residue, define R8(z) as its
least positive residue in `{1,...,8}`; a zero residue has R8 value 8.
If integer d covers I in lap m, its left slack numerator is

`N_l = d*(8k+1)-v*(8m-1)`

`    = 8*(k*d-m*v)+(d+v) > 0`.

Let `g_v=gcd(d,v)`. Then

`N_l/g_v = 8*(k*d/g_v-m*v/g_v)+(d+v)/g_v`

is a positive integer in the residue class `(d+v)/g_v` modulo 8.
Consequently

`left slack >= g_v*R8((d+v)/g_v)/(8v)`.

The right slack numerator is

`N_r=w*(8m+1)-d*(8h-1)=8*(m*w-h*d)+(w+d)>0`,

giving the analogous inequality with w. Define

`lambda(d,v)=gcd(d,v)*R8((d+v)/gcd(d,v))`.

Every complete cover therefore requires, for every positive component,

`d*(r-l) <= 1/4-lambda(d,v)/(8v)-lambda(d,w)/(8w)`.              (8)

The weaker residues `R8(d+v)` and `R8(d+w)` already give necessary
conditions; retaining the gcd can strengthen them substantially. Both
equations follow from the same common lap label m and common integer d.
If the right side of (8) is negative, or is smaller than the left side,
the component contains a final-safe moment.

These controller bounds are complementary to the reduced-denominator
bounds in Section 4, not uniformly stronger. The valid combined left
bound is the maximum of `1/q` and all available
`lambda(d,v)/(8v)` controller bounds; similarly on the right. For
example, the entering endpoint 1/8 can be controlled by v=9. At d=16,
that controller's lambda bound is 1/72, whereas the reduced-denominator
bound is 1/8. A controller-only estimate must not erase the latter.

A particularly simple consequence is:

**If v controls a core endpoint and v divides d, strict blocking of that
endpoint requires 8v to divide d.**

Indeed, at an endpoint `(8k +/- 1)/(8v)`, if d=tv its final phase is
`+/- t/8` modulo 1. A multiple of 1/8 lies at distance strictly below
1/8 exactly when it is zero. Thus `t=0 mod 8` is necessary and
sufficient for blocking that endpoint. This can eliminate an entire
arithmetic class of d without reconstructing a final safe-time set.

## 6. Linked lap differences, and the limitation of local tests

For components with midpoints x_i and halfwidths h_i, complete coverage
requires integer labels m_i with

`|d*x_i-m_i| < e_i`, where `e_i=1/8-d*h_i>0`.

Subtracting two such requirements gives

`|d*(x_j-x_i)-(m_j-m_i)| < 1/4-d*(h_i+h_j)`.                    (9)

The differences are integers and must satisfy all cycle identities,
for example `(m_j-m_i)+(m_k-m_j)=m_k-m_i`. The actual labels cannot
be selected as unrelated phases on different components. Equation (9)
is necessary, while pair difference conditions by themselves do not
fix the absolute common-start phase. Equation (4), or equivalently
the endpoint residues plus width cap, retains that information exactly.

These descriptions advance the arithmetic interface but do not prove
that D_C contains no admissible integer for every core. An independently
declared exact diagnostic can test how much the integer slack and
endpoint residue restrictions actually eliminate. The unresolved
structural task is to force their incompatibility, with equality
witnesses retained. No broad tuple or phase search is part of this report.

## 7. A concrete integer obstruction on the inherited (3,7,24) core

The prior independently checked table supplies the core-safe interval

`I=[25/56,29/64]`, with `width(I)=3/448`,

for C={1,4,5,3,7,24}. Its reduced endpoint denominators are 56 and 64.
Equation (6) makes strict coverage possible only if

`3d/448 <= 1/4-1/56-1/64=97/448`, hence `d<=97/3`.

Thus d>=33 already succeeds by endpoint arithmetic, improving the raw
widest-window sufficient cutoff of 38 for integer final speeds.

In fact the **same one interval** guarantees a final-safe moment for
every integer d>24. Its possible covering bands are exactly

`((56m-7)/25,(64m+8)/29)`.                                     (10)

For d>24, an intersecting band requires m>=11. A nonempty band requires

`29*(56m-7)<25*(64m+8)`, equivalently `24m<403`,

so m<=16. These six bands are contained strictly between consecutive
integers as follows:

| m | Exact band | Integer-free containing interval |
| ---: | --- | --- |
| 11 | (609/25,712/29) | (24,25) |
| 12 | (665/25,776/29) | (26,27) |
| 13 | (721/25,840/29) | (28,29) |
| 14 | (777/25,904/29) | (31,32) |
| 15 | (833/25,968/29) | (33,34) |
| 16 | (889/25,1032/29) | (35,36) |

All comparisons are direct integer cross-products. No band contains an
integer, proving the claimed fixed-core family certificate. This is a
six-lap hand argument from the declared inherited component, not a
computed configuration search. The corresponding existence conclusion
is already covered by the known eight-runner theory; the contribution
here is an explicit local arithmetic certificate inside this framework.

The argument actually guarantees **positive final safe duration** for
every integer d>24. Replacing strict blocking with closed blocking
replaces (10) by the corresponding closed bands. The nonempty condition
becomes `24m<=403`, giving the same integer labels 11 through 16, and
all six closed bands still lie strictly inside the displayed open
integer-free intervals. Thus some point of I has final distance
strictly greater than 1/8. By continuity a subinterval in the interior
of I retains that strict inequality. Each core constraint is strictly
safe in the interior of its positive safe component, so this subinterval
has all seven distances strictly above 1/8. This strengthening was
checked in the separate internal challenge review; external review
and novelty assessment remain pending.

The bands are nonempty as **real** intervals. Thus a noninteger final
speed can cover this selected window even though every admissible integer
speed fails to cover it. This records precisely which arithmetic
information the raw component-width bound discards. It says nothing
by itself about coverage of every other component or every later core
period for a noninteger speed.
