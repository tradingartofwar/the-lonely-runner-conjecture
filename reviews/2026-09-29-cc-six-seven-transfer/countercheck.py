#!/usr/bin/env python3
"""Separately structured coordinator check; no project implementation imports.

Reconstruct six-form vertices from 34 global boundary planes using cross
products. Recompute only q=3,4,10 by opposing-contact candidate times.
Compare with the primary report only after both constructions finish.
This is shared AI authorship, not an independent review.
"""
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def fraction(x):
    return x - x.numerator // x.denominator


def distance(x):
    f = fraction(x)
    return min(f, 1-f)


def geometry():
    planes = [((0, 0, 1), Q(1, 8)), ((1, 0, 0), Q(1, 2))]
    for a, b in ROWS:
        for m in range(a+b):
            planes.extend([((a, b, -1), Q(m)), ((a, b, 1), Q(m+1))])
    assert len(planes) == 34
    result = defaultdict(set)
    triples = nonsingular = 0
    for (a, u), (b, v), (c, w) in combinations(planes, 3):
        triples += 1
        bc, ca, ab = cross(b, c), cross(c, a), cross(a, b)
        det = dot(a, bc)
        if not det:
            continue
        nonsingular += 1
        p = tuple((u*bc[i]+v*ca[i]+w*ab[i])/det for i in range(3))
        x, y, z = p
        if not Q(1, 8) <= z <= x <= Q(1, 2) or not z <= y <= 1-z:
            continue
        forms = [a*x+b*y for a, b in ROWS]
        if not all(z <= fraction(f) <= 1-z for f in forms):
            continue
        labels = tuple(f.numerator // f.denominator for f in forms)
        result[labels].add(p)
    assert triples == 5984
    return dict(result), {'boundary_planes': len(planes), 'plane_triples': triples,
                          'nonsingular_triples': nonsingular}


def optimize(speeds):
    # Interior maxima of a minimum of tents occur at a tent peak or a switch
    # from positive to negative slope. The latter forces (v_i+v_j)t integral.
    # Evaluate a superset of all such times, keeping all ties and endpoints.
    candidates = {Q(0), Q(1)}
    for v in speeds:
        candidates.update(Q(2*j+1, 2*v) for j in range(v))
    for a, b in combinations(speeds, 2):
        candidates.update(Q(j, a+b) for j in range(a+b+1))
    values = {t: min(distance(v*t) for v in speeds) for t in candidates}
    maximum = max(values.values())
    return {'maximum': str(maximum), 'all_maximizing_times': [str(t) for t in sorted(values) if values[t] == maximum],
            'candidate_times': len(candidates)}


def explicit_q10_face_contact():
    q = 10
    t, y, z = Q(17, 35), Q(6, 7), Q(1, 7)
    forms = [a*t+b*y for a, b in ROWS]
    labels = [f.numerator // f.denominator for f in forms]
    phases = [fraction(f) for f in forms]
    assert labels == [0, 0, 1, 1, 2, 3]
    assert all(z <= p <= 1-z for p in phases)
    active = [(i, side) for i, p in enumerate(phases)
              for side, value in [('lower', z), ('upper', 1-z)] if p == value]
    assert active == [(1, 'upper')] and z > Q(1, 8) and t < Q(1, 2)
    assert 10*t-y == 4 and distance(25*t) == z
    # Old slice: 10t+z<=5 and -23t+z<=-11 give 33z<=5.
    # Added band: -25t+z<=-12 replaces the second inequality, giving 35z<=5.
    old_t, old_z = Q(16, 33), Q(5, 33)
    assert min(distance(v*old_t) for v in (1, 10, 11, 12, 13, 23)) == old_z
    assert distance(25*old_t) == Q(4, 33) < Q(1, 8)
    assert 10*old_t + old_z == 5 and -23*old_t + old_z == -11
    assert 10*t + z == 5 and -25*t + z == -12
    return {'q': q, 'time': str(t), 'reflection': str(1-t),
            'height': str(z), 'ambient_labels': labels,
            'six_phases': list(map(str, phases)), 'active_parent_bands': active,
            'parent_minimal_face_dimension': 2,
            'old_same_slice_optimum': str(old_z), 'old_same_slice_time': str(old_t),
            'old_time_seventh_distance': '4/33',
            'old_upper_certificate': '23*(10t+z<=5)+10*(-23t+z<=-11) => 33z<=5',
            'new_upper_certificate': '25*(10t+z<=5)+10*(-25t+z<=-12) => 35z<=5'}


def main():
    cells, counts = geometry()
    physical = {}
    for q in (3, 4, 10):
        speeds = (1, q, q+1, q+2, q+3, 2*q+3, 2*q+5)
        for size in (6, 7):
            physical[q, size] = optimize(speeds[:size])
    q10 = explicit_q10_face_contact()
    # Primary output is consulted only now, after independent constructions.
    primary = json.loads((HERE / 'verification.json').read_text())
    expected_cells = {tuple(c['labels']): {tuple(map(Q, v)) for v in c['vertices']}
                      for c in primary['parents']}
    assert cells == expected_cells
    for record in primary['physical_controls']:
        for actual in record['optimization']:
            checked = physical[record['q'], actual['coordinates']]
            assert checked['maximum'] == actual['maximum']
            assert checked['all_maximizing_times'] == actual['all_maximizing_times']
    output = {'status': 'PASS: separately structured coordinator countercheck',
              'geometry': {**counts, 'cells': len(cells), 'vertices': sum(map(len, cells.values())),
                           'all_primary_parent_vertices_match': True,
                           'certificate': [{'labels': labels, 'vertices': [list(map(str, v)) for v in sorted(vertices)]}
                                           for labels, vertices in sorted(cells.items())]},
              'physical': [{'q': q, 'coordinates': size, **physical[q, size]} for q, size in sorted(physical)],
              'q10_new_face_contact': q10,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'primary_output_sha256': hashlib.sha256((HERE/'verification.json').read_bytes()).hexdigest(),
              'limits': 'Same AI coordinator; global-plane and opposing-contact methods were known from earlier work. No claim of independent authorship.'}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
