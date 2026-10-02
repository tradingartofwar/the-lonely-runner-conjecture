#!/usr/bin/env python3
"""Reproduce frozen selector-support outputs without expanding their domains."""
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
        raise RuntimeError('Run without -O; exact checks use assertions')
    inputs = json.loads((HERE/'INPUTS.json').read_text())
    for name, record in inputs['files'].items():
        assert digest(ROOT/name) == record['sha256'], name
    assert digest(HERE/'PROTOCOL.md') == inputs['protocol_sha256']
    names = ('support.json', 'classification.json', 'witnesses.json', 'classification_review.json')
    expected = {name: digest(HERE/name) for name in names}
    summaries = {}
    for stem in ('selector', 'classification_review'):
        run = subprocess.run([sys.executable, str(HERE/(stem+'.py'))],
                             check=True, capture_output=True, text=True)
        summaries[stem] = json.loads(run.stdout)
    for name in names:
        assert digest(HERE/name) == expected[name], name
    review = json.loads((HERE/'classification_review.json').read_text())
    result = dict(status='PASS', reproduced_byte_for_byte=expected,
                  input_hashes_verified=len(inputs['files']), summaries=summaries,
                  cross_comparison=review['coordinator_comparison'],
                  reproduce_script_sha256=digest(Path(__file__)),
                  scope='Only the proved 216-cell / M<=91 reduction, 174 derived failures and 54 archived configurations; no extra trial.')
    (HERE/'REPRODUCTION.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS', exact_outputs=4,
                         cross_comparison=result['cross_comparison']), sort_keys=True))


if __name__ == '__main__':
    main()
