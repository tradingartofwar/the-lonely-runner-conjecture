#!/usr/bin/env python3
"""Record mediated fresh-context trials. No inference API and no access to answer keys."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
OUT = HERE / "run"


def stamp():
    return datetime.now(timezone.utc).isoformat()


def read(p):
    return json.loads(Path(p).read_text())


def write(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def schedule():
    return read(HERE / "TRIAL_SCHEDULE.json")["trials"]


def trial_path(tid):
    assert tid in {x["trial_id"] for x in schedule()}, tid
    return OUT / "trials" / (tid + ".json")


def check_freeze():
    for name, sha in read(HERE / "FROZEN_MANIFEST.json")["sha256"].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == sha, name


def init(commit):
    check_freeze()
    assert not (OUT/"STATUS.json").exists(), "Run already exists; never silently restart."
    write(OUT/"STATUS.json", {"status": "RUNNING", "freeze_commit": commit,
          "started_at": stamp(), "started_epoch": time.time(), "deadline_seconds": 3600,
          "next_schedule_index": 0, "provider_model_snapshot": None, "provider_token_usage": None})
    return {"status": "RUNNING", "deadline_seconds": 3600}


def begin(tid):
    check_freeze()
    state = read(OUT/"STATUS.json")
    assert state["status"] == "RUNNING"
    assert time.time()-state["started_epoch"] < state["deadline_seconds"], "Execution budget elapsed."
    expected = schedule()[state["next_schedule_index"]]
    assert expected["trial_id"] == tid, (tid, expected["trial_id"])
    active = [p for p in (OUT/"trials").glob("*.json") if read(p)["status"] == "ACTIVE"] if (OUT/"trials").exists() else []
    assert len(active) < 5, "Maximum five active trial contexts."
    assert not trial_path(tid).exists()
    prompt = read(HERE/"STIMULI.json")[tid]["prompt"]
    trial = {**expected, "status": "ACTIVE", "agent": None, "started_at": stamp(),
             "started_epoch": time.time(), "source_requests": 0,
             "messages": [{"role": "user", "kind": "initial_prompt", "content": prompt, "recorded_at": stamp(), "delivery_state": "queued"}]}
    write(trial_path(tid), trial)
    state["next_schedule_index"] += 1
    write(OUT/"STATUS.json", state)
    return {"trial_id": tid, "prompt": prompt}


def register(tid, agent):
    p = trial_path(tid); trial = read(p)
    assert trial["status"] == "ACTIVE" and trial["agent"] is None
    trial["agent"] = agent
    trial["messages"][0].update(delivery_state="delivered", delivered_at=stamp())
    write(p, trial)
    return {"registered": tid, "agent": agent}


def delivered(tid):
    p=trial_path(tid);trial=read(p)
    message=trial["messages"][-1]
    assert trial["status"] == "ACTIVE" and message["kind"] == "source_response" and message["delivery_state"] == "queued"
    message.update(delivery_state="delivered",delivered_at=stamp())
    write(p,trial)
    return {"trial_id":tid,"source_delivery":"recorded"}


def finish(trial, status, reason=None):
    trial["status"] = status
    trial["ended_at"] = stamp()
    trial["elapsed_seconds"] = time.time()-trial["started_epoch"]
    if reason is not None: trial["stop_reason"] = reason
    trial["visible_input_characters"] = sum(len(x["content"]) for x in trial["messages"] if x["role"] == "user" and x.get("delivery_state") == "delivered")
    trial["visible_output_characters"] = sum(len(x["content"]) for x in trial["messages"] if x["role"] == "assistant")
    trial["visible_input_words"] = sum(len(x["content"].split()) for x in trial["messages"] if x["role"] == "user" and x.get("delivery_state") == "delivered")
    trial["visible_output_words"] = sum(len(x["content"].split()) for x in trial["messages"] if x["role"] == "assistant")
    trial["actual_total_tokens"] = None
    write(trial_path(trial["trial_id"]), trial)
    return {"trial_id": trial["trial_id"], "status": status, "source_requests": trial["source_requests"]}


def reply(tid, raw_path):
    p = trial_path(tid); trial = read(p)
    assert trial["status"] == "ACTIVE"
    raw = Path(raw_path).read_text()
    trial["messages"].append({"role": "assistant", "kind": "respondent_message", "content": raw, "recorded_at": stamp()})
    state = read(OUT/"STATUS.json")
    if time.time()-state["started_epoch"] >= state["deadline_seconds"]:
        trial["messages"][-1]["kind"] = "excluded_late_response"
        return finish(trial, "INFRASTRUCTURE_STOP", "One-hour budget elapsed; late message retained but not scored or continued.")
    body = raw.strip()
    if body.startswith("```json\n") and body.endswith("\n```"):
        body = body[8:-4]
    try:
        obj = json.loads(body)
        assert isinstance(obj, dict)
    except (ValueError, AssertionError):
        return finish(trial, "MODEL_PROTOCOL_ERROR", "Response was not a JSON object.")
    action = obj.get("action")
    if action == "answer":
        if not isinstance(obj.get("answer"), str) or not isinstance(obj.get("evidence"), list):
            return finish(trial, "MODEL_PROTOCOL_ERROR", "Missing answer/evidence fields.")
        trial["final_answer"] = obj
        return finish(trial, "COMPLETED")
    if action != "read" or not isinstance(obj.get("source"), str):
        return finish(trial, "MODEL_PROTOCOL_ERROR", "Unrecognized action or source format.")
    trial["source_requests"] += 1
    if trial["source_requests"] > 2:
        return finish(trial, "MODEL_PROTOCOL_ERROR", "Requested a third source.")
    card = next(c for c in read(HERE/"SOURCE_CARDS.json")["cards"] if c["id"] == trial["card_id"])
    src = next((s for s in card["sources"] if s["alias"] == obj["source"]), None)
    if src is None:
        payload = {"source": obj["source"], "status": "unknown_source", "text": None}
    else:
        payload = {"source": src["alias"], "date": src["date"], "status": "available" if src["available"] else "unavailable", "text": src["text"]}
    followup = "SOURCE_RESPONSE\n" + json.dumps(payload, indent=2, ensure_ascii=False)
    trial["messages"].append({"role": "user", "kind": "source_response", "content": followup, "recorded_at": stamp(), "delivery_state": "queued"})
    write(p, trial)
    return {"trial_id": tid, "status": "NEEDS_FOLLOWUP", "agent": trial["agent"], "followup": followup}


def stop(tid, reason):
    trial = read(trial_path(tid)); assert trial["status"] == "ACTIVE"
    return finish(trial, "INFRASTRUCTURE_STOP", reason)


def close():
    state = read(OUT/"STATUS.json")
    records = []
    for s in schedule():
        p = trial_path(s["trial_id"])
        if p.exists():
            t = read(p)
            assert t["status"] != "ACTIVE", "Close active trials explicitly."
        else:
            t = {**s, "status": "UNRUN", "reason": "Not dispatched before run closure."}
            write(p,t)
        records.append(t)
    counts = {status:sum(r["status"] == status for r in records) for status in sorted({r["status"] for r in records})}
    state.update(status="CLOSED", ended_at=stamp(), elapsed_seconds=time.time()-state["started_epoch"], counts=counts,
                 source_requests=sum(r.get("source_requests",0) for r in records))
    write(OUT/"STATUS.json",state)
    write(OUT/"TRANSCRIPTS.json",records)
    return state


def main():
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["init","begin","register","delivered","reply","stop","close","check"]);p.add_argument("args",nargs="*")
    a=p.parse_args()
    if a.command=="check": check_freeze(); result={"freeze_integrity":"PASS"}
    else: result=globals()[a.command](*a.args)
    print(json.dumps(result,ensure_ascii=False))


if __name__ == "__main__":
    main()
