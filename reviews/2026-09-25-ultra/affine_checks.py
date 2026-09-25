"""Independent bounded exact review checks; no repository code imported."""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
D=F(1,8)
def dist(z):
    z=z%1
    return min(z,1-z)
def fl(z): return z.numerator//z.denominator

def strict_interval(speeds, ab):
    l,r=map(F,ab)
    assert l<r
    for v in speeds:
        a,b=v*l,v*r
        j=fl(a)
        assert j==fl(b)
        assert D<a-j<=b-j<1-D

def phase_cells(terms,t):
    cuts={F(0),F(1)}
    for b,a in terms:
        lo,hi=a*t,b+a*t
        for j in range(fl(lo)-1,fl(hi)+2):
            for d in (D,1-D):
                x=(j+d-lo)/b
                if 0<=x<=1: cuts.add(x)
    cuts=sorted(cuts)
    cells=[]
    for l,r in zip(cuts,cuts[1:]):
        if all(dist(b*(l+r)/2+a*t)>D for b,a in terms): cells.append((l,r))
    points=[x for x in cuts if all(dist(b*x+a*t)>=D for b,a in terms)]
    return cells,points

archive_counts={}
for stem,row_key,speed_key,int_key in (
    ('affine_family','checks','speeds','interval'),
    ('fast_cluster','witness_checks','full_relative_speeds','certified_interval')):
    data=json.loads((ROOT/'experiments'/f'{stem}.json').read_text())
    count=0
    for p in data['profiles']:
        for w in p[row_key]:
            speeds=w[speed_key]; t=F(w['witness_time'])
            assert min(dist(v*t) for v in speeds)==F(w['minimum_distance'])>D
            strict_interval(speeds,w[int_key])
            for v,value in w['distances'].items(): assert dist(int(v)*t)==F(value)
            count+=1
    archive_counts[stem]=count

controls=[]
for terms,t,expected in (
    (((1,0),(1,4),(2,3),(2,5)),F(1,8),F(0)),
    (((1,0),(1,4),(2,3),(2,5)),F(13,100),F(1,40)),
    (((1,0),(1,4),(2,3),(2,6)),F(1,8),F(1,8))):
    cells,points=phase_cells(terms,t)
    length=sum((r-l for l,r in cells),F(0))
    assert length==expected
    if length==0: assert points==list(map(lambda n:F(n,8),(1,2,3,5,6,7)))
    controls.append({'terms':terms,'t':t,'length':length,'strict_cells':cells,'valid_boundary_points':points})

new=[]
for name,core,terms,t0 in (
    ('negative_tied_minimum',(1,4,5),((2,-9),(2,-4),(3,0),(5,7)),F(21,64)),
    ('zero_offsets_bmin_gt_one',(1,4,5),((2,0),(3,0),(4,0),(5,0)),F(21,64)),
    ('all_negative_offsets',(1,4,5),((1,-100),(2,-7),(3,-2),(4,-1)),F(21,64)),
    ('mixed_offsets',(2,3,5),((2,-5),(2,-3),(3,4),(4,7)),F(13,100))):
    cells,_=phase_cells(terms,t0)
    l,r=max(cells,key=lambda lr:lr[1]-lr[0]); x0=(l+r)/2
    mc=min(dist(c*t0) for c in core)-D
    mf=min(dist(b*x0+a*t0) for b,a in terms)-D
    assert mc>0 and mf>0
    M=max(core); A=max(abs(a) for b,a in terms)
    cl=max((fl(c*t0)+D)/c for c in core)
    cr=min((fl(c*t0)+1-D)/c for c in core)
    eta=min(t0-cl,cr-t0)
    bound=max(F(M+A),F(2*A),F(M,2)/mc,F(A,2)/mf,1/(2*eta))
    Q=fl(bound)+1
    checks=[]
    for q in (Q,Q+1,2*Q):
        speeds=(*core,*(b*q+a for b,a in terms))
        assert min(speeds)>0 and len(set(speeds))==7
        m=fl(q*t0-x0+F(1,2)); t=(m+x0)/q
        assert abs(t-t0)<=F(1,2*q)
        assert cl<t<cr
        d=min(dist(v*t) for v in speeds)
        assert d>D
        checks.append({'q':q,'speeds':speeds,'time':t,'minimum':d})
    new.append({'name':name,'core':core,'terms':terms,'t0':t0,'x0':x0,'core_margin':mc,'fast_margin':mf,'Q':Q,'checks':checks})

result={'archive_witnesses_and_strict_intervals':archive_counts,'phase_controls':controls,'new_degeneracy_profiles':new}
(OUT/'affine_checks.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps({'archive_checks':archive_counts,'phase_controls':len(controls),'new_profiles':[{'name':p['name'],'Q':p['Q'],'checks':len(p['checks'])} for p in new]},indent=2))
