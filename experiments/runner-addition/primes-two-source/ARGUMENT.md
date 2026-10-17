# Why this core needs two connected sources

October 17, 2026. **HYPOTHESIS / proof candidate awaiting independent review.**
This is a retrospective explanation of the already exposed primes-derived
case, not a new experiment, held-out validation, or novelty claim. The argument,
certificate and checker were prepared with AI; the checks have the same author.

**The useful compression:** one fixed interval handles every admissible added
speed except 4 and 8; one fixed time elsewhere repairs both exceptions. Every
single connected core-safe source fails at some admissible speed, so two are
necessary within that source class. The argument below supplies both bounds.

## 1. Statement and scope

Let `S={2,3,5,7,10,13,17,19}`, let `d=1/10`, and write
`||x||=min_{m in Z}|x-m|`. All runners start together. Reference speed is 0;
adding a positive integer `r` absent from S gives ten distinct runners.

The complete core-safe time set in one period is

    C = {t in [0,1] : ||v*t|| >= d for every v in S}.

A menu is a finite collection of fixed connected subsets of C. It succeeds
if for every admissible r some time t in one of its members satisfies
`||r*t||>=d`. The choice of t and member may depend on r. We also consider the
narrower class in which members must be maximal components of C.

**Claim:** the minimum is two in either class. An interval plus a point gives
the first upper bound; enlarging the point to its containing maximal component
gives the second. This concerns the stationary reference only. Naming a
disconnected union as one object changes the counting question.

## 2. Lower bound: every connected source has a blocker

For integer core speeds, `||v(1-t)||=||vt||`. The complete components in the
first half-period are the ten closed intervals below; their reflected copies
`[1-b,1-a]` supply the other ten. There is no component through 1/2 (speed 2
is unsafe there), and neither 0 nor 1 is safe.

The table can be recovered by the exact closed-set intersection

    C intersect [0,1/2]
      = [0,1/2] intersect
        intersection over v in S of
          union over j=0,...,floor(v/2) of [(j+d)/v,(j+1-d)/v].

The checker also reconstructs C directly from every threshold event
`(j+d)/v` and `(j+1-d)/v`: predicates are constant on each intervening open
cell, while event points are tested separately. This establishes completeness
of the table without assuming the earlier classifier's component list.

| Component ID | Closed interval [a,b] | Blocking speed r | Integer m | Open unsafe gap containing the whole interval |
|---|---|---:|---:|---|
| 0 | [11/170,9/130] | 1 | 0 | (-1/10,1/10) |
| 1 | [11/130,9/100] | 1 | 0 | (-1/10,1/10) |
| 2 | [21/190,19/170] | 9 | 1 | (1/10,11/90) |
| 3 | [21/170,9/70] | 8 | 1 | (9/80,11/80) |
| 4 | [31/190,29/170] | 6 | 1 | (3/20,11/60) |
| 5 | [11/50,29/130] | 9 | 2 | (19/90,7/30) |
| 6 | [41/170,49/190] | 4 | 1 | (9/40,11/40) |
| 7 | [51/190,19/70] | 4 | 1 | (9/40,11/40) |
| 8 | [71/190,49/130] | 8 | 3 | (29/80,31/80) |
| 9 | [31/70,9/20] | 9 | 4 | (13/30,41/90) |

Each row asserts the strict inequalities

    (m-d)/r < a <= b < (m+d)/r,

so every t in that interval has `||rt||<d`. All five recorded speeds
`{1,4,6,8,9}` are admissible. Reflection retains r and replaces m by r-m,
giving blockers for component IDs 19-i. Strictness matters: a gap boundary
would be a valid equality witness and could not certify a blocker.

Every connected subset of C lies in a single maximal component, so it inherits
that component's blocker. Hence no one connected source succeeds for all r.
This is `for every component, some blocker`; it is not one speed defeating C.
The upper bound now shows that C actually supplies a witness for every r.

## 3. Upper bound: one interval and one repair time

Use component 6 and the left endpoint of component 0:

    I = [a,b] = [41/170,49/190],    p = 11/170.

For the ordered speeds in S, the constant lap vector throughout I is
`(0,0,1,1,2,3,4,4)`. Direct endpoint inequalities give
`d <= v*a-lap <= v*b-lap <= 1-d` for each v; thus the entire I is core-safe.
The eight phases at p are

    (11/85,33/170,11/34,77/170,11/17,143/170,1/10,39/170),

all in `[1/10,9/10]`. In particular, equality for speed 17 is retained at
both p and a. Component 0 is `[11/170,9/130]` if a maximal-component menu is
desired, but only p is needed for the repair.

The interval has width

    w = b-a = 27/1615,
    (2d)/w = 323/27,    ceil((2d)/w) = 12.

For r>=12, any open unsafe time gap for speed r has length

    2d/r <= 1/60 < 27/1615 = w.

