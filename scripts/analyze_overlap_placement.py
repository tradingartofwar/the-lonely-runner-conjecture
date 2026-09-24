"""Local overlap certificates and a near-doubling proof candidate.

Run: python -m scripts.analyze_overlap_placement
Seven prescribed configurations; no parameter scan or time grid.
See notes/OVERLAP_PLACEMENT.md for the unbounded argument and review status.
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
BASE_COMMIT = "14b46f0dbb099168b84ec5dca4723dd8c0e5a99f"
CORE = (1, 4, 5)
N = 8
D = Q(1, N)
J = (Q(9, 32), Q(3, 8))
L = J[1] - J[0]
CASES = (
    ("doubled_control", (56, 112, 64, 72), (56, 112)),
    ("near_double_56", (56, 113, 64, 72), (56, 113)),
    ("tight_control", (6, 7, 11, 13), (6, 13)),
    ("tight_replacement_control", (6, 7, 8, 11), (8, 11)),
    ("below_coarse_cutoff", (309, 619, 320, 328), (309, 619)),
    ("at_coarse_cutoff", (310, 621, 320, 328), (310, 621)),
    ("above_coarse_cutoff", (320, 641, 328, 336), (320, 641)),
)


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def primitive(z):
    """Integral of the unit-period blocking indicator from 0 to z>=0."""
    assert z >= 0
    m = floor(z)
    r = z - m
    return 2 * D * m + min(r, D) + max(Q(0), r - (1 - D))


def single_duration(v):
    return (primitive(v * J[1]) - primitive(v * J[0])) / v


def drift_windows(q):
    """Exact positive-length overlap pieces for q,2q+1 on J.

    Endpoint pairs represent lengths only; blocking inequalities are strict.
    This construction uses the affine relation, not the general intersection.
    """
    alpha, beta = J
    lo = floor(((2 * q + 1) * alpha - D) / 2)
    hi = ceil(q * beta + D)
    rows = []
    for j in range(lo, hi + 1):
        a = max(alpha, (j - D) / q)
        b = min(beta, (2 * j + D) / (2 * q + 1))
        if a < b:
            t = (a + b) / 2
            x = q * t - j
            assert (2 * q + 1) * t - 2 * j == 2 * x + t
            assert abs(x) < D and abs(2 * x + t) < D
            rows.append({"meeting_index_j": j, "interval": (a, b), "width": b - a})
    return rows


def overlap_floor(q):
    return (q * L * L - L) / (2 * (2 * q + 1))


def uniform_clear_floor(q):
    return Q(9 * q * q - 2784 * q - 1152, 2048 * q * (2 * q + 1))


def boundary_measure(blockers):
    """Independent constant-status cells, with strict distance predicates."""
    cuts = sorted({*J, *(x for v in blockers for ab in blocking_intervals(v)
                         for x in ab if J[0] < x < J[1])})
    histogram = [Q(0)] * 5
    for a, b in zip(cuts, cuts[1:]):
        t = (a + b) / 2
        count = sum(circular_distance(v * t) < D for v in blockers)
        histogram[count] += b - a
    assert sum(histogram) == L
    return histogram


def analyze(label, blockers, pair):
    speeds = (*CORE, *blockers)
    assert len(set(speeds)) == N - 1
    individual = {str(v): single_duration(v) for v in blockers}
    for v in blockers:
        assert individual[str(v)] == duration(intersect(blocking_intervals(v), (J,)))
    total = sum(individual.values())
    excess = total - L
    overlap_parts = intersect(intersect(blocking_intervals(pair[0]), blocking_intervals(pair[1])), (J,))
    overlap = duration(overlap_parts)
    certificate = overlap - excess
    allowed = intersect(feasible_intervals(speeds, D), (J,))
    clear = duration(allowed)
    histogram = boundary_measure(blockers)
    redundancy = sum(max(m - 1, 0) * width for m, width in enumerate(histogram))
    assert histogram[0] == clear == redundancy - excess
    assert sum(m * width for m, width in enumerate(histogram)) == total
    assert redundancy >= overlap and clear >= certificate
    row = {"label": label, "four_blockers": blockers, "selected_pair": pair,
           "individual_blocking_durations": individual, "total_blocking_T": total,
           "excess_E": excess, "selected_pair_overlap": overlap,
           "selected_pair_overlap_intervals": overlap_parts,
           "single_pair_clear_lower_bound": certificate,
           "actual_clear_duration": clear, "redundancy_R": redundancy,
           "blocking_histogram": histogram, "allowed_intervals_in_J": allowed}
    if clear > 0:
        interval = max(allowed, key=lambda ab: ab[1] - ab[0])
        phases = phase_certificate(speeds, interval)
        t = sum(interval) / 2
        distances = {str(v): circular_distance(v * t) for v in speeds}
        assert min(distances.values()) > D
        row.update({"certified_clear_interval": interval, "affine_phase_certificate": phases,
                    "witness": {"time": t, "distances": distances, "minimum": min(distances.values())}})
    else:
        assert label == "tight_control"
        assert allowed == ((Q(3, 8), Q(3, 8)),)
        global_allowed = feasible_intervals(speeds, D)
        assert global_allowed == tuple((Q(k, 8), Q(k, 8)) for k in (1, 3, 5, 7))
        distances = {str(v): circular_distance(v * Q(3, 8)) for v in speeds}
        assert min(distances.values()) == D
        row.update({"global_allowed_singletons": global_allowed,
                    "equality_witness": {"time": Q(3, 8), "distances": distances}})
    if pair[1] == 2 * pair[0] + 1:
        q = pair[0]
        assert gcd(*pair) == 1
        windows = drift_windows(q)
        assert tuple(r["interval"] for r in windows) == tuple((a, b) for a, b in overlap_parts if a < b)
        low = overlap_floor(q)
        # Full windows alone certify the analytic lower bound; omit any clipped first piece.
        full = [r for r in windows if r["interval"][0] == (r["meeting_index_j"] - D) / q]
        assert overlap >= sum((r["width"] for r in full), Q(0)) >= low
        from_period_errors = low - Q(3, 16) * (Q(3, q) + Q(1, 2 * q + 1))
        assert from_period_errors == uniform_clear_floor(q)
        assert min(v for v in blockers if v not in pair) >= q
        assert clear >= uniform_clear_floor(q)
        row["near_doubling"] = {"q": q, "overlap_windows_from_affine_relation": windows,
            "overlap_lower_bound": low, "uniform_clear_lower_bound": uniform_clear_floor(q)}
    return row


def main():
    rows = [analyze(*case) for case in CASES]
    lookup = {row["label"]: row for row in rows}
    target = lookup["near_double_56"]
    widths = [r["width"] for r in target["near_doubling"]["overlap_windows_from_affine_relation"]]
    assert widths == [Q(k, 50624) for k in (41, 33, 25, 17, 9, 1)]
    assert target["excess_E"] == Q(1045, 911232)
    assert target["selected_pair_overlap"] == Q(9, 3616)
    assert target["single_pair_clear_lower_bound"] == Q(1223, 911232) > 0
    assert target["actual_clear_duration"] == Q(6193, 260352)
    assert lookup["tight_control"]["single_pair_clear_lower_bound"] < 0
    assert lookup["tight_control"]["redundancy_R"] == Q(1445, 96096)
    assert lookup["tight_replacement_control"]["single_pair_clear_lower_bound"] > 0
    assert uniform_clear_floor(309) < 0 < uniform_clear_floor(310)
    assert uniform_clear_floor(310) == Q(59, 32855040)
    assert 9 * 310**2 - 2784 * 310 - 1152 == 708
    assert 18 * 310 - 2775 > 0  # Difference P(q+1)-P(q); increasing thereafter.
    dependencies = ("scripts/analyze_overlap_placement.py", "lonely_runner/checker.py",
                    "scripts/analyze_blocking_overlaps.py", "scripts/analyze_local_overlap.py",
                    "scripts/analyze_two_variable_speeds.py")
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
        "claim_status": {"finite_certificates": "OBSERVED", "family_argument": "HYPOTHESIS: proof candidate awaiting independent review", "general_coverage": "OPEN"},
        "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in dependencies},
        "scope": "Eight total common-start runners, selected reference 0, positive distinct integer relative speeds, fixed target 1/8.",
        "core": CORE, "J": J, "length_J": L, "core_phase_certificate": phase_certificate(CORE, J),
        "family": {"velocities": "0,1,4,5,q,2q+1,u,v", "conditions": "q>=310, u,v>=q, all distinct positive integer relative speeds",
            "clear_duration_lower_bound": "(9q^2-2784q-1152)/(2048q(2q+1))", "at_310": uniform_clear_floor(310),
            "review_status": "Unreviewed complete argument in OVERLAP_PLACEMENT.md; no novelty claim."},
        "cases": rows,
        "verification_counts": {"prescribed_configurations": len(rows), "single_duration_crosschecks": 4 * len(rows),
            "near_doubling_window_crosschecks": 5, "affine_clear_interval_certificates_including_core": 7,
            "tight_global_equality_points": 4},
        "limitations": "One-pair lower bounds are sufficient, not necessary. Negative or zero bounds do not imply full coverage. Equality points retained. No all-reference, arbitrary-four-speed, or new-theorem claim.",
    }
    (ROOT / "experiments/overlap_placement.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"cases": [{k: row[k] for k in ("label", "excess_E", "selected_pair_overlap", "single_pair_clear_lower_bound", "actual_clear_duration")} for row in rows], "verification_counts": data["verification_counts"], "family": data["family"]}, indent=2, default=str))


if __name__ == "__main__":
    main()
