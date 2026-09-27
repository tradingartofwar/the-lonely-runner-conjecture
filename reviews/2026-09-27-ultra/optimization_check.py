"""Exact 16-state certificates; SciPy is used only by --write discovery.

--check uses standard-library Fraction arithmetic to verify archived primal and
 dual certificates, recompute physical moments by two exact constructions, and
 compare every claimed objective. No numeric optimizer is trusted as evidence.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

HERE=Path(__file__).resolve().parent
OUT=HERE/'optimization.json'
J=(F(9,32),F(3,8)); DELTA=F(1,8)
BASELINE='e94a87f650264826569cae63412c43a5175f5ae4'
CASES=[(6,7,11,16),(6,7,11,13),(6,7,11,45),(6,7,11,90),
       (6,7,11,266),(6,7,11,532),(56,64,72,113),(56,64,72,112),
       (3,10,28,1680),(3,10,28,3360)]
PAIR_MASKS=[s for s in range(16) if s.bit_count()<=2]

def frac(x): return str(x)
def distance(x):
    r=x%1
    return min(r,1-r)
def state(speeds,t):
    return sum(1<<i for i,v in enumerate(speeds) if distance(v*t)<DELTA)
def moments_from_states(masses):
    return [sum((masses[s] for s in range(16) if s&m==m),F(0)) for m in range(16)]
def physical(speeds):
    events={*J}
    for v in speeds:
        for k in range(int(v*J[0])-1,int(v*J[1])+2):
            for sign in (-1,1):
                t=(F(k)+sign*DELTA)/v
                if J[0]<=t<=J[1]: events.add(t)
    events=sorted(events)
    masses=[F(0)]*16
    atoms=[]
    for a,b in zip(events,events[1:]):
        s=state(speeds,(a+b)/2)
        masses[s]+=b-a
        atoms.append((a,b,s))
    moments=moments_from_states(masses)
    # Independent intersection of per-runner blocking occurrence lists.
    blocks=[]
    for v in speeds:
        blocks.append([(max(J[0],(F(k)-DELTA)/v),min(J[1],(F(k)+DELTA)/v))
                       for k in range(int(v*J[0])-1,int(v*J[1])+2)
                       if max(J[0],(F(k)-DELTA)/v)<min(J[1],(F(k)+DELTA)/v)])
    def intersect(a,b):
        i=j=0; result=[]
        while i<len(a) and j<len(b):
            lo=max(a[i][0],b[j][0]); hi=min(a[i][1],b[j][1])
            if lo<hi: result.append((lo,hi))
            if a[i][1]<b[j][1]: i+=1
            elif b[j][1]<a[i][1]: j+=1
            else: i+=1; j+=1
        return result
    for m in range(16):
        pieces=[J]
        for i in range(4):
            if m>>i&1: pieces=intersect(pieces,blocks[i])
        assert sum((b-a for a,b in pieces),F(0))==moments[m]
    return masses,moments,atoms,[t for t in events if state(speeds,t)==0]

def solve_linear(a,b):
    """Unique rational solution of a possibly overdetermined consistent system."""
    a=[[F(x) for x in row]+[F(v)] for row,v in zip(a,b)]
    n=len(a[0])-1; r=0; piv=[]
    for c in range(n):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        d=a[r][c]; a[r]=[x/d for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:
                d=a[i][c]; a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        piv.append(c);r+=1
    assert all(any(row[:-1]) or not row[-1] for row in a)
    assert len(piv)==n,(len(piv),n)
    answer=[F(0)]*n
    for i,c in enumerate(piv): answer[c]=a[i][-1]
    return answer

def model_specs(masses,moments):
    specs=[]
    def add(name,extra=(),forbidden=(),sum_triples=False):
        rows=[[F(int(s&m==m)) for s in range(16)] for m in PAIR_MASKS]
        rhs=[moments[m] for m in PAIR_MASKS]
        labels=['moment_'+str(m) for m in PAIR_MASKS]
        for m in extra:
            rows.append([F(int(s&m==m)) for s in range(16)])
            rhs.append(moments[m]);labels.append('moment_'+str(m))
        if sum_triples:
            rows.append([F(sum(int(s&m==m) for m in range(16) if m.bit_count()==3)) for s in range(16)])
            rhs.append(sum((moments[m] for m in range(16) if m.bit_count()==3),F(0)))
            labels.append('sum_triple_moments')
        specs.append(dict(name=name,rows=rows,rhs=rhs,labels=labels,forbidden=sorted(forbidden)))
    add('pairs')
    zero_triples=[m for m in range(16) if m.bit_count()==3 and not moments[m]]
    for m in zero_triples: add('pairs_zero_triple_'+str(m),forbidden=[s for s in range(16) if s&m==m])
    add('pairs_all_zero_triples',forbidden=[s for s in range(16) if any(s&m==m for m in zero_triples)])
    add('pairs_all_nonempty_support_zeros',forbidden=[s for s in range(1,16) if not masses[s]])
    for m in range(16):
        if m.bit_count()>=3: add('pairs_retained_moment_'+str(m),extra=[m])
    add('pairs_triple_sum',sum_triples=True)
    add('all_moments',extra=[m for m in range(16) if m.bit_count()>=3])
    return specs

def certify(spec,maximize=False):
    import numpy as np
    from scipy.optimize import linprog
    allowed=[s for s in range(16) if s not in spec['forbidden']]
    objective=[F((-1 if maximize else 1)*int(s==0)) for s in allowed]
    rows=[[row[s] for s in allowed] for row in spec['rows']]
    result=linprog(np.array(objective,dtype=float),A_eq=np.array(rows,dtype=float),
                   b_eq=np.array(spec['rhs'],dtype=float),bounds=(0,None),method='highs')
    assert result.success,result.message
    basis=[i for i,x in enumerate(result.x) if x>1e-9]
    exact=solve_linear([[row[i] for i in basis] for row in rows],spec['rhs'])
    primal=[F(0)]*16
    for i,x in zip(basis,exact): primal[allowed[i]]=x
    dual=[F(float(y)).limit_denominator(1000000) for y in result.eqlin.marginals]
    record={'sense':'max' if maximize else 'min','value':frac(primal[0]),
            'primal':list(map(frac,primal)),'dual':list(map(frac,dual))}
    verify_certificate(spec,record)
    return record

def verify_certificate(spec,record):
    p=list(map(F,record['primal']));d=list(map(F,record['dual']))
    assert len(p)==16 and len(d)==len(spec['rhs'])
    assert all(x>=0 for x in p)
    assert all(not p[s] for s in spec['forbidden'])
    for row,b in zip(spec['rows'],spec['rhs']): assert sum(x*y for x,y in zip(row,p))==b
    sign=-1 if record['sense']=='max' else 1
    for s in range(16):
        if s not in spec['forbidden']:
            assert sum(y*row[s] for y,row in zip(d,spec['rows']))<=sign*int(s==0)
    assert sum(y*b for y,b in zip(d,spec['rhs']))==sign*p[0]
    assert F(record['value'])==p[0]

def disjoint_pair_formula(m):
    """Analytic feasible interval when the first two blockers are disjoint."""
    assert m[3]==0
    c=m[0]-sum(m[1<<i] for i in range(4))+sum(m[s] for s in range(16) if s.bit_count()==2)
    lo_a=max(F(0),m[5]+m[9]-m[1]);hi_a=min(m[5],m[9])
    lo_b=max(F(0),m[6]+m[10]-m[2]);hi_b=min(m[6],m[10])
    lo_h=max(lo_a+lo_b,m[5]+m[6]+m[12]-m[4],m[9]+m[10]+m[12]-m[8])
    hi_h=min(hi_a+hi_b,m[12],c)
    assert lo_a<=hi_a and lo_b<=hi_b and lo_h<=hi_h
    return c-hi_h,c-lo_h

def generate():
    cases=[]
    for speeds in CASES:
        masses,moments,atoms,clear_events=physical(speeds)
        models=[]
        for spec in model_specs(masses,moments):
            models.append({'name':spec['name'],'row_labels':spec['labels'],'forbidden_states':spec['forbidden'],
                           'minimum':certify(spec),'maximum':certify(spec,True)})
        cases.append({'speeds':list(speeds),'state_masses':list(map(frac,masses)),
                      'moments':list(map(frac,moments)),'clear_duration':frac(masses[0]),
                      'zero_duration_clear_events':list(map(frac,clear_events)) if not masses[0] else None,
                      'models':models})
        print(speeds,'actual',masses[0],[(m['name'],m['minimum']['value'],m['maximum']['value']) for m in models if m['name'] in ('pairs','pairs_all_zero_triples','pairs_all_nonempty_support_zeros','pairs_triple_sum','all_moments')])
    return {'date':'2026-09-27','baseline':BASELINE,'status':'OBSERVED bounded exact certificates; no novelty claim',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'core':[1,4,5],'window':list(map(frac,J)),'threshold':frac(DELTA),
            'state_mask':'bit i corresponds to speeds[i]; moments[0]=length(J)',
            'cases':cases}

def check(data):
    assert data['script_sha256']==hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    count=0
    for case,speeds in zip(data['cases'],CASES):
        assert case['speeds']==list(speeds)
        masses,moments,_,clear_events=physical(speeds)
        assert masses==list(map(F,case['state_masses'])) and moments==list(map(F,case['moments']))
        assert F(case['clear_duration'])==masses[0]
        if not masses[0]: assert case['zero_duration_clear_events']==list(map(frac,clear_events))
        specs=model_specs(masses,moments)
        assert len(case['models'])==len(specs)
        for rec,spec in zip(case['models'],specs):
            assert rec['name']==spec['name'] and rec['row_labels']==spec['labels'] and rec['forbidden_states']==spec['forbidden']
            verify_certificate(spec,rec['minimum']);verify_certificate(spec,rec['maximum']);count+=2
        if not moments[3]:
            lower,upper=disjoint_pair_formula(moments)
            assert lower==F(case['models'][0]['minimum']['value'])
            assert upper==F(case['models'][0]['maximum']['value'])
    by_speed={tuple(c['speeds']):c for c in data['cases']}
    for y,z in [(45,90),(266,532)]:
        a,b=by_speed[(6,7,11,y)],by_speed[(6,7,11,z)]
        assert [a['moments'][m] for m in PAIR_MASKS]==[b['moments'][m] for m in PAIR_MASKS]
    a,b=by_speed[(3,10,28,1680)],by_speed[(3,10,28,3360)]
    assert a['moments']==b['moments'] and a['state_masses']==b['state_masses']
    assert a['zero_duration_clear_events']==['9/32'] and b['zero_duration_clear_events']==[]
    assert len(data['cases'])==len(CASES)
    print('PASS:',len(CASES),'physical cases, two exact moment constructions,',count,'rational primal/dual certificates')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    if args.write:
        data=generate();OUT.write_text(json.dumps(data,indent=2)+'\n');check(data)
    else: check(json.loads(OUT.read_text()))
