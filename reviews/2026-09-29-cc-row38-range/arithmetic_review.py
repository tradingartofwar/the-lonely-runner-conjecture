#!/usr/bin/env python3
"""Separate finite arithmetic review; direct contacts and forbidden-band tests.

No production code is imported. JSON is deterministic and written to stdout.
Run with --compare once all four coordinator classification files exist.
"""
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SEGMENTS = [
    ('L', ((F(1,4),F(7,8)),(F(3,8),F(3,4)))),
    ('S', ((F(7,24),F(1,4)),(F(55,168),F(1,7)))),
    ('C', ((F(1,8),F(1,8)),(F(1,8),F(3,16)))),
]
CORE = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2)]


def check(value, detail):
    if not value:
        raise ArithmeticError(detail)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe(v):
    return F(1,8) <= v % 1 <= F(7,8)


def safe_integer(numerator, denominator):
    r = numerator % denominator
    return denominator <= 8*r <= 7*denominator


def whole(a,b):
    """Reject intersections with open forbidden neighborhoods of integers."""
    lo,hi = sorted([a,b])
    for n in range(floor(lo)-1,floor(hi)+2):
        if hi > n-F(1,8) and lo < n+F(1,8):
            return False
    return True


def select(P,Q):
    check(P>0 and Q>0 and gcd(P,Q)==1, 'primitive domain')
    M=P+Q
    for role,(start,end) in SEGMENTS:
        v0=Q*start[0]-P*start[1]
        v1=Q*end[0]-P*end[1]
        lo,hi=sorted([v0,v1])
        h=ceil(lo)
        if h>hi:
            continue
        check(v0!=v1,'nonconstant projections on these positive directions')
        t=F(h-v0,v1-v0)
        x=start[0]+t*(end[0]-start[0])
        y=start[1]+t*(end[1]-start[1])
        check(Q*x-P*y==h,'contact equation')
        check(all(safe(a*x+b*y) for a,b in CORE),'first-six safety')
        den=x.denominator*y.denominator//gcd(x.denominator,y.denominator)
        xn=int(x*den);yn=int(y*den)
        rho=(P-2*M)%8
        if role=='L':
            check(x==F(1,4)+F(rho,8*M),'direct/residue point agreement')
        if role=='S':
            role='F' if (P,Q)==(1,4) else 'G'
        return dict(pair=[P,Q],M=M,rho=rho,role=role,h=h,
                    interval=[str(lo),str(hi)],point=[str(x),str(y)],
                    x_num=xn,y_num=yn,denominator=den,
                    auxiliary=P==Q)
    raise ArithmeticError('frozen menu missed a direction')


def R(A,B):
    return (whole(F(2*A+7*B,8),F(3*A+6*B,8))
            and safe(F(17*A+12*B,56)) and safe(F(18*A+9*B,56)))


def old(A,B):
    return (whole(F(2*A+3*B,8),F(3*A+B,8)) and safe(F(A+2*B,8)))


