"""Eight prescribed four-blocker comparisons; exact, standard library only.

Intersection lists and a separately structured phase partition crosscheck all
15 nonempty moments. --check compares with the archived output without writing.
This is a bounded diagnostic, not an arbitrary-speed certificate algorithm.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

D = F(1, 8)
J = (F(9, 32), F(3, 8))
CORE = (1, 4, 5)
EDGES = tuple(combinations(range(4), 2))
CASES = (
    ("doubled", (56, 112, 64, 72)),
    ("near_double_56", (56, 113, 64, 72)),
    ("tight", (6, 7, 11, 13)),
    ("tight_replacement", (6, 7, 8, 11)),
    ("below_old_coarse_cutoff", (309, 619, 320, 328)),
    ("at_old_coarse_cutoff", (310, 621, 320, 328)),
    ("above_old_coarse_cutoff", (320, 641, 328, 336)),
    ("original_missed_window", (6, 7, 11, 16)),
)


def floor(x):
    return x.numerator // x.denominator


def distance(x):
    p = x % 1
    return min(p, 1-p)


def occurrences(v):
    answer = []
    for m in range(floor(v*J[0]-D)+1, -floor(-(v*J[1]+D))):
        a, b = max(J[0], (m-D)/v), min(J[1], (m+D)/v)
        assert a < b
        answer.append((a, b, (m,)))
    return answer


def intersect_lists(left, right):
    """Two-pointer interval intersection; carries the actual lap labels."""
    answer = []
    i = j = 0
    while i < len(left) and j < len(right):
        a, b, labs = left[i]
        c, d, more = right[j]
        lo, hi = max(a, c), min(b, d)
        if lo < hi:
            answer.append((lo, hi, labs+more))
        if b <= d:
            i += 1
        if d <= b:
            j += 1
    return answer


def components(mask, state):
    parent = list(range(4))
    def root(i):
        while parent[i] != i:
            i = parent[i]
        return i
    for bit, (i, j) in enumerate(EDGES):
        if mask >> bit & 1 and state >> i & 1 and state >> j & 1:
            parent[root(i)] = root(j)
    return len({root(i) for i in range(4) if state >> i & 1})


def active_edges(mask, state):
    return sum(bool(mask >> bit & 1) and state >> i & 1 and state >> j & 1
               for bit, (i, j) in enumerate(EDGES))


def rank(mask, state):
    return active_edges(mask, state)-state.bit_count()+components(mask, state)


def forest(mask, state):
    return rank(mask, state) == 0


def unique_cycle(mask):
    assert mask.bit_count() == 4 and components(mask, 15) == 1
    # The minimal induced cyclic vertex set is the unique cycle.
    candidates = [s for s in range(1, 16) if rank(mask, s)]
    cycle = min(candidates, key=int.bit_count)
    for s in range(16):
        assert rank(mask, s) == int(s & cycle == cycle)
    return cycle


def partition(speeds):
    points = set(J)
    for v in (*CORE, *speeds):
        for m in range(floor(v*J[0])-1, floor(v*J[1])+2):
            for sign in (-1, 1):
                t = (m+sign*D)/v
                if J[0] < t < J[1]:
                    points.add(t)
    points = sorted(points)
    masses = [F(0) for _ in range(16)]
    clear_cells = []
    for a, b in zip(points, points[1:]):
        t = (a+b)/2
        assert all(distance(v*t) >= D for v in CORE)
        state = sum(1 << i for i, v in enumerate(speeds) if distance(v*t) < D)
        masses[state] += b-a
        if state == 0:
            clear_cells.append([a, b])
    boundaries = [t for t in points if all(distance(v*t) >= D for v in (*CORE, *speeds))]
    return masses, clear_cells, boundaries


def analyze(name, raw):
    speeds = tuple(sorted(raw))
    singles = [occurrences(v) for v in speeds]
    intervals = {}
    moments = {0: J[1]-J[0]}
    for subset in range(1, 16):
        lists = [singles[i] for i in range(4) if subset >> i & 1]
        joined = lists[0]
        for following in lists[1:]:
            joined = intersect_lists(joined, following)
        intervals[subset] = joined
        moments[subset] = sum((b-a for a, b, _ in joined), F(0))
        vertices = [v for i, v in enumerate(speeds) if subset >> i & 1]
        for a, b, laps in joined:
            assert a < b
            for v, m in zip(vertices, laps):
                assert v*J[0]-D < m < v*J[1]+D
            for (v, m), (w, n) in combinations(zip(vertices, laps), 2):
                assert abs(w*m-v*n) < D*(v+w)
    masses, clear_cells, boundaries = partition(speeds)
    for subset in range(16):
        assert moments[subset] == sum(z for s, z in enumerate(masses) if s & subset == subset)
    base = moments[0]-sum(moments[1 << i] for i in range(4))
    weights = [moments[(1 << i) | (1 << j)] for i, j in EDGES]

    def pair_bound(mask):
        return base+sum(z for bit, z in enumerate(weights) if mask >> bit & 1)

    def record(mask, correction=F(0)):
        return {"graph_mask": mask, "edges": [[speeds[i], speeds[j]] for bit, (i, j) in enumerate(EDGES) if mask >> bit & 1],
                "uncorrected_pair_expression": pair_bound(mask), "correction": correction,
                "bound": pair_bound(mask)-correction}

    tree_masks = [g for g in range(64) if g.bit_count() == 3 and forest(g, 15)]
    assert len(tree_masks) == 16
    tree = record(max(tree_masks, key=lambda g: (pair_bound(g), -g)))
    compatible_masks = [g for g in range(64) if all(forest(g, s) for s in range(1, 16) if moments[s] > 0)]
    compatible = record(max(compatible_masks, key=lambda g: (pair_bound(g), -g.bit_count(), -g)))
    assert compatible["bound"] >= tree["bound"]
    if moments[15] > 0:
        assert all(forest(g, 15) for g in compatible_masks)
        assert compatible["bound"] == tree["bound"]

    # Count identity for every graph/state, and integral gap for all 64 graphs.
    for g in range(64):
        for s in range(16):
            count = 1-s.bit_count()+active_edges(g, s)-rank(g, s)
            assert count == 1-components(g, s) <= int(s == 0)
        corrected = pair_bound(g)-sum(rank(g, s)*z for s, z in enumerate(masses))
        gap = sum((components(g, s)-1)*z for s, z in enumerate(masses) if s)
        assert masses[0]-corrected == gap >= 0

    one_cycle = []
    four_cycles = []
    for g in range(64):
        if g.bit_count() != 4 or components(g, 15) != 1:
            continue
        cycle = unique_cycle(g)
        row = {**record(g, moments[cycle]), "cycle_vertices": [v for i, v in enumerate(speeds) if cycle >> i & 1]}
        one_cycle.append(row)
        if cycle == 15:
            four_cycles.append(row)
    assert len(one_cycle) == 15 and len(four_cycles) == 3
    choose = lambda rows: max(rows, key=lambda r: (r["bound"], -r["graph_mask"]))
    best_one = choose(one_cycle)
    best_four = choose(four_cycles)
    assert best_one["bound"] >= tree["bound"]
    matchings = [(0, 5), (1, 4), (2, 3)]
    four_formula = base+sum(weights)-min(weights[i]+weights[j] for i, j in matchings)-moments[15]
    assert best_four["bound"] == four_formula

    diamonds = []
    for bit, (i, j) in enumerate(EDGES):
        g = 63 ^ (1 << bit)
        missing = (1 << i) | (1 << j)
        triangles = [s for s in range(16) if s.bit_count() == 3 and s & missing != missing]
        assert len(triangles) == 2
        for s in range(16):
            assert rank(g, s) == sum(s & t == t for t in triangles)
        row = {**record(g, sum(moments[t] for t in triangles)), "missing_edge": [speeds[i], speeds[j]],
               "triangles": [[v for k, v in enumerate(speeds) if t >> k & 1] for t in triangles],
               "gap_equals_missing_pair_only_mass": masses[missing]}
        assert row["bound"] == masses[0]-masses[missing]
        diamonds.append(row)
    best_diamond = choose(diamonds)
    assert best_diamond["bound"] >= best_one["bound"]
    exact = base+sum(weights)-sum(moments[s] for s in range(16) if s.bit_count() == 3)+moments[15]
    assert exact == masses[0]

    return {"name": name, "extras": speeds, "occurrence_counts": list(map(len, singles)),
            "state_mass_by_mask": masses, "moments_by_mask": {str(s): moments[s] for s in range(1, 16)},
            "pair_weights_in_lexicographic_order": weights,
            "triple_and_quad_intersections": [{"vertices": [v for i, v in enumerate(speeds) if s >> i & 1],
                "duration": moments[s], "lap_intersections": intervals[s]} for s in range(16) if s.bit_count() >= 3],
            "tree": tree, "compatibility": compatible, "one_cycle": best_one, "four_cycle": best_four,
            "diamond": best_diamond, "all_one_cycle_options": one_cycle, "all_diamond_options": diamonds,
            "clear_duration": masses[0], "clear_cells": clear_cells, "valid_boundaries": boundaries}


def main():
    for v in CORE:
        phase = floor(v*J[0])
        assert D <= v*J[0]-phase <= v*J[1]-phase <= 1-D
    cases = [analyze(*case) for case in CASES]
    assert cases[0]["moments_by_mask"]["15"] == F(1, 896)
    assert cases[1]["moments_by_mask"]["15"] == 0
    assert cases[2]["clear_duration"] == 0 and cases[2]["valid_boundaries"] == [F(3, 8)]
    assert cases[-1]["compatibility"]["bound"] == cases[-1]["clear_duration"] == F(1, 896)
    phase_exclusion = []
    for a, b, laps in intersect_lists(occurrences(56), occurrences(113)):
        k = floor(64*a)
        lo, hi = 64*a-k, 64*b-k
        assert D < lo <= hi < 1-D
        phase_exclusion.append({"56_113_laps": laps, "interval": [a, b], "64_lap": k, "64_phase_range": [lo, hi]})
    assert len(phase_exclusion) == 6
    result = {"date": "2026-09-25", "research_baseline": "91561c35751f1281c5b6920a8022f2f6653672bb",
              "status": "Eight prescribed cases; graph identities are self-contained proof candidates, no novelty claim or unbounded family conclusion.",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "core": CORE, "threshold": D, "window": J,
              "mask_convention": "Vertex bits follow sorted extras; edge bits follow lexicographic index pairs (01,02,03,12,13,23).",
              "verification": "120 nonempty moments crosschecked by interval joins and direct phase partitions; 8192 graph/state identities; every 64 graph corrected gaps in each case; equality endpoints checked directly.",
              "near_double_phase_exclusion": phase_exclusion,
              "cases": cases}
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads(Path(__file__).with_name("four_blocker_cycles.json").read_text())
        print("PASS: eight cases, 120 moment comparisons, 8192 graph/state identities, 512 corrected graph bounds, equality control.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
