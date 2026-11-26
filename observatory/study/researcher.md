# Which middle-gap returns can four weights explain?

**REPRODUCED on the opened panel.** In nine of the ten earlier-only successes, every opponent clears the reference at the reciprocal of a small integer. Four weights suffice to recognize exactly those returns. The tenth needs a displacement from a collision. The other two middle-gap lineups comprise one shared success and one unsafe earlier prediction. The original four-weight rule abstained on the latter.

The source is the opened 60-row subset-sum panel at repository revision `3316b381ca3386476c2bfda45a6584d6049838b3`. The coordinator reproduced the archived ledger before this assignment began. This solver used only the opened panel and its archived predictors. The derivation and code are AI-assisted.

## Assumptions and candidate

All 16 runners start together. Relative to the stationary reference, the 15 moving speeds are all nonempty subset sums of the four positive integer weights. The trial uses the protocol's primitive superincreasing weights and a total divisible by 16. Equality at distance 1/16 passes.

Revision `four-weight-direct-residues-v1` tests integer denominators 2 through 16 in increasing order. For each denominator q, start with the empty set R. Read a weight w and replace R by the union of its previous contents, the singleton {w mod q}, and {(r+w) mod q for each old r in R}. Every nonempty subset of a processed prefix either omits the new weight, consists of it alone, or adjoins it to a nonempty previous subset. By induction R contains exactly the reachable residues. Initializing with an empty set keeps the empty subset from manufacturing a collision. The implementation stores membership in at most 16 bits and uses one circular shift per weight.

As soon as zero is absent, return 1/q. Every speed then has distance at least 1/q from an integer, which is at least 1/16. If all denominators contain zero, abstain. The initial ordering resolves ties and all decisions use the four input weights alone. The direct rule makes no displaced prediction.

**Prediction for an unseen row.** The candidate returns the same time as the earlier rule whenever a clear denominator exists, and abstains exactly when all 15 anchors have a collision. This predicts zero candidate-only successes relative to the earlier rule. A mismatched denominator set, an unsafe return, a different time on a clear row, or any such candidate-only success would falsify the implementation or the explanation. No fresh success rate is assumed. The separate verifier commits its panel before the coordinator records the rule hash, then records a complete vector with one return or abstention per row before inspecting any true clearance.

## What the two descriptions retain

The archived four-weight predictor tries seven sufficient constructions, including parity, special congruences and a chart in which generator phases fit together within one lap. It does not test general subset-sum divisibility at denominators 2 through 16. For (2, 3, 17, 42) the four individual residues at denominator 12 are 2, 3, 5 and 6. They sum to 16, beyond the chart's one-lap allowance. Subsets wrap, yet none lands on zero. The least circular residue is one for speeds 47, 59 and 61, giving clearance 1/12 at time 1/12. The weights encode all the speeds. The operation that recovers this opportunity is addition of subset residues modulo each proposed denominator.

For (41, 80, 435, 564) every small denominator has a collider. The earlier rule selects denominator 9 with sole collider 999, then moves backward by 1/(16 × 999). At 1/9 the other speeds allow at least 7/98640 of backward movement before any reaches its nearest safe-arc boundary, compared with 7/155376 forward. The backward step fits. The return 1775/15984 has clearance exactly 1/16 at speed 999. The presence of residue zero explains the direct abstention. The actual collider speed and the noncolliders' directional margins explain the shifted success. Occupied residue bits alone at that anchor record neither speed magnitudes nor the displacement margin.

For (3, 5, 28, 60) every anchor also has a collider. At denominator 16 the closest noncolliders leave zero directional margin on both sides. The earlier rule breaks that tie forward. At its return 97/1536, speed 63 has distance 11/512, below 1/16. The direct rule abstains. The comparison grid supplies time 2/23 with clearance 2/23, attained by speeds 68, 91 and 93. This distinguishes a failed prediction from a lineup without a witness.

## Opened middle-gap results

| Four weights | Clear denominators | Earlier return | Earlier clearance | Archived four-weight outcome |
|---|---|---|---|---|
| 2, 3, 17, 42 | 12, 13 | 1/12 | 1/12 | abstain |
| 3, 6, 31, 72 | 11 | 1/11 | 1/11 | abstain |
| 3, 5, 28, 60 | none | 97/1536 | 11/512 | abstain |
| 14, 28, 105, 157 | 11, 13 | 1/11 | 1/11 | 33/224 passes at 1/16 |
| 16, 25, 144, 215 | 14 | 1/14 | 1/14 | abstain |
| 9, 10, 58, 83 | 12, 13, 14 | 1/12 | 1/12 | abstain |
| 43, 74, 322, 441 | 15 | 1/15 | 1/15 | abstain |
| 28, 29, 177, 262 | 15 | 1/15 | 1/15 | abstain |
| 41, 80, 435, 564 | none | 1775/15984 | 1/16 | abstain |
| 218, 411, 2222, 2861 | 15 | 1/15 | 1/15 | abstain |
| 220, 233, 1491, 2136 | 14 | 1/14 | 1/14 | abstain |
| 177, 197, 1618, 2024 | 7, 9, 10, 13, 14 | 1/7 | 1/7 | abstain |

## Work and replay

| Method | Inputs to predictor | Choices made before exact scoring |
|---|---|---|
| Direct residue candidate | Four weights | Screens 1 to 15 reciprocal anchors using four mask updates each. Returns the smallest clear denominator's reciprocal or abstains. Zero full clearance evaluations. |
| Earlier one-time rule | Fifteen physical speeds | Ranks all 15 anchors by collider count, then fastest minimum collider, then smallest denominator. This ranking alone makes 225 speed remainder checks per row. Returns one direct or displaced time. Zero full clearance evaluations. |
| Archived four-weight rule | Four weights | Tries up to seven ordered constructions, returns one time or abstains. Zero full clearance evaluations. |
| Denominator-32 comparison grid | Fifteen physical speeds | Fixes 162 reduced positive rational times up to reflection, ordered by denominator then numerator. Evaluates physical clearance until the first success or exhaustion. |

On these 12 opened middle-gap rows the direct rule screened 146 denominators and performed 584 weight/bit-mask updates. The earlier rule's ranking made 2,700 speed remainder checks before computing its selected return. These counts describe different operations and do not establish a wall-clock speedup. Four weights are a shorter list of inputs and determine the same underlying lineup.

From the repository root run:

```sh
python -m observatory.study.candidate --check-opened
python -m observatory.study.candidate 2 3 17 42
```

The replay compares all 900 reachable residue sets in the opened 60 × 15 denominator pairs with the residues of the physical speeds. All matched. It recomputes the earlier returns, checks proposed direct times exactly, and prints the 12 middle-gap rows. The direct rule returned 45 safe times in the full 60 and ten safe times in the middle-gap 12. These opened counts are explanatory observations. A successful direct return can never be a gain over the earlier direct branch under this tie break. The shifted case motivates a separately frozen test of a certificate that retains speed and direction within each residue class.
