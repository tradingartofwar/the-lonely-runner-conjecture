"""Compare archived phase partitions with the existing safe-interval checker."""
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
    source = HERE / "residue_collisions.json"
    data = json.loads(source.read_text())
    a, b = map(F, data["window"])
    cases = [case for pair in data["physical_controls"] for case in pair["cases"]]
    cases += data["zero_duration_cases"]
    rows = []
    for case in cases:
        y = case["y"]
        intervals = feasible_intervals((1, 4, 5, 6, 7, 11, y), F(1, 8))
        clipped = [(max(a, l), min(b, r)) for l, r in intervals if max(a, l) <= min(b, r)]
        assert clipped == [tuple(map(F, I)) for I in case["components"]]
        length = sum((r-l for l, r in clipped), F(0))
        assert length == F(case["clear_duration"])
        rows.append({"y": y, "component_count": len(clipped),
                     "positive_components": sum(l < r for l, r in clipped),
                     "isolated_components": sum(l == r for l, r in clipped), "duration": length})
    result = {"date": "2026-09-27", "cases": rows,
              "dependencies_sha256": {"check_residue_collisions.py": sha(HERE / "check_residue_collisions.py"),
                                      "residue_collisions.json": sha(source),
                                      "crosscheck_residue_controls.py": sha(Path(__file__)),
                                      "lonely_runner/checker.py": sha(ROOT / "lonely_runner/checker.py")}}
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads((HERE / "residue_checker_comparison.json").read_text())
        print("PASS: existing interval-intersection checker agrees on all 12 component lists and durations, including isolated points.")
    else:
        assert not sys.argv[1:]
        print(encoded, end="")


if __name__ == "__main__":
    main()
