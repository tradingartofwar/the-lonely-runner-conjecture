"""Service client for the private Observatory queue. The bearer is read from stdin or a masked terminal."""
import argparse
import getpass
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
import uuid
import warnings
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://lonely-runner-observatory.senthein.chatgpt.site"
FREEZE = "783ec79f0ed2d9ff9234baffbb57386834bd16df"
HISTORICAL = "96dfed6b2ea74cec250c301e454b6b2c4cd13860"
SCRIPT = "observatory/escape_trial/continuation.py"
FROZEN_PATHS = (
    "experiments/one-time-prediction/predictor.py", "experiments/subset-sum-prediction/generate.py",
    "observatory/study/panel.py", "observatory/study/candidate.py", "observatory/escape_trial/rule.py",
    "observatory/escape_trial/exclusions.json", "observatory/escape_trial/reveal/panel.json",
    SCRIPT, "observatory/escape_trial/continuation_check.py",
)
FROZEN_HASH = "86bdf8223fee95d9b6d6cb1774979740334e96b2f53f3a251497dbf32dc52c1b"
FINDING = "escape-frozen-panel-verified"
FIRST_JOB = "prospective-collision-cohorts"


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def check_freeze():
    digest = hashlib.sha256()
    for path in FROZEN_PATHS:
        digest.update(hashlib.sha256((ROOT / path).read_bytes()).digest())
    if digest.hexdigest() != FROZEN_HASH:
        raise RuntimeError("Source files differ from the frozen continuation revision")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ServiceError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(f"Private Observatory service returned HTTP {code}")


class Service:
    def __init__(self, bearer):
        self.bearer = bearer
        self.opener = build_opener(NoRedirect())

    def request(self, payload=None):
        endpoint = "/api/pilot" if payload is None else "/api/dispatch"
        data = None if payload is None else canonical(payload)
        req = Request(SITE + endpoint, data=data, headers={
            "Accept": "application/json", "Content-Type": "application/json",
            "OAI-Sites-Authorization": "Bearer " + self.bearer,
        })
        for attempt in range(3):
            try:
                with self.opener.open(req, timeout=20) as reply:
                    if reply.geturl() != SITE + endpoint:
                        raise RuntimeError("Unexpected service origin or path")
                    if reply.headers.get_content_type() != "application/json":
                        raise RuntimeError("The private Site did not return queue JSON")
                    return json.load(reply)
            except HTTPError as exc:
                if exc.code not in (502, 503, 504) or attempt == 2:
                    raise ServiceError(exc.code) from None
            except (URLError, TimeoutError, ConnectionError):
                if attempt == 2:
                    raise RuntimeError("Private Site connection failed") from None
            time.sleep(0.35 * (attempt + 1))

    def post(self, action, request_id=None, **body):
        return self.request(dict(action=action, request_id=request_id or uuid.uuid4().hex, **body))


def bearer_input():
    if sys.stdin.isatty():
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            token = getpass.getpass("Private Site bearer: ")
    else:
        token = sys.stdin.readline(16385)
    token = token.strip().removeprefix("Bearer ")
    if not token or len(token) > 16384 or not re.fullmatch(r"[!-~]+", token):
        raise ValueError("Expected one private Sites service bearer")
    return token


def compact(state):
    jobs = state["jobs"]
    pending = [j for j in jobs if j["state"] == "queued" or j.get("stale")]
    model_items = [j for j in pending if j.get("protocol") not in ("cohorts", "wrap")]
    keys = ("id", "role", "task", "state", "parent_id", "source_finding_id")
    first = {k: model_items[0].get(k) for k in keys} if model_items else None
    p = state["pilot"]
    evaluation = state["evaluation"]
    dispatched = [{k: j.get(k) for k in ("id", "role", "mode", "run_id", "state", "started_at",
                                           "finished_at", "attempt", "result_digest")}
                  for j in jobs if j.get("run_id")]
    return dict(as_of=state["generated_at"], pilot={k: p.get(k) for k in (
        "status", "started_at", "ends_at", "provider_hold", "paused")},
        evaluation={k: evaluation.get(k) for k in ("model_dispatches", "deterministic_dispatches",
            "controller_runs", "completed_jobs", "verified_findings", "followups_claimed", "retries", "decision")},
        pending=len(pending), next_native_item=first, usage=state.get("usage"),
        plan=state.get("plan"), dispatches=dispatched)


