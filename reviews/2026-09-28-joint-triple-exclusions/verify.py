#!/usr/bin/env python3
"""Independent event geometry and exact simplex for the frozen subset lattice.

Standard library only. No primary or primary-helper imports. The exact simplex
is reused from this verifier author's prior collective-window implementation.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
D = Q(1, 8)
MOMENTS = [s for s in range(16) if s.bit_count() <= 2]
TRIPLES = [7, 11, 13, 14]
SUBSETS = [list(s) for k in range(5) for s in combinations(TRIPLES, k)]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def incidence(mask):
    return [Q(s & mask == mask) for s in range(16)]


HROW = [sum(incidence(t)[s] for t in TRIPLES)-Q(s == 15) for s in range(16)]


def distance(v, t):
    x = (v*t) % 1
    return min(x, 1-x)


def geometry(core, speeds, window):
    a, b = map(Q, window)
    # Each core runner's containing safe lap certifies all of this window.
    for v in core:
        k = (v*a).numerator//(v*a).denominator
        assert (k+D)/v <= a <= b <= (k+1-D)/v
    cuts = {a, b}
    for v in speeds:
        for k in range((v*a).numerator//(v*a).denominator-1,
                       (v*b).numerator//(v*b).denominator+2):
            for e in [-D, D]:
                t = (k+e)/v
                if a < t < b:
                    cuts.add(t)
    cuts = sorted(cuts)
    masses = [Q(0)]*16
    cells = []
    for lo, hi in zip(cuts, cuts[1:]):
        t = (lo+hi)/2
        state = sum(1 << i for i, v in enumerate(speeds) if distance(v, t) < D)
        masses[state] += hi-lo
        cells.append({'left': str(lo), 'right': str(hi), 'state': state})
    moments = [dot(incidence(s), masses) for s in range(16)]
    c = moments[0]-sum(moments[1 << i] for i in range(4))+sum(moments[s] for s in MOMENTS if s.bit_count() == 2)
    h = dot(HROW, masses)
    assert masses[0]+h == c
    points = {str(t): [str(distance(v, t)) for v in core+speeds] for t in cuts}
    return {'window': list(map(str, [a, b])), 'speeds': speeds,
            'moments': list(map(str, moments)), 'atoms': list(map(str, masses)),
            'triples': [str(moments[t]) for t in TRIPLES],
            'H': str(h), 'C': str(c), 'U': str(masses[0]),
            'cells': cells, 'point_distances': points}


def simplex(rows, rhs, objective):
    """Bland-rule exact two-phase primal tableau; own primal and dual output."""
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
    return value, primal, dual, pivots


def solve(physical, subset=None, collective=False):
    moments = list(map(Q, physical['moments']))
    le_rows = [HROW] if collective else [incidence(t) for t in subset]
    le_rhs = [Q(physical['H'])] if collective else [moments[t] for t in subset]
    width = len(le_rows)
    rows = [incidence(t)+[Q(0)]*width for t in MOMENTS]
    rhs = [moments[t] for t in MOMENTS]
    rows += [row+[Q(i == j) for j in range(width)] for i, row in enumerate(le_rows)]
    rhs += le_rhs
    value, primal, dual, pivots = simplex(rows, rhs, [Q(1)]+[Q(0)]*(15+width))
    assert all(z <= 0 for z in dual[len(MOMENTS):])
    assert value <= Q(physical['U'])
    return {'value': str(value), 'primal': list(map(str, primal[:16])),
            'slacks': list(map(str, primal[16:])),
            'dual_eq': list(map(str, dual[:len(MOMENTS)])),
            'dual_le': list(map(str, dual[len(MOMENTS):])),
            'exact_tableau_pivots': pivots}


def lattice(physical, stop_empty=False):
    speed_tuple = lambda t: tuple(v for i, v in enumerate(physical['speeds']) if t >> i & 1)
    physical_order = sorted(SUBSETS, key=lambda s: (len(s), tuple(speed_tuple(t) for t in s)))
    assert physical_order == SUBSETS
    results = []
    for subset in SUBSETS[:1] if stop_empty else SUBSETS:
        cert = solve(physical, subset=subset)
        positive = Q(cert['value']) > 0
        minimal = positive and not any(r['positive'] and set(r['masks']) < set(subset) for r in results)
        results.append({'masks': subset, 'certificate': cert, 'positive': positive,
                        'inclusion_minimal': minimal,
                        'cover_countermodel': cert['primal'] if not positive else None})
    successful = [r for r in results if r['positive']]
    return {'coordinate_subsets': results, 'selected': successful[0]['masks'] if successful else None,
            'inclusion_minimal_subsets': [r['masks'] for r in results if r['inclusion_minimal']]}


def check_cert(cert):
    rows, rhs = [list(map(Q, r)) for r in cert['eq_rows']], list(map(Q, cert['eq_rhs']))
    le, lr = [list(map(Q, r)) for r in cert['le_rows']], list(map(Q, cert['le_rhs']))
    c, x = list(map(Q, cert['objective'])), list(map(Q, cert['primal']))
    y, z = list(map(Q, cert['dual_eq'])), list(map(Q, cert['dual_le']))
    assert all(t >= 0 for t in x) and all(t <= 0 for t in z)
    assert all(dot(r, x) == b for r, b in zip(rows, rhs))
    assert all(dot(r, x) <= b for r, b in zip(le, lr))
    assert all(c[j] >= sum(y[i]*row[j] for i, row in enumerate(rows))+
               sum(z[i]*row[j] for i, row in enumerate(le)) for j in range(16))
    assert dot(c, x) == dot(rhs, y)+dot(lr, z) == Q(cert['value'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    protocol = json.loads((HERE/'protocol.json').read_text())
    contract = protocol['source_contract']
    for key in ['target_results', 'control_results', 'abstract_collective_results']:
        assert sha256((ROOT/contract[key]).read_bytes()).hexdigest() == contract[key+'_sha256']
    abstract = json.loads((ROOT/contract['abstract_collective_results']).read_text())
    abstract_moments = {int(k): Q(v) for k, v in abstract['cases'][0]['moments'].items()}
    canonical_covers = [list(map(Q, x)) for x in abstract['main_canonical_cover_models']]
    for x in canonical_covers:
        assert x[0] == 0 and all(v >= 0 for v in x)
        assert all(dot(incidence(t), x) == abstract_moments[t] for t in MOMENTS)
    assert all(any(all(dot(incidence(t), x) == 0 for t in subset) for x in canonical_covers)
               for subset in SUBSETS[:-1])
    # Pointwise U+H identity checked on every logical state, not only moments.
    for state in range(16):
        rhs = 1-state.bit_count()+len(list(combinations(range(state.bit_count()), 2)))
        assert Q(state == 0)+HROW[state] == rhs
    descriptions = [
        ('target', [7,8,23], [15,38,61,100], ['33/184','39/184']),
        ('strict_16', [1,4,5], [6,7,11,16], ['9/32','3/8']),
        ('doubling_112', [1,4,5], [56,64,72,112], ['9/32','3/8']),
        ('tight_13', [1,4,5], [6,7,11,13], ['9/32','3/8'])]
    result = {'method': 'threshold-event geometry; independently authored exact rational two-phase simplex',
              'cases': {}, 'protocol_sha256': sha256((HERE/'protocol.json').read_bytes()).hexdigest(),
              'prior_abstract_canonical_models_rechecked': 4,
              'prior_abstract_proper_subsets_covered': 15}
    for name, core, speeds, window in descriptions:
        physical = geometry(core, speeds, window)
        record = {'physical': physical, **lattice(physical, stop_empty=name == 'doubling_112')}
        record['collective'] = solve(physical, collective=True) if name != 'doubling_112' else None
        result['cases'][name] = record
    target = result['cases']['target']['physical']
    for key, expected in [('U','1/600'), ('C','6121/2781600'), ('H','99/185440')]:
        assert target[key] == expected
    reflection = geometry([7,8,23], [15,38,61,100], ['145/184','151/184'])
    assert all(reflection[key] == target[key] for key in ['moments','atoms','triples','H','C','U'])
    reflected_cells = [{'left': str(1-Q(c['right'])), 'right': str(1-Q(c['left'])), 'state': c['state']}
                       for c in reversed(target['cells'])]
    assert reflection['cells'] == reflected_cells
    result['reflection'] = reflection
    endpoint = Q(3, 8)
    speeds = [1,4,5,6,7,11,13]
    distances = [distance(v, endpoint) for v in speeds]
    assert all(d >= D for d in distances)
    left = [v for v in speeds if (v*endpoint) % 1 == D]
    right = [v for v in speeds if (v*endpoint) % 1 == 1-D]
    assert left == [11] and right == [5,13]
    result['tight_endpoint'] = {'time': '3/8', 'distances': dict(zip(map(str,speeds), map(str,distances))),
                                'left_neighborhood_blockers': left, 'right_neighborhood_blockers': right,
                                'valid': True, 'isolated': True}
    # Compare only after our geometry and all 52 own optimizations are complete.
    primary = json.loads((HERE/'results.json').read_text())
    assert primary['protocol_sha256'] == result['protocol_sha256']
    assert primary['primary_sha256'] == sha256((HERE/'primary.py').read_bytes()).hexdigest()
    for key in ['window','speeds','moments','atoms','triples','H','C','U']:
        assert reflection[key] == primary['target_reflection'][key]
    for key, value in result['tight_endpoint'].items():
        assert value == primary['tight_endpoint'][key]
    for name, record in result['cases'].items():
        other = primary['cases'][name]
        for key in ['window','speeds','moments','atoms','triples','H','C','U']:
            assert record['physical'][key] == other['physical'][key], (name, key)
        assert len(record['coordinate_subsets']) == len(other['coordinate_subsets'])
        for own, old in zip(record['coordinate_subsets'], other['coordinate_subsets']):
            for key in ['masks','positive','inclusion_minimal']:
                assert own[key] == old[key], (name, key)
            assert own['certificate']['value'] == old['certificate']['value']
            check_cert(old['certificate'])
            if not own['positive']:
                x = list(map(Q, old['cover_countermodel']))
                assert x[0] == 0 and all(v >= 0 for v in x)
                assert all(dot(incidence(t), x) == Q(record['physical']['moments'][t]) for t in MOMENTS)
                assert all(dot(incidence(t), x) <= Q(record['physical']['moments'][t]) for t in own['masks'])
        assert record['selected'] == other['selected']
        if record['collective'] is not None:
            assert record['collective']['value'] == other['collective']['value']
            check_cert(other['collective'])
    result['primary_sha256'] = sha256((HERE/'results.json').read_bytes()).hexdigest()
    result['summary'] = {'exact_lp_solves': sum(len(c['coordinate_subsets'])+(c['collective'] is not None)
                                               for c in result['cases'].values()),
                         'physical_cells': sum(len(c['physical']['cells']) for c in result['cases'].values())+len(reflection['cells']),
                         'target_selected': result['cases']['target']['selected'],
                         'target_minimal': result['cases']['target']['inclusion_minimal_subsets'],
                         'target_subset_values': [r['certificate']['value'] for r in result['cases']['target']['coordinate_subsets']]}
    assert result['summary']['exact_lp_solves'] == 52
    content = json.dumps(result, indent=2, sort_keys=True)+'\n'
    path = HERE/'verification.json'
    if args.check:
        assert path.read_text() == content
        print('PASS:', json.dumps(result['summary'], sort_keys=True))
    else:
        path.write_text(content)
        print('Wrote verification.json:', json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
