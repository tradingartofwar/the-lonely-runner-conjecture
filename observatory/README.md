# Lonely Runner Observatory

Why did the predictors disagree on stretched middle-gap lineups? The four weights specify all fifteen moving speeds. The archived four-weight predictor tried seven sufficient conditions. It could abstain even when a simple reciprocal time was already clear. The new rule takes the four weights and tracks which residues their nonempty subset sums can reach. If zero is absent modulo a denominator from 2 through 16, its reciprocal works. The rule emits the first such reciprocal and otherwise abstains.

## Private live board

[Open the Observatory](https://lonely-runner-observatory.senthein.chatgpt.site). The hosted board reads a durable queue, shows each claim and its verified parent, timestamps Pacific-day usage and provides an owner pause button. The original foreground session is preserved in its historical archive. [Unattended pilot](PILOT.md) · [Hosted service and controls](hosted/PROTOCOL.md).

The [frozen signed-escape rule](escape_trial/RULE.md) cleared all 12 independently held fresh lineups. Its one success beyond both baselines had a single collider. The [challenger's five-collider example](escape_trial/CHALLENGE.md) shows how a runner can leave safety and return during a successful displacement. The [fresh verification](escape_trial/VERIFICATION.md) distinguishes the measured gain from the open multiple-collider question. The hosted worker takes that question into unconditioned and collision-enriched cohorts with independently checked physical speeds.

```sh
python observatory/escape_trial/check.py --case fresh-06
```

## Replay the original foreground study

Run from the repository root with CPython 3.11 or newer. The implementation uses the standard library.

```sh
python -m observatory serve
```

Open <http://127.0.0.1:8765>. The host serves its actual SQLite queue, worker leases, events and results. The original foreground export is available in the hosted archive. The [operating guide](OPERATIONS.md) covers authenticated phone access, recovery and the capped pilot. The existing [Compatibility Calculus explorer](https://compatibility-calculus.senthein.chatgpt.site) remains available.

```sh
python observatory/study/verify.py --case fresh-04
```

Omit `--case fresh-04` to regenerate and compare the full scored record. [All 24 row records](study/results.json) contain the inputs, predicted times, actual minimum distances, ties and method-specific work. [Researcher derivation](study/researcher.md) · [Challenger checks](study/challenger.md) · [Independent verification](study/verification.md).

## What the team found

All runners start together. The reference is stationary. The other fifteen speeds are the distinct nonempty subset sums of the four positive weights in the original generator. The reference needs a distance of at least 1/16 from every competitor. Each number below counts lineups with a valid returned time.

| Panel | Earlier predictor | Archived four-weight rule | Frozen reciprocal rule | Grid, denominator ≤32 |
|---|---:|---:|---:|---:|
| 12 opened middle-gap lineups | 11 | 1 | 10 | 12 |
| 12 separately sealed middle-gap lineups | 11 | 1 | 11 | 12 |

**REPRODUCED.** The original 60-row ledger matched byte for byte. Among the ten opened earlier-only successes, nine had a clear reciprocal. On the tenth, weights (41, 80, 435, 564), every small denominator collides. Moving backward from 1/9 to 1775/15984 puts speed 999 exactly at distance 1/16 and keeps all the others clear. For the direct example (2, 3, 17, 42), time 1/12 gives minimum 1/12 at speeds 47, 59 and 61.

**OBSERVED.** The frozen rule and the earlier predictor returned the same eleven valid fresh times. On the remaining row the earlier rule made an unsafe prediction and the reciprocal rule abstained. The archived four-weight rule abstained eleven times. The grid returned a valid time on every row. The reciprocal rule made 552 small mask updates on 48 input weights. The earlier rule made 2,700 speed divisibility tests for its denominator ranking alone. These are different operations. We made no wall-clock speed comparison.

### The case that changed the next assignment

Weights **(14, 17, 103, 154)**. At 1/16 a single runner collides. The earlier predictor tries to free it by shifting to **289/4608**, but speed 271 comes within **17/4608** of the reference. The reciprocal rule abstained, and the grid found **8/23** with a minimum of **2/23**.

After scoring, the coordinator tried an anchor with *more* collisions. At 1/3, speeds 117, 120, 168, 171 and 288 all coincide with the reference. Move forward by 1/1872. The slowest collider reaches the threshold first, the others are already clear and every initially clear runner has room for the move. At **625/1872** the exact minimum is **1/16**, attained by **117** alone. This is an exploratory repair. The frozen score stays at 11/12.

The researcher and verifier then took separate assignments through the live queue. The first safe interval reached going forward from 1/3 is **[625/1872, 1375/4112]**. Speed 117 is the last to enter safety and 257 is the first to leave. The verifier recovered both endpoints by sweeping exact threshold-crossing events on the physical trajectories. Run `python observatory/study/verify_shift.py` to replay this result. [Derivation](study/shift-derivation.md) · [Independent endpoint check](study/shift-verification.md) · [Queue record](session/shift-run.json).

**Original handoff.** This assignment led to the signed-escape study above. At each anchor, could all colliders escape before an initially clear runner reached its nearest unsafe arc? Keep the smallest and largest speed in each residue class. Return at most one certified time. Compare with the earlier ranking and the reciprocal rule on a new independently sealed panel. A runner can leave and re-enter its safe arc, so a failed sufficient check must remain an abstention. The pilot began with this question.

## Timing, independence and reproducibility

The project default head at intake was `c8a287f`. Work continued from the opened study at `741b709` and PR #5 at `3316b38`. Separate researcher and verifier contexts handled the candidate and the hidden panel. The verifier committed the [sampling procedure and hashes](study/commitment.json) at `5694845`, before the researcher’s [frozen rule](study/candidate.py) at `6924924`. The revealed seed reproduces all twelve lineups, three per scale band. The independent checker reconstructs the physical speeds and checks every returned time. Agreement supports bounded observations about this family and reference.

The [recorded foreground events](session/foreground.jsonl) document the human-directed research session. Running the software again creates fresh local events for a deterministic replay. A static copy can be regenerated with `python -m observatory run` followed by `python -m observatory.export_board /path/to/export`. For a new run after a code or input revision, use a fresh database path and retain the previous database for its history.

AI-assisted design, implementation, exploration and independent computation. The adjudicated evidence, its scope and the command to reproduce it accompany each claim.
