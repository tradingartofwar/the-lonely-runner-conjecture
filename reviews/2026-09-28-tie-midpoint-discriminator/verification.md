# Independent tie-midpoint verification

**Status:** PASS

This verifier independently reconstructs every blocker threshold event with exact rational arithmetic. It does not import `primary.py` or any primary helper.

## Scope

- Active labels: 7 (four reflection mechanisms)
- Tied pairs: 16
- Reconstructed positive components / midpoint samples: 16
- Complement phase reductions: 32
- Selected compound queries: 7
- Postselection oracle queries: 16
- Score-sign false positives / false negatives: 2 / 0
- Score-order inversions: 0

## Dispatch and semantics

- `doubling_112` exits on its inherited positive pair-only minimum before scoring.
- `tight_13` has no positive-slack eligible pair, issues no duration query, and retains only the valid isolated equality at `3/8`.
- Strict blocker semantics use distance `< 1/8`; equality is safe. Open cells and every exact event point were checked.
- Reflected labels agree on choices, scores, and containment outcomes; they are not counted as independent validation.

## Primary comparison

- Status: PASS
- Compared scalar fields: 491

## Limits

This is an independently structured internal exact check, not independent human mathematical validation. The finite midpoint score is a selector diagnostic, not a containment proof.
