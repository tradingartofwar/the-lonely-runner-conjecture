"""Exact local overlap accounting and a structured four-blocker bound.

Run: python -m scripts.analyze_local_overlap
Eight prescribed cases; no speed-set scan. See notes/LOCAL_OVERLAP.md.
"""

import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_blocking_overlaps import blocking_intervals
from scripts.analyze_two_variable_speeds import phase_certificate


ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "d15a56a7818e229a0118041e2f28ae4298379608"
CORE = (1, 4, 5)
DELTA = Q(1, 8)
J = (Q(9, 32), Q(3, 8))
CASES = (
    ("tight_11_13", (6, 7, 11, 13)),
    ("replace_13_with_8", (6, 7, 8, 11)),
    ("cooperative_16_23", (6, 7, 16, 23)),
    ("fast_eighths", (40, 48, 56, 64)),
    ("doubled_below_uniform_cutoff", (52, 104, 56, 64)),
    ("doubled_at_uniform_cutoff", (53, 106, 56, 64)),
    ("doubled_eighths", (56, 112, 64, 72)),
    ("perturbed_double", (56, 113, 64, 72)),
)


def intersect(left, right):
    """Intersect sorted disjoint interval lists; retain equality points."""
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        a, b = left[i]
        c, d = right[j]
        if max(a, c) <= min(b, d):
            result.append((max(a, c), min(b, d)))
        if b < d:
            i += 1
        else:
            j += 1
    return tuple(result)


def duration(intervals):
    return sum((b - a for a, b in intervals), Q(0))


def measure(blockers, region):
    """Complete constant-status partition, crosschecked by interval operations.

    Numerical endpoint pairs for bad intervals are used only for durations;
    strict predicates and the closed feasibility checker handle endpoints.
    """
    assert len(set(blockers)) == 4
    windows = {v: blocking_intervals(v) for v in blockers}
    cuts = sorted({Q(0), Q(1), *(p for interval in region for p in interval),
                   *(p for intervals in windows.values() for interval in intervals for p in interval)})
    histogram = [Q(0)] * 5
    individual = {v: Q(0) for v in blockers}
    pair_counts = {pair: Q(0) for pair in combinations(sorted(blockers), 2)}
    cells = 0
    for a, b in zip(cuts, cuts[1:]):
        t = (a + b) / 2
        if not any(c <= t <= d for c, d in region):
            continue
        cells += 1
        active = sorted(v for v in blockers if circular_distance(v * t) < DELTA)
        histogram[len(active)] += b - a
        for v in active:
            individual[v] += b - a
        for pair in combinations(active, 2):
            pair_counts[pair] += b - a

    length = duration(region)
    total = sum(individual.values(), Q(0))
    redundancy = sum(max(m - 1, 0) * width for m, width in enumerate(histogram))
    excess = total - length  # Four individual cycle fractions sum to one.
    clear = histogram[0]
    assert sum(histogram) == length
    assert total == sum(m * width for m, width in enumerate(histogram))
    assert clear == redundancy - excess
    group_allowed = intersect(feasible_intervals(blockers, DELTA), region)
    assert clear == duration(group_allowed)

    # Independent of the cell-count construction: intersect actual intervals.
    clipped_bad = {v: intersect(windows[v], region) for v in blockers}
    for v in blockers:
        assert individual[v] == duration(clipped_bad[v])
    pairs = []
    for a, b in combinations(sorted(blockers), 2):
        overlap = duration(intersect(clipped_bad[a], clipped_bad[b]))
        assert pair_counts[(a, b)] == overlap
        assert redundancy >= overlap
        pairs.append({"speeds": [a, b], "overlap_duration": overlap})

    return {"region": region, "length": length,
            "individual_blocking": {str(v): value for v, value in individual.items()},
            "total_individual_blocking_T": total, "excess_over_local_average_E": excess,
            "redundant_blocking_R": redundancy, "clear_duration_U": clear,
            "histogram": {str(m): width for m, width in enumerate(histogram)},
            "pair_overlaps": pairs, "allowed_intervals": group_allowed,
            "complete_partition_cells": cells}


