# Which final anchor helps after both shared anchors fail?

This owner-authorized comparison uses the four-weight stretch-middle generator, the four original smallest-weight bands (1–4, 5–16, 17–64, 65–256), the first-arc predictor and the bounded membership test at revision dfb24ff. Each lineup consists of a stationary reference and the fifteen nonempty subset sums, with common start and inclusive target 1/16.

## Eligibility and paired endpoint rule

A lineup reaches the final anchor exactly when the original first-arc predictor abstains and the existing four-lap membership test emits no time in either direction at q=3 or q=5. Failure means the frozen selector abstains, whether obstructed or beyond its lap budget. The first-arc test retains its full original anchor range. Final-arm outputs cannot affect admission. In each arm try positive then negative at its one denominator, retaining the first certificate. Use the same membership test for 4 and 7. A success requires an issued time and independently computed physical clearance of at least 1/16 across all fifteen speeds. An unsafe issuance invalidates the safety claim. Tabulate 4 only, 7 only, both and neither, with the accepted paired cases as denominator. Use 4-only minus 7-only as the signed net. A strict advantage for either denominator requires a net with the corresponding sign; zero is a tie on the panel. Do not infer a population ranking.

## Independent samples and stopping rule

The verifier draws one fresh random 32-byte seed after the rule freezes and records its SHA-256 before generation. Derive independent streams per band with the existing continuation.stream using domain labels last-anchor-ordinary-v1 and last-anchor-conditional-v1. Use draw_weights(..., "stretch_middle") for both.

* Ordinary incidence: take exactly 8,192 raw draws per band, with replacement, and retain every primitive draw, including repeats. Count how many retained draws reach the final anchor. Record counts by band and the pooled numerator/denominator. These are observations for the specified generator; prior no-clear screens have a different denominator. Do not compare 4 or 7 on this sample.
* Conditional experiment: exclude all archived and opened panels identified in anchor_swap/select_panel.py, the membership and anchor-swap panels, and **all** lineups drawn for ordinary incidence. Within band draw at most 131,072 raw lineups. Accept the first 32 distinct fresh primitive lineups reaching the final anchor, or all that qualify before the cap. No top-up. Never select on 4 or 7. Keep band shortfalls. Conditioning and quotas make this sample unsuitable for estimating ordinary incidence.
* Commit the ordered conditional inputs and ordinary counts before evaluating either final arm. Replay exclusions and both streams from the revealed seed. On every admitted case recheck eligibility with the original implementation, and independently compute exact modular clearance at both signed endpoints of each arm (including an unissued direction). Save all paired outcomes, times and minimum clearances. A discrepancy in eligibility, safety or reproducibility must be reported. Finite-panel counts are descriptive.

The prior 774- and 768-lineup experiments motivate the question and contribute no cases to the paired score.
