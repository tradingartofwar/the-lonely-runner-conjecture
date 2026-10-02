# Independent verification: one-containment selector

**Status: PASS.** A separately structured `fractions.Fraction` event-cell reconstruction agrees with the primary result on 142 critical fields. It imports no primary implementation.

## Reconstructed outcomes

- Target: largest potential slack selects `[61, 100]` and fails its sole containment query; fewest positive occurrence components selects `[15, 38]` and certifies `49/524400`.
- Strict16: both rules select `[6, 11]` and certify `1/896`.
- Doubling112: the archived pair-only primal/dual certificate is rechecked exactly at `761/32256`. Selector outcomes are diagnostics only; their chosen pairs are `[56, 112]` and `[56, 64]`.
- Tight13: no pair has positive potential slack, so neither rule issues a query. Exact endpoint reconstruction confirms valid isolated equality at `t=3/8`, not positive duration.

## Scope and semantics

The verifier reconstructs all four windows directly from their speeds, checks the pinned source hashes, reproduces every single and pair duration used in `C_0`, enumerates all six base-pair slacks and positive occurrence components, reapplies both frozen physical-lexicographic tie rules, and tests one compound containment at most. Strict blockers use the open condition `distance < 1/8`; equality is safe. Window endpoints are evaluated explicitly. No failed selection triggers a second query.

This is internal exact computational agreement, not independent human mathematical validation.
