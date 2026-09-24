"""Exact ratio-overlap certificates at the fixed eight-runner threshold.

Run: python -m scripts.analyze_speed_ratios
Eleven prescribed reduced ratios, five full configurations, no speed-set scan.
See notes/SPEED_RATIOS.md for the unbounded argument and literature match.
"""

import hashlib
import json
from fractions import Fraction as Q
from math import gcd
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_blocking_overlaps import blocking_intervals
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate


ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "c740a21549dce1dd2eb40c224b2a9aacc8986b4f"
N = 8
DELTA = Q(1, N)
CORE = (1, 4, 5)
J = (Q(9, 32), Q(3, 8))
LENGTH = J[1] - J[0]
RATIOS = tuple((1, b) for b in range(2, 10)) + ((2, 3), (3, 5), (56, 113))
CASES = (
    ("doubled", (56, 112), (64, 72)),
    ("triple", (80, 240), (88, 96)),
    ("three_to_two", (160, 240), (88, 96)),
    ("minimum_overlap_ratio", (192, 1344), (200, 208)),
    ("perturbed_double", (56, 113), (64, 72)),
)


def frac(x):
    return x - x.numerator // x.denominator


def f(x):
    return x * (1 - x)


def h(x):
    """Sum over integer d of max(x-|d|, 0), in closed form."""
    m = x.numerator // x.denominator
    return x * (2 * m + 1) - m * (m + 1)


def overlap(a, b):
    """Full-cycle simultaneous blocking fraction; reduced positive pair."""
    assert 0 < a < b and gcd(a, b) == 1
    return Q(1, 16) + (f(frac(Q(a + b, 8))) - f(frac(Q(b - a, 8)))) / (a * b)


def literature_overlap(a, b):
    """Perarnau--Serra Proposition 8, delta=1/8, reduced pair."""
    x, y = frac(Q(a, 8)), frac(Q(b, 8))
    correction = min(x, y) + max(x + y - 1, Q(0)) - 2 * x * y
    return Q(1, 16) + 2 * correction / (a * b)


def clear_bound(rho, g, u, v):
    return rho * LENGTH - (Q(1, 4) - rho * rho) / g - Q(3, 16 * u) - Q(3, 16 * v)


def ratio_check(a, b):
    rho = overlap(a, b)
    geometric = (h(Q(a + b, 8)) - h(Q(b - a, 8))) / (a * b)
    direct = duration(intersect(blocking_intervals(a), blocking_intervals(b)))
    assert rho == geometric == direct == literature_overlap(a, b)
    assert Q(1, 28) <= rho <= Q(1, 4)
    cutoff = (Q(5, 8) - rho * rho) / (rho * LENGTH)
    return {"reduced_pair": [a, b], "overlap_fraction": rho,
            "union_fraction": Q(1, 2) - rho,
            "strict_g_cutoff_if_u_v_at_least_g": cutoff,
            "first_sufficient_integer_g": cutoff.numerator // cutoff.denominator + 1,
            "geometric_formula": geometric, "direct_interval_overlap": direct,
            "perarnau_serra_formula": literature_overlap(a, b)}


def local_check(label, pair, other):
    A, B = pair
    u, v = other
    speeds = (*CORE, A, B, u, v)
    assert len(set(speeds)) == N - 1 and min(speeds) > 0
    g = gcd(A, B)
    a, b = A // g, B // g
    rho = overlap(a, b)
    bad_A, bad_B = blocking_intervals(A), blocking_intervals(B)
    # Direct full-cycle and single-period measurements check scale invariance.
    pair_bad = intersect(bad_A, bad_B)
    assert duration(pair_bad) == rho
    assert duration(intersect(pair_bad, ((Q(0), Q(1, g)),))) == rho / g
    local_pair_overlap = duration(intersect(pair_bad, (J,)))
    local_pair_union = (duration(intersect(bad_A, (J,)))
                        + duration(intersect(bad_B, (J,))) - local_pair_overlap)
    p = Q(1, 2) - rho
    union_upper = p * LENGTH + p * (1 - p) / g
    assert local_pair_union <= union_upper
    individual = {w: duration(intersect(blocking_intervals(w), (J,))) for w in other}
    assert all(individual[w] <= LENGTH / 4 + Q(3, 16 * w) for w in other)
    allowed = intersect(feasible_intervals(speeds, DELTA), (J,))
    clear = duration(allowed)
    bound = clear_bound(rho, g, u, v)
    assert clear >= LENGTH - local_pair_union - sum(individual.values()) >= bound
    assert clear > 0
    # A separate affine phase certificate validates a whole chosen interval.
    witness_interval = max(allowed, key=lambda ab: ab[1] - ab[0])
    phases = phase_certificate(speeds, witness_interval)
    t = sum(witness_interval) / 2
    distances = {str(w): circular_distance(w * t) for w in speeds}
    assert min(distances.values()) > DELTA
    old_distance = min(circular_distance(w * Q(6, 17)) for w in speeds)
    return {"label": label, "pair": pair, "other_two": other,
            "relative_speeds": speeds, "gcd": g, "reduced_pair": [a, b],
            "joint_pattern_period": Q(1, g), "global_pair_overlap": rho,
            "pair_overlap_in_J": local_pair_overlap, "pair_union_in_J": local_pair_union,
            "pair_union_upper_bound": union_upper, "other_blocking_in_J": individual,
            "clear_lower_bound": bound, "actual_clear_duration_in_J": clear,
            "allowed_intervals_in_J": allowed, "witness_interval": witness_interval,
            "affine_phase_certificate": phases,
            "witness": {"time": t, "distances": distances, "minimum": min(distances.values())},
            "old_time_6_17_minimum": old_distance}


