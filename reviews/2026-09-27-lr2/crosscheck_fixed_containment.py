"""Independent exact replay: lattice points, event cells, interval intersections.

Imports no project code. --write records the comparison; default/--check
compares read-only. All arithmetic is rational/integer.
"""
import argparse
from fractions import Fraction
from math import floor
from pathlib import Path
import json

Q = Fraction
HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'fixed_containment.json'
OUT = HERE / 'fixed_containment_crosscheck.json'
DELTA = Q(1, 8)
WINDOW = (Q(9, 32), Q(5, 16))
OPENING = (Q(17, 56), Q(5, 16))
BASE = (1, 4, 5, 6, 7)


def distance_at(v, t):
    z = v*t
    remainder = z.numerator % z.denominator
    return Q(min(remainder, z.denominator-remainder), z.denominator)


def vertices(speeds, window):
    points = set(window)
    for v in speeds:
        for k in range(1, 8*v):
            if k % 8 in (1, 7):
                t = Q(k, 8*v)
                if window[0] < t < window[1]:
                    points.add(t)
    return sorted(points)


def safe(speeds, t):
    return all(distance_at(v, t) >= DELTA for v in speeds)


def allowed(speeds, window):
    points = vertices(speeds, window)
    pieces = [(t, t) for t in points if safe(speeds, t)]
    for a, b in zip(points, points[1:]):
        if safe(speeds, (a+b)/2):
            assert safe(speeds, a) and safe(speeds, b)
            pieces.append((a, b))
    merged = []
    for a, b in sorted(pieces):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


def length(pieces):
    return sum((b-a for a, b in pieces), Q(0))


def blocked(v, window):
    # Closures suffice here: this function is used only for durations.
    pieces = []
    for lap in range(v+1):
        a = max(window[0], Q(8*lap-1, 8*v))
        b = min(window[1], Q(8*lap+1, 8*v))
        if a < b:
            pieces.append((a, b))
    return pieces


def common(left, right):
    return [(max(a, c), min(b, d)) for a, b in left for c, d in right
            if max(a, c) < min(b, d)]


