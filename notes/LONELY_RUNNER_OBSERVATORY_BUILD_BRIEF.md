# Lonely Runner Observatory
## Codex build brief · November 26, 2026

**Build a research team whose work Vance can follow on a phone.** At a glance he should be able to tell what the team is trying to distinguish, what each agent is doing, what the last exact check established, and which decision could benefit from his intuition. The first investigation belongs to Lonely Runner. The broader representation-science question is whether changing the description of a lineup makes a useful prediction possible, and what information or operation made the difference.

### Where to start

Work in `tradingartofwar/the-lonely-runner-conjecture`. The research starting point is [commit 741b709](https://github.com/tradingartofwar/the-lonely-runner-conjecture/tree/741b709186300823e1e8d657b321218d5ede0b1f) on `research/forced-overlap-handoff-2026-11-24`. Compare with the current project head and record the revision actually used. Read `AGENTS.md`, `HANDOFF.md`, `CLAIM_STATUS.md` and `CONTRIBUTING.md`. Inspect `experiments/subset-sum-prediction/` for the protocol, sealed panel, ledger and scorer, `experiments/one-time-prediction/predictor.py` for the earlier rule, and `demo/` for reusable mathematics and display code. Keep the existing Compatibility Calculus explorer available.

### First research assignment

**Why did the earlier rule find a time in ten middle-gap lineups where the four-weight rule abstained? Can the four weights yield a cheap, testable certificate for the same opportunity?** The weights determine all 15 moving speeds. A performance difference alone cannot tell us whether a calculation overlooks a relationship, expresses it inefficiently, or loses it in an intermediate summary.

Use the stationary reference, 16 total runners, starting together, and clearance **at least 1/16**. The moving speeds are all nonempty subset sums of four positive weights in the existing protocol. “Stretched middle gap” refers to the generator's `stretch_middle` stratum, where the third weight exceeds the sum of the first two by a comparatively large amount. A result for this reference and this family has exactly that scope.

| Already opened sample | Earlier one-time rule | Four-weight rule | Comparison grid |
|---|---:|---:|---:|
| All 60 lineups | 56 valid | 39 valid, 21 abstentions | 60 witnessed |
| 12 stretched middle-gap lineups | 11 valid | 1 valid, 11 abstentions | 12 witnessed |

The 12 split into one success shared by both predictors, ten earlier-only successes, and one where neither returned a valid time. This panel is available for exploration. It has already been opened.

**A diagnostic to reproduce.** In nine of the ten earlier-only successes, some integer denominator `q` from 2 through 16 divides none of the 15 speeds. At time `1/q` each speed is then at least `1/q ≥ 1/16` from the nearest integer. For the tenth earlier-only success the earlier rule shifts away from the initial time. The difference is visible in three real cases:

| Four weights | Exact return | Why this case matters |
|---|---|---|
| 2, 3, 17, 42 | At 1/12 the minimum distance is 1/12. | The four-weight rule abstains even though denominator 12 works directly. |
| 41, 80, 435, 564 | The earlier rule starts at 1/9 and returns 1775/15984, with clearance exactly 1/16. | Every denominator from 2 through 16 divides some opponent. A rule recognizing only clear denominators misses this case. |
| 3, 5, 28, 60 | The earlier rule returns 97/1536 with clearance 11/512. The grid finds 2/23 with clearance 2/23. | An unsafe prediction and an abstention are distinct outcomes. Both differ from failure of the lineup itself. |

Reproduce the archived ledger before developing a new rule. From the experiment directory run `python score.py panel.json /tmp/observatory-ledger.json` and `python check_controls.py`. Compare the generated ledger with the versioned one. For each middle-gap row, use `choose_time(speeds)` and independently count denominators in `range(2, 17)` with `all(v % q for v in speeds)`. Verify every displayed time using exact arithmetic. For `t=p/q` the clearance is `min_v min((vp) mod q, (−vp) mod q)/q`.

**First comparison.** Give one worker the nine simple cases and the shifted case. Ask which operation exposes the distinction. A concrete candidate is to compute the reachable residues of nonempty subset sums directly from the four weights. For each weight add its own residue and its sum with each previously reachable residue, preserving the previous set. Check the direct method against the list of 15 physical speeds. Matching the earlier rule's clear denominators is an explanatory result. Credit for a new prediction requires a separately identifiable gain. Record what inputs each method reads, how many candidate times it evaluates, and which choices are made before the checker is consulted.

**Fresh test.** A separate checker commits to a fresh input panel, sampling recipe and seed hash before the new rule is frozen. Use the existing middle-gap generator across its four scale bands. A first panel of 12 unseen lineups, three per band, is enough to exercise the pipeline. Exclude previously opened lineups and keep inputs and witnesses out of the solver's context until freeze. Record the rule revision, then reveal and score every row against the same earlier rule, four-weight rule and denominator-32 grid. Report correct predictions, abstentions, unsafe predictions, old-only and new-only cases, and a concrete failure when there is one. If both predictors succeed equally, report whether one used less information or work and how that was measured. Preserve unresolved and negative results. A bounded test earns only the evidence status supported by its scope.

### How the agents work

| Role | Assignment | Required return |
|---|---|---|
| Coordinator | Recover the last durable state, select a question, prevent duplicate assignments, and decide which finding changes the next task. | Question, owner, dependencies, attempt, evidence link and next decision. |
| Researcher | Propose a distinction, name what would falsify it, derive a candidate rule, and freeze it. | Assumptions, rule revision, predicted consequence and exploratory examples. |
| Challenger | Look for opposing explanations and the smallest counterexample to the stated rule. | A reproducible example, or the exact bounds of an unsuccessful search. |
| Verifier | Keep the fresh cases separate, check original speeds with an independently structured calculation, and audit equality. | Exact witness or failed inequality, command, scope, and repository claim label. |

Roles can run at different times. Use separate contexts for the solver and verifier. A deterministic checker can perform most arithmetic. Use model time for choosing distinctions, deriving rules, and interpreting failures. Let Vance redirect the question in the project thread. Record which future assignment his direction changes.

### What Vance sees

Make the board legible in portrait at 360 px and on desktop. The home screen should work in one short glance. Use plain language first and exact details one tap away.

| Part of the display | Information and behavior |
|---|---|
| Research question | The current question, the comparison that could answer it, and the latest finding that changed the next move. |
| Workers | One row per actual assignment. Show role, plain-language task, running/waiting/completed/failed state, last real update and elapsed time. Show a lost connection or overdue heartbeat explicitly. |
| Evidence | Tap a finding to see a concrete lineup, prediction and actual clearance side by side, the limiting speed, threshold, exact fractions, claim status, source revision and replay command. Show abstentions and counterexamples as first-class results. |
| Mathematical view | On the same lineup, switch between the four weights and their 15 speeds. Select a proposed time and see which runner sets the minimum clearance. If showing safe time windows, draw isolated equality times as points. A runner can meet the threshold at a single instant even when every nearby instant fails. |
| Direction and history | Show what is queued, why it follows, and the smallest decision awaiting Vance. Keep previous versions and link a corrected claim to the evidence that changed it. |
| Operating state | Clearly label live activity, historical replay, last known state, idle, and paused. Show last update, work remaining under the pilot cap, and a working pause control or authenticated operator command. |

Use the three lineups above for the first case views. A tap on **Why did this pass?** for `(2,3,17,42)` should reveal `t=1/12`, the `1/16` threshold, and the three limiting speeds 47, 59 and 61. The home screen should let Vance reach the corresponding evidence with one tap. Keep histories of tool actions and experiment outputs behind the result. Worker status comes from the executor. Avoid simulated activity and speculative percentages of progress toward a proof.

### What keeps working when a thread closes

Implement one durable queue and event store shared by the coordinator, workers and board. A small single-host implementation can use SQLite and a read-only dashboard endpoint. The project repository is the durable record for reviewed protocols, checkers and research returns. Keep high-frequency heartbeats in the operational store. Persist task IDs, parent or dependency IDs, attempts, lease expiry, event times, last activity, input and code revisions, and artifact references. Use atomic claims, bounded retries and idempotent final results so a restart cannot manufacture two successes for one job. A failed verifier leaves a research claim pending. Scrub credentials from anything the display can read. Keep the board limited to project research.

Build a foreground mode first. It must be runnable from a clean checkout and produce genuine events that the board can replay. For background operation, supply a persistent runner independent of the chat, a durable disk, a reachable phone view and a way to stop new work. State where it runs, what happens if the host sleeps, and how to resume from the recorded state. If only a static site is available, serve a clearly timestamped snapshot and retain the live board on the actual worker host. Report the access mode honestly.

### Delivery sequence and acceptance

1. **Replay the baseline.** Reproduce the 60-row ledger and the 12-row breakdown. Mark imported results as historical. Demonstrate the inclusive equality check on speeds 0 through 15 at time 1/16 for reference zero.
2. **Deliver one working path from assignment to evidence.** Use a real researcher and a separate verifier on one bounded assignment. Show a transition from queued to running to a result on the phone-sized board, together with its exact check. Supply one command to start the system and one to replay the result. Save a screenshot or accessible preview of the real run.
3. **Exercise recovery and the research comparison.** Interrupt a worker, restart the coordinator, recover the assignment once, and verify that pausing prevents new assignments. Disconnect the feed and verify the stale indicator. Freeze a candidate and run the fresh comparison. Record the case that best explains what changed, including a failed prediction if found.
4. **Prepare a capped 24-hour pilot.** Proposed first settings are up to six dispatches four hours apart, two concurrent workers, and 18 total model invocations including coordination and retries. Stop at the first applicable time, run or usage limit. Publish the counts used, unfinished tasks and a restart point. Reuse the owner's existing access when available. Follow the repository's authorization for paid compute and broad unattended runs. Build and verify the foreground path and stop controls as part of this assignment. Activate the recurring pilot when Vance chooses the host and authorizes its usage limit.

**Return to Vance** the branch or draft PR, the working board or tested local access route, the reproduction command, one real exact result, and the current operating state. State what is running now and what needs host access or a pilot decision. The most useful final sentence answers **“What can we distinguish now that we could not distinguish before, and what should we try because of it?”**

*AI-assisted design handoff. Baseline figures come from the linked project revision. The nine-case denominator diagnostic was calculated on the opened panel during preparation of this brief.*
