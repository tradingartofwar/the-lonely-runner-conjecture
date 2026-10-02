#!/usr/bin/env python3
"""Same-author structural/arithmetic preflight, not semantic review or model trial."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
import re

import materials as m


def arithmetic():
    computed = {}
    # Explicit scenario primitives transcribed from histories; source alignment needs review.
    assert F(119, 120) >= F(99, 100)
    assert F(198, 200) == F(99, 100)
    units = {"A": (8, None, None, False, F(9)),
             "B": (8, F(119, 120), F(6), True, F("7.5")),
             "C": (8, F(198, 200), F(7), True, F(8))}
    def eligible(values):
        version, packets, latency, buffer, runtime = values
        return (version == 8 and packets is not None and packets >= F(99, 100)
                and latency is not None and latency <= 7 and buffer and runtime >= 8)
    assert {u for u, values in units.items() if eligible(values)} == {"C"}
    computed["H01-Q1"] = {"eligible_count": sum(eligible(v) for v in units.values())}
    units["B"] = (*units["B"][:-1], F("8.5"))
    assert {u for u, values in units.items() if eligible(values)} == {"B", "C"}
    computed["H01-Q3"] = {"eligible_count": sum(eligible(v) for v in units.values())}
    samples = {"S": (F(100), F(104)), "T": (F("100.5"), F("104.5")),
               "U": (F(102), F(108))}
    delays = {k: gateway - 3 - acquired for k, (acquired, gateway) in samples.items()}
    assert {k for k, d in delays.items() if d > 2} == {"U"}
    computed["H02-Q1"] = {"unique_samples": len(samples), "late_samples": sum(d > 2 for d in delays.values())}
    computed["H02-Q2"] = {"S_arrival": str(samples["S"][1] - 3), "T_arrival": str(samples["T"][1] - 3)}
    computed["H02-Q3"] = {k + "_delay_interval": [int(g - a - 4), int(g - a - 2)]
                           for k, (a, g) in samples.items()}
    cohort = {f"A{i}" for i in range(1, 9)} | {f"B{i}" for i in range(1, 5)}
    passed = {f"A{i}" for i in range(1, 8)} | {"B1", "B2"}
    failed, untested = {"A8", "B3"}, {"B4"}
    assert passed | failed | untested == cohort
    assert not (passed & failed or passed & untested or failed & untested)
    computed["H03-Q1"] = {"passes": len(passed), "failures": len(failed), "untested": len(untested), "cohort": len(cohort)}
    computed["H03-Q2"] = {"observed_pass_fraction": str(F(len(passed), len(passed | failed))),
                           "cohort_pass_fraction": str(F(len(passed), len(cohort)))}
    computed["H03-Q3"] = {"passes": 1, "failures": 0, "untested": len(cohort - {"B3"})}
    current = {i: 1 for i in range(1, 98)}
    current[12] = 2
    verified = {i: 1 for i in range(1, 95)}
    count = lambda: sum(verified.get(i) == revision for i, revision in current.items())
    computed["H04-Q1"] = {"current_keys": len(current), "verified_current": count()}
    computed["H04-Q2"] = {"distinct_backup_objects": len(set(["object-amber", "object-amber"]))}
    verified.update({95: 1, 96: 1})
    computed["H04-Q3"] = {"verified_current": count(), "current_keys": len(current)}
    jobs = {"A": ([4, 6, 4], 8), "B": ([5, 5, 5], 10), "C": ([3, 4, 3], 6)}
    pairs = {a+b: ([x+y for x, y in zip(jobs[a][0], jobs[b][0])], jobs[a][1]+jobs[b][1])
             for a, b in combinations(jobs, 2)}
    feasible = lambda caps: {k: v for k, v in pairs.items() if all(x <= cap for x, cap in zip(v[0], caps))}
    assert set(feasible([8, 9, 8])) == {"BC"}
    computed["H05-Q1"] = {"output": pairs["BC"][1], "resources": pairs["BC"][0]}
    computed["H05-Q2"] = {"pair_resources": pairs["AB"][0], "new_caps": [10, 9, 8]}
    assert {k for k in feasible([8, 10, 8]) if "A" in k} == {"AC"}
    computed["H05-Q3"] = {"output": pairs["AC"][1], "resources": pairs["AC"][0], "caps": [8, 10, 8]}
    spare = min(24, 24, 2 * 12) - 22
    computed["H06-Q2"] = {"room_spare": 24-22, "kit_spare": 24-22, "leader_spare": 2*12-22, "overall_spare": spare}
    computed["H06-Q3"] = {"new_participants": 22 + 2}
    keys = {q["id"]: q["numbers"] for q in m.load("evaluator/QUESTIONS_AND_KEY.json")["questions"] if "numbers" in q}
    assert computed == keys, (computed, keys)
    return len(computed)


def reject(fn, *args):
    try:
        fn(*args)
    except (ValueError, TypeError):
        return
    raise AssertionError("invalid dummy response was accepted")


def main():
    cfg = m.load("CONFIG.json")
    questions = m.load("evaluator/QUESTIONS_AND_KEY.json")["questions"]
    authors = m.load("prepared/AUTHOR_INPUTS.json")
    readers = m.load("prepared/RECIPIENT_SCHEDULE.json")
    catalogue = m.load("prepared/QUESTION_PROMPTS.json")
    assert len(questions) == 18 and len({q["id"] for q in questions}) == 18
    counts, source_ids = {}, {}
    for i in range(1, 7):
        hid = f"H{i:02}"
        text = m.history(hid)
        counts[hid] = len(text.split())
        assert 1100 <= counts[hid] <= 1400, (hid, counts[hid])
        ids = re.findall(r"^## ([A-Z]\d{2}) — Day (\d+),", text, flags=re.M)
        assert len(ids) == 12 and [int(day) for _, day in ids] == list(range(1, 13))
        assert len({event for event, _ in ids}) == 12
        source_ids[hid] = {event for event, _ in ids}
        assert {q["kind"] for q in questions if q["history"] == hid} == {"current_decision", "evidence_scope", "changed_use"}
    for q in questions:
        assert set(q["evidence"]) <= source_ids[q["history"]], q["id"]
        assert q["required"] and q["unsupported_traps"]
        assert catalogue[q["id"]] == {"history": q["history"], "query": q["query"]}
    method_counts = {k: len(m.read(f"method_{k}.txt").split()) for k in ["cc", "conventional"]}
    assert len(set(method_counts.values())) == 1, method_counts
    assert len(authors) == 12 and len({a["id"] for a in authors}) == 12
    assert Counter(a["method"] for a in authors) == {"cc": 6, "conventional": 6}
    assert {(a["history"], a["method"]) for a in authors} == {(h, method) for h in counts for method in method_counts}
    first = {}
    for a in authors:
        assert a["status"] == "UNRUN"
        assert a["prompt"] == m.author_prompt(a["history"], a["method"])
        assert m.digest(a["prompt"]) == a["prompt_sha256"]
        assert not any(q["query"] in a["prompt"] for q in questions)
        assert "QUESTIONS_AND_KEY" not in a["prompt"]
        assert a["prompt"].count(m.history(a["history"])) == 1
        first.setdefault(a["history"], a["method"])
    assert Counter(first.values()) == {"cc": 3, "conventional": 3}
    assert len(readers) == 54 and len({r["id"] for r in readers}) == 54
    assert Counter(r["method"] for r in readers) == {"cc": 18, "conventional": 18, "full_source": 18}
    assert {(r["question"], r["method"]) for r in readers} == {(q["id"], arm) for q in questions for arm in ["cc", "conventional", "full_source"]}
    by_author = {a["id"]: a for a in authors}
    dummy = json.dumps({"status": "Dummy current state.", "evidence": "Dummy evidence only.", "next": "Dummy source recovery."})
    for r in readers:
        assert r["status"] == "UNRUN"
        q = catalogue[r["question"]]
        assert q["history"] == r["history"]
        if r["method"] == "full_source":
            assert r["author"] is None
            prompt = m.recipient_prompt(q["query"], "full_source", m.history(r["history"]))
        else:
            a = by_author[r["author"]]
            assert (a["history"], a["method"]) == (r["history"], r["method"])
            prompt = m.recipient_prompt(q["query"], "handoff", m.render_handoff(dummy))
            assert m.history(r["history"]) not in prompt
        assert q["query"] in prompt
    # Fixture-only schema/limit checks: not a recorder rehearsal or experimental responses.
    assert m.validate_author(dummy)["words"] == 9
    exactly = json.dumps({"status": "word " * 218, "evidence": "word", "next": "word"})
    assert m.validate_author(exactly)["words"] == 220
    reject(m.validate_author, json.dumps({"status": "word " * 219, "evidence": "word", "next": "word"}))
    reject(m.validate_author, '{"status":"a","status":"b","evidence":"c","next":"d"}')
    reject(m.validate_author, '{"status":"a","evidence":"b","next":"c","extra":"d"}')
    reject(m.validate_author, '{"status":null,"evidence":"b","next":"c"}')
    reject(m.validate_author, '{"status":"","evidence":"b","next":"c"}')
    reject(m.validate_author, '{"next":"c","status":"a","evidence":"b"}')
    reject(m.validate_author, "not JSON")
    valid = json.dumps({"answer": "Insufficient evidence.", "recover": True})
    assert m.validate_recipient(valid)["words"] == 2
    reject(m.validate_recipient, valid, "recovery")
    reject(m.validate_recipient, valid, "full_source")
    reject(m.validate_recipient, '{"answer":"","recover":true}')
    reject(m.validate_recipient, '{"answer":"x","recover":"true"}')
    reject(m.validate_recipient, json.dumps({"answer": "word " * 161, "recover": False}))
    assert m.validate_recipient(json.dumps({"answer": "word " * 160, "recover": False}), "full_source")["words"] == 160
    n = arithmetic()
    result = {"status": "PASS_SAME_AUTHOR_STATIC_PREFLIGHT",
              "history_words": counts, "method_instruction_words": method_counts,
              "history_events": 72, "questions": 18, "authors_prepared": 12,
              "handoff_recipient_cells": 36, "full_source_control_cells": 18,
              "numeric_key_records_checked": n, "exact_question_leakage_in_author_packets": False,
              "dummy_schema_checks": "PASS; no participant responses",
              "source_key_semantic_review": "PENDING", "recorder_rehearsal": "NOT_PERFORMED",
              "model_calls": 0, "comparative_results": None,
              "limits": "Source primitives and arithmetic share the designer's authorship. Structural checks do not certify source-key semantics, hypothetical scope, fair difficulty, successful isolation, or empirical benefit."}
    m.write("PREFLIGHT.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
