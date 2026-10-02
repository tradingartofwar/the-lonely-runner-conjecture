#!/usr/bin/env python3
"""Independent exact review: direct interval selection and coordinate congruences.

No coordinator imports. The mathematical prerequisites are proved in the
accompanying markdown; enumeration is the protocol's complete finite reduction.
Only archived progression cases receive positive physical checks.
"""
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2))
OLD = ROOT / 'reviews/2026-09-29-cc-coefficient-range'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe(value):
    return F(1, 8) <= value % 1 <= F(7, 8)


def select(p, q):
    d = gcd(p, q)
    P, Q = p // d, q // d
    lo, hi = F(2 * Q - 3 * P, 8), F(3 * Q - P, 8)
    h = ceil(lo)
    M = Q + 2 * P
    rho = 8 * h - (2 * Q - 3 * P)
    assert rho == (-P - 2 * M) % 8
    if h <= hi:
        x = F(8 * h + 7 * P, 8 * M)
        y = F(7, 8) - 2 * x
        role = 'L'
        assert x == F(1, 4) + F(rho, 8 * M)
        assert 0 <= rho <= min(7, M)
    else:
        assert (P, Q) == (1, 2)
        x, y, h, role = F(1, 8), F(1, 4), 0, 'C'
    assert Q * x - P * y == h
    assert all(safe(a * x + b * y) for a, b in CORE)
    return dict(P=P, Q=Q, d=d, M=M, rho=rho, x=x, y=y, h=h,
                interval=[lo, hi], role=role)


def physical(A, B, p, q):
    s = select(p, q)
    P, Q, d = s['P'], s['Q'], s['d']
    x, y, h = s['x'], s['y'], s['h']
    i = (-h * pow(Q, -1, P)) % P if P > 1 else 0
    j = (Q * i + h) // P
    assert P * j == Q * i + h
    tau = (x + i) / P
    assert 0 < tau < 1 and Q * tau == y + j
    t = tau / d
    rows = CORE + ((A, B),)
    speeds = [a * p + b * q for a, b in rows]
    values = [a * x + b * y for a, b in rows]
    torus_laps = [floor(value) for value in values]
    laps = [m + a * i + b * j for m, (a, b) in zip(torus_laps, rows)]
    phases = [v * t % 1 for v in speeds]
    assert phases == [v % 1 for v in values]
    assert laps == [floor(v * t) for v in speeds]
    reflected = 1 - t
    return dict(row=[A, B], pair=[p, q], primitive=[P, Q], gcd=d,
                role=s['role'], point=[str(x), str(y)], h=h,
                coordinate_laps=[i, j], primitive_time=str(tau), time=str(t),
                speeds=speeds, torus_laps=torus_laps, physical_laps=laps,
                phases=list(map(str, phases)),
                minimum=str(min(min(f, 1 - f) for f in phases)),
                reflected_time=str(reflected),
                reflected_phases=[str(v * reflected % 1) for v in speeds],
                reflected_laps=[floor(v * reflected) for v in speeds],
                distinct_speeds=len(set([0] + speeds)) == 8,
                seventh_safe=safe(values[-1]),
                core_safe=all(safe(v) for v in values[:-1]))


def whole_leader_and_C(A, B):
    ends = [F(A, 4) + F(3 * B, 8), F(3 * A, 8) + F(B, 8)]
    low, high = min(ends), max(ends)
    lap = floor(low)
    return lap + F(1, 8) <= low <= high <= lap + F(7, 8) and safe(F(A, 8) + F(B, 4))


def serial_support(index, s):
    return dict(index=index, primitive=[s['P'], s['Q']], M=s['M'],
                rho=s['rho'], role=s['role'], h=s['h'],
                interval=list(map(str, s['interval'])),
                point=[str(s['x']), str(s['y'])],
                repeated_speed_auxiliary=s['P'] == s['Q'])


