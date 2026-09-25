"""Exact phase-area correction and bounded diagnostics; no time sampling.

Run: python -m scripts.analyze_phase_discrepancy
Fifteen prescribed configurations: nine retained controls and the integer
immediately below/at each of three sufficient cutoffs. Standard library only.
The unbounded derivation is in OVERLAP_PLACEMENT.md, Section 7; review pending.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from scripts.analyze_residual_overlap import J, L, PRESETS, analyze, phase_profile


ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "6b2364130224fa45d4dff8f97ac6d56bd36216a5"
AREAS = {1: Q(9, 4096), 2: Q(1, 512), 3: Q(143, 12288)}
CUTOFFS = {1: 413, 2: 464, 3: 78}


def primitive(z):
    """Continuous periodic primitive of {z}-1/2, range [-1/8,0]."""
    x = z - z.numerator // z.denominator
    return x * (x - 1) / 2


def bands(r):
    """(time interval, lower a(t), upper b(t)); affine form (slope,offset).

    Pair blocking is a(t)<qt-j<b(t) for some integer j, except endpoints
    of measure zero. No blocking is possible outside these time pieces.
    """
    if r == 1:
        return ((J, (Q(0), -Q(1, 8)), (-Q(1, 2), Q(1, 16))),)
    if r == 2:
        return (((Q(5, 16), J[1]), (-Q(1), Q(7, 16)), (Q(0), Q(1, 8))),)
    if r == 3:
        lower = (-Q(3, 2), Q(7, 16))
        return (((J[0], Q(7, 24)), lower, (Q(0), Q(1, 8))),
                ((Q(7, 24), J[1]), lower, (-Q(3, 2), Q(9, 16))))
    raise ValueError("This local derivation covers only residuals 1,2,3")


def endpoint_integral(q, affine, interval):
    slope, offset = affine
    frequency = q - slope
    assert frequency > 0
    a, b = interval
    return (primitive(frequency * b - offset) -
            primitive(frequency * a - offset)) / frequency


def area_and_correction(q, r):
    area, correction = Q(0), Q(0)
    for interval, lower, upper in bands(r):
        a, b = interval
        slope, offset = upper[0] - lower[0], upper[1] - lower[1]
        area += slope * (b * b - a * a) / 2 + offset * (b - a)
        correction += (endpoint_integral(q, upper, interval) -
                       endpoint_integral(q, lower, interval))
    assert area == AREAS[r]
    return area, correction


def discrepancy_bound(q, r):
    return Q(1, 8 * q) + Q(1, 4 * (2 * q + r))


def excess_bound(q, r):
    """Uniform in the remaining two speeds u,v>=q."""
    return Q(3, 16) * (Q(3, q) + Q(1, 2 * q + r))


def clear_floor(q, r):
    return AREAS[r] - Q(11, 16 * q) - Q(7, 16 * (2 * q + r))


def main():
    presets = [(q, r, u, v, "retained_control")
               for q, u, v in PRESETS for r in (1, 2, 3)]
    for r, cutoff in CUTOFFS.items():
        for q in (cutoff - 1, cutoff):
            presets.append((q, r, q + 1, q + 2, "below_cutoff" if q < cutoff else "at_cutoff"))
        assert clear_floor(cutoff - 1, r) < 0 < clear_floor(cutoff, r)
    cases = []
    for q, r, u, v, label in presets:
        # This independently uses explicit window intersections, closed allowed
        # sets, and a separate boundary partition; not the endpoint primitive.
        row = analyze(q, r, u, v)
        area, correction = area_and_correction(q, r)
        bound = discrepancy_bound(q, r)
        assert area + correction == row["pair_overlap_duration"]
        assert abs(correction) <= bound
        assert u >= q and v >= q
        assert row["excess_E"] <= excess_bound(q, r)
        floor = clear_floor(q, r)
        assert floor == area - bound - excess_bound(q, r)
        assert floor <= row["one_pair_lower_bound"] <= row["actual_clear_duration"]
        if label == "below_cutoff":
            assert floor < 0 < row["actual_clear_duration"]
        row.update({"label": label, "phase_area": area,
                    "endpoint_correction": correction, "overlap_from_endpoints": area + correction,
                    "absolute_error_bound": bound, "uniform_excess_bound": excess_bound(q, r),
                    "uniform_clear_lower_bound": floor})
        cases.append(row)
    # Separate trapezoid computation checks the three phase areas.
    for r, area in AREAS.items():
        profile = phase_profile(r)
        assert area == sum(((b - a) * (ka + kb) / 2
            for (a, ka), (b, kb) in zip(profile, profile[1:])), Q(0))
    lookup = {(row["q"], row["residual_r"]): row for row in cases}
    assert lookup[(56, 1)]["endpoint_correction"] > 0
    assert lookup[(56, 2)]["endpoint_correction"] < 0
    assert lookup[(57, 1)]["endpoint_correction"] < 0
    assert lookup[(57, 2)]["endpoint_correction"] > 0
    assert lookup[(6, 1)]["actual_clear_duration"] == 0
    dependencies = ("scripts/analyze_phase_discrepancy.py", "scripts/analyze_residual_overlap.py",
        "scripts/analyze_overlap_placement.py", "scripts/analyze_local_overlap.py",
        "scripts/analyze_blocking_overlaps.py", "scripts/analyze_two_variable_speeds.py",
        "lonely_runner/checker.py")
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
        "claim_status": {"finite_checks": "OBSERVED", "unbounded_derivation":
            "HYPOTHESIS: complete AI-generated proof candidate, independent review pending",
            "arbitrary_coverage": "OPEN"},
        "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in dependencies},
        "scope": "Eight common-start runners, selected reference 0; distinct positive integer relative speeds {1,4,5,q,2q+r,u,v}, r in {1,2,3}, u,v>=q; threshold 1/8.",
        "J": J, "length_J": L, "bands": {r: bands(r) for r in (1, 2, 3)},
        "phase_areas": AREAS, "error_bound": "1/(8q)+1/(4(2q+r))",
        "uniform_clear_lower_bound": "I_r-11/(16q)-7/(16(2q+r))",
        "sufficient_cutoffs_for_this_bound": CUTOFFS,
        "earlier_stronger_r1_cutoff_retained": 310,
        "cutoff_rationale": "The two subtracted reciprocal terms strictly decrease for q>0; positivity at the cutoff therefore persists. The preceding integer is negative. This is not a sharp geometric cutoff.",
        "cases": cases,
        "verification_counts": {"prescribed_configurations": 15, "endpoint_formula_crosschecks": 15,
            "affine_window_crosschecks": 15, "single_duration_crosschecks": 60,
            "independent_full_duration_checks": 15, "positive_interval_certificates": 14,
            "area_crosschecks": 3, "cutoff_sign_brackets": 3, "small_q_endpoint_checks": 3},
        "limitations": "Finite diagnostics do not prove the infinite statement. Closed equality points retained. No sharp cutoff, all-reference result, broad search, novelty claim, or independent mathematical review.",
    }
    out = ROOT / "experiments/phase_discrepancy.json"
    out.write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"cases": [{k: row[k] for k in ("q", "residual_r", "label",
        "pair_overlap_duration", "endpoint_correction", "absolute_error_bound",
        "uniform_clear_lower_bound", "actual_clear_duration")} for row in cases],
        "counts": data["verification_counts"]}, indent=2, default=str))


if __name__ == "__main__":
    main()
