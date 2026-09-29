"""Separate exact reconstruction of the bounded coverage certificate.

No production/discovery module is imported. Geometry is rebuilt by line/plane
intersection, then integer contacts are enumerated in each projected interval.
Production failure controls are exercised only in a separately marked process.
AI-authored review, not independent human or formal verification.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json"
ARCHIVE = PARENT.with_name("discovery.json")


def ceiling(x):
    return (x.numerator + x.denominator - 1) // x.denominator


def floor(x):
    return x.numerator // x.denominator


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def provenance(rec):
    return rec['parent'], tuple(rec['edge']), rec['seventh_lap']


def dot(row, point):
    return sum(a*b for a, b in zip(row, point))


def safe(point, rows, laps, threshold):
    return all(threshold <= dot(row, point)-m <= 1-threshold
               for row, m in zip(rows, laps))


def rebuild(data):
    threshold = F(data['threshold'])
    rows = tuple(map(tuple, data['rows'])) + ((5, 2),)
    answer = []
    edge_count = 0
    boundary_intersections = 0
    for index, parent in enumerate(data['parents']):
        vertices = [tuple(map(F, v)) for v in parent['vertices']]
        for i, j in sorted(parent['edges']):
            a3, b3 = vertices[i], vertices[j]
            if a3[2] != threshold or b3[2] != threshold:
                continue
            edge_count += 1
            a, b = a3[:2], b3[:2]
            assert a != b
            # Endpoints satisfy all parent bands. Their convex hull does too.
            assert safe(a, rows[:6], parent['labels'], threshold)
            assert safe(b, rows[:6], parent['labels'], threshold)
            assert all(threshold <= p[0] <= F(1, 2)
                       and threshold <= p[1] <= 1-threshold for p in (a, b))
            # Supporting line A*x+B*y=C, not the production affine t clipping.
            A, B = b[1]-a[1], a[0]-b[0]
            C = A*a[0]+B*a[1]
            # Folded box implies 7/8 <= 5*x+2*y <= 17/4. Exactly k=0..4
            # can have their [k+1/8,k+7/8] bands meet that global range.
            for lap in range(5):
                labels = tuple(parent['labels']) + (lap,)
                points = {p for p in (a, b) if safe(p, rows, labels, threshold)}
                for row, m in zip(rows, labels):
                    U, V = row
                    det = A*V-B*U
                    if not det:
                        continue
                    for W in (m+threshold, m+1-threshold):
                        boundary_intersections += 1
                        point = ((C*V-B*W)/det, (A*W-C*U)/det)
                        if (all(min(a[k], b[k]) <= point[k] <= max(a[k], b[k])
                                for k in range(2))
                                and safe(point, rows, labels, threshold)):
                            points.add(point)
                if points:
                    coord = 0 if a[0] != b[0] else 1
                    parameters = sorted((p[coord]-a[coord])/(b[coord]-a[coord])
                                        for p in (min(points), max(points)))
                    answer.append({'id':f'P{index}:E{i}-{j}:K{lap}',
                                   'parent':index, 'edge':(i, j),
                                   'seventh_lap':lap, 'labels':labels,
                                   'endpoints':(min(points), max(points)),
                                   'source_parameters':parameters})
    answer.sort(key=provenance)
    return rows, threshold, answer, edge_count, boundary_intersections


def contact(rec, pair):
    P, Q = pair
    a, b = rec['endpoints']
    Ha, Hb = Q*a[0]-P*a[1], Q*b[0]-P*b[1]
    lo, hi = min(Ha, Hb), max(Ha, Hb)
    # Enumerate the exact integer set, rather than treating width as existence.
    integers = list(range(ceiling(lo), floor(hi)+1))
    if not integers:
        return {'interval':(lo, hi), 'contact':None}
    h = integers[0]
    weight = F(0) if Ha == Hb else (h-Ha)/(Hb-Ha)
    point = tuple((1-weight)*a[k]+weight*b[k] for k in range(2))
    assert 0 <= weight <= 1 and Q*point[0]-P*point[1] == h
    return {'interval':(lo, hi), 'contact':{
        'h':h, 'parameter':weight, 'point':point}}


def construct(records):
    ranking = []
    for rec in records:
        a, b = rec['endpoints']
        alpha, beta = b[0]-a[0], a[1]-b[1]
        if alpha > 0 and beta > 0:
            Pmax, Qmax = ceiling(1/beta)-1, ceiling(1/alpha)-1
            ranking.append({'id':rec['id'], 'alpha':alpha, 'beta':beta,
                            'P_max':Pmax, 'Q_max':Qmax,
                            'rectangle_pairs':Pmax*Qmax})
    by_id = {r['id']:r for r in records}
    ranking.sort(key=lambda r:(r['rectangle_pairs'], provenance(by_id[r['id']])))
    lead = ranking[0]
    pairs = [pair for pair in product(range(1, lead['P_max']+1),
                                      range(1, lead['Q_max']+1))
             if gcd(*pair) == 1 and lead['alpha']*pair[1]+lead['beta']*pair[0] < 1]
    matrix = {r['id']:[contact(r, p) for p in pairs] for r in records}
    selected = [lead['id']]
    gaps = {j for j in range(len(pairs)) if matrix[lead['id']][j]['contact'] is None}
    first_gaps = sorted(gaps)
    steps = []
    while gaps:
        counts = {r['id']:sum(matrix[r['id']][j]['contact'] is not None for j in gaps)
                  for r in records}
        best = min(records, key=lambda r:(-counts[r['id']], provenance(r)))['id']
        covered = sorted(j for j in gaps if matrix[best][j]['contact'] is not None)
        if not covered:
            break
        steps.append({'before':[pairs[j] for j in sorted(gaps)], 'chosen':best,
                      'newly_covered':[pairs[j] for j in covered]})
        selected.append(best)
        gaps.difference_update(covered)
    return {'ranking':ranking, 'residual_pairs':pairs, 'contact_matrix':matrix,
            'chosen_ids':selected, 'greedy_steps':steps,
            'leader_misses':[pairs[j] for j in first_gaps],
            'uncovered':[pairs[j] for j in sorted(gaps)]}


def compare_production(data, rows, threshold, records, result):
    cert = json.loads((HERE/'certificate.json').read_text())
    run = json.loads((HERE/'run.json').read_text())
    assert cert['schema'] == 'cc-positive-coverage-v1'
    assert cert['status'] == 'COMPLETE_COVER_CERTIFICATE'
    assert cert['rows'] == encode(rows) and F(cert['threshold']) == threshold
    assert cert['domain'] == 'positive integer p,q; p!=q for distinct speeds'
    assert cert['budget'] == 400
    assert cert['candidates'] == encode(records)
    for field in ('ranking', 'residual_pairs', 'chosen_ids', 'greedy_steps', 'uncovered'):
        assert cert[field] == encode(result[field]), field
    assert cert['leader'] == encode(result['ranking'][0])
    matrix = []
    for rec in records:
        cells = []
        for pair, cell in zip(result['residual_pairs'], result['contact_matrix'][rec['id']]):
            item = {'pair':pair, 'interval':cell['interval'],
                    'first_integer':ceiling(cell['interval'][0]),
                    'hit':cell['contact'] is not None}
            if cell['contact'] is not None:
                item.update({k:v for k, v in cell['contact'].items() if k != 'h'})
                assert cell['contact']['h'] == item['first_integer']
            cells.append(item)
        matrix.append({'id':rec['id'], 'contacts':cells})
    assert cert['contact_matrix'] == encode(matrix)
    assert cert['counts'] == {'candidates':27, 'descending':10, 'rectangle_pairs':21,
                              'residual_pairs':8, 'contacts':216, 'chosen':2}
    source = ROOT/data['source_path']
    source_data = json.loads(source.read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == data['source_sha256']
    assert data['parents'] == source_data['parents']
    assert data['rows'] == source_data['rows'][:6]
    provenance_data = cert['provenance']
    assert provenance_data['source_commit'] == '17b2fca8541540af52cd6c5bf2b09c26c646d240'
    for name, digest in provenance_data['input_sha256'].items():
        assert hashlib.sha256((PARENT.parent/name).read_bytes()).hexdigest() == digest
    for name in ('compiler', 'protocol'):
        path = HERE/('compiler.py' if name == 'compiler' else 'PROTOCOL.md')
        assert hashlib.sha256(path.read_bytes()).hexdigest() == provenance_data[name+'_sha256']
    assert provenance_data['clipping_counts'] == {'edge_lap_pairs':27, 'floor_edges':24}
    assert provenance_data['known_answer_development_example'] is True
    assert hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest() == run['certificate_sha256']
    assert run['compiler_sha256'] == provenance_data['compiler_sha256']
    assert run['status'] == 'PASS'
    endpoint_loss = []
    for rec in records:
        if rec['id'] not in result['chosen_ids']:
            continue
        a, b = rec['endpoints']
        low, high = sorted((4*a[0]-a[1], 4*b[0]-b[1]))
        interior_integers = [h for h in range(ceiling(low), floor(high)+1)
                             if low < h < high]
        assert low < high and not interior_integers
        endpoint_loss.append({'id':rec['id'], 'interval':[low, high],
                              'first_strict_integer':floor(low)+1, 'open_hit':False})
    endpoint_loss.sort(key=lambda r:result['chosen_ids'].index(r['id']))
    assert run['endpoint_loss_pair'] == [1, 4]
    assert run['endpoint_loss'] == encode(endpoint_loss)
    return {'schema':'all geometry, ranking, coverage and provenance fields compared',
            'full_contact_entries':len(records)*len(result['residual_pairs']),
            'endpoint_loss':endpoint_loss}


def production_failure_controls():
    # The numerical reconstruction above has no production imports. This
    # isolated process deliberately calls the implementation to test its
    # declared failure outputs on the four frozen same-input ablations.
    code = r'''
import copy,json,runpy,sys
from fractions import Fraction as F
api=runpy.run_path(sys.argv[1]); cert=json.load(open(sys.argv[2]))
rows=cert['candidates']; leader=next(r for r in rows if r['id']==cert['leader']['id'])
non_descending=[]
for rec in rows:
 a,b=[tuple(map(F,p)) for p in rec['endpoints']]
 if not(b[0]>a[0] and b[1]<a[1]): non_descending.append(rec)
bad=copy.deepcopy(leader);bad['labels'][0]+=1
outputs={
 'no_descending':api['compile_records'](non_descending),
 'leader_only':api['compile_records']([leader]),
 'zero_budget':api['compile_records'](rows,budget=0),
 'wrong_lap':api['compile_records']([bad])}
assert outputs['zero_budget']['enumerated_rectangle_pairs']==0
assert 'contact_matrix' not in outputs['zero_budget']
keep={'status','reason','uncovered','leader','enumerated_rectangle_pairs','budget'}
print(json.dumps(api['encode']({k:{a:b for a,b in v.items() if a in keep} for k,v in outputs.items()}),sort_keys=True))
'''
    process = subprocess.run([sys.executable, '-c', code, str(HERE/'compiler.py'),
                              str(HERE/'certificate.json')], check=True,
                             capture_output=True, text=True)
    failures = json.loads(process.stdout)
    expected = {'no_descending':'NO_DESCENDING_SEGMENT',
                'leader_only':'UNCOVERED_PRIMITIVE_PAIRS',
                'zero_budget':'SCOPE_LIMIT', 'wrong_lap':'INVALID_CANDIDATE'}
    assert {k:v['status'] for k, v in failures.items()} == expected
    assert failures['leader_only']['uncovered'] == [[1, 2], [1, 4]]
    assert failures == json.loads((HERE/'run.json').read_text())['failure_controls']
    return failures


def main():
    data = json.loads(PARENT.read_text())
    rows, threshold, records, edges, intersections = rebuild(data)
    archived = json.loads(ARCHIVE.read_text())['candidates']
    fields = ('id', 'parent', 'edge', 'seventh_lap', 'labels', 'endpoints', 'source_parameters')
    assert encode(records) == [{k:r[k] for k in fields} for r in archived]
    result = construct(records)
    assert not result['uncovered']
    assert len(records) == 27
    comparison = compare_production(data, rows, threshold, records, result)
    failures = production_failure_controls()
    output = {'status':'PASS: separate geometry/coverage reconstruction and fixed failure controls',
              'authorship':'Separately tasked AI reviewer; no compiler imports in numerical reconstruction',
              'candidate_records':len(records), 'floor_edges':edges,
              'line_boundary_intersections':intersections,
              'endpoint_band_inequalities':len(records)*2*len(rows)*2,
              'result':result, 'production_comparison':comparison,
              'production_failure_controls':failures,
              'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in (PARENT, ARCHIVE, HERE/'PROTOCOL.md',
                                        HERE/'compiler.py', HERE/'certificate.json', HERE/'run.json')},
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(encode(output), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
