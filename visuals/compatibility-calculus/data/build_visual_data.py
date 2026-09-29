#!/usr/bin/env python3
"""Deterministic browser data from pinned exact certificates; no prose parsing.

All construction uses Fraction. Floats are rendering conveniences only.
Run from any directory. --check compares outputs without writing them.
"""
import argparse
import hashlib
import json
import re
import subprocess
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parents[1]
PIN = '6b2b9316dbc87499a1cb5184aadbd6614d4d6c32'
REPO = 'https://github.com/tradingartofwar/the-lonely-runner-conjecture'
PREFIX = 'reviews/2026-09-29-'
SOURCES = {
    'geometry': PREFIX + 'cc-other-ray-review/geometry_check.json',
    'caps': PREFIX + 'cc-other-ray-review/reconciliation.json',
    'physical_b': PREFIX + 'cc-other-ray-review/physical_check.json',
    'arithmetic_b': PREFIX + 'cc-other-ray-review/arithmetic_check.json',
    'transfer': PREFIX + 'cc-six-seven-transfer/verification.json',
    'transfer_countercheck': PREFIX + 'cc-six-seven-transfer/countercheck.json',
    'selector': PREFIX + 'cc-bounded-selector/verification.json',
    'selector_countercheck': PREFIX + 'cc-bounded-selector/countercheck.json',
    'original_geometry': PREFIX + 'ltcm-spectrum/ambient.json',
}
NOTES = [
    'AGENTS.md', 'CLAIM_STATUS.md',
    'notes/CC_VISUAL_PRESENTATION_PLAN_2026_09_29.md',
    'notes/CC_REPRESENTATION_RULES.md',
    'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md',
    'notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md',
    'notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md',
    'notes/CC_BOUNDED_SELECTOR_2026_09_29.md',
]
ROWS = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2)]
B_CONTROLS = [2, 3, 4, 5, 6, 7]
A_CONTROLS = [3, 4, 5, 6, 10]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_bytes(path):
    """Keep the visual's mathematical snapshot stable as research continues."""
    return subprocess.check_output(['git', 'show', f'{PIN}:{path}'], cwd=ROOT)


def fraction(value):
    q = F(value)
    return {'num': q.numerator, 'den': q.denominator, 'text': str(q), 'float': float(q)}


