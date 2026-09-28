#!/usr/bin/env python3
"""Independent exact finite verifier for the frozen mixed-kernel protocol.

No primary imports. Train averages use a periodic occupancy primitive, and
kernel density/CDF uses a sweep of signed endpoint events. Only protocol.json
is read. General mathematical conclusions are not inferred from fixtures.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = "6cda7c02943bf88fbb315cba9adda3c318f367c26d8c381498d27c6fc8387f8b"


def primitive(t, period, start):
    """Continuous primitive of an open quarter-duty periodic train."""
    quotient = (t - start) // period
    remainder = t - start - quotient * period
    assert 0 <= remainder < period
    return quotient * period / 4 + min(remainder, period / 4)


def occupied(t, period, start):
    """Exact threshold predicate, including safe boundaries."""
    remainder = (t - start) % period
    return int(0 < remainder < period / 4)


def make_kernel(periods):
    anchor = periods.index(max(periods))
    width = periods[anchor]
    others = [i for i in range(4) if i != anchor]
    translations = [
        sum((r * periods[i] / 4 for i, r in zip(others, digits)), Q(0))
        for digits in product(range(4), repeat=3)
    ]
    support = width + Q(3, 4) * sum((periods[i] for i in others), Q(0))
    assert len(translations) == 64
    assert min(translations) == 0
    assert max(translations) + width == support
    return anchor, width, support, translations


def sweep_kernel(translations, width):
    """Return exact open-box density and integrated CDF at sorted events.

    At a breakpoint both ending and newly starting boxes are excluded.
    Hence its count is the left-cell count minus the ending multiplicity.
    The next-cell count then includes the starting multiplicity. These
    formulas do not test box membership at each query point.
    """
    starts = Counter(translations)
    ends = Counter(t + width for t in translations)
    events = sorted(set(starts) | set(ends))
    cells = []
    points = []
    cdf = []
    active = 0
    cumulative = Q(0)
    scale = len(translations) * width
    for j, t in enumerate(events):
        if j:
            left = events[j - 1]
            value = Q(active) / scale
            cumulative += value * (t - left)
            cells.append({
                "left": str(left), "right": str(t),
                "midpoint": str((left + t) / 2), "value": str(value),
            })
        point_value = Q(active - ends[t]) / scale
        points.append({"t": str(t), "value": str(point_value)})
        cdf.append({"t": str(t), "value": str(cumulative)})
        active += starts[t] - ends[t]
        assert active >= 0
    assert active == 0
    assert cumulative == 1
    assert points[0]["value"] == points[-1]["value"] == "0"
    assert all(Q(cell["value"]) > 0 for cell in cells)
    assert all(Q(point["value"]) > 0 for point in points[1:-1])
    return cells, points[1:-1], [points[0], points[-1]], cdf


def verify_fixture(tile, perturbation, sample_names):
    periods = [Q(v) for v in tile["periods"]]
    starts = [Q(v) for v in tile["starts"]]
    field = perturbation["field"]
    if field is not None:
        values = {"periods": periods, "starts": starts}[field]
        values[perturbation["runner"]] += Q(perturbation["delta"])
    assert all(p > 0 for p in periods)
    anchor, width, support, translations = make_kernel(periods)
    anchor_values = {"0": Q(0), "1/7": Q(1, 7), "H": support,
                     "H+1/7": support + Q(1, 7)}
    samples = []
    for name in sample_names:
        a = anchor_values[name]
        averages = [
            sum((primitive(a + t + width, p, s) - primitive(a + t, p, s)
                 for t in translations), Q(0)) / (64 * width)
            for p, s in zip(periods, starts)
        ]
        assert averages == [Q(1, 4)] * 4
        total = sum(averages, Q(0))
        assert total == 1
        samples.append({"name": name, "a": str(a),
                        "train_integrals": list(map(str, averages)),
                        "total": str(total)})
    cells, breakpoints, endpoints, cdf = sweep_kernel(translations, width)
    discrete = []
    for i in range(4):
        if i == anchor:
            continue
        for kind, t, expected in (
            ("boundary", starts[i], Q(0)),
            ("interior", starts[i] + periods[i] / 8, Q(1, 4)),
        ):
            value = sum((occupied(t + r * periods[i] / 4, periods[i], starts[i])
                         for r in range(4)), Q(0)) / 4
            assert value == expected
            discrete.append({"label": i, "t": str(t),
                             "kind": kind, "value": str(value)})
    fixture = {
        "id": tile["id"] + "__" + perturbation["id"],
        "periods": list(map(str, periods)), "starts": list(map(str, starts)),
        "anchor_index": anchor, "P": str(width), "H": str(support),
        "atom_count": len(translations), "samples": samples,
        "kernel_cells": cells, "kernel_breakpoints": breakpoints,
        "kernel_endpoints": endpoints, "discrete_checks": discrete,
    }
    return fixture, {"id": fixture["id"], "cdf_breakpoints": cdf}


def threshold_events(periods, starts, left, right):
    """Independent finite event generator for open train thresholds."""
    events = {left, right}
    for period, start in zip(periods, starts):
        for offset in (Q(0), period / 4):
            origin = start + offset
            lower = (left - origin) // period - 1
            upper = (right - origin) // period + 1
            for integer in range(lower, upper + 1):
                event = origin + integer * period
                if left <= event <= right:
                    events.add(event)
    return sorted(events)


def verify_equality(spec):
    """Event-only check; deliberately no kernel or train integral evaluation."""
    periods = list(map(Q, spec["periods"]))
    starts = list(map(Q, spec["starts"]))
    left, right = map(Q, spec["window"])
    anchor = periods.index(max(periods))
    support = periods[anchor] + Q(3, 4) * sum(
        (p for i, p in enumerate(periods) if i != anchor), Q(0))
    assert support == right - left == Q(spec["expected_H"])
    events = threshold_events(periods, starts, left, right)
    multiplicity = lambda t: sum(occupied(t, p, s) for p, s in zip(periods, starts))
    points = [{"t": str(t), "multiplicity": multiplicity(t),
               "safe": multiplicity(t) == 0} for t in events]
    cells = [{"left": str(a), "right": str(b), "midpoint": str((a + b) / 2),
              "multiplicity": multiplicity((a + b) / 2)}
             for a, b in zip(events, events[1:])]
    safe_points = [point["t"] for point in points if point["safe"]]
    safe_duration = sum((Q(cell["right"]) - Q(cell["left"])
                         for cell in cells if cell["multiplicity"] == 0), Q(0))
    assert safe_points == spec["expected_safe_points"]
    assert len(points) == 14 and len(cells) == 13
    assert all(point["multiplicity"] == 0 for point in points)
    assert all(cell["multiplicity"] == 1 for cell in cells)
    assert safe_duration == 0
    return {"id": spec["id"], "periods": list(map(str, periods)),
            "starts": list(map(str, starts)), "window": [str(left), str(right)],
            "H": str(support), "width": str(right - left), "points": points,
            "cells": cells, "safe_points": safe_points,
            "safe_duration": str(safe_duration)}


def main():
    protocol_bytes = (HERE / "protocol.json").read_bytes()
    assert sha256(protocol_bytes).hexdigest() == PROTOCOL_SHA256
    protocol = json.loads(protocol_bytes)
    assert len(protocol["tiles"]) == len(protocol["perturbations"]) == 3
    assert protocol["samples"] == ["0", "1/7", "H", "H+1/7"]
    fixtures = []
    cdfs = []
    for tile in protocol["tiles"]:
        for perturbation in protocol["perturbations"]:
            fixture, cdf = verify_fixture(tile, perturbation, protocol["samples"])
            fixtures.append(fixture)
            cdfs.append(cdf)
    equality = verify_equality(protocol["equality_window"])
    counts = {
        "fixtures": len(fixtures),
        "train_integrals": sum(len(s["train_integrals"]) for f in fixtures for s in f["samples"]),
        "totals": sum(len(f["samples"]) for f in fixtures),
        "kernel_cells": sum(len(f["kernel_cells"]) for f in fixtures),
        "kernel_breakpoints": sum(len(f["kernel_breakpoints"]) for f in fixtures),
        "kernel_endpoints": sum(len(f["kernel_endpoints"]) for f in fixtures),
        "discrete_checks": sum(len(f["discrete_checks"]) for f in fixtures),
        "cdf_breakpoints": sum(len(f["cdf_breakpoints"]) for f in cdfs),
        "equality_points": len(equality["points"]),
        "equality_cells": len(equality["cells"]),
    }
    assert counts["train_integrals"] == 144 and counts["totals"] == 36
    assert counts["kernel_endpoints"] == 18 and counts["discrete_checks"] == 54
    result = {
        "status": "OBSERVED within the frozen finite protocol; no general proof certification",
        "method": "Periodic occupancy primitive; sorted signed-event density/CDF; threshold events",
        "protocol_sha256": PROTOCOL_SHA256, "counts": counts,
        "fixtures": fixtures, "equality_window": equality,
        "independent_cdf": cdfs,
    }
    output = HERE / "verifier_results.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": output.name, "counts": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
