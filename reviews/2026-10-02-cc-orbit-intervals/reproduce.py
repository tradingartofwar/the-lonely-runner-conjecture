"""Reproduce three deterministic outputs without replacing collected files."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent


def run():
    freeze=json.loads((HERE/'run/RESULTS.json').read_text())['freeze_commit']
    hashes={}
    with tempfile.TemporaryDirectory(prefix='lr-orbit-intervals-') as directory:
        out=Path(directory)
        for script,args in [('run.py',['--freeze',freeze]),('verify.py',[])]:
            subprocess.run([sys.executable,str(HERE/script),*args,'--out',str(out)],check=True,capture_output=True,text=True,timeout=600)
        for name in ('RESULTS.json','SUMMARY.json','VERIFICATION.json'):
            raw=(out/name).read_bytes();assert raw==(HERE/'run'/name).read_bytes(),name
            hashes[name]=hashlib.sha256(raw).hexdigest()
    result={'status':'PASS_BYTE_FOR_BYTE','freeze_commit':freeze,'outputs':hashes,
            'scope':'Temporary output directory in the same pinned checkout; no new domain or new participant.'}
    (HERE/'REPRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result))


if __name__=='__main__':run()
