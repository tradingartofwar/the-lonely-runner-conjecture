# Independent verification: collective higher-order obligations

September 28, 2026 UTC. This verifier is separately structured from the primary calculation: it uses exact rational primal/dual replay plus direct Möbius inversion and face parameterization. It imports no primary functions and uses no optimizer. AI agreement is not independent human mathematical validation.

## Result

All **19 exact LP certificates** pass: three baseline minima, twelve cover-constrained individual-triple minima, three cover-constrained collective minima, and the main `H <= 0` repair. Every primal meets the frozen moments and side constraints; every dual is feasible; exact primal and dual values agree.

For the symmetric main moments, write `u=x_empty`, `q=x_1234`, and `y_i` for exact-three mass on the state missing event `i`. Möbius inversion gives the complete feasible-face parameterization

`u + sum_i y_i + 3q = 1/7`, with all six parameters nonnegative,

and reconstructs the lower states as `x_i=sum_(j!=i)y_j+2q` and `x_ij=u+y_i+y_j+2q`. Therefore on the cover face `u=0`, every individual inclusive triple can have minimum zero, while

`H = sum_K T_K - Q = sum_i y_i + 3q = 1/7`.

This is a real distinction between `sum(min T_K)=0` and `min(sum T_K-Q)=1/7`; the separate minima occur at different covers. In fact, any fixed **proper subset** of the four triple queries can vanish simultaneously: place all `1/7` exact-three mass on an omitted triple. Thus this abstract control genuinely requires a collective all-four statistic under the frozen query language.

The same retained moments also admit the explicit open model `x_empty=1/7` and `x_ij=1/7` for all six exact-pair states, with all other masses zero. Imposing `H<=0` forces this form and repairs the minimum empty mass to `1/7`.

The controls behave as intended. The zero-burden partition is uniquely the four singleton states of mass `1/4`, so all triple and collective minima are zero. In the quadruple control, nonnegative pair-only mass and exact-three mass force `q=1/4` and all exact-three masses to zero. Hence each inclusive triple is `1/4`, raw `sum T=1`, but `H=sum T-Q=3/4`; omitting the `Q` correction would overcount.

## Scope

These are exact finite facts about three prescribed abstract four-event moment models. They do not show that the distributions are realizable by common-start runners, provide a speed-derived upper bound on `H`, or establish a general Lonely Runner selector. The proper-subset limitation is specific to the frozen inclusive-triple query language.

Reproduce read-only with:

```bash
python -B reviews/2026-09-28-collective-obligations/verify.py --check
```
