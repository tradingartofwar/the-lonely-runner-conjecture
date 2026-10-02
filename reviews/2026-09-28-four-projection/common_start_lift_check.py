"""Exact single-instance check of the coordinator's common-start lift.

This separately marked follow-on case was chosen algebraically after the
auxiliary counterexample. No search, adjustment, lap scan, or main-code import.
"""
from fractions import Fraction as F
from math import gcd, lcm
import json

D = F(1, 8)
SCALED = [F(127, 128), F(1), F(6, 5), F(33, 20)]
PHASES = [F(12363, 45056), F(925, 1056), F(127, 220), D]
M = lcm(*(p.denominator for p in PHASES))
P = M // 3 + 1
N = 640 * M * 10**6
ANCHOR = F(P, M)
assert gcd(P, M) == 1
RESIDUES = [int(M * p) * pow(P, -1, M) % M for p in PHASES]
SPEEDS = [int(N * v) + r for v, r in zip(SCALED, RESIDUES)]
assert all((u * ANCHOR) % 1 == p for u, p in zip(SPEEDS, PHASES))
assert all(u < v for u, v in zip(SPEEDS, SPEEDS[1:]))
assert len(set([0, 1, 4, 5] + SPEEDS)) == 8


def project(t, v):
    z = v * t - 1 + D
    lap = -((-z.numerator) // z.denominator)
    return max(t, (lap + D) / v)


def shifted_bad(index, lap):
    v, alpha = SPEEDS[index], PHASES[index]
    return (ANCHOR + (lap - D - alpha) / v,
            ANCHOR + (lap + D - alpha) / v)


left = ANCHOR + (-D - PHASES[0]) / SPEEDS[0]
right = ANCHOR + (1 + D - PHASES[3]) / SPEEDS[3]
order = [0, 1, 2, 3, 2, 3, 1, 2, 3, 2, 3] * 2
t = left
trace = []
for i in order:
    t = project(t, SPEEDS[i])
    trace.append(t)
assert t == right
end_phases = [(u * t) % 1 for u in SPEEDS]
assert end_phases[0] > 1 - D
assert all(D <= x <= 1 - D for x in end_phases[1:])
earliest = project(right, SPEEDS[0])
assert all(D <= (u * earliest) % 1 <= 1 - D
           for u in [1, 4, 5] + SPEEDS)

# Separate interval geometry certifies emptiness before the next a entry.
triple_chain = [shifted_bad(3, 0), shifted_bad(1, 1),
                shifted_bad(2, 1), shifted_bad(3, 1)]
assert all(triple_chain[i+1][0] < triple_chain[i][1] for i in range(3))
cover = [shifted_bad(2, 0), shifted_bad(0, 0),
         (triple_chain[0][0], triple_chain[-1][1]), shifted_bad(0, 1)]
assert cover[0][0] < left < cover[0][1]
assert all(cover[i+1][0] < cover[i][1] for i in range(3))
assert cover[-1][1] == earliest
core_lifts = []
for v in [1, 4, 5]:
    low, high = v * left, v * earliest
    lap = low.numerator // low.denominator
    assert lap + D <= low <= high <= lap + 1 - D
    core_lifts.append({'speed': v, 'lap': lap, 'low': str(low), 'high': str(high)})

if __name__ == '__main__':
    print(json.dumps({
        'provenance': 'Coordinator algebraic lift, structural agent exact verification; one constructed follow-on case, no scan.',
        'M': M, 'P': P, 'N': N, 'anchor': str(ANCHOR),
        'residues': RESIDUES, 'velocities': [0, 1, 4, 5] + SPEEDS,
        'phases': ['0'] * 8, 'threshold': str(D),
        'window': [str(left), str(right)],
        'trace': list(map(str, trace)),
        'final_time': str(t), 'final_residual_phases': list(map(str, end_phases)),
        'first_runner_violation': str(end_phases[0] - (1 - D)),
        'window_empty_by_open_cover': True,
        'earliest_joint_time_after_left': str(earliest),
        'triple_chain': [[str(x), str(y)] for x, y in triple_chain],
        'cover_until_earliest': [[str(x), str(y)] for x, y in cover],
        'core_lifts': core_lifts,
    }, indent=2))
