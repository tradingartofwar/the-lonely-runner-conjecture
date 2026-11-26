"""Foreground coordinator, operator commands and read-only local dashboard."""
import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from contextlib import suppress
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
import os
from pathlib import Path
import signal
import subprocess
import sys
from tempfile import TemporaryDirectory
import threading
import time
from urllib.parse import urlsplit

from .runtime import (EXTERNAL, FAMILY, HEARTBEAT_SECONDS, JOBS, ROOT, STUDY, WORKERS, Store,
                      ROLES, default_db, revisions)

ARTIFACTS = {job: artifact for job, _, _, _, artifact in JOBS}
MAX_ACTION_SECONDS = 180


class Interrupted(Exception):
    pass


def check_process(store, lease, stop, argv, cwd, summary):
    if stop.is_set() or not store.action(lease, summary):
        raise Interrupted
    # The command table is fixed. Child output can contain paths or environment information.
    # Only reviewed command labels, artifact references and exit status enter the public board.
    with subprocess.Popen([sys.executable, "-E", *argv], cwd=cwd, stdin=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as process:
        start = time.monotonic()
        try:
            while True:
                if stop.is_set() or not store.heartbeat(lease):
                    raise Interrupted
                if time.monotonic() - start > MAX_ACTION_SECONDS:
                    raise ValueError("Checker exceeded its time limit")
                try:
                    code = process.wait(timeout=HEARTBEAT_SECONDS)
                except subprocess.TimeoutExpired:
                    continue
                if code:
                    raise ValueError(f"Checker exited with status {code}")
                return
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()


def execute(store, lease, stop):
    job = lease["id"]
    try:
        if revisions() != (lease["input_revision"], lease["code_revision"]):
            raise ValueError("Recorded checker or input digest changed")
        if job == "baseline":
            directory = ROOT / FAMILY
            with TemporaryDirectory() as temp:
                output = Path(temp) / "ledger.json"
                check_process(store, lease, stop, ["score.py", "panel.json", str(output)], directory,
                              "Run score.py on the archived panel and byte-compare the 60-row ledger")
                if output.read_bytes() != (directory / "ledger.json").read_bytes():
                    raise ValueError("Archived ledger mismatch")
            check_process(store, lease, stop, ["check_controls.py"], directory,
                          "Run the independently structured archived controls")
        elif job == "candidate":
            check_process(store, lease, stop, ["-m", "observatory.study.candidate", "--check-opened"], ROOT,
                          "Audit the frozen residue rule against all 60 opened lineups")
        elif job == "challenge":
            check_process(store, lease, stop, [f"{STUDY}/challenger.py"], ROOT,
                          "Recalculate the opened counterexamples and equality boundaries")
        elif job == "verify":
            check_process(store, lease, stop, [f"{STUDY}/verify.py"], ROOT,
                          "Regenerate the committed panel and independently verify the published evidence")
        else:
            raise ValueError("Unknown assignment")
        store.finish(lease, True, ARTIFACTS[job])
    except Interrupted:
        store.finish(lease, False, reason="Worker interrupted before completion")
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        # Only our own ValueErrors are public. OS error text can contain host-specific information.
        reason = str(error) if isinstance(error, ValueError) else "Local checker could not execute"
        store.finish(lease, False, reason=reason)


def coordinate(store, stop, persistent=False, worker=execute):
    """Drain runnable work. A persistent coordinator also waits through spacing and pause."""
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = set()
        while not stop.is_set():
            while len(futures) < WORKERS and not stop.is_set():
                lease = store.claim()
                if not lease:
                    break
                futures.add(pool.submit(worker, store, lease, stop))
            if futures:
                done, futures = wait(futures, timeout=1, return_when=FIRST_COMPLETED)
                for future in done:
                    future.result()
                continue
            board = store.board()
            if not persistent:
                waiting_on_lease = any(j["source"] != EXTERNAL for j in board["active_workers"] + board["stale_workers"])
                if board["paused"] or not waiting_on_lease or board["pilot"]["stop_reason"]:
                    return
            stop.wait(1 if board["unfinished"] else 5)


ROUTES = {"/": "observatory/web/index.html", "/index.html": "observatory/web/index.html",
          "/style.css": "observatory/web/style.css", "/app.js": "observatory/web/app.js",
          "/snapshot.json": "observatory/web/snapshot.json", "/results.json": f"{STUDY}/results.json",
          "/demo/": "demo/index.html", "/demo/index.html": "demo/index.html",
          "/demo/cases.json": "demo/cases.json"}


def dashboard(store, bind, port):
    class Reader(BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.read_page(head=True)

        def do_GET(self):
            self.read_page(head=False)

        def read_page(self, head):
            path = urlsplit(self.path).path
            if path == "/api/board":
                body = json.dumps(store.board(), allow_nan=False).encode()
                mime = "application/json"
            elif path in ROUTES and (ROOT / ROUTES[path]).is_file():
                file = ROOT / ROUTES[path]
                body = file.read_bytes()
                mime = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; "
                             "style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; "
                             "object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            if not head:
                with suppress(BrokenPipeError, ConnectionResetError):
                    self.wfile.write(body)

        def log_message(self, fmt, *args):
            pass  # Do not log query strings or peer addresses.

    server = ThreadingHTTPServer((bind, port), Reader)
    server.timeout = 0.5
    return server


def external_command(store, args):
    if args.command == "assign":
        store.assign(args.id, args.role, args.task, args.depends, args.input_revision, args.code_revision,
                     args.max_attempts)
        print(f"Assignment recorded: {args.id}")
        return 0
    if args.command == "claim":
        # Exclusive create protects another worker's token and rejects existing symlinks.
        fd = os.open(args.lease_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        try:
            with os.fdopen(fd, "w") as handle:
                lease = store.claim(args.model_calls, external_id=args.id)
                if lease:
                    json.dump(lease, handle)
            if not lease:
                raise ValueError("No eligible lease. Inspect status, dependencies, active leases and pilot caps.")
        except BaseException:
            args.lease_file.unlink(missing_ok=True)
            raise
        print(f"Claimed {args.id}, attempt {lease['attempt']}.")
        return 0
    lease = json.loads(args.lease_file.read_text())
    if args.command == "heartbeat":
        ok = store.heartbeat(lease)
    elif args.command == "reserve-model":
        ok = store.reserve_model(lease, args.call_id)
    else:
        ok = store.finish(lease, args.outcome == "completed", args.artifact, reason="Worker reported failed check")
    if not ok:
        raise ValueError("Lease, budget or invocation ID refused. No new work authorized.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=default_db(), help="local SQLite database")
    actions = parser.add_subparsers(dest="command", required=True)
    for name, help_text in [
        ("assign", "queue a bounded project assignment and its prerequisites"),
        ("claim", "claim an eligible external assignment using a private lease file"),
        ("heartbeat", "renew the live worker's lease"),
        ("finish", "record the external worker's result"),
        ("reserve-model", "charge one additional model invocation before use"),
        ("serve", "serve the board and process the durable queue"),
        ("run", "drain eligible work in the foreground"),
        ("snapshot", "print the timestamped public board as JSON"),
        ("status", "print operating state, usage and restart point"),
        ("pause", "stop new dispatches, allowing already leased checks to finish"),
        ("resume", "allow new dispatches within the original caps"),
        ("pilot-start", "explicitly open the 24-hour window using the existing queue"),
    ]:
        sub = actions.add_parser(name, help=help_text)
        sub.add_argument("--db", type=Path, default=argparse.SUPPRESS)
        if name in ("assign", "claim"):
            sub.add_argument("id")
        if name == "assign":
            sub.add_argument("--role", required=True, choices=sorted(ROLES))
            sub.add_argument("--task", required=True)
            sub.add_argument("--input-revision", required=True)
            sub.add_argument("--code-revision", required=True)
            sub.add_argument("--depends", action="append", default=[])
            sub.add_argument("--max-attempts", type=int, choices=(1, 2, 3), default=2)
        if name in ("claim", "heartbeat", "finish", "reserve-model"):
            sub.add_argument("--lease-file", type=Path, required=True)
        if name == "claim":
            sub.add_argument("--model-calls", type=int, choices=(0, 1), default=0,
                             help="reserve the first invocation before receiving this lease")
        if name == "reserve-model":
            sub.add_argument("--call-id", required=True)
        if name == "finish":
            sub.add_argument("outcome", choices=("completed", "failed"))
            sub.add_argument("--artifact", help="existing public project-relative evidence path")
        if name == "serve":
            sub.add_argument("--bind", default="127.0.0.1")
            sub.add_argument("--port", type=int, default=8765)
            sub.add_argument("--board-only", action="store_true", help="serve without starting any workers")
    args = parser.parse_args(argv)
    store = Store(args.db)
    if args.command in ("assign", "claim", "heartbeat", "finish", "reserve-model"):
        return external_command(store, args)
    if args.command in ("run", "pilot-start") or (args.command == "serve" and not args.board_only):
        store.seed()
    if args.command in ("run", "serve", "snapshot"):
        store.import_journal()
    if args.command == "snapshot":
        print(json.dumps(store.board(snapshot=True), indent=2))
        return 0
    if args.command in ("pause", "resume"):
        store.set_paused(args.command == "pause")
    elif args.command == "pilot-start":
        store.start_pilot()
    elif args.command in ("run", "serve"):
        stop = threading.Event()
        previous = {}
        for sig in (signal.SIGTERM, signal.SIGINT):
            previous[sig] = signal.signal(sig, lambda *_: stop.set())
        try:
            if args.command == "serve":
                with dashboard(store, args.bind, args.port) as server:
                    print(f"Research board at http://{args.bind}:{server.server_port}/", flush=True)
                    failure = []
                    def work():
                        try:
                            coordinate(store, stop, persistent=True)
                        except Exception as exc:
                            failure.append(exc)
                            stop.set()
                    workers = None
                    if not args.board_only:
                        workers = threading.Thread(target=work)
                        workers.start()
                    try:
                        while not stop.is_set():
                            server.handle_request()
                    finally:
                        stop.set()
                        if workers:
                            workers.join()
                    if failure:
                        raise failure[0]
            else:
                coordinate(store, stop)
        finally:
            for sig, prev in previous.items():
                signal.signal(sig, prev)
    board = store.board()
    print(json.dumps({k: board[k] for k in ("mode", "paused", "claim_status", "unfinished", "pilot")}, indent=2))
    failed = any(job["state"] == "failed" and job["source"] == "deterministic-replay" for job in board["jobs"])
    return int(args.command == "run" and failed)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        sys.exit(str(error))
