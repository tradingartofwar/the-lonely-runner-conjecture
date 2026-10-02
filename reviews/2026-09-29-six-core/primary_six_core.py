#!/usr/bin/env python3
"""Exact evaluation of the coordinator-frozen six-core domain only."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_HASH = "25c818133f6e78054d14e82bf4b0f0c6b63c9dd7d1ca9a12071d83f878b891a2"
THRESHOLD = Q(1, 8)


def union_closed(intervals):
    merged = []
    for left, right in sorted(intervals):
        assert left <= right
        if merged and left <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(right, merged[-1][1]))
        else:
            merged.append((left, right))
    return merged


def safe_bands(v):
    return [(Q(8*j+1, 8*v), Q(8*j+7, 8*v)) for j in range(v)]


def intersection(first, second):
    pieces = []
    for left1, right1 in first:
        for left2, right2 in second:
            left, right = max(left1, left2), min(right1, right2)
            if left <= right:
                pieces.append((left, right))
    return union_closed(pieces)


def distance(v, t):
    raw = v*t
    phase = raw - raw.numerator // raw.denominator
    return min(phase, 1-phase)


def point_certificate(core, t):
    values = [distance(v, t) for v in core]
    assert all(x >= THRESHOLD for x in values)
    return {"time": str(t),
            "distances": {str(v): str(x) for v, x in zip(core, values)}}


def interval_json(interval):
    return [str(interval[0]), str(interval[1])]


def declared_domain(protocol):
    result = []
    pairs = 0
    for a_text, bs in protocol["a_b_branches"].items():
        a = int(a_text)
        width = Q(protocol["widths"][a_text])
        for b in bs:
            pairs += 1
            for c in range(b+1, 63):
                triple = (a, b, c)
                if c in (1, 4, 5):
                    continue
                if Q(1, 4*b)+Q(1, 2*c) < width:
                    continue
                if not any(v % 6 == 0 for v in triple):
                    continue
                if not any(v % 7 == 0 for v in triple):
                    continue
                residues = {v % 8 for v in triple}
                if not (any(v % 8 == 0 for v in triple)
                        or {3, 7}.issubset(residues)):
                    continue
                result.append(triple)
    assert pairs == 36
    assert len(result) == len(set(result))
    return sorted(result)


def evaluate(triple):
    core = (1, 4, 5, *triple)
    assert len(set(core)) == 6 and list(triple) == sorted(triple)
    components = [(Q(0), Q(1))]
    for v in core:
        components = intersection(components, safe_bands(v))
    assert components == sorted(components)
    assert all(components[i][1] < components[i+1][0]
               for i in range(len(components)-1))
    assert components == sorted((1-r, 1-l) for l, r in components)
    for left, right in components:
        for v in core:
            assert any(l <= left <= right <= r for l, r in safe_bands(v))
    positive = [(l, r) for l, r in components if l < r]
    isolated = [l for l, r in components if l == r]
    measure = sum((r-l for l, r in positive), Q(0))
    record = {
        "triple": list(triple),
        "core_in_intersection_order": list(core),
        "components": [interval_json(i) for i in components],
        "positive_components": [interval_json(i) for i in positive],
        "isolated_points": [str(t) for t in isolated],
        "positive_component_count": len(positive),
        "isolated_point_count": len(isolated),
        "safe_measure": str(measure),
        "selected_earliest_widest_component": None,
        "width": None,
        "widest_ties": [],
        "widest_tie_count": 0,
        "sufficient_last_residual_threshold": None,
        "selected_component_certificates": None,
        "isolated_point_certificates": [point_certificate(core, t) for t in isolated],
    }
    if positive:
        width = max(r-l for l, r in positive)
        ties = [(l, r) for l, r in positive if r-l == width]
        chosen = ties[0]
        bound = Q(1, 4)/width
        cutoff = -(-bound.numerator // bound.denominator)
        assert Q(1, 4*cutoff) <= width
        assert cutoff == 1 or Q(1, 4*(cutoff-1)) > width
        record.update({
            "selected_earliest_widest_component": interval_json(chosen),
            "width": str(width),
            "widest_ties": [interval_json(i) for i in ties],
            "widest_tie_count": len(ties),
            "sufficient_last_residual_threshold": cutoff,
            "selected_component_certificates": {
                "left": point_certificate(core, chosen[0]),
                "midpoint": point_certificate(core, (chosen[0]+chosen[1])/2),
                "right": point_certificate(core, chosen[1]),
            },
        })
    return record


def main():
    raw = (HERE / "PROTOCOL.json").read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_HASH
    protocol = json.loads(raw)
    domain = declared_domain(protocol)
    records = [evaluate(triple) for triple in domain]
    result = {
        "status": "OBSERVED exact finite arithmetic; general implications remain proof candidates",
        "parent_commit": protocol["parent_commit"],
        "date": protocol["date"],
        "threshold": "1/8",
        "time_domain": ["0", "1"],
        "blocking": "open; threshold equality safe",
        "arithmetic": "Python fractions.Fraction",
        "algorithm": "successive closed safe-band intersections in order1,4,5,a,b,c; merge touching pieces",
        "domain": [list(t) for t in domain],
        "record_count": len(records),
        "tie_policy": "smallest left endpoint among positive maximum-width components",
        "last_runner_cutoff": "ceil(1/(4w)); no final d values evaluated",
        "command": "python reviews/2026-09-29-six-core/primary_six_core.py",
        "source_sha256": {
            "PROTOCOL.json": PROTOCOL_HASH,
            "primary_six_core.py": sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "records": records,
    }
    (HERE / "primary_six_core.json").write_text(json.dumps(result, indent=2)+"\n")
    lines = [
        "# Frozen direct six-core exact table", "",
        "**OBSERVED** on the complete frozen protocol domain. No final d values",
        "were evaluated. General reductions and the final-speed implication remain",
        "proof candidates; this bounded calculation is not an external proof certificate.", "",
        "| (a,b,c) | Earliest widest closed window | Width | Safe measure | Sufficient d >= | Isolated points |",
        "| --- | --- | --- | --- | ---: | ---: |",
    ]
    for row in records:
        selected = row["selected_earliest_widest_component"]
        window = "none" if selected is None else f"[{selected[0]}, {selected[1]}]"
        lines.append(f"| {tuple(row['triple'])} | {window} | {row['width']} | "
                     f"{row['safe_measure']} | {row['sufficient_last_residual_threshold']} | "
                     f"{row['isolated_point_count']} |")
    lines += ["", "All maximal components, isolated points, widest ties, exact endpoint",
              "and midpoint distances, and source hashes are retained in the JSON.", ""]
    (HERE / "PRIMARY_TABLE.md").write_text("\n".join(lines))
    print(json.dumps({
        "records": len(records),
        "all_have_positive_components": all(r["positive_component_count"] for r in records),
        "minimum_width": min((Q(r["width"]) for r in records if r["width"]), default=None),
        "maximum_last_runner_cutoff": max((r["sufficient_last_residual_threshold"] or 0
                                            for r in records), default=0),
        "positive_components": sum(r["positive_component_count"] for r in records),
        "isolated_points": sum(r["isolated_point_count"] for r in records),
    }, default=str, indent=2))


if __name__ == "__main__":
    main()
