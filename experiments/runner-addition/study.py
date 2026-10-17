"""Exact runner-addition study. Uses the pinned existing band-intersection checker."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import ceil, floor
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from lonely_runner.checker import feasible_intervals


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def first_contact(interval, r, delta):
    left, right = interval
    lap = ceil(r*left - (1-delta))
    candidate = max(left, (lap+delta)/r)
    require(candidate <= (lap+1-delta)/r, "contact not in proposed safe band")
    return {"candidate": candidate, "lap": lap, "hit": candidate <= right}


def witness_record(t, speeds, delta):
    phases = [v*t % 1 for v in speeds]
    require(all(delta <= x <= 1-delta for x in phases), "unsafe physical witness")
    return {"time": t, "phases": phases, "laps": [floor(v*t) for v in speeds]}


def component_certificate(interval, speeds, delta):
    left, right = interval
    laps = [floor(v*(left+right)/2) for v in speeds]
    endpoints = [[v*t-lap for v, lap in zip(speeds, laps)] for t in interval]
    require(all(delta <= x <= 1-delta for row in endpoints for x in row),
            "component has invalid endpoint/lap certificate")
    return {"interval": interval, "width": right-left, "laps": laps,
            "endpoint_phases": endpoints}


def minimum_menu(leader, component_count, cases, cfg):
    misses = [case for case in cases if not case["contacts"][leader]["hit"]]
    if any(not case["full_safe_set"] for case in misses):
        return {"status": "NO_SUFFICIENT_MENU", "ids": None,
                "reason": "complete core fails a finite input", "states": 0, "transitions": 0}
    if not misses:
        return {"status": "EXACT", "ids": [leader], "states": 1, "transitions": 0}
    target = (1 << len(misses))-1
    masks = {i: sum((1 << j) for j, case in enumerate(misses) if case["contacts"][i]["hit"])
             for i in range(component_count) if i != leader}
    states = {0: ()}
    transitions = 0
    peak = 1
    for i in sorted(masks):
        if not masks[i]:
            continue
        updated = dict(states)
        for mask, subset in states.items():
            transitions += 1
            if transitions > cfg["max_dp_transitions"]:
                return {"status": "UNKNOWN_BUDGET", "ids": None, "states": peak,
                        "transitions": transitions, "reason": "DP transition budget"}
            union = mask | masks[i]
            candidate = subset + (i,)
            old = updated.get(union)
            if old is None or (len(candidate), candidate) < (len(old), old):
                updated[union] = candidate
        states = updated
        peak = max(peak, len(states))
        if len(states) > cfg["max_dp_states"]:
            return {"status": "UNKNOWN_BUDGET", "ids": None, "states": peak,
                    "transitions": transitions, "reason": "DP state budget"}
    require(target in states, "complete coverage but DP failed to find a menu")
    return {"status": "EXACT", "ids": sorted((leader,) + states[target]),
            "states": peak, "transitions": transitions}


def evaluate(source, cfg):
    delta = F(source["threshold"])
    speeds = source["speeds"]
    intervals = [tuple(map(F, row)) for row in source["components"]]
    leader = source["leader"]
    # Frozen cores are inputs; cost of their original construction remains visible.
    require(list(feasible_intervals(speeds, delta)) == intervals, "frozen core mismatch")
    certificates = [component_certificate(interval, speeds, delta) for interval in intervals]
    cases = []
    for r in source["matched_inputs"]:
        full = feasible_intervals(speeds + [r], delta)
        contacts = []
        for i, interval in enumerate(intervals):
            contact = first_contact(interval, r, delta)
            pieces = [(max(a, interval[0]), min(b, interval[1])) for a, b in full
                      if max(a, interval[0]) <= min(b, interval[1])]
            require(bool(pieces) == contact["hit"], "contact/complete-set disagreement")
            if pieces:
                require(contact["candidate"] == pieces[0][0], "first contact disagreement")
                witness_record(contact["candidate"], speeds + [r], delta)
            contacts.append({"component": i, **contact, "surviving_pieces": pieces})
        cases.append({
            "r": r, "necessary_remainder": r < source["cutoff"],
            "contacts": contacts, "full_safe_set": full,
            "complete_witness": witness_record(full[0][0], speeds+[r], delta) if full else None,
            "positive_sources_hit": any(c["hit"] and intervals[c["component"]][0] < intervals[c["component"]][1]
                                        for c in contacts),
        })
    menu = minimum_menu(leader, len(intervals), cases, cfg)
    for case in cases:
        ids = menu["ids"] or []
        successful = [i for i in ids if case["contacts"][i]["hit"]]
        if successful:
            i = min(successful, key=lambda j: (case["contacts"][j]["candidate"], j))
            case["menu_witness"] = {"component": i, **witness_record(
                case["contacts"][i]["candidate"], speeds+[case["r"]], delta)}
        else:
            case["menu_witness"] = None
    tail = []
    for r in source["tail_controls"]:
        contact = first_contact(intervals[leader], r, delta)
        require(contact["hit"], "width-tail control failed")
        tail.append({"r": r, "component": leader,
                     **witness_record(contact["candidate"], speeds+[r], delta)})
    leader_misses = [c["r"] for c in cases if not c["contacts"][leader]["hit"]]
    full_misses = [c["r"] for c in cases if not c["full_safe_set"]]
    singleton_required = [c["r"] for c in cases if c["full_safe_set"] and not c["positive_sources_hit"]]
    return {
        "pair": source["pair"], "threshold": source["threshold"], "speeds": speeds,
        "components": certificates, "leader": leader, "cutoff": source["cutoff"],
        "cases": cases, "menu": menu, "tail_controls": tail,
        "summary": {
            "finite_cases": len(cases), "core_components": len(intervals),
            "positive_components": sum(a < b for a, b in intervals),
            "isolated_components": sum(a == b for a, b in intervals),
            "core_speed_sum": sum(speeds), "component_queries": len(cases)*len(intervals),
            "leader_misses": leader_misses, "full_core_misses": full_misses,
            "isolated_sources_required": singleton_required,
            "minimum_menu_size": len(menu["ids"]) if menu["ids"] else None,
            "leader_plus_one_suffices": len(menu["ids"]) <= 2 if menu["ids"] else None,
            "all_r_status": "CANDIDATE_CERTIFICATE" if menu["status"] == "EXACT" else menu["status"],
        },
    }


def preflight(freeze):
    manifest_bytes = (HERE / "manifest.json").read_bytes()
    archived_manifest = subprocess.check_output(
        ["git", "show", freeze + ":experiments/runner-addition/manifest.json"], cwd=ROOT)
    require(manifest_bytes == archived_manifest, "manifest differs from execution freeze")
    manifest = json.loads(manifest_bytes)
    for path, expected in manifest["sha256"].items():
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        require(actual == expected, "local frozen input mismatch: " + path)
        archived = subprocess.check_output(["git", "show", freeze + ":" + path], cwd=ROOT)
        require(hashlib.sha256(archived).hexdigest() == expected, "freeze content mismatch: " + path)
    return manifest


def run(freeze):
    manifest = preflight(freeze)
    cfg = json.loads((HERE / "protocol.json").read_text())
    inputs = json.loads((HERE / "inputs.json").read_text())
    records = [evaluate(source, cfg) for source in inputs["records"]]
    return {
        "study": cfg["study"], "freeze_commit": freeze,
        "protocol_commit": manifest["protocol_commit"],
        "arithmetic": "exact fractions.Fraction; existing interval checker",
        "claim_status": "finite observations; all-r derivations remain proof candidates",
        "records": records,
        "summary": {"records": len(records), "finite_cases": sum(len(r["cases"]) for r in records),
                    "component_queries": sum(r["summary"]["component_queries"] for r in records),
                    "full_core_misses": sum(len(r["summary"]["full_core_misses"]) for r in records)},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--output", type=Path, default=HERE / "results/RESULTS.json")
    args = parser.parse_args()
    require(not args.output.exists(), "refusing to overwrite an existing run")
    result = run(args.freeze)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result, default=encode, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "COMPUTED_PENDING_VERIFICATION", **result["summary"],
                      "families": [{"pair": r["pair"], "threshold": r["threshold"],
                                    **r["summary"]} for r in result["records"]]}, indent=2))
