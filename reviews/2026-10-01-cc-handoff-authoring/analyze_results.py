#!/usr/bin/env python3
"""Reproduce the stored-record audit and descriptive aggregation after closure.

Semantic grades are review artifacts, not inferred by this script.
"""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import random
import subprocess
import materials as m
import run_support as r

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(name):
    return json.loads((HERE / name).read_text())


def write(name, obj):
    path = HERE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def epoch(value):
    return datetime.fromisoformat(value).timestamp()


def audit_abort():
    """Check this zero-delivery closeout without inventing a completed reader phase."""
    r.check()
    state = read("run/STATUS.json")
    closeout = read("run/CLOSEOUT.json")
    assert state["status"] == "AUTHORS_CLOSED" and state["phase"] is None
    assert "recipients" not in state["phases"]
    assert closeout["status"] == "ABORTED_BEFORE_PARTICIPANT_DELIVERY"
    authors = r.records("authors")
    assert len(authors) == 12 and not r.records("recipients")
    assert Counter(t["status"] for t in authors) == {"INFRASTRUCTURE_STOP": 1, "UNRUN": 11}
    assert read("run/AUTHORS_TRANSCRIPTS.json") == authors
    seal = read("run/AUTHORS_SEALED.json")
    for t in authors:
        assert t["freeze_commit"] == state["freeze_commit"]
        assert t.get("agent") is None and "author_raw" not in t
        assert all(x["role"] == "user" and x["delivery"] == "queued" for x in t["messages"])
        path = r.trial_path(t["id"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == seal["trial_sha256"][t["id"]]
    queued = authors[0]["messages"]
    assert len(queued) == 1 and queued[0]["content"] == r.schedule("authors")[0]["prompt"]
    assert m.digest(queued[0]["content"]) == queued[0]["sha256"]
    assert not list((HERE / "run/incoming").glob("*.json"))
    events = [json.loads(x) for x in (HERE / "run/EVENTS.jsonl").read_text().splitlines()]
    assert not any(x["operation"] in {"spawn_agent", "followup_task"} for x in events)
    deviations = [json.loads(x) for x in (HERE / "run/DEVIATIONS.jsonl").read_text().splitlines()]
    assert deviations[0]["raw_message"] == "agent_name must use only lowercase letters, digits, and underscores"
    result = {
        "status": "PASS_ZERO_DELIVERY_CLOSEOUT",
        "frozen_input_files": len(read("EXECUTION_MANIFEST.json")["sha256"]),
        "author_records": 12, "confirmed_participant_deliveries": 0, "raw_responses": 0,
        "author_statuses": dict(Counter(t["status"] for t in authors)),
        "reader_phase_started": False, "reader_control_cells_unrun": 54,
        "deviation_records": len(deviations), "freeze_commit": state["freeze_commit"],
        "comparison_result": None,
        "limits": "Stored-record audit and coordinator recovery report, not independent provider telemetry. The elapsed pause after the rejected launch has no established cause."
    }
    write("AUDIT.json", result)
    print(json.dumps(result, indent=2))


def audit():
    r.check()
    state = read("run/STATUS.json")
    assert state["status"] == "CLOSED"
    schedules = {p: r.schedule(p) for p in ("authors", "recipients")}
    trials = {x["id"]: read(f"run/trials/{x['id']}.json") for p in schedules for x in schedules[p]}
    identities, raw_count, recoveries = [], 0, 0
    for phase, schedule in schedules.items():
        assert read(f"run/{phase.upper()}_TRANSCRIPTS.json") == [trials[x["id"]] for x in schedule]
        clock = state["phases"][phase]
        deadline = clock["started_epoch"] + clock["limit_seconds"]
        assert dict(Counter(trials[x["id"]]["status"] for x in schedule)) == clock["counts"]
        for item in schedule:
            t = trials[item["id"]]
            assert t["freeze_commit"] == state["freeze_commit"]
            for key in ("history", "method"):
                assert t[key] == item[key]
            if phase == "recipients":
                assert t["question"] == item["question"] and t["author"] == item["author"]
            messages = t["messages"]
            if not messages:
                assert t["status"] in {"UNRUN", "AUTHOR_PROTOCOL_ERROR", "AUTHOR_UNAVAILABLE"}
                continue
            assert t["started_epoch"] >= clock["started_epoch"]
            assert t["started_epoch"] < deadline
            if phase == "authors":
                expected = item["prompt"]
            else:
                query = read("prepared/QUESTION_PROMPTS.json")[item["question"]]["query"]
                evidence = (m.history(item["history"]) if item["author"] is None
                            else m.render_handoff(trials[item["author"]]["author_raw"]))
                expected = m.recipient_prompt(query, "full_source" if item["author"] is None else "handoff", evidence)
            assert messages[0]["content"] == expected
            if t.get("agent"):
                identities.append(t["agent"])
                assert t["fork_turns"] == "none" and t["model_override"] is None and t["reasoning_override"] is None
            for msg in messages:
                assert m.digest(msg["content"]) == msg["sha256"]
                if msg["role"] == "user":
                    if msg.get("delivery") == "delivered":
                        assert epoch(msg["delivered_at"]) < deadline
                    if msg["kind"] == "source":
                        assert msg["content"] == m.recovery_prompt(item["history"])
                        assert t["first_answer"]["recover"]
                        assert epoch(t["first_answer_recorded_at"]) <= epoch(msg["recorded_at"])
                        if msg.get("delivery") == "delivered":
                            assert epoch(t["first_answer_recorded_at"]) <= epoch(msg["delivered_at"])
                            recoveries += 1
                else:
                    raw_count += 1
                    envelope = read("run/" + msg["raw_file"])
                    assert envelope == {"raw_text": msg["content"]}
                    diagnostic = r.diagnostics(msg["content"], phase)
                    assert all(msg["validation"][k] == v for k, v in diagnostic.items())
                    if msg["validation"]["schema_and_cap_status"] == "PASS":
                        parsed = (m.validate_author(msg["content"]) if phase == "authors"
                                  else m.validate_recipient(msg["content"], msg["validation"]["mode"]))
                        assert parsed["words"] == msg["validation"]["decoded_words"]
            replies = [x for x in messages if x["role"] == "assistant"]
            if "first_answer" in t:
                assert m.decode(replies[0]["content"]) == t["first_answer"]
            if "final_answer" in t:
                assert m.decode(replies[-1]["content"]) == t["final_answer"]
                if not t["recovery_requested"]:
                    assert t["final_answer"] == t["first_answer"]
            if t["recovery_served"]:
                assert t["recovery_requested"] and len(messages) >= 3
            if phase == "authors" and t["status"] == "COMPLETED":
                assert t["author_raw"] == replies[0]["content"]
                assert t["author_object"] == m.decode(t["author_raw"])
                assert t["rendered_handoff"] == m.render_handoff(t["author_raw"])
                assert t["handoff_words"] == m.validate_author(t["author_raw"])["words"]
            if t["status"] == "COMPLETED":
                assert t["ended_epoch"] < deadline
            for role, prefix in (("user", "input"), ("assistant", "output")):
                texts = [x["content"] for x in messages if x["role"] == role and
                         (role == "assistant" or x.get("delivery") == "delivered")]
                assert t["visible_" + prefix + "_words"] == sum(len(x.split()) for x in texts)
                assert t["visible_" + prefix + "_characters"] == sum(map(len, texts))
    assert len(identities) == len(set(identities))
    seal = read("run/AUTHORS_SEALED.json")
    for aid, sha in seal["trial_sha256"].items():
        path = HERE / "run/trials" / (aid + ".json")
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
        rel = path.relative_to(ROOT)
        published = subprocess.check_output(["git", "show", state["author_seal_commit"] + ":" + str(rel)], cwd=ROOT)
        assert published == path.read_bytes()
    events = [json.loads(line) for line in (HERE / "run/EVENTS.jsonl").read_text().splitlines()]
    active, maximum, dispatch = set(), 0, []
    for event in events:
        tid, op = event["trial_id"], event["operation"]
        if op == "begin":
            active.add(tid); dispatch.append(tid)
            maximum = max(maximum, len(active))
        if op == "finish":
            active.discard(tid)
    assert maximum <= read("CONFIG.json")["max_active_contexts"] and not active
    expected_dispatch = [x["id"] for p in schedules for x in schedules[p] if trials[x["id"]]["messages"]]
    assert dispatch == expected_dispatch
    checkpoint_counts = {}
    for path in sorted((HERE / "run/checkpoints").glob("*.json")):
        data = json.loads(path.read_text())
        for t in data["terminal_records"]:
            assert t == trials[t["id"]]
        checkpoint_counts[path.name] = len(data["terminal_records"])
    deviations = []
    if (HERE / "run/DEVIATIONS.jsonl").exists():
        deviations = [json.loads(x) for x in (HERE / "run/DEVIATIONS.jsonl").read_text().splitlines()]
    result = {
        "status": "PASS", "frozen_input_files": len(read("EXECUTION_MANIFEST.json")["sha256"]),
        "trial_records": len(trials), "unique_participant_identities": len(identities),
        "raw_responses": raw_count, "source_followups_delivered": recoveries,
        "maximum_recorded_active": maximum, "checkpoints": checkpoint_counts,
        "freeze_commit": state["freeze_commit"], "author_seal_commit": state["author_seal_commit"],
        "phases": state["phases"], "deviation_records": len(deviations),
        "checks": ["frozen hashes", "individual/aggregate equality", "scheduled exact prompts",
                   "exact raw envelope equality and hashes", "decoded validation counts",
                   "first-answer preservation before source delivery", "final-answer consistency",
                   "unique fresh-context declarations", "phase deadlines", "fixed dispatch order",
                   "checkpoint equality", "sealed author bytes equal published commit",
                   "visible length arithmetic"],
        "limits": "Stored-record audit, not independent provider telemetry, semantic certification, or proof of inaccessible evaluator files."
    }
    write("AUDIT.json", result)
    print(json.dumps({k: v for k, v in result.items() if k not in {"phases", "checks"}}, indent=2))


def mask():
    assert read("run/STATUS.json")["status"] == "CLOSED"
    out = HERE / "grading"
    assert not (out / "MASKED_PACKET.json").exists(), "Never replace a grading packet."
    trials = r.records("recipients")
    authors = {t["id"]: t for t in r.records("authors")}
    rng = random.Random(2026100137)
    shuffled = list(authors); rng.shuffle(shuffled)
    author_ids = {aid: f"S{i:02}" for i, aid in enumerate(shuffled, 1)}
    rng.shuffle(trials)
    rows, mapping = [], {}
    questions = read("prepared/QUESTION_PROMPTS.json")
    for i, t in enumerate(trials, 1):
        mid = f"R{i:03}"
        mapping[mid] = {"trial": t["id"], "method": t["method"], "history": t["history"], "question": t["question"]}
        rows.append({
            "id": mid, "summary_id": author_ids.get(t["author"]), "history": t["history"],
            "question": t["question"], "query": questions[t["question"]]["query"],
            "status": t["status"], "evidence_mode": "full_source" if t["author"] is None else "handoff",
            "delivered_evidence": (m.history(t["history"]) if t["author"] is None
                                   else authors[t["author"]].get("rendered_handoff")),
            "first_answer": t.get("first_answer"), "final_answer": t.get("final_answer"),
            "recovery_requested": t["recovery_requested"], "recovery_served": t["recovery_served"],
            "source_followup": next((x["content"] for x in t["messages"] if x["kind"] == "source" and
                                     x.get("delivery") == "delivered"), None),
            "response_validation": [x.get("validation") for x in t["messages"] if x["role"] == "assistant"]
        })
    summaries = [{"id": author_ids[aid], "history": authors[aid]["history"],
                  "status": authors[aid]["status"], "handoff": authors[aid].get("rendered_handoff")}
                 for aid in shuffled]
    write("grading/MASKED_PACKET.json", {"limits": "Condition labels and agent/trial identities removed; prose style may reveal method.",
                                       "summaries": summaries, "answers": rows})
    write("grading/PRIVATE_MASK_MAP.json", {"answers": mapping, "summaries": {author_ids[a]: a for a in shuffled}})
    print(json.dumps({"masked_summaries": len(summaries), "masked_answers": len(rows)}))


def summarize():
    packet = read("grading/MASKED_PACKET.json")
    grades = read("grading/FINAL_GRADES.json")["grades"]
    mapping = read("grading/PRIVATE_MASK_MAP.json")["answers"]
    assert len(grades) == 2 * len(packet["answers"])
    assert len({(g["id"], g["stage"]) for g in grades}) == len(grades)
    flags = ["requested_outputs_correct", "supported_by_exposure", "source_faithful", "primary",
             "unsupported_assertion", "unsupported_approval"]
    for g in grades:
        for f in flags:
            assert g[f] in (0, 1, None), (g["id"], f)
        if g["primary"] is not None:
            assert g["primary"] == int(all(g[f] == 1 for f in flags[:3]) and g["protocol_valid"])
    def group(method, stage, history=None, category=None):
        gs = [g for g in grades if mapping[g["id"]]["method"] == method and g["stage"] == stage
              and (history is None or mapping[g["id"]]["history"] == history)
              and (category is None or mapping[g["id"]]["question"].endswith(category))]
        return {"planned": len(gs), "observed": sum(g["primary"] is not None for g in gs),
                **{f: sum(g[f] == 1 for g in gs) for f in flags},
                "abstention": dict(Counter(g["abstention"] for g in gs))}
    methods = ["cc", "conventional", "full_source"]
    recs = r.records("recipients")
    report = {
        "by_method": {method: {stage: group(method, stage) for stage in ["first", "final"]} for method in methods},
        "by_history": {f"H{i:02}": {method: {stage: group(method, stage, f"H{i:02}") for stage in ["first", "final"]}
                                   for method in methods} for i in range(1, 7)},
        "by_question_type": {cat: {method: group(method, "first", category=f"Q{i}") for method in methods}
                             for i, cat in enumerate(["current_decision", "evidence_scope", "changed_use"], 1)},
        "recovery": {method: {"requested": sum(t["recovery_requested"] for t in recs if t["method"] == method),
                              "served": sum(t["recovery_served"] for t in recs if t["method"] == method)}
                     for method in methods},
        "statuses": {method: dict(Counter(t["status"] for t in recs if t["method"] == method)) for method in methods},
        "author_words": {t["id"]: t.get("handoff_words") for t in r.records("authors")},
        "actual_token_usage": None, "inferential_test": None,
        "limits": "Six paired synthetic history clusters; one author realization each; repeated questions are correlated; descriptive counts only."
    }
    report["paired_first_primary_differences_cc_minus_conventional"] = {
        h: v["cc"]["first"]["primary"] - v["conventional"]["first"]["primary"]
        for h, v in report["by_history"].items()}
    write("AGGREGATE.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["audit", "audit_abort", "mask", "summarize"])
    args = parser.parse_args()
    globals()[args.command]()
