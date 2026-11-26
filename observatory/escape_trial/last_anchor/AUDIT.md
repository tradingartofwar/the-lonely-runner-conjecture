# What helps after denominators 3 and 5 both fail?

**Denominator 4 returned a safe time on 25 of 67 fresh eligible lineups. Denominator 7 returned one on 11.** There were 21 rescues unique to 4 and seven unique to 7, for a net of 14 additional cases (20.9 percentage points on this panel). Four lineups admitted a return from both rules. The remaining 35 received neither. All 36 issued times passed an exact modular check across the fifteen physical speeds.

| Smallest weight | Raw draws screened | Eligible fresh lineups selected | 4 only | 7 only | Both | Neither |
|---|---:|---:|---:|---:|---:|---:|
| 1–4 | 131,072 | 0 | 0 | 0 | 0 | 0 |
| 5–16 | 131,072 | 3 | 0 | 1 | 1 | 1 |
| 17–64 | 52,990 | 32 | 10 | 2 | 1 | 19 |
| 65–256 | 30,013 | 32 | 11 | 4 | 2 | 15 |

Each lineup had exhausted the first-arc rule and both directions at denominators 3 and 5. The two smaller bands hit the fixed draw cap. No additional search filled those bands. The two larger bands supplied 64 of the 67 lineups.

For weights (20,40,171,265), denominator 4 returned 81/320, with limiting speed 20 at exactly 1/16. The two denominator-7 clearances were 2/231 and 3/154. Conversely, on (14,16,139,183), denominator 7 returned 31/224, with limiting speed 14 at exactly 1/16; the denominator-4 clearances were 5/256 and 7/256. Both comparisons use inclusive clearance 1/16 from the stationary reference. All four signed times and their limiting speeds on every case appear in results.json.

## Ordinary incidence

A separate with-replacement sample took 8,192 raw draws per band before selecting the comparison panel. The generator was the same stretch-middle family. The denominator here includes every primitive draw, retaining repeats. Of 32,768 raw draws, 28,102 were primitive. Only 14 of those 28,102 reached the final-anchor decision (0.0498%, about 1 in 2,007).

| Smallest weight | Primitive draws | First-arc abstentions | Both shared denominators also failed |
|---|---:|---:|---:|
| 1–4 | 6,954 | 0 | 0 |
| 5–16 | 7,008 | 2 | 0 |
| 17–64 | 7,093 | 13 | 6 |
| 65–256 | 7,047 | 21 | 8 |

The conditional panel excluded every ordinary draw. Its stopping quotas and band composition differ from the ordinary sample, so the conditional net gain cannot be used directly as an ordinary-sample improvement rate. Both measurements concern this generator and predictor.

## Replay

The rule and sample budgets froze at a081a6c9. The seed commitment preceded selection at bcd144a6; the full ordered panel, seed reveal and ordinary counts preceded scoring at 0768aefc. The verifier separately checked the integer selection gate against the original first-arc implementation on archived controls, and rechecked every selected case against the original gate and shared anchors.

From the repository root, regenerate the selected inputs and the full score.

```sh
python3 observatory/escape_trial/last_anchor/select_cases.py | sha256sum
python3 observatory/escape_trial/last_anchor/score.py | sha256sum
```

Expected hashes, in order, are `325a7feec6300c1d49ccd9c5b2b87b06c2fa5c8e574fff41af2913f0ec002419` and `e6b07335f4492971efa909e385a0e283bec411802ebab6317565c2b0d3ed1619`. An independent Codex verifier carried out selection and exact scoring.
