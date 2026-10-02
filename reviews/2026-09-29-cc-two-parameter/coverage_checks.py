#!/usr/bin/env python3
"""Exact finite certificate supporting the two-parameter coverage proof.

This checker does not search a parameter box.  Its only parameter enumeration
is the proved finite exceptional triangle Q + 2P < 8.  The infinite tail is
covered by the interval-width argument in coverage_review.md.
"""

from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json


ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
SEGMENTS = {
    "P1:E1-3:K1": {
        "endpoints": ((F(1, 8), F(1, 2)), (F(5, 24), F(1, 4))),
        "labels": (0, 0, 0, 0, 0, 1, 1),
        "c": 3,
        "intercept": F(7, 8),
        "H_coefficients_P_Q": ((F(-1, 2), F(1, 8)), (F(-1, 4), F(5, 24))),
        "width_coefficients_P_Q": (F(1, 4), F(1, 12)),
        "constant_contact_row": 4,
        "constant_contact_phase": F(7, 8),
    },
    "P3:E0-1:K2": {
        "endpoints": ((F(3, 8), F(3, 8)), (F(1, 2), F(1, 8))),
        "labels": (0, 0, 0, 1, 1, 1, 2),
        "c": 2,
        "intercept": F(9, 8),
        "H_coefficients_P_Q": ((F(-3, 8), F(3, 8)), (F(-1, 8), F(1, 2))),
        "width_coefficients_P_Q": (F(1, 4), F(1, 8)),
        "constant_contact_row": 3,
        "constant_contact_phase": F(1, 8),
    },
}


def ceil(value):
    return -((-value.numerator) // value.denominator)


def phases(segment, point):
    x, y = point
    return tuple(a * x + b * y - m for (a, b), m in zip(ROWS, segment["labels"]))


def test_segment(key, P, Q):
    segment = SEGMENTS[key]
    interval = tuple(Q * x - P * y for x, y in segment["endpoints"])
    lower, upper = interval
    h = ceil(lower)
    covered = h <= upper
    result = {"segment": key, "interval": interval, "first_integer": h, "covered": covered}
    if covered:
        x = (h + P * segment["intercept"]) / (Q + segment["c"] * P)
        y = segment["intercept"] - segment["c"] * x
        x0, x1 = (point[0] for point in segment["endpoints"])
        assert x0 <= x <= x1
        assert Q * x - P * y == h
        values = phases(segment, (x, y))
        assert all(F(1, 8) <= value <= F(7, 8) for value in values)
        assert min(min(value, 1 - value) for value in values) == F(1, 8)
        result.update({"point": (x, y), "phases": values})
    return result


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    endpoint_records = []
    for key, segment in SEGMENTS.items():
        for index, point in enumerate(segment["endpoints"]):
            x, y = point
            assert y == segment["intercept"] - segment["c"] * x
            values = phases(segment, point)
            assert all(F(1, 8) <= value <= F(7, 8) for value in values)
            assert values[segment["constant_contact_row"]] == segment["constant_contact_phase"]
            assert (-y, x) == segment["H_coefficients_P_Q"][index]
            endpoint_records.append({"segment": key, "endpoint_index": index, "point": point, "phases": values})
        (x0, y0), (x1, y1) = segment["endpoints"]
        assert (y0 - y1, x1 - x0) == segment["width_coefficients_P_Q"]
        assert x1 > x0 and y0 > y1
        contact_a, contact_b = ROWS[segment["constant_contact_row"]]
        assert contact_a - segment["c"] * contact_b == 0

    # P >= 4 makes Q + 2P >= 9 because Q >= 1.  The bounds below therefore
    # exhaust the exceptional triangle, rather than truncate a larger scan.
    triangle = []
    excluded_nonprimitive = []
    for P in range(1, 4):
        for Q in range(1, 8 - 2 * P):
            assert Q + 2 * P < 8
            if gcd(P, Q) != 1:
                excluded_nonprimitive.append((P, Q))
                continue
            primary = test_segment("P3:E0-1:K2", P, Q)
            fallback = None if primary["covered"] else test_segment("P1:E1-3:K1", P, Q)
            assert primary["covered"] or fallback["covered"]
            triangle.append({"P": P, "Q": Q, "distinct_speed_configuration": P != Q, "primary": primary, "fallback": fallback})

    declared_triangle = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 3), (3, 1))
    assert tuple((r["P"], r["Q"]) for r in triangle) == declared_triangle
    assert excluded_nonprimitive == [(2, 2)]
    misses = tuple((r["P"], r["Q"]) for r in triangle if not r["primary"]["covered"])
    assert misses == ((1, 2), (1, 4))

    equality_case = next(r for r in triangle if (r["P"], r["Q"]) == (1, 4))
    fallback = equality_case["fallback"]
    assert fallback["interval"] == (F(0), F(7, 12))
    assert fallback["first_integer"] == 0
    assert fallback["point"] == SEGMENTS["P1:E1-3:K1"]["endpoints"][0]
    # Opening either entire segment removes its endpoints.  The P1 image is
    # then (0,7/12), which has no integer; P3 already misses this pair.
    assert 0 < fallback["interval"][1] < 1

    report = {
        "status": "exact finite supporting checks; infinite proof remains an internally reviewed proof candidate",
        "arithmetic": "fractions.Fraction",
        "scope": "joint seven-form endpoint safety and complete primitive triangle Q+2P<8; no other parameter scan",
        "endpoint_phase_checks": 28,
        "endpoint_band_inequalities": 56,
        "endpoint_records": endpoint_records,
        "projection_coefficients": {key: {"endpoints_P_Q": s["H_coefficients_P_Q"], "width_P_Q": s["width_coefficients_P_Q"]} for key, s in SEGMENTS.items()},
        "infinite_tail_argument": "P3 width=(Q+2P)/8>=1 when Q+2P>=8; ceil(lower)<=lower+1<=upper",
        "positive_triangle_pair_count": 9,
        "excluded_nonprimitive_pairs": excluded_nonprimitive,
        "primitive_triangle_pair_count": len(triangle),
        "primitive_triangle": triangle,
        "sole_P3_misses": misses,
        "all_misses_covered_by_P1": True,
        "endpoint_removal_failure": {"pair": (1, 4), "open_P1_image": (F(0), F(7, 12)), "no_integer": True, "P3_already_misses": True},
        "cost_scope": "at most two segment tests after gcd reduction; no constant bound claimed for extended Euclid, whole algorithm, or bit cost",
        "proof_limits": ["one selected-reference witness", "not an optimum or all-maximizer claim", "not arbitrary seven speeds or all reference runners", "not a new run or retuning of the frozen discovery procedure", "no novelty or formal verification claim"],
    }
    target = Path(__file__).with_name("coverage_checks.json")
    target.write_text(json.dumps(report, default=encode, indent=2) + "\n")
    print(json.dumps({"output": str(target), "endpoint_band_inequalities": 56, "primitive_triangle_pairs": 8, "sole_P3_misses": misses, "all_misses_covered": True}))


if __name__ == "__main__":
    main()
