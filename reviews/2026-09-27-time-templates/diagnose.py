#!/usr/bin/env python3
"""Bounded diagnostics selected only by the frozen fixed-template classifier.

Primary method: closed safe-lap intersections, followed by exact interval
projection onto the chosen runner's phase circle. No project imports, phase
grid, multiplicity profile, or new-template search. --write creates the
archive; default/--check recomputes and compares without changing files.
"""

from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json


HERE = Path(__file__).resolve().parent
PROTOCOL_HASH = "0932c23c6c65dd8faaae4d319770ae0bca583237c0f92fee9c5ae7f8ce474f02"
EXCLUDED = {1, 4, 5, 6, 7, 11}
H = F(1, 8)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def canonical_digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"))+"\n"
    return sha256(raw.encode()).hexdigest()


def merge_closed(intervals):
    result = []
    for left, right in sorted(intervals):
        assert left <= right
        if result and left <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], right))
        else:
            result.append((left, right))
    return result


def intersection(A, B):
    return merge_closed((max(a, c), min(b, d))
                        for a, b in A for c, d in B
                        if max(a, c) <= min(b, d))


def safe_laps(speed):
    assert isinstance(speed, int) and speed > 0
    return [(F(8*m+1, 8*speed), F(8*m+7, 8*speed))
            for m in range(speed)]


def safe_set(speeds):
    result = [(F(0), F(1))]
    for speed in speeds:
        result = intersection(result, safe_laps(speed))
    return result


def circle_union(intervals):
    """Input linear closures; 1 is excluded in the canonical circle cut."""
    result = []
    for left, right in merge_closed(intervals):
        assert F(0) <= left <= right <= F(1)
        if left == 1:
            continue
        result.append((left, right, True, right != 1))
    return result


def project_components(components, chosen_speed=11):
    images = []
    for left, right in components:
        lo, hi = chosen_speed*left, chosen_speed*right
        first = lo.numerator//lo.denominator
        last = hi.numerator//hi.denominator
        for lap in range(first, last+1):
            a, b = max(lo, F(lap))-lap, min(hi, F(lap+1))-lap
            if a <= b and a < 1:
                images.append((a, b))
    return circle_union(images)


def contains(pieces, point):
    assert 0 <= point < 1
    return any(a < point < b or (point == a and lc) or (point == b and rc)
               for a, b, lc, rc in pieces)


def metrics(pieces):
    if not pieces:
        return {"nonempty": False, "measure": F(0),
                "maximum_circular_gap": F(1),
                "minimum_covering_arc_length": F(0),
                "maximal_gap_arcs": []}
    gaps = []
    for previous, current in zip(pieces, pieces[1:]):
        a, b = previous[1], current[0]
        if a < b:
            gaps.append((a % 1, b % 1, b-a))
    a, b = pieces[-1][1], pieces[0][0]+1
    if a < b:
        gaps.append((a % 1, b % 1, b-a))
    maximum = max((row[2] for row in gaps), default=F(0))
    return {"nonempty": True,
            "measure": sum((b-a for a, b, _, _ in pieces), F(0)),
            "maximum_circular_gap": maximum,
            "minimum_covering_arc_length": 1-maximum,
            "maximal_gap_arcs": sorted(row for row in gaps if row[2] == maximum)}


def witness(speeds, components):
    if not components:
        return None
    positive = [cell for cell in components if cell[0] < cell[1]]
    if positive:
        left, right = min(positive, key=lambda cell: (-(cell[1]-cell[0]), cell[0]))
        time = (left+right)/2
    else:
        time = components[0][0]
    phases = [(speed*time) % 1 for speed in speeds]
    distances = [min(x, 1-x) for x in phases]
    minimum = min(distances)
    assert minimum >= H
    kind = "strict" if minimum > H else "equality"
    assert (kind == "strict") == bool(positive)
    return {"time": time, "kind": kind, "phases": phases,
            "distances": distances, "minimum_distance": minimum}


