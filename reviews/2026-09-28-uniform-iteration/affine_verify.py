#!/usr/bin/env python3
"""Exact checks on declared affine fixtures; no parameter/word search or LP.

Standard library only. The formal identities support the accompanying proof
candidate; this program does not automatically certify its general logic.
"""

from fractions import Fraction as F
import json


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def unit(i, amount):
    out = [F(0)] * 8
    out[i] = F(amount)
    return tuple(out)


def endpoint(i, m):
    return add(unit(i, F(m) + F(1, 8)), unit(4 + i, 1))


def evaluate(vector, periods, shifts):
    return sum(x * y for x, y in zip(vector, periods + shifts))


TEMPLATES = [
    ("ABCD", [F(1)] * 4, [F(-1, 8), F(1, 8), F(3, 8), F(5, 8)]),
    ("ACDBCD", [F(1), F(1), F(1, 2), F(1, 2)],
     [F(-1, 8), F(3, 8), F(1, 16), F(3, 16)]),
    ("ADBDCD", [F(1), F(1), F(1), F(1, 3)],
     [F(-1, 8), F(5, 24), F(13, 24), F(1, 24)]),
]


def check_template(word, periods, shifts):
    indices = [ord(x) - ord("A") for x in word]
    size = len(indices)
    counts = [indices.count(i) for i in range(4)]
    seen = [0] * 4
    colors, ends = [], []
    for j in range(2 * size + 1):
        i = indices[j % size]
        colors.append(i)
        ends.append(endpoint(i, seen[i]))
        seen[i] += 1
    gaps = [sub(unit(colors[j + 1], F(1, 4)), sub(ends[j + 1], ends[j]))
            for j in range(2 * size)]
    summed = tuple(sum(gap[k] for gap in gaps[:size]) for k in range(8))
    expected = tuple(F(counts[k], 4) - (counts[k] if k == indices[0] else 0)
                     if k < 4 else F(0) for k in range(8))
    assert summed == expected
    for j in range(size):
        drift = sub(unit(colors[j], counts[colors[j]]),
                    unit(colors[j + 1], counts[colors[j + 1]]))
        assert sub(gaps[j + size], gaps[j]) == drift
        assert sub(ends[j + size], ends[j]) == unit(colors[j], counts[colors[j]])
    times = [evaluate(e, periods, shifts) for e in ends]
    assert all(a < b for a, b in zip(times, times[1:]))
    assert all(evaluate(g, periods, shifts) == 0 for g in gaps)
    assert times[0] == 0 and times[size] == 1 and times[-1] == 2
    gamma = min(periods) / 4
    rho = gamma / 336
    assert (F(40) + F(1, 8) + 1) * rho < gamma / 8
    assert min(periods) - rho > F(1, 6)
    assert max(periods) + rho < F(3, 2)
    assert max(abs(x) for x in shifts) + rho < 2
    return {"word": word, "counts": counts, "formal_edge_identities": size,
            "tiling_endpoints": [str(t) for t in times[:size + 1]],
            "gamma": str(gamma), "rho": str(rho),
            "conditional_local_move_bound": 2 * size}


def inherited_trace():
    # Exactly the previously preserved auxiliary distinct fixture, not new data.
    speeds = [F(127, 128), F(1), F(6, 5), F(33, 20)]
    phases = [F(12363, 45056), F(925, 1056), F(127, 220), F(1, 8)]
    periods = [1 / v for v in speeds]
    shifts = [-alpha / v for alpha, v in zip(phases, speeds)]
    word = [0, 1, 2, 3, 2, 3, 1, 2, 3, 2, 3]
    t = F(-17995, 44704)
    moves = []
    for call, i in enumerate(word * 3, 1):
        theta = speeds[i] * t + phases[i]
        lap = theta.numerator // theta.denominator
        frac = theta - lap
        if F(1, 8) <= frac <= F(7, 8):
            lo = (F(lap) + F(1, 8)) * periods[i] + shifts[i]
            hi = (F(lap) + F(7, 8)) * periods[i] + shifts[i]
            assert lo <= t <= hi
            continue
        m = lap if frac < F(1, 8) else lap + 1
        left = (F(m) - F(1, 8)) * periods[i] + shifts[i]
        right = (F(m) + F(1, 8)) * periods[i] + shifts[i]
        phase_output = t + ((F(1, 8) - frac) if frac < F(1, 8)
                            else (F(9, 8) - frac)) / speeds[i]
        assert left < t < right == phase_output
        assert 0 < right - t < periods[i] / 4
        moves.append({"call": call, "runner": "ABCD"[i], "occurrence": m,
                      "input": str(t), "output": str(right)})
        t = right
    assert [x["call"] for x in moves] == [3, 12, 15, 18, 19, 20, 23]
    assert t == F(38325, 44704)
    assert all(F(1, 8) <= (v * t + alpha) % 1 <= F(7, 8)
               for v, alpha in zip(speeds, phases))
    return {"status": "pass", "calls": 33, "moves": moves,
            "final_time": str(t), "all_safe": True}


def main():
    print(json.dumps({
        "status": "pass",
        "scope": "Three declared exact tilings and one inherited rational trace; no scan",
        "templates": [check_template(*item) for item in TEMPLATES],
        "inherited_auxiliary_distinct": inherited_trace(),
    }, indent=2))


if __name__ == "__main__":
    main()
