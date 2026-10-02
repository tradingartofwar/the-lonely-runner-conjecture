"""Separate exact reconstruction of the bounded coverage certificate.

No production/discovery module is imported. Geometry is rebuilt by line/plane
intersection, then integer contacts are enumerated in each projected interval.
The old-row regression precedes the one frozen changed-row reconstruction.
AI-authored review, not independent human or formal verification.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd
from pathlib import Path
import hashlib
import json

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


def rebuild(data, added_row, laps_to_try):
    threshold = F(data['threshold'])
    rows = tuple(map(tuple, data['rows'])) + (tuple(added_row),)
    answer = []
    edge_count = 0
    boundary_intersections = 0
    assert 24*len(laps_to_try) <= 256
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
            # Laps supplied from a preflight global-box bound, fixed before clipping.
            for lap in laps_to_try:
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
    assert len(answer) <= 256
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
    assert ranking, 'NO_DESCENDING_SEGMENT'
    lead = ranking[0]
    assert lead['rectangle_pairs'] <= 400, 'SCOPE_LIMIT'
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


def matrix_as_certificate(records, result):
    matrix = []
    for rec in records:
        cells = []
        for pair, cell in zip(result['residual_pairs'], result['contact_matrix'][rec['id']]):
            item = {'pair':pair, 'interval':cell['interval'],
                    'first_integer':ceiling(cell['interval'][0]),
                    'hit':cell['contact'] is not None}
            if cell['contact'] is not None:
                item.update({k:v for k,v in cell['contact'].items() if k != 'h'})
                assert cell['contact']['h'] == item['first_integer']
            cells.append(item)
        matrix.append({'id':rec['id'], 'contacts':cells})
    return matrix


def compare(cert, rows, threshold, records, result):
    assert cert['schema'] == 'cc-positive-coverage-v1'
    assert cert['status'] == ('UNCOVERED_PRIMITIVE_PAIRS' if result['uncovered'] else 'COMPLETE_COVER_CERTIFICATE')
    assert cert['rows'] == encode(rows) and F(cert['threshold']) == threshold
    assert cert['domain'] == 'positive integer p,q; p!=q for distinct speeds'
    assert cert['budget'] == 400
    assert cert['candidates'] == encode(records)
    for field in ('ranking', 'residual_pairs', 'chosen_ids', 'greedy_steps', 'uncovered'):
        assert cert[field] == encode(result[field]), field
    assert cert['leader'] == encode(result['ranking'][0])
    assert cert['contact_matrix'] == encode(matrix_as_certificate(records, result))
    expected_counts = {'candidates':len(records), 'descending':len(result['ranking']),
        'rectangle_pairs':result['ranking'][0]['rectangle_pairs'],
        'residual_pairs':len(result['residual_pairs']),
        'contacts':len(records)*len(result['residual_pairs']), 'chosen':len(result['chosen_ids'])}
    assert cert['counts'] == expected_counts
    return expected_counts


def preflight(data, added):
    z = F(data['threshold'])
    # Positive added coefficients. Both archived and changed cases satisfy this.
    a,b = added
    assert a > 0 and b > 0
    minimum = (a+b)*z
    maximum = a*F(1,2)+b*(1-z)
    laps = list(range(ceiling(minimum-(1-z)),floor(maximum-z)+1))
    return {'row':added,'box_minimum':minimum,'box_maximum':maximum,
            'laps':laps,'edge_lap_attempt_bound':24*len(laps)}


def richer_diagnostic(data, records, result, rows, threshold):
    if not result['uncovered']:
        return {'status':'NOT_TRIGGERED'}
    distinct = [p for p in result['uncovered'] if p[0] != p[1]]
    pair = distinct[0] if distinct else result['uncovered'][0]
    P,Q = pair
    low,high = Q*threshold-P*(1-threshold), Q*F(1,2)-P*threshold
    integers = list(range(ceiling(low),floor(high)+1))
    section_bound = len(data['parents'])*4*len(integers)
    if section_bound > 10000:
        return {'status':'SCOPE_LIMIT','pair':pair,'section_bound':section_bound}
    # Reconstruct each section by intersecting its line with every boundary;
    # this differs from the production affine-interval clipping.
    sections = []
    chosen = None
    for i,parent in enumerate(data['parents']):
        for lap in range(1,5):
            labels = tuple(parent['labels'])+(lap,)
            bounds = [(F(a),F(b),F(m)+1-threshold)
                      for (a,b),m in zip(rows,labels)]
            bounds += [(-F(a),-F(b),-F(m)-threshold)
                       for (a,b),m in zip(rows,labels)]
            bounds += [(F(1),F(0),F(1,2))]
            for h in integers:
                points=set()
                for a,b,c in bounds:
                    determinant=Q*b+P*a
                    if determinant:
                        point=((h*b+P*c)/determinant,(Q*c-a*h)/determinant)
                        if all(u*point[0]+v*point[1] <= w for u,v,w in bounds):
                            points.add(point)
                rec={'parent':i,'seventh_lap':lap,'h':h,
                     'x_interval':None if not points else (min(points)[0],max(points)[0])}
                sections.append(rec)
                if points and chosen is None:
                    x=(min(points)[0]+max(points)[0])/2
                    y=(Q*x-h)/P
                    assert safe((x,y),rows,labels,threshold)
                    edges=[]
                    for j,par in enumerate(data['parents']):
                        vs=[tuple(map(F,v)) for v in par['vertices']]
                        for u,v in sorted(par['edges']):
                            A,B=vs[u],vs[v]
                            if A[2]!=threshold or B[2]!=threshold:
                                continue
                            if ((x-A[0])*(B[1]-A[1]) == (y-A[1])*(B[0]-A[0])
                                and min(A[0],B[0])<=x<=max(A[0],B[0])
                                and min(A[1],B[1])<=y<=max(A[1],B[1])):
                                edges.append({'parent':j,'edge':(u,v)})
                    chosen=dict(rec,point=(x,y),labels=labels,original_floor_edges=edges)
    # Diagnostic exhaustively confirms all section intervals, selects first only.
    return {'status':'FOUND' if chosen else 'NO_WITNESS_IN_RESTORED_PARENTS',
            'pair':pair,'distinct':P!=Q,'orbit_box':(low,high),
            'orbit_integers':integers,'section_bound':section_bound,
            'sections':sections,'selected':chosen}


def main():
    data=json.loads(PARENT.read_text())
    source=ROOT/data['source_path']
    assert hashlib.sha256(source.read_bytes()).hexdigest()==data['source_sha256']
    source_data=json.loads(source.read_text())
    assert data['parents']==source_data['parents'] and data['rows']==source_data['rows'][:6]
    assert hashlib.sha256(PARENT.read_bytes()).hexdigest()=='53779c7cf3303e71635b5ba4dd1d9a4dc485612b6a87e1556df80703438f5f62'
    # Complete old-row regression before constructing any changed-row candidate.
    old_preflight=preflight(data,(5,2))
    old_rows,z,old_records,old_edges,old_intersections=rebuild(data,(5,2),old_preflight['laps'])
    archived=json.loads(ARCHIVE.read_text())['candidates']
    fields=('id','parent','edge','seventh_lap','labels','endpoints','source_parameters')
    assert encode(old_records)==[{k:r[k] for k in fields} for r in archived]
    old_result=construct(old_records)
    old_certificate=ROOT/'reviews/2026-09-29-cc-coverage-compiler/certificate.json'
    old_counts=compare(json.loads(old_certificate.read_text()),old_rows,z,old_records,old_result)
    # One and only one changed row, frozen in PROTOCOL.md.
    new_preflight=preflight(data,(6,2))
    assert new_preflight['laps']==[1,2,3,4]
    rows,z,records,edges,intersections=rebuild(data,(6,2),new_preflight['laps'])
    assert edges==24
    result=construct(records)
    cert=json.loads((HERE/'certificate.json').read_text())
    counts=compare(cert,rows,z,records,result)
    run=json.loads((HERE/'run.json').read_text())
    assert run['certificate_sha256']==hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest()
    assert run['diagnostic']=={'status':'NOT_TRIGGERED'} if not result['uncovered'] else True
    endpoint_checks=[]
    by_id={r['id']:r for r in records}
    assert run['endpoint_scope']=='chosen menu'
    for item in run['endpoint_checks']:
        p,q=item['pair']; d=gcd(p,q); P,Q=p//d,q//d
        open_identity=None
        for identity in result['chosen_ids']:
            rec=by_id[identity]; a,b=rec['endpoints']
            ha,hb=Q*a[0]-P*a[1],Q*b[0]-P*b[1]
            low,high=min(ha,hb),max(ha,hb)
            hit=(a!=b and low==high and low.denominator==1) or any(
                low<h<high for h in range(ceiling(low),floor(high)+1))
            if hit:
                open_identity=identity
                break
        check={'pair':item['pair'], 'closed_hit':any(
            contact(by_id[i],(P,Q))['contact'] is not None for i in result['chosen_ids']),
            'open_hit':open_identity is not None,'open_candidate':open_identity}
        assert check==item
        endpoint_checks.append(check)
    diagnostic=richer_diagnostic(data,records,result,rows,z)
    if result['uncovered']:
        # The full finite matrix gives the stronger candidate-class conclusion.
        for pair in result['uncovered']:
            assert all(contact(rec,pair)['contact'] is None for rec in records)
    output={'status':'PASS','authorship':'Separately tasked AI reviewer; no production imports',
        'method':'Exact supporting-line/boundary intersections; explicit integer projection contacts',
        'regression':{'status':'PASS','counts':old_counts,'preflight':old_preflight},
        'preflight':new_preflight,'counts':counts,'floor_edges':edges,
        'line_boundary_intersections':intersections,
        'endpoint_band_inequalities':len(records)*2*len(rows)*2,
        'result':result,'diagnostic':diagnostic,'menu_endpoint_checks':endpoint_checks,
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (PARENT,ARCHIVE,old_certificate,HERE/'PROTOCOL.md',HERE/'certificate.json',HERE/'run.json')},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(encode(output),sort_keys=True,indent=2))


if __name__=='__main__':
    main()
