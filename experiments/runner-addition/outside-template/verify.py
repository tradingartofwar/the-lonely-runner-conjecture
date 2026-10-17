"""Alternate event geometry for explicit cores; no primary/checker import."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import ceil, floor, gcd
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("outside_parent_verifier",HERE.parent / "exception-cover/verify.py")
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)
alt,check,canon = parent.alt,parent.check,parent.canon
reference,compiled,recovery = parent.reference,parent.compiled,parent.recovery


def family(record,item,cfg,counts):
    speeds = item["speeds"]
    d = F(cfg["threshold"])
    check(record["name"] == item["name"] and record["speeds"] == speeds and F(record["threshold"]) == d,"family identity")
    check(speeds == sorted(set(speeds)) and len(speeds) == 8 and all(type(v) is int and v > 0 for v in speeds) and gcd(*speeds) == 1,"primitive distinct core")
    matches = []
    coefficients = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8)]
    for p in speeds:
        for q in speeds:
            if sorted(a*p+b*q for a,b in coefficients) == speeds:
                matches.append([p,q])
    check(not matches and record["input_audit"] == {"gcd":1,"template_pairs_checked":64,"template_matches":[]},"template exclusion")
    if sum(speeds) > cfg["max_core_speed_sum"]:
        check(record["status"] == "UNKNOWN_CORE_BUDGET","core budget status")
        return {"name":item["name"],"status":record["status"]}
    core,_ = alt.event_set(speeds,d)
    counts["core_sets"] += 1
    check(alt.intervals(record["core"]) == core and record["core_input_bands"] == sum(speeds),"core geometry/cost")
    if not core or len(core) > cfg["max_components"]:
        expected = "UNSUPPORTED_EMPTY_CORE" if not core else "UNKNOWN_COMPONENT_BUDGET"
        check(record["status"] == expected,"unsupported core")
        return {"name":item["name"],"status":expected}
    leader = min(range(len(core)),key=lambda i:(-(core[i][1]-core[i][0]),core[i][0]))
    width = core[leader][1]-core[leader][0]
    if not width:
        check(record["status"] == "UNSUPPORTED_ZERO_WIDTH","zero width")
        return {"name":item["name"],"status":record["status"]}
    cutoff = ceil(2*d/width)
    if cutoff > cfg["max_tail_cutoff"]:
        check(record["status"] == "UNKNOWN_DOMAIN_BUDGET" and record["cutoff"] == cutoff,"cutoff budget")
        return {"name":item["name"],"status":record["status"]}
    check(record["status"] == "EVALUATED","family not evaluated")
    domain = [r for r in range(1,cutoff) if r not in speeds]
    tail = []
    for seed in (cutoff,cutoff+1,10**6+1,10**18+1):
        r = seed
        while r in speeds:
            r += 1
        if r not in tail:
            tail.append(r)
    source = {"pair":None,"speeds":speeds,"threshold":str(d),"components":core,"leader":leader,
              "cutoff":cutoff,"matched_inputs":domain,"necessary_remainder":domain,"tail_controls":tail}
    check(record["source"] == canon(source),"complete source contract")
    ref = record["reference"]
    check(ref["pair"] is None and ref["speeds"] == speeds and ref["threshold"] == str(d) and
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
    return {"name":item["name"],"status":"VERIFIED","minimum_status":minimum_status,"constructor_status":c["status"],
            "route":c["route"],"ids":c["ids"],"optional_status":c["optional_common"]["status"]}


def verify(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    cfg = json.loads((HERE / "config.json").read_text())
    freeze = data["freeze_commit"]
    manifest_raw = (HERE / "manifest.json").read_bytes()
    relative = "experiments/runner-addition/outside-template/manifest.json"
    check(manifest_raw == subprocess.check_output(["git","show",freeze+":"+relative],cwd=ROOT),"changed manifest")
    for p,h in json.loads(manifest_raw)["sha256"].items():
        source = (ROOT/p).read_bytes()
        check(hashlib.sha256(source).hexdigest() == h and source == subprocess.check_output(["git","show",freeze+":"+p],cwd=ROOT),"frozen dependency changed")
    check(data["study"] == cfg["study"] and data["source_commit"] == cfg["source_commit"],"study identity")
    check(cfg["reference"] == 0 and cfg["total_runners"] == 10 and F(cfg["threshold"]) == F(1,10),"physical scope")
    check(len(data["families"]) == len(cfg["cores"]),"record count")
    counts = {"core_sets":0,"child_sets":0,"reference_contacts":0,"constructor_contacts":0,
              "physical_witnesses":0,"minimum_subsets":0,"optional_sets":0}
    families = [family(r,item,cfg,counts) for r,item in zip(data["families"],cfg["cores"])]
    resolved = all(r["status"] == "VERIFIED" and r["minimum_status"] == "EXACT_VERIFIED" and r["constructor_status"] == "EXACT" for r in families)
    return {"status":"PASS" if resolved else "VERIFIED_WITH_UNRESOLVED_FAMILIES","freeze_commit":freeze,
            "results_sha256":hashlib.sha256(raw).hexdigest(),"counts":counts,"families":families,
            "limits":"Same-author alternate event/subset algorithms with inherited trace audits. DP counters are instrumentation. This tests only eight explicit stationary-reference cores and their added-speed reductions; no independent human or formal proof review."}


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
