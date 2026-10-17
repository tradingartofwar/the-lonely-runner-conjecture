"""Frozen unsafe-gap selector; compare with lazy two-menu and exact cover."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import ceil, floor
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("gap_reference_primary", HERE.parent / "study.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def preflight(freeze):
    raw = (HERE / "manifest.json").read_bytes()
    prefix = "experiments/runner-addition/gap-selection/"
    require(raw == subprocess.check_output(["git", "show", freeze+":"+prefix+"manifest.json"], cwd=ROOT),
            "manifest differs from freeze")
    manifest = json.loads(raw)
    for path, expected in manifest["sha256"].items():
        data = (ROOT / path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected, "local frozen file changed: "+path)
        require(data == subprocess.check_output(["git", "show", freeze+":"+path], cwd=ROOT),
                "archive differs: "+path)
    return manifest


def leader_classification(interval, domain, d):
    a, b = interval
    c, h = (a+b)/2, (b-a)/2
    out = []
    for r in domain:
        x = r*c
        m = floor(x) if x % 1 <= F(1, 2) else floor(x)+1
        value = abs(x-m)+r*h
        out.append({"r": r, "value": value, "hit": value >= d,
                    "blocking_integer": m if value < d else None,
                    "unsafe_gap": ((m-d)/r, (m+d)/r) if value < d else None})
    return out


def gap_search(core, failures, d, cap):
    visits, probes, jumps = [], 0, 0
    for i, (a, b) in enumerate(core):
        visit = {"component": i, "probes": []}
        visits.append(visit)
        t = a
        while t <= b:
            moved = False
            for r in failures:
                if probes >= cap:
                    return {"status": "UNKNOWN_BUDGET", "component": None, "time": None,
                            "trace": visits, "point_tests": probes, "jumps": jumps,
                            "components_visited": len(visits)}
                probes += 1
                x = r*t
                phase = x % 1
                ok = d <= phase <= 1-d
                m = None if ok else (floor(x) if phase < d else floor(x)+1)
                jump = None if ok else (m+d)/r
                visit["probes"].append({"r": r, "time": t, "safe": ok,
                                         "blocking_integer": m, "jump_to": jump})
                if not ok:
                    require(jump > t, "unsafe-gap jump did not advance")
                    jumps += 1
                    t, moved = jump, True
                    break
            if not moved:
                return {"status": "FOUND", "component": i, "time": t, "trace": visits,
                        "point_tests": probes, "jumps": jumps, "components_visited": len(visits)}
    return {"status": "NO_COMMON_REPAIR_POINT", "component": None, "time": None,
            "trace": visits, "point_tests": probes, "jumps": jumps, "components_visited": len(visits)}


def lazy_search(core, failures, d, cap, leader=None):
    visits, count = [], 0
    for i, interval in enumerate(core):
        if i == leader:
            continue
        visit = {"component": i, "contacts": []}
        visits.append(visit)
        all_hit = True
        for r in failures:
            if count >= cap:
                return {"status": "UNKNOWN_BUDGET", "component": None, "trace": visits,
                        "interval_tests": count, "components_visited": len(visits)}
            count += 1
            contact = base.first_contact(interval, r, d)
            visit["contacts"].append({"r": r, **contact})
            if not contact["hit"]:
                all_hit = False
                break
        if all_hit:
            return {"status": "FOUND", "component": i, "trace": visits,
                    "interval_tests": count, "components_visited": len(visits)}
    return {"status": "NO_TWO_COMPONENT_MENU", "component": None, "trace": visits,
            "interval_tests": count, "components_visited": len(visits)}


def recover(method, selection, source, failures):
    d, core = F(source["threshold"]), source["components"]
    if selection["ids"] is None:
        return {"status": "NO_SELECTOR_CERTIFICATE", "finite": [], "tail": [],
                "finite_first_contact_calls": 0, "tail_first_contact_calls": 0}
    out = {"status": "RECOVERED", "finite": [], "tail": [],
           "finite_first_contact_calls": 0, "tail_first_contact_calls": 0}
    for kind, domain in (("finite", source["matched_inputs"]), ("tail", source["tail_controls"])):
        for r in domain:
            if method == "gap" and r in failures:
                i, t = selection["component"], selection["time"]
            else:
                if method == "exact":
                    ids = selection["ids"]
                else:
                    ids = [selection["component"] if r in failures else source["leader"]]
                candidates = []
                for j in ids:
                    contact = base.first_contact(core[j], r, d)
                    out[kind+"_first_contact_calls"] += 1
                    if contact["hit"]:
                        candidates.append((contact["candidate"], j))
                require(bool(candidates), method+" recovery missed")
                t, i = min(candidates)
            require(core[i][0] <= t <= core[i][1], "recovery outside source")
            out[kind].append({"r": r, "component": i,
                              **base.witness_record(t, source["speeds"]+[r], d)})
    return out


def evaluate(pair, cfg):
    p, q = pair
    speeds = [p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q]
    require(len(set([0]+speeds)) == 9, "non-distinct core")
    d = F(cfg["threshold"])
    if sum(speeds) > cfg["max_core_speed_sum"]:
        return {"pair": pair, "status": "UNKNOWN_CORE_BUDGET", "speeds": speeds}
    core = list(base.feasible_intervals(speeds, d))
    record = {"pair": pair, "speeds": speeds, "core": core,
              "core_input_bands": sum(speeds), "core_components": len(core)}
    if not core:
        return {**record, "status": "UNSUPPORTED_EMPTY_CORE"}
    if len(core) > cfg["max_components"]:
        return {**record, "status": "UNKNOWN_COMPONENT_BUDGET"}
    leader = min(range(len(core)), key=lambda i: (-(core[i][1]-core[i][0]), core[i][0]))
    width = core[leader][1]-core[leader][0]
    if not width:
        return {**record, "status": "UNSUPPORTED_ZERO_WIDTH"}
    cutoff = ceil(2*d/width)
    if cutoff > cfg["max_tail_cutoff"]:
        return {**record, "status": "UNKNOWN_DOMAIN_BUDGET", "leader": leader, "cutoff": cutoff}
    domain = [r for r in range(1, cutoff) if r not in speeds]
    controls = []
    for seed in (cutoff, cutoff+1, 10**6+1, 10**18+1):
        r = seed
        while r in speeds:
            r += 1
        if r not in controls:
            controls.append(r)
    source = {"pair": pair, "speeds": speeds, "threshold": cfg["threshold"], "components": core,
              "leader": leader, "cutoff": cutoff, "matched_inputs": domain,
              "necessary_remainder": domain, "tail_controls": controls}
    classification = leader_classification(core[leader], domain, d)
    failures = [x["r"] for x in classification if not x["hit"]]
    if failures:
        gap = gap_search(core, failures, d, cfg["max_gap_probes"])
        lazy = lazy_search(core, failures, d, cfg["max_lazy_contacts"], leader)
        for selection in (gap, lazy):
            selection["ids"] = sorted([leader, selection["component"]]) if selection["status"] == "FOUND" else None
    else:
        gap = {"status": "LEADER_ONLY", "component": None, "time": None, "ids": [leader],
               "trace": [], "point_tests": 0, "jumps": 0, "components_visited": 0}
        lazy = {"status": "LEADER_ONLY", "component": None, "ids": [leader],
                "trace": [], "interval_tests": 0, "components_visited": 0}
    # Full matrix and optimality reference are computed only AFTER both selectors.
    exact = base.evaluate(source, cfg)
    require(failures == exact["summary"]["leader_misses"], "leader predicate disagreement")
    recovery = {name: recover(name, selection, source, failures)
                for name, selection in (("gap", gap), ("lazy", lazy), ("exact", exact["menu"]))}
    exact_size = len(exact["menu"]["ids"]) if exact["menu"]["ids"] else None
    sizes = {name: len(sel["ids"]) if sel["ids"] else None for name, sel in (("gap",gap),("lazy",lazy))}
    return {**record, "status": "EVALUATED", "source": source, "leader_classification": classification,
            "failures": failures, "gap": gap, "lazy": lazy, "exact": exact, "recovery": recovery,
            "comparison": {"exact_size": exact_size, "selector_sizes": sizes,
                "equal_minimum": {name: size == exact_size if size is not None and exact_size is not None else None
                                  for name, size in sizes.items()},
                "common_point_miss_despite_two_menu": gap["status"] == "NO_COMMON_REPAIR_POINT" and lazy["status"] == "FOUND"},
            "cost": {"shared_leader_tests": len(domain), "gap_point_tests": gap["point_tests"],
                     "gap_jumps": gap["jumps"], "lazy_interval_tests": lazy["interval_tests"],
                     "full_matrix_contacts": exact["summary"]["component_queries"],
                     "dp_states": exact["menu"]["states"], "dp_transitions": exact["menu"]["transitions"]}}


def controls(cfg):
    fixtures = [
        {"name": "touching_open_gaps", "core": [(F(3,10),F(2,5))], "speeds": [1,2], "d": F(1,3)},
        {"name": "separate_not_joint", "core": [(F(111,670),F(19,110))], "speeds": [17,18], "d": F(1,10)},
    ]
    for x in fixtures:
        x["gap"] = gap_search(x["core"], x["speeds"], x["d"], cfg["max_gap_probes"])
        x["lazy"] = lazy_search(x["core"], x["speeds"], x["d"], cfg["max_lazy_contacts"])
    require(fixtures[0]["gap"]["time"] == F(1,3), "lost equality fixture")
    require(fixtures[1]["gap"]["status"] == "NO_COMMON_REPAIR_POINT", "false simultaneous contact")
    require(fixtures[1]["lazy"]["status"] == "FOUND", "lost separate contacts")
    return fixtures


def run(freeze):
    preflight(freeze)
    cfg = json.loads((HERE / "config.json").read_text())
    fixtures = controls(cfg)
    records = []
    for pair in cfg["pairs"]:
        record = evaluate(pair, cfg)
        records.append(record)
        print(json.dumps({"pair": pair, "status": record["status"], "failures": record.get("failures"),
                          "comparison": record.get("comparison"), "cost": record.get("cost")}), flush=True)
    return {"study": cfg["study"], "freeze_commit": freeze, "rule_commit": cfg["rule_commit"],
            "claim_status": "bounded observations; universal implications remain same-author proof candidates",
            "records": records, "semantic_controls": fixtures}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--output", type=Path, default=HERE / "results/RESULTS.json")
    args = parser.parse_args()
    require(not args.output.exists(), "refusing to overwrite results")
    result = run(args.freeze)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result, default=base.encode, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"status": "COMPUTED_PENDING_VERIFICATION", "records": len(result["records"])}))
