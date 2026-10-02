#!/usr/bin/env python3
"""Reproduce only the frozen finite/residue reductions and physical controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((HERE/name).read_text())


def compare():
    own, other = read('classification.json'), read('algebra_review.json')
    assert own['W_rows'] == sorted([c['A'], c['B']] for c in other['W_rows'])
    independent = {(c['A'], c['B']): c for c in other['W_complete_finite_domain']}
    assert len(independent) == len(own['W_complete_finite_domain']) == 147
    for case in own['W_complete_finite_domain']:
        matched = independent[tuple(case['row'])]
        for kind in ('L', 'F', 'C'):
            assert case[kind+'_safe'] == matched[kind]['safe']
            assert case[kind+'_lap'] == matched[kind]['lap']
        for kind in ('W', 'R'):
            assert case[kind] == matched[kind]
    residues = {(c['delta'], c['B_mod8']): c['representative']['R']
                for c in other['R_complete_13_by_8']}
    assert len(residues) == len(own['R_complete_13_by_8']) == 104
    for case in own['R_complete_13_by_8']:
        assert case['R'] == residues[(case['delta'], case['B_mod8'])]
    assert own['R_accepted_B_residues_by_delta'] == other['R_accepted_B_residues_by_delta']
    own, other = read('witnesses.json'), read('physical_review.json')
    counts = {}
    for group in ('progression_controls', 'negative_controls'):
        ours, theirs = own[group], other[group]
        assert len(ours) == len(theirs)
        n = 0
        for a, b in zip(ours, theirs):
            for key in a.keys() & b.keys():
                assert a[key] == b[key], (group, a['row'], a['pair'], key)
                n += 1
        counts[group+'_shared_fields'] = n
    for key in own['counts']:
        assert own['counts'][key] == other['counts'][key]
    return dict(finite_rows=147, residue_cells=104, W_rows=31, R_classes=42,
                shared_count_fields=len(own['counts']), **counts)


def main():
    if not __debug__:
        raise RuntimeError('Run without -O; exact checks use assertions')
    inputs = read('INPUTS.json')
    for name, record in inputs['files'].items():
        assert digest(ROOT/name) == record['sha256'], name
    assert digest(HERE/'PROTOCOL.md') == inputs['protocol_sha256']
    names = ('classification.json', 'witnesses.json', 'algebra_review.json', 'physical_review.json')
    expected = {name: digest(HERE/name) for name in names}
    for stem in ('classify', 'algebra_review', 'physical_review'):
        subprocess.run([sys.executable, str(HERE/(stem+'.py'))], check=True,
                       capture_output=True, text=True)
    for name in names:
        assert digest(HERE/name) == expected[name], name
    comparison = compare()
    result = dict(status='PASS', reproduced_byte_for_byte=expected,
                  input_hashes_verified=len(inputs['files']),
                  cross_comparison=comparison,
                  reproduce_script_sha256=digest(Path(__file__)),
                  scope='Complete proved reductions only; 54 frozen progression configurations and two negative physical controls; no new trials.')
    (HERE/'REPRODUCTION.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS', exact_outputs=len(names), comparison=comparison), sort_keys=True))


if __name__ == '__main__':
    main()
