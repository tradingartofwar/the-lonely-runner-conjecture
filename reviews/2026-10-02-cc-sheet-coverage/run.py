"""Frozen fresh-domain evaluation; never changes a menu after exposure."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import criterion as c

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def save(path, data):
    path.write_text(json.dumps(data, default=c.old.encode, sort_keys=True, separators=(',', ':'))+'\n')


def check(freeze):
    manifest = read(HERE/'MANIFEST.json')
    for name, expected in manifest['sha256'].items():
        raw = (c.ROOT/name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == expected, name
        committed = subprocess.check_output(['git', 'show', f'{freeze}:{name}'], cwd=c.ROOT)
        assert committed == raw, name
    relative = str((HERE/'MANIFEST.json').relative_to(c.ROOT))
    assert subprocess.check_output(['git', 'show', f'{freeze}:{relative}'], cwd=c.ROOT) == (HERE/'MANIFEST.json').read_bytes()
    return manifest


def run(freeze, out):
    manifest = check(freeze)
    out.mkdir(parents=True, exist_ok=True)
    assert not (out/'RESULTS.json').exists(), 'Never overwrite a collected result; use a new reproduction directory.'
    inputs = read(HERE/'VALIDATION_INPUTS.json')
    development = read(HERE/'DEVELOPMENT.json')
    assert inputs['menus']['new7'] == development['new_menu']['indices']
    assert inputs['menus']['new4'] == inputs['menus']['new7'][:4]
    sources = c.old.sources()
    sheets = c.old.objects(sources)['sheets']
    c.COUNTS.clear()
    cases, reasons = [], Counter()
    for triple in inputs['fresh_triples']:
        lat = c.old.lattice(triple)
        decisions = [c.contact(sheet, lat) for sheet in sheets]
        bits = ''.join('1' if d['hit'] else '0' for d in decisions)
        reasons.update(d['reason'] for d in decisions)
        selections = {name: next((i for i in indices if bits[i] == '1'), None)
                      for name, indices in inputs['menus'].items()}
        selections['full36'] = next((i for i, bit in enumerate(bits) if bit == '1'), None)
        witnesses = {str(i): c.old.witness(triple, lat, sheets[i], decisions[i]['hit'], sources)
                     for i in sorted({i for i in selections.values() if i is not None})}
        miss_details = ({str(i): decisions[i] for i in inputs['menus']['new7']}
                        if selections['new7'] is None else {})
        cases.append({'pqr': triple, 'lattice': lat, 'sheet_bits': bits,
                      'selections': selections, 'witnesses': witnesses,
                      'new7_miss_diagnostics': miss_details})
    assert len(cases) == inputs['fresh_count']
    summary = {'status': 'COMPLETED_FROZEN_FINITE_COMPARISON', 'freeze_commit': freeze,
        'fresh_cases': len(cases), 'menus': inputs['menus'],
        'coverage': {name: sum(row['selections'][name] is not None for row in cases)
                     for name in ('legacy4', 'new4', 'new7', 'full36')},
        'misses': {name: [row['pqr'] for row in cases if row['selections'][name] is None]
                   for name in ('legacy4', 'new4', 'new7', 'full36')},
        'by_pair_gcd': {group: {'cases': sum((row['lattice']['d'] == 1) == (group == 'd1') for row in cases),
            'coverage': {name: sum(row['selections'][name] is not None for row in cases
                                   if (row['lattice']['d'] == 1) == (group == 'd1'))
                         for name in ('legacy4', 'new4', 'new7', 'full36')}}
                       for group in ('d1', 'd_at_least_2')},
        'criterion_counts': dict(c.COUNTS), 'criterion_reasons': dict(reasons),
        'comparison_limits': 'Finite deterministic outer box; new selection trained on exposed 407 cases; seven versus four is a size change; no uniform coverage, novelty or runtime claim.'}
    save(out/'RESULTS.json', {'freeze_commit': freeze, 'input_manifest_sha256': hashlib.sha256((HERE/'MANIFEST.json').read_bytes()).hexdigest(),
                            'sources': sources, 'cases': cases, 'summary': summary})
    save(out/'SUMMARY.json', summary)
    print(json.dumps({key: summary[key] for key in ('status', 'fresh_cases', 'coverage', 'by_pair_gcd', 'criterion_counts')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze', required=True)
    parser.add_argument('--out', type=Path, default=HERE/'run')
    args = parser.parse_args()
    run(args.freeze, args.out)
