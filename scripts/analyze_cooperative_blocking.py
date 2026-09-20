"""Seven fixed eight-runner configurations and exact cooperative coverage.

Run: python -m scripts.analyze_cooperative_blocking
No sampled search or general classification is performed.
"""

import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from pathlib import Path

from lonely_runner.checker import check, circular_distance, feasible_intervals

ROOT = Path(__file__).resolve().parents[1]
CORE = (1, 4, 5, 6, 7)
DELTA = Q(1, 8)
TOUCHES = tuple(Q(q, 8) for q in (1, 3, 5, 7))
CASES = {
    "consecutive": tuple(range(1, 8)),
    "single_replacement": (1, 2, 3, 4, 5, 7, 12),
    "double_replacement": (*CORE, 11, 13),
    "control_11_12": (*CORE, 11, 12),
    "control_12_13": (*CORE, 12, 13),
    # Keep labels in this order to compare corresponding phase coordinates.
    "same_phases_19_13": (*CORE, 19, 13),
    "same_phases_11_21": (*CORE, 11, 21),
}


def intervals_json(intervals):
    return [[str(a), str(b)] for a, b in intervals]


def value(speeds, t):
    return min(circular_distance(v*t) for v in speeds)


def peak_faces(speeds, t, height):
    active = [v for v in speeds if circular_distance(v*t) == height]
    slopes = {v: (v if v*t % 1 < Q(1, 2) else -v) for v in active}
    # All selected maxima are below 1/2, so active curves are affine nearby.
    assert Q(0) < height < Q(1, 2)
    left_slope, right_slope = max(slopes.values()), min(slopes.values())
    assert left_slope > 0 > right_slope
    return {"time": str(t), "active_speeds": active,
            "active_phases": {str(v): str(v*t % 1) for v in active},
            "active_slopes": {str(v): s for v, s in slopes.items()},
            "left_controller": next(v for v in active if slopes[v] == left_slope),
            "right_controller": next(v for v in active if slopes[v] == right_slope),
            "left_slope": left_slope, "right_slope": right_slope}


