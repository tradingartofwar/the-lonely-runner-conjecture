#!/usr/bin/env python3
"""Repeat only the frozen reached experiment and its separate exact reviews."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__: raise RuntimeError('Run without -O')
    pins=json.loads((HERE/'INPUTS.json').read_text())
    assert digest(HERE/'PROTOCOL.md')==pins['protocol_sha256']
    for name,pin in pins['files'].items(): assert digest(ROOT/name)==pin['sha256'],name
    names=['regression.json','screen.json','restricted.json','full_clipping.json','full.json','comparison.json','diagnostic.json','summary.json','geometry_review.json','physical_review.json']
    expected={name:digest(HERE/name) for name in names}
    run=subprocess.run([sys.executable,str(HERE/'compare.py')],cwd=ROOT,check=True,capture_output=True,text=True)
    summary=json.loads(run.stdout)
    for name in names[:-2]: assert digest(HERE/name)==expected[name],name
    for stem in ['geometry_review','physical_review']:
        run=subprocess.run([sys.executable,str(HERE/(stem+'.py'))],cwd=ROOT,check=True,capture_output=True)
        assert run.stdout==(HERE/(stem+'.json')).read_bytes(),stem
    result=dict(status='PASS',reproduced_byte_for_byte=expected,input_hashes_verified=len(pins['files']),
                summary=summary,reproduce_script_sha256=digest(Path(__file__)),
                scope='Frozen screen/full comparison and reached paths only; no new coefficients or parameter scans.')
    (HERE/'REPRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS',exact_outputs=len(names),input_hashes=len(pins['files']))))


if __name__=='__main__': main()
