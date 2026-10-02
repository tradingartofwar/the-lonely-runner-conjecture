#!/usr/bin/env python3
"""Exercise recorder paths on invented dummy data outside the six study histories."""
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import tempfile
import materials as m
import run_support as r

ROOT = Path(__file__).resolve().parent
checks = []


def denied(fn, *args):
    try:
        fn(*args)
    except (AssertionError, FileExistsError, ValueError):
        return
    raise AssertionError("Forbidden mutation accepted.")


@contextmanager
def fixture():
    old = r.HERE, r.OUT, m.HERE, r.now
    with tempfile.TemporaryDirectory(prefix="cc-authoring-dummy-") as name:
        p = Path(name)
        r.HERE = m.HERE = p
        r.OUT = p / "run"
        clock = [1000.0]
        r.now = lambda: clock[0]
        r.write(p / "CONFIG.json", {"author_word_cap": 220, "recipient_answer_word_cap": 160,
                "max_active_contexts": 1, "author_phase_seconds": 20, "recipient_phase_seconds": 30})
        r.write(p / "prepared/AUTHOR_INPUTS.json",
                [{"id": "A001", "history": "DUMMY", "method": "cc", "prompt": "DUMMY AUTHOR ONE"},
                 {"id": "A002", "history": "DUMMY", "method": "conventional", "prompt": "DUMMY AUTHOR TWO"}])
        r.write(p / "prepared/RECIPIENT_SCHEDULE.json",
                [{"id": "Q001", "history": "DUMMY", "question": "DUMMY-Q", "method": "cc", "author": "A001"},
                 {"id": "Q002", "history": "DUMMY", "question": "DUMMY-Q", "method": "full_source", "author": None},
                 {"id": "Q003", "history": "DUMMY", "question": "DUMMY-Q", "method": "conventional", "author": "A002"}])
        r.write(p / "prepared/QUESTION_PROMPTS.json", {"DUMMY-Q": {"history": "DUMMY", "query": "What is the dummy value?"}})
        (p / "histories").mkdir()
        (p / "histories/DUMMY.md").write_text("Dummy value is seven. This is not a study history.")
        (p / "recipient_common.txt").write_text("DUMMY recipient instructions.")
        r.write(p / "EXECUTION_MANIFEST.json", {"sha256": {
            str(f.relative_to(p)): hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob("*") if f.is_file()}})
        r.init("DUMMY-FREEZE")
        yield p, clock
    r.HERE, r.OUT, m.HERE, r.now = old


def capture(p, text):
    path = p / "capture.json"
    r.write(path, {"raw_text": text})
    return str(path)


AUTHOR = json.dumps({"status": "Dummy ready.", "evidence": "Value seven.", "next": "No action."})
FIRST = json.dumps({"answer": "The supplied summary omits the dummy value.", "recover": True})
FINAL = json.dumps({"answer": "Seven.", "recover": False})


def authors(p, bad_second=False):
    r.start("authors")
    for i in [1, 2]:
        tid = f"A{i:03}"
        r.begin(tid)
        r.register(tid, f"/dummy/a{i}")
        r.reply(tid, capture(p, "malformed" if bad_second and i == 2 else AUTHOR))
    r.close()


