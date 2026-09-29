#!/usr/bin/env python3
"""Compare frozen independent results with primary output and 12 hand Q rows."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEPENDENT_SHA = "434fcbb15424c6c2d4387a1281eef2a808dcbd34a281ac73d85c7372c29a587e"
PRIMARY_SHA = "4bbf907e6dc9b85d868a4d739e7f75a88969dead514ae2aca4a9879ca7fa997a"


def read_pinned(name, sha):
    raw = (HERE / name).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == sha, name
    return json.loads(raw)


def certificate(time, speeds):
    t = F(time)
    distances = {}
    for v in speeds:
        p = v * t
        remainder = F(p.numerator % p.denominator, p.denominator)
        distances[str(v)] = str(min(remainder, 1 - remainder))
    return {"time": str(t), "distances": distances}


def leaf_count(value):
    if isinstance(value, dict):
        return sum(leaf_count(v) for v in value.values())
    if isinstance(value, list):
        return sum(leaf_count(v) for v in value)
    return 1


independent = read_pinned("independent_core_windows.json", INDEPENDENT_SHA)
primary = read_pinned("primary_core_windows.json", PRIMARY_SHA)
assert independent["a_values"] == primary["domain"]
assert independent["domain"] == primary["time_domain"]
assert independent["threshold"] == primary["threshold"]
assert independent["base_commit"] == primary["base_commit"]
assert len(independent["rows"]) == len(primary["records"]) == 31
comparisons = []
for mine, theirs in zip(independent["rows"], primary["records"]):
    left, right = map(F, mine["selected_window"])
    points = {"left": left, "midpoint": (left + right) / 2, "right": right}
    normalized = {
        "a": mine["a"],
        "core_in_intersection_order": mine["core"],
        "positive_components": mine["positive_components"],
        "isolated_points": mine["isolated_points"],
        "positive_component_count": mine["positive_component_count"],
        "isolated_point_count": mine["isolated_point_count"],
        "safe_measure": mine["safe_measure"],
        "selected_earliest_widest_component": mine["selected_window"],
        "width": mine["width"],
        "widest_ties": mine["widest_components"],
        "widest_tie_count": mine["widest_tie_count"],
        "sufficient_second_residual_threshold": mine["b_cutoff"],
        "selected_component_certificates": {
            name: {
                "time": str(t),
                "distances": {
                    str(v): distance
                    for v, distance in zip(mine["core"], mine["selected_distances"][name])
                },
            }
            for name, t in points.items()
        },
        "isolated_point_certificates": [certificate(t, mine["core"]) for t in mine["isolated_points"]],
    }
    assert normalized == theirs, f"Primary disagreement at a={mine['a']}"
    comparisons.append({"a": mine["a"], "numerical_fields": leaf_count(normalized), "match": True})

expected_q = {
    2: "1/16", 3: "1/6", 6: "17/120", 7: "89/560", 8: "1/16", 9: "1/9",
    10: "1/20", 11: "93/880", 12: "1/12", 13: "23/208", 14: "69/560", 15: "7/80",
}
by_a = {row["a"]: row for row in independent["rows"]}
q_comparisons = []
for a, expected in expected_q.items():
    actual = F(3, 8) - F(by_a[a]["safe_measure"])
    assert actual == F(expected), f"Hand Q disagreement at v={a}"
    q_comparisons.append({"v": a, "Q_from_independent_safe_measure": str(actual), "Q_in_scope_md": expected, "match": True})

result = {
    "scope": "Only the frozen31 a values;12 Q rows are a subset, with no extra speed input",
    "independent_json_sha256": INDEPENDENT_SHA,
    "primary_json_sha256": PRIMARY_SHA,
    "comparison_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "primary_comparisons": comparisons,
    "primary_numerical_fields_matched": sum(row["numerical_fields"] for row in comparisons),
    "q_comparisons": q_comparisons,
    "q_values_matched": len(q_comparisons),
    "disagreements": 0,
}
(HERE / "independent_comparison.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: result[key] for key in ("primary_numerical_fields_matched", "q_values_matched", "disagreements")}, indent=2))
