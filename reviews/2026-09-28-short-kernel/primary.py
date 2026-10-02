#!/usr/bin/env python3
"""Frozen finite mixed-kernel calibration by exact interval intersections."""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import ceil, floor
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "protocol.json"
EXPECTED_PROTOCOL_SHA256 = "6cda7c02943bf88fbb315cba9adda3c318f367c26d8c381498d27c6fc8387f8b"


def blocked(t, start, period):
    phase = (t - start) % period
    return 0 < phase < period / 4


def intersecting_occurrences(left, right, start, period):
    """Only train occurrences whose open interiors meet the given box."""
    first = floor((left - start - period / 4) / period) + 1
    last = ceil((right - start) / period) - 1
    for occurrence in range(first, last + 1):
        lo = start + occurrence * period
        hi = lo + period / 4
        assert lo < right and hi > left
        yield lo, hi


def train_integral(a, shifts, P, start, period):
    overlap = F(0)
    for shift in shifts:
        left, right = a + shift, a + shift + P
        for lo, hi in intersecting_occurrences(left, right, start, period):
            overlap += max(F(0), min(right, hi) - max(left, lo))
    value = overlap / (len(shifts) * P)
    assert value == F(1, 4)
    return value


def density(t, shifts, P):
    """The specified open-box representative, including at breakpoints."""
    return F(sum(shift < t < shift + P for shift in shifts), len(shifts)) / P


def kernel_fixture(tile, perturbation, sample_names):
    parameters = {key: list(map(F, tile[key])) for key in ("periods", "starts")}
    if perturbation["field"] is not None:
        parameters[perturbation["field"]][perturbation["runner"]] += F(perturbation["delta"])
    periods, starts = parameters["periods"], parameters["starts"]
    P = max(periods)
    anchor = periods.index(P)
    discrete_labels = [i for i in range(4) if i != anchor]
    shifts = [
        sum((r * periods[i] / 4 for r, i in zip(choice, discrete_labels)), F(0))
        for choice in product(range(4), repeat=3)
    ]
    assert len(shifts) == 64
    H = P + F(3, 4) * sum((periods[i] for i in discrete_labels), F(0))
    assert max(shifts) + P == H

    samples = []
    for name, a in zip(sample_names, (F(0), F(1, 7), H, H + F(1, 7))):
        integrals = [train_integral(a, shifts, P, starts[i], periods[i]) for i in range(4)]
        total = sum(integrals, F(0))
        assert total == 1
        samples.append({"name": name, "a": str(a), "train_integrals": list(map(str, integrals)), "total": str(total)})

    endpoints = sorted({point for shift in shifts for point in (shift, shift + P)})
    assert endpoints[0] == 0 and endpoints[-1] == H
    assert len(endpoints) <= 128
    cells = []
    for left, right in zip(endpoints, endpoints[1:]):
        midpoint = (left + right) / 2
        value = density(midpoint, shifts, P)
        assert value > 0
        cells.append({"left": str(left), "right": str(right), "midpoint": str(midpoint), "value": str(value)})
    breakpoints = []
    for t in endpoints[1:-1]:
        value = density(t, shifts, P)
        assert value > 0
        breakpoints.append({"t": str(t), "value": str(value)})
    support_endpoints = []
    for t in (F(0), H):
        value = density(t, shifts, P)
        assert value == 0
        support_endpoints.append({"t": str(t), "value": str(value)})

    discrete_checks = []
    for i in discrete_labels:
        for kind, t, expected in (("boundary", starts[i], F(0)), ("interior", starts[i] + periods[i] / 8, F(1, 4))):
            value = F(sum(blocked(t + r * periods[i] / 4, starts[i], periods[i]) for r in range(4)), 4)
            assert value == expected
            discrete_checks.append({"label": i, "t": str(t), "kind": kind, "value": str(value)})

    return {
        "id": tile["id"] + "__" + perturbation["id"],
        "periods": list(map(str, periods)), "starts": list(map(str, starts)),
        "anchor_index": anchor, "P": str(P), "H": str(H), "atom_count": len(shifts),
        "samples": samples, "kernel_cells": cells, "kernel_breakpoints": breakpoints,
        "kernel_endpoints": support_endpoints, "discrete_checks": discrete_checks,
    }


