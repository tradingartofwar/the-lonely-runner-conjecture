# When all twelve initially clear runners leave their safe arcs

**OBSERVED on the first unattended assignment, November 26, 2026.** The new first-arc rule is sufficient on this family. Its abstention can also conceal a safe time. In one fresh case, every initially clear runner left its starting safe arc during a successful escape.

All sixteen runners start together. The stationary reference is zero and the fifteen moving speeds are the nonempty subset sums of the four weights. A distance of exactly 1/16 qualifies. The [rule](RULE.md), [earlier concealed holdout](VERIFICATION.md) and [challenger controls](CHALLENGE.md) informed the question. Code for both prospective stages and the separately written physical verifier was frozen at `783ec79f0ed2d9ff9234baffbb57386834bd16df` before the hosted coordinator drew the seed. The draw excluded 106 known lineups and removed duplicates across arms.

## Could several colliders escape?

| Fresh sample | Rows | Safe multi-collider selections | Multi-collider selections missed by both baselines | All safe returns of the frozen rule |
| --- | ---: | ---: | ---: | ---: |
| Unconditioned | 16 | 2 | 1 | 16 |
| Collision-enriched | 16 | 15 | 5 | 16 |

Both arms took four primitive lineups per smallest-weight band. The enriched arm required every reciprocal anchor from 1/2 through 1/16 to have a collider, and at least five colliders at 1/3. Conditioning used only arithmetic available before any shift was chosen. The denominators stay separate because the two arms sample different populations.

On the unconditioned lineup **(123, 205, 1055, 1385)**, speeds 1260, 1590 and 2440 coincide with the reference at 1/10. A forward move of 1/20160 lets the slowest collider reach the clearance threshold before speed 2768 reaches the edge of its safe arc. At **2017/20160**, the minimum is **1/16**, attained by 1260 alone. The direct reciprocal selector abstained. The earlier fifteen-speed predictor returned 2769/44288, where speed 1055 has clearance 1713/44288, below 1/16.

## Why the next worker studied re-entry

The verifier confirmed safe multiple-collider predictions and zero abstentions in both cohorts. That outcome selected the preregistered fresh screen for re-entry. The screen used a separate random stream and searched for lineups having no clear reciprocal. It accepted 115 new rows. The four bands contributed 19, 32, 32 and 32. The smallest band reached its fixed draw cap, leaving a shortfall of 13.

The first-arc rule returned 114 safe times and abstained once. On **(60, 63, 449, 644)**, speeds 60, 63 and 123 collide at 1/3. Move forward by 1/960. At **107/320**, all fifteen speeds are clear and **60** is the only one at **1/16**. Each of the twelve initially clear runners finishes outside its original unwrapped safe arc. Five of the thirty signed earliest-escape endpoints pass on this lineup. The result led to a new assignment asking whether a cheaper test can certify re-entry while still catching an unsafe speed in the interior of a residue class.

## Exact replay

Use Python 3.10+ from the research repository root. Each command prints the measured result and exercises the independent physical checker. Add `--json` for the complete row ledger, selection counts and all limiting speeds.

```sh
python observatory/escape_trial/continuation.py --stage cohorts --role verifier --seed 456475a077509b60f82776ad017e5b42
python observatory/escape_trial/continuation.py --stage wrap --role verifier --seed 456475a077509b60f82776ad017e5b42
```

Independent worker processes reproduced the submitted SHA-256 digests of the canonical JSON object containing summary and evidence. The first digest is `1550a91fb6735f45ecc2f2c9887679217b73a63711558bb9b0e70c4ad675e94f`. The second is `60973c119b6c6d54cd4abad5d1f90d8dff276d492afcc97ceb08fd8a93dc71a9`. The private board holds the scheduled-run receipt and the actual claim and completion times. These are bounded observations for one reference in the four-weight family.
