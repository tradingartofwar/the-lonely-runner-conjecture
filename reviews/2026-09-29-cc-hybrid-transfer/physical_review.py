#!/usr/bin/env python3
"""Independent physical audit of the data-bound (102,50) hybrid transfer.
Reuses only hash-pinned independent reviewer primitives, never production code.
"""
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path
import hashlib
import importlib.util
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
TARGET=(102,50)
ROWS=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),TARGET)
CONTROLS=((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
    (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10),
    (2,2),(4,2),(1,20),(2,40),(5,1),(10,2))
PROTOCOL_SHA='a9ad5edbf140ee15bffc2ad4cf2a47de5c9884c7875172cc33f3a2a37f077f3d'
REVIEWER='reviews/2026-09-29-cc-hybrid-recovery/physical_review.py'


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)): return [encode(v) for v in value]
    return value


def source_query(source,P,Q,opened=False):
    """Intersect new safe parameter bands with an exact orbit point or line."""
    A,B=[tuple(map(F,p)) for p in source['endpoints']]
    if opened and A==B: return None
    Ha,Hb=Q*A[0]-P*A[1],Q*B[0]-P*B[1]
    Ra,Rb=[sum(a*b for a,b in zip(TARGET,p)) for p in (A,B)]
    for h in range(ceil(min(Ha,Hb)),floor(max(Ha,Hb))+1):
        orbit=(F(0),F(1)) if Ha==Hb else ((h-Ha)/(Hb-Ha),)*2
        for m in range(ceil(min(Ra,Rb)-F(7,8)),floor(max(Ra,Rb)-F(1,8))+1):
            if Ra==Rb:
                if not m+F(1,8)<=Ra<=m+F(7,8): continue
                lo,hi=orbit
            else:
                lower,upper=sorted(((m+F(1,8)-Ra)/(Rb-Ra),(m+F(7,8)-Ra)/(Rb-Ra)))
                lo,hi=max(F(0),orbit[0],lower),min(F(1),orbit[1],upper)
            if lo>hi: continue
            if opened:
                if lo==hi:
                    if not 0<lo<1: continue
                    s=lo
                else: s=lo if lo>0 else (lo+hi)/2
                if not 0<s<1: continue
            else: s=lo
            point=[a+s*(b-a) for a,b in zip(A,B)]
            raw=sum(a*b for a,b in zip(TARGET,point))
            assert Q*point[0]-P*point[1]==h and F(1,8)<=raw-m<=F(7,8)
            return encode(dict(point=point,h=h,ninth_lap=m,parameter=s))
    return None


def recover_sources(sources,pair,opened=False):
    visits=[]
    for source in sources:
        hit=source_query(source,*pair,opened)
        visits.append(dict(source_id=source['id'],hit=hit is not None))
        if hit is None: continue
        lo,hi=map(F,source['source_parameters']);s=F(hit['parameter'])
        return dict(pair=list(pair),source_id=source['id'],parent=source['parent'],edge=source['edge'],
            point=hit['point'],h=hit['h'],labels=source['labels']+[hit['ninth_lap']],
            ninth_lap=hit['ninth_lap'],local_parameter=hit['parameter'],
            original_parameter=str(lo+s*(hi-lo)),
            source_endpoint=source['endpoints'][0]==source['endpoints'][1] or s in (0,1)),visits
    return None,visits


def membership(exception,sources,parents,full):
    source=next(s for s in sources if s['id']==exception['source_id'])
    s=F(exception['local_parameter']);original=F(exception['original_parameter'])
    point=tuple(map(F,exception['point']));A,B=[tuple(map(F,p)) for p in source['endpoints']]
    assert point==tuple(a+s*(b-a) for a,b in zip(A,B))
    lo,hi=map(F,source['source_parameters']);assert original==lo+s*(hi-lo)
    assert (A==B or s in (0,1))==exception['source_endpoint']
    assert exception['labels'][:-1]==source['labels']
    i,j=source['edge'];parent=parents[source['parent']]
    C,D=[tuple(map(F,parent['vertices'][v][:2])) for v in (i,j)]
    assert point==tuple(a+original*(b-a) for a,b in zip(C,D))
    raw=sum(a*b for a,b in zip(TARGET,point))
    assert floor(raw)==exception['ninth_lap'] and F(1,8)<=raw-floor(raw)<=F(7,8)
    cid=source['id']+':M'+str(exception['ninth_lap'])
    candidate=next(c for c in full if c['id']==cid)
    assert candidate['labels']==exception['labels'] and R.on_segment(point,candidate['endpoints']) is not None
    a,b=map(F,candidate['source_parameters']);assert a<=original<=b
    return dict(pair=exception['pair'],candidate_id=cid,original_parameter=str(original),
                full_parameter_interval=candidate['source_parameters'],labels_equal=True)


