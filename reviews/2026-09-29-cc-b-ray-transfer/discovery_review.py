#!/usr/bin/env python3
"""Parent-only, native-coordinate reconstruction of B segment discovery.

Independently authored within shared AI context. No imports from discovery or
adapter code, no optimum/selector output input. Uses Fraction throughout.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / '2026-09-29-cc-segment-discovery' / 'PARENT_INPUT.json'
ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
Z = F(1, 8)


def ceil(v):
    return -((-v.numerator) // v.denominator)


def floor(v):
    return v.numerator // v.denominator


def phase(point, row, lap):
    return row[0] * point[0] + row[1] * point[1] - lap


def interpolate(a, b, w):
    return tuple(a[i] + w * (b[i] - a[i]) for i in range(3))


def key(c):
    return c['parent'], c['edge'], c['lap']


def orbit(point, q):
    return q * point[1] - point[0]


def interval(c, q):
    return tuple(sorted(orbit(p, q) for p in c['endpoints']))


def covers(c, q):
    low, high = interval(c, q)
    return ceil(low) <= high


def recover(c, q):
    a, b = c['endpoints']
    ha, hb = orbit(a, q), orbit(b, q)
    low, high = min(ha, hb), max(ha, hb)
    h = ceil(low)
    assert h <= high
    w = F(0) if ha == hb else (h - ha) / (hb - ha)
    assert 0 <= w <= 1
    p = interpolate(a, b, w)
    assert orbit(p, q) == h
    laps = tuple(m + row[0] * h for row, m in zip(ROWS, c['labels']))
    return {'q': q, 'key': key(c), 'point': p, 'clock': p[1], 'h': h,
            'physical_laps_row_order': laps}


def reconstruct(data):
    candidates = []
    floor_edges = []
    for pid, parent in enumerate(data['parents']):
        vertices = [tuple(map(F, p)) for p in parent['vertices']]
        # Audit all input vertex constraints, independently of incidence input.
        for p in vertices:
            for _, normal, bound in parent['constraints']:
                assert sum(F(n) * v for n, v in zip(normal, p)) <= F(bound)
        for edge in parent['edges']:
            a, b = [vertices[i] for i in edge]
            if a[2] != Z or b[2] != Z:
                continue
            floor_edges.append((pid, tuple(edge)))
            sa, sb = 5*a[0] + 2*a[1], 5*b[0] + 2*b[1]
            # Integer laps whose closed safe band can meet this edge image.
            kmin = ceil(min(sa, sb) - (1-Z))
            kmax = floor(max(sa, sb) - Z)
            for k in range(kmin, kmax + 1):
                lo, hi = F(0), F(1)
                if sa == sb:
                    if not k + Z <= sa <= k + 1 - Z:
                        continue
                else:
                    left, right = sorted(((k+Z-sa)/(sb-sa), (k+1-Z-sa)/(sb-sa)))
                    lo, hi = max(lo, left), min(hi, right)
                    if lo > hi:
                        continue
                points = sorted((interpolate(a,b,lo), interpolate(a,b,hi)),
                                key=lambda p: (p[1],p[0],p[2]))
                labels = tuple(parent['labels']) + (k,)
                phases = [[phase(p, row, m) for row,m in zip(ROWS, labels)] for p in points]
                assert all(Z <= f <= 1-Z for row in phases for f in row)
                dx = points[1][0]-points[0][0]
                dy = points[1][1]-points[0][1]
                assert dy >= 0
                Q = max(2, ceil((1+dx)/dy)) if dy > 0 else None
                if Q is not None:
                    assert Q*dy-dx >= 1
                    if Q > 2:
                        assert (Q-1)*dy-dx < 1
                candidates.append({'parent':pid,'edge':tuple(edge),'lap':k,
                    'labels':labels,'endpoints':tuple(points),'source_parameter':(lo,hi),
                    'dx':dx,'dy':dy,'tail_Q':Q, 'endpoint_phases':phases})
    candidates.sort(key=key)
    finite_tail = [c for c in candidates if c['tail_Q'] is not None]
    primary = min(finite_tail, key=lambda c: (c['tail_Q'], key(c)))
    Q = primary['tail_Q']
    if Q > 26:
        raise RuntimeError('Frozen scope guard: derived prefix would exceed q=25')
    prefix = set(range(2, Q))
    chosen = [primary]
    remaining = prefix - {q for q in prefix if covers(primary,q)}
    greedy = [{'key':key(primary),'remaining':sorted(remaining)}]
    while remaining:
        eligible = [(len([q for q in remaining if covers(c,q)]), c) for c in candidates]
        gain, nxt = min(eligible, key=lambda pair: (-pair[0], key(pair[1])))
        if gain == 0:
            raise RuntimeError('Frozen candidate class does not cover prefix')
        chosen.append(nxt)
        remaining -= {q for q in remaining if covers(nxt,q)}
        greedy.append({'key':key(nxt),'remaining':sorted(remaining)})
    matrix = [{'key':key(c),'tail_Q':c['tail_Q'],
               'covered_prefix':[q for q in sorted(prefix) if covers(c,q)],
               'prefix_intervals':[{'q':q,'interval':interval(c,q),'first_integer':ceil(interval(c,q)[0]),
                                    'covered':covers(c,q)} for q in sorted(prefix)]}
              for c in candidates]
    selected = []
    for q in range(2,26):
        c = next(c for c in chosen if covers(c,q))
        selected.append(recover(c,q))
    return {'floor_edge_count':len(floor_edges), 'floor_edges':floor_edges,
            'candidate_count':len(candidates),'candidates':candidates,
            'minimum_tail_Q':Q,'prefix':sorted(prefix),'prefix_matrix':matrix,
            'chosen_keys':[key(c) for c in chosen], 'greedy_trace':greedy,
            'selection_cost_bound':len(chosen),
            'tail_certificate':{'key':key(primary),'dy':primary['dy'],'dx':primary['dx'],
                                'Q':Q,'width_at_Q':Q*primary['dy']-primary['dx']},
            'archived_scope_selected_points':selected}


def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)):
        return [serial(v) for v in x]
    return x


def main():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    assert F(data['threshold']) == Z
    assert tuple(map(tuple,data['rows'])) == ROWS[:-1]
    result = reconstruct(data)
    out = {'status':'REPRODUCED arithmetic; all-q coverage remains proof candidate',
           'authorship':'Separate AI reviewer within shared model/context; not independent human review',
           'read_order':['AGENTS.md','PROTOCOL.md','PARENT_INPUT.json','CLAIM_STATUS.md','CONTRIBUTING.md'],
           'input_sha256':hashlib.sha256(raw).hexdigest(),
           'inputs_used_for_choices':['PARENT_INPUT.json','frozen B-ray transfer protocol'],
           'excluded_inputs':['A discovery output/code','coordinator B adapter/results','B optimum/spectrum'],
           'coordinate_convention':'native (x,y); H_prime=q*y-x; physical clock y; endpoint orientation (y,x)',
           'checks':result}
    path = HERE / 'discovery_review.json'
    path.write_text(json.dumps(serial(out),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'candidate_count':result['candidate_count'],'minimum_tail_Q':result['minimum_tail_Q'],
                      'chosen_keys':serial(result['chosen_keys']),'greedy_trace':serial(result['greedy_trace']),
                      'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))


def compare_after_freeze():
    """Post-freeze comparison only; never an input to reconstruct()."""
    ours_raw = (HERE / 'discovery_review.json').read_bytes()
    theirs_raw = (HERE / 'transfer.json').read_bytes()
    ours = json.loads(ours_raw)['checks']
    theirs = json.loads(theirs_raw)
    def cid(c):
        return f"P{c['parent']}:E{c['edge'][0]}-{c['edge'][1]}:K{c['lap']}"
    observed = {c['id']: c for c in theirs['candidates']}
    assert len(observed) == len(ours['candidates'])
    for c in ours['candidates']:
        other = observed[cid(c)]
        assert c['parent'] == other['parent']
        assert c['edge'] == other['edge']
        assert c['lap'] == other['seventh_lap']
        assert c['labels'] == other['labels']
        assert c['endpoints'] == [[p[1],p[0],'1/8'] for p in other['endpoints']]
        assert c['dx'] == other['dy'] and c['dy'] == other['dx']
        assert c['tail_Q'] == other['tail_cutoff']
        assert c['source_parameter'] == other['source_parameters']
    for m in ours['prefix_matrix']:
        pid, edge, lap = m['key']
        id_ = f'P{pid}:E{edge[0]}-{edge[1]}:K{lap}'
        assert m['covered_prefix'] == theirs['cover']['coverage'][id_]
    keys = [f'P{pid}:E{edge[0]}-{edge[1]}:K{lap}' for pid,edge,lap in ours['chosen_keys']]
    assert keys == theirs['cover']['chosen_ids']
    assert ours['minimum_tail_Q'] == theirs['cover']['cutoff']
    assert ours['prefix'] == theirs['cover']['prefix']
    for c, other in zip(ours['archived_scope_selected_points'], theirs['physical_controls']):
        cert = other['certificate']
        assert c['q'] == cert['q']
        assert c['point'] == cert['native_point']
        assert c['clock'] == cert['time']
        assert c['h'] == cert['h']
        assert c['physical_laps_row_order'] == cert['physical_laps']
    print(json.dumps({'comparison':'ALL MATCH', 'candidate_records':len(ours['candidates']),
                      'prefix_boolean_entries':len(ours['candidates'])*len(ours['prefix']),
                      'selected_recovery_records':len(ours['archived_scope_selected_points']),
                      'frozen_review_sha256':hashlib.sha256(ours_raw).hexdigest(),
                      'coordinator_output_sha256':hashlib.sha256(theirs_raw).hexdigest()},indent=2))


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--compare']:
        compare_after_freeze()
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit('Usage: discovery_review.py [--compare]')
