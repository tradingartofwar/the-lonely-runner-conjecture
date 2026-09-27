#!/usr/bin/env python3
"""Exact, standalone arithmetic review checks; no project imports.

Run from any directory. Writes only the adjacent arithmetic_check.json.
Finite checks supplement, rather than establish, the general arguments.
"""

from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json


def primitive(z, delta):
    shifted = z + delta
    integer = shifted.numerator // shifted.denominator
    return 2 * delta * integer + min(shifted - integer, 2 * delta)


def correction(z, delta):
    return primitive(z, delta) - 2 * delta * z


def duration(v, a, b, delta):
    return (primitive(v * b, delta) - primitive(v * a, delta)) / v


def blocked(v, t, delta):
    phase = (v * t) % 1
    return min(phase, 1 - phase) < delta


def event_points(speeds, delta, a=F(0), b=F(1)):
    points = {a, b}
    for v in speeds:
        for lap in range(-1, v + 2):
            for sign in (-1, 1):
                t = (lap + sign * delta) / v
                if a < t < b:
                    points.add(t)
    return sorted(points)


def state_masses(speeds, delta, a=F(0), b=F(1)):
    points = event_points(speeds, delta, a, b)
    masses = [F(0) for _ in range(1 << len(speeds))]
    for left, right in zip(points, points[1:]):
        middle = (left + right) / 2
        mask = sum(1 << j for j, v in enumerate(speeds)
                   if blocked(v, middle, delta))
        masses[mask] += right - left
    assert sum(masses) == b - a
    return masses


def moments(masses):
    return [sum((mass for mask, mass in enumerate(masses)
                 if mask & subset == subset), F(0))
            for subset in range(len(masses))]


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def main():
    delta = F(1, 8)
    fixed = (1, 3, 4, 5, 10, 28)
    fixed_mass = state_masses(fixed, delta)
    assert fixed_mass[0] == F(15, 112)
    fixed_points = event_points(fixed, delta)
    assert reduce(lcm, (t.denominator for t in fixed_points)) == 3360
    full = []
    for h in (1, 2):
        y = 1680 * h
        actual = state_masses(fixed + (y,), delta)
        # Independent event partitions versus the predicted product law.
        expected = [(1 - 2 * delta) * m for m in fixed_mass]
        expected += [2 * delta * m for m in fixed_mass]
        assert actual == expected
        assert actual[0] == F(45, 448)
        assert all(gcd(v, y) == v for v in fixed)
        full.append({"h": h, "y": y, "states": actual,
                     "moments": moments(actual), "U": actual[0]})
    assert full[0]["moments"] == full[1]["moments"]

    grid_checks = []
    for threshold in (F(1, 8), F(1, 5), F(2, 7), F(3, 8)):
        assert correction(F(0), threshold) == threshold
        assert correction(F(1, 2), threshold) == threshold
        neutral = []
        for y in range(1, 25):
            values = [duration(y, F(j, 12), F(j + 1, 12), threshold)
                      for j in range(12)]
            exact = all(x == 2 * threshold / 12 for x in values)
            assert exact == (y % 6 == 0)
            if exact:
                neutral.append(y)
        grid_checks.append({"delta": threshold, "P": 12,
                            "tested_y": [1, 24], "neutral_y": neutral})

    # The target-sensitive added window, including large parameters where
    # the primitive replaces prohibitively large event enumerations.
    a, b = F(9, 32), F(9, 32) + F(1, 6720)
    probes = []
    for h in list(range(1, 25)) + [1001, 1002, 1000001, 1000002]:
        y = 1680 * h
        value = duration(y, a, b, delta)
        expected = F(1, 26880)
        if h % 2:
            expected += F(-1 if h % 4 == 1 else 1, 26880 * h)
        assert value == expected
        assert (value == F(1, 26880)) == (h % 2 == 0)
        assert blocked(y, a, delta) == (h % 2 == 0)
        if h <= 4:
            direct = state_masses((y,), delta, a, b)[1]
            assert direct == value
        probes.append({"h": h, "D_K": value, "left_blocked": h % 2 == 0})

    # An exact change of temporal order is visible in a weighted duration.
    # On the first half-grid cell, y=1680 has its blocked part at the left;
    # y=3360 has equal pieces at both ends.
    weighted = {}
    for y in (1680, 3360):
        points = event_points((y,), delta, F(0), F(1, 3360))
        value = sum(((right * right - left * left) / 2
                     for left, right in zip(points, points[1:])
                     if blocked(y, (left + right) / 2, delta)), F(0))
        weighted[y] = value
    assert weighted[1680] == F(1, 32 * 3360**2)
    assert weighted[3360] == F(1, 8 * 3360**2)

    report = {
        "baseline": "e94a87f650264826569cae63412c43a5175f5ae4",
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "method": "Exact Fraction threshold-event partition, plus independent primitive formulas",
        "fixed_speeds": fixed,
        "threshold": delta,
        "fixed_full_period_state_masses": fixed_mass,
        "full_period_controls": full,
        "rational_grid_controls": grid_checks,
        "added_window": [a, b],
        "added_window_controls": probes,
        "first_cell_weighted_duration": weighted,
        "finite_scope": "Full event partition h=1,2; probe event partition h=1..4; grid P=12,y=1..24 at four thresholds; larger probes use primitive only",
    }
    destination = Path(__file__).with_name("arithmetic_check.json")
    destination.write_text(json.dumps(serial(report), indent=2) + "\n")
    print("PASS: full-period product law, all 128 moments, grid neutrality, parity probe, weighted separation")
    print(destination)


if __name__ == "__main__":
    main()
