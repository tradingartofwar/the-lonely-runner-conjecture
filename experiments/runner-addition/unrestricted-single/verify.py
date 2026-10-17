"""Alternate safe-band and event-set audit; no primary/checker imports."""
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
SOURCE = HERE.parent / "anchor-removal/results"


def load(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pv = load("single_placement_verifier",HERE.parent / "placement/verify.py")
alt = load("single_phase_verifier",HERE.parent / "verify.py")
check = alt.check


def canon(x):
    return json.loads(json.dumps(x,default=str))


def classification(row,interval,speeds,d,cfg,counts):
    a,b = interval
    check(list(map(F,row["interval"])) == [a,b] and F(row["width"]) == b-a,"interval metadata")
    check(pv.full_interval(interval,speeds,d) and row["laps"] == [floor(s*a) for s in speeds],"core band/laps")
    cutoff = ceil(2*d/(b-a)) if a < b else None
    check(row["cutoff"] == cutoff and row["anchor"] is None and cfg["max_denominator"] == 0,"cutoff/disabled anchor search")
    domain = [a.denominator] if cutoff is None else [r for r in range(1,min(cutoff-1,cfg["max_r"])+1) if r not in speeds]
    expected = []
    for r in domain:
        expected.append(r)
        if not pv.band_hit(interval,r,d):
            break
    check([x["r"] for x in row["checks"]] == expected,"classification prefix")
    for obs in row["checks"]:
        r = obs["r"]
        check(r > 0 and r not in speeds,"inadmissible query")
        hit = pv.band_hit(interval,r,d)
        check(obs["blocked"] != hit,"band/obstruction disagreement")
        phase = r*(a+b)/2 % 1
        distance,sweep = min(phase,1-phase),r*(b-a)/2
        check(F(obs["distance"]) == distance and F(obs["half_sweep"]) == sweep and F(obs["score"]) == distance+sweep,"midpoint fields")
        if hit:
            check(obs["blocking_integer"] is None,"spurious blocker")
        else:
            m = obs["blocking_integer"]
            check(type(m) is int and r*b-d < m < r*a+d,"strict unsafe-gap certificate")
            counts["blocker_certificates"] += 1
    counts["classification_queries"] += len(expected)
    failed = bool(expected) and not pv.band_hit(interval,expected[-1],d)
    status = "BLOCKED" if failed else ("UNIVERSAL_CANDIDATE" if cutoff is not None and cutoff-1 <= cfg["max_r"] else "UNKNOWN_BUDGET")
    check(row["status"] == status,"classification status")
    if status != "UNIVERSAL_CANDIDATE":
        check(row["recovery"] is None,"recovery without universal interval")
        return
    tail = []
    for seed in (cutoff,cutoff+1,10**6+1,10**18+1):
        r = seed
        while r in speeds:
            r += 1
        if r not in tail:
            tail.append(r)
    check(set(row["recovery"]) == {"finite","tail"},"recovery domains")
    for name,domain in (("finite",expected),("tail",tail)):
        output = row["recovery"][name]
        check([w["r"] for w in output["witnesses"]] == domain and output["first_contact_calls"] == len(domain),"recovery queries/cost")
        for w in output["witnesses"]:
            t = alt.phase_first(a,w["r"],d)
            check(F(w["time"]) == t and a <= t <= b,"single-source first contact")
            alt.verify_witness(w,speeds+[w["r"]],d)
            counts["universal_witnesses"] += 1


def family(row,old,cfg,counts):
    speeds,d = old["speeds"],F(cfg["threshold"])
    check(row["name"] == old["name"] and row["speeds"] == speeds and F(row["threshold"]) == d,"family identity")
    check(len(speeds) == len(set(speeds)) == 8 and gcd(*speeds) == 1 and sum(speeds) <= cfg["max_core_speed_sum"],"core assumptions")
    check(old["constructor"]["status"] == "EXACT" and len(old["constructor"]["ids"]) == 2,"source upper bound")
    core,events = alt.event_set(speeds,d)
    counts["core_sets"] += 1
    counts["events"] += events
    check(core == alt.intervals(old["core"]) and len(row["components"]) == len(core) <= cfg["max_components"],"complete core")
    check(row["source_geometry_cost"] == {"input_bands":sum(speeds),"components":len(core),"primary_rebuilt":False},"geometry cost")
    for i,(interval,component) in enumerate(zip(core,row["components"])):
        check(component["id"] == i,"component ID")
        classification(component,interval,speeds,d,cfg,counts)
        counts["components"] += 1
    cert = row["source_certificate"]
    check(cert == old["constructor"]["certificate"],"upper-bound certificate identity")
    check(cert["family_context"] == {"core_speeds":speeds,"reference":0,"total_runners":10,"period":[0,1],"tail_from":old["source"]["cutoff"]},"source certificate scope")
    blockers = sorted({x["checks"][-1]["r"] for x in row["components"] if x["status"] == "BLOCKED"})
    check([x["r"] for x in row["children_at_blockers"]] == blockers,"blocker child domain")
    misses,unresolved = [],[]
    for child in row["children_at_blockers"]:
        r = child["r"]
        if r > cfg["max_child_speed"]:
            check(child == {"r":r,"status":"UNKNOWN_CHILD_BUDGET"},"child cap")
            unresolved.append(r)
            continue
        full,events = alt.event_set(speeds+[r],d)
        counts["child_sets"] += 1
        counts["events"] += events
        check(child["status"] == "AUDITED" and alt.intervals(child["full_safe_set"]) == full,"complete child")
        if not full:
            check(child["complete_witness"] is None and child["source_menu_witness"] is None and child["dispatcher_contact_calls"] == 0,"empty child witness")
            misses.append(r)
            continue
        check(F(child["complete_witness"]["time"]) == full[0][0],"earliest full witness")
        alt.verify_witness(child["complete_witness"],speeds+[r],d)
        counts["repair_witnesses"] += 1
        check(r not in speeds and (r in cert["domain"] or r >= cert["family_context"]["tail_from"]),"dispatcher scope")
        exception = next((x for x in cert["exception_table"] if x["r"] == r),None)
        if exception:
            point = cert["common_repair"] or exception
            t,i,calls = F(point["time"]),point["component"],0
        else:
            i = cert["leader"]["component"]
            t,calls = alt.phase_first(core[i][0],r,d),1
        w = child["source_menu_witness"]
        check(F(w["time"]) == t and w["component"] == i and core[i][0] <= t <= core[i][1] and child["dispatcher_contact_calls"] == calls,"source dispatcher output")
        alt.verify_witness(w,speeds+[r],d)
        counts["repair_witnesses"] += 1
    universal = [x["id"] for x in row["components"] if x["status"] == "UNIVERSAL_CANDIDATE"]
    blocked = [x["id"] for x in row["components"] if x["status"] == "BLOCKED"]
    unknown = [x["id"] for x in row["components"] if x["status"] == "UNKNOWN_BUDGET"]
    minimum = 1 if universal else (2 if not unknown else None)
    status = "MINIMUM_ONE_CANDIDATE" if universal else ("MINIMUM_TWO_CANDIDATE" if not unknown else "UNKNOWN_SINGLE_COMPONENT")
    if misses:
        status,minimum = "SOURCE_DISCREPANCY",None
    expected = {"status":status,"minimum_candidate":minimum,"upper_bound_from_source":2,"universal_components":universal,
                "blocked_components":blocked,"unknown_components":unknown,"classification_complete":not unknown,
                "component_queries":sum(len(x["checks"]) for x in row["components"]),"full_core_misses_at_blockers":misses,
                "unresolved_child_audits":unresolved}
    check(row["summary"] == expected,"decision summary")
    return {"name":row["name"],**expected}


def verify(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    cfg = json.loads((HERE / "config.json").read_text())
    freeze = data["freeze_commit"]
    manifest = (HERE / "manifest.json").read_bytes()
    check(manifest == subprocess.check_output(["git","show",freeze+":experiments/runner-addition/unrestricted-single/manifest.json"],cwd=ROOT),"changed manifest")
    for p,h in json.loads(manifest)["sha256"].items():
        source = (ROOT/p).read_bytes()
        check(hashlib.sha256(source).hexdigest() == h and source == subprocess.check_output(["git","show",freeze+":"+p],cwd=ROOT),"changed dependency")
    check(data["study"] == cfg["study"] and data["source_commit"] == cfg["source_commit"],"study identity")
    check(cfg["reference"] == 0 and cfg["total_runners"] == 10 and F(cfg["threshold"]) == F(1,10) and cfg["max_denominator"] == 0,"scope")
    previous_raw = (SOURCE / "RESULTS.json").read_bytes()
    previous_verification = json.loads((SOURCE / "VERIFICATION.json").read_text())
    check(hashlib.sha256(previous_raw).hexdigest() == data["source_results_sha256"] == cfg["source_results_sha256"] == previous_verification["results_sha256"] and previous_verification["status"] == "PASS","source provenance")
    prior = {x["name"]:x for x in json.loads(previous_raw)["families"]}
    check([x["name"] for x in data["families"]] == cfg["names"] and len(data["controls"]) == len(cfg["controls"]),"record scope")
    counts = {"core_sets":0,"components":0,"events":0,"classification_queries":0,"blocker_certificates":0,
              "universal_witnesses":0,"child_sets":0,"repair_witnesses":0}
    controls = []
    for row,item in zip(data["controls"],cfg["controls"]):
        check(row["name"] == item["name"] and row["scope"] == "SUPPLIED_INTERVAL_CONTROL","control identity")
        local = {**cfg,"max_r":item.get("max_r",cfg["max_r"])}
        c = row["classification"]
        classification(c,tuple(map(F,item["interval"])),item["speeds"],F(cfg["threshold"]),local,counts)
        check(c["status"] == item["expect"] and (c["checks"][-1]["r"] if c["status"] == "BLOCKED" else None) == item["blocker"],"control outcome")
        controls.append({"name":item["name"],"status":"PASS","outcome":c["status"]})
    families = [family(row,prior[row["name"]],cfg,counts) for row in data["families"]]
    resolved = all(x["classification_complete"] and not x["unresolved_child_audits"] and x["minimum_candidate"] in (1,2) for x in families)
    return {"status":"PASS" if resolved else "VERIFIED_WITH_LIMITS","freeze_commit":freeze,
            "results_sha256":hashlib.sha256(raw).hexdigest(),"source_results_sha256":cfg["source_results_sha256"],
            "counts":counts,"families":families,"controls":controls,
            "limits":"Same-author band/event/phase counterchecks; no independent human/formal proof review. Universal/minimum claims rely on component completeness, individual width tails and the pinned prior upper bound. Minimum is within fixed connected core-safe component menus."}


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
