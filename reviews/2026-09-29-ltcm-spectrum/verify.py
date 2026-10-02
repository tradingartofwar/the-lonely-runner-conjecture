"""Frozen small-q checks by two structurally different exact methods."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).parent

def speeds(q): return (1,q,q+1,q+2,q+3,2*q+3,2*q+5)
def dist(x):
    x=x-x.numerator//x.denominator
    return min(x,1-x)
def value(q,t): return min(dist(v*t) for v in speeds(q))
def candidate(q):
    if q==4: return F(1,8),F(1,8)
    if q%3==0:
        m=F(q,3*(2*q+1));return m,2*m
    if q%6 in (1,2):return F(1,6),F(1,6)
    if q%6==4:
        m=F(q-1,3*(2*q+1));return m,2*m
    assert q%6==5
    m=F(q+1,2*(3*q+5));return m,3*m

def direct(q):
    """All tent knots; maximize lower affine envelope separately per time cell."""
    v=speeds(q)
    knots=sorted({F(j,2*w) for w in v for j in range(2*w+1)})
    best=F(0);times=set();crossings=0
    for a,b in zip(knots,knots[1:]):
        mid=(a+b)/2;lines=[]
        for w in v:
            x=w*mid;lap=x.numerator//x.denominator
            lines.append((w,-lap) if x-lap<F(1,2) else (-w,lap+1))
        tests={a,b}
        for (s,c),(r,d) in combinations(lines,2):
            if s!=r:
                t=F(d-c,s-r)
                if a<t<b: tests.add(t);crossings+=1
        for t in tests:
            val=min(s*t+c for s,c in lines)
            if val>best:best=val;times={t}
            elif val==best:times.add(t)
    return best,sorted(times),len(knots),crossings

def ceil(x):return -((-x.numerator)//x.denominator)
def floor(x):return x.numerator//x.denominator

def ambient(q,cells):
    """At most one extremal integer-plane choice per edge plus all vertices."""
    best=None;times=set();count=0
    def add(p):
        nonlocal best,times,count
        h=q*p[0]-p[1]
        assert h.denominator==1
        assert value(q,p[0])>=p[2]
        count+=1
        if best is None or p[2]>best:best=p[2];times={p[0]}
        elif p[2]==best:times.add(p[0])
    for c in cells:
        vs=[tuple(map(F,p)) for p in c['vertices']]
        for p in vs:
            if (q*p[0]-p[1]).denominator==1:add(p)
        for i,j in c['edges']:
            a,b=vs[i],vs[j];ha=q*a[0]-a[1];hb=q*b[0]-b[1]
            if ha==hb:
                if ha.denominator==1:add(max((a,b),key=lambda p:p[2]))
                continue
            lo,hi=ceil(min(ha,hb)),floor(max(ha,hb))
            if lo>hi:continue
            slope=(b[2]-a[2])/(hb-ha)
            h=hi if slope>=0 else lo
            r=(h-ha)/(hb-ha)
            add(tuple(a[k]+r*(b[k]-a[k]) for k in range(3)))
    return best,sorted(times),count

def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x

if __name__=='__main__':
    cells=json.loads(ROOT.joinpath('ambient.json').read_text())
    rows=[]
    for q in range(2,26):
        m,t=candidate(q)
        exact,all_times,knots,crossings=direct(q)
        geom,selected,count=ambient(q,cells)
        assert exact==geom==value(q,t)==m,(q,m,exact,geom)
        if q==4:assert all_times==[F(1,8),F(3,8),F(5,8),F(7,8)]
        rows.append(dict(q=q,maximum=m,witness=t,all_maximizers=all_times,ambient_selected=selected,ambient_candidates=count,time_knots=knots,line_crossings=crossings))
        print(q,m,t,'maximizers',len(all_times))
    large=[]
    for q in (100003,100004):
        m,t=candidate(q);assert value(q,t)==m
        large.append(dict(q=q,claimed_maximum=m,witness=t,distances=[dist(v*t) for v in speeds(q)],scope='witness only; no exhaustive maximum'))
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'PROTOCOL.md',ROOT/'PREVALIDATION_DERIVATION.md',ROOT/'ambient.py',ROOT/'ambient.json',Path(__file__)]}
    out=dict(small_q=rows,large_q=large,hashes=hashes,scope='24 complete one-dimensional maxima, two large witnesses; symbolic proof separate')
    ROOT.joinpath('verification.json').write_text(json.dumps(encode(out),indent=2)+'\n')
    print('PASS',len(rows),'complete small-q cases;',len(large),'large witness checks')
