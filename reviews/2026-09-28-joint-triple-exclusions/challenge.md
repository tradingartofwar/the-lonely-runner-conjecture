# Adversarial review: simultaneous triple upper bounds

September 28, 2026 UTC. Baseline `01c3ea2658a51e138f89837bf16ab44f16c81007`. Scope fixed by this directory's protocol: one target window, its reflection check, and the three named historical controls. AI-assisted internal review, not independent human mathematical certification. This reviewer edits only this report.

## Direction and quantifiers

For a subset S of the four inclusive triples, retain the total/single/pair equalities and impose T_K<=b_K for K in S. These are upper bounds, not equalities and not lower bounds. Inclusive T_K counts both its exact-three atom and the four-way atom. Let f(S) be the minimum uncovered mass U over this model.

The physical atom table satisfies every true bound and is feasible for every subset. Hence 0<=f(S)<=U_physical. Adding bounds can only increase the minimum: S subset R implies f(S)<=f(R). Any result violating this monotonicity, exceeding physical U, or losing feasibility is a defect. Exact equality of a nonnegative feasible primal objective and a valid dual objective establishes an optimum. A zero optimum must have an explicit complete-cover primal satisfying all simultaneous bounds, rather than separate countermodels for its members.

The previous zero individual minima show each singleton upper-bound subset fails, but they do not imply the union of two or more such restrictions fails. Separate single-triple countermodels may be incompatible with each other. This is precisely the joint-versus-separate quantifier issue being tested.

For a successful S, inclusion minimality means every proper subset fails. It is enough to check its immediate one-element deletions if monotonicity has been verified, but all sixteen subsets are prescribed here anyway. Cardinality minimality instead means no successful subset anywhere in the lattice has fewer members. An inclusion-minimal success need not have globally minimum cardinality. The frozen lexicographic rule chooses among cardinality-minimal successes; report the entire inclusion-minimal family before this tie break.

## Full-set and scalar checks known before calculation

On the target, inclusion-exclusion gives U=C-sum T+Q. The four physical upper bounds sum to 99/185440 and C=6121/2781600, so C-sum b=1/600. Since Q>=0, retaining all four upper bounds forces U>=1/600. The physical atom table attains U=1/600. Thus the full-set optimum must be exactly 1/600; this is a direct acceptance check, not a surprise inferred from solver output.

The scalar comparison uses H=sum T-Q, with U+H=C. A supplied H<=99/185440 likewise implies U>=1/600 and the physical table attains equality. H is one scalar **at optimization time**, but its current exact physical value was obtained from all four triple durations and Q. No new low-cost geometric method for H is present. It would be misleading to call this a one-query practical improvement without charging that derivation. The target's Q=0 also means all four triple upper bounds alone achieve the same conclusion without adding a separate Q=0 constraint to the LP.

Minimality is only within the four given coordinate upper bounds at their frozen exact values, with the supplied pair moments. It is not a minimum number of geometric facts, bits, arithmetic operations, runner constraints, or all possible useful statistics. Different bound values, a joint phase exclusion, a lower bound, or another window form different contracts.

## Controls, reflection, and endpoints

Strict16 is a reproduction control for the already-known single exclusion T_(6,11,16)=0 and duration 1/896. Its other triple exclusions are not new repairs. Doubling112 already has pair-only optimum 761/32256>0, so its empty subset succeeds and no higher-order subset lattice should be evaluated. Its actual positive higher intersections cannot be silently zeroed. Tight13 has physical U=0; every valid subset minimum is therefore zero. Its isolated safe point 3/8 is a separate pointwise certificate, not a duration repair.

The target and reflected window are related by t -> 1-t at common start. Matching atoms, moments, and decisions is a symmetry check, not a second independent physical discovery. All conclusions concern reference 0 and the fixed windows. A feasible cover countermodel is an abstract measurable-event mass table, not a second constant-speed runner realization. “Complete cover” means full measure and may coexist with safe isolated points.

## Prior-work boundaries

The collective-window audit already supplies this target, all individual-triple failures, physical moments, and actual opening. The abstract symmetric example already shows how individually avoidable triples can carry collective burden. In that symmetric example every proper zero-triple subset is compatible with a cover; it must not be substituted for the actual target's potentially asymmetric subset lattice.

The sparse selector already uses two arithmetic triple tests in its fixed family, and the two-speed transfer already supplies an alternate-window dispatch. They demonstrate prior successful joint geometric information and must not be described as discoveries of this run. Here the bounded increment is an exact coordinate-subset minimality analysis on the preserved target, with simultaneous cover countermodels and charged scalar comparison. It adds no new existence coverage or novelty claim.

