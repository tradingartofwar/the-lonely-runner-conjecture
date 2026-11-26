# WSL ordinary-lineup measurement

**WSL research return pending separate verification.** The masked authenticated hosted service granted the deterministic WSL lease at 12:24:51 p.m. Pacific on November 26, 2026. The comparison, seed commitment and ordered input digests were published before scoring at cc3bafb, 467b84b and fc617d5. All calculations concern the stationary reference and the existing four-weight stretch-middle family.

| Smallest weight | Ordinary draws retained | Reached final anchor | Fixed 4 safe | Adaptive safe | Gains | Losses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1–4 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5–16 | 22,328 | 0 | 22,328 | 22,328 | 0 | 0 |
| 17–64 | 55,730 | 42 | 55,707 | 55,714 | 7 | 0 |
| 65–256 | 56,569 | 61 | 56,534 | 56,541 | 7 | 0 |
| Total | 134,627 | 103 | 134,569 | 134,583 | 14 | 0 |

Both arms issued zero unsafe times. The adaptive rule recovered 59 of the 103 final-anchor cases, compared with 45 for fixed 4. Both abstained on 44 ordinary draws. The net was 10.40 additional verified safe witnesses per 100,000 retained draws. The 51 switches included 14 gains, including weights (35,49,224,316), where denominator 7 emitted 81/560 with exact minimum 1/16.

The sealed draw budget was 65,536 raw inputs per band. In total 37,104 draws were nonprimitive, 90,413 were excluded as previously opened, and 19,772 retained rows were repeats beyond the first occurrence. All primitive draws in the 1–4 band matched opened inputs. The pooled result concerns the retained panel and this band mixture. Estimated gain rates per 100,000 retained draws, with 95% Clopper–Pearson binomial intervals by nonempty band, are 0 (0 to 16.52), 12.56 (5.05 to 25.88), and 12.37 (4.98 to 25.49). The intervals treat the with-replacement draw stream per band as independent. They quantify the rate of an adaptive-only safe return. The observed fixed-only count is zero in each band.

## Paired WSL timing

Python 3.12.3 on WSL Linux x86-64, pinned to logical CPU 0. Values are median wall-clock microseconds per input across rounds or eligible repetitions, with warm-up, paired blocks and alternating arm order from the frozen code.

| Timed work | Fixed 4 | Adaptive | Median paired difference | Range of paired differences |
| --- | ---: | ---: | ---: | ---: |
| Complete predictor, all ordinary draws | 70.24 | 70.44 | +0.21 | −0.56 to +0.57 |
| Final stage only, eligible draws | 3.59 | 5.85 | +2.25 | +2.11 to +2.37 |

The final-stage overhead had the same sign in all nine timing pairs. The three end-to-end differences crossed zero. This run could not resolve a consistent end-to-end change. The raw ledger retains wall and process CPU measurements.

## Evidence and replay

The sealed manifest is panel.json. The full score stores a digest of the exact paired records for each band and all final-stage rows. From the repository root with Python 3.12:

```sh
python3 observatory/escape_trial/ordinary_adoption/measure.py score | sha256sum
python3 observatory/escape_trial/ordinary_adoption/measure.py time
```

Expected exact-score SHA-256 is 21697895ec974f938451372ccfdcd9cb8d0536ca34b5bf121d49233669c9bfe2. The recorded timing ledger hash is 50e201055c06a9ae71c1652b3c07ce6f0ccf6db623490c41cb6c50c0cb21a059. A fresh timing uses the same procedure under current runtime conditions. Adoption remains an owner decision.
