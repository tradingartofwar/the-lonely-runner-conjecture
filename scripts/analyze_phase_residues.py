"""Finite rational endpoint classes, exact sign certificates and controls.

Run: python -m scripts.analyze_phase_residues
Scope: 144 overlap classes, 160 pair-budget classes, two prescribed pair
checks per budget class, and 17 full configurations. No time sampling.
The finite reduction and unbounded implication await independent review.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from scripts.analyze_phase_discrepancy import AREAS, CUTOFFS, bands, primitive, area_and_correction
from scripts.analyze_residual_overlap import J, L, PRESETS, affine_windows, analyze
from scripts.analyze_overlap_placement import single_duration
from scripts.analyze_blocking_overlaps import blocking_intervals
from scripts.analyze_local_overlap import duration, intersect


ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "81b028b752bc3cfe056e01694619a8446a82ad15"
OVERLAP_PERIODS = {1: 32, 2: 16, 3: 96}
BUDGET_PERIODS = {1: 32, 2: 32, 3: 96}


def overlap_coefficients(q, r):
    """Exact O=I+A/q+B/(2q+r); coefficients depend on endpoint phases."""
    a, b = Q(0), Q(0)
    for (lo, hi), lower, upper in bands(r):
        for sign, (slope, offset) in ((1, upper), (-1, lower)):
            delta = sign * (primitive((q - slope) * hi - offset) -
                            primitive((q - slope) * lo - offset))
            if slope == 0:
                a += delta
            else:
                assert slope == -Q(r, 2)
                b += 2 * delta
    return a, b


def centered_duration_primitive(z):
    """C(z)-z/4, periodic, with range [-3/32,3/32]."""
    x = z - z.numerator // z.denominator
    return min(x, Q(1, 8)) + max(Q(0), x - Q(7, 8)) - x / 4


def duration_coefficient(w):
    """D_w=L/4+e(w)/w; e is periodic modulo 32 for integer w."""
    return centered_duration_primitive(w * J[1]) - centered_duration_primitive(w * J[0])


def bound_coefficients(q, r, kind):
    a, b = overlap_coefficients(q, r)
    if kind == "overlap_only":
        return a - Q(9, 16), b - Q(3, 16)
    if kind == "pair_budget":
        return a - duration_coefficient(q) - Q(3, 8), b - duration_coefficient(2 * q + r)
    raise ValueError(kind)


def lower_bound(q, r, kind):
    a, b = bound_coefficients(q, r, kind)
    return AREAS[r] + a / q + b / (2 * q + r)


def class_certificate(r, s, period, kind):
    # Periodicity follows algebraically: adding period to q adds an integer
    # to every primitive argument. These exact denominator checks cover all
    # time endpoints used by the formula, including the r=3 slope change.
    assert all((period * t).denominator == 1
               for interval, _, _ in bands(r) for t in interval)
    if kind == "pair_budget":
        assert all((period * t).denominator == 1 for t in J)
    a, b = bound_coefficients(s, r, kind)
    assert a < 0
    polynomial = (2 * AREAS[r], r * AREAS[r] + 2 * a + b, r * a)
    assert polynomial[0] > 0 and polynomial[2] < 0

    def value(q):
        return AREAS[r] + a / q + b / (2 * q + r)

    def numerator(q):
        c2, c1, c0 = polynomial
        return c2 * q * q + c1 * q + c0

    first = s or period
    while value(first) <= 0:
        first += period
        assert first < CUTOFFS[r] + period  # proven previous sufficient bound
    previous = first - period
    assert numerator(first) == value(first) * first * (2 * first + r) > 0
    if previous > 0:
        assert numerator(previous) == value(previous) * previous * (2 * previous + r) <= 0
    # Positive leading coefficient and negative constant imply exactly one
    # positive root. These two signs therefore certify this entire class.
    A, B = overlap_coefficients(s, r)
    row = {"residue": s, "period": period, "overlap_A": A, "overlap_B": B,
        "bound_a": a, "bound_b": b, "numerator_coefficients_descending": polynomial,
        "first_positive_q_in_class": first, "value_at_first": value(first),
        "last_nonpositive_q_in_class": previous if previous > 0 else None,
        "value_at_last": value(previous) if previous > 0 else None}
    if kind == "pair_budget":
        row.update({"duration_e_q": duration_coefficient(s),
                    "duration_e_pair": duration_coefficient(2 * s + r)})
    return row


def classify(r, kind):
    periods = OVERLAP_PERIODS if kind == "overlap_only" else BUDGET_PERIODS
    period = periods[r]
    rows = [class_certificate(r, s, period, kind) for s in range(period)]
    last = max(row["last_nonpositive_q_in_class"] or 0 for row in rows)
    cutoff = last + 1
    assert lower_bound(last, r, kind) <= 0 < lower_bound(cutoff, r, kind)
    return {"residual_r": r, "period": period, "uniform_cutoff": cutoff,
        "last_nonpositive_q": last, "value_at_last": lower_bound(last, r, kind),
        "value_at_cutoff": lower_bound(cutoff, r, kind), "classes": rows}


def check_pair(q, r):
    pair = (q, 2 * q + r)
    A, B = overlap_coefficients(q, r)
    predicted = AREAS[r] + A / q + B / pair[1]
    direct = duration(intersect(intersect(blocking_intervals(pair[0]), blocking_intervals(pair[1])), (J,)))
    affine = sum((w["width"] for w in affine_windows(q, r)), Q(0))
    area, correction = area_and_correction(q, r)
    assert predicted == direct == affine == area + correction
    durations = []
    for w in pair:
        exact = single_duration(w)
        assert exact == L / 4 + duration_coefficient(w) / w
        assert exact == duration(intersect(blocking_intervals(w), (J,)))
        assert abs(duration_coefficient(w)) <= Q(3, 16)
        durations.append(exact)
    assert lower_bound(q, r, "pair_budget") == direct - (sum(durations) - L / 2) - Q(3, 8 * q)
    assert lower_bound(q, r, "pair_budget") >= lower_bound(q, r, "overlap_only")
    return {"q": q, "pair_overlap": direct, "pair_individual_durations": durations}


def main():
    overlap = [classify(r, "overlap_only") for r in (1, 2, 3)]
    budget = [classify(r, "pair_budget") for r in (1, 2, 3)]
    assert [row["uniform_cutoff"] for row in overlap] == [303, 345, 62]
    assert [row["uniform_cutoff"] for row in budget] == [242, 263, 36]
    pair_checks = 0
    for result in budget:
        r, period = result["residual_r"], result["period"]
        for row in result["classes"]:
            s = row["residue"]
            qs = (period + s, 2 * period + s)
            row["independent_pair_checks"] = [check_pair(q, r) for q in qs]
            assert overlap_coefficients(qs[0], r) == overlap_coefficients(qs[1], r)
            assert bound_coefficients(qs[0], r, "pair_budget") == bound_coefficients(qs[1], r, "pair_budget")
            pair_checks += 2
    presets = [(q, r, u, v, "retained_control")
        for q, u, v in PRESETS for r in (1, 2, 3)]
    for result in budget:
        r, cutoff = result["residual_r"], result["uniform_cutoff"]
        for q in (cutoff - 1, cutoff):
            presets.append((q, r, q + 1, q + 2, "below_cutoff" if q < cutoff else "at_cutoff"))
    presets.extend((q, 3, q + 1, q + 2, "nonmonotone_control") for q in (33, 34))
    cases = []
    for q, r, u, v, label in presets:
        exact = analyze(q, r, u, v)
        G = lower_bound(q, r, "overlap_only")
        H = lower_bound(q, r, "pair_budget")
        assert u >= q and v >= q
        assert G <= H <= exact["one_pair_lower_bound"] <= exact["actual_clear_duration"]
        if label == "below_cutoff":
            assert H <= 0 < exact["actual_clear_duration"]
        keys = ("pair", "other_two", "pair_overlap_duration", "individual_blocking_durations",
            "excess_E", "one_pair_lower_bound", "actual_clear_duration", "allowed_intervals",
            "blocking_histogram", "certified_clear_interval", "affine_phase_certificate", "witness")
        row = {k: exact[k] for k in keys if k in exact}
        row.update({"q": q, "residual_r": r, "label": label,
            "overlap_only_bound_G": G, "pair_budget_bound_H": H})
        cases.append(row)
    assert all(lower_bound(q, 3, "pair_budget") > 0 for q in (33, 34, 36))
    assert lower_bound(35, 3, "pair_budget") < 0
    source_paths = ("scripts/analyze_phase_residues.py", "scripts/analyze_phase_discrepancy.py",
        "scripts/analyze_residual_overlap.py", "scripts/analyze_overlap_placement.py",
        "scripts/analyze_local_overlap.py", "scripts/analyze_blocking_overlaps.py",
        "scripts/analyze_two_variable_speeds.py", "lonely_runner/checker.py")
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
        "claim_status": {"finite_exact_certificates": "OBSERVED",
            "finite_reduction_and_infinite_implication": "HYPOTHESIS: AI-generated proof candidate; independent review pending",
            "arbitrary_coverage": "OPEN"},
        "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
        "scope": "Eight total common-start runners, reference 0, threshold 1/8; distinct positive integer relative speeds {1,4,5,q,2q+r,u,v}, r in {1,2,3}, u,v>=q.",
        "J": J, "phase_areas": AREAS,
        "overlap_formula": "O=I_r+A_s/q+B_s/(2q+r)",
        "duration_formula": "D_w=L/4+e(w)/w; e(w+32)=e(w)",
        "bound_G": "I_r+(A_s-9/16)/q+(B_s-3/16)/(2q+r)",
        "bound_H": "I_r+(A_s-e(q)-3/8)/q+(B_s-e(2q+r))/(2q+r)",
        "class_certificate_logic": "After multiplication by q(2q+r)>0, each bound is a quadratic with positive leading coefficient and negative constant. Its unique positive root is bracketed between the recorded last nonpositive and first positive class members, if a positive predecessor exists. This proves each infinite class given the endpoint reduction.",
        "overlap_only_classification": overlap, "pair_budget_classification": budget,
        "full_cases": cases,
        "verification_counts": {"overlap_classes": 144, "pair_budget_classes": 160,
            "independent_pair_checks": pair_checks, "pair_single_duration_checks": 2 * pair_checks,
            "full_configurations": 17, "full_single_duration_checks": 68,
            "independent_full_duration_checks": 17, "positive_interval_certificates": 16,
            "small_q_endpoint_checks": 3},
        "limitations": "Cutoffs are minimal for the stated positive-bound tests, not for actual loneliness. Numerical class certificates require the written finite reduction; they are not an independently reviewed proof. Equality points retained. No all-reference, arbitrary-speed or novelty claim.",
    }
    (ROOT / "experiments/phase_residues.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"overlap_cutoffs": [{k: x[k] for k in ("residual_r", "uniform_cutoff", "value_at_last", "value_at_cutoff")} for x in overlap],
        "pair_budget_cutoffs": [{k: x[k] for k in ("residual_r", "uniform_cutoff", "value_at_last", "value_at_cutoff")} for x in budget],
        "full_cases": [{k: x[k] for k in ("q", "residual_r", "label", "pair_budget_bound_H", "actual_clear_duration")} for x in cases],
        "counts": data["verification_counts"]}, indent=2, default=str))


if __name__ == "__main__":
    main()
