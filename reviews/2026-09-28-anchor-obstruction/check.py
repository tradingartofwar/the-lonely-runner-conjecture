#!/usr/bin/env python3
"""Exact constructed obstruction; no speed scan or lap enumeration.

Run from any directory. --check compares the committed deterministic results.
The unbounded statement is a written proof candidate, not a finite test result.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

DELTA = F(1, 8)
CORE = (1, 4, 5, 6, 7)
Q = 840
HERE = Path(__file__).resolve().parent


def phase(value):
    return value % 1


def distance(value):
    p = phase(value)
    return min(p, 1 - p)


def first_band(v, anchor, direction):
    p = phase(v * anchor)
    if p == 0:
        return DELTA / v, (1 - DELTA) / v
    assert DELTA <= p <= 1 - DELTA
    exit_ = ((1 - DELTA - p) if direction == 1 else (p - DELTA)) / v
    return F(0), exit_


def interval_certificate(speeds, left, right):
    """One lifted safe band per runner proves the entire closed interval safe."""
    assert left <= right
    rows = []
    for v in speeds:
        mid = v * (left + right) / 2
        lap = mid.numerator // mid.denominator
        low, high = v * left - lap, v * right - lap
        assert DELTA <= low <= high <= 1 - DELTA
        minimum_margin = min(low - DELTA, 1 - DELTA - high)
        rows.append({"speed": v, "absolute_lap": lap,
                     "phase_left": str(low), "phase_right": str(high),
                     "minimum_margin": str(minimum_margin),
                     "midpoint_margin": str(distance(mid) - DELTA)})
    return {"left": str(left), "right": str(right),
            "width": str(right - left), "runners": rows}


def calculate():
    speeds = CORE + (Q, 8 * Q)
    anchors = sorted({F(a, d) for d in range(1, 9) for a in range(d)})
    assert len(anchors) == 22
    records = []
    for anchor in anchors:
        assert phase(Q * anchor) == phase(8 * Q * anchor) == 0
        for direction in (1, -1):
            bands = {v: first_band(v, anchor, direction) for v in speeds}
            entry = max(a for a, b in bands.values())
            exit_ = min(b for a, b in bands.values())
            pair_gap = bands[Q][0] - bands[8 * Q][1]
            assert pair_gap == F(1, 64 * Q)
            assert entry - exit_ >= pair_gap > 0
            records.append({
                "anchor": str(anchor), "direction": direction,
                "entry": str(entry), "exit": str(exit_), "status": "fails",
                "entry_controllers": [v for v, b in bands.items() if b[0] == entry],
                "exit_controllers": [v for v, b in bands.items() if b[1] == exit_],
                "pair_gap": str(pair_gap),
                "first_bands": {str(v): [str(a), str(b)]
                                for v, (a, b) in bands.items()},
            })

    # Original predeclared certificate and post-protocol same-menu refinement.
    # B=10^12 is formula-only: no iteration through B laps is performed.
    diagnostics = []
    for budget in (1, 10**12):
        fast = 8 * budget * Q
        first_entry = F(1, 8 * Q)
        last_exit = F(8 * budget - 1, 64 * budget * Q)
        gap = first_entry - last_exit
        assert gap == F(1, 64 * budget * Q) > 0
        s_left = F(8 * budget + 1, 64 * budget * Q)
        s_right = F(8 * budget + 7, 64 * budget * Q)
        assert DELTA < Q * s_left < Q * s_right < 1 - DELTA
        assert fast * s_left == budget + DELTA
        assert fast * s_right == budget + 1 - DELTA
        assert s_right < F(1, 112) < F(1, 48)
        forward = interval_certificate(CORE + (Q, fast),
                                       F(17, 56) + s_left, F(17, 56) + s_right)
        backward = interval_certificate(CORE + (Q, fast),
                                        F(3, 8) - s_right, F(3, 8) - s_left)
        for cert in (forward, backward):
            assert F(cert["width"]) == F(3, 32 * budget * Q)
            assert all(F(row["midpoint_margin"]) > 0 for row in cert["runners"])
            assert all(F(row["minimum_margin"]) > 0
                       for row in cert["runners"] if row["speed"] != fast)
            assert cert["runners"][-1]["minimum_margin"] == "0"
        diagnostics.append({
            "q": Q, "early_lap_budget": budget, "fast_speed": fast,
            "kind": "physical predeclared case" if budget == 1 else "formula-only diagnostic",
            "slow_first_entry": str(first_entry),
            "fast_last_exit_within_budget": str(last_exit), "strict_gap": str(gap),
            "safe_displacements": [str(s_left), str(s_right)],
            "slow_lap_index": 0, "fast_lap_index": budget,
            "original_forward_from_17_over_56": forward,
            "post_protocol_backward_from_3_over_8": backward,
        })

    # Sharp ratio7 contact: equality is valid, not an obstruction.
    boundary_speeds = CORE + (Q, 7 * Q)
    a = F(17, 56)
    bands = {v: first_band(v, a, 1) for v in boundary_speeds}
    entry = max(x for x, y in bands.values())
    exit_ = min(y for x, y in bands.values())
    assert entry == exit_ == F(1, 8 * Q)
    t = a + entry
    point = interval_certificate(boundary_speeds, t, t)
    assert distance(Q * t) == distance(7 * Q * t) == DELTA
    # One-sided blocking on a whole neighborhood follows from these phases
    # staying in the adjacent affine lap: slow blocks left, fast blocks right.
    epsilon = F(1, 16 * 7 * Q)
    assert 0 < phase(Q * (t - epsilon)) < DELTA
    assert 1 - DELTA < phase(7 * Q * (t + epsilon)) < 1

    return {
        "status": "pass", "n": 8, "reference": 0, "threshold": str(DELTA),
        "moving_speeds": list(speeds), "common_start": True,
        "anchor_count": len(anchors), "directional_failures": len(records),
        "first_bands_checked": len(records) * len(speeds),
        "all_anchor_records": records,
        "diagnostics": diagnostics,
        "ratio7_boundary": {"anchor": str(a), "direction": 1,
                            "displacement": str(entry), "point": point,
                            "left_blocker": Q, "right_blocker": 7 * Q,
                            "certified_local_radius": str(epsilon)},
        "interpretation": "The first/first-B-safe-lap certificate class is incomplete. "
                          "This is not failed loneliness or new family coverage.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = calculate()
    target = HERE / "results.json"
    if args.check:
        assert json.loads(target.read_text()) == payload, "Committed results differ"
    else:
        target.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"status": "pass", "anchors": payload["anchor_count"],
                      "directional_failures": payload["directional_failures"],
                      "first_bands": payload["first_bands_checked"],
                      "diagnostic_budgets": [d["early_lap_budget"] for d in payload["diagnostics"]],
                      "mode": "check" if args.check else "write"}))


if __name__ == "__main__":
    main()
