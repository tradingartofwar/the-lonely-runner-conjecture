#!/usr/bin/env python3
"""Independent exact reconstruction of the fixed LTCM polyhedral arrangement.

No original project module or certificate is imported. Construction 1 clips a
three-dimensional vertex representation with every lap-band half-space.
Construction 2 exhausts the 48 global boundary planes using Cramer's rule.
This script evaluates no physical parameter q and performs no speed-family scan.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
from pathlib import Path
import hashlib
import json

A = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_suffix('.json')
# Every constraint is (normal, rhs) with normal dot (x,y,z) <= rhs.
BASE = (((0, 0, -1), F(-1, 8)), ((1, 0, 0), F(1, 2)),
        ((-1, 0, 1), F(0)), ((1, 0, 1), F(1)),
        ((0, -1, 1), F(0)), ((0, 1, 1), F(1)))
BASE_VERTICES = ((F(1, 8), F(1, 8), F(1, 8)),
                 (F(1, 8), F(7, 8), F(1, 8)),
                 (F(1, 2), F(1, 8), F(1, 8)),
                 (F(1, 2), F(7, 8), F(1, 8)),
                 (F(1, 2), F(1, 2), F(1, 2)))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def det(rows):
    return dot(rows[0], cross(rows[1], rows[2]))


def rank(rows):
    nonzero = [tuple(r) for r in rows if any(r)]
    if not nonzero:
        return 0
    first = nonzero[0]
    second = next((r for r in nonzero[1:] if any(cross(first, r))), None)
    if second is None:
        return 1
    n = cross(first, second)
    return 3 if any(dot(n, r) for r in nonzero) else 2


def active(point, inequalities):
    return tuple(i for i, (normal, rhs) in enumerate(inequalities)
                 if dot(normal, point) == rhs)


def clip(vertices, inequalities, inequality):
    """Clip via ALL crossing vertex pairs, then discard nonextreme points.

    All-pairs includes every crossing edge. An intersection is extreme iff the
    complete active constraint normals span R^3. This holds in every dimension.
    """
    normal, rhs = inequality
    values = {p: dot(normal, p) - rhs for p in vertices}
    candidates = {p for p in vertices if values[p] <= 0}
    positive = [p for p in vertices if values[p] > 0]
    negative = [p for p in vertices if values[p] < 0]
    for p in positive:
        for q in negative:
            u = values[p] / (values[p] - values[q])
            candidates.add(tuple(p[i] + u*(q[i]-p[i]) for i in range(3)))
    new_inequalities = inequalities + (inequality,)
    result = tuple(sorted(p for p in candidates
                          if rank([new_inequalities[i][0] for i in active(p, new_inequalities)]) == 3))
    assert all(all(dot(n, p) <= r for n, r in new_inequalities) for p in result)
    return result, new_inequalities


def all_lap_cells():
    states = [((0, 0), tuple(sorted(BASE_VERTICES)), BASE)]
    branch_counts = []
    for a, b in A[2:]:
        next_states = []
        attempted = 0
        for labels, vertices, inequalities in states:
            for m in range(a+b):
                attempted += 1
                lower = ((-a, -b, 1), F(-m))
                upper = ((a, b, 1), F(m+1))
                v, cons = clip(vertices, inequalities, lower)
                v, cons = clip(v, cons, upper)
                if v:
                    next_states.append((labels+(m,), v, cons))
        branch_counts.append({'row': [a, b], 'attempted_bands': attempted,
                              'nonempty_prefixes': len(next_states)})
        states = next_states
    return states, branch_counts


def plane_intersection(triple):
    rows = tuple(n for n, _ in triple)
    denominator = det(rows)
    if denominator == 0:
        return None
    rhs = tuple(r for _, r in triple)
    coordinates = []
    for column in range(3):
        substituted = tuple(tuple(rhs[i] if j == column else rows[i][j]
                                  for j in range(3)) for i in range(3))
        coordinates.append(det(substituted) / denominator)
    return tuple(coordinates)


def global_arrangement():
    # Integral coefficients/rhs avoid any matrix-elimination dependency.
    planes = [((0, 0, 8), F(1)), ((2, 0, 0), F(1))]
    for a, b in A:
        for m in range(a+b):
            planes.append(((a, b, -1), F(m)))
            planes.append(((a, b, 1), F(m+1)))
    assert len(planes) == len(set(planes)) == 48
    vertices_by_label = {}
    counts = Counter()
    for ids in combinations(range(len(planes)), 3):
        counts['triples'] += 1
        p = plane_intersection(tuple(planes[i] for i in ids))
        if p is None:
            counts['singular_triples'] += 1
            continue
        counts['nonsingular_triples'] += 1
        x, y, z = p
        if z < F(1,8) or x > F(1,2):
            continue
        labels = []
        for a, b in A:
            phase = a*x + b*y
            m = phase.numerator // phase.denominator
            if not 0 <= m < a+b or not z <= phase-m <= 1-z:
                break
            labels.append(m)
        if len(labels) != len(A):
            continue
        counts['feasible_triple_occurrences'] += 1
        vertices_by_label.setdefault(tuple(labels), set()).add(p)
    return planes, vertices_by_label, dict(counts)


def cell_record(labels, vertices, inequalities):
    acts = [active(p, inequalities) for p in vertices]
    edges = []
    for i, j in combinations(range(len(vertices)), 2):
        common = sorted(set(acts[i]).intersection(acts[j]))
        if rank([inequalities[k][0] for k in common]) == 2:
            edges.append((i, j))
    dimension = rank([tuple(p[k]-vertices[0][k] for k in range(3)) for p in vertices[1:]])
    facets = set()
    for n, rhs in inequalities:
        ids = tuple(i for i, p in enumerate(vertices) if dot(n, p) == rhs)
        if ids and rank([tuple(vertices[i][k]-vertices[ids[0]][k] for k in range(3))
                         for i in ids[1:]]) == dimension-1:
            facets.add(ids)
    if dimension == 3:
        assert len(vertices)-len(edges)+len(facets) == 2
    return {'label': labels, 'dimension': dimension, 'vertices': vertices,
            'active_constraints': acts, 'constraints': inequalities, 'edges': edges,
            'facets': sorted(facets), 'z_range': (min(p[2] for p in vertices), max(p[2] for p in vertices)),
            'coordinate_ranges': [(min(p[k] for p in vertices), max(p[k] for p in vertices)) for k in range(3)]}


def strings(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): strings(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [strings(v) for v in obj]
    return obj


def main():
    # Check the initial pyramid independently from all its facet triples.
    recovered_base = {p for triple in combinations(BASE, 3)
                      if (p := plane_intersection(triple)) is not None
                      and all(dot(n,p) <= r for n,r in BASE)}
    assert recovered_base == set(BASE_VERTICES)
    states, branches = all_lap_cells()
    planes, global_cells, counts = global_arrangement()
    clipped_cells = {label: set(vertices) for label, vertices, _ in states}
    assert clipped_cells == global_cells
    records = [cell_record(*state) for state in states]
    summary = {'cell_count': len(states), 'dimension_counts': dict(Counter(c['dimension'] for c in records)),
               'vertex_occurrences': sum(len(c['vertices']) for c in records),
               'unique_vertices': len(set(p for c in records for p in c['vertices'])),
               'edge_occurrences': sum(len(c['edges']) for c in records),
               'height_counts': dict(Counter(p[2] for c in records for p in c['vertices'])),
               'global_plane_count': len(planes), 'constructions_agree': True}
    # Comparison is performed only AFTER both independent reconstructions.
    archive_path = ROOT / 'reviews/2026-09-29-ltcm-spectrum/ambient.json'
    archive = json.loads(archive_path.read_text())
    archived_cells = {tuple(c['m']): {tuple(map(F, p)) for p in c['vertices']} for c in archive}
    assert archived_cells == clipped_cells
    archived_edges = {tuple(c['m']): {tuple(sorted((tuple(map(F,c['vertices'][i])),
                                                 tuple(map(F,c['vertices'][j])))))
                                    for i,j in c['edges']} for c in archive}
    recovered_edges = {tuple(c['label']): {tuple(sorted((c['vertices'][i], c['vertices'][j])))
                                          for i,j in c['edges']} for c in records}
    assert archived_edges == recovered_edges
    comparison = {'archive_sha256': hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                  'all_labels_vertices_and_edges_match': True,
                  'archive_used_only_after_reconstruction': True}
    output = {'description': 'Independently authored exact fixed-arrangement review; no physical q scan.',
              'frozen_candidate_commit': '8a967b30fcd73abd814e4c8f7f53f216c4b3f61e',
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'coefficient_rows': A, 'coarse_lap_domains': [list(range(a+b)) for a,b in A],
              'complete_coarse_label_product': 840, 'summary': summary,
              'archive_comparison': comparison,
              'clip_branch_counts': branches, 'global_intersection_counts': counts,
              'global_planes': planes, 'cells': records}
    OUT.write_text(json.dumps(strings(output), indent=2)+'\n')
    print(json.dumps(strings(summary), sort_keys=True))
    print(json.dumps(counts, sort_keys=True))
    print(str(OUT))


if __name__ == '__main__':
    main()
