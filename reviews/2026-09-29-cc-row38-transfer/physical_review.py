#!/usr/bin/env python3
"""Frozen row (3,8) physical review using coordinate laps.
Adapted from the prior separate physical checker; no compiler/selector imports.
Exactly the protocol control pairs, with a conditional one-pair diagnostic only.
"""
from fractions import Fraction as F
from math import gcd, floor, ceil
from pathlib import Path
import json
import hashlib

HERE = Path(__file__).resolve().parent
ROWS = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(3,8)]
CONTROLS = [(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
            (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10)]


def phase(t):
    return t - floor(t)


def physical_from_coordinates(p, q, xy, labels):
    """Use coordinate-lap congruence, not a Bezout clock, as primary recovery."""
    d = gcd(p,q)
    P, Q = p//d, q//d
    x,y = map(F,xy)
    assert 0 <= x < 1 and 0 <= y < 1
    h = Q*x-P*y
    assert h.denominator == 1
    h = int(h)
    # Q*i+h=P*j, i=floor(P*tau), j=floor(Q*tau).
    i = (-h * pow(Q,-1,P)) % P if P > 1 else 0
    j = (Q*i+h)//P
    assert P*j == Q*i+h
    tau = (x+i)/P
    assert 0 <= tau < 1 and Q*tau == y+j
    assert floor(P*tau) == i and floor(Q*tau) == j
    t = tau/d
    speeds = [a*p+b*q for a,b in ROWS]
    direct = [phase(v*t) for v in speeds]
    laps = [floor(v*t) for v in speeds]
    torus_phases = [a*x+b*y-m for (a,b),m in zip(ROWS,labels)]
    coordinate_laps = [m+a*i+b*j for (a,b),m in zip(ROWS,labels)]
    assert direct == torus_phases
    assert laps == coordinate_laps
    assert all(F(1,8) <= f <= F(7,8) for f in direct)
    assert (len(set([0]+speeds)) == 8) == (p != q)
    minimum = min(min(f,1-f) for f in direct)
    reflected_time = 1-t
    reflected = [phase(v*reflected_time) for v in speeds]
    reflected_laps = [floor(v*reflected_time) for v in speeds]
    assert reflected == [1-f for f in direct]
    assert reflected_laps == [v-1-l for v,l in zip(speeds,laps)]
    # A second derivation, using an inverse modulo Q, supplies Bezout choices.
    r = pow(P,-1,Q) if Q>1 else 0
    s = (1-r*P)//Q
    assert r*P+s*Q == 1
    alternative = []
    for k in [-1,1]:
        rr, ss = r+k*Q,s-k*P
        T=rr*x+ss*y
        N=floor(T)
        assert phase(T)==tau
        alternate_laps = [m+(-a*ss+b*rr)*h-(a*P+b*Q)*N
                          for (a,b),m in zip(ROWS,labels)]
        assert alternate_laps == laps
        alternative.append({'shift':k,'r':rr,'s':ss,'T':str(T),'N':N,
                            'primitive_time':str(phase(T)),
                            'physical_laps':alternate_laps})
    return {'p':p,'q':q,'gcd':d,'primitive':[P,Q],
            'distinct_speeds':len(set([0]+speeds))==8,
            'point':[str(x),str(y)],'h':h,'coordinate_laps':[i,j],
            'primitive_time':str(tau),'time':str(t),'speeds':speeds,
            'torus_laps':labels,'phases':list(map(str,direct)),
            'physical_laps':laps,'minimum':str(minimum),
            'reflected_time':str(reflected_time),
            'reflected_phases':list(map(str,reflected)),
            'reflected_laps':reflected_laps,'alternative_bezout':alternative}


def contact_on_segment(P,Q,endpoints,open_endpoints=False):
    """Recover contact directly from a rational segment, including point cases."""
    A,B = [tuple(map(F,pt)) for pt in endpoints]
    ha,hb = Q*A[0]-P*A[1],Q*B[0]-P*B[1]
    lo,hi = min(ha,hb),max(ha,hb)
    if A==B and open_endpoints:
        return None
    if ha==hb:
        if ha.denominator != 1:
            return None
        return [(A[k]+B[k])/2 for k in range(2)] if open_endpoints else list(A)
    h=floor(lo)+1 if open_endpoints else ceil(lo)
    if (h>=hi if open_endpoints else h>hi):
        return None
    u=(h-ha)/(hb-ha)
    assert 0 < u < 1 if open_endpoints else 0 <= u <= 1
    return [A[k]+u*(B[k]-A[k]) for k in range(2)]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()



def first_contact(records,P,Q,opened=False):
    for tests,c in enumerate(records,1):
        xy=contact_on_segment(P,Q,c['endpoints'],opened)
        if xy is not None:
            return c,xy,tests
    return None


def check_candidate_endpoints(c):
    assert len(c['labels'])==len(ROWS)
    phases=[[a*F(pt[0])+b*F(pt[1])-m
             for (a,b),m in zip(ROWS,c['labels'])] for pt in c['endpoints']]
    assert all(F(1,8)<=f<=F(7,8) for fs in phases for f in fs)
    return {'id':c['id'],'endpoint_phases':[list(map(str,fs)) for fs in phases],
            'constant_extremal_rows':[i+1 for i in range(7)
             if phases[0][i]==phases[1][i] and phases[0][i] in (F(1,8),F(7,8))]}


def check_emitted(rec,emitted):
    fields=['gcd','primitive','distinct_speeds','point','h','primitive_time',
            'time','speeds','torus_laps','phases','physical_laps','minimum',
            'reflected_time','reflected_phases','reflected_laps']
    for key in fields:
        assert rec[key]==emitted[key],(key,rec[key],emitted[key])
    P,Q=rec['primitive'];x,y=map(F,rec['point'])
    r,s=emitted['bezout']
    assert r*P+s*Q==1
    assert F(emitted['unwrapped_clock'])==r*x+s*y
    assert emitted['N']==floor(r*x+s*y)
    assert F(emitted['alternate_bezout_time'])==F(rec['time'])


def check_emitted_contact(rec, candidate, emitted):
    endpoints=[tuple(map(F,point)) for point in candidate['endpoints']]
    P,Q=rec['primitive'];x,y=map(F,rec['point'])
    projected=[Q*a-P*b for a,b in endpoints]
    low,high=sorted(projected)
    parameter=F(0) if projected[0]==projected[1] else (F(rec['h'])-projected[0])/(projected[1]-projected[0])
    assert emitted['contact']=={'interval':[str(low),str(high)],
        'first_integer':ceil(low),'hit':True,'parameter':str(parameter),
        'point':[str(x),str(y)]}
    assert ceil(low)<=high and rec['h']==ceil(low)
    a,b=P,Q;divisions=0
    while b:
        a,b=b,a%b
        divisions+=1
    assert emitted['euclid_divisions']==divisions


def diagnostic_review(cert,emitted):
    """Frozen one-pair diagnostic only when complete candidate class misses it."""
    assert cert['status']=='UNCOVERED_PRIMITIVE_PAIRS'
    pairs=sorted(map(tuple,cert['uncovered']))
    selected=next((p for p in pairs if p[0]!=p[1]),pairs[0])
    P,Q=selected
    assert all(contact_on_segment(P,Q,c['endpoints']) is None for c in cert['candidates'])
    parent_path=HERE.parent/'2026-09-29-cc-segment-discovery/PARENT_INPUT.json'
    data=json.loads(parent_path.read_text())
    hs=list(range(ceil(F(Q,8)-F(7*P,8)),floor(F(Q,2)-F(P,8))+1))
    full_bound=len(data['parents'])*8*len(hs)
    if full_bound>10000:
        assert emitted['status']=='DIAGNOSTIC_SCOPE_LIMIT'
        return {'status':'SCOPE_LIMIT','pair':list(selected),'full_bound':full_bound}
    found=None;sections=0;examined=[]
    for number,parent in enumerate(data['parents']):
        for m in range(1,9):
            for h in hs:
                sections+=1
                # Direct constraints in x after y=(Q*x-h)/P.
                lo,hi=F(1,8),F(1,2)
                inequalities=[]
                for name,raw,bound in parent['constraints']:
                    a,b,c=map(F,raw)
                    inequalities.append((a+b*F(Q,P),F(bound)-c*F(1,8)+b*F(h,P)))
                inequalities.extend([(F(3)+F(8*Q,P),F(m)+F(7,8)+F(8*h,P)),
                                     (-F(3)-F(8*Q,P),-F(m)-F(1,8)-F(8*h,P))])
                impossible=False
                for a,bound in inequalities:
                    if a>0: hi=min(hi,bound/a)
                    elif a<0: lo=max(lo,bound/a)
                    elif bound<0: impossible=True
                section={'parent':number,'seventh_lap':m,'H':h,
                         'x_interval':[str(lo),str(hi)],'nonempty':not impossible and lo<=hi}
                examined.append(section)
                assert section == emitted['sections'][sections-1]
                if not impossible and lo<=hi:
                    x=(lo+hi)/2;y=(Q*x-h)/P
                    found=(number,m,h,lo,hi,x,y,parent['labels']+[m]);break
            if found:break
        if found:break
    if found is None:
        assert emitted['status']=='NO_WITNESS_IN_RESTORED_INPUT'
        return {'status':'NO_WITNESS_IN_DIAGNOSTIC_SCOPE','pair':list(selected),
                'full_bound':full_bound,'sections':sections,'examined_sections':examined}
    number,m,h,lo,hi,x,y,labels=found
    for _, raw, bound in data['parents'][number]['constraints']:
        assert sum(a*b for a,b in zip(map(F,raw),[x,y,F(1,8)])) <= F(bound)
    rec=physical_from_coordinates(P,Q,[x,y],labels)
    assert emitted['status']=='RESTORED_PARENT_WITNESS'
    assert emitted['pair']==list(selected)
    assert emitted['maximum_sections']==full_bound and emitted['examined']==sections
    last=emitted['sections'][-1]
    assert last['parent']==number and last['seventh_lap']==m and last['H']==h
    assert last['x_interval']==[str(lo),str(hi)]
    check_emitted(rec,emitted['witness'])
    edge_hits=[]
    for pn,parent in enumerate(data['parents']):
        for i,j in parent['edges']:
            A,B=[tuple(map(F,parent['vertices'][v])) for v in (i,j)]
            if A[2]!=F(1,8) or B[2]!=F(1,8):continue
            dx,dy=B[0]-A[0],B[1]-A[1]
            if dx*(y-A[1])!=dy*(x-A[0]):continue
            if min(A[0],B[0])<=x<=max(A[0],B[0]) and min(A[1],B[1])<=y<=max(A[1],B[1]):
                edge_hits.append({'parent':pn,'edge':[i,j]})
    assert edge_hits==emitted['original_floor_edge_memberships']
    return {'status':'WITNESS_FOUND','pair':list(selected),'parent':number,
            'seventh_lap':m,'h':h,'x_interval':[str(lo),str(hi)],
            'full_bound':full_bound,'sections':sections,'examined_sections':examined,
            'original_floor_edge_memberships':edge_hits,
            'recovered':rec,'parent_input_sha256':digest(parent_path)}

def fixed_rule_comparison(comparison, by_pair, complete):
    """Recover the old failure geometrically, without importing the checker."""
    old=comparison['old_decision']
    assert old['status']=='REJECTED' and old['reason']=='BOUNDED_DIRECTION'
    assert old['row']==[3,8] and old['delta']==-13 and old['B_mod8']==0
    assert old['threshold']=='1/8'
    # Endpoint raw values 30/8 and 17/8 cannot share a closed safe lap band.
    assert 30//8 != 17//8 and (3+2*8)%8 != 0
    expected_attempts=[]
    for P,Q in [(1,2),(1,3),(2,1),(1,4)]:
        ends=[(F(1,4),F(3,8)),(F(3,8),F(1,8))]
        xy=contact_on_segment(P,Q,ends)
        if xy is None:
            assert (P,Q)==(1,2)
            xy=[F(1,8),F(1,4)]
        f=phase(3*xy[0]+8*xy[1])
        expected_attempts.append({'pair':[P,Q],'seventh_phase':str(f)})
    assert old['construction']=={'absolute_delta':13,'left_phase':'3/4',
        'attempts':expected_attempts,'contact_tests':4}
    assert all(F(1,8)<=F(a['seventh_phase'])<=F(7,8) for a in expected_attempts[:-1])
    assert F(expected_attempts[-1]['seventh_phase'])>F(7,8)
    p,q=1,4
    x,y=contact_on_segment(p,q,[(F(1,4),F(3,8)),(F(3,8),F(1,8))])
    h=q*x-p*y
    # P=1 means the first coordinate fixes tau directly.
    i=0;j=int(h);t=x
    assert (x,y,t)==(F(5,16),F(1,4),F(5,16)) and q*t==y+j
    speeds=[a*p+b*q for a,b in ROWS]
    phases=[phase(v*t) for v in speeds]
    physical_laps=[floor(v*t) for v in speeds]
    torus_laps=[floor(a*x+b*y) for a,b in ROWS]
    assert physical_laps==[m+a*i+b*j for (a,b),m in zip(ROWS,torus_laps)]
    distances=[min(f,1-f) for f in phases]
    expected={'pair':[p,q],'row':[3,8],'gcd':1,'primitive':[p,q],
        'point':[str(x),str(y)],'h':int(h),'M':q+2*p,
        'rho':int(8*(q+2*p)*(x-F(1,4))),'role':'L',
        'primitive_time':str(t),'time':str(t),'speeds':speeds,
        'torus_laps':torus_laps,'physical_laps':physical_laps,
        'phases':list(map(str,phases)),'distances':list(map(str,distances)),
        'minimum':str(min(distances)),'core_safe':True,'seventh_safe':False,
        'failed_runner_indices':[7],'distinct_speeds':len(set([0]+speeds))==8,
        'repeated_initial_speeds':False,'seventh_core_collisions':[],
        'reflected_time':str(1-t),
        'reflected_phases':[str(phase(v*(1-t))) for v in speeds],
        'reflected_laps':[floor(v*(1-t)) for v in speeds]}
    assert all(F(1,8)<=f<=F(7,8) for f in phases[:6]) and distances[-1]==F(1,16)
    emitted=old['counterexample']
    for key,value in expected.items():
        assert emitted[key]==value,(key,emitted[key],value)
    r,ss=emitted['bezout'];N=emitted['N']
    assert r*p+ss*q==1 and N==floor(r*x+ss*y) and phase(r*x+ss*y)==t
    domain={'empty':False,'identically_repeated_core_row':None,
        'conditions':{'p_not_equal_q':True,'nonzero_linear_forms':[
            {'core_row':[a,b],'p_coefficient':3-a,'q_coefficient':8-b} for a,b in ROWS[2:6]]}}
    assert old['distinct_speed_domain']==domain
    repaired=by_pair[(1,4)].get('status') != 'NO_CANDIDATE_CONTACT'
    assert comparison['repaired_at_pair']==repaired
    assert comparison['uniform_compiler_repair']==complete
    if repaired:
        new=by_pair[(1,4)]
        check_emitted(new,comparison['new_witness_at_known_failure'])
        assert new['segment']==comparison['new_witness_at_known_failure']['segment']
    else:
        assert comparison['new_witness_at_known_failure'] is None
    return {'status':'PASS','old_fixed_rule_failure':expected,
        'old_construction_attempts':expected_attempts,
        'new_time':by_pair[(1,4)].get('time'),
        'new_minimum':by_pair[(1,4)].get('minimum'),
        'repaired_at_pair':repaired,'complete_certificate_emitted':complete,
        'scope':'Direct check of the one predeclared old failure and its corresponding new control. Uniform coverage is reviewed separately.'}


def main():
    assert digest(HERE/'PROTOCOL.md') == '0f1ac5c22a2921077d66339512dc63bb299d79b1fe937cc1c40c6951e7cd1c70'
    cert=json.loads((HERE/'certificate.json').read_text())
    run=json.loads((HERE/'run.json').read_text())
    assert cert['status'] in ('COMPLETE_COVER_CERTIFICATE','UNCOVERED_PRIMITIVE_PAIRS',
        'NO_DESCENDING_SEGMENT','SCOPE_LIMIT','INVALID_CANDIDATE','INPUT_SCOPE_MISMATCH','CLIPPING_SCOPE_LIMIT')
    if 'rows' in cert:
        assert list(map(tuple,cert['rows']))==ROWS and F(cert['threshold'])==F(1,8)
    assert run['certificate_sha256']==digest(HERE/'certificate.json')
    candidates=cert.get('candidates',[])
    if not candidates:
        assert cert['status'] not in ('COMPLETE_COVER_CERTIFICATE','UNCOVERED_PRIMITIVE_PAIRS')
        print(json.dumps({'status':'PASS','certificate_status':cert['status'],
            'physical_outcome':'NOT_EVALUATED_NO_VALIDATED_CANDIDATES',
            'physical_conclusion':None,'conditional_diagnostic':'NOT_TRIGGERED',
            'scope':'Preserved early stop; no statement of absent physical witnesses.'},indent=2,sort_keys=True))
        return
    by_id={c['id']:c for c in candidates}
    assert len(by_id)==len(candidates)
    menu=[by_id[cid] for cid in cert.get('chosen_ids',[])] if cert['status']=='COMPLETE_COVER_CERTIFICATE' else []
    endpoint_checks=[check_candidate_endpoints(c) for c in candidates]
    records=[];boundary=[]
    for p,q in CONTROLS:
        d=gcd(p,q);P,Q=p//d,q//d
        candidate_ids=[c['id'] for c in candidates if contact_on_segment(P,Q,c['endpoints']) is not None]
        opened_ids=[c['id'] for c in candidates if contact_on_segment(P,Q,c['endpoints'],True) is not None]
        closed_menu=[c['id'] for c in menu if c['id'] in candidate_ids]
        opened_menu=[c['id'] for c in menu if c['id'] in opened_ids]
        chosen=first_contact(menu,P,Q)
        # Complete certificates use menu; failure checks use first actual candidate.
        source='menu' if cert['status']=='COMPLETE_COVER_CERTIFICATE' else 'candidates'
        if source=='candidates':chosen=first_contact(candidates,P,Q)
        if chosen:
            c,xy,tests=chosen
            rec=physical_from_coordinates(p,q,xy,c['labels'])
            rec.update(segment=c['id'],contact_source=source,segment_tests=tests)
        else:
            rec={'p':p,'q':q,'primitive':[P,Q],'gcd':d,'distinct_speeds':p!=q,
                 'status':'NO_CANDIDATE_CONTACT','contact_source':source}
        rec['closed_candidate_ids']=candidate_ids
        records.append(rec)
        boundary.append({'pair':[p,q],'closed_candidate_ids':candidate_ids,'open_candidate_ids':opened_ids,
                         'closed_menu_ids':closed_menu,'open_menu_ids':opened_menu,
                         'loses_all_candidate_contacts':bool(candidate_ids) and not opened_ids,
                         'menu_completeness':cert['status']=='COMPLETE_COVER_CERTIFICATE',
                         'loses_all_menu_contacts':bool(closed_menu) and not opened_menu})
    by_pair={(r['p'],r['q']):r for r in records}
    normalization=[]
    for scaled,primitive in [((4,6),(2,3)),((6,10),(3,5))]:
        large,small=by_pair[scaled],by_pair[primitive]
        if large.get('status')=='NO_CANDIDATE_CONTACT':
            assert small.get('status')=='NO_CANDIDATE_CONTACT'
            normalization.append({'scaled':list(scaled),'primitive':list(primitive),'status':'BOTH_NO_CANDIDATE_CONTACT'})
            continue
        for key in ['point','h','coordinate_laps','primitive_time','phases','physical_laps']:
            assert large[key]==small[key]
        assert F(large['time'])*large['gcd']==F(small['time'])
        assert large['speeds']==[large['gcd']*v for v in small['speeds']]
        normalization.append({'scaled':list(scaled),'primitive':list(primitive),'status':'PASS'})
    diag=None
    if cert['status']=='UNCOVERED_PRIMITIVE_PAIRS':
        # No diagnostic is run for a successful certificate.
        diag=diagnostic_review(cert,run['diagnostic'])
    actual=[r for r in records if 'time' in r]
    assert [list((r['p'],r['q'])) for r in actual]==[w['pair'] for w in run['controls']]
    assert [list((r['p'],r['q'])) for r in records if 'time' not in r]==run['uncovered_controls']
    for rec,emitted in zip(actual,run['controls']):
        check_emitted(rec,emitted)
        check_emitted_contact(rec,by_id[rec['segment']],emitted)
        assert rec['segment']==emitted['segment'] and rec['segment_tests']==emitted['segment_tests']
    for independent,emitted in zip(boundary,run['endpoint_checks']):
        assert independent['pair']==emitted['pair']
        for field,target in [('candidate','all_candidates'),('menu','chosen_menu')]:
            if field=='menu' and cert['status']!='COMPLETE_COVER_CERTIFICATE':
                assert emitted[target] is None
                continue
            opened=independent['open_'+field+'_ids']
            closed=independent['closed_'+field+'_ids']
            assert bool(opened)==emitted[target]['open_hit']
            assert bool(closed)==emitted[target]['closed_hit']
            assert (opened[0] if opened else None)==emitted[target]['first_open_candidate']
            assert (closed[0] if closed else None)==emitted[target]['first_closed_candidate']
    assert sum(r['distinct_speeds'] for r in records)==17
    if cert['status'] != 'UNCOVERED_PRIMITIVE_PAIRS':
        assert run['diagnostic']['status']=='NOT_TRIGGERED'
    fixed_comparison=fixed_rule_comparison(run['fixed_selector_comparison'],by_pair,
        cert['status']=='COMPLETE_COVER_CERTIFICATE')
    out={'status':'PASS','review_type':'separately structured internal AI physical review',
         'certificate_status':cert['status'],
         'inputs':{'certificate_sha256':digest(HERE/'certificate.json'),
                   'run_sha256':digest(HERE/'run.json'),
                   'protocol_sha256':digest(HERE/'PROTOCOL.md'),
                   'physical_review_py_sha256':digest(Path(__file__))},
         'method':'Coordinate-lap congruence Q*i=-H (mod P), tau=(x+i)/P; direct phases and floors. No production imports.',
         'scope':'The same 18 parameter pairs are new speed configurations under row (3,8), with (1,1) a repeated-speed auxiliary.',
         'candidate_endpoint_checks':endpoint_checks,'records':records,'normalization_controls':normalization,
         'endpoint_opening_controls':boundary,'conditional_diagnostic':diag,
         'fixed_selector_comparison':fixed_comparison,
         'counts':{'parameter_pairs':18,'physical_witnesses':len(actual),
                   'selected_phase_checks':7*len(actual),'reflected_phase_checks':7*len(actual),
                   'selected_lap_checks':7*len(actual),'reflected_lap_checks':7*len(actual),
                   'alternative_bezout_recoveries':2*len(actual),
                   'candidate_endpoint_band_checks':14*len(candidates),
                   'conditional_diagnostic_pairs':int(diag is not None)},
         'limits':'Finite physical controls and affine candidate safety do not establish infinite coverage. No external human/formal review, general portability, optimum, new existence or originality claim.'}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
