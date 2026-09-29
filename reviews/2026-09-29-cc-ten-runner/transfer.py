#!/usr/bin/env python3
"""Frozen three-added-row transfer; exact arithmetic and explicit domain adapter."""
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from itertools import product
from math import ceil, floor, gcd, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2))
ADDED = ((6,2),(3,8),(38,18))
ROWS = CORE + ADDED
PAIRS = ((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
         (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10),
         (2,2),(4,2),(1,20),(2,40))


def encode(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [encode(x) for x in v]
    return v


def save(name,v):
    (HERE/name).write_text(json.dumps(encode(v),indent=2,sort_keys=True)+'\n')


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def verify_inputs():
    data=json.loads((HERE/'INPUTS.json').read_text())
    assert digest(HERE/'PROTOCOL.md')==data['protocol_sha256']
    for path,item in data['files'].items(): assert digest(ROOT/path)==item['sha256'],path
    return data


def primary(p,q): return p!=q and p!=2*q


def key(s): return s['parent'],*s['edge'],*s['added_laps']


def dot(row,point): return sum(a*x for a,x in zip(row,point))


def lap_range(row,z):
    a,b=row
    return range(ceil((a+b)*z-(1-z)),floor(F(a,2)+b*(1-z)-z)+1)


def bands(rows,labels,z):
    return [(a,b,m+1-z) for (a,b),m in zip(rows,labels)]+[(-a,-b,-m-z) for (a,b),m in zip(rows,labels)]


def hull(points):
    points=sorted(set(points))
    if len(points)<=2: return points
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower=[];upper=[]
    for p in points:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0: lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0: upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]


def clip_polygon(poly,a,b,c):
    if not poly: return []
    out=[]
    for i,p in enumerate(poly):
        q=poly[(i+1)%len(poly)];vp=a*p[0]+b*p[1]-c;vq=a*q[0]+b*q[1]-c
        if vp<=0: out.append(p)
        if (vp<0<vq) or (vq<0<vp):
            t=vp/(vp-vq);out.append(tuple(x+t*(y-x) for x,y in zip(p,q)))
    return hull(out)


def regenerate(z):
    ranges=[range(1),range(1)]+[lap_range(row,z) for row in CORE[2:]]
    count=prod(map(len,ranges))
    if count>1024: return {'status':'LABEL_SCOPE_LIMIT','label_tuples':count,'parents':[]}
    parents=[]
    for labels in product(*ranges):
        constraints=bands(CORE,labels,z)+[(1,0,F(1,2))]
        poly=[(z,z),(F(1,2),z),(F(1,2),1-z),(z,1-z)]
        for a,b,c in constraints: poly=clip_polygon(poly,a,b,c)
        if not poly: continue
        vertices=sorted(poly);index={v:i for i,v in enumerate(vertices)}
        edges=sorted({tuple(sorted((index[p],index[poly[(i+1)%len(poly)]]))) for i,p in enumerate(poly)})
        parents.append({'labels':labels,'vertices':[(x,y,z) for x,y in vertices],
                        'edges':edges,'constraints':[['band',[a,b,0],c] for a,b,c in constraints]})
    return {'status':'PASS','threshold':z,'rows':CORE,'label_tuples':count,'parents':parents}


def candidates(data,z):
    jobs=[]
    for pi,parent in enumerate(data['parents']):
        vs=[tuple(map(F,v)) for v in parent['vertices']]
        for i,j in sorted(parent['edges']):
            if vs[i][2]!=z or vs[j][2]!=z: continue
            a,b=vs[i][:2],vs[j][:2];ranges=[]
            for row in ADDED:
                vals=[dot(row,p) for p in (a,b)]
                ranges.append(range(ceil(min(vals)-(1-z)),floor(max(vals)-z)+1))
            jobs.append((pi,parent,i,j,a,b,ranges))
    attempts=sum(prod(map(len,j[-1])) for j in jobs)
    counts={'floor_edges':len(jobs),'edge_lap_triple_attempts':attempts,'budget':2048}
    if attempts>2048: return [],dict(counts,status='CLIPPING_SCOPE_LIMIT',enumerated=0)
    out=[]
    for pi,parent,i,j,a,b,ranges in jobs:
        for laps in product(*ranges):
            lo,hi=F(0),F(1)
            for row,m in zip(ADDED,laps):
                sa,sb=dot(row,a),dot(row,b);ds=sb-sa
                if ds:
                    u,v=sorted(((m+z-sa)/ds,(m+1-z-sa)/ds));lo=max(lo,u);hi=min(hi,v)
                elif not m+z<=sa<=m+1-z: lo,hi=F(1),F(0)
            if lo>hi: continue
            endpoints=sorted(tuple(x+t*(y-x) for x,y in zip(a,b)) for t in (lo,hi))
            k,l,m=laps
            out.append({'id':f'P{pi}:E{i}-{j}:K{k}:L{l}:M{m}','parent':pi,'edge':(i,j),
                        'seventh_lap':k,'eighth_lap':l,'ninth_lap':m,'added_laps':laps,'labels':tuple(parent['labels'])+laps,
                        'endpoints':endpoints,'source_parameters':(lo,hi)})
    return sorted(out,key=key),dict(counts,status='PASS',candidate_records=len(out),
                                   point_records=sum(s['endpoints'][0]==s['endpoints'][1] for s in out))


def recover(api,record,hit,p,q,z):
    d=gcd(p,q);P,Q=p//d,q//d;x,y=hit['point'];h=hit['first_integer']
    r,s,steps=api.bezout(P,Q);T=r*x+s*y;N=floor(T);tau=T-N;t=tau/d
    speeds=[a*p+b*q for a,b in ROWS]
    phases=[a*x+b*y-m for (a,b),m in zip(ROWS,record['labels'])]
    laps=[m+(-a*s+b*r)*h-(a*P+b*Q)*N for (a,b),m in zip(ROWS,record['labels'])]
    assert 0<t<F(1,d) and all(z<=f<=1-z for f in phases)
    assert all(v*t==ell+f for v,ell,f in zip(speeds,laps,phases))
    cardinality=len(set([0]+speeds));assert (cardinality==10)==primary(p,q)
    reflected_laps=[floor(v*(1-t)) for v in speeds]
    reflected_phases=[v*(1-t)-ell for v,ell in zip(speeds,reflected_laps)]
    assert reflected_laps==[v-1-ell for v,ell in zip(speeds,laps)]
    assert reflected_phases==[1-f for f in phases]
    alt=(r+Q)*x+(s-P)*y;assert alt-floor(alt)==tau
    return dict(pair=[p,q],primitive=[P,Q],gcd=d,distinct_speeds=primary(p,q),
                distinct_speed_count=cardinality,segment=record['id'],contact=hit,
                point=[x,y],h=h,torus_laps=record['labels'],bezout=[r,s],euclid_divisions=steps,
                unwrapped_clock=T,N=N,primitive_time=tau,time=t,speeds=speeds,phases=phases,
                physical_laps=laps,minimum=min(min(f,1-f) for f in phases),
                reflected_time=1-t,reflected_laps=reflected_laps,reflected_phases=reflected_phases,
                alternate_bezout_time=(alt-floor(alt))/d)


def controls(api,prior,cert,z,primary_complete):
    records=cert.get('candidates',[]);byid={s['id']:s for s in records}
    menu=[byid[x] for x in cert.get('chosen_ids',[])]
    full=cert['status']=='COMPLETE_COVER_CERTIFICATE'
    witnesses=[];misses=[];endpoints=[]
    for p,q in PAIRS:
        d=gcd(p,q);P,Q=p//d,q//d
        chosen=menu if full or (primary_complete and primary(p,q)) else records
        for s in chosen:
            hit=api.contact(s,P,Q)
            if hit['hit']:
                witnesses.append(recover(api,s,hit,p,q,z));break
        else: misses.append({'pair':[p,q],'primary':primary(p,q)})
        item={'pair':[p,q],'primary':primary(p,q)}
        for name,seq in [('all_candidates',records),('chosen_menu',menu)]:
            item[name]={'closed_hit':any(prior.first_contact(s,P,Q) is not None for s in seq),
                        'open_hit':any(prior.first_contact(s,P,Q,opened=True) is not None for s in seq)}
        endpoints.append(item)
    return dict(witnesses=witnesses,misses=misses,endpoint_checks=endpoints)


def diagnostic(api,data,cert,z):
    missed=[tuple(p) for p in cert.get('uncovered',[]) if primary(*p)]
    if cert['status']!='UNCOVERED_PRIMITIVE_PAIRS' or not missed:
        return {'status':'NOT_TRIGGERED'}
    P,Q=min(missed);ranges=[lap_range(row,z) for row in ADDED]
    hs=range(ceil(Q*z-P*(1-z)),floor(F(Q,2)-P*z)+1)
    attempts=len(data['parents'])*prod(map(len,ranges))*len(hs)
    result={'pair':[P,Q],'threshold':z,'preflight_tuples':attempts,'budget':100000}
    if attempts>100000: return dict(result,status='DIAGNOSTIC_SCOPE_LIMIT',enumerated=0)
    trace=[]
    for pi,parent in enumerate(data['parents']):
        constraints=[(F(n[0]),F(n[1]),F(rhs)-F(n[2])*z) for _,n,rhs in parent['constraints']]
        for laps in product(*ranges):
            all_constraints=constraints+bands(ADDED,laps,z)
            for h in hs:
                lo,hi=z,F(1,2);possible=True
                for a,b,c in all_constraints:
                    slope=a+b*F(Q,P);rhs=c+b*F(h,P)
                    if slope>0: hi=min(hi,rhs/slope)
                    elif slope<0: lo=max(lo,rhs/slope)
                    elif rhs<0: possible=False
                good=possible and lo<=hi
                trace.append({'parent':pi,'added_laps':laps,'h':h,'interval':[lo,hi],
                              'constant_constraints_pass':possible,'nonempty':good})
                if good:
                    x=(lo+hi)/2;y=(Q*x-h)/P
                    assert all(a*x+b*y<=c for a,b,c in all_constraints)
                    s={'id':f'FULL:P{pi}:K{laps[0]}:L{laps[1]}:M{laps[2]}:H{h}',
                       'labels':tuple(parent['labels'])+laps}
                    hit={'hit':True,'point':[x,y],'first_integer':h}
                    w=recover(api,s,hit,P,Q,z)
                    edge_members=[]
                    for ei,(i,j) in enumerate(parent['edges']):
                        a,b=[tuple(map(F,parent['vertices'][k])) for k in (i,j)]
                        if a[2]!=z or b[2]!=z: continue
                        dx,dy=b[0]-a[0],b[1]-a[1]
                        if (x-a[0])*dy==(y-a[1])*dx and min(a[0],b[0])<=x<=max(a[0],b[0]) and min(a[1],b[1])<=y<=max(a[1],b[1]):
                            edge_members.append([i,j])
                    return dict(result,status='PARENT_WITNESS',trace=trace,enumerated=len(trace),
                                witness=w,source_floor_edge_membership=edge_members)
    return dict(result,status='EXHAUSTED_FOR_PAIR',trace=trace,enumerated=len(trace))


def regress(api,prior,data):
    old=load('pinned_nine_engine','reviews/2026-09-29-cc-nine-runner/transfer.py')
    api.key=old.key
    got=old.run_stage(api,prior,data,F(1,8))
    archived=json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())
    assert encode(got)==archived
    return {'status':'PASS','scope':'Entire archived nine-runner stage8 record, including20 controls.',
            'all_stage_fields_exact':True,'archived_sha256':digest(ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json')}


def motivation(api):
    old=json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())
    w=api.select(old['certificate'],1,20)
    t=w['time'];speeds=[a+20*b for a,b in ROWS]
    laps=[floor(v*t) for v in speeds];phases=[v*t-ell for v,ell in zip(speeds,laps)]
    assert t==F(7,24) and speeds[-1]==398 and phases[-1]==F(1,12)
    assert len(set([0]+speeds))==10
    assert all(F(1,8)<=f<=F(7,8) for f in phases[:-1])
    archived=json.loads((ROOT/'reviews/2026-09-29-cc-row38-range/controls.json').read_text())
    failure=archived['old_only']['new_failure']
    assert failure['pair']==[1,20] and F(failure['time'])==t
    assert list(map(F,failure['phases']))==phases[:6]+phases[-1:]
    assert failure['physical_laps']==laps[:6]+laps[-1:]
    assert failure['speeds']==speeds[:6]+speeds[-1:]
    return {'status':'REPRODUCED_SELECTOR_FAILURE','pair':[1,20],'old_menu_witness':w,
            'new_speeds':speeds,'physical_laps':laps,'phases':phases,'minimum':min(min(f,1-f) for f in phases),
            'fails_thresholds':[F(1,8),F(1,10)],'distinct_speed_count':10,'archived_failure_fields_match':True,
            'scope':'Failure of one prior selected time; no nonexistence or candidate-class exhaustion.'}


def run_stage(api,prior,data,z):
    rec,count=candidates(data,z)
    if count['status']=='PASS':
        cert=api.compile_records(rec,rows=ROWS,threshold=z,budget=400)
        cert['domain']='positive integer p,q; ten distinct speeds iff p!=q and p!=2q; full labelled compilation includes auxiliaries'
    else: cert={'status':count['status'],'candidates':[]}
    complete=cert['status']=='COMPLETE_COVER_CERTIFICATE'
    primary_complete=complete or (cert['status']=='UNCOVERED_PRIMITIVE_PAIRS' and not any(primary(*p) for p in cert['uncovered']))
    result={'threshold':z,'geometry':data,'clipping':count,'certificate':cert,
            'primary_status':'PRIMARY_COMPLETE' if primary_complete else 'NO_PRIMARY_GUARANTEE',
            'controls':controls(api,prior,cert,z,primary_complete),
            'diagnostic':diagnostic(api,data,cert,z)}
    return result


def main():
    inputs=verify_inputs()
    api=load('ten_imported_compiler','reviews/2026-09-29-cc-coverage-compiler/compiler.py')
    prior=load('ten_imported_transfer','reviews/2026-09-29-cc-coefficient-transfer/transfer.py')
    data=json.loads((ROOT/'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json').read_text())
    save('regression.json',regress(api,prior,data))
    save('motivation.json',motivation(api))
    api.key=key
    a=run_stage(api,prior,data,F(1,8));save('stage8.json',a)
    summary={'protocol_sha256':inputs['protocol_sha256'],'stage8':{'status':a['certificate']['status'],
             'primary_status':a['primary_status'],'counts':a['certificate'].get('counts'),
             'diagnostic_status':a['diagnostic']['status']}}
    if a['primary_status']!='PRIMARY_COMPLETE':
        geometry=regenerate(F(1,10))
        if geometry['status']=='PASS': b=run_stage(api,prior,geometry,F(1,10))
        else: b={'threshold':F(1,10),'geometry':geometry,'certificate':{'status':geometry['status']},'primary_status':'NO_PRIMARY_GUARANTEE'}
        save('stage10.json',b)
        summary['stage10']={'status':b['certificate']['status'],'primary_status':b['primary_status'],
                           'counts':b['certificate'].get('counts'),'diagnostic_status':b.get('diagnostic',{}).get('status')}
    else: summary['stage10']={'status':'NOT_TRIGGERED','reason':'Stage A primary guarantee already implies 1/10 safety.'}
    save('summary.json',summary);print(json.dumps(encode(summary),sort_keys=True))


if __name__=='__main__': main()
