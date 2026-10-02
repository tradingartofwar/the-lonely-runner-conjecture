# Adversarial review: collective cover obligations

September 28, 2026 UTC. AI adversarial review of the frozen protocol. This is not independent human mathematical validation. Scope is the three prescribed abstract four-event controls; no physical speed realization, literature, or novelty claim was checked.

## Verdict

The proposed main example correctly exposes a **quantifier-order failure** that coordinatewise triple minima discard. It does not yet provide a nontrivial selector for runner geometry. In the retained representation, the collective quantity is exactly the inclusion-exclusion deficit, so its value on the full-cover face is fixed before optimization. An upper bound on that quantity strong enough to exclude full coverage is mathematically equivalent to a positive lower bound on the opening. The remaining substantive problem is therefore the **cost and derivation** of such an upper bound from runner geometry, not its selection by this abstract LP.

This is not fatal if the round is reported as a representation countermodel and a cost warning. It is fatal to any stronger claim that the symmetric LP has discovered a new geometric repair, selected one triple, or made proving an opening easier.

## 1. The identity is exact, and the collective optimum is tautological

Let `U=x_empty`, let the four inclusive triple durations be `T_K`, and let `Q=x_1234`. Ordinary inclusion-exclusion gives

```text
U = L - sum D_i + sum O_ij - sum T_K + Q.
```

Thus, with `C=L-sum D_i+sum O_ij` and `H=sum T_K-Q`,

```text
U + H = C.
```

Equivalently, if `y_K=x_K` denotes the mass of the exact triple-only state and `q=x_1234`, then

```text
H = sum y_K + 3q.
```

The coefficient `3` is essential: a four-way state belongs to all four inclusive triples and is then corrected once.

For the main moments,

```text
C = 1 - 4(3/7) + 6(1/7) = 1/7.
```

Therefore every feasible full cover (`U=0`) has `H=1/7`, without solving an LP. The proposed minimum of `H` on the full-cover face is an exact consequence of the identity, and its dual certificate can be no stronger than this equality. Likewise, imposing `H<=h<1/7` immediately gives `U>=1/7-h`.

The latter implication is valid, but its cost must not be hidden: obtaining a useful upper bound on `H` is already obtaining the missing inclusion-exclusion information. In particular, an exact evaluation of `H` is equivalent to an exact evaluation of `U` once the retained moments are known.

## 2. Stronger countermodel: every proper subset of triples can vanish together

The main moments admit the advertised open arrangement:

```text
x_empty = 1/7,
x_{i,j} = 1/7 for each of the six pairs,
all other masses = 0.
```

It has total mass `1`, every single duration `3/7`, every pair duration `1/7`, `H=0`, and `U=1/7`.

They also admit four especially transparent full-cover arrangements. For any triple `K` and its omitted label `d`, put

```text
x_K = 1/7,
x_{d,i} = 1/7 for each i in K,
x_i = 1/7 for each i in K,
all other masses = 0.
```

The seven displayed states have total mass `1`. Each label in `K` occurs in its triple, one pair with `d`, and its singleton, so its single duration is `3/7`; label `d` occurs in three pairs, also giving `3/7`. A pair inside `K` occurs in the triple and a pair containing `d` occurs in its exact pair state, so every pair duration is `1/7`.

This cover has `T_K=1/7`, every other inclusive triple zero, `Q=0`, and `H=1/7`. Consequences:

- each individual triple minimum on the cover face is zero;
- more strongly, for any proper subset of the four triple types, there is a compatible full cover on which all triples in that subset vanish simultaneously;
- no summary-only rule inspecting fewer than all four triple types can force positive higher-order mass in this symmetric example;
- the failure is `for every K, there exists a cover with T_K=0` versus the false interchange `there exists a cover for which every T_K=0`.

This is the genuine distinction preserved by the experiment. It is stronger and clearer than merely listing four separate coordinate minima.

## 3. What the diagnostic `H=0` does and does not establish

Because `H=sum y_K+3q` with nonnegative exact-state masses, `H=0` excludes every state containing at least three blockers. In the main example it is a **global four-triple support statement**, not a selected single-triple query.

The compatible open arrangement proves that the retained moments do not themselves rule out `H=0`. It does **not** supply a geometric upper bound for an unspecified physical runner configuration. An abstract feasible arrangement is not another common-start runner realization, and one feasible distribution cannot be used as an upper bound on another distribution's `H`.

