"""Alternate exact verifier: event cells and exhaustive subset sizes.

Imports neither study.py nor lonely_runner.checker. Same AI author; this is not
independent human review or formal proof verification.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from math import ceil, floor
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def check(ok, message):
    if not ok:
        raise ValueError(message)


def safe(speeds, t, delta):
    return all(delta <= (v*t % 1) <= 1-delta for v in speeds)


def join(pieces):
    union = []
    for left, right in sorted(pieces):
        if union and left <= union[-1][1]:
            union[-1] = (union[-1][0], max(right, union[-1][1]))
        else:
            union.append((left, right))
    return union


def event_set(speeds, delta):
    events = sorted({F(0), F(1)} | {(F(j)+d)/v for v in speeds for j in range(v)
                                   for d in (delta, 1-delta)})
    points = [(t, t) for t in events if safe(speeds, t, delta)]
    cells = [(a, b) for a, b in zip(events, events[1:]) if safe(speeds, (a+b)/2, delta)]
    return join(points+cells), len(events)


def intervals(rows):
    return [tuple(map(F, row)) for row in rows]


def clip(union, interval):
    a, b = interval
    return [(max(a, l), min(b, u)) for l, u in union if max(a, l) <= min(b, u)]


def phase_first(left, r, delta):
    position = r*left
    lap = floor(position)
    phase = position-lap
    if delta <= phase <= 1-delta:
        return left
    if phase < delta:
        return (lap+delta)/r
    return (lap+1+delta)/r


def verify_witness(record, speeds, delta):
    t = F(record["time"])
    check(safe(speeds, t, delta), "invalid witness")
    check([v*t % 1 for v in speeds] == list(map(F, record["phases"])), "witness phase mismatch")
    check([floor(v*t) for v in speeds] == record["laps"], "witness lap mismatch")


def verify_minimum(leader, count, incidence, reported, budget):
    if any(not any(row) for row in incidence):
        check(reported["status"] == "NO_SUFFICIENT_MENU", "missed full-core failure")
        return 0, "NO_SUFFICIENT_MENU"
    if reported["status"] == "UNKNOWN_BUDGET":
        return 0, "UNKNOWN_BUDGET"
    check(reported["status"] == "EXACT", "invalid minimum status")
    tests = 0
    best = None
    others = [i for i in range(count) if i != leader]
    for size in range(len(reported["ids"])):
        valid = []
        for extra in combinations(others, size):
            tests += 1
            if tests > budget:
                return tests, "UNKNOWN_VERIFIER_BUDGET"
            menu = sorted((leader,)+extra)
            if all(any(row[i] for i in menu) for row in incidence):
                valid.append(menu)
        if valid:
            best = min(valid)
            break
    check(best == reported["ids"], "minimum size or lexicographic choice disagrees")
    return tests, "EXACT_VERIFIED"


def verify(path):
    raw = path.read_bytes()
    result = json.loads(raw)
    manifest = json.loads((HERE / "manifest.json").read_text())
    cfg = json.loads((HERE / "protocol.json").read_text())
    inputs = json.loads((HERE / "inputs.json").read_text())
    freeze = result["freeze_commit"]
    archived_manifest = subprocess.check_output(
        ["git", "show", freeze+":experiments/runner-addition/manifest.json"], cwd=ROOT)
    check(archived_manifest == (HERE / "manifest.json").read_bytes(), "modified manifest")
    check(result["study"] == cfg["study"], "study identity mismatch")
    check(result["protocol_commit"] == manifest["protocol_commit"], "protocol identity mismatch")
    for relative, expected in manifest["sha256"].items():
        data = (ROOT / relative).read_bytes()
        check(hashlib.sha256(data).hexdigest() == expected, "modified frozen dependency")
        archived = subprocess.check_output(["git", "show", freeze+":"+relative], cwd=ROOT)
        check(archived == data, "file differs from execution freeze")
    check(len(inputs["records"]) == len(result["records"]) == 6, "record count mismatch")
    check([(r["pair"], r["threshold"]) for r in inputs["records"]] ==
          [(pair, threshold) for pair in cfg["pairs"] for threshold in cfg["thresholds"]],
          "frozen configuration order mismatch")
    counts = {"core_sets": 0, "child_sets": 0, "events": 0, "component_contacts": 0,
              "witnesses": 0, "subset_combinations": 0}
    audits = []
    for source, record in zip(inputs["records"], result["records"]):
        check(source["pair"] == record["pair"] and source["threshold"] == record["threshold"],
              "configuration identity mismatch")
        p, q = source["pair"]
        speeds = [p, q, p+q, 2*p+q, 3*p+q, 3*p+2*q, 6*p+2*q, 3*p+8*q]
        check(speeds == source["speeds"] == record["speeds"], "speed generation mismatch")
        check(len(set([0]+speeds)) == 9, "repeated core speed")
        delta = F(source["threshold"])
        core, events = event_set(speeds, delta)
        counts["events"] += events
        counts["core_sets"] += 1
        check(core == intervals(source["components"]), "event/core mismatch")
        check(len(core) == len(record["components"]), "component count mismatch")
        leader = min(range(len(core)), key=lambda i: (-(core[i][1]-core[i][0]), core[i][0]))
        cutoff = ceil(2*delta/(core[leader][1]-core[leader][0]))
        check(leader == source["leader"] == record["leader"], "leader identity mismatch")
        check(cutoff == source["cutoff"] == record["cutoff"], "tail cutoff mismatch")
        for interval, cert in zip(core, record["components"]):
            check(interval == tuple(map(F, cert["interval"])), "component interval mismatch")
            check(interval[1]-interval[0] == F(cert["width"]), "component width mismatch")
            expected_laps = [floor(v*interval[0]) for v in speeds]
            check(expected_laps == cert["laps"], "component lap mismatch")
            endpoints = [[v*t-lap for v, lap in zip(speeds, expected_laps)] for t in interval]
            check(endpoints == [list(map(F, row)) for row in cert["endpoint_phases"]], "endpoint phases")
            check(all(delta <= x <= 1-delta for row in endpoints for x in row), "endpoint band failure")
        check([c["r"] for c in record["cases"]] == source["matched_inputs"], "finite input mismatch")
        incidence = []
        leader_misses, full_misses, singleton_required = [], [], []
        for case in record["cases"]:
            r = case["r"]
            check(r > 0 and r not in speeds, "inadmissible added speed")
            check(case["necessary_remainder"] == (r < cutoff), "remainder flag mismatch")
            full, events = event_set(speeds+[r], delta)
            counts["events"] += events
            counts["child_sets"] += 1
            check(full == intervals(case["full_safe_set"]), "complete child set mismatch")
            check(len(case["contacts"]) == len(core), "contact count mismatch")
            hits = []
            for i, (interval, contact) in enumerate(zip(core, case["contacts"])):
                pieces = clip(full, interval)
                check(contact["component"] == i, "component ID mismatch")
                check(pieces == intervals(contact["surviving_pieces"]), "surviving pieces mismatch")
                expected = phase_first(interval[0], r, delta)
                check(expected == F(contact["candidate"]), "first contact mismatch")
                check(floor(r*expected) == contact["lap"], "added lap mismatch")
                hit = bool(pieces)
                check(hit == contact["hit"] == (expected <= interval[1]), "contact Boolean mismatch")
                if hit:
                    check(expected == pieces[0][0] and safe(speeds+[r], expected, delta), "unsafe contact")
                hits.append(hit)
                counts["component_contacts"] += 1
            incidence.append(hits)
            positive_hit = any(hit and a < b for hit, (a, b) in zip(hits, core))
            check(positive_hit == case["positive_sources_hit"], "positive source classification")
            if not hits[leader]:
                leader_misses.append(r)
            if not full:
                full_misses.append(r)
                check(case["complete_witness"] is None, "witness on empty set")
            else:
                check(F(case["complete_witness"]["time"]) == full[0][0], "first full witness")
                verify_witness(case["complete_witness"], speeds+[r], delta)
                counts["witnesses"] += 1
                if not positive_hit:
                    singleton_required.append(r)
            ids = record["menu"]["ids"]
            if ids:
                selected = [i for i in ids if hits[i]]
                check(bool(selected), "menu missed a finite input")
                best = min(selected, key=lambda i: (F(case["contacts"][i]["candidate"]), i))
                check(case["menu_witness"]["component"] == best, "menu witness component")
                check(F(case["menu_witness"]["time"]) == F(case["contacts"][best]["candidate"]), "menu time")
                verify_witness(case["menu_witness"], speeds+[r], delta)
                counts["witnesses"] += 1
            else:
                check(case["menu_witness"] is None, "witness without selected menu")
        tests, minimum_status = verify_minimum(leader, len(core), incidence, record["menu"],
                                               cfg["max_verifier_combinations"])
        counts["subset_combinations"] += tests
        summary = record["summary"]
        check(summary["leader_misses"] == leader_misses, "leader miss summary")
        check(summary["full_core_misses"] == full_misses, "core miss summary")
        check(summary["isolated_sources_required"] == singleton_required, "singleton summary")
        check(summary["finite_cases"] == len(incidence), "finite count")
        check(summary["component_queries"] == len(core)*len(incidence), "contact count")
        check(summary["core_components"] == len(core), "core component summary")
        check(summary["positive_components"] == sum(a < b for a, b in core), "positive count")
        check(summary["isolated_components"] == sum(a == b for a, b in core), "isolated count")
        check(summary["core_speed_sum"] == sum(speeds), "core construction size")
        ids = record["menu"]["ids"]
        check(summary["minimum_menu_size"] == (len(ids) if ids else None), "minimum summary")
        check(summary["leader_plus_one_suffices"] == (len(ids) <= 2 if ids else None), "two-source summary")
        check(summary["all_r_status"] == ("CANDIDATE_CERTIFICATE" if record["menu"]["status"] == "EXACT"
                                           else record["menu"]["status"]), "claim status summary")
        expected_controls = []
        for seed in (cutoff, cutoff+1, 10**6+1, 10**18+1):
            r = seed
            while r in speeds:
                r += 1
            if r not in expected_controls:
                expected_controls.append(r)
        check(source["tail_controls"] == expected_controls, "incomplete tail controls")
        check([c["r"] for c in record["tail_controls"]] == source["tail_controls"], "tail input mismatch")
        for row in record["tail_controls"]:
            check(row["r"] >= cutoff and row["r"] not in speeds, "invalid tail control")
            t = phase_first(core[leader][0], row["r"], delta)
            check(core[leader][0] <= t <= core[leader][1], "tail contact outside leader")
            check(t == F(row["time"]) and row["component"] == leader, "tail witness mismatch")
            verify_witness(row, speeds+[row["r"]], delta)
            counts["witnesses"] += 1
        audits.append({"pair": source["pair"], "threshold": source["threshold"],
                       "minimum_status": minimum_status, "subsets_checked": tests})
    # Verify domains were derived completely, rather than trusting the input list.
    for offset in range(0, 6, 2):
        pair = inputs["records"][offset:offset+2]
        bound = max(row["cutoff"] for row in pair)
        expected = [r for r in range(1, bound) if r not in pair[0]["speeds"]]
        for row in pair:
            check(row["matched_inputs"] == expected, "incomplete matched finite domain")
            check(row["necessary_remainder"] == [r for r in expected if r < row["cutoff"]], "remainder domain")
    # Fixed exact semantics controls, not new research inputs.
    check(event_set([1,2], F(1,3))[0] == [(F(1,3), F(1,3)), (F(2,3), F(2,3))], "equality control")
    check(event_set([1,2], F(2,5))[0] == [], "empty-set control")
    check(phase_first(F(7,8), 1, F(1,8)) == F(7,8), "exact-width equality control")
    check(safe([1], F(9,8), F(1,8)), "exact-width other endpoint")
    check(result["summary"]["finite_cases"] == counts["child_sets"], "overall case count")
    check(result["summary"]["component_queries"] == counts["component_contacts"], "overall contact count")
    check(result["summary"]["records"] == len(audits), "overall record count")
    check(result["summary"]["full_core_misses"] == sum(
        len(r["summary"]["full_core_misses"]) for r in result["records"]), "overall full misses")
    status = "PASS" if all(x["minimum_status"] == "EXACT_VERIFIED" for x in audits) else "VERIFIED_WITH_UNRESOLVED_MINIMA"
    return {"status": status, "freeze_commit": freeze,
            "results_sha256": hashlib.sha256(raw).hexdigest(), "counts": counts, "records": audits,
            "semantics_controls": 3,
            "method": "exact event decomposition + cardinality-ordered subset enumeration",
            "limits": "Same-author alternate algorithms; no independent human or formal proof certification."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "results/RESULTS.json")
    parser.add_argument("--output", type=Path, default=HERE / "results/VERIFICATION.json")
    args = parser.parse_args()
    check(not args.output.exists(), "refusing to overwrite verification")
    result = verify(args.input)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))
