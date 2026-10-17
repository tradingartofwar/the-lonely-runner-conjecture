"""Frozen arithmetic pairing and unchanged exact family construction."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASELINE = HERE.parent / "outside-template"
spec = importlib.util.spec_from_file_location("removal_parent_runner",BASELINE / "run.py")
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)
require = parent.require


def preflight(freeze):
    raw = (HERE / "manifest.json").read_bytes()
    relative = "experiments/runner-addition/anchor-removal/manifest.json"
    require(raw == subprocess.check_output(["git","show",freeze+":"+relative],cwd=ROOT),"manifest changed")
    for path,h in json.loads(raw)["sha256"].items():
        data = (ROOT/path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == h,"changed dependency: "+path)
        require(data == subprocess.check_output(["git","show",freeze+":"+path],cwd=ROOT),"archive mismatch: "+path)


def select(item):
    speeds = item["speeds"]
    candidates = []
    for removed in speeds:
        for inserted in range(10,max(speeds)+11,10):
            if inserted in speeds:
                continue
            changed = sorted([v for v in speeds if v != removed]+[inserted])
            try:
                parent.input_audit({"speeds":changed})
            except ValueError:
                continue
            candidates.append((abs(inserted-removed),inserted,removed))
    require(bool(candidates),"no eligible replacement")
    distance,inserted,removed = min(candidates)
    return {"name":item["name"],"speeds":sorted([v for v in speeds if v != removed]+[inserted]),
            "removed":removed,"inserted":inserted,"distance":distance,"eligible_replacements":len(candidates)}


def paired(old,new,d):
    if new["status"] != "EVALUATED":
        return {"status":"UNRESOLVED_NEW_CORE","new_status":new["status"]}
    old_core = [tuple(map(F,x)) for x in old["core"]]
    new_core = [tuple(map(F,x)) for x in new["core"]]
    intersection = sorted({(max(a,c),min(b,e)) for a,b in old_core for c,e in new_core if max(a,c) <= min(b,e)})
    anchor = F(1,10)
    blocked = lambda speeds,t:[v for v in speeds if not d <= (v*t % 1) <= 1-d]
    require(not blocked(old["speeds"],anchor) and blocked(new["speeds"],anchor),"anchor not removed")
    require(any(a <= anchor <= b for a,b in old_core) and not any(a <= anchor <= b for a,b in new_core),"anchor geometry mismatch")
    prior = old["constructor"]["certificate"]["common_repair"]
    recovery = {"status":"NOT_APPLICABLE"}
    if prior:
        t = F(prior["time"])
        recovery = {"status":"CHECKED","time":t,"blocking_new_core_speeds":blocked(new["speeds"],t),
                    "blocking_new_exceptions":blocked(new["constructor"]["failures"],t)
                    if new["constructor"]["classification_complete"] else None}
    old_cases = {x["r"]:x["full_safe_set"] for x in old["reference"]["cases"]}
    new_cases = {x["r"]:x["full_safe_set"] for x in new["reference"]["cases"]}
    common = sorted(old_cases.keys() & new_cases.keys())
    # Old saved values are strings; the fresh output still contains Fractions.
    old_sets = {r:[tuple(map(F,x)) for x in old_cases[r]] for r in common}
    new_sets = {r:[tuple(map(F,x)) for x in new_cases[r]] for r in common}
    return {"status":"COMPARED","old_minimum":old["reference"]["menu"],"new_minimum":new["reference"]["menu"],
            "old_leader_interval":old_core[old["source"]["leader"]],"new_leader_interval":new_core[new["source"]["leader"]],
            "old_cutoff":old["source"]["cutoff"],"new_cutoff":new["source"]["cutoff"],
            "old_failures":old["constructor"]["failures"],
            "new_failures":new["constructor"]["failures"] if new["constructor"]["classification_complete"] else None,
            "anchor_blocking_new_speeds":blocked(new["speeds"],anchor),"core_intersection":intersection,
            "core_measures":{"old":sum((b-a for a,b in old_core),F(0)),"new":sum((b-a for a,b in new_core),F(0)),
                             "intersection":sum((b-a for a,b in intersection),F(0))},
            "common_finite_inputs":common,
            "identical_child_sets":[r for r in common if old_sets[r] == new_sets[r]],
            "changed_child_sets":[r for r in common if old_sets[r] != new_sets[r]],
            "old_repair_point":recovery}


def run(freeze,checkpoint_dir):
    preflight(freeze)
    cfg = json.loads((HERE / "config.json").read_text())
    old_cfg = json.loads((BASELINE / "config.json").read_text())
    require([select(x) for x in old_cfg["cores"]] == cfg["cores"],"arithmetic pairing mismatch")
    require(cfg["reference"] == 0 and cfg["total_runners"] == 10 and F(cfg["threshold"]) == F(1,10),"physical scope")
    old_raw = (BASELINE / "results/RESULTS.json").read_bytes()
    old_verification = json.loads((BASELINE / "results/VERIFICATION.json").read_text())
    require(hashlib.sha256(old_raw).hexdigest() == cfg["baseline_results_sha256"] == old_verification["results_sha256"] and old_verification["status"] == "PASS","baseline provenance")
    baseline = json.loads(old_raw)["families"]
    require([x["name"] for x in baseline] == [x["name"] for x in cfg["cores"]],"baseline names")
    checkpoint_dir.mkdir(parents=True,exist_ok=False)
    records = []
    for old,item in zip(baseline,cfg["cores"]):
        row = parent.family(item,cfg)
        row["paired"] = paired(old,row,F(cfg["threshold"]))
        records.append(row)
        (checkpoint_dir / (item["name"]+".json")).write_text(json.dumps(row,default=parent.base.encode,sort_keys=True,separators=(",",":"))+"\n")
        c = row.get("constructor",{})
        print(json.dumps({"name":item["name"],"status":row["status"],"route":c.get("route"),"ids":c.get("ids"),
                          "failures":c.get("failures"),"comparison":row.get("comparison")}),flush=True)
    return {"study":cfg["study"],"freeze_commit":freeze,"source_commit":cfg["source_commit"],
            "baseline_results_sha256":cfg["baseline_results_sha256"],"families":records,
            "claim_status":"bounded paired observations; all-r implications remain same-author proof candidates"}


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
        handle.write(json.dumps(result,default=parent.base.encode,sort_keys=True,separators=(",",":"))+"\n")
