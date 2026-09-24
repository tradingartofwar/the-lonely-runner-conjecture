"""Finite certificates for {0,1,4,5,6,7,x,y}, with unbounded integer x,y.

Run: python -m scripts.analyze_two_variable_speeds
See notes/TWO_VARIABLE_SPEEDS.md for the unbounded reduction and review scope.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals


ROOT = Path(__file__).resolve().parents[1]
CORE = (1, 4, 5, 6, 7)
N = 8
DELTA = Q(1, N)
J = (Q(25, 56), Q(15, 32))
FAST_CUTOFF = 34
BASE_COMMIT = "499a6ba638d82a04c53a80a48266e0f9d67607b4"


def phase_certificate(speeds, interval):
    """Direct certificate for every point of a closed interval, no sampling.

    With one fixed integer part, each phase is affine between the endpoints.
    Checking its endpoints against [delta,1-delta] certifies the entire interval.
    """
    a, b = interval
    assert a < b
    rows = []
    for v in speeds:
        va, vb = v * a, v * b
        integer = va.numerator // va.denominator
        assert integer == vb.numerator // vb.denominator
        left, right = va - integer, vb - integer
        assert DELTA <= left < right <= 1 - DELTA
        rows.append({"speed": v, "integer_part": integer,
                     "phase_left": str(left), "phase_right": str(right)})
    return rows


def point_certificate(speeds, t):
    distances = {str(v): circular_distance(v * t) for v in speeds}
    minimum = min(distances.values())
    assert minimum >= DELTA
    return {"time": str(t), "distances": {v: str(d) for v, d in distances.items()},
            "minimum": str(minimum)}


def encode_intervals(intervals):
    return [[str(a), str(b)] for a, b in intervals]


def clipped_intervals(intervals, window):
    a, b = window
    return tuple((max(a, c), min(b, d)) for c, d in intervals
                 if max(a, c) <= min(b, d))


def duration(intervals):
    return sum((b - a for a, b in intervals), Q(0))


def main():
    length = J[1] - J[0]
    assert length == Q(5, 224)
    base_intervals = feasible_intervals(CORE, DELTA)
    assert J in base_intervals
    base_phases = phase_certificate(CORE, J)

    # The note proves B_v(J) <= L/4 + 3/(16v). Two speeds >=34 therefore
    # leave positive duration. Evaluating the worst-case bound is exact.
    fast_clear_lower_bound = length / 2 - Q(3, 16) * (Q(1, 34) + Q(1, 34))
    assert fast_clear_lower_bound == Q(1, 7616) > 0

    # Exhaustive only after the analytic reduction to min(x,y)<34.
    slow_speeds = tuple(v for v in range(1, FAST_CUTOFF) if v not in CORE)
    assert len(slow_speeds) == 28
    slow_rows, residual_pairs = [], []
    for x in slow_speeds:
        intervals = feasible_intervals((*CORE, x), DELTA)
        interval = max(intervals, key=lambda ab: ab[1] - ab[0])
        width = interval[1] - interval[0]
        assert width > 0
        phases = phase_certificate((*CORE, x), interval)
        strict_cap = 2 * DELTA / width
        # Complete removal of a connected CLOSED interval by disjoint OPEN
        # windows requires 1/(4y)>width, hence the strict y<cap.
        integer_upper = (strict_cap.numerator - 1) // strict_cap.denominator
        candidates = [y for y in range(x + 1, integer_upper + 1)
                      if y not in CORE and (x % 8 == 0 or y % 8 == 0)]
        residual_pairs.extend((x, y) for y in candidates)
        slow_rows.append({"x": x, "interval": list(map(str, interval)),
                          "width": str(width), "strict_upper_bound_on_y": str(strict_cap),
                          "candidate_y": candidates, "phase_certificate": phases})

    expected_pairs = [(2, 8), (3, 8), (8, 9), (8, 10),
                      (8, 11), (11, 16), (11, 24), (22, 24)]
    assert residual_pairs == expected_pairs
    simple_times = {pair: Q(t) for pair, t in zip(expected_pairs,
                    ("4/13", "5/11", "6/13", "5/11", "4/13", "7/15", "4/13", "4/13"))}
    pair_certificates = []
    for x, y in residual_pairs:
        speeds = (*CORE, x, y)
        assert len(set(speeds)) == N - 1
        allowed = feasible_intervals(speeds, DELTA)
        t = simple_times[(x, y)]
        assert any(a <= t <= b for a, b in allowed)
        point = point_certificate(speeds, t)
        assert Q(point["minimum"]) > DELTA
        pair_certificates.append({"x": x, "y": y, "witness": point,
                                  "allowed_intervals": encode_intervals(allowed)})

    # Actual cooperative coverage defeats the previous one-runner mechanism.
    old_interval = (Q(17, 56), Q(5, 16))
    window23 = ((Q(7) - DELTA) / 23, (Q(7) + DELTA) / 23)
    window16 = ((Q(5) - DELTA) / 16, (Q(5) + DELTA) / 16)
    a, b = old_interval
    assert window23[0] < a < window16[0] < window23[1] < b < window16[1]
    overlap = window23[1] - window16[0]
    assert overlap == Q(15, 2944)
    assert circular_distance(16 * a) == Q(1, 7) > DELTA
    assert circular_distance(23 * b) == Q(3, 16) > DELTA
    cooperative_speeds = (*CORE, 16, 23)
    assert not clipped_intervals(feasible_intervals(cooperative_speeds, DELTA), old_interval)
    cooperative_phases = phase_certificate(cooperative_speeds, J)
    cooperative_witness = point_certificate(cooperative_speeds, Q(5, 11))
    assert Q(cooperative_witness["minimum"]) == Q(2, 11)

    # Fast control: both variable speeds are multiples of 8, so 1/8 fails.
    # Check the duration inequality against exact interval intersections.
    fast_speeds = (40, 48)
    single_durations = []
    for v in fast_speeds:
        clear = clipped_intervals(feasible_intervals((v,), DELTA), J)
        blocked = length - duration(clear)
        upper = length / 4 + Q(3, 16 * v)
        assert blocked <= upper
        single_durations.append({"speed": v, "blocked_duration_in_J": str(blocked),
                                 "duration_upper_bound": str(upper)})
    fast_allowed = clipped_intervals(feasible_intervals((*CORE, *fast_speeds), DELTA), J)
    fast_clear_duration = duration(fast_allowed)
    assert fast_clear_duration >= fast_clear_lower_bound
    c, d = max(fast_allowed, key=lambda ab: ab[1] - ab[0])
    fast_witness = point_certificate((*CORE, *fast_speeds), (c + d) / 2)

    # The old tight case remains a control against inferring universal slack.
    tight_control = (*CORE, 11, 13)
    tight_allowed = feasible_intervals(tight_control, DELTA)
    old_times = (Q(1, 8), Q(3, 8), Q(5, 8), Q(7, 8))
    assert tight_allowed == tuple((t, t) for t in old_times)

    data = {
        "date": "2026-09-24", "base_commit": BASE_COMMIT,
        "checker_sha256": hashlib.sha256((ROOT / "lonely_runner/checker.py").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "Elementary finite-reduction argument with exact certificates; independent proof review outstanding; no novelty claim",
        "scope": {"n": N, "selected_reference": 0, "fixed_speeds": CORE,
                  "variables": "distinct positive integers x<y, both outside CORE",
                  "threshold": str(DELTA), "starts": "all together"},
        "core_allowed_intervals": encode_intervals(base_intervals),
        "fast_case": {"interval_J": list(map(str, J)), "length": str(length),
                      "phase_certificate": base_phases,
                      "single_speed_blocking_bound": "L/4+3/(16v)",
                      "both_speeds_at_least": FAST_CUTOFF,
                      "clear_duration_lower_bound": str(fast_clear_lower_bound)},
        "modular_restriction": "If neither x nor y is divisible by 8, t=1/8 is valid",
        "slow_speed_table": slow_rows,
        "residual_pairs": pair_certificates,
        "cooperative_control": {"pair": [16, 23], "old_interval": list(map(str, old_interval)),
                                "window23": list(map(str, window23)), "window16": list(map(str, window16)),
                                "strict_overlap": str(overlap), "whole_J_phase_certificate": cooperative_phases,
                                "witness": cooperative_witness},
        "fast_control": {"pair": fast_speeds, "single_blocking_durations": single_durations,
                         "clear_intervals_in_J": encode_intervals(fast_allowed),
                         "clear_duration_in_J": str(fast_clear_duration), "witness": fast_witness},
        "tight_control": {"pair": [11, 13], "allowed_intervals": encode_intervals(tight_allowed)},
        "verification_counts": {"slow_speed_interval_certificates": len(slow_rows),
                                "residual_pair_witnesses": len(pair_certificates),
                                "additional_prescribed_pair_controls": 3},
        "limitations": "Selected reference only. Integer two-parameter family, not arbitrary speeds or runner counts. Finite checks support the written reduction; no all-reference or maximum classification claim.",
    }
    output = ROOT / "experiments/two_variable_speeds.json"
    output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"slow_speed_count": len(slow_rows),
                      "fast_clear_lower_bound": str(fast_clear_lower_bound),
                      "residual_pairs": [{"pair": [r["x"], r["y"]], **r["witness"]}
                                         for r in pair_certificates],
                      "cooperative_witness": cooperative_witness,
                      "fast_control_clear_duration": str(fast_clear_duration)}, indent=2))


if __name__ == "__main__":
    main()
