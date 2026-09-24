"""Exact certificates for one unbounded, selected-reference speed family.

Run: python -m scripts.analyze_variable_speed_family
The general argument is in notes/VARIABLE_SPEED_FAMILY.md. Finite examples
check its arithmetic; they do not replace the argument over all integers.
"""

import hashlib
import json
from fractions import Fraction as Q
from math import lcm
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals


ROOT = Path(__file__).resolve().parents[1]
CORE = (1, 4, 5, 6, 7, 11)
N = 8  # Original total, retained when examining only the six fixed constraints.
DELTA = Q(1, N)
LEFT, RIGHT = Q(17, 56), Q(5, 16)
BASE_COMMIT = "71f3c8b4929aa703d394d9816fc015bbe4374f5f"


def witness(w: int) -> tuple[Q, str]:
    """One certified time for every positive integer w distinct from CORE.

    No loop over time or over the magnitude of w is needed. The number of
    arithmetic operations is bounded; integer bit-operation costs still grow.
    """
    if type(w) is not int or w <= 0 or w in CORE:
        raise ValueError("w must be a positive integer distinct from the core")
    if w % 8:
        return Q(1, 8), "old_eighth"
    if w % 56:
        return LEFT, "seventh_residue_at_left"
    return LEFT + Q(1, 8 * w), "exit_after_left_collision"


