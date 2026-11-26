"""Replay the challenger’s checks on the twelve opened stretch_middle cases."""

import json
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OPENED = ROOT / "experiments" / "subset-sum-prediction"
sys.path.insert(0, str(ROOT / "experiments" / "one-time-prediction"))
from predictor import choose_time

TARGET = F(1, 16)


def limiting(speeds, time):
    p, q = time.as_integer_ratio()
    distances = [(min((v*p) % q, (-v*p) % q), v) for v in speeds]
    numerator = min(n for n, _ in distances)
    return F(numerator, q), tuple(v for n, v in distances if n == numerator)


def first_escape(speeds, q, direction):
    """Local safe-arc arithmetic and an independent endpoint audit."""
    hits = [v for v in speeds if v % q == 0]
    step = TARGET / min(hits)
    times_to_edge = []
    for v in speeds:
        if v % q:
            phase = F(v % q, q)
            room = (1 - TARGET - phase) if direction == 1 else (phase - TARGET)
            times_to_edge.append((room / v, v))
    headroom = min(t for t, _ in times_to_edge)
    edges = tuple(v for t, v in times_to_edge if t == headroom)
    time = F(1, q) + direction * step
    distance, limiters = limiting(speeds, time)
    first_arc = all(TARGET <= v * step <= 1 - TARGET for v in hits)
    if step <= headroom and first_arc:
        assert distance >= TARGET
    return hits, step, headroom, edges, time, distance, limiters


def main():
    panel = json.loads((OPENED / 'panel.json').read_text())['instances']
    ledger = json.loads((OPENED / 'ledger.json').read_text())
    assert len(panel) == len(ledger) == 60
    middle = {}
    earlier_only_without_reciprocal = []
    unsafe = []
    counts = [0, 0, 0]  # shared, earlier-only, neither
    for index, (row, old) in enumerate(zip(panel, ledger), 1):
        if row['pattern'] != 'stretch_middle':
            continue
        weights = tuple(row['weights'])
        speeds = sorted(sum(s) for size in range(1, 5) for s in combinations(weights, size))
        assert speeds == row['speeds'] and tuple(old['weights']) == weights
        middle[weights] = speeds
        clear_q = [q for q in range(2, 17) if all(v % q for v in speeds)]
        _, t, _ = choose_time(speeds)
        m, limiters = limiting(speeds, t)
        assert (m >= TARGET) == old['prior']
        four_weight_success = old['time'] is not None
        if four_weight_success:
            assert limiting(speeds, F(old['time']))[0] >= TARGET and m >= TARGET
            counts[0] += 1
        elif m >= TARGET:
            counts[1] += 1
            if not clear_q:
                earlier_only_without_reciprocal.append(index)
        else:
            counts[2] += 1
            unsafe.append(index)
        print(f'row {index} {weights}  clear q={clear_q}  earlier {t}  min {m} at {limiters}')
    assert len(middle) == 12 and counts == [1, 10, 1]
    assert earlier_only_without_reciprocal == [42] and unsafe == [12]

    shifted = middle[41, 80, 435, 564]
    failed = middle[3, 5, 28, 60]
    assert [min(v for v in shifted if v % q == 0) for q in range(2, 17)] == [
        80, 435, 80, 80, 564, 476, 80, 999, 80, 121, 564, 1040, 476, 435, 80]
    assert limiting(failed, F(2, 23)) == (F(2, 23), (68, 91, 93))
    for speeds, q, sign, expected in [
        (shifted, 9, -1, ([999], F(1,15984), F(7,98640), (685,), F(1775,15984), TARGET, (999,))),
        (shifted, 9, +1, ([999], F(1,15984), F(7,155376), (1079,), F(1777,15984), F(697,15984), (1079,))),
        (failed, 16, +1, ([96], F(1,1536), F(0), (31,63), F(97,1536), F(11,512), (63,))),
        (failed, 16, -1, ([96], F(1,1536), F(0), (33,65), F(95,1536), F(31,1536), (65,))),
        (failed, 10, +1, ([60], F(1,960), F(1,640), (88,), F(97,960), TARGET, (60,))),
        (middle[3,6,31,72], 10, +1, ([40], F(1,640), F(3,8720), (109,), F(13,128), TARGET, (40,))),
    ]:
        actual = first_escape(speeds, q, sign)
        assert actual == expected, (actual, expected)
        hits, step, headroom, edges, time, distance, runners = actual
        print(f'total {max(speeds)} q={q} direction={sign:+} hits={hits} escape={step}'
              f' room={headroom} at {edges} t={time} min={distance} at {runners}')
    assert F(13 * 109, 128) % 1 == F(9, 128)


if __name__ == '__main__':
    main()
