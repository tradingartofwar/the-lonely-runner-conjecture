#!/usr/bin/env python3
"""Repeat one frozen boundary transfer in a sparse temporary repository."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    if not __debug__: raise RuntimeError('Run without -O')
    pins=json.loads((HERE/'INPUTS.json').read_text())
    assert digest(HERE/'PROTOCOL.md')==pins['protocol_sha256']
    for p,pin in pins['files'].items(): assert digest(ROOT/p)==pin['sha256'],p
    names=['regression.json','adapter.json','screen.json','hybrid.json','full.json','audit.json','summary.json',
           'geometry_review.json','physical_review.json']
    expected={name:digest(HERE/name) for name in names};timing_hash=digest(HERE/'timing.json')
    with tempfile.TemporaryDirectory(prefix='cc-boundary-reproduction-') as directory:
        temp=Path(directory);package=temp/HERE.relative_to(ROOT);package.mkdir(parents=True)
        for p in pins['files']:
            target=temp/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p,target)
        for p in HERE.iterdir():
            if p.is_file(): shutil.copyfile(p,package/p.name)
        subprocess.run([sys.executable,str(package/'transfer.py')],cwd=temp,check=True,capture_output=True)
        for name in names[:7]: assert digest(package/name)==expected[name],name
        for stem in ('geometry_review','physical_review'):
            run=subprocess.run([sys.executable,str(package/(stem+'.py'))],cwd=temp,check=True,capture_output=True)
            assert run.stdout==(HERE/(stem+'.json')).read_bytes(),stem
        spec=importlib.util.spec_from_file_location('boundary_roundtrip',package/'transfer.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        _,h,t,phase,api,physical,_=mod.setup();t.bind(h,phase,api,physical,mod.TARGET)
        hybrid=json.loads((package/'hybrid.json').read_text());full=json.loads((package/'full.json').read_text())
        audit=json.loads((package/'audit.json').read_text());hybrid_count=0;full_count=0
        for r in audit['comparison']:
            assert mod.encode(t.hybrid_select(h,api,physical,hybrid,*r['pair']))==r['hybrid'];hybrid_count+=1
        for r in audit['controls']:
            assert mod.encode(t.hybrid_select(h,api,physical,hybrid,*r['pair']))==r['hybrid'];hybrid_count+=1
            assert mod.encode(t.full_select(h,api,physical,full,*r['pair']))==r['full'];full_count+=1
        assert digest(package/'timing.json')==timing_hash
    record=dict(status='PASS',protocol_sha256=pins['protocol_sha256'],input_hashes_verified=len(pins['files']),
        reproduced_byte_for_byte=expected,serialized_hybrid_dispatch_checks=hybrid_count,
        serialized_full_dispatch_checks=full_count,timing_rerun=False,preserved_timing_sha256=timing_hash,
        reproduce_script_sha256=digest(Path(__file__)),
        scope='Same frozen regression and one target; no further row, family classification, open-target scan or timing repeat.')
    (HERE/'REPRODUCTION.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS',exact_outputs=len(names),input_hashes=len(pins['files']),
                         hybrid_dispatches=hybrid_count,full_dispatches=full_count)))


if __name__=='__main__': main()
