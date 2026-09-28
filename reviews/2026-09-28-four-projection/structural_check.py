"""Exact checks of two analytically constructed auxiliary counterexamples.

No speed/phase scan, imported selector, or event enumeration. This is the
structural author's own arithmetic check, not independent verification.
"""
from fractions import Fraction as F
import json

D = F(1, 8)
T0 = -F(159, 1056)
TRIPLE_END = F(640, 1056)
ORDER = [0, 1, 2, 3, 2, 3, 1, 2, 3, 2, 3] * 2


def project(t, v, alpha):
    z = v * t + alpha - 1 + D
    lap = -((-z.numerator) // z.denominator)
    return max(t, (lap + D - alpha) / v)


def bad_band(v, alpha, lap):
    return ((lap - D - alpha) / v, (lap + D - alpha) / v)


def run(a):
    speeds = [a, F(1), F(6, 5), F(33, 20)]
    phases = [D - a * T0, F(925, 1056), F(127, 220), D]
    left = T0 - F(1, 4) / a
    bands = [
        bad_band(speeds[3], phases[3], 0),
        bad_band(speeds[1], phases[1], 1),
        bad_band(speeds[2], phases[2], 1),
        bad_band(speeds[3], phases[3], 1),
    ]
    expected = [(F(x, 1056), F(y, 1056)) for x, y in
                [(-160, 0), (-1, 263), (262, 482), (480, 640)]]
    assert bands == expected
    assert all(bands[i + 1][0] < bands[i][1] for i in range(3))
    previous_c = bad_band(speeds[2], phases[2], 0)
    assert previous_c == (-F(618, 1056), -F(398, 1056))
    assert previous_c[0] < left < previous_c[1] < T0
    first_triple = previous_c[1]
    assert all(D <= (v * first_triple + p) % 1 <= 1 - D
               for v, p in zip(speeds[1:], phases[1:]))
    assert T0 < TRIPLE_END - F(3, 4) / a
    trace = []
    t = left
    for index in ORDER:
        t = project(t, speeds[index], phases[index])
        trace.append(t)
    assert trace[10] == first_triple
    assert trace[11] == T0
    assert t == TRIPLE_END
    final_phases = [(v * t + p) % 1 for v, p in zip(speeds, phases)]
    assert final_phases[0] > 1 - D
    assert all(D <= x <= 1 - D for x in final_phases[1:])
    earliest = T0 + 1 / a
    assert project(t, speeds[0], phases[0]) == earliest
    assert all(D <= (v * earliest + p) % 1 <= 1 - D
               for v, p in zip(speeds, phases))
    # These four open intervals strictly overlap and cover [left,earliest).
    cover = [previous_c, (left, T0),
             (bands[0][0], bands[-1][1]),
             (T0 + F(3, 4) / a, earliest)]
    assert cover[0][0] < left < cover[0][1]
    assert all(cover[i + 1][0] < cover[i][1] for i in range(3))
    return {
        'speeds': list(map(str, speeds)),
        'phases': list(map(str, phases)),
        'window': [str(left), str(TRIPLE_END)],
        'window_empty_by_open_cover': True,
        'trace': list(map(str, trace)),
        'final_phases': list(map(str, final_phases)),
        'final_time_unsafe': str(t),
        'a_phase_violation': str(final_phases[0] - (1-D)),
        'earliest_joint_time_after_left': str(earliest),
        'cover_until_earliest': [[str(x), str(y)] for x,y in cover],
    }


if __name__ == '__main__':
    print(json.dumps({'provenance': 'Two algebraically constructed auxiliary cases; no scan.',
                      'equal_speed_simple': run(F(1)),
                      'distinct_speed_follow_on': run(F(127, 128))}, indent=2))
