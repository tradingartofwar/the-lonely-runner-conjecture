"""Alternate verification of menus, linked views and exact per-runner states."""
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
spec = importlib.util.spec_from_file_location("runner_addition_alternate_v1",HERE.parent / "verify.py")
alt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alt)


def check(ok,message):
    if not ok:
        raise ValueError(message)


def overlaps(xs,ys):
    i,j = 0,0
    while i < len(xs) and j < len(ys):
        a,b = map(F,xs[i]); c,d = map(F,ys[j])
        if max(a,c) <= min(b,d):
            return True
        if b < d:
            i += 1
        else:
            j += 1
    return False


def expected_diagnostic(record,cap):
    trials = 0
    cases = record["cases"]
    for component in range(len(record["components"])):
        for x in range(len(cases)):
            for y in range(x+1,len(cases)):
                trials += 1
                if trials > cap:
                    return {"status":"UNKNOWN_BUDGET","trials":trials}
                first,second = cases[x],cases[y]
                a,b = first["contacts"][component],second["contacts"][component]
                if a["hit"] and b["hit"] and not overlaps(a["surviving_pieces"],b["surviving_pieces"]):
                    return {"status":"FOUND","trials":trials,"component":component,
                            "r":first["r"],"s":second["r"],"r_pieces":a["surviving_pieces"],
                            "s_pieces":b["surviving_pieces"],"r_time":a["candidate"],
                            "s_time":b["candidate"],"common_pieces":[]}
    return {"status":"NOT_FOUND_IN_DOMAIN","trials":trials}


def band_state(speed,a,b,delta,point):
    bands = [((j+delta)/speed,(j+1-delta)/speed)
             for j in range(floor(speed*a)-1,floor(speed*b)+2)]
    if point:
        return any(left <= a <= right for left,right in bands)
    covered = any(left <= a and b <= right for left,right in bands)
    if not covered:
        check(not any(max(a,left) < min(b,right) for left,right in bands),
              "runner state changes inside a purported event cell")
    return covered


