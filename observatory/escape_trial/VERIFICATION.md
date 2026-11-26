# A signed shift recovered one fresh middle-gap lineup

**OBSERVED.** The frozen four-weight rule returned a safe time for each of twelve fresh sixteen-runner lineups. Eleven were the same direct reciprocals as before. On the twelfth, both the direct rule and the earlier fifteen-speed rule missed. The new rule moved forward from 1/15 and gave a valid time at the exact threshold. This meets the written forecast of at least one signed gain on this panel. The successful fresh shift had **one collider**. The selected shifts with three or five colliders came from previously opened cases.

Every case has a stationary reference at zero, a common start and fifteen distinct moving speeds given by all nonempty subset sums of four primitive superincreasing weights. The target distance is inclusive at 1/16. Sampling used the four middle-gap scale bands alone.

## The one new gain

Fresh-06 has weights **(12, 20, 121, 183)**. Every denominator from 2 through 16 divides at least one moving speed. At 1/15 only speed 195 collides. It takes 1/3120 of a time unit to move 1/16 of a lap. The first initially safe runner to reach its forward edge is speed 133 after 17/31920. That leaves room for the escape. The exact first closed safe interval along that direction is **[209/3120, 143/2128]**, of width **11/51870**. Speed 195 is the only limiter at its entrance and 133 is the only limiter at its exit.

| Method on fresh-06 | Time | Exact clearance | Limiting speeds |
| --- | --- | --- | --- |
| Direct reciprocal, four weights | Abstained | — | — |
| Earlier heuristic, fifteen speeds | 383/5376 | 67/1792, unsafe | 183 |
| Archived seven-branch rule, four weights | Abstained | — | — |
| Frozen first escape, four weights | 209/3120 | 1/16 | 195 |
| First valid reduced grid time, denominator ≤32 | 7/23 | 2/23 | 20, 141 |

Of the 30 earliest signed escapes at the fifteen blocked anchors on fresh-06, exactly one fits the first safe arcs. Seven other endpoints are physically safe after some runners pass outside those arcs. For instance, starting at 1/2 and advancing 1/192 gives 97/192, with clearance 1/16 at speed 12. At that anchor the fastest collider, 336, travels more than one full lap during the shift. This rejected direction shows how a valid endpoint can evade the certificate even on the successful fresh row.

## Paired results

| Cohort (12 each) | First escape, valid | Direct reciprocal, valid | Earlier heuristic, valid | Archived seven-branch, valid | Grid, valid | First-escape branches |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Original, opened | 12 | 10 | 11 | 1 | 12 | 10 direct, 2 shifted |
| Previous holdout, opened | 12 | 11 | 11 | 1 | 12 | 11 direct, 1 shifted |
| **Fresh, concealed until freeze** | **12** | **11** | **11** | **2** | **12** | **11 direct, 1 shifted** |

On the fresh cases the escape rule gained one and lost zero against each of the direct and earlier rules. Both gains were fresh-06. It gained ten and lost zero against the archived seven-branch rule, and tied the raw grid on coverage. The earlier heuristic issued one unsafe time. The direct rule abstained once and the archived seven-branch rule abstained ten times. The new rule had zero unsafe returns and zero abstentions on this panel. Each denominator-ordered grid search stopped at its first safe point. Across the twelve fresh cases it evaluated 319 exact clearances. The new predictor built 135 residue tables, tested 17 signed headrooms and performed zero full clearance evaluations to choose its twelve predictions. These operations measure different kinds of work.

| Opened case | Colliders at selected anchor | First certified time | Entry limiter | Exit limiter |
| --- | --- | ---: | ---: | ---: |
| Original-03, (3, 5, 28, 60) | 28, 63, 91 at 1/7 | 65/448 | 28 | 96 |
| Original-09, (41, 80, 435, 564) | 435, 564, 999 at 1/3 | 2321/6960 | 435 | 1079 |
| Previous-04, (14, 17, 103, 154) | 117, 120, 168, 171, 288 at 1/3 | 625/1872 | 117 | 257 |

**DISPROVEN.** The stronger claim that every primitive four-weight lineup in the middle-gap shape has an accepted reciprocal or first-arc shift has a counterexample. The separate [challenger](CHALLENGE.md) found (260,264,1567,2101), beyond the pilot's scale bands, where the frozen rule abstains at every anchor. At 1/3 + 1/4224 the physical minimum is 1/16 at speed 264. The trial verifier independently reproduced the abstention and all five safe signed endpoints that the first-arc check declines. This adversarial case contributes zero rows to the pilot score. How often a signed prediction involving multiple colliders adds coverage on unopened inputs remains open.

## Seal, audit and replay

The verifier sampled once using the versioned generator with a private random 256-bit seed. The 94 disallowed lineups comprise the earlier study's 80 exclusions, its 12 revealed lineups and two additional published controls. Each scale contributed its first three eligible, distinct draws. No clock time entered selection. The panel and seed commitments precede the [rule and its forecast](RULE.md) in Git history at seal `7fc97bf` and freeze `3c37443`. Separate AI workers operated in a shared workspace. The private reveal stayed outside the checkout until the freeze. This separation was procedural.

The [complete prediction vector](predictions.json) was recorded and its SHA-256 (`83c4b9c76edc23bf494e4e7a3ad8c5157e1510308c7fa07069a38c5b8e6304ce`) reported before any of the fresh outputs were scored. All thirty-six rows and every baseline return, abstention and limiter appear in [the results](results.json).

**REPRODUCED.** The verifier expands the four weights into fifteen actual speeds. At each signed candidate it checks whether the unwrapped terminal position of each runner lies in its first eligible closed interval of the form [m+1/16, m+15/16]. This independently recovers the first passing anchor and direction or an abstention. It also checks the residue counts and extreme speeds for all 540 row–denominator pairs, measures distance from the nearest whole lap, repeats the distance calculation using modular integers, and tests all 966 signed candidates at blocked anchors. Of these, all 245 first-arc certificates gave safe endpoints; 73 more endpoints were safe after leaving a required arc. The 24 opened rows agree with the previous study's earlier, direct, seven-branch and grid records. These are finite arithmetic checks for the selected reference.

Run from the repository root with Python 3.10 or later and its standard library.

```sh
python observatory/escape_trial/check.py
python observatory/escape_trial/check.py --case fresh-06
python observatory/escape_trial/seal.py verify observatory/escape_trial/reveal
python observatory/escape_trial/challenge.py
```

The first command checks the sampler and freeze digests, reproduces the pre-score vector, rescans the physical trajectories and compares the regenerated results to the archived bytes. The last command replays the independent adversarial search. AI assistance contributed to generation, derivation and checking. The finite score carries no general Lonely Runner or novelty claim.