def main():
    cases = []
    for label, relative in CASES.items():
        actual = (1, *(v+1 for v in relative))
        references = []
        for ref, speed in enumerate(actual):
            result = check(actual, reference=ref)
            assert result["maximum"]["crosschecked_with_intervals"]
            if ref == 0:
                selected = result
            references.append({"actual_speed": speed,
                               "maximum": result["maximum"]["separation"],
                               "tight": result["maximum"]["tight"],
                               "peak_times": result["maximum"]["times_original"]})
        maximum = Q(selected["maximum"]["separation"])
        assert all(value(relative, t) == DELTA for t in TOUCHES)
        triads = [(a,b,a+b) for a,b in combinations_with_replacement(sorted(relative),2)
                  if a+b in relative]
        cases.append({"label": label, "relative_speeds_in_label_order": relative,
                      "actual_speeds_in_label_order": actual, "reference_speed": 1,
                      "maximum": str(maximum), "tight": maximum == DELTA,
                      "peak_times": selected["maximum"]["times_original"],
                      "allowed_intervals": selected["intervals_original"],
                      "old_touch_phases": [[str(v*t % 1) for v in relative] for t in TOUCHES],
                      "peak_faces": [peak_faces(relative,Q(t),maximum)
                                     for t in selected["maximum"]["times_original"]],
                      "additive_triads": triads, "triad_count": len(triads),
                      "all_references": references,
                      "tight_actual_speeds": [r["actual_speed"] for r in references if r["tight"]]})
    by_name = {c["label"]: c for c in cases}
    expected = {"consecutive":"1/8", "single_replacement":"1/8", "double_replacement":"1/8",
                "control_11_12":"2/13", "control_12_13":"2/11",
                "same_phases_19_13":"4/25", "same_phases_11_21":"2/13"}
    assert all(by_name[name]["maximum"] == m for name,m in expected.items())
    # One actual speed changes from 14 to 13; the unique tight role transfers
    # from actual speed 1 to actual speed 8, whose absolute differences become
    # the consecutive set. This preserves that reference's whole distance curve.
    assert by_name["double_replacement"]["tight_actual_speeds"] == [1]
    assert by_name["control_11_12"]["tight_actual_speeds"] == [8]
    old_eight = next(r for r in by_name["double_replacement"]["all_references"] if r["actual_speed"] == 8)
    new_eight = next(r for r in by_name["control_11_12"]["all_references"] if r["actual_speed"] == 8)
    assert old_eight["maximum"] == "1/5" and new_eight["maximum"] == "1/8"
    new_actual = by_name["control_11_12"]["actual_speeds_in_label_order"]
    assert sorted(abs(v-8) for v in new_actual if v != 8) == list(range(1,8))
    for name in ("same_phases_19_13", "same_phases_11_21"):
        assert by_name[name]["old_touch_phases"] == by_name["double_replacement"]["old_touch_phases"]

    allowed = feasible_intervals(CORE, DELTA)
    windows = [(a,b) for a,b in allowed if a < b]
    half = [(Q(17,56),Q(5,16)), (Q(17,48),Q(3,8)), (Q(25,56),Q(15,32))]
    assert windows == sorted(half + [(1-b,1-a) for a,b in half])
    assert [a for a,b in allowed if a == b] == [Q(1,8),Q(7,8)]

    # Every possible change of the strict blocking predicate occurs at one of
    # these exact endpoints. Certify every open cell and every internal endpoint.
    blocking = {v: [(Q(m,v)-DELTA/v,Q(m,v)+DELTA/v) for m in range(v+1)] for v in (11,13)}
    evidence = []
    for a,b in windows:
        cuts = sorted({a,b,*(x for ints in blocking.values() for edge in ints for x in edge if a<x<b)})
        cells = []
        for left,right in zip(cuts,cuts[1:]):
            t = (left+right)/2
            assert value(CORE,t) > DELTA
            blockers = [v for v in blocking if circular_distance(v*t) < DELTA]
            assert blockers
            cells.append({"open_interval":[str(left),str(right)], "strict_blockers":blockers})
        for t in cuts[1:-1]:
            assert value(CORE,t) > DELTA
            assert any(circular_distance(v*t)<DELTA for v in blocking)
        evidence.append({"core_open_window":[str(a),str(b)], "cells":cells,
                         "internal_boundaries_checked":list(map(str,cuts[1:-1]))})

    assert feasible_intervals(CASES["double_replacement"],DELTA) == tuple((t,t) for t in TOUCHES)
    overlap = Q(41,88)-Q(47,104)
    assert overlap == Q(2,143)
    handoff = next(r for r in by_name["double_replacement"]["peak_faces"] if r["time"] == "3/8")
    assert handoff["active_speeds"] == [5,11,13]
    assert (handoff["left_controller"],handoff["right_controller"]) == (11,13)

    # Certify the claimed local envelope by its affine pieces on a small exact
    # neighborhood, including all vertices of each triangular distance curve.
    t0, eps = Q(3,8), Q(1,10000)
    for a,b,slope in [(t0-eps,t0,11),(t0,t0+eps,-13)]:
        for v in CASES["double_replacement"]:
            assert not any(a<Q(m,2*v)<b for m in range(2*v+1))
            assert all(circular_distance(v*t) >= DELTA+slope*(t-t0) for t in (a,b))
        assert value(CASES["double_replacement"],(a+b)/2) == DELTA+slope*((a+b)/2-t0)

    deletions = []
    for removed in (5,11,13):
        relative = tuple(v for v in CASES["double_replacement"] if v != removed)
        result = check((1,*(v+1 for v in relative)),threshold=DELTA)
        assert Q(result["maximum"]["separation"]) > DELTA
        deletions.append({"omitted_relative_speed":removed,"fixed_original_target":"1/8",
                          "maximum":result["maximum"]["separation"],
                          "peak_times":result["maximum"]["times_original"]})

    witnesses = []
    for t in (Q(9,20), Q(6,13), Q(7,15)):
        assert value(CORE,t)>DELTA
        witnesses.append({"time":str(t),"core_gap":str(value(CORE,t)),
                          "distance_11":str(circular_distance(11*t)),
                          "distance_13":str(circular_distance(13*t))})
    data = {"date":"2026-09-20", "base_commit":"79d88a4df75ee86d113c65d49670da6e83600f96",
            "checker_sha256":hashlib.sha256((ROOT/'lonely_runner/checker.py').read_bytes()).hexdigest(),
            "scope":"7 specified eight-runner configurations, all 56 references, and 3 fixed-target deletions",
            "threshold":"1/8", "core":CORE, "core_closed_allowed_intervals":intervals_json(allowed),
            "coverage":evidence, "third_window_blocking_intervals":{"11":["39/88","41/88"],"13":["47/104","49/104"]},
            "third_window_strict_overlap":str(overlap), "third_window_witnesses":witnesses,
            "cases":cases,"deletions":deletions,
            "role_transfer":{"actual_speed_change":[14,13],"old_unique_tight_speed":1,
                             "new_unique_tight_speed":8,"new_reference_absolute_differences":list(range(1,8)),
                             "old_speed_8_maximum":"1/5","new_speed_8_maximum":"1/8"},
            "limitations":"Known tight examples, bounded controls, exact explanations; no novelty or general proof claim"}
    (ROOT/'experiments/cooperative_blocking.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({"references_checked":sum(len(c['all_references']) for c in cases),
                      "cases":[{key:c[key] for key in ('label','maximum','triad_count','tight_actual_speeds')} for c in cases],
                      "core_open_windows":len(windows),"overlap":str(overlap),"deletions":deletions},indent=2))


if __name__ == '__main__':
    main()
