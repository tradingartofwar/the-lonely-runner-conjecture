"""Minimum fixed-leader menus with linked Boolean, placement and time views."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations
import json
from math import floor
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("runner_addition_primary_v1",HERE.parent / "study.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def require(ok,message):
    if not ok:
        raise ValueError(message)


def join(pieces):
    out = []
    for a,b in sorted(pieces):
        if out and a <= out[-1][1]:
            out[-1] = out[-1][0], max(b,out[-1][1])
        else:
            out.append((a,b))
    return out


def composition(record,cap):
    trials = 0
    for i in range(len(record["components"])):
        for first,second in combinations(record["cases"],2):
            trials += 1
            if trials > cap:
                return {"status":"UNKNOWN_BUDGET","trials":trials}
            x,y = first["contacts"][i],second["contacts"][i]
            if not x["hit"] or not y["hit"]:
                continue
            common = join([(max(a,c),min(b,d)) for a,b in x["surviving_pieces"]
                           for c,d in y["surviving_pieces"] if max(a,c) <= min(b,d)])
            if not common:
                return {"status":"FOUND","trials":trials,"component":i,
                        "r":first["r"],"s":second["r"],
                        "r_pieces":x["surviving_pieces"],"s_pieces":y["surviving_pieces"],
                        "r_time":x["candidate"],"s_time":y["candidate"],"common_pieces":common}
    return {"status":"NOT_FOUND_IN_DOMAIN","trials":trials}


def enrich(record,prior,cfg):
    d = F(record["threshold"])
    core = [tuple(c["interval"]) for c in record["components"]]
    for component,(a,b) in zip(record["components"],core):
        component["center"],component["half_width"] = (a+b)/2,(b-a)/2
    for case in record["cases"]:
        case["coverage_mask"] = sum(1 << i for i,c in enumerate(case["contacts"]) if c["hit"])
        case["coverage_bits_id_order"] = "".join("1" if c["hit"] else "0" for c in case["contacts"])
        for i,contact in enumerate(case["contacts"]):
            a,b = core[i]
            z = case["r"]*(a+b)/2
            m = floor(z) if z % 1 <= F(1,2) else floor(z)+1
            value = abs(z-m)+case["r"]*(b-a)/2
            require((value >= d) == contact["hit"], "placement/contact discrepancy")
            contact["placement"] = {"value":value,"blocking_integer":m if value < d else None,
                "unsafe_gap":((m-d)/case["r"],(m+d)/case["r"]) if value < d else None,
                "gap_center":F(m,case["r"]) if value < d else None}
    ids = record["menu"]["ids"] or []
    failures = [{"component":i,"blocked_r":[c["r"] for c in record["cases"] if not c["contacts"][i]["hit"]]}
                for i in ids]
    common = sorted(set.intersection(*(set(x["blocked_r"]) for x in failures))) if failures else None
    if ids:
        require(common == [], "selected menu has a shared blocker")
    misses = record["summary"]["leader_misses"]
    repair = None
    for i in sorted((i for i in ids if i != record["leader"]),key=lambda j:(core[j][0],j)):
        t = core[i][0]
        if misses and all(d <= r*t % 1 <= 1-d for r in misses):
            repair = {"component":i,"time":t,"exception_speeds":misses,
                      "witnesses":[{"r":r,**base.witness_record(t,record["speeds"]+[r],d)} for r in misses]}
            break
    old = next(x for x in prior["new_records"] if x["pair"] == record["pair"])
    all_singles_blocked = all(x["status"] == "BLOCKED" for x in old["components"])
    require([tuple(map(F,x["interval"])) for x in old["components"]] == core, "source identity mismatch")
    record["views"] = {
        "component_ids":list(range(len(core))),"finite_speed_order":[c["r"] for c in record["cases"]],
        "component_case_masks":[sum(1 << j for j,c in enumerate(record["cases"]) if c["contacts"][i]["hit"])
                                for i in range(len(core))],
        "selected_failure_sets":failures,"common_failure_speeds":common,
        "leader_unsafe_gaps":[{"r":c["r"],**c["contacts"][record["leader"]]["placement"]}
                              for c in record["cases"] if c["r"] in misses],
        "fixed_exception_repair":repair,
        "minimum_without_forced_leader":2 if len(ids) == 2 and all_singles_blocked else None,
        "composition_diagnostic":composition(record,cfg["max_composition_trials"])}
    return record


def trace(speeds,d,max_events):
    events = sorted({F(0),F(1)} | {(F(j)+x)/s for s in speeds for j in range(s) for x in (d,1-d)})
    require(len(events) <= max_events,"time event budget")
    records = []
    def append(kind,left,right,t):
        flags = [d <= s*t % 1 <= 1-d for s in speeds]
        records.append({"id":len(records),"kind":kind,"left":left,"right":right,
                        "time":t,"mask":sum(1 << i for i,b in enumerate(flags) if b),
                        "bits_speed_order":"".join("1" if b else "0" for b in flags)})
    for i,t in enumerate(events):
        append("point",t,t,t)
        if i+1 < len(events):
            append("open_cell",t,events[i+1],(t+events[i+1])/2)
    full_mask = (1 << len(speeds))-1
    decoded = join([(r["left"],r["right"]) for r in records if r["mask"] == full_mask])
    return {"speeds":speeds,"threshold":d,"events":events,"records":records,
            "decoded_safe_set":decoded,"full_mask":full_mask}


def preflight(freeze):
    raw = (HERE / "manifest.json").read_bytes()
    require(raw == subprocess.check_output(["git","show",freeze+
        ":experiments/runner-addition/menu-views/manifest.json"],cwd=ROOT),"manifest freeze mismatch")
    for path,expected in json.loads(raw)["sha256"].items():
        data = (ROOT/path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected,"changed dependency: "+path)
        require(data == subprocess.check_output(["git","show",freeze+":"+path],cwd=ROOT),"archived dependency mismatch")


def run(freeze):
    preflight(freeze)
    cfg = json.loads((HERE / "config.json").read_text())
    inputs = json.loads((HERE / "inputs.json").read_text())
    prior = json.loads((HERE.parent / "placement/results/RESULTS.json").read_text())
    records = []
    for source in inputs["records"]:
        require(sum(source["speeds"]) <= cfg["max_core_speed_sum"],"core budget")
        records.append(enrich(base.evaluate(source,cfg),prior,cfg))
    chosen = next(x for x in records if x["pair"] == cfg["trace_pair"])
    r = cfg["trace_added_speed"]
    time_view = trace(chosen["speeds"]+[r],F(cfg["threshold"]),cfg["max_event_points"])
    case = next(c for c in chosen["cases"] if c["r"] == r)
    require(time_view["decoded_safe_set"] == list(case["full_safe_set"]),"time-view decoding mismatch")
    old = next(x for x in prior["new_records"] if x["pair"] == cfg["trace_pair"])
    saved = next(x for x in old["children_at_blockers"] if x["r"] == r)
    require(time_view["decoded_safe_set"] == [tuple(map(F,x)) for x in saved["full_safe_set"]],"saved case mismatch")
    leader = chosen["components"][chosen["leader"]]["interval"]
    first = tuple(map(F,saved["full_safe_set"][0]))
    boundaries = [("leader_start",leader[0]),("leader_end",leader[1]),
                  ("recovery_start",first[0]),("recovery_end",first[1])]
    focus = []
    for name,t in boundaries:
        at = 2*time_view["events"].index(t)
        before,point,after = (time_view["records"][i] for i in (at-1,at,at+1))
        focus.append({"name":name,"time":t,"before_id":at-1,"point_id":at,"after_id":at+1,
                      "become_true_at":[s for i,s in enumerate(time_view["speeds"])
                          if not (before["mask"] >> i & 1) and (point["mask"] >> i & 1)],
                      "become_false_after":[s for i,s in enumerate(time_view["speeds"])
                          if (point["mask"] >> i & 1) and not (after["mask"] >> i & 1)]})
    time_view["focus"] = focus
    fixture = trace([1,2],F(1,3),cfg["max_event_points"])
    require(fixture["decoded_safe_set"] == [(F(1,3),F(1,3)),(F(2,3),F(2,3))],"isolated-time fixture")
    require(not any(x["mask"] == 3 and x["kind"] == "open_cell" for x in fixture["records"]),"fixture cell")
    return {"study":cfg["study"],"freeze_commit":freeze,"source_commit":cfg["source_commit"],
            "records":records,"time_view":time_view,"singleton_fixture":"PASS",
            "claim_status":"Exact finite records; all-r and minimum implications remain proof candidates."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze",required=True)
    parser.add_argument("--output",type=Path,default=HERE / "results/RESULTS.json")
    args = parser.parse_args()
    require(not args.output.exists(),"refusing to overwrite result")
    result = run(args.freeze)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result,default=base.encode,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"families":[{"pair":r["pair"],**r["summary"],"menu":r["menu"]["ids"],
                      "composition":r["views"]["composition_diagnostic"]["status"]} for r in result["records"]],
                      "time_events":len(result["time_view"]["events"]),
                      "time_records":len(result["time_view"]["records"])},indent=2))
