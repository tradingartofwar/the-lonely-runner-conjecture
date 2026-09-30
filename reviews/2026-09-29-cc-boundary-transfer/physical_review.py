#!/usr/bin/env python3
"""Independent physical audit of the data-bound (78,50) different-boundary transfer.
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
TARGET=(78,50)
ROWS=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),TARGET)
CONTROLS=((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
    (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10),
    (2,2),(4,2),(1,20),(2,40),(5,1),(10,2))
PROTOCOL_SHA='2ea70d567b25185bbd3bf48b4b53fe78d022e0c70fb9dcdc2f8695ebf8f2be0b'
REVIEWER='reviews/2026-09-29-cc-hybrid-recovery/physical_review.py'


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)): return [encode(v) for v in value]
    return value


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
    assert hybrid['screen_certificate']['status']=='COMPLETE_COVER_CERTIFICATE'
    assert completeness['exception_pairs']==[]
    assert hybrid['recovery']['exceptions']==[] and hybrid['recovery']['queries']==[]
    assert hybrid['recovery']['uncovered']==[] and audit['exception_membership']==[]
    for field in ('h_tests','parallel_band_tests','point_phase_tests','source_visits'):
        assert hybrid['recovery']['counts'][field]==0
    assert hybrid['recovery']['preflight']['work_bound']==0
    assert 'old_time_failure' not in audit
    reloaded=json.loads(json.dumps(hybrid));full_reloaded=json.loads(json.dumps(fullcert))
    assert isinstance(reloaded['screen_certificate']['candidates'][0]['endpoints'][0][0],str)
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
    assert audit['comparison_scope']=='ALL_POSITIVE_PRIMITIVE_DIRECTIONS' and not audit['dispatch_coverage_mismatches'] and not audit['screen_class_lost_pairs']
    union_records=[];contact_tests=0;screen_contact_tests=0
    assert [row['pair'] for row in audit['comparison']]==list(map(list,union))
    for pair,emitted in zip(union,audit['comparison']):
        rec=R.select_loaded(hybrid,*pair);assert rec==R.select_loaded(reloaded,*pair)
        R.compare_dispatch(rec,dict(pair=list(pair),**emitted['hybrid']),hybrid)
        ids=[c['id'] for c in full if R.contact(*pair,c['endpoints']) is not None]
        contact_tests+=len(full)
        assert ids==emitted['full_contact_ids'] and bool(ids)==emitted['full_class_hit']
        screened=[c['id'] for c in hybrid['screen_certificate']['candidates'] if R.contact(*pair,c['endpoints']) is not None]
        screen_contact_tests+=len(hybrid['screen_certificate']['candidates'])
        assert screened==emitted['screen_contact_ids'] and bool(screened)==emitted['screen_class_hit']
        assert emitted['dispatch_coverage_equal'] and emitted['primary']==R.primary(*pair)
        union_records.append(dict(pair=list(pair),hybrid=rec,full_contact_ids=ids,screen_contact_ids=screened))
        memberships.append(dict(scope='union',method='hybrid',**dispatch_membership(rec['witness'],parents,full)))
    screen_byid={c['id']:c for c in hybrid['screen_certificate']['candidates']}
    selected=hybrid['screen_certificate']['chosen_ids']
    singleton_ids=[cid for cid in selected if screen_byid[cid]['endpoints'][0]==screen_byid[cid]['endpoints'][1]]
    assert len(selected)==5 and singleton_ids==[selected[-1]]==['P4:E0-1:K3:L5:M54']
    contact_row=next(row for row in union_records if row['pair']==[1,4])
    selected_contacts=[cid for cid in selected if cid in contact_row['screen_contact_ids']]
    assert selected_contacts==singleton_ids
    nondegenerate_contacts=[cid for cid in contact_row['screen_contact_ids']
        if screen_byid[cid]['endpoints'][0]!=screen_byid[cid]['endpoints'][1]]
    assert nondegenerate_contacts==['P7:E0-1:K4:L8:M79']
    assert screen_byid[singleton_ids[0]]['endpoints'][0]==['3/8','1/2']
    singleton_distinction=dict(pair=[1,4],selected_nondegenerate_count=4,selected_singleton_count=1,
        singleton_id=singleton_ids[0],point=screen_byid[singleton_ids[0]]['endpoints'][0],
        selected_menu_contact_ids=selected_contacts,all_screen_contact_ids=contact_row['screen_contact_ids'],
        nondegenerate_screen_contact_ids=nondegenerate_contacts,
        evidence='Uses the contact matrix already independently checked above; no additional contact or parameter scan.',
        conclusion='The singleton is necessary for this selected closed menu at (1,4), but not for the entire screened class or physical existence. No opening of the selected menu was evaluated.')
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
    open_diag=audit['open_source_diagnostic']
    assert open_diag['status']=='COMPLETE_EXCEPTION_RECOVERY'
    for field in ('exceptions','queries','uncovered'): assert open_diag[field]==[]
    for field in ('h_tests','parallel_band_tests','point_phase_tests','source_visits'):
        assert open_diag['counts'][field]==0
    assert open_diag['preflight']['status']=='PASS' and open_diag['preflight']['work_bound']==0
    assert open_diag['preflight']['rows']==[]
    assert audit['zero_budget']['status']=='PASS' and audit['zero_budget']['budget']==0
    assert audit['zero_budget']['work_bound']==0
    assert audit['full_source_diagnostic']=={'status':'NOT_TRIGGERED'}
    vacuity=dict(status='NO_EXCEPTION_DIRECTIONS',raw_open_recovery_status=open_diag['status'],
        physical_diagnostic_records=0,source_queries=0,endpoint_claim=None,
        zero_budget_status='PASS',zero_budget_work=0,
        explanation='Empty input produces a vacuous completion. No source endpoint was tested or removed, and no physical open-source witness was evaluated.')
    assert len(controls)==24 and sum(row['primary'] for row in controls)==20
    assert len(union_records)==28 and sum(R.primary(*pair) for pair in union)==26
    out=dict(status='PASS',review_type='Internal AI physical review; inherited independent primitives, no production imports.',
        inputs=dict(protocol_sha256=PROTOCOL_SHA,inputs_sha256=digest(HERE/'INPUTS.json'),
            independent_primitive_path=REVIEWER,independent_primitive_sha256=digest(ROOT/REVIEWER),
            reviewer_sha256=digest(Path(__file__)),hybrid_sha256=digest(HERE/'hybrid.json'),
            full_sha256=digest(HERE/'full.json'),audit_sha256=digest(HERE/'audit.json')),
        adaptation=dict(reused_independent_binding='ROWS',old_rows=old_rows,new_rows=ROWS,
            source_recovery_exercised=False,production_imports=[]),
        conditional_completeness=completeness,controls=controls,
        union_dispatch=union_records,dispatch_membership=memberships,
        hybrid_full_time_differences=differences,normalization_controls=normalization,
        singleton_menu_distinction=singleton_distinction,
        recovery_diagnostic_vacuity=vacuity,full_source_diagnostic=audit['full_source_diagnostic'],
        menu_comparison=dict(screen_menu=hybrid['screen_certificate']['chosen_ids'],full_menu=fullcert['chosen_ids'],
            same_menu=hybrid['screen_certificate']['chosen_ids']==fullcert['chosen_ids'],
            control_time_differences=differences),
        counts=dict(physical_controls_per_method=24,primary_controls_per_method=20,
            auxiliary_controls_per_method=4,hybrid_union_dispatches=28,primary_union_dispatches=26,
            control_phase_checks_per_method=216,control_lap_checks_per_method=216,
            control_reflected_phase_checks_per_method=216,control_reflected_lap_checks_per_method=216,
            control_alternative_bezout_recoveries_per_method=48,
            union_phase_checks=252,union_lap_checks=252,union_reflected_phase_checks=252,
            union_reflected_lap_checks=252,union_alternative_bezout_recoveries=56,
            hybrid_json_roundtrip_dispatches=52,full_json_roundtrip_dispatches=24,
            full_candidate_dispatch_memberships=len(memberships),full_union_contact_tests=contact_tests,
            screen_endpoint_band_checks=180,screen_union_contact_tests=screen_contact_tests,
            open_source_physical_records=0,exception_dispatch_records=0),
        scope='The same 24 controls for each method and 28 frozen union directions. Empty exception diagnostics perform no source or physical queries. No new target or benchmark.',
        limits='This reuse is not blind independence. Generic kernel regression, production body-identity and timing are reviewed separately. Universal coverage remains an internally reviewed proof candidate.')
    print(json.dumps(encode(out),indent=2,sort_keys=True))


if __name__=='__main__': main()
