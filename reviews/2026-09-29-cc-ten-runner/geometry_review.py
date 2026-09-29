#!/usr/bin/env python3
"""Independent frozen ten-runner geometry audit. No production imports."""
import hashlib
import itertools
import json
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CORE=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2))
ROWS=CORE+((6,2),(3,8),(38,18))
SOURCE=ROOT/'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json'


def encode(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [encode(x) for x in v]
    return v


def need(value,label):
    if not value: raise ArithmeticError(label)


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def primary(p,q): return p!=q and p!=2*q


def restrict(interval,slope,constant,bound):
    lo,hi=interval
    if slope>0: hi=min(hi,(bound-constant)/slope)
    elif slope<0: lo=max(lo,(bound-constant)/slope)
    elif constant>bound: return F(1),F(0)
    return lo,hi


def band_constraints(labels,z,rows=CORE):
    out=[(-F(1),F(0),-z),(F(1),F(0),F(1,2)),
         (F(0),-F(1),-z),(F(0),F(1),1-z)]
    for (a,b),m in zip(rows,labels):
        out.extend([(F(a),F(b),m+1-z),(-F(a),-F(b),-m-z)])
    return out


def convex_hull(vertices):
    pts=sorted(set(vertices))
    if len(pts)<3: return pts
    def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        out=[]
        for p in seq:
            while len(out)>=2 and cross(out[-2],out[-1],p)<=0: out.pop()
            out.append(p)
        return out
    return half(pts)[:-1]+half(pts[::-1])[:-1]


def stage_a_parents(z):
    data=json.loads(SOURCE.read_text())
    out=[]
    for p in data['parents']:
        vs=[tuple(map(F,v)) for v in p['vertices']]
        constraints=[]
        for _,coeff,bound in p['constraints']:
            a,b,c=map(F,coeff)
            constraints.append((a,b,F(bound)-c*z))
        out.append(dict(labels=p['labels'],vertices=[v[:2] for v in vs],
                        edges=[tuple(e) for e in sorted(p['edges']) if vs[e[0]][2]==vs[e[1]][2]==z],
                        constraints=constraints))
    return out,dict(source='pinned floor edges',parents=len(out),floor_edges=sum(len(p['edges']) for p in out))


def stage_b_parents(z):
    ranges=[range(ceil((a+b)*z-(1-z)),floor(F(a,2)+b*(1-z)-z)+1) for a,b in CORE[2:]]
    count=1
    for r in ranges: count*=len(r)
    if count>1024: return [],dict(status='LABEL_SCOPE_LIMIT',label_tuples=count)
    out=[]
    for rest in itertools.product(*ranges):
        labels=(0,0)+rest
        constraints=band_constraints(labels,z)
        points=set()
        # Reconstruct by pairwise boundary intersections, not polygon clipping.
        for (a,b,c),(d,e,f) in itertools.combinations(constraints,2):
            det=a*e-b*d
            if not det: continue
            x,y=(c*e-b*f)/det,(a*f-c*d)/det
            if all(A*x+B*y<=C for A,B,C in constraints): points.add((x,y))
        hull=convex_hull(points)
        if not hull: continue
        vertices=sorted(hull)
        if len(vertices)==1: edges=[(0,0)]
        elif len(vertices)==2: edges=[(0,1)]
        else:
            index={p:i for i,p in enumerate(vertices)}
            edges=sorted(set(tuple(sorted((index[hull[i]],index[hull[(i+1)%len(hull)]]))) for i in range(len(hull))))
        out.append(dict(labels=labels,vertices=vertices,edges=edges,constraints=constraints))
    out.sort(key=lambda p:(p['labels'],p['vertices']))
    return out,dict(source='line-pair intersection reconstruction',label_tuples=count,
                    parents=len(out),floor_edges=sum(len(p['edges']) for p in out))


def clipped(parents,z):
    jobs=[]
    for pi,parent in enumerate(parents):
        for i,j in parent['edges']:
            x,y=parent['vertices'][i],parent['vertices'][j]
            ranges=[]
            for row in ROWS[-3:]:
                low,high=sorted((dot(row,x),dot(row,y)))
                ranges.append(range(ceil(low-(1-z)),floor(high-z)+1))
            jobs.append((pi,parent,i,j,x,y,ranges))
    attempts=sum(len(r[0])*len(r[1])*len(r[2]) for *_,r in jobs)
    counts=dict(floor_edges=len(jobs),edge_lap_triple_attempts=attempts)
    if attempts>2048: return [],dict(counts,status='CLIPPING_SCOPE_LIMIT',enumerated=0)
    records=[]
    endpoint_band_checks=0
    for pi,parent,i,j,start,end,ranges in jobs:
        direction=tuple(b-a for a,b in zip(start,end))
        for seventh,eighth,ninth in itertools.product(*ranges):
            labels=tuple(parent['labels'])+(seventh,eighth,ninth)
            interval=(F(0),F(1))
            for a,b,c in band_constraints(labels,z,ROWS):
                interval=restrict(interval,a*direction[0]+b*direction[1],a*start[0]+b*start[1],c)
            for a,b,c in parent['constraints']:
                interval=restrict(interval,a*direction[0]+b*direction[1],a*start[0]+b*start[1],c)
            lo,hi=interval
            if lo>hi: continue
            endpoints=sorted(tuple(a+u*d for a,d in zip(start,direction)) for u in interval)
            for point in endpoints:
                for row,m in zip(ROWS,labels):
                    need(z<=dot(row,point)-m<=1-z,'unsafe endpoint')
                    endpoint_band_checks+=1
            records.append(dict(id=f'P{pi}:E{i}-{j}:K{seventh}:L{eighth}:M{ninth}',parent=pi,edge=[i,j],
                                seventh_lap=seventh,eighth_lap=eighth,ninth_lap=ninth,
                                added_laps=[seventh,eighth,ninth],labels=labels,
                                endpoints=endpoints,source_parameters=interval))
    need(len(records)<=attempts<=2048,'attempt bound')
    counts.update(status='PASS',candidate_records=len(records),
                  point_records=sum(r['endpoints'][0]==r['endpoints'][1] for r in records),
                  labelled_endpoint_band_checks=endpoint_band_checks)
    return records,counts


def contact(record,P,Q):
    p0,p1=record['endpoints']
    h0,h1=Q*p0[0]-P*p0[1],Q*p1[0]-P*p1[1]
    low,high=sorted((h0,h1))
    integers=range(ceil(low),floor(high)+1)
    out=dict(interval=[low,high],first_integer=ceil(low),hit=bool(integers))
    if integers:
        u=F(0) if h0==h1 else (integers[0]-h0)/(h1-h0)
        point=tuple(a+u*(b-a) for a,b in zip(p0,p1))
        need(0<=u<=1 and Q*point[0]-P*point[1]==integers[0],'contact')
        out.update(parameter=u,point=point)
    return out


def coverage(records,z):
    ranking=[]
    for r in records:
        (x0,y0),(x1,y1)=r['endpoints']
        dx,dy=x1-x0,y0-y1
        if dx>0 and dy>0:
            pm,qm=ceil(1/dy)-1,ceil(1/dx)-1
            ranking.append(dict(id=r['id'],alpha=dx,beta=dy,P_max=pm,Q_max=qm,rectangle_pairs=pm*qm))
    ranking.sort(key=lambda v:v['rectangle_pairs'])
    out=dict(candidates=records,ranking=ranking,budget=400)
    if not ranking: return dict(out,status='NO_DESCENDING_SEGMENT',primary_status='INCOMPLETE')
    lead=ranking[0]
    out['leader']=lead
    if lead['rectangle_pairs']>400:
        return dict(out,status='SCOPE_LIMIT',primary_status='INCOMPLETE',enumerated_rectangle_pairs=0)
    residual=[(p,q) for p in range(1,lead['P_max']+1) for q in range(1,lead['Q_max']+1)
              if gcd(p,q)==1 and p*lead['beta']+q*lead['alpha']<1]
    matrix=[dict(id=r['id'],contacts=[dict(pair=pair,**contact(r,*pair)) for pair in residual]) for r in records]
    hits={r['id']:{tuple(c['pair']) for c in r['contacts'] if c['hit']} for r in matrix}
    menu=[lead['id']]
    missed=set(residual)-hits[lead['id']]
    steps=[]
    while missed:
        gains=[(len(missed&hits[r['id']]),r['id']) for r in records]
        most=max(n for n,_ in gains)
        if not most: break
        best=next(identity for n,identity in gains if n==most)
        gained=sorted(missed&hits[best])
        steps.append(dict(before=sorted(missed),chosen=best,newly_covered=gained))
        menu.append(best)
        missed-=set(gained)
    primary_misses=sorted(pair for pair in missed if primary(*pair))
    out.update(status='UNCOVERED_PRIMITIVE_PAIRS' if missed else 'COMPLETE_COVER_CERTIFICATE',
               primary_status='INCOMPLETE' if primary_misses else 'PRIMARY_COMPLETE',
               primary_uncovered=primary_misses,auxiliary_uncovered=sorted(set(missed)-set(primary_misses)),
               chosen_ids=menu,residual_pairs=residual,contact_matrix=matrix,
               uncovered=sorted(missed),greedy_steps=steps,
               counts=dict(candidates=len(records),descending=len(ranking),rectangle_pairs=lead['rectangle_pairs'],
                           residual_pairs=len(residual),contacts=len(records)*len(residual),chosen=len(menu)))
    return out


def diagnose(parents,z,certificate):
    if certificate['status']!='UNCOVERED_PRIMITIVE_PAIRS' or not certificate['primary_uncovered']:
        return dict(status='NOT_TRIGGERED')
    P,Q=certificate['primary_uncovered'][0]
    ranges=[]
    for a,b in ROWS[-3:]:
        ranges.append(range(ceil((a+b)*z-(1-z)),floor(F(a,2)+b*(1-z)-z)+1))
    H_range=range(ceil(Q*z-P*(1-z)),floor(F(Q,2)-P*z)+1)
    bound=len(parents)*len(ranges[0])*len(ranges[1])*len(ranges[2])*len(H_range)
    out=dict(pair=[P,Q],maximum_sections=bound,section_budget=100000,
             orbit_range=[H_range.start,H_range.stop-1])
    if bound>100000: return dict(out,status='DIAGNOSTIC_SCOPE_LIMIT',examined=0)
    sections=[]
    for pi,parent in enumerate(parents):
        for seventh,eighth,ninth,H in itertools.product(*ranges,H_range):
            labels=tuple(parent['labels'])+(seventh,eighth,ninth)
            constraints=parent['constraints']+band_constraints(labels,z,ROWS)
            interval=(z,F(1,2))
            for a,b,c in constraints:
                interval=restrict(interval,a+b*F(Q,P),-b*F(H,P),c)
            lo,hi=interval
            section=dict(parent=pi,seventh_lap=seventh,eighth_lap=eighth,ninth_lap=ninth,
                         added_laps=[seventh,eighth,ninth],H=H,
                         x_interval=interval,nonempty=lo<=hi)
            sections.append(section)
            if lo<=hi:
                x=(lo+hi)/2
                y=F(Q,P)*x-F(H,P)
                need(all(a*x+b*y<=c for a,b,c in constraints),'diagnosed point')
                return dict(out,status='RESTORED_PARENT_WITNESS',sections=sections,examined=len(sections),
                            parent=pi,labels=labels,point=[x,y],h=H)
    return dict(out,status='NO_WITNESS_IN_RESTORED_INPUT',sections=sections,examined=len(sections))


def run_stage(z,parents,geometry):
    records,counts=clipped(parents,z)
    certificate=coverage(records,z) if counts['status']=='PASS' else dict(status=counts['status'],primary_status='INCOMPLETE')
    diagnostic=diagnose(parents,z,certificate)
    return dict(threshold=z,geometry=geometry,clipping=counts,certificate=certificate,diagnostic=diagnostic)


def compare(expected,actual,path=''):
    need(type(expected)==type(actual),'type mismatch '+path)
    if isinstance(expected,dict):
        need(expected.keys()==actual.keys(),'keys mismatch '+path)
        return sum(compare(v,actual[k],path+'/'+k) for k,v in expected.items())
    if isinstance(expected,list):
        need(len(expected)==len(actual),'length mismatch '+path)
        return sum(compare(v,actual[i],path+'/'+str(i)) for i,v in enumerate(expected))
    need(expected==actual,'value mismatch '+path)
    return 1


def compare_stage(name,stage):
    production=json.loads((HERE/(name+'.json')).read_text())
    expected={k:v for k,v in stage['certificate'].items() if k not in
              ('primary_status','primary_uncovered','auxiliary_uncovered')}
    expected.update(schema='cc-positive-coverage-v1',rows=ROWS,threshold=stage['threshold'],
                    domain='positive integer p,q; ten distinct speeds iff p!=q and p!=2q; full labelled compilation includes auxiliaries')
    fields=compare(encode(expected),production['certificate'],'certificate')
    counts={k:v for k,v in stage['clipping'].items() if k!='labelled_endpoint_band_checks'}
    counts['budget']=2048
    fields+=compare(counts,production['clipping'],'clipping')
    fields+=compare(stage['certificate']['primary_status'],production['primary_status'],'primary_status')
    fields+=compare(str(stage['threshold']),production['threshold'],'threshold')
    fields+=compare(encode(stage['diagnostic']),production['diagnostic'],'diagnostic')
    # Stage A's full persisted source wrapper is checked as well. Stage B
    # geometry would use a distinct line-intersection representation.
    if name=='stage8':
        fields+=compare(json.loads(SOURCE.read_text()),production['geometry'],'geometry')
    return dict(status='PASS',scalar_fields_compared=fields,production_sha256=digest(HERE/(name+'.json')),
                scope='complete reached candidate/coverage/primary status, clipping counts, diagnostic status and Stage A source geometry; physical controls reviewed separately')


def main():
    pins=json.loads((HERE/'INPUTS.json').read_text())
    need(digest(HERE/'PROTOCOL.md')==pins['protocol_sha256'],'protocol changed')
    for path,pin in pins['files'].items(): need(digest(ROOT/path)==pin['sha256'],'input changed '+path)
    parents,geometry=stage_a_parents(F(1,8))
    a=run_stage(F(1,8),parents,geometry)
    stages={'stage8':a}
    if a['certificate']['primary_status']!='PRIMARY_COMPLETE':
        parents,geometry=stage_b_parents(F(1,10))
        stages['stage10']=run_stage(F(1,10),parents,geometry)
    out=dict(status='AWAITING_PRODUCTION_COMPARISON',protocol_sha256=pins['protocol_sha256'],
             script_sha256=digest(Path(__file__)),stages=stages,
             method='independent joint all-band clipping; direct integer interval contacts; Stage B line-pair intersections if reached')
    if all((HERE/(name+'.json')).exists() for name in stages):
        out['comparison']={name:compare_stage(name,stage) for name,stage in stages.items()}
        out['status']='PASS'
    print(json.dumps(encode(out),indent=2,sort_keys=True))


if __name__=='__main__': main()
