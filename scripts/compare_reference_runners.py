"""Compare every reference runner in 13 explicit configurations.

Run: python -m scripts.compare_reference_runners
These are selected examples and symmetry checks, not an exhaustive census.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import check


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "consecutive_4": list(range(1, 5)),
    "consecutive_8": list(range(1, 9)),
    "consecutive_12": list(range(1, 13)),
    "uneven_5": [1, 2, 4, 5, 8],
    "uneven_6": [1, 2, 4, 5, 6, 10],
    "uneven_8_single": [1, 2, 3, 4, 5, 6, 8, 13],
    "uneven_8_double": [1, 2, 5, 6, 7, 8, 12, 14],
    "uneven_14": [1, *range(2, 13), 14, 25],
    "reflected_8": [1, 6, 8, 9, 10, 11, 12, 13],
    "middle_tight_8": [1, 2, 3, 4, 8, 9, 11, 16],
    "no_tight_3": [1, 2, 5],
    "no_tight_4": [1, 2, 5, 11],
    "no_tight_8": [1, 2, 4, 8, 16, 32, 64, 128],
}


def main():
    cases = []
    for label, velocities in CASES.items():
        rows = []
        for index, speed in enumerate(velocities):
            result = check(velocities, reference=index)
            maximum = result["maximum"]
            assert maximum["crosschecked_with_intervals"]
            rows.append({"speed": speed, "speed_rank": index + 1,
                         "maximum": maximum["separation"], "tight": maximum["tight"],
                         "excess_over_threshold": maximum["excess_over_conjecture_threshold"],
                         "peak_times": maximum["times_original"],
                         "crosschecked": True})
        least_best = min(Q(row["maximum"]) for row in rows)
        cases.append({"label": label, "n": len(velocities), "actual_speeds": velocities,
                      "threshold": str(Q(1, len(velocities))),
                      "tight_speeds": [row["speed"] for row in rows if row["tight"]],
                      "smallest_best_gap": str(least_best),
                      "most_constrained_speeds": [row["speed"] for row in rows if Q(row["maximum"]) == least_best],
                      "runners": rows})

    by_name = {case["label"]: case for case in cases}
    original = by_name["uneven_8_single"]
    reflected = by_name["reflected_8"]
    middle = by_name["middle_tight_8"]
    assert original["tight_speeds"] == [1]
    assert reflected["tight_speeds"] == [13]
    assert middle["tight_speeds"] == [4]
    assert sorted(14-v for v in original["actual_speeds"]) == reflected["actual_speeds"]
    for row in original["runners"]:
        mirror = next(r for r in reflected["runners"] if r["speed"] == 14-row["speed"])
        assert (row["maximum"],row["peak_times"]) == (mirror["maximum"],mirror["peak_times"])
    assert sorted(abs(v-4) for v in middle["actual_speeds"] if v != 4) == [1,2,3,4,5,7,12]
    mid_row = next(r for r in middle["runners"] if r["speed"] == 4)
    assert mid_row["peak_times"] == original["runners"][0]["peak_times"]
    assert all(not by_name[name]["tight_speeds"] for name in ("no_tight_3","no_tight_4","no_tight_8"))

    output = {
        "date": "2026-09-19",
        "base_commit": "f4cf10452071896eb1c63d1a1110a9caad55d4c4",
        "checker_sha256": hashlib.sha256((ROOT/'lonely_runner/checker.py').read_bytes()).hexdigest(),
        "scope": f"{len(cases)} explicit integer-speed configurations; all {sum(c['n'] for c in cases)} references; full relative cycles",
        "definition": "For each runner maximize nearest-neighbor separation over time; then minimize those maxima over runners",
        "limitations": "No exhaustive classification, prevalence estimate, novelty claim, or general conjecture proof",
        "cases": cases,
        "symmetry_checks": {
            "reflection": "v -> 14-v reverses every relative velocity, preserving every corresponding pairwise distance for all times",
            "middle_runner": "Only the selected runner's distance curves are preserved by independently changing relative signs; other runners were rechecked",
        },
    }
    (ROOT/'experiments/reference_runner_roles.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({"configurations":len(cases), "references":sum(c['n'] for c in cases),
                      "results":[{k:c[k] for k in ('label','tight_speeds','smallest_best_gap','most_constrained_speeds')} for c in cases]},indent=2))


if __name__ == '__main__':
    main()
