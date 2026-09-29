#!/usr/bin/env python3
"""Fresh exact one-dimensional audit of the CC other-ray candidate.

Scope: exhaustive maxima and complete maximizer sets for q=2,...,25;
witness evaluation ONLY for q=100002,...,100007. Standard library only.

Authored before consulting any prior optimizer implementation or saved output.
The statement and current prose entrypoints were read. This is fresh internal
AI authorship, not external certification or epistemic independence.

Completeness of the primary method:
For each v, ||v t|| has tent corners at j/(2v). On every closed interval between
consecutive corners of their union, all seven functions are affine. A line i
is on their lower envelope exactly on the interval obtained by clipping the
base interval against line_i <= line_j for every j. These closed dominance
intervals cover the base interval, including ties. An affine function attains
its maximum at its appropriate endpoint; a zero slope preserves the entire
interval. Taking the union of all pieces attaining the global maximum thus
preserves every maximizing point, including any flat intervals.

No contact-pair enumeration, ambient cells, orbit slices, residue formula,
time-reflection reduction, or claimed maximizer count enters optimize().
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


FROZEN_RESEARCH_HEAD = "12d08824ead7b772032ba240d0e858250fbd183c"
SMALL_Q = tuple(range(2, 26))
WITNESS_ONLY_Q = tuple(range(100002, 100008))


def speeds(q):
    return (1, q, q + 1, 2 * q + 1, 3 * q + 1, 3 * q + 2, 5 * q + 2)


def distance(t):
    """Direct rational distance to Z; separate from the affine construction."""
    fractional = t - t.numerator // t.denominator
    return min(fractional, 1 - fractional)


def value(velocities, t):
    return min(distance(v * t) for v in velocities)


def merge_components(intervals):
    """Closed union; touching intervals and duplicated isolated points merge."""
    out = []
    for left, right in sorted(intervals):
        assert left <= right
        if out and left <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], right))
        else:
            out.append((left, right))
    return out


def envelope_pieces(lines, left, right, counts):
    """Return (lo, hi, slope, intercept) for every nonempty dominance set."""
    pieces = []
    for index, (slope, intercept) in enumerate(lines):
        lo, hi = left, right
        for other_index, (other_slope, other_intercept) in enumerate(lines):
            if index == other_index:
                continue
            counts["dominance_inequalities"] += 1
            # (slope - other_slope) * t <= other_intercept - intercept.
            coefficient = slope - other_slope
            bound = other_intercept - intercept
            if coefficient > 0:
                hi = min(hi, Q(bound, coefficient))
            elif coefficient < 0:
                lo = max(lo, Q(bound, coefficient))
            elif bound < 0:
                lo, hi = Q(1), Q(0)
            if lo > hi:
                break
        if lo <= hi:
            pieces.append((lo, hi, slope, intercept))
            counts["dominance_pieces"] += 1
            counts["singleton_dominance_pieces"] += (lo == hi)
    # Complete coverage is an explicit invariant, independent of maximization.
    assert merge_components((lo, hi) for lo, hi, _, _ in pieces) == [(left, right)]
    counts["envelope_coverage_checks"] += 1
    return pieces


def maximize_pieces(pieces):
    best = None
    winners = []
    for lo, hi, slope, intercept in pieces:
        if slope > 0:
            winning_component = (hi, hi)
            local_best = slope * hi + intercept
        elif slope < 0:
            winning_component = (lo, lo)
            local_best = slope * lo + intercept
        else:
            winning_component = (lo, hi)
            local_best = intercept
        if best is None or local_best > best:
            best = local_best
            winners = [winning_component]
        elif local_best == best:
            winners.append(winning_component)
    assert best is not None
    return best, merge_components(winners)


def optimize(velocities):
    """Exhaust the physical time interval, taking only speeds as input."""
    assert velocities and all(isinstance(v, int) and v > 0 for v in velocities)
    counts = Counter()
    corners = sorted({Q(j, 2 * v) for v in velocities for j in range(2 * v + 1)})
    counts["tent_corner_occurrences"] = sum(2 * v + 1 for v in velocities)
    counts["distinct_tent_corners"] = len(corners)
    counts["base_intervals"] = len(corners) - 1
    assert corners[0] == 0 and corners[-1] == 1
    all_pieces = []
    for left, right in zip(corners, corners[1:]):
        midpoint = (left + right) / 2
        lines = []
        for v in velocities:
            # The tent number fixes its slope without any optimization claim.
            tent_number = (2 * v * midpoint).numerator // (2 * v * midpoint).denominator
            if tent_number % 2 == 0:
                line = (v, Q(-tent_number, 2))
            else:
                line = (-v, Q(tent_number + 1, 2))
            slope, intercept = line
            for t in (left, midpoint, right):
                assert slope * t + intercept == distance(v * t)
                counts["affine_distance_checks"] += 1
            lines.append(line)
        pieces = envelope_pieces(lines, left, right, counts)
        for lo, hi, slope, intercept in pieces:
            for t in (lo, (lo + hi) / 2, hi):
                assert slope * t + intercept == value(velocities, t)
                counts["envelope_value_checks"] += 1
        all_pieces.extend(pieces)
    best, components = maximize_pieces(all_pieces)
    # The full domain was covered; endpoints are also checked directly.
    for endpoint in (Q(0), Q(1)):
        endpoint_value = value(velocities, endpoint)
        assert endpoint_value <= best
        assert (endpoint_value == best) == any(lo <= endpoint <= hi for lo, hi in components)
        counts["domain_endpoint_checks"] += 1
    for lo, hi in components:
        for t in (lo, (lo + hi) / 2, hi):
            assert value(velocities, t) == best
            counts["maximizer_value_checks"] += 1
    return best, components, counts


def threshold_set(velocities, threshold):
    """Independent closed-safe-band intersection at the computed optimum."""
    assert 0 <= threshold <= Q(1, 2)
    current = [(Q(0), Q(1))]
    count = 0
    for v in velocities:
        bands = [(Q(j + threshold, v), Q(j + 1 - threshold, v)) for j in range(v)]
        count += len(bands)
        intersections = []
        i, j = 0, 0
        while i < len(current) and j < len(bands):
            lo = max(current[i][0], bands[j][0])
            hi = min(current[i][1], bands[j][1])
            if lo <= hi:
                intersections.append((lo, hi))
            if current[i][1] < bands[j][1]:
                i += 1
            elif current[i][1] > bands[j][1]:
                j += 1
            else:
                i += 1
                j += 1
        current = merge_components(intersections)
    return current, count


def claimed_value_and_time(q):
    """Written theorem, used only after the small-q optimizer has returned."""
    residue = q % 6
    if residue == 0:
        return Q(2 * q, 3 * (4 * q + 1)), Q(4 * q + 3, 3 * (4 * q + 1))
    if residue == 2:
        return Q(5 * q + 2, 6 * (5 * q + 3)), Q(5 * q + 8, 6 * (5 * q + 3))
    if residue == 5:
        return Q(q, 3 * (2 * q + 1)), Q(2 * q, 3 * (2 * q + 1))
    return Q(1, 6), Q(1, 6)


def component_json(components):
    return [
        {"start": str(lo), "end": str(hi), "kind": "point" if lo == hi else "interval"}
        for lo, hi in components
    ]


def physical_witness(velocities, t):
    rows = []
    for v in velocities:
        phase = v * t
        lap = phase.numerator // phase.denominator
        fractional = phase - lap
        rows.append({
            "speed": v,
            "lap": lap,
            "fractional_phase": str(fractional),
            "distance": str(min(fractional, 1 - fractional)),
        })
    achieved = value(velocities, t)
    return {
        "time": str(t),
        "achieved_value": str(achieved),
        "limiting_speeds": [row["speed"] for row in rows if Q(row["distance"]) == achieved],
        "runners": rows,
    }


def helper_controls():
    """Synthetic affine controls, not additional physical runner inputs."""
    # A flat optimal interval, tied at both ends, must not become two points.
    c = Counter()
    flat = envelope_pieces([(Q(1), Q(0)), (Q(0), Q(1, 3)), (Q(-1), Q(1))], Q(0), Q(1), c)
    assert maximize_pieces(flat) == (Q(1, 3), [(Q(1, 3), Q(2, 3))])
    # Boundary maximum and duplicate affine functions exercise other tie paths.
    c = Counter()
    endpoint = envelope_pieces([(Q(1), Q(0)), (Q(1), Q(0)), (Q(1), Q(2))], Q(0), Q(1), c)
    assert maximize_pieces(endpoint) == (Q(1), [(Q(1), Q(1))])
    assert merge_components([(Q(0), Q(1, 3)), (Q(1, 3), Q(2, 3)), (Q(1), Q(1))]) == [
        (Q(0), Q(2, 3)), (Q(1), Q(1))
    ]
    return {"synthetic_affine_control_count": 3, "passed": True, "new_physical_inputs": 0}


def main():
    failures = []
    records = []
    totals = Counter()
    controls = helper_controls()
    for q in SMALL_Q:
        velocities = speeds(q)
        # Information barrier: exhaustive calculation and independent
        # threshold-set reconstruction precede comparison with the statement.
        maximum, components, counts = optimize(velocities)
        threshold_components, generated_bands = threshold_set(velocities, maximum)
        threshold_matches = components == threshold_components
        expected, t = claimed_value_and_time(q)
        expected_components = sorted([(t, t), (1 - t, 1 - t)])
        value_matches = maximum == expected
        all_times_match = components == expected_components
        if not (threshold_matches and value_matches and all_times_match):
            failures.append({"q": q, "threshold_matches": threshold_matches,
                             "value_matches": value_matches, "all_times_match": all_times_match})
        counts["threshold_bands_generated"] = generated_bands
        counts["threshold_set_comparisons"] = 1
        totals.update(counts)
        records.append({
            "q": q, "residue_mod_6": q % 6, "speeds": velocities,
            "maximum": str(maximum), "maximizing_components": component_json(components),
            "positive_length_maximizing_components": sum(lo < hi for lo, hi in components),
            "threshold_components": component_json(threshold_components),
            "threshold_set_matches": threshold_matches,
            "claimed_value": str(expected), "claimed_times": [str(a) for a, _ in expected_components],
            "claimed_value_matches": value_matches, "claimed_all_times_match": all_times_match,
            "maximizer_witnesses": [physical_witness(velocities, lo) for lo, hi in components if lo == hi],
            "counts": dict(sorted(counts.items())),
        })
    witnesses = []
    for q in WITNESS_ONLY_Q:
        velocities = speeds(q)
        expected, t = claimed_value_and_time(q)
        witness_rows = [physical_witness(velocities, t), physical_witness(velocities, 1 - t)]
        matches = all(Q(row["achieved_value"]) == expected for row in witness_rows)
        if not matches:
            failures.append({"q": q, "witness_value_matches": False})
        witnesses.append({
            "q": q, "residue_mod_6": q % 6, "speeds": velocities,
            "claimed_value": str(expected), "witnesses": witness_rows,
            "witness_value_matches": matches,
            "exhaustive_maximum_computed": False,
            "all_maximizers_checked": False,
        })
    report = {
        "title": "Fresh physical tent-segment audit of the CC other ray",
        "date": "2026-09-29",
        "frozen_research_head_from_protocol": FROZEN_RESEARCH_HEAD,
        "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "arithmetic": "fractions.Fraction; no floating point",
        "scope": {
            "total_runners": 8, "reference_speed": 0, "common_start": True,
            "time_domain": "[0,1]", "exhaustive_q": SMALL_Q,
            "witness_only_q": WITNESS_ONLY_Q,
            "large_q_exhaustive_optimization": False,
        },
        "provenance": {
            "prior_optimizer_code_read_before_authoring": False,
            "prior_saved_optimizer_output_read_before_authoring": False,
            "prior_optimizer_code_or_saved_output_read_after_authoring": False,
            "written_statement_read": True,
            "current_entrypoint_prose_read": True,
            "fresh_ai_authorship_is_external_certification": False,
        },
        "helper_controls": controls,
        "summary": {
            "exhaustive_case_count": len(records),
            "isolated_maximizer_occurrences": sum(len(r["maximizer_witnesses"]) for r in records),
            "positive_length_maximizing_components": sum(r["positive_length_maximizing_components"] for r in records),
            "small_q_distance_records_at_maximizers": sum(len(r["maximizer_witnesses"]) * 7 for r in records),
            "witness_only_case_count": len(witnesses),
            "witness_only_time_count": sum(len(r["witnesses"]) for r in witnesses),
            "witness_only_distance_records": sum(len(r["witnesses"]) * 7 for r in witnesses),
            "failures": len(failures),
        },
        "total_optimizer_counts": dict(sorted(totals.items())),
        "exhaustive_results": records,
        "witness_only_results": witnesses,
        "failures": failures,
        "conclusion": "PASS within the declared finite scope" if not failures else "FAIL; inspect failures",
        "limits": [
            "No infinite-q upper bound or uniqueness proof is certified by this finite calculation.",
            "Large-q checks establish only achieved witness values, not maxima or uniqueness.",
            "No other speed family, reference runner, or initial phase was examined.",
            "Fresh internally AI-authored code is a useful countercheck, not external certification.",
        ],
    }
    print(json.dumps(report, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
