"""Exact fixed ambient cells; no q parameter is enumerated here."""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

ROWS=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2))
D=F(1,8)

def clip(poly,a,b,c):
    if not poly: return []
    out=[]
    for P,Q in zip(poly,poly[1:]+poly[:1]):
        f=a*P[0]+b*P[1]-c
        g=a*Q[0]+b*Q[1]-c
        if f<=0: out.append(P)
        if (f<0 and g>0) or (f>0 and g<0):
            t=f/(f-g)
            out.append(tuple(P[j]+t*(Q[j]-P[j]) for j in range(2)))
    return list(dict.fromkeys(out))

def det(A):
    a,b,c=A
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def solve(eq):
    A=[e[:3] for e in eq]; B=[e[3] for e in eq]
    d=det(A)
    if not d: return None
    return tuple(F(det([tuple(B[i] if j==k else A[i][j] for j in range(3)) for i in range(3)]),d) for k in range(3))

def inequalities(m):
    out=[(1,0,0,F(1,2)),(0,0,-1,-D)]
    for (a,b),l in zip(ROWS,m):
        out.extend([(-a,-b,1,-l),(a,b,1,l+1)])
    return out

def cells():
    states=[((0,0),[(D,D),(F(1,2),D),(F(1,2),1-D),(D,1-D)])]
    for a,b in ROWS[2:]:
        nxt=[]
        for m,P in states:
            for l in range(a+b):
                Q=clip(clip(P,-a,-b,-l-D),a,b,l+1-D)
                if Q: nxt.append((m+(l,),Q))
        states=nxt
    return states

def construct():
    out=[]
    for m,poly in cells():
        eq=inequalities(m)
        verts=set()
        for triple in combinations(eq,3):
            p=solve(triple)
            if p is not None and all(sum(e[j]*p[j] for j in range(3))<=e[3] for e in eq): verts.add(p)
        verts=sorted(verts)
        active=[{i for i,e in enumerate(eq) if sum(e[j]*p[j] for j in range(3))==e[3]} for p in verts]
        edges=[]
        for i,j in combinations(range(len(verts)),2):
            common=active[i]&active[j]
            if any(any(eq[u][s]*eq[v][t]!=eq[u][t]*eq[v][s] for s,t in combinations(range(3),2)) for u,v in combinations(common,2)):
                edges.append((i,j))
        out.append({'m':m,'base':poly,'vertices':verts,'edges':edges})
    return out

def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [encode(v) for v in x]
    return x

if __name__=='__main__':
    result=construct()
    Path(__file__).with_name('ambient.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print('cells',len(result),'vertices',sum(len(c['vertices']) for c in result),'edges',sum(len(c['edges']) for c in result))
    peak=max(p[2] for c in result for p in c['vertices'])
    print('ambient maximum',peak)
    print('maximizers',sorted({p for c in result for p in c['vertices'] if p[2]==peak}))
    for c in result: print(c['m'],'vertices',len(c['vertices']),'max',max(p[2] for p in c['vertices']))
