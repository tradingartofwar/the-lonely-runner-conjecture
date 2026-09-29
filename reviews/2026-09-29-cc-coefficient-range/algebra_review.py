#!/usr/bin/env python3
"""Independent fixed-geometry audit: interval versus open forbidden bands.

No production imports; no coefficient trials outside the frozen protocol.
"""
from fractions import Fraction as F
from math import floor
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
L = ((F(1,4), F(3,8)), (F(3,8), F(1,8)))
SEG_F = ((F(1,8), F(3,16)), (F(1,8), F(1,4)))
C = SEG_F[1]

def image(row, points):
    vals = [row[0]*x+row[1]*y for x,y in points]
    return min(vals), max(vals)

def inspect_interval(lo, hi):
    # Unsafe phase set is the union of OPEN 1/8-neighborhoods of integers.
    # A closed image interval meets (n-1/8,n+1/8) precisely under these
    # two strict comparisons. Equality at either band edge stays safe.
    conflicts = [n for n in range(floor(lo)-1, floor(hi)+2)
                 if lo < F(n)+F(1,8) and hi > F(n)-F(1,8)]
    return {'image':[str(lo),str(hi)], 'safe':not conflicts,
            'unsafe_integer_centers':conflicts,
            'lap':floor((lo+hi)/2) if not conflicts else None}

def inspect(row):
    leader=inspect_interval(*image(row,L))
    fallback=inspect_interval(*image(row,SEG_F))
    point=inspect_interval(*image(row,[C]))
    return {'A':row[0], 'B':row[1], 'delta':row[0]-2*row[1],
            'L':leader, 'F':fallback, 'C':point,
            'W':leader['safe'] and fallback['safe'],
            'R':leader['safe'] and point['safe']}


def main():
    finite=[inspect((2*b+d,b)) for b in range(1,13)
            for d in range(-6,7) if 2*b+d>0]
    assert len(finite)==147
    accepted=[x for x in finite if x['W']]
    assert all(x['R'] for x in accepted)
    residues=[{'delta':d,'B_mod8':b, 'representative':inspect((2*(b+8)+d,b+8))}
              for d in range(-6,7) for b in range(8)]
    table={str(d):[r['B_mod8'] for r in residues
                  if r['delta']==d and r['representative']['R']]
           for d in range(-6,7)}
    # Exhaustive residue-pattern consistency on the allowed finite W domain,
    # not a fresh coefficient scan or empirical periodicity claim.
    for x in finite:
        assert x['R'] == (x['B']%8 in table[str(x['delta'])])
    # Fixed analytically declared controls only.
    controls=[inspect(row) for row in [(6,2),(22,10),(38,18),(4,2),(5,2)]]
    collision_point=(F(1,8), F(9,40))
    collision=F(22)*collision_point[0]+F(10)*collision_point[1]
    assert collision==5
    assert controls[1]['L']['safe'] and not controls[1]['F']['safe'] and controls[1]['C']['safe']
    # Both native F endpoints are safe, but in DIFFERENT laps.
    endpoint_details=[inspect_interval(*image((22,10),[point])) for point in SEG_F]
    assert all(x['safe'] for x in endpoint_details)
    assert [x['lap'] for x in endpoint_details]==[4,5]
    assert not controls[3]['C']['safe'] and controls[3]['L']['safe']
    assert not controls[4]['L']['safe']
    # Exact extremal attainment records from the permitted finite reduction.
    boundary={
        'delta_minus6':[{'A':x['A'],'B':x['B']} for x in accepted if x['delta']==-6],
        'delta_plus6':[{'A':x['A'],'B':x['B']} for x in accepted if x['delta']==6],
        'B12':[{'A':x['A'],'B':x['B']} for x in accepted if x['B']==12],
        'L_closed_band_edges':[{'A':x['A'],'B':x['B'],'image':x['L']['image']}
          for x in accepted if any(F(v)-floor(F(v)) in (F(1,8),F(7,8)) for v in x['L']['image'])],
        'F_closed_band_edges':[{'A':x['A'],'B':x['B'],'image':x['F']['image']}
          for x in accepted if any(F(v)-floor(F(v)) in (F(1,8),F(7,8)) for v in x['F']['image'])]
    }
    result={'method':'direct affine images tested against open forbidden neighborhoods of integers',
            'finite_W_domain_count':len(finite), 'finite_W_accepted_count':len(accepted),
            'W_rows':[{'A':x['A'],'B':x['B'],'delta':x['delta'],'L_lap':x['L']['lap'],'F_lap':x['F']['lap']} for x in accepted],
            'R_residue_class_count':sum(map(len,table.values())),
            'R_accepted_B_residues_by_delta':table,
            'R_complete_13_by_8':residues,
            'W_complete_finite_domain':finite,
            'boundary_attainment':boundary,
            'fixed_controls':controls,
            'ambient_22_10_control':{'point':list(map(str,collision_point)), 'seventh_value':str(collision), 'F_endpoint_checks':endpoint_details},
            'scope':'Exact W/R geometric contracts only; no global discovery or maximal deterministic-output claim.'}
    (HERE/'algebra_review.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'finite_W_domain_count':len(finite),'W_count':len(accepted),'R_residue_count':sum(map(len,table.values())), 'W_rows':result['W_rows'], 'R_table':table,'boundary':{k:v for k,v in boundary.items() if k in ['delta_minus6','delta_plus6','B12']}},indent=2))

if __name__=='__main__':main()
