#!/usr/bin/env python3
"""Exact fixed-geometry classification and frozen physical controls.

Standard library only. No clipping, discovery or optimization. See PROTOCOL.md.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / '2026-09-29-cc-coefficient-transfer'
CORE = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)]
PAIRS = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 3), (3, 1),
         (1, 6), (2, 5), (3, 2), (3, 4), (4, 3), (5, 2), (5, 7),
         (3, 5), (4, 6), (6, 10)]
L = [(F(1, 4), F(3, 8)), (F(3, 8), F(1, 8))]
FALLBACK = [(F(1, 8), F(3, 16)), (F(1, 8), F(1, 4))]
C = FALLBACK[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packed(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [packed(v) for v in value]
    if isinstance(value, dict):
        return {str(k): packed(v) for k, v in value.items()}
    return value


def floor(x):
    return x.numerator // x.denominator


def frac(x):
    return x - floor(x)


def classify(A, B):
    assert A > 0 and B > 0
    u, v, w = 2*A+3*B, 3*A+B, A+2*B
    lo, hi = min(u, v), max(u, v)
    m, n, c = lo//8, u//16, w//8
    ls = 8*m+1 <= lo <= hi <= 8*m+7
    fs = 16*n+2 <= u <= u+B <= 16*n+14
    cs = w % 8 != 0
    return dict(row=[A, B], delta=A-2*B, B_mod8=B % 8, u=u, v=v, w=w,
                L_safe=ls, F_safe=fs, C_safe=cs, W=ls and fs, R=ls and cs,
                L_lap=m if ls else None, F_lap=n if fs else None,
                C_lap=c if cs else None,
                L_image=[F(lo, 8), F(hi, 8)],
                F_image=[F(u, 16), F(u+B, 16)], C_value=F(w, 8))


def bezout(P, Q):
    old_r, r, old_s, s, old_t, t = P, Q, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r-q*r
        old_s, s = s, old_s-q*s
        old_t, t = t, old_t-q*t
    assert old_r == 1 and old_s*P+old_t*Q == 1
    return old_s, old_t


def recover(A, B, p, q, require_R=True):
    contract = classify(A, B)
    if require_R:
        assert contract['R']
    d = gcd(p, q)
    P, Q = p//d, q//d
    lower, upper = F(2*Q-3*P, 8), F(3*Q-P, 8)
    h = -floor(-lower)
    if h <= upper:
        x = F(8*h+7*P, 8*(Q+2*P))
        y, role, core_laps = F(7, 8)-2*x, 'L', [0, 0, 0, 0, 1, 1]
    else:
        assert (P, Q) == (1, 2)
        x, y = C
        h, role, core_laps = 0, 'C', [0]*6
    assert Q*x-P*y == h
    r, s = bezout(P, Q)
    T = r*x+s*y
    N = floor(T)
    tau = T-N
    t = tau/d
    assert 0 < tau < 1 and frac(P*tau) == x and frac(Q*tau) == y
    rows = CORE+[(A, B)]
    values = [a*x+b*y for a, b in rows]
    labels = core_laps+[floor(values[6])]
    phases = [value-m for value, m in zip(values, labels)]
    speeds = [a*p+b*q for a, b in rows]
    laps = [m+(-a*s+b*r)*h-(a*P+b*Q)*N
            for (a, b), m in zip(rows, labels)]
    assert phases == [frac(v*t) for v in speeds]
    assert laps == [floor(v*t) for v in speeds]
    minimum = min(min(f, 1-f) for f in phases)
    if require_R:
        expected = contract['L_lap'] if role == 'L' else contract['C_lap']
        assert labels[6] == expected
        assert all(F(1, 8) <= f <= F(7, 8) for f in phases)
        assert minimum == F(1, 8)
    alt = frac((r+Q)*x+(s-P)*y)/d
    assert alt == t
    reflected = [frac(v*(1-t)) for v in speeds]
    reflected_laps = [floor(v*(1-t)) for v in speeds]
    assert reflected == [1-f if f else F(0) for f in phases]
    assert reflected_laps == [v-m-int(bool(f)) for v, m, f in zip(speeds, laps, phases)]
    distinct = p != q and all((A-a)*p+(B-b)*q != 0 for a, b in CORE[2:])
    assert distinct == (len(set([0]+speeds)) == 8)
    return packed(dict(row=[A, B], pair=[p, q], gcd=d, primitive=[P, Q],
                       role=role, point=[x, y], h=h, bezout=[r, s], N=N,
                       primitive_time=tau, time=t, alternate_bezout_time=alt,
                       speeds=speeds, torus_laps=labels, phases=phases,
                       physical_laps=laps, reflected_time=1-t,
                       reflected_phases=reflected, reflected_laps=reflected_laps,
                       minimum=minimum, distinct_speeds=distinct,
                       contract_R=contract['R']))


def main():
    if not __debug__:
        raise RuntimeError('Run without -O; exact checks use assertions')
    pins = {'certificate.json': '6e62958d0b0f081ee0213054e1ea02f3da4de30de2278812b37d3e938d71431d',
            'run.json': '0c7e680983dde7941022c4b242970fb4678914c34884cdaa5b5f8d679f12e72a'}
    for name, sha in pins.items():
        assert digest(PRIOR/name) == sha
    assert digest(HERE/'PROTOCOL.md') == 'f867de38d4cd852313c50d824b8909378f808865e8bfe5a81804e3b9617c1a4c'
    cert = json.loads((PRIOR/'certificate.json').read_text())
    records = {row['id']: row for row in cert['candidates']}
    for name, ends, labels in [('P2:E0-3:K2', L, [0, 0, 0, 0, 1, 1, 2]),
                               ('P0:E0-1:K1', FALLBACK, [0, 0, 0, 0, 0, 0, 1])]:
        assert records[name]['endpoints'] == packed(ends)
        assert records[name]['labels'] == labels
        for x, y in ends:
            assert all(F(1, 8) <= a*x+b*y-m <= F(7, 8)
                       for (a, b), m in zip(CORE, labels))
    assert cert['chosen_ids'] == ['P2:E0-3:K2', 'P0:E0-1:K1']
    finite = [classify(2*B+delta, B) for B in range(1, 13)
              for delta in range(-6, 7) if 2*B+delta > 0]
    table = [dict(delta=delta, B_mod8=b, representative=classify(2*(b+8)+delta, b+8))
             for delta in range(-6, 7) for b in range(8)]
    for cell in table:
        cell['R'] = cell['representative']['R']
    accepted = {delta: [c['B_mod8'] for c in table if c['delta'] == delta and c['R']]
                for delta in range(-6, 7)}
    wrows = sorted(c['row'] for c in finite if c['W'])
    assert len(finite) == 147 and len(wrows) == 31
    assert len(table) == 104 and sum(c['R'] for c in table) == 42
    for case in finite:
        assert not case['W'] or case['R']
        assert case['R'] == (case['B_mod8'] in accepted[case['delta']])
    assert classify(4, 5)['W'] and classify(23, 12)['W']
    ambient = []
    for point in [FALLBACK[0], (F(1, 8), F(9, 40)), C]:
        x, y = point
        values = [a*x+b*y for a, b in CORE+[(22, 10)]]
        phases = list(map(frac, values))
        assert all(F(1, 8) <= f <= F(7, 8) for f in phases[:6])
        ambient.append(dict(point=point, values=values, phases=phases,
                            laps=list(map(floor, values))))
    assert [c['values'][6] for c in ambient] == [F(37, 8), F(5), F(21, 4)]
    assert classify(22, 10)['R'] and not classify(22, 10)['W']
    provenance = dict(input_head='9e72fb318d83a4556f9063553da5a0b207aec72c',
                      protocol_sha256=digest(HERE/'PROTOCOL.md'),
                      script_sha256=digest(Path(__file__)), source_sha256=pins)
    classification = dict(status='PASS', provenance=provenance,
        finite_W_domain_count=len(finite), finite_W_accepted_count=len(wrows),
        R_residue_cell_count=len(table), R_residue_class_count=sum(c['R'] for c in table),
        W_rows=wrows, W_complete_finite_domain=finite, R_complete_13_by_8=table,
        R_accepted_B_residues_by_delta=accepted, W_proper_subset_R=True,
        ambient_22_10_control=ambient, boundary_rows=[classify(4, 5), classify(23, 12)],
        identically_repeated_core_rows=[[1, 1], [2, 1], [3, 1], [3, 2]],
        scope='Exact W/R geometric contracts via proved finite/residue reductions; not maximal deterministic-selector success or global witness existence.')
    archive = json.loads((PRIOR/'run.json').read_text())['controls']
    assert [tuple(c['pair']) for c in archive] == PAIRS
    controls, stale = [], []
    for k in range(3):
        for (p, q), old in zip(PAIRS, archive):
            out = recover(6+16*k, 2+8*k, p, q)
            for key in ('point', 'time', 'phases'):
                assert out[key] == old[key]
            if k == 0:
                for key in ('primitive', 'gcd', 'h', 'primitive_time', 'time', 'speeds',
                            'point', 'torus_laps', 'physical_laps', 'phases',
                            'reflected_time', 'reflected_phases', 'reflected_laps',
                            'distinct_speeds', 'minimum'):
                    assert out[key] == old[key], (key, p, q)
            constant = 7 if out['role'] == 'L' else 4
            assert out['torus_laps'][6] == old['torus_laps'][6]+constant*k
            if k:
                x, y = map(F, out['point'])
                wrong = (6+16*k)*x+(2+8*k)*y-old['torus_laps'][6]
                assert wrong > 1 and wrong != F(out['phases'][6])
                stale.append(dict(row=out['row'], pair=[p, q], claimed_phase=wrong,
                                  correct_phase=out['phases'][6]))
            controls.append(dict(k=k, **out))
    negative = [recover(4, 2, 1, 2, False), recover(5, 2, 2, 3, False)]
    assert all(v['time'] == '1/8' and v['phases'][6] == '0'
               and v['distinct_speeds'] and not v['contract_R'] for v in negative)
    witnesses = dict(status='PASS', provenance=provenance,
        counts=dict(progression_configurations=len(controls),
                    distinct_speed_configurations=sum(v['distinct_speeds'] for v in controls),
                    repeated_speed_auxiliaries=sum(not v['distinct_speeds'] for v in controls),
                    archived_cases_reproduced=18, negative_physical_controls=2,
                    stale_label_failures=len(stale)),
        progression_controls=controls, negative_controls=negative, stale_label_controls=stale,
        scope='Only predeclared k=0,1,2 and 18 pairs plus two negative controls; infinite progression relies on symbolic identity.')
    for name, obj in [('classification.json', classification), ('witnesses.json', witnesses)]:
        (HERE/name).write_text(json.dumps(packed(obj), indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS', W_rows=len(wrows), R_classes=42,
                          physical_controls=len(controls), negative_controls=2), sort_keys=True))


if __name__ == '__main__':
    main()
