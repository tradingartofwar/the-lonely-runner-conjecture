"""Reproduce deterministic outputs in a temporary output directory."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def run():
    freeze=json.loads((HERE/'run/RESULTS.json').read_text())['freeze_commit']
    with tempfile.TemporaryDirectory(prefix='lr-sheet-reproduce-') as directory:
        out=Path(directory)
        for script,args in [('run.py',['--freeze',freeze]),('verify.py',[])]:
            subprocess.run([sys.executable,str(HERE/script),*args,'--out',str(out)],check=True,capture_output=True,text=True,timeout=600)
        hashes={}
        for name in ('RESULTS.json','SUMMARY.json','VERIFICATION.json'):
            actual=(out/name).read_bytes();assert actual==(HERE/'run'/name).read_bytes(),name
            hashes[name]=hashlib.sha256(actual).hexdigest()
    report={'status':'PASS_BYTE_FOR_BYTE','freeze_commit':freeze,'outputs':hashes,
            'scope':'Temporary output directory, same checked source checkout; not a fresh clone or fresh mathematical domain.'}
    (HERE/'REPRODUCTION.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report))


if __name__=='__main__':run()
