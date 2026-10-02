# Independent verification: selector transfer audit

**Status: PASS.** A separately structured exact rational threshold-event sweep agrees with the primary output on 848 critical fields. It imports neither the primary program nor its floor-sum and containment helpers.

## Scope

- Reconstructed records: 18 (2 development labels and 16 archival-transfer labels).
- Reflection pairs: 9; each pair has identical exact outcomes and is explicitly not counted as independent evidence.
- Physical sweep: 280 exact event points and 262 open cells.
- Dispatch: 8 pair-only exits and 10 active selector records.
- One-query work: 20 logical selections, 18 unique physical selected-pair checks. The 38 eligible-pair oracle checks are separately marked postselection-only.

Across the 10 active labelled records, largest slack certifies 4 and fewest components certifies 10. Across all 16 transfer labels (including pair-only exits), the corresponding direct selector certifications are 4 and 8; pair-only exits remain a separate prior certificate branch.

## Independent checks

The verifier recomputes all 16 physical moments per record, `C_0`, positive-slack eligibility, exact pair components, physical-speed lexicographic selections, selected containments, and the all-eligible postselection oracle. Strict blocking is `distance < 1/8`; equality is safe, and event points are tested separately from open cells. A selected failure never issues a fallback query.

`strict_16` reproduces the `(6, 11)` selection and containment; `doubling_112` exits at the prior pair-only value `761/32256` before any active query; `tight_13` has no eligible duration pair and retains isolated equality at `3/8` only.

This is internal exact computational agreement, not independent human mathematical validation.
