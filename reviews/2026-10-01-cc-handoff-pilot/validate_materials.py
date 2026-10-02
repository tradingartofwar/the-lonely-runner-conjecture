#!/usr/bin/env python3
"""Static data/oracle preflight. This never calls a model or scores respondents."""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json

HERE = Path(__file__).resolve().parent


def contains(interval, x):
    a, b, lc, rc = interval
    return (a < x < b) or (x == a and lc) or (x == b and rc)


def derive(data):
    kind = data["kind"]
    if kind == "build":
        eligible = sorted(k for k, checks in data["rows"].items() if all(checks))
        return {"decision": "yes" if eligible else "no", "eligible_builds": eligible}
    if kind == "interval":
        intervals = data["intervals"]
        lo = max(Fraction(x[0]) for x in intervals)
        hi = min(Fraction(x[1]) for x in intervals)
        point = lo < hi or (lo == hi and all(contains(x, lo) for x in intervals))
        if data["dwell"] is None:
            out = {"instant": "yes" if point else "no", "positive_duration": "yes" if lo < hi else "no"}
            if point and lo == hi:
                out["instant_witness"] = str(lo)
            return out
        dwell = Fraction(data["dwell"])
        exists = hi-lo > dwell or (hi-lo == dwell and all(contains(x, lo) and contains(x, hi) for x in intervals))
        return {"decision": "yes" if exists else "no"}
    if kind == "validation":
        all_cases = set(data["holdout"])
        groups = [set(data[k]) for k in ["passes", "failures", "untested"]]
        assert set.union(*groups) == all_cases
        assert all(not groups[i] & groups[j] for i in range(3) for j in range(i+1, 3))
        out = {"decision": "fail" if groups[1] else "unresolved" if groups[2] else "pass",
               "passed": len(groups[0]), "failed": len(groups[1]), "untested": len(groups[2])}
        if groups[1]: out["failing_case"] = next(iter(groups[1]))
        if groups[2]: out["untested_case"] = next(iter(groups[2]))
        return out
    if kind == "version":
        if not data["v2_available"]:
            assert data["v2_failures"] is None
            return {"decision": "unknown"}
        return {"decision": "yes" if data["v2_failures"] else "no", "version": "v2",
                "failing_case": data["v2_failures"][0]}
    raise ValueError(kind)


def signature(cid, answer):
    if cid.startswith("T"):
        return answer["instant"], answer["positive_duration"]
    return answer["decision"]


def main():
    cards = json.loads((HERE/"SOURCE_CARDS.json").read_text())["cards"]
    key = json.loads((HERE/"ANSWER_KEY_DRAFT.json").read_text())["answers"]
    pins = json.loads((HERE/"MATERIAL_PINS.json").read_text())["sha256"]
    for p, sha in pins.items():
        assert hashlib.sha256((HERE/p).read_bytes()).hexdigest() == sha, p
    derived = {}
    for c in cards:
        cid = c["id"]
        derived[cid] = derive(c["structured_source"])
        assert all(key[cid][k] == v for k,v in derived[cid].items()), cid
        for src in c["sources"]:
            assert (src["text"] is not None) == src["available"]
    # Verify the supplied positive-dwell witness directly, not only its existence decision.
    c = next(c for c in cards if c["id"] == "S2")
    start, end = map(Fraction, key["S2"]["example_task"])
    assert end-start == 1
    assert all(contains(i, start) and contains(i, end) for i in c["structured_source"]["intervals"])
    trials = json.loads((HERE/"TRIAL_SCHEDULE.json").read_text())["trials"]
    assert len(trials) == 80 and len({x["trial_id"] for x in trials}) == 80
    counts = Counter((x["card_id"],x["arm"]) for x in trials)
    assert len(counts) == 20 and set(counts.values()) == {4}
    assert all(x["status"] == "UNRUN" for x in trials)
    groups = defaultdict(list)
    for c in cards:
        groups[(c["neutral_summary"],c["query"])].append(c["id"])
    collisions = [ids for ids in groups.values() if len({signature(i,key[i]) for i in ids}) > 1]
    assert collisions == [["K1","K2"],["T1","T2"],["M1","M2"],["V1","V2"]]
    report = {"status": "STATIC_PREFLIGHT_PASS_NOT_MODEL_RESULTS", "cards": len(cards),
              "draft_oracle_checks": len(derived), "planned_answers": len(trials), "actual_model_answers": 0,
              "same_author_check": True, "independent_review": "PENDING",
              "neutral_summary_query_collisions": collisions,
              "scope": "Checks data and proposed semantics. Does not test CC or conventional handoff behavior.",
              "derived_answers": derived}
    (HERE/"PREFLIGHT.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k != "derived_answers"}))


if __name__ == "__main__":
    main()
