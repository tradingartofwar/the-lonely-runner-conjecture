#!/usr/bin/env python3
"""Separate exact event sweep and rational two-phase simplex verification.

No primary imports or numerical optimization. --check is read-only.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
D = Q(1, 8)
MASKS = [s for s in range(16) if s.bit_count() <= 2]
TRIPLES = [7, 11, 13, 14]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def incidence(mask):
    return [Q((s & mask) == mask) for s in range(16)]


def distance(v, t):
    x = (v*t) % 1
    return min(x, 1-x)


def events(speeds, a, b):
    out = {a, b}
    for v in speeds:
        for k in range((v*a).numerator//(v*a).denominator-1,
                       (v*b).numerator//(v*b).denominator+2):
            for e in (-D, D):
                t = (k+e)/v
                if a < t < b:
                    out.add(t)
    return sorted(out)


def core_components(speeds):
    cuts = events(speeds, Q(0), Q(1))
    pieces = [(a, b) for a, b in zip(cuts, cuts[1:])
              if all(distance(v, (a+b)/2) >= D for v in speeds)]
    pieces += [(t, t) for t in cuts if all(distance(v, t) >= D for v in speeds)]
    result = []
    for a, b in sorted(pieces):
        if result and a <= result[-1][1]:
            result[-1] = (result[-1][0], max(b, result[-1][1]))
        else:
            result.append((a, b))
    return result


def sweep(speeds, window, atoms=False):
    a, b = window
    cuts = events(speeds, a, b)
    moments = {mask: Q(0) for mask in MASKS}
    masses = [Q(0)]*16 if atoms else None
    states_seen = set()
    safe_pieces = []
    def mask_at(t):
        return sum(1 << i for i, v in enumerate(speeds) if distance(v, t) < D)
    for lo, hi in zip(cuts, cuts[1:]):
        s = mask_at((lo+hi)/2)
        states_seen.add(s)
        for mask in MASKS:
            if s & mask == mask:
                moments[mask] += hi-lo
        if atoms:
            masses[s] += hi-lo
            if s == 0:
                safe_pieces.append([str(lo), str(hi)])
    # Pointwise membership matters to containment and equality, unlike mass.
    states_seen.update(mask_at(t) for t in cuts)
    vanished = [i for i in range(4) if not any(s >> i & 1 for s in states_seen)]
    edges = [(i, j) for i in range(4) for j in range(4) if i != j
             and not any(s >> i & 1 and not (s >> j & 1) for s in states_seen)]
    points = [str(t) for t in cuts if atoms and mask_at(t) == 0]
    return moments, masses, vanished, edges, len(cuts)-1, safe_pieces, points


def tree_bound(moments, retained):
    # Kruskal maximum spanning tree; primary/source enumerate tree candidates.
    parent = {i: i for i in retained}
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    weight = Q(0)
    pairs = sorted(combinations(retained, 2),
                   key=lambda ij: (-moments[(1 << ij[0]) | (1 << ij[1])], ij))
    for i, j in pairs:
        x, y = find(i), find(j)
        if x != y:
            parent[y] = x
            weight += moments[(1 << i) | (1 << j)]
    return moments[0]-sum(moments[1 << i] for i in retained)+weight


def locate(archive):
    selected, diagnostics = [], []
    for case in archive['cases']:
        speeds = case['velocities']
        full = [(Q(a), Q(b)) for a, b in case['full_allowed_components']]
        for entry in case['cores']:
            if not entry['summary']['positive_actual_tree_misses']:
                continue
            labels = entry['core']
            residual = entry['residual']
            windows = core_components([speeds[i] for i in labels])
            digest = sha256()
            misses, cells = 0, 0
            for index, window in enumerate(windows):
                a, b = window
                moment, _, vanished, edges, count, _, _ = sweep([speeds[i] for i in residual], window)
                cells += count
                nonempty = [i for i in range(4) if i not in vanished]
                edge_set = set(edges)
                proper = {(i, j) for i, j in edges if i in nonempty and j in nonempty
                          and (j, i) not in edge_set}
                retained = []
                for i in nonempty:
                    equals = [j for j in nonempty if j == i or ((i, j) in edge_set and (j, i) in edge_set)]
                    if i == min(equals) and not any((i, j) in proper for j in nonempty):
                        retained.append(i)
                bound = tree_bound(moment, retained)
                actual = sum((max(Q(0), min(b, v)-max(a, u)) for u, v in full), Q(0))
                row = [str(a), str(b), str(bound), str(actual),
                       [residual[i] for i in vanished],
                       [[residual[i], residual[j]] for i, j in edges],
                       [residual[i] for i in retained]]
                digest.update((json.dumps(row, separators=(',', ':'))+'\n').encode())
                if actual > 0 and bound <= 0:
                    misses += 1
                    selected.append({'case_id': case['id'], 'velocities': speeds,
                                     'core_labels': labels, 'residual_labels': residual,
                                     'component_index': index, 'window': list(map(str, window)),
                                     'archived_actual_duration': str(actual),
                                     'reduced_tree_bound': str(bound)})
            assert digest.hexdigest() == entry['component_sha256'], (case['id'], labels, 'digest')
            assert len(windows) == entry['summary']['components']
            assert misses == entry['summary']['positive_actual_tree_misses']
            diagnostics.append({'case_id': case['id'], 'core_labels': labels,
                                'component_count': len(windows), 'locator_cells': cells,
                                'component_sha256': digest.hexdigest(), 'miss_count': misses})
    assert len(selected) == archive['totals']['positive_actual_tree_misses'] == 18
    return selected, diagnostics


def simplex(rows, rhs, objective):
    """Bland-rule exact two-phase primal tableau; returns own primal and dual."""
    m, n = len(rows), len(objective)
    assert all(b >= 0 for b in rhs)
    mat = [[Q(v) for v in row]+[Q(i == j) for j in range(m)] for i, row in enumerate(rows)]
    b = list(map(Q, rhs))
    transform = [[Q(i == j) for j in range(m)] for i in range(m)]
    basis = list(range(n, n+m))
    pivots = 0
    def pivot(r, col):
        nonlocal pivots
        p = mat[r][col]
        mat[r] = [x/p for x in mat[r]]
        b[r] /= p
        transform[r] = [x/p for x in transform[r]]
        for i in range(len(mat)):
            if i != r and mat[i][col]:
                scale = mat[i][col]
                mat[i] = [x-scale*y for x, y in zip(mat[i], mat[r])]
                b[i] -= scale*b[r]
                transform[i] = [x-scale*y for x, y in zip(transform[i], transform[r])]
        basis[r] = col
        pivots += 1
    def optimize(cost, width):
        while True:
            reduced = [cost[j]-sum(cost[basis[i]]*mat[i][j] for i in range(len(mat)))
                       for j in range(width)]
            negative = [j for j in range(width) if reduced[j] < 0]
            if not negative:
                return sum(cost[basis[i]]*b[i] for i in range(len(mat)))
            col = min(negative)
            candidates = [(b[i]/mat[i][col], basis[i], i) for i in range(len(mat)) if mat[i][col] > 0]
            assert candidates, 'unbounded LP'
            pivot(min(candidates)[2], col)
    assert optimize([Q(0)]*n+[Q(1)]*m, n+m) == 0, 'infeasible LP'
    for r in range(len(mat)-1, -1, -1):
        if basis[r] >= n:
            candidates = [j for j in range(n) if j not in basis and mat[r][j] != 0]
            if candidates:
                pivot(r, min(candidates))
            else:
                assert b[r] == 0
                del mat[r], b[r], basis[r], transform[r]
    value = optimize(list(objective)+[Q(0)]*m, n)
    primal = [Q(0)]*n
    for i, j in enumerate(basis):
        primal[j] = b[i]
    dual = [sum(objective[basis[i]]*transform[i][j] for i in range(len(mat))) for j in range(m)]
    assert all(x >= 0 for x in primal)
    assert all(dot(row, primal) == t for row, t in zip(rows, rhs))
    assert all(objective[j] >= sum(dual[i]*rows[i][j] for i in range(m)) for j in range(n))
    assert dot(primal, objective) == dot(dual, rhs) == value
    return {'value': str(value), 'primal': list(map(str, primal)), 'dual': list(map(str, dual)),
            'exact_tableau_pivots': pivots}


def certify(moments, mask=None, cover=False):
    rows = [incidence(s) for s in MASKS]
    rhs = [moments[s] for s in MASKS]
    if cover:
        rows.append([Q(1)]+[Q(0)]*15)
        rhs.append(Q(0))
    objective = incidence(mask) if mask is not None else [Q(1)]+[Q(0)]*15
    return simplex(rows, rhs, objective)


def check_archived_certificate(cert):
    rows = [list(map(Q, row)) for row in cert['eq_rows']]
    rhs = list(map(Q, cert['eq_rhs']))
    le = [list(map(Q, row)) for row in cert['le_rows']]
    lr = list(map(Q, cert['le_rhs']))
    c, x = list(map(Q, cert['objective'])), list(map(Q, cert['primal']))
    y, z = list(map(Q, cert['dual_eq'])), list(map(Q, cert['dual_le']))
    assert all(t >= 0 for t in x) and all(t <= 0 for t in z)
    assert all(dot(row, x) == v for row, v in zip(rows, rhs))
    assert all(dot(row, x) <= v for row, v in zip(le, lr))
    assert all(c[j] >= sum(y[i]*row[j] for i, row in enumerate(rows))+
               sum(z[i]*row[j] for i, row in enumerate(le)) for j in range(16))
    assert dot(c, x) == dot(rhs, y)+dot(lr, z) == Q(cert['value'])


def controls():
    source = json.loads((ROOT/'reviews/2026-09-28-cover-obligations/results.json').read_text())
    out = []
    for c in source['cases']:
        moments, masses, _, _, cells, _, _ = sweep(c['speeds'], (Q(9, 32), Q(3, 8)), atoms=True)
        assert {str(k): str(v) for k, v in moments.items()} == c['moments']
        check_archived_certificate(c['baseline'])
        baseline = certify(moments)
        assert baseline['value'] == c['baseline']['value']
        triple = []
        for old in c['cover_triples']:
            check_archived_certificate(old['certificate'])
            new = certify(moments, old['mask'], cover=True)
            assert new['value'] == old['certificate']['value']
            triple.append({'mask': old['mask'], 'certificate': new})
        if c['repaired']:
            check_archived_certificate(c['repaired'])
        endpoint = c['endpoint']
        if endpoint:
            t = Q(endpoint['time'])
            ds = {str(v): str(distance(v, t)) for v in [1, 4, 5]+c['speeds']}
            assert ds == endpoint['distances'] and min(map(Q, ds.values())) == D
            left, right = [], []
            for v in [1, 4, 5]+c['speeds']:
                phase = (v*t) % 1
                if phase == D:
                    left.append(v)
                if phase == 1-D:
                    right.append(v)
            assert left == endpoint['left_neighborhood_blockers']
            assert right == endpoint['right_neighborhood_blockers']
            assert bool(left and right) == endpoint['isolated']
        out.append({'name': c['name'], 'baseline': baseline, 'cover_triples': triple,
                    'physical_atoms': list(map(str, masses)), 'endpoint_checked': endpoint is not None,
                    'cell_count': cells})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    protocol = json.loads((HERE/'protocol.json').read_text())
    for file_key, hash_key in [('archive', 'archive_sha256'), ('reconstruction', 'reconstruction_sha256'),
                               ('source_protocol', 'source_protocol_sha256')]:
        assert sha256((ROOT/protocol['source_contract'][file_key]).read_bytes()).hexdigest() == protocol['source_contract'][hash_key]
    archive = json.loads((ROOT/protocol['source_contract']['archive']).read_text())
    selected, locator = locate(archive)
    result = {'method': 'independent threshold-event sweep and exact two-phase Bland-rule simplex',
              'locator': locator, 'cases': [], 'controls': controls()}
    for record in selected:
        speeds = [record['velocities'][i] for i in record['residual_labels']]
        moments, masses, _, _, cells, safe, points = sweep(speeds, tuple(map(Q, record['window'])), atoms=True)
        assert masses[0] == Q(record['archived_actual_duration']) > 0
        all_moments = [dot(incidence(s), masses) for s in range(16)]
        baseline = certify(moments)
        triples = []
        if Q(baseline['value']) == 0:
            triples = [{'mask': t, 'certificate': certify(moments, t, cover=True)} for t in TRIPLES]
        collective = Q(baseline['value']) == 0 and all(Q(t['certificate']['value']) == 0 for t in triples)
        result['cases'].append({**record, 'residual_speeds': speeds, 'cell_count': cells,
                                'moments': list(map(str, all_moments)), 'atoms': list(map(str, masses)),
                                'baseline': baseline, 'cover_triples': triples,
                                'collective_only_counterpart': collective,
                                'safe_open_cells': safe, 'safe_threshold_points': points})
    # Result comparison is completed against the primary archive below.
    primary = json.loads((HERE/'results.json').read_text())
    assert len(primary['cases']) == len(result['cases']) == 18
    for own, other in zip(result['cases'], primary['cases']):
        for key in ['case_id', 'velocities', 'core_labels', 'residual_labels', 'component_index',
                    'window', 'archived_actual_duration', 'reduced_tree_bound',
                    'collective_only_counterpart']:
            assert own[key] == other[key], (key, own[key], other[key])
        assert own['moments'] == other['moments']
        assert own['atoms'] == other['atoms']
        assert own['baseline']['value'] == other['baseline']['value']
        check_archived_certificate(other['baseline'])
        others = other['cover_triple_minima']
        assert len(own['cover_triples']) == len(others)
        for a, b in zip(own['cover_triples'], others):
            assert a['mask'] == b['mask'] and a['certificate']['value'] == b['certificate']['value']
            check_archived_certificate(b['certificate'])
    result['primary_sha256'] = sha256((HERE/'results.json').read_bytes()).hexdigest()
    result['summary'] = {'selected_windows': len(result['cases']),
                         'pair_positive': sum(Q(c['baseline']['value']) > 0 for c in result['cases']),
                         'collective_only_counterparts': sum(c['collective_only_counterpart'] for c in result['cases']),
                         'locator_components': sum(c['component_count'] for c in locator),
                         'locator_cells': sum(c['locator_cells'] for c in locator),
                         'selected_window_cells': sum(c['cell_count'] for c in result['cases']),
                         'new_case_exact_lp_solves': sum(1+len(c['cover_triples']) for c in result['cases'])}
    content = json.dumps(result, indent=2, sort_keys=True)+'\n'
    path = HERE/'verification.json'
    if args.check:
        assert path.read_text() == content
        print('PASS independent audit:', json.dumps(result['summary'], sort_keys=True))
    else:
        path.write_text(content)
        print('Wrote verification.json:', json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
