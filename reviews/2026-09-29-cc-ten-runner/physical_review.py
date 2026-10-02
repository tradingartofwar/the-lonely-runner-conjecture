#!/usr/bin/env python3
"""Independent physical review of the frozen joint ten-runner transfer.
No production imports. Exact coordinate-lap recovery and direct time bands.
"""
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ROWS=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),(38,18))
CONTROLS=((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
          (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10),
          (2,2),(4,2),(1,20),(2,40))
PROTOCOL_SHA='7d380e243a06de179fa2b456a86ebbeee35f8b8de75fc5ead6ebf8d15684f506'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [encode(v) for v in value]
    return value


def phase(value):
    return value-floor(value)


def primary(p,q):
    return p!=q and p!=2*q


def physical(p,q,xy,labels,z):
    d=gcd(p,q);P,Q=p//d,q//d
    x,y=map(F,xy);labels=list(labels)
    assert len(labels)==9 and 0<=x<1 and 0<=y<1
    H=Q*x-P*y
    assert H.denominator==1
    H=int(H)
    i=(-H*pow(Q,-1,P))%P if P>1 else 0
    j=(Q*i+H)//P
    assert P*j==Q*i+H
    tau=(x+i)/P;t=tau/d
    assert 0<tau<1 and Q*tau==y+j
    assert floor(P*tau)==i and floor(Q*tau)==j
    speeds=[a*p+b*q for a,b in ROWS]
    phases=[phase(v*t) for v in speeds]
    laps=[floor(v*t) for v in speeds]
    assert phases==[a*x+b*y-m for (a,b),m in zip(ROWS,labels)]
    assert laps==[m+a*i+b*j for (a,b),m in zip(ROWS,labels)]
    assert all(z<=f<=1-z for f in phases)
    distinct_count=len(set([0]+speeds))
    assert (distinct_count==10)==primary(p,q)
    rt=1-t
    reflected=[phase(v*rt) for v in speeds]
    reflected_laps=[floor(v*rt) for v in speeds]
    assert reflected==[1-f for f in phases]
    assert reflected_laps==[v-l-1 for v,l in zip(speeds,laps)]
    r=pow(P,-1,Q) if Q>1 else 0
    s=(1-r*P)//Q
    assert r*P+s*Q==1
    alternative=[]
    for shift in (-1,1):
        rr,ss=r+shift*Q,s-shift*P
        T=rr*x+ss*y;N=floor(T)
        assert phase(T)==tau
        shifted=[m+(-a*ss+b*rr)*H-(a*P+b*Q)*N for (a,b),m in zip(ROWS,labels)]
        assert shifted==laps
        alternative.append(dict(shift=shift,r=rr,s=ss,N=N,unwrapped_clock=T,
            primitive_time=phase(T),physical_laps=shifted))
    return encode(dict(pair=[p,q],primitive=[P,Q],gcd=d,point=[x,y],h=H,
        coordinate_laps=[i,j],primitive_time=tau,time=t,speeds=speeds,
        distinct_speeds=distinct_count==10,distinct_speed_count=distinct_count,
        torus_laps=labels,physical_laps=laps,phases=phases,
        minimum=min(min(f,1-f) for f in phases),reflected_time=rt,
        reflected_phases=reflected,reflected_laps=reflected_laps,
        alternative_bezout=alternative))


def contact(P,Q,endpoints,opened=False):
    A,B=[tuple(map(F,pt)) for pt in endpoints]
    ha,hb=Q*A[0]-P*A[1],Q*B[0]-P*B[1]
    lo,hi=sorted((ha,hb))
    if opened and A==B: return None
    if ha==hb:
        if ha.denominator!=1: return None
        h=int(ha);u=F(1,2) if opened else F(0)
    else:
        h=floor(lo)+1 if opened else ceil(lo)
        if (h>=hi if opened else h>hi): return None
        u=(h-ha)/(hb-ha)
    assert (0<u<1) if opened else (0<=u<=1)
    xy=[a+u*(b-a) for a,b in zip(A,B)]
    assert Q*xy[0]-P*xy[1]==h
    return encode(dict(point=xy,h=h,parameter=u,interval=[lo,hi]))


def first_contact(records,P,Q,opened=False):
    for tests,c in enumerate(records,1):
        hit=contact(P,Q,c['endpoints'],opened)
        if hit is not None: return c,hit,tests
    return None


def check_emitted(record,emitted,candidate=None):
    for key in ('primitive','gcd','point','h','primitive_time','time','speeds',
                'distinct_speeds','torus_laps','physical_laps','phases','minimum',
                'reflected_time','reflected_phases','reflected_laps'):
        assert record[key]==emitted[key],(key,record[key],emitted[key])
    if 'distinct_speed_count' in emitted:
        assert record['distinct_speed_count']==emitted['distinct_speed_count']
    P,Q=record['primitive'];x,y=map(F,record['point'])
    r,s=emitted['bezout'];T=r*x+s*y
    assert r*P+s*Q==1 and emitted['N']==floor(T)
    assert F(emitted['unwrapped_clock'])==T
    assert F(emitted['alternate_bezout_time'])==F(record['time'])
    assert phase(T)==F(record['primitive_time'])
    if candidate is not None:
        hit=contact(P,Q,candidate['endpoints'])
        expected={'point':hit['point'],'first_integer':hit['h'],
                  'parameter':hit['parameter'],'interval':hit['interval'],'hit':True}
        assert emitted['contact']==expected
        assert record['segment']==emitted['segment']
        if 'segment_tests' in emitted:
            assert record['segment_tests']==emitted['segment_tests']
    a,b=P,Q;steps=0
    while b: a,b=b,a%b;steps+=1
    assert emitted['euclid_divisions']==steps


def physical_time_bands(P,Q,z):
    """One diagnosed direction; complete direct band unions subject to frozen caps."""
    assert gcd(P,Q)==1 and P>0 and Q>0
    speeds=[a*P+b*Q for a,b in ROWS]
    report=dict(pair=[P,Q],threshold=z,
        method='Direct physical safe-lap unions in one period, folded by {P*t}<=1/2.',
        full_band_preflight=sum(speeds),speed_sum_budget=10000,interval_band_test_budget=200000)
    if sum(speeds)>10000:
        return encode(dict(report,status='REVIEW_SCOPE_LIMIT',reason='SPEED_SUM_LIMIT',
                           interval_band_tests=0,exhausted=None,safe_intervals=None))
    branches=[(F(0),F(1),[])];counts=[];total_tests=0
    for index,v in enumerate(speeds):
        next_tests=len(branches)*v
        if total_tests+next_tests>200000:
            return encode(dict(report,status='REVIEW_SCOPE_LIMIT',reason='INTERVAL_BAND_TEST_LIMIT',
                next_row=index+1,next_row_test_preflight=next_tests,
                interval_band_tests=total_tests,stage_counts=counts,
                exhausted=None,safe_intervals=None))
        upper=F(1,2) if index==0 else 1-z
        next_branches=[];intersections=0
        bands=[(F(ell+z,v),F(ell+upper,v),ell) for ell in range(v)]
        for lo,hi,labels in branches:
            for left,right,ell in bands:
                total_tests+=1
                if right<lo or left>hi: continue
                intersections+=1
                L,R=max(lo,left),min(hi,right)
                if L<=R: next_branches.append((L,R,labels+[ell]))
        branches=next_branches
        counts.append(dict(row=index+1,speed=v,lap_bands=v,
            interval_band_tests=next_tests,nonempty_intersections=intersections,
            surviving_intervals=len(branches)))
        if not branches: break
    return encode(dict(report,status='COMPLETE',interval_band_tests=total_tests,
        stage_counts=counts,
        safe_intervals=[dict(time_interval=[L,R],physical_laps=labels) for L,R,labels in branches],
        exhausted=not branches))


def diagnostic_review(stage):
    cert=stage['certificate'];diag=stage['diagnostic'];z=F(stage['threshold'])
    missed=sorted(tuple(pair) for pair in cert.get('uncovered',[]) if primary(*pair))
    if cert['status']!='UNCOVERED_PRIMITIVE_PAIRS' or not missed:
        assert diag['status']=='NOT_TRIGGERED'
        return {'status':'NOT_TRIGGERED','physical_time_bands_evaluated':False}
    P,Q=missed[0]
    assert diag['pair']==[P,Q] and primary(P,Q)
    assert all(contact(P,Q,c['endpoints']) is None for c in cert['candidates'])
    if diag['status']=='DIAGNOSTIC_SCOPE_LIMIT':
        assert diag['preflight_tuples']>100000 and diag['enumerated']==0
        return {'status':'PRESERVED_SCOPE_LIMIT','pair':[P,Q],
                'physical_time_bands_evaluated':False,'physical_conclusion':None}
    direct=physical_time_bands(P,Q,z)
    if diag['status']=='EXHAUSTED_FOR_PAIR':
        if direct['status']=='REVIEW_SCOPE_LIMIT':
            return dict(status='REVIEW_SCOPE_LIMIT',production_outcome=diag['status'],
                        direct_physical_bands=direct,exhaustion_confirmed=False)
        assert direct['exhausted']
        return dict(status='EXHAUSTION_CONFIRMED',direct_physical_bands=direct)
    assert diag['status']=='PARENT_WITNESS'
    w=diag['witness'];rec=physical(P,Q,w['point'],w['torus_laps'],z)
    check_emitted(rec,w)
    if direct['status']=='REVIEW_SCOPE_LIMIT':
        return dict(status='WITNESS_CONFIRMED_BAND_REVIEW_CAPPED',recovered=rec,
                    direct_physical_bands=direct)
    assert not direct['exhausted']
    t=F(rec['time'])
    memberships=[j for j,band in enumerate(direct['safe_intervals'])
                 if F(band['time_interval'][0])<=t<=F(band['time_interval'][1])]
    assert memberships
    for j in memberships:
        assert direct['safe_intervals'][j]['physical_laps']==rec['physical_laps']
    return dict(status='WITNESS_CONFIRMED',recovered=rec,
                direct_physical_bands=direct,matching_time_intervals=memberships)


def review_stage(path):
    stage=json.loads(path.read_text());z=F(stage['threshold'])
    cert=stage['certificate'];controls=stage.get('controls')
    if controls is None:
        assert stage['primary_status']=='NO_PRIMARY_GUARANTEE'
        return {'status':'PRESERVED_EARLY_STOP','stage_file':path.name,
                'certificate_status':cert['status'],'physical_conclusion':None}
    candidates=cert.get('candidates',[]);byid={c['id']:c for c in candidates}
    assert len(byid)==len(candidates)
    if 'rows' in cert:
        assert tuple(map(tuple,cert['rows']))==ROWS and F(cert['threshold'])==z
    menu=[byid[cid] for cid in cert.get('chosen_ids',[])]
    full=cert['status']=='COMPLETE_COVER_CERTIFICATE'
    primary_complete=stage['primary_status']=='PRIMARY_COMPLETE'
    assert not full or primary_complete
    if primary_complete and not full:
        assert cert['status']=='UNCOVERED_PRIMITIVE_PAIRS'
        assert not any(primary(*pair) for pair in cert['uncovered'])
    endpoint_bands=[]
    for c in candidates:
        assert len(c['labels'])==9
        phases=[[a*F(x)+b*F(y)-m for (a,b),m in zip(ROWS,c['labels'])]
                for x,y in c['endpoints']]
        assert all(z<=f<=1-z for row in phases for f in row)
        endpoint_bands.append(encode({'id':c['id'],'phases':phases}))
    records=[];misses=[];endpoint_checks=[]
    for p,q in CONTROLS:
        d=gcd(p,q);P,Q=p//d,q//d
        selected=menu if full or (primary_complete and primary(p,q)) else candidates
        hit=first_contact(selected,P,Q)
        if hit is not None:
            candidate,selection,tests=hit
            rec=physical(p,q,selection['point'],candidate['labels'],z)
            rec.update(segment=candidate['id'],segment_tests=tests,
                contact_source='menu' if selected is menu else 'candidates')
            records.append(rec)
        else:
            misses.append(dict(pair=[p,q],primary=primary(p,q)))
        boundary=dict(pair=[p,q],primary=primary(p,q),menu_full_complete=full,
                      menu_primary_complete=primary_complete)
        for name,seq in [('all_candidates',candidates),('chosen_menu',menu)]:
            closed=[c['id'] for c in seq if contact(P,Q,c['endpoints']) is not None]
            opened=[c['id'] for c in seq if contact(P,Q,c['endpoints'],True) is not None]
            boundary[name]=dict(closed_hit=bool(closed),open_hit=bool(opened),
                closed_candidate_ids=closed,open_candidate_ids=opened,
                loses_all_contacts=bool(closed) and not opened)
        endpoint_checks.append(boundary)
    assert misses==controls['misses']
    assert [r['pair'] for r in records]==[w['pair'] for w in controls['witnesses']]
    for rec,emitted in zip(records,controls['witnesses']):
        assert rec['pair']==emitted['pair']
        check_emitted(rec,emitted,byid[rec['segment']])
    assert len(controls['endpoint_checks'])==22
    for got,expected in zip(endpoint_checks,controls['endpoint_checks']):
        assert got['pair']==expected['pair'] and got['primary']==expected['primary']
        for name in ('all_candidates','chosen_menu'):
            assert got[name]['closed_hit']==expected[name]['closed_hit']
            assert got[name]['open_hit']==expected[name]['open_hit']
    bypair={tuple(rec['pair']):rec for rec in records};normalization=[]
    for scaled,primitive in [((4,6),(2,3)),((6,10),(3,5)),((2,2),(1,1)),((4,2),(2,1)),((2,40),(1,20))]:
        if scaled not in bypair:
            assert primitive not in bypair
            normalization.append(dict(scaled=scaled,primitive=primitive,status='BOTH_MISSED'))
            continue
        large,small=bypair[scaled],bypair[primitive]
        for key in ('point','h','coordinate_laps','primitive_time','phases','physical_laps','distinct_speeds','distinct_speed_count'):
            assert large[key]==small[key]
        assert F(large['time'])*large['gcd']==F(small['time'])
        assert large['speeds']==[large['gcd']*v for v in small['speeds']]
        normalization.append(dict(scaled=scaled,primitive=primitive,status='PASS'))
    assert sum(primary(p,q) for p,q in CONTROLS)==18
    diag=diagnostic_review(stage)
    n=len(records)
    return encode(dict(status='PASS',stage_file=path.name,stage_sha256=digest(path),threshold=z,
        certificate_status=cert['status'],primary_status=stage['primary_status'],
        records=records,misses=misses,endpoint_band_checks=endpoint_bands,
        endpoint_contact_checks=endpoint_checks,normalization_controls=normalization,
        diagnostic=diag,counts=dict(parameter_controls=22,primary_controls=18,auxiliary_controls=4,
        physical_witnesses=n,primary_witnesses=sum(r['distinct_speeds'] for r in records),
        selected_phase_checks=9*n,selected_lap_checks=9*n,reflected_phase_checks=9*n,
        reflected_lap_checks=9*n,alternate_bezout_recoveries=2*n,
        candidate_endpoint_band_checks=18*len(candidates))))


def motivation_review():
    raw=json.loads((HERE/'motivation.json').read_text())
    assert raw['pair']==[1,20] and raw['status']=='REPRODUCED_SELECTOR_FAILURE'
    source=ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json'
    old=json.loads(source.read_text())['certificate']
    byid={c['id']:c for c in old['candidates']}
    menu=[byid[cid] for cid in old['chosen_ids']]
    candidate,hit,tests=first_contact(menu,1,20)
    x,y=map(F,hit['point']);h=hit['h'];t=x
    assert (x,y,t)==(F(7,24),F(5,6),F(7,24))
    assert 20*t==y+h
    speeds=[a+20*b for a,b in ROWS]
    phases=[phase(v*t) for v in speeds]
    laps=[floor(v*t) for v in speeds]
    labels=list(candidate['labels'])+[floor(38*x+18*y)]
    assert phases==[a*x+b*y-m for (a,b),m in zip(ROWS,labels)]
    assert laps==[m+b*h for (a,b),m in zip(ROWS,labels)]
    assert all(F(1,8)<=f<=F(7,8) for f in phases[:-1])
    assert phases[-1]==F(1,12) and speeds[-1]==398
    old_w=raw['old_menu_witness']
    expected=encode(dict(pair=[1,20],primitive=[1,20],gcd=1,point=[x,y],h=h,
        primitive_time=t,time=t,speeds=speeds[:-1],torus_laps=labels[:-1],
        phases=phases[:-1],physical_laps=laps[:-1],minimum=F(1,8),
        segment=candidate['id'],segment_tests=tests,distinct_speeds=True))
    for key,value in expected.items(): assert old_w[key]==value,(key,value,old_w[key])
    assert old_w['contact']==dict(interval=hit['interval'],first_integer=h,hit=True,
                                 parameter=hit['parameter'],point=hit['point'])
    r,ss=old_w['bezout'];T=r*x+ss*y
    assert r+20*ss==1 and F(old_w['unwrapped_clock'])==T
    assert old_w['N']==floor(T) and phase(T)==t and old_w['euclid_divisions']==2
    assert raw['new_speeds']==speeds and raw['phases']==list(map(str,phases))
    assert raw['physical_laps']==laps
    minimum=min(min(f,1-f) for f in phases)
    assert raw['minimum']==str(minimum)== '1/12'
    assert raw['fails_thresholds']==['1/8','1/10'] and minimum<F(1,10)<F(1,8)
    assert raw['distinct_speed_count']==len(set([0]+speeds))==10
    archive_path=ROOT/'reviews/2026-09-29-cc-row38-range/controls.json'
    archive=json.loads(archive_path.read_text())['old_only']['new_failure']
    assert archive['pair']==[1,20] and archive['time']==str(t) and archive['point']==list(map(str,[x,y]))
    indices=list(range(6))+[8]
    for key,values in [('speeds',speeds),('phases',list(map(str,phases))),('physical_laps',laps),('torus_laps',labels)]:
        assert archive[key]==[values[i] for i in indices]
    assert raw['archived_failure_fields_match'] is True
    return encode(dict(status='PASS',motivation_sha256=digest(HERE/'motivation.json'),
        pair=[1,20],old_selected_time=t,old_selected_point=[x,y],new_speeds=speeds,
        phases=phases,physical_laps=laps,torus_laps=labels,minimum=minimum,
        fails_thresholds=raw['fails_thresholds'],distinct_speed_count=10,
        archived_failure_fields_match=True,
        scope='The single declared prior-selector failure, evaluated by direct products; no physical nonexistence conclusion.'))


def main():
    assert digest(HERE/'PROTOCOL.md')==PROTOCOL_SHA
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    assert inputs['protocol_sha256']==PROTOCOL_SHA
    for name,identity in inputs['files'].items():
        raw=(ROOT/name).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==identity['sha256']
        blob=b'blob '+str(len(raw)).encode()+b'\0'+raw
        assert hashlib.sha1(blob).hexdigest()==identity['git_blob_sha']
    summary=json.loads((HERE/'summary.json').read_text())
    motivation=motivation_review()
    stages=[review_stage(HERE/'stage8.json')]
    if summary['stage10']['status']=='NOT_TRIGGERED':
        assert stages[0]['primary_status']=='PRIMARY_COMPLETE'
        assert not (HERE/'stage10.json').exists()
        stage10={'status':'NOT_TRIGGERED','reason':'Stage A already supplies primary safety at 1/8, hence 1/10.'}
    else:
        assert stages[0]['primary_status']=='NO_PRIMARY_GUARANTEE'
        stages.append(review_stage(HERE/'stage10.json'))
        stage10={'status':'REVIEWED'}
    repairs=[]
    for stage in stages:
        records={tuple(r['pair']):r for r in stage.get('records',[])}
        rec=records.get((1,20))
        repairs.append(dict(stage_file=stage['stage_file'],pair=[1,20],repaired=rec is not None,
            time=rec.get('time') if rec else None,minimum=rec.get('minimum') if rec else None,
            new_row_phase=rec['phases'][-1] if rec else None))
    out=dict(status='PASS',review_type='Separate internal AI physical review; no production imports.',
        protocol_sha256=PROTOCOL_SHA,inputs_sha256=digest(HERE/'INPUTS.json'),
        reviewer_sha256=digest(Path(__file__)),summary_sha256=digest(HERE/'summary.json'),
        method='Coordinate-lap congruence, direct physical speed products, exact closed/open contacts; conditional physical time-band intersection.',
        stages=stages,stage10=stage10,motivation=motivation,repair_comparison=repairs,
        limits='Frozen controls only. Infinite coverage is a separate proof-candidate argument. Conditional paths not triggered provide no execution evidence. No external human/formal review, general portability or novelty claim.')
    print(json.dumps(encode(out),indent=2,sort_keys=True))


if __name__=='__main__': main()
