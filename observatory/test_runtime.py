"""Replay-store regression checks, including a real worker process death and restart."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from http.client import HTTPConnection
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import threading
import time
import unittest

from .__main__ import dashboard, main
from .runtime import (DAY, EXTERNAL, HEARTBEAT_SECONDS, LEASE_SECONDS, MAX_MODELS, REPLAY, ROOT,
                      SPACING, Store, public_artifact, public_text)


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / "research.db"
        self.now = time.time()
        self.store = Store(self.db, clock=lambda: self.now)
        self.seed = ("a"*64, "b"*64)
        self.store.seed(self.seed)

    def add_job(self, job, role="researcher", deps=(), attempts=2):
        self.store.assign(job, role, "Check a bounded sample", deps, *self.seed, max_attempts=attempts)

    def test_atomic_claim_idempotence_and_concurrency(self):
        with ThreadPoolExecutor(8) as pool:
            leases = [l for l in pool.map(lambda _: self.store.claim(), range(8)) if l]
        self.assertEqual([l["id"] for l in leases], ["baseline"])
        first = leases[0]
        self.assertTrue(self.store.finish(first, True, "experiments/subset-sum-prediction/ledger.json"))
        self.assertFalse(self.store.finish(first, True))
        self.assertFalse(self.store.heartbeat(first))
        self.assertFalse(self.store.action(first, "Old worker"))
        with ThreadPoolExecutor(8) as pool:
            leases = [l for l in pool.map(lambda _: self.store.claim(), range(8)) if l]
        self.assertEqual({l["id"] for l in leases}, {"candidate", "challenge"})
        self.add_job("another")
        self.assertIsNone(self.store.claim(external_id="another"))
        self.assertEqual(len(self.store.board()["active_workers"]), 2)
        self.store.seed(self.seed)
        with self.assertRaises(ValueError):
            self.store.seed(("0"*64,"1"*64))
        successes = [e for e in self.store.board()["events"] if e["state"] == "completed"]
        self.assertEqual(len(successes), 1)

    def test_kill_worker_reopen_recover_once(self):
        # Subprocess obtains a REAL lease, does an exact equality check, then waits for further work.
        child_code = """
from fractions import Fraction
from observatory.runtime import Store
import json, sys, time
store = Store(sys.argv[1])
lease = store.claim()
t = Fraction(1,16)
assert min(min(v*t%1,-v*t%1) for v in range(1,16)) == t
print(json.dumps(lease), flush=True)
while store.heartbeat(lease):
    time.sleep(1)
