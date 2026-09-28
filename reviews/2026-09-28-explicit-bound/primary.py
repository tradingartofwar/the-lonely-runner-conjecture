#!/usr/bin/env python3
"""Frozen nine-fixture exact convolution calibration; no parameter search."""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import ceil, floor, prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "protocol.json"
EXPECTED_PROTOCOL_SHA256 = "63d509f00dd73cfc54094030ed942d0e929215213a5e20604305dc4e99192d06"


def subset_terms(periods):
    for size in range(5):
        for indexes in combinations(range(4), size):
            yield (-1) ** size, sum((periods[i] for i in indexes), F(0))


def kernel_value(t, periods, degree):
    """degree=3 gives density K; degree=4 gives its CDF."""
    factorial = {3: 6, 4: 24}[degree]
    value = sum(
        (sign * max(t - shift, F(0)) ** degree for sign, shift in subset_terms(periods)),
        F(0),
    )
    return value / (factorial * prod(periods))


def train_integral(x, periods, start, period):
    support = sum(periods)
    first = floor((x - support - start - period / 4) / period) + 1
    last = ceil((x - start) / period) - 1
    total = F(0)
    for occurrence in range(first, last + 1):
        left = start + occurrence * period
        right = left + period / 4
        assert left < x and right > x - support
        contribution = kernel_value(x - left, periods, 4) - kernel_value(x - right, periods, 4)
        assert contribution >= 0
        total += contribution
    assert total == F(1, 4)
    return {
        "first_occurrence": first,
        "last_occurrence": last,
        "occurrences": last - first + 1,
        "value": str(total),
    }


def run():
    protocol_bytes = PROTOCOL.read_bytes()
    protocol_hash = sha256(protocol_bytes).hexdigest()
    assert protocol_hash == EXPECTED_PROTOCOL_SHA256
    protocol = json.loads(protocol_bytes)
    assert len(protocol["tiles"]) == 3 and len(protocol["perturbations"]) == 3
    fixtures = []
    for tile in protocol["tiles"]:
        for perturbation in protocol["perturbations"]:
            parameters = {key: list(map(F, tile[key])) for key in ("periods", "starts")}
            if perturbation["field"] is not None:
                parameters[perturbation["field"]][perturbation["runner"]] += F(perturbation["delta"])
            periods, starts = parameters["periods"], parameters["starts"]
            support = sum(periods)
            samples = []
            for sample_name, x in zip(protocol["samples"], (F(0), F(1, 7), support, support + F(1, 7))):
                train_results = [train_integral(x, periods, start, period) for start, period in zip(starts, periods)]
                total = sum((F(result["value"]) for result in train_results), F(0))
                assert total == 1
                samples.append({"name": sample_name, "x": str(x), "trains": train_results, "total": str(total)})
            interior = []
            for j in protocol["kernel_samples"]["interior_j"]:
                t = support * j / 8
                value = kernel_value(t, periods, 3)
                assert value > 0
                interior.append({"j": j, "t": str(t), "value": str(value)})
            endpoints = []
            for t in (F(0), support):
                value = kernel_value(t, periods, 3)
                assert value == 0
                endpoints.append({"t": str(t), "value": str(value)})
            fixtures.append({
                "id": tile["id"] + "/" + perturbation["id"],
                "periods": list(map(str, periods)),
                "starts": list(map(str, starts)),
                "support": str(support),
                "samples": samples,
                "kernel_interior": interior,
                "kernel_endpoints": endpoints,
            })
    result = {
        "protocol_sha256": protocol_hash,
        "primary_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "PASS: exact bounded calibration only; general theorem requires mathematical review.",
        "counts": {"fixtures": 9, "x_samples": 36, "train_integrals": 144, "totals": 36, "positive_kernel_samples": 63, "zero_kernel_endpoints": 18},
        "fixtures": fixtures,
    }
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"], "protocol_sha256": protocol_hash, "primary_sha256": result["primary_sha256"]}, indent=2))


if __name__ == "__main__":
    run()
