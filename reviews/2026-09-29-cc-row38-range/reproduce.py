#!/usr/bin/env python3
"""Reproduce only the frozen coefficient reductions and physical controls."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__:raise RuntimeError('Run without -O')
    pins=json.loads((HERE/'INPUTS.json').read_text())
    for path,s in pins['files'].items():assert digest(ROOT/path)==s['sha256'],path
    assert digest(HERE/'PROTOCOL.md')==pins['protocol_sha256']
    names=['support.json','classification.json','whole_segments.json','comparison.json',
           'auxiliary_failures.json','controls.json']
    names += sorted(str(p.relative_to(HERE)) for p in (HERE/'failures').glob('*.json'))
    names += ['arithmetic_review.json','physical_review.json']
    expected={name:digest(HERE/name) for name in names}
    result=subprocess.run([sys.executable,str(HERE/'classify.py')],cwd=ROOT,check=True,
                          capture_output=True,text=True)
    summary=json.loads(result.stdout)
    for name in names[:-2]:assert digest(HERE/name)==expected[name],name
    for stem,args in [('arithmetic_review',['--compare']),('physical_review',[])]:
        output=subprocess.run([sys.executable,str(HERE/(stem+'.py')),*args],cwd=ROOT,
                              check=True,capture_output=True)
        assert output.stdout==(HERE/(stem+'.json')).read_bytes(),stem
    record=dict(status='PASS',reproduced_byte_for_byte=expected,input_hashes_verified=len(pins['files']),
        summary=summary,reproduce_script_sha256=digest(Path(__file__)),
        scope='Frozen complete reductions, derived rejection records and predeclared controls only.')
    (HERE/'REPRODUCTION.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS',exact_outputs=len(names),input_hashes=len(pins['files']))))


if __name__=='__main__':main()
