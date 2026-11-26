"""Audit the first closed safe component at or after 1/3 on the revealed fresh-04."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

START = F(1, 3)
LIMIT = F(1, 16)


def unsafe(speeds, t):
    return [v for v in speeds if abs(v * t - round(v * t)) < LIMIT]


def limiting(speeds, t):
    distances = [abs(v * t - round(v * t)) for v in speeds]
    assert min(distances) == LIMIT
    return [v for v, d in zip(speeds, distances) if d == LIMIT]


def first_component(speeds):
    # On each open cell between two consecutive threshold crossings, the set
    # of blockers is constant. Endpoints are checked separately so a single
    # equality instant with unsafe cells on both sides still counts.
    events = {START, F(1)}
    for v in speeds:
        for lap in range(v // 3, v + 1):
            for offset in (LIMIT, -LIMIT):
                t = (lap + offset) / v
                if START < t < 1:
                    events.add(t)
    ordered = sorted(events)
    probes = []
    for left, right in zip(ordered, ordered[1:]):
        probes.extend((left, (left + right) / 2))
    probes.append(ordered[-1])
    first = next(i for i, t in enumerate(probes) if not unsafe(speeds, t))
    past = next(i for i in range(first + 1, len(probes)) if unsafe(speeds, probes[i]))
    assert first % 2 == (past - 1) % 2 == 0
    lo, hi = probes[first], probes[past - 1]
    return {"window": [str(lo), str(hi)], "width": str(hi - lo),
            "left_limiters": limiting(speeds, lo), "right_limiters": limiting(speeds, hi),
            "previous_event": str(probes[first - 2]), "next_event": str(probes[past + 1]),
            "blocked_immediately_before": unsafe(speeds, probes[first - 1]),
            "blocked_immediately_after": unsafe(speeds, probes[past]),
            "event_points_tested_before_pass": first // 2,
            "open_cells_tested_before_pass": first // 2}


def main():
    record = json.loads(Path(__file__).with_name("reveal").joinpath("panel.json").read_bytes())
    weights = record["instances"][3]["weights"]
    assert weights == [14, 17, 103, 154]
    speeds = sorted(sum(s) for n in range(1, 5) for s in combinations(weights, n))
    audit = first_component(speeds)
    assert audit["window"] == ["625/1872", "1375/4112"]
    assert audit["left_limiters"] == audit["blocked_immediately_before"] == [117]
    assert audit["right_limiters"] == audit["blocked_immediately_after"] == [257]
    print(json.dumps({"case": "fresh-04", "weights": weights, **audit}, indent=2))


if __name__ == "__main__":
    main()
