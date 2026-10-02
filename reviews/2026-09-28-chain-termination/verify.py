#!/usr/bin/env python3
"""Independent exact replay from protocol inputs only.

No primary imports or saved answers. Feasibility uses a complete local
threshold partition; projections use direct fractional-part cases; excess is
integrated by a separate event partition. Standard library only.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = F(1, 8)


def floor(x):
    return x.numerator // x.denominator


def phase(v, t):
    return (v * t) % 1


def safe(v, t):
    p = phase(v, t)
    return D <= p <= 1-D


def joint(vs, t):
    return all(safe(v, t) for v in vs)


def events(vs, left, right):
    points = {left, right}
    for v in vs:
        # The number of iterations depends only on this local window.
        for k in range(floor(v*left)-1, floor(v*right)+3):
            for e in (F(k-D, v), F(k+D, v)):
                if left <= e <= right:
                    points.add(e)
    return sorted(points)


def safe_components(vs, left, right):
    points = events(vs, left, right)
    pieces = [(p, p) for p in points if joint(vs, p)]
    for p, q in zip(points, points[1:]):
        if joint(vs, (p+q)/2):
            assert joint(vs, p) and joint(vs, q)
            pieces.append((p, q))
    out = []
    for p, q in sorted(pieces):
        if out and p <= out[-1][1]:
            out[-1] = (out[-1][0], max(q, out[-1][1]))
        else:
            out.append((p, q))
    return out, len(points)


def advance(v, t):
    x = v*t
    k = floor(x)
    p = x-k
    if D <= p <= 1-D:
        return t, None
    meeting = k if p < D else k+1
    interval = (F(meeting-D, v), F(meeting+D, v))
    assert interval[0] < t < interval[1]
    assert safe(v, interval[0]) and safe(v, interval[1])
    return interval[1], (meeting, interval[0], interval[1])


def potential(vs, t):
    # Integrate the blocked indicator from phase 0, then subtract mean 1/4.
    value = F(0)
    for v in vs:
        theta = phase(v, t)
        blocked_length = min(theta, D) + max(theta-(1-D), F(0))
        value += (blocked_length-theta/4)/v
    return value


def integrate_excess(vs, left, right):
    if left == right:
        return F(0), 0
    answer = F(0)
    pts = events(vs, left, right)
    for p, q in zip(pts, pts[1:]):
        multiplicity = sum(not safe(v, (p+q)/2) for v in vs)
        assert multiplicity >= 1, 'Selected chain must cover every open cell'
        answer += (multiplicity-1)*(q-p)
    return answer, len(pts)-1


def clipped_excess(vs, left, right):
    total = F(0)
    for v in vs:
        for k in range(floor(v*left)-1, floor(v*right)+3):
            lo, hi = max(left, F(k-D, v)), min(right, F(k+D, v))
            total += max(F(0), hi-lo)
    return total-(right-left)


def case_record(case, order):
    vs = case['speeds']
    assert len(vs) == 4 and all(isinstance(v, int) and v > 0 for v in vs)
    L, R = map(F, case['window'])
    components, threshold_count = safe_components(vs, L, R)
    if case['core']:
        core_components, _ = safe_components(case['core'], L, R)
        assert core_components == [(L, R)]
    Q = max(lcm(u, v) for u, v in combinations(vs, 2))
    eta = F(1, 8*Q)
    reciprocal_sum = sum((F(1, v) for v in vs), F(0))
    Hmax = F(3, 32)*reciprocal_sum
    Hstart = potential(vs, L)
    m_L = sum(not safe(v, L) for v in vs)
    Kglobal = floor(1+F(3*Q, 2)*reciprocal_sum)
    Kphase = m_L+floor((Hmax-Hstart)/eta)
    K = min(Kglobal, Kphase)
    t = L
    trace = []
    selected = []
    done = joint(vs, t)
    while not done:
        before_round = t
        for idx in order:
            old = t
            t, interval = advance(vs[idx], old)
            trace.append({'runner': idx, 'input': str(old), 'output': str(t)})
            if interval:
                k, lo, hi = interval
                selected.append((idx, k, lo, hi))
                assert len(selected) <= K
            if t > R:
                done = True
                break
        else:
            assert t > before_round, 'An unsafe completed round must move'
            done = joint(vs, t)
    calls = len(trace)
    completed_rounds = calls // len(order)
    started_rounds = (calls+len(order)-1) // len(order)
    assert started_rounds <= K or not calls
    verdict = 'empty' if t > R else 'earliest'
    if components:
        assert verdict == 'earliest' and t == components[0][0]
    else:
        assert verdict == 'empty'
    overlaps = []
    for first, second in zip(selected, selected[1:]):
        overlap = min(first[3], second[3])-max(first[2], second[2])
        assert overlap >= eta
        overlaps.append(overlap)
    assert len({(row[0], row[1]) for row in selected}) == len(selected)
    if selected:
        A = min(row[2] for row in selected)
        B = max(row[3] for row in selected)
        assert B == t
        selected_excess = sum((row[3]-row[2] for row in selected), F(0))-(B-A)
        actual_union, union_cells = integrate_excess(vs, A, B)
        H_union_difference = potential(vs, B)-potential(vs, A)
        union_span = [str(A), str(B)]
        assert (len(selected)-1)*eta <= selected_excess <= actual_union
        assert actual_union == H_union_difference <= F(3, 16)*reciprocal_sum
        assert actual_union == clipped_excess(vs, A, B)
    else:
        selected_excess = actual_union = H_union_difference = F(0)
        union_span = None
        union_cells = 0
    actual_start, start_cells = integrate_excess(vs, L, t)
    assert actual_start == clipped_excess(vs, L, t)
    selected_excess_from_start = sum(
        (max(F(0), min(t, row[3])-max(L, row[2])) for row in selected), F(0))-(t-L)
    H_start_difference = potential(vs, t)-Hstart
    assert actual_start == H_start_difference <= Hmax-Hstart
    assert (len(selected)-m_L)*eta <= actual_start
    assert (len(selected)-m_L)*eta <= selected_excess_from_start <= actual_start
    return {
        'id': case['id'], 'speeds': vs, 'window': case['window'],
        'verdict': verdict, 'earliest': str(t) if components else None,
        'first_component': list(map(str, components[0])) if components else None,
        'all_components': [list(map(str, pair)) for pair in components],
        'threshold_count': threshold_count, 'final_time': str(t),
        'final_safe': joint(vs, t), 'trace': trace, 'calls': calls,
        'completed_rounds': completed_rounds, 'started_rounds': started_rounds,
        'nonzero_moves': len(selected),
        'selected_intervals': [
            {'runner': i, 'occurrence': k, 'left': str(lo), 'right': str(hi)}
            for i, k, lo, hi in selected],
        'consecutive_overlaps': list(map(str, overlaps)),
        'union_span': union_span, 'selected_excess': str(selected_excess),
        'selected_excess_from_start': str(selected_excess_from_start),
        'actual_excess_union': str(actual_union),
        'actual_excess_from_start': str(actual_start),
        'H_union_difference': str(H_union_difference),
        'H_start_difference': str(H_start_difference),
        'union_partition_cells': union_cells, 'start_partition_cells': start_cells,
        'Q': Q, 'eta': str(eta), 'H_start': str(Hstart), 'Hmax': str(Hmax),
        'K_global': Kglobal, 'K_phase': Kphase, 'K': K, 'm_L': m_L,
        'core_safe': True,
    }


def main():
    protocol = json.loads((HERE/'protocol.json').read_text())
    assert F(protocol['threshold']) == D
    order = protocol['algorithm']['round_order']
    records = [case_record(case, order) for case in protocol['cases']]
    result = {'status': 'pass',
              'provenance': 'Independent threshold and clipping reconstruction from protocol only; no primary imports or answers.',
              'cases': records}
    (HERE/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'pass', 'cases': len(records),
                      'empty': sum(r['verdict']=='empty' for r in records),
                      'scalar_calls': sum(r['calls'] for r in records),
                      'nonzero_moves': sum(r['nonzero_moves'] for r in records),
                      'max_started_rounds': max(r['started_rounds'] for r in records)}))


if __name__ == '__main__':
    main()