def archived_events():
    foreground = (ROOT / "observatory/session/foreground.jsonl").read_text().splitlines()
    shifts = json.loads((ROOT / "observatory/session/shift-run.json").read_bytes())["events"]
    allowed = ("time", "role", "state", "task", "artifact", "job_id")
    return [{k: row[k] for k in allowed if row.get(k) is not None}
            for row in [*(json.loads(line) for line in foreground), *shifts]]


def bootstrap(service, meter):
    check_freeze()
    service.post("begin", "observatory-window-v1")
    service.post("record", "observatory-foreground-history-v1", source="Versioned foreground and shift event logs",
                 events=archived_events())
    recorded = "2026-11-26T18:00:19Z"  # publication time of the archived audit commit
    history = dict(revision=HISTORICAL, artifact="observatory/escape_trial/VERIFICATION.md",
                   replay="python observatory/escape_trial/check.py",
                   summary="The frozen selector returned 12/12 verified fresh witnesses, eleven direct. "
                           "On fresh-06, t=209/3120 gave clearance 1/16 at its sole collider 195. "
                           "The original direct and fifteen-speed rules each passed 11/12.")
    service.post("record", "observatory-escape-history-v1", source="Publication of exact verification and challenge at 96dfed6",
                 events=[dict(time=recorded, role="verifier", state="published", task=history["summary"],
                              artifact=history["artifact"], revision=HISTORICAL, replay=history["replay"]),
                         dict(time=recorded, role="challenger", state="published", revision=HISTORICAL,
                              task="Outside the four bands, (260,264,1567,2101) defeats the first-arc selector. "
                                   "Five signed endpoints are safe after re-entry; 1409/4224 has clearance 1/16 at 264.",
                              artifact="observatory/escape_trial/CHALLENGE.md",
                              replay="python observatory/escape_trial/challenge.py")],
                 finding=dict(id=FINDING, verified_at=recorded, verifier="archived-physical-verifier", **history))
    if meter:
        reading = json.loads(Path(meter).read_bytes())
        service.request(meter_payload(reading))
    state = service.request()
    existing = next((j for j in state["jobs"] if j["id"] == FIRST_JOB), None)
    if not existing:
        try:
            service.post("seed", "observatory-cohorts-seed-v1", id=FIRST_JOB, role="researcher",
                         source_finding_id=FINDING, protocol="cohorts", seed=secrets.token_hex(16),
                         task="On fresh band-matched cohorts, can the frozen rule select a safe shift with several "
                              "colliders, including a witness missed by the direct and earlier predictors?")
        except ServiceError as exc:
            # A simultaneous bootstrap may already have committed its seed.
            if exc.code != 409:
                raise
        state = service.request()
        existing = next((j for j in state["jobs"] if j["id"] == FIRST_JOB), None)
    if not existing or existing.get("protocol") != "cohorts" or existing.get("source_finding_id") != FINDING:
        raise RuntimeError("Initial prospective job could not be confirmed")
    return compact(state)


def meter_payload(reading):
    payload = dict(action="telemetry", measured_at=reading["measured_at"], source="Codex app-server allowance probe")
    if reading.get("status") == "available" and reading.get("windows"):
        payload["windows"] = [dict(label={300: "5-hour", 10080: "Weekly"}.get(row.get("duration_minutes"),
                                    "Secondary" if row.get("window") == "secondary" else "Primary"),
                                   remaining_percent=row["remaining_percent"], resets_at=row.get("resets_at"))
                              for row in reading["windows"]]
    else:
        reasons = {"cli_not_found", "read_timed_out", "initialize_refused", "app_server_closed",
                   "app_server_unavailable", "no_account", "no_codex_windows", "rate_read_refused"}
        reason = reading.get("reason")
        payload["plan_error"] = reason if reason in reasons else "allowance_read_unavailable"
        if reason == "no_account":
            payload["auth_unavailable"] = True
    payload["request_id"] = "meter-" + hashlib.sha256(canonical(payload)).hexdigest()[:32]
    return payload


