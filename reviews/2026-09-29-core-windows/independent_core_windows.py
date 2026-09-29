#!/usr/bin/env python3
"""Independent, exact threshold-event verification of the frozen 31 cores.

No project or primary implementation imports. Finite evaluation is enabled only
when the caller supplies the SHA-256 of the coordinator-approved protocol.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

BASE_COMMIT = "db2867ed65c4df3668f5275878f21ba400faff2b"
A_DOMAIN = (2, 3, *range(6, 35))
THRESHOLD = F(1, 8)


def phase_safe(t: F, v: int) -> bool:
    """Evaluate the modular predicate directly; no interval formula."""
    phase = v * t
    remainder = phase.numerator % phase.denominator
    return 8 * remainder >= phase.denominator and 8 * remainder <= 7 * phase.denominator


def evaluate_core(a: int) -> dict:
    speeds = (1, 4, 5, a)
    events = {F(0), F(1)}
    for v in speeds:
        for lap in range(v):
            events.add(F(8 * lap + 1, 8 * v))
            events.add(F(8 * lap + 7, 8 * v))
    points = sorted(events)
    endpoint_safe = [all(phase_safe(t, v) for v in speeds) for t in points]
    cell_safe = [
        all(phase_safe((lo + hi) / 2, v) for v in speeds)
        for lo, hi in zip(points, points[1:])
    ]
    # No threshold lies in an open cell, so its midpoint gives its entire state.
    # Weak safety is closed; a safe cell must have both endpoints safe.
    for i, flag in enumerate(cell_safe):
        assert not flag or (endpoint_safe[i] and endpoint_safe[i + 1])

    # Walk the alternating endpoint/open-cell topology, including point-only runs.
    components = []
    start = None
    for i, t in enumerate(points):
        if endpoint_safe[i] and start is None:
            start = t
        if start is not None and (i == len(cell_safe) or not cell_safe[i]):
            components.append((start, t))
            start = None
    assert start is None
    positive = [(lo, hi) for lo, hi in components if lo < hi]
    isolated = [lo for lo, hi in components if lo == hi]
    assert positive
    widest_width = max(hi - lo for lo, hi in positive)
    widest = [(lo, hi) for lo, hi in positive if hi - lo == widest_width]
    selected = min(widest)
    cutoff_fraction = F(7, 4) / widest_width
    cutoff = -(-cutoff_fraction.numerator // cutoff_fraction.denominator)
    assert F(7, 4 * cutoff) <= widest_width
    assert cutoff == 1 or F(7, 4 * (cutoff - 1)) > widest_width

    encode_pair = lambda pair: [str(pair[0]), str(pair[1])]
    def distances(t: F) -> list[str]:
        result = []
        for v in speeds:
            phase = v * t
            p = F(phase.numerator % phase.denominator, phase.denominator)
            result.append(str(min(p, 1 - p)))
        return result

    return {
        "a": a,
        "core": list(speeds),
        "components": [encode_pair(pair) for pair in components],
        "positive_components": [encode_pair(pair) for pair in positive],
        "isolated_points": [str(point) for point in isolated],
        "safe_measure": str(sum((hi - lo for lo, hi in positive), F(0))),
        "widest_components": [encode_pair(pair) for pair in widest],
        "selected_window": encode_pair(selected),
        "width": str(widest_width),
        "b_cutoff": cutoff,
        "positive_component_count": len(positive),
        "isolated_point_count": len(isolated),
        "widest_tie_count": len(widest),
        "selected_distances": {
            "left": distances(selected[0]),
            "midpoint": distances(sum(selected) / 2),
            "right": distances(selected[1]),
        },
        "event_count": len(points),
        "cell_count": len(cell_safe),
        "safe_event_count": sum(endpoint_safe),
        "safe_cell_count": sum(cell_safe),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol-hash", required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    protocol = here / "PRIMARY_PROTOCOL.md"
    actual_hash = hashlib.sha256(protocol.read_bytes()).hexdigest()
    if actual_hash != args.protocol_hash:
        raise SystemExit(f"Protocol hash mismatch: {actual_hash}")
    rows = [evaluate_core(a) for a in A_DOMAIN]
    data = {
        "schema": "independent-core-window-events-v1",
        "status": "OBSERVED exact arithmetic on the frozen 31 core values",
        "base_commit": BASE_COMMIT,
        "protocol_sha256": actual_hash,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "method": "threshold-event partition; direct modular endpoint and midpoint predicates; topological run reconstruction",
        "threshold": "1/8",
        "domain": ["0", "1"],
        "a_values": list(A_DOMAIN),
        "cutoff_rule": "ceil(7/(4*widest_positive_width))",
        "rows": rows,
        "totals": {
            "cores": len(rows),
            "components": sum(len(row["components"]) for row in rows),
            "positive_components": sum(len(row["positive_components"]) for row in rows),
            "isolated_points": sum(len(row["isolated_points"]) for row in rows),
            "event_checks": sum(row["event_count"] for row in rows),
            "cell_checks": sum(row["cell_count"] for row in rows),
        },
    }
    output = here / "independent_core_windows.json"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "totals": data["totals"]}, indent=2))


if __name__ == "__main__":
    main()
