"""Alternate pairing, union-speed event sets and inherited exact-family audit."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import gcd
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASELINE = HERE.parent / "outside-template"
spec = importlib.util.spec_from_file_location("removal_parent_verifier",BASELINE / "verify.py")
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)
alt,check,canon = parent.alt,parent.check,parent.canon


def pairing(item,prior):
    speeds = prior["speeds"]
    eligible = []
    coefficients = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8)]
    for k in range(1,(max(speeds)+10)//10+1):
        m = 10*k
        for v in speeds:
            changed = (set(speeds)-{v}) | {m}
            if m in speeds or len(changed) != 8 or gcd(*changed) != 1:
                continue
            template = any(sorted(a*p+b*q for a,b in coefficients) == sorted(changed) for p in changed for q in changed)
            if not template:
                eligible.append((abs(m-v),m,v))
    check(bool(eligible),"empty candidate domain")
    distance,inserted,removed = sorted(eligible)[0]
    expected = {"name":prior["name"],"speeds":sorted((set(speeds)-{removed}) | {inserted}),
                "removed":removed,"inserted":inserted,"distance":distance,"eligible_replacements":len(eligible)}
    check(item == expected,"pairing selection")


def paired(old,new,d,counts):
    actual = new["paired"]
    if new["status"] != "EVALUATED":
        check(actual == {"status":"UNRESOLVED_NEW_CORE","new_status":new["status"]},"unresolved pairing")
        return
    core_old,core_new = alt.intervals(old["core"]),alt.intervals(new["core"])
    shared,events = alt.event_set(sorted(set(old["speeds"]) | set(new["speeds"])),d)
    counts["paired_union_sets"] += 1
    counts["paired_union_events"] += events
    check(alt.intervals(actual["core_intersection"]) == shared,"complete core intersection")
    t = F(1,10)
    check(alt.safe(old["speeds"],t,d) and not alt.safe(new["speeds"],t,d),"physical anchor removal")
    check(any(a <= t <= b for a,b in core_old) and not any(a <= t <= b for a,b in core_new),"anchor membership")
    old_cases = {x["r"]:alt.intervals(x["full_safe_set"]) for x in old["reference"]["cases"]}
    new_cases = {x["r"]:alt.intervals(x["full_safe_set"]) for x in new["reference"]["cases"]}
    common = sorted(set(old_cases)&set(new_cases))
    repair = old["constructor"]["certificate"]["common_repair"]
    point = {"status":"NOT_APPLICABLE"}
    if repair:
        u = F(repair["time"])
        point = {"status":"CHECKED","time":u,
                 "blocking_new_core_speeds":[v for v in new["speeds"] if not alt.safe([v],u,d)],
                 "blocking_new_exceptions":[r for r in new["constructor"]["failures"] if not alt.safe([r],u,d)]
                 if new["constructor"]["classification_complete"] else None}
    expected = {"status":"COMPARED","old_minimum":old["reference"]["menu"],"new_minimum":new["reference"]["menu"],
                "old_leader_interval":core_old[old["source"]["leader"]],"new_leader_interval":core_new[new["source"]["leader"]],
                "old_cutoff":old["source"]["cutoff"],"new_cutoff":new["source"]["cutoff"],
                "old_failures":old["constructor"]["failures"],
                "new_failures":new["constructor"]["failures"] if new["constructor"]["classification_complete"] else None,
                "anchor_blocking_new_speeds":[v for v in new["speeds"] if not alt.safe([v],t,d)],
                "core_intersection":shared,
                "core_measures":{name:sum((b-a for a,b in intervals),F(0)) for name,intervals in (("old",core_old),("new",core_new),("intersection",shared))},
                "common_finite_inputs":common,
                "identical_child_sets":[r for r in common if old_cases[r] == new_cases[r]],
                "changed_child_sets":[r for r in common if old_cases[r] != new_cases[r]],"old_repair_point":point}
    check(actual == canon(expected),"paired diagnostics")


def verify(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    cfg = json.loads((HERE / "config.json").read_text())
    freeze = data["freeze_commit"]
    manifest = (HERE / "manifest.json").read_bytes()
    check(manifest == subprocess.check_output(["git","show",freeze+":experiments/runner-addition/anchor-removal/manifest.json"],cwd=ROOT),"changed manifest")
    for p,h in json.loads(manifest)["sha256"].items():
        source = (ROOT/p).read_bytes()
        check(hashlib.sha256(source).hexdigest() == h and source == subprocess.check_output(["git","show",freeze+":"+p],cwd=ROOT),"changed dependency")
    check(data["study"] == cfg["study"] and data["source_commit"] == cfg["source_commit"],"study identity")
    check(cfg["reference"] == 0 and cfg["total_runners"] == 10 and F(cfg["threshold"]) == F(1,10),"scope")
    old_raw = (BASELINE / "results/RESULTS.json").read_bytes()
    previous = json.loads((BASELINE / "results/VERIFICATION.json").read_text())
    check(hashlib.sha256(old_raw).hexdigest() == cfg["baseline_results_sha256"] == data["baseline_results_sha256"] == previous["results_sha256"] and previous["status"] == "PASS","baseline provenance")
    old_cfg = json.loads((BASELINE / "config.json").read_text())
    baseline = json.loads(old_raw)["families"]
    check(len(data["families"]) == len(cfg["cores"]) == len(baseline) == len(old_cfg["cores"]) == 8,"scope size")
    counts = {"core_sets":0,"child_sets":0,"reference_contacts":0,"constructor_contacts":0,
              "physical_witnesses":0,"minimum_subsets":0,"optional_sets":0,"paired_union_sets":0,"paired_union_events":0}
    audited = []
    for row,item,old,prior in zip(data["families"],cfg["cores"],baseline,old_cfg["cores"]):
        pairing(item,prior)
        check(old["name"] == prior["name"] and old["speeds"] == prior["speeds"],"baseline identity")
        audited.append(parent.family(row,item,cfg,counts))
        paired(old,row,F(cfg["threshold"]),counts)
    resolved = all(r["status"] == "VERIFIED" and r["minimum_status"] == "EXACT_VERIFIED" and r["constructor_status"] == "EXACT" for r in audited)
    return {"status":"PASS" if resolved else "VERIFIED_WITH_UNRESOLVED_FAMILIES","freeze_commit":freeze,
            "results_sha256":hashlib.sha256(raw).hexdigest(),"baseline_results_sha256":cfg["baseline_results_sha256"],
            "counts":counts,"families":audited,
            "limits":"Same-author alternate event/subset algorithms; baseline evidence reused, not rerun. Paired core intersections separately checked via union-speed events. No independent human/formal proof review, causal isolation, or general LRC claim."}


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
