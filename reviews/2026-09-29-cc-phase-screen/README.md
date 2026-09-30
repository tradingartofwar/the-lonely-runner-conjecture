# Frozen boundary-phase screening comparison

**Sound but incomplete.** For the new tenth row (54,26), the sufficient
whole-segment screen retains five candidates and misses exactly the primitive
directions (1,2),(1,4),(5,1). Full append clipping retains 61 candidates and
finds a complete five-segment certificate at 1/8. All five screened candidates
are identical members of the full output.

Both leaders cover Q+2P>=18; their complete residual-domain union has 47
directions. The all-candidate comparison therefore identifies all positive
primitive coverage differences. The three lost rays are physical witnesses
omitted by the screen, not lonely-runner counterexamples.

Read the [research note](../../notes/CC_PHASE_SCREEN_2026_09_29.md), followed
by PROTOCOL.md and EXECUTION_RECORD.md. Universal arguments remain internally
reviewed proof candidates; the coverage-preservation claim has an explicit
counterexample. Separate AI reviews are not blind, human or formal proof.

| File | Purpose |
| --- | --- |
| INPUTS.json | Eight pinned source files and frozen protocol identity |
| compare.py | Whole-record phase screen, full append clipping, fixed compilation and comparison |
| regression.json | Sequential clipping exactly reproduces prior (38,18) coverage certificate |
| screen.json | All 48 coefficient tests, 36 boundary decisions, reasons, labels and retained records |
| restricted.json | Incomplete screened certificate, residual matrix and 22 controls |
| full_clipping.json | All 61 full source/lap attempts and original-parameter mappings |
| full.json | Complete wider certificate, full matrix and 22 controls |
| comparison.json | Exact subset, global direction comparison and first omitted-source physical witness |
| diagnostic.json | Full-parent diagnostic NOT_TRIGGERED |
| summary.json | Counts, statuses and lost directions |
| geometry_review.py / .json / .md | Independent screening/clipping/coverage; 25,843 target and 17,890 regression matches |
| physical_review.py / .json / .md | Coordinate-lap recovery and 3,102 independent candidate-contact tests |
| proof_review.md | Soundness, global comparison, loss explanation and scope |
| reproduce.py / REPRODUCTION.json | Ten exact outputs reproduced byte-for-byte |
| MANIFEST.json | Final package/note SHA256 and Git blob identities |

```sh
python3 reviews/2026-09-29-cc-phase-screen/reproduce.py
```

Restricted controls give 20 witnesses and two misses; full controls give all
22 witnesses. The third lost primitive direction appears in the complete
comparison, not the control list. The diagnostic witness at (1,2) has time
1/8 and new speed106 phase1/4. Its source fails the whole-boundary predicate,
although the same phase identity holds at that one needed contact.

No screen was enlarged after the result, and no hybrid was implemented.
Full-parent diagnosis was unnecessary; threshold1/10 was outside this fixed
comparison. The proposed hybrid would recover only residual misses, with its
costs and coverage separately frozen and tested. Smaller record counts do not
by themselves prove runtime savings.

Frozen September 29, 2026; review/reproduction completed September 30 UTC,
still September 29 in America/Los_Angeles. Earlier packages remain unchanged.
