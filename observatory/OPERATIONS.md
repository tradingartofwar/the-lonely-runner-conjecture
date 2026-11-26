# Operate the Lonely Runner Observatory

## Foreground and phone access

From a clean checkout with Python 3.11+ run `python -m observatory serve`. Open [the local board](http://127.0.0.1:8765/). This starts two available worker slots, executes the four bounded local replay assignments and stays available to display results. The replay makes zero model calls. Ctrl+C stops the server and executor. A completed checkout can reproduce the evidence separately with `python observatory/study/verify.py`.

The default database is `$XDG_STATE_HOME/lonely-runner/observatory.sqlite3`, falling back to `~/.local/state/lonely-runner/observatory.sqlite3`. Set `OBSERVATORY_DB` or pass `--db PATH` to use a different file. Use persistent local storage on the worker host. Keep the database and any SQLite WAL files together. For a consistent live backup use SQLite’s backup API. Keep the old database when starting a replay against revised inputs or code.

Local commands:

| Command after `python -m observatory` | Effect |
|---|---|
| `run` | Drain eligible deterministic checks. A restart respects existing leases and completed jobs. |
| `status` | Print operating state, remaining IDs, verification state and pilot counters. |
| `pause` | Persist the pause immediately. New leases and model reservations stop. Checks already in flight can finish. |
| `resume` | Clear the pause. Run the coordinator again if it is stopped. Original budgets and deadlines carry over. |
| `serve --board-only` | Display this store without starting arithmetic workers. |
| `snapshot` | Print a timestamped JSON projection of the store and reviewed foreground journal. |
| `pilot-start` | Open the one-time pilot window in this database. A separate executor must be running to dispatch work. |

The server binds to loopback by default and accepts read-only board requests. Operator commands require host access to the database. For a phone, use an authenticated SSH tunnel on the phone forwarding its local port 8765 to the host’s `127.0.0.1:8765`, then open that loopback URL on the phone. A trusted VPN or authenticated reverse proxy can also reach an explicitly chosen `--bind ADDRESS --port PORT`. The native server supplies neither login nor TLS. Keep it behind the chosen access boundary. The separate hosted static edition displays the timestamp and cannot pause or dispatch work.

## Evidence and recovery

`recorded-research` events use original timestamps from the reviewed project journal. They preserve the separate solver and verifier activity. The reviewed terminal export in `session/shift-run.json` also preserves the dependency from `fresh-04-audit` to `fresh-04-shift`, their original timestamps, content revisions and evidence. A clean checkout restores both as historical returns. Their originating database keeps its real rows once. `deterministic-replay` events come from real subprocesses in this checkout. `operator-assignment` events come from later worker claims. The public projection includes project task summaries, artifact paths, input/code revisions and exact event times. Private lease tokens, raw child output and environment values stay off the board. Use only public project summaries and reviewed relative artifact paths when assigning work.

A worker renews a 30-second lease during a check. After nine seconds without a heartbeat the board marks it stale. When the lease expires, the coordinator can return its assignment to the queue. Each new claim has a new token. An old token cannot publish a result or renew a lease. The default is two attempts total. Exhausted work stays failed and dependent jobs stay queued. An unsuccessful verifier leaves the research claim pending. A replacement investigation gets a new ID and preserves both histories. When the host sleeps, execution stops, the phone can lose its feed, and elapsed pilot time continues. Restart on the same disk to recover expired work.

Run `python -m unittest observatory.test_runtime -v`. The recovery test kills a real worker subprocess after its exact equality check, opens another database connection, and advances the test clock through the stale and expiry boundaries. Its durable history is queued → running (attempt 1) → queued after expiry → running (attempt 2) → completed once. The first token's late result is rejected. Other tests verify that a persisted pause blocks a restarted coordinator, a failed verifier leaves its claim pending, and simultaneous claimers cannot obtain the same assignment.

## Assign a follow-up

A new project assignment can use the same store. The automatic replay coordinator only acquires its four named arithmetic jobs. Use `assign` with a new stable ID, a short public question, a role, the input digest and a code commit or content digest. Add `--depends ID` for each prerequisite. Repeating an identical assignment is safe. This example records a bounded check on the published panel; use an existing project evidence path for its return.

```sh
panel_sha=$(python -c 'from pathlib import Path; from hashlib import sha256; print(sha256(Path("observatory/study/results.json").read_bytes()).hexdigest())')
revision=$(git rev-parse HEAD)
python -m observatory assign equality-review --role researcher \
  --task 'Recheck all tied speeds at equality on fresh-04' \
  --input-revision "$panel_sha" --code-revision "$revision"
python -m observatory assign independent-equality-review --role verifier --depends equality-review \
  --task 'Check the fresh-04 limiting speed directly from all fifteen subset sums' \
  --input-revision "$panel_sha" --code-revision "$revision"
```

On the worker host, use a private lease file with a new path for each attempt. The following commands illustrate the researcher's actual replay and return. The worker renews the lease every three seconds during longer work, and stops if renewal fails. Give the dependent verifier its own worker context and lease. Complete its return only after checking the proposed evidence independently.

```sh
lease_dir=$(mktemp -d)
lease=$lease_dir/researcher.json
python -m observatory claim equality-review --lease-file "$lease"
python observatory/study/verify.py --case fresh-04
python -m observatory heartbeat --lease-file "$lease"
python -m observatory finish completed --lease-file "$lease" --artifact observatory/study/results.json
```

Use `finish failed --lease-file "$lease"` for a failed check. A nonzero exit from `claim`, `heartbeat`, `reserve-model` or `finish` means the requested permission or write did not succeed. The public history records the terminal return once. A proposal's status changes to “verified return” only after a dependent verifier successfully attaches evidence. This records review of that assignment, without promoting an exploratory claim to an established mathematical result.

## Prepare a capped pilot on the chosen host

The pilot uses a 24-hour wall-clock window, at most six dispatches spaced at least four hours apart, at most two simultaneous leases and at most 18 model invocations across roles and retries. Dispatch and invocation reservations are charged inside the same locked transaction as the claim when applicable. An expired lease, abandoned reservation or process restart does not refund the counters. Work stops taking new reservations at the first applicable limit. Already authorized checks can report their final result. New operator work requires an explicit assignment. The bundled executor only performs local deterministic checks, and supplies no paid model adapter.

After host and usage authorization, select a dedicated persistent database, enqueue the bounded work and activate the pilot with `python -m observatory pilot-start`. This command also queues the four replay checks in a fresh database. To start with those already completed, first run the foreground replay against the chosen database. Keep every worker and the coordinator pointed at that same database.

For a trusted model worker, use `claim JOB --model-calls 1 --lease-file FILE` before its first invocation. For each additional invocation, including coordination, use `reserve-model --lease-file FILE --call-id UNIQUE-ID` immediately before calling the model. Only a successful reservation authorizes **one** call in that worker. Never reuse a reservation after a crash. The store refuses duplicate additional invocation IDs. The host operator must connect an approved model adapter and make it honor this gate. No external model or paid resource is contacted by these commands. `status` reports charged reservations conservatively, including interrupted calls.

An always-on Linux host can run the native coordinator as a user service. Save the following unit on the chosen host under `~/.config/systemd/user/lonely-runner.service`, replacing the checkout path and picking an installed Python 3.11+ executable. This template has no installation effect on its own.

```ini
[Unit]
Description=Lonely Runner research board and local checks

[Service]
WorkingDirectory=/absolute/path/to/the-lonely-runner-conjecture
ExecStart=/usr/bin/python3 -m observatory serve
Environment=OBSERVATORY_DB=%h/.local/state/lonely-runner/observatory.sqlite3
Restart=on-failure
RestartSec=5
UMask=0077

[Install]
WantedBy=default.target
```

After authorization, use `systemctl --user daemon-reload` and `systemctl --user enable --now lonely-runner.service`. The user manager must remain active after logout for unattended service. Use `systemctl --user stop lonely-runner.service` to stop both web access and execution, or `python -m observatory pause` to keep observing while dispatch is stopped. On reboot or wake, launch the same unit and use `status` to see the original deadline, usage and restart point. Repeating `pilot-start` cannot replenish a pilot. No service or recurring pilot was activated during the foreground delivery.
