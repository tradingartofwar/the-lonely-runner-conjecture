#!/usr/bin/env python3
"""Independent exact halfspace clipping and coverage review; no production imports."""
import hashlib
import json
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json'
ROWS = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(3,8))
Z = F(1,8)


def encode(v):
    if isinstance(v,F):
        return str(v)
    if isinstance(v,dict):
        return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):
        return [encode(x) for x in v]
    return v


def need(v,why):
    if not v:
        raise ArithmeticError(why)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(row,point):
    return sum(a*b for a,b in zip(row,point))


def restrict(lo,hi,slope,constant,bound):
    """Intersect with slope*u + constant <= bound."""
    if slope>0:
        hi=min(hi,(bound-constant)/slope)
    elif slope<0:
        lo=max(lo,(bound-constant)/slope)
    elif constant>bound:
        return F(1),F(0)
    return lo,hi


def reconstruct_candidates(data):
    records=[]
    edges=attempts=band_checks=parent_checks=0
    for parent_index,parent in enumerate(data['parents']):
        vs=[tuple(map(F,p)) for p in parent['vertices']]
        for i,j in sorted(parent['edges']):
            if not vs[i][2]==vs[j][2]==Z:
                continue
            edges+=1
            first,last=vs[i][:2],vs[j][:2]
            direction=tuple(b-a for a,b in zip(first,last))
            values=sorted((dot(ROWS[-1],first),dot(ROWS[-1],last)))
            for lap in range(1,9):
                # Counting preflight edge-band overlaps is separate from clipping.
                if max(values[0],lap+Z)<=min(values[1],lap+1-Z):
                    attempts+=1
                labels=parent['labels']+[lap]
                lo,hi=F(0),F(1)
                # Unlike the production added-band clip, reconstruct by all
                # fourteen closed inequalities and every stored halfspace.
                for (a,b),m in zip(ROWS,labels):
                    slope=a*direction[0]+b*direction[1]
                    base=a*first[0]+b*first[1]
                    lo,hi=restrict(lo,hi,slope,base,m+1-Z)
                    lo,hi=restrict(lo,hi,-slope,-base,-m-Z)
                for _,coeff,bound in parent['constraints']:
                    a,b,c=map(F,coeff)
                    lo,hi=restrict(lo,hi,a*direction[0]+b*direction[1],
                                   a*first[0]+b*first[1]+c*Z,F(bound))
                if lo>hi:
                    continue
                endpoints=sorted(tuple(a+u*d for a,d in zip(first,direction)) for u in (lo,hi))
                for x,y in endpoints:
                    for row,m in zip(ROWS,labels):
                        need(Z<=dot(row,(x,y))-m<=1-Z,'unsafe clipped endpoint')
                        band_checks+=1
                    for _,coeff,bound in parent['constraints']:
                        need(dot(tuple(map(F,coeff)),(x,y,Z))<=F(bound),'parent halfspace')
                        parent_checks+=1
                records.append(dict(id=f'P{parent_index}:E{i}-{j}:K{lap}',
                                    parent=parent_index,edge=[i,j],seventh_lap=lap,
                                    labels=labels,endpoints=endpoints,source_parameters=[lo,hi]))
    need(edges==24,'floor edge count')
    need(len(records)<=attempts<=192<=256,'candidate bound')
    return records,dict(floor_edges=edges,edge_lap_attempts=attempts,
                        candidate_records=len(records),
                        point_records=sum(r['endpoints'][0]==r['endpoints'][1] for r in records),
                        labelled_endpoint_band_checks=band_checks,
                        stored_parent_endpoint_checks=parent_checks)


def project(record,P,Q):
    endpoints=record['endpoints']
    h0,h1=(Q*x-P*y for x,y in endpoints)
    lo,hi=min(h0,h1),max(h0,h1)
    integers=list(range(ceil(lo),floor(hi)+1))
    out=dict(interval=[lo,hi],first_integer=ceil(lo),hit=bool(integers))
    if integers:
        h=integers[0]
        u=F(0) if h0==h1 else (h-h0)/(h1-h0)
        point=tuple(a+u*(b-a) for a,b in zip(*endpoints))
        need(0<=u<=1 and Q*point[0]-P*point[1]==h,'projection interpolation')
        out.update(parameter=u,point=point)
    return out


