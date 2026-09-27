"""Exact pre-specified relationship-map experiment, standard library only.

--write creates the archive; default/--check regenerates and compares read-only.
G and Q read only their declared features. Exact allowed sets are benchmarks.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'relationship_selector_protocol.json'
PROTOCOL_SHA = '0e2d4a37dcd2c0276ca8d7dd68938d1bfe7bdbf1a32012a19a8ac15e39ae7dfb'
OUT = HERE / 'relationship_selector.json'
D = F(1, 8)
PAIRS = list(combinations(range(4), 2))


def distance(z):
    r = z % 1
    return min(r, 1-r)


def intersect(left, right):
    result = []
    for a, b in left:
        for c, d in right:
            lo, hi = max(a, c), min(b, d)
            if lo <= hi:
                result.append((lo, hi))
    return sorted(result)


def feasible(speeds, window=(F(0), F(1))):
    result = [window]
    for v in speeds:
        result = intersect(result, [((m+D)/v, (m+1-D)/v) for m in range(v)])
    return result


def length(pieces):
    return sum((b-a for a, b in pieces), F(0))


def encode(pieces):
    return [[str(a), str(b)] for a, b in pieces]


def decode(pieces):
    return [(F(a), F(b)) for a, b in pieces]


def state_at(speeds, t):
    return sum(1 << i for i, v in enumerate(speeds) if distance(v*t) < D)


def partition(speeds, window):
    a, b = window
    cuts = {a, b}
    for v in speeds:
        for m in range(v):
            for phase in (D, 1-D):
                t = (m+phase)/v
                if a < t < b:
                    cuts.add(t)
    cuts = sorted(cuts)
    vertices = [(t, state_at(speeds, t)) for t in cuts]
    cells = [(lo, hi, state_at(speeds, (lo+hi)/2)) for lo, hi in zip(cuts, cuts[1:])]
    masses = [F(0)]*16
    for lo, hi, mask in cells:
        masses[mask] += hi-lo
    return vertices, cells, masses


def tree_bound(kept, singles, overlaps, L):
    if not kept:
        return L, []
    if len(kept) == 1:
        return L-singles[kept[0]], []
    best = None
    best_edges = None
    for edges in combinations(list(combinations(kept, 2)), len(kept)-1):
        reached = {kept[0]}
        for _ in kept:
            for i, j in edges:
                if i in reached or j in reached:
                    reached.update((i, j))
        if len(reached) != len(kept):
            continue
        value = L-sum(singles[i] for i in kept)+sum(overlaps[e] for e in edges)
        if best is None or value > best:
            best, best_edges = value, edges
    return best, [list(e) for e in best_edges]


def window_record(case, fixed, core, index, window):
    speeds = tuple(fixed)+(case['x'], case['y'])
    residual = tuple(v for v in speeds if v not in core)
    assert len(residual) == 4
    vertices, cells, masses = partition(residual, window)
    probes = vertices + [((a+b)/2, s) for a, b, s in cells]
    support = {s for t, s in probes}
    vanished = [i for i in range(4) if all(not s & (1 << i) for s in support)]
    edges = [(i, j) for i in range(4) for j in range(4) if i != j
             and all(not s & (1 << i) or s & (1 << j) for s in support)]
    edge_set = set(edges)
    groups = []
    remaining = set(range(4))-set(vanished)
    while remaining:
        i = min(remaining)
        group = sorted(j for j in remaining if j == i or ((i, j) in edge_set and (j, i) in edge_set))
        groups.append(group)
        remaining.difference_update(group)
    retained = sorted(g[0] for g in groups if not any(
        (g[0], h[0]) in edge_set for h in groups if g != h))
    covers = [[i, next(j for j in retained if (i, j) in edge_set)]
              for i in range(4) if i not in vanished and i not in retained]
    kept_mask = sum(1 << i for i in retained)
    assert all(bool(s) == bool(s & kept_mask) for s in support)
    nonedges = []
    for i in range(4):
        for j in range(4):
            if i != j and (i, j) not in edge_set:
                t = next(t for t, s in sorted(probes) if s & (1 << i) and not s & (1 << j))
                nonedges.append(dict(edge=[i, j], violating_time=str(t)))
    singles = [sum((masses[s] for s in range(16) if s & (1 << i)), F(0)) for i in range(4)]
    overlaps = {(i, j): sum((masses[s] for s in range(16)
                            if s & (1 << i) and s & (1 << j)), F(0)) for i, j in PAIRS}
    ae_edges = [[i, j] for i in range(4) for j in range(4) if i != j
                and singles[i] == overlaps[tuple(sorted((i, j)))]]
    L = window[1]-window[0]
    full, full_tree = tree_bound(list(range(4)), singles, overlaps, L)
    reduced, reduced_tree = tree_bound(retained, singles, overlaps, L)
    actual_set = feasible(speeds, window)
    actual = length(actual_set)
    assert actual == masses[0] and reduced <= actual and full == reduced
    assert feasible(tuple(residual[i] for i in retained), window) == actual_set
    status = 'positive_duration' if actual > 0 else ('contacts_only' if actual_set else 'empty')
    return dict(id=case['id']+'__'+','.join(map(str, core))+'__'+str(index),
                case_id=case['id'], core=list(core), component_index=index,
                residual=list(residual), window=list(map(str, window)), length=str(L),
                vanished=vanished, containment_edges=[list(e) for e in edges],
                noncontainment_witnesses=nonedges, equivalence_classes=groups,
                retained=retained, removed_cover=covers, ae_containment_edges=ae_edges,
                vertices=[[str(t), s] for t, s in vertices],
                cells=[[str(a), str(b), s] for a, b, s in cells],
                state_masses=list(map(str, masses)), single_durations=list(map(str, singles)),
                pair_durations=[str(overlaps[e]) for e in PAIRS],
                full_tree_edges=full_tree, full_tree_bound=str(full),
                reduced_tree_edges=reduced_tree, reduced_tree_bound=str(reduced),
                reduced_moment_count=len(retained)*(len(retained)+1)//2,
                allowed=encode(actual_set), actual_duration=str(actual), status=status,
                tree_slack=str(actual-reduced))


def geometry_key(row):
    # G reads these declared inputs only; no outcome or quantitative moment.
    return len(row['retained']), -F(row['length']), tuple(row['core']), F(row['window'][0])


def quantitative_key(row):
    return (-F(row['reduced_tree_bound']),)+geometry_key(row)


def choose(rows, speeds):
    candidates = [r for r in rows if F(r['length']) > 0]
    g = min(candidates, key=geometry_key)
    q = min(candidates, key=quantitative_key)
    result = dict(G=dict(window_id=g['id'], bound=g['reduced_tree_bound'],
                         positive=F(g['reduced_tree_bound']) > 0),
                  Q=dict(window_id=q['id'], bound=q['reduced_tree_bound'],
                         positive=F(q['reduced_tree_bound']) > 0))
    if F(q['reduced_tree_bound']) > 0:
        reduced = [q['residual'][i] for i in q['retained']]
        parts = feasible(reduced, tuple(map(F, q['window'])))
        t = next((a+b)/2 for a, b in parts if a < b)
        source = 'positive_reduced_tree'
        endpoint_checks = []
    else:
        endpoints = sorted({F(t) for r in rows for t in r['window']})
        endpoint_checks = []
        t = None
        for candidate in endpoints:
            distances = [distance(v*candidate) for v in speeds]
            ok = min(distances) >= D
            endpoint_checks.append(dict(time=str(candidate), valid=ok,
                                        minimum_distance=str(min(distances))))
            if ok:
                t = candidate
                break
        source = 'endpoint_fallback' if t is not None else 'inconclusive'
    result.update(witness_source=source, endpoint_checks=endpoint_checks)
    if t is not None:
        distances = [distance(v*t) for v in speeds]
        assert min(distances) >= D
        if source == 'positive_reduced_tree':
            assert min(distances) > D
        result.update(witness=str(t), witness_distances=list(map(str, distances)),
                      witness_type='strict' if min(distances) > D else 'equality')
    return result


def matching(rows):
    result = {}
    for level in ('map', 'map_singles', 'map_singles_pairs'):
        buckets = {}
        for row in rows:
            summary = [row['core'], row['window'], row['vanished'], row['containment_edges']]
            if level != 'map':
                summary.append(row['single_durations'])
            if level == 'map_singles_pairs':
                summary.append(row['pair_durations'])
            key = json.dumps(summary, separators=(',', ':'))
            buckets.setdefault(key, []).append(row)
        groups = []
        for group in buckets.values():
            if len(group) < 2:
                continue
            groups.append(dict(window_ids=[r['id'] for r in group],
                different_duration=len({r['actual_duration'] for r in group}) > 1,
                different_existence=len({bool(r['allowed']) for r in group}) > 1,
                different_status=len({r['status'] for r in group}) > 1,
                different_allowed_set=len({json.dumps(r['allowed']) for r in group}) > 1))
        result[level] = groups
    return result


def run():
    raw = PROTOCOL.read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_SHA
    protocol = json.loads(raw)
    fixed = protocol['fixed_speeds']
    cores = [tuple(c) for c in protocol['cores']]
    rows, cases = [], []
    for case in protocol['cases']:
        speeds = tuple(fixed)+(case['x'], case['y'])
        assert len(set((0,)+speeds)) == 8
        local = []
        for core in cores:
            for i, window in enumerate(feasible(core)):
                local.append(window_record(case, fixed, core, i, window))
        decision = choose(local, speeds)
        actual = feasible(speeds)
        cases.append(dict(**case, speeds=list(speeds), selectors=decision,
                          global_allowed=encode(actual), global_duration=str(length(actual))))
        rows.extend(local)
    matches = matching(rows)
    stats = dict(configurations=len(cases), windows=len(rows),
        positive_actual_windows=sum(F(r['actual_duration']) > 0 for r in rows),
        positive_tree_windows=sum(F(r['reduced_tree_bound']) > 0 for r in rows),
        reduced_count_histogram={str(i): sum(len(r['retained']) == i for r in rows) for i in range(5)},
        reduced_moment_count=sum(r['reduced_moment_count'] for r in rows),
        unreduced_moment_count=10*len(rows),
        pointwise_ae_map_disagreements=sum(r['containment_edges'] != r['ae_containment_edges'] for r in rows),
        G_positive_cases=sum(c['selectors']['G']['positive'] for c in cases),
        Q_positive_cases=sum(c['selectors']['Q']['positive'] for c in cases),
        Q_endpoint_fallback_cases=sum(c['selectors']['witness_source'] == 'endpoint_fallback' for c in cases),
        matches={level: {field: sum(g[field] for g in groups) for field in
                 ('different_duration', 'different_existence', 'different_status', 'different_allowed_set')}
                 | {'groups': len(groups)} for level, groups in matches.items()})
    return dict(protocol_sha256=PROTOCOL_SHA, baseline_commit=protocol['baseline_commit'],
                pairs=[list(e) for e in PAIRS], cases=cases, windows=rows,
                matched_summaries=matches, summary=stats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert json.loads(OUT.read_text()) == result
    print(json.dumps(result['summary'], indent=2))
    print('PASS: exact relationship maps, reductions, and fixed selectors.')
