#!/usr/bin/env python3
"""Compare only the frozen nine-fixture exact convolution results."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_PROTOCOL_SHA256 = "63d509f00dd73cfc54094030ed942d0e929215213a5e20604305dc4e99192d06"


def digest(name):
    return sha256((HERE / name).read_bytes()).hexdigest()


def main():
    primary = json.loads((HERE / "results.json").read_text())
    verifier = json.loads((HERE / "challenge_verification.json").read_text())
    assert digest("protocol.json") == EXPECTED_PROTOCOL_SHA256
    assert primary["protocol_sha256"] == EXPECTED_PROTOCOL_SHA256
    assert verifier["protocol_sha256"] == EXPECTED_PROTOCOL_SHA256
    assert primary["primary_sha256"] == digest("primary.py")

    numeric_counts = Counter()
    metadata_counts = Counter()

    def number(category, left, right):
        assert Fraction(left) == Fraction(right), (category, left, right)
        numeric_counts[category] += 1

    def metadata(category, left, right):
        assert left == right, (category, left, right)
        metadata_counts[category] += 1

    metadata("protocol_sha256", primary["protocol_sha256"], verifier["protocol_sha256"])
    assert len(primary["fixtures"]) == len(verifier["fixtures"]) == 9
    verified = {fixture["id"].replace(":", "/"): fixture for fixture in verifier["fixtures"]}
    assert len(verified) == 9
    for left in primary["fixtures"]:
        right = verified[left["id"]]
        metadata("fixture_ids", left["id"], right["id"].replace(":", "/"))
        for field in ("periods", "starts"):
            assert len(left[field]) == len(right[field]) == 4
            for a, b in zip(left[field], right[field]):
                number(field, a, b)
        number("support_lengths", left["support"], right["S"])
        assert len(left["samples"]) == len(right["samples"]) == 4
        for a, b in zip(left["samples"], right["samples"]):
            number("convolution_arguments", a["x"], b["x"])
            assert len(a["trains"]) == len(b["trains"]) == 4
            for c, d in zip(a["trains"], b["trains"]):
                number("train_integrals", c["value"], d)
            number("convolution_totals", a["total"], b["total"])
        left_kernel = left["kernel_interior"] + left["kernel_endpoints"]
        right_kernel = right["kernel_samples"]
        assert len(left_kernel) == len(right_kernel) == 9
        for a, b in zip(left_kernel, right_kernel):
            number("kernel_arguments", a["t"], b["argument"])
            number("kernel_values", a["value"], b["value"])

    expected_counts = {"periods": 36, "starts": 36, "support_lengths": 9,
                       "convolution_arguments": 36, "train_integrals": 144,
                       "convolution_totals": 36, "kernel_arguments": 81,
                       "kernel_values": 81}
    assert dict(numeric_counts) == expected_counts
    assert sum(numeric_counts.values()) == 459
    assert dict(metadata_counts) == {"protocol_sha256": 1, "fixture_ids": 9}
    result = {
        "status": "PASS: all declared exact numerical fields agree between independently structured implementations.",
        "scope": "Nine inherited fixtures only. Identifier separator normalized from colon to slash. No new numerical case or scan.",
        "numeric_comparisons": dict(numeric_counts),
        "numeric_comparisons_total": sum(numeric_counts.values()),
        "metadata_comparisons": dict(metadata_counts),
        "metadata_comparisons_total": sum(metadata_counts.values()),
        "integrity_checks": "Current protocol matches frozen hash and both result references; current primary matches its hash embedded in results.json.",
        "sha256": {name: digest(name) for name in ("protocol.json", "primary.py", "challenge_verify.py", "compare.py", "results.json", "challenge_verification.json")},
        "limits": "Agreement calibrates only these formulas and fixtures. It is not external mathematical review or proof of the global 39-move candidate.",
    }
    (HERE / "comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
