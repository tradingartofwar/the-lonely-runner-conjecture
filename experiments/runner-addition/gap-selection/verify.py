"""Alternate event-set and subset verifier. Does not import the primary path."""
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
spec = importlib.util.spec_from_file_location("gap_alternate_events", HERE.parent / "verify.py")
alt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alt)
check = alt.check


def verify_gap(gap, core, failures, d, common, cap):
    status = gap["status"]
    if status == "LEADER_ONLY":
        check(not failures and not gap["trace"], "invalid leader-only gap")
        check(gap["component"] is None and gap["time"] is None, "spurious repair point")
        check(gap["point_tests"] == gap["jumps"] == gap["components_visited"] == 0, "nonzero empty work")
        return
    check(bool(failures), "gap search without failures")
    if status != "UNKNOWN_BUDGET":
        check(status == ("FOUND" if common else "NO_COMMON_REPAIR_POINT"), "common-set status mismatch")
        if common:
            t = common[0][0]
            i = next(i for i, (a,b) in enumerate(core) if a <= t <= b)
            check(F(gap["time"]) == t and gap["component"] == i, "not earliest common repair")
        else:
            check(gap["time"] is None and gap["component"] is None, "point on empty common set")
    else:
        check(gap["point_tests"] == cap, "gap budget not exhausted")
        check(gap["time"] is None and gap["component"] is None, "point after budget stop")
    visits = gap["trace"]
    if status == "FOUND":
        check(bool(visits) and visits[-1]["component"] == gap["component"], "missing successful gap trace")
    check([v["component"] for v in visits] == list(range(len(visits))), "skipped gap component")
    check(len(visits) <= len(core), "extra gap component")
    probes = jumps = 0
    for index, visit in enumerate(visits):
        a,b = core[index]
        t, cursor = a, 0
        done = False
        for row in visit["probes"]:
            check(not done and t <= b and cursor < len(failures), "probe after completion")
            r = failures[cursor]
            check(row["r"] == r and F(row["time"]) == t, "gap probe order/time")
            ok = alt.safe([r], t, d)
            check(row["safe"] == ok, "incorrect point predicate")
            probes += 1
            if ok:
                check(row["blocking_integer"] is None and row["jump_to"] is None, "jump from safe point")
                cursor += 1
                done = cursor == len(failures)
            else:
                m = row["blocking_integer"]
                check(type(m) is int, "noninteger blocking label")
                left, right = (m-d)/r, (m+d)/r
                check(left < t < right and F(row["jump_to"]) == right, "invalid skipped unsafe gap")
                t, cursor = right, 0
                jumps += 1
        last = index == len(visits)-1
        if done:
            check(last and status == "FOUND" and F(gap["time"]) == t, "unreturned completed search")
        elif t <= b:
            check(last and status == "UNKNOWN_BUDGET", "premature component stop")
    if status == "NO_COMMON_REPAIR_POINT":
        check(len(visits) == len(core), "incomplete negative gap search")
    check(probes == gap["point_tests"] <= cap, "gap probe accounting")
    check(jumps == gap["jumps"] and len(visits) == gap["components_visited"], "gap trace accounting")