def next_action(result, stage, seed):
    e = result["evidence"]
    if stage == "cohorts" and result.get("next_question"):
        return dict(next_question=result["next_question"], next_protocol="wrap", next_seed=seed)
    if stage == "wrap" and e["trigger"] in ("cohort_abstentions", "new_screen"):
        recovered = sum(c["wrap_recovered"] for c in e["counts"].values())
        inspected = sum(c["wrap_evaluated"] for c in e["counts"].values())
        if recovered:
            return dict(next_question="Can a cheap within-residue test detect safe re-entry on first-arc abstentions? "
                        "Derive one-output membership bounds using opened examples, including the unsafe interior "
                        "speed 3613. Freeze the rule before an unseen band-matched comparison with the full 30-endpoint "
                        "scan. Any unsafe issued time falsifies soundness; zero recovered misses falsifies the panel gain.")
        if inspected:
            return dict(next_question="Can a bounded predeclared anchor family recover a first-arc abstention after all "
                        "30 earliest signed endpoints failed? Design it on opened cases, freeze before an unseen "
                        "matched panel, and compare exact physical distances and losses against the frozen rule. "
                        "Any unsafe return or zero additional safe witnesses rejects the corresponding prediction.")
        return dict(next_question="This bounded screen produced no first-arc abstentions. Can a pre-outcome residue or "
                    "speed-spread criterion enrich for them? Design it on opened controls and freeze before a small "
                    "unseen band-matched comparison against an unconditioned arm. Score every draw and abstention, "
                    "then all 30 physical endpoints on misses. No increase in abstentions or zero recovered misses "
                    "falsifies the corresponding forecast.")
    return dict(decision=result["decision"])


def run_role(service, job_id):
    check_freeze()
    pid = os.getpid()
    identity = f"python-{pid}-{uuid.uuid4().hex[:12]}"
    run_id = f"process-{pid}-{time.time_ns()}"
    response = service.post("claim", id=job_id, worker=identity, run_id=run_id, mode="deterministic")
    if not response.get("job"):
        return dict(claimed=False, reason=response.get("reason"))
    job = response["job"]
    lease = dict(id=job["id"], worker=identity, lease_token=response["lease_token"])
    try:
        stage, seed, role = job["protocol"], job["seed"], job["role"]
        if stage not in ("cohorts", "wrap") or role not in ("researcher", "verifier") or not re.fullmatch(r"[0-9a-f]{32}", seed):
            raise ValueError("Unrecognized deterministic job")
        args = [SCRIPT, "--stage", stage, "--seed", seed, "--role", role, "--json"]
        proc = subprocess.run([sys.executable, *args], cwd=ROOT, stdin=subprocess.DEVNULL,
                              capture_output=True, timeout=180, check=True)
        result = json.loads(proc.stdout)
        digest = hashlib.sha256(canonical({k: result[k] for k in ("summary", "evidence")})).hexdigest()
        complete = dict(lease, revision=FREEZE, replay="python " + " ".join(args), artifact=SCRIPT,
                        summary=result["summary"], result_digest=digest)
        if role == "verifier":
            parent = response["handoff"]["parent"]
            if parent and parent.get("result_digest") == digest:
                complete.update(verdict="verified", **next_action(result, stage, seed))
            else:
                complete.update(verdict="refuted", summary="Independent replay disagrees with the submitted evidence digest. "
                                + result["summary"], decision="Review the first differing row in the saved parent and verifier replays.")
        receipt = service.post("complete", **complete)
        return dict(claimed=True, job_id=job["id"], role=role, protocol=stage, run_id=run_id,
                    summary=complete["summary"], result_digest=digest, verdict=complete.get("verdict"),
                    finding_id=receipt.get("finding_id"), next_job_id=receipt.get("next_job_id"),
                    decision_id=receipt.get("decision_id"))
    except BaseException:
        try:
            service.post("release", **lease, reason="The deterministic process could not return a complete, auditable result.")
        except (ServiceError, RuntimeError):
            pass
        raise