def diagnose_case(residue, V):
    unchanged = [1, 4, 5, 6, 7, V]
    speeds = [1, 4, 5, 6, 7, 11, V]
    assert len(set(speeds)) == 7
    A = safe_set(unchanged)
    positive_A = [(a, b) for a, b in A if a < b]
    isolated_A = [a for a, b in A if a == b]
    P = project_components(A)
    B = project_components(positive_A)
    extra_points = sorted({(11*t) % 1 for t in isolated_A
                           if not contains(B, (11*t) % 1)})
    assert P == circle_union([(a, b) for a, b, _, _ in B]+[(x, x) for x in extra_points])
    pm, bm = metrics(P), metrics(B)
    allowed = intersection(A, safe_laps(11))
    duration = sum((b-a for a, b in allowed), F(0))
    positive_count = sum(a < b for a, b in allowed)
    isolated = [a for a, b in allowed if a == b]
    status = "strict" if duration > 0 else ("contacts" if allowed else "empty")
    result = encode({
        "residue": residue, "V": V, "velocities": [0]+speeds,
        "unchanged_speeds": unchanged,
        "A_components": A,
        "A_duration": sum((b-a for a, b in A), F(0)),
        "A_positive_component_count": len(positive_A),
        "A_isolated_times": isolated_A,
        "P_components": P, "B_components": B,
        "extra_isolated_projection_points": extra_points,
        "P_metrics": pm, "B_metrics": bm,
        "all_phase_decisions": {
            "nonempty_for_every_phase": bool(P) and pm["minimum_covering_arc_length"] >= 2*H,
            "positive_duration_for_every_phase": bool(B) and bm["minimum_covering_arc_length"] > 2*H,
            "nonempty_covering_margin": pm["minimum_covering_arc_length"]-2*H,
            "positive_duration_covering_margin": bm["minimum_covering_arc_length"]-2*H,
            "criterion_status": "supplied covering criteria; general proof-candidate status retained"},
        "common_start_components": allowed, "common_start_duration": duration,
        "common_start_positive_component_count": positive_count,
        "common_start_isolated_times": isolated,
        "common_start_status": status,
        "common_start_witness": witness(speeds, allowed)})
    result["case_sha256"] = canonical_digest(result)
    return result


def build():
    protocol_raw = (HERE/"protocol.json").read_bytes()
    assert sha256(protocol_raw).hexdigest() == PROTOCOL_HASH
    protocol = json.loads(protocol_raw)
    assert protocol["family"]["threshold"] == "1/8"
    classification_raw = (HERE/"classification.json").read_bytes()
    classification = json.loads(classification_raw)
    assert classification["protocol_sha256"] == PROTOCOL_HASH
    assert classification["period"] == 120
    assert set(classification["excluded_V"]) == EXCLUDED
    failed = classification["failed_residue_classes"]
    assert failed == sorted(set(failed))
    assert failed == [row["residue"] for row in classification["residue_rows"]
                      if row["union"]["status"] == "failure"]
    representatives = []
    for residue in failed:
        assert 0 <= residue < 120
        V = residue if residue else 120
        while V in EXCLUDED:
            V += 120
        representatives.append({"residue": residue, "V": V})
    assert representatives == classification["failure_representatives"]
    performed = len(failed) <= 6
    cases = [diagnose_case(row["residue"], row["V"]) for row in representatives] if performed else []
    totals = {
        "cases": len(cases),
        "A_components": sum(len(row["A_components"]) for row in cases),
        "A_positive_components": sum(row["A_positive_component_count"] for row in cases),
        "A_isolated_times": sum(len(row["A_isolated_times"]) for row in cases),
        "common_start_components": sum(len(row["common_start_components"]) for row in cases),
        "common_start_positive_components": sum(row["common_start_positive_component_count"] for row in cases),
        "common_start_isolated_times": sum(len(row["common_start_isolated_times"]) for row in cases),
        "all_phase_nonempty_cases": sum(row["all_phase_decisions"]["nonempty_for_every_phase"] for row in cases),
        "all_phase_positive_duration_cases": sum(row["all_phase_decisions"]["positive_duration_for_every_phase"] for row in cases),
        "common_start_strict_cases": sum(row["common_start_status"] == "strict" for row in cases),
        "common_start_contact_cases": sum(row["common_start_status"] == "contacts" for row in cases),
        "common_start_empty_cases": sum(row["common_start_status"] == "empty" for row in cases)}
    return {"schema_version": 1,
            "status": "OBSERVED bounded representative diagnostics; supplied covering implications retain proof-candidate status",
            "protocol_sha256": PROTOCOL_HASH,
            "classification_sha256": sha256(classification_raw).hexdigest(),
            "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "failed_residues": failed,
            "selected_representatives": representatives,
            "diagnostics_performed": performed,
            "stop_reason": None if performed else "more_than_six_failed_classes",
            "cases": cases, "totals": totals}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    path = HERE/"diagnostics.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2)+"\n")
    else:
        assert json.loads(path.read_text()) == result, "diagnostics.json mismatch"
    print(json.dumps({"diagnostics_performed": result["diagnostics_performed"],
                      "totals": result["totals"]}, sort_keys=True))


if __name__ == "__main__":
    main()
