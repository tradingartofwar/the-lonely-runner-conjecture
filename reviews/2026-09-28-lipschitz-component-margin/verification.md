# Independent Lipschitz component-margin verification

**Status:** PASS

This verifier does not import `primary.py`. It reconstructs base components from a complete exact threshold-event sweep, then checks each Lipschitz lower margin against a separate direct minimum-distance calculation on the closed component.

## Scope

- Active tie labels: 7 (4 reflection mechanisms)
- Tied pair labels: 16
- Reconstructed positive components: 16
- Lipschitz complement evaluations: 32
- Exact numeric lower-bound defects: 0
- Impossible nonnegative-score false positives: 0

## Outcome

- Nonnegative sufficient-certificate true positives: 14
- Negative-score containing pairs (inconclusive): 0
- Negative-score noncontaining pairs (inconclusive): 2
- Nonnegative-score false positives: 0
- The squares rule selects `{25,121}` with score `51/484`; failed `{25,169}` has score `-1/52` and is not certified.
- All Fibonacci selected pairs and the `strict_16` selected pair have nonnegative scores.
- `doubling_112` exits on `761/32256`; `tight_13` retains only isolated equality `3/8`.

## Separately charged audit

- Postselection containment threshold events: 248
- Postselection open cells: 232
- Archived containment disagreements: 0
- Containment schedules were not used to select or certify a pair.

## Primary comparison

- Status: PASS
- Compared scalar fields: 573
- Disagreements: 0

## Limits

This is an independently structured internal exact check, not independent human mathematical validation. Nonnegative score is sufficient, while negative score is only inconclusive. The squares case is fitted development data; the controls are archival; reflections are not independent examples; and every tested tied pair has one component.
