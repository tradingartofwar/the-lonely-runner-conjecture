#!/usr/bin/env python3
"""Compare all shared exact fields; do not evaluate additional fixtures."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_PROTOCOL_SHA256 = "6cda7c02943bf88fbb315cba9adda3c318f367c26d8c381498d27c6fc8387f8b"


def compare(left, right, path, counts):
    assert type(left) is type(right), (path, type(left).__name__, type(right).__name__)
    if isinstance(left, dict):
        assert set(left) == set(right), (path, sorted(left), sorted(right))
        for key in left:
            compare(left[key], right[key], path + "." + key, counts)
        return
    if isinstance(left, list):
        assert len(left) == len(right), (path, len(left), len(right))
        for i, (a, b) in enumerate(zip(left, right)):
            compare(a, b, path + "[" + str(i) + "]", counts)
        return
    assert left == right, (path, left, right)
    if isinstance(left, bool):
        category = "boolean_fields"
    elif isinstance(left, int):
        category = "numerical_fields"
    elif isinstance(left, str):
        try:
            Fraction(left)
            category = "numerical_fields"
        except ValueError:
            category = "text_fields"
    else:
        raise AssertionError((path, "unexpected scalar type"))
    counts[category] += 1


def run():
    paths = ["protocol.json", "primary.py", "verify.py", "results.json", "verifier_results.json", "compare.py"]
    hashes = {name: sha256((HERE / name).read_bytes()).hexdigest() for name in paths}
    assert hashes["protocol.json"] == EXPECTED_PROTOCOL_SHA256
    primary = json.loads((HERE / "results.json").read_text())
    verifier = json.loads((HERE / "verifier_results.json").read_text())
    assert primary["protocol_sha256"] == verifier["protocol_sha256"] == EXPECTED_PROTOCOL_SHA256
    assert primary["primary_sha256"] == hashes["primary.py"]

    counts = {"numerical_fields": 0, "boolean_fields": 0, "text_fields": 0}
    compare(primary["fixtures"], verifier["fixtures"], "fixtures", counts)
    compare(primary["equality_window"], verifier["equality_window"], "equality_window", counts)
    count_keys = {
        "kernel_fixtures": "fixtures", "train_integrals": "train_integrals", "totals": "totals",
        "positive_kernel_cells": "kernel_cells", "positive_kernel_breakpoints": "kernel_breakpoints",
        "zero_kernel_endpoints": "kernel_endpoints", "discrete_point_checks": "discrete_checks",
        "equality_points": "equality_points", "equality_cells": "equality_cells",
    }
    for primary_key, verifier_key in count_keys.items():
        assert primary["counts"][primary_key] == verifier["counts"][verifier_key], (primary_key, verifier_key)

    # These values are verifier-only recorded outputs, not an additional
    # primary CDF calculation or a cross-implementation CDF claim.
    cdf_records = verifier["independent_cdf"]
    assert len(cdf_records) == len(primary["fixtures"]) == 9
    cdf_summary = []
    for record, fixture in zip(cdf_records, primary["fixtures"]):
        assert record["id"] == fixture["id"]
        first, last = record["cdf_breakpoints"][0], record["cdf_breakpoints"][-1]
        assert first == {"t": "0", "value": "0"}
        assert last == {"t": fixture["H"], "value": "1"}
        cdf_summary.append({"id": record["id"], "recorded_breakpoints": len(record["cdf_breakpoints"]), "mass": last["value"]})

    result = {
        "status": "PASS: every shared fixture and equality-window scalar agrees exactly.",
        "protocol_sha256": EXPECTED_PROTOCOL_SHA256,
        "compared": counts,
        "additional_metadata_comparisons": {"mapped_count_fields": len(count_keys), "protocol_hash": 1, "primary_self_hash": 1},
        "excluded_method_metadata": ["status", "method", "implementation-specific hash fields"],
        "verifier_only_cdf": {
            "status": "Recorded independent internal normalization; no primary CDF values or cross-implementation CDF comparison.",
            "recorded_breakpoints": verifier["counts"]["cdf_breakpoints"], "fixtures": cdf_summary,
        },
        "hashes": hashes,
        "limits": "Frozen finite calibration only. Agreement is not proof of universal statements, sharpness, or novelty; no new fixture is evaluated by this comparator.",
    }
    (HERE / "comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "compared", "additional_metadata_comparisons", "protocol_sha256")}, indent=2))


if __name__ == "__main__":
    run()