def equality_window(case):
    periods, starts = (list(map(F, case[key])) for key in ("periods", "starts"))
    left, right = map(F, case["window"])
    P = max(periods)
    anchor = periods.index(P)
    H = P + F(3, 4) * sum((period for i, period in enumerate(periods) if i != anchor), F(0))
    assert H == right - left == F(case["expected_H"])

    events = {left, right}
    for start, period in zip(starts, periods):
        for lo, hi in intersecting_occurrences(left, right, start, period):
            events.update(t for t in (lo, hi) if left < t < right)
    events = sorted(events)
    assert len(events) == 14
    points = []
    for t in events:
        multiplicity = sum(blocked(t, start, period) for start, period in zip(starts, periods))
        assert multiplicity == 0
        points.append({"t": str(t), "multiplicity": multiplicity, "safe": multiplicity == 0})
    cells = []
    safe_duration = F(0)
    for lo, hi in zip(events, events[1:]):
        midpoint = (lo + hi) / 2
        multiplicity = sum(blocked(midpoint, start, period) for start, period in zip(starts, periods))
        assert multiplicity == 1
        if multiplicity == 0:
            safe_duration += hi - lo
        cells.append({"left": str(lo), "right": str(hi), "midpoint": str(midpoint), "multiplicity": multiplicity})
    safe_points = [point["t"] for point in points if point["safe"]]
    assert safe_points == case["expected_safe_points"]
    assert len(cells) == 13 and safe_duration == 0
    return {
        "id": case["id"], "periods": list(map(str, periods)), "starts": list(map(str, starts)),
        "window": [str(left), str(right)], "H": str(H), "width": str(right - left),
        "points": points, "cells": cells, "safe_points": safe_points, "safe_duration": str(safe_duration),
    }


def run():
    protocol_bytes = PROTOCOL.read_bytes()
    protocol_hash = sha256(protocol_bytes).hexdigest()
    assert protocol_hash == EXPECTED_PROTOCOL_SHA256
    protocol = json.loads(protocol_bytes)
    assert len(protocol["tiles"]) == len(protocol["perturbations"]) == 3
    assert protocol["samples"] == ["0", "1/7", "H", "H+1/7"]
    fixtures = [kernel_fixture(tile, perturbation, protocol["samples"])
                for tile in protocol["tiles"] for perturbation in protocol["perturbations"]]
    equality = equality_window(protocol["equality_window"])
    counts = {
        "kernel_fixtures": len(fixtures), "translation_samples": sum(len(f["samples"]) for f in fixtures),
        "train_integrals": sum(len(s["train_integrals"]) for f in fixtures for s in f["samples"]),
        "totals": sum(len(f["samples"]) for f in fixtures),
        "positive_kernel_cells": sum(len(f["kernel_cells"]) for f in fixtures),
        "positive_kernel_breakpoints": sum(len(f["kernel_breakpoints"]) for f in fixtures),
        "zero_kernel_endpoints": sum(len(f["kernel_endpoints"]) for f in fixtures),
        "discrete_point_checks": sum(len(f["discrete_checks"]) for f in fixtures),
        "equality_windows": 1, "equality_points": len(equality["points"]), "equality_cells": len(equality["cells"]),
    }
    assert counts["kernel_fixtures"] == 9 and counts["translation_samples"] == 36
    assert counts["train_integrals"] == 144 and counts["totals"] == 36
    assert counts["discrete_point_checks"] == 54 and counts["zero_kernel_endpoints"] == 18
    result = {
        "protocol_sha256": protocol_hash, "primary_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "PASS: exact finite mixed-kernel and endpoint calibration only; general statements remain proof candidates.",
        "method": "64 translated boxes with multiplicity; exact blocked-interval intersection lengths; direct open-box density counts.",
        "counts": counts, "fixtures": fixtures, "equality_window": equality,
    }
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "counts", "protocol_sha256", "primary_sha256")}, indent=2))


if __name__ == "__main__":
    run()
