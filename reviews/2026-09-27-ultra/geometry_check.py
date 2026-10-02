#!/usr/bin/env python3
"""Exact, standalone contact selection/stratification checks; no project imports."""
from fractions import Fraction as Q
from math import gcd
from itertools import combinations
from collections import defaultdict
from pathlib import Path
import hashlib
import json

BASE = 'e94a87f650264826569cae63412c43a5175f5ae4'
J = (Q(9,32), Q(3,8))

def ceil(x):
    return -((-x.numerator)//x.denominator)

def phase(v,t):
    return (v*t)%1

def safe(v,t,n):
    return Q(1,n) <= phase(v,t) <= 1-Q(1,n)

def contact_pair(u,v,n,window):
    """Oriented lower u, upper v; n>=3, u,v positive integers."""
    assert n>=3 and u>0 and v>0
    g=gcd(u,v)
    a,b=u//g,v//g
    if (a+b)%n:
        return []
    c=pow(a,-1,n)
    lo=ceil(g*window[0]-Q(c,n))
    hi=(g*window[1]-Q(c,n)).__floor__()
    return [Q(n*j+c,n*g) for j in range(lo,hi+1)]

def candidates(vs,n,window):
    eligible=[]
    ts=set(window)
    for u,v in combinations(vs,2):
        g=gcd(u,v)
        if ((u+v)//g)%n==0:
            eligible.append([u,v])
            ts.update(contact_pair(u,v,n,window))
            ts.update(contact_pair(v,u,n,window))
    return eligible, sorted(ts)

def cell(vs,n,t,window):
    phases=[phase(v,t) for v in vs]
    if not all(Q(1,n)<=p<=1-Q(1,n) for p in phases):
        return {'safe':False,'blockers':[v for v,p in zip(vs,phases) if not Q(1,n)<=p<=1-Q(1,n)]}
    laps=[(v*t).__floor__() for v in vs]
    L=max([window[0]]+[(m+Q(1,n))/v for v,m in zip(vs,laps)])
    R=min([window[1]]+[(m+1-Q(1,n))/v for v,m in zip(vs,laps)])
    assert L<=t<=R
    return {'safe':True,'component':[L,R], 'laps':laps,
            'lower':[v for v,p in zip(vs,phases) if p==Q(1,n)],
            'upper':[v for v,p in zip(vs,phases) if p==1-Q(1,n)]}

def intersect(xs,ys):
    out=[]; i=j=0
    while i<len(xs) and j<len(ys):
        l=max(xs[i][0],ys[j][0]); r=min(xs[i][1],ys[j][1])
        if l<=r: out.append((l,r))
        if xs[i][1]<ys[j][1]: i+=1
        else: j+=1
    return out

def intervals(vs,n,window):
    out=[window]
    for v in sorted(vs):
        current=[]
        for lap in range((v*window[0]).__floor__()-1,(v*window[1]).__floor__()+2):
            l=max(window[0],(lap+Q(1,n))/v)
            r=min(window[1],(lap+1-Q(1,n))/v)
            if l<=r: current.append((l,r))
        out=intersect(out,current)
    return out

def stratify(vs,n,window):
    """Common exact event partition: duration and signed vertex-minus-edge data."""
    events=set(window)
    for v in vs:
        for lap in range((v*window[0]).__floor__()-1,(v*window[1]).__floor__()+2):
            for t in ((lap+Q(1,n))/v,(lap+1-Q(1,n))/v):
                if window[0]<t<window[1]: events.add(t)
    events=sorted(events)
    def mask(t):
        return sum(1<<i for i,v in enumerate(vs) if not safe(v,t,n))
    durations=defaultdict(Q); euler=defaultdict(int)
    for t in events: euler[mask(t)]+=1
    for l,r in zip(events,events[1:]):
        m=mask((l+r)/2)
        durations[m]+=r-l
        euler[m]-=1
    moments=[sum((d for m,d in durations.items() if m&a==a),Q(0)) for a in range(1<<len(vs))]
    emoments=[sum(e for m,e in euler.items() if m&a==a) for a in range(1<<len(vs))]
    inclusion=sum((-1)**a.bit_count()*emoments[a] for a in range(len(emoments)))
    assert inclusion==euler[0]
    return {'events':len(events),'duration_moments':moments,'euler_moments':emoments,
            'clear_duration':durations[0],'clear_euler':euler[0]}

def output(obj):
    if isinstance(obj,Q): return str(obj)
    if isinstance(obj,dict): return {str(k):output(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)): return [output(v) for v in obj]
    return obj

checks=0
# Exhaustive bounded arithmetic crosscheck independent of gcd criterion:
# enumerate only lower threshold events and test upper phase directly.
for n in range(3,11):
    for u in range(1,33):
        for v in range(1,33):
            direct=[(Q(m)+Q(1,n))/u for m in range(u) if phase(v,(Q(m)+Q(1,n))/u)==1-Q(1,n)]
            assert contact_pair(u,v,n,(Q(0),Q(1)))==direct
            checks+=1

family=[]; first=None
for h in (1,2,3,4):
    vs=(1,3,4,5,10,28,1680*h)
    eligible,ts=candidates(vs,8,J)
    assert eligible==[[3,5],[4,28]] and ts==list(J)
    fs=intervals(vs,8,J)
    expected=[(J[0],J[0])] if h%2 else []
    assert fs==expected
    data=stratify(vs,8,J)
    assert data['clear_duration']==0 and data['clear_euler']==h%2
    if first is None: first=data['duration_moments']
    else: assert data['duration_moments']==first
    family.append({'h':h,'speeds':vs,'eligible_pairs':eligible,'candidates':ts,'allowed':fs,
                   'contact_cells':{str(t):cell(vs,8,t,J) for t in ts},**data})

large=[]
for h in (1000000,1000001):
    vs=(1,3,4,5,10,28,1680*h)
    eligible,ts=candidates(vs,8,J)
    assert eligible==[[3,5],[4,28]] and ts==list(J)
    assert cell(vs,8,J[0],J)['safe']==bool(h%2)
    assert not cell(vs,8,J[1],J)['safe']
    large.append({'h':h,'eligible_pairs':eligible,'candidates':ts,
                  'contact_cells':{str(t):cell(vs,8,t,J) for t in ts}})

controls=[]
for name,vs,n,t,window,expected in [
    ('frozen_37',(6,12,18,25,31,37,43),8,Q(3,8),(Q(0),Q(1)),(Q(3,8),Q(3,8))),
    ('frozen_35',(6,12,18,25,31,35,43),8,Q(3,8),(Q(0),Q(1)),(Q(3,8),Q(55,144))),
    ('third_controller',(35,70,105,141,1119,807,1923),8,Q(5,24),(Q(0),Q(1)),(Q(5,24),Q(5,24))),
    ('clipped_interval',(1,3),3,Q(4,9),(Q(0),Q(4,9)),(Q(4,9),Q(4,9))),
    ('tight_three',(1,2),3,Q(1,3),(Q(0),Q(1)),(Q(1,3),Q(1,3))),
]:
    fs=intervals(vs,n,window)
    info=cell(vs,n,t,window)
    assert tuple(info['component'])==expected
    assert expected in fs
    eligible,ts=candidates(vs,n,window)
    assert all(l in ts for l,r in fs if l==r)
    controls.append({'name':name,'speeds':vs,'n':n,'window':window,'time':t,'cell':info,
                     'component_count':len(fs),'singleton_count':sum(l==r for l,r in fs),
                     'arithmetic_candidate_count':len(ts)})

# Without the zero-duration premise, an opposing-contact selector can miss existence.
assert candidates((1,3),3,(Q(0),Q(1)))[1]==[Q(0),Q(1)]
assert intervals((1,3),3,(Q(0),Q(1)))==[(Q(4,9),Q(5,9))]
# An eligible pair contact can still be strictly blocked by a third runner.
negative_vs=(1,3,4,5,10,28,3360)
assert safe(4,J[0],8) and safe(28,J[0],8) and not safe(3360,J[0],8)
# Sum divisible by n alone is insufficient: reduced sum is necessary.
assert (8+16)%8==0 and contact_pair(8,16,8,(Q(0),Q(1)))==[]
# Candidate list size is not uniformly bounded even at fixed n and global gcd 1.
growth=[]
for q in (1,7,101):
    vs=(1,q,3*q)
    # This illustration is about pair arithmetic; q=1 duplicates a constraint,
    # so use q>=7 as actual distinct four-runner inputs.
    ts=sorted(set(contact_pair(q,3*q,4,(Q(0),Q(1)))+contact_pair(3*q,q,4,(Q(0),Q(1)))))
    assert len(ts)==2*q
    growth.append({'q':q,'pair_candidates':len(ts),'global_gcd':gcd(*vs),
                   'distinct_speeds':len(set(vs))==3})

result={'baseline':BASE,'status':'OBSERVED exact finite checks; unbounded derivations remain proof candidates',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'pair_identity_checks':checks,'pair_scope':'3<=n<=10, 1<=u,v<=32, including u=v; [0,1]',
        'family':family,'large_direct_controls':large,'required_controls':controls,
        'unbounded_candidate_count_controls':growth,
        'limits':'No full-event enumeration for large h; no global/all-reference/novelty claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(output(result),indent=2)+'\n')
print(json.dumps({'pair_identity_checks':checks,'family_controls':len(family),
                  'large_direct_controls':len(large),'required_controls':len(controls),
                  'output':str(Path(__file__).with_suffix('.json'))}))