def main():
    assert LENGTH == Q(3, 32)
    core_certificate = phase_certificate(CORE, J)
    ratios = [ratio_check(a, b) for a, b in RATIOS]
    # A proven reduction, not an exploratory scan: ab>=10 implies rho>=3/80.
    small_pairs = tuple((a, b) for a in range(1, 4) for b in range(a + 1, 10)
                        if a * b < 10 and gcd(a, b) == 1)
    assert small_pairs == tuple((1, b) for b in range(2, 10)) + ((2, 3),)
    minimum = min(overlap(a, b) for a, b in small_pairs)
    assert minimum == Q(1, 28)
    assert [(a, b) for a, b in small_pairs if overlap(a, b) == minimum] == [(1, 7)]
    assert Q(1, 16) - Q(1, 4 * 10) == Q(3, 80) > minimum
    universal_bound = clear_bound(minimum, 187, 187, 187)
    assert universal_bound == Q(15, 1172864) > 0
    cases = [local_check(*case) for case in CASES]
    lookup = {row["label"]: row for row in cases}
    for label in ("doubled", "triple", "three_to_two", "minimum_overlap_ratio"):
        assert lookup[label]["clear_lower_bound"] > 0
    assert lookup["perturbed_double"]["clear_lower_bound"] < 0
    assert lookup["doubled"]["pair_overlap_in_J"] == Q(11, 896)
    assert lookup["perturbed_double"]["pair_overlap_in_J"] == Q(9, 3616)
    assert lookup["doubled"]["actual_clear_duration_in_J"] == Q(53, 1792)
    assert lookup["perturbed_double"]["actual_clear_duration_in_J"] == Q(6193, 260352)
    assert lookup["doubled"]["old_time_6_17_minimum"] == Q(4, 17)
    assert lookup["perturbed_double"]["old_time_6_17_minimum"] == Q(2, 17)
    dependencies = ("scripts/analyze_speed_ratios.py", "lonely_runner/checker.py",
                    "scripts/analyze_blocking_overlaps.py", "scripts/analyze_local_overlap.py",
                    "scripts/analyze_two_variable_speeds.py")
    data = {
        "date": "2026-09-24", "base_commit": BASE_COMMIT,
        "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in dependencies},
        "scope": "Eight total runners, common start, selected stationary reference, positive distinct integer relative speeds, threshold fixed at 1/8.",
        "core": CORE, "interval_J": J, "length_J": LENGTH,
        "core_phase_certificate": core_certificate, "prescribed_ratios": ratios,
        "uniform_pair_overlap_argument": {"finite_remainder_ab_less_than_10": small_pairs,
            "minimum_fraction": minimum, "unique_reduced_minimizer": [1, 7],
            "ab_at_least_10_lower_bound": Q(3, 80)},
        "general_local_bound": "rho*L-(1/4-rho^2)/g-3/(16u)-3/(16v)",
        "ratio_free_sufficient_family": {"conditions": "gcd(A,B)>=187 and u,v>=187; all seven speeds 1,4,5,A,B,u,v distinct",
            "uniform_clear_duration_lower_bound": universal_bound},
        "prescribed_full_configurations": cases,
        "verification_counts": {"reduced_ratio_crosschecks": len(ratios),
            "finite_remainder_pairs": len(small_pairs), "full_configuration_checks": len(cases),
            "affine_interval_certificates_including_core": len(cases) + 1},
        "limitations": "Known pairwise formula reproduced. Local-family argument is unreviewed, with no novelty claim. Insufficient lower bounds do not imply coverage; zero duration does not exclude valid equality points. No general four-blocker or all-reference conclusion.",
    }
    (ROOT / "experiments/speed_ratios.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"ratios": ratios, "local_cases": [{k: row[k] for k in
        ("label", "gcd", "global_pair_overlap", "pair_overlap_in_J", "clear_lower_bound",
         "actual_clear_duration_in_J", "witness")} for row in cases],
        "uniform_clear_bound": universal_bound, "counts": data["verification_counts"]}, indent=2, default=str))


if __name__ == "__main__":
    main()
