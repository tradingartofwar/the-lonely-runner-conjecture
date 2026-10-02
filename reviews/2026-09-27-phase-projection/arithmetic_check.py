#!/usr/bin/env python3
"""Compact two-time and safe-interval certificates for the fixed two cases.

Does not reconstruct the complete unchanged safe set. Uses exact rational and
integer endpoint inequalities, and imports no project implementation.
--write creates arithmetic.json; default/--check only recomputes and compares.
"""

from fractions import Fraction as F
from hashlib import sha256
from math import lcm
from pathlib import Path
import argparse
import json


HERE = Path(__file__).resolve().parent
PROTOCOL_HASH = "8eba9a06595a2014095f84cc22c6b91d65d6f9fd71771912e0af368293bdff17"
H = F(1, 8)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def phase(v, t):
    value = v*t
    return value - value.numerator//value.denominator


def distance(x):
    x -= x.numerator//x.denominator
    return min(x, 1-x)


def interval_certificate(speeds, interval):
    left, right = interval
    midpoint = (left+right)/2
    laps = []
    for v in speeds:
        x = v*midpoint
        m = x.numerator//x.denominator
        lo = F(8*m+1, 8*v)
        hi = F(8*m+7, 8*v)
        lower_slack = 8*v*left.numerator-left.denominator*(8*m+1)
        upper_slack = right.denominator*(8*m+7)-8*v*right.numerator
        assert lo <= left <= right <= hi
        assert lower_slack >= 0 and upper_slack >= 0
        laps.append({"speed": v, "lap": m, "safe_lap": [lo, hi],
                     "lower_endpoint_integer_slack": lower_slack,
                     "upper_endpoint_integer_slack": upper_slack})
    return {"interval": interval, "duration": right-left, "laps": laps}


