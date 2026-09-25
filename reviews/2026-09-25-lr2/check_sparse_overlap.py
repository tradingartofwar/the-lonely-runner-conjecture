"""Sparse graph certificates for one fixed six-speed core and variable w.

No third-party or project imports. --check verifies the archived JSON.
The finite branch is w=1..298 excluding the six fixed speeds; the written
argument supplies the tail w>=299. Direct partitions only check the finite
branch, not arbitrarily large speeds. No general Lonely Runner proof.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

D = F(1, 8)
CORE = (1, 4, 5, 6, 7, 11)
J = (F(9, 32), F(3, 8))
P = (F(31, 88), F(17, 48))  # 6 and 11 block together
Q = (J[0], F(25, 88))       # 7 and 11 block together
FIXED = {
    6: [(F(5, 16), F(17, 48))],
    7: [(J[0], F(17, 56))],
    11: [Q, (F(31, 88), J[1])],
}
FIXED_SUM = sum((b-a for parts in FIXED.values() for a, b in parts), F(0))
TAIL_START = 299


def floor(x):
    return x.numerator // x.denominator


def distance(x):
    p = x % 1
    return min(p, 1-p)


def primitive(x):
    y = x+D
    m = floor(y)
    return 2*D*m+min(y-m, 2*D)


def blocked(interval, w):
    a, b = interval
    return (primitive(w*b)-primitive(w*a))/w


def triple_possible(interval, w):
    a, b = interval
    # Strictly between w*a-D and w*b+D must lie an integer meeting label.
    return floor(w*a-D)+1 < w*b+D


def is_forest(vertices, edges):
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for a, b in edges:
        if a in parent and b in parent:
            x, y = find(a), find(b)
            if x == y:
                return False
            parent[x] = y
    return True


def sparse(w):
    assert w > 0 and w not in CORE
    edge_list = [(6, 11), (7, 11), (6, w), (7, w), (11, w)]
    weights = [P[1]-P[0], Q[1]-Q[0]] + [
        sum((blocked(interval, w) for interval in FIXED[v]), F(0))
        for v in (6, 7, 11)
    ]
    hp, hq = triple_possible(P, w), triple_possible(Q, w)
    positive_mask = sum(1 << i for i, x in enumerate(weights) if x > 0)
    candidates = []
    # Five possible positive pair edges; no 6/7 overlap.
    for mask in range(32):
        if mask & positive_mask != mask:
            continue
        if hp and mask & 0b10101 == 0b10101:
            continue
        if hq and mask & 0b11010 == 0b11010:
            continue
        value = sum((x for i, x in enumerate(weights) if mask >> i & 1), F(0))
        candidates.append((value, -mask.bit_count(), -mask))
    weight, _, negative_mask = max(candidates)
    mask = -negative_mask
    graph = [e for i, e in enumerate(edge_list) if mask >> i & 1]
    base = J[1]-J[0]-FIXED_SUM-blocked(J, w)
    bound = base+weight
    tree_values = [value for value, _, minus_mask in candidates
                   if is_forest((6, 7, 11, w), [e for i, e in enumerate(edge_list)
                                             if (-minus_mask) >> i & 1])]
    best_tree_bound = base+max(tree_values)

    # Verify the pointwise inequality on all states consistent with our facts.
    for bits in range(16):
        state = {v for i, v in enumerate((6, 7, 11, w)) if bits >> i & 1}
        if {6, 7} <= state:
            continue
        if not hp and {6, 11, w} <= state:
            continue
        if not hq and {7, 11, w} <= state:
            continue
        assert is_forest(state, graph)
        active_edges = sum(set(e) <= state for e in graph)
        assert 1-len(state)+active_edges <= int(not state)

    star = base+sum(weights[2:], F(0))
    uniform = F(31, 9856)-F(15, 16*w)
    assert bound >= star >= uniform
    if w >= TAIL_START:
        assert uniform > 0
    return {
        "replacement": w, "triple_6_11_w_possible": hp,
        "triple_7_11_w_possible": hq, "selected_edges": graph,
        "selected_pair_weight": weight, "clear_lower_bound": bound,
        "best_runner_tree_bound": best_tree_bound,
        "fast_runner_star_bound": star, "uniform_star_lower_bound": uniform,
    }


def direct(w):
    speeds = (*CORE, w)
    points = set(J)
    for v in speeds:
        for m in range(floor(v*J[0])-1, floor(v*J[1])+2):
            for sign in (-1, 1):
                t = (m+sign*D)/v
                if J[0] < t < J[1]:
                    points.add(t)
    points = sorted(points)
    singles = {v: F(0) for v in (6, 7, 11, w)}
    pairs = {e: F(0) for e in combinations((6, 7, 11, w), 2)}
    triples = {"p": F(0), "q": F(0)}
    clear = F(0)
    for a, b in zip(points, points[1:]):
        t = (a+b)/2
        assert all(distance(v*t) >= D for v in (1, 4, 5))
        active = {v for v in (6, 7, 11, w) if distance(v*t) < D}
        assert not {6, 7} <= active
        for v in active:
            singles[v] += b-a
        for e in pairs:
            if set(e) <= active:
                pairs[e] += b-a
        if {6, 11, w} <= active:
            triples["p"] += b-a
        if {7, 11, w} <= active:
            triples["q"] += b-a
        if not active:
            clear += b-a
    assert singles[w] == blocked(J, w)
    for v in (6, 7, 11):
        assert singles[v] == sum((b-a for a, b in FIXED[v]), F(0))
        assert pairs[v, w] == sum((blocked(I, w) for I in FIXED[v]), F(0))
    assert pairs[6, 11] == P[1]-P[0] and pairs[7, 11] == Q[1]-Q[0]
    assert (triples["p"] > 0) == triple_possible(P, w)
    assert (triples["q"] > 0) == triple_possible(Q, w)
    valid = [t for t in points if all(distance(v*t) >= D for v in speeds)]
    return clear, valid


def main():
    for v in (1, 4, 5):
        cell = floor(v*J[0])
        assert D <= v*J[0]-cell <= v*J[1]-cell <= 1-D
    assert FIXED_SUM == F(331, 3696)
    assert F(3, 4)*(J[1]-J[0]-FIXED_SUM) == F(31, 9856)
    assert F(15, 16)/F(31, 9856) == F(9240, 31)
    rows = []
    for w in range(1, TAIL_START):
        if w in CORE:
            continue
        r = sparse(w)
        actual, valid = direct(w)
        assert r["clear_lower_bound"] <= actual
        assert (r["clear_lower_bound"] == 0) == (w in (3, 10, 13, 26))
        if w not in (3, 10, 13, 26):
            assert r["clear_lower_bound"] > 0
        else:
            assert actual == 0 and F(3, 8) in valid
        r.update(actual_clear_duration=actual,
                 exact_duration_recovered=(actual == r["clear_lower_bound"]))
        if actual == 0:
            r["valid_times"] = valid
        rows.append(r)
    assert len(rows) == 292
    assert sum(r["exact_duration_recovered"] for r in rows) == 79
    assert min((r["clear_lower_bound"], r["replacement"])
               for r in rows if r["clear_lower_bound"] > 0) == (F(1, 896), 16)
    # Large examples exercise the formula without enumerating their meetings.
    large = []
    for w in (299, 10**12, 56*10**12):
        row = sparse(w)
        if w % 8:
            witness = F(1, 8)
        elif w % 56:
            witness = F(17, 56)
        else:
            witness = F(17, 56)+F(1, 8*w)
        assert all(distance(v*witness) >= D for v in (*CORE, w))
        row["separately_checked_existing_family_witness"] = witness
        row["direct_partition_performed"] = False
        large.append(row)
    result = {
        "date": "2026-09-25", "research_baseline": "c1cc625a2ee77d6a85da17dffb427c1ac2024e77",
        "status": "Restricted selected-reference certificate; analytic tail awaits independent review; no new-family or novelty claim.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fixed_relative_speeds": CORE, "window": J, "threshold": D,
        "finite_domain": "1 <= w <= 298, w not in {1,4,5,6,7,11}",
        "finite_cases": len(rows), "positive_lower_bounds": 288,
        "exact_duration_cases": 79, "zero_duration_replacements": [3, 10, 13, 26],
        "tail_start": TAIL_START,
        "tail_uniform_bound_at_299": F(31, 9856)-F(15, 16*299),
        "finite_results": rows, "large_formula_controls": large,
    }
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads(Path(__file__).with_name("sparse_overlap.json").read_text())
        print("PASS: 292 exact local partitions, 288 positive certificates, four equality cases, and three large-speed formula controls.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
