#!/usr/bin/env python3
"""Prepare the fixed ten-card pilot. No model invocation or experimental answers."""
from pathlib import Path
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent
BASELINE = "bbdf1b7c3f699eda46e4cd4bc9aac9a7a486a970"


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def source(alias, text, available=True, date="day1"):
    return {"alias": alias, "date": date, "available": available, "text": text}


def card(cid, summary, query, sources, data):
    return {"id": cid, "neutral_summary": summary, "query": query,
            "sources": sources, "structured_source": data}


def make_cards():
    cards = []
    build_summary = "Security and performance have each passed on a build."
    build_query = "Is one build eligible, requiring both?"
    for cid, rows, text in [
        ("K1", {"A": [True, False], "B": [False, True]},
         "Build A: security PASS, performance FAIL. Build B: security FAIL, performance PASS."),
        ("K2", {"A": [True, True], "B": [False, False]},
         "Build A: security PASS, performance PASS. Build B: security FAIL, performance FAIL."),
    ]:
        cards.append(card(cid, build_summary, build_query, [source("record-v1", text)],
                          {"kind": "build", "checks": ["security", "performance"], "rows": rows}))
    time_summary = "Each resource has two units of availability."
    time_query = "Is an instantaneous shared event possible, and is a positive-duration joint task possible?"
    for cid, right_closed, text in [
        ("T1", True, "Resource A available [2,4]; B available [4,6]; endpoints included."),
        ("T2", False, "Resource A available [2,4); B available [4,6]. Square brackets include the endpoint; parentheses exclude it."),
    ]:
        cards.append(card(cid, time_summary, time_query, [source("record-v1", text)],
                          {"kind": "interval", "intervals": [[2, 4, True, right_closed], [4, 6, True, True]], "dwell": None}))
    policy_summary = "Source class covers all16 cases; training-selected policy covered all training."
    policy_query = "Did unchanged P pass held-out validation?"
    for cid, failure, untested, text in [
        ("M1", [16], [], "Frozen policy P covers TRAIN cases1–8 and HOLDOUT cases9–15; misses16. The full source policy class contains a policy covering case16. Search ended normally."),
        ("M2", [], [16], "Frozen policy P covers TRAIN cases1–8 and HOLDOUT cases9–15. HOLDOUT evaluation stopped at a fixed budget after cases9–15; case16 was not evaluated. The full source policy class contains a policy covering case16."),
    ]:
        cards.append(card(cid, policy_summary, policy_query, [source("record-v1", text)],
                          {"kind": "validation", "train": list(range(1, 9)), "holdout": list(range(9, 17)),
                           "passes": list(range(9, 16)), "failures": failure, "untested": untested,
                           "policy": "P", "class_covers_all": True}))
    version_summary = "The day1 report found no failures in tested cases."
    version_query = "Does current recorded evidence contain a failure?"
    for cid, available in [("V1", True), ("V2", False)]:
        later_text = ("Source v2, dated day2: case7 fails; first six unchanged."
                      if available else None)
        cards.append(card(cid, version_summary, version_query,
                          [source("record-v1", "Source v1, dated day1: tested cases1–6, no failure observed."),
                           source("record-v2", later_text, available, "day2")],
                          {"kind": "version", "v1_cases": list(range(1, 7)), "v1_failures": [],
                           "v2_exists": True, "v2_available": available,
                           "v2_failures": [7] if available else None}))
    cards.append(card("S1", "Build C has passed both security and performance.",
                      "Is some build eligible, requiring both?",
                      [source("record-v1", "Build C: security PASS, performance PASS. Build D: security FAIL, performance FAIL.")],
                      {"kind": "build", "checks": ["security", "performance"], "rows": {"C": [True, True], "D": [False, False]}}))
    cards.append(card("S2", "Both resources are available throughout [2,6], including endpoints.",
                      "Is a shared task of duration1 possible?",
                      [source("record-v1", "Resource A available [2,6]; B available [2,6]; endpoints included.")],
                      {"kind": "interval", "intervals": [[2, 6, True, True], [2, 6, True, True]], "dwell": 1}))
    return cards


def main():
    cards = make_cards()
    write("SOURCE_CARDS.json", {
        "status": "FIXED_SOURCE_CARDS_AWAITING_INDEPENDENT_ORACLE_REVIEW",
        "source_commit": BASELINE,
        "source_path": "reviews/2026-09-30-ultra-transfer-value/information_transfer.md",
        "scope": "Synthetic operations examples only; no private business or personal records.",
        "expansion_notes": [
            "Same-query references are expanded to the identical question text.",
            "M2 replaces the M1 miss with an untested case; it does not inherit a failure at16.",
            "V2 has no hidden later report content: unavailable remains unspecified.",
            "T2 notation is explained without changing endpoint membership.",
            "Source aliases and synthetic dates are presentation metadata, not outcomes.",
        ],
        "cards": cards,
    })
    answer_key = {
        "K1": {"decision": "no", "eligible_builds": []},
        "K2": {"decision": "yes", "eligible_builds": ["A"]},
        "T1": {"instant": "yes", "instant_witness": "4", "positive_duration": "no"},
        "T2": {"instant": "no", "positive_duration": "no"},
        "M1": {"decision": "fail", "passed": 7, "failed": 1, "untested": 0, "failing_case": 16},
        "M2": {"decision": "unresolved", "passed": 7, "failed": 0, "untested": 1, "untested_case": 16},
        "V1": {"decision": "yes", "version": "v2", "failing_case": 7},
        "V2": {"decision": "unknown", "reason": "Latest report unavailable; no failure established in available v1."},
        "S1": {"decision": "yes", "eligible_builds": ["C"]},
        "S2": {"decision": "yes", "example_task": ["2", "3"], "other_valid_witnesses_allowed": True},
    }
    write("ANSWER_KEY_DRAFT.json", {"status": "PROPOSED_ORACLE_NOT_INDEPENDENTLY_REVIEWED", "answers": answer_key})
    trials = []
    for block, seed in enumerate([20261001, 20261002, 20261003, 20261004], 1):
        order = [(c["id"], arm) for c in cards for arm in ["conventional", "cc_informed"]]
        random.Random(seed).shuffle(order)
        for position, (cid, arm) in enumerate(order, 1):
            trials.append({"trial_id": f"R{len(trials)+1:03d}", "block": block, "order": position,
                           "seed": seed, "card_id": cid, "arm": arm, "status": "UNRUN"})
    write("TRIAL_SCHEDULE.json", {"status": "ORDER_FIXED_NOT_EXECUTED", "trials": trials})
    paths = ["SOURCE_CARDS.json", "ANSWER_KEY_DRAFT.json", "TRIAL_SCHEDULE.json"]
    write("MATERIAL_PINS.json", {"scope": "Stage1 cards, proposed oracle and order only; not an execution freeze.",
                                "sha256": {p: hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in paths}})


if __name__ == "__main__":
    main()
