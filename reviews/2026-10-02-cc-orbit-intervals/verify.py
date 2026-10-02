"""Alternate exact band intersections; no import of construct.py."""
import argparse
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
from math import floor,gcd
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
BASE=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8));D=F(1,8)


def run(out):
    for name,digest in json.loads((HERE/'MANIFEST.json').read_text())['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    spec=spec_from_file_location('band_checker',ROOT/'reviews/2026-09-30-cc-three-parameter/verify.py')
    alt=module_from_spec(spec);spec.loader.exec_module(alt)
    raw=(out/'RESULTS.json').read_bytes();data=json.loads(raw)
    inputs=json.loads((HERE/'VALIDATION_INPUTS.json').read_text())
    assert [row['pqr'] for row in data['cases']]==inputs['triples']
    counts={'core_components':0,'source_endpoint_band_checks':0,'component_bits':0,'witnesses':0,'full_physical_cases':0}
    cores={}
    for key,record in data['cores'].items():
        P,Q=record['pair'];vs=[a*P+b*Q for a,b in BASE]
        assert key==f'{P},{Q}' and gcd(P,Q)==1
        expected=alt.safe_intervals(vs,D)
        assert expected==[[F(x) for x in comp['interval']] for comp in record['components']],key
        order=sorted(range(len(expected)),key=lambda i:(-(expected[i][1]-expected[i][0]),expected[i][0]))
        assert order==record['order'] and record['primary']==(order[0] if order else None)
        pos=sum(l<u for l,u in expected)
        kind='EMPTY' if not expected else 'ISOLATED_ONLY' if not pos else 'POSITIVE_ONLY' if pos==len(expected) else 'MIXED'
        assert record['classification']==kind
        for i,comp in enumerate(record['components']):
            l,u=expected[i];assert F(comp['width'])==u-l and comp['id']==i and comp['dimension']==int(l<u)
            mid=(l+u)/2;pl=[floor(v*mid) for v in vs];pair_laps=[floor(P*mid),floor(Q*mid)]
            assert pl==comp['core_physical_laps'] and pair_laps==comp['pair_laps']
            assert comp['torus_laps']==[lap-a*pair_laps[0]-b*pair_laps[1] for lap,(a,b) in zip(pl,BASE)]
            xy=[[P*t-pair_laps[0],Q*t-pair_laps[1]] for t in (l,u)]
            assert xy==[[F(x) for x in point] for point in comp['xy_endpoints']]
            for t in (l,u):
                for v,lap in zip(vs,pl):assert D<=v*t-lap<=1-D;counts['source_endpoint_band_checks']+=1
            counts['core_components']+=1
        cores[key]=expected
    coverage={name:0 for name in ('widest','all_components','positive_only')};diagnostics=[]
    for row in data['cases']:
        p,q,r=row['pqr'];assert gcd(p,q,r)==1 and 12<max(p,q,r)<=15 and min(p,q,r)>=1
        vs=[a*p+b*q for a,b in BASE]+[r];assert len(set([0]+vs))==10
        cl=row['clock'];d=gcd(p,q);assert cl=={'g':1,'A':p,'B':q,'C':r,'d':d,'P':p//d,'Q':q//d}
        core=data['cores'][row['core_key']];components=cores[row['core_key']]
        rbands=alt.bands(r,D);component_unions=[]
        for l,u in components:
            intervals=[[(l+j)/d,(u+j)/d] for j in range(d)]
            component_unions.append(alt.common(intervals,rbands))
        bits=''.join('1' if intervals else '0' for intervals in component_unions)
        assert bits==row['component_bits'],row['pqr'];counts['component_bits']+=len(bits)
        primary=core['primary']
        selected={'widest':primary if primary is not None and component_unions[primary] else None,
                  'all_components':next((i for i in core['order'] if component_unions[i]),None),
                  'positive_only':next((i for i in core['order'] if components[i][0]<components[i][1] and component_unions[i]),None)}
        assert selected==row['selected']
        for name in coverage:coverage[name]+=selected[name] is not None
        for key,w in row['witnesses'].items():
            i=int(key);assert i==w['component'];t=F(w['time']);tau=F(w['tau']);u=F(w['core_clock']);j=w['lift']
            assert t==tau==component_unions[i][0][0] and 0<=j<d and u==d*t-j
            assert components[i][0]<=u<=components[i][1]
            phases=[(v*t)%1 for v in vs]
            assert phases==list(map(F,w['phases'])) and all(D<=f<=1-D for f in phases)
            assert [floor(v*t) for v in vs]==w['physical_laps'] and floor(r*t)==w['r_band']
            assert phases[:2]==list(map(F,w['xy']))
            counts['witnesses']+=1
        full=alt.safe_intervals(vs,D);recovered=alt.merge([interval for group in component_unions for interval in group])
        assert recovered==full,('full set mismatch',row['pqr']);counts['full_physical_cases']+=1
        # Preserve complete target unions when compression loses a solution or no 1/8 solution exists.
        if selected['widest'] is None or selected['positive_only'] is None or not full:
            weak=None
            if not full:
                alt.negative_crosscheck(vs,D);weak=alt.safe_intervals(vs,F(1,10))
                if not weak:alt.negative_crosscheck(vs,F(1,10))
            diagnostics.append({'pqr':row['pqr'],'full8_intervals':full,'full10_when8_empty':weak})
    assert coverage==data['summary']['coverage']
    assert json.loads((out/'SUMMARY.json').read_text())==data['summary']
    report={'status':'PASS','freeze_commit':data['freeze_commit'],'results_sha256':hashlib.sha256(raw).hexdigest(),
            'checks':counts,'coverage':coverage,'compression_failure_unions':diagnostics,
            'negative_event_checks':alt.CHECKS['negative_events_checked'],
            'limits':'Same-author alternate exact algorithms, not independent human or formal proof review. Full-set equality verifies the representation/extension implementation; it does not prove universal core existence.'}
    (out/'VERIFICATION.json').write_text(json.dumps(report,default=alt.encode,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:report[k] for k in ('status','checks','coverage','negative_event_checks')}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=HERE/'run');run(parser.parse_args().out)
