"""Exact lap-labelled overlap certificates for five prescribed local cases.

Standard library only. No project imports. Default prints JSON; --check compares
the archived result. No general Lonely Runner or graph-selection claim.
"""
from collections import defaultdict
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


def episodes(speeds):
    result = []
    for v in speeds:
        for lap in range(v+1):
            a, b = max(LO, (lap-D)/v), min(HI, (lap+D)/v)
            if a < b:
                result.append({"speed": v, "lap": lap, "left": a, "right": b})
    return sorted(result, key=lambda x: (x["left"], x["right"], x["speed"], x["lap"]))


def overlap(a, b):
    return max(F(0), min(a["right"], b["right"])-max(a["left"], b["left"]))


def label(e):
    return [e["speed"], e["lap"]]


def components(count, edges):
    parent = list(range(count))

    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i

    selected = []
    for i, j, weight in sorted(edges, key=lambda e: (-e[2], e[0], e[1])):
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
            selected.append((i, j, weight))
    return selected


def case(w):
    speeds = (6, 7, 11, w)
    ep = episodes(speeds)
    edges = [(i, j, overlap(a, b))
             for (i, a), (j, b) in combinations(enumerate(ep), 2) if overlap(a, b)]
    maximum_forest = components(len(ep), edges)

    # Construct another forest directly by increasing left endpoints.
    sweep_forest = []
    leader = None
    for i, e in enumerate(ep):
        if leader is not None and overlap(e, ep[leader]):
            sweep_forest.append((leader, i, overlap(e, ep[leader])))
        if leader is None or e["right"] > ep[leader]["right"]:
            leader = i
    total = sum((e["right"]-e["left"] for e in ep), F(0))
    forest_weight = sum((z for i, j, z in maximum_forest), F(0))
    assert forest_weight == sum((z for i, j, z in sweep_forest), F(0))
    certificate = HI-LO-total+forest_weight

    # Separate check: direct threshold partition and phase evaluation.
    cuts = {LO, HI}
    for v in speeds:
        for lap in range(v+1):
            for sign in (-1, 1):
                t = (lap+sign*D)/v
                if LO < t < HI:
                    cuts.add(t)
    cuts = sorted(cuts)
    masses = defaultdict(F)
    clear_cells = []
    for a, b in zip(cuts, cuts[1:]):
        t = (a+b)/2
        assert all(distance(v*t) >= D for v in CORE)
        state = tuple(v for v in speeds if distance(v*t) < D)
        masses[state] += b-a
        if not state:
            clear_cells.append([a, b])
    valid_boundaries = [t for t in cuts
                        if all(distance(v*t) >= D for v in (*CORE, *speeds))]
    assert certificate == masses[()]
    expected = {13: F(0), 14: F(1, 112), 15: F(1, 112),
                16: F(1, 896), 17: F(1, 112)}
    assert certificate == expected[w]
    if w == 13:
        assert valid_boundaries == [F(3, 8)]

    triangles = []
    for a, b, c in combinations(ep, 3):
        left = max(e["left"] for e in (a, b, c))
        right = min(e["right"] for e in (a, b, c))
        pairwise = all(overlap(x, y) > 0 for x, y in combinations((a, b, c), 2))
        assert pairwise == (left < right)
        if left < right:
            triangles.append({"episodes": [label(e) for e in (a, b, c)],
                              "interval": [left, right], "duration": right-left})
    if w == 16:
        assert not triangles and len(ep) == 6 and len(edges) == 4
        assert clear_cells == [[F(17, 56), F(39, 128)]]
    if w in (14, 17):
        assert triangles

    def edge_records(items):
        return [{"episodes": [label(ep[i]), label(ep[j])], "duration": z}
                for i, j, z in items]

    return {
        "replacement": w, "episodes": ep, "positive_pair_edges": edge_records(edges),
        "maximum_weight_forest": edge_records(maximum_forest),
        "sweep_forest": edge_records(sweep_forest),
        "all_episode_pairs_form_forest": len(edges) == len(maximum_forest),
        "triple_intersections": triangles, "single_duration_sum": total,
        "forest_overlap_sum": forest_weight, "forest_clear_certificate": certificate,
        "direct_clear_duration": masses[()], "clear_cells_closures": clear_cells,
        "valid_threshold_boundaries": valid_boundaries,
        "direct_state_masses": [{"active": s, "duration": m}
                                for s, m in sorted(masses.items())],
    }


def main():
    for v in CORE:
        cell = int(v*LO)
        assert D <= v*LO-cell <= v*HI-cell <= 1-D
    rows = [case(w) for w in (13, 14, 15, 16, 17)]
    target = rows[3]
    original = {tuple(x["active"]): x["duration"] for x in target["direct_state_masses"]}
    altered = defaultdict(F, original)
    theta = F(1, 896)
    altered[()] -= theta
    for pair in ((6, 11), (6, 16), (11, 16)):
        altered[pair] -= theta
    for v in (6, 11, 16):
        altered[(v,)] += theta
    altered[(6, 11, 16)] += theta
    for size in (0, 1, 2):
        for subset in combinations((6, 7, 11, 16), size):
            def marginal(d):
                return sum((m for s, m in d.items() if set(subset) <= set(s)), F(0))
            assert marginal(original) == marginal(altered)
    assert min(altered.values()) >= 0 and altered[()] == 0
    assert altered[(6, 11, 16)] == theta

    # A triple would need the SAME speed-16 lap in both incident pair edges.
    neighbor_laps = {}
    for other in (6, 11):
        laps = set()
        for edge in target["positive_pair_edges"]:
            a, b = edge["episodes"]
            if {a[0], b[0]} == {other, 16}:
                laps.add(a[1] if a[0] == 16 else b[1])
        neighbor_laps[other] = sorted(laps)
    assert neighbor_laps == {6: [5], 11: [6]}
    assert set(neighbor_laps[6]).isdisjoint(neighbor_laps[11])
    # The arithmetic relation alone allows all-zero phases at t=0.
    assert 6+16 == 2*11
    assert all(distance(v*F(0)) < D for v in (6, 11, 16))
    result = {
        "date": "2026-09-25", "research_baseline": "3817153be1a6bd892c33a5b9019deb9ae6571ec4",
        "status": "Five exact local cases; no general successful-window selection theorem or novelty claim.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "core": CORE, "window": [LO, HI], "threshold": D,
        "artificial_distribution": {
            "same_total_single_pair_marginals": True, "clear_duration": altered[()],
            "forbidden_triple_mass": altered[(6, 11, 16)],
            "speed_16_laps_overlapping_each_neighbor": neighbor_laps,
            "no_consistent_speed_16_lap_for_triple": True,
        },
        "cases": rows,
    }
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads(Path(__file__).with_name("lap_constraints.json").read_text())
        print("PASS: five lap-labelled forests, direct phase crosschecks, equality boundary, and artificial-mass exclusion.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
