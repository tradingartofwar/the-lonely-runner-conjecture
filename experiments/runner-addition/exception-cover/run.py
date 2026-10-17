"""Frozen four-family constructor transfer and seven finite semantic controls."""
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
spec = importlib.util.spec_from_file_location("exception_constructor",HERE / "constructor.py")
ctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctor)
base, require = ctor.base, ctor.require


def preflight(freeze):
    raw = (HERE / "manifest.json").read_bytes()
    require(raw == subprocess.check_output(["git","show",freeze+":experiments/runner-addition/exception-cover/manifest.json"],cwd=ROOT),"manifest changed")
    for p,h in json.loads(raw)["sha256"].items():
        data = (ROOT/p).read_bytes()
        require(hashlib.sha256(data).hexdigest() == h,"local freeze mismatch: "+p)
        require(data == subprocess.check_output(["git","show",freeze+":"+p],cwd=ROOT),"archived freeze mismatch: "+p)


def recover(result, domains, speeds, core, d):
    output = {"status":"RECOVERED" if result["certificate"] else "NO_CERTIFICATE","domains":{}}
    for name, domain in domains.items():
        rows, calls = [], 0
        if result["certificate"]:
            for r in domain:
                t,i,count = ctor.dispatch(result["certificate"],r)
                require(core[i][0] <= t <= core[i][1],"dispatch outside source")
                rows.append({"r":r,"component":i,**base.witness_record(t,speeds+[r],d)})
                calls += count
        output["domains"][name] = {"witnesses":rows,"first_contact_calls":calls}
    return output


def guards(result, repeated=None):
    if not result["certificate"]:
        return []
    queries = [0]
    if repeated is not None:
        queries.append(repeated)
    else:
        r = 1
        while r in result["certificate"]["domain"]:
            r += 1
        queries.append(r)
    records = []
    for r in queries:
        try:
            ctor.dispatch(result["certificate"],r)
        except ValueError as error:
            records.append({"r":r,"status":"REJECTED","reason":str(error)})
        else:
            raise ValueError("invalid dispatcher query accepted")
    return records


def family(pair,cfg):
    p,q = pair
    speeds = [p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q]
    require(gcd(p,q) == 1 and len(set([0]+speeds)) == 9,"invalid primitive core")
    d = F(cfg["threshold"])
    record = {"pair":pair,"speeds":speeds,"threshold":d}
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
    source = {"pair":pair,"speeds":speeds,"threshold":str(d),"components":core,
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


def fixture_reference(core,leader,domain,d,cfg):
    cases = []
    for r in domain:
        bands = base.feasible_intervals([r],d)
        contacts, full = [], []
        for i,interval in enumerate(core):
            pieces = [(max(a,interval[0]),min(b,interval[1])) for a,b in bands if max(a,interval[0]) <= min(b,interval[1])]
            contact = base.first_contact(interval,r,d)
            require(contact["hit"] == bool(pieces),"fixture contact mismatch")
            contacts.append({"component":i,**contact,"surviving_pieces":pieces})
            full.extend(pieces)
        cases.append({"r":r,"contacts":contacts,"full_safe_set":sorted(full)})
    return {"cases":cases,"menu":base.minimum_menu(leader,len(core),cases,cfg)}


def control(item,cfg):
    local = {**cfg,**item.get("overrides",{})}
    core = [tuple(map(F,x)) for x in item["core"]]
    d = F(item["threshold"])
    compiled = ctor.construct(core,item["leader"],item["domain"],d,local)
    require(compiled["status"] == item["expect_status"] and compiled["ids"] == item["expect_ids"] and
            compiled["route"] == item["expect_route"],"control expectation: "+item["name"])
    if "expect_optional" in item:
        require(compiled["optional_common"]["status"] == item["expect_optional"],"optional control: "+item["name"])
    recovery = recover(compiled,{"finite":item["domain"]},[],core,d)
    return {"name":item["name"],"scope":"SUPPLIED_INTERVAL_FINITE_CONTROL","constructor":compiled,
            "reference":fixture_reference(core,item["leader"],item["domain"],d,cfg),
            "recovery":recovery,"guard_checks":guards(compiled)}


def run(freeze):
    preflight(freeze)
    cfg = json.loads((HERE / "config.json").read_text())
    controls = [control(item,cfg) for item in cfg["controls"]]
    print(json.dumps({"controls":len(controls),"status":"EXPECTED_BEHAVIOR"}),flush=True)
    records = []
    for pair in cfg["pairs"]:
        row = family(pair,cfg)
        records.append(row)
        result = row.get("constructor",{})
        print(json.dumps({"pair":pair,"status":row["status"],"route":result.get("route"),
                          "ids":result.get("ids"),"failures":result.get("failures"),
                          "comparison":row.get("comparison")}),flush=True)
    return {"study":cfg["study"],"freeze_commit":freeze,"source_commit":cfg["source_commit"],
            "claim_status":"finite observations; family implications remain same-author proof candidates",
            "families":records,"controls":controls}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze",required=True)
    parser.add_argument("--output",type=Path,default=HERE / "results/RESULTS.json")
    args = parser.parse_args()
    require(not args.output.exists(),"refusing to overwrite results")
    result = run(args.freeze)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result,default=base.encode,sort_keys=True,separators=(",",":"))+"\n")
    print(json.dumps({"status":"COMPUTED_PENDING_VERIFICATION","families":len(result["families"])}))
