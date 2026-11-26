# A structural choice between final denominators 4 and 7

**Observed on 64 fresh eligible lineups.** The frozen selector recovered 36, compared with 28 for fixed 4 and 13 for fixed 7. The paired comparison with fixed 4 had eight gains, zero losses, 28 shared recoveries and 28 abstentions by both. The gain was 12.5 percentage points within this conditional sample. All eight cases recoverable only by 7 were captured. Every issued time passed the independent physical test at inclusive clearance 1/16.

| Smallest weight | Draws | Eligible | Chose 7 | Adaptive | Fixed 4 | Fixed 7 | Added vs 4 | Lost vs 4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1–4 | 131,072 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5–16 | 131,072 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 17–64 | 60,400 | 32 | 20 | 13 | 8 | 6 | 5 | 0 |
| 65–256 | 44,585 | 32 | 11 | 23 | 20 | 7 | 3 | 0 |

The two smallest bands exhausted their draw caps. Every comparison therefore concerns one of the two larger bands. This run sampled lineups already missed by the first-arc rule and both shared denominators. The earlier separate ordinary sample observed this situation on 14 of 28,102 primitive draws. The new conditional score measures neither incidence nor overall deployment improvement.

## A switch with a physical witness

For weights (53, 91, 560, 736), the least speed divisible by 4 is 144. Two odd subset speeds, 613 and 651, represent residues 1 and 3. Both lie strictly between 432 and 720, the bounds 3m and 5m. The two 4 endpoints then have physical minimum clearances 25/768 and 37/2304, each below 1/16. The chosen denominator 7 returned 207/1456 in the negative direction, with minimum clearance exactly 1/16 at speed 91.

The strict open intervals in the frozen rule make every switch an obstruction to both 4 endpoints. A multiple-of-4 speed in its prescribed window approaches the same integer on both signed shifts. Alternatively the two odd residues approach integers on opposite shifts. On a lineup without either certificate the selector executes the same 4 branch as the baseline. This argument preserves all safe 4 returns under the frozen arithmetic; it does not guarantee the selected 7 will help. The verifier recomputed all four signed endpoint times and all fifteen physical distances for every lineup. Across the 31 switches, all 62 rejected denominator-4 endpoints failed the target. Eight of those switches produced new recoveries.

## Computation and replay

The adaptive selector inspected 767 speed entries before selecting a denominator and built 31 extra residue tables. It attempted 109 signed membership tests across the 64 cases, compared with 111 for fixed 4 and 122 for fixed 7. Each final policy remained bounded by two signed attempts per case. No runtime comparison was measured.

The rule froze at 4f6d9040 and the independent seed commitment at e50948eb. The ordered panel was sealed at edea7a05 before scoring. The panel excludes prior panels and the prior ordinary sample. The ledger records every issued direction, sign-specific time, exact clearance, and limiting speeds. Replay from the repository root:

```sh
python3 observatory/escape_trial/adaptive_anchor/sample.py | sha256sum
python3 observatory/escape_trial/adaptive_anchor/verify.py | sha256sum
```

Expected SHA-256 hashes are f12acb9e634c9839b74ea8cdb60b66227856da844570275e88a2f7030133864d and 5f8fa41a582b8c8f391713e35e22160b450fbf95a6d7a5830a6948e3f6afb7ad, respectively. Separate Codex researcher and verifier contexts developed and checked this bounded experiment.
