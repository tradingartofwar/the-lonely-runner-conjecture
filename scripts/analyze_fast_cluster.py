"""Construct witnesses for a fixed core and four speeds with a common offset.

Run: python -m scripts.analyze_fast_cluster
Five prescribed family profiles, four q checks each, nine nearby controls,
three frozen-phase controls, and the original tight q=6 control. No scan.
The general argument is a proof candidate; see notes/FAST_CLUSTER.md.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_core_transfer import boundary_certificate, merged
from scripts.analyze_local_overlap import duration, intersect, measure
from scripts.analyze_pair_selection import all_trees, kruskal
from scripts.analyze_two_variable_speeds import phase_certificate

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "b46243f905784d3016db8b4925775898a290e257"
D = Q(1, 8)


def floor(x):
    return x.numerator // x.denominator


def frozen_phase(offsets, t):
    """Allowed common rotations x; this is auxiliary, not a new start phase."""
    region = ((Q(0), Q(1)),)
    for a in offsets:
        phase = a * t % 1
        windows = []
        for m in range(-1, 3):
            left, right = max(Q(0), m + D - phase), min(Q(1), m + 1 - D - phase)
            if left <= right:
                windows.append((left, right))
        region = intersect(region, windows)
    # Separately reconstruct open cells and every boundary.
    cuts = sorted({Q(0), Q(1), *((sign * D - a * t) % 1 for a in offsets for sign in (-1, 1))})
    cells = [(a, b) for a, b in zip(cuts, cuts[1:])
             if all(circular_distance((a + b) / 2 + v * t) >= D for v in offsets)]
    points = [(x, x) for x in cuts if all(circular_distance(x + v * t) >= D for v in offsets)]
    assert merged([*cells, *points]) == region
    positions = sorted(a * t % 1 for a in offsets)
    gaps = [b - a for a, b in zip(positions, positions[1:])] + [1 + positions[0] - positions[-1]]
    assert sum(gaps) == 1
    clear = sum((max(Q(0), gap - 2 * D) for gap in gaps), Q(0))
    assert clear == duration(region)
    tiled = all(gap == Q(1, 4) for gap in gaps)
    assert (clear == 0) == tiled
    if tiled:
        assert all((4 * (a - offsets[0]) * t).denominator == 1 for a in offsets)
    return {"offsets": offsets, "slow_time": t, "offset_positions": positions,
            "cyclic_gaps": gaps, "allowed_common_phases": region,
            "clear_phase_duration": clear, "exact_quarter_tiling": tiled}


def family_profile(core, offsets):
    assert len(core) == len(set(core)) == 3 and min(core) > 0
    assert tuple(sorted(set(offsets))) == tuple(offsets) and len(offsets) == 4 and offsets[0] == 0
    allowed = feasible_intervals(core, D)
    assert duration(allowed) >= Q(1, 4)
    left, right = max(allowed, key=lambda ab: ab[1] - ab[0])
    assert left < right
    t0 = (left + right) / 2
    d = offsets[1]
    if (4 * d * t0).denominator == 1:
        t0 -= min((right - left) / 4, Q(1, 8 * d))
    assert left < t0 < right and (4 * d * t0).denominator != 1
    phase = frozen_phase(offsets, t0)
    a, b = max(phase["allowed_common_phases"], key=lambda ab: ab[1] - ab[0])
    assert a < b
    x0 = (a + b) / 2
    core_margin = min(circular_distance(v * t0) - D for v in core)
    offset_margin = min(circular_distance(x0 + a * t0) - D for a in offsets)
    assert core_margin > 0 and offset_margin > 0
    bounds = {"distinctness": Q(max(core)), "core_drift": Q(max(core), 2) / core_margin,
              "internal_drift": Q(max(offsets), 2) / offset_margin,
              "stay_inside_core_component": 1 / (2 * min(t0 - left, right - t0))}
    strict_bound = max(bounds.values())
    return {"core": core, "offsets": offsets, "core_component": (left, right),
            "slow_time_t0": t0, "chosen_phase_x0": x0,
            "core_margin": core_margin, "offset_margin": offset_margin,
            "phase_geometry": phase, "strict_q_bounds": bounds,
            "strict_q_bound": strict_bound, "sufficient_integer_q": floor(strict_bound) + 1}


def witness(profile, q):
    core, offsets = profile["core"], profile["offsets"]
    speeds = tuple(sorted((*core, *(q + a for a in offsets))))
    assert len(speeds) == len(set(speeds)) == 7 and min(speeds) > 0
    t0, x0 = profile["slow_time_t0"], profile["chosen_phase_x0"]
    integer = floor(q * t0 - x0 + Q(1, 2))
    t = (integer + x0) / q
    assert abs(t - t0) <= Q(1, 2 * q)
    assert q * t % 1 == x0
    core_lower = D + profile["core_margin"] - Q(max(core), 2 * q)
    fast_lower = D + profile["offset_margin"] - Q(max(offsets), 2 * q)
    distances = {v: circular_distance(v * t) for v in speeds}
    assert all(distances[v] >= core_lower for v in core)
    assert all(distances[q + a] >= fast_lower for a in offsets)
    minimum = min(distances.values())
    guaranteed = q >= profile["sufficient_integer_q"]
    if guaranteed:
        assert min(core_lower, fast_lower) > D
        assert profile["core_component"][0] < t < profile["core_component"][1]
        assert minimum > D
    complete = feasible_intervals(speeds, D)
    reconstruction = boundary_certificate(speeds)
    assert complete == reconstruction["complete_allowed_set"]
    row = {"q": q, "covered_by_uniform_argument": guaranteed,
           "full_relative_speeds": speeds, "rounded_integer": integer,
           "witness_time": t, "time_adjustment": t - t0,
           "core_distance_lower_bound": core_lower, "fast_distance_lower_bound": fast_lower,
           "distances": distances, "minimum_distance": minimum,
           "complete_allowed_set": complete, "clear_duration": duration(complete),
           "isolated_contacts": reconstruction["isolated_contact_certificates"]}
    if minimum > D:
        radius = (minimum - D) / (2 * max(speeds))
        interval = (t - radius, t + radius)
        assert 0 < interval[0] < interval[1] < 1
        assert intersect(complete, (interval,)) == (interval,)
        row["certified_interval"] = interval
        row["affine_certificate"] = phase_certificate(speeds, interval)
    return row


def nearby_case(core, extra):
    allowed = feasible_intervals(core, D)
    trees = all_trees(extra)
    rows = []
    for ab in allowed:
        m = measure(extra, (ab,))
        weights = {tuple(p["speeds"]): p["overlap_duration"] for p in m["pair_overlaps"]}
        chosen = kruskal(extra, weights)
        tree_weight = sum(weights[e] for e in chosen)
        assert tree_weight == max(sum(weights[e] for e in tree) for tree in trees)
        E, R, U = m["excess_over_local_average_E"], m["redundant_blocking_R"], m["clear_duration_U"]
        assert max(weights.values()) <= tree_weight <= R
        rows.append({"interval": ab, "E": E, "R": R, "U": U,
                     "best_pair_bound": max(weights.values()) - E,
                     "tree_bound": tree_weight - E, "chosen_tree": chosen,
                     "pair_overlaps": m["pair_overlaps"], "allowed_set": m["allowed_intervals"]})
    full = boundary_certificate(tuple(sorted((*core, *extra))))
    assert merged([ab for row in rows for ab in row["allowed_set"]]) == full["complete_allowed_set"]
    return {"core": core, "extra": extra, "components": rows, "boundary_certificate": full}


def main():
    prescribed = (((1, 4, 5), (0, 1, 5, 7)), ((1, 4, 8), (0, 1, 5, 7)),
                  ((2, 3, 5), (0, 1, 5, 7)), ((1, 2, 4), (0, 2, 3, 5)),
                  ((1, 3, 5), (0, 1, 2, 3)))
    profiles = []
    for core, offsets in prescribed:
        profile = family_profile(core, offsets)
        cutoff = profile["sufficient_integer_q"]
        profile["witness_checks"] = [witness(profile, q) for q in (cutoff - 1, cutoff, cutoff + 1, 2 * cutoff)]
        profiles.append(profile)
    nearby = [nearby_case(core, (6, 7, 11, speed)) for core in ((1, 4, 8), (2, 3, 5)) for speed in (12, 13, 14)]
    nearby += [nearby_case((1, 2, 4), (3, 5, 6, speed)) for speed in (7, 8, 9)]
    original, changed = nearby[1]["components"][0], nearby[0]["components"][0]
    assert original["allowed_set"] == changed["allowed_set"] == ((Q(17, 88), Q(7, 32)),)
    assert original["U"] == changed["U"] == Q(9, 352)
    assert original["best_pair_bound"] < 0 and changed["best_pair_bound"] < 0
    packing = [frozen_phase((0, 1, 2, 3), Q(1, 4)),
               frozen_phase((0, 1, 2, 3), Q(13, 50)),
               frozen_phase((0, 1, 5, 7), Q(1, 4))]
    assert packing[0]["allowed_common_phases"] == tuple((Q(i, 8), Q(i, 8)) for i in (1, 3, 5, 7))
    assert packing[1]["clear_phase_duration"] > 0 and packing[2]["clear_phase_duration"] > 0
    tight = witness(profiles[0], 6)
    assert tight["minimum_distance"] == Q(1, 256) < D
    assert tight["clear_duration"] == 0
    assert tight["complete_allowed_set"] == packing[0]["allowed_common_phases"]
    assert profiles[0]["slow_time_t0"] == Q(21, 64) and profiles[0]["chosen_phase_x0"] == Q(23, 128)
    assert profiles[0]["sufficient_integer_q"] == 65
    assert profiles[0]["witness_checks"][1]["witness_time"] == Q(2711, 8320)
    assert profiles[0]["witness_checks"][1]["minimum_distance"] == Q(23, 128)
    counts = {"family_profiles": len(profiles), "rounded_witness_checks": 4 * len(profiles),
              "witness_checks_inside_uniform_range": 3 * len(profiles), "below_cutoff_checks": len(profiles),
              "affine_interval_certificates": sum("affine_certificate" in w for p in profiles for w in p["witness_checks"]),
              "nearby_decompositions": len(nearby), "nearby_components": sum(len(c["components"]) for c in nearby),
              "nearby_pair_duration_checks": 6 * sum(len(c["components"]) for c in nearby),
              "complete_boundary_reconstructions": 4 * len(profiles) + len(nearby) + 1,
              "frozen_phase_reconstructions": len(profiles) + len(packing),
              "explicit_quarter_tiling_controls": len(packing), "tight_small_q_control": 1}
    paths = ("scripts/analyze_fast_cluster.py", "scripts/analyze_pair_selection.py", "scripts/analyze_core_transfer.py",
             "scripts/analyze_local_overlap.py", "scripts/analyze_blocking_overlaps.py", "scripts/analyze_phase_discrepancy.py",
             "scripts/analyze_overlap_placement.py", "scripts/analyze_two_variable_speeds.py", "lonely_runner/checker.py")
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
            "scope": "n=8, selected reference 0, common start, three fixed distinct positive integer core speeds, four speeds q+a_i with distinct fixed nonnegative integer offsets and min offset 0.",
            "claim_status": {"family_argument": "HYPOTHESIS: complete AI-generated proof candidate, independent review outstanding; no novelty claim.",
                             "finite_controls": "OBSERVED; exact rational computations.",
                             "particular_sum_relation_is_necessary": "DISPROVEN for the recorded local tree-only opening.",
                             "arbitrary_seven_speeds": "OPEN in this investigation; not settled by this family."},
            "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "profiles": profiles, "nearby_controls": nearby, "packing_controls": packing,
            "tight_small_q_control": tight, "verification_counts": counts,
            "limitations": "Offsets and core stay fixed as q grows. No sharp cutoff claim, arbitrary-speed conclusion, all-reference result, or independent mathematical review. The auxiliary phase x is realized by rounding time; it is never an independent starting position."}
    (ROOT / "experiments/fast_cluster.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"profiles": [{k: p[k] for k in ("core", "offsets", "slow_time_t0", "chosen_phase_x0", "core_margin", "offset_margin", "sufficient_integer_q")} for p in profiles], "counts": counts}, indent=2, default=str))


if __name__ == "__main__":
    main()