def main():
    with fixture() as (p, clock):
        denied(r.init, "ANOTHER-FREEZE")
        r.start("authors")
        denied(r.begin, "A002")
        r.begin("A001")
        denied(r.begin, "A002")
        denied(r.close)
        r.register("A001", "/dummy/a1")
        result = r.reply("A001", capture(p, AUTHOR))
        assert result["status"] == "COMPLETED"
        assert r.read(r.OUT / "incoming/A001-01.json")["raw_text"] == AUTHOR
        denied(r.reply, "A001", capture(p, AUTHOR))
        r.begin("A002")
        denied(r.register, "A002", "/dummy/a1")
        r.register("A002", "/dummy/a2")
        too_long = json.dumps({"status": "x " * 219, "evidence": "x", "next": "x"})
        assert r.reply("A002", capture(p, too_long))["status"] == "AUTHOR_PROTOCOL_ERROR"
        assert r.read(r.trial_path("A002"))["messages"][-1]["validation"] == {
            "json_parse_status": "PASS", "decoded_words": 221,
            "schema_and_cap_status": "FAIL", "error": "author word cap"}
        r.checkpoint("dummy-authors")
        r.close()
        denied(r.start, "authors")
        r.start("recipients", "DUMMY-AUTHOR-SEAL")
        r.begin("Q001")
        r.register("Q001", "/dummy/q1")
        result = r.reply("Q001", capture(p, FIRST))
        assert result["status"] == "SOURCE_QUEUED"
        first = r.read(r.trial_path("Q001"))["first_answer"]
        denied(r.reply, "Q001", capture(p, FINAL))
        r.delivered("Q001")
        denied(r.delivered, "Q001")
        assert r.reply("Q001", capture(p, FINAL))["status"] == "COMPLETED"
        t = r.read(r.trial_path("Q001"))
        assert t["first_answer"] == first and t["final_answer"]["answer"] == "Seven."
        assert t["messages"][1]["validation"]["decoded_words"] == len(first["answer"].split())
        assert t["messages"][3]["validation"]["decoded_words"] == 1
        assert t["messages"][3]["validation"]["schema_and_cap_status"] == "PASS"
        assert t["recovery_served"] and t["messages"][2]["delivery"] == "delivered"
        r.begin("Q002")
        r.register("Q002", "/dummy/q2")
        assert r.reply("Q002", capture(p, FINAL))["status"] == "COMPLETED"
        assert r.read(r.trial_path("Q002"))["first_answer"] == r.read(r.trial_path("Q002"))["final_answer"]
        assert r.begin("Q003")["status"] == "AUTHOR_PROTOCOL_ERROR"
        r.checkpoint("dummy-readers")
        r.close()
        assert r.state()["status"] == "CLOSED"
        checks.extend(["no restart or overwrite", "ordered dispatch and active cap", "close rejects active",
                       "unique participant identities", "exact envelope capture without newline alteration",
                       "overlength author failure propagation", "first answer precedes source delivery",
                       "first answer immutable through recovery", "full-source no-recovery completion",
                       "terminal checkpoints and phase sealing",
                       "per-response validation and decoded first/recovery word counts"])
    with fixture() as (p, clock):
        authors(p, bad_second=True)
        invalid = r.read(r.trial_path("A002"))["messages"][-1]["validation"]
        assert invalid["json_parse_status"] == "FAIL" and invalid["decoded_words"] is None
        r.start("recipients", "DUMMY-SEAL")
        r.begin("Q001"); r.register("Q001", "/dummy/q1")
        r.reply("Q001", capture(p, FIRST))
        r.delivered("Q001")
        assert r.reply("Q001", capture(p, FIRST))["status"] == "RECIPIENT_PROTOCOL_ERROR"
        assert r.read(r.trial_path("Q001"))["first_answer"]["recover"]
        checks.append("second recovery prohibited while first answer preserved")
    with fixture() as (p, clock):
        authors(p)
        r.start("recipients", "DUMMY-SEAL")
        r.begin("Q001"); r.register("Q001", "/dummy/q1")
        r.reply("Q001", capture(p, FIRST))
        r.stop("Q001", "DUMMY source delivery failed")
        t = r.read(r.trial_path("Q001"))
        assert "first_answer" in t and "final_answer" not in t
        assert t["messages"][-1]["delivery"] == "queued" and not t["recovery_served"]
        r.begin("Q002")
        r.stop("Q002", "DUMMY initial delivery failed")
        assert r.read(r.trial_path("Q002"))["visible_input_words"] == 0
        r.close()
        assert r.read(r.trial_path("Q003"))["status"] == "UNRUN"
        checks.extend(["source delivery failure retains first answer", "undelivered prompt excluded from exposure", "undispatched cells remain UNRUN"])
    with fixture() as (p, clock):
        r.start("authors")
        r.begin("A001"); r.register("A001", "/dummy/a1")
        clock[0] += 21
        assert r.reply("A001", capture(p, AUTHOR))["status"] == "BUDGET_STOP"
        assert r.read(r.trial_path("A001"))["messages"][-1]["kind"] == "excluded_late_response"
        denied(r.begin, "A002")
        r.close()
        r.start("recipients", "DUMMY-SEAL")
        assert r.begin("Q001")["status"] == "AUTHOR_UNAVAILABLE"
        checks.extend(["late raw response retained without scoring", "dispatch stops at deadline", "unavailable author propagated distinctly"])
    with fixture() as (p, clock):
        (p / "recipient_common.txt").write_text("CHANGED")
        denied(r.start, "authors")
        checks.append("changed frozen input rejects execution")
    result = {"status": "PASS", "checks": checks, "check_count": len(checks),
              "data": "Temporary DUMMY sources only; none of the six study histories or model outputs used.",
              "model_calls": 0, "limits": "Same-author rehearsal of the local recorder, not provider delivery telemetry."}
    r.write(ROOT / "review/RECORDER_REHEARSAL.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
