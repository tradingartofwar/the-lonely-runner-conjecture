#!/usr/bin/env python3
"""Separate physical review. No compiler/selector imports or parameter scans."""
from fractions import Fraction as F
from math import gcd, floor, ceil
from pathlib import Path
import json
import hashlib

HERE = Path(__file__).resolve().parent
ROWS = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2)]
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
    assert min(min(f,1-f) for f in direct) == F(1,8)
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
            'physical_laps':laps,'minimum':'1/8',
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


# Certificate/run adaptation and fixed controls are added after the coordinator
# emits its first frozen run. Primary recovery above has no dependency on it.

def main():
    cert=json.loads((HERE/'certificate.json').read_text())
    run=json.loads((HERE/'run.json').read_text())
    assert cert['status']=='COMPLETE_COVER_CERTIFICATE' and run['status']=='PASS'
    assert list(map(tuple,cert['rows']))==ROWS and F(cert['threshold'])==F(1,8)
    assert run['certificate_sha256']==digest(HERE/'certificate.json')
    assert [tuple(r['pair']) for r in run['controls']]==CONTROLS
    candidates={c['id']:c for c in cert['candidates']}
    assert len(candidates)==len(cert['candidates'])
    menu=[candidates[cid] for cid in cert['chosen_ids']]
    assert len(menu)>0 and len(set(cert['chosen_ids']))==len(menu)
    menu_checks=[]
    for c in menu:
        assert len(c['labels'])==len(ROWS)
        endpoint_phases=[[a*F(pt[0])+b*F(pt[1])-m
                         for (a,b),m in zip(ROWS,c['labels'])]
                        for pt in c['endpoints']]
        assert all(F(1,8)<=f<=F(7,8) for fs in endpoint_phases for f in fs)
        constant_extremal_rows=[i+1 for i in range(len(ROWS))
                               if endpoint_phases[0][i]==endpoint_phases[1][i]
                               and endpoint_phases[0][i] in (F(1,8),F(7,8))]
        assert constant_extremal_rows
        menu_checks.append({'id':c['id'],
                            'endpoint_phases':[list(map(str,fs)) for fs in endpoint_phases],
                            'constant_extremal_rows':constant_extremal_rows})
    records=[]
    comparison_fields=['gcd','primitive','distinct_speeds','point','h','primitive_time',
                       'time','speeds','torus_laps','phases','physical_laps','minimum',
                       'reflected_time','reflected_phases','reflected_laps']
    for (p,q),emitted in zip(CONTROLS,run['controls']):
        d=gcd(p,q)
        P,Q=p//d,q//d
        selected=None
        for tests,c in enumerate(menu,1):
            xy=contact_on_segment(P,Q,c['endpoints'])
            if xy is not None:
                selected=c
                break
        assert selected is not None
        rec=physical_from_coordinates(p,q,xy,selected['labels'])
        rec['segment']=selected['id']
        rec['segment_tests']=tests
        assert emitted['segment']==rec['segment']
        assert emitted['segment_tests']==tests
        for field in comparison_fields:
            assert rec[field]==emitted[field],((p,q),field,rec[field],emitted[field])
        r,s=emitted['bezout']
        x,y=map(F,rec['point'])
        assert r*P+s*Q==1
        assert F(emitted['unwrapped_clock'])==r*x+s*y
        assert emitted['N']==floor(r*x+s*y)
        assert F(emitted['alternate_bezout_time'])==F(rec['time'])
        records.append(rec)
    by_pair={(r['p'],r['q']):r for r in records}
    scaled_checks=[]
    for scaled,primitive in [((4,6),(2,3)),((6,10),(3,5))]:
        large,small=by_pair[scaled],by_pair[primitive]
        d=large['gcd']
        for key in ['point','h','coordinate_laps','primitive_time','phases','physical_laps']:
            assert large[key]==small[key]
        assert F(large['time'])*d==F(small['time'])
        assert large['speeds']==[d*v for v in small['speeds']]
        scaled_checks.append({'original_pair':list(scaled),'primitive_pair':list(primitive),
                              'gcd':d,'primitive_time':small['time'],
                              'physical_time':large['time'],'same_phases_and_laps':True})
    endpoint_loss=[]
    for c in menu:
        closed=contact_on_segment(1,4,c['endpoints'])
        opened=contact_on_segment(1,4,c['endpoints'],open_endpoints=True)
        assert opened is None
        endpoint_loss.append({'id':c['id'],
                              'closed_point':list(map(str,closed)) if closed else None,
                              'open_point':None})
    assert any(row['closed_point'] is not None for row in endpoint_loss)
    assert by_pair[(1,4)]['time']=='1/8'
    assert sum(r['distinct_speeds'] for r in records)==17
    out={'status':'PASS','review_type':'separately structured AI physical review',
         'inputs':{'certificate_sha256':digest(HERE/'certificate.json'),
                   'run_sha256':digest(HERE/'run.json'),
                   'protocol_sha256':digest(HERE/'PROTOCOL.md'),
                   'physical_review_py_sha256':digest(Path(__file__))},
         'scope':'Exactly 18 archived pairs: 17 distinct-speed configurations and one repeated-speed auxiliary.',
         'method':'Coordinate-lap congruence Q*i = -h (mod P), tau=(x+i)/P; direct physical phases and floors. No compiler or selector imports.',
         'menu_endpoint_checks':menu_checks,'records':records,'normalization_controls':scaled_checks,
         'endpoint_loss_pair':[1,4],'endpoint_loss':endpoint_loss,
         'counts':{'physical_pairs':len(records),'selected_phase_checks':7*len(records),
                   'reflected_phase_checks':7*len(records),'selected_lap_checks':7*len(records),
                   'reflected_lap_checks':7*len(records),'alternative_bezout_recoveries':2*len(records),
                   'menu_endpoint_band_checks':14*len(menu),'new_parameter_pairs':0},
         'limits':'Finite physical controls and affine menu safety do not replace the separate infinite coverage argument. No external/human/formal verification, no new existence domain or originality claim.'}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
