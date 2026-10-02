#!/usr/bin/env python3
"""Exact same-threshold transfer; explicitly reuses reviewed geometry/physics.

Only physical controls q=3,4,10. Full fixed geometry is independent of q.
No original proof package is modified. Standard library, assertions enabled.
"""
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FROZEN_HEAD = 'a9a9c2746bd39740888ecd4ae48ed8f5d47b4dcd'
REVIEW = ROOT / 'reviews/2026-09-29-cc-other-ray-review'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


g = load_module('reviewed_geometry', REVIEW / 'geometry_check.py')
phy = load_module('reviewed_physics', REVIEW / 'physical_check.py')
ROWS = g.ROWS


def add_band(vertices, constraints, row_index, lap):
    a, b = ROWS[row_index]
    v, c = g.clip(vertices, constraints,
                  g.constraint(f'{row_index}.lower', (-a, -b, 1), -lap))
    if v:
        v, c = g.clip(v, c,
                      g.constraint(f'{row_index}.upper', (a, b, 1), lap + 1))
    return v, c


def record(labels, vertices, constraints):
    return {'labels': labels, 'dimension': g.dimension(vertices),
            'vertices': vertices, 'edges': g.face_edges(vertices, constraints),
            'constraints': constraints, 'maximum_z': max(v[2] for v in vertices)}


def face_dimension(point, parent):
    active = [c[1] for c in parent['constraints'] if g.slack(c, point) == 0]
    return 3 - g.rank(active)


def build():
    v, c = g.seed()
    branches = [((0, 0), v, c)]
    for i, (a, b) in enumerate(ROWS[2:6], 2):
        new = []
        for labels, v, c in branches:
            for lap in range(a + b):
                w, d = add_band(v, c, i, lap)
                if w:
                    new.append((labels + (lap,), w, d))
        branches = new
    parents = [record(*b) for b in branches]
    children, maps = [], []
    for parent_index, p in enumerate(parents):
        mapping = {'parent_index': parent_index, 'labels': p['labels'],
                   'child_indices': [], 'empty_seventh_laps': []}
        for lap in range(7):
            v, c = add_band(p['vertices'], p['constraints'], 6, lap)
            if not v:
                mapping['empty_seventh_laps'].append(lap)
                continue
            child = record(p['labels'] + (lap,), v, c)
            child['parent_index'] = parent_index
            child['unchanged_parent'] = set(v) == set(p['vertices'])
            child['vertex_parent_face_dimensions'] = [face_dimension(w, p) for w in v]
            child['edge_parent_face_dimensions'] = [
                face_dimension(tuple((v[i][k] + v[j][k]) / 2 for k in range(3)), p)
                for i, j in child['edges']]
            child['new_vertex_indices'] = [i for i, w in enumerate(v) if w not in p['vertices']]
            mapping['child_indices'].append(len(children))
            children.append(child)
        maps.append(mapping)
    return parents, children, maps


def old_child_comparison(children):
    path = ROOT / 'reviews/2026-09-29-ltcm-spectrum/ambient.json'
    old = {tuple(c['m']): c for c in json.loads(path.read_text())}
    assert set(old) == {c['labels'] for c in children}
    for c in children:
        previous = old[c['labels']]
        vertices = [tuple(map(Q, v)) for v in previous['vertices']]
        assert set(vertices) == set(c['vertices'])
        prior_edges = {tuple(sorted((vertices[i], vertices[j]))) for i, j in previous['edges']}
        new_edges = {tuple(sorted((c['vertices'][i], c['vertices'][j]))) for i, j in c['edges']}
        assert prior_edges == new_edges
    return {'all_child_labels_vertices_edges_match': True, 'cells': len(children)}


