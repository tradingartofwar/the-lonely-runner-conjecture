"""Select local pairs/trees on the eleven existing core decompositions.

Run: python -m scripts.analyze_pair_selection
No new speed sets. Hunter's tree inequality is known (S13, Lemma 13).
Finite diagnostics and the local gap interpretation await independent review.
"""

import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_blocking_overlaps import blocking_intervals
from scripts.analyze_core_transfer import boundary_certificate, merged
from scripts.analyze_local_overlap import duration, measure
from scripts.analyze_two_variable_speeds import phase_certificate

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "13a939e7cf0a25afa0590a5251e423aa5a36c1cc"
D = Q(1, 8)


def components(vertices, edges):
    """Number of connected components, including isolated active vertices."""
    remaining = set(vertices)
    count = 0
    while remaining:
        reached = {min(remaining)}
        while True:
            expanded = reached | {v for e in edges if any(w in reached for w in e) for v in e}
            expanded &= remaining
            if expanded == reached:
                break
            reached = expanded
        remaining -= reached
        count += 1
    return count


def all_trees(vertices):
    edges = tuple(combinations(sorted(vertices), 2))
    result = tuple(es for es in combinations(edges, 3) if components(vertices, es) == 1)
    assert len(result) == 16
    # Complete finite graph check, independent of any speeds or durations.
    for tree in result:
        for size in range(5):
            for active in combinations(vertices, size):
                induced = tuple(e for e in tree if all(v in active for v in e))
                assert len(induced) <= max(size - 1, 0)
                assert max(size - 1, 0) - len(induced) == max(components(active, induced) - 1, 0)
    return result


def kruskal(vertices, weights):
    """Independent maximum spanning tree check, with deterministic ties."""
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v

    chosen = []
    for edge in sorted(weights, key=lambda e: (-weights[e], e)):
        a, b = map(find, edge)
        if a != b:
            parent[a] = b
            chosen.append(edge)
    assert len(chosen) == 3
    return tuple(sorted(chosen))


def status_durations(extra, interval):
    left, right = interval
    cuts = sorted({left, right, *(x for v in extra for ab in blocking_intervals(v)
                                 for x in ab if left < x < right)})
    result = {}
    for a, b in zip(cuts, cuts[1:]):
        active = tuple(v for v in sorted(extra) if circular_distance(v * (a + b) / 2) < D)
        result[active] = result.get(active, Q(0)) + b - a
    assert sum(result.values(), Q(0)) == right - left
    return result


def analyze_opening(core, extra, interval, trees, contacts):
    accounting = measure(extra, (interval,))
    E = accounting["excess_over_local_average_E"]
    R = accounting["redundant_blocking_R"]
    U = accounting["clear_duration_U"]
    weights = {tuple(x["speeds"]): x["overlap_duration"] for x in accounting["pair_overlaps"]}
    best = max(weights.values())
    scores = {tree: sum((weights[e] for e in tree), Q(0)) for tree in trees}
    tree_weight = max(scores.values())
    chosen = kruskal(extra, weights)
    assert scores[chosen] == tree_weight
    assert best <= tree_weight <= R
    active_durations = status_durations(extra, interval)
    assert active_durations.get((), Q(0)) == U
    gap_rows = []
    for active, width in sorted(active_durations.items()):
        induced = tuple(e for e in chosen if all(v in active for v in e))
        missing = max(components(active, induced) - 1, 0)
        if missing:
            gap_rows.append({"active_blockers": active, "duration": width,
                             "uncounted_copies": missing, "gap_contribution": missing * width})
    gap = sum((x["gap_contribution"] for x in gap_rows), Q(0))
    assert gap == R - tree_weight
    for edge, weight in weights.items():
        assert weight == sum((width for active, width in active_durations.items()
                              if all(v in active for v in edge)), Q(0))
    for tree, weight in scores.items():
        # Check every tree against the status partition, not just the winner.
        missing = sum((max(components(active, tuple(e for e in tree if all(v in active for v in e))) - 1, 0) * width
                       for active, width in active_durations.items()), Q(0))
        assert weight + missing == R
    allowed = accounting["allowed_intervals"]
    row = {"interval": interval, "E": E, "R": R, "U": U,
        "individual_blocking": accounting["individual_blocking"],
        "pair_overlaps": accounting["pair_overlaps"],
        "individual_only_bound": -E,
        "original_pair": tuple(sorted(extra[:2])),
        "original_pair_bound": weights[tuple(sorted(extra[:2]))] - E,
        "best_pairs": [e for e, w in weights.items() if w == best],
        "best_pair_bound": best - E,
        "chosen_maximum_tree": chosen,
        "maximum_tree_ties": sum(w == tree_weight for w in scores.values()),
        "tree_weight": tree_weight, "tree_bound": tree_weight - E,
        "tree_gap": gap, "tree_gap_contributions": gap_rows,
        "allowed_set": allowed,
        "isolated_contacts": [x for x in contacts if interval[0] <= x["time"] <= interval[1]],
        "status": "positive_duration" if U > 0 else "isolated_only" if allowed else "empty"}
    if U > 0:
        witness_interval = max(allowed, key=lambda ab: ab[1] - ab[0])
        row["positive_interval_certificate"] = phase_certificate(tuple(sorted((*core, *extra))), witness_interval)
    return row


