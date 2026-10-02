#!/usr/bin/env python3
"""Post-collection packaging and arithmetic; semantic grades are supplied separately.

This is not part of the frozen respondent apparatus. It never edits run records.
"""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import random
import statistics

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def closed_run():
    status = read("run/STATUS.json")
    assert status["status"] == "CLOSED", "Do not grade an ongoing collection."
    trials = read("run/TRANSCRIPTS.json")
    assert len(trials) == 80 and len({t["trial_id"] for t in trials}) == 80
    assert all(t["status"] != "ACTIVE" for t in trials)
    for name, sha in read("FROZEN_MANIFEST.json")["sha256"].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == sha, name
    return status, trials


def blind():
    _, trials = closed_run()
    cards = {c["id"]: c for c in read("SOURCE_CARDS.json")["cards"]}
    handoffs = read("HANDOFFS.json")["cards"]
    shuffled = list(trials)
    random.Random(20261001).shuffle(shuffled)
    mapping, packet = {}, []
    for i, t in enumerate(shuffled, 1):
        bid = f"U{i:03d}"
        mapping[bid] = t["trial_id"]
        c = cards[t["card_id"]]
        # The atoms are identical in both arms; sort away the treatment's order.
        atoms = sorted(handoffs[t["card_id"]]["shared_atoms"].values())
        delivered = [m["content"] for m in t.get("messages", [])
                     if m["kind"] == "source_response" and m.get("delivery_state") == "delivered"]
        packet.append({"blind_id": bid, "card_id": t["card_id"],
                       "question": c["query"], "neutral_summary": c["neutral_summary"],
                       "handoff_statements_without_condition_labels": atoms,
                       "actually_delivered_source_responses": delivered,
                       "status": t["status"], "final_answer": t.get("final_answer"),
                       "respondent_messages": [m["content"] for m in t.get("messages", [])
                                               if m["role"] == "assistant"],
                       "stop_reason": t.get("stop_reason")})
    write("BLIND_MAPPING.json", mapping)
    write("BLIND_PACKET.json", {"scope": "Internal condition-masked grading; not human/formal verification.",
          "masking": "Trial IDs, arm names, prompt labels/order, agent paths and primary grades withheld. Shared atoms normalized; source exposure preserved.",
          "instructions": (HERE / "RESPONDENT_INSTRUCTIONS.md").read_text(),
          "rubric": (HERE / "SCORING.md").read_text(), "trials": packet})
    print(json.dumps({"blind_packet_trials": len(packet)}))


