"""Independent exact interval-set and Kruskal verification of the selector.

No project imports. Strict endpoints are represented explicitly. State masses
come from interval intersections and Boolean inversion, not a state sweep.
Full feasible sets and core components come from threshold vertices/cells.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'relationship_selector.json'
OUT = HERE / 'relationship_selector_crosscheck.json'
PROTOCOL_SHA = '0e2d4a37dcd2c0276ca8d7dd68938d1bfe7bdbf1a32012a19a8ac15e39ae7dfb'
DELTA = Q(1, 8)


def near(v, t):
    z = v*t
    k = z.numerator % z.denominator
    return Q(min(k, z.denominator-k), z.denominator)


def contains(interval, t):
    a, b, ac, bc = interval
    return (a < t or (a == t and ac)) and (t < b or (t == b and bc))


def meet(left, right):
    out = []
    for p in left:
        for q in right:
            a, b = max(p[0], q[0]), min(p[1], q[1])
            ac, bc = contains(p, a) and contains(q, a), contains(p, b) and contains(q, b)
            if a < b or (a == b and ac and bc):
                out.append((a, b, ac, bc))
    return sorted(out)


def size(intervals):
    return sum((p[1]-p[0] for p in intervals), Q(0))


def blocking(v, window):
    return meet([(Q(8*m-1, 8*v), Q(8*m+1, 8*v), False, False)
                 for m in range(v+1)], [(window[0], window[1], True, True)])


def safe_laps(v, window):
    return meet([(Q(8*m+1, 8*v), Q(8*m+7, 8*v), True, True)
                 for m in range(v)], [(window[0], window[1], True, True)])


def event_points(speeds, window):
    points = set(window)
    for v in speeds:
        points.update(Q(k, 8*v) for k in range(1, 8*v)
                      if k % 8 in (1, 7) and window[0] < Q(k, 8*v) < window[1])
    return sorted(points)


def allowed(speeds, window=(Q(0), Q(1))):
    points = event_points(speeds, window)
    ok = lambda t: all(near(v, t) >= DELTA for v in speeds)
    pieces = [(t, t) for t in points if ok(t)]
    for a, b in zip(points, points[1:]):
        if ok((a+b)/2):
            assert ok(a) and ok(b)
            pieces.append((a, b))
    merged = []
    for a, b in sorted(pieces):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


def encoding(intervals):
    return [[str(a), str(b)] for a, b in intervals]


def kruskal(nodes, singles, pairs, L):
    parent = {i: i for i in nodes}
    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i
    weight = Q(0)
    for i, j in sorted(combinations(nodes, 2), key=lambda e: (-pairs[e], e)):
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
            weight += pairs[i, j]
    return L-sum(singles[i] for i in nodes)+weight


def check_tree(nodes, edges, singles, pairs, L, value):
    assert len(edges) == max(0, len(nodes)-1)
    assert len({tuple(e) for e in edges}) == len(edges)
    assert all(i in nodes and j in nodes and i < j for i, j in edges)
    if nodes:
        reached = {nodes[0]}
        previous = set()
        while reached != previous:
            previous = set(reached)
            for i, j in edges:
                if i in reached or j in reached:
                    reached.update((i, j))
        assert reached == set(nodes)
    assert L-sum(singles[i] for i in nodes)+sum(pairs[tuple(e)] for e in edges) == value


def verify_window(row, speeds):
    W = tuple(map(Q, row['window']))
    L = W[1]-W[0]
    assert Q(row['length']) == L
    residual = [v for v in speeds if v not in row['core']]
    assert row['residual'] == residual
    blocks = [blocking(v, W) for v in residual]
    safes = [safe_laps(v, W) for v in residual]
    vanished = [i for i in range(4) if not blocks[i]]
    edges = [[i, j] for i in range(4) for j in range(4) if i != j and not meet(blocks[i], safes[j])]
    assert row['vanished'] == vanished and row['containment_edges'] == edges
    contained = {(i, j) for i, j in edges} | {(i, i) for i in range(4)}
    # Exhaust candidate representatives instead of constructing a maximal-class DAG.
    candidates = [list(c) for n in range(5) for c in combinations(range(4), n)
                  if all(i in vanished or any((i, j) in contained for j in c) for i in range(4))]
    retained = min(candidates, key=lambda c: (len(c), c))
    assert row['retained'] == retained
    classes = []
    seen = set(vanished)
    for i in range(4):
        if i not in seen:
            group = [j for j in range(4) if j not in vanished and blocks[j] == blocks[i]]
            classes.append(group)
            seen.update(group)
    assert row['equivalence_classes'] == classes
    assert row['removed_cover'] == [[i, min(j for j in retained if (i, j) in contained)]
                                    for i in range(4) if i not in vanished and i not in retained]
    assert len(row['noncontainment_witnesses']) == 12-len(edges)
    for item in row['noncontainment_witnesses']:
        i, j = item['edge']
        t = Q(item['violating_time'])
        assert W[0] <= t <= W[1] and any(contains(p, t) for p in blocks[i])
        assert any(contains(p, t) for p in safes[j])
    assert {tuple(w['edge']) for w in row['noncontainment_witnesses']} == {
        (i, j) for i in range(4) for j in range(4) if i != j and [i, j] not in edges}

    joints = []
    for mask in range(16):
        pieces = [(W[0], W[1], True, True)]
        for i in range(4):
            if mask & (1 << i):
                pieces = meet(pieces, blocks[i])
        joints.append(size(pieces))
    masses = list(joints)
    for bit in range(4):
        for mask in range(16):
            if not mask & (1 << bit):
                masses[mask] -= masses[mask | (1 << bit)]
    assert all(v >= 0 for v in masses) and sum(masses) == L
    assert list(map(Q, row['state_masses'])) == masses
    singles = [joints[1 << i] for i in range(4)]
    pairs = {(i, j): joints[(1 << i) | (1 << j)] for i, j in combinations(range(4), 2)}
    assert row['single_durations'] == list(map(str, singles))
    assert row['pair_durations'] == [str(v) for v in pairs.values()]
    ae = [[i, j] for i in range(4) for j in range(4) if i != j
          and singles[i] == pairs[tuple(sorted((i, j)))]]
    assert row['ae_containment_edges'] == ae

    full = kruskal(list(range(4)), singles, pairs, L)
    reduced = kruskal(retained, singles, pairs, L)
    assert full == reduced == Q(row['full_tree_bound']) == Q(row['reduced_tree_bound'])
    check_tree(list(range(4)), row['full_tree_edges'], singles, pairs, L, full)
    check_tree(retained, row['reduced_tree_edges'], singles, pairs, L, reduced)
    assert row['reduced_moment_count'] == len(retained)*(len(retained)+1)//2
    actual = allowed(speeds, W)
    assert allowed([residual[i] for i in retained], W) == actual
    U = sum((b-a for a, b in actual), Q(0))
    assert encoding(actual) == row['allowed'] and Q(row['actual_duration']) == U == masses[0]
    assert row['status'] == ('positive_duration' if U > 0 else 'contacts_only' if actual else 'empty')
    assert Q(row['tree_slack']) == U-reduced >= 0
    cuts = event_points(residual, W)
    def mask_at(t):
        return sum(1 << i for i in range(4) if any(contains(p, t) for p in blocks[i]))
    assert row['vertices'] == [[str(t), mask_at(t)] for t in cuts]
    assert row['cells'] == [[str(a), str(b), mask_at((a+b)/2)] for a, b in zip(cuts, cuts[1:])]


def geometric_key(row):
    return len(row['retained']), -Q(row['length']), tuple(row['core']), Q(row['window'][0])


def verify_choices(case, rows):
    eligible = [r for r in rows if Q(r['length']) > 0]
    g = sorted(eligible, key=geometric_key)[0]
    q = sorted(eligible, key=lambda r: (-Q(r['reduced_tree_bound']),)+geometric_key(r))[0]
    result = case['selectors']
    for name, selected in [('G', g), ('Q', q)]:
        assert result[name] == dict(window_id=selected['id'], bound=selected['reduced_tree_bound'],
                                    positive=Q(selected['reduced_tree_bound']) > 0)
    if Q(q['reduced_tree_bound']) > 0:
        assert result['witness_source'] == 'positive_reduced_tree' and result['endpoint_checks'] == []
        intervals = allowed([q['residual'][i] for i in q['retained']], tuple(map(Q, q['window'])))
        expected_t = next((a+b)/2 for a, b in intervals if a < b)
    else:
        checks = []
        expected_t = None
        for t in sorted({Q(t) for r in rows for t in r['window']}):
            minimum = min(near(v, t) for v in case['speeds'])
            checks.append(dict(time=str(t), valid=minimum >= DELTA, minimum_distance=str(minimum)))
            if minimum >= DELTA:
                expected_t = t
                break
        assert result['endpoint_checks'] == checks
        assert result['witness_source'] == ('endpoint_fallback' if expected_t is not None else 'inconclusive')
    if expected_t is not None:
        assert Q(result['witness']) == expected_t
        ds = [near(v, expected_t) for v in case['speeds']]
        assert min(ds) >= DELTA
        assert result['witness_distances'] == list(map(str, ds))
        assert result['witness_type'] == ('strict' if min(ds) > DELTA else 'equality')


def collision_groups(rows, level):
    fields = ['core', 'window', 'vanished', 'containment_edges']
    if level != 'map':
        fields.append('single_durations')
    if level == 'map_singles_pairs':
        fields.append('pair_durations')
    used, result = set(), []
    for row in rows:
        if row['id'] in used:
            continue
        group = [r for r in rows if all(r[f] == row[f] for f in fields)]
        used.update(r['id'] for r in group)
        if len(group) < 2:
            continue
        result.append(dict(window_ids=[r['id'] for r in group],
            different_duration=any(r['actual_duration'] != row['actual_duration'] for r in group),
            different_existence=any(bool(r['allowed']) != bool(row['allowed']) for r in group),
            different_status=any(r['status'] != row['status'] for r in group),
            different_allowed_set=any(r['allowed'] != row['allowed'] for r in group)))
    return result


def run():
    raw = (HERE / 'relationship_selector_protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_SHA
    protocol, archive = json.loads(raw), json.loads(SOURCE.read_text())
    assert protocol['reference'] == 0 and protocol['total_runners'] == 8 and protocol['threshold'] == '1/8'
    assert archive['protocol_sha256'] == PROTOCOL_SHA
    assert archive['baseline_commit'] == protocol['baseline_commit']
    assert archive['pairs'] == [list(e) for e in combinations(range(4), 2)]
    assert [c['id'] for c in archive['cases']] == [c['id'] for c in protocol['cases']]
    expected_ids = []
    for case, spec in zip(archive['cases'], protocol['cases']):
        assert all(case[k] == spec[k] for k in ('id', 'x', 'y'))
        assert case['speeds'] == protocol['fixed_speeds']+[case['x'], case['y']]
        assert len(set([0]+case['speeds'])) == 8
        rows = [r for r in archive['windows'] if r['case_id'] == case['id']]
        for core in protocol['cores']:
            core_rows = [r for r in rows if r['core'] == core]
            windows = allowed(core)
            assert [r['window'] for r in core_rows] == encoding(windows)
            for i, row in enumerate(core_rows):
                assert row['component_index'] == i
                expected_id = case['id']+'__'+','.join(map(str, core))+'__'+str(i)
                assert row['id'] == expected_id
                expected_ids.append(expected_id)
                verify_window(row, case['speeds'])
        verify_choices(case, rows)
        full_set = allowed(case['speeds'])
        assert case['global_allowed'] == encoding(full_set)
        assert Q(case['global_duration']) == sum((b-a for a, b in full_set), Q(0))
    rows, cases = archive['windows'], archive['cases']
    assert [r['id'] for r in rows] == expected_ids
    matches = {level: collision_groups(rows, level) for level in ('map', 'map_singles', 'map_singles_pairs')}
    assert matches == archive['matched_summaries']
    counts = dict(configurations=len(cases), windows=len(rows),
        positive_actual_windows=sum(Q(r['actual_duration']) > 0 for r in rows),
        positive_tree_windows=sum(Q(r['reduced_tree_bound']) > 0 for r in rows),
        reduced_count_histogram={str(i): sum(len(r['retained']) == i for r in rows) for i in range(5)},
        reduced_moment_count=sum(r['reduced_moment_count'] for r in rows), unreduced_moment_count=10*len(rows),
        pointwise_ae_map_disagreements=sum(r['containment_edges'] != r['ae_containment_edges'] for r in rows),
        G_positive_cases=sum(c['selectors']['G']['positive'] for c in cases),
        Q_positive_cases=sum(c['selectors']['Q']['positive'] for c in cases),
        Q_endpoint_fallback_cases=sum(c['selectors']['witness_source'] == 'endpoint_fallback' for c in cases),
        matches={level: {field: sum(g[field] for g in groups) for field in
                 ('different_duration', 'different_existence', 'different_status', 'different_allowed_set')}
                 | {'groups': len(groups)} for level, groups in matches.items()})
    assert counts == archive['summary']
    assert counts['windows'] == 80 and counts['Q_positive_cases'] == 4 and counts['G_positive_cases'] == 0
    return dict(status='PASS', protocol_sha256=PROTOCOL_SHA, summary=counts,
        methods=['strict interval intersections with endpoint flags', 'all-subset intersections and Boolean inversion',
                 'exhaustive minimal dominating representative subsets', 'Kruskal maximum trees',
                 'threshold vertices and cells for complete allowed sets', 'direct pairwise summary matching'],
        limits='Five named configurations at reference 0 and two specified cores. No original checker or primary script imported. No general correctness or efficiency claim for selection.')


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
    print('PASS: independent strict-set maps, all 80 reductions, moments, optima, selections, and collisions.')
