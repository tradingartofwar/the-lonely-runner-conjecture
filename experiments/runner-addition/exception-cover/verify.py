"""Alternate exact sets/subsets and specification-level query-trace audit."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import ceil, floor, gcd
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


alt = load("exception_event_verifier",HERE.parent / "verify.py")
gv = load("exception_gap_trace_verifier",HERE.parent / "gap-selection/verify.py")
check = alt.check


def canon(x):
    return json.loads(json.dumps(x,default=str))


def reference(ref,core,leader,domain,d,speeds,cfg,counts,family=False):
    check([x["r"] for x in ref["cases"]] == domain,"reference query domain")
    incidence = []
    full_sets = {}
    for case in ref["cases"]:
        r = case["r"]
        if family:
            full,events = alt.event_set(speeds+[r],d)
            counts["child_sets"] += 1
        else:
            allowed,events = alt.event_set([r],d)
            full = alt.join([p for interval in core for p in alt.clip(allowed,interval)])
        full_sets[r] = full
        check(alt.intervals(case["full_safe_set"]) == full,"reference complete set")
        check(len(case["contacts"]) == len(core),"reference contact count")
        hits = []
        for i,(a,b) in enumerate(core):
            contact = case["contacts"][i]
            pieces = alt.clip(full,(a,b))
            t = alt.phase_first(a,r,d)
            check(contact["component"] == i,"contact source label")
            check(contact["hit"] == bool(pieces) == (t <= b),"reference hit")
            check(F(contact["candidate"]) == t and contact["lap"] == floor(r*t),"reference first contact")
            check(alt.intervals(contact["surviving_pieces"]) == pieces,"reference surviving pieces")
            if pieces:
                check(t == pieces[0][0] and alt.safe(speeds+[r],t,d),"contact witness")
            hits.append(bool(pieces))
            counts["reference_contacts"] += 1
        incidence.append(hits)
        if family:
            check(case["necessary_remainder"] is True,"incorrect remainder label")
            check(case["positive_sources_hit"] == any(hit and a < b for hit,(a,b) in zip(hits,core)),"positive-source label")
            if full:
                check(F(case["complete_witness"]["time"]) == full[0][0],"earliest full witness")
                alt.verify_witness(case["complete_witness"],speeds+[r],d)
                counts["physical_witnesses"] += 1
            else:
                check(case["complete_witness"] is None,"witness on empty set")
            ids = ref["menu"]["ids"]
            if ids:
                t,i = min((alt.phase_first(core[i][0],r,d),i) for i in ids if hits[i])
                w = case["menu_witness"]
                check(F(w["time"]) == t and w["component"] == i,"reference menu witness")
                alt.verify_witness(w,speeds+[r],d)
                counts["physical_witnesses"] += 1
            else:
                check(case["menu_witness"] is None,"witness without reference menu")
    tests,status = alt.verify_minimum(leader,len(core),incidence,ref["menu"],cfg["max_verifier_combinations"])
    counts["minimum_subsets"] += tests
    return incidence,full_sets,status


def audit_requests(core,leader,domain,incidence,cfg):
    """Replay the declared query ORDER from independently computed hit bits."""
    hits = {r:row for r,row in zip(domain,incidence)}
    seen,expected,failures = set(),[],[]
    reuses,complete,stage = 0,False,"LEADER"

    class Stop(Exception):
        pass

    def ask(i,r,label):
        nonlocal reuses
        if (i,r) in seen:
            reuses += 1
        else:
            if len(seen) >= cfg["max_contact_queries"]:
                raise Stop()
            seen.add((i,r))
            expected.append((i,r,label))
        return hits[r][i]

    try:
        for r in domain:
            if not ask(leader,r,"leader"):
                failures.append(r)
        complete = True
        if not failures:
            return expected,reuses,failures,complete,"LEADER_ONLY"
        stage = "LAZY"
        for i in range(len(core)):
            if i != leader and all(ask(i,r,"lazy") for r in failures):
                return expected,reuses,failures,complete,"LAZY_TWO"
        stage = "RESIDUAL_FILL"
        for i in range(len(core)):
            if i != leader:
                for r in failures:
                    ask(i,r,"residual")
        route = "RESIDUAL_DP" if all(any(hits[r]) for r in failures) else "RESIDUAL_NO_COVER"
        return expected,reuses,failures,complete,route
    except Stop:
        return expected,reuses,failures,complete,stage


def compiled(result,core,leader,domain,d,incidence,cfg,ref_menu,context,counts):
    expected,reuses,failures,complete,route = audit_requests(core,leader,domain,incidence,cfg)
    check(result["failures"] == failures and result["classification_complete"] == complete,"failure classification")
    check(result["route"] == route,"constructor route")
    rows = result["queries"]
    check([(x["component"],x["r"],x["stage"]) for x in rows] == expected,"query order/short circuit")
    check(len({(x["component"],x["r"]) for x in rows}) == len(rows),"duplicate evaluated contact")
    lookup = {r:h for r,h in zip(domain,incidence)}
    for row in rows:
        i,r = row["component"],row["r"]
        t = alt.phase_first(core[i][0],r,d)
        check(F(row["candidate"]) == t and row["lap"] == floor(r*t),"queried contact value")
        check(row["hit"] == lookup[r][i] == (t <= core[i][1]),"queried contact Boolean")
        check(i == leader or r in failures,"nonleader nonexception queried")
    counter = Counter(x["stage"] for x in rows)
    expected_cost = {k:counter[k] for k in ("leader","lazy","residual")}
    expected_cost.update({"unique":len(rows),"cache_reuses":reuses})
    check(result["query_costs"] == expected_cost,"query accounting")
    check(len(rows) <= cfg["max_contact_queries"],"query budget exceeded")
    counts["constructor_contacts"] += len(rows)
    status = result["status"]
    if route in ("LEADER","LAZY","RESIDUAL_FILL"):
        check(status == "UNKNOWN_BUDGET" and len(rows) == cfg["max_contact_queries"],"unjustified contact stop")
    elif route == "RESIDUAL_NO_COVER":
        check(status == "NO_SUFFICIENT_MENU","missing no-cover result")
    elif route in ("LEADER_ONLY","LAZY_TWO"):
        check(status == "EXACT","failed fast path")
    else:
        check(result["dp"] is not None and result["dp"]["status"] == status and result["dp"]["ids"] == result["ids"],"DP identity")
        dp = result["dp"]
        check(0 <= dp["states"] <= cfg["max_dp_states"] and 0 <= dp["transitions"] <= cfg["max_dp_transitions"],"DP cap")
        if status == "UNKNOWN_BUDGET":
            check((dp["reason"] == "transitions" and dp["transitions"] == cfg["max_dp_transitions"]) or
                  (dp["reason"] == "states" and dp["states"] == cfg["max_dp_states"]),"unjustified DP stop")
    if route in ("RESIDUAL_DP","RESIDUAL_NO_COVER"):
        masks = [{"component":i,"mask":sum(1 << j for j,r in enumerate(failures) if lookup[r][i])}
                 for i in range(len(core)) if i != leader]
        check(result["residual_masks"] == masks,"residual masks")
        missing = [r for r in failures if not any(lookup[r])]
        check(result["uncovered_speeds"] == missing,"uncovered query list")
    else:
        check(result["residual_masks"] is None and not result["uncovered_speeds"] and result["dp"] is None,"spurious fallback data")
    if status != "UNKNOWN_BUDGET" and ref_menu["status"] != "UNKNOWN_BUDGET":
        check(status == ref_menu["status"] and result["ids"] == ref_menu["ids"],"minimum/tie discrepancy")
    certificate = result["certificate"]
    optional = result["optional_common"]
    if status != "EXACT":
        check(result["ids"] is None and certificate is None,"certificate on unresolved/empty cover")
        check(optional == {"status":"NOT_ATTEMPTED","component":None,"search":None},"optional search without cover")
        return
    ids = result["ids"]
    check(leader in ids and ids == sorted(set(ids)) and all(any(row[i] for i in ids) for row in incidence),"invalid menu")
    table = []
    for r in failures:
        i = next(i for i in ids if lookup[r][i])
        check(any(x["component"] == i and x["r"] == r for x in rows),"uncached exception witness")
        table.append({"r":r,"component":i,"time":alt.phase_first(core[i][0],r,d)})
    common = None
    if len(ids) == 2:
        j = next(i for i in ids if i != leader)
        safe_set = alt.clip(alt.event_set(failures,d)[0],core[j])
        check(optional["component"] == j and optional["status"] == optional["search"]["status"],"optional identity")
        gv.verify_gap(optional["search"],[core[j]],failures,d,safe_set,cfg["max_gap_probes"])
        counts["optional_sets"] += 1
        if optional["status"] == "FOUND":
            common = {"component":j,"time":safe_set[0][0]}
    else:
        check(optional == {"status":"NOT_ATTEMPTED","component":None,"search":None},"unexpected common query")
    wanted = {"threshold":d,"domain":domain,"leader":{"component":leader,"interval":core[leader]},
              "menu":[{"component":i,"interval":core[i]} for i in ids],"exception_table":table,
              "common_repair":common,"family_context":context}
    check(certificate == canon(wanted),"certificate payload")


def recovery(record,core,domains,speeds,d,counts):
    result = record["constructor"]
    saved = record["recovery"]
    cert = result["certificate"]
    check(saved["status"] == ("RECOVERED" if cert else "NO_CERTIFICATE"),"recovery status")
    check(set(saved["domains"]) == set(domains),"recovery domain names")
    for name,domain in domains.items():
        output = saved["domains"][name]
        rows = output["witnesses"]
        check([x["r"] for x in rows] == (domain if cert else []),"dispatch query domain")
        calls = 0
        for row in rows:
            r = row["r"]
            exception = next((x for x in cert["exception_table"] if x["r"] == r),None)
            if exception:
                point = cert["common_repair"] or exception
                t,i = F(point["time"]),point["component"]
            else:
                i = cert["leader"]["component"]
                t = alt.phase_first(core[i][0],r,d)
                calls += 1
            check(F(row["time"]) == t and row["component"] == i and core[i][0] <= t <= core[i][1],"dispatch value")
            alt.verify_witness(row,speeds+[r],d)
            counts["physical_witnesses"] += 1
        check(output["first_contact_calls"] == calls,"dispatch accounting")
    guards = record["guard_checks"]
    if cert:
        other = speeds[0] if speeds else next(r for r in range(1,len(cert["domain"])+2) if r not in cert["domain"])
        check([x["r"] for x in guards] == [0,other] and all(x["status"] == "REJECTED" and x["reason"] for x in guards),"dispatcher guard evidence")
    else:
        check(guards == [],"guards without certificate")


def family(record,pair,cfg,counts):
    p,q = pair
    speeds = [p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q]
    d = F(cfg["threshold"])
    check(record["pair"] == pair and record["speeds"] == speeds and F(record["threshold"]) == d,"family identity")
    check(gcd(p,q) == 1 and len(set([0]+speeds)) == 9,"primitive distinct core")
    if sum(speeds) > cfg["max_core_speed_sum"]:
        check(record["status"] == "UNKNOWN_CORE_BUDGET","core budget status")
        return {"pair":pair,"status":record["status"]}
    core,_ = alt.event_set(speeds,d)
    counts["core_sets"] += 1
    check(alt.intervals(record["core"]) == core and record["core_input_bands"] == sum(speeds),"core geometry/cost")
    if not core or len(core) > cfg["max_components"]:
        expected = "UNSUPPORTED_EMPTY_CORE" if not core else "UNKNOWN_COMPONENT_BUDGET"
        check(record["status"] == expected,"unsupported core")
        return {"pair":pair,"status":expected}
    leader = min(range(len(core)),key=lambda i:(-(core[i][1]-core[i][0]),core[i][0]))
    width = core[leader][1]-core[leader][0]
    if not width:
        check(record["status"] == "UNSUPPORTED_ZERO_WIDTH","zero width")
        return {"pair":pair,"status":record["status"]}
    cutoff = ceil(2*d/width)
    if cutoff > cfg["max_tail_cutoff"]:
        check(record["status"] == "UNKNOWN_DOMAIN_BUDGET" and record["cutoff"] == cutoff,"cutoff budget")
        return {"pair":pair,"status":record["status"]}
    check(record["status"] == "EVALUATED","family not evaluated")
    domain = [r for r in range(1,cutoff) if r not in speeds]
    tail = []
    for seed in (cutoff,cutoff+1,10**6+1,10**18+1):
        r = seed
        while r in speeds:
            r += 1
        if r not in tail:
            tail.append(r)
    source = {"pair":pair,"speeds":speeds,"threshold":str(d),"components":core,"leader":leader,
              "cutoff":cutoff,"matched_inputs":domain,"necessary_remainder":domain,"tail_controls":tail}
    check(record["source"] == canon(source),"complete source contract")
    ref = record["reference"]
    check(ref["pair"] == pair and ref["speeds"] == speeds and ref["threshold"] == str(d) and
          ref["leader"] == leader and ref["cutoff"] == cutoff,"reference identity")
    check(len(ref["components"]) == len(core),"core certificate count")
    for (a,b),cert in zip(core,ref["components"]):
        laps = [floor(v*a) for v in speeds]
        phases = [[v*t-j for v,j in zip(speeds,laps)] for t in (a,b)]
        expected = {"interval":[a,b],"width":b-a,"laps":laps,"endpoint_phases":phases}
        check(cert == canon(expected) and all(d <= x <= 1-d for row in phases for x in row),"core band certificate")
    incidence,sets,minimum_status = reference(ref,core,leader,domain,d,speeds,cfg,counts,True)
    failures = [r for r,row in zip(domain,incidence) if not row[leader]]
    full_misses = [r for r in domain if not sets[r]]
    isolated = [r for r,row in zip(domain,incidence) if sets[r] and not any(hit and a < b for hit,(a,b) in zip(row,core))]
    ids = ref["menu"]["ids"]
    expected_summary = {"finite_cases":len(domain),"core_components":len(core),"positive_components":sum(a < b for a,b in core),
        "isolated_components":sum(a == b for a,b in core),"core_speed_sum":sum(speeds),"component_queries":len(core)*len(domain),
        "leader_misses":failures,"full_core_misses":full_misses,"isolated_sources_required":isolated,
        "minimum_menu_size":len(ids) if ids else None,"leader_plus_one_suffices":len(ids) <= 2 if ids else None,
        "all_r_status":"CANDIDATE_CERTIFICATE" if ref["menu"]["status"] == "EXACT" else ref["menu"]["status"]}
    check(ref["summary"] == expected_summary,"reference summary")
    check([x["r"] for x in ref["tail_controls"]] == tail,"reference tail domain")
    for row in ref["tail_controls"]:
        t = alt.phase_first(core[leader][0],row["r"],d)
        check(F(row["time"]) == t and row["component"] == leader and t <= core[leader][1],"reference tail witness")
        alt.verify_witness(row,speeds+[row["r"]],d)
        counts["physical_witnesses"] += 1
    context = {"core_speeds":speeds,"reference":0,"total_runners":10,"period":[0,1],"tail_from":cutoff}
    compiled(record["constructor"],core,leader,domain,d,incidence,cfg,ref["menu"],context,counts)
    recovery(record,core,{"finite":domain,"tail":tail},speeds,d,counts)
    c = record["constructor"]
    expected_comparison = {"same_status":c["status"] == ref["menu"]["status"],"same_ids":c["ids"] == ids,
                           "constructor_contacts":c["query_costs"]["unique"],"full_matrix_contacts":len(core)*len(domain)}
    check(record["comparison"] == expected_comparison,"comparison summary")
    return {"pair":pair,"status":"VERIFIED","minimum_status":minimum_status,"constructor_status":c["status"],
            "route":c["route"],"ids":c["ids"],"optional_status":c["optional_common"]["status"]}


def verify(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    cfg = json.loads((HERE / "config.json").read_text())
    freeze = data["freeze_commit"]
    manifest_raw = (HERE / "manifest.json").read_bytes()
    check(manifest_raw == subprocess.check_output(["git","show",freeze+":experiments/runner-addition/exception-cover/manifest.json"],cwd=ROOT),"changed manifest")
    for p,h in json.loads(manifest_raw)["sha256"].items():
        source = (ROOT/p).read_bytes()
        check(hashlib.sha256(source).hexdigest() == h and source == subprocess.check_output(["git","show",freeze+":"+p],cwd=ROOT),"frozen dependency changed")
    check(data["study"] == cfg["study"] and data["source_commit"] == cfg["source_commit"],"study identity")
    check(len(data["families"]) == len(cfg["pairs"]) and len(data["controls"]) == len(cfg["controls"]),"record count")
    counts = {"core_sets":0,"child_sets":0,"reference_contacts":0,"constructor_contacts":0,
              "physical_witnesses":0,"minimum_subsets":0,"optional_sets":0}
    families = [family(r,p,cfg,counts) for r,p in zip(data["families"],cfg["pairs"])]
    controls = []
    for row,item in zip(data["controls"],cfg["controls"]):
        check(row["name"] == item["name"] and row["scope"] == "SUPPLIED_INTERVAL_FINITE_CONTROL","control identity")
        core,d = alt.intervals(item["core"]),F(item["threshold"])
        incidence,sets,minimum_status = reference(row["reference"],core,item["leader"],item["domain"],d,[],cfg,counts)
        local = {**cfg,**item.get("overrides",{})}
        c = row["constructor"]
        compiled(c,core,item["leader"],item["domain"],d,incidence,local,row["reference"]["menu"],None,counts)
        recovery(row,core,{"finite":item["domain"]},[],d,counts)
        check(c["status"] == item["expect_status"] and c["ids"] == item["expect_ids"] and c["route"] == item["expect_route"],"control expectation")
        if "expect_optional" in item:
            check(c["optional_common"]["status"] == item["expect_optional"],"optional expectation")
        controls.append({"name":item["name"],"status":"PASS","constructor_status":c["status"],"route":c["route"],
                         "reference_minimum_status":minimum_status})
    resolved = all(r["status"] == "VERIFIED" and r["minimum_status"] == "EXACT_VERIFIED" and r["constructor_status"] == "EXACT" for r in families)
    return {"status":"PASS" if resolved else "VERIFIED_WITH_UNRESOLVED_FAMILIES","freeze_commit":freeze,
            "results_sha256":hashlib.sha256(raw).hexdigest(),"counts":counts,"families":families,"controls":controls,
            "limits":"Same-author alternate algorithms. Query-order accounting replays the specification; minimum proof uses independent subset enumeration. DP counters are instrumentation. No independent human or formal proof review."}


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
