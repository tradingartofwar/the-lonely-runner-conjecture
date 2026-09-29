#!/usr/bin/env python3
"""Reproduce runtime validation and independent audit in the frozen scope."""
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
        raise RuntimeError('Run this harness without -O; runtime -O is tested separately.')
    inputs = json.loads((HERE/'INPUTS.json').read_text())
    for path, record in inputs['files'].items():
        assert digest(ROOT/path) == record['sha256'], path
    assert digest(HERE/'PROTOCOL.md') == inputs['protocol_sha256']
    previous = json.loads((HERE/'validation.json').read_text())
    for path, sha in previous['provenance'].items():
        assert digest(ROOT/path) == sha, path
    names = ('validation.json', 'audit.json')
    expected = {name:digest(HERE/name) for name in names}
    for stem in ('validate', 'audit'):
        subprocess.run([sys.executable, str(HERE/(stem+'.py'))],
                       cwd=ROOT, check=True, capture_output=True, text=True)
    for name in names:
        assert digest(HERE/name) == expected[name], name
    audit = json.loads((HERE/'audit.json').read_text())
    out = dict(status='PASS', reproduced_byte_for_byte=expected,
        input_hashes_verified=len(inputs['files']), counts=previous['counts'],
        independent_field_comparisons=audit['total_field_comparisons'],
        runtime_sha256=digest(ROOT/'lonely_runner/cc_coefficients.py'),
        reproduce_script_sha256=digest(Path(__file__)),
        scope='Frozen checker validation only; no added coefficient/physical trial or old-suite claim.')
    (HERE/'REPRODUCTION.json').write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS', exact_outputs=2,
                         independent_field_comparisons=out['independent_field_comparisons']), sort_keys=True))


if __name__ == '__main__':
    main()
