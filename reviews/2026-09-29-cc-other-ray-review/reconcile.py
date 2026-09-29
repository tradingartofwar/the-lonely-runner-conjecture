#!/usr/bin/env python3
"""Coordinator reconciliation, using the newly reproduced exact certificates.

Checks the cap extrema printed in the supplement and the two quantifier
counterexamples. It is not another independent geometry reconstruction.
No new physical inputs or optimization scan are introduced.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
# Each affine projection is encoded as (constant, coefficient of q).
EXTREMA = {
    (Q(1, 6), Q(1, 6)): ((-1, -2), (1, 1)),
    (Q(1, 6), Q(1, 3)): ((-1, -4), (1, 2)),
    (Q(1, 2), Q(1, 6)): ((-3, -5), (0, 1)),
    (Q(1, 2), Q(1, 3)): ((-1, -2), (0, Q(1, 2))),
    (Q(1, 3), Q(5, 6)): ((-2, -1), (1, 2)),
    (Q(1, 2), Q(2, 3)): ((-1, -2), (0, 1)),
    (Q(1, 2), Q(5, 6)): ((Q(-3, 5), -1), (0, Q(1, 2))),
}


def certify_positive_affine(coeff):
    constant, slope = coeff
    assert slope >= 0 and constant + 2 * slope > 0
    return {'constant': str(constant), 'slope': str(slope),
            'at_q2': str(constant + 2 * slope), 'domain': 'q>=2'}


def check_point(point, labels):
    x, y, z = point
    slacks = [z - Q(1, 8), Q(1, 2) - x]
    phases = []
    for (a, b), m in zip(ROWS, labels):
        phase = a * x + b * y - m
        phases.append(phase)
        slacks.extend((phase - z, 1 - z - phase))
    assert all(s >= 0 for s in slacks)
    return phases, sum(s == 0 for s in slacks)


def main():
    geometry = json.loads((HERE / 'geometry_check.json').read_text())
    arithmetic = json.loads((HERE / 'arithmetic_check.json').read_text())
    cap_records = []
    geometric_directions = set()
    for cell in geometry['cells']:
        if not cell['peak_indices']:
            continue
        assert len(cell['peak_indices']) == 1 and len(cell['peak_edges']) == 3
        peak = tuple(map(Q, cell['vertices'][cell['peak_indices'][0]]))
        lower, upper = EXTREMA[peak[:2]]
        projections = []
        for edge in cell['peak_edges']:
            alpha, beta = Q(edge['alpha']), Q(edge['beta'])
            assert Q(edge['max_loss']) >= Q(1, 42)
            projections.append((alpha, -beta))
            cap_point = (peak[0] + alpha / 42, peak[1] + beta / 42, Q(1, 7))
            check_point(cap_point, cell['labels'])
            geometric_directions.add((peak[:2], alpha, beta, Q(edge['max_loss'])))
        assert lower in projections and upper in projections
        middle = [p for p in projections if p not in (lower, upper)]
        assert len(middle) == 1
        mid = middle[0]
        below = certify_positive_affine(tuple(a - b for a, b in zip(mid, lower)))
        above = certify_positive_affine(tuple(a - b for a, b in zip(upper, mid)))
        certify_positive_affine(tuple(-a for a in lower))
        certify_positive_affine(upper)
        cap_records.append({'peak': list(map(str, peak)),
                            'middle_minus_minimum': below,
                            'maximum_minus_middle': above})
    assert len(cap_records) == 7 and len(geometric_directions) == 21
    letter_to_peak = dict(zip('ABCDEFG', EXTREMA))
    arithmetic_directions = {
        (letter_to_peak[e['peak']], *map(Q, e['direction']), Q(e['maximum_e']))
        for e in arithmetic['edges']
    }
    assert geometric_directions == arithmetic_directions

    point = (Q(37, 80), Q(37, 160), Q(3, 20))
    phases, active_count = check_point(point, (0, 0, 0, 1, 1, 1, 2))
    assert point[0] - 2 * point[1] == 0
    assert active_count == 1
    assert phases == [Q(n, 160) for n in (74, 37, 111, 25, 99, 136, 124)]
    assert min(min(p, 1 - p) for p in phases) == point[2]
    assert Q(1, 7) < point[2] < Q(2, 13)
    singleton = next(c for c in geometry['cells'] if c['labels'] == [0, 0, 0, 0, 1, 1, 2])
    point2 = tuple(map(Q, singleton['vertices'][0]))
    assert singleton['dimension'] == 0 and len(singleton['vertices']) == 1
    assert point2 == (Q(3, 8), Q(1, 8), Q(1, 8))
    check_point(point2, singleton['labels'])
    assert point2[0] - 11 * point2[1] == -1 and point2[2] < Q(11, 69)
    report = {
        'status': 'PASS: reconciliation of supplied fresh certificates',
        'scope': 'B-ray cap projection table and two in-scope quantifier examples; no new scan',
        'source_sha256': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ('reconcile.py', 'geometry_check.json', 'arithmetic_check.json')},
        'geometry_arithmetic_direction_records_match': 21,
        'cap_count': 7,
        'strict_middle_projection_certificates': 14,
        'retained_extremal_directions': 14,
        'cap_records': cap_records,
        'quantifier_examples': {
            'q2': {'point': list(map(str, point)), 'active_constraints': active_count,
                   'H': '0', 'phases': list(map(str, phases))},
            'q11': {'point': list(map(str, point2)), 'cell_dimension': 0, 'H': '-1'},
        },
        'limits': 'Uses the new geometry certificate; tangent-cone and optimal-face arguments are reviewed prose.',
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
