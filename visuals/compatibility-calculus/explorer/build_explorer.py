#!/usr/bin/env python3
"""Build one offline explorer without modifying the guided presentation."""
import argparse
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    paths = ['data/cc_geometry.json', 'data/cc_examples.json', 'data/visual_manifest.json',
             'data/source_hashes.json', 'js/cc-core.js', 'explorer/model.js',
             'explorer/app.js', 'explorer/style.css', 'explorer/template.html',
             'explorer/build_explorer.py']
    inputs = {p: (PACKAGE / p).read_bytes() for p in paths}
    base = json.loads(inputs['data/visual_manifest.json'])
    original = json.loads(inputs['data/cc_examples.json'])
    manifest = {
        'schema_version': 1, 'source_commit': base['source_commit'],
        'repository': base['repository'], 'data_build_sha256': base['data_build_sha256'],
        'domain': {'rays': ['A', 'B'], 'integer_q': [2, 60], 'required_forms': [6, 7],
                   'safe_thresholds': ['1/8', '1/7', '1/6'], 'common_start': True,
                   'reference_speed': 0, 'comparison_floor': '1/8'},
        'status': 'REPRODUCED finite controls; all-q source arguments remain proof candidates',
        'answer_method': 'Enumerate closed integer-orbit sections of the full pinned atlas. Reflect and deduplicate physical times. A-ray one-witness output uses the pinned E1-then-E2 selector.',
        'limits': 'Selected object and hidden display markers do not replace the complete global answer. No new coefficients, arbitrary runner systems or all-q proof.',
        'sources': sorted(set(base['scene_sources'][k] for k in [
            'cap', 'first_hit', 'physical', 'representation_rules', 'joint_derivation',
            'parent_child_geometry', 'parent_child_physical', 'selector_geometry',
            'selector_physical', 'representation_selector'])),
        'input_sha256': {p: digest(b) for p, b in inputs.items()},
    }
    data = {'geometry': json.loads(inputs['data/cc_geometry.json']),
            'examples': {'selector_visual': {'segments': original['selector_visual']['segments']}},
            'manifest': manifest}
    replacements = {
        '/*EXPLORER_CSS*/': inputs['explorer/style.css'].decode(),
        '/*EXPLORER_DATA*/': 'const CC_EXPLORER=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';',
        '/*CC_CORE*/': inputs['js/cc-core.js'].decode(),
        '/*EXPLORER_MODEL*/': inputs['explorer/model.js'].decode(),
        '/*EXPLORER_APP*/': inputs['explorer/app.js'].decode(),
    }
    html = inputs['explorer/template.html'].decode()
    for marker, content in replacements.items():
        assert html.count(marker) == 1, marker
        html = html.replace(marker, content)
    manifest['explorer_html_sha256'] = digest(html.encode())
    outputs = {'explorer.html': html, 'explorer/manifest.json': json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'}
    for name, text in outputs.items():
        target = PACKAGE / name
        if args.check:
            assert target.read_text() == text, f'Stale output: {name}'
        else:
            target.write_text(text)
    print(('Verified' if args.check else 'Built') + ' offline research explorer; sources ' + base['source_commit'][:12])


if __name__ == '__main__':
    main()