def verify_lazy(lazy, core, failures, d, sets, cap, leader=None):
    status = lazy["status"]
    if status == "LEADER_ONLY":
        check(not failures and not lazy["trace"] and lazy["component"] is None, "invalid lazy leader-only")
        check(lazy["interval_tests"] == lazy["components_visited"] == 0, "empty lazy work")
        return
    order = [i for i in range(len(core)) if i != leader]
    good = [i for i in order if all(alt.clip(sets[r], core[i]) for r in failures)]
    if status != "UNKNOWN_BUDGET":
        check(status == ("FOUND" if good else "NO_TWO_COMPONENT_MENU"), "lazy exact eligibility mismatch")
        check(lazy["component"] == (good[0] if good else None), "lazy first eligible component")
    else:
        check(lazy["interval_tests"] == cap and lazy["component"] is None, "lazy budget accounting")
    visits = lazy["trace"]
    if status == "FOUND":
        check(bool(visits) and visits[-1]["component"] == lazy["component"], "missing successful lazy trace")
    check([v["component"] for v in visits] == order[:len(visits)], "lazy ordering")
    tests = 0
    for k, visit in enumerate(visits):
        a,b = core[visit["component"]]
        stopped = False
        rows = visit["contacts"]
        check(len(rows) <= len(failures), "extra lazy contact")
        for j, row in enumerate(rows):
            check(not stopped and row["r"] == failures[j], "lazy short circuit/order")
            r = row["r"]
            t = alt.phase_first(a, r, d)
            hit = bool(alt.clip(sets[r], (a,b)))
            check(F(row["candidate"]) == t and row["lap"] == floor(r*t), "lazy contact value")
            check(row["hit"] == hit == (t <= b), "lazy contact Boolean")
            tests += 1
            stopped = not hit
        if not stopped:
            if len(rows) == len(failures):
                check(k == len(visits)-1 and status == "FOUND", "unreturned lazy success")
            else:
                check(k == len(visits)-1 and status == "UNKNOWN_BUDGET", "premature lazy stop")
    if status == "NO_TWO_COMPONENT_MENU":
        check(len(visits) == len(order), "incomplete lazy rejection")
    check(tests == lazy["interval_tests"] <= cap and len(visits) == lazy["components_visited"], "lazy costs")


def verify_recovery(method, selection, rec, source, failures, core, d, counts):
    ids = selection["ids"]
    if ids is None:
        check(rec == {"status":"NO_SELECTOR_CERTIFICATE", "finite":[], "tail":[],
                      "finite_first_contact_calls":0, "tail_first_contact_calls":0}, "recovery without certificate")
        return
    check(rec["status"] == "RECOVERED", "missing recovery")
    for kind, domain in (("finite",source["matched_inputs"]),("tail",source["tail_controls"])):
        rows, calls = rec[kind], 0
        check([x["r"] for x in rows] == domain, "incomplete recovery domain")
        for row in rows:
            r = row["r"]
            if method == "gap" and r in failures:
                expected = (F(selection["time"]), selection["component"])
            else:
                chosen = ids if method == "exact" else [selection["component"] if r in failures else source["leader"]]
                candidates = [(alt.phase_first(core[i][0],r,d),i) for i in chosen]
                calls += len(chosen)
                expected = min((t,i) for t,i in candidates if t <= core[i][1])
            check((F(row["time"]),row["component"]) == expected, "wrong recovery dispatch")
            a,b = core[row["component"]]
            check(a <= F(row["time"]) <= b, "witness outside selected component")
            alt.verify_witness(row, source["speeds"]+[r], d)
            counts["physical_witnesses"] += 1
        check(calls == rec[kind+"_first_contact_calls"], "recovery contact accounting")


