"""Replay the two frozen studies. From the repository root use PYTHONPATH=."""
import argparse
import json
from collections import Counter, defaultdict
from contextlib import nullcontext
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, count
from math import ceil, floor, gcd

from lonely_runner.checker import feasible_intervals
from pair_overlap import blocked_pair_count

MEASURES = ("base", "three_residues", "point_one", "three_or_point", "tree", "exact")
CATEGORIES = ("internal", "crossing", "external")


def distance_units(speed, a, d):
    residue = (speed * a) % d
    return min(residue, d - residue)


def class_size(c, d, n):
    g = gcd(c, d)
    return g * (2 * ((d // g - 1) // n) + 1)


def signed_shell(k, length):
    if k == 0:
        if length == 0:
            yield ()
        return
    for x in range(-length, length + 1):
        for tail in signed_shell(k - 1, length - abs(x)):
            yield (x,) + tail


@lru_cache(None)
def shell_up_to_sign(k, length):
    return [v for v in signed_shell(k, length) if next(x for x in v if x) > 0]


def shortest_relations(v):
    for length in count(2):
        relations = [m for m in shell_up_to_sign(len(v), length)
                     if sum(x*y for x, y in zip(v, m)) == 0]
        if relations:
            return relations


def tree_credit(classes, d, n):
    # Kruskal's algorithm with descending intersection weights.
    edges = [(blocked_pair_count(d, n, a, b), a, b) for a, b in combinations(classes, 2)]
    parent = {c: c for c in classes}

    def root(c):
        while c != parent[c]:
            parent[c] = parent[parent[c]]
            c = parent[c]
        return c

    credit = 0
    for weight, a, b in sorted(edges, reverse=True):
        a, b = root(a), root(b)
        if a != b:
            parent[a] = b
            credit += weight
    return credit


def assess(v, n, d, intervals=None):
    labels = defaultdict(list)
    for speed in v:
        labels[distance_units(speed, 1, d)].append(speed)
    classes = sorted(labels)
    sizes = [class_size(c, d, n) for c in classes]
    raw = d - sum(sizes)
    multiplicity_one = sum(n*c < d for c in classes)
    base = max(0, raw + len(classes) - 1)
    # Every pair sum here is at least 3. The probes 1 and -1 are distinct.
    three = max(0, raw + len(classes) - 1 + 2*max(0, multiplicity_one - 1))
    tree = max(0, raw + tree_credit(classes, d, n))
    safe = [a for a in range(d) if all(n*distance_units(s, a, d) >= d for s in v)]
    if intervals is not None:
        from_intervals = {a for left, right in intervals
                          for a in range(ceil(left*d), min(d-1, floor(right*d)) + 1)}
        assert safe == sorted(from_intervals)
    point_one = multiplicity_one == 0
    assert point_one == (1 in safe)
    assert 0 <= base <= three <= len(safe) and base <= tree <= len(safe)
    if safe:
        assert all(Fraction(distance_units(s, safe[0], d), d) >= Fraction(1, n) for s in v)
    return {"d": d, "classes": dict(labels), "sizes": sizes, "safe": safe,
            "base": base, "three_residues": three, "point_one": point_one,
            "three_or_point": three > 0 or point_one, "tree": tree, "exact": len(safe)}


def audit_pair_counts():
    cases = 0
    for d in range(2, 61):
        for n in (5, 16):
            masks = [sum(1 << a for a in range(d) if n*distance_units(c, a, d) < d)
                     for c in range(d//2 + 1)]
            for a in range(len(masks)):
                for b in range(a, len(masks)):
                    expected = (masks[a] & masks[b]).bit_count()
                    assert blocked_pair_count(d, n, a, b) == expected
                    assert blocked_pair_count(d, n, b, a) == expected
                    cases += 1
    return cases


def controls():
    expected = [
        ((1, 2), 3, 2, 2, [1, 2]),
        ((1, 2, 5, 9), 3, 0, 0, []),
        ((1, 2, 5, 9), 10, 2, 2, [3, 7]),
        ((1, 4, 5, 6, 7, 11, 13), 8, 3, 3, [1, 3, 5, 7]),
        ((1, 4, 5, 6, 7, 11, 13), 24, 0, 0, [3, 9, 15, 21]),
        ((1, 3, 12), 4, 0, 0, []),
        ((1, 3, 12), 13, 0, 2, [6, 7]),
        ((1, 3, 12), 15, 0, 2, [7, 8]),
    ]
    for v, d, lower, improved, safe in expected:
        n = len(v) + 1
        row = assess(v, n, d, feasible_intervals(v, Fraction(1, n)))
        assert (row["base"], row["three_residues"], row["safe"]) == (lower, improved, safe)
    return len(expected)


def analyze(v, relations, intervals, export, stage):
    n = len(v) + 1
    pairs = defaultdict(list)
    for i, j in combinations(range(len(v)), 2):
        pair_labels = []
        for rel in relations:
            occupied = bool(rel[i]) + bool(rel[j])
            pair_labels.append(("external", "crossing", "internal")[occupied])
        pairs[v[i] + v[j]].append({"pair": [v[i], v[j]], "labels_by_relation": pair_labels})

    grid_counts, work = Counter(), Counter()
    won = set()
    example = None
    for d, sources in sorted(pairs.items()):
        row = assess(v, n, d, intervals)
        labels = {tag for p in sources for tag in p["labels_by_relation"]} | {"all"}
        for tag in labels:
            grid_counts[tag, "examined"] += 1
            for measure in MEASURES:
                if row[measure]:
                    grid_counts[tag, measure] += 1
                    won.add((tag, measure))
        num_classes = len(row["classes"])
        work.update({"generating_pairs": len(sources), "grids": 1, "class_sizes": num_classes,
                     "named_residue_locations": 3, "named_class_tests_without_symmetry": 3*num_classes,
                     "pair_sizes": num_classes*(num_classes-1)//2,
                     "full_grid_locations": d, "full_grid_class_tests_without_short_circuit": d*num_classes})
        if example is None and row["exact"]:
            a = row["safe"][0]
            example = {"pair": sources[0]["pair"], "d": d, "a": a,
                       "distances_in_numerator_units": [distance_units(s, a, d) for s in v]}
        if export:
            export.write(json.dumps({"stage": stage, "speeds": v, "relations": relations,
                                     "pairs": sources, **row}, separators=(",", ":")) + "\n")
    return grid_counts, won, work, example


def format_counts(counter, labels):
    return {tag: {m: counter[tag, m] for m in ("examined", *MEASURES)} for tag in labels}


def four_speed_box(export):
    grid_counts, tuple_counts, work, ties, internal_miss_recoveries = (Counter() for _ in range(5))
    for v in combinations(range(1, 16), 4):
        if gcd(*v) != 1:
            continue
        relations = shortest_relations(v)
        ties[len(relations)] += 1
        intervals = feasible_intervals(v, Fraction(1, 5))
        grids, won, cost, _ = analyze(v, relations, intervals, export, "four-speed")
        grid_counts.update(grids)
        tuple_counts.update(won)
        for tag in ("all", *CATEGORIES):
            if grids[tag, "examined"]:
                tuple_counts[tag, "examined"] += 1
        if ("internal", "exact") not in won:
            internal_miss_recoveries.update(won)
        work.update(cost)
    return {"tuples": format_counts(tuple_counts, ("all", *CATEGORIES)),
            "grids": format_counts(grid_counts, ("all", *CATEGORIES)), "cost": work,
            "number_of_tied_minimizers_up_to_sign": dict(sorted(ties.items())),
            "among_internal_exact_failures": {tag: {m: internal_miss_recoveries[tag, m] for m in MEASURES}
                                             for tag in ("all", *CATEGORIES)}}


def sixteen_runner_panel(export):
    panel = []
    shapes = {"j^2": lambda j: j*j, "j^2+3j": lambda j: j*j+3*j, "j^3": lambda j: j**3}
    for name, f in shapes.items():
        for shift in (1, 5):
            v = tuple(f(j) + shift for j in range(1, 16))
            intervals = feasible_intervals(v, Fraction(1, 16))
            grids, _, work, witness = analyze(v, [], intervals, export, "sixteen-runner")
            panel.append({"shape": name, "shift": shift, "speeds": v,
                          "grids": format_counts(grids, ("all",))["all"], "cost": work,
                          "physical_witness": witness})
    return panel


def supplementary_controls():
    for v, expected_safe, expected_triple in [
        ((1, 3, 8, 13), [7, 9], 1),
        ((1, 7, 8, 15), [], 3),
    ]:
        row = assess(v, 5, 16)
        sets = [{a for a in range(16) if 5*distance_units(c, a, 16) < 16}
                for c in sorted(row["classes"])]
        assert row["sizes"] == [7, 7, 8]
        assert [len(a & b) for a, b in combinations(sets, 2)] == [3, 3, 3]
        assert len(set.intersection(*sets)) == expected_triple and row["safe"] == expected_safe
    for q in range(1, 33):
        v = (1, 2, 4, 30*q)
        for a, b in combinations(v, 2):
            d = a + b
            result = assess(v, 5, d)
            assert result["three_residues"] == 0
            if b == 30*q:
                witness = (3*d + 9) // 10
                assert witness in result["safe"]
            else:
                assert result["safe"] == []
    return {"paired_grid_controls": 2, "sparse_counting_family_controls": 32}


def dyadic_witness(r):
    """One time for all nonnegative dyadic exponents and the added speed r."""
    if r % 3:
        return Fraction(1, 3), 0
    scale, j = 1, 0
    while r > 12 * scale:
        scale *= 4
        j += 1
    return Fraction(1, 3) + Fraction(1, 15 * scale), 2*j


def audit_dyadic():
    cases = set(range(1, 4097))
    for j in (10, 50, 100):
        for delta in (-3, -1, 0, 1, 3):
            cases.add(12 * 4**j + delta)
    for r in sorted(cases):
        t, switch = dyadic_witness(r)
        p, q = t.numerator, t.denominator
        assert 5*distance_units(r, p, q) >= q
        # The first full cycle beyond the switch also checks its return phase.
        for i in range(switch + 5):
            assert 5*distance_units(2**i, p, q) >= q
        if r % 3 == 0:
            assert (2**switch*t) % 1 == Fraction(2, 5)
        else:
            assert t == Fraction(1, 3)
    for r in (3, 6, 9, 12, 15, 18, 21, 24, 27, 30):
        m = (5*r - 1).bit_length()
        speeds = sorted({r} | {2**i for i in range(m + 1)})
        grids = {a + b for a, b in combinations(speeds, 2)}
        best = max(Fraction(max(min(distance_units(v, a, d) for v in speeds)
                                for a in range(d)), d) for d in grids)
        assert best == Fraction(1, 5)
    return {"added_speeds": len(cases), "finite_prefix_exact_maximum_controls": 10}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", help="write all per-grid records, including every unreduced safe numerator, as JSONL")
    args = parser.parse_args()
    with (open(args.rows, "w", encoding="utf-8") if args.rows else nullcontext()) as export:
        summary = {"handoff_controls": controls(), "pair_size_audit_unordered_cases": audit_pair_counts(),
                   "four_speed_box": four_speed_box(export), "sixteen_runner_panel": sixteen_runner_panel(export),
                   "exploratory_grid_controls": supplementary_controls(),
                   "exploratory_dyadic_controls": audit_dyadic()}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