def witness_record(w: int) -> dict:
    t, branch = witness(w)
    distances = {str(v): circular_distance(v * t) for v in (*CORE, w)}
    assert len(distances) == N - 1
    assert min(distances.values()) >= DELTA
    if branch == "exit_after_left_collision":
        assert w * LEFT == 17 * (w // 56)
        assert LEFT < t < RIGHT
        assert distances[str(w)] == DELTA
        assert min(distances[str(v)] for v in CORE) > DELTA
    return {"w": w, "time": str(t), "branch": branch,
            "distances": {v: str(d) for v, d in distances.items()},
            "minimum": str(min(distances.values()))}


def main():
    width = RIGHT - LEFT
    assert width == Q(1, 112)
    allowed = feasible_intervals(CORE, DELTA)
    assert (LEFT, RIGHT) in allowed

    # Independently certify the WHOLE closed interval: each unwrapped phase
    # stays in one unit cell and its endpoint phases lie in [1/8, 7/8].
    # Affinity then certifies every intervening time, not a sampled time grid.
    phase_rows = []
    for v in CORE:
        start, end = v * LEFT, v * RIGHT
        integer = start.numerator // start.denominator
        assert integer == end.numerator // end.denominator
        low, high = start - integer, end - integer
        assert DELTA <= low < high <= 1 - DELTA
        phase_rows.append({"speed": v, "integer_cell": integer,
                           "phase_left": str(low), "phase_right": str(high)})

    # First argument: exclude nonmultiples of 8 at 1/8; any blocker covering
    # the closed interval must have open-window width 1/(4w) > 1/112.
    residues8 = [circular_distance(Q(r, 8)) for r in range(8)]
    assert residues8[0] == 0 and min(residues8[1:]) == DELTA
    assert min(circular_distance(Q(v, 8)) for v in CORE) == DELTA
    strict_cap = 2 * DELTA / width
    assert strict_cap == 28
    candidates = [w for w in range(1, int(strict_cap)) if w % 8 == 0]
    assert candidates == [8, 16, 24]
    finite_checks = []
    for w in candidates:
        item = witness_record(w)
        assert Q(item["time"]) == LEFT
        # Separate interval-intersection method checks the explicit witness.
        full_allowed = feasible_intervals((*CORE, w), DELTA)
        assert any(a <= LEFT <= b for a, b in full_allowed)
        item["interval_crosscheck"] = True
        finite_checks.append(item)

    # Sharper argument: w=8m gives phase 17m/7 at LEFT. Multiplication by 17
    # permutes the nonzero residues modulo 7. Only 7|m can block this time.
    residues7 = [circular_distance(8 * m * LEFT) for m in range(7)]
    assert residues7 == [Q(0), Q(3, 7), Q(1, 7), Q(2, 7),
                         Q(2, 7), Q(1, 7), Q(3, 7)]
    assert min(residues7[1:]) == Q(1, 7) > DELTA
    # For every remaining w=56m, m>=1, this bounds the delay to leave a
    # collision at LEFT. Monotonicity in m is the unbounded step in the note.
    largest_exit_delay = DELTA / 56
    assert largest_exit_delay == Q(1, 448) < width

    # Two deliberate counterchecks against tempting shortcuts.
    blocking13 = ((Q(4) - DELTA) / 13, (Q(4) + DELTA) / 13)
    assert blocking13[0] < LEFT < RIGHT < blocking13[1]
    assert min(circular_distance(Q(v, 8)) for v in (*CORE, 13)) == DELTA
    both_endpoints = [circular_distance(112 * t) for t in (LEFT, RIGHT)]
    assert both_endpoints == [Q(0), Q(0)]
    interior112 = witness_record(112)
    assert Q(interior112["time"]) == Q(39, 128)

    fixed_times = (Q(1, 8), LEFT, RIGHT, Q(4, 13))
    common_multiple = lcm(*(t.denominator for t in fixed_times))
    assert common_multiple == 1456
    assert all(circular_distance(common_multiple * t) == 0 for t in fixed_times)

    # Prescribed diagnostic inputs, not a scan or evidence for an infinite tail.
    examples = [witness_record(w) for w in (2, 8, 16, 24, 32, 56, 112,
                                           common_multiple, 56 * 10**12)]
    data = {
        "date": "2026-09-24", "base_commit": BASE_COMMIT,
        "checker_sha256": hashlib.sha256((ROOT / "lonely_runner/checker.py").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "Elementary argument with exact certificates; independent proof review outstanding; no novelty claim",
        "scope": {"n": N, "selected_reference_speed": 0, "core_relative_speeds": CORE,
                  "variable_speed": "any positive integer w not in CORE",
                  "threshold": str(DELTA), "starts": "all at the same position"},
        "core_allowed_intervals": [[str(a), str(b)] for a, b in allowed],
        "certified_interval": {"left": str(LEFT), "right": str(RIGHT),
                               "width": str(width), "phase_endpoint_certificate": phase_rows},
        "finite_reduction": {"necessary_divisor": 8, "necessary_strict_upper_bound": str(strict_cap),
                             "remaining_candidates": candidates, "checks": finite_checks,
                             "unbounded_step": "A connected closed interval cannot be covered by disjoint open blocking windows unless one window strictly contains it"},
        "sharper_reduction": {"modulo8_distances": list(map(str, residues8)),
                              "modulo7_distances_at_left_for_w_8m": list(map(str, residues7)),
                              "necessary_divisor_to_block_both_times": 56,
                              "largest_exit_delay_after_left": str(largest_exit_delay),
                              "witness_formula": ["8 does not divide w: t=1/8",
                                                  "8 divides w but 56 does not: t=17/56",
                                                  "56 divides w: t=17/56+1/(8w)"]},
        "counterchecks": {"w13_covers_entire_interval": list(map(str, blocking13)),
                          "w13_still_allows_old_eighth": True,
                          "w112_blocks_both_endpoints": list(map(str, both_endpoints)),
                          "w112_interior_witness": interior112,
                          "four_fixed_rational_times": list(map(str, fixed_times)),
                          "speed_colliding_at_all_four": common_multiple},
        "prescribed_examples": examples,
        "limitations": "Selected reference only; integer one-parameter family; no general LRC, real-speed family, all-reference, maximal-separation, or tightness classification claim",
    }
    output = ROOT / "experiments/variable_speed_family.json"
    output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"candidate_speeds": candidates, "sharper_necessary_divisor": 56,
                      "certified_interval": [str(LEFT), str(RIGHT)],
                      "examples": [{k: row[k] for k in ("w", "time", "minimum", "branch")}
                                   for row in examples]}, indent=2))


if __name__ == "__main__":
    main()
