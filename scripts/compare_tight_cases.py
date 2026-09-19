"""Reproduce the bounded 4/8/12-runner comparison using exact arithmetic.

Run from the repository root: python -m scripts.compare_tight_cases
This is a finite study of specified inputs, not an exhaustive classification.
"""

import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

from lonely_runner.checker import check, circular_distance, feasible_intervals


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments" / "tight_cases_4_8_12.json"


def interval_status(intervals):
    if not intervals:
        return "below_threshold"
    # A finite lower envelope of affine pieces with nonzero slopes cannot
    # equal a constant on an interval. Thus positive width implies excess.
    return "tight" if all(a == b for a, b in intervals) else "above_threshold"


def envelope_vertices(speeds, n):
    """Exact polygon for display, including every slope change of the minimum.

    Uses the checker's piecewise-linear idea; this is not a third independent
    certification method. The plot consumes these vertices, not a time grid.
    """
    corners = sorted({Q(m, 2 * v) for v in speeds for m in range(2 * v + 1)})
    candidates = set(corners)
    for a, b in zip(corners, corners[1:]):
        mid = (a + b) / 2
        lines = []
        for v in speeds:
            position = v * mid
            whole = position.numerator // position.denominator
            lines.append((v, -whole) if position % 1 < Q(1, 2) else (-v, whole + 1))
        for (m, c), (p, q) in combinations(lines, 2):
            if m != p:
                crossing = Q(q - c, m - p)
                if a < crossing < b:
                    candidates.add(crossing)
    points = []
    for t in sorted(candidates):
        points.append((t, n * min(circular_distance(v * t) for v in speeds)))
        while len(points) >= 3:
            a, b, c = points[-3:]
            if (b[1] - a[1]) * (c[0] - b[0]) != (c[1] - b[1]) * (b[0] - a[0]):
                break
            points.pop(-2)
    return [[str(t), str(y)] for t, y in points]


def detailed_case(label, relative):
    # Keep every physical runner moving, consistent with the conversation.
    velocities = (1, *(v + 1 for v in relative))
    result = check(velocities, reference=0)
    maxima = result["maximum"]
    handoffs = []
    for text in maxima["times_original"]:
        t = Q(text)
        limiting = [v for v in relative if circular_distance(v * t) == Q(maxima["separation"])]
        handoffs.append({
            "time": text,
            "limiting_relative_speeds": limiting,
            "receding_relative_speeds": [v for v in limiting if v * t % 1 < Q(1, 2)],
            "approaching_relative_speeds": [v for v in limiting if v * t % 1 > Q(1, 2)],
            "relative_positions": ["0", *(str(v * t % 1) for v in relative)],
        })
    refs = []
    for index, velocity in enumerate(velocities):
        r = result if index == 0 else check(velocities, reference=index)
        refs.append({"reference_velocity": velocity,
                     "maximum": r["maximum"]["separation"],
                     "tight": r["maximum"]["tight"]})
    return {"label": label, "relative_speeds": list(relative),
            "selected_runner_result": result, "peak_handoffs": handoffs,
            "all_reference_summary": refs,
            "normalized_envelope": envelope_vertices(relative, len(velocities))}


def main():
    mutations = []
    summaries = []
    for n in (4, 8, 12):
        rows = []
        for removed in range(1, n):
            for added in range(n, 2 * n - 1):
                speeds = tuple(sorted((set(range(1, n)) - {removed}) | {added}))
                intervals = feasible_intervals(speeds, Q(1, n))
                rows.append({"n": n, "removed_relative_speed": removed,
                             "added_relative_speed": added, "relative_speeds": speeds,
                             "status": interval_status(intervals),
                             "threshold_intervals": [[str(a), str(b)] for a, b in intervals]})
        mutations.extend(rows)
        summaries.append({"n": n, "mutations": len(rows),
                          **{status: sum(r["status"] == status for r in rows)
                             for status in ("tight", "above_threshold", "below_threshold")}})

    cases = [detailed_case(f"consecutive-{n}", tuple(range(1, n))) for n in (4, 8, 12)]
    tight_mutations = [row for row in mutations if row["status"] == "tight"]
    for row in tight_mutations:
        cases.append(detailed_case(
            f"changed-{row['n']}-remove-{row['removed_relative_speed']}-add-{row['added_relative_speed']}",
            row["relative_speeds"]))
    # Independent maximum method and complete interval method agree for every
    # listed tight case. All selected runners are explicitly identified.
    assert all(c["selected_runner_result"]["maximum"]["tight"] for c in cases)
    assert all(c["selected_runner_result"]["maximum"]["crosschecked_with_intervals"] for c in cases)

    controls = []
    for n in (4, 8, 12):
        relative = (*range(1, n - 1), n)
        controls.append(check((1, *(v + 1 for v in relative))))
    assert all(Q(c["maximum"]["excess_over_conjecture_threshold"]) > 0 for c in controls)

    output = {
        "date": "2026-09-19",
        "checker_base_commit": "2d97b34828c8ceadc81fe5c6ceb60439e554b4c1",
        "checker_sha256": hashlib.sha256((ROOT / "lonely_runner/checker.py").read_bytes()).hexdigest(),
        "scope": "n=4,8,12; reference speed 1; common start; one full relative period [0,1]",
        "mutation_domain": "Replace r in 1..n-1 by b in n..2(n-1), one relative speed at a time",
        "classification": "Exact closed intervals; only singleton feasible times means tight; positive width means excess",
        "limitations": "Not all speed combinations; no new theorem or full conjecture proof; plots are displays of exact rational data",
        "summaries": summaries, "tight_cases": cases,
        "fastest_plus_one_controls": controls, "mutations": mutations,
    }
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"summaries": summaries,
                      "tight_cases": [{"label": c["label"], "maximum": c["selected_runner_result"]["maximum"]["separation"],
                                       "times": c["selected_runner_result"]["maximum"]["times_original"],
                                       "tight_reference_velocities": [r["reference_velocity"] for r in c["all_reference_summary"] if r["tight"]]}
                                      for c in cases],
                      "controls": [{"n": c["n"], "maximum": c["maximum"]["separation"]} for c in controls]}, indent=2))


if __name__ == "__main__":
    main()
