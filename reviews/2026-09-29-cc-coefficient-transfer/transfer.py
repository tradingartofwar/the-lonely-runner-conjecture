#!/usr/bin/env python3
"""One frozen coefficient transfer; unchanged imported coverage/evaluator rule."""
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT/'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json'
COMPILER = ROOT/'reviews/2026-09-29-cc-coverage-compiler/compiler.py'
OLD_CERT = COMPILER.with_name('certificate.json')
OLD_ROWS = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2))
ROWS = OLD_ROWS[:-1]+((6,2),)
CONTROLS = ((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
            (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10))
PARENT_SHA = '53779c7cf3303e71635b5ba4dd1d9a4dc485612b6a87e1556df80703438f5f62'
COMPILER_SHA = 'f998170868ebb261f5a9ae431caba3ace3ecd837438246571a591bfc4e616d92'
OLD_CERT_SHA = '88142d4442d65cb50e8e6068cd1826b5957015ffd2d0742cb6867ab5ab452aa1'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    if isinstance(value,F):
        return str(value)
    if isinstance(value,dict):
        return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [encode(v) for v in value]
    return value


def save(name,value):
    (HERE/name).write_text(json.dumps(encode(value),indent=2,sort_keys=True)+'\n')


def load_api():
    for path,sha in ((PARENT,PARENT_SHA),(COMPILER,COMPILER_SHA),(OLD_CERT,OLD_CERT_SHA)):
        if digest(path)!=sha:
            raise ValueError('Pinned source mismatch: '+str(path))
    spec=importlib.util.spec_from_file_location('frozen_coverage_compiler',COMPILER)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dot(row,point):
    return sum(a*x for a,x in zip(row,point))


def clip_candidates(data,added_row):
    """Parameter-only adaptation of the preserved closed affine edge clip."""
    z=F(data['threshold'])
    jobs=[]
    for parent_index,parent in enumerate(data['parents']):
        vertices=[tuple(map(F,v)) for v in parent['vertices']]
        for i,j in sorted(parent['edges']):
            if vertices[i][2]!=z or vertices[j][2]!=z:
                continue
            a,b=vertices[i][:2],vertices[j][:2]
            sa,sb=dot(added_row,a),dot(added_row,b)
            first,last=ceil(min(sa,sb)-(1-z)),floor(max(sa,sb)-z)
            jobs.append((parent_index,parent,i,j,a,b,sa,sb,first,last))
    attempts=sum(max(0,last-first+1) for *_,first,last in jobs)
    if len(jobs)!=24:
        return [],{'status':'INPUT_SCOPE_MISMATCH','floor_edges':len(jobs)}
    if attempts>256:
        return [],{'status':'CLIPPING_SCOPE_LIMIT','edge_lap_attempts':attempts,'enumerated':0}
    records=[]
    for parent_index,parent,i,j,a,b,sa,sb,first,last in jobs:
        ds=sb-sa
        for k in range(first,last+1):
            if ds:
                u,v=sorted(((k+z-sa)/ds,(k+1-z-sa)/ds))
                lo,hi=max(F(0),u),min(F(1),v)
                if lo>hi:
                    continue
            elif k+z<=sa<=k+1-z:
                lo,hi=F(0),F(1)
            else:
                continue
            endpoints=sorted(tuple(x+t*(y-x) for x,y in zip(a,b)) for t in (lo,hi))
            records.append({'id':f'P{parent_index}:E{i}-{j}:K{k}',
                            'parent':parent_index,'edge':(i,j),'seventh_lap':k,
                            'labels':tuple(parent['labels'])+(k,),
                            'endpoints':endpoints,'source_parameters':(lo,hi)})
    assert len(records)<=attempts<=256
    return records,{'status':'PASS','floor_edges':len(jobs),
                    'edge_lap_attempts':attempts,'candidate_records':len(records),
                    'point_records':sum(s['endpoints'][0]==s['endpoints'][1] for s in records)}


def regression(api,data):
    records,counts=clip_candidates(data,(5,2))
    assert counts['status']=='PASS'
    generated=api.compile_records(records,rows=OLD_ROWS,threshold=F(1,8),budget=400)
    archived=json.loads(OLD_CERT.read_text())
    expected={k:v for k,v in archived.items() if k!='provenance'}
    assert encode(generated)==expected
    return {'status':'PASS','old_row':(5,2),'candidate_records':len(records),
            'all_coverage_fields_exact':True,'compared_fields':sorted(expected),
            'archived_certificate_sha256':digest(OLD_CERT),
            'scope':'Old-row geometry/coverage regression before changed-row execution; no old physical scan.'}


def first_contact(record,P,Q,opened=False):
    a,b=[tuple(map(F,p)) for p in record['endpoints']]
    ha,hb=Q*a[0]-P*a[1],Q*b[0]-P*b[1]
    low,high=sorted((ha,hb))
    if opened and a==b:
        return None
    if ha==hb:
        if ha.denominator!=1:
            return None
        u=F(1,2) if opened else F(0)
        h=int(ha)
    else:
        h=floor(low)+1 if opened else ceil(low)
        if (h>=high if opened else h>high):
            return None
        u=(h-ha)/(hb-ha)
    point=tuple(x+u*(y-x) for x,y in zip(a,b))
    assert Q*point[0]-P*point[1]==h
    return {'interval':(low,high),'first_integer':h,'hit':True,'parameter':u,'point':point}


def recover_partial(api,record,hit,p,q):
    """Recover a real contact without relabelling a partial cover complete."""
    d=gcd(p,q);P,Q=p//d,q//d
    x,y=hit['point'];h=hit['first_integer']
    r,s,steps=api.bezout(P,Q)
    T=r*x+s*y;N=floor(T);tau=T-N;t=tau/d
    laps=[m+(-a*s+b*r)*h-(a*P+b*Q)*N for (a,b),m in zip(ROWS,record['labels'])]
    phases=[a*x+b*y-m for (a,b),m in zip(ROWS,record['labels'])]
    speeds=[a*p+b*q for a,b in ROWS]
    assert all(v*t==ell+f for v,ell,f in zip(speeds,laps,phases))
    assert 0<t<F(1,d) and all(F(1,8)<=f<=F(7,8) for f in phases)
    return {'pair':[p,q],'primitive':[P,Q],'gcd':d,'distinct_speeds':p!=q,
            'segment':record['id'],'contact':hit,'point':[x,y],'h':h,
            'torus_laps':record['labels'],'bezout':[r,s],'euclid_divisions':steps,
            'unwrapped_clock':T,'N':N,'primitive_time':tau,'time':t,'speeds':speeds,
            'phases':phases,'physical_laps':laps,'minimum':min(min(f,1-f) for f in phases)}


def augment_physical(w):
    t=F(w['time']);speeds=w['speeds']
    laps=[floor(v*t) for v in speeds]
    phases=[v*t-ell for v,ell in zip(speeds,laps)]
    assert laps==w['physical_laps'] and phases==w['phases']
    assert len(set([0]+speeds))==(8 if w['distinct_speeds'] else 7)
    reflected_laps=[floor(v*(1-t)) for v in speeds]
    reflected_phases=[v*(1-t)-ell for v,ell in zip(speeds,reflected_laps)]
    assert reflected_laps==[v-1-ell for v,ell in zip(speeds,laps)]
    assert reflected_phases==[1-f for f in phases]
    P,Q=w['primitive'];r,s=w['bezout'];x,y=w['point']
    T=(r+Q)*x+(s-P)*y
    assert T-floor(T)==w['primitive_time']
    w.update(reflected_time=1-t,reflected_laps=reflected_laps,
             reflected_phases=reflected_phases,alternate_bezout_time=(T-floor(T))/w['gcd'])
    return w


def controls(api,certificate):
    records=certificate.get('candidates',[])
    by_id={r['id']:r for r in records}
    complete=certificate['status']=='COMPLETE_COVER_CERTIFICATE'
    chosen=[by_id[i] for i in certificate['chosen_ids']] if complete else records
    witnesses=[];misses=[];endpoint_checks=[]
    for p,q in CONTROLS:
        d=gcd(p,q);P,Q=p//d,q//d
        if complete:
            w=api.select(certificate,p,q)
        else:
            w=None
            for tests,record in enumerate(chosen,1):
                hit=first_contact(record,P,Q)
                if hit:
                    w=recover_partial(api,record,hit,p,q)
                    w['segment_tests']=tests
                    break
        if w:
            witnesses.append(augment_physical(w))
        else:
            misses.append([p,q])
        opened=next((record['id'] for record in chosen if first_contact(record,P,Q,True)),None)
        endpoint_checks.append({'pair':[p,q],'closed_hit':w is not None,
                                'open_hit':opened is not None,'open_candidate':opened})
    return {'controls':witnesses,'uncovered_controls':misses,
            'endpoint_scope':'chosen menu' if complete else 'all supplied candidates',
            'endpoint_checks':endpoint_checks,
            'counts':{'parameter_pairs':18,'physical_witnesses':len(witnesses),
                      'selected_phase_checks':7*len(witnesses),'reflected_phase_checks':7*len(witnesses),
                      'alternate_bezout_checks':len(witnesses)},
            'scope':'Same 18 parameter pairs, newly evaluated changed-family speed configurations.'}


def on_old_floor_edges(data,point):
    x,y=point;out=[];z=F(data['threshold'])
    for parent_index,parent in enumerate(data['parents']):
        vs=[tuple(map(F,v)) for v in parent['vertices']]
        for i,j in sorted(parent['edges']):
            a,b=vs[i],vs[j]
            if a[2]!=z or b[2]!=z:
                continue
            if ((x-a[0])*(b[1]-a[1])==(y-a[1])*(b[0]-a[0])
                and min(a[0],b[0])<=x<=max(a[0],b[0])
                and min(a[1],b[1])<=y<=max(a[1],b[1])):
                out.append({'parent':parent_index,'edge':[i,j]})
    return out


def diagnose(api,data,certificate):
    if certificate['status']!='UNCOVERED_PRIMITIVE_PAIRS':
        return {'status':'NOT_TRIGGERED'}
    pairs=sorted(tuple(p) for p in certificate['uncovered'])
    P,Q=next((pair for pair in pairs if pair[0]!=pair[1]),pairs[0])
    lower,upper=ceil(F(Q-7*P,8)),floor(F(4*Q-P,8))
    max_sections=8*4*max(0,upper-lower+1)
    report={'pair':[P,Q],'distinct_speeds':P!=Q,'orbit_range':[lower,upper],
            'section_budget':10000,'maximum_sections':max_sections}
    if max_sections>10000:
        return dict(report,status='DIAGNOSTIC_SCOPE_LIMIT',examined=0)
    examined=[]
    for index,parent in enumerate(data['parents']):
        for lap in range(1,5):
            labels=parent['labels']+[lap]
            for H in range(lower,upper+1):
                lo,hi=F(0),F(1,2)
                for (a,b),m in zip(ROWS,labels):
                    slope=a+F(b*Q,P)
                    lo=max(lo,(m+F(1,8)+F(b*H,P))/slope)
                    hi=min(hi,(m+F(7,8)+F(b*H,P))/slope)
                section={'parent':index,'seventh_lap':lap,'H':H,
                         'x_interval':[lo,hi],'nonempty':lo<=hi}
                examined.append(section)
                if lo<=hi:
                    x=(lo+hi)/2;y=(Q*x-H)/P
                    rec={'id':f'P{index}:FULL:K{lap}:H{H}','labels':labels}
                    hit={'point':(x,y),'first_integer':H}
                    witness=augment_physical(recover_partial(api,rec,hit,P,Q))
                    membership=on_old_floor_edges(data,(x,y))
                    assert not membership, 'Uncovered edge certificate contradicts diagnosed edge contact'
                    return dict(report,status='RESTORED_PARENT_WITNESS',sections=examined,
                                examined=len(examined),witness=witness,
                                original_floor_edge_memberships=membership)
    return dict(report,status='NO_WITNESS_IN_RESTORED_INPUT',sections=examined,examined=len(examined))


def main():
    api=load_api()
    data=json.loads(PARENT.read_text())
    assert tuple(map(tuple,data['rows']))==ROWS[:-1] and F(data['threshold'])==F(1,8)
    old=regression(api,data)
    save('regression.json',old)
    records,counts=clip_candidates(data,(6,2))
    if counts['status']!='PASS':
        certificate={'status':counts['status'],'clipping':counts}
    else:
        assert all(1<=s['seventh_lap']<=4 for s in records)
        certificate=api.compile_records(records,rows=ROWS,threshold=F(1,8),budget=400)
    certificate['transfer_provenance']={'source_commit':'50d0379628f4a1097d30bbc55d38c581c4338f02',
        'old_added_row':(5,2),'added_row':(6,2),'selection_rule_changed':False,
        'parent_sha256':digest(PARENT),'compiler_sha256':digest(COMPILER),
        'transfer_script_sha256':digest(Path(__file__)),'protocol_sha256':digest(HERE/'PROTOCOL.md'),
        'regression_sha256':digest(HERE/'regression.json'),'clipping_counts':counts}
    save('certificate.json',certificate)
    restored=json.loads((HERE/'certificate.json').read_text())
    run=controls(api,restored) if records else {'controls':[],'uncovered_controls':list(CONTROLS)}
    run.update(status='PASS' if restored['status']=='COMPLETE_COVER_CERTIFICATE' else 'BOUNDED_OUTCOME',
               certificate_status=restored['status'],certificate_sha256=digest(HERE/'certificate.json'),
               diagnostic=diagnose(api,data,restored))
    save('run.json',run)
    print(json.dumps({'status':certificate['status'],'clipping':counts,
                      'coverage_counts':certificate.get('counts'),'chosen_ids':certificate.get('chosen_ids'),
                      'uncovered':certificate.get('uncovered'),'diagnostic':run['diagnostic']['status']}))


if __name__=='__main__':
    main()
