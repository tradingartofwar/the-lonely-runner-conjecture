"""Exact replacement-speed classification; standard library, no sampling.

--write creates the archive. Default/--check replays and compares read-only.
Finite arithmetic is evidence; the completeness argument is in the note.
"""
import argparse
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
OUT = HERE / 'fixed_containment.json'
D = F(1, 8)
J = (F(9, 32), F(5, 16))
S = (F(17, 56), F(5, 16))
FIXED = (1, 4, 5, 6, 7)
BASELINE = '9831bbee22c0e226911eac99e65a0c9624bef963'


def dist(z):
    z %= 1
    return min(z, 1-z)


def primitive(z):
    m = floor(z)
    r = z-m
    return F(m, 4) + min(r, D) + max(F(0), r-1+D)


def blocked_length(v, window):
    a, b = window
    return (primitive(v*b)-primitive(v*a))/v


def intersection(left, right):
    return [(max(a, c), min(b, d)) for a, b in left for c, d in right
            if max(a, c) <= min(b, d)]


def feasible(speeds, window):
    result = [window]
    for v in speeds:
        safe = [((m+D)/v, (m+1-D)/v) for m in range(v)]
        result = intersection(result, safe)
    return result


def duration(intervals):
    return sum((b-a for a, b in intervals), F(0))


def encode(intervals):
    return [[str(a), str(b)] for a, b in intervals]


def classification(x):
    lower = ceil(x*S[1]-1+D)
    upper = floor(x*S[0]-D)
    safe = lower <= upper
    row = dict(x=x, lap_lower=lower, lap_upper=upper, safe_on_S=safe,
               repeated_fixed_speed=x in FIXED,
               admissible=safe and x not in FIXED,
               blocked_duration_S=str(blocked_length(x, S)))
    assert safe == (F(row['blocked_duration_S']) == 0)
    if safe:
        assert lower == upper
        m = lower
        p, q = 17*x-56*m-7, 16*m+14-5*x
        assert min(p, q) >= 0 and 2*p+7*q == 84-x
        row.update(lap=m, integer_slacks=[p, q],
                   phase_margins=[str(F(p, 56)), str(F(q, 16))],
                   threshold_endpoints=[name for name, slack in
                                        [('left', p), ('right', q)] if slack == 0])
    else:
        # A strict violating witness, not just an unsafe numerical sample.
        for m in range(x+1):
            a, b = max(S[0], (m-D)/x), min(S[1], (m+D)/x)
            if a < b:
                t = (a+b)/2
                assert dist(x*t) < D
                row.update(violating_time=str(t),
                           violating_distance=str(dist(x*t)))
                break
        assert 'violating_time' in row
    return row


def certificate(x, y):
    speeds = FIXED + (x, y)
    assert len(set((0,)+speeds)) == 8
    residual = (5, 7, x, y)
    events = set(J)
    for v in residual:
        for m in range(v):
            for phase in (D, 1-D):
                t = (m+phase)/v
                if J[0] < t < J[1]:
                    events.add(t)
    cuts = sorted(events)
    masses = [F(0)]*16
    for a, b in zip(cuts, cuts[1:]):
        t = (a+b)/2
        state = sum(1 << i for i, v in enumerate(residual) if dist(v*t) < D)
        masses[state] += b-a
    singles = [sum((masses[s] for s in range(16) if s & (1 << i)), F(0))
               for i in range(4)]
    edges = ((0, 1), (1, 2), (1, 3))
    pairs = [sum((masses[s] for s in range(16)
                  if s & (1 << i) and s & (1 << j)), F(0)) for i, j in edges]
    tree = J[1]-J[0]-sum(singles)+sum(pairs)
    allowed = feasible(speeds, J)
    actual = duration(allowed)
    assert actual == masses[0] and tree <= actual
    assert tree == S[1]-S[0]-blocked_length(x, S)-blocked_length(y, S)
    if classification(x)['admissible']:
        assert tree == actual == S[1]-S[0]-blocked_length(y, S)
    witness = next((a+b)/2 for a, b in allowed if a < b)
    distances = [dist(v*witness) for v in speeds]
    assert min(distances) > D
    return dict(x=x, y=y, residual=list(residual),
                tree_edges=[[residual[i], residual[j]] for i, j in edges],
                single_durations=list(map(str, singles)),
                edge_overlap_durations=list(map(str, pairs)),
                tree_bound=str(tree), actual_duration=str(actual),
                tree_slack=str(actual-tree), allowed_on_J=encode(allowed),
                strict_witness=str(witness), witness_distances=list(map(str, distances)))


def run():
    assert J in feasible((1, 4, 6), (F(0), F(1)))
    assert feasible(FIXED, J) == [S]
    rows = [classification(x) for x in range(1, 86)]
    raw = [r['x'] for r in rows if r['safe_on_S']]
    admissible = [r['x'] for r in rows if r['admissible']]
    assert len(raw) == 35 and len(admissible) == 30 and max(admissible) == 73
    cases = [(x, 29) for x in admissible] + [(11, y) for y in (28, 44, 45, 46)] + [(19, 45)]
    certs = [certificate(x, y) for x, y in cases]
    for c in certs:
        if c['x'] in admissible:
            assert F(c['actual_duration']) >= F(3, 448)-F(3, 16*c['y'])
    correction = [(z, primitive(z)-z/4) for z in (F(0), D, 1-D, F(1))]
    assert max(v for z, v in correction)-min(v for z, v in correction) == F(3, 16)
    return dict(baseline_commit=BASELINE, reference=0, total_runners=8,
                threshold=str(D), fixed_speeds=list(FIXED), core=[1, 4, 6],
                J=list(map(str, J)), S=list(map(str, S)),
                exhaustive_finite_domain=[1, 84], extra_failure_control=85,
                raw_safe_speeds=raw, admissible_replacements=admissible,
                classification=rows, certificates=certs,
                primitive_correction_vertices=[[str(z), str(v)] for z, v in correction],
                claim_status='OBSERVED / REPRODUCED finite evidence; unbounded completeness and tail remain proof candidates.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert json.loads(OUT.read_text()) == result
    print('PASS: 85 exact classifications; 30 admissible replacements; 35 local certificates.')
