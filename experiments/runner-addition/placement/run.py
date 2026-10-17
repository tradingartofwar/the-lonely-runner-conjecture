"""Frozen exact placement study: midpoint obstruction and rational anchors."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import ceil, floor, gcd
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lonely_runner.checker import feasible_intervals


def require(ok, message):
    if not ok:
        raise ValueError(message)


def obstruction(interval, r, d):
    a, b = interval
    c, h = (a+b)/2, (b-a)/2
    z = r*c
    m = floor(z) if z % 1 <= F(1, 2) else floor(z)+1
    distance = abs(z-m)
    score = distance+r*h
    return {"r": r, "distance": distance, "half_sweep": r*h, "score": score,
            "blocked": score < d, "blocking_integer": m if score < d else None}


def whole_interval_safe(interval, speeds, d):
    a, b = interval
    return all(d <= s*a-floor(s*a) and s*b-floor(s*a) <= 1-d for s in speeds)


def anchor_interval(anchor, d):
    t = F(anchor["u"], anchor["v"])
    return tuple(sorted((t, t+anchor["direction"]*d/anchor["v"])))


def anchors_in(interval, d, cap):
    a, b = interval
    for v in range(1, min(floor(1/d), cap)+1):
        for u in range(v+1):
            if gcd(u, v) != 1:
                continue
            for direction in (-1, 1):
                anchor = {"u": u, "v": v, "direction": direction}
                left, right = anchor_interval(anchor, d)
                if a <= left <= right <= b:
                    return {**anchor, "interval": (left, right)}
    return None


def witness(t, speeds, d):
    phases = [s*t % 1 for s in speeds]
    require(all(d <= x <= 1-d for x in phases), "unsafe physical witness")
    return {"time": t, "phases": phases, "laps": [floor(s*t) for s in speeds]}


def palette(anchor, d):
    u, v, direction = (anchor[k] for k in ("u", "v", "direction"))
    bound = floor(v*(1-2*d)/d)
    allowed = []
    for s in range(1, bound+1):
        j = s*u % v
        ok = (j >= v*d and j+s*d <= v*(1-d)) if direction == 1 else (
            j <= v*(1-d) and j-s*d >= v*d)
        if ok:
            allowed.append(s)
    return {"bound": bound, "speeds": allowed}


def classify(interval, speeds, d, cfg):
    a, b = interval
    anchor = anchors_in(interval, d, cfg["max_denominator"])
    require(whole_interval_safe(interval, speeds, d), "invalid core interval")
    checks = []
    if a == b:
        cutoff = None
        domain = [a.denominator]
        require(domain[0] not in speeds, "singleton blocker is a core speed")
    else:
        cutoff = ceil(2*d/(b-a))
        domain = [r for r in range(1, min(cutoff-1, cfg["max_r"])+1) if r not in speeds]
    for r in domain:
        checks.append(obstruction(interval, r, d))
        if checks[-1]["blocked"]:
            break
    if checks and checks[-1]["blocked"]:
        status = "BLOCKED"
    elif cutoff is not None and cutoff-1 <= cfg["max_r"]:
        status = "UNIVERSAL_CANDIDATE"
    else:
        status = "UNKNOWN_BUDGET"
    require(not anchor or status == "UNIVERSAL_CANDIDATE", "anchor/obstruction disagreement")
    return {"interval": interval, "width": b-a, "cutoff": cutoff, "anchor": anchor,
            "laps": [floor(s*a) for s in speeds], "checks": checks, "status": status}


def preflight(freeze):
    data = (HERE / "manifest.json").read_bytes()
    archived = subprocess.check_output(
        ["git", "show", freeze+":experiments/runner-addition/placement/manifest.json"], cwd=ROOT)
    require(data == archived, "manifest differs from freeze")
    manifest = json.loads(data)
    for path, expected in manifest["sha256"].items():
        raw = (ROOT / path).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, "modified dependency: "+path)
        require(raw == subprocess.check_output(["git", "show", freeze+":"+path], cwd=ROOT),
                "dependency differs from freeze: "+path)


def run(freeze):
    preflight(freeze)
    cfg = json.loads((HERE / "config.json").read_text())
    old = json.loads((HERE.parent / "results/RESULTS.json").read_text())
    regression_contacts = 0
    for row in old["records"]:
        core = [tuple(map(F, x["interval"])) for x in row["components"]]
        d = F(row["threshold"])
        for case in row["cases"]:
            for interval, contact in zip(core, case["contacts"]):
                require(obstruction(interval, case["r"], d)["blocked"] != contact["hit"],
                        "midpoint/stored contact disagreement")
                regression_contacts += 1
    d = F(cfg["threshold"])
    development = []
    for anchor in cfg["anchors"]:
        source = next(row for row in old["records"] if row["pair"] == anchor["pair"]
                      and row["threshold"] == cfg["threshold"])
        leader = tuple(map(F, source["components"][source["leader"]]["interval"]))
        segment = anchor_interval(anchor, d)
        require(leader[0] <= segment[0] <= segment[1] <= leader[1], "predicted anchor outside leader")
        allowed = palette(anchor, d)
        require(set(source["speeds"]) <= set(allowed["speeds"]), "core absent from predicted palette")
        require(whole_interval_safe(segment, allowed["speeds"], d), "palette interval failure")
        v = anchor["v"]
        domain = list(range(1, 33))+[v*10**6, v*10**6+1, v*10**18, v*10**18+1]
        witnesses = []
        for r in domain:
            t = F(anchor["u"], v)+(anchor["direction"]*d/r if r % v == 0 else 0)
            require(segment[0] <= t <= segment[1], "anchor witness leaves interval")
            witnesses.append({"r": r, **witness(t, source["speeds"]+[r], d)})
        development.append({"anchor": anchor, "interval": segment, "leader": leader,
                            "core_speeds": source["speeds"], "palette": allowed,
                            "witnesses": witnesses})
    new = []
    for p, q in cfg["pairs"]:
        speeds = [p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q]
        require(len(set([0]+speeds)) == 9 and sum(speeds) <= cfg["max_core_speed_sum"], "core input cap")
        core = list(feasible_intervals(speeds, d))
        require(core and len(core) <= cfg["max_components"], "core component cap or empty core")
        rows = [{"id": i, **classify(interval, speeds, d, cfg)} for i, interval in enumerate(core)]
        blockers = sorted({row["checks"][-1]["r"] for row in rows if row["status"] == "BLOCKED"})
        children = []
        for r in blockers:
            full = feasible_intervals(speeds+[r], d)
            children.append({"r": r, "full_safe_set": full,
                             "witness": witness(full[0][0], speeds+[r], d) if full else None})
        leader = min(range(len(core)), key=lambda i: (-(core[i][1]-core[i][0]), core[i][0]))
        summary = {"components": len(rows), "leader": leader,
                   "universal_components": [r["id"] for r in rows if r["status"] == "UNIVERSAL_CANDIDATE"],
                   "blocked_components": [r["id"] for r in rows if r["status"] == "BLOCKED"],
                   "unknown_components": [r["id"] for r in rows if r["status"] == "UNKNOWN_BUDGET"],
                   "anchor_components": [r["id"] for r in rows if r["anchor"]],
                   "component_queries": sum(len(r["checks"]) for r in rows),
                   "full_core_misses_at_blockers": [x["r"] for x in children if not x["full_safe_set"]]}
        new.append({"pair": [p,q], "speeds": speeds, "components": rows,
                    "children_at_blockers": children, "summary": summary})
    fixtures = [([F(7,8),F(9,8)], 1, F(1,8), False),
                ([F(1,8),F(1,8)], 8, F(1,8), True),
                ([F(1,10),F(1,9)], 9, F(1,10), False),
                ([F(0),F(1,90)], 1, F(1,10), True)]
    for interval, r, delta, blocked in fixtures:
        require(obstruction(interval, r, delta)["blocked"] == blocked, "semantic obstruction control")
    require(not whole_interval_safe((F(9,10), F(11,10)), [1], F(1,10)), "lap-wrap control")
    return {"study": cfg["study"], "freeze_commit": freeze, "rule_commit": cfg["rule_commit"],
            "prior_contacts_matched": regression_contacts, "development": development,
            "new_records": new, "semantic_controls": 5,
            "claim_status": "finite exact observations; universal rules remain proof candidates"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--output", type=Path, default=HERE / "results/RESULTS.json")
    args = parser.parse_args()
    require(not args.output.exists(), "refusing to overwrite results")
    result = run(args.freeze)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result, default=str, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"prior_contacts_matched": result["prior_contacts_matched"],
                      "palette_sizes": [len(x["palette"]["speeds"]) for x in result["development"]],
                      "new_records": [{"pair": x["pair"], **x["summary"]} for x in result["new_records"]]}, indent=2))