def verify():
    archive = json.loads(SOURCE.read_text())
    assert archive['total_runners'] == 8 and archive['reference'] == 0
    assert archive['threshold'] == str(DELTA)
    assert archive['core'] == [1, 4, 6] and archive['fixed_speeds'] == list(BASE)
    assert archive['J'] == list(map(str, WINDOW)) and archive['S'] == list(map(str, OPENING))
    assert archive['exhaustive_finite_domain'] == [1, 84] and archive['extra_failure_control'] == 85
    assert WINDOW in allowed((1, 4, 6), (Q(0), Q(1)))
    assert allowed(BASE, WINDOW) == [OPENING]
    assert allowed((5,), WINDOW) == [WINDOW]
    assert allowed((7,), WINDOW) == [OPENING]

    # Enumerate integer points in the triangle independently of floor/ceil test.
    lattice = [(x, m) for m in range(26) for x in range(1, 85)
               if 17*x-56*m >= 7 and 5*x-16*m <= 14]
    by_x = dict(lattice)
    assert len(by_x) == len(lattice) == 35
    raw = sorted(by_x)
    good = sorted(set(raw)-set(BASE))
    assert archive['raw_safe_speeds'] == raw
    assert archive['admissible_replacements'] == good
    rows = archive['classification']
    assert [r['x'] for r in rows] == list(range(1, 86))
    contacts = []
    for row in rows:
        x = row['x']
        pieces = allowed((x,), OPENING)
        eligible = pieces == [OPENING]
        assert eligible == (x in by_x) == row['safe_on_S']
        assert row['repeated_fixed_speed'] == (x in BASE)
        assert row['admissible'] == (x in good)
        assert Q(row['blocked_duration_S']) == OPENING[1]-OPENING[0]-length(pieces)
        # Direct implication test at every vertex and open cell of J.
        cuts = vertices((x, 7), WINDOW)
        probes = cuts + [(a+b)/2 for a, b in zip(cuts, cuts[1:])]
        contained = all(distance_at(x, t) >= DELTA or distance_at(7, t) < DELTA
                        for t in probes)
        assert contained == eligible
        low, high = row['lap_lower'], row['lap_upper']
        assert low-1 < x*OPENING[1]-Q(7, 8) <= low
        assert high <= x*OPENING[0]-Q(1, 8) < high+1
        if eligible:
            m = by_x[x]
            assert row['lap'] == low == high == m
            left = x*OPENING[0]-m-DELTA
            right = m+1-DELTA-x*OPENING[1]
            assert list(map(Q, row['phase_margins'])) == [left, right]
            p, q = row['integer_slacks']
            assert (p, q) == (56*left, 16*right)
            assert x == 84-2*p-7*q and m == Q(203-5*p-17*q, 8)
            names = [name for name, margin in [('left', left), ('right', right)] if margin == 0]
            assert row['threshold_endpoints'] == names
            if names and x in good:
                contacts.append(dict(x=x, endpoints=names))
        else:
            t = Q(row['violating_time'])
            assert OPENING[0] <= t <= OPENING[1]
            assert Q(row['violating_distance']) == distance_at(x, t) < DELTA

    expected_cases = [(x, 29) for x in good] + [(11, y) for y in (28, 44, 45, 46)] + [(19, 45)]
    assert [(c['x'], c['y']) for c in archive['certificates']] == expected_cases
    for case in archive['certificates']:
        x, y = case['x'], case['y']
        speeds = BASE+(x, y)
        assert len(set((0,)+speeds)) == 8
        residual = [5, 7, x, y]
        edges = [(5, 7), (7, x), (7, y)]
        assert case['residual'] == residual
        assert case['tree_edges'] == [list(e) for e in edges]
        blocks = {v: blocked(v, WINDOW) for v in residual}
        single = [length(blocks[v]) for v in residual]
        pair = [length(common(blocks[u], blocks[v])) for u, v in edges]
        assert list(map(Q, case['single_durations'])) == single
        assert list(map(Q, case['edge_overlap_durations'])) == pair
        tree = WINDOW[1]-WINDOW[0]-sum(single)+sum(pair)
        intervals = allowed(speeds, WINDOW)
        actual = length(intervals)
        assert case['allowed_on_J'] == [[str(a), str(b)] for a, b in intervals]
        assert Q(case['actual_duration']) == actual
        assert Q(case['tree_bound']) == tree > 0
        overlap_in_S = length(common(blocked(x, OPENING), blocked(y, OPENING)))
        assert Q(case['tree_slack']) == actual-tree == overlap_in_S
        t = Q(case['strict_witness'])
        distances = [distance_at(v, t) for v in speeds]
        assert WINDOW[0] < t < WINDOW[1] and min(distances) > DELTA
        assert list(map(Q, case['witness_distances'])) == distances
        if x in good:
            assert tree == actual >= Q(3, 448)-Q(3, 16*y)

    # Reconstruct the correction function by integrating intervals on [0,z].
    vertices_psi = [(z, length(blocked(1, (Q(0), z)))-z/4)
                    for z in (Q(0), DELTA, 1-DELTA, Q(1))]
    assert archive['primitive_correction_vertices'] == [[str(z), str(v)] for z, v in vertices_psi]
    assert max(v for z, v in vertices_psi)-min(v for z, v in vertices_psi) == Q(3, 16)
    assert contacts == [dict(x=x, endpoints=[side]) for x, side in
                        [(22, 'right'), (38, 'right'), (54, 'right'), (63, 'left'), (70, 'right')]]
    control = archive['certificates'][-1]
    assert (control['tree_bound'], control['actual_duration'], control['tree_slack']) == (
        '47/31920', '1/210', '1/304')
    for case in archive['certificates'][:30]:
        assert case['allowed_on_J'] == [['17/56', '71/232']]
        assert case['actual_duration'] == '1/406'
    assert max(good) == 73
    assert [(x, m) for x, m in lattice if m >= 22] == [(73, 22)]
    return dict(status='PASS', independently_reconstructed_classifications=85,
                lattice_points=len(lattice), admissible_count=len(good),
                largest_admissible=max(good), admissible_endpoint_contacts=contacts,
                local_certificates_checked=len(expected_cases),
                containment_failure_but_positive_tree=dict(x=19, y=45,
                    tree_bound='47/31920', actual_duration='1/210', slack='1/304'),
                methods=['integer lattice enumeration', 'exact threshold vertices and cells',
                         'strict-set containment probes', 'interval intersections for moments'],
                scope_limit='Finite replay plus checks of algebraic ingredients; no external proof certification.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = verify()
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert json.loads(OUT.read_text()) == result
    print('PASS: independent lattice, strict containment, endpoints, and 35 certificates.')
