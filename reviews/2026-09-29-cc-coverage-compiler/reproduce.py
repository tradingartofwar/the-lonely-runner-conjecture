#!/usr/bin/env python3
"""Reproduce frozen outputs and compare the archived physical witnesses."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__:
        raise RuntimeError('Run without -O; the exact checkers use assertions')
    inputs = json.loads((HERE/'INPUTS.json').read_text())
    for name,record in inputs['files'].items():
        assert digest(ROOT/name) == record['sha256'], name
    assert digest(HERE/'PROTOCOL.md') == inputs['protocol_sha256']
    expected = {name:digest(HERE/name) for name in
                ('certificate.json','run.json','coverage_review.json','physical_review.json')}
    process = subprocess.run([sys.executable,str(HERE/'compiler.py')],check=True,
                             capture_output=True,text=True)
    summary = json.loads(process.stdout)
    assert summary['status']=='COMPLETE_COVER_CERTIFICATE'
    for name in ('certificate.json','run.json'):
        assert digest(HERE/name)==expected[name], name
    for stem in ('coverage_review','physical_review'):
        result = subprocess.run([sys.executable,str(HERE/(stem+'.py'))],check=True,
                                capture_output=True)
        assert result.stdout==(HERE/(stem+'.json')).read_bytes(), stem
    old = json.loads((ROOT/'reviews/2026-09-29-cc-two-parameter/selector.json').read_text())['records']
    new = json.loads((HERE/'run.json').read_text())['controls']
    fields = ('point','time','phases','physical_laps','reflected_time','reflected_phases')
    assert len(old)==len(new)==18
    for a,b in zip(old,new):
        assert [a['p'],a['q']]==b['pair']
        for field in fields:
            assert a[field]==b[field], (b['pair'],field)
    output = {'status':'PASS','reproduced_byte_for_byte':expected,
              'compiler_summary':summary,
              'archived_selector_comparison':{'pairs':18,'fields':fields,'all_exact':True},
              'input_hashes_verified':len(inputs['files']),
              'reproduce_script_sha256':digest(Path(__file__)),
              'limits':'Same frozen controls, no expanded scan. Separate AI implementations are not human or formal proof.'}
    (HERE/'REPRODUCTION.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','exact_outputs':4,'archived_pairs':18,
                      'source_hashes':len(inputs['files'])}))


if __name__=='__main__':
    main()
