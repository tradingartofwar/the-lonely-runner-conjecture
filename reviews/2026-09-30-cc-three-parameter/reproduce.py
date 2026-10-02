"""Reproduce the frozen result in a temporary sparse repository."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PACKAGE=HERE.relative_to(ROOT)
OUTPUTS=['discovery.json','summary.json','verification.json','verification_summary.json']


def run():
    pins=json.loads((HERE/'INPUTS.json').read_text())
    for path,record in pins['files'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['sha256']
    with tempfile.TemporaryDirectory(prefix='cc-three-parameter-') as temporary:
        root=Path(temporary)
        for path in list(pins['files'])+[str(PACKAGE/'INPUTS.json')]:
            dest=root/path; dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/path,dest)
        for script in ['discover.py','verify.py']:
            subprocess.run([sys.executable,str(root/PACKAGE/script)],cwd=root,
                           check=True,capture_output=True,text=True)
        for name in OUTPUTS:
            assert (root/PACKAGE/name).read_bytes()==(HERE/name).read_bytes(),name
    result={'status':'PASS','input_pins':len(pins['files']),
            'byte_identical':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in OUTPUTS},
            'scope':'Same frozen boxes, objects, menus and physical diagnostics; no enlargement',
            'reproduce_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'REPRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','outputs':len(OUTPUTS),'pins':len(pins['files'])}))


if __name__=='__main__': run()