def drain(service):
    finished = []
    while True:
        state = service.request()
        if state["pilot"]["status"] in ("ended", "paused", "not_started"):
            break
        job = next((j for j in state["jobs"] if (j["state"] == "queued" or j.get("stale"))
                    and j.get("protocol") in ("cohorts", "wrap") and j.get("role") in ("researcher", "verifier")), None)
        if job is None:
            break
        # Each claim and its exact replay execute under a separate real process identity.
        child = subprocess.run([sys.executable, str(Path(__file__).resolve()), "_one", job["id"]],
                               input=service.bearer + "\n", text=True, capture_output=True, timeout=360)
        if child.returncode:
            raise RuntimeError("Deterministic worker failed; inspect the queue release or lease expiry")
        result = json.loads(child.stdout)
        if not result["claimed"]:
            if result.get("reason") == "no_eligible_work":
                continue
            break
        finished.append(result)
    return dict(completed=finished, **compact(service.request()))


def observed_work(service, scheduled_run):
    if not scheduled_run:
        return drain(service)
    body = dict(run_id=scheduled_run, worker="native-observatory-coordinator", mode="model",
                task="Inspect the private Observatory queue, drain bounded deterministic work, and surface pending native assignments.")
    key = "wake-" + hashlib.sha256(scheduled_run.encode()).hexdigest()[:32]
    service.post("observe", key + "-start", state="running", **body)
    try:
        result = drain(service)
    except BaseException:
        service.post("observe", key + "-failed", state="failed", **body)
        raise
    service.post("observe", key + "-complete", state="completed", **body)
    result.update(as_of=utc(), scheduled_run=scheduled_run)
    return result


def public_response(value):
    if isinstance(value, dict):
        return {k: public_response(v) for k, v in value.items() if k not in ("lease_token", "authorization")}
    if isinstance(value, list):
        return [public_response(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="operation", required=True)
    subs.add_parser("status")
    subs.add_parser("bootstrap").add_argument("--meter", type=Path)
    subs.add_parser("work").add_argument("--scheduled-run")
    post = subs.add_parser("post")
    post.add_argument("json_file", type=Path)
    post.add_argument("--receipt", type=Path, help="Create a new owner-only file for the full service response")
    subs.add_parser("_one", help=argparse.SUPPRESS).add_argument("job_id")
    args = parser.parse_args()
    service = Service(bearer_input())
    if args.operation == "status":
        result = compact(service.request())
    elif args.operation == "bootstrap":
        result = bootstrap(service, args.meter)
    elif args.operation == "work":
        result = observed_work(service, args.scheduled_run)
    elif args.operation == "_one":
        result = run_role(service, args.job_id)
    else:
        data = json.loads(args.json_file.read_bytes())
        if not isinstance(data, dict) or not data.get("request_id") or not data.get("action"):
            raise ValueError("Supply a JSON object with an explicit action and retry-stable request_id")
        if data["action"] == "claim" and not args.receipt:
            raise ValueError("Use --receipt to retain the lease for completing the claimed assignment")
        if args.receipt:
            with os.fdopen(os.open(args.receipt, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as f:
                try:
                    response = service.request(data)
                    f.write(canonical(response))
                    f.flush()
                    os.fsync(f.fileno())
                except BaseException:
                    args.receipt.unlink(missing_ok=True)
                    raise
        else:
            response = service.request(data)
        result = dict(as_of=utc(), response=public_response(response))
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, ServiceError, subprocess.SubprocessError, KeyError) as error:
        # Do not propagate provider output, local pathnames, payloads or credentials.
        text = str(error) if isinstance(error, (ServiceError, RuntimeError)) else type(error).__name__
        print(json.dumps(dict(as_of=utc(), error=text)), file=sys.stderr)
        raise SystemExit(1)
