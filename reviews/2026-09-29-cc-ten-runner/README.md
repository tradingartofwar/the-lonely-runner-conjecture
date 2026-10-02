# Frozen ten-runner joint transfer

Adding (38,18) to the previous nine-runner family yields a complete **1/8**
certificate, stronger than the ten-runner target 1/10. The fixed compiler
finds 52 candidates, 47 residual primitive directions, 2,444 contacts and four
menu entries. All 22 controls pass. Ten distinct speeds require p!=q,p!=2q.

At the known failed input (1,20), the old selected time 7/24 gives ninth
phase 1/12; the new time 63/176 gives phase 41/88 and full minimum 1/8.
The leader makes the new row's phase equal to row (6,2), with different laps.

Read the [research note](../../notes/CC_TEN_RUNNER_TRANSFER_2026_09_29.md),
PROTOCOL.md and EXECUTION_RECORD.md. General arguments remain internally
reviewed proof candidates. No arbitrary ten-runner, general optimum,
all-reference or originality claim is made.

| File | Purpose |
| --- | --- |
| INPUTS.json | Frozen protocol and eight verified source identities |
| transfer.py | Three-added-lap clipping, adapted compiler key/domain and physical recovery |
| regression.json | Exact full nine-runner stage reproduction |
| motivation.json | Preserved old-selector physical failure at (1,20) |
| stage8.json | Source geometry, candidates, coverage matrix, menu and 22 controls |
| summary.json | Reached statuses and untriggered 1/10 stage |
| geometry_review.py / .json / .md | Independent clipping and coverage; 18,731 scalar fields agree |
| physical_review.py / .json / .md | Coordinate-lap recovery, direct products, endpoints and scaling |
| proof_review.md | Uniform construction and separate post-protocol analytic interpretation |
| reproduce.py / REPRODUCTION.json | Six exact outputs reproduced byte-for-byte |
| MANIFEST.json | Final package/note SHA256 and Git blob identities |

```sh
python3 reviews/2026-09-29-cc-ten-runner/reproduce.py
```

Stage10.json is absent because the stronger Stage A certificate succeeds.
Neither threshold regeneration nor full-parent diagnosis was executed or
validated by this run. Prior packages remain unchanged.

A post-protocol hand argument, clearly separate from the frozen outputs,
shows the exact optimum at the existing control (1,2) is 1/6. This explains
why losing all open edge contacts there does not exclude strictly safe
physical points. It neither enumerates a complete safe set nor adds another
compiler trial.
