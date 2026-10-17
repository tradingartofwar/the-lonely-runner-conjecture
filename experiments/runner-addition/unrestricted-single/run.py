"""Unrestricted component decisions using the unchanged placement classifier."""
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
SOURCE = HERE.parent / "anchor-removal/results"


def load(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


placement = load("single_placement",HERE.parent / "placement/run.py")
base = load("single_contacts",HERE.parent / "study.py")
ctor = load("single_prior_dispatch",HERE.parent / "exception-cover/constructor.py")
require = base.require


def preflight(freeze):
    raw = (HERE / "manifest.json").read_bytes()
    relative = "experiments/runner-addition/unrestricted-single/manifest.json"
    require(raw == subprocess.check_output(["git","show",freeze+":"+relative],cwd=ROOT),"manifest changed")
    for p,h in json.loads(raw)["sha256"].items():
        data = (ROOT/p).read_bytes()
        require(hashlib.sha256(data).hexdigest() == h,"changed dependency: "+p)
        require(data == subprocess.check_output(["git","show",freeze+":"+p],cwd=ROOT),"archive mismatch: "+p)


def recover(row,speeds,d):
    if row["status"] != "UNIVERSAL_CANDIDATE":
        return None
    interval = row["interval"]
    finite = [x["r"] for x in row["checks"]]
    tail = []
    for seed in (row["cutoff"],row["cutoff"]+1,10**6+1,10**18+1):
        r = seed
        while r in speeds:
            r += 1
        if r not in tail:
            tail.append(r)
    output = {}
    for label,domain in (("finite",finite),("tail",tail)):
        rows = []
        for r in domain:
            contact = base.first_contact(interval,r,d)
            require(contact["hit"],"universal component contact failed")
            rows.append({"r":r,**base.witness_record(contact["candidate"],speeds+[r],d)})
        output[label] = {"witnesses":rows,"first_contact_calls":len(rows)}
    return output


def classify(interval,speeds,d,cfg):
    row = placement.classify(interval,speeds,d,cfg)
    row["recovery"] = recover(row,speeds,d)
    return row


def decision(rows,children):
    universal = [x["id"] for x in rows if x["status"] == "UNIVERSAL_CANDIDATE"]
    blocked = [x["id"] for x in rows if x["status"] == "BLOCKED"]
    unknown = [x["id"] for x in rows if x["status"] == "UNKNOWN_BUDGET"]
    misses = [x["r"] for x in children if x["status"] == "AUDITED" and not x["full_safe_set"]]
    minimum = 1 if universal else (2 if not unknown else None)
    status = "MINIMUM_ONE_CANDIDATE" if universal else ("MINIMUM_TWO_CANDIDATE" if not unknown else "UNKNOWN_SINGLE_COMPONENT")
    if misses:
        status,minimum = "SOURCE_DISCREPANCY",None
    return {"status":status,"minimum_candidate":minimum,"upper_bound_from_source":2,
            "universal_components":universal,"blocked_components":blocked,"unknown_components":unknown,
            "classification_complete":not unknown,"component_queries":sum(len(x["checks"]) for x in rows),
            "full_core_misses_at_blockers":misses,
            "unresolved_child_audits":[x["r"] for x in children if x["status"] != "AUDITED"]}


def family(old,cfg):
    speeds,d = old["speeds"],F(cfg["threshold"])
    require(len(speeds) == len(set(speeds)) == 8 and gcd(*speeds) == 1 and sum(speeds) <= cfg["max_core_speed_sum"],"invalid core")
    require(old["status"] == "EVALUATED" and old["constructor"]["status"] == "EXACT" and len(old["constructor"]["ids"]) == 2,"missing two-source upper bound")
    require(F(old["threshold"]) == d,"threshold changed")
    core = [tuple(map(F,x)) for x in old["core"]]
    require(core and len(core) <= cfg["max_components"],"core component cap")
    rows = [{"id":i,**classify(interval,speeds,d,cfg)} for i,interval in enumerate(core)]
    blockers = sorted({x["checks"][-1]["r"] for x in rows if x["status"] == "BLOCKED"})
    certificate = old["constructor"]["certificate"]
    children = []
    for r in blockers:
        if r > cfg["max_child_speed"]:
            children.append({"r":r,"status":"UNKNOWN_CHILD_BUDGET"})
            continue
        full = base.feasible_intervals(speeds+[r],d)
        witness = base.witness_record(full[0][0],speeds+[r],d) if full else None
        menu,calls = None,0
        if full:
            t,i,calls = ctor.dispatch(certificate,r)
            require(core[i][0] <= t <= core[i][1],"source dispatcher leaves component")
            menu = {"component":i,**base.witness_record(t,speeds+[r],d)}
        children.append({"r":r,"status":"AUDITED","full_safe_set":full,"complete_witness":witness,
                         "source_menu_witness":menu,"dispatcher_contact_calls":calls})
    return {"name":old["name"],"speeds":speeds,"threshold":d,"components":rows,
            "source_geometry_cost":{"input_bands":sum(speeds),"components":len(core),"primary_rebuilt":False},
            "source_certificate":certificate,"children_at_blockers":children,"summary":decision(rows,children)}


def control(item,cfg):
    local = {**cfg,"max_r":item.get("max_r",cfg["max_r"])}
    row = classify(tuple(map(F,item["interval"])),item["speeds"],F(cfg["threshold"]),local)
    require(row["status"] == item["expect"],"control status: "+item["name"])
    blocker = row["checks"][-1]["r"] if row["status"] == "BLOCKED" else None
    require(blocker == item["blocker"],"control blocker: "+item["name"])
    return {"name":item["name"],"scope":"SUPPLIED_INTERVAL_CONTROL","classification":row}


def run(freeze,checkpoint_dir):
    preflight(freeze)
    cfg = json.loads((HERE / "config.json").read_text())
    require(cfg["reference"] == 0 and cfg["total_runners"] == 10 and F(cfg["threshold"]) == F(1,10) and cfg["max_denominator"] == 0,"scope changed")
    raw = (SOURCE / "RESULTS.json").read_bytes()
    verified = json.loads((SOURCE / "VERIFICATION.json").read_text())
    require(hashlib.sha256(raw).hexdigest() == cfg["source_results_sha256"] == verified["results_sha256"] and verified["status"] == "PASS","source provenance")
    sources = {x["name"]:x for x in json.loads(raw)["families"]}
    controls = [control(x,cfg) for x in cfg["controls"]]
    print(json.dumps({"controls":len(controls),"status":"EXPECTED_BEHAVIOR"}),flush=True)
    checkpoint_dir.mkdir(parents=True,exist_ok=False)
    records = []
    for name in cfg["names"]:
        row = family(sources[name],cfg)
        records.append(row)
        (checkpoint_dir / (name+".json")).write_text(json.dumps(row,default=base.encode,sort_keys=True,separators=(",",":"))+"\n")
        s = row["summary"]
        print(json.dumps({"name":name,"status":s["status"],"universal":s["universal_components"],"blocked":len(s["blocked_components"]),
                          "unknown":s["unknown_components"],"queries":s["component_queries"],"blocker_children":len(row["children_at_blockers"])}),flush=True)
        require(s["status"] != "SOURCE_DISCREPANCY","source discrepancy retained in checkpoint")
    return {"study":cfg["study"],"freeze_commit":freeze,"source_commit":cfg["source_commit"],
            "source_results_sha256":cfg["source_results_sha256"],"families":records,"controls":controls,
            "claim_status":"exact finite classification; universal and unrestricted minimum implications remain same-author proof candidates"}


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
