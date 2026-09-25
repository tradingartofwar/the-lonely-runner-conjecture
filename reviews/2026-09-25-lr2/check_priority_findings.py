"""Small exact controls for the LR 2 research-priority review.

Standard library only; no project imports. Prints results without writing files.
Use --check to compare with the archived JSON. This is not a theorem prover.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

D = F(1, 8)
LO, HI = F(9, 32), F(3, 8)
CORE = (1, 4, 5)


def distance(x):
    p = x % 1
    return min(p, 1-p)


def is_forest(vertices, edges):
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for a, b in edges:
        if a in parent and b in parent:
            a, b = find(a), find(b)
            if a == b:
                return False
            parent[a] = b
    return True


def case(w):
    speeds = (6, 7, 11, w)
    motif = ((6, 11), (6, w), (11, w), (7, 11))
    points = {LO, HI}
    # Core is safe throughout the closed window, certified in fixed phase cells.
    for v in CORE:
        cell = int(v*LO)
        assert D <= v*LO-cell <= v*HI-cell <= 1-D
    for v in speeds:
        for j in range(v+1):
            for offset in (-D, D):
                t = (j+offset)/v
                if LO < t < HI:
                    points.add(t)
    points = sorted(points)
    cells = [(a, b, {v for v in speeds if distance(v*(a+b)/2) < D})
             for a, b in zip(points, points[1:])]
    singles = sum((b-a)*len(s) for a, b, s in cells)
    pairs = {e: sum((b-a for a, b, s in cells if set(e) <= s), F(0))
             for e in combinations(speeds, 2)}
    positive_graph = {e for e, value in pairs.items() if value > 0}
    triple = sum((b-a for a, b, s in cells if {6, 11, w} <= s), F(0))
    clear = sum((b-a for a, b, s in cells if not s), F(0))
    pair_expression = HI-LO-singles+sum(pairs.values())
    corrected = HI-LO-singles+sum(pairs[e] for e in motif)-triple
    assert corrected <= clear
    forest = all(is_forest(s, positive_graph) for a, b, s in cells)
    if forest:
        assert pair_expression <= clear
    valid_boundaries = [t for t in points
                        if all(distance(v*t) >= D for v in (*CORE, *speeds))]
    if w == 13:
        assert clear == 0 and valid_boundaries == [F(3, 8)]
    if w == 16:
        assert triple == 0 and corrected == clear == F(1, 896)
    if w in (14, 17):
        assert pair_expression > clear and corrected < 0
    return {
        "replacement": w,
        "all_pair_expression_not_always_a_lower_bound": pair_expression,
        "actual_clear_duration": clear,
        "all_positive_edges": sorted(positive_graph),
        "all_active_graphs_are_forests_on_open_cells": forest,
        "fixed_triangle_and_leaf_corrected_lower_bound": corrected,
        "fixed_triangle_overlap": triple,
        "valid_threshold_boundaries": valid_boundaries,
    }


def main():
    vertices = (6, 7, 11, 16)
    edges = ((6, 11), (6, 16), (11, 16), (7, 11))
    for mask in range(16):
        s = {v for i, v in enumerate(vertices) if mask >> i & 1}
        triangle = {6, 11, 16} <= s
        edge_count = sum(set(e) <= s for e in edges)
        assert is_forest(s, edges) == (not triangle)
        assert 1-len(s)+edge_count-triangle <= int(not s)
        if not triangle:
            assert edge_count <= max(len(s)-1, 0)
    assert (1-F(15, 32), 1-F(41, 88)) == (F(17, 32), F(47, 88))
    # Speed-specific exclusion from LR 1, independently reevaluated.
    common = (max((F(2)-D)/6, (F(4)-D)/11),
              min((F(2)+D)/6, (F(4)+D)/11))
    assert common == (F(31, 88), F(17, 48))
    phases = tuple(16*t-5 for t in common)
    assert phases == (F(7, 11), F(2, 3))
    assert D < min(phases) <= max(phases) < 1-D
    result = {
        "date": "2026-09-25",
        "research_baseline": "1955eb3ce66bd3574fb0b14fb5726c18dc8861a0",
        "status": "Bounded review diagnostics; no general selection theorem or novelty claim.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "core": CORE,
        "window": (LO, HI),
        "triangle_leaf_logical_states_checked": 16,
        "forbidden_triangle_states_for_forest_version": 2,
        "successful_intervals_are_reflections": True,
        "triple_exclusion_phase_bounds": phases,
        "cases": [case(w) for w in (13, 14, 15, 16, 17)],
    }
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        archived = Path(__file__).with_name("priority_findings.json")
        assert json.loads(encoded) == json.loads(archived.read_text())
        print("PASS: 16 logical states, five exact controls, reflection and phase bounds.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
