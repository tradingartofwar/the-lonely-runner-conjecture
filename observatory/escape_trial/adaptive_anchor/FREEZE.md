# Choose the last denominator using a shared obstruction

**Finite-panel forecast.** After the first-arc predictor and both shared denominators 3 and 5 abstain, an advance choice between 4 and 7 will produce a positive net gain in safe returns against fixed 4 on the fresh panel below. The target is inclusive clearance 1/16 from the stationary reference among the 15 nonempty subset speeds of four primitive stretch-middle weights. All start together. The prior 67 paired rows were used for development only.

## Rule and reason

Build the usual residue table for 4 and let m be its smallest positive multiple-of-4 speed. It exists on eligible inputs. Switch to 7 if either condition holds.

1. A speed divisible by 4 lies strictly between 15m and 17m.
2. Both odd residue classes (1 and 3 modulo 4) have a speed strictly between 3m and 5m, or both have a speed strictly between 11m and 13m. The two speeds must be in the same interval.

Otherwise choose 4. Apply the existing bounded membership test at the chosen denominator only, positive direction first and negative second, returning at most one time. There is no fallback. Equality at a window edge does not trigger the certificate.

To see why switching preserves safe 4 returns, write its two candidate times as 1/4 ± 1/(16m). Condition 1 puts the speed's displacement v/(16m) strictly within 1/16 of 1, while its initial phase v/4 is an integer. The speed therefore blocks both directions. In condition 2 the two initial phases are 1/4 and 3/4. Their displacements are both within 1/16 of 1/4, or both within 1/16 of 3/4. In each case one speed blocks the positive direction and the other blocks the negative direction. These are sufficient obstructions. Absence of a certificate leaves 4's outcome open.

The selector never computes either signed time or tests endpoint membership before choosing. The added work is a pass over at most 15 grouped speeds (actual probes counted in choose.py) and one extra residue table whenever it switches. On nonswitches it reuses the existing 4 table. Report total preselection probes, extra tables, signed membership attempts under each policy, and switches. These counts do not establish a runtime advantage.

On the opened 67 rows, comparing candidate certificates suggested retaining both odd intervals and the multiple-of-4 condition. The combined rule switched 38 times, collecting seven gains with zero losses against fixed 4 (32 versus 25 recoveries). It inspected 761 speed entries. Replay those development rows with `python3 observatory/escape_trial/adaptive_anchor/choose.py`.

## Frozen unseen test

The verifier draws one independent 32-byte seed after publication and commits its SHA-256 before sampling. Use continuation.stream with domain adaptive-anchor-v1 and the same four fixed smallest-weight bands and stretch-middle generator as last_anchor/FREEZE.md. Use last_anchor/select_cases.archive(), exclude the entire prior last_anchor conditional panel, and regenerate and exclude all 8,192 prior ordinary draws per band via the previous revealed seed and domain. Accept only distinct fresh primitive inputs for which the previous first_arc_fails and shared_fail gates both hold. Screen each band in stream order for up to 131,072 raw draws or 32 accepted rows, whichever comes first. No replenishing or extension. Neither the new switch nor either final arm may influence selection. Commit the full panel and draw counts before scoring.

Recheck all qualifying inputs against the original first-arc predictor and both signs at 3 and 5. Compare the adaptive policy to fixed 4 on the same lineups. Independently compute all four signed final endpoint clearances physically with exact arithmetic. Audit each switch by checking that both 4 endpoints are strictly unsafe, and every issued time by checking that clearance reaches 1/16. A failed obstruction check or unsafe issuance refutes the corresponding safety claim. Zero or negative net paired gain refutes the positive-gain forecast on this panel. Record adaptive-only, fixed-4-only, shared and neither; total, per-band and unique-7 recoveries left on the table; include safety and cost diagnostics. Save weights, decisions and exact outcomes for replay. The separately measured incidence of reaching this decision in ordinary draws remains 14/28,102 for the previous generator sample; this conditional experiment yields no new ordinary incidence or overall effect estimate.

AI-assisted derivation and opened-case exploration preceded this freeze. No fresh draws were used during rule development.
