# What the fresh comparison established

**OBSERVED.** The four-weight reciprocal rule and the earlier fifteen-speed rule returned the same eleven valid times on twelve fresh middle-gap lineups. On the remaining lineup the reciprocal rule abstained and the earlier rule issued an unsafe time. The archived four-weight rule found one valid time. The comparison grid witnessed all twelve.

The scope is stationary runner zero among sixteen runners starting together. Its fifteen moving opponents are the nonempty subset sums of the four positive weights in the archived family. Clearance equal to 1/16 passes. Each of the two panels has three lineups in each scale band.

| Method | Opened valid / abstain / unsafe | Fresh valid / abstain / unsafe |
| --- | --- | --- |
| Earlier one-time rule | 11 / 0 / 1 | 11 / 0 / 1 |
| Archived four-weight rule | 1 / 11 / 0 | 1 / 11 / 0 |
| Frozen four-weight reciprocal rule | 10 / 2 / 0 | 11 / 1 / 0 |
| Reduced rational grid through denominator 32 | 12 / 0 / 0 | 12 / 0 / 0 |

Of the ten earlier-only successes relative to the archived four-weight rule on the opened panel, nine had a clear reciprocal. The tenth, historical-09, required a displacement from the earlier rule's anchor. On fresh inputs the reciprocal rule found ten witnesses where the archived four-weight rule abstained. Its successes all overlapped the earlier method. This is a change in how the same successful choice can be calculated. The JSON contains counts and row IDs for all six pairwise comparisons on both panels.

## Fresh failure and exact follow-up

For fresh-04, the weights are (14,17,103,154). Every denominator from 2 through 16 divides at least one opponent. Both four-weight rules abstained. The earlier rule chose 289/4608. Speed 271 gives clearance 17/4608, below 1/16. The frozen grid reached 8/23 with clearance 2/23 at speed 17.

After scoring, the coordinator suggested a shift from 1/3. Speeds 117, 120, 168, 171 and 288 all collide there. Moving forward by 1/1872 gives 625/1872, with minimum clearance exactly 1/16 at speed 117. On the opened historical-03 the challenger similarly found 97/960, with minimum 1/16 at speed 60. Their status is post-hoc **OBSERVED**. Neither time enters the frozen scores. These examples motivate a fresh comparison of a preselected anchor-and-shift certificate that accounts for the colliders' speeds and the other runners' directional margins.

## Provenance and replay

The mathematical baseline is 741b709186300823e1e8d657b321218d5ede0b1f. This investigation started from 3316b381ca3386476c2bfda45a6584d6049838b3, which adds the observatory brief. The independent verifier drew the panel without evaluating times and kept both its inputs and its raw 256-bit seed outside the repository and solver context. The commitment is 5694845cd501f8083e6286be61650e900a66f513. The rule was frozen at 69249249feeb9798ac143ab6417e6341e4725ea2 before the verifier disclosed the inputs and seed. Separation was procedural between AI workers with a shared work environment. The versioned recipe identifies the exact finite sources screened for prior inputs.

From the repository root on CPython 3.11 or later, run:

```sh
python observatory/study/verify.py
python observatory/study/verify.py --case fresh-04
python observatory/study/panel.py verify observatory/study/reveal
```

The first command replays the archived 60-row ledger and its original controls, verifies the freeze digests, regenerates the fresh input panel and checks the complete result against the recorded bytes. The second also prints the requested row. The third checks only sampling, recipe, exclusions and commitments. The reproduced archival ledger contains 56 earlier successes, 39 archived four-weight successes, 21 four-weight abstentions and 60 grid successes.

All three single-output rules choose their outputs on every lineup before the scorer consults any clearance. For each nonempty subset, the independent numerical check multiplies the proposed rational time by the physical speed, rounds to the nearest whole lap using exact fractions, and takes the absolute difference. Each distance also agrees with the integer residue calculation. The record identifies every speed attaining the minimum. The complete physical residue sets agree with the candidate's bit sets at all fifteen denominators for all twenty-four rows.

## What the work counts measure

| Fresh method | Inputs per lineup | Work on twelve lineups | Full clearance checks used to choose a time |
| --- | --- | --- | --- |
| Earlier | 15 speeds | 180 denominator rankings across the panel using 2,700 divisibility tests, then 180 divisibility retests at the selected anchors. The shifted row also tested 15 noncollider memberships and computed 28 directional headrooms. | 0 |
| Archived four-weight | 4 weights | 78 ordered certificate branches considered, with one time emitted. | 0 |
| Reciprocal | 4 weights | 138 denominator trials, each with four small bit-mask updates. Eleven times emitted. | 0 |
| Grid | 15 speeds | 334 times evaluated in denominator then numerator order. Up to 162 reduced clock classes per lineup. | 334 |

“Times emitted” counts the single chosen rational time or zero on abstention. Every single-output method subsequently incurs one independent clearance check per emitted time. The grid stops at its first verified witness. The four weights determine all fifteen speeds. The smaller input count concerns the representation read, and the operation counts use different units. Runtime performance was not benchmarked.

## Controls

**REPRODUCED.** At 1/16 the lineup with speeds 0 through 15 has clearance exactly 1/16, attained by 1 and 15 relative to zero. At this time the nearest safe point is isolated locally because either side immediately loses one of those two speeds.

At 1/15, knowing the same stationary reference, family, sixteen total runners and moving-speed extrema 1 and 112 leaves the answer underdetermined. Weights (1,2,13,96) include speed 15, giving clearance zero. Weights (1,3,8,100) achieve clearance 1/15 at speeds 1 and 104. At 1/16, knowing 112 suffices for a negative answer on both completions. Two further 1/15 controls with the same extrema are recorded alongside these. The verifier also tested the seventeen original complement and three-prefix controls against the physical speeds.

The code, panel setting, arithmetic review and interpretation used AI assistance. The study establishes reproducible finite comparisons. Performance on other strata and the choice of a general certified shifted rule remain open.

[Sealed recipe](commitment.json) · [Frozen files](freeze.json) · [All rows and controls](results.json) · [Independent checks](verify.py)
