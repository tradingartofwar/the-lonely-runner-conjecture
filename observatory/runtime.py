"""Durable assignments, leases, public events and budget reservations (stdlib only)."""
from contextlib import contextmanager
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import sqlite3
import time

ROOT = Path(__file__).resolve().parent.parent
FAMILY = "experiments/subset-sum-prediction"
STUDY = "observatory/study"
REVISION = "3316b381ca3386476c2bfda45a6584d6049838b3"
JOURNAL = ROOT / "observatory/session/foreground.jsonl"
REVIEWED = ROOT / "observatory/session/shift-run.json"
REPLAY = "deterministic-replay"
RECORDED = "recorded-research"
EXTERNAL = "operator-assignment"
LEASE_SECONDS = 30
HEARTBEAT_SECONDS = 3
DAY = 24 * 3600
SPACING = 4 * 3600
MAX_DISPATCHES, MAX_MODELS, WORKERS = 6, 18, 2
ROLES = {"coordinator", "researcher", "challenger", "verifier"}
STATES = {"queued", "running", "completed", "failed", "waiting"}
# Only reviewed, project-relative artifacts can become links.
ALLOWED_ROOTS = ("observatory/study/", "observatory/session/", "experiments/", "notes/")
PRIVATE = re.compile(
    r"(?:-----BEGIN [^-]*PRIVATE KEY-----[\s\S]*|"
    r"(?:https?|ssh|postgres(?:ql)?|mysql)://\S+|"
    r"\b(?:authorization|bearer|basic|api[-_ ]?key|secret|password|token|credential|cookie)"
    r"\s*[:= ]\s*\S+(?:\s+\S+)?|"
    r"\b(?:sk-|gh[pousr]_|github_pat_|xox[baprs]-|AKIA)[a-zA-Z0-9_\-]{6,}|"
    r"[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})",
    re.I,
)
JOBS = (
    ("baseline", "coordinator", "Reproduce the archived 60-row ledger and its exact controls",
     (), f"{FAMILY}/ledger.json"),
    ("candidate", "researcher", "Replay the frozen four-weight rule on the opened panel",
     ("baseline",), f"{STUDY}/candidate.py"),
    ("challenge", "challenger", "Recheck the limits of reciprocal times on the opened panel",
     ("baseline",), f"{STUDY}/challenger.py"),
    ("verify", "verifier", "Independently check the revealed panel and every reported result",
     ("candidate", "challenge"), f"{STUDY}/results.json"),
)


def utc(epoch):
    return datetime.fromtimestamp(epoch, timezone.utc).isoformat() if epoch is not None else None


def public_text(value):
    if not isinstance(value, str):
        raise ValueError("Public summaries must be text")
    return " ".join(PRIVATE.sub("[redacted]", value).split())[:240]


def public_artifact(path):
    if not isinstance(path, str) or not path.startswith(ALLOWED_ROOTS):
        return None
    if not re.fullmatch(r"[a-zA-Z0-9_./-]+", path) or any(p.startswith(".") for p in path.split("/")):
        return None
    if PurePosixPath(path).suffix not in {".json", ".jsonl", ".md", ".py", ".txt"}:
        return None
    return path


