"""Check new decisions using the frozen old physical-time implementation.

No imports of criterion.py or its floor-sum implementation. Same AI author;
different coordinates/algorithm, not independent human proof review.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def run(out):
    pins = json.loads((HERE/'MANIFEST.json').read_text())
    for name, digest in pins['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    spec = importlib.util.spec_from_file_location('physical_time_checker', ROOT/'reviews/2026-09-30-cc-three-parameter/verify.py')
    physical = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(physical)
    raw = (out/'RESULTS.json').read_bytes()
    data = json.loads(raw)
    inputs = json.loads((HERE/'VALIDATION_INPUTS.json').read_text())
    dev = json.loads((HERE/'DEVELOPMENT.json').read_text())
    sources = json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())['certificate']['candidates']
    sources.sort(key=lambda s: (s['parent'], *s['edge'], s['seventh_lap'], s['eighth_lap']))
    assert sources == data['sources']
    sources = [{**s, 'endpoints': [list(map(F, p)) for p in s['endpoints']]} for s in sources]
    assert len(sources) == 36
    for s in sources:
        for x, y in s['endpoints']:
            for (a, b), label in zip(physical.BASE, s['labels']):
                assert F(1,8) <= a*x+b*y-label <= F(7,8)
                physical.CHECKS['source_endpoint_bands'] += 1
    objects = {s['id']+':ZSLAB': {'id':s['id']+':ZSLAB', 'source':i,
               'endpoints': s['endpoints'], 'z_range':[F(1,8),F(7,8)]} for i,s in enumerate(sources)}
    assert [row['pqr'] for row in data['cases']] == inputs['fresh_triples']
    assert len({tuple(row['pqr']) for row in data['cases']}) == inputs['fresh_count']
    assert not ({tuple(r['pqr']) for r in data['cases']} & {tuple(r['pqr']) for r in dev['development_rows']})
    # Rebuild the development-trained greedy menu without importing its compiler.
    rows = dev['development_rows']; remaining=set(range(len(rows))); menu=[]
    while remaining and len(menu)<8:
        gains=[sum(rows[j]['bits'][i]=='1' for j in remaining) for i in range(36)]
        if not max(gains): break
        i=gains.index(max(gains));menu.append(i)
        remaining={j for j in remaining if rows[j]['bits'][i]=='0'}
    assert menu == inputs['menus']['new7'] and menu[:4] == inputs['menus']['new4']
    counts={name:0 for name in ('legacy4','new4','new7','full36')}
    failures=[]
    for row in data['cases']:
        p,q,r=row['pqr']; lat=row['lattice']
        assert 1<=min(p,q,r) and 9<max(p,q,r)<=12 and gcd(p,q,r)==1
        speeds=[a*p+b*q for a,b in physical.BASE]+[r]
        assert len(set([0]+speeds))==10
        assert lat['g']==1 and lat['normalized']==[p,q,r] and lat['d']==gcd(p,q)
        assert lat['P']*lat['d']==p and lat['Q']*lat['d']==q
        assert lat['a']*lat['P']+lat['b']*lat['Q']==1
        assert lat['c']*lat['d']+lat['e']*r==1
        R,S=lat['relations']
        assert [R[1]*S[2]-R[2]*S[1],R[2]*S[0]-R[0]*S[2],R[0]*S[1]-R[1]*S[0]]==[p,q,r]
        bits=physical.physical_contacts([p,q,r],sources)['sheets']
        assert bits==row['sheet_bits'],row['pqr']
        physical.CHECKS['contact_bits']+=36
        for name,indices in {**inputs['menus'],'full36':list(range(36))}.items():
            chosen=next((i for i in indices if bits[i]=='1'),None)
            assert row['selections'][name]==chosen
            counts[name]+=chosen is not None
            if chosen is not None: assert str(chosen) in row['witnesses']
        for key,w in row['witnesses'].items():
            assert int(key)==w['source']
            physical.inspect_witness([p,q,r],w,sources,objects,lat)
        if '1' not in bits:
            full8=physical.safe_intervals(speeds,F(1,8))
            full10=None
            if not full8:
                physical.negative_crosscheck(speeds,F(1,8))
                full10=physical.safe_intervals(speeds,F(1,10))
                if not full10:physical.negative_crosscheck(speeds,F(1,10))
            failures.append({'pqr':[p,q,r],'full8_intervals':full8,'full10_when8_empty':full10})
    assert counts==data['summary']['coverage']
    assert json.loads((out/'SUMMARY.json').read_text())==data['summary']
    report={'status':'PASS','freeze_commit':data['freeze_commit'],
            'results_sha256':hashlib.sha256(raw).hexdigest(),'fresh_cases':len(data['cases']),
            'checks':physical.CHECKS,'coverage':counts,'full_class_failure_diagnostics':failures,
            'limits':'Same-author alternate physical-time code, not independent human or formal review. Physical checker also computes unused edge bits; contact_bits counts only compared sheet bits.'}
    (out/'VERIFICATION.json').write_text(json.dumps(report,default=physical.encode,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:report[k] for k in ('status','fresh_cases','checks','coverage')}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=HERE/'run')
    run(parser.parse_args().out)