def verify(path):
    raw = path.read_bytes()
    result = json.loads(raw)
    cfg = json.loads((HERE / "config.json").read_text())
    inputs = json.loads((HERE / "inputs.json").read_text())
    prior = json.loads((HERE.parent / "placement/results/RESULTS.json").read_text())
    freeze = result["freeze_commit"]
    manifest_raw = (HERE / "manifest.json").read_bytes()
    check(manifest_raw == subprocess.check_output(["git","show",freeze+
        ":experiments/runner-addition/menu-views/manifest.json"],cwd=ROOT),"manifest freeze mismatch")
    for name,digest in json.loads(manifest_raw)["sha256"].items():
        data = (ROOT/name).read_bytes()
        check(hashlib.sha256(data).hexdigest() == digest,"dependency hash mismatch")
        check(data == subprocess.check_output(["git","show",freeze+":"+name],cwd=ROOT),"dependency freeze mismatch")
    check(result["study"] == cfg["study"] and result["source_commit"] == cfg["source_commit"],"identity")
    check([x["pair"] for x in result["records"]] == cfg["pairs"] == [x["pair"] for x in inputs["records"]],"pair domain")
    counts = {"cores":0,"child_sets":0,"contacts":0,"physical_witnesses":0,
              "minimum_subsets":0,"single_component_blockers":0,"time_records":0,"time_predicates":0}
    audits = []
    d = F(cfg["threshold"])
    for source,record in zip(inputs["records"],result["records"]):
        p,q = record["pair"]
        speeds = [p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q]
        check(speeds == record["speeds"] == source["speeds"],"core speeds")
        check(record["threshold"] == source["threshold"] == cfg["threshold"],"threshold identity")
        core,_ = alt.event_set(speeds,d)
        counts["cores"] += 1
        check(core == alt.intervals(source["components"]),"frozen core")
        check(core == [tuple(map(F,c["interval"])) for c in record["components"]],"complete core")
        leader = min(range(len(core)),key=lambda i:(-(core[i][1]-core[i][0]),core[i][0]))
        cutoff = ceil(2*d/(core[leader][1]-core[leader][0]))
        check(leader == source["leader"] == record["leader"] and cutoff == source["cutoff"] == record["cutoff"],"leader/cutoff")
        check(sum(speeds) <= cfg["max_core_speed_sum"] and len(core) <= cfg["max_components"]
              and cutoff <= cfg["max_tail_cutoff"],"input caps")
        domain = [r for r in range(1,cutoff) if r not in speeds]
        check(domain == source["matched_inputs"] == source["necessary_remainder"]
              == [c["r"] for c in record["cases"]],"finite remainder completeness")
        for (a,b),component in zip(core,record["components"]):
            check(F(component["width"]) == b-a,"width")
            check(F(component["center"]) == (a+b)/2 and F(component["half_width"]) == (b-a)/2,"coordinate translation")
            laps = [floor(s*a) for s in speeds]
            phases = [[s*t-lap for s,lap in zip(speeds,laps)] for t in (a,b)]
            check(component["laps"] == laps and [list(map(F,x)) for x in component["endpoint_phases"]] == phases,"core certificate")
            check(all(d <= x <= 1-d for row in phases for x in row),"core endpoint safety")
        incidence = []
        for case in record["cases"]:
            r = case["r"]
            full,_ = alt.event_set(speeds+[r],d)
            counts["child_sets"] += 1
            check(full == alt.intervals(case["full_safe_set"]),"full child set")
            check(case["necessary_remainder"] is True and len(case["contacts"]) == len(core),"case metadata")
            hits = []
            for i,(interval,contact) in enumerate(zip(core,case["contacts"])):
                pieces = alt.clip(full,interval)
                hit = bool(pieces)
                check(i == contact["component"] and hit == contact["hit"],"contact identity")
                check(pieces == alt.intervals(contact["surviving_pieces"]),"surviving pieces")
                t = alt.phase_first(interval[0],r,d)
                check(t == F(contact["candidate"]) and floor(r*t) == contact["lap"],"first contact")
                check(hit == (t <= interval[1]),"contact endpoint")
                if hit:
                    check(alt.safe(speeds+[r],t,d),"unsafe contact")
                z = r*(interval[0]+interval[1])/2
                value = min(z % 1,1-z % 1)+r*(interval[1]-interval[0])/2
                placement = contact["placement"]
                check(F(placement["value"]) == value and (value >= d) == hit,"placement equivalence")
                if hit:
                    check(all(placement[k] is None for k in ("blocking_integer","unsafe_gap","gap_center")),"false blocker")
                else:
                    m = placement["blocking_integer"]
                    check(isinstance(m,int) and r*interval[1]-d < m < r*interval[0]+d,"strict blocker inequalities")
                    gap = ((m-d)/r,(m+d)/r)
                    check(tuple(map(F,placement["unsafe_gap"])) == gap and F(placement["gap_center"]) == F(m,r),"unsafe gap recovery")
                    check(gap[0] < interval[0] <= interval[1] < gap[1],"strict interval containment")
                hits.append(hit)
                counts["contacts"] += 1
            incidence.append(hits)
            mask = sum((1 << i) for i,hit in enumerate(hits) if hit)
            check(case["coverage_mask"] == mask and case["coverage_bits_id_order"] ==
                  "".join("1" if hit else "0" for hit in hits),"coverage encoding")
            check(case["positive_sources_hit"] == any(hit and a < b for hit,(a,b) in zip(hits,core)),"positive source status")
            if full:
                check(F(case["complete_witness"]["time"]) == full[0][0],"complete witness time")
                alt.verify_witness(case["complete_witness"],speeds+[r],d)
                counts["physical_witnesses"] += 1
            else:
                check(case["complete_witness"] is None,"witness on empty set")
            ids = record["menu"]["ids"] or []
            if ids:
                selected = [i for i in ids if hits[i]]
                check(bool(selected),"menu failure")
                chosen = min(selected,key=lambda i:(F(case["contacts"][i]["candidate"]),i))
                check(case["menu_witness"]["component"] == chosen and F(case["menu_witness"]["time"])
                      == F(case["contacts"][chosen]["candidate"]),"menu witness selection")
                alt.verify_witness(case["menu_witness"],speeds+[r],d)
                counts["physical_witnesses"] += 1
            else:
                check(case["menu_witness"] is None,"witness without menu")
        tests,minimum_status = alt.verify_minimum(leader,len(core),incidence,record["menu"],cfg["max_verifier_combinations"])
        counts["minimum_subsets"] += tests
        ids = record["menu"]["ids"] or []
        misses = [r for r,hits in zip(domain,incidence) if not hits[leader]]
        full_misses = [r for r,hits in zip(domain,incidence) if not any(hits)]
        positive_misses = [r for r,hits in zip(domain,incidence) if any(hits) and not any(
            hit and a < b for hit,(a,b) in zip(hits,core))]
        summary = {"finite_cases":len(domain),"core_components":len(core),
                   "positive_components":sum(a < b for a,b in core),"isolated_components":sum(a == b for a,b in core),
                   "core_speed_sum":sum(speeds),"component_queries":len(core)*len(domain),
                   "leader_misses":misses,"full_core_misses":full_misses,"isolated_sources_required":positive_misses,
                   "minimum_menu_size":len(ids) if ids else None,"leader_plus_one_suffices":len(ids) <= 2 if ids else None,
                   "all_r_status":"CANDIDATE_CERTIFICATE" if record["menu"]["status"] == "EXACT" else record["menu"]["status"]}
        check(record["summary"] == summary,"summary fields")
        views = record["views"]
        check(views["component_ids"] == list(range(len(core))) and views["finite_speed_order"] == domain,"view axes")
        check(views["component_case_masks"] == [sum(1 << j for j,hits in enumerate(incidence) if hits[i])
              for i in range(len(core))],"component mask encoding")
        failures = [{"component":i,"blocked_r":[r for r,hits in zip(domain,incidence) if not hits[i]]} for i in ids]
        common = [r for r,hits in zip(domain,incidence) if all(not hits[i] for i in ids)] if ids else None
        check(views["selected_failure_sets"] == failures and views["common_failure_speeds"] == common,"complementarity")
        expected_gaps = [{"r":c["r"],**c["contacts"][leader]["placement"]} for c in record["cases"] if c["r"] in misses]
        check(views["leader_unsafe_gaps"] == expected_gaps,"leader gaps")
        repair_id = next((i for i in sorted((j for j in ids if j != leader),key=lambda j:(core[j][0],j))
                          if misses and alt.safe(speeds+misses,core[i][0],d)),None)
        repair = views["fixed_exception_repair"]
        if repair_id is None:
            check(repair is None,"unexpected fixed repair")
        else:
            check(repair["component"] == repair_id and F(repair["time"]) == core[repair_id][0]
                  and repair["exception_speeds"] == misses,"fixed repair choice")
            check([w["r"] for w in repair["witnesses"]] == misses,"repair witness domain")
            for row in repair["witnesses"]:
                check(F(row["time"]) == core[repair_id][0],"fixed repair time")
                alt.verify_witness(row,speeds+[row["r"]],d)
                counts["physical_witnesses"] += 1
        old = next(x for x in prior["new_records"] if x["pair"] == record["pair"])
        check(core == [tuple(map(F,c["interval"])) for c in old["components"]],"prior lower-bound source")
        all_singles_fail = all(c["status"] == "BLOCKED" for c in old["components"])
        if all_singles_fail:
            for interval,c in zip(core,old["components"]):
                r = c["checks"][-1]["r"]
                check(r not in speeds and alt.phase_first(interval[0],r,d) > interval[1],"prior component blocker")
                counts["single_component_blockers"] += 1
        check(views["minimum_without_forced_leader"] == (2 if len(ids) == 2 and all_singles_fail else None),"unrestricted minimum implication")
        check(views["composition_diagnostic"] == expected_diagnostic(record,cfg["max_composition_trials"]),"composition diagnostic")
        controls = []
        for seed in (cutoff,cutoff+1,10**6+1,10**18+1):
            while seed in speeds:
                seed += 1
            if seed not in controls:
                controls.append(seed)
        check(controls == source["tail_controls"] == [x["r"] for x in record["tail_controls"]],"tail control domain")
        for row in record["tail_controls"]:
            t = alt.phase_first(core[leader][0],row["r"],d)
            check(row["component"] == leader and t == F(row["time"]) and t <= core[leader][1],"tail contact")
            alt.verify_witness(row,speeds+[row["r"]],d)
            counts["physical_witnesses"] += 1
        audits.append({"pair":record["pair"],"minimum_status":minimum_status,"minimum_menu_size":len(ids) if ids else None,
                       "minimum_without_forced_leader":views["minimum_without_forced_leader"]})
    view = result["time_view"]
    selected = next(r for r in result["records"] if r["pair"] == cfg["trace_pair"])
    trace_r = cfg["trace_added_speed"]
    speeds = selected["speeds"]+[trace_r]
    check(view["speeds"] == speeds and F(view["threshold"]) == d,"time-view meaning")
    events = {F(0),F(1)}
    for s in speeds:
        for lap in range(s):
            events.add((lap+d)/s); events.add((lap+1-d)/s)
    events = sorted(events)
    check(list(map(F,view["events"])) == events and len(events) <= cfg["max_event_points"],"time event completeness")
    check(len(view["records"]) == 2*len(events)-1,"time record count")
    full_mask = (1 << len(speeds))-1
    check(view["full_mask"] == full_mask,"time full mask")
    decoded = []
    for i,row in enumerate(view["records"]):
        point = i % 2 == 0
        left,right = events[i//2],events[i//2] if point else events[i//2+1]
        check(row["id"] == i and row["kind"] == ("point" if point else "open_cell"),"time record identity")
        check((F(row["left"]),F(row["right"])) == (left,right) and F(row["time"]) == (left+right)/2,"time coordinates")
        flags = [band_state(s,left,right,d,point) for s in speeds]
        mask = sum(1 << j for j,flag in enumerate(flags) if flag)
        check(row["mask"] == mask and row["bits_speed_order"] == "".join("1" if b else "0" for b in flags),"time state meaning")
        if mask == full_mask:
            decoded.append((left,right))
        counts["time_records"] += 1; counts["time_predicates"] += len(speeds)
    decoded = alt.join(decoded)
    check(decoded == alt.intervals(view["decoded_safe_set"]),"decoded time union")
    case = next(c for c in selected["cases"] if c["r"] == trace_r)
    check(decoded == alt.intervals(case["full_safe_set"]),"time/geometry conformance")
    old = next(r for r in prior["new_records"] if r["pair"] == cfg["trace_pair"])
    saved = next(r for r in old["children_at_blockers"] if r["r"] == trace_r)
    check(decoded == alt.intervals(saved["full_safe_set"]),"saved time case")
    leader_interval = tuple(map(F,selected["components"][selected["leader"]]["interval"]))
    first = tuple(map(F,saved["full_safe_set"][0]))
    boundaries = [("leader_start",leader_interval[0]),("leader_end",leader_interval[1]),
                  ("recovery_start",first[0]),("recovery_end",first[1])]
    check(len(view["focus"]) == len(boundaries),"focus count")
    for focus,(name,t) in zip(view["focus"],boundaries):
        at = 2*events.index(t)
        check(focus["name"] == name and F(focus["time"]) == t and
              (focus["before_id"],focus["point_id"],focus["after_id"]) == (at-1,at,at+1),"focus identity")
        before,point,after = [view["records"][j]["bits_speed_order"] for j in (at-1,at,at+1)]
        check(focus["become_true_at"] == [s for s,b,p in zip(speeds,before,point) if b == "0" and p == "1"],"entering conditions")
        check(focus["become_false_after"] == [s for s,p,a in zip(speeds,point,after) if p == "1" and a == "0"],"leaving conditions")
    check(alt.event_set([1,2],F(1,3))[0] == [(F(1,3),F(1,3)),(F(2,3),F(2,3))]
          and result["singleton_fixture"] == "PASS","isolated-time fixture")
    status = "PASS" if all(a["minimum_status"] in ("EXACT_VERIFIED","NO_SUFFICIENT_MENU") for a in audits) else "VERIFIED_WITH_UNRESOLVED_MINIMA"
    return {"status":status,"freeze_commit":freeze,"counts":counts,"families":audits,
            "results_sha256":hashlib.sha256(raw).hexdigest(),
            "limits":"Same-author alternate algorithms; no independent human or formal proof review."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,default=HERE / "results/RESULTS.json")
    parser.add_argument("--output",type=Path,default=HERE / "results/VERIFICATION.json")
    args = parser.parse_args()
    check(not args.output.exists(),"refusing to overwrite verification")
    result = verify(args.input)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2))
