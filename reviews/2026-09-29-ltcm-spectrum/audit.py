"""Independent fixed-arrangement reconstruction and universal linear certificates.
No physical q instances are scanned here.
"""
from fractions import Fraction as R
from itertools import combinations
from pathlib import Path
import json

P=Path(__file__).parent
forms=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2))

def linear_solve(rows):
    m=[list(map(R,row)) for row in rows]
    for c in range(3):
        pivot=next((r for r in range(c,3) if m[r][c]),None)
        if pivot is None:return None
        m[c],m[pivot]=m[pivot],m[c]
        scale=m[c][c];m[c]=[x/scale for x in m[c]]
        for r in range(3):
            if r!=c:
                scale=m[r][c];m[r]=[m[r][j]-scale*m[c][j] for j in range(4)]
    return tuple(m[i][3] for i in range(3))

def fractional(v):return v-v.numerator//v.denominator
def norm(v):
    f=fractional(v);return min(f,1-f)

planes={(1,0,0,R(1,2)),(0,0,1,R(1,8))}
for a,b in forms:
    for lap in range(a+b):
        planes.add((a,b,-1,lap));planes.add((a,b,1,lap+1))
planes=sorted(planes)
vertices={};triples=0
for rows in combinations(planes,3):
    triples+=1
    point=linear_solve(rows)
    if point is None:continue
    x,y,z=point
    if not (R(1,8)<=x<=R(1,2) and R(1,8)<=y<=R(7,8) and R(1,8)<=z<=R(1,2)):continue
    vals=[a*x+b*y for a,b in forms]
    if min(map(norm,vals))<z:continue
    label=tuple(t.numerator//t.denominator for t in vals)
    vertices.setdefault(label,set()).add(point)
archived=json.loads(P.joinpath('ambient.json').read_text())
expected={tuple(c['m']):{tuple(map(R,v)) for v in c['vertices']} for c in archived}
assert vertices==expected

# For q=q0+6r, r>=0, compare all outward edge integer-hit losses
# with the proposed minimum.  Cross-multiplication gives A*q+B>=0.
peaks=[(R(1,6),R(1,6),[(-1,2),(R(1,5),-1),(1,-1)]),
 (R(1,6),R(1,3),[(-1,1),(-1,4),(1,-2)]),
 (R(1,2),R(1,6),[(-3,5),(0,-1),(0,R(1,2))]),
 (R(1,2),R(1,3),[(-1,2),(0,R(-1,2)),(0,1)]),
 (R(1,3),R(5,6),[(-2,1),(0,1),(1,-2)]),
 (R(1,2),R(2,3),[(-1,2),(0,-1),(0,R(1,2))]),
 (R(1,2),R(5,6),[(R(-3,5),1),(0,R(-1,2)),(0,1)])]
actual_directions={}
for cell in archived:
    vs=[tuple(map(R,v)) for v in cell['vertices']]
    for i,j in cell['edges']:
        for top,other in ((vs[i],vs[j]),(vs[j],vs[i])):
            if top[2]!=R(1,6):continue
            extent=top[2]-other[2]
            direction=((other[0]-top[0])/extent,(other[1]-top[1])/extent)
            actual_directions.setdefault(top[:2],set()).add(direction)
            assert extent==(R(1,42) if top[:2]==(R(1,3),R(5,6)) and direction==(-2,1) else R(1,24))
assert actual_directions=={(x,y):set(ds) for x,y,ds in peaks}
residues=[(0,6,1,12,6),(3,3,1,12,6),(4,10,1,4,2),(5,5,1,9,15)]
certs=[]
for residue,q0,num,aa,bb in residues:
    for index,(x,y,dirs) in enumerate(peaks):
        rho=fractional(q0*x-y)
        assert rho>0
        for alpha,beta in dirs:
            sign=1 if alpha*q0-beta>0 else -1
            da,db=sign*alpha,-sign*beta
            assert da>=0 and da*q0+db>0
            gap=(1-rho) if sign==1 else rho
            A=gap*aa-num*da;B=gap*bb-num*db
            assert A>=0 and A*q0+B>=0,(residue,index,alpha,beta,A,B)
            certs.append(dict(residue=residue,q0=q0,peak=index,direction=[alpha,beta],slope=A,constant=B,value_at_q0=A*q0+B))

# Universal lower certificates are affine in error e; endpoint checks suffice.
phase_checks=[]
for name,x0,xa,y0,ya,end,labels in [
 ('E',R(1,3),-2,R(5,6),1,R(1,42),(0,0,1,1,1,2,3)),
 ('C',R(1,2),-3,R(1,6),5,R(1,24),(0,0,0,1,1,1,2))]:
    for e in (R(0),end):
        z=R(1,6)-e;x=x0+xa*e;y=y0+ya*e
        phase=[a*x+b*y-m for (a,b),m in zip(forms,labels)]
        assert all(z<=f<=1-z for f in phase)
        phase_checks.append(dict(chart=name,error=e,margin=z,phases=phase))

# The exceptional q4 is certified by the complete range of 4x-y in each cell.
q4=[]
for label,vs in sorted(vertices.items()):
    lo=min(4*x-y for x,y,z in vs);hi=max(4*x-y for x,y,z in vs)
    ints=list(range(-((-lo.numerator)//lo.denominator),hi.numerator//hi.denominator+1))
    if ints:
        assert len(ints)==1 and ints[0]==lo==hi or (ints==[0] and lo==0)
        on=[p for p in vs if 4*p[0]-p[1]==ints[0]]
        assert len(on)==1 and on[0][2]==R(1,8)
    q4.append(dict(label=label,min=lo,max=hi,integers=ints))

def enc(x):
    if isinstance(x,R):return str(x)
    if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v) for v in x]
    return x
out=dict(plane_count=len(planes),triple_systems=triples,matched_cells=len(vertices),matched_vertices=sum(map(len,vertices.values())),universal_loss_certificates=certs,affine_phase_endpoint_certificates=phase_checks,q4_ranges=q4)
P.joinpath('audit.json').write_text(json.dumps(enc(out),indent=2)+'\n')
print('PASS',len(vertices),'cells',sum(map(len,vertices.values())),'vertices;',len(certs),'universal loss comparisons; affine phase tables; q4 completeness')
