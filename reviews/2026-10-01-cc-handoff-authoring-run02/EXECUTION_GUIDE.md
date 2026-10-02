# Mediated collection instructions

This guide implements PROTOCOL.md. One coordinator writes run/ using run_support.py. Do not read evaluator/QUESTIONS_AND_KEY.json, SCORING.md, reviewer answers, prior study results, or any grades during collection. Reading names or hashes without content is permitted. Do not grade or compare response correctness. Never change inputs or repair participant answers.

The owner initializes the recorder with the published execution-freeze commit. The collection coordinator may then start authors. Only after the owner has published and checked the author-seal commit may the coordinator start recipients with that commit. The recorder checks frozen inputs on start and dispatch and checks sealed author hashes at the reader boundary; the owner, not the recorder, verifies remote publication.

Use the CLI from this package:

~~~
python run_support.py check
python run_support.py status
python run_support.py start authors
python run_support.py begin A001
python run_support.py register A001 /root/collection/a001
python run_support.py reply A001 /absolute/path/envelope.json
python run_support.py checkpoint 004
python run_support.py close
python run_support.py start recipients ACTUAL_PUBLISHED_AUTHOR_SEAL_SHA
~~~

The example identity is illustrative; register the actual returned canonical identity. The prepared arrays define the exact dispatch order. Begin returns either a prompt or a dependent-author failure. Never spawn a participant for a failure status.

For each prompt, call collaboration.spawn_agent directly with fork_turns="none", no model or reasoning override, and message equal to the returned prompt string exactly. No prefixed context, file path, condition name, commentary, or suffix. Use a lowercase opaque task name: trial A001 maps to task_name a001; Q001 maps to q001. Validate against ^[a-z0-9_]+$ before calling. The uppercase trial ID remains unchanged in recorder files. A rejected spawn with an explicit no-creation error may be corrected under the same queued trial after preserving the rejection; no respondent retry is involved. Notify the owner immediately of any rejection or uncertain delivery. Do not silently wait or terminate while a next action is available. Up to five study participants may be active; preserve dispatch order. Author and reader contexts are distinct. Do not use a respondent as a helper.

After successful spawning, register the actual identity before processing its answer. Tool return metadata and final messages are the collection record. Do not let the respondent write its own response file or call tools. Save the exact final-message string without trimming, reformatting, newline changes, or JSON repair inside an envelope with one string field, raw_text. Use structured file writing or an apply_patch payload with a JSON serialization; do not interpolate unescaped shell text. Pass the envelope path to reply. The envelope's framing newline is not part of raw_text. Put staging envelopes outside run/; the recorder saves its own immutable copy.

If reply returns SOURCE_QUEUED, the first answer has already been saved. Before the deadline, call collaboration.followup_task on the same actual participant, with message exactly the returned followup. Only after successful delivery, call delivered on its trial ID. Save the final answer through another exact-string envelope and reply. Never serve source absent a recorded request, use a new context for recovery, or give grading feedback.

A completed participant's additional unsolicited messages or observed unauthorized tool use must be preserved as a deviation; do not silently treat them as valid study exposure. Only final answers enter the raw response envelope. Append deviations to run/DEVIATIONS.jsonl, recording UTC time, trial/agent identity, event type, exact raw message where present, factual delivery/exposure status, and the handling decision. Do not rewrite previous lines. If none occur, the closeout note may report none; do not invent a dummy event. A respondent that fails schema or word checks receives no retry. Keep unavailable delivery distinct from a model protocol error. If delivery is uncertain, do not resend blindly. Use stop with the factual reason, preserve any first answer, and record a deviation.

Poll status to respect the 20-minute author and 55-minute reader/control budgets. No new spawn or recovery begins after the deadline. Interrupt outstanding participants at the deadline, record stops with explicit budget reasons, and preserve late raw messages separately as excluded deviations if the trial was already closed. Late replies passed to reply before a stop are retained as BUDGET_STOP. Close fills undispatched cells with UNRUN. Do not extend budgets, selectively rerun, replace an author, or silently exclude a cell.

Write raw checkpoints when the terminal author count reaches 4, 8, and 12, and when terminal reader/control count reaches 12, 24, 36, 48, and 54. Process one completion at a time so thresholds are exact. These checkpoints contain raw records, never grades. At each threshold notify the owner of counts only. Continue collection within the fixed budget; publication by the owner must not modify active recorder files.

After authors close, stop and report counts, elapsed collection seconds, protocol/infrastructure statuses, and that recipients have not started. Wait for the owner to give the actual published seal SHA. After recipients close, report analogous counts, recovery requests/served, and deviations. No substantive comparative conclusions during collection.

The runtime exposes no reliable provider snapshot, actual token counts, or adjustable hard token caps. Record null; inherited settings and visible word counts are not hidden-compute equivalence. Isolation is by no-fork prompts and participant instructions in a shared workspace, not a security boundary.

The current run identity and inherited-review scope are in RUN_IDENTITY.md. Send the owner a status update after the first successful registration and at the prescribed checkpoints. If no progress occurs for sixty seconds, report the concrete blocking state promptly. Owner monitors recorder status independently.
