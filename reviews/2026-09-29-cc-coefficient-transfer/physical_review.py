#!/usr/bin/env python3
"""Changed-row physical review using coordinate laps.
Adapted from the prior separate physical checker; no compiler/selector imports.
Exactly the protocol control pairs, with a conditional one-pair diagnostic only.
"""
from fractions import Fraction as F
from math import gcd, floor, ceil
from pathlib import Path
import json
import hashlib

HERE = Path(__file__).resolve().parent
ROWS = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2)]
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
            'distinct_speeds':len(set(speeds))==7,
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
    full_bound=len(data['parents'])*4*len(hs)
    if full_bound>10000:
        assert emitted['status']=='DIAGNOSTIC_SCOPE_LIMIT'
        return {'status':'SCOPE_LIMIT','pair':list(selected),'full_bound':full_bound}
    found=None;sections=0
    for number,parent in enumerate(data['parents']):
        for m in range(1,5):
            for h in hs:
                sections+=1
                # Direct constraints in x after y=(Q*x-h)/P.
                lo,hi=F(1,8),F(1,2)
                inequalities=[]
                for name,raw,bound in parent['constraints']:
                    a,b,c=map(F,raw)
                    inequalities.append((a+b*F(Q,P),F(bound)-c*F(1,8)+b*F(h,P)))
                inequalities.extend([(F(6)+F(2*Q,P),F(m)+F(7,8)+F(2*h,P)),
                                     (-F(6)-F(2*Q,P),-F(m)-F(1,8)-F(2*h,P))])
                impossible=False
                for a,bound in inequalities:
                    if a>0: hi=min(hi,bound/a)
                    elif a<0: lo=max(lo,bound/a)
                    elif bound<0: impossible=True
                if not impossible and lo<=hi:
                    x=(lo+hi)/2;y=(Q*x-h)/P
                    found=(number,m,h,lo,hi,x,y,parent['labels']+[m]);break
            if found:break
        if found:break
    if found is None:
        assert emitted['status']=='NO_WITNESS_IN_RESTORED_INPUT'
        return {'status':'NO_WITNESS_IN_DIAGNOSTIC_SCOPE','pair':list(selected),
                'full_bound':full_bound,'sections':sections}
    number,m,h,lo,hi,x,y,labels=found
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
            'full_bound':full_bound,'sections':sections,'original_floor_edge_memberships':edge_hits,
            'recovered':rec,'parent_input_sha256':digest(parent_path)}

def main():
    cert=json.loads((HERE/'certificate.json').read_text())
    run=json.loads((HERE/'run.json').read_text())
    assert list(map(tuple,cert['rows']))==ROWS and F(cert['threshold'])==F(1,8)
    assert run['certificate_sha256']==digest(HERE/'certificate.json')
    assert cert['status'] in ('COMPLETE_COVER_CERTIFICATE','UNCOVERED_PRIMITIVE_PAIRS')
    candidates=cert['candidates'];by_id={c['id']:c for c in candidates}
    assert len(by_id)==len(candidates)
    menu=[by_id[cid] for cid in cert['chosen_ids']]
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
        assert rec['segment']==emitted['segment'] and rec['segment_tests']==emitted['segment_tests']
    for independent,emitted in zip(boundary,run['endpoint_checks']):
        assert independent['pair']==emitted['pair']
        field='menu' if cert['status']=='COMPLETE_COVER_CERTIFICATE' else 'candidate'
        opened=independent['open_'+field+'_ids']
        closed=independent['closed_'+field+'_ids']
        assert bool(opened)==emitted['open_hit'] and bool(closed)==emitted['closed_hit']
        assert (opened[0] if opened else None)==emitted['open_candidate']
    assert sum(r['distinct_speeds'] for r in records)==17
    out={'status':'PASS','review_type':'separately structured internal AI physical review',
         'certificate_status':cert['status'],
         'inputs':{'certificate_sha256':digest(HERE/'certificate.json'),
                   'run_sha256':digest(HERE/'run.json'),
                   'protocol_sha256':digest(HERE/'PROTOCOL.md'),
                   'physical_review_py_sha256':digest(Path(__file__))},
         'method':'Coordinate-lap congruence Q*i=-H (mod P), tau=(x+i)/P; direct phases and floors. No production imports.',
         'scope':'The same18parameterpairs are new speed configurations under row(6,2), with(1,1) repeated-speed auxiliary.',
         'candidate_endpoint_checks':endpoint_checks,'records':records,'normalization_controls':normalization,
         'endpoint_opening_controls':boundary,'conditional_diagnostic':diag,
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
