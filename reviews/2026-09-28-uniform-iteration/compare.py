"""Compare the independent exact checks; no new fixtures or search."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    p=json.loads((HERE/'results.json').read_text())
    v=json.loads((HERE/'verification.json').read_text())
    assert p['status']=='pass' and v['summary']['all_pass']
    assert p['protocol_sha256']==v['protocol_sha256']
    count=0
    assert len(p['cases'])==len(v['cases'])==15
    for a,b in zip(p['cases'],v['cases']):
        for field in ['tile','perturbation','periods','starts','order','earliest']:
            assert a[field]==b[field],(a['tile'],a['perturbation'],field)
            count+=1
        for field in ['status','time','calls','rounds','moving_labels','square_free','squares']:
            assert a['selector'][field]==b['selector'][field],field
            count+=1
        assert len(a['selector']['trace'])==len(b['selector']['trace'])
        for x,y in zip(a['selector']['trace'],b['selector']['trace']):
            for field in x:
                assert x[field]==y[field],field
                count+=1
        assert len(a['cycles'])==len(b['cycles'])==4
        for x,y in zip(a['cycles'],b['cycles']):
            for field in ['anchor','q','sum','expected','coefficients','identity_ok']:
                assert x[field]==y[field],field
                count+=1
            assert x['gaps']==[g['gap'] for g in y['gaps']]
            count+=len(x['gaps'])
        # Exact tilings retain isolated equality contacts, not open coverage.
        if a['perturbation']=='exact':
            assert b['safe_components'] and all(x==y for x,y in b['safe_components'])
            assert b['earliest']=='0'
    for a,b in zip(p['occupancy'],v['occupancy']):
        for field in a:
            assert a[field]==b[field]
            count+=1
        assert b['blocked']==a['formula']
        count+=1
    assert v['occupancy'][1]['equality']
    summary=dict(status='pass',cases=15,formal_cycles=60,occupancy_checks=4,
        scalar_calls=p['counts']['scalar_calls'],nonzero_moves=p['counts']['nonzero_moves'],
        exact_field_comparisons=count,partition_points=v['summary']['partition_points'],
        partition_cells=v['summary']['partition_cells'],
        validation_limit='Constructed algebra/boundary calibration. Moving words have at most two letters here; these are not stress tests or proof of uniformity.')
    names=['protocol.json','primary.py','results.json','verify.py','verification.json','compare.py']
    data=dict(summary=summary,sha256={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names})
    (HERE/'comparison.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))


if __name__=='__main__':
    main()