def pair_overlap(summary, pair):
    ordered = sorted(pair)
    return next(row["overlap_duration"] for row in summary["pair_overlaps"]
                if row["speeds"] == ordered)


def analyze_case(label, blockers, core_allowed):
    assert len(set((*CORE, *blockers))) == 7
    global_summary = measure(blockers, ((Q(0), Q(1)),))
    inside = measure(blockers, core_allowed)
    per_opening = [measure(blockers, (interval,)) for interval in core_allowed]
    assert global_summary["total_individual_blocking_T"] == 1
    assert global_summary["clear_duration_U"] == global_summary["redundant_blocking_R"]
    assert all(value == Q(1, 4) for value in global_summary["individual_blocking"].values())
    assert global_summary["redundant_blocking_R"] >= Q(3, 4 * max(blockers))
    for key in ("total_individual_blocking_T", "redundant_blocking_R", "clear_duration_U"):
        assert inside[key] == sum((row[key] for row in per_opening), Q(0))
    all_allowed = feasible_intervals((*CORE, *blockers), DELTA)
    assert all_allowed == inside["allowed_intervals"]
    assert duration(all_allowed) == inside["clear_duration_U"]
    return {"label": label, "four_blockers": blockers, "global": global_summary,
            "inside_fixed_runner_openings": inside, "per_opening": per_opening,
            "redundancy_outside_openings": global_summary["redundant_blocking_R"] - inside["redundant_blocking_R"],
            "all_seven_allowed_intervals": all_allowed}


