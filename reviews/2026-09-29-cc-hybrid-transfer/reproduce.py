#!/usr/bin/env python3
"""Reproduce the frozen transfer and separate reviews without repeating timing."""
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


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__: raise RuntimeError('Run without -O')
    pins=json.loads((HERE/'INPUTS.json').read_text())
    assert digest(HERE/'PROTOCOL.md')==pins['protocol_sha256']
    for p,pin in pins['files'].items(): assert digest(ROOT/p)==pin['sha256'],p
    names=['adapter_regression.json','adapter.json','hybrid.json','full.json','audit.json','summary.json',
           'geometry_review.json','physical_review.json']
    hashes={name:digest(HERE/name) for name in names};timing_hash=digest(HERE/'timing.json')
    with tempfile.TemporaryDirectory(prefix='cc-hybrid-transfer-reproduction-') as directory:
        temp=Path(directory);package=temp/HERE.relative_to(ROOT);package.mkdir(parents=True)
        for path in pins['files']:
            dest=temp/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,dest)
        for path in HERE.iterdir():
            if path.is_file(): shutil.copyfile(path,package/path.name)
        subprocess.run([sys.executable,str(package/'transfer.py')],cwd=temp,check=True,capture_output=True)
        for name in names[:6]: assert digest(package/name)==hashes[name],name
        for stem in ('geometry_review','physical_review'):
            run=subprocess.run([sys.executable,str(package/(stem+'.py'))],cwd=temp,check=True,capture_output=True)
            assert run.stdout==(HERE/(stem+'.json')).read_bytes(),stem
        spec=importlib.util.spec_from_file_location('transfer_roundtrip',package/'transfer.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        _,h,phase,api,physical,_=mod.setup();mod.bind(h,phase,api,physical,mod.TARGET)
        hybrid=json.loads((package/'hybrid.json').read_text());full=json.loads((package/'full.json').read_text())
        audit=json.loads((package/'audit.json').read_text());hybrid_count=0;full_count=0
        for r in audit['comparison']:
            assert mod.encode(mod.hybrid_select(h,api,physical,hybrid,*r['pair']))==r['hybrid'];hybrid_count+=1
        for r in audit['controls']:
            assert mod.encode(mod.hybrid_select(h,api,physical,hybrid,*r['pair']))==r['hybrid'];hybrid_count+=1
            assert mod.encode(mod.full_select(h,api,physical,full,*r['pair']))==r['full'];full_count+=1
        assert digest(package/'timing.json')==timing_hash
    result=dict(status='PASS',protocol_sha256=pins['protocol_sha256'],input_hashes_verified=len(pins['files']),
                reproduced_byte_for_byte=hashes,serialized_hybrid_dispatch_checks=hybrid_count,
                serialized_full_dispatch_checks=full_count,timing_rerun=False,preserved_timing_sha256=timing_hash,
                reproduce_script_sha256=digest(Path(__file__)),
                scope='Frozen regression and one target only; sparse temporary copy preserves original evidence; no further target or timing repeat.')
    (HERE/'REPRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS',exact_outputs=len(names),input_hashes=len(pins['files']),
                         hybrid_dispatches=hybrid_count,full_dispatches=full_count)))


if __name__=='__main__': main()
