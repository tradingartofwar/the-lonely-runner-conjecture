#!/usr/bin/env python3
"""Independent coordinate-lap review; standard library, no production imports.

Only the protocol's 54 progression cases and two negative physical controls
are evaluated. Coefficient classification is a separate symbolic contract.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
CORE = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)]
PAIRS = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1),
         (2, 3), (3, 1), (1, 6), (2, 5), (3, 2), (3, 4),
         (4, 3), (5, 2), (5, 7), (3, 5), (4, 6), (6, 10)]
L = [(F(1, 4), F(3, 8)), (F(3, 8), F(1, 8))]
C = (F(1, 8), F(1, 4))


def floor(x):
    return x.numerator // x.denominator


def frac(x):
    return x - floor(x)


def ceiling(x):
    return -floor(-x)


def packed(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [packed(v) for v in value]
    if isinstance(value, dict):
        return {k: packed(v) for k, v in value.items()}
    return value


def leader_contact(P, Q):
    hs = [Q*x-P*y for x, y in L]
    h = ceiling(hs[0])
    if h > hs[1]:
        return None
    z = (h-hs[0]) / (hs[1]-hs[0])
    point = tuple(L[0][j]+z*(L[1][j]-L[0][j]) for j in range(2))
    return point, h


def recover(A, B, p, q, assert_safe=True):
    d = gcd(p, q)
    P, Q = p//d, q//d
    contact = leader_contact(P, Q)
    if contact is None:
        assert (P, Q) == (1, 2)
        point, h, role = C, 0, 'C'
    else:
        point, h = contact
        role = 'L'
    x, y = point
    assert Q*x-P*y == h
    # Independently recover the clock through the first coordinate's lap.
    i = (-h * pow(Q, -1, P)) % P if P > 1 else 0
    assert (Q*i+h) % P == 0
    j = (Q*i+h)//P
    tau = (x+i)/P
    assert 0 < tau < 1 and P*tau == x+i and Q*tau == y+j
    t = tau/d
    rows = CORE + [(A, B)]
    speeds = [a*p+b*q for a, b in rows]
    torus_values = [a*x+b*y for a, b in rows]
    torus_laps = list(map(floor, torus_values))
    phases = list(map(frac, torus_values))
    laps = [m+a*i+b*j for (a, b), m in zip(rows, torus_laps)]
    direct_values = [v*t for v in speeds]
    assert list(map(frac, direct_values)) == phases
    assert list(map(floor, direct_values)) == laps
    reflected_time = 1-t
    reflected_phases = [frac(v*reflected_time) for v in speeds]
    reflected_laps = [floor(v*reflected_time) for v in speeds]
    assert reflected_phases == [0 if f == 0 else 1-f for f in phases]
    assert reflected_laps == [v-m-(f != 0) for v, m, f in zip(speeds, laps, phases)]
    minimum = min(min(f, 1-f) for f in phases)
    if assert_safe:
        assert all(F(1, 8) <= f <= F(7, 8) for f in phases)
        assert minimum == F(1, 8)
    # Positivity implies no collision with p or q. Core collisions are p=q only.
    noncollisions = [(A-a)*p+(B-b)*q != 0 for a, b in CORE[2:]]
    distinct = p != q and all(noncollisions)
    assert distinct == (len(set([0] + speeds)) == 8)
    return packed(dict(row=[A, B], pair=[p, q], gcd=d, primitive=[P, Q],
                       role=role, point=point, h=h, coordinate_laps=[i, j],
                       primitive_time=tau, time=t, speeds=speeds,
                       torus_laps=torus_laps, phases=phases,
                       physical_laps=laps, reflected_time=reflected_time,
                       reflected_phases=reflected_phases,
                       reflected_laps=reflected_laps, minimum=minimum,
                       distinct_speeds=distinct))


def main():
    # Complete finite coverage complement, justified by Q+2P<8.
    residual = []
    for P in range(1, 4):
        for Q in range(1, 8-2*P):
            if gcd(P, Q) == 1:
                residual.append(dict(pair=[P, Q], hit=leader_contact(P, Q) is not None))
    assert len(residual) == 8
    assert [v['pair'] for v in residual if not v['hit']] == [[1, 2]]
    core_endpoints = []
    for point, labels in [(L[0], [0, 0, 0, 0, 1, 1]),
                          (L[1], [0, 0, 0, 0, 1, 1]),
                          (C, [0]*6)]:
        phases = [a*point[0]+b*point[1]-m for (a, b), m in zip(CORE, labels)]
        assert all(F(1, 8) <= f <= F(7, 8) for f in phases)
        core_endpoints.append(packed(dict(point=point, phases=phases)))
    archive = json.loads((HERE.parent/'2026-09-29-cc-coefficient-transfer'/'run.json').read_text())
    archived = {tuple(v['pair']): v for v in archive['controls']}
    assert list(archived) == PAIRS
    controls, stale_labels = [], []
    for k in range(3):
        A, B = 6+16*k, 2+8*k
        for p, q in PAIRS:
            out = recover(A, B, p, q)
            old = archived[(p, q)]
            assert out['time'] == old['time']
            assert out['point'] == old['point']
            assert out['phases'] == old['phases']
            if k == 0:
                for key in ('primitive', 'gcd', 'h', 'primitive_time', 'time',
                            'speeds', 'point', 'torus_laps', 'physical_laps',
                            'phases', 'reflected_time', 'reflected_phases',
                            'reflected_laps', 'distinct_speeds', 'minimum'):
                    assert out[key] == old[key], (key, p, q)
            i, j = out['coordinate_laps']
            constant = 7 if out['role'] == 'L' else 4
            assert out['torus_laps'][6] == old['torus_laps'][6] + constant*k
            shift = k*(constant+16*i+8*j)
            assert out['physical_laps'][6] == old['physical_laps'][6]+shift
            if k:
                x, y = map(F, out['point'])
                stale = A*x+B*y-old['torus_laps'][6]
                assert stale > 1 and stale != F(out['phases'][6])
                stale_labels.append(packed(dict(row=[A, B], pair=[p, q],
                    stale_seventh_label=old['torus_laps'][6], claimed_phase=stale,
                    true_seventh_label=out['torus_laps'][6], phase=out['phases'][6])))
            controls.append(dict(k=k, **out))
    negative = [recover(4, 2, 1, 2, False), recover(5, 2, 2, 3, False)]
    assert [(v['role'], v['time'], v['phases'][6], v['minimum']) for v in negative] == [
        ('C', '1/8', '0', '0'), ('L', '1/8', '0', '0')]
    assert all(v['distinct_speeds'] for v in negative)
    # Ambient F control only. No extra (p,q) is evaluated here.
    native = [(F(1, 8), F(3, 16)), (F(1, 8), F(9, 40)), C]
    vals = [22*x+10*y for x, y in native]
    assert vals == [F(37, 8), F(5), F(21, 4)]
    ambient = [packed(dict(point=point, seventh_value=value,
                           lap=floor(value), phase=frac(value)))
               for point, value in zip(native, vals)]
    result = dict(status='PASS', method='coordinate congruence and direct physical multiplication; no production imports',
        counts=dict(progression_configurations=54, distinct_speed_configurations=51,
                    repeated_speed_auxiliaries=3, selected_phase_checks=378,
                    reflected_phase_checks=378, selected_lap_checks=378,
                    reflected_lap_checks=378, negative_physical_controls=2,
                    stale_label_failures=36, archived_cases_reproduced=18),
        residual_coverage=residual, core_endpoint_checks=core_endpoints,
        progression_controls=controls, negative_controls=negative,
        ambient_fallback_control=ambient, stale_label_controls=stale_labels,
        symbolic_progression=dict(leader_seventh_lap='2+7k',
                                 fallback_C_seventh_lap='1+4k',
                                 leader_seventh_phase='2x-1/4',
                                 fallback_C_seventh_phase='1/4',
                                 physical_seventh_lap_shift='k*(c+16i+8j), c=7 on L and c=4 at C'),
        scope='Finite checks are only the frozen 54 configurations and two negative controls. R sufficiency and progression uniformity depend on the accompanying algebraic proof.')
    (HERE/'physical_review.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'], counts=result['counts']), sort_keys=True))


if __name__ == '__main__':
    main()
