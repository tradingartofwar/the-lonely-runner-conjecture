#!/usr/bin/env python3
"""Reproduce frozen deterministic outputs in a temporary sparse repository."""
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
    review_pins=json.loads((HERE/'REVIEW_INPUTS.json').read_text())
    for p,pin in review_pins['files'].items(): assert digest(ROOT/p)==pin['sha256'],p
    names=['hybrid.json','audit.json','summary.json','geometry_review.json','physical_review.json']
    expected={name:digest(HERE/name) for name in names}
    timing_hash=digest(HERE/'timing.json')
    with tempfile.TemporaryDirectory(prefix='cc-hybrid-reproduction-') as directory:
        temp=Path(directory); package=temp/HERE.relative_to(ROOT)
        package.mkdir(parents=True)
        for path in set(pins['files'])|set(review_pins['files']):
            target=temp/path; target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/path,target)
        for source in HERE.iterdir():
            if source.is_file(): shutil.copyfile(source,package/source.name)
        subprocess.run([sys.executable,str(package/'hybrid.py')],cwd=temp,check=True,capture_output=True)
        for name in names[:3]: assert digest(package/name)==expected[name],name
        for stem in ('geometry_review','physical_review'):
            run=subprocess.run([sys.executable,str(package/(stem+'.py'))],cwd=temp,check=True,capture_output=True)
            assert run.stdout==(HERE/(stem+'.json')).read_bytes(),stem
        # Exercise the production dispatcher after a real JSON read, on the
        # same predeclared 47 residual and 24 physical records, not new inputs.
        spec=importlib.util.spec_from_file_location('hybrid_roundtrip',package/'hybrid.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        _,_,api,ten,_=mod.setup()
        hybrid=json.loads((package/'hybrid.json').read_text())
        audit=json.loads((package/'audit.json').read_text()); count=0
        for record in audit['residual_dispatch']+audit['physical_controls']:
            selected=dict(pair=record['pair'],**mod.select(api,ten,hybrid,*record['pair']))
            assert mod.encode(selected)==record,record['pair'];count+=1
        assert digest(package/'timing.json')==timing_hash
    result=dict(status='PASS',reproduced_byte_for_byte=expected,input_hashes_verified=len(pins['files']),
                supplementary_review_input_hashes_verified=len(review_pins['files']),
                protocol_sha256=pins['protocol_sha256'],serialized_dispatch_checks=count,
                preserved_timing_sha256=timing_hash,timing_rerun=False,
                reproduce_script_sha256=digest(Path(__file__)),
                scope='Same frozen hybrid outputs and independent reviews; no new target or timing repeat. Temporary sparse copy preserves original evidence.')
    (HERE/'REPRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS',exact_outputs=len(names),input_hashes=len(pins['files']),serialized_dispatch_checks=count)))


if __name__=='__main__': main()