def audit():
    state, trials = closed_run()
    cards = {c["id"]: c for c in read("SOURCE_CARDS.json")["cards"]}
    stimuli = read("STIMULI.json")
    invocations = [json.loads(line) for line in (HERE / "run/INVOCATIONS.jsonl").read_text().splitlines()]
    events, exceeded_word_target, raw_count = [], [], 0
    all_agents = []
    for t in trials:
        tid = t["trial_id"]
        assert t == read(f"run/trials/{tid}.json"), tid
        if t["status"] == "UNRUN":
            continue
        assert t["messages"][0]["content"] == stimuli[tid]["prompt"], tid
        seen_sources, requested, output_index = [], 0, 0
        for m in t["messages"]:
            if m["role"] == "assistant":
                output_index += 1
                raw = (HERE / f"run/incoming/{tid}-{output_index:02}.txt").read_text()
                assert raw == m["content"], (tid, output_index, "raw text")
                raw_count += 1
                if len(raw.split()) > 150:
                    exceeded_word_target.append([tid, output_index, len(raw.split())])
                try:
                    b = raw.strip()
                    if b.startswith("```json\n") and b.endswith("\n```"):
                        b = b[8:-4]
                    obj = json.loads(b)
                    if m["kind"] != "excluded_late_response" and isinstance(obj, dict) and obj.get("action") == "read" and isinstance(obj.get("source"), str):
                        requested += 1
                except ValueError:
                    pass
            elif m["kind"] == "source_response":
                payload = json.loads(m["content"].removeprefix("SOURCE_RESPONSE\n"))
                src = next((s for s in cards[t["card_id"]]["sources"] if s["alias"] == payload["source"]), None)
                expected = ({"source": src["alias"], "date": src["date"], "status": "available" if src["available"] else "unavailable", "text": src["text"]}
                            if src else {"source": payload["source"], "status": "unknown_source", "text": None})
                assert payload == expected, (tid, "source content")
                if m.get("delivery_state") == "delivered":
                    seen_sources.append(m["content"])
        assert requested == t["source_requests"], tid
        for role, prefix in [("user", "input"), ("assistant", "output")]:
            texts = [m["content"] for m in t["messages"] if m["role"] == role and (role != "user" or m.get("delivery_state") == "delivered")]
            assert sum(map(len, texts)) == t[f"visible_{prefix}_characters"], (tid, prefix, "characters")
            assert sum(len(x.split()) for x in texts) == t[f"visible_{prefix}_words"], (tid, prefix, "words")
        calls = [v for v in invocations if v["trial_id"] == tid]
        spawn = [v for v in calls if v["operation"] == "spawn_agent"]
        assert len(spawn) == 1 and spawn[0]["fork_turns"] == "none", tid
        all_agents.append(t["agent"])
        assert all(v["model_override"] is None and v["reasoning_override"] is None and v["agent_path"] == t["agent"] and v["elapsed_seconds"] < 3600 for v in calls), tid
        assert spawn[0]["message_sha256"] == stimuli[tid]["sha256"], tid
        followups = [v for v in calls if v["operation"] == "followup_task"]
        assert [v["message_sha256"] for v in followups] == [hashlib.sha256(s.encode()).hexdigest() for s in seen_sources], tid
        if t["status"] == "COMPLETED":
            assert datetime.fromisoformat(t["ended_at"]).timestamp() - state["started_epoch"] < 3600, tid
        assert t["actual_total_tokens"] is None, tid
        events.extend([(t["started_epoch"], 1), (datetime.fromisoformat(t["ended_at"]).timestamp(), -1)])
    assert len(all_agents) == len(set(all_agents))
    active = maximum = 0
    for _, delta in sorted(events):
        active += delta
        maximum = max(maximum, active)
    assert maximum <= 5 and active == 0
    dispatched = [t for t in trials if t["status"] != "UNRUN"]
    assert [t["trial_id"] for t in sorted(dispatched, key=lambda t: t["started_epoch"])] == [t["trial_id"] for t in dispatched]
    assert len(invocations) == len(all_agents) + sum(m["kind"] == "source_response" and m.get("delivery_state") == "delivered" for t in trials for m in t.get("messages", []))
    for cp in sorted((HERE / "checkpoints").glob("*.json")):
        snapshot = json.loads(cp.read_text())
        final = {t["trial_id"]: t for t in trials}
        assert all(t == final[t["trial_id"]] for t in snapshot["trials"]), cp.name
    result = {"status": "PASS", "frozen_hashes": "unchanged", "planned_records": len(trials),
              "unique_respondent_agents": len(all_agents), "recorded_invocations": len(invocations),
              "raw_messages_matched": raw_count, "max_active_trial_contexts": maximum,
              "over_150_word_messages": exceeded_word_target,
              "checks": ["Aggregate and individual records agree", "Recorded initial prompts match frozen stimuli", "Source payloads match frozen cards", "Raw responses and transcript text agree", "Request and visible character/word counts recompute", "Invocation hashes, agents and inherited configuration agree with recorder", "Dispatch order, five-context cap and completed-record deadlines hold", "Published terminal-record checkpoints agree with final records"],
              "limits": "Record consistency audit, not independent provider telemetry, hidden-context inspection, semantic grading or token accounting."}
    write("COLLECTION_AUDIT.json", result)
    print(json.dumps(result, indent=2))


