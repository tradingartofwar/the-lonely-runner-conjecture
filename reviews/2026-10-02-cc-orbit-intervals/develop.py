"""Exposed-data development and explicit fixed-pair finite reduction."""
from collections import Counter
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
from math import gcd
from pathlib import Path
import json
import construct as c

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]


def load_physical():
    spec=spec_from_file_location('physical',ROOT/'reviews/2026-09-30-cc-three-parameter/verify.py')
    m=module_from_spec(spec);spec.loader.exec_module(m);return m


def run():
    physical=load_physical()
    a=json.loads((ROOT/'reviews/2026-09-30-cc-three-parameter/discovery.json').read_text())
    b=json.loads((ROOT/'reviews/2026-10-02-cc-sheet-coverage/run/RESULTS.json').read_text())
    triples=sorted({tuple(row['pqr']) for row in a['cases'] if row['split']!='scaling_control'}|
                   {tuple(row['pqr']) for row in b['cases']})
    assert len(triples)==1050
    cores={};cases=[];mismatches=[]
    for v in triples:
        key=(v[0]//gcd(v[0],v[1]),v[1]//gcd(v[0],v[1]))
        if key not in cores:
            core=c.source_core(*key)
            expected=physical.safe_intervals(c.speeds(*key),c.D)
            assert [item['interval'] for item in core['components']]==expected,key
            cores[key]=core
        row=c.evaluate(v,cores[key]);full=physical.safe_intervals(c.speeds(v[0],v[1])+[v[2]],c.D)
        assert (row['selected']['all_components'] is not None)==bool(full),v
        cases.append(row)
    key=(1,2);core=cores[key];primary=core['components'][core['primary']]
    assert primary['interval']==[F(25,152),F(7,40)] and primary['width']==F(1,95)
    lower=[]
    for r in range(1,24):
        if r in c.speeds(1,2):continue
        row=c.evaluate((1,2,r),core)
        full=physical.safe_intervals(c.speeds(1,2)+[r],c.D)
        assert full and row['selected']['all_components'] is not None
        direct=F(1,8) if r in (6,12) else row['witnesses'][str(row['selected']['widest'])]['time']
        assert all(c.D<=(v*direct)%1<=1-c.D for v in c.speeds(1,2)+[r])
        lower.append({'r':r,'interval_succeeds':row['selected']['widest'] is not None,'time':direct})
    assert [x['r'] for x in lower if not x['interval_succeeds']]==[6,12]
    controls=[]
    for v in [(1,2,24),(1,2,40),(1,2,80),(1,2,40*10**30),(2,4,5),(4,8,10),(3,6,120),(2,4,1),(4,8,2)]:
        cl=c.clock(v);key=(cl['P'],cl['Q']);row=c.evaluate(v,cores[key])
        assert row['selected']['all_components'] is not None
        controls.append(row)
    assert controls[-2]['witnesses'][str(controls[-2]['selected']['widest'])]['lift']==1
    assert controls[-1]['witnesses'][str(controls[-1]['selected']['widest'])]['time']*2==controls[-2]['witnesses'][str(controls[-2]['selected']['widest'])]['time']
    band_fixtures=[(F(7,8),F(9,8),1,True),(F(7,8)+F(1,100),F(9,8)-F(1,100),1,False),
                   (F(1,8),F(1,8),1,True),(F(7,8),F(7,8),1,True),(F(0),F(0),1,False)]
    for l,u,C,want in band_fixtures:assert (c.first_band(l,u,C) is not None)==want
    point_core={'pair':[1,2],'classification':'ISOLATED_ONLY_SUPPLIED_SUBSET','components':[cores[(1,2)]['components'][0]],'order':[0],'primary':0}
    point_controls=[c.evaluate(v,point_core) for v in [(1,2,6),(1,2,8),(2,4,1)]]
    assert [r['selected']['all_components'] is not None for r in point_controls]==[True,False,True]
    ablated=[row['pqr'] for row in cases if row['selected']['all_components'] is not None and row['selected']['positive_only'] is None]
    result={'status':'PASS_DEVELOPMENT_ONLY','domain':'1050 exposed primitive triples in [1,12]^3; controls excluded',
            'core_pairs':len(cores),'core_classes':dict(Counter(x['classification'] for x in cores.values())),
            'coverage':{name:sum(row['selected'][name] is not None for row in cases) for name in ('widest','all_components','positive_only')},
            'cores':{f'{P},{Q}':core for (P,Q),core in sorted(cores.items())},'cases':cases,
            'widest_misses':[row['pqr'] for row in cases if row['selected']['widest'] is None],
            'isolated_points_required':ablated,'family_lower_cases':lower,'explicit_controls':controls,
            'band_boundary_fixtures':band_fixtures,'isolated_subset_controls':point_controls,
            'counts':dict(c.COUNTS),'limits':'Same-author alternate algorithms; finite exposed checks. General family argument needs independent review.'}
    (HERE/'DEVELOPMENT.json').write_text(json.dumps(result,default=c.encode,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:result[k] for k in ('status','core_pairs','core_classes','coverage','widest_misses','isolated_points_required','counts')}))


if __name__=='__main__':run()
