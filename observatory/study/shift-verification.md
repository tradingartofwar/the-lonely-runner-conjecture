# Independent interval check for fresh-04

**REPRODUCED.** For weights (14,17,103,154), the first connected set of safe times going forward from 1/3 is the closed interval **[625/1872, 1375/4112]**, of width **125/240552**. Both endpoints have clearance exactly 1/16. Speed 117 is the sole limiter at entry and speed 257 is the sole limiter at exit. This is a post-score check of one revealed lineup of sixteen common-start runners relative to zero.

| Open time interval | Speeds below 1/16 |
| --- | --- |
| From 641/1920 to 625/1872, immediately before entry | 117 only |
| From 625/1872 to 1375/4112, inside the safe component | None |
| From 1375/4112 to 991/2960, immediately after exit | 257 only |

The audit generated all fifteen physical speeds, sorted all exact times at which any speed crosses distance 1/16 on [1/3,1], and tested event points and the intervening open cells in chronological order. The set of blockers is constant on each open cell, so one rational midpoint classifies that entire cell. Checking each event separately preserves equality and would detect an isolated safe instant. The first five event points (including 1/3) and five open cells all fail. This computation uses nearest-integer distances on the individual speeds.

The verifier fixed the endpoints, limiters and adjacent blockers before reading the researcher's residue-class derivation. The two methods agree. The post-hoc discovery leaves the frozen comparison at eleven correct predictions and one abstention on the twelve fresh lineups.

Run `python observatory/study/verify_shift.py` from the repository root. [Independent audit](verify_shift.py) · [Researcher's derivation](shift-derivation.md) · [Frozen study](verification.md)