def main():
    source = json.loads((ROOT / "experiments/core_transfer.json").read_text())
    cases = []
    for previous in source["cases"]:
        core, extra = tuple(previous["core"]), tuple(previous["extra"])
        region = feasible_intervals(core, D)
        assert region == tuple(tuple(map(Q, ab)) for ab in previous["core_allowed"])
        full = boundary_certificate(tuple(sorted((*core, *extra))))
        assert full["complete_allowed_set"] == tuple(tuple(map(Q, ab)) for ab in previous["boundary_certificate"]["complete_allowed_set"])
        trees = all_trees(extra)
        rows = [analyze_opening(core, extra, ab, trees, full["isolated_contact_certificates"]) for ab in region]
        for key in ("E", "R", "U"):
            assert sum((x[key] for x in rows), Q(0)) == Q(previous[key])
        assert merged([ab for x in rows for ab in x["allowed_set"]]) == full["complete_allowed_set"]
        # Common-start integer speeds imply exact reflection symmetry t -> 1-t.
        for row, reflection in zip(rows, reversed(rows)):
            assert row["interval"] == (1 - reflection["interval"][1], 1 - reflection["interval"][0])
            for key in ("E", "R", "U", "pair_overlaps", "best_pairs", "chosen_maximum_tree", "tree_bound"):
                assert row[key] == reflection[key]
        cases.append({"label": previous["label"], "core": core, "extra": extra,
            "components": rows, "summary": {"core_components": len(rows),
                "positive_duration": sum(x["U"] > 0 for x in rows),
                "individual_only_certifies": sum(x["individual_only_bound"] > 0 for x in rows),
                "original_pair_certifies": sum(x["original_pair_bound"] > 0 for x in rows),
                "best_pair_certifies": sum(x["best_pair_bound"] > 0 for x in rows),
                "tree_certifies": sum(x["tree_bound"] > 0 for x in rows),
                "isolated_only": sum(x["status"] == "isolated_only" for x in rows),
                "empty": sum(x["status"] == "empty" for x in rows)}})
    rows = [x for case in cases for x in case["components"]]
    counts = {"decompositions": len(cases),
        "distinct_full_speed_sets": len({tuple(sorted((*c["core"], *c["extra"]))) for c in cases}),
        "components": len(rows), "positive_width_core_components": sum(x["interval"][0] < x["interval"][1] for x in rows),
        "positive_duration": sum(x["U"] > 0 for x in rows),
        "individual_only_certifies": sum(x["individual_only_bound"] > 0 for x in rows),
        "original_pair_certifies": sum(x["original_pair_bound"] > 0 for x in rows),
        "best_pair_certifies": sum(x["best_pair_bound"] > 0 for x in rows),
        "tree_certifies": sum(x["tree_bound"] > 0 for x in rows),
        "isolated_only": sum(x["status"] == "isolated_only" for x in rows),
        "empty": sum(x["status"] == "empty" for x in rows),
        "isolated_contact_certificates": sum(len(x["isolated_contacts"]) for x in rows),
        "pair_interval_crosschecks": 6 * len(rows),
        "tree_partition_checks": 16 * len(rows),
        "maximum_tree_algorithm_comparisons": len(rows),
        "complete_boundary_reconstructions": len(cases),
        "positive_interval_certificates": sum("positive_interval_certificate" in x for x in rows),
        "positive_components_with_exact_tree_bound": sum(x["U"] > 0 and x["tree_gap"] == 0 for x in rows)}
    assert counts["components"] == 72 and counts["positive_width_core_components"] == 62
    assert counts["positive_duration"] == counts["tree_certifies"] == 38
    assert counts["original_pair_certifies"] == 22 and counts["best_pair_certifies"] == 32
    assert counts["isolated_only"] == counts["isolated_contact_certificates"] == 18
    assert counts["empty"] == 16
    paths = ("scripts/analyze_pair_selection.py", "experiments/core_transfer.json", "scripts/analyze_core_transfer.py",
             "scripts/analyze_local_overlap.py", "scripts/analyze_blocking_overlaps.py",
             "scripts/analyze_phase_discrepancy.py", "scripts/analyze_overlap_placement.py",
             "scripts/analyze_two_variable_speeds.py", "lonely_runner/checker.py")
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
        "scope": "Existing eleven decompositions only, ten distinct speed sets, selected reference 0, n=8, delta=1/8, common start, distinct positive integer relative speeds.",
        "claim_status": {"tree_inequality": "KNOWN: Hunter, as stated in S13 Lemma 13; restrict time measure to J.",
                         "finite_results": "OBSERVED: exact rational computations; not independently reviewed.",
                         "local_gap_interpretation": "HYPOTHESIS: AI-written elementary derivation pending independent review.",
                         "universal_tree_or_contact_selection": "OPEN; not asserted."},
        "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
        "verification_counts": counts, "cases": cases,
        "limitations": "No new speed-set scan, universal existence claim, independent mathematical review, or novelty claim. Tree selection is fixed over each entire core component; it does not change on each status cell. Durations cannot certify isolated times."}
    (ROOT / "experiments/pair_selection.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"counts": counts, "cases": [{"label": c["label"], **c["summary"]} for c in cases]}, indent=2))


if __name__ == "__main__":
    main()
