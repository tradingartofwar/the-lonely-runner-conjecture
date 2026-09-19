"""Exact interval explanation and touch-time patterns; no sampled certification.

Run: python -m scripts.analyze_eight_runner_replacement
"""

import hashlib
import json
from fractions import Fraction as Q
from math import gcd
from pathlib import Path

from lonely_runner.checker import check, circular_distance, feasible_intervals
from scripts.compare_tight_cases import envelope_vertices


ROOT = Path(__file__).resolve().parents[1]
CORE = (1, 2, 3, 4, 5, 7)
THRESHOLD = Q(1, 8)  # Keep the original eight-runner target after omitting one constraint.


def compact(result):
    return {"n": result["n"], "actual_speeds": result["velocities"],
            "reference_speed": result["reference_velocity"],
            "maximum": result["maximum"]["separation"],
            "tight": result["maximum"]["tight"],
            "peak_times": result["maximum"]["times_original"],
            "threshold_intervals": result["intervals_original"],
            "crosschecked": result["maximum"]["crosschecked_with_intervals"]}


def main():
    allowed = feasible_intervals(CORE, THRESHOLD)
    isolated = [a for a, b in allowed if a == b]
    windows = [(a, b) for a, b in allowed if a < b]
    assert windows == [(Q(9, 56), Q(7, 40)), (Q(33, 40), Q(47, 56))]
    assert isolated == [Q(1, 8), Q(3, 8), Q(5, 8), Q(7, 8)]
    core_vertices = [(Q(t), Q(y)) for t, y in envelope_vertices(CORE, 1)]
    # Certify strict > threshold throughout each open window: check every
    # interior corner/crossing and one point on each affine piece.
    for a, b in windows:
        cuts = sorted({a, b, *(t for t, y in core_vertices if a < t < b)})
        for t in [*cuts[1:-1], *((u + v) / 2 for u, v in zip(cuts, cuts[1:]))]:
            assert min(circular_distance(v * t) for v in CORE) > THRESHOLD

    replacements = []
    for w in (6, 11, 12, 13, 18):
        result = check((1, *(v + 1 for v in sorted((*CORE, w)))))
        old_values = [min(circular_distance(v * t) for v in (*CORE, w)) for t in isolated]
        assert old_values == [THRESHOLD] * 4
        replacements.append({"relative_speed": w, **compact(result),
                             "old_touch_values": [str(v) for v in old_values]})

    # Both original and doubled speed stay strictly below 1/8 on the closed
    # extra windows. Their nearest integer is fixed on each such window.
    blockers = []
    for w in (6, 12):
        evidence = []
        for (a, b), center in zip(windows, (Q(1, 6), Q(5, 6))):
            assert w * center == int(w * center)
            assert max(abs(w * (a - center)), abs(w * (b - center))) < THRESHOLD
            evidence.append({"window": [str(a), str(b)], "meeting": str(center),
                             "blocking_interval": [str(center - THRESHOLD / w), str(center + THRESHOLD / w)],
                             "largest_distance_on_window": str(max(circular_distance(w*a), circular_distance(w*b)))})
        blockers.append({"relative_speed": w, "coverage": evidence})

    # At 1/6, a tight integer replacement must be a multiple of six. To cover
    # the entire right side of the opening, 1/(8w) >= 7/40 - 1/6 = 1/120.
    center = Q(1, 6)
    right_reach = windows[0][1] - center
    speed_cap = THRESHOLD / right_reach
    assert speed_cap == 15
    candidates = [w for w in range(8, int(speed_cap) + 1) if w % 6 == 0]
    assert candidates == [12]

    schedules = []
    for n in (4, 8, 12, 16):
        result = check(range(1, n + 1))
        times = list(map(Q, result["maximum"]["times_original"]))
        assert times == [Q(q, n) for q in range(1, n) if gcd(q, n) == 1]
        gaps = [b-a for a, b in zip(times, times[1:] + [times[0] + 1])]
        assert all(1-t in times for t in times)
        schedules.append({"n": n, "times": list(map(str, times)),
                          "cyclic_gaps": list(map(str, gaps)),
                          "uniform_cyclic_spacing": len(set(gaps)) == 1})

    family_checks = []
    for n in (4, 8, 12, 14):
        speeds = sorted((set(range(1, n)) - {n-2}) | {2*(n-2)})
        result = check((1, *(v+1 for v in speeds)))
        assert result["maximum"]["tight"] == (n % 6 == 2)
        family_checks.append({"removed_relative_speed": n-2,
                              "inserted_relative_speed": 2*(n-2), **compact(result)})

    # Exact polygon vertices for a zoomed explanatory plot. Certification above
    # covers [0,1]; the focus below is only a display window.
    left, right = Q(31, 200), Q(9, 50)
    all_times = {left, right, center, *windows[0]}
    for speeds in (CORE, (*CORE, 6), (*CORE, 12), (*CORE, 18)):
        all_times.update(Q(t) for t, y in envelope_vertices(speeds, 1) if left <= Q(t) <= right)
    focus = []
    for t in sorted(all_times):
        values = {str(w): circular_distance(w*t) for w in (6,12,18)}
        base = min(circular_distance(v*t) for v in CORE)
        focus.append({"t": str(t), "core": str(base),
                      "inserted": {k: str(v) for k,v in values.items()},
                      "combined": {k: str(min(v,base)) for k,v in values.items()}})

    data = {"date": "2026-09-19", "base_commit": "c7b00467700d3a65ab95f91af147edccb8f876f1",
            "checker_sha256": hashlib.sha256((ROOT/'lonely_runner/checker.py').read_bytes()).hexdigest(),
            "scope": "selected actual speed 1; eight-runner target 1/8; positive integer relative replacements",
            "core_relative_speeds": CORE, "threshold": str(THRESHOLD),
            "core_closed_allowed_intervals": [[str(a),str(b)] for a,b in allowed],
            "core_strict_open_windows": [[str(a),str(b)] for a,b in windows],
            "unchanged_touch_times": list(map(str,isolated)), "blocker_coverage": blockers,
            "replacement_results": replacements,
            "fixed_replacement_classification": {"necessary_multiple": 6, "necessary_upper_bound": str(speed_cap),
                                                 "unique_tight_integer_replacement_above_7": 12},
            "consecutive_schedules": schedules, "acceleration_family_checks": family_checks,
            "focus_plot": focus,
            "limitations": "No classification of arbitrary tight sets; new proof candidates require independent review; elementary fixed-case argument reproduces known structure"}
    path=ROOT/'experiments/eight_runner_replacement.json'
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({"replacements": [{k:r[k] for k in ('relative_speed','maximum','tight','peak_times')} for r in replacements],
                      "schedules":schedules, "unique_tight_replacement_above_7":12},indent=2))


if __name__ == '__main__':
    main()
