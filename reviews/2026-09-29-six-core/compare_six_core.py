#!/usr/bin/env python3
"""Compare frozen outputs only after independent reconstruction completed."""

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
numeric_leaves = 0
null_leaves = 0


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def compare(expected, actual, path):
    global numeric_leaves, null_leaves
    if isinstance(expected, dict):
        assert isinstance(actual, dict), path
        assert set(expected) == set(actual), (path, set(expected), set(actual))
        for key, value in expected.items():
            compare(value, actual[key], path + "." + key)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(expected) == len(actual), path
        for i, (a, b) in enumerate(zip(expected, actual)):
            compare(a, b, path + "[" + str(i) + "]")
    elif expected is None:
        assert actual is None, path
        null_leaves += 1
    else:
        assert F(expected) == F(actual), (path, expected, actual)
        numeric_leaves += 1


def distance(t, v):
    q = F(t) * v
    r = q - q.numerator // q.denominator
    return str(min(r, 1 - r))


def canonical(row):
    isolated = [l for l, r in row["components"] if l == r]
    positive = [[l, r] for l, r in row["components"] if F(r) > F(l)]
    selected_certs = None
    if row["selected_distances"] is not None:
        selected_certs = {
            cert["point"]: {"time": cert["time"], "distances": cert["distances"]}
            for cert in row["selected_distances"]
        }
    return {
        "triple": row["triple"],
        "core_in_intersection_order": row["speeds"],
        "components": row["components"],
        "positive_components": positive,
        "isolated_points": isolated,
        "positive_component_count": row["positive_component_count"],
        "isolated_point_count": row["isolated_point_count"],
        "safe_measure": row["safe_measure"],
        "selected_earliest_widest_component": row["earliest_widest"],
        "width": row["widest_width"] if row["earliest_widest"] else None,
        "widest_ties": row["widest_ties"],
        "widest_tie_count": len(row["widest_ties"]),
        "sufficient_last_residual_threshold": row["last_runner_cutoff"],
        "selected_component_certificates": selected_certs,
        "isolated_point_certificates": [
            {"time": t, "distances": {str(v): distance(t, v) for v in row["speeds"]}}
            for t in isolated
        ],
    }


def main():
    independent_path = HERE / "independent_six_core.json"
    primary_path = HERE / "primary_six_core.json"
    assert sha(independent_path) == "6cbd1cf544659a52eea00cf27fc0879eb6a48658e1544f81c0c4ade2479be736"
    assert sha(primary_path) == "f4718e3c3257efcd594111cbd0a363775e4eaa61ae62bea8ecead4b4678ffdc0"
    independent = json.loads(independent_path.read_text())
    primary = json.loads(primary_path.read_text())
    assert independent["protocol_sha256"] == sha(HERE / "PROTOCOL.json")
    assert independent["source_sha256"] == sha(HERE / "independent_six_core.py")
    for name, digest in primary["source_sha256"].items():
        assert sha(HERE / name) == digest
    compare(independent["triples"], primary["domain"], "domain")
    compare([canonical(r) for r in independent["rows"]], primary["records"], "records")
    result = {
        "status": "PASS",
        "case_count": len(independent["rows"]),
        "numeric_leaf_comparisons": numeric_leaves,
        "null_leaf_comparisons": null_leaves,
        "summary": independent["summary"],
        "comparison_scope": "Entire domain and every primary mathematical record field; isolated-point certificates reconstructed from the independently identified points.",
        "independence": "Independent endpoint/midcell output frozen before primary output or code was read.",
        "source_sha256": {name: sha(HERE / name) for name in (
            "PROTOCOL.json", "primary_six_core.py", "primary_six_core.json",
            "independent_six_core.py", "independent_six_core.json", "compare_six_core.py")},
    }
    output = HERE / "comparison.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