def main():
    core_allowed = feasible_intervals(CORE, DELTA)
    assert J in core_allowed
    assert len(core_allowed) == 6 and duration(core_allowed) == Q(3, 8)
    core_phases = phase_certificate(CORE, J)
    cases = [analyze_case(label, blockers, core_allowed) for label, blockers in CASES]
    lookup = {row["label"]: row for row in cases}
    tight = lookup["tight_11_13"]["inside_fixed_runner_openings"]
    loose = lookup["replace_13_with_8"]["inside_fixed_runner_openings"]
    assert tight["redundant_blocking_R"] == tight["excess_over_local_average_E"] == Q(34079, 240240)
    assert tight["clear_duration_U"] == 0
    assert tight["allowed_intervals"] == tuple((Q(k, 8), Q(k, 8)) for k in (1, 3, 5, 7))
    assert loose["redundant_blocking_R"] == Q(271, 2310) < tight["redundant_blocking_R"]
    assert loose["clear_duration_U"] == Q(29, 1232) > 0

    # Unit-phase proof of B_q(1/8) intersect B_2q(1/8) = B_q(1/16).
    # These boundaries give the COMPLETE predicate partition; endpoints are checked.
    cuts = sorted({Q(0), Q(1), Q(1, 16), Q(15, 16),
                   *(p for v in (1, 2) for interval in blocking_intervals(v) for p in interval)})
    points = [*cuts, *((a + b) / 2 for a, b in zip(cuts, cuts[1:]))]
    for s in points:
        both = circular_distance(s) < DELTA and circular_distance(2 * s) < DELTA
        assert both == (circular_distance(s) < DELTA / 2)
    overlap_density = duration(intersect(blocking_intervals(1), blocking_intervals(2)))
    union_density = 1 - duration(feasible_intervals((1, 2), DELTA))
    assert overlap_density == Q(1, 8) and union_density == Q(3, 8)

    length = J[1] - J[0]
    assert length == Q(3, 32)
    uniform_cutoff = 53
    assert length / 8 - Q(39, 64 * 52) == 0
    assert length / 8 - Q(39, 64 * uniform_cutoff) == Q(3, 13568) > 0
    family_checks = []
    for label in ("doubled_below_uniform_cutoff", "doubled_at_uniform_cutoff", "doubled_eighths"):
        case = lookup[label]
        q, double, u, v = case["four_blockers"]
        assert double == 2 * q and min(u, v) >= q
        row = next(row for row in case["per_opening"] if row["region"] == (J,))
        local_pair_overlap = pair_overlap(row, (q, double))
        local_pair_union = (row["individual_blocking"][str(q)] +
                            row["individual_blocking"][str(double)] - local_pair_overlap)
        pair_union_upper = Q(3, 8) * length + Q(15, 64 * q)
        assert local_pair_union <= pair_union_upper
        refined = length / 8 - Q(15, 64 * q) - Q(3, 16 * u) - Q(3, 16 * v)
        uniform = length / 8 - Q(39, 64 * q)
        assert row["clear_duration_U"] >= refined >= uniform
        t = Q(6, 17)  # A simple witness for these three prescribed diagnostics.
        assert any(a <= t <= b for a, b in row["allowed_intervals"])
        distances = {str(s): circular_distance(s * t) for s in (*CORE, q, double, u, v)}
        assert min(distances.values()) >= DELTA
        family_checks.append({"label": label, "q": q, "u": u, "v": v,
                              "pair_union_duration_in_J": local_pair_union,
                              "pair_union_upper_bound": pair_union_upper,
                              "refined_clear_lower_bound": refined, "uniform_clear_lower_bound": uniform,
                              "actual_clear_duration_in_J": row["clear_duration_U"],
                              "witness": {"time": t, "distances": distances,
                                          "minimum": min(distances.values())}})

    original_J = next(row for row in lookup["doubled_eighths"]["per_opening"] if row["region"] == (J,))
    changed_J = next(row for row in lookup["perturbed_double"]["per_opening"] if row["region"] == (J,))
    original_pair = pair_overlap(original_J, (56, 112))
    changed_pair = pair_overlap(changed_J, (56, 113))
    assert original_pair == Q(11, 896) > changed_pair == Q(9, 3616)
    assert original_J["clear_duration_U"] == Q(53, 1792)
    assert changed_J["clear_duration_U"] == Q(6193, 260352) > 0
    assert circular_distance(113 * Q(6, 17)) == Q(2, 17) < DELTA

    data = {
        "date": "2026-09-24", "base_commit": BASE_COMMIT,
        "checker_sha256": hashlib.sha256((ROOT / "lonely_runner/checker.py").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "Exact local measurements and a structured-family proof candidate; independent review outstanding; no novelty claim",
        "scope": {"n": 8, "selected_reference": 0, "threshold": DELTA,
                  "fixed_relative_speeds": CORE, "starts": "all together",
                  "prescribed_cases": len(cases)},
        "fixed_runner_allowed_set": core_allowed, "fixed_runner_allowed_duration": duration(core_allowed),
        "local_identity": "U = length - total individual blocking + redundant blocking = R-E for four blockers",
        "cases": cases,
        "structured_family": {"speeds": "0,1,4,5,q,2q,u,v, all distinct",
                              "conditions": "positive integers q>=53, u>=q, v>=q",
                              "interval_J": J, "length_J": length, "core_phase_certificate": core_phases,
                              "doubled_pair_overlap_density": overlap_density,
                              "doubled_pair_union_density": union_density,
                              "uniform_clear_lower_bound": "(3q-156)/(256q)",
                              "refined_clear_lower_bound": "3/256-15/(64q)-3/(16u)-3/(16v)",
                              "finite_diagnostic_checks": family_checks},
        "perturbed_pair_control": {"original": [56, 112], "changed": [56, 113],
                                   "original_local_overlap": original_pair, "changed_local_overlap": changed_pair,
                                   "original_clear_J": original_J["clear_duration_U"],
                                   "changed_clear_J": changed_J["clear_duration_U"],
                                   "old_witness_time": Q(6, 17), "changed_speed_distance_at_old_witness": Q(2, 17)},
        "verification_counts": {"measured_regions": len(cases) * 8,
                                "pair_duration_crosschecks": len(cases) * 8 * 6},
        "limitations": "Accounting identity alone proves no new existence statement. Durations do not resolve isolated endpoints. Structured family uses exact doubling, not arbitrary four-speed inputs; selected reference only.",
    }
    (ROOT / "experiments/local_overlap.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"inside_openings": [{"label": row["label"], **{key: row["inside_fixed_runner_openings"][key]
                      for key in ("redundant_blocking_R", "excess_over_local_average_E", "clear_duration_U")}}
                      for row in cases], "family_checks": family_checks,
                      "verification_counts": data["verification_counts"]}, indent=2, default=str))


if __name__ == "__main__":
    main()
