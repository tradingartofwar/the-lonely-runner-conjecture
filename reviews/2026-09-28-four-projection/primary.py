#!/usr/bin/env python3
"""Frozen fourth-residual test: bound gate plus22projection diagnostic.

No interval/event enumeration. Exact rational arithmetic only.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELTA = F(1, 8)


def ceiling(x):
    return -((-x.numerator) // x.denominator)


def distance(x):
    p = x % 1
    return min(p, 1 - p)


def project(v, phase, t):
    lap = ceiling(v * t + phase - 1 + DELTA)
    out = max(t, (lap + DELTA - phase) / v)
    assert 0 <= out-t < 2*DELTA/v
    assert distance(v*out+phase) >= DELTA
    return out, {"speed": v, "phase": str(phase), "input": str(t),
                 "output": str(out), "lap": lap, "advance": str(out-t)}


def lifted(speeds, phases, left, right):
    rows = []
    for v, alpha in zip(speeds, phases):
        value = v*(left+right)/2+alpha
        lap = value.numerator//value.denominator
        lo, hi = v*left+alpha-lap, v*right+alpha-lap
        assert DELTA <= lo <= hi <= 1-DELTA
        rows.append({"speed": v, "phase": str(alpha), "lap": lap,
                     "phase_left": str(lo), "phase_right": str(hi)})
    return rows


def calculate_case(case, core, window, kind):
    speeds = case["speeds"]
    phases = list(map(F, case.get("phases", ["0"]*4)))
    a, b, c, d = speeds
    assert 0 < a <= b <= c <= d
    left, right = map(F, window)
    triple_bound = F(1,4*b)+F(1,2*c)+F(1,d)
    slow_width = F(3,4*a)
    certified = triple_bound <= slow_width
    # Nested order is fixed before comparison with the oracle.
    triple = [1,2,3,2,3,1,2,3,2,3]
    order = [0]+triple+[0]+triple
    t, trace = left, []
    for index in order:
        t, row = project(speeds[index], phases[index], t)
        row["runner_index"] = index
        trace.append(row)
    assert len(trace) == 22
    margins = [distance(v*t+alpha)-DELTA for v,alpha in zip(speeds,phases)]
    feasible = min(margins) >= 0
    if certified:
        assert feasible
    if t > right:
        verdict = "empty_window"
    elif feasible:
        verdict = "earliest_witness"
    else:
        verdict = "inconclusive"
    component, certificate = None, None
    if verdict == "earliest_witness":
        end = right
        for v, alpha in zip(speeds,phases):
            x = v*t+alpha
            lap = x.numerator//x.denominator
            end = min(end,(lap+1-DELTA-alpha)/v)
        assert t <= end
        component = [str(t),str(end)]
        certificate = lifted(core+speeds,[F(0)]*len(core)+phases,t,end)
    return {"id": case["id"], "kind": kind, "speeds": speeds,
            "phases": list(map(str,phases)), "core": core, "window":list(map(str,(left,right))),
            "core_certificate":lifted(core,[F(0)]*len(core),left,right),
            "triple_wait_bound":str(triple_bound), "slow_safe_width":str(slow_width),
            "bound_minus_width":str(triple_bound-slow_width),
            "condition_passes":certified,
            "gated_policy": "guaranteed_selector" if certified else "condition_not_met",
            "diagnostic_trace":trace, "final_time":str(t),
            "final_safe":feasible, "final_margins":list(map(str,margins)),
            "diagnostic_verdict":verdict,
            "earliest_in_window":str(t) if verdict=="earliest_witness" else None,
            "first_component":component, "first_component_certificate":certificate}


def calculate():
    protocol=json.loads((HERE/'protocol.json').read_text())
    physical=[calculate_case(c,protocol['physical_core'],protocol['physical_window'],'physical')
              for c in protocol['cases']]
    auxiliary=[calculate_case(c,[],c['window'],'auxiliary') for c in protocol['auxiliary_cases']]
    return {"status":"pass","physical_cases":physical,"auxiliary_cases":auxiliary,
            "physical_count":len(physical),"auxiliary_count":len(auxiliary),
            "projection_calls":22*(len(physical)+len(auxiliary)),
            "claim_status":"General conditional implication is a supplied proof candidate; raw22step outcomes are bounded observations."}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    result=calculate()
    target=HERE/'results.json'
    if args.check:
        assert json.loads(target.read_text())==result
    else:
        target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"status":"pass","physical_condition_passes":sum(c['condition_passes'] for c in result['physical_cases']),
                      "physical_outcomes":{c['id']:c['diagnostic_verdict'] for c in result['physical_cases']},
                      "auxiliary_condition_passes":sum(c['condition_passes'] for c in result['auxiliary_cases']),
                      "projection_calls":result['projection_calls']}))


if __name__=='__main__':
    main()