def ceil(q):
    return -((-q.numerator) // q.denominator)


def H(point, q):
    return q * point[0] - point[1]


def S(point):
    return 5 * point[0] + 2 * point[1]


def slice_candidates(cell, q):
    """Exhaust edge/integer-plane crossings for the three bounded controls."""
    v = cell['vertices']
    points = {p for p in v if H(p, q).denominator == 1}
    for i, j in cell['edges']:
        a, b = v[i], v[j]
        ha, hb = H(a, q), H(b, q)
        if ha == hb:
            continue  # endpoints already cover a compatible constant-H edge
        lo, hi = sorted((ha, hb))
        for h in range(ceil(lo), hi.numerator // hi.denominator + 1):
            lam = (h - ha) / (hb - ha)
            points.add(tuple(x + lam * (y - x) for x, y in zip(a, b)))
    return points


def physical_point(t, q, z):
    assert 0 <= t <= Q(1, 2)
    y = q * t - (q * t).numerator // (q * t).denominator
    return (t, y, z)


def containing_cell(point, cells):
    matches = [i for i, c in enumerate(cells)
               if all(g.slack(inequality, point) >= 0 for inequality in c['constraints'])]
    assert len(matches) == 1
    return matches[0]


def physical_controls(parents, children):
    archive_path = ROOT / 'reviews/2026-09-29-ltcm-ultra-review/physical_check.json'
    archive = {r['q']: r for r in json.loads(archive_path.read_text())['small_q_results']}
    results = []
    for q in (3, 4, 10):
        speeds = (1, q, q + 1, q + 2, q + 3, 2 * q + 3, 2 * q + 5)
        outputs = []
        for size, cells in ((6, parents), (7, children)):
            maximum, components, counts = phy.optimize(speeds[:size])
            bands, _ = phy.threshold_set(speeds[:size], maximum)
            assert bands == components
            assert all(a == b for a, b in components)
            candidates = set().union(*(slice_candidates(c, q) for c in cells))
            assert candidates and max(p[2] for p in candidates) == maximum
            folded = sorted({p[0] for p in candidates if p[2] == maximum})
            physical = sorted({t for x in folded for t in (x, 1 - x)})
            times = [a for a, _ in components]
            assert physical == times
            outputs.append({'coordinates': size, 'maximum': maximum,
                            'all_maximizing_times': times,
                            'slice_candidate_count': len(candidates),
                            'threshold_set_matches': True,
                            'physical_optimizer_counts': dict(counts)})
        six, seven = outputs
        old = archive[q]
        assert seven['maximum'] == Q(old['maximum'])
        assert seven['all_maximizing_times'] == sorted(map(Q, old['maximizing_times']))
        old_witnesses = [{'time': t, 'six_value': six['maximum'],
                          'seventh_distance': phy.distance(speeds[-1] * t),
                          'new_value': phy.value(speeds, t)}
                         for t in six['all_maximizing_times']]
        assert all(w['new_value'] < Q(1, 8) for w in old_witnesses)
        origins = []
        for t in seven['all_maximizing_times']:
            if t > Q(1, 2):
                continue
            point = physical_point(t, q, seven['maximum'])
            ci = containing_cell(point, children)
            pi = children[ci]['parent_index']
            p = parents[pi]
            own_slice = [v for v in slice_candidates(p, q) if H(v, q) == H(point, q)]
            assert own_slice
            origins.append({'time': t, 'point': point, 'H': H(point, q),
                            'child_index': ci, 'parent_index': pi,
                            'parent_face_dimension': face_dimension(point, p),
                            'six_value_at_time': phy.value(speeds[:6], t),
                            'six_parent_slice_maximum': max(v[2] for v in own_slice),
                            'seventh_distance': phy.distance(speeds[-1] * t)})
        # Complete same-threshold safe sets, not just maximizers.
        safe6, _ = phy.threshold_set(speeds[:6], Q(1, 8))
        safe7, _ = phy.threshold_set(speeds, Q(1, 8))
        results.append({'q': q, 'speeds': speeds, 'optimization': outputs,
                        'old_global_optimizers_after_addition': old_witnesses,
                        'folded_child_maximizer_origins': origins,
                        'six_safe_components_at_1_over_8': safe6,
                        'seven_safe_components_at_1_over_8': safe7,
                        'archived_seven_result_matches': True})
    return results


def marginal_failure(parents, children):
    """One fixed declared q=4 section; no search for a favorable example."""
    p = parents[2]
    assert p['labels'] == (0, 0, 0, 0, 1, 1)
    base = [v for v in p['vertices'] if v[2] == Q(1, 8)]
    h_range = (min(H(v, 4) for v in base), max(H(v, 4) for v in base))
    s_range = (min(S(v) for v in base), max(S(v) for v in base))
    assert h_range == (Q(5, 8), Q(11, 8))
    assert s_range == (Q(23, 12), Q(17, 8))
    assert h_range[0] <= 1 <= h_range[1]
    assert s_range[1] == 2 + Q(1, 8)
    conditional = sorted(v for v in slice_candidates(p, 4)
                         if v[2] == Q(1, 8) and H(v, 4) == 1)
    assert len(conditional) == 2
    joint_range = (min(S(v) for v in conditional), max(S(v) for v in conditional))
    assert joint_range == (Q(109, 56), Q(33, 16))
    assert joint_range[0] > 1 - Q(1, 8) + 1  # upper end of k=1 safe band
    assert joint_range[1] < 2 + Q(1, 8)      # lower end of k=2 safe band
    descendant = [c for c in children if c['parent_index'] == 2]
    assert len(descendant) == 1 and descendant[0]['dimension'] == 0
    lone = descendant[0]['vertices'][0]
    assert H(lone, 4) == Q(11, 8)
    for v in conditional + [lone]:
        h, s = H(v, 4), S(v)
        assert ((s + 2*h)/13, (4*s - 5*h)/13, v[2]) == v
    return {'q': 4, 'parent_index': 2, 'height': Q(1, 8),
            'marginal_H_range': h_range, 'marginal_S_range': s_range,
            'false_positive_pair': (Q(1), Q(17, 8)),
            'conditional_H': 1, 'conditional_section_endpoints': conditional,
            'conditional_S_range': joint_range,
            'only_child_point': lone, 'child_H': H(lone, 4),
            'conclusion': 'Independent marginal intervals give a false positive; the joint section is necessary.'}


def main():
    parents, children, maps = build()
    comparison = old_child_comparison(children)
    assert len(parents) == 8 and all(p['dimension'] == 3 and len(p['vertices']) == 4 for p in parents)
    assert len(children) == 10
    assert sum(len(c['vertices']) for c in children) == 33
    assert sum(len(c['edges']) for c in children) == 45
    vertex_origins = Counter(d for c in children for d in c['vertex_parent_face_dimensions'])
    edge_origins = Counter(d for c in children for d in c['edge_parent_face_dimensions'])
    all_parent_vertices = {v for p in parents for v in p['vertices']}
    all_child_vertices = {v for c in children for v in c['vertices']}
    removed = sorted(all_parent_vertices - all_child_vertices)
    parent_peaks = {v for p in parents for v in p['vertices'] if v[2] == Q(1, 6)}
    child_peaks = {v for c in children for v in c['vertices'] if v[2] == Q(1, 6)}
    removed_peaks = sorted(parent_peaks - child_peaks)
    assert removed_peaks == [(Q(1, 3), Q(1, 6), Q(1, 6))]
    report = {'status': 'PASS: exact fixed transfer and three bounded physical controls',
              'frozen_head': FROZEN_HEAD, 'rows': ROWS,
              'summary': {'parent_cells': len(parents), 'parent_vertices': sum(len(p['vertices']) for p in parents),
                          'parent_edges': sum(len(p['edges']) for p in parents),
                          'seventh_lap_branches': 56, 'empty_branches': sum(len(m['empty_seventh_laps']) for m in maps),
                          'child_cells': len(children), 'child_vertices': 33, 'child_edges': 45,
                          'singleton_children': sum(c['dimension'] == 0 for c in children),
                          'unchanged_parent_cells': sum(c['unchanged_parent'] for c in children),
                          'split_parents': sum(len(m['child_indices']) > 1 for m in maps),
                          'new_child_vertices': len(all_child_vertices - all_parent_vertices),
                          'removed_parent_vertices': len(removed),
                          'vertex_parent_face_dimensions': dict(vertex_origins),
                          'edge_parent_face_dimensions': dict(edge_origins)},
              'parent_child_map': maps, 'parents': parents, 'children': children,
              'removed_parent_vertices': removed, 'removed_parent_peaks': removed_peaks,
              'archived_child_comparison': comparison,
              'physical_controls': physical_controls(parents, children),
              'marginal_projection_counterexample': marginal_failure(parents, children),
              'provenance': 'Coordinator reuses reviewed geometry clipping and tent-envelope implementations; not independent authorship.',
              'input_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in
                              (REVIEW/'geometry_check.py', REVIEW/'physical_check.py',
                               ROOT/'reviews/2026-09-29-ltcm-spectrum/ambient.json',
                               ROOT/'reviews/2026-09-29-ltcm-ultra-review/physical_check.json')},
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(g.encode(report), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
