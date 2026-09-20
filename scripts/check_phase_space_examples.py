"""Exact checks for the phase-space explanation; three selected comparisons."""

import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import check, circular_distance, feasible_intervals


def main():
    rows = []
    for velocities, target, expected, relation in [
        ([0, 1, 2], Q(1, 3), "boundary_only", [2, -1]),
        ([0, 1, 3], Q(1, 3), "enters_interior", [3, -1]),
        ([0, 1, 2], Q(2, 5), "misses_raised_target", [2, -1]),
    ]:
        result = check(velocities, reference=0, threshold=target)
        assert result["maximum"]["crosschecked_with_intervals"]
        speeds = velocities[1:]
        intervals = feasible_intervals(speeds, target)
        maximum = Q(result["maximum"]["separation"])
        status = ("misses_raised_target" if not intervals else
                  "boundary_only" if maximum == target else "enters_interior")
        assert status == expected
        assert sum(a*b for a, b in zip(relation, speeds)) == 0
        witnesses = []
        for left, right in intervals:
            t = (left + right) / 2
            phases = [(v*t) % 1 for v in speeds]
            distances = [circular_distance(v*t) for v in speeds]
            # Independently check the box description at each interval midpoint.
            assert all(target <= x <= 1-target for x in phases)
            assert all(d >= target for d in distances)
            assert sum(a*x for a, x in zip(relation, phases)).denominator == 1
            witnesses.append({"time": str(t), "phases": list(map(str, phases)),
                              "distances": list(map(str, distances))})
        rows.append({"actual_speeds": velocities, "reference_speed": 0,
                     "relative_speeds": speeds, "target": str(target),
                     "conjecture_target": "1/3", "status": status,
                     "maximum": str(maximum), "relation_coefficients": relation,
                     "feasible_intervals": [[str(a), str(b)] for a,b in intervals],
                     "witnesses": witnesses})
    assert rows[0]["feasible_intervals"] == [["1/3", "1/3"], ["2/3", "2/3"]]
    assert rows[1]["feasible_intervals"] == [["4/9", "5/9"]]
    assert rows[2]["feasible_intervals"] == []
    payload = {"date": "2026-09-20", "scope": "Three fixed selected-reference comparisons; no general proof",
               "cases": rows}
    path = Path(__file__).resolve().parents[1]/"experiments/phase_space_examples.json"
    path.write_text(json.dumps(payload, indent=2)+"\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
