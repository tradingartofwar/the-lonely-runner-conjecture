"""Independent closed-interval check of the contact audit's physical controls."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from lonely_runner.checker import feasible_intervals


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = HERE / "contact_moments.json"
    data = json.loads(source.read_text())
    a, b = map(F, data["window"])
    cases = data["physical_controls"]+data["constructive_boundary_family"]["controls"]
    rows = []
    for case in cases:
        speeds = (*data["core"], *case["fixed_blockers"], case["y"])
        intervals = feasible_intervals(speeds, F(1, 8))
        clipped = [(max(a, l), min(b, r)) for l, r in intervals if max(a, l) <= min(b, r)]
        assert clipped == [tuple(map(F, I)) for I in case["components"]]
        assert sum((r-l for l, r in clipped), F(0)) == F(case["clear_duration"]) == 0
        assert intervals  # Empty J is not empty throughout the full period.
        rows.append({"fixed_blockers": case["fixed_blockers"], "y": case["y"],
                     "components_in_J": clipped, "full_period_has_solution": True})
    result = {"date": "2026-09-27", "cases": rows,
              "dependencies_sha256": {"check_contact_moments.py": sha(HERE / "check_contact_moments.py"),
                                      "contact_moments.json": sha(source),
                                      "crosscheck_contact_moments.py": sha(Path(__file__)),
                                      "lonely_runner/checker.py": sha(ROOT / "lonely_runner/checker.py")}}
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads((HERE / "contact_checker_comparison.json").read_text())
        print("PASS: all 15 local component lists agree with the existing safe-interval checker; each configuration has solutions elsewhere in the full period.")
    else:
        assert not sys.argv[1:]
        print(encoded, end="")


if __name__ == "__main__":
    main()