def revision(paths):
    digest = sha256()
    for path in sorted(set(paths)):
        digest.update(path.relative_to(ROOT).as_posix().encode() + b"\x00")
        digest.update(sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def revisions():
    family, study = ROOT / FAMILY, ROOT / STUDY
    # Bind the actual replay inputs and checkers even in a source archive without Git.
    inputs = [*(ROOT / "experiments").rglob("*.json"),
              *(study / name for name in ("commitment.json", "exclusions.json", "freeze.json",
                                          "results.json", "reveal/seed.hex", "reveal/panel.json"))]
    code = [*family.glob("*.py"), *(ROOT / "experiments/one-time-prediction").glob("*.py"),
            *(ROOT / "experiments/count-invariants").glob("*.py"), ROOT / "experiments/two-replacements/lr_two_swap.py",
            *(study / name for name in ("panel.py", "candidate.py", "challenger.py", "verify.py")),
            ROOT / "observatory/runtime.py", ROOT / "observatory/__main__.py"]
    return revision(inputs), revision(code)


def default_db():
    if os.environ.get("OBSERVATORY_DB"):
        return Path(os.environ["OBSERVATORY_DB"]).expanduser()
    home = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    return home / "lonely-runner/observatory.sqlite3"


SCHEMA = """
CREATE TABLE IF NOT EXISTS settings(
 id INTEGER PRIMARY KEY CHECK(id=1), paused INTEGER NOT NULL DEFAULT 0,
 pilot_start REAL, next_dispatch REAL, dispatches INTEGER NOT NULL DEFAULT 0,
 models INTEGER NOT NULL DEFAULT 0);
INSERT OR IGNORE INTO settings(id) VALUES(1);
CREATE TABLE IF NOT EXISTS jobs(
 id TEXT PRIMARY KEY, role TEXT NOT NULL, task TEXT NOT NULL, state TEXT NOT NULL,
 attempt INTEGER NOT NULL DEFAULT 0, max_attempts INTEGER NOT NULL DEFAULT 2,
 created REAL NOT NULL, started REAL, updated REAL NOT NULL, finished REAL,
 token TEXT, expires REAL, artifact TEXT, input_rev TEXT NOT NULL, code_rev TEXT NOT NULL, source TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS deps(job TEXT NOT NULL REFERENCES jobs, required TEXT NOT NULL REFERENCES jobs,
 PRIMARY KEY(job,required));
CREATE TABLE IF NOT EXISTS events(
 id INTEGER PRIMARY KEY, at REAL NOT NULL, job TEXT, role TEXT NOT NULL, state TEXT NOT NULL,
 task TEXT NOT NULL, attempt INTEGER NOT NULL, artifact TEXT, source TEXT NOT NULL,
 journal_key TEXT UNIQUE);
CREATE INDEX IF NOT EXISTS timeline ON events(at,id);
CREATE TABLE IF NOT EXISTS model_reservations(
 job TEXT NOT NULL REFERENCES jobs, attempt INTEGER NOT NULL, key TEXT NOT NULL,
 PRIMARY KEY(job,attempt,key));
"""


class Store:
    def __init__(self, path, clock=time.time):
        self.path = Path(path)
        self.clock = clock
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        # SQLite uses the DB's permissions for its journal files.
        self.path.touch(mode=0o600, exist_ok=True)
        with self.connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(SCHEMA)

    @contextmanager
    def connection(self, write=False):
        conn = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA foreign_keys=ON")
            if write:
                conn.execute("BEGIN IMMEDIATE")
            yield conn
            if conn.in_transaction:
                conn.commit()
        except BaseException:
            if conn.in_transaction:
                conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def event(conn, at, job, role, state, task, attempt=0, artifact=None, source=REPLAY, key=None):
        conn.execute("""INSERT OR IGNORE INTO events(at,job,role,state,task,attempt,artifact,source,journal_key)
                        VALUES(?,?,?,?,?,?,?,?,?)""",
                     (at, job, role, state, public_text(task), attempt, public_artifact(artifact), source, key))

    def seed(self, revs=None):
        """Idempotent across restarts. Never mix different frozen inputs in one database."""
        input_rev, code_rev = revs or revisions()
        with self.connection(write=True) as conn:
            now = self.clock()
            for job, role, task, deps, _ in JOBS:
                existing = conn.execute("SELECT input_rev,code_rev FROM jobs WHERE id=?", (job,)).fetchone()
                if existing:
                    if tuple(existing) != (input_rev, code_rev):
                        raise ValueError("Replay files changed. Preserve this database and select a new --db.")
                    continue
                conn.execute("""INSERT INTO jobs(id,role,task,state,created,updated,input_rev,code_rev,source)
                                VALUES(?,?,?,'queued',?,?,?,?,?)""", (job, role, task, now, now, input_rev, code_rev, REPLAY))
                conn.executemany("INSERT INTO deps VALUES(?,?)", [(job, dep) for dep in deps])
                self.event(conn, now, job, role, "queued", task)

    def assign(self, job, role, task, deps, input_revision, code_revision, max_attempts=2):
        if not re.fullmatch(r"[a-z][a-z0-9-]{1,47}", job) or job.startswith("session-"):
            raise ValueError("Choose a short lowercase project job ID")
        task = public_text(task)
        if role not in ROLES or not task or not 1 <= max_attempts <= 3:
            raise ValueError("Provide a role, bounded task and one to three attempts")
        if not all(re.fullmatch(r"[0-9a-f]{7,64}", r) for r in (input_revision, code_revision)):
            raise ValueError("Input and code revisions must be hexadecimal commit IDs or digests")
        deps = sorted(set(deps))
        with self.connection(write=True) as conn:
            now = self.clock()
            previous = conn.execute("""SELECT source,role,task,input_rev,code_rev,max_attempts FROM jobs
                                       WHERE id=?""", (job,)).fetchone()
            if previous:
                recorded_deps = [r[0] for r in conn.execute("SELECT required FROM deps WHERE job=? ORDER BY required", (job,))]
                if tuple(previous) == (EXTERNAL, role, task, input_revision, code_revision, max_attempts) and deps == recorded_deps:
                    return
                raise ValueError("This ID already identifies another assignment")
            for dep in deps:
                if not conn.execute("SELECT 1 FROM jobs WHERE id=?", (dep,)).fetchone():
                    raise ValueError("A prerequisite does not exist")
            conn.execute("""INSERT INTO jobs(id,role,task,state,created,updated,input_rev,code_rev,source,max_attempts)
                            VALUES(?,?,?,'queued',?,?,?,?,?,?)""",
                         (job, role, task, now, now, input_revision, code_revision, EXTERNAL, max_attempts))
            conn.executemany("INSERT INTO deps VALUES(?,?)", [(job, d) for d in deps])
            self.event(conn, now, job, role, "queued", task, source=EXTERNAL)

    def import_journal(self, path=JOURNAL):
        if not path.is_file():
            return
        entries = []
        for line in path.read_text().splitlines():
            row = json.loads(line)
            role, state, attempt = row["role"], row["state"], row["attempt"]
            if role not in ROLES or state not in STATES or type(attempt) is not int or attempt < 1:
                raise ValueError("Invalid recorded assignment")
            stamp = datetime.fromisoformat(row["time"].replace("Z", "+00:00"))
            if stamp.utcoffset() is None:
                raise ValueError("Journal times require a timezone")
            key = sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
            entries.append((stamp.timestamp(), "session-" + role, role, state, row["task"], attempt,
                            row.get("artifact"), RECORDED, key))
        with self.connection(write=True) as conn:
            for entry in entries:
                self.event(conn, *entry)

        if path == JOURNAL:
            self.import_reviewed()

    def import_reviewed(self, path=REVIEWED):
        """Rehydrate only signed-off, terminal external returns. No lease or budget is imported."""
        if not path.is_file():
            return
        archive = json.loads(path.read_bytes())
        allowed = STATES | {"checking", "reserved"}
        def epoch(value):
            stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if stamp.utcoffset() is None:
                raise ValueError("Recorded assignment requires an absolute time")
            return stamp.timestamp()

        with self.connection(write=True) as conn:
            imported = {}
            for job in archive["jobs"]:
                key = job["id"]
                if (not re.fullmatch(r"[a-z][a-z0-9-]{1,47}", key) or key.startswith("session-")
                        or job["role"] not in ROLES or job["state"] not in ("completed", "failed")
                        or job["source"] != EXTERNAL or type(job["attempt"]) is not int or job["attempt"] < 1
                        or not all(re.fullmatch("[0-9a-f]{7,64}", job[r]) for r in ("input_revision", "code_revision"))):
                    raise ValueError("Invalid reviewed job")
                previous = conn.execute("SELECT * FROM jobs WHERE id=?", (key,)).fetchone()
                if previous:
                    if (previous["role"], previous["input_rev"], previous["code_rev"], previous["state"],
                        utc(previous["finished"])) != (job["role"], job["input_revision"], job["code_revision"],
                        job["state"], utc(epoch(job["finished_at"]))) or previous["source"] not in (EXTERNAL, RECORDED):
                        raise ValueError("Reviewed job ID collides with a different assignment")
                    continue
                start, finish = epoch(job["started_at"]), epoch(job["finished_at"])
                created = min((epoch(e["time"]) for e in archive["events"] if e["job_id"] == key), default=start)
                conn.execute("""INSERT INTO jobs(id,role,task,state,attempt,created,started,updated,finished,
                                artifact,input_rev,code_rev,source) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                             (key, job["role"], public_text(job["task"]), job["state"], job["attempt"], created,
                              start, epoch(job["updated_at"]), finish, public_artifact(job["artifact"]),
                              job["input_revision"], job["code_revision"], RECORDED))
                imported[key] = job
            for key, job in imported.items():
                conn.executemany("INSERT INTO deps VALUES(?,?)", [(key, dep) for dep in job["dependencies"]])
            for e in archive["events"]:
                job = imported.get(e["job_id"])
                if job is None:
                    continue
                if (e["role"] != job["role"] or e["source"] != EXTERNAL or e["state"] not in allowed
                        or type(e["attempt"]) is not int):
                    raise ValueError("Invalid reviewed event")
                stamp = epoch(e["time"])
                digest = sha256(json.dumps(e, sort_keys=True).encode()).hexdigest()
                self.event(conn, stamp, e["job_id"], e["role"], e["state"], e["task"], e["attempt"],
                           e.get("artifact"), RECORDED, digest)

    def set_paused(self, paused):
        with self.connection(write=True) as conn:
            changed = conn.execute("UPDATE settings SET paused=? WHERE paused!=?", (paused, paused)).rowcount
            if changed:
                self.event(conn, self.clock(), None, "coordinator", "paused" if paused else "resumed",
                           "Operator paused new work" if paused else "Operator resumed new work")

    def start_pilot(self):
        with self.connection(write=True) as conn:
            now = self.clock()
            if conn.execute("SELECT 1 FROM jobs WHERE state='running'").fetchone():
                raise ValueError("Finish or recover active leases before starting a pilot")
            changed = conn.execute("""UPDATE settings SET pilot_start=?,next_dispatch=?
                                      WHERE pilot_start IS NULL""", (now, now)).rowcount
            if not changed:
                raise ValueError("A pilot already exists in this database. Its counters are durable.")
            self.event(conn, now, None, "coordinator", "pilot-started", "Operator activated the capped pilot")

    @staticmethod
    def pilot(settings, now):
        start = settings["pilot_start"]
        ends = start + DAY if start is not None else None
        runs, models = settings["dispatches"], settings["models"]
        reason = None
        if ends is not None:
            if now >= ends:
                reason = "time limit"
            elif runs >= MAX_DISPATCHES:
                reason = "dispatch limit"
            elif models >= MAX_MODELS:
                reason = "model invocation limit"
        return dict(enabled=start is not None, dispatches_used=runs, dispatches_remaining=MAX_DISPATCHES-runs,
                    model_calls_used=models, model_calls_remaining=MAX_MODELS-models, max_dispatches=MAX_DISPATCHES,
                    max_model_calls=MAX_MODELS, concurrency=WORKERS, ends_at=utc(ends), started_at=utc(start),
                    next_dispatch_at=utc(settings["next_dispatch"]), stop_reason=reason)

    def claim(self, model_calls=0, external_id=None):
        """Atomically charge a dispatch and any required model calls before returning a lease."""
        if type(model_calls) is not int or model_calls < 0:
            raise ValueError("Invalid number of model calls")
        with self.connection(write=True) as conn:
            now = self.clock()
            for row in conn.execute("SELECT * FROM jobs WHERE state='running' AND expires<=?", (now,)).fetchall():
                self.release(conn, row, now, "Lease expired")
            settings = conn.execute("SELECT * FROM settings").fetchone()
            pilot = self.pilot(settings, now)
            if settings["paused"] or pilot["stop_reason"]:
                return None
            if model_calls and not pilot["enabled"]:
                raise ValueError("Model reservations require an explicitly activated pilot")
            if pilot["enabled"] and (now < settings["next_dispatch"] or model_calls > pilot["model_calls_remaining"]):
                return None
            if conn.execute("SELECT count(*) FROM jobs WHERE state='running'").fetchone()[0] >= WORKERS:
                return None
            row = conn.execute("""SELECT j.* FROM jobs j WHERE state='queued' AND j.source=?
                AND (? IS NULL OR j.id=?) AND NOT EXISTS
                (SELECT 1 FROM deps d JOIN jobs p ON p.id=d.required
                 WHERE d.job=j.id AND p.state!='completed') ORDER BY j.rowid LIMIT 1""",
                (EXTERNAL if external_id else REPLAY, external_id, external_id)).fetchone()
            if row is None:
                return None
            token, attempt = secrets.token_hex(20), row["attempt"] + 1
            conn.execute("""UPDATE jobs SET state='running',attempt=?,started=?,updated=?,token=?,expires=?
                            WHERE id=?""", (attempt, now, now, token, now+LEASE_SECONDS, row["id"]))
            if pilot["enabled"]:
                conn.execute("""UPDATE settings SET dispatches=dispatches+1,models=models+?,next_dispatch=?""",
                             (model_calls, now+SPACING))
            self.event(conn, now, row["id"], row["role"], "running", row["task"], attempt, source=row["source"])
            return dict(id=row["id"], role=row["role"], token=token, attempt=attempt,
                        code_revision=row["code_rev"], input_revision=row["input_rev"])

    def reserve_model(self, lease, call_key):
        """Issue a one-time permission before an additional invocation, including coordinator calls."""
        if not re.fullmatch(r"[a-z0-9-]{1,48}", call_key):
            raise ValueError("Provide a short project-local invocation ID")
        with self.connection(write=True) as conn:
            now = self.clock()
            row = conn.execute("SELECT * FROM jobs WHERE id=? AND token=? AND state='running' AND expires>?",
                               (lease["id"], lease["token"], now)).fetchone()
            settings = conn.execute("SELECT * FROM settings").fetchone()
            pilot = self.pilot(settings, now)
            if row is None or settings["paused"] or not pilot["enabled"] or pilot["stop_reason"]:
                return False
            if not conn.execute("INSERT OR IGNORE INTO model_reservations VALUES(?,?,?)",
                                (row["id"], row["attempt"], call_key)).rowcount:
                return False
            conn.execute("UPDATE settings SET models=models+1")
            self.event(conn, now, row["id"], row["role"], "reserved", "Reserved one model invocation",
                       row["attempt"], source=row["source"])
            return True

    def heartbeat(self, lease):
        with self.connection(write=True) as conn:
            now = self.clock()
            return bool(conn.execute("""UPDATE jobs SET updated=?,expires=? WHERE id=? AND token=?
                      AND state='running' AND expires>?""",
                      (now, now+LEASE_SECONDS, lease["id"], lease["token"], now)).rowcount)

    def action(self, lease, summary, artifact=None):
        with self.connection(write=True) as conn:
            now = self.clock()
            row = conn.execute("SELECT * FROM jobs WHERE id=? AND token=? AND state='running' AND expires>?",
                               (lease["id"], lease["token"], now)).fetchone()
            if row is None:
                return False
            self.event(conn, now, row["id"], row["role"], "checking", summary, row["attempt"], artifact, row["source"])
            return True

    def release(self, conn, row, now, reason):
        state = "failed" if row["attempt"] >= row["max_attempts"] else "queued"
        conn.execute("""UPDATE jobs SET state=?,updated=?,finished=?,token=NULL,expires=NULL WHERE id=?""",
                     (state, now, now if state == "failed" else None, row["id"]))
        self.event(conn, now, row["id"], row["role"], state, reason, row["attempt"], source=row["source"])

    def finish(self, lease, success, artifact=None, reason="Check returned an error"):
        """Late, duplicate or fenced completions are no-ops."""
        with self.connection(write=True) as conn:
            now = self.clock()
            row = conn.execute("SELECT * FROM jobs WHERE id=? AND token=? AND state='running' AND expires>?",
                               (lease["id"], lease["token"], now)).fetchone()
            if row is None:
                return False
            if success:
                artifact = public_artifact(artifact)
                if row["source"] == EXTERNAL and (not artifact or not (ROOT / artifact).is_file()):
                    raise ValueError("External completion requires an existing public project artifact")
                conn.execute("""UPDATE jobs SET state='completed',finished=?,updated=?,token=NULL,
                                expires=NULL,artifact=? WHERE id=?""", (now, now, artifact, row["id"]))
                self.event(conn, now, row["id"], row["role"], "completed", row["task"], row["attempt"], artifact, row["source"])
            else:
                self.release(conn, row, now, reason)
            return True

    def board(self, snapshot=False):
        with self.connection() as conn:
            conn.execute("BEGIN")  # All projections reflect one committed point in time.
            now = self.clock()
            settings = conn.execute("SELECT * FROM settings").fetchone()
            deps = {}
            for job, parent in conn.execute("SELECT job,required FROM deps ORDER BY required"):
                deps.setdefault(job, []).append(parent)
            events = [dict(id=r["id"], time=utc(r["at"]), role=r["role"], state=r["state"], task=r["task"],
                           job_id=r["job"], attempt=r["attempt"], artifact=r["artifact"], source=r["source"])
                      for r in conn.execute("SELECT * FROM events ORDER BY at,id")]
            jobs = []
            recorded = {}
            retained_ids = {r[0] for r in conn.execute("SELECT id FROM jobs WHERE source=?", (RECORDED,))}
            for e in events:
                if e["source"] != RECORDED or e["job_id"] in retained_ids:
                    continue
                job = recorded.setdefault(e["job_id"], dict(id=e["job_id"], role=e["role"], dependencies=[],
                    started_at=None, lease_expires=None, stale=False, source=RECORDED, artifact=None,
                    finished_at=None, elapsed_seconds=None, input_revision=None, code_revision=None))
                if e["state"] == "running" and job["started_at"] is None:
                    job["started_at"] = e["time"]
                if e["state"] in ("completed", "failed"):
                    job["finished_at"] = e["time"]
                job.update(state=e["state"], task=e["task"], attempt=e["attempt"], updated_at=e["time"])
                if e["artifact"]:
                    job["artifact"] = e["artifact"]
                if job["started_at"]:
                    job["elapsed_seconds"] = max(0, int((datetime.fromisoformat(e["time"]) -
                                                        datetime.fromisoformat(job["started_at"])).total_seconds()))
            jobs.extend(recorded.values())
            for r in conn.execute("SELECT * FROM jobs ORDER BY rowid"):
                elapsed = max(0, int((r["finished"] or now) - r["started"])) if r["started"] is not None else None
                jobs.append(dict(id=r["id"], role=r["role"], task=r["task"], state=r["state"], attempt=r["attempt"],
                    dependencies=deps.get(r["id"], []), started_at=utc(r["started"]), updated_at=utc(r["updated"]),
                    finished_at=utc(r["finished"]), lease_expires=utc(r["expires"]), elapsed_seconds=elapsed,
                    stale=r["state"] == "running" and (r["expires"] <= now or now-r["updated"] > HEARTBEAT_SECONDS*3),
                    artifact=r["artifact"], source=r["source"], input_revision=r["input_rev"], code_revision=r["code_rev"]))
        operational = [j for j in jobs if j["source"] != RECORDED]
        replay = [j for j in operational if j["source"] == REPLAY]
        reviews = {}
        for j in jobs:
            if j["source"] in (EXTERNAL, RECORDED) and j["role"] == "verifier" and j["state"] == "completed":
                for dependency in j["dependencies"]:
                    reviews.setdefault(dependency, []).append(j["id"])
        for j in jobs:
            if j["source"] == EXTERNAL or j["id"] in retained_ids:
                j["verified_by"] = reviews.get(j["id"], [])
                if j["role"] == "verifier":
                    j["claim_status"] = {"completed":"audit completed", "failed":"failed audit"}.get(j["state"],"audit pending")
                else:
                    j["claim_status"] = "verified return" if j["verified_by"] else "pending verification"
        stale = [j for j in operational if j["stale"]]
        active = [j for j in operational if j["state"] == "running" and not j["stale"]]
        pending = [j["id"] for j in operational if j["state"] != "completed"]
        pilot = self.pilot(settings, now)
        if settings["paused"]:
            mode = "paused"
        elif stale:
            mode = "stale"
        elif active:
            mode = "live"
        elif pending:
            mode = "waiting"
        else:
            mode = "idle"
        verified = any(j["id"] == "verify" and j["state"] == "completed" for j in replay)
        claim = "OBSERVED" if verified else "pending verification"
        if not replay and reviews:
            claim = "verified return"
        return dict(generated_at=utc(now), last_event_at=events[-1]["time"] if events else None,
                    source="snapshot" if snapshot else "local-executor", mode=mode, paused=bool(settings["paused"]),
                    claim_status=claim, claim_scope="bounded study replay" if replay else "operator assignments",
                    source_revision=REVISION,
                    active_workers=active, stale_workers=stale, jobs=jobs, events=events, pilot=pilot,
                    unfinished=pending)
