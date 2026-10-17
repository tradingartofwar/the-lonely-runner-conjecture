# Interval placement and a rational-anchor sufficient rule

October 17, 2026. Rule freeze, before selecting the next validation domain.
Parent study: `b76f57855c1bcd8d1e350bda807848cd0f7987b4`.

Status: elementary derivations and **proof candidates**, materially developed
with AI; no independent human review or novelty claim. This is a refinement of
the existing exact interval/contact representation, using ordinary modular
arithmetic. It does not introduce a new mathematical language.

## 1. Exact obstruction for one interval

Let 0 < d < 1/2, I=[a,b], c=(a+b)/2 and h=(b-a)/2. Write ||x|| for distance
to the nearest integer. For a positive integer added speed r, I contains a
d-safe time if and only if

`||r*c|| + r*h >= d`.

Proof: rI is a connected closed interval. It is wholly unsafe exactly when it
lies strictly inside one open gap (m-d,m+d), for an integer m. This is equivalent
to `|r*c-m|+r*h < d`. Such an m exists exactly when `||r*c||+r*h < d`.
Equality is safe. Equivalently, a blocking integer satisfies

`r*b-d < m < r*a+d`.

This expresses the distinct roles of midpoint placement and width. It is an
equivalent predicate to the earlier first-contact formula, not a stronger
existence theorem or an efficiency result.

For w=b-a>0, all possible blockers satisfy r<2d/w, so the finite domain is
1 <= r < ceil(2d/w). For a rational singleton a=b=u/v in lowest terms, r=v
blocks it. A rational singleton cannot supply a witness for every positive
integer r. If I is already safe for the fixed core, any blocking r is
automatically absent from that core; a repeated core speed cannot block I.

## 2. A sufficient rule with a two-case witness

Choose a reduced rational time u/v, v>=1, with `v*d <= 1`, and a direction
e in {-1,+1}. Let J be the closed interval joining

`t0=u/v` and `t0+e*d/v`.

Assume every fixed positive integer core speed is d-safe throughout J. Then
for **every positive integer added speed r**, the following time is safe for
the core and the added runner:

```
if r is not divisible by v:  t = u/v
if r is divisible by v:      t = u/v + e*d/r
```

Proof: if v does not divide r, reduction of u/v implies the nonzero fractional
part of ru/v is a multiple of 1/v. Its distance from an integer is at least
1/v >= d. If v divides r, ru/v is an integer, and the displacement gives phase
d or 1-d. Moreover r>=v, so d/r<=d/v and the displaced time remains in J.
The core-safety hypothesis covers either time. Endpoint equality is included.

At d=1/n, with n-2 distinct positive core speeds and the reference at 0, this
is a sufficient certificate for the reference runner in a ten-runner problem
when n=10, or more generally an n-runner problem after adding r distinct from
the core. It is not a certificate for every reference runner.

The direction must be fixed and the entire J must be core-safe. Safety at the
anchor alone does not justify the displacement. v*d<=1 is essential to the
nondivisible case; this rule does not assert necessity among all intervals.

## 3. Compile suitable cores from residues

For a fixed speed s let j be the least nonnegative residue of s*u modulo v.
The J condition is equivalent to the following inequalities:

| Direction | Necessary and sufficient endpoint conditions for speed s |
| --- | --- |
| +1 | j >= v*d and j+s*d <= v*(1-d) |
| -1 | j <= v*(1-d) and j-s*d >= v*d |

These inequalities ensure both endpoints stay in the same closed safe band;
affinity ensures safety between them. Conversely a connected safe J cannot
cross an unsafe gap, so its lap stays fixed and these inequalities hold.

At d=1/n the conditions use integers only:

- +1: `n*j >= v` and `n*j+s <= v*(n-1)`.
- -1: `n*j <= v*(n-1)` and `n*j-s >= v`.

This specifies a family of admissible cores: choose any n-2 distinct speeds
meeting one fixed anchor's conditions, then add any other positive integer
speed. No restriction to the earlier p,q coefficient rows is needed. Enumeration
of all such cores is unnecessary; the individual-speed inequalities imply
their joint safety on the same J. The common anchor, direction and interval
must not be chosen separately for each speed.

## 4. A concrete limit of this certificate class

If a positive speed V is safe on J, J must fit into one of its closed safe
bands. Its length d/v therefore satisfies

`d/v <= (1-2d)/V`, hence `V <= v*(1-2d)/d`.

Since v <= floor(1/d), at d=1/10 no speed greater than 80 can appear in a core
certified by this rule. Also no core speed can be divisible by v, because that
speed would have phase zero at the anchor. These are necessary conditions for
this particular rational-anchor rule. They do not rule out another safe
interval, a collection of components, or a different representation.

## 5. Development predictions from the already published three examples

The old 1/10 leaders appear to contain the following J intervals. These are
specific predictions to verify against the frozen existing endpoints, not
fresh-data discoveries:

| Pair | u/v | Direction | J |
| --- | --- | ---: | --- |
| (1,2) | 1/8 | -1 | [9/80, 1/8] |
| (1,4) | 1/9 | -1 | [1/10, 1/9] |
| (1,6) | 3/10 | +1 | [3/10, 31/100] |

If containment and core endpoint inequalities pass, the two-case proof explains
the previous all-r results without a table of small-speed exceptions. The
existing first-contact algorithm already constructs witnesses without scanning
all time laps; no asymptotic speed advantage is being claimed here.

## 6. Representation and validation obligations

Supported output: one physical witness for a selected stationary reference
after adding a positive integer speed. Retained: exact anchor, direction,
threshold, common interval, core speeds, endpoint/lap conditions and divisibility.
Omitted: other safe times, optimum and other reference runners. Recover the
complete core and use the exact obstruction predicate when this sufficient
rule fails; do not call that failure physical nonexistence.

Next validation must pin code and cases before evaluation; compare the exact
obstruction with a differently structured contact computation; verify every
anchor endpoint and generated witness; retain failed sufficient-rule cases.
Distinguish rules derived here from implementation checks and independent proof
review. Select a bounded domain only after this rule document is committed.
