#!/usr/bin/env python3
"""Exact fixed-cell and symbolic upper-bound audit for V(q,1), q>=2.

Print JSON; do not write files. Geometry is reconstructed from 48 global planes.
No original geometry or upper-bound program is imported. The previous witness
module supplies its explicitly declared symbolic lower-bound certificates.
The same AI coordinator read the earlier programs; this is not external review.
"""
from fractions import Fraction as F
from hashlib import sha256, sha1
from itertools import combinations
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
BASE = "44bd7854cd14c15cc52d991a0c61a22295af1234"
ROWS = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2))
PEAK_NAMES = {
    (F(1,6),F(1,6)): "A", (F(1,6),F(1,3)): "B",
    (F(1,2),F(1,6)): "C", (F(1,2),F(1,3)): "D",
    (F(1,3),F(5,6)): "E", (F(1,2),F(2,3)): "F",
    (F(1,2),F(5,6)): "G",
}
DOMAINS = ((0,6,"B",F(-1),F(4)), (2,2,"C",F(-3),F(5)),
           (5,5,"F",F(-1),F(2)))
LOCAL_WINNERS = {
    0: {"A":(-1,2),"B":(-1,4),"C":(-3,5),"D":(-1,2),
        "E":(-2,1),"F":(-1,2),"G":(-F(3,5),1)},
    2: {"A":(1,-1),"B":(-1,4),"C":(-3,5),"D":(0,-F(1,2)),
        "E":(1,-2),"F":(-1,2),"G":(0,-F(1,2))},
    5: {"A":(-1,2),"B":(-1,4),"C":(-3,5),"D":(0,-F(1,2)),
        "E":(-2,1),"F":(-1,2),"G":(-F(3,5),1)},
}


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def eliminate(rows, columns=3):
    matrix = [list(map(F,row)) for row in rows]
    pivot_row = 0
    for col in range(columns):
        pivot = next((i for i in range(pivot_row,len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][col]
        matrix[pivot_row] = [x/divisor for x in matrix[pivot_row]]
        for i in range(len(matrix)):
            if i != pivot_row:
                factor = matrix[i][col]
                matrix[i] = [x-factor*y for x,y in zip(matrix[i],matrix[pivot_row])]
        pivot_row += 1
    return pivot_row, matrix


def fractional(value):
    return value-value.numerator//value.denominator


def facets(labels):
    out = [(F(1),F(0),F(0),F(1,2)), (F(0),F(0),F(-1),F(-1,8))]
    for (a,b),m in zip(ROWS,labels):
        out.extend([(-F(a),-F(b),F(1),-F(m)), (F(a),F(b),F(1),F(m+1))])
    return out


def geometry():
    planes = [(1,0,0,F(1,2)), (0,0,1,F(1,8))]
    for a,b in ROWS:
        for m in range(a+b):
            planes.extend([(a,b,-1,m), (a,b,1,m+1)])
    assert len(planes) == 48
    found = {}
    triples = 0
    for triple in combinations(planes,3):
        triples += 1
        rank, matrix = eliminate(triple)
        if rank != 3:
            continue
        p = tuple(row[3] for row in matrix)
        x,y,z = p
        if not (F(1,8) <= z <= x <= F(1,2) and z <= y <= 1-z):
            continue
        forms = [a*x+b*y for a,b in ROWS]
        if not all(z <= fractional(u) <= 1-z for u in forms):
            continue
        labels = tuple(u.numerator//u.denominator for u in forms)
        found.setdefault(labels,set()).add(p)
    cells, peak_edges = [], []
    for labels, points in sorted(found.items()):
        vs = sorted(points)
        fs = facets(labels)
        active = []
        for p in vs:
            assert all(dot(f[:3],p) <= f[3] for f in fs)
            ids = {i for i,f in enumerate(fs) if dot(f[:3],p) == f[3]}
            assert eliminate([fs[i][:3] for i in ids])[0] == 3
            active.append(ids)
        dimension = eliminate([tuple(x-y for x,y in zip(p,vs[0])) for p in vs[1:]])[0]
        assert dimension == (0 if len(vs)==1 else 3)
        edges = []
        for i,j in combinations(range(len(vs)),2):
            common = active[i] & active[j]
            if eliminate([fs[k][:3] for k in common])[0] != 2:
                continue
            edges.append((i,j))
            if max(vs[i][2],vs[j][2]) != F(1,6):
                assert max(vs[i][2],vs[j][2]) <= F(1,7)
                continue
            peak, endpoint = sorted((vs[i],vs[j]),key=lambda p:p[2],reverse=True)
            emax = peak[2]-endpoint[2]
            assert emax > 0
            alpha,beta = [(endpoint[k]-peak[k])/emax for k in (0,1)]
            a,b = -beta,alpha  # H change is (a*q+b)*e, H=x-q*y.
            sign = 1 if 2*a+b > 0 else -1
            assert sign*a >= 0 and sign*(2*a+b) > 0
            peak_edges.append({"name":PEAK_NAMES[peak[:2]],"peak":peak,
                "direction":(alpha,beta),"emax":emax,"projection_sign":sign,
                "abs_projection":(sign*a,sign*b),"labels":labels})
        cells.append({"labels":labels,"vertices":vs,"edges":edges,"dimension":dimension})
    assert len(cells)==10 and sum(len(c['vertices']) for c in cells)==33
    assert sum(len(c['edges']) for c in cells)==45 and len(peak_edges)==21
    assert sum(c['dimension']==0 for c in cells)==3
    all_vertices = [p for c in cells for p in c['vertices']]
    assert max(p[2] for p in all_vertices)==F(1,6)
    assert max(p[2] for p in all_vertices if p[2] < F(1,6))==F(1,7)
    assert set(p[:2] for p in all_vertices if p[2]==F(1,6))==set(PEAK_NAMES)
    return cells,peak_edges,triples


def compare_archive(cells):
    path = ROOT/'reviews/2026-09-29-ltcm-spectrum/ambient.json'
    data = path.read_bytes()
    blob = sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob == '0d2b6da07b31adb119eea9de3ea8dd2ba2524498'
    old = json.loads(data)
    assert len(cells)==len(old)
    for new, archived in zip(cells,old):
        av = [tuple(map(F,p)) for p in archived['vertices']]
        assert tuple(archived['m']) == new['labels']
        assert set(av)==set(new['vertices'])
        old_edges = {tuple(sorted((av[i],av[j]))) for i,j in archived['edges']}
        new_edges = {tuple(sorted((new['vertices'][i],new['vertices'][j]))) for i,j in new['edges']}
        assert old_edges==new_edges
    return {"git_blob":blob,"cells_vertices_edges_match":True}


def loss(edge, residue):
    x,y,_ = edge['peak']
    assert (6*y).denominator==1
    rho = fractional(x-residue*y)
    assert 0 < rho < 1
    numerator = rho if edge['projection_sign'] < 0 else 1-rho
    return {"edge":edge,"rho":rho,"numerator":numerator,
            "denominator":edge['abs_projection']}


def compare_losses(other, winner, qmin):
    n,(a,b) = other['numerator'],other['denominator']
    nw,(aw,bw) = winner['numerator'],winner['denominator']
    slope,intercept = n*aw-nw*a,n*bw-nw*b
    value = slope*qmin+intercept
    assert slope >= 0 and value >= 0
    return {"slope":slope,"intercept":intercept,"value_at_qmin":value}


def cross_product(a,b):
    return (a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[1]*b[1])


def substitute(poly,residue):
    # Convert b+a*q into b+a*r+6*a*k for q=6*k+r.
    return (poly[0]+poly[1]*residue,6*poly[1])


def symbolic(peak_edges, lower):
    integral_peaks = {r:sorted(name for (x,y),name in PEAK_NAMES.items()
                              if (x-r*y).denominator==1) for r in range(6)}
    assert integral_peaks == {0:[],1:['A'],2:[],3:['C','G'],4:['E'],5:[]}
    for r in (1,3,4):
        times = {y for (x,y),name in PEAK_NAMES.items() if name in integral_peaks[r]}
        assert times | {1-y for y in times} == {F(1,6),F(5,6)}
    global_checks, local_checks, domains = [], [], []
    for residue,qmin,name,alpha,beta in DOMAINS:
        losses = [loss(edge,residue) for edge in peak_edges]
        winner = next(v for v in losses if v['edge']['name']==name
                      and v['edge']['direction']==(alpha,beta))
        n,(a,b) = winner['numerator'],winner['denominator']
        assert n==F(1,6) and winner['edge']['projection_sign']==-1 and a>0
        e_at_min = n/(a*qmin+b)
        assert e_at_min < F(1,42) and e_at_min <= winner['edge']['emax']
        for other in losses:
            check = compare_losses(other,winner,qmin)
            if other is not winner:
                assert check['value_at_qmin']>0  # Unique winning edge for all q.
            global_checks.append({"residue":residue,"qmin":qmin,
                "peak":other['edge']['name'],"direction":other['edge']['direction'],
                "rho":other['rho'],"loss_numerator":other['numerator'],
                "loss_denominator":other['denominator'],"comparison":check})
        table = {}
        for peak_name,direction in LOCAL_WINNERS[residue].items():
            candidates = [v for v in losses if v['edge']['name']==peak_name]
            chosen = next(v for v in candidates if v['edge']['direction']==tuple(direction))
            for other in candidates:
                local_checks.append({"residue":residue,"peak":peak_name,
                    "direction":other['edge']['direction'],
                    "comparison":compare_losses(other,chosen,qmin)})
            table[peak_name] = {"six_times_loss_numerator":6*chosen['numerator'],
                                "denominator":chosen['denominator']}
        x0,y0,_ = winner['edge']['peak']
        # Since H'=-(a*q+b), the first hit has H=x0-q*y0-1/6.
        h_coefficients = (x0-residue*y0-F(1,6),-6*y0)
        assert all(c.denominator==1 for c in h_coefficients)
        denominator = (6*b,6*a)
        y_numerator = (6*b*y0+beta,6*a*y0)
        t_numerator = (tuple(denominator[i]-y_numerator[i] for i in (0,1))
                       if residue==5 else y_numerator)
        nk,dk = substitute(t_numerator,residue),substitute(denominator,residue)
        chart = lower.CHARTS[residue]
        assert cross_product(nk,chart['D'])==cross_product(chart['N'],dk)
        value_numerator = (b-1,a)  # 1/6 - 1/[6(a*q+b)].
        vk = substitute(value_numerator,residue)
        assert cross_product(vk,chart['D'])==cross_product(chart['A'],dk)
        domains.append({"residue":residue,"qmin":qmin,"winner":winner,
            "loss_at_qmin":e_at_min,"H_coefficients_in_k":h_coefficients,
            "physical_y_numerator_in_q":y_numerator,"denominator_in_q":denominator,
            "chosen_time_reflects_y":residue==5,"previous_witness_identity":True,
            "previous_value_identity":True,"peak_minimum_loss_table":table})
    assert len(global_checks)==63 and len(local_checks)==63
    return {"integral_peak_residues":integral_peaks,"domains":domains,
            "global_comparisons":global_checks,"table_comparisons":local_checks}


def ceil(value):
    return -((-value.numerator)//value.denominator)


def slice_maximum(cells,q):
    candidates = set()
    for cell in cells:
        vs = cell['vertices']
        for p in vs:
            if (p[0]-q*p[1]).denominator==1:
                candidates.add(p)
        for i,j in cell['edges']:
            p,r = vs[i],vs[j]
            hp,hr = p[0]-q*p[1],r[0]-q*r[1]
            if hp==hr:
                if hp.denominator==1:
                    candidates.update((p,r))
                continue
            lo,hi = sorted((hp,hr))
            first,last = ceil(lo),hi.numerator//hi.denominator
            if first>last:
                continue
            for h in {first,last}:
                weight = (h-hp)/(hr-hp)
                point = tuple(p[k]+weight*(r[k]-p[k]) for k in range(3))
                assert 0 <= weight <= 1 and point[0]-q*point[1]==h
                candidates.add(point)
    best = max(p[2] for p in candidates)
    assert best>F(1,7)  # At this height no horizontal original edge exists.
    times = {p[1] for p in candidates if p[2]==best}
    return best, sorted(times | {1-t for t in times})


def main():
    cells,peak_edges,triples = geometry()
    archive_comparison = compare_archive(cells)
    lower_path = ROOT/'reviews/2026-09-29-ltcm-other-ray/verify.py'
    spec = importlib.util.spec_from_file_location('frozen_lower_witnesses',lower_path)
    lower = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lower)
    lower_certificates = lower.symbolic_witnesses()
    symbolic_result = symbolic(peak_edges,lower)
    frozen_path = ROOT/'reviews/2026-09-29-ltcm-other-ray/verification.json'
    frozen = json.loads(frozen_path.read_text())
    assert [r['q'] for r in frozen['cases']]==list(range(2,151))
    comparisons = []
    for old in frozen['cases']:
        q = old['q']
        best,times = slice_maximum(cells,q)
        assert best==F(old['maximum']) and times==list(map(F,old['maximizing_times']))
        claimed,witness = lower.proposed(q)
        assert best==claimed and times==sorted((witness,1-witness))
        for t in times:
            phases = [fractional(v*t) for v in lower.speeds(q)]
            assert min(min(p,1-p) for p in phases)==best
        comparisons.append({"q":q,"maximum":best,"all_maximizing_times":times,
                            "matches_frozen_physical_calculation":True})
    dependencies = ['reviews/2026-09-29-ltcm-spectrum/ambient.json',
                    'reviews/2026-09-29-ltcm-other-ray/verify.py',
                    'reviews/2026-09-29-ltcm-other-ray/verification.json']
    report = {
        "status":"PASS; complete upper/lower proof candidate with exact finite cell certificate",
        "base_commit":BASE,"script_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_sha256":{p:sha256((ROOT/p).read_bytes()).hexdigest() for p in dependencies},
        "summary":{"boundary_planes":48,"plane_triples":triples,"cells":len(cells),
            "vertices":sum(len(c['vertices']) for c in cells),
            "edges":sum(len(c['edges']) for c in cells),"peak_edges":len(peak_edges),
            "unbounded_domain_upper_comparisons":63,"peak_table_comparisons":63,
            "symbolic_lower_phase_identities":42,"symbolic_lower_inequalities":84,
            "frozen_physical_cases_compared":len(comparisons),"new_physical_q_values":0},
        "geometry":cells,"peak_edges":peak_edges,"archive_comparison":archive_comparison,
        "symbolic_upper_bound":symbolic_result,
        "lower_certificate_residues":[c['residue'] for c in lower_certificates],
        "slice_comparisons":comparisons,
        "limits":"Same AI author; exact arithmetic and symbolic-domain checks are not external or formal review. No novelty claim.",
    }
    print(json.dumps(report,indent=2,default=lambda v:str(v) if isinstance(v,F) else v))


if __name__=='__main__':
    main()
