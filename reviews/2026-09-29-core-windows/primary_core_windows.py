#!/usr/bin/env python3
"""Frozen 31-core exact calculation; see PRIMARY_PROTOCOL.md.

No project imports. Do not execute before coordinator protocol approval.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DOMAIN = (2, 3, *range(6, 35))
THRESHOLD = Q(1, 8)


def rat(value):
    return str(value)


def serialize_interval(interval):
    return [rat(interval[0]), rat(interval[1])]


def canonicalize(intervals):
    """Union closed intervals, retaining zero-width pieces and touching joins."""
    result = []
    for left, right in sorted(intervals):
        assert left <= right
        if result and left <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], right))
        else:
            result.append((left, right))
    return result


def bands(speed):
    return [(Q(8 * j + 1, 8 * speed), Q(8 * j + 7, 8 * speed))
            for j in range(speed)]


def intersect(left_union, right_union):
    result = []
    for left_a, right_a in left_union:
        for left_b, right_b in right_union:
            left, right = max(left_a, left_b), min(right_a, right_b)
            if left <= right:
                result.append((left, right))
    return canonicalize(result)


def distance(speed, time):
    raw = speed * time
    phase = raw - raw.numerator // raw.denominator
    return min(phase, 1 - phase)


def point_certificate(core, time):
    distances = {str(v): distance(v, time) for v in core}
    assert all(value >= THRESHOLD for value in distances.values())
    return {"time": rat(time),
            "distances": {key: rat(value) for key, value in distances.items()}}


def core_record(a):
    core = (1, 4, 5, a)
    components = [(Q(0), Q(1))]
    for speed in core:
        components = intersect(components, bands(speed))

    assert components == sorted(components)
    assert all(components[i][1] < components[i + 1][0]
               for i in range(len(components) - 1))
    assert components == sorted((1 - right, 1 - left)
                                for left, right in components)
    for component in components:
        for speed in core:
            assert any(left <= component[0] <= component[1] <= right
                       for left, right in bands(speed))

    positive = [(left, right) for left, right in components if left < right]
    isolated = [left for left, right in components if left == right]
    assert positive
    width = max(right - left for left, right in positive)
    ties = [(left, right) for left, right in positive if right - left == width]
    chosen = min(ties, key=lambda pair: pair[0])
    assert chosen == ties[0]
    bound = Q(7, 4) / width
    threshold_b = -(-bound.numerator // bound.denominator)
    assert Q(7, 4 * threshold_b) <= width
    assert threshold_b == 1 or Q(7, 4 * (threshold_b - 1)) > width

    return {
        "a": a,
        "core_in_intersection_order": list(core),
        "positive_components": [serialize_interval(x) for x in positive],
        "isolated_points": [rat(x) for x in isolated],
        "positive_component_count": len(positive),
        "isolated_point_count": len(isolated),
        "safe_measure": rat(sum((right - left for left, right in positive), Q(0))),
        "selected_earliest_widest_component": serialize_interval(chosen),
        "width": rat(width),
        "widest_ties": [serialize_interval(x) for x in ties],
        "widest_tie_count": len(ties),
        "sufficient_second_residual_threshold": threshold_b,
        "selected_component_certificates": {
            "left": point_certificate(core, chosen[0]),
            "midpoint": point_certificate(core, sum(chosen, Q(0)) / 2),
            "right": point_certificate(core, chosen[1]),
        },
        "isolated_point_certificates": [point_certificate(core, t) for t in isolated],
    }


def main():
    records = [core_record(a) for a in DOMAIN]
    assert len(records) == 31
    result = {
        "status": "OBSERVED exact finite arithmetic; theorem implication remains HYPOTHESIS / proof candidate",
        "base_commit": "db2867ed65c4df3668f5275878f21ba400faff2b",
        "date": "2026-09-29",
        "domain": list(DOMAIN),
        "time_domain": ["0", "1"],
        "threshold": "1/8",
        "safety": "distance_to_integer(v*t) >= 1/8; equality included",
        "arithmetic": "Python fractions.Fraction",
        "algorithm": "closed lap-safe band union intersections in order 1,4,5,a; touching pieces merged",
        "tie_policy": "smallest left endpoint among positive components of maximum width",
        "threshold_formula": "ceil(7/(4*w_a)); no integer-separation refinement",
        "command": "python reviews/2026-09-29-core-windows/primary_core_windows.py",
        "source_sha256": {
            name: sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("PRIMARY_PROTOCOL.md", "primary_core_windows.py")
        },
        "records": records,
    }
    output = HERE / "primary_core_windows.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    lines = [
        "# Exact primary core-window table",
        "",
        "**OBSERVED** exact arithmetic on the frozen 31-value domain. The all-fast-residual",
        "implication is a **HYPOTHESIS / proof candidate**, conditional on the three-train",
        "span argument. Equality is safe. The selected window is the earliest widest",
        "positive closed component; all ties and isolated points are retained in JSON.",
        "",
        "| a | Selected closed window | Width w_a | Sufficient b >= B_a | Widest ties | Isolated points |",
        "| ---: | --- | --- | ---: | ---: | ---: |",
    ]
    for row in records:
        left, right = row["selected_earliest_widest_component"]
        lines.append(f"| {row['a']} | [{left}, {right}] | {row['width']} | "
                     f"{row['sufficient_second_residual_threshold']} | "
                     f"{row['widest_tie_count']} | {row['isolated_point_count']} |")
    lines += [
        "",
        "For a < b < c < d, the bound is obtained from",
        "`T3 = 1/(4b)+1/(2c)+1/d <= 7/(4b) <= w_a`.",
        "This table does not enumerate b,c,d or establish the remaining cases below B_a.",
        "No all-reference, full-conjecture, or novelty claim is made. This calculation",
        "was materially AI-assisted and awaits the stated independent comparison.",
        "",
        "Reproduce from the repository root with:",
        "`python reviews/2026-09-29-core-windows/primary_core_windows.py`.",
        "",
    ]
    (HERE / "PRIMARY_TABLE.md").write_text("\n".join(lines))
    print(json.dumps({
        "records": len(records),
        "minimum_width": str(min(Q(row["width"]) for row in records)),
        "maximum_sufficient_b": max(row["sufficient_second_residual_threshold"]
                                    for row in records),
        "isolated_points": sum(row["isolated_point_count"] for row in records),
        "json": str(output),
    }, indent=2))


if __name__ == "__main__":
    main()
