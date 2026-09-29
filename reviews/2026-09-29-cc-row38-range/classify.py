#!/usr/bin/env python3
"""Frozen coefficient classification; exact reduction and physical records."""
from fractions import Fraction as F
from math import gcd, lcm, ceil, floor
from pathlib import Path
import hashlib
import importlib.util
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CORE=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2))
PAIRS=((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
       (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pack(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):pack(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [pack(x) for x in v]
    return v


def save(name,data,compact=False):
    path=HERE/name;path.parent.mkdir(parents=True,exist_ok=True)
    options=dict(separators=(',',':')) if compact else dict(indent=2)
    path.write_text(json.dumps(pack(data),sort_keys=True,**options)+'\n')


def phase(x):return x-floor(x)
def safe(x):return F(1,8)<=phase(x)<=F(7,8)


def point(P,Q):
    assert P>0 and Q>0 and gcd(P,Q)==1
    M=P+Q;rho=(P-2*M)%8
    if rho<=M:
        x=F(1,4)+F(rho,8*M);y=F(9,8)-x;role='L'
    else:
        x,y,role={(1,4):(F(17,56),F(3,14),'F'),
                  (2,1):(F(9,28),F(9,56),'G'),
                  (1,1):(F(1,8),F(1,8),'C')}[(P,Q)]
    h=Q*x-P*y
    assert h.denominator==1 and all(safe(a*x+b*y) for a,b in CORE)
    return dict(pair=[P,Q],M=M,rho=rho,point=[x,y],h=int(h),role=role)


def bezout(P,Q):
    a,b,r,r1,s,s1=P,Q,1,0,0,1
    while b:
        k=a//b;a,b=b,a-k*b;r,r1=r1,r-k*r1;s,s1=s1,s-k*s1
    assert a==1 and r*P+s*Q==1
    return r,s


def physical(A,B,p,q):
    d=gcd(p,q);P,Q=p//d,q//d;c=point(P,Q);x,y=c['point'];h=c['h']
    r,s=bezout(P,Q);N=floor(r*x+s*y);tau=r*x+s*y-N;t=tau/d
    rows=CORE+((A,B),);speeds=[a*p+b*q for a,b in rows]
    raw=[a*x+b*y for a,b in rows];m=list(map(floor,raw));phases=list(map(phase,raw))
    laps=[z+(-a*s+b*r)*h-(a*P+b*Q)*N for (a,b),z in zip(rows,m)]
    assert 0<tau<1 and phase(P*tau)==x and phase(Q*tau)==y
    assert laps==[floor(v*t) for v in speeds] and phases==[phase(v*t) for v in speeds]
    distinct=len(set([0]+speeds))==8
    assert distinct==(p!=q and all((A-a)*p+(B-b)*q!=0 for a,b in CORE[2:]))
    refl=[phase(v*(1-t)) for v in speeds];refl_laps=[floor(v*(1-t)) for v in speeds]
    assert refl==[1-f if f else F(0) for f in phases]
    assert refl_laps==[v-z-int(bool(f)) for v,z,f in zip(speeds,laps,phases)]
    alternate=(r+Q)*x+(s-P)*y
    assert phase(alternate)==tau
    return pack(dict(row=[A,B],pair=[p,q],gcd=d,primitive=[P,Q],role=c['role'],
        point=[x,y],h=h,M=c['M'],rho=c['rho'],bezout=[r,s],N=N,primitive_time=tau,time=t,
        speeds=speeds,torus_laps=m,physical_laps=laps,phases=phases,
        reflected_time=1-t,reflected_phases=refl,reflected_laps=refl_laps,
        alternate_bezout_time=phase(alternate)/d,distinct_speeds=distinct,
        minimum=min(min(f,1-f) for f in phases),seventh_safe=safe(raw[-1])))


def leader_contract(A,B):
    u,v=2*A+7*B,3*A+6*B;m=min(u,v)//8
    return 8*m+1<=min(u,v)<=max(u,v)<=8*m+7,m


def R_contract(A,B):
    return leader_contract(A,B)[0] and 7<=(17*A+12*B)%56<=49 and 7<=(18*A+9*B)%56<=49


def W_contract(A,B):
    u,v=49*A+42*B,55*A+24*B;n=min(u,v)//168
    return leader_contract(A,B)[0] and 168*n+21<=min(u,v)<=max(u,v)<=168*n+147,n


def old_contract(A,B):
    u,v=2*A+3*B,3*A+B;m=min(u,v)//8
    return 8*m+1<=min(u,v)<=max(u,v)<=8*m+7 and (A+2*B)%8!=0


def analytic_failure(A,B):
    delta=A-B;D=abs(delta);a=(9*B+2*delta)%8
    assert D>=14 and 1<=a<=7
    c=7-a if delta>0 else a-1
    assert 1<=c<=6
    lower=(F(7*D,c+2)-1)/4;upper=(F(7*D,c)-1)/4;j=floor(lower)+1
    assert lower<j<upper and j>=3
    w=physical(A,B,1,4*j)
    assert not w['seventh_safe'] and w['distinct_speeds']
    return dict(construction=pack(dict(delta=delta,c=c,j=j,open_j_interval=[lower,upper])),witness=w)


def main():
    if not __debug__:raise RuntimeError('Run without -O')
    pins=json.loads((HERE/'INPUTS.json').read_text())
    for path,s in pins['files'].items():assert digest(ROOT/path)==s['sha256'],path
    assert digest(HERE/'PROTOCOL.md')==pins['protocol_sha256']
    provenance=dict(source_commit=pins['source_commit'],protocol_sha256=pins['protocol_sha256'],
                    script_sha256=digest(Path(__file__)),input_record_sha256=digest(HERE/'INPUTS.json'))
    directions=[point(P,M-P) for M in range(2,92) for P in range(1,M) if gcd(P,M)==1]
    primary=[c for c in directions if c['pair'][0]!=c['pair'][1]]
    support=dict(provenance=provenance,directions=directions,counts=dict(
        primitive_directions=len(directions),primary_directions=len(primary),
        distinct_leader_points=len({tuple(c['point']) for c in directions if c['role']=='L'})))
    save('support.json',support,True)
    fast=[]
    for c in primary:
        x,y=c['point'];den=lcm(x.denominator,y.denominator)
        fast.append((int(x*den),int(y*den),den))
    cells=[];auxiliary=[];total_failures=0
    for delta in range(-13,14):
        failures=[]
        for b in range(56):
            B=b+56;A=B+delta;a=(9*B+2*delta)%8
            tail=a!=0 and not(delta>0 and a==7) and not(delta<0 and a==1)
            first=None;bad=0
            for i,(x,y,den) in enumerate(fast):
                r=(A*x+B*y)%den
                if not den<=8*r<=7*den:
                    bad+=1
                    if first is None:first=i
            assert tail or first is not None
            t=tail and first is None;ta=t and (A+B)%8!=0
            cell=dict(delta=delta,B_mod56=b,representative=[A,B],left_residue=a,tail_safe=tail,
                      T=t,T_all=ta,R=R_contract(A,B),finite_primary_failures=bad,
                      first_failure_pair=primary[first]['pair'] if first is not None else None)
            cells.append(cell)
            if not t:
                w=physical(A,B,*cell['first_failure_pair'])
                assert not w['seventh_safe'] and w['distinct_speeds']
                failures.append(dict(delta=delta,B_mod56=b,**w))
            if t and not ta:
                w=physical(A,B,1,1);assert not w['seventh_safe'] and not w['distinct_speeds']
                auxiliary.append(dict(delta=delta,B_mod56=b,**w))
        total_failures+=len(failures)
        save('failures/delta_'+('m'+str(-delta) if delta<0 else 'p'+str(delta))+'.json',failures,True)
    accepted={d:[c['B_mod56'] for c in cells if c['delta']==d and c['T']] for d in range(-13,14)}
    counts=dict(cells=len(cells),T=sum(c['T'] for c in cells),T_all=sum(c['T_all'] for c in cells),
                R=sum(c['R'] for c in cells),outside_R=sum(c['T'] and not c['R'] for c in cells),
                primary_failures=total_failures,auxiliary_failures=len(auxiliary))
    classification=dict(status='PASS',provenance=provenance,cells=cells,counts=counts,
        accepted_B_residues_by_delta=accepted,
        T_all_accepted_B_residues_by_delta={d:[c['B_mod56'] for c in cells if c['delta']==d and c['T_all']] for d in range(-13,14)},
        T_equals_R=all(c['T']==c['R'] for c in cells),T_all_equals_T=all(c['T_all']==c['T'] for c in cells),
        identically_repeated_core_rows=list(CORE[2:]))
    save('classification.json',classification,True);save('auxiliary_failures.json',auxiliary,True)
    whole=[]
    for B in range(1,14):
        for delta in range(-6,7):
            A=B+delta
            if A<1:continue
            ok,n=W_contract(A,B)
            whole.append(dict(A=A,B=B,delta=delta,W=ok,R=R_contract(A,B),
                              leader_lap=leader_contract(A,B)[1],fallback_lap=n))
    save('whole_segments.json',dict(cases=whole,accepted_rows=[[c['A'],c['B']] for c in whole if c['W']],
                                   counts=dict(cases=len(whole),accepted=sum(c['W'] for c in whole))))
    indexed={(c['delta'],c['B_mod56']):c for c in cells}
    def new_contract(A,B):
        return abs(A-B)<=13 and indexed[(A-B,B%56)]['T']
    archived=json.loads((ROOT/'reviews/2026-09-29-cc-selector-support/classification.json').read_text())
    assert all(old_contract(*c['representative'])==c['T'] for c in archived['cells'])
    comparison=[]
    for B in range(1,20):
        for delta in range(-13,14):
            A=B+delta
            if A>0:comparison.append(dict(row=[A,B],old=old_contract(A,B),new=new_contract(A,B)))
    overlap=[c['row'] for c in comparison if c['old'] and c['new']]
    save('comparison.json',dict(cases=comparison,intersection=overlap,counts=dict(
        cases=len(comparison),intersection=len(overlap),old_archive_cells_checked=len(archived['cells'])),
        old_only_progression=dict(base=[6,2],step=[16,8],k_min=2,new_delta='4+8k'),
        new_only_progression=dict(base=[3,8],step=[56,56],k_min=0,old_delta='-13-56k')))
    physical_controls=[physical(A,B,p,q) for A,B in ((3,8),(59,64),(6,2)) for p,q in PAIRS]
    physical_controls += [physical(A,B,2,3) for A,B in CORE[2:]]
    oldrun=json.loads((ROOT/'reviews/2026-09-29-cc-row38-transfer/run.json').read_text())
    common=('pair','primitive','gcd','point','h','primitive_time','time','speeds','phases',
            'torus_laps','physical_laps','reflected_time','reflected_phases','reflected_laps','minimum','distinct_speeds')
    for w,old in zip(physical_controls[:18],oldrun['controls']):
        assert all(w[k]==old[k] for k in common)
    for w,lift in zip(physical_controls[:18],physical_controls[18:36]):
        assert all(w[k]==lift[k] for k in ('pair','point','time','phases','reflected_phases','minimum'))
        shift={'L':63,'F':29,'G':27,'C':14}[w['role']]
        assert lift['torus_laps'][6]-w['torus_laps'][6]==shift
        assert lift['physical_laps'][6]-w['physical_laps'][6]==int(56*sum(w['pair'])*F(w['time']))
    large=[]
    for delta in (-14,14,-15,15,-(10**12+14),10**12+14):
        D=abs(delta);b=(2-2*delta)%8;B=8*(D//8+1)+b;A=B+delta
        assert (9*B+2*delta)%8==2
        large.append(analytic_failure(A,B))
    oldonly=analytic_failure(38,18)
    spec=importlib.util.spec_from_file_location('pinned_old_checker',ROOT/'lonely_runner/cc_coefficients.py')
    oldapi=importlib.util.module_from_spec(spec);spec.loader.exec_module(oldapi)
    oldw=oldapi.evaluate_selector(38,18,*oldonly['witness']['pair'])
    assert old_contract(38,18) and oldw['seventh_safe']
    additional=[]
    outsider=next((c for c in cells if c['T'] and not c['R']),None)
    if outsider:
        additional=[physical(*outsider['representative'],p,q) for p,q in PAIRS]
    A,B=59,64;lo=F(7,24);hi=F(55,168)
    endpoint_values=[(A-3*B)*x+F(9*B,8) for x in (lo,hi)]
    integer=ceil(min(endpoint_values));x=(integer-F(9*B,8))/(A-3*B);y=F(9,8)-3*x
    assert min(endpoint_values)<=integer<=max(endpoint_values) and lo<x<hi
    assert not W_contract(A,B)[0] and R_contract(A,B) and new_contract(A,B)
    ambient=dict(row=[A,B],point=[x,y],seventh_raw=integer,seventh_phase=0,
                 all_core_safe=all(safe(a*x+b*y) for a,b in CORE),strictly_inside_S=True,
                 scope='Ambient whole-S failure, not asserted to be a selected physical output')
    assert ambient['all_core_safe']
    controls=dict(physical_controls=physical_controls,large_slope_controls=large,
        old_only=dict(new_failure=oldonly['witness'],old_witness=oldw,construction=oldonly['construction']),
        conditional_outside_R=additional,ambient_fallback_failure=ambient,
        archive_fields_compared=18*len(common),phase_period_pairs_compared=18,
        counts=dict(physical_controls=len(physical_controls),large_slope_controls=len(large),old_only_pairs=1,
                    conditional_outside_R=len(additional)))
    save('controls.json',controls)
    print(json.dumps(dict(status='PASS',support=pack(support['counts']),classification=counts,
        T_equals_R=classification['T_equals_R'],T_all_equals_T=classification['T_all_equals_T'],
        whole_accepted=sum(c['W'] for c in whole),intersection=overlap,controls=controls['counts'])))


if __name__=='__main__':main()
