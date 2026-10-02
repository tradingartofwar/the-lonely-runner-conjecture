#!/usr/bin/env python3
"""Compile the fixed parent-edge class into an exact sufficient certificate.

The only geometry input is the pinned six-form parent file. The reused
clipping function does not execute its old ray-specific ranking or controls.
This development example has a previously known answer; see PROTOCOL.md.
"""
import copy
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / '2026-09-29-cc-segment-discovery'
SOURCE_COMMIT = '17b2fca8541540af52cd6c5bf2b09c26c646d240'
PINNED = {
    'PARENT_INPUT.json': '53779c7cf3303e71635b5ba4dd1d9a4dc485612b6a87e1556df80703438f5f62',
    'discover.py': '67e5c1b187bfdcfae57ad5993e330048c20a108c63ed0a8c8e0d1bafcdfd2f5f',
}
ROWS = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2))
CONTROLS = ((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
            (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10))


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def write_json(path, value):
    path.write_text(json.dumps(encode(value), indent=2, sort_keys=True)+'\n')


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(record):
    return record['parent'], *record['edge'], record['seventh_lap']


def checked_record(raw, rows, threshold):
    s = copy.deepcopy(raw)
    s['endpoints'] = [tuple(map(F, p)) for p in s['endpoints']]
    if len(s['endpoints']) != 2 or any(len(p) != 2 for p in s['endpoints']):
        raise ValueError('need exactly two planar endpoints')
    if len(s['labels']) != len(rows) or any(type(m) is not int for m in s['labels']):
        raise ValueError('one integer lap required for each row')
    s['endpoints'].sort()
    for x, y in s['endpoints']:
        if not (0 <= x < 1 and 0 <= y < 1):
            raise ValueError('endpoint outside fundamental square')
        if not all(threshold <= a*x+b*y-m <= 1-threshold
                   for (a,b),m in zip(rows,s['labels'])):
            raise ValueError('endpoint violates a labelled safety band')
    return s


def contact(segment, P, Q):
    first, last = [tuple(map(F,p)) for p in segment['endpoints']]
    values = [Q*x-P*y for x,y in (first,last)]
    low, high = sorted(values)
    h = ceil(low)
    result = {'interval': [low,high], 'first_integer': h, 'hit': h <= high}
    if h <= high:
        u = F(0) if values[0] == values[1] else (h-values[0])/(values[1]-values[0])
        point = tuple(a+u*(b-a) for a,b in zip(first,last))
        assert 0 <= u <= 1 and Q*point[0]-P*point[1] == h
        result.update(parameter=u,point=point)
    return result


def compile_records(records, rows=ROWS, threshold=F(1,8), budget=400):
    """Deterministic sufficient cover; failures never mean failed loneliness."""
    if type(budget) is not int or budget < 0:
        raise ValueError('budget must be a nonnegative integer')
    checked = []
    try:
        for record in sorted(records,key=key):
            checked.append(checked_record(record, rows, threshold))
        if len({s['id'] for s in checked}) != len(checked):
            raise ValueError('duplicate candidate identity')
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
        return {'status':'INVALID_CANDIDATE','reason':str(exc)}
    result = {'schema':'cc-positive-coverage-v1','rows':rows,'threshold':threshold,
              'domain':'positive integer p,q; p!=q for distinct speeds',
              'candidates':checked,'budget':budget}
    ranking = []
    for s in checked:
        (x0,y0),(x1,y1) = s['endpoints']
        alpha,beta = x1-x0,y0-y1
        if alpha > 0 and beta > 0:
            pmax,qmax = ceil(1/beta)-1,ceil(1/alpha)-1
            ranking.append({'id':s['id'],'alpha':alpha,'beta':beta,
                            'P_max':pmax,'Q_max':qmax,'rectangle_pairs':pmax*qmax})
    # Stable sort retains canonical provenance for equal rectangle sizes.
    ranking.sort(key=lambda item:item['rectangle_pairs'])
    result['ranking'] = ranking
    if not ranking:
        return dict(result,status='NO_DESCENDING_SEGMENT')
    lead = ranking[0]
    result['leader'] = lead
    if lead['rectangle_pairs'] > budget:
        return dict(result,status='SCOPE_LIMIT',enumerated_rectangle_pairs=0)
    residual = [(P,Q) for P in range(1,lead['P_max']+1)
                for Q in range(1,lead['Q_max']+1)
                if gcd(P,Q)==1 and lead['alpha']*Q+lead['beta']*P < 1]
    matrix = [{'id':s['id'],'contacts':[dict(pair=pair,**contact(s,*pair)) for pair in residual]}
              for s in checked]
    covered = {row['id']:{tuple(c['pair']) for c in row['contacts'] if c['hit']} for row in matrix}
    menu = [lead['id']]
    missed = set(residual)-covered[lead['id']]
    steps = []
    while missed:
        best = max(checked,key=lambda s:len(missed & covered[s['id']]))
        gained = sorted(missed & covered[best['id']])
        if not gained:
            break
        steps.append({'before':sorted(missed),'chosen':best['id'],'newly_covered':gained})
        menu.append(best['id'])
        missed.difference_update(gained)
    result.update(status='UNCOVERED_PRIMITIVE_PAIRS' if missed else 'COMPLETE_COVER_CERTIFICATE',
                  residual_pairs=residual,contact_matrix=matrix,greedy_steps=steps,
                  chosen_ids=menu,uncovered=sorted(missed),
                  counts={'candidates':len(checked),'descending':len(ranking),
                          'rectangle_pairs':lead['rectangle_pairs'],
                          'residual_pairs':len(residual),'contacts':len(checked)*len(residual),
                          'chosen':len(menu)})
    return result


def bezout(P,Q):
    a,b,r0,r1,s0,s1,steps = P,Q,1,0,0,1,0
    while b:
        k = a//b
        a,b = b,a-k*b
        r0,r1 = r1,r0-k*r1
        s0,s1 = s1,s0-k*s1
        steps += 1
    assert a==1 and r0*P+s0*Q==1
    return r0,s0,steps


def select(certificate, p, q):
    """Evaluate a generated certificate, including after JSON round trip."""
    if type(p) is not int or type(q) is not int or p<=0 or q<=0:
        raise ValueError('positive integer parameters required')
    if certificate['status'] != 'COMPLETE_COVER_CERTIFICATE':
        raise ValueError('complete certificate required')
    d = gcd(p,q)
    P,Q = p//d,q//d
    rows = certificate['rows']
    z = F(certificate['threshold'])
    by_id = {s['id']:s for s in certificate['candidates']}
    for tests,identity in enumerate(certificate['chosen_ids'],1):
        s = checked_record(by_id[identity],rows,z)
        hit = contact(s,P,Q)
        if hit['hit']:
            break
    else:
        raise ArithmeticError('claimed complete menu misses this primitive pair')
    x,y = hit['point']
    h = hit['first_integer']
    r,sb,divisions = bezout(P,Q)
    T = r*x+sb*y
    N = floor(T)
    tau,t = T-N,(T-N)/d
    speeds = [a*p+b*q for a,b in rows]
    phases = [a*x+b*y-m for (a,b),m in zip(rows,s['labels'])]
    laps = [m+(-a*sb+b*r)*h-(a*P+b*Q)*N for (a,b),m in zip(rows,s['labels'])]
    assert 0<t<F(1,d)
    assert all(z<=f<=1-z for f in phases)
    assert all(v*t==ell+f for v,ell,f in zip(speeds,laps,phases))
    return {'pair':[p,q],'primitive':[P,Q],'gcd':d,'distinct_speeds':p!=q,
            'segment':identity,'segment_tests':tests,'contact':hit,
            'point':[x,y],'h':h,'torus_laps':s['labels'],'bezout':[r,sb],
            'euclid_divisions':divisions,'unwrapped_clock':T,'N':N,
            'primitive_time':tau,'time':t,'speeds':speeds,'phases':phases,
            'physical_laps':laps,'minimum':min(min(f,1-f) for f in phases)}


def load_candidates():
    for name,digest in PINNED.items():
        if sha256(PRIOR/name) != digest:
            raise ValueError('pinned source mismatch: '+name)
    spec = importlib.util.spec_from_file_location('preserved_clipping',PRIOR/'discover.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = json.loads((PRIOR/'PARENT_INPUT.json').read_text())
    if tuple(map(tuple,data['rows']))!=ROWS[:-1] or F(data['threshold'])!=F(1,8):
        raise ValueError('unsupported coefficient/threshold input')
    records,counts = module.candidates(data)
    fields = ('id','parent','edge','seventh_lap','labels','endpoints','source_parameters')
    return [{k:s[k] for k in fields} for s in records],counts


def run_controls(certificate):
    witnesses = [select(certificate,p,q) for p,q in CONTROLS]
    for w in witnesses:
        t = w['time']
        direct_laps = [floor(v*t) for v in w['speeds']]
        direct_phases = [v*t-ell for v,ell in zip(w['speeds'],direct_laps)]
        reflected_laps = [floor(v*(1-t)) for v in w['speeds']]
        reflected_phases = [v*(1-t)-ell for v,ell in zip(w['speeds'],reflected_laps)]
        assert direct_laps==w['physical_laps'] and direct_phases==w['phases']
        assert reflected_phases==[1-f for f in w['phases']]
        assert reflected_laps==[v-1-ell for v,ell in zip(w['speeds'],w['physical_laps'])]
        P,Q = w['primitive']; r,s = w['bezout']; x,y = w['point']
        alternate = (r+Q)*x+(s-P)*y
        assert alternate-floor(alternate)==w['primitive_time']
        w.update(reflected_time=1-t,reflected_phases=reflected_phases,
                 reflected_laps=reflected_laps,alternate_bezout_time=(alternate-floor(alternate))/w['gcd'])
    records = [checked_record(s,certificate['rows'],F(certificate['threshold']))
               for s in certificate['candidates']]
    lead = next(s for s in records if s['id']==certificate['leader']['id'])
    non_descending = [s for s in records if not(s['endpoints'][1][0]>s['endpoints'][0][0]
                      and s['endpoints'][1][1]<s['endpoints'][0][1])]
    corrupted = copy.deepcopy(lead)
    corrupted['labels'] = list(corrupted['labels'])
    corrupted['labels'][0] += 1
    failures = {'no_descending':compile_records(non_descending),
                'leader_only':compile_records([lead]),
                'zero_budget':compile_records(records,budget=0),
                'wrong_lap':compile_records([corrupted])}
    expected = {'no_descending':'NO_DESCENDING_SEGMENT','leader_only':'UNCOVERED_PRIMITIVE_PAIRS',
                'zero_budget':'SCOPE_LIMIT','wrong_lap':'INVALID_CANDIDATE'}
    assert all(failures[k]['status']==status for k,status in expected.items())
    endpoint_loss = []
    for identity in certificate['chosen_ids']:
        s = next(s for s in records if s['id']==identity)
        values = sorted(4*x-y for x,y in s['endpoints'])
        first_strict = floor(values[0])+1
        # Both selected images are nondegenerate; a constant image would
        # require testing whether the physical segment has an interior.
        assert values[0]!=values[1]
        endpoint_loss.append({'id':identity,'interval':values,'first_strict_integer':first_strict,
                              'open_hit':first_strict<values[1]})
    assert not any(s['open_hit'] for s in endpoint_loss)
    # Compact failure outputs retain the specific reason and missed pairs.
    summaries = {name:{k:v for k,v in result.items() if k in
                 ('status','reason','uncovered','leader','enumerated_rectangle_pairs','budget')}
                 for name,result in failures.items()}
    return {'status':'PASS','controls':witnesses,'failure_controls':summaries,
            'endpoint_loss_pair':[1,4],'endpoint_loss':endpoint_loss,
            'counts':{'physical_pairs':len(witnesses),'new_physical_pairs':0,
                      'selected_phase_checks':7*len(witnesses),'reflected_phase_checks':7*len(witnesses),
                      'alternate_bezout_checks':len(witnesses)},
            'limits':'Finite controls check implementation; coverage uses the conditional width argument and complete residual domain.'}


def main():
    records,counts = load_candidates()
    certificate = compile_records(records)
    certificate['provenance'] = {'source_commit':SOURCE_COMMIT,'input_sha256':PINNED,
                                 'protocol_sha256':sha256(HERE/'PROTOCOL.md'),
                                 'compiler_sha256':sha256(Path(__file__)),
                                 'clipping_counts':counts,
                                 'known_answer_development_example':True}
    write_json(HERE/'certificate.json',certificate)
    # The evaluator demonstrably reads the generated, serialized record.
    restored = json.loads((HERE/'certificate.json').read_text())
    report = run_controls(restored) if restored['status']=='COMPLETE_COVER_CERTIFICATE' else {'status':restored['status']}
    report['certificate_sha256'] = sha256(HERE/'certificate.json')
    report['compiler_sha256'] = sha256(Path(__file__))
    write_json(HERE/'run.json',report)
    print(json.dumps({'status':certificate['status'],'counts':certificate.get('counts'),
                      'chosen_ids':certificate.get('chosen_ids'),'controls':report['status']}))


if __name__=='__main__':
    main()