def full_select(certificate,p,q):
    d=gcd(p,q);P,Q=p//d,q//d
    byid={c['id']:c for c in certificate['candidates']}
    records=[byid[cid] for cid in certificate['chosen_ids']] if certificate['status']=='COMPLETE_COVER_CERTIFICATE' else certificate['candidates']
    chosen=R.first_contact(records,P,Q)
    if chosen is None: return None
    candidate,hit,tests=chosen
    rec=R.physical(p,q,hit['point'],candidate['labels'],F(1,8))
    rec.update(segment=candidate['id'],segment_tests=tests)
    return rec


def dispatch_membership(record,parents,full):
    cid=record['segment'].removeprefix('EXCEPTION:')
    candidate=next(c for c in full if c['id']==cid)
    assert candidate['labels']==record['torus_laps']
    s=R.on_segment(record['point'],candidate['endpoints']);assert s is not None
    lo,hi=map(F,candidate['source_parameters']);original=lo+s*(hi-lo)
    parent=parents[candidate['parent']];i,j=candidate['edge']
    A,B=[tuple(map(F,parent['vertices'][v][:2])) for v in (i,j)]
    assert tuple(map(F,record['point']))==tuple(a+original*(b-a) for a,b in zip(A,B))
    return dict(pair=record['pair'],full_candidate_id=cid,candidate_parameter=str(s),original_parameter=str(original))


def old_time_review(emitted):
    p,q=5,1;t=F(9,40)
    speeds=[a*p+b*q for a,b in ROWS]
    phases=[v*t-floor(v*t) for v in speeds];laps=[floor(v*t) for v in speeds]
    distances=[min(f,1-f) for f in phases]
    assert speeds[-1]==560 and speeds[-1]*t==126 and phases[-1]==0
    assert all(F(1,8)<=f<=F(7,8) for f in phases[:-1])
    assert len(set([0]+speeds))==10
    reflected_t=1-t
    reflected=[v*reflected_t-floor(v*reflected_t) for v in speeds]
    reflected_laps=[floor(v*reflected_t) for v in speeds]
    assert reflected==[1-f if f else F(0) for f in phases]
    assert reflected_laps==[v-l-int(bool(f)) for v,l,f in zip(speeds,laps,phases)]
    assert reflected[-1]==0 and reflected_laps[-1]==434
    expected=encode(dict(pair=[5,1],new_speed=560,old_time=t,raw=F(126),phase=F(0),safe=False))
    assert emitted==expected
    old=json.loads((ROOT/'reviews/2026-09-29-cc-hybrid-recovery/audit.json').read_text())
    oldw=next(r['witness'] for r in old['physical_controls'] if r['pair']==[5,1])
    assert F(oldw['time'])==t and oldw['phases'][:-1]==list(map(str,phases[:-1]))
    assert oldw['physical_laps'][:-1]==laps[:-1]
    return encode(dict(status='PASS',pair=[5,1],old_time=t,speeds=speeds,phases=phases,
        distances=distances,physical_laps=laps,minimum=min(distances),failed_runner_indices=[9],
        reflected_time=reflected_t,reflected_phases=reflected,reflected_laps=reflected_laps,
        scope='Failure of the prior selected time only. Zero-phase reflection retains phase zero and uses lap v-old_lap.'))


