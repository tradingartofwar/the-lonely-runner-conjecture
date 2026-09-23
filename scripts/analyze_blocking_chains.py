"""Exact open-interval cover certificates for eight prescribed configurations.

Run: python -m scripts.analyze_blocking_chains
Seven configurations are reused; one changes relative speed 13 to 8.
Greedy chains are crosschecked by shortest paths in a directed interval graph.
"""

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import check, circular_distance, feasible_intervals
from scripts.analyze_cooperative_blocking import CASES

ROOT = Path(__file__).resolve().parents[1]
DELTA = Q(1, 8)
EXTRA = (1, 4, 5, 6, 7, 8, 11)


@dataclass(frozen=True)
class Window:
    speed: int
    meeting: int

    @property
    def left(self):
        return (self.meeting - DELTA) / self.speed

    @property
    def right(self):
        return (self.meeting + DELTA) / self.speed

    @property
    def center(self):
        return Q(self.meeting, self.speed)

    def shifted(self):
        return Window(self.speed, self.meeting + self.speed)

    def json(self):
        return {"speed": self.speed, "meeting": self.meeting,
                "open_interval": [str(self.left), str(self.right)]}


def value(speeds, time):
    return min(circular_distance(v * time) for v in speeds)


def signed_gap(first, second):
    determinant = first.speed * second.meeting - second.speed * first.meeting
    gap = second.left - first.right
    assert second.center > first.center
    assert gap == Q(8 * determinant - first.speed - second.speed,
                    8 * first.speed * second.speed)
    return {"first": [first.speed, first.meeting],
            "second": [second.speed, second.meeting],
            "determinant": determinant, "signed_gap": str(gap)}


def chain_for_component(speeds, start, end):
    windows = [Window(v, j) for v in speeds for j in range(2 * v + 1)
               if Window(v, j).right > start and Window(v, j).left < end]
    assert windows and all(start <= w.left < w.right <= end for w in windows)

    # Greedy extends the covered open prefix as far as possible. A mere touch
    # is not an overlap: internal transitions require left < reach, not <=.
    chain, reach = [], start
    while reach < end:
        eligible = [w for w in windows if w.right > reach and
                    (w.left <= reach if not chain else w.left < reach)]
        assert eligible, (start, end, reach)
        selected = max(eligible, key=lambda w: (w.right, -w.speed, -w.meeting))
        chain.append(selected)
        reach = selected.right
    assert chain[0].left == start and chain[-1].right == end

    # Independent shortest-path dynamic program. Edges strictly advance the
    # right endpoint and overlap; initial vertices begin at start.
    ordered = sorted(windows, key=lambda w: (w.right, w.left, w.speed, w.meeting))
    distances, edge_count = {}, 0
    for i, w in enumerate(ordered):
        options = [1] if w.left == start else []
        for previous in ordered[:i]:
            if w.left < previous.right < w.right:
                edge_count += 1
                if previous in distances:
                    options.append(distances[previous] + 1)
        if options:
            distances[w] = min(options)
    shortest = min(distances[w] for w in windows if w.right == end and w in distances)
    assert shortest == len(chain)

    # Check each open cell and each internal endpoint of the selected union.
    # These are all its status boundaries, not a sampled time grid.
    cuts = sorted({start, end, *(x for w in chain for x in (w.left, w.right))})
    probes = cuts[1:-1] + [(a + b) / 2 for a, b in zip(cuts, cuts[1:])]
    assert all(any(w.left < t < w.right for w in chain) for t in probes)
    assert all(value(speeds, t) < DELTA for t in probes)
    assert value(speeds, start) >= DELTA and value(speeds, end) >= DELTA
    gaps = [signed_gap(a, b) for a, b in zip(chain, chain[1:])]
    assert all(Q(row["signed_gap"]) < 0 for row in gaps)
    return chain, {"blocked_component": [str(start), str(end)],
                   "candidate_windows": len(windows), "graph_edges": edge_count,
                   "minimum_chain_length": shortest,
                   "chain": [w.json() for w in chain], "internal_handoffs": gaps,
                   "endpoint_and_cell_checks": len(probes)}


def sole_blocker_witnesses(speeds):
    cuts = sorted({Q(0), Q(1), *(x for v in speeds for j in range(v + 1)
                   for x in (Window(v, j).left, Window(v, j).right) if 0 < x < 1)})
    witnesses = {}
    for a, b in zip(cuts, cuts[1:]):
        time = (a + b) / 2
        blockers = [v for v in speeds if circular_distance(v * time) < DELTA]
        if len(blockers) != 1 or blockers[0] in witnesses:
            continue
        blocker = blockers[0]
        remaining = tuple(v for v in speeds if v != blocker)
        other_gap = value(remaining, time)
        assert other_gap > DELTA
        assert any(left <= time <= right for left, right in feasible_intervals(remaining, other_gap))
        witnesses[blocker] = {"omitted_speed": blocker, "time": str(time),
                              "other_speeds_minimum_distance": str(other_gap),
                              "omitted_speed_distance": str(circular_distance(blocker * time)),
                              "fixed_original_target": str(DELTA)}
    return [witnesses[v] for v in sorted(witnesses)]