def summarize():
    status, trials = closed_run()
    mapping = read("BLIND_MAPPING.json")
    grades = {mapping[g["blind_id"]]: g for g in read("GRADES.json")["grades"]}
    assert set(grades) == {t["trial_id"] for t in trials}
    for t in trials:
        g = grades[t["trial_id"]]
        if t["status"] in ("INFRASTRUCTURE_STOP", "UNRUN"):
            assert g["primary"] is None
        elif t["status"] == "MODEL_PROTOCOL_ERROR":
            assert g["primary"] == 0
        else:
            assert g["primary"] in (0, 1)
        assert g["unsupported_approval"] in (0, 1, None)

    def tally(ts):
        gs = [grades[t["trial_id"]] for t in ts]
        return {"planned": len(ts), "statuses": dict(Counter(t["status"] for t in ts)),
                "correct": sum(g["primary"] == 1 for g in gs),
                "incorrect": sum(g["primary"] == 0 for g in gs),
                "requested_outputs_correct_diagnostic": sum(g["requested_outputs_correct"] for g in gs),
                "permissive_interpretation_correct_sensitivity": sum(g["permissive_whole_answer_primary"] for g in gs),
                "missing_scores": sum(g["primary"] is None for g in gs),
                "unsupported_approvals": sum(g["unsupported_approval"] == 1 for g in gs),
                "unsupported_approval_missing": sum(g["unsupported_approval"] is None for g in gs),
                "source_requests": sum(t.get("source_requests", 0) for t in ts),
                "median_visible_input_words": statistics.median([t["visible_input_words"] for t in ts if "visible_input_words" in t]) if any("visible_input_words" in t for t in ts) else None,
                "median_visible_output_words": statistics.median([t["visible_output_words"] for t in ts if "visible_output_words" in t]) if any("visible_output_words" in t for t in ts) else None}

    arms = sorted({t["arm"] for t in trials})
    cards = [c["id"] for c in read("SOURCE_CARDS.json")["cards"]]
    result = {"claim_status": "OBSERVED", "freeze_commit": status["freeze_commit"],
              "collection": status, "overall": tally(trials),
              "arms": {a: tally([t for t in trials if t["arm"] == a]) for a in arms},
              "cards": {c: {a: tally([t for t in trials if t["arm"] == a and t["card_id"] == c]) for a in arms} for c in cards},
              "blocks": {str(b): {a: tally([t for t in trials if t["arm"] == a and t["block"] == b]) for a in arms} for b in sorted({t["block"] for t in trials})},
              "adequate_summary_controls": {a: tally([t for t in trials if t["arm"] == a and t["card_id"] in ("S1", "S2")]) for a in arms},
              "actual_total_token_cost": None, "original_cost_effectiveness_gate": "UNASSESSABLE",
              "grading_adjudication": {"record": "ADJUDICATION.md", "initial_primary_correct": 80,
                    "adjudicated_primary_correct": sum(g["primary"] == 1 for g in grades.values()),
                    "revised_blind_ids": read("GRADES.json")["changed_blind_ids"],
                    "scope": "Five M2 explanations add unsupported distinct-policy identity under a strict reading; all requested outputs remain correct. Diagnostic and permissive sensitivity counts do not replace the frozen primary endpoint."},
              "limitations": ["Ten fixed synthetic cards; four repetitions are not eighty independent situations.",
                              "Same information in both arms; only labels, order and grouping differ.",
                              "Instruction-based respondent isolation and inherited model configuration; exact snapshot unknown.",
                              "Visible words/characters are not tokens; elapsed time includes orchestration.",
                              "Internal AI semantic grading, not independent human or formal certification."]}
    write("RESULTS.json", result)
    print(json.dumps({"overall": result["overall"], "arms": result["arms"]}, indent=2))


def manifest():
    status, _ = closed_run()
    paths = [p for p in HERE.rglob("*") if p.is_file() and "__pycache__" not in p.parts
             and p.name != "RESULT_MANIFEST.json"]
    write("RESULT_MANIFEST.json", {"freeze_commit": status["freeze_commit"],
          "scope": "Pilot package at result publication; historical preparation and freeze manifests retained.",
          "sha256": {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}})
    print(json.dumps({"result_files_hashed": len(paths)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["audit", "blind", "summarize", "manifest"])
    args = parser.parse_args()
    globals()[args.command]()
