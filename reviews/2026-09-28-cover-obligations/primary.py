"""Frozen one-triple cover-obligation experiment; exact acceptance, no full geometry.

--write uses SciPy solely to propose rational primal/dual certificates.
--check is read-only and needs only the standard library. It recomputes singles,
pairs, and (only after summary-based selection) at most one triple per case.
Bits 0..3 index sorted extras; the empty state has mask 0. All duration interval
endpoints are measure-only; threshold equality membership is checked separately.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse, hashlib, json

HERE=Path(__file__).resolve().parent
PROTOCOL=HERE/'protocol.json'; OUT=HERE/'results.json'
J=(F(9,32), F(3,8)); DELTA=F(1,8)
PM=[s for s in range(16) if s.bit_count()<=2]
TM=[s for s in range(16) if s.bit_count()==3]

def serialize(obj):
    if isinstance(obj,F): return str(obj)
    if isinstance(obj,dict): return {str(k):serialize(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)): return [serialize(x) for x in obj]
    return obj

def solve_linear(rows,rhs):
    a=[[F(x) for x in row]+[F(v)] for row,v in zip(rows,rhs)]
    n=len(a[0])-1; r=0; piv=[]
    for c in range(n):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]; d=a[r][c]; a[r]=[x/d for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:
                d=a[i][c]; a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        piv.append(c); r+=1
    assert all(any(row[:-1]) or not row[-1] for row in a)
    assert len(piv)==n,(len(piv),n)
    ans=[F(0)]*n
    for i,c in enumerate(piv): ans[c]=a[i][-1]
    return ans

def row(mask): return [int(s&mask==mask) for s in range(16)]
def spec(moments,objective_mask=None,cover=False,upper=None):
    result=dict(objective=[int(s==0) for s in range(16)] if objective_mask is None else row(objective_mask),
      eq_rows=[row(m) for m in PM],eq_rhs=[moments[m] for m in PM],eq_labels=['moment_'+str(m) for m in PM],
      le_rows=[],le_rhs=[],le_labels=[])
    if cover:
        result['eq_rows'].append([int(s==0) for s in range(16)])
        result['eq_rhs'].append(F(0)); result['eq_labels'].append('empty_mass_zero')
    if upper:
        m,b=upper; result['le_rows'].append(row(m)); result['le_rhs'].append(b)
        result['le_labels'].append('triple_'+str(m)+'_upper')
    return result

def verify_cert(c):
    p=list(map(F,c['primal'])); de=list(map(F,c['dual_eq'])); dl=list(map(F,c['dual_le']))
    er=c['eq_rows']; eb=list(map(F,c['eq_rhs'])); ur=c['le_rows']; ub=list(map(F,c['le_rhs']))
    assert len(p)==16 and len(de)==len(er)==len(eb) and len(dl)==len(ur)==len(ub)
    assert all(x>=0 for x in p) and all(x<=0 for x in dl)
    assert all(sum(x*y for x,y in zip(r,p))==b for r,b in zip(er,eb))
    assert all(sum(x*y for x,y in zip(r,p))<=b for r,b in zip(ur,ub))
    assert all(sum(y*r[s] for y,r in zip(de,er))+sum(y*r[s] for y,r in zip(dl,ur))<=c['objective'][s] for s in range(16))
    pv=sum(x*y for x,y in zip(p,c['objective']))
    dv=sum(x*y for x,y in zip(de,eb))+sum(x*y for x,y in zip(dl,ub))
    assert pv==dv==F(c['value'])

def certify(s):
    import numpy as np
    from scipy.optimize import linprog
    a=s['eq_rows']; b=s['eq_rhs']; u=s['le_rows']; h=s['le_rhs']
    r=linprog(np.array(s['objective'],float),A_eq=np.array(a,float),b_eq=np.array(b,float),
       A_ub=np.array(u,float) if u else None,b_ub=np.array(h,float) if u else None,
       bounds=(0,None),method='highs')
    assert r.success,r.message
    support=[i for i,x in enumerate(r.x) if x>1e-9]
    active=[i for i,x in enumerate(r.ineqlin.residual) if abs(x)<1e-9]
    rows=a+[u[i] for i in active]; rhs=b+[h[i] for i in active]
    vals=solve_linear([[r[i] for i in support] for r in rows],rhs)
    p=[F(0)]*16
    for i,x in zip(support,vals): p[i]=x
    de=[F(float(x)).limit_denominator(1000000) for x in r.eqlin.marginals]
    dl=[F(float(x)).limit_denominator(1000000) for x in r.ineqlin.marginals]
    c={**s,'primal':p,'dual_eq':de,'dual_le':dl,'value':sum(x*y for x,y in zip(p,s['objective']))}
    verify_cert(c); return serialize(c)

def blocks(v,cost):
    result=[]
    for k in range(int(v*J[0])-1,int(v*J[1])+2):
        cost['lap_candidates']+=1
        a=max(J[0],(F(k)-DELTA)/v); b=min(J[1],(F(k)+DELTA)/v)
        if a<b: result.append((a,b,(k,)))
    cost['individual_interval_pieces']+=len(result)
    return result

def intersect(a,b,cost,key):
    i=j=0; out=[]
    while i<len(a) and j<len(b):
        cost[key]+=1
        lo=max(a[i][0],b[j][0]); hi=min(a[i][1],b[j][1])
        if lo<hi: out.append((lo,hi,a[i][2]+b[j][2]))
        if a[i][1]<b[j][1]: i+=1
        elif b[j][1]<a[i][1]: j+=1
        else: i+=1;j+=1
    return out

def measure(pieces): return sum((b-a for a,b,*_ in pieces),F(0))
def distance(x):
    r=x%1; return min(r,1-r)

def endpoint(speeds):
    t=J[1]; allspeeds=[1,4,5]+speeds
    phases={v:(v*t)%1 for v in allspeeds}
    ds={v:distance(v*t) for v in allspeeds}
    valid=all(d>=DELTA for d in ds.values())
    left=[v for v,r in phases.items() if r==DELTA]
    right=[v for v,r in phases.items() if r==1-DELTA]
    return dict(time=t,distances=ds,valid=valid,left_neighborhood_blockers=left,
       right_neighborhood_blockers=right,isolated=bool(valid and left and right))

def run_case(control,archived=None):
    speeds=control['extras']; cost=dict(lp_solves=0,logical_states=16,lap_candidates=0,
      individual_interval_lists=4,individual_interval_pieces=0,pair_queries=6,pair_comparisons=0,
      selected_triple_queries=0,selected_triple_comparisons=0,endpoint_queries=0)
    bs=[blocks(v,cost) for v in speeds]; ms={0:J[1]-J[0]}; pairs={}
    for i in range(4): ms[1<<i]=measure(bs[i])
    for i,j in combinations(range(4),2):
        m=(1<<i)|(1<<j); pairs[m]=intersect(bs[i],bs[j],cost,'pair_comparisons'); ms[m]=measure(pairs[m])
    record=dict(name=control['name'],speeds=speeds,moments=ms,blocks=bs,pair_pieces=pairs)
    def solve(s,old):
        cost['lp_solves']+=1
        if old is None: return certify(s)
        assert {k:old[k] for k in s}==serialize(s)
        verify_cert(old); return old
    record['baseline']=solve(spec(ms),archived['baseline'] if archived else None)
    record['cover_triples']=[]; record['selected']=None; record['repaired']=None; record['endpoint']=None
    if F(record['baseline']['value'])>0: record['outcome']='pair_only_positive'
    else:
        for m in TM:
            old=archived['cover_triples'][len(record['cover_triples'])]['certificate'] if archived else None
            c=solve(spec(ms,objective_mask=m,cover=True),old)
            record['cover_triples'].append(dict(mask=m,speeds=[v for i,v in enumerate(speeds) if m>>i&1],certificate=c))
        positive=[x for x in record['cover_triples'] if F(x['certificate']['value'])>0]
        if positive:
            chosen=min(positive,key=lambda x:(-F(x['certificate']['value']),x['speeds']))
            m=chosen['mask']; inds=[i for i in range(4) if m>>i&1]
            i,j,k=inds
            cost['selected_triple_queries']+=1
            pieces=intersect(pairs[(1<<i)|(1<<j)],bs[k],cost,'selected_triple_comparisons')
            actual=measure(pieces); forced=F(chosen['certificate']['value'])
            record['selected']=dict(mask=m,speeds=chosen['speeds'],forced_min=forced,actual_upper=actual,
               pieces=pieces,queried_pair_mask=(1<<i)|(1<<j),tested_third_speed=speeds[k],
               pair_phase_ranges=[dict(interval=[a,b],unwrapped_phase=[speeds[k]*a,speeds[k]*b]) for a,b,_ in pairs[(1<<i)|(1<<j)]])
            if actual<forced:
                record['repaired']=solve(spec(ms,upper=(m,actual)),archived['repaired'] if archived else None)
                assert F(record['repaired']['value'])>0
                record['outcome']='one_triple_repair_positive'
            else: record['outcome']='selected_triple_failed'
        else: record['outcome']='no_individually_forced_triple'
        if record['repaired'] is None:
            cost['endpoint_queries']+=1; record['endpoint']=endpoint(speeds)
    record['cost']=cost
    result=serialize(record)
    if archived is not None: assert result==archived
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    protocol=json.loads(PROTOCOL.read_text())
    meta=dict(baseline=protocol['baseline'],protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
      primary_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),window=list(map(str,J)),threshold=str(DELTA),
      mask_convention='bit i corresponds to sorted speeds[i]; moments are inclusive; LP primal atoms are exact active states',
      certificate_convention='min c.x with Aeq.x=b, Ale.x<=h, x>=0; dual y free,z<=0; Aeq^T.y+Ale^T.z<=c; equal rational objectives')
    if args.write:
        data={**meta,'cases':[run_case(c) for c in protocol['controls']]}; OUT.write_text(json.dumps(data,indent=2)+'\n')
    else:
        data=json.loads(OUT.read_text());assert {k:data[k] for k in meta}==meta
    for case,c in zip(data['cases'],protocol['controls']):
        run_case(c,case)
        print(c['name'],case['outcome'],'baseline',case['baseline']['value'],
          'selected',case['selected'],'repair',case['repaired']['value'] if case['repaired'] else None,'cost',case['cost'])
    assert len(data['cases'])==3
    print('PASS: three frozen controls; all rational primal/dual certificates, selection, requested geometry and costs verified.')

if __name__=='__main__': main()