def fixed_pair(unchanged, chosen, times):
    unchanged_rows = []
    for t in times:
        ds = [distance(v*t) for v in unchanged]
        unchanged_rows.append({"time": t,
                               "residues": [(v*t.numerator) % t.denominator for v in unchanged],
                               "denominator": t.denominator,
                               "distances": ds,
                               "minimum": min(ds)})
    xs = [phase(chosen, t) for t in times]
    circular_separation = distance(xs[1]-xs[0])
    gamma = min(*(row["minimum"] for row in unchanged_rows), circular_separation/2)
    p, q = gamma.numerator, gamma.denominator
    integer_certificates = []
    for t in times:
        a, b = t.numerator, t.denominator
        rows = []
        for v in unchanged:
            r = v*a % b
            lower, upper = q*r-p*b, q*(b-r)-p*b
            assert lower >= 0 and upper >= 0
            rows.append([v, r, lower, upper])
        integer_certificates.append({"time": t, "rows_speed_residue_lower_upper": rows})
    common_denominator = lcm(*(t.denominator for t in times))
    residues = [(chosen*t.numerator*(common_denominator//t.denominator)) % common_denominator
                for t in times]
    raw_delta = abs(residues[1]-residues[0])
    short_delta = min(raw_delta, common_denominator-raw_delta)
    pair_slack = q*short_delta-2*p*common_denominator
    assert pair_slack >= 0
    assert circular_separation == F(short_delta, common_denominator)
    assert gamma == unchanged_rows[0]["minimum"] == unchanged_rows[1]["minimum"]
    capped_by = [[v for v, d in zip(unchanged, row["distances"]) if d == gamma]
                 for row in unchanged_rows]
    result = {"times": times, "unchanged_speed_order": unchanged,
              "unchanged_checks": unchanged_rows,
              "chosen_speed_phases": xs,
              "circular_phase_separation": circular_separation,
              "uniform_minimum_distance": gamma,
              "margin_above_threshold": gamma-H,
              "unchanged_caps_at_each_time": capped_by,
              "best_of_the_two_distance_is_constant_for_all_phases": gamma,
              "unchanged_integer_certificates": integer_certificates,
              "pair_integer_certificate": {"common_denominator": common_denominator,
                                           "phase_residues": residues,
                                           "short_circular_integer_separation": short_delta,
                                           "nonnegative_slack": pair_slack}}
    if gamma > H:
        unchanged_radii = [[(d-H)/v for v, d in zip(unchanged, row["distances"])]
                           for row in unchanged_rows]
        unchanged_radius = min(radius for row in unchanged_radii for radius in row)
        chosen_radius = (gamma-H)/chosen
        radius = min(unchanged_radius, chosen_radius)
        intervals = [(t-radius, t+radius) for t in times]
        assert all(F(0) <= left < right <= F(1) for left, right in intervals)
        result["strict_interval_menu"] = {
            "unchanged_radius_by_speed": unchanged_radii,
            "unchanged_uniform_radius": unchanged_radius,
            "chosen_speed_uniform_radius": chosen_radius,
            "selected_radius": radius,
            "intervals": [interval_certificate(unchanged, item) for item in intervals],
            "guaranteed_total_duration_lower_bound": 2*radius,
            "selection_rule": "Choose a menu interval whose center has shifted speed11 distance at least gamma; at least one always does."}
        # A longer interval need not be fixed in advance. These constants check
        # the separate one-sided clipping argument supplied in arithmetic.md.
        safe_lap_duration = (1-2*H)/chosen
        assert safe_lap_duration >= 2*unchanged_radius
        result["one_sided_refinement"] = {
            "unchanged_symmetric_radius": unchanged_radius,
            "chosen_safe_lap_duration": safe_lap_duration,
            "chosen_minimum_one_sided_radius": chosen_radius,
            "guaranteed_duration_lower_bound": unchanged_radius+min(unchanged_radius, chosen_radius)}
    return result


def known_subset(V, unchanged):
    if V == 13:
        first = (F(17, 48), F(3, 8))
        integers = [4, 7]
        expected = [[F(-5, 48), F(1, 8)], [F(-1, 8), F(5, 48)]]
    else:
        first = (F(25, 56), F(15, 32))
        integers = [5, 6]
        expected = [[F(-5, 56), F(5, 32)], [F(-5, 32), F(5, 56)]]
    intervals = [first, (1-first[1], 1-first[0])]
    certificates = [interval_certificate(unchanged, item) for item in intervals]
    images = [[11*t-integer for t in item] for item, integer in zip(intervals, integers)]
    assert images == expected
    assert max(row[0] for row in images) <= min(row[1] for row in images)
    union = [min(row[0] for row in images), max(row[1] for row in images)]
    width = union[1]-union[0]
    assert width < 1
    return {"unchanged_safe_interval_certificates": certificates,
            "centered_chosen_phase_images": images,
            "phase_union": union, "phase_union_length": width,
            "blocking_arc_length": 2*H,
            "excess_phase_width": width-2*H,
            "phase_independent_duration_bound": max(F(0), (width-2*H)/11),
            "nonzero_phase_bound_if_exact_fit": "min(||theta||,1/4)/11" if V == 13 else None}


def profile_comparison(cases):
    """Compare with primary data after deriving the independent certificates."""
    raw = (HERE/"results.json").read_bytes()
    profile = json.loads(raw)
    assert profile["protocol_sha256"] == PROTOCOL_HASH
    assert [row["id"] for row in profile["cases"]] == [row["id"] for row in cases]

    def belongs(x, pieces):
        return any((F(a) < x < F(b)) or (x == F(a) and lc) or
                   (x == F(b) and rc)
                   for a, b, lc, rc in pieces)

    rows = []
    for derived, full in zip(cases, profile["cases"]):
        subset = derived["known_safe_subset_certificate"]
        neg, pos = subset["phase_union"]
        subset_pieces = [(F(0), pos, True, True), (1+neg, F(1), True, False)]
        bulk = full["B_components"]
        events = {F(0), F(1)}
        for a, b, _, _ in [*subset_pieces, *bulk]:
            events.update([F(a), F(b)])
        ordered = sorted(events)
        checks = ordered[:-1]+[(a+b)/2 for a, b in zip(ordered, ordered[1:])]
        assert all(not belongs(x, subset_pieces) or belongs(x, bulk) for x in checks)
        bulk_measure = sum((F(b)-F(a) for a, b, _, _ in bulk), F(0))
        assert bulk_measure == F(full["B_metrics"]["measure"])
        full_measure_bound = max(F(0), (bulk_measure-2*H)/11)
        exact_minimum = F(full["duration_extrema"]["minimum"])
        assert full_measure_bound == exact_minimum
        pair_phases = derived["pair_certificate"]["chosen_speed_phases"]
        assert all(belongs(x, full["P_components"]) for x in pair_phases)
        extras = list(map(F, full["extra_isolated_projection_points"]))
        if derived["V"] == 13:
            assert extras == pair_phases
            assert bulk_measure == subset["phase_union_length"] == F(1, 4)
        else:
            assert extras == []
            assert bulk_measure-subset["phase_union_length"] == F(11, 448)
            assert full_measure_bound-subset["phase_independent_duration_bound"] == F(1, 448)
        rows.append({"id": derived["id"],
                     "certified_subset_is_contained_in_full_bulk": True,
                     "certified_subset_phase_measure": subset["phase_union_length"],
                     "full_bulk_measure": bulk_measure,
                     "additional_bulk_measure": bulk_measure-subset["phase_union_length"],
                     "extra_isolated_projection_points": extras,
                     "full_bulk_measure_only_duration_bound": full_measure_bound,
                     "profile_exact_minimum": exact_minimum,
                     "profile_exact_maximum": F(full["duration_extrema"]["maximum"]),
                     "profile_minimizer_set": full["duration_extrema"]["minimizer_set"],
                     "improvement_over_previous_subset_constant_bound":
                     full_measure_bound-subset["phase_independent_duration_bound"]})
    return {"results_sha256": sha256(raw).hexdigest(),
            "used_as_input_to_compact_certificates": False,
            "cases": rows}


def build():
    raw = (HERE/"protocol.json").read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_HASH
    protocol = json.loads(raw)
    assert protocol["chosen_runner_speed"] == 11
    prescriptions = protocol["compact_certificate_test"]["fixed_candidate_pairs"]
    cases = []
    for prescribed, pair in zip(protocol["cases"], prescriptions):
        assert pair["case"] == prescribed["id"]
        V = prescribed["velocities"][-1]
        assert prescribed["velocities"] == [0, 1, 4, 5, 6, 7, 11, V]
        assert V in [13, 16]
        unchanged = [1, 4, 5, 6, 7, V]
        times = list(map(F, pair["times"]))
        result = fixed_pair(unchanged, 11, times)
        if V == 13:
            assert times == [F(1, 8), F(7, 8)]
            assert result["uniform_minimum_distance"] == F(1, 8)
            assert result["circular_phase_separation"] == F(1, 4)
        else:
            assert times == [F(7, 15), F(8, 15)]
            assert result["uniform_minimum_distance"] == F(2, 15)
            assert result["margin_above_threshold"] == F(1, 120)
            assert result["strict_interval_menu"]["selected_radius"] == F(1, 1320)
            assert result["one_sided_refinement"]["guaranteed_duration_lower_bound"] == F(1, 352)
        cases.append({"id": prescribed["id"], "V": V,
                      "pair_certificate": result,
                      "known_safe_subset_certificate": known_subset(V, unchanged)})
    return encode({"status": "OBSERVED finite integer certificates; all-phase implications are supplied proof candidates",
                   "protocol_sha256": PROTOCOL_HASH,
                   "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                   "complete_unchanged_safe_set_reconstructed": False,
                   "additional_test_time_search_performed": False,
                   "cases": cases,
                   "full_profile_comparison": profile_comparison(cases),
                   "totals": {"cases": 2, "prescribed_test_times": 4,
                              "unchanged_distance_checks": 24,
                              "two_phase_separation_certificates": 2,
                              "known_safe_intervals": 4,
                              "strict_fixed_menu_intervals": 2}})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    path = HERE/"arithmetic.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2)+"\n")
    else:
        assert json.loads(path.read_text()) == result, "arithmetic.json mismatch"
    print(json.dumps(result["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
