"""Frozen explicit-core transfer; the constructor and reference are unchanged."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import ceil, gcd
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("outside_parent_runner",HERE.parent / "exception-cover/run.py")
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)
ctor,base,require = parent.ctor,parent.base,parent.require
recover,guards = parent.recover,parent.guards


def preflight(freeze):
    raw = (HERE / "manifest.json").read_bytes()
    relative = "experiments/runner-addition/outside-template/manifest.json"
    require(raw == subprocess.check_output(["git","show",freeze+":"+relative],cwd=ROOT),"manifest changed")
    for p,h in json.loads(raw)["sha256"].items():
        data = (ROOT/p).read_bytes()
        require(hashlib.sha256(data).hexdigest() == h,"local freeze mismatch: "+p)
        require(data == subprocess.check_output(["git","show",freeze+":"+p],cwd=ROOT),"archived freeze mismatch: "+p)


def input_audit(item):
    speeds = item["speeds"]
    require(len(speeds) == 8 and speeds == sorted(set(speeds)) and
            all(type(v) is int and v > 0 for v in speeds),"invalid explicit speeds")
    require(gcd(*speeds) == 1,"nonprimitive core")
    matches = [[p,q] for p in speeds for q in speeds if sorted(
        [p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q]) == speeds]
    require(not matches,"selected core belongs to excluded template")
    return {"gcd":gcd(*speeds),"template_pairs_checked":len(speeds)**2,"template_matches":matches}


def family(item,cfg):
    speeds = item["speeds"]
    audit = input_audit(item)
    d = F(cfg["threshold"])
    record = {"name":item["name"],"speeds":speeds,"threshold":d,"input_audit":audit}
    if sum(speeds) > cfg["max_core_speed_sum"]:
        return {**record,"status":"UNKNOWN_CORE_BUDGET"}
    core = list(base.feasible_intervals(speeds,d))
    record.update({"core":core,"core_input_bands":sum(speeds)})
    if not core:
        return {**record,"status":"UNSUPPORTED_EMPTY_CORE"}
    if len(core) > cfg["max_components"]:
        return {**record,"status":"UNKNOWN_COMPONENT_BUDGET"}
    leader = min(range(len(core)),key=lambda i:(-(core[i][1]-core[i][0]),core[i][0]))
    width = core[leader][1]-core[leader][0]
    if not width:
        return {**record,"status":"UNSUPPORTED_ZERO_WIDTH"}
    cutoff = ceil(2*d/width)
    if cutoff > cfg["max_tail_cutoff"]:
        return {**record,"status":"UNKNOWN_DOMAIN_BUDGET","cutoff":cutoff}
    domain = [r for r in range(1,cutoff) if r not in speeds]
    controls = []
    for seed in (cutoff,cutoff+1,10**6+1,10**18+1):
        r = seed
        while r in speeds:
            r += 1
        if r not in controls:
            controls.append(r)
    source = {"pair":None,"speeds":speeds,"threshold":str(d),"components":core,
              "leader":leader,"cutoff":cutoff,"matched_inputs":domain,"necessary_remainder":domain,"tail_controls":controls}
    compiled = ctor.construct(core,leader,domain,d,cfg)
    if compiled["certificate"]:
        compiled["certificate"]["family_context"] = {"core_speeds":speeds,"reference":0,"total_runners":10,
                                                      "period":[0,1],"tail_from":cutoff}
    recovery = recover(compiled,{"finite":domain,"tail":controls},speeds,core,d)
    invalid = guards(compiled,speeds[0])
    # Constructor, optional point and dispatch run before accessing the reference matrix.
    reference = base.evaluate(source,cfg)
    if compiled["status"] != "UNKNOWN_BUDGET" and reference["menu"]["status"] != "UNKNOWN_BUDGET":
        require(compiled["status"] == reference["menu"]["status"] and compiled["ids"] == reference["menu"]["ids"],"constructor/reference discrepancy")
    return {**record,"status":"EVALUATED","source":source,"constructor":compiled,"recovery":recovery,
            "guard_checks":invalid,"reference":reference,
            "comparison":{"same_status":compiled["status"] == reference["menu"]["status"],
                          "same_ids":compiled["ids"] == reference["menu"]["ids"],
                          "constructor_contacts":compiled["query_costs"]["unique"],
                          "full_matrix_contacts":len(core)*len(domain)}}


def run(freeze,checkpoint_dir):
    preflight(freeze)
    cfg = json.loads((HERE / "config.json").read_text())
    require(cfg["reference"] == 0 and cfg["total_runners"] == 10 and F(cfg["threshold"]) == F(1,10),"physical scope")
    require(len({x["name"] for x in cfg["cores"]}) == len(cfg["cores"]),"duplicate names")
    audits = [input_audit(item) for item in cfg["cores"]]
    print(json.dumps({"input_audits":len(audits),"template_matches":0}),flush=True)
    checkpoint_dir.mkdir(parents=True,exist_ok=False)
    records = []
    for item in cfg["cores"]:
        row = family(item,cfg)
        records.append(row)
        (checkpoint_dir / (item["name"]+".json")).write_text(json.dumps(row,default=base.encode,sort_keys=True,separators=(",",":"))+"\n")
        c = row.get("constructor",{})
        print(json.dumps({"name":item["name"],"status":row["status"],"route":c.get("route"),
                          "ids":c.get("ids"),"failures":c.get("failures"),"comparison":row.get("comparison")}),flush=True)
    return {"study":cfg["study"],"freeze_commit":freeze,"source_commit":cfg["source_commit"],
            "claim_status":"finite observations; all-r implications remain same-author proof candidates","families":records}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze",required=True)
    parser.add_argument("--output",type=Path,default=HERE / "results/RESULTS.json")
    parser.add_argument("--checkpoint-dir",type=Path,required=True)
    args = parser.parse_args()
    require(not args.output.exists(),"refusing to overwrite results")
    result = run(args.freeze,args.checkpoint_dir)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result,default=base.encode,sort_keys=True,separators=(",",":"))+"\n")
    print(json.dumps({"status":"COMPUTED_PENDING_VERIFICATION","families":len(result["families"])}))