def main():
    global R
    assert digest(HERE/'PROTOCOL.md')==PROTOCOL_SHA
    inputs=json.loads((HERE/'INPUTS.json').read_text());assert inputs['protocol_sha256']==PROTOCOL_SHA
    for name,identity in inputs['files'].items():
        raw=(ROOT/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==identity['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==identity['git_blob_sha']
    spec=importlib.util.spec_from_file_location('pinned_independent_physical_primitives',ROOT/REVIEWER)
    R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
    old_rows=R.ROWS;assert old_rows[-1]==(54,26)
    R.ROWS=ROWS
    assert R.CONTROLS==CONTROLS
    hybrid=json.loads((HERE/'hybrid.json').read_text());full_wrapper=json.loads((HERE/'full.json').read_text())
    fullcert=full_wrapper['certificate'];full=fullcert['candidates'];full_byid={c['id']:c for c in full}
    audit=json.loads((HERE/'audit.json').read_text());summary=json.loads((HERE/'summary.json').read_text())
    sources=json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())['certificate']['candidates']
    sources.sort(key=lambda s:(s['parent'],*s['edge'],s['seventh_lap'],s['eighth_lap']))
    parents=json.loads((ROOT/'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json').read_text())['parents']
    completeness=R.check_conditional_completeness(hybrid)
    assert full_wrapper['clipping']['status']=='PASS' and fullcert['status']=='COMPLETE_COVER_CERTIFICATE'
    for candidate in hybrid['screen_certificate']['candidates']: assert candidate==full_byid[candidate['id']]
    closed=[];closed_visits=[];members=[]
    for pair in completeness['exception_pairs']:
        record,visits=recover_sources(sources,pair)
        assert record is not None
        closed.append(record);closed_visits.append(dict(pair=pair,visits=visits))
        members.append(membership(record,sources,parents,full))
    assert closed==hybrid['recovery']['exceptions']==summary['recovered']
    assert members==audit['exception_membership']
    assert sum(len(r['visits']) for r in closed_visits)==hybrid['recovery']['counts']['source_visits']
    old_failure=old_time_review(audit['old_time_failure'])
    assert summary['old_time_failure']==audit['old_time_failure']
    reloaded=json.loads(json.dumps(hybrid));full_reloaded=json.loads(json.dumps(fullcert))
    assert isinstance(reloaded['recovery']['exceptions'][0]['point'][0],str)
    controls=[];memberships=[];differences=[]
    assert [r['pair'] for r in audit['controls']]==list(map(list,CONTROLS))
    for pair,emitted in zip(CONTROLS,audit['controls']):
        rec=R.select_loaded(hybrid,*pair);after=R.select_loaded(reloaded,*pair)
        assert rec==after and emitted['hybrid']['status']=='HIT'
        R.compare_dispatch(rec,dict(pair=list(pair),**emitted['hybrid']),hybrid)
        baseline=full_select(fullcert,*pair)
        assert baseline==full_select(full_reloaded,*pair) and emitted['full']['status']=='HIT'
        R.check_emitted(baseline,emitted['full']['witness'],full_byid[baseline['segment']])
        assert emitted['primary']==R.primary(*pair)
        controls.append(dict(pair=list(pair),primary=R.primary(*pair),hybrid=rec,full=baseline))
        if rec['witness']['time']!=baseline['time']:
            differences.append(dict(pair=list(pair),hybrid_time=rec['witness']['time'],full_time=baseline['time']))
        for method,record in [('hybrid',rec['witness']),('full',baseline)]:
            memberships.append(dict(scope='control',method=method,**dispatch_membership(record,parents,full)))
    union=sorted(set(map(tuple,hybrid['screen_certificate']['residual_pairs']))|set(map(tuple,fullcert['residual_pairs'])))
    assert len(union)<=800 and list(map(list,union))==audit['union_pairs']
    assert audit['comparison_scope']=='ALL_POSITIVE_PRIMITIVE_DIRECTIONS' and not audit['coverage_mismatches']
    union_records=[];contact_tests=0
    assert [row['pair'] for row in audit['comparison']]==list(map(list,union))
    for pair,emitted in zip(union,audit['comparison']):
        rec=R.select_loaded(hybrid,*pair);assert rec==R.select_loaded(reloaded,*pair)
        R.compare_dispatch(rec,dict(pair=list(pair),**emitted['hybrid']),hybrid)
        ids=[c['id'] for c in full if R.contact(*pair,c['endpoints']) is not None]
        contact_tests+=len(full)
        assert ids==emitted['full_contact_ids'] and bool(ids)==emitted['full_class_hit']
        assert emitted['coverage_equal'] and emitted['primary']==R.primary(*pair)
        union_records.append(dict(pair=list(pair),hybrid=rec,full_contact_ids=ids))
        memberships.append(dict(scope='union',method='hybrid',**dispatch_membership(rec['witness'],parents,full)))
    normalization=[];by_pair={tuple(r['pair']):r for r in controls}
    for scaled,primitive in [((4,6),(2,3)),((6,10),(3,5)),((2,2),(1,1)),((4,2),(2,1)),((2,40),(1,20)),((10,2),(5,1))]:
        for method in ('hybrid','full'):
            large,small=by_pair[scaled][method],by_pair[primitive][method]
            if method=='hybrid':
                assert large['route']==small['route'];large,small=large['witness'],small['witness']
            for key in ('point','h','coordinate_laps','primitive_time','phases','physical_laps','distinct_speeds','distinct_speed_count'):
                assert large[key]==small[key]
            assert F(large['time'])*large['gcd']==F(small['time'])
            assert large['speeds']==[large['gcd']*v for v in small['speeds']]
            normalization.append(dict(method=method,scaled=scaled,primitive=primitive,status='PASS'))
    opened=[];open_visits=[];open_physical=[];open_members=[]
    for pair in completeness['exception_pairs']:
        record,visits=recover_sources(sources,pair,True)
        assert record is not None and not record['source_endpoint']
        opened.append(record);open_visits.append(dict(pair=pair,visits=visits))
        open_members.append(membership(record,sources,parents,full))
        open_physical.append(R.physical(*pair,record['point'],record['labels'],F(1,8)))
    assert opened==audit['open_source_diagnostic']['exceptions']
    assert audit['open_source_diagnostic']['status']=='COMPLETE_EXCEPTION_RECOVERY'
    assert not audit['open_source_diagnostic']['uncovered']
    assert sum(len(r['visits']) for r in open_visits)==audit['open_source_diagnostic']['counts']['source_visits']
    retention=[dict(pair=c['pair'],closed_source=c['source_id'],closed_point=c['point'],
        closed_source_endpoint=c['source_endpoint'],open_source=o['source_id'],open_point=o['point'],
        open_local_parameter=o['local_parameter'],same_point=c['point']==o['point']) for c,o in zip(closed,opened)]
    assert len(controls)==24 and sum(row['primary'] for row in controls)==20
    assert len(union_records)==47 and sum(R.primary(*pair) for pair in union)==45
    out=dict(status='PASS',review_type='Internal AI physical review; inherited independent primitives, no production imports.',
        inputs=dict(protocol_sha256=PROTOCOL_SHA,inputs_sha256=digest(HERE/'INPUTS.json'),
            independent_primitive_path=REVIEWER,independent_primitive_sha256=digest(ROOT/REVIEWER),
            reviewer_sha256=digest(Path(__file__)),hybrid_sha256=digest(HERE/'hybrid.json'),
            full_sha256=digest(HERE/'full.json'),audit_sha256=digest(HERE/'audit.json')),
        adaptation=dict(reused_independent_binding='ROWS',old_rows=old_rows,new_rows=ROWS,
            local_source_query_target=TARGET,production_imports=[]),
        conditional_completeness=completeness,closed_source_queries=closed_visits,
        exception_membership=members,old_time_failure=old_failure,controls=controls,
        union_dispatch=union_records,dispatch_membership=memberships,
        hybrid_full_time_differences=differences,normalization_controls=normalization,
        open_source_queries=open_visits,open_source_exceptions=opened,open_source_physical=open_physical,
        open_source_membership=open_members,endpoint_retention=retention,
        counts=dict(physical_controls_per_method=24,primary_controls_per_method=20,
            auxiliary_controls_per_method=4,hybrid_union_dispatches=47,primary_union_dispatches=45,
            control_phase_checks_per_method=216,control_lap_checks_per_method=216,
            control_reflected_phase_checks_per_method=216,control_reflected_lap_checks_per_method=216,
            control_alternative_bezout_recoveries_per_method=48,
            union_phase_checks=423,union_lap_checks=423,union_reflected_phase_checks=423,
            union_reflected_lap_checks=423,union_alternative_bezout_recoveries=94,
            hybrid_json_roundtrip_dispatches=71,full_json_roundtrip_dispatches=24,
            full_candidate_dispatch_memberships=len(memberships),full_union_contact_tests=contact_tests,
            screen_endpoint_band_checks=90,old_time_phase_checks=9,old_time_lap_checks=9,
            old_time_reflected_phase_checks=9,old_time_reflected_lap_checks=9,
            open_source_physical_records=3,open_source_phase_checks=27,open_source_lap_checks=27,
            open_source_reflected_phase_checks=27,open_source_reflected_lap_checks=27,
            open_source_alternative_bezout_recoveries=6),
        scope='The same24 controls for each method,47 frozen union directions and3 open-source exceptions; old-time failure separately scoped. No new target or benchmark.',
        limits='This reuse is not blind independence. Generic kernel regression, production body-identity and timing are reviewed separately. Universal coverage remains an internally reviewed proof candidate.')
    print(json.dumps(encode(out),indent=2,sort_keys=True))


if __name__=='__main__': main()
