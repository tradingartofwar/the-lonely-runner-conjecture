# Independent verification: lap-band component count

## Outcome

PASS. A separately structured exact threshold-event sweep reconstructs all 24 pair intersections on the four frozen windows. Every reconstructed interval and component count matches the pinned physical geometry, and the frozen minimum-count selector matches the archived selector in all four cases.

Primary critical-field comparison: PASS.

## Method

For each pair, the verifier generates only the exact threshold contacts `(m +/- 1/8)/v` inside the supplied window. It tests each resulting open cell and each event point directly using `||vt|| < 1/8`. Components are joined across an event only when that event itself remains strictly blocking for both runners. Thus threshold equality is safe and can split two positive components; window endpoints are included only when strict blocking holds there.

This is intentionally different from the primary calculation: it does not use the per-lap integer-band row formula or import `primary.py`.

## Exact checks

- 4 frozen windows and 24 physical pairs.
- 311 pair-specific threshold events and 287 open cells.
- All 24 exact interval lists match the pinned geometry archive.
- All 4 frozen selector outcomes match.
- `strict_16`: the eligible count tie resolves lexicographically to `(6,11)`.
- `tight_13`: no positive-slack pair, no positive lonely interval, and the isolated valid equality point is exactly `3/8`.
- `doubling_112`: the archived pair-only lower bound is `761/32256>0`; the component selector is diagnostic only and does not replace that exit.
- No new complement-containment query was made.

## Limits

This verifies the finite calculation, endpoint semantics, and control roles. It is internal AI verification rather than independent human validation, and it does not by itself prove the general lap-band lemma or any whole-configuration Lonely Runner claim.