def main():
    # Before executing this reduction, the reviewer derived the |delta|<=13
    # obstruction and M>=91 safe tail, as recorded in classification_review.md.
    support = []
    for M in range(3, 92):
        for P in range(1, (M + 1) // 2):
            Q = M - 2 * P
            if Q > 0 and gcd(P, Q) == 1:
                support.append(select(P, Q))
    assert len(support) == 1275
    assert sum(s['role'] == 'C' for s in support) == 1
    assert sum(s['P'] == s['Q'] for s in support) == 1
    cells, accepted, accepted_all, outside_R = [], [], [], []
    for delta in range(-13, 14):
        for residue in range(8):
            B = residue + 8
            A = 2 * B + delta
            assert A > 0 and B > 0
            a = (2 * A + 3 * B) % 8
            tail_ok = (a != 0 and not (delta > 0 and a == 7)
                       and not (delta < 0 and a == 1))
            failures = []
            auxiliary_failure = None
            for index, s in enumerate(support):
                raw = A * s['x'] + B * s['y']
                if not safe(raw):
                    if s['P'] == s['Q']:
                        auxiliary_failure = index
                    else:
                        failures.append(index)
            # Every analytic tail precondition rejection also has a finite
            # failure in this declared support, so every rejection gets a
            # directly reconstructed distinct-speed certificate.
            assert failures or tail_ok
            T = not failures and tail_ok
            T_all = T and auxiliary_failure is None
            R = whole_leader_and_C(A, B)
            key = [delta, residue]
            if T:
                accepted.append(key)
            if T_all:
                accepted_all.append(key)
            if T and not R:
                outside_R.append(key)
            record = dict(delta=delta, B_mod8=residue, representative=[A, B],
                          left_phase=str(F(a, 8)), tail_preconditions=tail_ok,
                          T=T, T_all=T_all, R=R,
                          distinct_domain_failure_count=len(failures),
                          auxiliary_failure_index=auxiliary_failure,
                          first_failure_index=failures[0] if failures else None)
            if failures:
                s = support[failures[0]]
                certificate = physical(A, B, s['P'], s['Q'])
                assert not certificate['seventh_safe']
                assert certificate['core_safe'] and certificate['distinct_speeds']
                record['first_failure_certificate'] = certificate
            cells.append(record)
    assert len(cells) == 216
    assert len(accepted) == len(accepted_all) == 42
    assert accepted == accepted_all and not outside_R
    assert all(r['T'] == r['R'] for r in cells)
    old_class = json.loads((OLD / 'classification.json').read_text())
    old_keys = [[r['delta'], r['B_mod8']] for r in old_class['R_complete_13_by_8'] if r['R']]
    assert accepted == old_keys

    archive = json.loads((OLD / 'witnesses.json').read_text())
    comparisons = []
    count_fields = 0
    compare_fields = ['row', 'pair', 'primitive', 'gcd', 'role', 'point', 'h',
                      'primitive_time', 'time', 'speeds', 'torus_laps',
                      'physical_laps', 'phases', 'minimum', 'reflected_time',
                      'reflected_phases', 'reflected_laps', 'distinct_speeds']
    for old in archive['progression_controls']:
        A, B = old['row']
        p, q = old['pair']
        current = physical(A, B, p, q)
        assert current['seventh_safe'] and current['core_safe']
        for key in compare_fields:
            assert old[key] == current[key], (old['row'], old['pair'], key)
            count_fields += 1
        current['k'] = old['k']
        current['archive_fields_matched'] = compare_fields
        comparisons.append(current)
    assert len(comparisons) == 54
    assert not outside_R  # Therefore the conditional 18 positive controls do not trigger.

    # Post-computation comparison only. Reading emitted JSON cannot determine
    # our independently computed geometry, classification, or recovery.
    production_support = json.loads((HERE / 'support.json').read_text())
    production_classes = json.loads((HERE / 'classification.json').read_text())
    production_witnesses = json.loads((HERE / 'witnesses.json').read_text())
    direction_map = {tuple(s['pair']): s for s in production_support['directions']}
    direction_fields = 0
    for index, s in enumerate(support):
        ours = serial_support(index, s)
        theirs = direction_map[tuple(ours['primitive'])]
        for left, right in [('primitive', 'pair'), ('M', 'M'), ('rho', 'rho'),
                            ('h', 'h'), ('role', 'role'), ('point', 'point')]:
            assert ours[left] == theirs[right]
            direction_fields += 1
    class_map = {(c['delta'], c['B_mod8']): c for c in production_classes['cells']}
    classification_fields = 0
    for ours in cells:
        theirs = class_map[(ours['delta'], ours['B_mod8'])]
        for left, right in [('T', 'T'), ('T_all', 'T_all'), ('R', 'R'),
                            ('representative', 'representative'),
                            ('left_phase', 'left_phase'),
                            ('tail_preconditions', 'tail_safe'),
                            ('distinct_domain_failure_count', 'finite_primary_failures')]:
            assert ours[left] == theirs[right]
            classification_fields += 1
        expected_pair = (ours['first_failure_certificate']['pair']
                         if ours['first_failure_index'] is not None else None)
        assert theirs['first_failure_pair'] == expected_pair
        assert theirs['finite_all_failures'] == (ours['distinct_domain_failure_count']
                                                 + (ours['auxiliary_failure_index'] is not None))
        classification_fields += 2
    negative_map = {(c['delta'], c['B_mod8']): c
                    for c in production_witnesses['negative_certificates']}
    positive_map = {(tuple(c['row']), tuple(c['pair'])): c
                    for c in production_witnesses['progression_controls']}
    physical_fields = 0
    review_witnesses = [(c['first_failure_certificate'], negative_map[(c['delta'], c['B_mod8'])])
                        for c in cells if c['first_failure_index'] is not None]
    review_witnesses += [(c, positive_map[(tuple(c['row']), tuple(c['pair']))]) for c in comparisons]
    for ours, theirs in review_witnesses:
        for field in compare_fields + ['seventh_safe']:
            assert ours[field] == theirs[field], (ours['row'], ours['pair'], field)
            physical_fields += 1

    output = dict(
        status='Internally reviewed proof candidate; exact finite reduction reproduced',
        method='Direct projected interval rounding; Fraction arithmetic; coordinate-congruence physical recovery; no coordinator imports',
        provenance={str(path.relative_to(ROOT)): digest(path) for path in [
            HERE / 'PROTOCOL.md', HERE / 'classification_review.py',
            OLD / 'classification.json', OLD / 'witnesses.json']},
        prerequisite_arguments=dict(
            delta_bound=13,
            large_slope_family='P=1, Q=4j-2, M=4j, rho=7, j>=2',
            first_forbidden_j_interval_positive='(7D/(4(9-a)), 7D/(4(7-a))) for 1<=a<=6',
            first_forbidden_j_interval_negative='(7D/(4(a+1)), 7D/(4(a-1))) for 2<=a<=7',
            minimum_interval_width='7D/96 > 1 when D>=14',
            minimum_lower_endpoint='7D/32 > 3 when D>=14',
            tail_threshold=91,
            tail_drift_bound='7|delta|/(8M)<=1/8 for |delta|<=13 and M>=91',
            tail_conditions='left residue nonzero; exclude positive drift at 7/8 and negative drift at 1/8',
            proof_location='classification_review.md'),
        support_order='M increasing, then P increasing; Q=M-2P>0 and gcd(P,Q)=1',
        counts=dict(residue_cells=216, support_records=1275,
                    leader_records=1274, fallback_records=1,
                    p_ne_q_support_records=1274,
                    distinct_leader_points=len({(s['x'], s['y']) for s in support if s['role'] == 'L'}),
                    T_classes=len(accepted), T_all_classes=len(accepted_all),
                    R_classes=len(old_keys), rejected_classes=216-len(accepted),
                    genuine_distinct_speed_negative_certificates=sum(not r['T'] for r in cells),
                    archived_positive_controls=54, archived_fields_matched=count_fields,
                    added_positive_controls=0),
        coordinator_comparison=dict(direction_fields_matched=direction_fields, classification_fields_matched=classification_fields, physical_fields_matched=physical_fields, method='JSON comparison after independent calculation; not blind'),
        accepted_classes=accepted, accepted_T_all_classes=accepted_all,
        accepted_outside_R=outside_R,
        coefficient_cells=cells,
        full_bounded_support=[serial_support(i, s) for i, s in enumerate(support)],
        archived_progression_reproductions=comparisons,
        interpretation='T=T_all=R for positive integer coefficient rows. Every rejected finite class has a p!=q failure and eight distinct speeds; this refutes the fixed selector, not loneliness. Four identically core rows remain vacuous for eight-distinct-speed existence.',
        identically_repeated_core_rows=[[1, 1], [2, 1], [3, 1], [3, 2]],
    )
    destination = HERE / 'classification_review.json'
    destination.write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print(json.dumps(output['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