"""
        with subprocess.Popen([sys.executable, "-c", child_code, str(self.db)], cwd=ROOT,
                              stdout=subprocess.PIPE, text=True) as child:
            old = json.loads(child.stdout.readline())
            child.kill()
            child.wait(timeout=3)
        # Advance the coordinator's clock deterministically past heartbeat then lease deadlines.
        self.now = time.time() + HEARTBEAT_SECONDS*3 + 1
        reopened = Store(self.db, clock=lambda: self.now)
        self.assertEqual(reopened.board()["mode"], "stale")
        self.assertEqual(reopened.board()["stale_workers"][0]["id"], "baseline")
        self.assertIsNone(reopened.claim())
        self.now += LEASE_SECONDS
        new = reopened.claim()
        self.assertEqual((new["id"],new["attempt"]), ("baseline",2))
        self.assertFalse(reopened.finish(old, True))
        self.assertFalse(reopened.heartbeat(old))
        self.assertTrue(reopened.finish(new, True, "experiments/subset-sum-prediction/ledger.json"))
        transitions = [(e["state"], e["attempt"]) for e in reopened.board()["events"] if e["job_id"] == "baseline"]
        self.assertEqual(transitions, [("queued",0),("running",1),("queued",1),("running",2),("completed",2)])

    def test_pause_survives_restart_and_failed_verifier_stays_pending(self):
        self.store.set_paused(True)
        store = Store(self.db, clock=lambda: self.now)
        self.assertEqual(store.board()["mode"], "paused")
        self.assertIsNone(store.claim())
        store.set_paused(False)
        for job in ("baseline", "candidate", "challenge"):
            lease = store.claim()
            self.assertEqual(lease["id"], job)
            self.assertTrue(store.finish(lease, True))
        for _ in range(2):
            verifier = store.claim()
            self.assertEqual(verifier["id"], "verify")
            store.finish(verifier, False)
        self.assertIsNone(store.claim())
        self.assertFalse(store.finish(verifier, True))
        board = store.board()
        self.assertEqual(board["claim_status"], "pending verification")
        self.assertEqual(board["active_workers"], [])
        self.assertEqual(board["unfinished"], ["verify"])
        self.assertEqual(board["jobs"][-1]["state"], "failed")

    def test_dispatch_caps_spacing_and_restart(self):
        for i in range(7):
            self.add_job(f"hold-{i}")
        self.store.start_pilot()
        with self.assertRaises(ValueError):
            self.store.start_pilot()
        for i in range(6):
            lease = self.store.claim(external_id=f"hold-{i}")
            self.assertIsNotNone(lease)
            self.assertTrue(self.store.finish(lease, True, "observatory/study/candidate.py"))
            self.assertIsNone(self.store.claim())
            if i < 5:
                self.now += SPACING
        store = Store(self.db, clock=lambda: self.now)
        self.assertEqual(store.board()["pilot"]["stop_reason"], "dispatch limit")
        self.assertEqual(store.board()["pilot"]["dispatches_used"], 6)
        self.assertIsNone(store.claim(external_id="hold-6"))
        self.now += SPACING
        self.assertEqual(store.board()["pilot"]["stop_reason"], "time limit")
        self.assertIsNone(store.claim())

    def test_model_cap_before_invocations_including_retries(self):
        self.add_job("model-work")
        with self.assertRaises(ValueError):
            self.store.claim(model_calls=1, external_id="model-work")
        self.store.start_pilot()
        first = self.store.claim(model_calls=1, external_id="model-work")
        self.assertTrue(self.store.reserve_model(first, "review"))
        self.assertFalse(self.store.reserve_model(first, "review"))
        self.store.finish(first, False)
        self.assertFalse(self.store.reserve_model(first, "fenced"))
        self.now += SPACING
        store = Store(self.db, clock=lambda: self.now)
        second = store.claim(model_calls=1, external_id="model-work")
        store.set_paused(True)
        self.assertFalse(store.reserve_model(second, "paused"))
        store.set_paused(False)
        for i in range(MAX_MODELS-3):
            self.assertTrue(store.reserve_model(second, str(i)))
        self.assertFalse(store.reserve_model(second,"over-cap"))
        self.assertIsNone(store.claim())
        self.assertEqual(store.board()["pilot"]["model_calls_remaining"], 0)
        self.assertTrue(store.finish(second, True, "observatory/study/candidate.py"))
        self.assertEqual(store.board()["pilot"]["stop_reason"], "model invocation limit")

    def test_pilot_deadline_exclusive(self):
        self.store.start_pilot()
        self.now += DAY
        self.assertIsNone(self.store.claim())
        self.assertEqual(self.store.board()["pilot"]["dispatches_used"], 0)

    def test_operator_workflow(self):
        self.add_job("study-two")
        self.add_job("study-two")
        self.add_job("review-two","verifier",("study-two",),attempts=1)
        self.assertIsNone(self.store.claim(external_id="review-two"))
        self.assertIsNone(self.store.claim(external_id="candidate"))
        lease = self.store.claim(external_id="study-two")
        self.assertEqual(self.store.board()["active_workers"][0]["source"],EXTERNAL)
        with self.assertRaises(ValueError):
            self.store.finish(lease, True, "observatory/study/file-does-not-exist.md")
        self.store.finish(lease, True, "observatory/study/candidate.py")
        review = self.store.claim(external_id="review-two")
        self.store.finish(review, False)
        jobs = {j["id"]:j for j in self.store.board()["jobs"]}
        self.assertEqual(jobs["study-two"]["claim_status"], "pending verification")
        self.assertEqual(jobs["review-two"]["state"],"failed")
        self.add_job("review-three","verifier",("study-two",))
        lease = self.store.claim(external_id="review-three")
        self.store.finish(lease, True, "observatory/study/researcher.md")
        jobs = {j["id"]:j for j in self.store.board()["jobs"]}
        self.assertEqual(jobs["study-two"]["claim_status"], "verified return")
        events = [e for e in self.store.board()["events"] if e["job_id"] == "study-two"]
        self.assertTrue(all(e["source"] == EXTERNAL for e in events))

    def test_cli_tokens_stay_private_and_out_of_board(self):
        private = Path(self.temp.name) / "lease.json"
        self.add_job("cli-task")
        cli = lambda *args: main(["--db",str(self.db), *args])
        with redirect_stdout(io.StringIO()):
            self.assertEqual(cli("claim","cli-task","--lease-file",str(private)),0)
            self.assertEqual(cli("heartbeat","--lease-file",str(private)),0)
            self.assertEqual(cli("finish","completed","--artifact","observatory/study/candidate.py",
                                 "--lease-file",str(private)),0)
        self.assertEqual(os.stat(private).st_mode & 0o777,0o600)
        self.assertNotIn(json.loads(private.read_text())["token"], json.dumps(self.store.board()))

    def test_safe_public_projection_and_recorded_history(self):
        self.assertIsNone(public_artifact("observatory/study/../../secret.txt"))
        self.assertIsNone(public_artifact("observatory/study/.env"))
        text = public_text("Authorization: Bearer ghp_abcdef12345678 https://user:pwd@host/path?k=secret")
        self.assertNotIn("abcdef", text)
        self.assertNotIn("pwd", text)
        journal = Path(self.temp.name) / "journal.jsonl"
        event = dict(time="2026-11-26T12:34:56+00:00",role="researcher",state="running",
                     task="Archived algebra task", attempt=1)
        journal.write_text(json.dumps(event)+"\n")
        self.store.import_journal(journal)
        self.store.import_journal(journal)
        board = self.store.board(snapshot=True)
        self.assertEqual(board["source"], "snapshot")
        self.assertEqual(board["active_workers"], [])
        recorded = [e for e in board["events"] if e["source"] != REPLAY]
        self.assertEqual(len(recorded),1)
        self.assertEqual(recorded[0]["time"],event["time"])

    def test_imported_verified_returns_retain_provenance_and_cannot_dispatch(self):
        self.add_job("direction-change")
        self.add_job("check-direction", "verifier", ("direction-change",))
        for key in ("direction-change", "check-direction"):
            lease = self.store.claim(external_id=key)
            self.now += 1
            self.store.finish(lease, True, "observatory/study/results.json")
        board = self.store.board()
        bundle = {field: [row for row in board[field] if row["source"] == EXTERNAL] for field in ("jobs","events")}
        archive = Path(self.temp.name) / "signed-off.json"
        archive.write_text(json.dumps(bundle))
        self.store.import_reviewed(archive)
        self.assertEqual(self.store.board()["events"], board["events"])
        fresh = Store(Path(self.temp.name)/"fresh.sqlite")
        fresh.import_reviewed(archive)
        fresh.import_reviewed(archive)
        result = fresh.board()
        self.assertEqual(len(result["jobs"]), 2)
        self.assertEqual(len(result["events"]), len(bundle["events"]))
        self.assertFalse(result["active_workers"])
        self.assertIsNone(fresh.claim(external_id="direction-change"))
        for original, restored in zip(bundle["jobs"], result["jobs"]):
            self.assertEqual(restored["source"], "recorded-research")
            for field in ("id","dependencies","started_at","updated_at","finished_at","artifact",
                          "input_revision","code_revision","verified_by","claim_status"):
                self.assertEqual(restored[field], original[field])
        self.assertEqual(result["jobs"][0]["verified_by"], ["check-direction"])

    def test_read_only_http(self):
        with dashboard(self.store, "127.0.0.1", 0) as server:
            thread = threading.Thread(target=server.serve_forever)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                for method, path, code in [("GET","/api/board",200),("POST","/pause",501),
                                            ("GET","/../AGENTS.md",404),("GET","/demo/",200)]:
                    conn.request(method,path)
                    response = conn.getresponse()
                    body = response.read()
                    self.assertEqual(response.status, code)
                    if path == "/api/board":
                        self.assertEqual(json.loads(body)["source"],"local-executor")
                conn.close()
            finally:
                server.shutdown()
                thread.join()


if __name__ == "__main__":
    unittest.main()