def verify_record(record, pair, cfg, counts):
    p,q = pair
    speeds = [p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q]
    check(record["pair"] == pair and record["speeds"] == speeds and len(set([0]+speeds)) == 9, "core identity")
    d = F(cfg["threshold"])
    if sum(speeds) > cfg["max_core_speed_sum"]:
        check(record["status"] == "UNKNOWN_CORE_BUDGET", "core budget status")
        return {"pair":pair,"status":record["status"]}
    core, events = alt.event_set(speeds, d)
    counts["core_sets"] += 1
    counts["events"] += events
    check(core == alt.intervals(record["core"]), "complete core discrepancy")
    check(record["core_input_bands"] == sum(speeds) and record["core_components"] == len(core), "core cost")
    unsupported = "UNSUPPORTED_EMPTY_CORE" if not core else None
    if len(core) > cfg["max_components"]:
        unsupported = "UNKNOWN_COMPONENT_BUDGET"
    if unsupported:
        check(record["status"] == unsupported, "unsupported core status")
        return {"pair":pair,"status":unsupported}
    leader = min(range(len(core)), key=lambda i:(-(core[i][1]-core[i][0]),core[i][0]))
    width = core[leader][1]-core[leader][0]
    if not width:
        check(record["status"] == "UNSUPPORTED_ZERO_WIDTH", "zero width status")
        return {"pair":pair,"status":record["status"]}
    cutoff = ceil(2*d/width)
    if cutoff > cfg["max_tail_cutoff"]:
        check(record["status"] == "UNKNOWN_DOMAIN_BUDGET" and record["leader"] == leader and record["cutoff"] == cutoff,
              "domain budget status")
        return {"pair":pair,"status":record["status"]}
    check(record["status"] == "EVALUATED", "missing evaluation")
    domain = [r for r in range(1,cutoff) if r not in speeds]
    controls = []
    for seed in (cutoff,cutoff+1,10**6+1,10**18+1):
        r = seed
        while r in speeds:
            r += 1
        if r not in controls:
            controls.append(r)
    source = record["source"]
    check(source["pair"] == pair and source["speeds"] == speeds and source["threshold"] == cfg["threshold"], "source identity")
    check(alt.intervals(source["components"]) == core and source["leader"] == leader and source["cutoff"] == cutoff, "source geometry")
    check(source["matched_inputs"] == source["necessary_remainder"] == domain and source["tail_controls"] == controls, "derived domain")
    exact = record["exact"]
    check(exact["pair"] == pair and exact["speeds"] == speeds and exact["threshold"] == cfg["threshold"], "reference identity")
    check(exact["leader"] == leader and exact["cutoff"] == cutoff and len(exact["components"]) == len(core), "reference source")
    for interval, cert in zip(core,exact["components"]):
        check(tuple(map(F,cert["interval"])) == interval and F(cert["width"]) == interval[1]-interval[0], "component certificate")
        laps = [floor(v*interval[0]) for v in speeds]
        phases = [[v*t-j for v,j in zip(speeds,laps)] for t in interval]
        check(cert["laps"] == laps and [list(map(F,row)) for row in cert["endpoint_phases"]] == phases, "component laps/phases")
        check(all(d <= x <= 1-d for row in phases for x in row), "unsafe core endpoint")
    check([c["r"] for c in exact["cases"]] == domain, "reference finite domain")
    sets, incidence, failures, full_misses, isolated = {}, [], [], [], []
    for case in exact["cases"]:
        r = case["r"]
        full, events = alt.event_set(speeds+[r],d)
        sets[r] = full
        counts["child_sets"] += 1
        counts["events"] += events
        check(full == alt.intervals(case["full_safe_set"]), "complete child discrepancy")
        check(case["necessary_remainder"] is True and len(case["contacts"]) == len(core), "case shape")
        hits = []
        for i,(a,b) in enumerate(core):
            contact = case["contacts"][i]
            pieces = alt.clip(full,(a,b))
            t = alt.phase_first(a,r,d)
            check(contact["component"] == i and alt.intervals(contact["surviving_pieces"]) == pieces, "contact geometry")
            check(contact["hit"] == bool(pieces) == (t <= b), "contact existence")
            check(F(contact["candidate"]) == t and contact["lap"] == floor(r*t), "first contact value")
            if pieces:
                check(pieces[0][0] == t and alt.safe(speeds+[r],t,d), "first contact safety")
            hits.append(bool(pieces))
            counts["component_contacts"] += 1
        incidence.append(hits)
        positive = any(hit and a < b for hit,(a,b) in zip(hits,core))
        check(case["positive_sources_hit"] == positive, "positive component summary")
        if not hits[leader]:
            failures.append(r)
        if full:
            check(F(case["complete_witness"]["time"]) == full[0][0], "first complete witness")
            alt.verify_witness(case["complete_witness"],speeds+[r],d)
            counts["physical_witnesses"] += 1
            if not positive:
                isolated.append(r)
        else:
            full_misses.append(r)
            check(case["complete_witness"] is None, "witness on empty child")
        ids = exact["menu"]["ids"]
        if ids:
            expected = min((alt.phase_first(core[i][0],r,d),i) for i in ids if hits[i])
            witness = case["menu_witness"]
            check((F(witness["time"]),witness["component"]) == expected, "reference menu witness")
            alt.verify_witness(witness,speeds+[r],d)
            counts["physical_witnesses"] += 1
        else:
            check(case["menu_witness"] is None, "menu witness without menu")
    tests, minimum_status = alt.verify_minimum(leader,len(core),incidence,exact["menu"],cfg["max_verifier_combinations"])
    counts["minimum_subsets"] += tests
    check(record["failures"] == failures, "leader failure list")
    check([x["r"] for x in record["leader_classification"]] == domain, "leader classification domain")
    a,b = core[leader]
    for row,hits in zip(record["leader_classification"],incidence):
        r = row["r"]
        z = r*(a+b)/2
        value = min(z%1,1-z%1)+r*(b-a)/2
        check(F(row["value"]) == value and row["hit"] == hits[leader] == (value >= d), "placement predicate")
        if row["hit"]:
            check(row["blocking_integer"] is None and row["unsafe_gap"] is None, "gap on hit")
        else:
            m = row["blocking_integer"]
            check(type(m) is int and r*b-d < m < r*a+d, "blocking integer not strict")
            check(tuple(map(F,row["unsafe_gap"])) == ((m-d)/r,(m+d)/r), "leader gap endpoints")
    check([x["r"] for x in exact["tail_controls"]] == controls, "tail controls domain")
    for row in exact["tail_controls"]:
        t = alt.phase_first(a,row["r"],d)
        check(a <= t <= b and F(row["time"]) == t and row["component"] == leader, "tail contact")
        alt.verify_witness(row,speeds+[row["r"]],d)
        counts["physical_witnesses"] += 1
    summary = exact["summary"]
    expected_summary = {"finite_cases":len(domain),"core_components":len(core),
        "positive_components":sum(a < b for a,b in core),"isolated_components":sum(a == b for a,b in core),
        "core_speed_sum":sum(speeds),"component_queries":len(core)*len(domain),
        "leader_misses":failures,"full_core_misses":full_misses,"isolated_sources_required":isolated,
        "minimum_menu_size":len(exact["menu"]["ids"]) if exact["menu"]["ids"] else None,
        "leader_plus_one_suffices":len(exact["menu"]["ids"]) <= 2 if exact["menu"]["ids"] else None,
        "all_r_status":"CANDIDATE_CERTIFICATE" if exact["menu"]["status"] == "EXACT" else exact["menu"]["status"]}
    check(summary == expected_summary, "reference summary mismatch")
    common = []
    if failures:
        common, events = alt.event_set(speeds+failures,d)
        counts["common_repair_sets"] += 1
        counts["events"] += events
    verify_gap(record["gap"],core,failures,d,common,cfg["max_gap_probes"])
    verify_lazy(record["lazy"],core,failures,d,sets,cfg["max_lazy_contacts"],leader)
    for name in ("gap","lazy"):
        sel = record[name]
        ids = ([leader] if not failures else sorted([leader,sel["component"]])) if sel["status"] in ("FOUND","LEADER_ONLY") else None
        check(sel["ids"] == ids, "selected menu identity")
        if ids:
            check(all(any(h[i] for i in ids) for h in incidence), "selected menu miss")
        verify_recovery(name,sel,record["recovery"][name],source,failures,core,d,counts)
    verify_recovery("exact",exact["menu"],record["recovery"]["exact"],source,failures,core,d,counts)
    sizes = {name:len(record[name]["ids"]) if record[name]["ids"] else None for name in ("gap","lazy")}
    exact_size = expected_summary["minimum_menu_size"]
    expected_comparison = {"exact_size":exact_size,"selector_sizes":sizes,
        "equal_minimum":{name:size == exact_size if size is not None and exact_size is not None else None for name,size in sizes.items()},
        "common_point_miss_despite_two_menu":record["gap"]["status"] == "NO_COMMON_REPAIR_POINT" and record["lazy"]["status"] == "FOUND"}
    check(record["comparison"] == expected_comparison, "comparison summary")
    expected_cost = {"shared_leader_tests":len(domain),"gap_point_tests":record["gap"]["point_tests"],
        "gap_jumps":record["gap"]["jumps"],"lazy_interval_tests":record["lazy"]["interval_tests"],
        "full_matrix_contacts":len(core)*len(domain),"dp_states":exact["menu"]["states"],"dp_transitions":exact["menu"]["transitions"]}
    check(record["cost"] == expected_cost, "cost summary mismatch")
    # DP counters are bounded execution instrumentation, not independently replayed by subset enumeration.
    if exact["menu"]["status"] == "EXACT":
        check(exact["menu"]["states"] <= cfg["max_dp_states"] and exact["menu"]["transitions"] <= cfg["max_dp_transitions"], "DP budget")
    return {"pair":pair,"status":"VERIFIED","minimum_status":minimum_status,
            "comparison":expected_comparison,"common_repair_set":common,
            "gap_status":record["gap"]["status"],"lazy_status":record["lazy"]["status"]}