def reconstruct_coverage(records):
    ranking=[]
    for r in records:
        (x0,y0),(x1,y1)=r['endpoints']
        dx,dy=x1-x0,y0-y1
        if dx>0 and dy>0:
            # p*dy<1 and q*dx<1 produce the strict bounding rectangle.
            pm,qm=ceil(1/dy)-1,ceil(1/dx)-1
            ranking.append(dict(id=r['id'],alpha=dx,beta=dy,
                                P_max=pm,Q_max=qm,rectangle_pairs=pm*qm))
    ranking.sort(key=lambda r:r['rectangle_pairs'])
    out=dict(schema='cc-positive-coverage-v1',rows=ROWS,threshold=Z,
             domain='positive integer p,q; p!=q for distinct speeds',
             candidates=records,budget=400,ranking=ranking)
    if not ranking:
        return dict(out,status='NO_DESCENDING_SEGMENT')
    leader=ranking[0]
    out['leader']=leader
    if leader['rectangle_pairs']>400:
        return dict(out,status='SCOPE_LIMIT',enumerated_rectangle_pairs=0)
    residual=[]
    for p in range(1,leader['P_max']+1):
        for q in range(1,leader['Q_max']+1):
            if gcd(p,q)==1 and p*leader['beta']+q*leader['alpha']<1:
                residual.append((p,q))
    matrix=[dict(id=r['id'],contacts=[dict(pair=pair,**project(r,*pair)) for pair in residual])
            for r in records]
    hits={r['id']:set(tuple(c['pair']) for c in r['contacts'] if c['hit']) for r in matrix}
    chosen=[leader['id']]
    missed=set(residual)-hits[chosen[0]]
    steps=[]
    while missed:
        gains=[(len(missed&hits[r['id']]),r['id']) for r in records]
        most=max(n for n,_ in gains)
        if most==0:
            break
        best=next(identity for n,identity in gains if n==most)
        gained=sorted(missed&hits[best])
        steps.append(dict(before=sorted(missed),chosen=best,newly_covered=gained))
        chosen.append(best)
        missed-=set(gained)
    out.update(status='UNCOVERED_PRIMITIVE_PAIRS' if missed else 'COMPLETE_COVER_CERTIFICATE',
               residual_pairs=residual,contact_matrix=matrix,greedy_steps=steps,
               chosen_ids=chosen,uncovered=sorted(missed),
               counts=dict(candidates=len(records),descending=len(ranking),
                           rectangle_pairs=leader['rectangle_pairs'],residual_pairs=len(residual),
                           contacts=len(records)*len(residual),chosen=len(chosen)))
    return out


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


def main():
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    need(digest(HERE/'PROTOCOL.md')==inputs['protocol_sha256'],'protocol changed')
    for path,pin in inputs['files'].items():
        need(digest(ROOT/path)==pin['sha256'],'source changed '+path)
    data=json.loads(SOURCE.read_text())
    need(tuple(map(tuple,data['rows']))==ROWS[:-1] and F(data['threshold'])==Z,'parent scope')
    records,counts=reconstruct_candidates(data)
    certificate=reconstruct_coverage(records)
    report=dict(status='AWAITING_PRODUCTION_COMPARISON',
                method='all seven bands and stored parent halfspaces; direct integer projection enumeration; no production imports',
                protocol_sha256=inputs['protocol_sha256'],source_sha256=digest(SOURCE),
                script_sha256=digest(Path(__file__)),clipping=counts,
                reconstructed=certificate,production_fields_compared=0)
    if (HERE/'certificate.json').exists():
        production=json.loads((HERE/'certificate.json').read_text())
        core={k:v for k,v in production.items() if k!='transfer_provenance'}
        report['production_fields_compared']=compare(encode(certificate),core)
        report['production_certificate_sha256']=digest(HERE/'certificate.json')
        report['status']='PASS'
    print(json.dumps(encode(report),indent=2,sort_keys=True))


if __name__=='__main__':
    main()
