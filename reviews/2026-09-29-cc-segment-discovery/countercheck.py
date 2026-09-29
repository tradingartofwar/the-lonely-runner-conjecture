"""Reconstruct floor polygons by 2D halfspace vertices; no discovery import.

Check their intersections with old parent edges, the deterministic coverage
choices, direct physical witnesses and endpoint deletion. Same coordinator.
"""
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def ceil(x):
    return -((-x.numerator) // x.denominator)


def floor(x):
    return x.numerator // x.denominator


def constraints(rows, labels, z):
    out = [(F(1), F(0), F(1, 2))]
    for (a, b), m in zip(rows, labels):
        out.extend(((F(a), F(b), F(m+1)-z), (F(-a), F(-b), -F(m)-z)))
    return out


def vertices(planes):
    points = set()
    for (a, b, c), (d, e, f) in itertools.combinations(planes, 2):
        det = a*e-b*d
        if det == 0:
            continue
        x, y = (c*e-b*f)/det, (a*f-c*d)/det
        if all(u*x+v*y <= w for u, v, w in planes):
            points.add((x, y))
    return sorted(points)


def on_segment(p, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    if dx*(p[1]-a[1]) != dy*(p[0]-a[0]):
        return False
    return all(min(u, v) <= w <= max(u, v) for w, u, v in zip(p, a, b))


def orbit(pair, q):
    return sorted(q*x-y for x, y in pair)


def coverage(pair, q):
    low, high = orbit(pair, q)
    return ceil(low) <= floor(high)


def interior_coverage(pair, q):
    if pair[0] == pair[1]:
        return False
    low, high = orbit(pair, q)
    if low == high:
        return low.denominator == 1
    return floor(low)+1 < high


def recover(pair, q):
    low, high = orbit(pair, q)
    h = ceil(low)
    if h > high:
        return None
    p, r = pair
    hp, hr = q*p[0]-p[1], q*r[0]-r[1]
    lam = F(0) if hp == hr else (h-hp)/(hr-hp)
    assert 0 <= lam <= 1
    x, y = (p[i]+lam*(r[i]-p[i]) for i in (0, 1))
    assert q*x-y == h
    return x, y, h


def main():
    data = json.loads((HERE/'PARENT_INPUT.json').read_text())
    output = json.loads((HERE/'discovery.json').read_text())
    source = json.loads((ROOT/data['source_path']).read_text())
    assert data['parents'] == source['parents'] and data['rows'] == source['rows'][:6]
    assert hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest() == data['source_sha256']
    z = F(data['threshold']); rows = tuple(map(tuple, data['rows']))
    all_rows = rows+((5, 2),)
    reconstructed, polygons = {}, []
    plane_pair_attempts = 0
    for pi, parent in enumerate(data['parents']):
        original = [tuple(map(F, v)) for v in parent['vertices']]
        parent_planes = constraints(rows, parent['labels'], z)
        floor_points = vertices(parent_planes)
        assert floor_points == sorted(v[:2] for v in original if v[2] == z)
        floor_edges = [(i, j) for i, j in parent['edges'] if original[i][2] == original[j][2] == z]
        # Reconstruct boundary incidence from common active halfplanes.
        rebuilt_edges = []
        for i, j in itertools.combinations([i for i, v in enumerate(original) if v[2] == z], 2):
            if any(a*original[i][0]+b*original[i][1] == c == a*original[j][0]+b*original[j][1]
                   for a, b, c in parent_planes):
                rebuilt_edges.append((i, j))
        assert sorted(floor_edges) == sorted(rebuilt_edges)
        # From x in [1/8,1/2], y in [1/8,7/8], S in [7/8,17/4]:
        # only k=0,...,4 can meet [k+1/8,k+7/8]. No child atlas is read.
        for k in range(5):
            labels = tuple(parent['labels'])+(k,)
            planes = constraints(all_rows, labels, z)
            plane_pair_attempts += len(planes)*(len(planes)-1)//2
            points = vertices(planes)
            if not points:
                continue
            polygons.append({'parent': pi, 'seventh_lap': k,
                             'vertices': [[str(v) for v in p] for p in points]})
            for i, j in floor_edges:
                incident = [p for p in points if on_segment(p, original[i][:2], original[j][:2])]
                if incident:
                    reconstructed[f'P{pi}:E{i}-{j}:K{k}'] = (min(incident), max(incident))
    observed = {s['id']: tuple(tuple(map(F, p)) for p in s['endpoints']) for s in output['candidates']}
    assert observed == reconstructed
    # Check the frozen canonical order, tail ranking and complete prefix matrix.
    candidates = output['candidates']
    assert [(s['parent'],s['edge'],s['seventh_lap']) for s in candidates] == sorted(
        (s['parent'],s['edge'],s['seventh_lap']) for s in candidates)
    cutoffs = {}
    for s in candidates:
        p, r = reconstructed[s['id']]
        dx, dy = r[0]-p[0], r[1]-p[1]
        cutoff = max(2,ceil((1+dy)/dx)) if dx else None
        assert s['tail_cutoff'] == cutoff and F(s['dx']) == dx and F(s['dy']) == dy
        if cutoff is not None:
            cutoffs[s['id']] = cutoff
    tail = min(cutoffs, key=cutoffs.get)
    cover = output['cover']; assert cover['tail'] == tail
    cutoff = cutoffs[tail]; assert cover['cutoff'] == cutoff
    prefix = list(range(2,cutoff)); assert cover['prefix'] == prefix
    matrix = {key:[q for q in prefix if coverage(pair,q)] for key,pair in observed.items()}
    assert matrix == cover['coverage']
    selected = [tail]; gaps = set(prefix)-set(matrix[tail]); steps=[]
    while gaps:
        best = min(matrix,key=lambda key:-len(gaps.intersection(matrix[key])))
        new = sorted(gaps.intersection(matrix[best])); assert new
        steps.append({'before':sorted(gaps),'chosen':best,'newly_covered':new})
        selected.append(best);gaps.difference_update(new)
    assert selected == cover['chosen_ids'] and steps == cover['greedy_steps']
    p,r=observed[tail];dx,dy=r[0]-p[0],r[1]-p[1]
    assert dx>0 and cutoff*dx-dy>=1
    # A single affine inequality certifies every q>=cutoff.
    tail_proof={'q_min':cutoff,'width_slope':str(dx),'width_intercept':str(-dy),
                'width_at_cutoff':str(cutoff*dx-dy),'width_minus_one_slope':str(dx)}
    cert_by_id={s['id']:s for s in candidates}
    physical=[]
    for item in output['physical_controls']:
        cert=item['certificate'];q=cert['q']
        chosen=next(key for key in selected if coverage(observed[key],q))
        t,y,h=recover(observed[chosen],q)
        assert chosen==cert['segment'] and str(t)==cert['time'] and h==cert['h']
        laps=[m+b*h for m,(_,b) in zip(cert_by_id[chosen]['labels'],all_rows)]
        assert laps==cert['physical_laps']
        speeds=[a+b*q for a,b in all_rows]
        for j,time in enumerate((t,1-t)):
            direct_laps=[floor(v*time) for v in speeds]
            phases=[v*time-ell for v,ell in zip(speeds,direct_laps)]
            assert all(z<=f<=1-z for f in phases)
            assert direct_laps == (laps if j==0 else [v-1-ell for v,ell in zip(speeds,laps)])
            assert item['physical'][j]['laps']==direct_laps
            assert item['physical'][j]['phases']==list(map(str,phases))
        physical.append({'q':q,'time':str(t),'segment':chosen})
    assert [p['q'] for p in physical]==list(range(2,26))
    # Endpoint removal negative control. No positive segment interior covers q=4.
    closed_q4=sorted({str(recover(pair,4)[0]) for pair in observed.values() if coverage(pair,4)})
    open_q4=[key for key,pair in observed.items() if interior_coverage(pair,4)]
    assert closed_q4==['1/8','3/8'] and open_q4==[]
    out={'status':'PASS: polygon reconstruction, coverage and physical recovery',
         'authorship':'same coordinator; separate structure, not independent review',
         'parent_floor_polygons_reconstructed':len(data['parents']),
         'child_floor_polygons':polygons,'candidate_records_matched':len(reconstructed),
         'plane_pair_attempts_for_child_polygons':plane_pair_attempts,
         'coverage_entries_checked':len(matrix)*len(prefix),'chosen_ids':selected,
         'tail_certificate':tail_proof,'physical_controls':physical,
         'endpoint_removal_control':{'q':4,'closed_folded_times':closed_q4,
                                     'relative_interior_candidates':open_q4},
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (HERE/'PARENT_INPUT.json',HERE/'discovery.json')}}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
