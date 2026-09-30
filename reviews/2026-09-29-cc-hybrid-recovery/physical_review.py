#!/usr/bin/env python3
"""Independent physical review of the frozen contact-first hybrid recovery.
No production imports. Exact coordinate-lap recovery and direct time bands.
"""
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ROWS=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),(54,26))
CONTROLS=((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
          (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10),
          (2,2),(4,2),(1,20),(2,40),(5,1),(10,2))
PROTOCOL_SHA='eb3a894b8d2c411b177ef26f3916a0138adad975f9848a590aaaf1ee11723ccf'


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


def on_segment(point,endpoints):
    X=tuple(map(F,point));A,B=[tuple(map(F,p)) for p in endpoints]
    if A==B: return F(0) if X==A else None
    axis=next(i for i in (0,1) if B[i]!=A[i])
    s=(X[axis]-A[axis])/(B[axis]-A[axis])
    return s if 0<=s<=1 and all(X[i]==A[i]+s*(B[i]-A[i]) for i in (0,1)) else None


def source_query(source,P,Q,opened=False):
    """Intersect safe parameter bands with an exact orbit point/line.

    This uses explicit new-row band intervals, not the production point-phase
    query. Only the three frozen exception directions call this routine.
    """
    A,B=[tuple(map(F,p)) for p in source['endpoints']]
    if opened and A==B: return None
    Ha,Hb=Q*A[0]-P*A[1],Q*B[0]-P*B[1]
    Ra,Rb=54*A[0]+26*A[1],54*B[0]+26*B[1]
    first_h,last_h=ceil(min(Ha,Hb)),floor(max(Ha,Hb))
    first_m,last_m=ceil(min(Ra,Rb)-F(7,8)),floor(max(Ra,Rb)-F(1,8))
    for h in range(first_h,last_h+1):
        if Ha==Hb:
            assert Ha==h
            orbit_lo,orbit_hi=F(0),F(1)
        else:
            orbit_lo=orbit_hi=(h-Ha)/(Hb-Ha)
        for m in range(first_m,last_m+1):
            if Ra==Rb:
                if not m+F(1,8)<=Ra<=m+F(7,8): continue
                lo,hi=orbit_lo,orbit_hi
            else:
                lower,upper=sorted(((m+F(1,8)-Ra)/(Rb-Ra),(m+F(7,8)-Ra)/(Rb-Ra)))
                lo,hi=max(F(0),orbit_lo,lower),min(F(1),orbit_hi,upper)
            if lo>hi: continue
            if opened:
                if lo==hi:
                    if not 0<lo<1: continue
                    s=lo
                else:
                    s=lo if lo>0 else (lo+hi)/2
                    if not 0<s<1: continue
            else: s=lo
            point=[a+s*(b-a) for a,b in zip(A,B)]
            assert Q*point[0]-P*point[1]==h
            assert F(1,8)<=54*point[0]+26*point[1]-m<=F(7,8)
            return encode(dict(point=point,h=h,ninth_lap=m,parameter=s))
    return None


def exception_from_sources(sources,pair,opened=False):
    P,Q=pair;visits=[]
    for source in sources:
        hit=source_query(source,P,Q,opened)
        visits.append(dict(source_id=source['id'],hit=hit is not None))
        if hit is not None:
            a,b=map(F,source['source_parameters']);s=F(hit['parameter'])
            A,B=source['endpoints']
            rec=dict(pair=list(pair),source_id=source['id'],parent=source['parent'],edge=source['edge'],
                point=hit['point'],h=hit['h'],labels=source['labels']+[hit['ninth_lap']],
                ninth_lap=hit['ninth_lap'],local_parameter=hit['parameter'],
                original_parameter=str(a+s*(b-a)),source_endpoint=A==B or s in (0,1))
            return rec,visits
    return None,visits


def source_membership(exception,sources,parents,full_candidates):
    source=next(s for s in sources if s['id']==exception['source_id'])
    s=F(exception['local_parameter']);original=F(exception['original_parameter'])
    point=tuple(map(F,exception['point']));A,B=[tuple(map(F,p)) for p in source['endpoints']]
    assert point==tuple(a+s*(b-a) for a,b in zip(A,B))
    assert 0<=s<=1 and (A==B or s in (0,1))==exception['source_endpoint']
    lo,hi=map(F,source['source_parameters'])
    assert original==lo+s*(hi-lo)
    parent=parents[source['parent']];i,j=source['edge']
    C,D=[tuple(map(F,parent['vertices'][v][:2])) for v in (i,j)]
    assert point==tuple(a+original*(b-a) for a,b in zip(C,D))
    assert exception['labels'][:-1]==source['labels']
    P,Q=exception['pair'];assert Q*point[0]-P*point[1]==exception['h']
    raw=54*point[0]+26*point[1]
    assert floor(raw)==exception['ninth_lap'] and F(1,8)<=phase(raw)<=F(7,8)
    candidate_id=source['id']+':M'+str(exception['ninth_lap'])
    candidate=next(c for c in full_candidates if c['id']==candidate_id)
    assert on_segment(point,candidate['endpoints']) is not None
    assert candidate['labels']==exception['labels']
    c_lo,c_hi=map(F,candidate['source_parameters'])
    assert c_lo<=original<=c_hi
    return dict(pair=exception['pair'],candidate_id=candidate_id,
                full_parameter_interval=candidate['source_parameters'],
                original_parameter=str(original),labels_equal=True)


def select_loaded(hybrid,p,q):
    """Separate selector operating on the emitted JSON string-valued record."""
    d=gcd(p,q);P,Q=p//d,q//d
    exceptions={tuple(e['pair']):e for e in hybrid['recovery']['exceptions']}
    exception=exceptions.get((P,Q))
    if exception is not None:
        rec=physical(p,q,exception['point'],exception['labels'],F(1,8))
        rec.update(segment='EXCEPTION:'+exception['source_id']+':M'+str(exception['ninth_lap']))
        return dict(pair=[p,q],route='EXCEPTION_POINT',source_id=exception['source_id'],witness=rec)
    cert=hybrid['screen_certificate'];byid={s['id']:s for s in cert['candidates']}
    menu=[byid[sid] for sid in cert['chosen_ids']]
    chosen=first_contact(menu,P,Q)
    if chosen is None:
        raise ValueError('No exception dispatch and no screen-menu contact; no witness.')
    candidate,hit,tests=chosen
    rec=physical(p,q,hit['point'],candidate['labels'],F(1,8))
    rec.update(segment=candidate['id'],segment_tests=tests)
    return dict(pair=[p,q],route='SCREEN_MENU',witness=rec)


def compare_dispatch(result,emitted,hybrid):
    assert result['pair']==emitted['pair'] and result['route']==emitted['route']
    rec=result['witness'];w=emitted['witness'];assert rec['pair']==w['pair']
    if result['route']=='EXCEPTION_POINT':
        assert result['source_id']==emitted['source_id']
        exception=next(e for e in hybrid['recovery']['exceptions'] if e['pair']==rec['primitive'])
        check_emitted(rec,w)
        assert rec['segment']==w['segment']
        assert w['contact']==dict(first_integer=exception['h'],hit=True,
            parameter=exception['local_parameter'],point=exception['point'])
    else:
        candidate=next(c for c in hybrid['screen_certificate']['candidates'] if c['id']==rec['segment'])
        check_emitted(rec,w,candidate)


def check_conditional_completeness(hybrid):
    cert=hybrid['screen_certificate'];byid={s['id']:s for s in cert['candidates']}
    lead=byid[cert['leader']['id']]
    (x0,y0),(x1,y1)=[tuple(map(F,p)) for p in lead['endpoints']]
    alpha,beta=x1-x0,y0-y1
    assert alpha>0 and beta>0
    pmax,qmax=ceil(1/beta)-1,ceil(1/alpha)-1
    assert pmax*qmax<=400
    residual=[(P,Q) for P in range(1,pmax+1) for Q in range(1,qmax+1)
              if gcd(P,Q)==1 and alpha*Q+beta*P<1]
    assert list(map(list,residual))==cert['residual_pairs']
    menu=[byid[cid] for cid in cert['chosen_ids']]
    missing=[pair for pair in residual if first_contact(menu,*pair) is None]
    assert list(map(list,missing))==cert['uncovered']
    exceptions=[tuple(e['pair']) for e in hybrid['recovery']['exceptions']]
    assert exceptions==missing
    assert hybrid['status']=='COMPLETE_HYBRID_CERTIFICATE'
    assert hybrid['recovery']['status']=='COMPLETE_EXCEPTION_RECOVERY' and not hybrid['recovery']['uncovered']
    bands=[]
    for c in cert['candidates']:
        phases=[[a*F(x)+b*F(y)-m for (a,b),m in zip(ROWS,c['labels'])]
                for x,y in c['endpoints']]
        assert all(F(1,8)<=f<=F(7,8) for values in phases for f in values)
        bands.append(encode(dict(id=c['id'],phases=phases)))
    return encode(dict(status='PASS',conditional_statement='If supplied candidates and exception points are safe and all listed residual dispatches recover, the positive-width leader covers the remaining directions.',
        alpha=alpha,beta=beta,P_max=pmax,Q_max=qmax,rectangle_pairs=pmax*qmax,
        residual_pairs=list(map(list,residual)),exception_pairs=list(map(list,missing)),
        endpoint_band_checks=bands,universal_status='Internally reviewed proof candidate.'))


def main():
    assert digest(HERE/'PROTOCOL.md')==PROTOCOL_SHA
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    assert inputs['protocol_sha256']==PROTOCOL_SHA
    for name,identity in inputs['files'].items():
        raw=(ROOT/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==identity['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==identity['git_blob_sha']
    review_inputs=json.loads((HERE/'REVIEW_INPUTS.json').read_text())
    assert review_inputs['source_commit']==inputs['source_commit']
    assert set(review_inputs['files'])=={'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json'}
    for name,identity in review_inputs['files'].items():
        raw=(ROOT/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==identity['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==identity['git_blob_sha']
    hybrid=json.loads((HERE/'hybrid.json').read_text());audit=json.loads((HERE/'audit.json').read_text())
    summary=json.loads((HERE/'summary.json').read_text())
    assert summary['protocol_sha256']==PROTOCOL_SHA
    sources=json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())['certificate']['candidates']
    sources.sort(key=lambda s:(s['parent'],*s['edge'],s['seventh_lap'],s['eighth_lap']))
    parents=json.loads((ROOT/'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json').read_text())['parents']
    full_certificate=json.loads((ROOT/'reviews/2026-09-29-cc-phase-screen/full.json').read_text())['certificate']
    full=full_certificate['candidates']
    completeness=check_conditional_completeness(hybrid)
    reconstructed=[];source_queries=[];members=[]
    for pair in completeness['exception_pairs']:
        exception,visits=exception_from_sources(sources,pair)
        reconstructed.append(exception);source_queries.append(dict(pair=pair,visits=visits))
        members.append(source_membership(exception,sources,parents,full))
    assert reconstructed==hybrid['recovery']['exceptions']==summary['recovered']
    assert members==audit['exception_membership']
    assert sum(len(q['visits']) for q in source_queries)==hybrid['recovery']['counts']['source_visits']
    # Loaded strings, then a fresh serialization roundtrip, exercise the same
    # independent selector on every declared physical and residual input.
    reloaded=json.loads(json.dumps(hybrid))
    assert isinstance(reloaded['recovery']['exceptions'][0]['point'][0],str)
    controls=[];residual=[];roundtrips=0
    assert [r['pair'] for r in audit['physical_controls']]==list(map(list,CONTROLS))
    assert [r['pair'] for r in audit['residual_dispatch']]==completeness['residual_pairs']
    for pairs,emitted,output in [(CONTROLS,audit['physical_controls'],controls),
        (completeness['residual_pairs'],audit['residual_dispatch'],residual)]:
        for pair,target in zip(pairs,emitted):
            rec=select_loaded(hybrid,*pair);after=select_loaded(reloaded,*pair)
            assert rec==after;roundtrips+=1
            compare_dispatch(rec,target,hybrid);output.append(rec)
    full_byid={c['id']:c for c in full}
    dispatch_membership=[]
    for scope,records in [('control',controls),('residual',residual)]:
        for result in records:
            rec=result['witness'];cid=rec['segment'].removeprefix('EXCEPTION:')
            candidate=full_byid[cid]
            assert candidate['labels']==rec['torus_laps']
            u=on_segment(rec['point'],candidate['endpoints']);assert u is not None
            lo,hi=map(F,candidate['source_parameters']);original=lo+u*(hi-lo)
            parent=parents[candidate['parent']];i,j=candidate['edge']
            A,B=[tuple(map(F,parent['vertices'][k][:2])) for k in (i,j)]
            assert tuple(map(F,rec['point']))==tuple(a+original*(b-a) for a,b in zip(A,B))
            dispatch_membership.append(dict(scope=scope,pair=rec['pair'],full_candidate_id=cid,
                candidate_parameter=str(u),original_parameter=str(original)))
    bypair={tuple(r['pair']):r for r in controls};normalization=[]
    for scaled,primitive in [((4,6),(2,3)),((6,10),(3,5)),((2,2),(1,1)),((4,2),(2,1)),((2,40),(1,20)),((10,2),(5,1))]:
        large,small=bypair[scaled]['witness'],bypair[primitive]['witness']
        assert bypair[scaled]['route']==bypair[primitive]['route']
        for key in ('point','h','coordinate_laps','primitive_time','phases','physical_laps','distinct_speeds','distinct_speed_count'):
            assert large[key]==small[key]
        assert F(large['time'])*large['gcd']==F(small['time'])
        assert large['speeds']==[large['gcd']*v for v in small['speeds']]
        normalization.append(dict(scaled=scaled,primitive=primitive,status='PASS'))
    opened=[];open_queries=[];open_physical=[];open_members=[]
    for pair in completeness['exception_pairs']:
        exception,visits=exception_from_sources(sources,pair,True)
        assert exception is not None and not exception['source_endpoint']
        opened.append(exception);open_queries.append(dict(pair=pair,visits=visits))
        open_members.append(source_membership(exception,sources,parents,full))
        open_physical.append(physical(*pair,exception['point'],exception['labels'],F(1,8)))
    assert opened==audit['open_source_diagnostic']['exceptions']
    assert audit['open_source_diagnostic']['status']=='COMPLETE_EXCEPTION_RECOVERY'
    assert not audit['open_source_diagnostic']['uncovered']
    assert sum(len(q['visits']) for q in open_queries)==audit['open_source_diagnostic']['counts']['source_visits']
    endpoint_retention=[dict(pair=e['pair'],closed_source=e['source_id'],
        closed_point=e['point'],closed_local_parameter=e['local_parameter'],
        selected_closed_point_is_source_endpoint=e['source_endpoint'],
        open_source=o['source_id'],open_point=o['point'],
        open_local_parameter=o['local_parameter'],same_point=e['point']==o['point'])
        for e,o in zip(reconstructed,opened)]
    baseline=[]
    full_menu=[full_byid[cid] for cid in full_certificate['chosen_ids']]
    for pair in completeness['exception_pairs']:
        candidate,hit,tests=first_contact(full_menu,*pair)
        rec=physical(*pair,hit['point'],candidate['labels'],F(1,8))
        rec.update(segment=candidate['id'],segment_tests=tests)
        old=bypair[tuple(pair)]['witness']
        baseline.append(dict(pair=pair,hybrid_time=old['time'],full_menu_time=rec['time'],
            same_point=old['point']==rec['point'],same_time=old['time']==rec['time'],
            full_menu_physical=rec))
    n=len(controls);r=len(residual)
    assert n==24 and r==47
    assert sum(x['witness']['distinct_speeds'] for x in controls)==20
    assert sum(x['witness']['distinct_speeds'] for x in residual)==45
    out=dict(status='PASS',review_type='Separate internal AI physical review; no production imports.',
        inputs=dict(protocol_sha256=PROTOCOL_SHA,inputs_sha256=digest(HERE/'INPUTS.json'),
            review_inputs_sha256=digest(HERE/'REVIEW_INPUTS.json'),
            hybrid_sha256=digest(HERE/'hybrid.json'),audit_sha256=digest(HERE/'audit.json'),
            reviewer_sha256=digest(Path(__file__))),
        conditional_completeness=completeness,closed_source_queries=source_queries,
        exception_membership=members,physical_controls=controls,residual_dispatch=residual,
        dispatch_full_membership=dispatch_membership,full_menu_exception_comparison=baseline,
        normalization_controls=normalization,open_source_queries=open_queries,
        open_source_exceptions=opened,open_source_physical=open_physical,
        open_source_full_membership=open_members,endpoint_retention=endpoint_retention,
        counts=dict(physical_controls=n,primary_controls=20,auxiliary_controls=4,
            residual_dispatches=r,primary_residual_dispatches=45,auxiliary_residual_dispatches=2,
            control_selected_phase_checks=9*n,control_selected_lap_checks=9*n,
            control_reflected_phase_checks=9*n,control_reflected_lap_checks=9*n,
            control_alternative_bezout_recoveries=2*n,
            residual_selected_phase_checks=9*r,residual_selected_lap_checks=9*r,
            residual_reflected_phase_checks=9*r,residual_reflected_lap_checks=9*r,
            residual_alternative_bezout_recoveries=2*r,
            json_roundtrip_dispatch_checks=roundtrips,screen_endpoint_band_checks=90,
            full_candidate_dispatch_memberships=len(dispatch_membership),
            full_menu_comparison_pairs=3,full_menu_comparison_phase_checks=27,
            full_menu_comparison_lap_checks=27,full_menu_comparison_reflected_phase_checks=27,
            full_menu_comparison_reflected_lap_checks=27,full_menu_comparison_alternative_bezout_recoveries=6,
            open_source_diagnostic_pairs=3,open_source_phase_checks=27,
            open_source_selected_lap_checks=27,open_source_reflected_phase_checks=27,
            open_source_reflected_lap_checks=27,open_source_alternative_bezout_recoveries=6),
        scope='24 fixed controls, the 47 declared residual directions and the three open-source exception diagnostics only; no timing rerun or new parameter scan.',
        limits='Generic kernel synthetic fixtures and production timing are reviewed separately. No external human/formal verification, optimality or arbitrary-family portability claim.')
    print(json.dumps(encode(out),indent=2,sort_keys=True))


if __name__=='__main__': main()
