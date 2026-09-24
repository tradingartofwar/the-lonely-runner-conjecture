"""Exact diagnostics for four speeds b_i*q+a_i above a fixed core triple.

Run: python -m scripts.analyze_affine_family
Three prescribed profiles, four q values each, three frozen-phase controls,
one small-q failure, and three common-scaling controls. No speed-set scan.
The Fourier and transfer arguments are proof candidates; see FAST_CLUSTER.md.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_core_transfer import boundary_certificate, merged
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "89087ffb3b3371567a8a415fa9a59bb9ef5d0e5c"
D = Q(1, 8)


def floor(x):
    return x.numerator // x.denominator


def frozen_phase(terms, t):
    """Intersect exact affine strips, then reconstruct cells and boundaries."""
    assert len(terms) == len(set(terms)) == 4
    assert all(isinstance(b, int) and b > 0 and isinstance(a, int) for b, a in terms)
    region = ((Q(0), Q(1)),)
    for b, a in terms:
        p = a * t % 1
        windows = []
        for m in range(-1, b + 1):
            left = max(Q(0), (m + D - p) / b)
            right = min(Q(1), (m + 1 - D - p) / b)
            if left <= right:
                windows.append((left, right))
        assert duration(windows) == Q(3, 4)
        region = intersect(region, windows)
    # Build all endpoints independently from the original (unreduced) phase.
    cuts = {Q(0), Q(1)}
    for b, a in terms:
        for m in range(floor(a * t) - 1, floor(b + a * t) + 2):
            for sign in (-1, 1):
                x = (m + sign * D - a * t) / b
                if 0 <= x <= 1:
                    cuts.add(x)
    cuts = sorted(cuts)
    cells, hist, individual = [], [Q(0)] * 5, [Q(0)] * 4
    for left, right in zip(cuts, cuts[1:]):
        x = (left + right) / 2
        blocked = [circular_distance(b * x + a * t) < D for b, a in terms]
        hist[sum(blocked)] += right - left
        for i, active in enumerate(blocked):
            if active:
                individual[i] += right - left
        if not any(blocked):
            cells.append((left, right))
    points = [(x, x) for x in cuts
              if all(circular_distance(b * x + a * t) >= D for b, a in terms)]
    assert merged([*cells, *points]) == region
    assert individual == [Q(1, 4)] * 4 and sum(hist) == 1
    redundancy = sum((m - 1) * hist[m] for m in range(1, 5))
    assert hist[0] == redundancy == duration(region)
    b_min = min(b for b, a in terms)
    min_terms = [a for b, a in terms if b == b_min]
    # For these explicit controls, all lowest-frequency phasors are real.
    # Other phases are left symbolic: no floating-point zero test is used.
    min_phases = [a * t % 1 for a in min_terms]
    exact_real_sum = None
    if all(p in (0, Q(1, 2)) for p in min_phases):
        exact_real_sum = sum(1 if p == 0 else -1 for p in min_phases)
        if exact_real_sum:
            assert hist[0] > 0
    if len(min_terms) == 1:
        assert hist[0] > 0
    return {"terms_b_a": terms, "slow_time": t, "allowed_phases": region,
            "clear_phase_duration": hist[0], "redundant_blocking": redundancy,
            "blocking_count_histogram": hist, "individual_blocked_durations": individual,
            "minimum_winding": b_min, "minimum_winding_offsets": min_terms,
            "minimum_winding_phases": min_phases, "exact_real_phasor_sum": exact_real_sum,
            "unique_minimum_winding": len(min_terms) == 1}


def profile(core, terms, t0):
    assert len(core) == len(set(core)) == 3 and min(core) > 0
    allowed = feasible_intervals(core, D)
    assert duration(allowed) >= Q(1, 4)
    left, right = next((l, r) for l, r in allowed if l < t0 < r)
    phase = frozen_phase(terms, t0)
    l, r = max(phase["allowed_phases"], key=lambda ab: ab[1] - ab[0])
    assert l < r
    x0 = (l + r) / 2
    mc = min(circular_distance(c * t0) for c in core) - D
    mf = min(circular_distance(b * x0 + a * t0) for b, a in terms) - D
    assert mc > 0 and mf > 0
    M, A = max(core), max(abs(a) for b, a in terms)
    bounds = {"above_core": Q(M + A), "fast_distinctness": Q(2 * A),
              "core_drift": Q(M, 2) / mc, "offset_drift": Q(A, 2) / mf,
              "inside_core_component": 1 / (2 * min(t0 - left, right - t0))}
    return {"core": core, "terms_b_a": terms, "core_component": (left, right),
            "slow_time_t0": t0, "phase_x0": x0, "core_margin": mc, "fast_margin": mf,
            "frozen_phase": phase, "strict_q_bounds": bounds,
            "strict_q_bound": max(bounds.values()),
            "sufficient_integer_q": floor(max(bounds.values())) + 1}


def witness(p, q):
    core, terms = p["core"], p["terms_b_a"]
    extra = tuple(b * q + a for b, a in terms)
    speeds = tuple(sorted((*core, *extra)))
    assert len(speeds) == len(set(speeds)) == 7 and min(speeds) > 0
    t0, x0 = p["slow_time_t0"], p["phase_x0"]
    m = floor(q * t0 - x0 + Q(1, 2))
    t = (m + x0) / q
    assert abs(t - t0) <= Q(1, 2 * q) and q * t % 1 == x0
    for b, a in terms:
        assert (b * q + a) * t == b * m + b * x0 + a * t
    lower_c = D + p["core_margin"] - Q(max(core), 2 * q)
    lower_f = D + p["fast_margin"] - Q(max(abs(a) for b, a in terms), 2 * q)
    distances = {v: circular_distance(v * t) for v in speeds}
    assert all(distances[c] >= lower_c for c in core)
    assert all(distances[v] >= lower_f for v in extra)
    guaranteed = q >= p["sufficient_integer_q"]
    if guaranteed:
        assert min(lower_c, lower_f) > D
        assert p["core_component"][0] < t < p["core_component"][1]
    minimum = min(distances.values())
    full = feasible_intervals(speeds, D)
    independent = boundary_certificate(speeds)
    assert full == independent["complete_allowed_set"]
    result = {"q": q, "in_guaranteed_range": guaranteed, "speeds": speeds,
              "rounded_integer": m, "witness_time": t, "time_shift": t - t0,
              "distances": distances, "minimum_distance": minimum,
              "core_lower_bound": lower_c, "fast_lower_bound": lower_f,
              "complete_allowed_summary": {"component_count": len(full),
                  "sha256_json_string_endpoints": hashlib.sha256(json.dumps(full, default=str).encode()).hexdigest(),
                  "first_component": full[0] if full else None,
                  "last_component": full[-1] if full else None},
              "clear_duration": duration(full),
              "isolated_contacts": independent["isolated_contact_certificates"]}
    if duration(full) == 0:
        result["complete_allowed_set"] = full
    if minimum > D:
        radius = (minimum - D) / (2 * max(speeds))
        interval = (t - radius, t + radius)
        assert 0 < interval[0] < interval[1] < 1
        assert intersect(full, (interval,)) == (interval,)
        result["interval"] = interval
        result["affine_certificate"] = phase_certificate(speeds, interval)
    return result


def main():
    terms = ((1, 0), (2, 1), (3, 5), (4, 7))
    tiler = ((1, 0), (1, 4), (2, 3), (2, 5))
    profiles = [profile((1, 4, 5), terms, Q(21, 64)),
                profile((1, 4, 5), ((1, 0), (1, 1), (1, 5), (1, 7)), Q(21, 64)),
                profile((2, 3, 5), tiler, Q(13, 100))]
    for p in profiles:
        cutoff = p["sufficient_integer_q"]
        p["checks"] = [witness(p, q) for q in (cutoff - 1, cutoff, cutoff + 1, 2 * cutoff)]
    assert profiles[0]["sufficient_integer_q"] == 16
    assert profiles[0]["checks"][1]["witness_time"] == Q(8555, 24576)
    assert profiles[0]["checks"][1]["minimum_distance"] == Q(6377, 24576)
    assert profiles[1]["sufficient_integer_q"] == 65
    assert profiles[1]["phase_x0"] == Q(23, 128)
    assert profiles[1]["checks"][1]["witness_time"] == Q(2711, 8320)
    assert profiles[1]["checks"][1]["minimum_distance"] == Q(23, 128)
    controls = [frozen_phase(tiler, Q(1, 8)), frozen_phase(tiler, Q(13, 100)),
                frozen_phase(((1, 0), (1, 4), (2, 3), (2, 6)), Q(1, 8))]
    assert min(circular_distance(c * Q(1, 8)) for c in (2, 3, 5)) == Q(1, 4)
    assert controls[0]["allowed_phases"] == tuple((Q(i, 8), Q(i, 8)) for i in (1, 2, 3, 5, 6, 7))
    assert controls[0]["clear_phase_duration"] == 0
    assert controls[0]["exact_real_phasor_sum"] == controls[2]["exact_real_phasor_sum"] == 0
    assert controls[1]["clear_phase_duration"] > 0 and controls[2]["clear_phase_duration"] > 0
    tight = witness(profiles[1], 6)
    assert tight["minimum_distance"] == Q(1, 256) < D
    assert tight["clear_duration"] == 0
    assert tight["complete_allowed_set"] == tuple((Q(i, 8),) * 2 for i in (1, 3, 5, 7))
    scaling = []
    for q in (1, 2, 3):
        speeds = tuple(q * v for v in range(1, 8))
        full = feasible_intervals(speeds, D)
        assert full == boundary_certificate(speeds)["complete_allowed_set"]
        expected = tuple((Q(8 * j + i, 8 * q),) * 2 for j in range(q) for i in (1, 3, 5, 7))
        assert full == expected and duration(full) == 0
        scaling.append({"q": q, "speeds": speeds, "complete_allowed_set": full, "clear_duration": Q(0)})
    paths = ("scripts/analyze_affine_family.py", "scripts/analyze_core_transfer.py",
             "scripts/analyze_local_overlap.py", "scripts/analyze_blocking_overlaps.py",
             "scripts/analyze_overlap_placement.py", "scripts/analyze_phase_discrepancy.py",
             "scripts/analyze_two_variable_speeds.py", "lonely_runner/checker.py")
    counts = {"profiles": len(profiles), "witness_checks": 4 * len(profiles),
              "guaranteed_witness_checks": 3 * len(profiles), "below_cutoff_checks": len(profiles),
              "affine_interval_certificates": sum("affine_certificate" in w for p in profiles for w in p["checks"]),
              "frozen_phase_reconstructions": len(profiles) + len(controls),
              "complete_boundary_reconstructions": 4 * len(profiles) + 1 + len(scaling),
              "explicit_frozen_controls": len(controls), "small_q_failure_controls": 1,
              "common_scaling_controls": len(scaling)}
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
            "scope": "n=8, common start, reference 0; fixed positive integer core triple; four fixed distinct pairs (b_i,a_i), positive integer b_i, integer a_i; extras b_i*q+a_i for sufficiently large integer q.",
            "claim_status": {"general_argument": "HYPOTHESIS/proof candidate; AI-generated, independent review outstanding, no novelty claim.",
                             "finite_checks": "OBSERVED, exact rational computations.",
                             "all_seven_speeds_growing_forces_strictness": "DISPROVEN by common scaling of 1,...,7.",
                             "arbitrary_seven_speed_method": "OPEN in this investigation."},
            "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "profiles": profiles, "frozen_controls": controls, "small_q_control": tight,
            "common_scaling_controls": scaling, "verification_counts": counts,
            "limits": "Only these inputs are computed. Complete positive-duration allowed unions are reconstructed and compared in memory; the output keeps their SHA-256, counts, duration, and first/last components, alongside explicit witness interval certificates. Zero-duration allowed sets are retained in full. The Fourier nonvanishing and infinite-q implication come from the written proof candidate, not numerical Fourier estimates or these finite checks. All three profiles use nonnegative offsets; the written argument allows fixed negative offsets via absolute-value bounds. Fixed core and coefficients are essential to the stated uniform guarantee. No independent mathematical review."}
    (ROOT / "experiments/affine_family.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"profiles": [{k: p[k] for k in ("core", "terms_b_a", "slow_time_t0", "phase_x0", "core_margin", "fast_margin", "sufficient_integer_q")} for p in profiles],
                      "controls": controls, "counts": counts}, indent=2, default=str))


if __name__ == "__main__":
    main()
