#!/usr/bin/env python3
"""Independent rational cell reconstruction and primal/dual certificate checker.

No imports from the primary implementation; no optimizer used here. Only the
three frozen windows are reconstructed. --check compares without writing.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A, B, DELTA = F(9, 32), F(3, 8), F(1, 8)
CONTROLS = [('strict_16', [6, 7, 11, 16]),
            ('doubling_112', [56, 64, 72, 112]),
            ('tight_13', [6, 7, 11, 13])]
MOMENT_MASKS = [i for i in range(16) if i.bit_count() <= 2]
TRIPLES = [7, 11, 13, 14]


def frac_distance(v, t):
    z = v*t
    f = z-z.numerator//z.denominator
    return min(f, 1-f)


def incidence(mask):
    return [F((state & mask) == mask) for state in range(16)]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def reconstruct(speeds):
    # All exact threshold cells, evaluated at their rational midpoint. This
    # differs from the primary's per-speed interval-list intersections.
    cuts = {A, B}
    for v in speeds:
        for lap in range((v*A).numerator//(v*A).denominator-1,
                         (v*B).numerator//(v*B).denominator+2):
            for sign in [-1, 1]:
                t = (lap+sign*DELTA)/v
                if A < t < B:
                    cuts.add(t)
    cuts = sorted(cuts)
    cells, masses = [], [F(0)]*16
    for left, right in zip(cuts, cuts[1:]):
        middle = (left+right)/2
        assert all(frac_distance(v, middle) >= DELTA for v in [1, 4, 5])
        state = sum(1 << i for i, v in enumerate(speeds)
                    if frac_distance(v, middle) < DELTA)
        masses[state] += right-left
        cells.append({'left': str(left), 'right': str(right), 'state': state})
    moments = {mask: dot(incidence(mask), masses) for mask in range(16)}
    # Check the entire core window, including all its endpoints: each core
    # speed stays inside one closed safe lap on J.
    for v in [1, 4, 5]:
        lap = (v*A).numerator//(v*A).denominator
        assert (lap+DELTA)/v <= A <= B <= (lap+1-DELTA)/v
    return cells, masses, moments


def cert_check(cert, moments, objective, cover=False, upper=None):
    c = list(map(F, cert['objective']))
    assert len(c) == 16 and c == objective
    rows = [list(map(F, row)) for row in cert['eq_rows']]
    rhs = list(map(F, cert['eq_rhs']))
    le = [list(map(F, row)) for row in cert['le_rows']]
    le_rhs = list(map(F, cert['le_rhs']))
    expected = [(tuple(incidence(mask)), moments[mask]) for mask in MOMENT_MASKS]
    if cover:
        expected.append((tuple([F(1)]+[F(0)]*15), F(0)))
    assert len(rows) == len(rhs)
    assert Counter(zip(map(tuple, rows), rhs)) == Counter(expected)
    expected_le = [] if upper is None else [(tuple(incidence(upper[0])), upper[1])]
    assert len(le) == len(le_rhs)
    assert Counter(zip(map(tuple, le), le_rhs)) == Counter(expected_le)
    x = list(map(F, cert['primal']))
    y, z = list(map(F, cert['dual_eq'])), list(map(F, cert['dual_le']))
    assert len(x) == 16 and all(t >= 0 for t in x)
    assert len(y) == len(rows) and len(z) == len(le)
    assert all(len(row) == 16 for row in rows+le)
    assert all(dot(row, x) == b for row, b in zip(rows, rhs))
    assert all(dot(row, x) <= b for row, b in zip(le, le_rhs))
    assert all(t <= 0 for t in z)
    reduced = [c[j]-sum(y[i]*row[j] for i, row in enumerate(rows))
               -sum(z[i]*row[j] for i, row in enumerate(le)) for j in range(16)]
    assert all(t >= 0 for t in reduced)
    value = F(cert['value'])
    assert dot(c, x) == dot(rhs, y)+dot(le_rhs, z) == value
    return {'value': str(value), 'primal_dual_equal': True,
            'reduced_costs_nonnegative': True,
            'positive_primal_states': [i for i, q in enumerate(x) if q]}


def forced_cover_algebra(moments):
    # Zero pair moments exclude every higher state containing that pair.
    zero_pairs = [i for i in MOMENT_MASKS if i.bit_count() == 2 and moments[i] == 0]
    forbidden = {state for state in range(16)
                 if any(state & p == p for p in zero_pairs)}
    high_allowed = [i for i in range(16) if i.bit_count() >= 3 and i not in forbidden]
    k = moments[0]-sum(moments[1 << i] for i in range(4))+sum(
        moments[i] for i in MOMENT_MASKS if i.bit_count() == 2)
    assert high_allowed in ([], [13])
    cover = [F(0)]*16
    if high_allowed:
        cover[13] = k
    else:
        assert k == 0
    # Exact pairs and singles are then uniquely determined by inversion.
    for state in sorted(range(1, 16), key=int.bit_count, reverse=True):
        if state.bit_count() > 2:
            continue
        cover[state] = moments[state]-sum(cover[j] for j in range(1, 16)
                                         if j != state and j & state == state)
    assert all(x >= 0 for x in cover)
    assert all(dot(incidence(mask), cover) == moments[mask] for mask in MOMENT_MASKS)
    return {'zero_pairs': zero_pairs, 'excluded_states': sorted(forbidden),
            'allowed_higher_states': high_allowed, 'K': str(k),
            'unique_abstract_cover_masses': list(map(str, cover)),
            'forced_triples': {str(t): str(dot(incidence(t), cover)) for t in TRIPLES}}


def cell_pieces(cells, speeds, mask):
    """Coalesce active threshold cells, retaining nearest-integer lap labels."""
    result = []
    for cell in cells:
        if cell['state'] & mask != mask:
            continue
        left, right = F(cell['left']), F(cell['right'])
        mid = (left+right)/2
        laps = []
        for i, speed in enumerate(speeds):
            if mask >> i & 1:
                pos = speed*mid+F(1, 2)
                laps.append(pos.numerator//pos.denominator)
        if result and result[-1][1] == str(left) and result[-1][2] == laps:
            result[-1][1] = str(right)
        else:
            result.append([str(left), str(right), laps])
    return result


def endpoint(speeds):
    all_speeds = [1, 4, 5]+speeds
    distances = {str(v): str(frac_distance(v, B)) for v in all_speeds}
    valid = all(frac_distance(v, B) >= DELTA for v in all_speeds)
    result = {'time': str(B), 'distances': distances, 'valid': valid}
    if valid:
        laps = []
        for v in all_speeds:
            pos = v*B
            k = pos.numerator//pos.denominator
            laps.append(((k+DELTA)/v, (k+1-DELTA)/v))
        left, right = max(x[0] for x in laps), min(x[1] for x in laps)
        result.update({'containing_safe_component': [str(left), str(right)],
                       'isolated': left == right,
                       'left_neighborhood_blockers': [v for v, lap in zip(all_speeds, laps) if lap[0] == B],
                       'right_neighborhood_blockers': [v for v, lap in zip(all_speeds, laps) if lap[1] == B]})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = (HERE/'results.json').read_bytes()
    primary = json.loads(raw)
    assert primary['protocol_sha256'] == hashlib.sha256((HERE/'protocol.json').read_bytes()).hexdigest()
    assert primary['primary_sha256'] == hashlib.sha256((HERE/'primary.py').read_bytes()).hexdigest()
    records = primary['cases']
    assert [(x['name'], x['speeds']) for x in records] == CONTROLS
    output = {'primary_sha256': hashlib.sha256(raw).hexdigest(),
              'method': 'independent exact threshold-cell partition; exact primal/dual checks; zero-pair algebra',
              'scope': 'three frozen windows only, selected reference 0, eight common-start runners',
              'cases': []}
    count = 0
    for record, (name, speeds) in zip(records, CONTROLS):
        cells, masses, moments = reconstruct(speeds)
        assert {str(m): str(moments[m]) for m in MOMENT_MASKS} == record['moments']
        assert record['blocks'] == [cell_pieces(cells, speeds, 1 << i) for i in range(4)]
        assert record['pair_pieces'] == {str(m): cell_pieces(cells, speeds, m)
                                         for m in MOMENT_MASKS if m.bit_count() == 2}
        out = {'name': name, 'cell_count': len(cells), 'cells': cells,
               'exact_state_masses': list(map(str, masses)),
               'all_moments': {str(k): str(v) for k, v in moments.items()},
               'actual_empty': str(masses[0]), 'certificates': []}
        empty_objective = [F(1)]+[F(0)]*15
        out['certificates'].append(cert_check(record['baseline'], moments, empty_objective))
        count += 1
        base = F(record['baseline']['value'])
        if base == 0:
            algebra = forced_cover_algebra(moments)
            out['cover_algebra'] = algebra
            queried = record['cover_triples']
            assert [q['mask'] for q in queried] == TRIPLES
            for q in queried:
                checked = cert_check(q['certificate'], moments, incidence(q['mask']), cover=True)
                assert checked['value'] == algebra['forced_triples'][str(q['mask'])]
                out['certificates'].append(checked)
                count += 1
            positive = [q for q in queried if F(q['certificate']['value']) > 0]
            positive.sort(key=lambda q: (-F(q['certificate']['value']),
                                        [speeds[i] for i in range(4) if q['mask'] >> i & 1]))
            if positive:
                selected = record['selected']
                mask = positive[0]['mask']
                assert selected['mask'] == mask
                actual = moments[mask]
                assert F(selected['forced_min']) == F(positive[0]['certificate']['value'])
                assert F(selected['actual_upper']) == actual
                assert selected['pieces'] == cell_pieces(cells, speeds, mask)
                pair_mask = selected['queried_pair_mask']
                third = selected['tested_third_speed']
                assert pair_mask & mask == pair_mask and pair_mask.bit_count() == 2
                assert third in [speeds[i] for i in range(4) if (mask ^ pair_mask) >> i & 1]
                assert selected['pair_phase_ranges'] == [
                    {'interval': [left, right], 'unwrapped_phase': [str(third*F(left)), str(third*F(right))]}
                    for left, right, laps in cell_pieces(cells, speeds, pair_mask)]
                out['selected_geometric_triple'] = {'mask': mask, 'duration': str(actual)}
                if actual < F(selected['forced_min']):
                    checked = cert_check(record['repaired'], moments, empty_objective,
                                         upper=(mask, actual))
                    out['certificates'].append(checked)
                    count += 1
                    assert F(checked['value']) <= masses[0]
                else:
                    out['endpoint'] = endpoint(speeds)
            else:
                assert record.get('selected') is None
                out['endpoint'] = endpoint(speeds)
        else:
            assert not record.get('cover_triples') and record.get('selected') is None
            assert base <= masses[0]
        if 'endpoint' in out:
            assert record['endpoint'] == {k: v for k, v in out['endpoint'].items()
                                          if k != 'containing_safe_component'}
        else:
            assert record['endpoint'] is None
        output['cases'].append(out)
    output['exact_certificates_checked'] = count
    output['total_cells'] = sum(c['cell_count'] for c in output['cases'])
    expected = json.dumps(output, indent=2, sort_keys=True)+'\n'
    dest = HERE/'verification.json'
    if args.check:
        assert dest.read_text() == expected, 'verification.json differs'
        print('PASS: independent geometry, cover algebra, and', count, 'exact LP certificates')
    else:
        dest.write_text(expected)
        print('Wrote', dest)


if __name__ == '__main__':
    main()
