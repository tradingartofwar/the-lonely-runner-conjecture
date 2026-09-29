#!/usr/bin/env python3
"""Internal AI upper-bound review; no imports from original proof package.

Input is the note's printed finite cell table, not its adjacency or audit files.
Reconstruct adjacency from common active facet rank, and certify inequalities
symbolically on entire unbounded residue domains. This is not a new q scan or
an independent completeness proof for the supplied vertex table.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
A = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2)]
LABELS = [
    (0,0,0,0,0,0,0), (0,0,0,0,0,0,1), (0,0,0,0,0,1,1),
    (0,0,0,0,1,1,2), (0,0,0,1,1,1,2), (0,0,0,1,1,2,2),
    (0,0,0,1,1,2,3), (0,0,1,1,1,2,3), (0,0,1,1,2,2,3),
    (0,0,1,1,2,3,4),
]
RAW_VERTICES = [
    [('1/8','1/8','1/8')],
    [('1/8','1/4','1/8'),('1/6','1/6','1/6'),('7/40','1/8','1/8'),('5/24','1/8','1/8')],
    [('1/8','3/8','1/8'),('1/8','1/2','1/8'),('1/6','1/3','1/6'),('5/24','1/4','1/8')],
    [('3/8','1/8','1/8')],
    [('3/8','3/8','1/8'),('1/2','1/8','1/8'),('1/2','1/6','1/6'),('1/2','3/16','1/8')],
    [('3/8','1/2','1/8')],
    [('11/24','5/12','1/8'),('1/2','5/16','1/8'),('1/2','1/3','1/6'),('1/2','3/8','1/8')],
    [('11/40','7/8','1/8'),('2/7','6/7','1/7'),('7/24','5/6','1/8'),('1/3','5/6','1/6'),('1/3','7/8','1/8'),('3/8','3/4','1/8')],
    [('11/24','3/4','1/8'),('1/2','5/8','1/8'),('1/2','2/3','1/6'),('1/2','11/16','1/8')],
    [('19/40','7/8','1/8'),('1/2','13/16','1/8'),('1/2','5/6','1/6'),('1/2','7/8','1/8')],
]
VERTICES = [[tuple(map(F,p)) for p in cell] for cell in RAW_VERTICES]
PEAK_NAMES = {1:'A', 2:'B', 4:'C', 6:'D', 7:'E', 8:'F', 9:'G'}
EXPECTED_DIRECTIONS = {
    'A':[('-1','2'),('1/5','-1'),('1','-1')],
    'B':[('-1','1'),('-1','4'),('1','-2')],
    'C':[('-3','5'),('0','-1'),('0','1/2')],
    'D':[('-1','2'),('0','-1/2'),('0','1')],
    'E':[('-2','1'),('0','1'),('1','-2')],
    'F':[('-1','2'),('0','-1'),('0','1/2')],
    'G':[('-3/5','1'),('0','-1/2'),('0','1')],
}

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def rank(rows):
    rows = [list(map(F,r)) for r in rows]
    k = 0
    for col in range(3):
        pivot = next((i for i in range(k,len(rows)) if rows[i][col]),None)
        if pivot is None:
            continue
        rows[k],rows[pivot] = rows[pivot],rows[k]
        div = rows[k][col]
        rows[k] = [v/div for v in rows[k]]
        for i in range(len(rows)):
            if i != k:
                f = rows[i][col]
                rows[i] = [u-f*v for u,v in zip(rows[i],rows[k])]
        k += 1
    return k

def facets(m):
    # Convention normal dot point <= bound.
    out = [((F(0),F(0),F(-1)),F(-1,8)), ((F(1),F(0),F(0)),F(1,2))]
    for (a,b),lap in zip(A,m):
        out.extend([((-F(a),-F(b),F(1)),-F(lap)), ((F(a),F(b),F(1)),F(lap+1))])
    return out

def frac(x):
    return x-x.numerator//x.denominator

def encode(obj):
    if isinstance(obj,F): return str(obj)
    if isinstance(obj,tuple): return [encode(v) for v in obj]
    if isinstance(obj,list): return [encode(v) for v in obj]
    if isinstance(obj,dict): return {str(k):encode(v) for k,v in obj.items()}
    return obj

def main():
    edges = []
    peak_edges = []
    cell_checks = []
    for cell,(m,vs) in enumerate(zip(LABELS,VERTICES)):
        fs = facets(m)
        active = []
        for p in vs:
            assert all(dot(n,p)<=b for n,b in fs)
            ap = {i for i,(n,b) in enumerate(fs) if dot(n,p)==b}
            assert rank([fs[i][0] for i in ap]) == 3
            active.append(ap)
        dim = rank([tuple(x-y for x,y in zip(p,vs[0])) for p in vs[1:]])
        assert dim == (0 if len(vs)==1 else 3)
        count = 0
        for i,j in combinations(range(len(vs)),2):
            common = active[i]&active[j]
            if rank([fs[k][0] for k in common]) != 2:
                continue
            count += 1
            edges.append({'cell':cell,'p':vs[i],'q':vs[j]})
            if max(vs[i][2],vs[j][2]) == F(1,6):
                p,r = sorted((vs[i],vs[j]),key=lambda v:v[2],reverse=True)
                loss = p[2]-r[2]
                assert loss>0
                alpha,beta = [(r[k]-p[k])/loss for k in (0,1)]
                # The affine projection has a uniform, nonzero sign on q>=2.
                a,b = alpha,-beta
                sign = 1 if 2*a+b>0 else -1
                assert sign*a>=0 and sign*(2*a+b)>0
                peak_edges.append({'cell':cell,'name':PEAK_NAMES[cell],
                    'peak':p,'endpoint':r,'alpha':alpha,'beta':beta,
                    'emax':loss,'projection_sign':sign,
                    'projection_abs_coefficients':(sign*a,sign*b),
                    'projection_abs_at_q2':sign*(2*a+b)})
        cell_checks.append({'cell':cell,'dimension':dim,'vertices':len(vs),'edges':count})
    assert len(edges)==45 and len(peak_edges)==21
    assert sum(len(v) for v in VERTICES)==33
    peaks = [p for vs in VERTICES for p in vs if p[2]==F(1,6)]
    assert len(peaks)==7
    assert max(p[2] for vs in VERTICES for p in vs if p[2]!=F(1,6))==F(1,7)
    for name,expected in EXPECTED_DIRECTIONS.items():
        got = {(e['alpha'],e['beta']) for e in peak_edges if e['name']==name}
        assert got == {tuple(map(F,d)) for d in expected}
    for e in peak_edges:
        assert e['emax']==(F(1,42) if (e['name'],e['alpha'],e['beta'])==('E',F(-2),F(1)) else F(1,24))

    # d_i(q)=n_i/(a_i*q+b_i), with all denominators positive on q>=2.
    # Four unbounded residue domains, no parameter sweep.
    domains = [(0,6,'E',F(-2),F(1)),(3,3,'E',F(-2),F(1)),
               (4,10,'E',F(-2),F(1)),(5,5,'C',F(-3),F(5))]
    certificates = []
    domain_checks = []
    for residue,qmin,win_name,win_alpha,win_beta in domains:
        losses = []
        for edge in peak_edges:
            p = edge['peak']
            # 6*x0 integral guarantees fractional part constant modulo six.
            assert (6*p[0]).denominator==1
            rho = frac(residue*p[0]-p[1])
            assert 0<rho<1
            n = rho if edge['projection_sign']<0 else 1-rho
            a,b = edge['projection_abs_coefficients']
            losses.append((edge,rho,n,a,b))
        winner = next(t for t in losses if (t[0]['name'],t[0]['alpha'],t[0]['beta'])==(win_name,win_alpha,win_beta))
        _,_,nw,aw,bw = winner
        ties = []
        for edge,rho,n,a,b in losses:
            # d_i >= d_win iff this linear polynomial is nonnegative.
            slope = n*aw-nw*a
            intercept = n*bw-nw*b
            at_min = slope*qmin+intercept
            assert slope>=0 and at_min>=0
            row = {'residue':residue,'qmin':qmin,'peak':edge['name'],
                   'direction':(edge['alpha'],edge['beta']),'rho':rho,
                   'loss_numerator':n,'loss_denominator_coefficients':(a,b),
                   'comparison_slope':slope,'comparison_intercept':intercept,
                   'comparison_at_qmin':at_min}
            certificates.append(row)
            if at_min==0:
                loss = n/(a*qmin+b)
                point = (edge['peak'][0]+edge['alpha']*loss,
                         edge['peak'][1]+edge['beta']*loss,F(1,6)-loss)
                h = qmin*point[0]-point[1]
                assert h.denominator==1
                ties.append({'peak':edge['name'],'direction':(edge['alpha'],edge['beta']),
                             'e':loss,'emax':edge['emax'],'within_edge':loss<=edge['emax'],
                             'point':point,'h':h})
        # Explicit domain-wide feasibility of winning ray's first integer.
        # e(q) decreases, so the left endpoint is the worst finite-length case.
        emax = winner[0]['emax']
        assert aw>0 and nw/(aw*qmin+bw)<=emax
        # Each resulting upper bound is >=1/7 over the entire domain.
        assert nw/(aw*qmin+bw)<=F(1,42)
        domain_checks.append({'residue':residue,'qmin':qmin,
            'winner':win_name,'winner_loss':(nw,aw,bw),'winner_edge_emax':emax,
            'upper_bound_at_qmin':F(1,6)-nw/(aw*qmin+bw),
            'boundary_ties':ties})
    assert len(certificates)==84

    # Residues with an actual ambient peak: all peak congruences, not only A/B.
    integral_peaks = {}
    for residue in range(6):
        integral_peaks[residue] = [PEAK_NAMES[cell] for cell,vs in enumerate(VERTICES)
            for p in vs if p[2]==F(1,6) and (residue*p[0]-p[1]).denominator==1]
    assert integral_peaks == {0:[],1:['A'],2:['B'],3:[],4:[],5:[]}

    # Exceptional q=4 upper bound from all vertices, preserving extremal faces.
    q4 = []
    for cell,vs in enumerate(VERTICES):
        hv = [4*p[0]-p[1] for p in vs]
        lo,hi = min(hv),max(hv)
        integers = list(range(-((-lo.numerator)//lo.denominator),hi.numerator//hi.denominator+1))
        witnesses = []
        for h in integers:
            assert h in (lo,hi)
            points = [p for p,val in zip(vs,hv) if val==h]
            assert len(points)==1 and points[0][2]==F(1,8)
            witnesses.extend(points)
        q4.append({'cell':cell,'H_range':(lo,hi),'integer_levels':integers,'points':witnesses})
    assert [(r['cell'],r['integer_levels']) for r in q4 if r['integer_levels']] == [(2,[0]),(5,[1])]

    # No original audit.py or generated JSON was read/imported by this program.
    report = {'status':'PASS; internal AI review conditional on printed-cell completeness',
        'candidate_frozen_commit':'8a967b30fcd73abd814e4c8f7f53f216c4b3f61e',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'cell_checks':cell_checks,'edge_count':len(edges),'peak_count':len(peaks),
        'peak_edges':peak_edges,'integral_peak_residues':integral_peaks,
        'certificate_count':len(certificates),'certificates':certificates,
        'domain_checks':domain_checks,'q4_cell_ranges':q4,
        'scope':'Fixed printed cell certificate; 84 universal rational inequalities; q4 exception. No physical optimum scan.'}
    out = Path(__file__).with_suffix('.json')
    out.write_text(json.dumps(encode(report),indent=2)+'\n')
    print(json.dumps({'status':'PASS','edges':len(edges),'peak_edges':len(peak_edges),
                      'symbolic_certificates':len(certificates),'output':str(out)},indent=2))

if __name__=='__main__':
    main()
