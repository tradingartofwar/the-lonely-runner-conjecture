#!/usr/bin/env python3
"""Single-writer mediated recorder. No inference calls or semantic answer-key reads."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import materials as m

HERE = Path(__file__).resolve().parent
OUT = HERE / "run"
ACTIVE = {"QUEUED", "ACTIVE", "SOURCE_QUEUED"}


def now():
    return time.time()


def stamp(t=None):
    return datetime.fromtimestamp(now() if t is None else t, timezone.utc).isoformat()


def read(p):
    return json.loads(Path(p).read_text())


def write(p, value, exclusive=False):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("x" if exclusive else "w") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def config():
    return read(HERE / "CONFIG.json")


def check():
    for name, sha in read(HERE / "EXECUTION_MANIFEST.json")["sha256"].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == sha, name
    return {"execution_integrity": "PASS"}


def state():
    return read(OUT / "STATUS.json")


def schedule(phase):
    name = "AUTHOR_INPUTS.json" if phase == "authors" else "RECIPIENT_SCHEDULE.json"
    return read(HERE / "prepared" / name)


def trial_path(tid):
    assert tid in {s["id"] for phase in ("authors", "recipients") for s in schedule(phase)}, tid
    return OUT / "trials" / (tid + ".json")


def records(phase):
    return [read(trial_path(s["id"])) for s in schedule(phase) if trial_path(s["id"]).exists()]


def event(operation, tid=None, **values):
    entry = {"operation": operation, "trial_id": tid, "recorded_at": stamp(), **values}
    with (OUT / "EVENTS.jsonl").open("a") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")


def init(commit):
    check()
    write(OUT / "STATUS.json", {"status": "READY", "freeze_commit": commit,
          "phase": None, "phases": {}, "provider_snapshot": None, "actual_tokens": None}, exclusive=True)
    event("init", freeze_commit=commit)
    return state()


def start(phase, seal_commit=None):
    check()
    s = state()
    assert phase in {"authors", "recipients"} and s["phase"] is None
    assert phase not in s["phases"], "Never restart a phase."
    if phase == "recipients":
        assert s["phases"]["authors"]["status"] == "CLOSED" and seal_commit
        seal = read(OUT / "AUTHORS_SEALED.json")
        for aid, sha in seal["trial_sha256"].items():
            assert hashlib.sha256(trial_path(aid).read_bytes()).hexdigest() == sha
        s["author_seal_commit"] = seal_commit
    limit = config()["author_phase_seconds" if phase == "authors" else "recipient_phase_seconds"]
    s["phases"][phase] = {"status": "RUNNING", "started_epoch": now(),
                          "started_at": stamp(), "limit_seconds": limit, "next_index": 0}
    s.update(status="RUNNING", phase=phase)
    write(OUT / "STATUS.json", s)
    event("start", phase=phase, author_seal_commit=seal_commit)
    return s


def budget():
    s = state()
    phase = s["phase"]
    assert phase is not None
    data = s["phases"][phase]
    return now() - data["started_epoch"] < data["limit_seconds"]


def finish(t, status, reason=None):
    t.update(status=status, ended_at=stamp(), ended_epoch=now())
    if reason is not None:
        t["reason"] = reason
    for role, prefix in (("user", "input"), ("assistant", "output")):
        texts = [x["content"] for x in t["messages"] if x["role"] == role and
                 (role == "assistant" or x.get("delivery") == "delivered")]
        t["visible_" + prefix + "_words"] = sum(len(x.split()) for x in texts)
        t["visible_" + prefix + "_characters"] = sum(map(len, texts))
    t["actual_tokens"] = None
    write(trial_path(t["id"]), t)
    event("finish", t["id"], status=status, reason=reason)
    return {"trial_id": t["id"], "status": status, "first_answer_preserved": "first_answer" in t}


def begin(tid):
    check()
    s = state()
    phase = s["phase"]
    assert phase and budget(), "Phase budget expired or not running."
    order = schedule(phase)
    index = s["phases"][phase]["next_index"]
    assert index < len(order) and order[index]["id"] == tid, "Wrong dispatch order."
    assert sum(t["status"] in ACTIVE for t in records(phase)) < config()["max_active_contexts"]
    assert not trial_path(tid).exists()
    item = order[index]
    t = {k: v for k, v in item.items() if k not in {"prompt", "prompt_sha256", "status"}}
    t.update(phase=phase, freeze_commit=s["freeze_commit"], status="QUEUED", agent=None, started_at=stamp(), started_epoch=now(),
             recovery_requested=False, recovery_served=False, messages=[])
    s["phases"][phase]["next_index"] += 1
    if phase == "authors":
        prompt = item["prompt"]
    else:
        q = read(HERE / "prepared/QUESTION_PROMPTS.json")[item["question"]]
        if item["author"] is not None:
            author = read(trial_path(item["author"]))
            if author["status"] != "COMPLETED":
                write(OUT / "STATUS.json", s)
                reason = author["status"]
                status = "AUTHOR_PROTOCOL_ERROR" if reason == "AUTHOR_PROTOCOL_ERROR" else "AUTHOR_UNAVAILABLE"
                return finish(t, status, reason)
            evidence = m.render_handoff(author["author_raw"])
            mode = "handoff"
        else:
            evidence, mode = m.history(item["history"]), "full_source"
        prompt = m.recipient_prompt(q["query"], mode, evidence)
    t["messages"].append({"role": "user", "kind": "initial", "content": prompt,
                           "delivery": "queued", "recorded_at": stamp(), "sha256": m.digest(prompt)})
    write(trial_path(tid), t, exclusive=True)
    write(OUT / "STATUS.json", s)
    event("begin", tid, prompt_sha256=m.digest(prompt))
    return {"trial_id": tid, "status": "QUEUED", "prompt": prompt}


def register(tid, agent):
    t = read(trial_path(tid))
    assert t["status"] == "QUEUED" and t["agent"] is None
    assert not any(r.get("agent") == agent for p in ("authors", "recipients") for r in records(p))
    t.update(agent=agent, fork_turns="none", model_override=None, reasoning_override=None, status="ACTIVE")
    t["messages"][0].update(delivery="delivered", delivered_at=stamp())
    write(trial_path(tid), t)
    event("spawn_agent", tid, agent=agent, fork_turns="none", model_override=None,
          reasoning_override=None, message_sha256=t["messages"][0]["sha256"])
    return {"registered": tid, "agent": agent}


def delivered(tid):
    t = read(trial_path(tid))
    assert t["status"] == "SOURCE_QUEUED"
    last = t["messages"][-1]
    assert last["kind"] == "source" and last["delivery"] == "queued"
    last.update(delivery="delivered", delivered_at=stamp())
    t.update(status="ACTIVE", recovery_served=True)
    write(trial_path(tid), t)
    event("followup_task", tid, agent=t["agent"], message_sha256=last["sha256"])
    return {"source_delivered": tid}


def diagnostics(raw, phase):
    """Record parse status and decoded cap units, even for a schema/cap error."""
    try:
        obj = m.decode(raw)
    except ValueError as exc:
        return {"json_parse_status": "FAIL", "decoded_words": None, "parse_error": str(exc)}
    words = None
    if isinstance(obj, dict):
        keys = ["status", "evidence", "next"] if phase == "authors" else ["answer"]
        if all(isinstance(obj.get(key), str) for key in keys):
            words = sum(len(obj[key].split()) for key in keys)
    return {"json_parse_status": "PASS", "decoded_words": words}


def reply(tid, envelope_path):
    t = read(trial_path(tid))
    assert t["status"] == "ACTIVE"
    # Capture the exact final-message string inside a JSON envelope. The envelope's
    # own trailing newline is not part of the response and never needs trimming.
    envelope = read(envelope_path)
    assert set(envelope) == {"raw_text"} and isinstance(envelope["raw_text"], str)
    raw = envelope["raw_text"]
    number = 1 + sum(x["role"] == "assistant" for x in t["messages"])
    incoming = OUT / "incoming" / f"{tid}-{number:02}.json"
    write(incoming, envelope, exclusive=True)
    t["messages"].append({"role": "assistant", "kind": "response", "content": raw,
                          "recorded_at": stamp(), "raw_file": str(incoming.relative_to(OUT)),
                          "sha256": m.digest(raw), "validation": diagnostics(raw, t["phase"])})
    validation = t["messages"][-1]["validation"]
    if not budget():
        t["messages"][-1]["kind"] = "excluded_late_response"
        validation.update(schema_and_cap_status="NOT_ASSESSED_LATE", error="Phase deadline expired.")
        return finish(t, "BUDGET_STOP", "Recorded after phase deadline; raw response retained.")
    try:
        if t["phase"] == "authors":
            parsed = m.validate_author(raw)
            validation.update(schema_and_cap_status="PASS", mode="author", error=None)
            t.update(author_raw=raw, author_object=parsed["object"], handoff_words=parsed["words"],
                     rendered_handoff=m.render_handoff(raw))
            return finish(t, "COMPLETED")
        mode = "recovery" if t["recovery_served"] else ("full_source" if t["author"] is None else "handoff")
        parsed = m.validate_recipient(raw, mode)
    except (ValueError, TypeError) as exc:
        validation.update(schema_and_cap_status="FAIL", error=str(exc))
        status = "AUTHOR_PROTOCOL_ERROR" if t["phase"] == "authors" else "RECIPIENT_PROTOCOL_ERROR"
        return finish(t, status, str(exc))
    validation.update(schema_and_cap_status="PASS", mode=mode, error=None)
    answer = parsed["object"]
    if not t["recovery_served"]:
        t["first_answer"] = answer
        t["first_answer_recorded_at"] = stamp()
        t["recovery_requested"] = answer["recover"]
    if answer["recover"]:
        followup = m.recovery_prompt(t["history"])
        t["messages"].append({"role": "user", "kind": "source", "content": followup,
                              "delivery": "queued", "recorded_at": stamp(), "sha256": m.digest(followup)})
        t["status"] = "SOURCE_QUEUED"
        write(trial_path(tid), t)
        event("recovery_queued", tid, message_sha256=m.digest(followup))
        return {"trial_id": tid, "status": "SOURCE_QUEUED", "agent": t["agent"], "followup": followup}
    t["final_answer"] = answer
    return finish(t, "COMPLETED")


def stop(tid, reason):
    t = read(trial_path(tid))
    assert t["status"] in ACTIVE
    return finish(t, "INFRASTRUCTURE_STOP", reason)


def close():
    s = state()
    phase = s["phase"]
    assert phase is not None
    assert not any(t["status"] in ACTIVE for t in records(phase)), "Stop active contexts explicitly."
    for item in schedule(phase):
        if not trial_path(item["id"]).exists():
            t = {k: v for k, v in item.items() if k not in {"prompt", "prompt_sha256", "status"}}
            t.update(phase=phase, freeze_commit=s["freeze_commit"], status="UNRUN", messages=[],
                     reason="Not dispatched before closure.")
            write(trial_path(item["id"]), t, exclusive=True)
    recs = records(phase)
    counts = {key: sum(t["status"] == key for t in recs) for key in sorted({t["status"] for t in recs})}
    s["phases"][phase].update(status="CLOSED", ended_at=stamp(), elapsed_seconds=now()-s["phases"][phase]["started_epoch"], counts=counts)
    s.update(phase=None, status="AUTHORS_CLOSED" if phase == "authors" else "CLOSED")
    write(OUT / "STATUS.json", s)
    write(OUT / (phase.upper() + "_TRANSCRIPTS.json"), recs, exclusive=True)
    if phase == "authors":
        write(OUT / "AUTHORS_SEALED.json", {"freeze_commit": s["freeze_commit"], "counts": counts,
              "trial_sha256": {t["id"]: hashlib.sha256(trial_path(t["id"]).read_bytes()).hexdigest() for t in recs}}, exclusive=True)
    event("close", phase=phase, counts=counts)
    return s


def checkpoint(label):
    s = state()
    phase = s["phase"]
    assert phase
    terminal = [t for t in records(phase) if t["status"] not in ACTIVE]
    path = OUT / "checkpoints" / f"{phase}-{label}.json"
    write(path, {"phase": phase, "terminal_records": terminal, "status": s}, exclusive=True)
    return {"checkpoint": str(path), "terminal_records": len(terminal)}


def status():
    s = state()
    result = {"state": s}
    if s["phase"]:
        result["active"] = [{"id": r["id"], "agent": r.get("agent"), "status": r["status"]}
                            for r in records(s["phase"]) if r["status"] in ACTIVE]
        result["terminal"] = sum(r["status"] not in ACTIVE for r in records(s["phase"]))
        result["remaining_seconds"] = s["phases"][s["phase"]]["limit_seconds"] - (now()-s["phases"][s["phase"]]["started_epoch"])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["check", "init", "start", "begin", "register", "reply",
                                           "delivered", "stop", "close", "checkpoint", "status"])
    parser.add_argument("args", nargs="*")
    args = parser.parse_args()
    print(json.dumps(globals()[args.command](*args.args), ensure_ascii=False))
