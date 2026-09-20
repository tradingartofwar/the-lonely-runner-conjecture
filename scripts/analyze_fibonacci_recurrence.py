"""Small upper-bound sets and full-prefix witnesses for four Fibonacci stages.

Run: python -m scripts.analyze_fibonacci_recurrence
All certificates use integers/Fraction; no time sampling or floating optimization.
The general prefix formula is already in Zhuravleva (2011), Theorem 1.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import circular_distance, exact_maximum, feasible_intervals

ROOT = Path(__file__).resolve().parents[1]


def sequences(last):
    fib, lucas = [0, 1], [2, 1]
    while len(fib) <= last:
        fib.append(fib[-1] + fib[-2])
        lucas.append(lucas[-1] + lucas[-2])
    return fib, lucas


def continued_fraction(terms):
    value = Q(terms[-1])
    for term in reversed(terms[:-1]):
        value = term + 1 / value
    return value


def strings(intervals):
    return [[str(left), str(right)] for left, right in intervals]


def main():
    fib, lucas = sequences(22)
    core = [1, 2, 3, 5]
    stages = []
    for m in range(2, 6):
        s = 2 * m + 1
        a, q = fib[s - 1], lucas[s]
        time, height = Q(a, q), Q(fib[s - 2], q)
        trigger = fib[4 * m - 2]
        meeting = fib[2 * m - 1] * fib[2 * m - 2]
        core.append(trigger)
        assert len(set(core)) == len(core)
        assert height == 1 - 3 * time
        assert Q(meeting + 1, trigger + 3) == time
        assert 5 * meeting == lucas[4 * m - 3] - 1
        assert trigger + 3 == fib[2 * m - 3] * q

        # Method B and Method A have separate implementations in the checker.
        maximum = exact_maximum(core)
        peaks = (time, 1 - time)
        allowed = feasible_intervals(core, height)
        assert maximum.value == height and maximum.times == peaks
        assert allowed == tuple((t, t) for t in peaks)
        assert feasible_intervals(core, height + Q(1, 10000)) == ()

        # Check one positive-width slice of the proposed interval lemma per stage.
        next_height = Q(fib[2 * m + 1], lucas[2 * m + 3])
        diagnostic = (height + next_height) / 2
        left, right = (meeting + diagnostic) / trigger, (1 - diagnostic) / 3
        diagnostic_intervals = ((left, right), (1 - right, 1 - left))
        assert feasible_intervals(core, diagnostic) == diagnostic_intervals

        # A witness for the longest prefix certifies all four nested prefixes.
        full = fib[2:4 * m + 2]
        assert len(full) + 1 == 4 * m + 1
        witness = []
        for r in range(2, 4 * m + 2):
            phase = fib[r] * time % 1
            distance = circular_distance(fib[r] * time)
            assert height <= phase <= 1 - height
            assert circular_distance(fib[r] * (1 - time)) == distance
            witness.append({"index": r, "speed": fib[r],
                            "phase": str(phase), "distance": str(distance)})
        assert min(Q(row["distance"]) for row in witness) == height
        assert [row["speed"] for row in witness if Q(row["distance"]) == height] == [3, trigger]
        assert height > Q(1, 4 * m - 2)

        # Bounded checks of identities used in the general handwritten argument.
        for r in range(1, s + 1):
            assert 5 * a * fib[r] == q * lucas[r - 1] + (-1) ** r * lucas[s - r]
        assert lucas[s] - lucas[s - 4] == 5 * fib[s - 2]
        assert fib[2 * s - 1] == q * a + 1
        assert fib[2 * s] == q * fib[s]
        for r in range(1, 2 * s):
            assert (fib[2 * s - r] - (-1) ** (r + 1) * fib[r]) % q == 0
        assert [lucas[r] % 5 for r in range(4)] == [2, 1, 3, 4]
        assert all(lucas[r + 4] % 5 == lucas[r] % 5 for r in range(19))
        assert continued_fraction([0, 3] + [1] * (2 * m - 1)) == time
        # A^s has diagonal entries F_(s-1), F_(s+1).
        assert fib[s - 1] + fib[s + 1] == q
        assert Q(fib[s + 1], q) == 1 - time

        overlap_ratio = None
        if m > 2:
            previous = stages[-1]
            old_trigger = previous["critical_speed"]
            old_meeting = previous["critical_meeting_count"]
            assert Q(meeting, trigger) == Q(previous["peak_times"][0])
            numerator = old_trigger * meeting - trigger * old_meeting
            assert numerator == fib[2 * m - 3] * fib[2 * m - 1]
            assert trigger + old_trigger == 3 * fib[4 * m - 4]
            overlap_ratio = Q(numerator, trigger + old_trigger)
            assert overlap_ratio < Q(1, 6)

        next_speed = fib[4 * m + 2]
        assert all(circular_distance(next_speed * t) == 0 for t in peaks)

        # Nearby counterchecks: decreasing the last speed by 1 destroys the old
        # maximum; increasing it by 1 preserves the maximum and both peaks.
        last = full[-1]
        minus, plus = [*full[:-1], last - 1], [*full[:-1], last + 1]
        assert len(set(minus)) == len(minus) and len(set(plus)) == len(plus)
        assert (last - 1) % q == 0
        assert feasible_intervals((*core, last - 1), height) == ()
        assert feasible_intervals((*core, last + 1), height) == allowed
        assert min(circular_distance(v * time) for v in minus) == 0
        assert min(circular_distance(v * time) for v in plus) == height

        stages.append({
            "stage": m, "total_runner_range": [4 * m - 2, 4 * m + 1],
            "selected_reference_speed": 0, "maximum": str(height),
            "peak_times": [str(t) for t in peaks], "critical_speed": trigger,
            "critical_meeting_count": meeting, "upper_bound_subset": list(core),
            "maximum_candidate_count": maximum.candidate_count,
            "interval_crosscheck": strings(allowed),
            "diagnostic_threshold": str(diagnostic),
            "diagnostic_intervals": strings(diagnostic_intervals),
            "induction_overlap_ratio": str(overlap_ratio) if overlap_ratio is not None else None,
            "full_prefix_witness": witness,
            "next_fibonacci_speed": next_speed, "next_speed_distances_at_old_peaks": ["0", "0"],
            "minus_one_control": {"old_speed": last, "new_speed": last - 1,
                                  "height_feasible_intervals": [],
                                  "conclusion": "maximum strictly below old height; new maximum not computed"},
            "plus_one_control": {"old_speed": last, "new_speed": last + 1,
                                 "maximum": str(height), "peak_times": [str(t) for t in peaks]},
            "continued_fraction_terms": [0, 3] + [1] * (2 * m - 1),
        })

    data = {
        "date": "2026-09-20", "base_commit": "3b9990a478d719c7a3faffa74dcc0b61dcb26d3c",
        "checker_sha256": hashlib.sha256((ROOT / "lonely_runner/checker.py").read_bytes()).hexdigest(),
        "scope": "Four prescribed sparse subsets; exact maxima crosschecked with intervals; full-prefix witnesses certify selected reference for n=6..21; eight last-speed controls.",
        "status": "Reproduced finite certificates. General plateau values are known from Zhuravleva (2011), Theorem 1; our written reconstruction has not had independent review.",
        "limitations": "Only reference speed 0. No all-reference extension, exhaustive speed-set search, novelty claim, or general Lonely Runner proof.",
        "stages": stages,
    }
    (ROOT / "experiments/fibonacci_recurrence.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"stages": [{key: row[key] for key in
                                  ("stage", "total_runner_range", "maximum", "peak_times", "critical_speed")}
                                 for row in stages],
                      "independent_maximum_crosschecks": len(stages),
                      "nearby_controls": 2 * len(stages)}, indent=2))


if __name__ == "__main__":
    main()
