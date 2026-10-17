"""Alternate placement verifier: safe-band intersections and threshold events.

Same author as run.py; no primary or checker imports, no formal certification.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import ceil, floor, gcd
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def check(ok, message):
    if not ok:
        raise ValueError(message)


def parse(rows):
    return [tuple(map(F, row)) for row in rows]


def safe(speeds, t, d):
    return all(d <= s*t % 1 <= 1-d for s in speeds)


def full_interval(interval, speeds, d):
    a, b = interval
    for s in speeds:
        low_lap, high_lap = floor(s*a), floor(s*b)
        if low_lap != high_lap or not safe([s], a, d) or not safe([s], b, d):
            return False
    return True


def band_hit(interval, r, d):
    a, b = interval
    for j in range(floor(r*a)-1, floor(r*b)+2):
        if max(a, (j+d)/r) <= min(b, (j+1-d)/r):
            return True
    return False


def events_union(speeds, d):
    events = sorted({F(0),F(1)} | {(F(j)+x)/s for s in speeds for j in range(s)
                                  for x in (d, 1-d)})
    pieces = [(t,t) for t in events if safe(speeds,t,d)]
    pieces += [(a,b) for a,b in zip(events,events[1:]) if safe(speeds,(a+b)/2,d)]
    result = []
    for a,b in sorted(pieces):
        if result and a <= result[-1][1]:
            result[-1] = result[-1][0], max(b,result[-1][1])
        else:
            result.append((a,b))
    return result, len(events)


def first_anchor(interval, speeds, d, cap):
    for denominator in range(1, min(cap, floor(1/d))+1):
        for numerator in range(denominator+1):
            if gcd(numerator,denominator) != 1:
                continue
            t0 = F(numerator,denominator)
            for direction in (-1,1):
                segment = tuple(sorted((t0,t0+direction*d/denominator)))
                if (interval[0] <= segment[0] <= segment[1] <= interval[1]
                        and full_interval(segment,speeds,d)):
                    return {"u":numerator,"v":denominator,"direction":direction,
                            "interval":[str(x) for x in segment]}
    return None


def check_witness(row, speeds, d):
    t = F(row["time"])
    check(safe(speeds,t,d), "unsafe witness")
    check([s*t % 1 for s in speeds] == list(map(F,row["phases"])), "witness phases")
    check([floor(s*t) for s in speeds] == row["laps"], "witness laps")


def verify(path):
    raw = path.read_bytes()
    result = json.loads(raw)
    cfg = json.loads((HERE / "config.json").read_text())
    manifest_bytes = (HERE / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    freeze = result["freeze_commit"]
    check(manifest_bytes == subprocess.check_output(
        ["git","show",freeze+":experiments/runner-addition/placement/manifest.json"],cwd=ROOT), "manifest freeze")
    for name, expected in manifest["sha256"].items():
        local = (ROOT/name).read_bytes()
        check(hashlib.sha256(local).hexdigest() == expected, "dependency hash")
        check(local == subprocess.check_output(["git","show",freeze+":"+name],cwd=ROOT), "dependency freeze")
    check(result["study"] == cfg["study"] and result["rule_commit"] == cfg["rule_commit"], "study identity")
    old = json.loads((HERE.parent / "results/RESULTS.json").read_text())
    counts = {"prior_contacts":0,"anchor_witnesses":0,"palette_candidates":0,
              "new_components":0,"new_contacts":0,"child_sets":0,"events":0,"repair_witnesses":0}
    for record in old["records"]:
        core = [tuple(map(F,c["interval"])) for c in record["components"]]
        for case in record["cases"]:
            for interval,contact in zip(core,case["contacts"]):
                check(band_hit(interval,case["r"],F(record["threshold"])) == contact["hit"], "prior contact regression")
                counts["prior_contacts"] += 1
    check(result["prior_contacts_matched"] == counts["prior_contacts"], "regression count")
    d = F(cfg["threshold"])
    check(len(result["development"]) == len(cfg["anchors"]), "development count")
    for configured, record in zip(cfg["anchors"],result["development"]):
        check(record["anchor"] == configured, "anchor identity")
        u,v,sgn = (configured[k] for k in ("u","v","direction"))
        check(gcd(u,v) == 1 and v*d <= 1 and sgn in (-1,1), "anchor hypotheses")
        segment = tuple(sorted((F(u,v),F(u,v)+sgn*d/v)))
        check(segment == tuple(map(F,record["interval"])), "anchor interval")
        source = next(x for x in old["records"] if x["pair"] == configured["pair"]
                      and x["threshold"] == cfg["threshold"])
        speeds = source["speeds"]
        check(record["core_speeds"] == speeds, "development speeds")
        leader = tuple(map(F,source["components"][source["leader"]]["interval"]))
        check(leader == tuple(map(F,record["leader"])), "development leader")
        check(leader[0] <= segment[0] <= segment[1] <= leader[1], "anchor containment")
        check(full_interval(segment,speeds,d), "core endpoint/lap condition")
        bound = floor((1-2*d)/(segment[1]-segment[0]))
        candidates = list(range(1,bound+1))
        permitted = [s for s in candidates if full_interval(segment,[s],d)]
        check(record["palette"] == {"bound":bound,"speeds":permitted}, "palette discrepancy")
        check(set(speeds) <= set(permitted), "development core not in palette")
        counts["palette_candidates"] += len(candidates)
        expected_domain = list(range(1,33))+[v*10**6,v*10**6+1,v*10**18,v*10**18+1]
        check([x["r"] for x in record["witnesses"]] == expected_domain, "witness domain")
        for row in record["witnesses"]:
            r = row["r"]
            expected = F(u,v) if r % v else F(u,v)+sgn*d/r
            check(F(row["time"]) == expected and segment[0] <= expected <= segment[1], "witness construction")
            check_witness(row,speeds+[r],d)
            counts["anchor_witnesses"] += 1
    check([row["pair"] for row in result["new_records"]] == cfg["pairs"], "new pair domain")
    summaries = []
    for record in result["new_records"]:
        p,q = record["pair"]
        speeds = [p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q]
        check(speeds == record["speeds"] and len(set([0]+speeds)) == 9, "new core identity")
        core,event_count = events_union(speeds,d)
        counts["events"] += event_count
        check(core == [tuple(map(F,x["interval"])) for x in record["components"]], "complete core mismatch")
        check(sum(speeds) <= cfg["max_core_speed_sum"] and len(core) <= cfg["max_components"], "core cap")
        statuses,anchors,blockers,queries = [],[],[],0
        for i,(interval,row) in enumerate(zip(core,record["components"])):
            a,b = interval
            counts["new_components"] += 1
            check(row["id"] == i and F(row["width"]) == b-a, "component metadata")
            check(full_interval(interval,speeds,d), "unsafe component")
            check(row["laps"] == [floor(s*a) for s in speeds], "component laps")
            cutoff = ceil(2*d/(b-a)) if a != b else None
            check(row["cutoff"] == cutoff, "cutoff")
            domain = ([a.denominator] if a == b else
                      [r for r in range(1,min(cutoff-1,cfg["max_r"])+1) if r not in speeds])
            expected_checks = []
            for r in domain:
                expected_checks.append(r)
                if not band_hit(interval,r,d):
                    break
            check([x["r"] for x in row["checks"]] == expected_checks, "incomplete classifier domain")
            for obs in row["checks"]:
                r = obs["r"]
                check(r not in speeds and r > 0, "inadmissible blocker test")
                hit = band_hit(interval,r,d)
                check(hit != obs["blocked"], "placement/band disagreement")
                z = r*(a+b)/2
                distance = min(z % 1,1-z % 1)
                check(F(obs["distance"]) == distance and F(obs["half_sweep"]) == r*(b-a)/2, "placement fields")
                check(F(obs["score"]) == distance+r*(b-a)/2, "placement score")
                if not hit:
                    m = obs["blocking_integer"]
                    check(isinstance(m,int) and r*b-d < m < r*a+d, "blocking integer certificate")
                else:
                    check(obs["blocking_integer"] is None, "spurious blocking integer")
                queries += 1
            failed = bool(expected_checks) and not band_hit(interval,expected_checks[-1],d)
            status = "BLOCKED" if failed else ("UNIVERSAL_CANDIDATE" if cutoff is not None
                      and cutoff-1 <= cfg["max_r"] else "UNKNOWN_BUDGET")
            check(row["status"] == status, "coverage status")
            statuses.append(status)
            if failed:
                blockers.append(expected_checks[-1])
            anchor = first_anchor(interval,speeds,d,cfg["max_denominator"])
            check(row["anchor"] == anchor, "anchor search disagreement")
            if anchor:
                check(status == "UNIVERSAL_CANDIDATE", "anchor theorem failure")
                anchors.append(i)
        counts["new_contacts"] += queries
        check([x["r"] for x in record["children_at_blockers"]] == sorted(set(blockers)), "child domain")
        misses = []
        for row in record["children_at_blockers"]:
            full,event_count = events_union(speeds+[row["r"]],d)
            counts["events"] += event_count
            counts["child_sets"] += 1
            check(full == parse(row["full_safe_set"]), "complete child set discrepancy")
            if full:
                check(F(row["witness"]["time"]) == full[0][0], "first repair witness")
                check_witness(row["witness"],speeds+[row["r"]],d)
                counts["repair_witnesses"] += 1
            else:
                check(row["witness"] is None, "witness on empty set")
                misses.append(row["r"])
        summary = {"components":len(core),
                   "leader":min(range(len(core)),key=lambda i:(-(core[i][1]-core[i][0]),core[i][0])),
                   "universal_components":[i for i,s in enumerate(statuses) if s == "UNIVERSAL_CANDIDATE"],
                   "blocked_components":[i for i,s in enumerate(statuses) if s == "BLOCKED"],
                   "unknown_components":[i for i,s in enumerate(statuses) if s == "UNKNOWN_BUDGET"],
                   "anchor_components":anchors,"component_queries":queries,
                   "full_core_misses_at_blockers":misses}
        check(record["summary"] == summary, "summary mismatch")
        summaries.append({"pair":record["pair"],**summary})
    controls = [((F(7,8),F(9,8)),1,F(1,8),True),((F(1,8),F(1,8)),8,F(1,8),False),
                ((F(1,10),F(1,9)),9,F(1,10),True),((F(0),F(1,90)),1,F(1,10),False)]
    for interval,r,delta,expected in controls:
        check(band_hit(interval,r,delta) == expected, "semantic hit control")
    check(not full_interval((F(9,10),F(11,10)),[1],F(1,10)), "wrap control")
    check(result["semantic_controls"] == 5, "control count")
    return {"status":"PASS","freeze_commit":freeze,"counts":counts,"new_summaries":summaries,
            "results_sha256":hashlib.sha256(raw).hexdigest(),"semantic_controls":5,
            "limits":"Same-author alternate algorithms. Universal statements remain proof candidates."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,default=HERE / "results/RESULTS.json")
    parser.add_argument("--output",type=Path,default=HERE / "results/VERIFICATION.json")
    args = parser.parse_args()
    check(not args.output.exists(), "refusing to overwrite verification")
    result = verify(args.input)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2))
