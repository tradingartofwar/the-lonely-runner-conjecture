#!/usr/bin/env python3
"""Small exact controls for the strategy review; no search campaign.

Run from any directory: python -B /path/to/strategy_check.py [--check]
The analytic all-parameter arguments are in strategy.md. These finite checks
do not certify their quantifiers. Uses the existing checker as a countercheck.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import lcm
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from lonely_runner.checker import check, circular_distance as distance


def minimum(speeds, t):
    return min(distance(Q(v) * t) for v in speeds)


def build():
    slow = (1, 3, 4, 5, 10, 28)
    t0 = Q(11, 64)
    assert minimum(slow, t0) == Q(9, 64)
    rows = []
    for h in (1, 2, 3, 4, 5, 10, 100, 10**12):
        y = 1680 * h
        # Round y*t0 - 1/2 to nearest integer, ties upwards.
        z = y * t0
        m = z.numerator // z.denominator
        t = (Q(m) + Q(1, 2)) / y
        bound = Q(9, 64) - Q(14, y)
        actual = minimum((*slow, y), t)
        assert abs(t - t0) <= Q(1, 2 * y)
        assert distance(y * t) == Q(1, 2)
        assert actual >= bound >= Q(127, 960) > Q(1, 8)
        rows.append({"h": h, "y": y, "witness": str(t),
                     "minimum": str(actual), "lower_bound": str(bound)})

    menu = (Q(9, 32), Q(3, 8), Q(11, 64))
    killer = lcm(1680, *(t.denominator for t in menu))
    assert killer == 6720
    assert all(distance(killer * t) == 0 for t in menu)

    perturbations = []
    for n in (1, 3, 5, 11, 101):
        speeds = (Q(1), Q(2) + Q(1, n))
        t = Q(n, 2)
        assert minimum(speeds, t) == Q(1, 2)
        crosscheck = check((0, *speeds))
        assert crosscheck["maximum"]["separation"] == "1/2"
        perturbations.append({"N": n, "speed": str(speeds[1]),
                              "half_lap_witness": str(t),
                              "maximum": crosscheck["maximum"]["separation"],
                              "necessary_time_for_gap_2_5": str(Q(n, 15))})
    limiting = check((0, 1, 2))
    assert limiting["maximum"]["separation"] == "1/3"
    references = []
    for r in range(3):
        c = check((0, 1, 2), reference=r)
        references.append({"reference": r, "maximum": c["maximum"]["separation"],
                           "constraint_speeds": c["normalization"]["constraint_speeds"],
                           "threshold": c["threshold"]})
    assert [r["maximum"] for r in references] == ["1/3", "1/2", "1/3"]

    diagonal = check(tuple(range(8)))
    assert diagonal["maximum"]["separation"] == "1/8"
    diagonals = []
    for q in (8, 100, 10**12):
        offsets = [v - q for v in (4, 5, 6, 7)]
        a = max(map(abs, offsets))
        assert [q + x for x in offsets] == [4, 5, 6, 7]
        assert not q > 2 * a
        diagonals.append({"q": q, "offsets": offsets, "A": a,
                          "satisfies_q_greater_than_2A": False})

    # For a relation using y at least once, total other coefficient mass is
    # <=16, so the slow terms can have absolute sum at most 28*16.
    assert 1680 > 28 * 16
    deps = (Path(__file__), ROOT / "lonely_runner" / "checker.py")
    return {
        "baseline": "e94a87f650264826569cae63412c43a5175f5ae4",
        "scope": "Finite exact controls plus separately written analytic arguments",
        "sha256": {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in deps},
        "adaptive_global_witnesses": rows,
        "fixed_menu": {"times": list(map(str, menu)), "killer_speed": killer},
        "rational_perturbations": perturbations,
        "limiting_maximum": limiting["maximum"]["separation"],
        "reference_change": references,
        "coefficient_diagonal": diagonals,
        "diagonal_maximum": diagonal["maximum"]["separation"],
        "short_relation_budget": 17,
        "slow_relation_cancellation_bound": 448,
    }


if __name__ == "__main__":
    result = build()
    path = Path(__file__).with_suffix(".json")
    if "--check" in sys.argv:
        assert json.loads(path.read_text()) == result, "archive differs"
        print("Strategy controls passed; archive matches.")
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
        print("Wrote strategy_check.json.")