A connected interval of width w cannot fit inside such a gap, so I has a
safe contact. Generally equality of widths also suffices because the unsafe
gaps are open and I is closed. The explicit recovery below avoids leaving
this existence argument without a physical witness.

The admissible speeds below 12 are exactly `{1,4,6,8,9,11}`:

| Added speed r | Chosen time t | Fractional part of r*t |
|---:|---|---|
| 1 | a=41/170 | 41/170 |
| 4 | p=11/170 | 22/85 |
| 6 | a=41/170 | 38/85 |
| 8 | p=11/170 | 44/85 |
| 9 | a=41/170 | 29/170 |
| 11 | a=41/170 | 111/170 |

All phases lie in `[d,1-d]`. The interval I really does fail at 4 and 8:
it lies strictly inside `(9/40,11/40)` and `(19/80,21/80)`, respectively.
Both gaps are centered at time 1/4. The point p is away from these gaps but
it fails at added speed 1. Their different placements make the sources
complementary. This finishes the upper bound and the minimum-two candidate.

## 4. A physical witness rule for the infinite tail

For admissible r>=12, put `x=r*a`, `m=floor(x)`, and `f=x-m`:

    t(r) = a                 if d <= f <= 1-d;
           (m+d)/r           if f < d;
           (m+1+d)/r         if f > 1-d.

In the first case the left endpoint already works. Otherwise, move right to
the next safe boundary. The displacement is less than `2d/r`, hence less
than w, and the resulting phase is exactly d. Thus t(r) belongs to I and
is safe for all eight core runners and the added runner at the same time.
For the finite domain, use the preceding table. Core-speed duplicates remain
excluded even when the tail formula happens to return a safe time for them.

Two fixed rational times are not the same representation as this rule. If we
retain only a and p, added speed 170 makes both phases zero. The interval
rule instead returns `t(170)=411/1700`, inside I with added-runner phase 1/10.
This exact countercheck shows why movable contact within I must be retained.

## 5. Representation record and verification

- **Question and operation:** minimum number of fixed connected sources for
  this one core and threshold, plus recovery of one physical time for each
  admissible added speed.
- **Retained:** all ten first-half components and exact reflection for the
  lower bound; strict blocker gaps; I, p, core validity, admissibility,
  finite exceptions, width and a same-time recovery rule for the upper bound.
- **Omitted:** full child safe sets, all alternative menus, earlier search
  traces and costs, other cores/references and different thresholds. The
  ten-row table can reconstruct C; the smaller pair/rule alone cannot.
- **Recovery:** [CERTIFICATE.json](CERTIFICATE.json) maps local IDs and exact
  fractions to the richer [unrestricted results](../unrestricted-single/results/RESULTS.json)
  and [certificate export](../unrestricted-single/results/CERTIFICATES.json)
  at commit `f7f87f7dd59b4809397730550fb0fd1a48eab2a1`, with SHA-256 bindings.
  Earlier [width/placement derivation](../unrestricted-single/DERIVATION.md)
  and [menu model](../menu-views/MODEL.md) supply the inherited operations.
- **Failure tests:** any missing core component, non-strict blocker, unsafe
  recovered phase, or incomplete finite remainder defeats the argument.
  Replacing I by its endpoint fails explicitly at r=170. A changed core,
  reference, threshold or simultaneous-added-runner question requires recovery
  and a fresh adequacy check.

[verify.py](verify.py) uses only Python's standard library and imports no
repository geometry, classifier or dispatcher. It checks pinned source bytes,
reconstructs the complete core by threshold events, compares every component,
checks all 20 strict blockers, and verifies I's constant lap bands, p, six
finite witnesses, the tail width inequality and the explicit recovery cases.
Its tail implementation is also checked on one admissible representative of
every residue modulo 170: r=12 through 181, with core duplicates 13,17,19
replaced by 183,187,189. This is a
bounded implementation check, not the reason the infinite tail follows: that
reason is the displacement argument above. The phase at a is periodic in r
modulo 170, while the displacement bound only improves as r increases.

Run from the repository root:

```sh
python experiments/runner-addition/primes-two-source/verify.py
```

The default prints a JSON verification record without changing files; add
`--output /tmp/primes-two-source-verification.json` to save a copy. The saved
[VERIFICATION.json](VERIFICATION.json) binds this argument, certificate and
checker by hash. No wider family search, new predictive evaluation, performance
comparison or independent human/formal proof review was performed. This stage
makes an existing result easier to inspect; it does not establish a general
two-source theorem or intrinsic incompressibility.

**Next proposed:** use this short argument as the review target, then consider
a rule that constructs a suitable interval and repair time directly from core
constraints. Any claim that such a rule generalizes needs a separately frozen
validation domain; this exposed example cannot provide that validation.