def exact(value):
    if isinstance(value, F):
        return fraction(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(?:/\d+)?', value):
        return fraction(value)
    if isinstance(value, (tuple, list)):
        return [exact(v) for v in value]
    if isinstance(value, dict):
        return {k: exact(v) for k, v in value.items()}
    return value


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()


def speeds(ray, q):
    return [1, q, q+1, q+2, q+3, 2*q+3, 2*q+5] if ray == 'A' else [1, q, q+1, 2*q+1, 3*q+1, 3*q+2, 5*q+2]


def witness(ray, q, t):
    runners = []
    for v in speeds(ray, q):
        lap = (v*t).__floor__()
        phase = v*t-lap
        runners.append({'speed': v, 'lap': lap, 'phase': phase, 'distance': min(phase, 1-phase)})
    minimum = min(r['distance'] for r in runners)
    return {'time': t, 'minimum': minimum, 'runners': runners,
            'active_speeds': [r['speed'] for r in runners if r['distance'] == minimum]}


def contact(cap, q):
    p = cap['peak']
    h0 = p[0]-q*p[1]
    directions = [r[0]-q*r[1] for r in cap['rays']]
    low, high = min(directions), max(directions)
    rho = h0-h0.__floor__()
    if rho == 0:
        loss, direction_index, h = F(0), None, int(h0)
    else:
        candidates = [(rho/-low, directions.index(low), h0.__floor__()),
                      ((1-rho)/high, directions.index(high), h0.__ceil__())]
        loss, direction_index, h = min(candidates)
    in_cap = loss <= F(1, 42)
    point = p if direction_index is None else [p[i]+loss*cap['rays'][direction_index][i] for i in range(3)]
    return {'cap': cap['id'], 'cell': cap['cell'], 'h0': h0, 'directions': directions,
            'd_min': low, 'd_max': high, 'rho': rho, 'loss': loss,
            'direction_index': direction_index, 'orbit_integer': h, 'in_cap': in_cap,
            'point': point if in_cap else None,
            'interval': [h0+loss*low, h0+loss*high] if in_cap else None}


def build():
    src = {key: json.loads(source_bytes(path)) for key, path in SOURCES.items()}
    cells, caps = [], []
    for ci, raw in enumerate(src['geometry']['cells']):
        vertices = [list(map(F, v)) for v in raw['vertices']]
        cell = {**raw, 'id': f'C{ci}', 'vertices': vertices,
                'singleton': raw['dimension'] == 0, 'source': SOURCES['geometry']}
        cells.append(cell)
        if not raw['peak_indices']:
            continue
        peak = vertices[raw['peak_indices'][0]]
        rays = [[F(e['alpha']), F(e['beta']), F(-1)] for e in raw['peak_edges']]
        caps.append({'id': chr(65+len(caps)), 'cell': ci, 'peak': peak, 'rays': rays,
                     'labels': raw['labels'], 'cut_loss': F(1, 42),
                     'vertices': [peak] + [[peak[i]+r[i]/42 for i in range(3)] for r in rays],
                     'source': SOURCES['geometry'], 'status': 'REPRODUCED — fixed finite geometry'})
    b_examples = []
    archived_b = {r['q']: r for r in src['physical_b']['exhaustive_results']}
    for q in B_CONTROLS:
        contacts = [contact(c, q) for c in caps]
        loss = min(c['loss'] for c in contacts if c['in_cap'])
        winners = [c for c in contacts if c['in_cap'] and c['loss'] == loss]
        times = sorted({c['point'][1] for c in winners} | {1-c['point'][1] for c in winners})
        assert times == list(map(F, archived_b[q]['claimed_times']))
        assert F(1, 6)-loss == F(archived_b[q]['maximum'])
        b_examples.append({'q': q, 'ray': 'B', 'residue': q % 6, 'speeds': speeds('B', q),
                           'contacts': contacts, 'winner_caps': [c['cap'] for c in winners],
                           'loss': loss, 'maximum': F(1, 6)-loss, 'times': times,
                           'witnesses': [witness('B', q, t) for t in times],
                           'archive': archived_b[q], 'source': SOURCES['physical_b']})
    selector_by_q = {r['certificate']['q']: r for r in src['selector']['physical_controls']}
    a_examples = [{'q': q, 'ray': 'A', 'speeds': speeds('A', q),
                   'selector': selector_by_q[q],
                   'witness': witness('A', q, F(selector_by_q[q]['certificate']['time'])),
                   'transfer': next((r for r in src['transfer']['physical_controls'] if r['q'] == q), None)}
                  for q in A_CONTROLS]
    families = {
        'common': {'total_runners': 8, 'moving_runners': 7, 'reference_speed': 0,
                   'common_start': True, 'closed_threshold': F(1, 8), 'rows': ROWS,
                   'fold': 'If x>1/2, reflect BOTH coordinates (x,y) -> (1-x,1-y).'},
        'A': {'speed_formulas': ['1','q','q+1','q+2','q+3','2q+3','2q+5'],
              'coordinates': 'x={t}, y={qt}', 'orbit': 'h=qx-y in Z', 'clock': 't=x',
              'physical_laps': 'ell_i=m_i+b_i*h', 'coefficient_to_speed_order': [0,1,2,3,4,5,6]},
        'B': {'speed_formulas': ['1','q','q+1','2q+1','3q+1','3q+2','5q+2'],
              'coordinates': 'x={qt}, y={t}', 'orbit': 'h=x-qy in Z', 'clock': 't=y',
              'physical_laps': 'ell_i=m_i-a_i*h; then swap the first two entries',
              'coefficient_to_speed_order': [1,0,2,3,4,5,6]},
        'reflection': 't -> 1-t; ell_i -> v_i-1-ell_i at positive separation',
    }
    geometry = exact({'full_cells': cells, 'top_caps': caps, 'parameter_families': families,
                      'parent_child': {k: src['transfer'][k] for k in ['parents','children','parent_child_map','removed_parent_vertices','summary']},
                      'selectors': {'A': {k: src['selector'][k] for k in ['segments','small_coverage','width_certificate','unbounded_residue_coverage']},
                                    'B': {'formula': 'min(rho/(-d_min),(1-rho)/d_max); zero when h0 is integral',
                                          'source': 'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md'}}})
    examples = exact({'A': a_examples, 'B': b_examples,
                      'marginal_counterexample': src['transfer']['marginal_projection_counterexample'],
                      'q10_face_contact': src['transfer_countercheck']['q10_new_face_contact']})
    hashes = {p: digest(source_bytes(p)) for p in sorted(set(SOURCES.values()) | set(NOTES))}
    implementation_paths = [Path(__file__), PACKAGE/'presentation.template.html', PACKAGE/'css/cc.css',
                            *sorted((PACKAGE/'js').glob('*.js')),
                            PACKAGE/'checks/check_visual_data.py', PACKAGE/'checks/check_browser.cjs']
    source_hashes = {'source_commit': PIN, 'algorithm': 'sha256', 'files': hashes,
                     'implementation_files': {str(p.relative_to(ROOT)): digest(p.read_bytes())
                                              for p in implementation_paths if p.exists()}}
    controls = {'geometry': {'cells':10,'vertices':33,'edges':45,'singletons':3,'caps':7},
                'transfer': {'parents':8,'children':10,'empty_branches':46,'inherited_vertices':27,
                             'new_vertices':6,'removed_vertices':5,'new_face_edges':9},
                'A_q': A_CONTROLS, 'B_q': B_CONTROLS,
                'q4_safe_times': ['1/8','3/8','5/8','7/8'], 'q10_required_times':['17/35','18/35'],
                'selector_fallback': {'q':5,'time':'25/56'},
                'selector_endpoints': {'4':'1/8','6':'5/24'}}
    data_hash = digest(json_bytes({'geometry': geometry, 'examples': examples, 'sources':source_hashes}))
    manifest = {'schema_version':1,'source_commit':PIN,'repository':REPO,'data_build_sha256':data_hash,
                'sources':SOURCES, 'claim_status':{'geometry':'REPRODUCED — exact finite certificate',
                'spectrum':'HYPOTHESIS — internally reviewed proof candidate; independent assessment remains open',
                'rendering':'ILLUSTRATION — animation and floating-point rendering are not proof'},
                'scope': 'Selected stationary reference; eight common-start runners; the fixed A/B families only.',
                'retained':'Full labelled cells including singletons, cap directions, same-point orbit, exact recovery, canonical controls.',
                'omitted_by_first_slice':'Complete 1/8-safe sets, other reference runners, A-ray interactions, parent-child animations.',
                'recovery':'Use the full_cells and parent_child data and the pinned notes before changing threshold, family or requested output.',
                'scene_sources':{'cap':SOURCES['geometry'],'projection':'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md',
                                 'first_hit':'notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md','physical':SOURCES['physical_b']},
                'implementation_scope':'Phase 0 + Phase 1 data and first B-ray visual slice; full deck and explorer remain pending.'}
    return {'cc_geometry.json':geometry,'cc_examples.json':examples,'source_hashes.json':source_hashes,
            'visual_manifest.json':manifest}, controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, controls = build()
    outputs = {PACKAGE/'data'/name:json_bytes(value) for name,value in data.items()}
    outputs[PACKAGE/'checks/expected_controls.json'] = json_bytes(controls)
    template = PACKAGE/'presentation.template.html'
    if template.exists():
        html = template.read_text()
        payload = {'geometry':data['cc_geometry.json'],'examples':data['cc_examples.json'], 'manifest':data['visual_manifest.json']}
        html = html.replace('/* CC_DATA */', 'const CC_DATA = '+json.dumps(payload,ensure_ascii=False).replace('</','<\\/')+';')
        html = html.replace('/* CC_CSS */', (PACKAGE/'css/cc.css').read_text())
        html = html.replace('/* CC_JS */', '\n'.join((PACKAGE/'js'/p).read_text() for p in ['cc-core.js','cc-geometry.js','cc-deck.js']))
        outputs[PACKAGE/'presentation.html'] = html.encode()
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_bytes() != content:
                raise SystemExit(f'Stale generated output: {path.relative_to(ROOT)}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    print(('Verified' if args.check else 'Wrote')+f' {len(outputs)} deterministic outputs; data {data["visual_manifest.json"]["data_build_sha256"][:16]}')


if __name__ == '__main__':
    main()