def analyze(label, speeds):
    result = check((0, *speeds))
    assert result["maximum"]["crosschecked_with_intervals"]
    allowed = feasible_intervals(speeds, DELTA)
    assert allowed and len(speeds) == 7
    assert result["n"] == 8
    chains, components = [], []
    for i, (_, start) in enumerate(allowed):
        end = allowed[i + 1][0] if i + 1 < len(allowed) else allowed[0][0] + 1
        chain, evidence = chain_for_component(speeds, start, end)
        chains.append(chain)
        components.append(evidence)
    boundaries = []
    for i, chain in enumerate(chains):
        next_window = chains[i + 1][0] if i + 1 < len(chains) else chains[0][0].shifted()
        boundary = signed_gap(chain[-1], next_window)
        a, b = allowed[(i + 1) % len(allowed)]
        assert Q(boundary["signed_gap"]) == b - a
        boundaries.append(boundary)
    unique_windows = {(w.speed, w.meeting % w.speed) for chain in chains for w in chain}
    count = sum(len(c) for c in chains)
    assert len(unique_windows) == count
    tight = Q(result["maximum"]["separation"]) == DELTA
    witnesses = sole_blocker_witnesses(speeds) if tight else []
    if tight:
        assert len(witnesses) == 7
        assert all(a == b for a, b in allowed)
        assert feasible_intervals(speeds, DELTA + Q(1, 800)) == ()
    return {"label": label, "original_n": 8, "selected_reference_speed": 0,
            "relative_speeds": list(speeds), "threshold": str(DELTA),
            "maximum": result["maximum"],
            "allowed_intervals": [[str(a), str(b)] for a, b in allowed],
            "all_blocking_windows_per_cycle": sum(speeds),
            "minimum_cover_windows": count, "components": components,
            "boundaries_between_chains": boundaries,
            "sole_blocker_witnesses": witnesses,
            "odd_eighth_distances": [str(value(speeds, Q(j, 8))) for j in (1, 3, 5, 7)]}


def main():
    cases = [analyze(label, speeds) for label, speeds in
             {**CASES, "grid_blocked_13_to_8": EXTRA}.items()]
    assert [c["minimum_cover_windows"] for c in cases[:3]] == [18, 18, 26]
    assert [len(c["sole_blocker_witnesses"]) for c in cases[:3]] == [7, 7, 7]
    for case in cases[:7]:
        assert all(v % 8 for v in case["relative_speeds"])
        assert case["odd_eighth_distances"] == ["1/8"] * 4
    added = cases[-1]
    assert added["odd_eighth_distances"] == ["0"] * 4
    assert added["maximum"]["separation"] == "2/13"
    assert added["maximum"]["times_original"] == ["4/13", "9/13"]
    new_allowed = feasible_intervals(EXTRA, DELTA)
    assert new_allowed[0] == (Q(17, 56), Q(5, 16))
    assert new_allowed[0][1] - new_allowed[0][0] == Q(1, 112)
    old_window = Window(13, 4)
    assert old_window.left < new_allowed[0][0] < new_allowed[0][1] < old_window.right
    assert any(a < new_allowed[0][0] < new_allowed[0][1] < b
               for a, b in feasible_intervals((8,), DELTA))
    witness = Q(4, 13)
    assert value(EXTRA, witness) == Q(2, 13) > DELTA
    assert circular_distance(13 * witness) == 0
    small_denominator_blockers = {str(q): next(v for v in EXTRA if v % q == 0)
                                 for q in range(1, 9)}
    # If q divides v, then v*(p/q) is an integer for every numerator p.
    assert all(v % int(q) == 0 for q, v in small_denominator_blockers.items())

    # Compare the already-present 13->12 control to the new 13->8 case.
    old_control = next(c for c in cases if c["label"] == "control_11_12")
    assert added["allowed_intervals"] == [p for p in old_control["allowed_intervals"] if p[0] != p[1]]
    data = {
        "date": "2026-09-23", "base_commit": "fe792b3646b72faed0df183a55c02d8226886dc8",
        "checker_sha256": hashlib.sha256((ROOT / "lonely_runner/checker.py").read_bytes()).hexdigest(),
        "scope": "Seven existing eight-runner inputs and one 13->8 control, selected reference only. No speed-set search.",
        "method": "Exact open-window chains; greedy length independently crosschecked by DAG shortest paths; maxima crosschecked by the existing two methods.",
        "cases": cases,
        "grid_destroying_control": {"relative_speed_change": [13, 8],
            "old_safe_times": ["1/8", "3/8", "5/8", "7/8"],
            "new_window": ["17/56", "5/16"], "window_width": "1/112",
            "removed_window": old_window.json(), "witness_time": str(witness),
            "blocker_for_each_denominator_1_through_8": small_denominator_blockers,
            "distances": {str(v): str(circular_distance(v * witness)) for v in EXTRA}},
        "limitations": "Minimum interval counts concern only these fixed inputs and this target. The modular shortcut is sufficient, not necessary. No general noncoverage proof or novelty claim; graph construction is a verification tool, not a reduction for arbitrary inputs.",
    }
    (ROOT / "experiments/blocking_chains.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"cases": [{"label": c["label"], "maximum": c["maximum"]["separation"],
                                 "windows": c["all_blocking_windows_per_cycle"],
                                 "minimum_cover": c["minimum_cover_windows"],
                                 "component_lengths": [x["minimum_chain_length"] for x in c["components"]]}
                                for c in cases],
                      "sole_blocker_witnesses": 21,
                      "graph_components_crosschecked": sum(len(c["components"]) for c in cases)}, indent=2))


if __name__ == "__main__":
    main()
