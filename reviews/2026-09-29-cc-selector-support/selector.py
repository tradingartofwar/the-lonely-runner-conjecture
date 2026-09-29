#!/usr/bin/env python3
"""Complete selector-safety reduction; frozen scope is in PROTOCOL.md."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'2026-09-29-cc-coefficient-range'
CORE = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)]


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
    return x.numerator//x.denominator


def phase(x):
    return x-floor(x)


def safe(x):
    return F(1, 8) <= phase(x) <= F(7, 8)


def contact(P, Q):
    assert P > 0 and Q > 0 and gcd(P, Q) == 1
    M = Q+2*P
    rho = (-P-2*M) % 8
    h = (2*Q-3*P+rho)//8
    assert 8*h-(2*Q-3*P) == rho
    if rho <= M:
        x, role = F(1, 4)+F(rho, 8*M), 'L'
        y = F(7, 8)-2*x
    else:
        assert (P, Q) == (1, 2)
        x, y, h, role = F(1, 8), F(1, 4), 0, 'C'
    assert Q*x-P*y == h
    assert all(safe(a*x+b*y) for a, b in CORE)
    return dict(pair=[P, Q], M=M, rho=rho, h=h, point=[x, y], role=role)


def bezout(P, Q):
    old_r, r, old_s, s, old_t, t = P, Q, 1, 0, 0, 1
    while r:
        q = old_r//r
        old_r, r = r, old_r-q*r
        old_s, s = s, old_s-q*s
        old_t, t = t, old_t-q*t
    assert old_r == 1 and old_s*P+old_t*Q == 1
    return old_s, old_t


def physical(A, B, p, q):
    d = gcd(p, q)
    P, Q = p//d, q//d
    out = contact(P, Q)
    x, y = out['point']
    h = out['h']
    r, s = bezout(P, Q)
    T = r*x+s*y
    N = floor(T)
    tau, t = T-N, (T-N)/d
    assert 0 < tau < 1 and phase(P*tau) == x and phase(Q*tau) == y
    rows = CORE+[(A, B)]
    speeds = [a*p+b*q for a, b in rows]
    raw = [a*x+b*y for a, b in rows]
    labels = list(map(floor, raw))
    phases = list(map(phase, raw))
    laps = [m+(-a*s+b*r)*h-(a*P+b*Q)*N for (a, b), m in zip(rows, labels)]
    assert phases == [phase(v*t) for v in speeds]
    assert laps == [floor(v*t) for v in speeds]
    assert all(F(1, 8) <= f <= F(7, 8) for f in phases[:6])
    distinct = len(set([0]+speeds)) == 8
    assert distinct == (p != q and all((A-a)*p+(B-b)*q != 0 for a, b in CORE[2:]))
    reflected = [phase(v*(1-t)) for v in speeds]
    reflected_laps = [floor(v*(1-t)) for v in speeds]
    assert reflected == [1-f if f else F(0) for f in phases]
    assert reflected_laps == [v-m-int(bool(f)) for v, m, f in zip(speeds, laps, phases)]
    return packed(dict(row=[A, B], pair=[p, q], gcd=d, primitive=[P, Q],
        role=out['role'], point=[x, y], h=h, M=out['M'], rho=out['rho'],
        bezout=[r, s], N=N, primitive_time=tau, time=t, speeds=speeds,
        torus_laps=labels, physical_laps=laps, phases=phases,
        reflected_time=1-t, reflected_phases=reflected, reflected_laps=reflected_laps,
        distinct_speeds=distinct, minimum=min(min(f, 1-f) for f in phases),
        seventh_safe=F(1, 8) <= phases[6] <= F(7, 8)))


def R_contract(A, B):
    u, v, w = 2*A+3*B, 3*A+B, A+2*B
    m = min(u, v)//8
    return 8*m+1 <= min(u, v) <= max(u, v) <= 8*m+7 and w % 8 != 0


def main():
    if not __debug__:
        raise RuntimeError('Run without -O')
    pins = {'classification.json': '665dd26bc1c84ec5033d5a3b5ac5784df70c7faa1202e1533e4ff160d07735c0',
            'witnesses.json': 'da9cb5bb4bd588909a667c08e522296733a5ad5a5a617e548d3b01eb99fa0ba6'}
    for name, sha in pins.items():
        assert digest(PRIOR/name) == sha
    assert digest(HERE/'PROTOCOL.md') == 'be10097639d5742d17da199ae34166965e4a5b41af60f4052b4a289c1c0c6594'
    provenance = dict(input_head='78c6b25cc4e96d35c6a60595120deb754bd90187',
                      script_sha256=digest(Path(__file__)), source_sha256=pins,
                      protocol_sha256=digest(HERE/'PROTOCOL.md'))
    directions = [contact(P, M-2*P) for M in range(3, 92)
                  for P in range(1, (M+1)//2) if gcd(P, M) == 1]
    assert [d['pair'] for d in directions if d['role'] == 'C'] == [[1, 2]]
    support = dict(provenance=provenance, directions=directions,
        counts=dict(all_primitive_directions=len(directions),
                    primary_directions=sum(d['pair'][0] != d['pair'][1] for d in directions),
                    distinct_leader_points=len({tuple(d['point']) for d in directions if d['role']=='L'})),
        scope='Complete bounded support 3<=M<=91, not the infinite support; the proven tail handles M>91.')
    prior_classes = json.loads((PRIOR/'classification.json').read_text())['R_accepted_B_residues_by_delta']
    cells, failures, additional = [], [], []
    for delta in range(-13, 14):
        for b in range(8):
            B, A = b+8, 2*(b+8)+delta
            assert A > 0 and B > 0
            a = (7*B+2*delta) % 8
            tail = a != 0 and not (delta > 0 and a == 7) and not (delta < 0 and a == 1)
            raw = [A*d['point'][0]+B*d['point'][1] for d in directions]
            hits = [safe(v) for v in raw]
            primary_bad = [i for i, (d, hit) in enumerate(zip(directions, hits))
                           if d['pair'][0] != d['pair'][1] and not hit]
            all_bad = [i for i, hit in enumerate(hits) if not hit]
            t_ok, ta_ok = tail and not primary_bad, tail and not all_bad
            r_ok = R_contract(A, B)
            assert r_ok == (b in prior_classes.get(str(delta), []))
            # Failed boundary/tail conditions already have bounded witnesses here.
            assert tail or primary_bad
            cell = dict(delta=delta, B_mod8=b, representative=[A, B],
                left_phase=F(a, 8), tail_safe=tail, T=t_ok, T_all=ta_ok, R=r_ok,
                finite_primary_failures=len(primary_bad), finite_all_failures=len(all_bad),
                phase_vector_sha256=hashlib.sha256(json.dumps(packed(list(map(phase, raw))),
                                                             separators=(',', ':')).encode()).hexdigest(),
                first_failure_pair=directions[primary_bad[0]]['pair'] if primary_bad else None)
            cells.append(cell)
            if primary_bad:
                P, Q = directions[primary_bad[0]]['pair']
                failure = physical(A, B, P, Q)
                assert not failure['seventh_safe'] and failure['distinct_speeds']
                failures.append(dict(delta=delta, B_mod8=b, **failure))
            if t_ok and not r_ok:
                additional.append(cell)
    accepted = {delta: [c['B_mod8'] for c in cells if c['delta']==delta and c['T']]
                for delta in range(-13, 14)}
    classification = dict(status='PASS', provenance=provenance, cells=cells,
        accepted_B_residues_by_delta=accepted,
        counts=dict(cells=len(cells), T=sum(c['T'] for c in cells),
                    T_all=sum(c['T_all'] for c in cells), R=sum(c['R'] for c in cells),
                    outside_R=len(additional), negative_certificates=len(failures)),
        T_equals_R=all(c['T']==c['R'] for c in cells),
        T_all_equals_R=all(c['T_all']==c['R'] for c in cells),
        scope='Complete delta/residue reduction with analytic |delta|>=14 obstruction and M>=91 tail; primary p!=q and auxiliary-inclusive contracts separated.')
    archive = json.loads((PRIOR/'witnesses.json').read_text())['progression_controls']
    positive = []
    for old in archive:
        A, B = old['row']
        p, q = old['pair']
        out = physical(A, B, p, q)
        for key in ('row', 'pair', 'gcd', 'primitive', 'role', 'point', 'h', 'primitive_time',
                    'time', 'speeds', 'torus_laps', 'physical_laps', 'phases',
                    'reflected_time', 'reflected_phases', 'reflected_laps', 'minimum',
                    'distinct_speeds'):
            assert out[key] == old[key], (key, A, B, p, q)
        assert out['seventh_safe'] and out['minimum'] == '1/8'
        positive.append(out)
    extra_controls = []
    if additional:
        A, B = additional[0]['representative']
        for old in archive[:18]:
            p, q = old['pair']
            # T only covers p!=q; keep any auxiliary result explicitly labelled.
            extra_controls.append(physical(A, B, p, q))
    witnesses = dict(status='PASS', provenance=provenance,
        progression_controls=positive, negative_certificates=failures,
        postclassification_extra_controls=extra_controls,
        counts=dict(archived_configurations_reproduced=len(positive),
                    derived_negative_certificates=len(failures),
                    postclassification_extra_controls=len(extra_controls)),
        scope='54 archived configurations; one derived failure per rejected residue cell. These failures are not held-out trials.')
    for name, obj in [('support.json', support), ('classification.json', classification),
                      ('witnesses.json', witnesses)]:
        (HERE/name).write_text(json.dumps(packed(obj), indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS', classification=classification['counts'],
                          support=support['counts'], witnesses=witnesses['counts']), sort_keys=True))


if __name__ == '__main__':
    main()
