#!/usr/bin/env python3
"""Post-protocol nested triple diagnostic on one already frozen input."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from primary import project, distance, lifted_certificate

HERE = Path(__file__).resolve().parent


def calculate():
    speeds = (1, 7, 8)
    delta = F(1, 8)
    left, right = F(7, 8), F(6, 5)
    a, b, c = speeds
    assert 2 * delta / c <= (1 - 2 * delta) / b
    pair_wait_bound = 2 * delta / b + 4 * delta / c
    assert pair_wait_bound <= (1 - 2 * delta) / a
    t, trace = left, []
    for v in (a, b, c, b, c, a, b, c, b, c):
        t, row = project(F(v), F(0), delta, t)
        trace.append(row)
    assert t == F(65, 56)
    assert all(distance(v * t) >= delta for v in speeds)
    end = right
    for v in speeds:
        x = v * t
        lap = x.numerator // x.denominator
        end = min(end, (lap + 1 - delta) / v)
    certificate = lifted_certificate(speeds, (F(0),) * 3, delta, t, end)
    return {"status": "pass", "provenance": "post-protocol; no new input",
            "speeds": speeds, "phases": ["0", "0", "0"], "delta": str(delta),
            "window": [str(left), str(right)], "trace": trace,
            "scalar_projections": len(trace), "pair_wait_bound": str(pair_wait_bound),
            "slow_safe_lap_width": str((1 - 2 * delta) / a),
            "earliest": str(t), "first_component": [str(t), str(end)],
            "certificate": certificate}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = json.loads(json.dumps(calculate()))
    target = HERE / "follow_on.json"
    if args.check:
        assert json.loads(target.read_text()) == result
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "pass", "earliest": result["earliest"],
                      "first_component": result["first_component"],
                      "projections": result["scalar_projections"],
                      "provenance": result["provenance"]}))


if __name__ == "__main__":
    main()
