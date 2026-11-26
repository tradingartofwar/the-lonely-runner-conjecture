# Independent check of the ordinary-lineup comparison

**REPRODUCED on the sealed finite panel.** A separate WSL verifier took the hosted audit lease and checked out the immutable research return at ac4f8839f521bebebe1ef41fbb7aa61adf469ba1. It regenerated the committed inputs. It reconstructed the first-arc and final-anchor choices from the fifteen physical subset speeds, checked rational distances to the nearest integer for every issued time, and checked that both denominator-4 endpoints were unsafe on each of the 51 switches. This path uses direct trajectory tests and rational interval bounds in place of the prediction routines. The complete score matched all four ordered band digests and reproduced the exact result SHA-256.

The adaptive arm recovered 134,583 of the 134,627 retained ordinary draws. Fixed 4 recovered 134,569. There were 14 adaptive-only safe returns, zero fixed-only safe returns and zero unsafe returns. The observed gain is **10.40 safe witnesses per 100,000 retained draws**. Only 103 draws reached the final-anchor comparison and all 14 gains were in the two larger bands. Both policies abstained on 44 draws. The smallest band contributed zero retained draws after removing opened cases. See [the measurement](MEASUREMENT.md) for the exposure counts and per-band uncertainty. The pooled rate describes the retained sample and its mixture.

## Timing repeat

The verifier checked both paired timing ledgers against the frozen schedule of blocks and repetitions, and reran the same harness as its own process on WSL, Python 3.12.3, on logical CPU 0. Values below are median wall-clock microseconds per draw. The paired difference is the median of within-round differences, so it can differ from the difference of the two arm medians.

| Run and timed work | Fixed 4 | Adaptive | Median paired difference | Range |
| --- | ---: | ---: | ---: | ---: |
| Measurement, complete predictor | 70.24 | 70.44 | +0.21 | −0.56 to +0.57 |
| Verifier, complete predictor | 68.77 | 68.74 | +0.19 | −0.04 to +0.19 |
| Measurement, eligible final stage | 3.59 | 5.85 | +2.25 | +2.11 to +2.37 |
| Verifier, eligible final stage | 3.62 | 5.95 | +2.35 | +2.16 to +2.55 |

The adaptive final stage took longer in all eighteen paired timing batches across both runs. The complete-predictor comparison changed sign across rounds in each run. The measured final-stage cost is concentrated on inputs that reach the final anchor. The end-to-end effect was unresolved at this timing resolution.

## Replay and adoption

From the repository root:

```sh
python3 observatory/escape_trial/ordinary_adoption/verify.py | sha256sum
python3 observatory/escape_trial/ordinary_adoption/measure.py time
```

The reproduced score hash is `21697895ec974f938451372ccfdcd9cb8d0536ca34b5bf121d49233669c9bfe2`. The recorded independent timing ledger has SHA-256 `233bd241991acbaddad8c49339565830e669fba2576e97a2e1521dee02e1476b`. A fresh timing run will have its own hash. The relevant choice is whether the observed extra witnesses on this generator are worth the measured final-stage cost. Adoption remains open. AI assisted the study implementation and interpretation. The two exact computational methods ran under distinct hosted leases.