def verify(path):
    raw = path.read_bytes()
    result = json.loads(raw)
    cfg = json.loads((HERE / "config.json").read_text())
    freeze = result["freeze_commit"]
    manifest_raw = (HERE / "manifest.json").read_bytes()
    prefix = "experiments/runner-addition/gap-selection/"
    check(manifest_raw == subprocess.check_output(["git","show",freeze+":"+prefix+"manifest.json"],cwd=ROOT), "manifest changed")
    for p,h in json.loads(manifest_raw)["sha256"].items():
        data = (ROOT/p).read_bytes()
        check(hashlib.sha256(data).hexdigest() == h, "dependency changed")
        check(data == subprocess.check_output(["git","show",freeze+":"+p],cwd=ROOT), "archive mismatch")
    check(result["study"] == cfg["study"] and result["rule_commit"] == cfg["rule_commit"], "study identity")
    check(len(result["records"]) == len(cfg["pairs"]), "record count")
    counts = {"core_sets":0,"child_sets":0,"common_repair_sets":0,"events":0,
              "component_contacts":0,"physical_witnesses":0,"minimum_subsets":0}
    records = [verify_record(r,p,cfg,counts) for r,p in zip(result["records"],cfg["pairs"])]
    fixtures = result["semantic_controls"]
    check(len(fixtures) == 2, "fixture count")
    expected = [("touching_open_gaps",[(F(3,10),F(2,5))],[1,2],F(1,3)),
                ("separate_not_joint",[(F(111,670),F(19,110))],[17,18],F(1,10))]
    for item,(name,core,speeds,d) in zip(fixtures,expected):
        check(item["name"] == name and alt.intervals(item["core"]) == core and item["speeds"] == speeds and F(item["d"]) == d, "fixture identity")
        common = alt.join([p for interval in core for p in alt.clip(alt.event_set(speeds,d)[0],interval)])
        sets = {r:alt.event_set([r],d)[0] for r in speeds}
        verify_gap(item["gap"],core,speeds,d,common,cfg["max_gap_probes"])
        verify_lazy(item["lazy"],core,speeds,d,sets,cfg["max_lazy_contacts"])
        check(common == ([(F(1,3),F(1,3))] if name == "touching_open_gaps" else []), "fixture semantics")
        check(item["lazy"]["status"] == "FOUND", "fixture lost separate feasibility")
    resolved = all(r["status"] == "VERIFIED" and r["minimum_status"] == "EXACT_VERIFIED" and
                   r["gap_status"] != "UNKNOWN_BUDGET" and r["lazy_status"] != "UNKNOWN_BUDGET" for r in records)
    return {"status":"PASS" if resolved else "VERIFIED_WITH_UNRESOLVED_CASES", "freeze_commit":freeze,
            "results_sha256":hashlib.sha256(raw).hexdigest(),"counts":counts,"records":records,"semantic_controls":2,
            "limits":"Same-author alternate algorithms; no independent human/formal review. DP operation counters are instrumentation, not independently reproduced by subset enumeration."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,default=HERE / "results/RESULTS.json")
    parser.add_argument("--output",type=Path,default=HERE / "results/VERIFICATION.json")
    args = parser.parse_args()
    check(not args.output.exists(),"refusing to overwrite verification")
    result = verify(args.input)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result,default=str,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,default=str,indent=2))
