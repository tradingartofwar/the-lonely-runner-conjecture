#!/usr/bin/env python3
"""Reproduce this frozen transfer without expanding its trial or control set."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__:
        raise RuntimeError('Run without -O; exact checkers use assertions')
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    for name,entry in inputs['files'].items():
        assert digest(ROOT/name)==entry['sha256'],name
    assert digest(HERE/'PROTOCOL.md')==inputs['protocol_sha256']
    names=('regression.json','certificate.json','run.json','geometry_review.json','physical_review.json')
    expected={name:digest(HERE/name) for name in names}
    process=subprocess.run([sys.executable,str(HERE/'transfer.py')],check=True,
                           capture_output=True,text=True)
    summary=json.loads(process.stdout)
    for name in names[:3]:
        assert digest(HERE/name)==expected[name],name
    for stem in ('geometry_review','physical_review'):
        result=subprocess.run([sys.executable,str(HERE/(stem+'.py'))],check=True,
                              capture_output=True)
        assert result.stdout==(HERE/(stem+'.json')).read_bytes(),stem
    output={'status':'PASS','reproduced_byte_for_byte':expected,
            'transfer_summary':summary,'input_hashes_verified':len(inputs['files']),
            'reproduce_script_sha256':digest(Path(__file__)),
            'scope':'One changed row and the frozen controls; old-row regression. No added trial or broad scan.'}
    (HERE/'REPRODUCTION.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','exact_outputs':5,'input_hashes':len(inputs['files']),
                      'changed_rows_tested':1}))


if __name__=='__main__':
    main()
