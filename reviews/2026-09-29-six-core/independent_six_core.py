#!/usr/bin/env python3
"""Frozen six-core domain; independent exact threshold-cell reconstruction."""

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_HASH = "25c818133f6e78054d14e82bf4b0f0c6b63c9dd7d1ca9a12071d83f878b891a2"
ALPHA = F(1, 8)


def distance(t, v):
    z = t * v
    rem = z - z.numerator // z.denominator
    return min(rem, 1 - rem)


def safe(t, speeds):
    return all(distance(t, v) >= ALPHA for v in speeds)


def endpoint_partition(speeds):
    events = {F(0), F(1)}
    for v in speeds:
        for lap in range(v):
            events.add((lap + ALPHA) / v)
            events.add((lap + 1 - ALPHA) / v)
    events = sorted(events)
    point_flags = [safe(t, speeds) for t in events]
    cell_flags = [safe((l + r) / 2, speeds)
                  for l, r in zip(events, events[1:])]

    # Every safe cell has safe endpoints because safety is closed. The
    # separate endpoint evaluation also retains points with unsafe neighbors.
    pieces = [(t, t) for t, flag in zip(events, point_flags) if flag]
    for i, flag in enumerate(cell_flags):
        if flag:
            assert point_flags[i] and point_flags[i + 1]
            pieces.append((events[i], events[i + 1]))
    pieces.sort()
    components = []
    for l, r in pieces:
        if components and l <= components[-1][1]:
            components[-1] = (components[-1][0], max(r, components[-1][1]))
        else:
            components.append((l, r))
    return components, len(events), len(cell_flags)


def selected_distances(interval, speeds):
    if interval is None:
        return None
    l, r = interval
    return [
        {"point": label, "time": str(t),
         "distances": {str(v): str(distance(t, v)) for v in speeds}}
        for label, t in (("left", l), ("midpoint", (l + r) / 2), ("right", r))
    ]


def row_for(triple):
    a, b, c = triple
    speeds = [1, 4, 5, a, b, c]
    components, endpoint_count, cell_count = endpoint_partition(speeds)
    positive = [(l, r) for l, r in components if r > l]
    width = max((r - l for l, r in positive), default=F(0))
    ties = [(l, r) for l, r in positive if r - l == width]
    selected = ties[0] if ties else None
    if width:
        cutoff_fraction = 1 / (4 * width)
        cutoff = -(-cutoff_fraction.numerator // cutoff_fraction.denominator)
    else:
        cutoff = None
    return {
        "triple": list(triple),
        "speeds": speeds,
        "components": [[str(l), str(r)] for l, r in components],
        "positive_component_count": len(positive),
        "isolated_point_count": len(components) - len(positive),
        "safe_measure": str(sum((r - l for l, r in components), F(0))),
        "widest_width": str(width),
        "earliest_widest": [str(x) for x in selected] if selected else None,
        "widest_ties": [[str(l), str(r)] for l, r in ties],
        "selected_distances": selected_distances(selected, speeds),
        "last_runner_cutoff": cutoff,
        "endpoint_evaluations": endpoint_count,
        "open_cell_evaluations": cell_count,
    }


def main():
    raw = (HERE / "PROTOCOL.json").read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_HASH, "Protocol hash changed"
    protocol = json.loads(raw)
    branches = protocol["a_b_branches"]
    assert sum(len(bs) for bs in branches.values()) == 36
    triples = []
    for a_text, bs in branches.items():
        a = int(a_text)
        width = F(protocol["widths"][a_text])
        for b in bs:
            for c in range(b + 1, 63):
                if c in {1, 4, 5}:
                    continue
                if F(1, 4 * b) + F(1, 2 * c) < width:
                    continue
                vs = (a, b, c)
                if not any(v % 6 == 0 for v in vs):
                    continue
                if not any(v % 7 == 0 for v in vs):
                    continue
                residues = {v % 8 for v in vs}
                if not (0 in residues or {3, 7} <= residues):
                    continue
                triples.append(vs)
    triples.sort()
    assert len(triples) == len(set(triples))
    rows = [row_for(t) for t in triples]
    output = {
        "status": "OBSERVED: exact finite domain only",
        "method": "Independent rational threshold endpoints and open-cell midpoints",
        "protocol_sha256": PROTOCOL_HASH,
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "triples": [list(t) for t in triples],
        "rows": rows,
        "summary": {
            "case_count": len(rows),
            "all_rows_positive": all(F(r["safe_measure"]) > 0 for r in rows),
            "positive_components": sum(r["positive_component_count"] for r in rows),
            "isolated_points": sum(r["isolated_point_count"] for r in rows),
            "endpoint_evaluations": sum(r["endpoint_evaluations"] for r in rows),
            "open_cell_evaluations": sum(r["open_cell_evaluations"] for r in rows),
            "maximum_last_runner_cutoff": max(
                (r["last_runner_cutoff"] for r in rows if r["last_runner_cutoff"] is not None),
                default=None),
        },
    }
    path = HERE / "independent_six_core.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"summary": output["summary"], "output_sha256": sha256(path.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