Accordingly, the proposed repair LP under the diagnostic condition `H<=0` is an internally consistent countermodel calculation, but not a physical certificate unless an independent speed-based argument establishes that bound for the target schedule. The next useful selector would have to identify a cheaply derivable joint geometric restriction, or a proper upper bound on `H`, without reconstructing the desired opening itself.

## 4. Raw triple sum and the two controls

The zero-burden partition behaves correctly. Four singleton states of mass `1/4` give `U=0`, all pair and higher intersections zero, and

```text
C = 1 - 4(1/4) = 0 = H.
```

The quadruple-correction control also checks the accounting exactly. With `x_1234=1/4` and four singleton masses `3/16`,

```text
D_i = 7/16,
O_ij = 1/4,
T_K = 1/4,
Q = 1/4,
sum T_K = 1,
H = 1 - 1/4 = 3/4,
C = 1 - 4(7/16) + 6(1/4) = 3/4.
```

Thus the raw inclusive-triple sum overcounts the four-way state. Substituting `sum T` for `H` would yield the wrong deficit by exactly `Q=1/4` in this control.

## 5. Claim and scope limits

- The examples are abstract event-measure models. They neither assert nor refute realization by common-start integer-speed runners.
- The main example is deliberately symmetric and algebraically constructed; it demonstrates information loss, not frequency or inevitability in runner schedules.
- Positive `min H` on a fixed full-cover face is automatic whenever `C>0`; it does not by itself distinguish a promising physical control.
- No individual triple is preferred here. Symmetry plus the explicit four covers proves that preference would require information outside the retained summary.
- A useful collective upper bound may still be substantially cheaper than reconstructing all sixteen state masses, but this experiment does not establish such a cost advantage.
- AI calculation and agreement do not provide independent mathematical validation.

## 6. Required framing of the next step

The actionable question is narrower than “does a collective obligation exist?” It always exists on a full-cover face here because `H=C`. The question is:

> Can a speed relation produce a reviewably cheap upper bound on `H=sum y_K+3q`, or another joint constraint separating the full-cover face, without already computing the clear duration or all higher intersections?

A future protocol should charge the derivation cost of that bound and compare it with direct opening reconstruction. A negative result would still be consequential: it would show that moving from coordinatewise minima to the correct joint representation fixes the quantifiers but not the discovery problem.

## 7. Implementation and note audit

The completed artifacts were audited after the mathematical challenge above was written.

Read-only reproduction succeeded:

```bash
python -B reviews/2026-09-28-collective-obligations/primary.py --check
python -B reviews/2026-09-28-collective-obligations/verify.py --check
```

The primary replay checks **19 exact rational primal/dual certificates**: three pair-baseline minima, twelve cover-constrained triple minima, three cover-constrained `H` minima, and the main `H<=0` repair. For every certificate, the archived nonnegative primal satisfies the exact rational moments and side constraints, the dual satisfies all sixteen column inequalities, and the primal and dual objectives agree. The reported values are:

```text
main pair minimum U             0
main four individual minima     0, 0, 0, 0
main cover minimum H            1/7
main repair under H<=0          U=1/7
zero-burden cover minimum H     0
quadruple raw sumT, Q, H        1, 1/4, 3/4
```

The separate verifier does not import primary functions or invoke an optimizer. It replays the certificate inequalities, reconstructs the full symmetric feasible polytope by Möbius inversion,

```text
x_i  = sum_(j!=i) y_j + 2q,
x_ij = u + y_i + y_j + 2q,
u + sum_i y_i + 3q = 1/7,
```

and checks the open model, the four concentrated covers, uniqueness of the zero-burden cover, and uniqueness of the prescribed quadruple cover. These formulas independently confirm that the reduced nonnegative parameterization used in the note is complete, not merely necessary.

The research note [COLLECTIVE_COVER_OBLIGATIONS_2026_09_28.md](../../notes/COLLECTIVE_COVER_OBLIGATIONS_2026_09_28.md) now states the central limitations accurately: abstract rather than runner-realizable models, no new existence coverage, `H=C-U`, no established cost advantage, the proper-subset quantifier obstruction, and the need for a speed-derived upper bound. It also identifies the cycle-rank interpretation as a connection to prior repository work rather than a new inequality. I found no fatal arithmetic, quantifier, or scope error in the completed artifacts.

The principal remaining limit is conceptual, not computational: exact certificates verify the frozen abstract statement, but the collective optimizer is fixed by inclusion-exclusion and supplies no physical selection rule. The proposed next archive-only runner check can test whether this obstruction occurs in existing realizable windows; even a positive example would still leave cheap derivation of a collective upper bound unresolved.