## Completed numerical and code review

Reviewed the protocol, current collective-window note, prior sparse/two-speed notes, `primary.py`, its exact LP helper, `results.json`, `verify.py`, and `verification.json`. Both read-only commands pass:

```bash
python -S -B reviews/2026-09-28-joint-triple-exclusions/primary.py --check
python -S -B reviews/2026-09-28-joint-triple-exclusions/verify.py --check
```

The primary proposes floating-point LP solutions only during generation and accepts them only after exact rational primal/dual verification. The separately authored verifier imports neither primary functions nor its LP helper. It reconstructs geometry by rational threshold events and solves the fifty-two prescribed LPs with its own exact two-phase simplex, adding nonnegative slack variables for the upper bounds. The signs are correct: minimization dual multipliers for <= constraints are nonpositive. Both implementations return the same objective for every subset and scalar comparison.

Verification covers 108 physical threshold cells across the target, its reflection, and the three controls; all retained moments, exact-state masses, triple bounds, and collective quantities match. The reflection has the same moments and atoms and the correctly reversed cell geometry. The tight endpoint passes all seven distance tests and has the opposing controllers 11 versus 5/13, preserving its isolated status.

All thirty-three zero-optimum coordinate cases retain simultaneous nonnegative complete-cover countermodels. The independent verifier checks each against its moment equalities and every bound belonging to that particular subset. Their counts are nine for the target, eight for strict16, sixteen for tight13, and zero for the already-positive doubling112 empty subset. These are abstract feasible covers, not runner realizations.

An additional read-only reviewer check compares every proper-subset inclusion in the three full lattices: all 195 monotonicity comparisons pass. Both scripts explicitly verify the frozen physical-triple lexicographic order; they do not substitute numeric subset-mask order.

## Accepted minimality result

Write A={15,38,61}, B={15,38,100}, C={15,61,100}, and D={38,61,100}. The target has exactly two inclusion-minimal successful subsets, both of minimum cardinality two:

| Simultaneous upper bounds | Optimal positive lower bound for U |
| --- | ---: |
| T_A<=0 and T_B<=0 | 49/524400 |
| T_C<=1/48800 and T_D<=119/231800 | 13/22800 |

Every singleton fails, as expected from the prior collective-only study. The other four two-element subsets also fail and have retained cover countermodels. Every three-element subset succeeds because it contains one of the two successful pairs; no three-element subset is inclusion-minimal. Adding one further bound to either minimal pair does not improve its optimum in this target. The full four-bound set reaches 1/600.

The frozen cardinality/lexicographic tie break selects {A,B}, even though {C,D} gives the larger numerical bound. Thus it is a selected smallest coordinate certificate, not the strongest smallest certificate. No reranking occurred. Within this exact coordinate-upper-bound contract, two bounds suffice for positivity, while all four are necessary to recover the actual duration 1/600. Neither conclusion is an unrestricted information-minimality theorem.

The controls behave correctly: strict16's only inclusion-minimal repair is its known T_(6,11,16)<=0; doubling112 selects the empty set without a lattice search; tight13 has no successful duration subset and retains its isolated equality point. The three scalar H optima are respectively 1/600, 1/896, and zero. The record charges their supplied-scalar count separately from the four triple values and Q used in the present physical derivation.

## The successful duals are prior graph corrections

The exact dual certificates have an already-known form. Let C0=L-sum D+sum O, avoiding confusion with the triple label C above. The selected pair gives

    U >= C0 - O_(61,100) - T_(15,38,61) - T_(15,38,100).

The other pair gives

    U >= C0 - O_(15,38) - T_(15,61,100) - T_(38,61,100).

Each is the five-edge K4-minus-one-edge bound, subtracting the two triangles left in that graph. `notes/FOUR_BLOCKER_CYCLE_CORRECTIONS.md`, section 5, already supplies this form and its exact gap: the omitted-pair-only mass. Their concrete optimality under the present supplied constraints is certified here, but the inequalities themselves are not new. This connects the new subset-lattice result to the project's existing cycle accounting without treating prior repairs as discoveries.

No fatal mathematical or computational issue was found in the frozen scope. The accepted contribution is a complete, exact, finite joint-coordinate audit with countermodels and independently structured verification. It does not produce a cheap speed-to-certificate selector, a new geometric derivation of H, additional family existence coverage, a novelty claim, or independent human proof certification.
