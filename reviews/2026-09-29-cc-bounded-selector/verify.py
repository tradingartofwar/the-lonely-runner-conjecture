"""Exact endpoint/coverage certificates and the predeclared physical controls.

Run from any directory: python .../verify.py > .../verification.json
Only q=2,...,25 receive direct physical evaluations. No optimizer is run.
"""

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from selector import ROWS, SEGMENTS, THRESHOLD, ceiling, select, select_formula

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ATLAS = ROOT / "reviews/2026-09-29-cc-six-seven-transfer/verification.json"
ARCHIVE = ROOT / "reviews/2026-09-29-ltcm-ultra-review/physical_check.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    return obj


def main():
    atlas = json.loads(ATLAS.read_text())
    assert tuple(map(tuple, atlas["rows"])) == ROWS
    segment_checks = []
    for s in SEGMENTS:
        p = atlas["parents"][s.parent]
        assert tuple(p["labels"]) == s.labels[:6]
        vertices = [tuple(map(F, v)) for v in p["vertices"]]
        endpoints = [(x, s.y(x), THRESHOLD) for x in (s.low_x, s.high_x)]
        ids = [vertices.index(v) for v in endpoints]
        assert sorted(ids) in p["edges"]
        endpoint_checks = []
        for x, y, z in endpoints:
            for _, normal, bound in p["constraints"]:
                assert sum(a * v for a, v in zip(map(F, normal), (x, y, z))) <= F(bound)
            phases = [a * x + b * y - m for (a, b), m in zip(ROWS, s.labels)]
            margins = [(f - THRESHOLD, 1 - THRESHOLD - f) for f in phases]
            assert all(lo >= 0 and hi >= 0 for lo, hi in margins)
            assert min(min(f, 1 - f) for f in phases) == THRESHOLD
            endpoint_checks.append({"point": (x, y, z), "phases": phases, "band_margins": margins})
        segment_checks.append({"segment": s.name, "parent": s.parent, "edge_indices": ids,
                               "torus_laps": s.labels, "endpoints": endpoint_checks})

    # q>=9: upper-lower-1=(q-9)/12, nonnegative on the stated domain.
    # Coefficients are extracted from the affine orbit endpoint definitions.
    e1 = SEGMENTS[0]
    width_slope = e1.high_x - e1.low_x
    width_intercept = e1.y(e1.low_x) - e1.y(e1.high_x)
    assert width_slope == F(1, 12) and width_intercept == F(1, 4)
    assert 9 * width_slope + width_intercept - 1 == 0
    small_coverage = []
    for q in range(2, 9):
        low, high = e1.orbit_interval(q)
        h = ceiling(low)
        success = h <= high
        assert success == (q != 5)
        small_coverage.append({"q": q, "interval": (low, high), "first_integer": h, "accept": success})

    residue_checks = []
    for r in range(8):
        epsilon = (r + 3) // 8
        domain_start = 1 if r in (0, 1) else 0
        success_start = 1 if r in (0, 1, 5) else 0
        # h-L=(8 epsilon-r+4)/8 must lie in [0,1).
        rounding_margin = F(8 * epsilon - r + 4, 8)
        assert 0 <= rounding_margin < 1
        constant = 5 * r - 6 - 24 * epsilon
        assert 16 * success_start + constant >= 0
        excluded = list(range(domain_start, success_start))
        assert all(16 * a + constant < 0 for a in excluded)
        assert [8 * a + r for a in excluded] == ([5] if r == 5 else [])
        residue_checks.append({"residue": r, "epsilon": epsilon,
                               "domain_a_min": domain_start, "primary_a_min": success_start,
                               "h_minus_lower": rounding_margin,
                               "24_times_upper_minus_h": {"slope": 16, "constant": constant,
                                                            "minimum": 16 * success_start + constant},
                               "excluded_q": [8 * a + r for a in excluded]})

    # Select first; consult archived optimum values only afterward.
    selected = [select(q) for q in range(2, 26)]
    archived = {v["q"]: v for v in json.loads(ARCHIVE.read_text())["small_q_results"]}
    physical_checks = []
    for cert in selected:
        q, t, h = cert["q"], cert["time"], cert["h"]
        x, y, z = cert["point"]
        assert t == select_formula(q) and t == x and q * x - y == h
        assert 0 < t <= F(1, 2) and 0 < y < 1
        assert cert["attempts"] == (2 if q == 5 else 1)
        speeds = [a + b * q for a, b in ROWS]
        assert speeds == archived[q]["speeds"]
        times = []
        for time, expected_laps in (
                (t, cert["physical_laps"]),
                (1 - t, tuple(v - 1 - ell for v, ell in zip(speeds, cert["physical_laps"])))):
            positions = [v * time for v in speeds]
            laps = [position.numerator // position.denominator for position in positions]
            phases = [position - lap for position, lap in zip(positions, laps)]
            distances = [min(f, 1 - f) for f in phases]
            assert tuple(laps) == expected_laps
            assert min(distances) == THRESHOLD
            times.append({"time": time, "physical_laps": laps, "phases": phases,
                          "distances": distances, "minimum": min(distances)})
        optimum = F(archived[q]["maximum"])
        assert THRESHOLD <= optimum
        physical_checks.append({"certificate": cert, "physical_checks": times,
                                "comparison_only_archived_maximum": optimum,
                                "selected_time_is_archived_maximizer": str(t) in archived[q]["maximizing_times"]})
    assert select(4)["time"] == F(1, 8)
    assert select(6)["time"] == F(5, 24)
    assert select(5)["time"] == F(25, 56)
    assert select(5)["physical_laps"] == (0, 2, 2, 3, 3, 5, 6)
    out = {
        "status": "PASS: exact certificates supporting an internally checked proof candidate",
        "frozen_base": "326347eafa512d2b49fb12bbcfd9a624a018ef6e",
        "scope": "A_q, selected stationary reference, integer q>=2, one closed 1/8-safe witness",
        "authorship": "Coordinator-authored; not independent review or formal verification",
        "input_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (ATLAS, ARCHIVE)},
        "script_sha256": {p.name: sha(p) for p in (HERE / "selector.py", Path(__file__))},
        "segments": segment_checks,
        "width_certificate": {"domain_q_min": 9, "width_slope": width_slope,
                              "width_intercept": width_intercept, "width_at_9": 1},
        "small_coverage": small_coverage,
        "unbounded_residue_coverage": residue_checks,
        "physical_scope": list(range(2, 26)), "physical_controls": physical_checks,
        "summary": {"fixed_segments": 2, "endpoint_band_inequalities": 56,
                    "unbounded_residue_domains": 8, "primary_failure_q": [5],
                    "physical_q_count": 24, "physical_time_count_with_reflections": 48,
                    "exact_distance_evaluations": 336, "maximum_selection_attempts": 2,
                    "all_selected_separations": "1/8", "new_physical_q_values": 0},
    }
    print(json.dumps(encode(out), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
