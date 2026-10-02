"""Frozen fresh comparison of orbit-aligned component representations."""
import argparse
from collections import Counter
import hashlib,json,subprocess
from pathlib import Path
import construct as c

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]


def save(path,obj):path.write_text(json.dumps(obj,default=c.encode,sort_keys=True,separators=(',',':'))+'\n')


def run(freeze,out):
    pins=json.loads((HERE/'MANIFEST.json').read_text())
    for name,digest in pins['sha256'].items():
        raw=(ROOT/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==digest,name
        assert subprocess.check_output(['git','show',f'{freeze}:{name}'],cwd=ROOT)==raw,name
    relative=str((HERE/'MANIFEST.json').relative_to(ROOT))
    assert subprocess.check_output(['git','show',f'{freeze}:{relative}'],cwd=ROOT)==(HERE/'MANIFEST.json').read_bytes()
    out.mkdir(parents=True,exist_ok=True);assert not (out/'RESULTS.json').exists(),'Refuse overwrite; use a separate reproduction directory.'
    inputs=json.loads((HERE/'VALIDATION_INPUTS.json').read_text())
    cores={};cases=[];c.COUNTS.clear()
    pairs=sorted({(c.clock(v)['P'],c.clock(v)['Q']) for v in inputs['triples']})
    for P,Q in pairs:cores[f'{P},{Q}']=c.source_core(P,Q)
    for v in inputs['triples']:
        clock=c.clock(v);key=f"{clock['P']},{clock['Q']}"
        row=c.evaluate(v,cores[key]);row['core_key']=key;cases.append(row)
    names=('widest','all_components','positive_only')
    summary={'status':'COMPLETED_FROZEN_COMPARISON','freeze_commit':freeze,'fresh_cases':len(cases),
        'coverage':{name:sum(row['selected'][name] is not None for row in cases) for name in names},
        'misses':{name:[row['pqr'] for row in cases if row['selected'][name] is None] for name in names},
        'core_pairs':len(cores),'core_classes':dict(Counter(core['classification'] for core in cores.values())),
        'core_components':sum(len(core['components']) for core in cores.values()),
        'maximum_components_per_core':max(len(core['components']) for core in cores.values()),
        'isolated_components':sum(comp['width']==0 for core in cores.values() for comp in core['components']),
        'by_clock_lifts':{group:{'cases':sum((row['clock']['d']==1)==(group=='one') for row in cases),
            'coverage':{name:sum(row['selected'][name] is not None for row in cases if (row['clock']['d']==1)==(group=='one')) for name in names}}
                           for group in ('one','multiple')},
        'by_pair_exposure':{group:{'cases':sum((row['core_key'] in inputs['development_core_keys'])==(group=='seen') for row in cases),
            'coverage':{name:sum(row['selected'][name] is not None for row in cases if (row['core_key'] in inputs['development_core_keys'])==(group=='seen')) for name in names}}
                            for group in ('seen','new')},
        'counts':dict(c.COUNTS),'limits':'Complete core construction is charged work, not free preprocessing. This is a one-runner extension and finite implementation check, not a universal existence or efficiency claim.'}
    assert len(cases)==inputs['count']
    save(out/'RESULTS.json',{'freeze_commit':freeze,'cores':cores,'cases':cases,'summary':summary})
    save(out/'SUMMARY.json',summary)
    print(json.dumps({k:summary[k] for k in ('status','fresh_cases','coverage','core_pairs','core_classes','core_components','maximum_components_per_core','counts')}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--freeze',required=True);parser.add_argument('--out',type=Path,default=HERE/'run')
    args=parser.parse_args();run(args.freeze,args.out)