def main(compare=False):
    support=[]
    for M in range(2,92):
        for P in range(1,M):
            Q=M-P
            if gcd(P,Q)==1:
                support.append(select(P,Q))
    check([s['pair'] for s in support if s['role']!='L']==[[1,1],[2,1],[1,4]],
          'only three off-leader primitive directions, in M/P order')
    primary=[s for s in support if not s['auxiliary']]
    cells=[];accepted=[];accepted_all=[];accepted_R=[]
    for delta in range(-13,14):
        for b in range(56):
            B=b+56;A=B+delta
            a=(2*A+7*B)%8
            tail=(a!=0 and not(delta>0 and a==7) and not(delta<0 and a==1))
            failures=[]
            for s in primary:
                if not safe_integer(A*s['x_num']+B*s['y_num'],s['denominator']):
                    failures.append(s['pair'])
            check(failures or tail,'tail rejection has finite primary witness')
            T=tail and not failures
            aux=safe(F(A+B,8))
            Tall=T and aux
            geometric=R(A,B)
            c=dict(delta=delta,B_mod56=b,representative=[A,B],left_residue=a,
                   tail_safe=tail,T=T,T_all=Tall,R=geometric,
                   auxiliary_safe=aux,finite_primary_failures=len(failures),
                   first_failure_pair=failures[0] if failures else None)
            cells.append(c)
            if T:accepted.append([delta,b])
            if Tall:accepted_all.append([delta,b])
            if geometric:accepted_R.append([delta,b])
    cellmap={(c['delta'],c['B_mod56']):c for c in cells}
    def new(A,B):
        return (-13<=A-B<=13 and cellmap[(A-B,B%56)]['T'])
    w_cases=[];w_rows=[]
    for B in range(1,14):
        for delta in range(-6,7):
            A=B+delta
            if A<1:continue
            leader=whole(F(2*A+7*B,8),F(3*A+6*B,8))
            fallback=whole(F(7*A+6*B,24),F(55*A+24*B,168))
            W=leader and fallback
            c=dict(A=A,B=B,delta=delta,W=W,R=R(A,B),
                   leader_safe=leader,whole_fallback_safe=fallback)
            c['leader_lap']=floor(min(F(2*A+7*B,8),F(3*A+6*B,8)))
            c['fallback_lap']=floor(min(F(7*A+6*B,24),F(55*A+24*B,168)))
            check(not W or c['R'],'W implies R at declared row')
            if W:
                w_rows.append([A,B])
            w_cases.append(c)
    overlap_cases=[];intersection=[]
    for B in range(1,20):
        for delta in range(-13,14):
            A=B+delta
            if A<1:continue
            c=dict(row=[A,B],old=old(A,B),new=new(A,B))
            overlap_cases.append(c)
            if c['old'] and c['new']:intersection.append([A,B])
    old_archive=json.loads((ROOT/'reviews/2026-09-29-cc-selector-support/classification.json').read_text())
    old_checked=0
    for c in old_archive['cells']:
        B=c['B_mod8']+8;A=2*B+c['delta']
        check(old(A,B)==c['R'],'old predicate versus archived complete table')
        old_checked+=1
    check(old(6,2),'old progression anchor')
    check(R(3,8),'new progression anchor')
    check(all(not new(*row) for row in [[38,18]]),'old-only frozen anchor')
    comparisons={}
    if compare:
        prod=json.loads((HERE/'support.json').read_text())
        # Field adapters are named explicitly rather than inferring equality from count.
        prodmap={tuple(s['pair']):s for s in prod['directions']}
        check(len(prodmap)==len(support),'support direction count')
        count=0
        for c in support:
            p=prodmap[tuple(c['pair'])]
            for k in ['pair','M','rho','h','point','role']:
                check(c[k]==p[k],f'support {c["pair"]} {k}')
                count+=1
        check(prod['counts']==dict(distinct_leader_points=len({tuple(s['point']) for s in support if s['role']=='L'}),primary_directions=len(primary),primitive_directions=len(support)),'support counts')
        comparisons['support_fields']=count
        comparisons['support_count_fields']=3
        prod=json.loads((HERE/'classification.json').read_text())
        prodmap={(c['delta'],c['B_mod56']):c for c in prod['cells']}
        check(len(prodmap)==len(cells),'coefficient cell count')
        count=0
        fields=['delta','B_mod56','representative','left_residue','tail_safe','T','T_all','R',
                'finite_primary_failures','first_failure_pair']
        for c in cells:
            p=prodmap[(c['delta'],c['B_mod56'])]
            for k in fields:
                check(c[k]==p[k],f'coefficient {(c["delta"],c["B_mod56"])} {k}')
                count+=1
        for field,table in [('accepted_B_residues_by_delta',accepted),('T_all_accepted_B_residues_by_delta',accepted_all)]:
            check(prod[field]=={str(d):[b for a,b in table if a==d] for d in range(-13,14)},field)
        check(prod['T_equals_R']==(accepted==accepted_R),'T=R flag')
        check(prod['T_all_equals_T']==(accepted==accepted_all),'T_all=T flag')
        check(prod['identically_repeated_core_rows']==[[1,1],[2,1],[3,1],[3,2]],'identical core repeats')
        check(prod['counts']==dict(R=len(accepted_R),T=len(accepted),T_all=len(accepted_all),auxiliary_failures=len(accepted)-len(accepted_all),cells=len(cells),outside_R=len(set(map(tuple,accepted))-set(map(tuple,accepted_R))),primary_failures=len(cells)-len(accepted)),'classification counts')
        comparisons['classification_fields']=count
        comparisons['classification_summary_fields']=64
        prod=json.loads((HERE/'whole_segments.json').read_text())
        prodmap={(c['A'],c['B']):c for c in prod['cases']}
        check(len(prodmap)==len(w_cases),'whole segment case count')
        count=0
        for c in w_cases:
            p=prodmap[(c['A'],c['B'])]
            for k in ['A','B','delta','W','R','leader_lap','fallback_lap']:
                check(c[k]==p[k],f'whole segment {(c["A"],c["B"])} {k}')
                count+=1
        check(prod['accepted_rows']==w_rows,'all W rows in declared order')
        check(prod['counts']==dict(accepted=len(w_rows),cases=len(w_cases)),'whole segment counts')
        comparisons['whole_segment_fields']=count
        comparisons['whole_segment_summary_fields']=3
        prod=json.loads((HERE/'comparison.json').read_text())
        prodmap={tuple(c['row']):c for c in prod['cases']}
        check(len(prodmap)==len(overlap_cases),'comparison case count')
        count=0
        for c in overlap_cases:
            p=prodmap[tuple(c['row'])]
            for k in ['row','old','new']:
                check(c[k]==p[k],f'comparison {c["row"]} {k}')
                count+=1
        check(prod['intersection']==intersection,'complete old/new intersection in declared order')
        check(prod['counts']==dict(cases=len(overlap_cases),intersection=len(intersection),old_archive_cells_checked=old_checked),'old/new counts')
        check(prod['new_only_progression']==dict(base=[3,8],k_min=0,old_delta='-13-56k',step=[56,56]),'new-only progression')
        check(prod['old_only_progression']==dict(base=[6,2],k_min=2,new_delta='4+8k',step=[16,8]),'old-only progression')
        comparisons['old_new_fields']=count
        comparisons['old_new_summary_fields']=12
    result=dict(
        status='PASS',
        method='Direct segment projection and first integer; open forbidden-band intersection; integer residue arithmetic; no production imports',
        scope='Frozen complete reductions; internally reviewed proof candidate, no human or formal proof certification',
        hashes={str(p.relative_to(ROOT)):digest(p) for p in [HERE/'PROTOCOL.md',Path(__file__),ROOT/'reviews/2026-09-29-cc-selector-support/classification.json']},
        counts=dict(directions=len(support),primary_directions=len(primary),leader_directions=sum(s['role']=='L' for s in support),
                    unique_leader_points=len({tuple(s['point']) for s in support if s['role']=='L'}),
                    coefficient_cells=len(cells),T=len(accepted),T_all=len(accepted_all),R=len(accepted_R),
                    rejected_T=len(cells)-len(accepted),T_without_T_all=len(set(map(tuple,accepted))-set(map(tuple,accepted_all))),
                    W_cases=len(w_cases),W=len(w_rows),comparison_cases=len(overlap_cases),intersection=len(intersection),old_archive_cells=old_checked),
        identities=dict(T_equals_R=accepted==accepted_R,T_equals_T_all=accepted==accepted_all),
        coordinator_comparison=comparisons,
        accepted_classes=accepted,accepted_T_all_classes=accepted_all,accepted_R_classes=accepted_R,
        W_rows=w_rows,intersection=intersection,
        cells=cells,whole_segment_cases=w_cases,old_new_cases=overlap_cases,support=support)
    print(json.dumps(result,sort_keys=True,separators=(',',':')))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--compare',action='store_true')
    args=p.parse_args()
    main(args.compare)
